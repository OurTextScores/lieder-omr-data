#!/usr/bin/env python3
"""Build the boundary-safe HOMR Lieder corpus from a locked source archive.

The frozen v4 alignment is retained as a provenance input: recomputing a numeric
alignment and silently accepting a different boundary would defeat the point of the
reviewed corpus.  Detection is rebuilt from the archived PDFs and must agree with that
frozen system topology before pairs are emitted.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "vendor" / "homr-stage2"
ALIGNMENT = ROOT / "provenance" / "alignment_v4_boundary_safe.json"


def run(module: str, *args: str, env: dict[str, str]) -> None:
    subprocess.run([sys.executable, "-m", module, *args], check=True, env=env)


def local_caches(openscore: Path, workspace: Path) -> tuple[Path, Path, Path]:
    scores = openscore / "data" / "scores.yaml"
    if not scores.is_file():
        raise SystemExit(f"missing OpenScore scores.yaml: {scores}")
    mscx = {}
    mxl = {}
    for path in openscore.rglob("*.mscx"):
        if path.stem.startswith("lc") and path.stem[2:].isdigit():
            mscx[path.stem[2:]] = str(path.resolve())
    for path in openscore.rglob("*.mxl"):
        if path.stem.startswith("lc") and path.stem[2:].isdigit():
            mxl[path.stem[2:]] = str(path.resolve())
    if not mscx or not mxl:
        raise SystemExit("locked source is missing local .mscx or .mxl files")
    workspace.mkdir(parents=True, exist_ok=True)
    mscx_cache = workspace / "mscx-tree.json"
    mxl_cache = workspace / "mxl-tree.json"
    mscx_cache.write_text(json.dumps(mscx, indent=2), encoding="utf-8")
    mxl_cache.write_text(json.dumps(mxl, indent=2), encoding="utf-8")
    return scores, mscx_cache, mxl_cache


def score_ids(pdfs: Path, destination: Path) -> Path:
    ids = sorted(path.stem for path in pdfs.glob("IMSLP*.pdf"))
    if not ids:
        raise SystemExit(f"no IMSLP PDFs found under {pdfs}")
    destination.write_text("\n".join(ids) + "\n", encoding="utf-8")
    return destination


def rebase_index(source_index: Path, pairs: Path, output: Path) -> int:
    by_stem = {}
    for line in pairs.read_text(encoding="utf-8").splitlines():
        image, tokens = line.split(",", 1)
        by_stem[Path(image).stem] = f"{image},{tokens}"
    selected = []
    for line in source_index.read_text(encoding="utf-8").splitlines():
        image = line.split(",", 1)[0]
        rebuilt = by_stem.get(Path(image).stem)
        if rebuilt:
            selected.append(rebuilt)
    if not selected:
        raise SystemExit(f"no rebuilt pairs matched frozen index {source_index}")
    output.write_text("\n".join(selected) + "\n", encoding="utf-8")
    return len(selected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "sources" / "lieder-all-source")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--skip-detection", action="store_true", help="Reuse existing detected systems.")
    args = parser.parse_args()
    if not ALIGNMENT.is_file():
        raise SystemExit(f"missing frozen alignment: {ALIGNMENT}")
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit(f"output must be empty or absent: {args.out}")
    pdfs = args.source / "pdfs"
    openscore = args.source / "openscore-lieder"
    manifests = args.source / "manifests"
    if not manifests.is_dir():
        raise SystemExit(f"not an extracted private Lieder source archive: {args.source}")
    args.out.mkdir(parents=True, exist_ok=True)
    work = args.out / "_build"
    scores_yaml, mscx_cache, mxl_cache = local_caches(openscore, work)
    ids = score_ids(pdfs, work / "score_ids.txt")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(RUNTIME), env.get("PYTHONPATH", "")])
    systems = work / "systems"
    pngs = work / "pages"
    ground_truth = work / "ground_truth"

    if not args.skip_detection:
        run("training.omr_datasets.detect_imslp_systems", "--pdfs", str(pdfs), "--pngs-out", str(pngs), "--systems-out", str(systems), env=env)
    run("training.omr_datasets.fetch_lieder_ground_truth", "--score-ids", str(ids), "--scores-yaml-cache", str(scores_yaml), "--file-tree-cache", str(mscx_cache), "--out", str(ground_truth), env=env)
    pairs = args.out / "pairs"
    manifest = args.out / "all_boundary_safe.txt"
    report = args.out / "build_report.json"
    run("training.omr_datasets.build_clean_stage2_pairs", "--alignment", str(ALIGNMENT), "--scores-yaml-cache", str(scores_yaml), "--file-tree-cache", str(mscx_cache), "--mxl-tree-cache", str(mxl_cache), "--systems", str(systems), "--pngs", str(pngs), "--out", str(pairs), "--manifest", str(manifest), "--report", str(report), env=env)
    empty_recovered = work / "recovered-empty.txt"
    empty_recovered.write_text("", encoding="utf-8")
    run("training.omr_datasets.audit_clean_stage2_pairs", "--manifest", str(manifest), "--alignment", str(ALIGNMENT), "--recovered-manifest", str(empty_recovered), "--out", str(args.out / "audit.json"), env=env)
    train = rebase_index(manifests / "imslp_train_index_v4_boundary_safe.txt", manifest, args.out / "train.txt")
    val = rebase_index(manifests / "imslp_val_index_v4_boundary_safe.txt", manifest, args.out / "val.txt")
    print(f"wrote {train} frozen-train and {val} frozen-validation pairs")


if __name__ == "__main__":
    main()
