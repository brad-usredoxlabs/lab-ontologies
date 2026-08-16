#!/usr/bin/env python3
"""OBO structure validation for lab-ontologies.

Checks (per ontology file):
  1. every [Term] has a well-formed, unique id (PREFIX:NNNNNNN)
  2. no id is shared between a [Term] and a [Typedef] in the same file
  3. every [Term] has a name, def, and is_a
  4. every local is_a / range / domain / xref reference resolves
     (local, the sibling ontology, or an import)
  5. no duplicate names within the same ontology
  6. acronym (oboInOwl:id or `remark: oboInOwl:id = X`) <= 17 chars, uppercase
  7. ontology header matches the prefix

Exit code 0 = all pass, 1 = failures.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMPORTS_DIR = REPO / "src" / "imports"
ONTOS = {
    "LWO": REPO / "src" / "lwo" / "lwo.base.obo",
    "LEQ": REPO / "src" / "leq" / "leq.base.obo",
}


def parse_obo(path: Path):
    """Minimal OBO parser -> (terms, typedefs, header)."""
    terms: dict[str, dict] = {}
    typedefs: dict[str, dict] = {}
    header: dict[str, str] = {}
    current: dict | None = None
    kind = None
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[Term]"):
            kind, current = "term", {}
            continue
        if line.startswith("[Typedef]"):
            kind, current = "typedef", {}
            continue
        m = re.match(r"^([\w:/-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if kind is None:
            header[key] = val
            continue
        if current is None:
            continue
        if key in ("id", "name", "def"):
            current[key] = val
        elif key in ("is_a", "domain", "range", "xref", "synonym"):
            current.setdefault(key, []).append(val)
        if key == "id":
            (terms if kind == "term" else typedefs)[val] = current
    return terms, typedefs, header


def import_ids():
    ids = set()
    for f in IMPORTS_DIR.glob("*.obo"):
        for m in re.finditer(r"^[ \t]*id:\s*(\S+)", f.read_text(), re.M):
            ids.add(m.group(1))
    return ids


def main() -> int:
    imp = import_ids()
    # parse all ontologies first so cross-ontology refs (LEQ -> LWO) resolve
    parsed = {p: parse_obo(f) for p, f in ONTOS.items()}
    all_ont_ids: set[str] = set()
    for terms, typedefs, _ in parsed.values():
        all_ont_ids |= set(terms) | set(typedefs)
    resolvable = imp | all_ont_ids

    failures: list[str] = []
    for prefix in ("LWO", "LEQ"):
        path = ONTOS[prefix]
        terms, typedefs, header = parsed[prefix]
        if not path.exists():
            failures.append(f"{prefix}: missing {path}")
            continue
        all_ids: dict[str, str] = {}
        for tid, _t in terms.items():
            if not re.fullmatch(rf"{prefix}:\d{{7}}", tid):
                failures.append(f"{prefix}: bad class id {tid}")
            if tid in all_ids:
                failures.append(f"{prefix}: duplicate id {tid}")
            all_ids[tid] = "class"
        for tid, _t in typedefs.items():
            if not re.fullmatch(rf"{prefix}:\d{{7}}", tid):
                failures.append(f"{prefix}: bad property id {tid}")
            if tid in all_ids:
                failures.append(f"{prefix}: id collision class/property {tid}")
            all_ids[tid] = "property"
        for tid, t in terms.items():
            if "name" not in t:
                failures.append(f"{prefix}: {tid} missing name")
            if "def" not in t:
                failures.append(f"{prefix}: {tid} missing def")
            if "is_a" not in t:
                failures.append(f"{prefix}: {tid} missing is_a")
        refs: set[str] = set()
        for t in list(terms.values()) + list(typedefs.values()):
            for k in ("is_a", "domain", "range", "xref"):
                for r in t.get(k, []):
                    refs.add(r.split()[0].split("!")[0].strip())
        for r in sorted(refs):
            if r not in resolvable:
                failures.append(f"{prefix}: unresolved reference {r}")
        names: dict[str, str] = {}
        for tid, t in terms.items():
            n = t.get("name", "")
            if n in names:
                failures.append(f"{prefix}: duplicate name {n!r} ({names[n]} vs {tid})")
            names[n] = tid
        acr = header.get("oboInOwl:id", "").strip()
        m = re.search(r"oboInOwl:id\s*[=]\s*\"?(\w+)", path.read_text())
        if not acr and m:
            acr = m.group(1)
        if not acr or not acr.isupper() or len(acr) > 17:
            failures.append(f"{prefix}: bad acronym {acr!r}")
        if header.get("ontology") != prefix.lower():
            failures.append(f"{prefix}: ontology header mismatch {header.get('ontology')!r}")
        print(f"{prefix}: {len(terms)} classes, {len(typedefs)} properties, acronym={acr}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for f in failures:
            print("  -", f)
        return 1
    print("\nAll OBO structure checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
