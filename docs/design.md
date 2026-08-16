# Design

## Two ontologies, one boundary rule

**LWO (Laboratory Ware Ontology)** — passive physical containers and
consumables: anything you put a sample *into*. Root `LWO:0000100
labware` is a BFO material entity (`BFO:0000040`, the BFO 1.1
numbering OBI 2026 uses) with an `xref:` to OBI:0000967 container.

**LEQ (Lab Equipment Ontology)** — active devices: anything that acts
*on* a sample or labware. Root `LEQ:0000100 lab equipment` is a
COB:0001300 device (inherited via the OBI import).

The boundary: **does it contain, or does it act?** A tip rack
contains tips (LWO); the liquid handler that picks the tips acts
(LEQ). A plate lid seals (LWO); the plate washer that removes it acts
(LEQ). LEQ's `accepts labware` object property (range LWO:0000100)
is the formal link: equipment declares what labware classes it
accepts.

## Why BFO-anchored, OBI-cross-mapped (not OBI-subsumed)

- OBI's container subtree is device-flavored (specimen container,
  glass bottle); labware is a different slice of material entity.
  `is_a OBI:0000967` would inherit OBI's clinical bias.
- OBI's device subtree (609 terms) is the right home for equipment,
  so LEQ grounds there and cross-maps ~85 OBI terms. LWO stands alone
  and cross-maps the ~11 OBI terms that do cover labware (vial,
  glass bottle, microtiter plate, syringe filter, …).
- Cross-mapping via `xref:` keeps both ontologies independently
  publishable and keeps BioPortal's mapping table populated.

## Three-layer architecture (the GO analogy)

| Layer | Where | Answers |
|---|---|---|
| Concept DAG (LWO/LEQ) | this repo, BioPortal | *what kind of thing is this?* |
| Product catalog | computable-lab records | *which specific product, its properties, where the robot finds it* (SKU → class annotation = GO gene→product) |
| Geometry | OT JSON v2 / PLR Python | *executable* metadata (well centers, volumes, load points) — referenced, never ontology |

Roles (computable-lab protocol `labwareRoles` / `instrumentRoles` /
`contextRoles`) bind to these layers via
`src/bindings/computable-lab.yaml` — see
docs/computable-lab-bindings.md.

## Id scheme

`LWO:NNNNNNN` / `LEQ:NNNNNNN`, 7 digits. Properties `00000xx`
(0000001+), classes `00001xx` (0000100 root, then upward). Allocate
with `tools/next_id.py`. Monotonic, never reused.

## Imports (pinned, in src/imports/)

| file | role |
|---|---|
| bfo.obo | root grounding (material entity BFO:0000040) |
| iao.owl | annotation properties (IAO:0000115 def, etc.) |
| uo.obo | units (UO:0000101 µL, UO:0000098 mL, UO:0000016 mm) |
| obi.obo | cross-maps + COB:0001300 device (OBI inlines COB) |

All four are fetched once and committed; `check.sh` validates the
full closure offline.

## Validation gate (check.sh)

1. `tools/validate_obo.py` — OBO structure: id format/uniqueness,
   term/property id separation, def coverage, is_a/xref resolution
   against imports + local, acronym check.
2. `tests/test_lwo.py` (pytest, oaklib/pronto) — both ontologies
   load with imports; every local id has a label; roots grounded
   (LWO→BFO, LEQ→COB); every xref resolves through the import
   closure; no duplicate labels.
3. Full import-closure load for both ontologies.

Any commit must pass all three. The hourly researcher cron
enforces it.

## Parser gotchas (learned the hard way — do not regress)

- **No `remark:` and no comment lines inside `[Term]`/`[Typedef]`
  blocks.** pronto's grammar rejects both (SyntaxError at the line
  after the block opens). Prose goes in the def; `#` comments only
  between blocks.
- **No multi-line block scalars in OBO headers** — `description:`
  must be single-line quoted.
- **`oboInOwl:id`** — pronto doesn't parse it as a header key; keep
  it as a `# oboInOwl:id = LWO` comment between header and first
  block (the BioPortal/oaklib toolchain still picks it up from the
  header `id:` IRI).
- **BFO numbering**: OBI 2026 uses BFO 1.1 ids (material entity =
  BFO:0000040, not BFO:0000002). Match the import you ship.
- **OBI ships 105 obsolete terms** referencing the undeclared
  `ObsoleteProperty` parent — a one-line stub typedef was appended to
  the pinned obi.obo so the import parses.

## Release strategy

- Alpha: IRI base `brad-usredoxlabs.github.io/lab-ontologies/`
  (GitHub Pages placeholder), dated `data-version` headers, dist
  zips via `tools/build_dist.py`.
- 1.0: migrate IRIs to a PURL (or owned domain), re-tag, refresh
  BioPortal version.

## What we deliberately do NOT put in the ontologies

- Brands, SKUs, catalog numbers → product catalog (computable-lab) +
  docs/crosswalk.md rows.
- Footprints, well coordinates, load heights → OT/PLR geometry
  libraries.
- Individuals (named products) → not yet; revisit only if a catalog
  release is wanted.
- Protocol semantics (steps, roles) → computable-lab.
