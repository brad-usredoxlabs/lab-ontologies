# agilent-bravo-labware — done

Aspect: Agilent Bravo (and Bravo II) liquid handler models + compatible
tip families (ontology: both).

## Findings (researched 2026-08-16 via Agilent product pages fetched
through a text-extraction proxy, labautowiki, and the local PyLabRobot
repo; web_search backend was down this run — EXA_API_KEY missing)

- **Platform**: Agilent Bravo (G5563AA) / AssayMAP Bravo — compact
  9-position ANSI/SLAS deck robot, fits in a laminar flow hood; accepts
  96-, 384-, and 1536-well plate formats; positive-displacement
  pipetting, 300 nL–250 µL across heads. Developed by Velocity11,
  acquired by Agilent in 2007.
- **Heads** (swappable): 96-channel "LT" large transfer (2–250 µL,
  G5055A), 96-channel "ST" small transfer (0.3–70 µL, G5057A),
  384-channel "ST" (0.3–70 µL, G5056A); AssayMAP heads (e.g. 96AM
  microchromatography).
- **Tips**: disposable, sold only in 96-position (SBS 96) and
  384-position (SBS 384) racks. 96-rack volumes incl. 10/20/30/100/250
  µL (250 µL: 19477-002, sterile 19477-012, wide-bore 19477-032,
  sterile-filtered 19477-022/19477-082); 384-rack volumes 10/30/70 µL
  (30 µL 11484-202, 70 µL 19133-102, conductive/sterile variants
  10734-302 / 11484-302 / 19133-212).
- **On-deck modules**: orbital shaking station (G5431B), vacuum
  filtration station w/ pump (G5432B), on-deck thermal cycler (ODTC).
- **PyLabRobot**: `agilent` dir = labware only (96-well 150 µL plate
  5042-8502, 2-reservoir 144 mL 203852-100); no Bravo robot definition
  (Bravo is OpenTrons-native).

## Ontology changes

- **LEQ:0000105 liquid handler** — def refined: pipette heads "1, 8,
  96, or 384 channels (96- and 384-channel heads being the standard
  high-throughput forms)". No "Bravo" synonym (product line, not a
  concept — brand stays in catalog).
- **LWO:0000137 384-position tip rack** — def refined: classic forms
  now "12.5, 125, 10, 30, and 70 microliter racks" (Bravo 384-tip
  volumes confirmed).
- **LWO:0000145 96-position tip rack** — confirmed sufficient; Bravo
  96-rack volumes (10–250 µL) already within def scope.
- No new classes: every Bravo artifact (instrument, heads, tip racks,
  on-deck shaker/vacuum/thermal modules) maps to existing LEQ/LWO
  terms.

## Files changed

- `src/leq/leq.base.obo` (LEQ:0000105 def)
- `src/lwo/lwo.base.obo` (LWO:0000137 def)
- `docs/crosswalk.md` (new "Agilent — Bravo / AssayMAP Bravo" section:
  instrument + head part numbers, tip part-number table, on-deck module
  mapping, PyLabRobot note)
- `aspects/queue.yaml` (status: done)

`bash check.sh`: ALL CHECKS PASSED (LWO 74 classes / LEQ 107 classes,
14 tests, full import-closure load). No hierarchy changes (no new
classes), so tests/class_hierarchy.yaml untouched.
