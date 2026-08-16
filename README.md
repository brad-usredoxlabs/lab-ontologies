# Lab Ontologies (LWO + LEQ) — ARCHIVED

> **SPLIT 2026-08-16.** Live development moved to two standalone repos:
>
> - **`/home/brad/git/lwo`** — Laboratory Ware Ontology (LWO; passive
>   containers/consumables). Note the rename: the display name was
>   "Labware Ontology", now "Laboratory Ware Ontology" (collision with
>   Bioprotocols' LabOP "Labware Ontology"). Acronym/namespace/ids
>   unchanged.
> - **`/home/brad/git/leq`** — Lab Equipment Ontology (LEQ; active
>   devices). Carries a pinned copy of the LWO base file under
>   `src/imports/` for the `accepts labware` range.
>
> Both new repos carry the full pre-split history (git filter-repo).
> This directory is a read-only archive of the combined repo — do not
> make new commits here.

Two small, BFO-grounded OBO ontologies for the wet lab:

- **LWO — Laboratory Ware Ontology** (`src/lwo/lwo.base.obo`): the
  physical containers and consumables. Root `LWO:0000100 labware` is
  a BFO material entity, cross-mapped to OBI:0000967 container.

- **LEQ — Lab Equipment Ontology** (`src/leq/leq.base.obo`): the
  powered and mechanical devices. Root `LEQ:0000100 lab equipment` is
  an OBI/COB device.
