# Lab Ontologies (LWO + LEQ)

Two small, BFO-grounded OBO ontologies for the wet lab:

- **LWO — Laboratory Ware Ontology** (`src/lwo/lwo.base.obo`): the physical
  containers and consumables — vessels (tubes, vials, bottles, flasks,
  reservoirs), microplates and aluminum blocks, pipette tips and tip
  racks, racks, lids and seals, filters, columns, culture ware.
  Root `LWO:0000100 labware` is a BFO material entity, cross-mapped to
  OBI:0000967 container.

- **LEQ — Lab Equipment Ontology** (`src/leq/leq.base.obo`): the
  powered and mechanical devices — liquid handlers, cyclers,
  centrifuges, plate readers, spectrometers, balances, sequencers,
  mass spec, vortexes, sonicators, shakers, freezers, biosafety
  cabinets, fume hoods, and support infrastructure. Root
  `LEQ:0000100 lab equipment` is an OBI/COB device.

## Why these exist

No active, biology-focused labware/lab-equipment ontology exists
(checked OLS4, OBO Foundry, BioPortal, Bioprotocols on 2026-08-15).
OBI covers the instrument side well (609 terms under `device`) but
almost none of the labware side. The OpenTrons and PyLabRobot
labware catalogs (98 + 122 definitions) have rich geometry data but
no formal categorization. LWO/LEQ provide the stable concept layer;
per-product records (vendor SKUs, properties, robot references) live
in the product catalog (computable-lab) and annotate these classes —
the GO analogy: the ontology is the gene set, the catalog is the
gene-product database, the SKU→class mapping is the annotation.

## Layout

```
lab-ontologies/
├── check.sh                     # validation gate (lint + pytest + closure load)
├── src/
│   ├── imports/                 # pinned: bfo.obo, iao.owl, uo.obo, obi.obo
│   ├── lwo/lwo.base.obo
│   ├── leq/leq.base.obo
│   ├── bindings/computable-lab.yaml
│   └── mappings/                # (reserved for external same_as files)
├── docs/
│   ├── design.md
│   ├── crosswalk.md             # OT 98 + PLR 122 → LWO class mapping
│   ├── obi-gap-analysis.md      # what OBI has vs the 4x we add
│   ├── computable-lab-bindings.md
│   └── bioportal-submission.md
├── aspects/
│   ├── queue.yaml               # hourly researcher cron consumes this
│   └── done/
├── tools/
│   ├── validate_obo.py          # OBO structure lint
│   ├── obi_gap.py               # regenerate OBI gap checklist
│   ├── next_id.py               # allocate the next free LWO/LEQ id
│   └── migrate_xref.py          # (one-time, kept for reference)
├── tests/test_lwo.py            # oaklib structural tests (both ontologies)
└── dist/                        # dated release files (Phase 4)
```

## Develop

```bash
python3 -m venv .venv && .venv/bin/pip install oaklib pytest
./check.sh        # 3-stage gate: structure lint → pytest → full import-closure load
```

`check.sh` is the only gate. It must pass before any commit (and the
hourly researcher cron enforces it).

## Conventions

- IDs: `LWO:NNNNNNN` / `LEQ:NNNNNNN`. Classes in the `00001xx` block,
  properties in the `00000xx` block. Allocate with
  `.venv/bin/python tools/next_id.py LWO`.
- Every `[Term]` needs `name`, `def` (with IAO:0000115-style
  reference), and `is_a` (except the root, which grounds in
  BFO/COB).
- Cross-ontology mapping is via `xref:` lines pointing at the OBI
  (or BFO/UO/COB) id. **No in-block `remark:` or comment lines** —
  the pronto parser rejects them; put prose in the def or a
  `#` comment *between* blocks.
- OBO headers: single-line `description: "..."` only (no block
  scalars). `oboInOwl:id` goes in a `#` comment between blocks.
- BFO numbering: we use the BFO 1.1 numbering that OBI 2026 uses
  (material entity = `BFO:0000040`), not the BFO 2.x renumbering.

## Release

Dated release files land in `dist/` (see `docs/bioportal-submission.md`
for the exact BioPortal form values).
