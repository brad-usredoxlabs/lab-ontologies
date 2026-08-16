# nest-products — Nest (cell-nest / NEST Scientific) products

Status: done (2026-08-16)

## Findings

- **PLR `resources/nest/`** (verified against `main` @ `be6becfb8`,
  2026-05-22; local `nest/plates.py` sha matches upstream) contains
  exactly **5 constructors** — all plates:
  - `nest_1_troughplate_195000uL_Vb` (360103, 195 mL single well)
  - `nest_1_troughplate_185000uL_Vb` (360104, 185 mL single well)
  - `nest_8_troughplate_22000uL_Vb` (360101, 8 × 22 mL)
  - `nest_12_troughplate_15000uL_Vb` (360102, 12 × 15 mL per PLR;
    14 mL per NEST datasheet)
  - `NEST_96_wellplate_2200uL_Ub` (503062, 96-well 2.2 mL U-bottom)
- The crosswalk's `nest.Tip_Rack_*` / `Tubes_*` / `AluBlock_*` /
  `Reservoir_*` / `Trash_Bin` / `PCR_Tip_Rack` constructors **never
  existed** in PLR (`git log --all -S` pickaxe over the module's full
  history returns nothing). NEST-branded tube racks and aluminum
  blocks are modeled under `resources/opentrons/tube_racks.py`.
- NEST's own Reservoir datasheet (fetched from
  cell-nest.oss-cn-zhangjiakou.aliyuncs.com, the URL cited in PLR)
  confirms 360101-360104: PP, ANSI/SBS, non-sterile, −80 °C / DMSO
  compatible, low profile for robotic tips.
- OBI has no trough/reservoir container term → no xref.
- PLR total: 564 constructor functions across 27 vendor packages
  (not "122").

## Changes

- **No new LWO classes** — the whole NEST line maps to existing terms.
- `src/lwo/lwo.base.obo` (data-version → 2026-08-16):
  - LWO:0000117 reservoir: def extended with SBS trough plate forms
    (NEST 360101-360104, 14-22 mL troughs, 185-195 mL single well)
  - LWO:0000118 trough: def extended with 8/12-channel SBS trough
    plate form
  - LWO:0000130 deep-well plate: def notes 2.2 mL U-bottom form
    (NEST 503062)
- `docs/crosswalk.md`:
  - PLR table header corrected (122 → 564 constructors; 27 vendor
    packages) and the 5 false `nest.*` rows replaced with the 5 real
    constructors + opentrons-modeled NEST tube racks / alu blocks
  - new "NEST (cell-nest / NEST Scientific)" vendor section with the
    4 trough catalog numbers + 503062 + NEST tube racks / alu blocks
  - gap table rows corrected (5 `nest.*` items marked "does not exist
    in PLR (verified 2026-08-16)"); `Tiprack_96_20` renamed to the
    real `opentrons_96_tiprack_20ul`
  - annotation-format example now uses a real constructor
    (`nest.nest_8_troughplate_22000uL_Vb`)
- `tests/class_hierarchy.yaml`: regenerated (unchanged — no new classes)

## Files changed

- src/lwo/lwo.base.obo
- docs/crosswalk.md
- aspects/queue.yaml
- aspects/done/nest-products.md

## Verification

`bash check.sh` — 3/3 stages green (structure lint, 14 pytest incl.
hierarchy tests, full import-closure load of LWO + LEQ).

## Note for future aspects

The `hamilton-labware` aspect can rely on `resources/hamilton/`
(tip_racks.py, tip_carriers.py) for the fixed-tip / 1000-channel
form; the "14 hamilton files" claim in the queue is plausible but
should be re-verified the same way (pickaxe + constructor listing).
