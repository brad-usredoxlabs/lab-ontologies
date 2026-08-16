#!/usr/bin/env python3
"""Build dated, self-contained dist/ release files for BioPortal.

BioPortal OBO upload needs the base file plus its import closure, with
the relative `import:` paths intact. The base files use `../imports/*`
(and LEQ also `../lwo/lwo.base.obo`), so the dist must mirror the src
layout EXACTLY — base file one level below the imports dir:

    dist/<name>-<date>/lwo/lwo.base.obo
    dist/<name>-<date>/imports/{bfo.obo,iao.owl,uo.obo,obi.obo}
    dist/leq-<date>/leq/leq.base.obo
    dist/leq-<date>/lwo/lwo.base.obo
    dist/leq-<date>/imports/{...}

and zip each directory. Run:  python tools/build_dist.py [date]
"""
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
DIST = REPO / "dist"
IMPORTS = ["bfo.obo", "iao.owl", "uo.obo", "obi.obo"]


def build(name: str, extra: list[tuple[str, str]], day: str) -> Path:
    out_dir = DIST / f"{name}-{day}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "imports").mkdir(parents=True)
    for f in IMPORTS:
        shutil.copy2(SRC / "imports" / f, out_dir / "imports" / f)
    # mirror src: base file lives in <name>/<name>.base.obo (so that
    # its `../imports/...` import lines resolve inside the dist dir)
    (out_dir / name).mkdir(parents=True)
    shutil.copy2(SRC / name / f"{name}.base.obo",
                 out_dir / name / f"{name}.base.obo")
    for rel, src_path in extra:
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / src_path, dest)
    zf = DIST / f"{name}-{day}.zip"
    with zipfile.ZipFile(zf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out_dir.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(DIST))
    return out_dir


def main() -> int:
    day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    DIST.mkdir(exist_ok=True)
    lwo = build("lwo", [], day)
    leq = build("leq", [("lwo/lwo.base.obo", "lwo/lwo.base.obo")], day)
    for d in (lwo, leq):
        files = sorted(p.relative_to(d) for p in d.rglob("*") if p.is_file())
        print(f"{d.name}: {len(files)} files -> {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
