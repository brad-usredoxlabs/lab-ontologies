#!/usr/bin/env python3
"""Allocate the next free id for LWO or LEQ.

Usage:
    python tools/next_id.py LWO        # next class id (00001xx block)
    python tools/next_id.py LWO prop   # next property id (00000xx block)

Prints the id to stdout. Bumps the file's data-version to today if it
changes.
"""
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FILES = {
    "LWO": REPO / "src/lwo/lwo.base.obo",
    "LEQ": REPO / "src/leq/leq.base.obo",
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in FILES:
        print(__doc__)
        return 2
    prefix = sys.argv[1]
    kind = sys.argv[2] if len(sys.argv) > 2 else "class"
    path = FILES[prefix]
    text = path.read_text()

    used = set()
    for m in re.finditer(rf"(?m)^id:\s*{prefix}:(\d{{7}})", text):
        used.add(int(m.group(1)))

    if kind == "prop":
        block = 1
        hi = 100  # 0000001..0000099
    else:
        block = 100  # 00001xx: 0000100..0000999
        hi = 1000
    step = 1

    nxt = block
    while nxt in used and nxt < hi:
        nxt += step
    if nxt >= hi:
        print(f"no free id in {prefix} {kind} block", file=sys.stderr)
        return 1
    print(f"{prefix}:{nxt:07d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
