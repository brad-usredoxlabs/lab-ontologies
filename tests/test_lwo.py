"""Structural tests for LWO and LEQ.

Loads each ontology through oaklib/pronto (which also parses all imports),
then asserts:
  - every local class/property id resolves to a label
  - every xref target resolves through the import closure
    (this is the cross-ontology mapping check)
  - the root class is grounded (LWO -> BFO material entity,
    LEQ -> COB device), checked textually and by label resolution
  - no duplicate labels within an ontology
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
from oaklib import get_adapter

REPO = Path(__file__).resolve().parent.parent
LWO = REPO / "src/lwo" / "lwo.base.obo"
LEQ = REPO / "src/leq" / "leq.base.obo"


def _local_ids(path: Path, prefix: str) -> list[str]:
    ids = []
    for line in path.read_text().splitlines():
        m = re.match(rf"id: ({prefix}:\d{{7}})", line)
        if m:
            ids.append(m.group(1))
    return ids


def _xrefs(path: Path) -> list[str]:
    out = []
    for line in path.read_text().splitlines():
        m = re.match(r"xref:\s*(\S+)", line)
        if m:
            out.append(m.group(1))
    return out


def _root_is_a(path: Path, prefix: str) -> str:
    """Return the is_a target of the root class (LWO:0000100 / LEQ:0000100)."""
    root = f"{prefix}:0000100"
    in_root = False
    for line in path.read_text().splitlines():
        if re.match(rf"id: {re.escape(root)}$", line):
            in_root = True
            continue
        if in_root:
            if line.startswith("[Term]"):
                break
            m = re.match(r"is_a:\s*(\S+)", line)
            if m:
                return m.group(1)
    return ""


@pytest.fixture(scope="module")
def lwo():
    return get_adapter(str(LWO))


@pytest.fixture(scope="module")
def leq():
    return get_adapter(str(LEQ))


def test_lwo_loads(lwo):
    for cid in _local_ids(LWO, "LWO"):
        assert lwo.label(cid) is not None, f"LWO {cid} has no label"


def test_leq_loads(leq):
    for cid in _local_ids(LEQ, "LEQ"):
        assert leq.label(cid) is not None, f"LEQ {cid} has no label"


def test_lwo_root_grounded_in_bfo(lwo):
    assert lwo.label("LWO:0000100") == "labware"
    assert _root_is_a(LWO, "LWO") == "BFO:0000040"
    assert lwo.label("BFO:0000040") == "material entity"


def test_leq_root_grounded_in_cob_device(leq):
    assert leq.label("LEQ:0000100") == "lab equipment"
    assert _root_is_a(LEQ, "LEQ") == "COB:0001300"
    assert leq.label("COB:0001300") == "device"


def test_lwo_xrefs_resolve(lwo):
    for x in _xrefs(LWO):
        assert lwo.label(x) is not None, f"LWO xref {x} does not resolve"


def test_leq_xrefs_resolve(leq):
    for x in _xrefs(LEQ):
        assert leq.label(x) is not None, f"LEQ xref {x} does not resolve"


def test_no_duplicate_labels_lwo(lwo):
    labels = [lwo.label(c) for c in _local_ids(LWO, "LWO")]
    assert None not in labels
    assert len(labels) == len(set(labels)), "duplicate labels in LWO"


def test_no_duplicate_labels_leq(leq):
    labels = [leq.label(c) for c in _local_ids(LEQ, "LEQ")]
    assert None not in labels
    assert len(labels) == len(set(labels)), "duplicate labels in LEQ"
