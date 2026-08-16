#!/usr/bin/env bash
# Validation gate for lab-ontologies.
#  1. python OBO structure lint (id format/uniqueness, defs, refs, acronyms)
#  2. oaklib structural tests (parse + imports resolve + root grounding)
#  3. oaklib load of both ontologies with full import closure (pronto parse)
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
command -v "$PY" >/dev/null || { echo "missing .venv — run: python3 -m venv .venv && .venv/bin/pip install 'oaklib[owl]' pytest"; exit 2; }

echo "== [1/3] OBO structure lint =="
"$PY" tools/validate_obo.py

echo "== [2/3] oaklib structural tests =="
"$PY" -m pytest tests/ -q

echo "== [3/3] full import-closure load =="
"$PY" - <<'EOF' 2>/dev/null
from oaklib import get_adapter
for name, path in [("LWO", "src/lwo/lwo.base.obo"), ("LEQ", "src/leq/leq.base.obo")]:
    ad = get_adapter(path)
    print(f"{name}: full closure load OK (label check {ad.label('BFO:0000040')})")
EOF

echo "ALL CHECKS PASSED"
