.DEFAULT_GOAL := help

check-inputs:

	python3 scripts/check_inputs.py --pdfs "$(IMSLP_PDFS)" --scores-yaml "$(SCORES_YAML)"

audit-rights: check-inputs

	python3 tools/audit_lieder_imslp_rights.py --help

build-private: check-inputs

	@echo "Use only v4 boundary-safe manifests; package into the private all-source repository."
	@echo "Never include historical/model-derived or boundary-ambiguous labels."

build-public-candidate: check-inputs

	@echo "Use only imslp_release_candidate_v4_score_ids.txt after final human source review."

verify:

	test -n "$(OUT)"
	python3 tools/package_dataset.py --root "$(OUT)" --verify-only

help:

	@echo "Set IMSLP_PDFS, SCORES_YAML, and OUT; then run make check-inputs."
