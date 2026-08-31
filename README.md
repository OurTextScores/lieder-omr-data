# Lieder OMR data build

Reproducible build instructions for the boundary-safe OpenScore Lieder staff-crop
corpus used by HOMR. This is a **code and provenance repository**: it contains no IMSLP
scans, PDFs, crops, or model-generated labels.

The full corpus has 215 exact IMSLP source files and remains private because scan rights
are file-specific. A conservative public candidate is limited to 25 exact records whose
IMSLP metadata says `Public Domain` and `Normal Scan`; that is a release candidate pending
final human review, not a CC0 declaration.

## Inputs

1. A pinned HOMR checkout with `lieder-rebuild/` manifests and
   `training/omr_datasets/` builders.
2. An authorised local source store containing the IMSLP PDFs. This repository never
   downloads or redistributes them automatically.
3. An OpenScore Lieder checkout (or the `scores.yaml` revision cached by HOMR) for the
   CC0 symbolic sources.
4. Python dependencies used by HOMR's crop, alignment, token, and package validators.

## Build from scratch

```bash
git clone https://github.com/MALerLab/lieder-omr-data.git
cd lieder-omr-data

export HOMR_SOURCE=/absolute/path/to/homr
export IMSLP_PDFS=/authorised/path/to/imslp_pdfs
export OUT=/absolute/path/to/lieder-omr-build

make check-inputs
make audit-rights
make build-private
# Only after final source review:
make build-public-candidate
make verify
```

`build-private` may use the complete v4 boundary-safe corpus only in an
access-controlled store. `build-public-candidate` must read the frozen 25-ID allow-list,
not the complete manifest. Both builds must materialize paths and pass HOMR's portable
package verifier before release.

## Rights model

- OpenScore Lieder symbolic transcriptions: CC0 according to the source project.
- Scan images: exact IMSLP file records; do not infer their status from the composer or
  work title.
- Combined public dataset: use a per-source provenance table and an explicit `other`
  rights statement unless final review establishes a suitable public-domain label.

See HOMR's `docs/LIEDER_IMSLP_RELEASE_AUDIT.md` and
`docs/HF_DATASET_PUBLICATION_PLAN.md` for the audit method, exclusions, expected
repository layout, and final release gates.

## License

MIT for this build documentation and helper scripts only. No scan, score, annotation, or
derived-dataset licence is granted by this repository.
