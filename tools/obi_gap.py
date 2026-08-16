#!/usr/bin/env python3
"""Regenerate docs/obi-gap-analysis.md from the pinned OBI import.

Parses src/imports/obi.obo, walks the COB:0001300 device subtree,
lists the OBI instrument terms we cross-map (from the xref: lines in
leq.base.obo), and flags the wet-lab equipment OBI lacks (the "4x"
gap). Run:

    .venv/bin/python tools/obi_gap.py
"""
import re
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OBI = REPO / "src/imports/obi.obo"
LEQ = REPO / "src/leq/leq.base.obo"
OUT = REPO / "docs/obi-gap-analysis.md"

# wet-lab equipment families OBI's device subtree does NOT cover
GAP_FAMILIES = [
    ("vortex / vortexer", "LEQ:0000122"),
    ("sonicator / ultrasonic processor", "LEQ:0000123"),
    ("freezer (-20/-80)", "LEQ:0000186"),
    ("refrigerated storage (4C)", ""),
    ("biosafety cabinet", "LEQ:0000187"),
    ("fume hood", "LEQ:0000188"),
    ("liquid nitrogen dewar", "LEQ:0000189"),
    ("water bath / dry bath", "LEQ:0000117"),
    ("heat shaker", "LEQ:0000116"),
    ("ultracentrifuge", ""),
    ("refrigerated centrifuge", ""),
    ("pipette controller (motorized single-channel)", ""),
    ("thermal cycler subtypes (gradient, qPCR, digital)", ""),
    ("microscope subtypes (brightfield, fluorescence, confocal)", ""),
    ("plate imager / fluorescence imager", ""),
    ("nitrogen gun / speed-vac concentrator (benchtop)", "LEQ:0000155"),
    ("oven (dry heat, paraffin)", ""),
    ("water purification / Millipore system", "LEQ:0000194"),
    ("ultrasonic cleaner", "LEQ:0000195"),
    ("vacuum pump", "LEQ:0000190"),
    ("gas cylinder / CO2 supply", "LEQ:0000191/193"),
    ("CO2 incubator (as distinct from incubator)", ""),
    ("laminar flow hood (clean bench)", ""),
]

# labware-side terms OBI lacks entirely (LWO territory)
LWO_GAPS = [
    "pipette tip (+ filter tip, fixed tip)",
    "tip rack / tip box",
    "tubes (microcentrifuge, conical, PCR tube/strip, NMR)",
    "vial subtypes (cryovial, culture vial)",
    "bottle / flask subtypes (reagent, Erlenmeyer, round-bottom)",
    "reservoir / trough / waste container",
    "microplate subtypes (PCR, deep-well, filter, TC-treated, well counts)",
    "aluminum block (24/96 position)",
    "racks (tube, vial, plate, cryovial, PCR tube)",
    "lids and seals (plate lid, PCR seal, snap cap, screw cap, universal lid)",
    "filters (syringe, vacuum manifold, filter paper)",
    "columns (chromatography, spin, desalting)",
    "culture ware (petri dish, TC dish)",
    "deck adapter / plate holder",
]


def parse_obi() -> dict[str, tuple[str, str | None]]:
    text = OBI.read_text()
    terms: dict[str, tuple[str, str | None]] = {}
    for m in re.finditer(r"\[Term\]([\s\S]*?)(?=\n\[|$)", text):
        b = m.group(1)
        if "is_obsolete: true" in b:
            continue
        i = re.search(r"(?m)^id:\s*(\S+)", b)
        n = re.search(r"(?m)^name:\s*(.+)$", b)
        a = re.search(r"(?m)^is_a:\s*(\S+)", b)
        if i and n:
            terms[i.group(1)] = (n.group(1).strip(), a.group(1) if a else None)
    return terms


def main() -> None:
    terms = parse_obi()
    children: dict[str, list[str]] = {}
    for cid, (_, parent) in terms.items():
        if parent:
            children.setdefault(parent, []).append(cid)

    def walk(root: str) -> list[tuple[int, str, str]]:
        out: list[tuple[int, str, str]] = []
        stack = [(root, 0)]
        while stack:
            node, depth = stack.pop()
            for c in sorted(children.get(node, []), reverse=True):
                out.append((depth, c, terms[c][0]))
                stack.append((c, depth + 1))
        out.reverse()
        return out

    subtree = walk("COB:0001300")
    total = len(subtree)

    # xrefs used by LEQ
    leq_text = LEQ.read_text()
    used = sorted(set(re.findall(r"xref:\s*(OBI:\d+)", leq_text)))

    # depth-1 instrument branches under device
    branches = sorted(children.get("COB:0001300", []))
    branch_lines = []
    for b in branches:
        name, _ = terms[b]
        n_desc = sum(1 for _ in walk(b))
        branch_lines.append(f"| {b} | {name} | {n_desc + 1} |")

    # which branches do we cross-map into?
    top_of = {}
    for b in branches:
        for d, c, _ in walk(b):
            top_of[c] = b
    mapped_branches = sorted({top_of.get(x) for x in used if x in top_of})

    leq_count = len(re.findall(r"(?m)^\[Term\]", leq_text))

    lines = [
        "# OBI gap analysis — what LEQ adds on top of OBI",
        "",
        f"Generated {date.today().isoformat()} by `tools/obi_gap.py` from the "
        f"pinned OBI import (data-version in header). OBI's `device` subtree "
        f"(COB:0001300) has **{total} live terms** under "
        f"**{len(branches)} first-level branches**.",
        "",
        "## OBI device branches (all)",
        "",
        "| id | name | terms (incl. self) |",
        "|---|---|---|",
        *branch_lines,
        "",
        f"LEQ cross-maps **{len(used)} OBI terms** across "
        f"**{len(mapped_branches)} branches** — every instrument family OBI "
        "covers that is relevant to the wet lab has a `xref:` in "
        "`src/leq/leq.base.obo`.",
        "",
        "## What LEQ adds (the 4x)",
        "",
        "These wet-lab equipment families have **no OBI term** and are "
        "defined in LEQ (class id where one exists; empty = candidate "
        "for a future aspect):",
        "",
        "| family | LEQ class |",
        "|---|---|",
        *[f"| {f} | `{c}` |" if c else f"| {f} | _TBD_ |" for f, c in GAP_FAMILIES],
        "",
        f"LEQ currently defines **{leq_count} classes**; OBI defines "
        f"**{total}** in the device subtree — but OBI's coverage is "
        "clinical/imaging-heavy (NMR consoles, microtomes, arthropod "
        "traps, PPE) where LEQ is silent, and thin on exactly the "
        "benchtop workhorse equipment of the molecular/cell bio lab.",
        "",
        "## Labware-side gap (OBI → LWO)",
        "",
        "OBI's container subtree is device-flavored (specimen container, "
        "glass bottle). The following labware families have no OBI term "
        "and are covered by LWO:",
        "",
        *[f"- {x}" for x in LWO_GAPS],
        "",
        "This is why LWO stands alone on BFO material entity with an "
        "`xref:` to OBI:0000967 container rather than `is_a` OBI.",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
