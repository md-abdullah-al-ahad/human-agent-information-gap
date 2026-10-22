"""Live acquisition runs only in the gateway's killable worker process."""

from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.request

from .store import MAX_HTML_BYTES, MAX_IMAGE_BYTES, utcnow


class RedirectLimit(urllib.request.HTTPRedirectHandler):
    max_redirections = 3
    max_repeats = 1


def acquire_http(store, source, seconds):
    request = urllib.request.Request(
        source["url"], headers={"User-Agent": "LWA-Web/2.0"}
    )
    opener = urllib.request.build_opener(RedirectLimit())
    try:
        response = opener.open(request, timeout=max(0.1, seconds))
    except urllib.error.HTTPError as error:
        response = error
    with response:
        html = response.read(MAX_HTML_BYTES + 1)
        if len(html) > MAX_HTML_BYTES:
            raise ValueError("HTML response exceeds byte limit")
        return store.ingest(
            html,
            mode="live_http",
            requested_url=source["url"],
            final_url=response.geturl(),
            captured_at=utcnow(),
            http_status=response.status,
            coverage=[
                "initial_html",
                "images_unchecked",
                "hydration_unchecked",
                "interactive_states_unchecked",
            ],
        )


def acquire_browser(store, source, seconds):
    from playwright.sync_api import Error as BrowserError
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        executable = os.environ.get("CHROMIUM_EXECUTABLE") or shutil.which("chromium")
        browser = playwright.chromium.launch(headless=True, executable_path=executable)
        try:
            page = browser.new_page(
                viewport={"width": 1280, "height": 900}, locale="en-US"
            )
            page.set_default_timeout(min(10000, int(seconds * 1000)))
            responses = []
            request_count = 0

            def route_request(route):
                nonlocal request_count
                request_count += 1
                if request_count > 100 or route.request.resource_type in {
                    "media",
                    "font",
                }:
                    route.abort()
                else:
                    route.continue_()

            page.route("**/*", route_request)
            page.on(
                "response",
                lambda r: (
                    responses.append(r)
                    if len(responses) < 8
                    and "json" in r.headers.get("content-type", "")
                    else None
                ),
            )
            response = page.goto(source["url"], wait_until="domcontentloaded")
            page.wait_for_timeout(500)
            geometry = page.evaluate("""() => {
                let i=0; const out=[];
                for (const e of document.querySelectorAll('*')) {
                    const id=String(++i); e.setAttribute('data-lwa-node',id);
                    const r=e.getBoundingClientRect(), s=getComputedStyle(e);
                    const visible=s.display!=='none' && s.visibility!=='hidden' && s.opacity!=='0';
                    e.setAttribute('data-lwa-visible',String(visible));
                    if (visible && r.width>0 && r.height>0 && out.length<6000)
                        out.push({locator:'node:'+id,tag:e.tagName.toLowerCase(),alt:e.getAttribute('alt')||'',parent:e.parentElement?.getAttribute('data-lwa-node'),bbox:[Math.max(0,Math.floor(r.left+scrollX)),Math.max(0,Math.floor(r.top+scrollY)),Math.ceil(r.right+scrollX),Math.ceil(r.bottom+scrollY)]});
                }
                return out;
            }""")
            html = page.content().encode()
            if len(html) > MAX_HTML_BYTES:
                raise ValueError("rendered HTML exceeds byte limit")
            height = min(
                6000,
                page.evaluate(
                    "Math.max(document.documentElement.scrollHeight, innerHeight)"
                ),
            )
            pixels = page.screenshot(
                clip={"x": 0, "y": 0, "width": 1280, "height": height},
                animations="disabled",
            )
            images = (
                [{"bytes": pixels, "role": "rendered_screenshot"}]
                if len(pixels) <= MAX_IMAGE_BYTES
                else []
            )
            network = []
            network_incomplete = False
            for r in responses:
                try:
                    body = r.body()
                    if len(body) <= 500000:
                        network.append(
                            {
                                "url": r.url,
                                "json": json.loads(body),
                                "captured_at": utcnow(),
                            }
                        )
                    else:
                        network_incomplete = True
                except (ValueError, BrowserError):
                    network_incomplete = True
            return store.ingest(
                html,
                images,
                mode="live_browser",
                requested_url=source["url"],
                final_url=page.url,
                captured_at=utcnow(),
                http_status=response.status if response else None,
                geometry=geometry,
                network=network,
                coverage=[
                    "rendered_dom",
                    "viewport_1280x900",
                    "screenshot_height_limited_6000",
                    "hydration_unverified",
                    "interactive_states_unchecked",
                    "iframe_content_unchecked",
                ]
                + ([] if images else ["screenshot_byte_limit"])
                + (["passive_json_incomplete"] if network_incomplete else []),
            )
        finally:
            browser.close()
