"""Validate private source paths without reading, copying, or uploading scans."""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--homr", type=Path, required=True)
parser.add_argument("--pdfs", type=Path, required=True)
args = parser.parse_args()
for path in (
    args.homr / "training/omr_datasets/audit_lieder_imslp_rights.py",
    args.homr / "lieder-rebuild/imslp_train_index_v4_boundary_safe.txt",
    args.homr / "lieder-rebuild/imslp_release_candidate_v4_score_ids.txt",
):
    if not path.exists():
        raise SystemExit(f"Missing required HOMR artifact: {path}")
if not args.pdfs.is_dir() or not any(args.pdfs.glob("IMSLP*.pdf")):
    raise SystemExit("IMSLP_PDFS must be an authorised directory containing IMSLP PDFs")
print("Input check passed. Rights audit and source review remain mandatory before public release.")
