# integra-pipette-tips — done

Aspect: Integra / Eppendorf pipette tips for automation (LWO).

## Findings (researched 2026-08-15/16 via vendor/distributor pages)

- **Integra GRIPTIPS automation line** (integraprep.com /
  midlandsci.com / selectscience.net / biocompare):
  - 96 tips/rack (SBS 96, 8 x 12): 300 µL (V96 line), 1250 µL
    (6445/6543), plus 10/20 µL singles-channel lines.
  - 384 tips/rack (SBS 384, 16 x 24): 12.5 µL (6404), 125 µL
    (6463/6563) — used with MINI 96, VIAFLO 96/384 heads.
  - 5000 µL GRIPTIPS are sold in **48-tip racks** (verified from
    shop.integra-biosciences.com product slug "5 racks of 48 tips"),
    *not* 96-position racks.
  - ECO racks: refillable, 96- and 384-config, 300/1250 µL and low
    retention.
  - Variants: non-sterile, pre-sterilized, filter, low-retention;
    all virgin polypropylene, RNase/DNase/pyrogen-free.
- **Eppendorf** (owns Integra; eppendorf.com/us-en, server-rendered):
  - epMotion 96 / 96xl: 96-channel heads, 5–1000 µL, use 96-position
    SBS tip racks (eptips).
  - eptips reusable tip boxes (not disposable) exist.
- **OBI**: no "pipette tip" class (only OBI:0002488 pipette, a
  device) → no xrefs added.

## Ontology changes

- **LWO:0000137** 384-position tip rack (is_a LWO:0000144) — new.
- **LWO:0000138** 48-position tip rack (is_a LWO:0000144) — new.
- **LWO:0000145** 96-position tip rack — def refined: added SBS 96
  9 mm pitch; 5000 µL removed from classic-forms list (it is a
  48-position format); added EXACT synonym "96-channel tip rack".
- Existing LWO:0000141/142/143/144/146/147 confirmed sufficient;
  no brand classes created (brands/SKUs → crosswalk only).

## Files changed

- `src/lwo/lwo.base.obo` (+2 classes, 1 def refined, 1 synonym)
- `tests/class_hierarchy.yaml` (regenerated via tools/build_hierarchy.py)
- `docs/crosswalk.md` (new "Vendor product rows" section: Integra
  GRIPTIPS table with SKUs, Eppendorf eptips/epMotion table, OBI
  gap note)
- `aspects/queue.yaml` (status: done)

`bash check.sh`: ALL CHECKS PASSED (74 LWO classes, 14 tests, full
import-closure load).
