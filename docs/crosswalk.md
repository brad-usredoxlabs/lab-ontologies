# Crosswalk: OpenTrons / PyLabRobot labware → LWO

This document maps the two unstructured labware libraries in this stack
(OpenTrons shared-data, pinned at commit `5b51a98`, and PyLabRobot's
`pylabrobot/resources` vendor constructors) onto LWO classes. The
ontology holds the *concepts*; the per-SKU records live in the product
catalog (computable-lab) and reference these classes.

## Layers

1. **LWO (this repo)** — the concept DAG. ~74 classes, stable.
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

## PyLabRobot resources (564 constructors, 27 vendor packages)

PLR constructors live in `pylabrobot/resources/<vendor>/`. Each
constructor returns a `Liquidware` (a labware instance with wells and
volumes). Inventory verified against PLR `main` @ `be6becfb8`
(2026-05-22). Coverage by category:

| PLR category (example constructors) | LWO class |
|---|---|
| `opentrons` tips: `opentrons_96_tiprack_1000ul`, `_300ul`, `_10ul`, `_20ul`, `eppendorf_96_tiprack_1000ul_eptips`, `opentrons_96_filtertiprack_*` | LWO:0000145 96-position tip rack (filter variants → LWO:0000142 tip) |
| `nest` trough plates: `nest_1_troughplate_195000uL_Vb`, `nest_1_troughplate_185000uL_Vb`, `nest_8_troughplate_22000uL_Vb`, `nest_12_troughplate_15000uL_Vb` | LWO:0000118 trough (reservoir plate) |
| `nest` deep well: `NEST_96_wellplate_2200uL_Ub` | LWO:0000130 deep-well plate |
| `opentrons` NEST tube racks: `opentrons_24_tuberack_nest_1_5ml_*`, `opentrons_15_tuberack_nest_15ml_conical`, `opentrons_6_tuberack_nest_50ml_conical`, `opentrons_10_tuberack_nest_4x50ml_6x15ml_conical` | LWO:0000151 tube rack |
| `opentrons` NEST alu blocks: `opentrons_24_aluminumblock_nest_*ml_*`, `opentrons_96_aluminumblock_nest_wellplate_100ul` | LWO:0000135 / LWO:0000136 aluminum block |
| `tecan` waste: `Trash_Container`, `Trash_Waste` | LWO:0000119 waste container |
| `opentrons` deck labware: `TPC`-style plate adapters | LWO:0000193 deck adapter |

## Gap table (as of 2026-08-16)

Items in OT/PLR that need an LWO class before they can be annotated:

| Item | Proposed LWO class (TBD id) |
|---|---|
| OT `universal-lid` (multi-format) | exists: LWO:0000165 universal lid — verify fit |
| OT `8x15mL-conical-tube` (24/48 variants) | tube rack covered; check strip form |
| PLR `nest.PCR_Plate_96` (0.1 mL) | does not exist in PLR (verified 2026-08-16); Tecan's `PCR_Plate_96_Well` → LWO:0000127 PCR plate |
| PLR `opentrons.96_Well_PCR_Plate_2mL` | LWO:0000127 |
| PLR `nest.Dish_35`, `nest.Dish_60`, `nest.Dish_100` | do not exist in PLR (verified 2026-08-16); NEST dishes map to LWO:0000191 petri dish / LWO:0000192 TC dish |
| PLR `nest.Vial_50mL` | does not exist in PLR (verified 2026-08-16); a 50 mL vial would map to LWO:0000108 vial (def range 1–20 mL would need widening if used) |
| PLR `opentrons.Plate_Lid` / `Plate_Seal` | LWO:0000161 / LWO:0000162 |
| PLR `nest.Strip_Tubes_0.2ml` | does not exist in PLR (verified 2026-08-16); a 0.2 mL strip would map to LWO:0000106 PCR strip |
| PLR `opentrons.Tiprack_96_20` (20 uL) | actual name `opentrons_96_tiprack_20ul` → LWO:0000145 — note: LWO def says 10–5000 uL; OK |
| PLR `nest.PCR_Tip_Rack` (strip form, 8-tip strips in rack) | does not exist in PLR (verified 2026-08-16; never did, per git pickaxe) — no strip tip rack class added |
| OT `aluminum-block-96-0.2ml` vs `96-position` | LWO:0000136 — OK |
| PLR `opentrons.Trash_Bin_1L` | does not exist in PLR; Tecan `Trash_Container` / `Trash_Waste` → LWO:0000119 |

The gap table is the input to the Phase 5 researcher queue.

## Vendor product rows (brand → LWO class)

Brands and SKUs are catalog data, not ontology classes. These rows
anchor the ontology concepts to real product lines.

### Integra Biosciences GRIPTIPS (Eppendorf) — automation tips

Integra's automation tips are sold in fixed-format racks; the rack
format, not the tip volume, selects the LWO class:

| Integra product (SKU) | Format | LWO class |
|---|---|---|
| GRIPTIPS 12.5 µL, 384 tips/rack (e.g. 6404) | 384-position, 16 x 24, SBS 384 | LWO:0000137 384-position tip rack |
| GRIPTIPS 125 µL, 384 tips/rack (6463), low-retention (6563) | 384-position, 16 x 24, SBS 384 | LWO:0000137 384-position tip rack |
| GRIPTIPS 300 µL, 96 tips/rack (V96 line) | 96-position, 8 x 12, SBS 96 | LWO:0000145 96-position tip rack |
| GRIPTIPS 1250 µL, 96 tips/rack (6445), low-retention (6543) | 96-position, 8 x 12, SBS 96 | LWO:0000145 96-position tip rack |
| GRIPTIPS 5000 µL, 48 tips/rack | 48-position | LWO:0000138 48-position tip rack |
| GRIPTIPS ECO racks (refillable 96- and 384-config, 300/1250 µL, low retention) | 96- or 384-position | LWO:0000145 / LWO:0000137 |
| GRIPTIPS filter variants (any volume) | per format above | LWO:0000142 filtered pipette tip (tip), rack class per format |
| GRIPTIPS low-retention (any volume) | per format above | LWO:0000141 pipette tip (no LWO class for low retention yet) |

Compatibility (Integra): 12.5 µL tips → 2/10/12.5/20 µL pipettes and
384-channel heads; 125 µL tips → 50/100/125 µL pipettes, MINI 96,
VIAFLO 96/384 heads; 1250 µL tips → 1000/1250 µL pipettes, MINI 96,
VIAFLO 96/384 heads.

### Eppendorf — robotic tips

| Eppendorf product | Format | LWO class |
|---|---|---|
| eptips for epMotion 96 / 96xl (96-channel heads, up to 1000 µL) | 96-position | LWO:0000145 96-position tip rack |
| eptips for 8-channel heads (8-position strip racks) | 8-position strip | LWO:0000144 tip rack (no 8-position class yet) |
| eptips reusable tip box (reusable, not disposable) | box of reusable tips | LWO:0000144 tip rack — def says consumable; see gap note |
| CombITips advanced (single/8-channel manual) | single or 8-strip | LWO:0000141 pipette tip |

Notes:
- Eppendorf's 96-channel heads (epMotion 96, 96xl, and robot
  96-channel modules) use 96-position SBS racks — covered by
  LWO:0000145.
- OBI has no "pipette tip" class (only OBI:0002488 pipette, the
  device), so LWO tip classes carry no OBI xref.

### Agilent — Bravo / AssayMAP Bravo liquid handler + tips

The Bravo (G5563AA; AssayMAP Bravo for high-throughput screening) is
the reference 96/384-channel deck robot: a 9-position ANSI/SLAS deck
that accepts 96-, 384-, and 1536-well plate formats. Developed by
Velocity11, acquired by Agilent in 2007. The instrument itself
annotates as **LEQ:0000105 liquid handler** (OBI:0400112); "Bravo" is
a product line, not an ontology class.

Heads (swappable; LEQ:0000105 def now lists 1/8/96/384 channels):
96-channel "LT" large-transfer (2–250 µL, G5055A), 96-channel "ST"
small-transfer (0.3–70 µL, G5057A), 384-channel "ST" (0.3–70 µL,
G5056A). AssayMAP heads (e.g. 96AM) cover chromatography.

Tips — sold in SBS 96- and 384-position racks only; the rack format
selects the LWO class:

| Agilent Bravo product (part no.) | Format | LWO class |
|---|---|---|
| Disposable tips, 10/20/30/100/250 µL, 96 in rack (250 µL: 19477-002; sterile 19477-012) | 96-position, 8 x 12, SBS 96 | LWO:0000145 96-position tip rack |
| Disposable tips, wide-bore 250 µL, 96 in rack (19477-032 / 19477-072) | 96-position, SBS 96 | LWO:0000145 96-position tip rack |
| Disposable tips, sterile filtered 250 µL, 96 in rack (19477-022 / 19477-082) | 96-position, SBS 96 | LWO:0000142 filtered pipette tip (tip), rack LWO:0000145 |
| Disposable tips, 10/30/70 µL, 384 in rack (30 µL: 11484-202; 70 µL: 19133-102), incl. conductive and sterile variants (10734-302, 11484-302, 19133-212) | 384-position, 16 x 24, SBS 384 | LWO:0000137 384-position tip rack |

Optional on-deck modules (LEQ classes already exist): orbital shaking
station (G5431B) → LEQ:0000120 plate shaker; vacuum filtration
station w/ pump (G5432B) → LEQ:0000126 vacuum manifold; on-deck
thermal cycler (ODTC) → LEQ:0000106 thermal cycler.

Notes:
- Bravo tip racks are the canonical SBS 96 / SBS 384 rack instances —
  LWO:0000145 and LWO:0000137 as defined are exactly the Bravo form
  (no new class needed).
- PyLabRobot's `agilent` resource directory holds only labware
  (96-well 150 µL plate 5042-8502, 2-reservoir 144 mL 203852-100 →
  LWO:0000126 / LWO:0000117), no Bravo robot definition; the Bravo is
  an OpenTrons-native instrument.

### Corning (Costar) — microplate catalog

All facts below verified against Corning's own product-description
PDFs (certs-ecatalog.corning.com, revisions dated 2026). Catalog
numbers are catalog data — the LWO class is selected by the plate
concept, and bottom geometry / skirt / treatment are data values on
the LWO:0000004 / LWO:0000010 / LWO:0000007 properties (no new LWO
classes needed for the Corning lines).

| Corning (Costar) catalog no. | Verified description | LWO class |
|---|---|---|
| 3506 | 6-well cell culture plate, flat bottom, with lid, 5 mL working/well | LWO:0000122 6-well plate |
| 3513 | 12-well cell culture plate, flat bottom, with lid, 3 mL working/well | LWO:0000123 12-well plate |
| 3548 | 48-well cell culture plate, flat bottom, with lid, 1 mL working/well | LWO:0000125 48-well plate |
| 3599 | 96-well cell culture plate, flat bottom, with lid | LWO:0000126 96-well plate |
| 3542 | 384-well low-volume TC-treated black plate, clear flat bottom, with lid, 50 µL total/well | LWO:0000132 384-well plate (TC variant → LWO:0000131 treatment property) |
| 3603 | 96-well TC-treated **black** plate, clear flat bottom, low-evaporation lid | LWO:0000131 cell culture plate |
| 3610 | 96-well TC-treated **white** plate, clear flat bottom, low-evaporation lid | LWO:0000131 cell culture plate |
| 3615 | 96-well black plate with ultra-thin clear bottom, non-treated (imaging) | LWO:0000128 assay plate |
| 3632 | 96-well **white** plate with clear **flat** bottom, non-treated (aspect said "clear, round bottom" — wrong) | LWO:0000128 assay plate |
| 3635 | 96-well UV plate: virgin acrylic walls, fluorinated-chlorinated thermoplastic bottom (aspect said "flat" PS — it is the UV-transmitting line) | LWO:0000128 assay plate |
| 3795 | 96-well assay plate, **round bottom**, clear, non-treated, 360 µL working/well (aspect said "PCR, full skirt" — wrong; it is not a 0.1 mL cycler plate) | LWO:0000128 assay plate |
| 3797 | 96-well assay plate, medium binding, **round bottom**, clear, 360 µL working/well | LWO:0000128 assay plate |
| 3798 | 96-well **TC-treated**, clear, **round bottom**, 360 µL working/well (aspect said "PCR 0.1 mL" — wrong) | LWO:0000131 cell culture plate |
| deep-well 96 lines (1 / 2 / 2.4 mL; catalog numbers not in the current ecatalog PDF set) | deep, narrow 96-well plates for storage/reagent prep | LWO:0000130 deep-well plate |
| 0.1 mL 96-well PCR plates (full skirt, flat bottom, thermal cycler) | the canonical PCR format — maps to LWO:0000127; note 3795/3798 are *not* this line | LWO:0000127 PCR plate |

Notes:
- Corning distinguishes plates by bottom geometry (flat vs round),
  wall color (clear/white/black), and surface treatment (non-treated
  vs TC-treated); all three dimensions are LWO data properties
  (LWO:0000004 bottom geometry, LWO:0000007 surface treatment), not
  separate classes. The existing microplate subclasses (LWO:0000126
  96-well, LWO:0000127 PCR, LWO:0000128 assay, LWO:0000130 deep-well,
  LWO:0000131 TC) are sufficient for the whole catalog.
- The 96-well Corning assay lines are ~0.36 mL working volume,
  inside the LWO:0000128 def range (100–500 µL); the 0.1 mL PCR
  format sits inside LWO:0000127's 50–200 µL range.

### NEST (cell-nest / NEST Scientific) — SBS trough plates + deep-well

Inventory verified against PLR `main` @ `be6becfb8` and NEST's own
Reservoir datasheet (cell-nest.oss-cn-zhangjiakou.aliyuncs.com, the
URL cited in the PLR constructor docstrings). **Important correction:**
the `resources/nest/` PLR module contains only these five constructors
(4 trough plates + 1 deep-well plate) — the earlier crosswalk rows
referencing `nest.Tip_Rack_*`, `nest.Tubes_*`, `nest.AluBlock_*`,
`nest.Reservoir_*`, `nest.Trash_Bin` never existed in PLR (verified by
`git log --all -S` pickaxe over the module's full history). NEST
*branded* tube racks and aluminum blocks are modeled under
`resources/opentrons/tube_racks.py` (`opentrons_24_tuberack_nest_*`,
`opentrons_24_aluminumblock_nest_*`). NEST's own tip line (吸头系列,
96-position SBS racks, 10–1000 µL) is sold by NEST Scientific but has
no PLR constructor; when catalogued it maps to LWO:0000145 as with any
SBS 96 tip rack.

| NEST product (cat. no.) | Verified description | LWO class |
|---|---|---|
| 360101 | Reservoir, multi-well, 8-channel trough, high profile, 22 mL, no cap, non-sterile, PP, ANSI/SBS, −80 °C / DMSO compatible | LWO:0000118 trough |
| 360102 | Reservoir, multi-well, 12-channel trough, high profile, 14 mL, no cap, non-sterile, PP, ANSI/SBS | LWO:0000118 trough |
| 360103 | Reservoir, single well, 96-channel trough, high profile, 195 mL, no cap, non-sterile (one shared container fed through 96 holes) | LWO:0000117 reservoir |
| 360104 | Reservoir, single well, 384-channel trough, high profile, 185 mL, no cap, non-sterile (one shared container fed through 384 holes) | LWO:0000117 reservoir |
| 503062 | 96-well deep-well plate, 2.2 mL/well, U-bottom | LWO:0000130 deep-well plate |
| NEST 24/15/6/10-position tube racks (0.5/1.5/2 mL snap- or screw-cap, 15/50 mL conical) | PLR: `opentrons_24_tuberack_nest_*`, `opentrons_15_tuberack_nest_15ml_conical`, `opentrons_6_tuberack_nest_50ml_conical`, `opentrons_10_tuberack_nest_4x50ml_6x15ml_conical` | LWO:0000151 tube rack |
| NEST 24-position aluminum blocks (0.5/1.5/2 mL) + 96-position 100 µL block | PLR: `opentrons_24_aluminumblock_nest_*`, `opentrons_96_aluminumblock_nest_wellplate_100ul` | LWO:0000135 / LWO:0000136 |

Notes:
- The single-well 185/195 mL trough plates are one continuous
  container under a 96- or 384-hole SBS lid pattern — LWO:0000117
  (reservoir) covers them; the 8/12-channel split troughs are
  LWO:0000118 (trough). No new LWO class is needed for any of the
  NEST line.
- OBI has no trough/reservoir container term, so no OBI xref applies.

### Hamilton — Microlab STAR / STARlet / VANTAGE — tips, carriers, troughs

Inventory verified against PLR `resources/hamilton/` (14 constructor
files) and the Hamilton Microlab STAR brochure (info.hamiltoncompany.com/
view/449349329/). **Key correction to the aspect:** there is no
"1000-channel head." Hamilton's high-channel heads are the **CO-RE 96-
and 384-Multi-Probe Heads (MPH)** — the "1000" in Hamilton part naming
refers to tip *volume* (1000 µL CO-RE tips / PLR
`hamilton_core_gripper_1000ul_*`), not channel count. Single-channel
heads (1, 8-channel) use disposable CO-RE tips in SBS racks; the
CO-RE 96/384 MPH load a whole 96- or 384-well plate of tips at once.
Disposable tips and fixed tips both exist: single/8-channel CO-RE heads
take disposable tips, and the classic Hamilton fixed-tip head (the
"core gripper") is the LWO:0000143 form.

**Disposable tip racks** (96-position SBS, 122.4 x 82.6 mm, 9 mm pitch
→ LWO:0000145; high-volume 24-position 4 x 6 @ 18 mm → LWO:0000139):

| Hamilton cat. no. | Verified description | LWO class |
|---|---|---|
| 235900 / 235935 | 96 x 10 µL low-volume tip rack (non- / sterile) | LWO:0000145 96-position tip rack |
| 235936 / 235901 | 96 x 10 µL low-volume tip rack, **with filter** | LWO:0000142 (filtered) — LWO:0000145 rack form |
| 235948 / 235979 / 235829 | 96 x 50 µL tip rack, with filter (clear/non-sterile) | LWO:0000142 — LWO:0000145 rack form |
| 235966 / 235978 | 96 x 50 µL tip rack, no filter | LWO:0000145 96-position tip rack |
| 235947 / 235964 / 235987 | 96 x 50 µL **nested** tip rack (nestable) | LWO:0000145 96-position tip rack |
| 235830 / 235903 / 235938 | 96 x 300 µL standard tip rack, with filter | LWO:0000142 — LWO:0000145 rack form |
| 235834 / 235902 / 235937 | 96 x 300 µL standard tip rack, no filter | LWO:0000145 96-position tip rack |
| 235646 | 96 x 300 µL slim tip rack, with filter (CO-RE II conductive) | LWO:0000142 — LWO:0000145 rack form |
| 235449 | 96 x 300 µL ultra-wide (1.55 mm orifice) tip rack, with filter | LWO:0000142 — LWO:0000145 rack form |
| 235820 / 235905 / 235940 | 96 x 1000 µL high-volume tip rack, with filter | LWO:0000142 — LWO:0000145 rack form |
| 235822 / 235904 / 235939 | 96 x 1000 µL high-volume tip rack, no filter | LWO:0000145 96-position tip rack |
| 184021 / 184023 | 24 x 4 mL tip rack, with filter, landscape (4 x 6 @ 18 mm) | LWO:0000142 — LWO:0000139 24-position tip rack |
| 184020 / 184022 | 24 x 5 mL tip rack, no filter, landscape (4 x 6 @ 18 mm) | LWO:0000139 24-position tip rack |

**Tip carriers** (a rack that holds several tip racks as one deck unit
→ new class LWO:0000148):

| Hamilton part (PLR constructor) | Verified description | LWO class |
|---|---|---|
| TIP_CAR_288 | carrier for 3 x 96-tip racks, portrait | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_384 | carrier for 4 x 96-tip racks, landscape | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_480 | carrier for 5 x 96-tip racks, landscape | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_72_4mlTF | carrier for 3 x 4 mL filter tip racks, portrait | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_96BC | carrier for 4 x 4 mL filter tip racks, landscape | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_120BC_4mlTF | carrier for 5 x 4 mL filter tip racks, landscape | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_120BC_5mlT | carrier for 5 x 5 mL tip racks, landscape | LWO:0000148 multi-tip-rack carrier |
| TIP_CAR_NTR | carrier for 5 nestable tip-rack positions | LWO:0000148 multi-tip-rack carrier |

**Other Hamilton deck labware** (all map to existing LWO classes):

| Hamilton cat. no. / part | Verified description | LWO class |
|---|---|---|
| 56694-01 / -02 | 60 mL self-standing V-bottom trough, with lid (black = conductive) | LWO:0000118 trough |
| 194052 | 120 mL self-standing V-bottom trough, no lid | LWO:0000118 trough |
| 56695-01 / -02 | 200 mL self-standing V-bottom trough, with lid (black = conductive) | LWO:0000118 trough |
| 185436 (Trough_CAR_4R200) | trough carrier, 4 x 200 mL, 2 tracks wide | LWO:0000118 trough (carrier = LWO:0000150 rack) |
| 53646-01 (Trough_CAR_5R60) | trough carrier, 5 x 60 mL, 1 track wide | LWO:0000118 trough (carrier = LWO:0000150 rack) |
| 173400 (Tube_CAR_24) / Tube_CAR_32 | tube carrier, 24- or 32-position | LWO:0000151 tube rack |
| 188182 (Hamilton_96_adapter) | adapter for 96-well PCR plate, plunged (non-SBS footprint) | LWO:0000193 deck adapter |
| 188229 / 188042 (MFX DWP flat / metal-tapped) | MFX deep-well plate holder module | LWO:0000194 plate holder |
| MFX_CAR_P3 / L5 / shaker carriers | MFX deck module carriers (shaker/plate/holder modules) | LWO:0000150 rack (module carrier) |

Notes:
- The 24-position 4/5 mL tip rack is genuinely new to LWO (existing
  LWO:0000138 48-position is a different 48-tip format) — added
  **LWO:0000139**. The multi-tip-rack carrier is also genuinely new —
  added **LWO:0000148** (is_a LWO:0000150 rack).
- CO-RE is a tip-coupling technology/brand line (CO-RE II = newer
  generation), not an ontology concept; it stays in the catalog. The
  fixed-tip head is LWO:0000143.
- No OBI xrefs: OBI's import has no tip-rack / tip-carrier / trough
  container term (only OBI:0002488 pipette), so none apply.

## Annotation format (computable-lab side)

```yaml
# product-catalog record (computable-lab)
recordId: prod_nest_trough_360101
name: NEST 8-Channel Trough Reservoir Plate, 22 mL
ontology_class: LWO:0000118
properties:
  nominal_volume: {value: 22000, unit: UO:0000101}
  material: polypropylene
  sterility: non-sterile
references:
  pylabrobot: nest.nest_8_troughplate_22000uL_Vb
footprint: {width_mm: 127.76, depth_mm: 85.48, height_mm: 31.4}
```

The `footprint` block is geometry — it belongs to the product record,
not the ontology. LWO describes *what it is*; the catalog says *which
one, and where the robot finds it*.
