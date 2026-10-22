"""Register sources, resolve questions, or emit a gated answer without an agent."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evidence_gateway.gateway import Gateway, resolve_worker
from evidence_gateway.store import Store, encode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", help="private v2 evidence-store directory")
    commands = parser.add_subparsers(dest="command", required=True)
    register = commands.add_parser(
        "register", help="administratively copy files beneath an allowed root"
    )
    register.add_argument("--root", required=True)
    register.add_argument("--html", required=True)
    register.add_argument("--image", action="append", default=[])
    register.add_argument("--captured-at")
    register.add_argument("--url")
    for name in ("resolve", "answer"):
        commands.add_parser(name, help="read a typed request as JSON from stdin")
    commands.add_parser(
        "verify", help="read certificate_id and proposed_answer as JSON from stdin"
    )
    inspect = commands.add_parser("inspect")
    inspect.add_argument("evidence_id")
    inspect.add_argument("--view", choices=("text", "crop"), default="text")
    inspect.add_argument("--output", help="destination PNG for a crop")
    commands.add_parser("_worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.command == "register":
            result = Store(args.store).register(
                args.root,
                args.html,
                args.image,
                captured_at=args.captured_at,
                url=args.url,
            )
        elif args.command == "_worker":
            result = resolve_worker(Store(args.store), json.load(sys.stdin))
        else:
            gateway = Gateway(args.store)
            if args.command in {"resolve", "answer"}:
                result = getattr(gateway, args.command)(json.load(sys.stdin))
            elif args.command == "verify":
                data = json.load(sys.stdin)
                result = gateway.verify(data["certificate_id"], data["proposed_answer"])
            else:
                result, pixels = gateway.inspect(args.evidence_id, args.view)
                if pixels:
                    if not args.output:
                        raise ValueError("--output is required for a crop")
                    Path(args.output).write_bytes(pixels)
                    result["output"] = args.output
        sys.stdout.buffer.write(encode(result) + b"\n")
    except Exception as error:  # noqa: BLE001 -- serialize failures at the worker/CLI boundary
        if args.command == "_worker":
            sys.stdout.buffer.write(encode({"error": str(error)[:300]}) + b"\n")
        else:
            parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    main()
