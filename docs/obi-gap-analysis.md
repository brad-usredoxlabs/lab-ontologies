# OBI gap analysis — what LEQ adds on top of OBI

Generated 2026-08-15 by `tools/obi_gap.py` from the pinned OBI import (data-version in header). OBI's `device` subtree (COB:0001300) has **609 live terms** under **76 first-level branches**.

## OBI device branches (all)

| id | name | terms (incl. self) |
|---|---|---|
| OBI:0000041 | pump valve switch | 1 |
| OBI:0000361 | ion source | 1 |
| OBI:0000394 | blot module | 1 |
| OBI:0000422 | syringe | 1 |
| OBI:0000436 | needle | 2 |
| OBI:0000484 | NMR sample holder | 2 |
| OBI:0000498 | NMR tube washing system | 2 |
| OBI:0000499 | NMR console | 4 |
| OBI:0000517 | NMR magnet | 6 |
| OBI:0000523 | magic angle spinning rotor | 1 |
| OBI:0000544 | Bruker SampleRail system | 1 |
| OBI:0000555 | autosampler | 6 |
| OBI:0000832 | measurement device | 240 |
| OBI:0000932 | material separation device | 92 |
| OBI:0000935 | micromanipulator | 1 |
| OBI:0000955 | electrode puller | 1 |
| OBI:0000967 | container | 40 |
| OBI:0001032 | light emission device | 21 |
| OBI:0001033 | perturbation device | 4 |
| OBI:0001034 | environmental control device | 14 |
| OBI:0001045 | capillary blotter | 1 |
| OBI:0001049 | chip spotting device | 1 |
| OBI:0001054 | PET synthesizer | 1 |
| OBI:0001060 | spot cutter | 1 |
| OBI:0001061 | microwave synthesis system | 1 |
| OBI:0001063 | automatic staining machine | 1 |
| OBI:0001064 | automatic tissue processor | 2 |
| OBI:0001067 | perfusion station | 1 |
| OBI:0001073 | microtome knife maker | 1 |
| OBI:0001074 | cryofixation device | 1 |
| OBI:0001084 | vitrification apparatus | 1 |
| OBI:0001087 | lyophilizer | 1 |
| OBI:0001093 | microtome knife sharpener | 1 |
| OBI:0001094 | plate shaker | 1 |
| OBI:0001103 | rocker | 1 |
| OBI:0001107 | tissue embedding station | 1 |
| OBI:0001113 | microplate washer | 2 |
| OBI:0001116 | vacuum manifold | 1 |
| OBI:0001119 | cell harvester | 1 |
| OBI:0001123 | microdissection instrument | 1 |
| OBI:0001124 | micropipette puller | 1 |
| OBI:0001127 | freeze substitution system | 1 |
| OBI:0001138 | X-ray source | 1 |
| OBI:0001865 | assay array | 41 |
| OBI:0002046 | surface plasmon resonance sensor chip | 1 |
| OBI:0002195 | microtome blade | 2 |
| OBI:0002488 | pipette | 1 |
| OBI:0002586 | digital acquisition card | 1 |
| OBI:0002786 | personal protective device | 25 |
| OBI:0002797 | apron | 1 |
| OBI:0002805 | transparent droplet barrier | 1 |
| OBI:0002814 | specimen collection device | 6 |
| OBI:0002821 | cotton swab | 1 |
| OBI:0002830 | catheter | 1 |
| OBI:0002920 | arthropod trap | 30 |
| OBI:0002924 | BG-Counter | 1 |
| OBI:0002927 | dipper for arthropod immatures | 1 |
| OBI:0003005 | device for collection of resting adult arthropods | 1 |
| OBI:0003006 | well net for arthropod immatures | 1 |
| OBI:0003048 | BG-lure scent dispenser | 1 |
| OBI:0003049 | hand-held sweep net | 1 |
| OBI:0003289 | mosquito membrane feeding device | 1 |
| OBI:0003369 | assay kit | 7 |
| OBI:0003481 | cow-baited arthropod trap | 1 |
| OBI:0003707 | mortar and pestle device | 1 |
| OBI:0400007 | analog-to-digital converter | 1 |
| OBI:0400019 | charge plate | 1 |
| OBI:0400080 | optical subsystem | 1 |
| OBI:0400086 | plate loader | 1 |
| OBI:0400101 | voltage amplifier | 3 |
| OBI:0400105 | arrayer | 1 |
| OBI:0400107 | computer | 3 |
| OBI:0400112 | liquid handler | 2 |
| OBI:0400142 | power supply | 1 |
| OBI:0400158 | digital-to-analog converter | 1 |
| OBI:0400170 | microscope slide | 1 |

LEQ cross-maps **86 OBI terms** across **6 branches** — every instrument family OBI covers that is relevant to the wet lab has a `xref:` in `src/leq/leq.base.obo`.

## What LEQ adds (the 4x)

These wet-lab equipment families have **no OBI term** and are defined in LEQ (class id where one exists; empty = candidate for a future aspect):

| family | LEQ class |
|---|---|
| vortex / vortexer | `LEQ:0000122` |
| sonicator / ultrasonic processor | `LEQ:0000123` |
| freezer (-20/-80) | `LEQ:0000186` |
| refrigerated storage (4C) | _TBD_ |
| biosafety cabinet | `LEQ:0000187` |
| fume hood | `LEQ:0000188` |
| liquid nitrogen dewar | `LEQ:0000189` |
| water bath / dry bath | `LEQ:0000117` |
| heat shaker | `LEQ:0000116` |
| ultracentrifuge | _TBD_ |
| refrigerated centrifuge | _TBD_ |
| pipette controller (motorized single-channel) | _TBD_ |
| thermal cycler subtypes (gradient, qPCR, digital) | _TBD_ |
| microscope subtypes (brightfield, fluorescence, confocal) | _TBD_ |
| plate imager / fluorescence imager | _TBD_ |
| nitrogen gun / speed-vac concentrator (benchtop) | `LEQ:0000155` |
| oven (dry heat, paraffin) | _TBD_ |
| water purification / Millipore system | `LEQ:0000194` |
| ultrasonic cleaner | `LEQ:0000195` |
| vacuum pump | `LEQ:0000190` |
| gas cylinder / CO2 supply | `LEQ:0000191/193` |
| CO2 incubator (as distinct from incubator) | _TBD_ |
| laminar flow hood (clean bench) | _TBD_ |

LEQ currently defines **100 classes**; OBI defines **609** in the device subtree — but OBI's coverage is clinical/imaging-heavy (NMR consoles, microtomes, arthropod traps, PPE) where LEQ is silent, and thin on exactly the benchtop workhorse equipment of the molecular/cell bio lab.

## Labware-side gap (OBI → LWO)

OBI's container subtree is device-flavored (specimen container, glass bottle). The following labware families have no OBI term and are covered by LWO:

- pipette tip (+ filter tip, fixed tip)
- tip rack / tip box
- tubes (microcentrifuge, conical, PCR tube/strip, NMR)
- vial subtypes (cryovial, culture vial)
- bottle / flask subtypes (reagent, Erlenmeyer, round-bottom)
- reservoir / trough / waste container
- microplate subtypes (PCR, deep-well, filter, TC-treated, well counts)
- aluminum block (24/96 position)
- racks (tube, vial, plate, cryovial, PCR tube)
- lids and seals (plate lid, PCR seal, snap cap, screw cap, universal lid)
- filters (syringe, vacuum manifold, filter paper)
- columns (chromatography, spin, desalting)
- culture ware (petri dish, TC dish)
- deck adapter / plate holder

This is why LWO stands alone on BFO material entity with an `xref:` to OBI:0000967 container rather than `is_a` OBI.
