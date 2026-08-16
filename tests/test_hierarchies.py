"""Hierarchy enforcement for LWO and LEQ.

tests/class_hierarchy.yaml is the canonical tree. This test asserts:
  1. every class in the OBO files has an entry in the hierarchy file
     (a researcher adding a class MUST register its parent)
  2. every hierarchy entry matches the actual is_a line in the OBO file
     (the two cannot drift apart)
  3. the tree is acyclic (follow is_a to the root, no loops)
  4. no orphan depth: every class reaches the root in <= 8 steps
  5. only designated branch classes may hang directly under the root
     (a new top-level branch is an explicit, reviewed decision)
"""
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
HIER = REPO / "tests/class_hierarchy.yaml"
LWO = REPO / "src/lwo" / "lwo.base.obo"
LEQ = REPO / "src/leq" / "leq.base.obo"

# The only classes allowed as direct children of each root. Everything else
# must hang under one of these (or under a further subclass).
LWO_ROOT_BRANCHES = {
    "LWO:0000101",  # vessel
    "LWO:0000117",  # reservoir
    "LWO:0000120",  # microplate
    "LWO:0000134",  # aluminum block
    "LWO:0000140",  # liquid-handling consumable
    "LWO:0000150",  # rack
    "LWO:0000160",  # lid or seal
    "LWO:0000170",  # filter
    "LWO:0000180",  # column
    "LWO:0000190",  # culture ware
    "LWO:0000200",  # deck support labware
}
LEQ_ROOT_BRANCHES = {
    "LEQ:0000101",  # liquid-handling equipment
    "LEQ:0000200",  # thermal equipment
    "LEQ:0000201",  # separation equipment
    "LEQ:0000202",  # measurement equipment
    "LEQ:0000203",  # preparation equipment
    "LEQ:0000204",  # storage and containment equipment
    "LEQ:0000205",  # imaging equipment
    "LEQ:0000206",  # support equipment
}


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


@pytest.mark.parametrize("path,prefix,root,allowed", [
    (LWO, "LWO", "LWO:0000100", LWO_ROOT_BRANCHES),
    (LEQ, "LEQ", "LEQ:0000100", LEQ_ROOT_BRANCHES),
])
def test_only_branches_hang_under_root(path, prefix, root, allowed):
    """Rule 5: a class may sit directly under the root ONLY if it is a
    designated branch. This is what stops the tree from flattening back
    out — a new top-level branch is an explicit, reviewed decision."""
    classes = parse(path, prefix)
    direct = [cid for cid, parent in classes.items() if parent == root]
    offenders = [cid for cid in direct if cid not in allowed]
    assert not offenders, (
        f"classes hang directly under root {root} but are not designated "
        f"branches — attach them to an existing branch (or add them to "
        f"{prefix}_ROOT_BRANCHES in this test as a deliberate new branch): "
        f"{offenders}"
    )
    # And every designated branch must actually exist and hang under root.
    for b in allowed:
        assert b in classes, f"designated branch {b} is not in {prefix}"
        assert classes[b] == root, f"designated branch {b} is not under root"


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
