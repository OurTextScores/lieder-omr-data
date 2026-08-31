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

The `all` archive contains the exact 215-source private v4 input; `pd25` contains the
frozen 25-ID release-candidate subset and its allow-list. The historical crop/token
transformation has not yet been relocated into this repository, so source extraction is
reproducible today but a fresh derived-corpus build is not yet claimed. The vendored audit
and package-verification tools remain runnable without HOMR.

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
