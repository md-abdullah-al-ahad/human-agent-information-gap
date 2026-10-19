import re
import os

html_path = "data/stage-4/raw/bd-qc02-dom.html"
raw_size = os.path.getsize(html_path)

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print(f"Raw DOM size: {raw_size:,} bytes")

# 1. Strip script tags
no_scripts = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", content, flags=re.IGNORECASE)
print(f"After stripping <script>: {len(no_scripts):,} bytes ({100 - len(no_scripts)/raw_size*100:.1f}% reduction)")

# 2. Strip style tags and link rel=stylesheet
no_styles = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", no_scripts, flags=re.IGNORECASE)
print(f"After stripping <style>: {len(no_styles):,} bytes ({100 - len(no_styles)/raw_size*100:.1f}% reduction)")

# 3. Strip SVG tags (massive icon path data)
no_svg = re.sub(r"<svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>", "[ICON]", no_styles, flags=re.IGNORECASE)
print(f"After stripping <svg>: {len(no_svg):,} bytes ({100 - len(no_svg)/raw_size*100:.1f}% reduction)")

# 4. Strip base64 inline images and long URLs
no_base64 = re.sub(r'data:image\/[^;]+;base64,[^"\']+', '[BASE64_IMAGE]', no_svg)
print(f"After stripping base64: {len(no_base64):,} bytes ({100 - len(no_base64)/raw_size*100:.1f}% reduction)")

# 5. Extract semantic text and interactive elements (text, headings, links, buttons, inputs, images with alt/src)
# Clean whitespace
compressed = re.sub(r'\s+', ' ', no_base64).strip()
print(f"Compressed semantic HTML: {len(compressed):,} bytes ({100 - len(compressed)/raw_size*100:.1f}% reduction)")
