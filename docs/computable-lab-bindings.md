# computable-lab role bindings — how the ontologies plug in

The two ontologies (LWO labware, LEQ equipment) give computable-lab a
stable, externally-published vocabulary for two things its records
already need but currently only capture ad hoc:

1. **What kind of thing a labware design is** (beyond the flat
   `labwareType` enum), and
2. **What kind of instrument a protocol step needs** (beyond a free-text
   roleId).

The bridge file is `src/bindings/computable-lab.yaml`. It is *data* —
no computable-lab schema or code changes are required to consume it.
This doc describes the three binding surfaces and the (future) wiring.

## The three binding surfaces

### 1. `Labware.labwareType` → LWO class

computable-lab's `Labware` record (schema/lab/labware.schema.yaml)
carries a flat `labwareType` enum: `plate, reservoir, tube_rack,
tiprack, tube, dish, slide, other, tubeset_*`.

The binding maps each enum value to an LWO annotation class. When a
`Labware` record is created, `labwareType` selects the LWO class;
finer subtypes (PCR vs assay vs deep-well vs TC-treated) are selected
by `tags`. Example:

```yaml
kind: labware
recordId: LBW-96-PLATE-CORNING-3635
name: Corning 3635 96-well polystyrene plate
labwareType: plate        # -> LWO:0000121 well plate (base)
tags: [ pcr, 96 ]          # -> LWO:0000127 PCR plate (refined)
format: { rows: 8, cols: 12, wellCount: 96 }   # -> LWO:0000003 has well count = 96
manufacturer: { name: Corning, catalogNumber: "3635" }
```

The `format` block maps to LWO data properties (see
`property_mapping` in the binding file) so the UI can render
ontology-typed values.

### 2. `Protocol.roles.instrumentRoles` → LEQ class

computable-lab's `Protocol` declares abstract
`instrumentRoles` (schema/workflow/protocol.schema.yaml, `InstrumentRole`
def: `roleId` + optional description). A step references a
`roleId`; a Run binds a concrete instrument.

The binding gives each well-known `roleId` an LEQ class, so a bound
instrument's LEQ annotation can be *checked* for subtype compatibility:
a `thermal_cycler` role requires an instrument whose LEQ class is a
subclass of `LEQ:0000106 thermal cycler`. Example:

```yaml
kind: protocol
recordId: PR-QPCR-2026
roles:
  instrumentRoles:
    - roleId: thermal_cycler     # -> LEQ:0000106
      description: PCR/qPCR thermal cycler
    - roleId: liquid_handler     # -> LEQ:0000105
  labwareRoles:
    - roleId: pcr-plate          # -> LWO:0000127
      expectedLabwareKinds: [ LBW-96-PLATE-CORNING-3635 ]
```

### 3. `context-role` records → LWO/LEQ classes

computable-lab's `context-role` records (schema/knowledge/
context-role.schema.yaml) are named semantic slots (`CR-*`) with
`applicable_domains` and machine-checkable `prerequisites`.

The binding maps each well-known context role to the LWO labware and/or
LEQ equipment classes that role can occupy. For example, the
`assay-plate` context role is constrained to LWO assay plates, and the
`qpcr-run` role requires an LEQ thermal cycler. Semantic control roles
(`positive-control`, `vehicle-control`) deliberately map to
`lwo: null / leq: null` — they are *biological* concepts, not labware;
the ontology constrains *where* they live, not *what* they are.

## What this buys computable-lab

- **A published, stable vocabulary.** LWO/LEQ ids are BioPortal-
  published, so a protocol that says "uses a LWO:0000127 PCR plate"
  points at a durable, externally-resolvable concept — not a local
  string.
- **Validation.** A Run that binds an instrument to an instrument
  role, or a labware to a context role, can be linted against the
  ontology class hierarchy (is the bound thing actually a subclass of
  the expected class?).
- **Interoperability.** Downstream consumers (OAK API, other tools) can
  resolve LWO/LEQ ids to definitions and synonyms via BioPortal / OLS.
- **UI hints.** The `property_mapping` table lets the UI render
  LWO-typed properties (nominal volume in UO units, well count, bottom
  geometry) with the ontology's own names.

## Suggested wiring (not required for the ontologies to ship)

1. **Ingestion:** when a `Labware` record is saved, derive the LWO
   class from `labwareType` + `tags` via the binding and store it as a
   `lwoClass` annotation (or tag). No schema change needed — it is a
   derived annotation, like the existing `DRV-LABWARE-ROLE` derivation.
2. **Lint:** add a lint rule that, for each `instrumentRole`, verifies
   the bound instrument's LEQ class is a subclass of the role's LEQ
   class (using the binding + the ontology `is_a` graph).
3. **UI:** for the `property_mapping` fields, render the LWO property
   name + UO unit instead of a raw number.

None of the above is required to publish LWO/LEQ to BioPortal — that
happens in Phase 4. The binding file and this doc are the
integration contract for when computable-lab is ready to consume them.
