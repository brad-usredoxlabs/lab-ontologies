#!/usr/bin/env python3
"""One-time migration: fix lab-ontology OBO files for the pronto parser.

- insert import: lines after the description line
- convert `remark:` lines inside [Term]/[Typedef] blocks to `#` comments,
  and when the remark contains a cross-map CURIE, also emit an `xref:` for
  the first CURIE (OBO's cross-mapping mechanism).
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

IMPORTS = [
    "import: ../imports/bfo.obo",
    "import: ../imports/iao.owl",
    "import: ../imports/obi.obo",
    "import: ../imports/uo.obo",
]

CURIE = re.compile(r"\b((?:OBI|LWO|LEQ|UO|BFO|COB|IAO|RO):\d{5,8})\b")


def fix(path: Path) -> None:
    lines = path.read_text().splitlines()
    if any(l.startswith("import: ../imports/bfo.obo") for l in lines):
        print(path, "already has imports; skipping")
        return
    out: list[str] = []
    in_block = False
    for ln in lines:
        if ln.startswith("[Term]") or ln.startswith("[Typedef]"):
            in_block = True
        elif ln == "" and in_block:
            in_block = False
        m = re.match(r"^( *)(?:# )?remark:\s*(.*)$", ln)
        if m and in_block:
            curies = CURIE.findall(m.group(2))
            if curies:
                out.append(f"{m.group(1)}xref: {curies[0]}")
            # prose is dropped: the xref encodes the cross-map, and this
            # pronto parser rejects remark/# lines inside [Term]/[Typedef]
            continue
        if in_block and ln.lstrip().startswith("#"):
            # any other in-block comment is rejected by the parser — drop it
            continue
        out.append(ln)
        if ln.startswith("description:"):
            out.extend(IMPORTS)
    path.write_text("\n".join(out) + "\n")
    print(path, "-> done")


for p in [REPO / "src/lwo/lwo.base.obo", REPO / "src/leq/leq.base.obo"]:
    fix(p)
print("done")
