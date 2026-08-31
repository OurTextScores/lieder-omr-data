.DEFAULT_GOAL := help

SOURCE_DIR ?= sources
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

package:
	test -n "$(OUT)"
	python3 tools/package_dataset.py --root "$(OUT)"

verify:
	test -n "$(OUT)"
	python3 tools/package_dataset.py --root "$(OUT)" --verify-only

help:
	@echo "make extract-private-source    Fetch the locked 215-source private snapshot."
	@echo "make extract-public-candidate  Fetch the locked 25-source public-candidate snapshot."
	@echo "make package OUT=/path         Verify a materialized portable dataset."
