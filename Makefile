.DEFAULT_GOAL := help

check-inputs:

	python3 scripts/check_inputs.py --homr "$(HOMR_SOURCE)" --pdfs "$(IMSLP_PDFS)"

audit-rights: check-inputs

	cd "$(HOMR_SOURCE)" && python3 -m training.omr_datasets.audit_lieder_imslp_rights --help

build-private: check-inputs

	@echo "Use only v4 boundary-safe manifests; package into the private all-source repository."
	@echo "Never include historical/model-derived or boundary-ambiguous labels."

build-public-candidate: check-inputs

	@echo "Use only imslp_release_candidate_v4_score_ids.txt after final human source review."

verify:

	test -n "$(OUT)"
	cd "$(HOMR_SOURCE)" && python3 -m training.omr_datasets.package_dataset --root "$(OUT)" --verify-only

help:

	@echo "Set HOMR_SOURCE, IMSLP_PDFS, and OUT; then run make check-inputs."
