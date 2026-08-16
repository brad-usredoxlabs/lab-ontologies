#!/usr/bin/env python3
"""Regenerate tests/class_hierarchy.yaml from the current OBO files.

The hierarchy file is the enforcement mechanism: tests/test_hierarchies.py
asserts that every LWO/LEQ class has an entry here AND that the entry's
parent matches the is_a line in the OBO file. The researcher cron must
update this file when adding a class, or the gate fails.

Run: .venv/bin/python tools/build_hierarchy.py
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "tests/class_hierarchy.yaml"

ONTOS = [
    ("LWO", "LWO", REPO / "src/lwo/lwo.base.obo", "LWO:0000100", "labware"),
    ("LEQ", "LEQ", REPO / "src/leq/leq.base.obo", "LEQ:0000100", "lab equipment"),
]


def parse_classes(path: Path, prefix: str):
    text = path.read_text()
    classes = {}
    cur = None      # current class id (None when not inside a [Term])
    in_term = False
    for line in text.splitlines():
        if line.startswith("[Term]"):
            in_term = True
            cur = None
            continue
        if line.startswith("[Typedef]"):
            in_term = False
            cur = None
            continue
        m = re.match(rf"id: ({prefix}:\d{{7}})", line)
        if m and in_term:
            cur = m.group(1)
            classes[cur] = None
            continue
        m = re.match(r"is_a:\s*((?:LWO|LEQ):\d{7})\b", line)
        if m and cur is not None:
            classes[cur] = m.group(1)
            continue
    return classes


def main() -> None:
    lines = [
        "# Canonical class hierarchy for LWO and LEQ (enforced by tests/test_hierarchies.py).",
        "#",
        "# One entry per class: the parent MUST equal the is_a line in the OBO file.",
        "# When you add a class, add its entry here (parent = the branch or class it",
        "# is_a's), or the gate fails. Regenerate from the OBO files with:",
        "#     .venv/bin/python tools/build_hierarchy.py",
        "",
    ]
    total = 0
    for name, prefix, path, root_id, root_label in ONTOS:
        classes = parse_classes(path, prefix)
        lines.append(f"{name}:")
        lines.append(f"  {root_id}:   # {root_label} (root)")
        for cid in sorted(classes):
            if cid == root_id:
                continue
            parent = classes[cid]
            if parent:
                lines.append(f"  {cid}: {parent}")
            else:
                lines.append(f"  {cid}: # UNPARENTED (is_a points outside LWO/LEQ)")
        total += len(classes)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({total} classes)")


if __name__ == "__main__":
    main()
