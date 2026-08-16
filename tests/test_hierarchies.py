"""Hierarchy enforcement for LWO and LEQ.

tests/class_hierarchy.yaml is the canonical tree. This test asserts:
  1. every class in the OBO files has an entry in the hierarchy file
     (a researcher adding a class MUST register its parent)
  2. every hierarchy entry matches the actual is_a line in the OBO file
     (the two cannot drift apart)
  3. the tree is acyclic (follow is_a to the root, no loops)
  4. no orphan depth: every class reaches the root in <= 8 steps
"""
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
HIER = REPO / "tests/class_hierarchy.yaml"
LWO = REPO / "src/lwo" / "lwo.base.obo"
LEQ = REPO / "src/leq" / "leq.base.obo"


def parse(path: Path, prefix: str):
    """Return {class_id: parent_id_or_None} for [Term] blocks only."""
    classes, cur, in_term = {}, None, False
    for line in path.read_text().splitlines():
        if line.startswith("[Term]"):
            in_term, cur = True, None
            continue
        if line.startswith("[Typedef]"):
            in_term, cur = False, None
            continue
        m = re.match(rf"id: ({prefix}:\d{{7}})", line)
        if m and in_term:
            cur = m.group(1)
            classes[cur] = None
            continue
        m = re.match(r"is_a:\s*((?:LWO|LEQ):\d{7})\b", line)
        if m and cur is not None:
            classes[cur] = m.group(1)
    return classes


def load_hier():
    """Return {ontology_key: {class_id: parent_id_or_None}}."""
    data = yaml.safe_load(HIER.read_text())
    out = {}
    for key, mapping in data.items():
        if not isinstance(mapping, dict):
            continue
        out[key] = {
            str(k): (None if v is None else str(v).strip())
            for k, v in mapping.items()
        }
    return out


@pytest.mark.parametrize("path,prefix,hkey,root", [
    (LWO, "LWO", "LWO", "LWO:0000100"),
    (LEQ, "LEQ", "LEQ", "LEQ:0000100"),
])
def test_hierarchy_matches_obo(path, prefix, hkey, root):
    obo = parse(path, prefix)
    hier = load_hier()[hkey]

    missing = set(obo) - set(hier)
    assert not missing, (
        f"classes missing from tests/class_hierarchy.yaml (register their "
        f"parent or the gate fails): {sorted(missing)}"
    )
    stale = set(hier) - set(obo)
    assert not stale, f"hierarchy entries with no OBO class: {sorted(stale)}"

    for cid, parent in obo.items():
        hparent = hier[cid]
        if cid == root:
            assert parent is None, f"root {root} must not have a local is_a"
            continue
        assert parent is not None, f"{cid} has no is_a to a local class"
        assert hparent == parent, (
            f"{cid}: hierarchy file says parent {hparent}, OBO file says "
            f"is_a {parent}. Update tests/class_hierarchy.yaml (or "
            f"tools/build_hierarchy.py) to match."
        )


@pytest.mark.parametrize("path,prefix,root", [
    (LWO, "LWO", "LWO:0000100"),
    (LEQ, "LEQ", "LEQ:0000100"),
])
def test_tree_is_acyclic_and_shallow(path, prefix, root):
    classes = parse(path, prefix)

    def depth(cid, seen):
        if cid in seen:
            pytest.fail(f"cycle detected at {cid}: {' -> '.join(list(seen) + [cid])}")
        if classes.get(cid) is None:
            return 0
        return 1 + depth(classes[cid], seen | {cid})

    for cid in classes:
        assert depth(cid, frozenset()) <= 8, f"{cid} is deeper than 8 levels"
