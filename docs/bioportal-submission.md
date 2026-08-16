# BioPortal submission — exact form values

BioPortal accepts OBO natively (no OWL conversion needed). The
`dist/` directory (built by `tools/build_dist.py`) contains the dated
release files + import closure, zipped per ontology.

**Prerequisite:** a free BioPortal account (register at
https://bioportal.bioontology.org/user/signup). Submission is a web
form; everything below is the exact value to type.

## Build the dist

```bash
cd /home/brad/git/lab-ontologies
.venv/bin/python tools/build_dist.py            # uses today's date
ls dist/                                          # lwo-<date>.zip, leq-<date>.zip
```

Upload the **zip** (BioPortal expands it; the base file's `import:`
lines resolve against the `imports/` dir inside).

## LWO form values

| Field | Value |
|---|---|
| Name | Laboratory Ware Ontology |
| Acronym | LWO |
| Short name | lwo |
| Description | An ontology of laboratory labware — the physical containers and consumables used to hold, move, and process samples and reagents: vessels (tubes, vials, bottles, flasks, reservoirs), microplates and aluminum blocks, pipette tips and tip racks, racks, lids and seals, filters, columns, and culture ware. LWO is grounded in BFO material entity and cross-mapped to OBI where OBI provides a matching concept. The passive counterpart of laboratory equipment (LEQ). |
| License | Creative Commons Attribution 4.0 (CC-BY-4.0) |
| Homepage | https://github.com/brad-usredoxlabs/lab-ontologies |
| Version IRI | https://brad-usredoxlabs.github.io/lab-ontologies/lwo |
| Ontology language | OBO |
| Status | Alpha |
| Contact / maintainer | Brad (Computable Lab) — email per BioPortal account |
| Imports (list) | BFO, IAO, OBI, UO |

## LEQ form values

| Field | Value |
|---|---|
| Name | Lab Equipment Ontology |
| Acronym | LEQ |
| Short name | leq |
| Description | An ontology of laboratory equipment — the powered and mechanical devices used to act upon samples, reagents, and labware: liquid-handling devices (pipettes, liquid handlers), thermal equipment (cyclers, incubators, dryers, baths), separation equipment (centrifuges, chromatography, electrophoresis, purification), reading and measurement devices (plate readers, spectrometers, balances, pH meters, counters, sequencers, mass spectrometers, NMR, microscopes), preparation devices (vortexes, sonicators, shakers, homogenizers, plate washers), storage and containment equipment (freezers, autoclaves, biosafety cabinets, fume hoods), imaging equipment, and support infrastructure (vacuum, gas, power). LEQ is grounded in the OBI device concept (COB:0001300) and cross-maps to OBI instrument terms where they exist. The active counterpart of labware (LWO). |
| License | CC-BY-4.0 |
| Homepage | https://github.com/brad-usredoxlabs/lab-ontologies |
| Version IRI | https://brad-usredoxlabs.github.io/lab-ontologies/leq |
| Ontology language | OBO |
| Status | Alpha |
| Contact / maintainer | Brad (Computable Lab) |
| Imports (list) | BFO, IAO, OBI, UO, LWO (labware, for the `accepts labware` range) |

## Notes for the reviewer (paste into BioPortal "comments")

> LWO and LEQ are companion ontologies. LWO covers passive labware
> (containers/consumables); LEQ covers active equipment (devices that
> act on samples). Both are small, BFO-grounded, and cross-mapped to
> OBI where OBI has a term (LEQ cross-maps ~85 OBI instrument terms).
> The gap they fill: OBI has no terms for the majority of benchtop
> molecular/cell-bio equipment (vortex, sonicator, freezer, BSC, fume
> hood, water bath) and essentially no labware terms (tips, tubes,
> plates, racks, lids, columns, filters). See
> docs/obi-gap-analysis.md. IRI base is a GitHub Pages placeholder for
> the alpha release; will migrate to a PURL before 1.0.

## Post-submission

- [ ] BioPortal assigns official `LWO` / `LEQ` ids + version IRIs.
- [ ] Once a stable IRI base exists, update `id:` headers in both
      `.base.obo` files and re-run `./check.sh`.
- [ ] Tag the release: `git tag lwo-0.1.0` / `leq-0.1.0`.
- [ ] (Optional) add `obi` to the cl-appliance ontology-service list so
      the OAK API serves OBI for the researcher cron (one line in
      `cl-appliance/roles/ontology-service/defaults/main.yml`, restart
      the service on appliance-01).
