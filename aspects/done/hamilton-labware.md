# hamilton-labware — done

Aspect: Hamilton liquid handler labware (Microlab STAR / STARlet /
VANTAGE) — LWO.

## Findings (researched 2026-08-16)

Sources: local PyLabRobot checkout `resources/hamilton/` (14
constructor files: tip_racks, tip_creators, tip_carriers, troughs,
trough_carriers, tube_carriers, plate_adapters, mfx_modules,
mfx_carriers, decks), the Hamilton Microlab STAR brochure
(info.hamiltoncompany.com/view/449349329/), a Copia Scientific product
page (STAR 96 Multichannel 300 µL Disposable Tip Head), and
DDG/Bing search snippets (Axygen Hamilton-compatible tips, CO-RE II
conductive tips).

- **The aspect's "1000-channel head" is a misnomer.** Hamilton's
  high-channel heads are the **CO-RE 96- and 384-Multi-Probe Heads
  (MPH)** (STAR brochure, verbatim). The "1000" in Hamilton part
  naming is tip *volume* (1000 µL CO-RE tips; PLR
  `hamilton_core_gripper_1000ul_*`). No 1000-channel head exists.
- **Disposable tips** (CO-RE / CO-RE II): 96-tip SBS racks (122.4 x
  82.6 mm, 9 mm pitch) in 10/50/300/1000 µL, with filter variants,
  slim (conductive), ultra-wide (1.55 mm orifice), and nested
  (nestable) forms; **24-position racks (4 x 6 @ 18 mm) for 4000 and
  5000 µL tips** (cat. 184020–184023). The 96-position form is
  LWO:0000145; the 24-position high-volume form is new.
- **Tip carriers** (TIP_CAR_288/384/480 = 3/4/5 x 96-tip racks;
  TIP_CAR_72/96/120 = 3/4/5 x 4–5 mL racks; TIP_CAR_NTR nestable):
  a rack that holds multiple tip racks as one deck unit — a
  genuinely new labware class (no OBI term exists for it).
- **Fixed tips**: already covered by LWO:0000143, whose def names
  the Hamilton fixed tip as its classic form.
- Everything else maps to existing classes: 60/120/200 mL V-bottom
  troughs → LWO:0000118; tube carriers 24/32 → LWO:0000151; 96 PCR
  plate adapter 188182 → LWO:0000193; MFX DWP holders 188229/188042
  → LWO:0000194; MFX P3/L5 module carriers → LWO:0000150.

## Ontology changes

- **LWO:0000139** 24-position tip rack (is_a LWO:0000144) — new;
  24 positions 4 x 6 @ 18 mm, classic form Hamilton 4/5 mL racks.
- **LWO:0000148** multi-tip-rack carrier (is_a LWO:0000150) — new;
  holds 3–5 tip racks as a single deck unit.
- **LWO:0000145** 96-position tip rack — def refined: Hamilton's
  10/50/300/1000 µL SBS racks share the footprint; high-volume
  4000/5000 µL tips use a 24-position rack (some brands' 5000 µL
  use a 48-position rack).
- No OBI xrefs: the import has no tip-rack / carrier / trough
  container term (only OBI:0002488 pipette). No LEQ edits (aspect
  ontology field = lwo; LEQ:0000105 already covers 96/384-channel
  heads).

## Files changed

- `src/lwo/lwo.base.obo` (+2 classes, 1 def refined)
- `tests/class_hierarchy.yaml` (regenerated via tools/build_hierarchy.py)
- `docs/crosswalk.md` (new "Hamilton" section: 13 tip-rack rows,
  8 tip-carrier rows, 10 other-deck-labware rows, correction note)
- `aspects/queue.yaml` (status: done + note)

`bash check.sh`: ALL CHECKS PASSED (76 LWO classes, 14 tests, full
import-closure load).
