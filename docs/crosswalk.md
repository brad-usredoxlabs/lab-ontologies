# Crosswalk: OpenTrons / PyLabRobot labware → LWO

This document maps the two unstructured labware libraries in this stack
(OpenTrons shared-data, pinned at commit `5b51a98`, and PyLabRobot's
`pylabrobot/resources` vendor constructors) onto LWO classes. The
ontology holds the *concepts*; the per-SKU records live in the product
catalog (computable-lab) and reference these classes.

## Layers

1. **LWO (this repo)** — the concept DAG. ~71 classes, stable.
   Answers: *what kind of thing is this?*
2. **Product catalog (computable-lab)** — one record per vendor SKU.
   Answers: *which specific product is this, what are its properties,
   and where can the robot get it?* Each record carries:
   - `ontology_class: LWO:NNNNNNN` — the annotation (GO: gene →
     gene-product analogy)
   - data values via LWO properties (nominal volume, well count,
     bottom geometry, material, sterility, surface treatment, pitch,
     skirt)
   - `opentrons_id` / `pylabrobot_constructor` — executable
     references into the geometry libraries
   - footprint geometry — referenced, never re-stated
3. **Geometry libraries (OT JSON v2, PLR Python)** — executable
   metadata: well centers, volumes, load points. Never ontology.

## Mapping rules

- An OT definition or PLR constructor maps to exactly **one** LWO
  class (the most specific that is true of every member of that
  constructor's family).
- Subtype distinctions that are *application-driven* (e.g. "PCR
  plate" vs "assay plate") map to the LWO subtype only when the
  product line is marketed for that application; otherwise they stay
  at the generic 96-well plate.
- Anything in OT/PLR that has no LWO class gets a row in the
  **gap table** below; the gap table is the work queue for the
  ontology researcher (Phase 5).

## OpenTrons shared-data (98 definitions)

OT definitions live under
`shared-data/labware/definitions/2/<vendor>/<product>.json` in the
OpenTrons `shared-data` repo. Category coverage in LWO:

| OT category (definition name) | LWO class |
|---|---|
| `96-well` (e.g. `96_Well_Aluminized_PCR_Plate`, `96_Well_PCR_Plate_2mL`) | LWO:0000127 PCR plate / LWO:0000126 96-well plate |
| `96-well-tip-rack` | LWO:0000145 96-position tip rack |
| `96-well-deep-well-plate` (1.5 mL, 2 mL, 2.4 mL) | LWO:0000130 deep-well plate |
| `96-well-filter-plate` | LWO:0000129 filter plate |
| `384-well` (e.g. `384_Well_PCR_Plate_120ul`) | LWO:0000132 384-well plate |
| `24-well` / `48-well` / `6-well` | LWO:0000124 / 0000125 / 0000122 |
| `24x1.5mL-tube` / `24x2mL-tube` / `24x15mL-conical-tube` / `24x50mL-conical-tube` / `48x15mL` / `48x50mL` / `24x10mL` / `24x20mL` | LWO:0000151 tube rack (holds LWO:0000103 / LWO:0000104 tubes) |
| `8-tube-strip` / `10-tube-strip` (0.2 mL PCR strips) | LWO:0000106 PCR strip |
| `1mL-trough` / `1L-trough` | LWO:0000118 trough |
| `waste-1L` | LWO:0000119 waste container |
| `aluminum-block-24` / `aluminum-block-96` | LWO:0000135 / LWO:0000136 |
| `plate-lid` / `plate-seal-96` | LWO:0000161 / LWO:0000162 |

## PyLabRobot resources (122 constructors, 27 vendors)

PLR constructors live in `pylabrobot/resources/<vendor>/`. Each
constructor returns a `Liquidware` (a labware instance with wells and
volumes). Coverage by category:

| PLR category (example constructors) | LWO class |
|---|---|
| `nest` tips: `Tip_Rack_1000`, `Tip_Rack_300`, `Tip_Rack_10`, … | LWO:0000145 96-position tip rack |
| `opentrons` tips: `Tiprack_96_1000`, `Tiprack_96_300`, `Tiprack_96_50`, `Tiprack_96_10` | LWO:0000145 96-position tip rack |
| `nest` tubes: `Tubes_15ml`, `Tubes_50ml`, `Tubes_1ml`, `Tubes_2ml` (rack families) | LWO:0000151 tube rack |
| `nest` plates: `Plate_96_2ml`, `Plate_96_120ul`, `Plate_96_500ul` | LWO:0000126 / LWO:0000130 / LWO:0000128 |
| `nest` blocks: `AluBlock_24_1ml`, `AluBlock_96_0.2ml` | LWO:0000135 / LWO:0000136 |
| `nest` reservoirs: `Reservoir_1L`, `Reservoir_500ml` | LWO:0000117 reservoir |
| trash bins (e.g. `nest.Trash_Bin`) | LWO:0000119 waste container |
| `opentrons` deck labware: `TPC`-style plate adapters | LWO:0000193 deck adapter |

## Gap table (as of 2026-08-15)

Items in OT/PLR that need an LWO class before they can be annotated:

| Item | Proposed LWO class (TBD id) |
|---|---|
| OT `universal-lid` (multi-format) | exists: LWO:0000165 universal lid — verify fit |
| OT `8x15mL-conical-tube` (24/48 variants) | tube rack covered; check strip form |
| PLR `nest.PCR_Plate_96` (0.1 mL) | LWO:0000127 PCR plate — confirm |
| PLR `opentrons.96_Well_PCR_Plate_2mL` | LWO:0000127 |
| PLR `nest.Dish_35`, `nest.Dish_60`, `nest.Dish_100` | LWO:0000191 petri dish / LWO:0000192 TC dish |
| PLR `nest.Vial_50mL` | LWO:0000108 vial (add 50 mL range to def?) |
| PLR `opentrons.Plate_Lid` / `Plate_Seal` | LWO:0000161 / LWO:0000162 |
| PLR `nest.Strip_Tubes_0.2ml` | LWO:0000106 PCR strip |
| PLR `opentrons.Tiprack_96_20` (20 uL) | LWO:0000145 — note: LWO def says 10–5000 uL; OK |
| PLR `nest.PCR_Tip_Rack` (strip form, 8-tip strips in rack) | NEW: strip tip rack? — candidate for Phase 5 |
| OT `aluminum-block-96-0.2ml` vs `96-position` | LWO:0000136 — OK |
| PLR `opentrons.Trash_Bin_1L` | LWO:0000119 |

The gap table is the input to the Phase 5 researcher queue.

## Annotation format (computable-lab side)

```yaml
# product-catalog record (computable-lab)
recordId: prod_nest_tiprack_300
name: Nest 96-Position Tip Rack, 300 uL
ontology_class: LWO:0000145
properties:
  nominal_volume: {value: 300, unit: UO:0000101}
  material: polystyrene
  sterility: sterile
references:
  opentrons_id: shared-data/labware/definitions/2/nest/96-Well-Tip-Rack-300uL.json
  pylabrobot: nest.Tip_Rack_300
footprint: {width_mm: 128.0, depth_mm: 85.5, height_mm: 49.0}
```

The `footprint` block is geometry — it belongs to the product record,
not the ontology. LWO describes *what it is*; the catalog says *which
one, and where the robot finds it*.
