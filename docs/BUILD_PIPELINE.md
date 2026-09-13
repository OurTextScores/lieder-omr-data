# Executable boundary-safe Lieder build

`tools/build_lieder_v4.py` produces the reviewed v4 training layout from the private
locked source archive. It uses only archived PDFs and archived OpenScore files for the
input corpus. The detector is rerun from PDF pages; its output is checked by the
vendored clean-pair builder against the frozen, reviewed boundary alignment.

The alignment is deliberately versioned in `provenance/alignment_v4_boundary_safe.json`
(SHA-256 `eb04c11398a0736df1b35a61a81df311a3cfcfcd38cbe4621f643a93e39a96d9`). It is
not recomputed opportunistically: a different DP boundary must be reviewed before it
can replace this source of truth.

```bash
make extract-private-source
make build-v4 OUT=build/lieder
```

The output contains materialized crops/tokens/sidecars, `all_boundary_safe.txt`, and
the canonical score-disjoint `train.txt`/`val.txt` re-based from the frozen v4 indexes.
`audit.json` must pass. The public PD25 archive is intentionally not wired to this
target: its 25 sources are a release candidate, not an approved substitute for the
private v4 corpus.
