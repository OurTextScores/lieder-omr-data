# Lieder OMR data build

Provenance and source-reconstruction instructions for the boundary-safe OpenScore Lieder
staff-crop corpus used by HOMR. This repository contains no IMSLP scans, PDFs, crops, or
model-generated labels; those are supplied as separately locked, checksummed archives.

The full corpus has 215 exact IMSLP source files and remains private because scan rights
are file-specific. A conservative public candidate is limited to 25 exact records whose
IMSLP metadata says `Public Domain` and `Normal Scan`; that is a release candidate pending
final human review, not a CC0 declaration.

## Locked source inputs

`sources.lock.json` records the CDN URL, exact byte length, SHA-256, archive layout, and
access class for both frozen v4 inputs. The downloader is standard-library Python,
retains an interrupted `.part` download for resumption, verifies SHA-256, and rejects
unsafe archive paths. It does not require an OpenScore checkout or a separately managed
IMSLP PDF store.

The lockfile uses the public R2 development origin. A future custom CDN domain can be
used without modifying the lockfile, for example
`make extract-private-source ARCHIVE_BASE_URL=https://archives.example.org`.

## Build from scratch

```bash
git clone https://github.com/jhlusko/lieder-omr-data.git
cd lieder-omr-data

make extract-private-source
# Or, for the exact 25-source public-domain normal-scan candidate:
make extract-public-candidate
```

## Build environment

The private v4 rebuild runs on Linux with **Python 3.11--3.12**, the packages in
`requirements.txt` plus HOMR's build dependencies (`torch`, `opencv-python-headless`,
`Pillow`, `onnxruntime`, `pypdfium2`, `music21`, and `PyYAML`). The detector also needs
its published segmentation/staff-detection weights; it obtains them through HOMR's
pinned downloader on first use. No live OpenScore checkout is required: the builder
reads the archived local `.mscx` and `.mxl` files.

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt \
  torch opencv-python-headless Pillow onnxruntime pypdfium2 music21
```

The full private source archive is required for `make build-v4`; the public PD25 archive
is deliberately not treated as an interchangeable training source.

The `all` archive contains the exact 215-source private v4 input; `pd25` contains the
frozen 25-ID release-candidate subset and its allow-list. The boundary-safe v4 detector,
alignment, crop, token, sidecar, audit, and frozen-split stages are vendored and exposed
as `make build-v4 OUT=/path`. See [the executable build notes](docs/BUILD_PIPELINE.md).

## Vendored runtime

The corpus is built by HOMR's own converter, vendored under `vendor/homr-stage2` so the
dataset can be rebuilt without a HOMR checkout. `vendor/PIN.json` records the commit it
came from and a SHA-256 for every vendored file, because "the current converter" is not a
reproducible claim and a snapshot whose origin is unrecorded can be neither audited nor
refreshed on purpose.

```bash
make verify-runtime                  # the vendored tree still matches its pin
python3 tools/vendor_runtime.py --refresh --source /path/to/homr    # move the pin
```

Refreshing refuses a checkout with uncommitted changes: a pin naming a commit nobody else
can check out is worse than no pin. Only `.py` sources are vendored - model weights and
ONNX graphs are fetched by HOMR's own pinned downloader at build time.

**Pin history.** The runtime was previously an unrecorded snapshot. It is now pinned at
`87ff3d2` (2026-09-13), which is the first revision to write notation sidecars at schema
**v5** - the schema carrying the per-note voice. Corpora built before that carry v4 and no
voice; see `docs/BUILD_PIPELINE.md`.

## Rights model

- OpenScore Lieder symbolic transcriptions: CC0 according to the source project.
- Scan images: exact IMSLP file records; do not infer their status from the composer or
  work title.
- Combined public dataset: use a per-source provenance table and an explicit `other`
  rights statement unless final review establishes a suitable public-domain label.

The private source database carries the original audit ledger and release plan; this
repository carries the code needed to reproduce the audit.

## License

MIT for this build documentation and helper scripts only. No scan, score, annotation, or
derived-dataset licence is granted by this repository.
