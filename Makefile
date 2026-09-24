.DEFAULT_GOAL := help

SOURCE_DIR ?= sources
CORPUS_DIR ?= corpus
ARCHIVE_BASE_URL ?=

fetch-private-source:
	python3 scripts/fetch_source.py all --dest "$(SOURCE_DIR)" $(if $(ARCHIVE_BASE_URL),--base-url "$(ARCHIVE_BASE_URL)")

extract-private-source: fetch-private-source
	python3 scripts/fetch_source.py all --dest "$(SOURCE_DIR)" --extract

fetch-public-candidate:
	python3 scripts/fetch_source.py pd25 --dest "$(SOURCE_DIR)" $(if $(ARCHIVE_BASE_URL),--base-url "$(ARCHIVE_BASE_URL)")

extract-public-candidate: fetch-public-candidate
	python3 scripts/fetch_source.py pd25 --dest "$(SOURCE_DIR)" --extract

audit-rights:
	python3 tools/audit_lieder_imslp_rights.py --help

build-v4: extract-private-source
	test -n "$(OUT)"
	python3 tools/build_lieder_v4.py --source "$(SOURCE_DIR)/lieder-all-source" --out "$(OUT)"

fetch-corpus:
	python3 scripts/fetch_corpus.py --dest "$(CORPUS_DIR)" $(if $(SPLIT),--split "$(SPLIT)")

verify-corpus:
	python3 scripts/fetch_corpus.py --dest "$(CORPUS_DIR)" --verify-only $(if $(SPLIT),--split "$(SPLIT)")

package:
	test -n "$(OUT)"
	python3 tools/package_dataset.py --root "$(OUT)"

verify:
	test -n "$(OUT)"
	python3 tools/package_dataset.py --root "$(OUT)" --verify-only

verify-runtime:
	python3 tools/vendor_runtime.py --verify

check-rasterization:
	python3 tools/check_rasterization.py

help:
	@echo "make fetch-corpus [SPLIT=valid]      Download the rights-cleared corpus (482MB, or 33MB for valid)."
	@echo "make verify-corpus [SPLIT=valid]     Re-check downloaded shards against the pinned digests."
	@echo "make verify-runtime            Check the vendored HOMR runtime against its pin."
	@echo "make extract-private-source    Fetch the locked 215-source private snapshot."
	@echo "make extract-public-candidate  Fetch the locked 25-source public-candidate snapshot."
	@echo "make build-v4 OUT=/path        Rebuild the audited boundary-safe private corpus."
	@echo "make package OUT=/path         Verify a materialized portable dataset."
