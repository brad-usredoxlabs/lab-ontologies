# vortex-sonicator-shaker-brands — done

Aspect: benchtop vortex / sonicator / shaker product classes
(LEQ). Researched 2026-08-16.

## Research note (method)

`web_search` was **unavailable this run** (EXA_API_KEY missing —
both `web_search` and `web_extract` route through Exa and failed).
Fallback: direct `curl` fetches of vendor and reference pages.
Qsonica's Q700 product page, Wikipedia (Vortex mixer, Shaker
(laboratory), Sonication), and Labnet's product nav fetched cleanly;
Thermo Fisher, Eppendorf, VWR, Scientific Industries, Cell Genomics,
and New Brunswick product pages were blocked/404 — rows based on
them are marked "family name only" in the crosswalk.

## Findings

- **Vortexers** (Wikipedia "Vortex mixer"): off-center rubber cup,
  100–3,200 rpm, 2- or 4-plate formats, continuous or trigger
  (foot/hand) operation; microtube, plate, and large-tube (50 mL)
  forms; a microplate vortexing/incubating variant exists.
  Vendor lines: Scientific Industries Vortex-Genie 2 (4-plate),
  Vortex-Genie 3 (large-tube), Labnet Orbit 300 / Orbit P4
  (microtube + microplate), Thermo Fisher PolyPrep 300/500/600.
- **Sonicators**: two classic forms — **probe** (transducer drives a
  metallic horn immersed in the sample; Qsonica line: Q55, Q125,
  Q500, **Q700 700 W touch-screen**, Q800R high-throughput DNA &
  chromatin shearing, Q2000/Q2500 industrial) and **bath** (liquid
  tank; plates and multi-tube lysis). Qsonica sells ultrasonic
  cleaners as a separate line (same cavitation physics). OBI:0400114
  "sonicator" is defined **probe-only** ("mechanical vibration of a
  metallic probe") — the bath form has no OBI term.
- **Shakers** (Wikipedia "Shaker (laboratory)"): vortex, platform
  (horizontal), orbital (25–500 rpm, low heat → microbial culture),
  incubator/thermal shaker. The **wrist-action shaker**
  (Eppendorf Innova line; New Brunswick also sells Innova
  wrist-action) is the classic reciprocating form for large-flask
  culture at settable amplitudes. Labnet also lists orbital, 3D
  (compound), and reciprocal shakers plus rotators and rocking
  platforms.
- **OBI sweep** (src/imports/obi.obo): only OBI:0001094 plate
  shaker, OBI:0001103 rocker, OBI:0001076 incubator shaker,
  OBI:0400118 vortexer, OBI:0400114 sonicator — no generic shaker,
  orbital, reciprocating, wrist-action, bath sonicator, or
  probe-sonicator term.

## Ontology changes (src/leq/leq.base.obo)

- **LEQ:0000207 probe sonicator** (NEW; is_a LEQ:0000123 sonicator)
  — 50–700 W benchtop classic, Qsonica Q700 as the classic form;
  RELATED synonyms "ultrasonic processor" / "probe ultrasonic
  processor". Genuinely new: OBI's sonicator def is probe-specific,
  so this is the term that best matches OBI:0400114 (xref stays on
  the parent LEQ:0000123, existing style).
- **LEQ:0000122 vortexer** — def expanded (100–3200 rpm;
  microtube / 4-plate / large-tube 50 mL forms); +EXACT "vortex
  shaker".
- **LEQ:0000123 sonicator** — def expanded (probe = immersed horn;
  bath = liquid tank for sealed vessels; explicit boundary vs
  LEQ:0000195 ultrasonic cleaner).
- **LEQ:0000197 orbital shaker** — def expanded (25–500 rpm, low
  heat/vibration, blot washing, microbial culture).
- **LEQ:0000198 reciprocating shaker** — def now names the
  wrist-action form (e.g. Eppendorf Innova) as classic; +EXACT
  "wrist action shaker". No new class: a motion variant, not a new
  device kind.
- **LEQ:0000116 incubator shaker** — +RELATED "thermal shaker"
  (Wikipedia: "incubator shaker (or thermal shaker)").
- data-version → 2026-08-16. LEQ: 107 → 108 classes.

No brand classes (hard rule): Qsonica / Innova / Vortex-Genie /
PolyPrep / Orbit appear only in defs' classic-form phrases and in
docs/crosswalk.md rows.

## Docs

- **docs/crosswalk.md** — new section "Benchtop agitation
  equipment — vortex / sonicator / shaker (brand → LEQ class)":
  vortexer table (5 rows), probe-sonicator table (7 rows incl.
  cleaner line), shaker table (4 rows), plus notes (wrist-action
  folded into reciprocating; 3D-shaker gap noted; OBI gap
  cross-reference; research-method caveat).
- **docs/obi-gap-analysis.md** — unchanged: the aspect's "update TBD
  rows" is a no-op, since the vortex (LEQ:0000122), sonicator
  (LEQ:0000123), and heat shaker (LEQ:0000116) rows were already
  resolved (not _TBD_); GAP_FAMILIES in tools/obi_gap.py untouched.

## Files changed

- src/leq/leq.base.obo (1 new class, 5 refined, data-version)
- tests/class_hierarchy.yaml (regenerated; +LEQ:0000207)
- docs/crosswalk.md (new brand section)
- aspects/queue.yaml (status: done + note)
- aspects/done/vortex-sonicator-shaker-brands.md (this file)
- .hermes/plans/2026-08-16_051307-vortex-sonicator-shaker-brands.md

## Verification

`bash check.sh` — all 3 stages green: structure lint (LEQ 108
classes), pytest 14/14 (incl. hierarchy match + branch rule), full
oaklib import-closure load.
