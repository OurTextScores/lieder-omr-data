"""Validate private source paths without reading, copying, or uploading scans."""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--pdfs", type=Path, required=True)
parser.add_argument("--scores-yaml", type=Path, required=True)
args = parser.parse_args()
if not args.pdfs.is_dir() or not any(args.pdfs.glob("IMSLP*.pdf")):
    raise SystemExit("IMSLP_PDFS must be an authorised directory containing IMSLP PDFs")
if not args.scores_yaml.is_file():
    raise SystemExit("SCORES_YAML must point to OpenScore Lieder's data/scores.yaml")
print("Input check passed. Rights audit and source review remain mandatory before public release.")
