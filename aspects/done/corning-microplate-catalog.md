# Aspect: corning-microplate-catalog (done)

## Findings
Researched the Corning (Costar) microplate catalog against Corning's
own product-description PDFs (certs-ecatalog.corning.com, revisions
dated 2026). Three of the aspect's four guesses were wrong:

- **3632** — NOT "clear, round bottom". It is a 96-well **white**
  plate with a clear **flat** bottom, non-treated → LWO:0000128
  (assay plate).
- **3635** — NOT a plain flat PS plate. It is the **UV plate**:
  virgin acrylic walls, fluorinated-chlorinated thermoplastic bottom
  (UV-transmitting) → LWO:0000128.
- **3795** — NOT a "PCR, full skirt" plate. It is a 96-well **round
  bottom** assay plate, clear, 360 uL working/well → LWO:0000128.
- **3798** — NOT "PCR 0.1 ml". It is a 96-well **TC-treated**,
  clear, **round bottom** plate, 360 uL working/well →
  LWO:0000131 (cell culture plate).

Also verified: 3506 (6-well), 3513 (12-well), 3548 (48-well),
3599 (96-well flat CC), 3542 (384-well TC black LV), 3603 (96 TC
black), 3610 (96 TC white), 3615 (96 black ultra-thin clear bottom
imaging), 3797 (round-bottom assay).

## Ontology changes
No new classes — the existing microplate subclasses (LWO:0000126
96-well, 0000127 PCR, 0000128 assay, 0000130 deep-well, 0000131 TC)
cover the whole Corning catalog; bottom geometry / skirt / color /
treatment are data properties (LWO:0000004, 0000010, 0000007), not
classes. Refined defs:

- LWO:0000127 PCR plate — noted 0.1 milliliter as the standard PCR
  format (def range 50-200 uL already covers it).
- LWO:0000128 assay plate — now says flat **or round (U-shaped)**
  bottom, round being the classic cell-based-assay form.
- LWO:0000131 cell culture plate — now says flat or round bottom and
  clear/white/black walls with clear flat or round bottom.

## Files changed
- `src/lwo/lwo.base.obo` (3 defs refined)
- `docs/crosswalk.md` (new "Corning (Costar) — microplate catalog"
  section, 13 product rows + mapping notes)
- `aspects/queue.yaml` (status → done + note)
- `aspects/done/corning-microplate-catalog.md` (this file)

## Verification
`bash check.sh` passes: 3/3 stages (structure lint, oaklib tests,
full import-closure load). No new classes, so tests/class_hierarchy.yaml
unchanged.
