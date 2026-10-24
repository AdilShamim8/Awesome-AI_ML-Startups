.PHONY: help validate test check build snapshot categories links stats clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## Run the full data validation (same as CI)
	python scripts/validate_data.py

test: ## Run the unit and integration test suite
	python -m unittest discover -s tests -v

check: validate test ## validate + test (the CI gate)

build: ## Regenerate both CSV mirrors from the canonical JSON
	python scripts/build_master_csv.py
	python scripts/build_funding_rounds_csv.py

snapshot: ## Build this month's snapshot from master (MONTH=october YEAR=2026 DATE= optional)
	@if [ -z "$(MONTH)" ] || [ -z "$(YEAR)" ]; then \
		echo "usage: make snapshot MONTH=october YEAR=2026 [DATE=2026-10-24]"; exit 2; fi
	@if [ -n "$(DATE)" ]; then \
		python scripts/build_snapshots.py --month $(MONTH) --year $(YEAR) --date $(DATE); \
	else \
		python scripts/build_snapshots.py --month $(MONTH) --year $(YEAR); \
	fi

categories: ## Regenerate the category pages from master
	python scripts/build_categories.py

links: ## Check website liveness (403/429 are bot-blocked, not failures)
	python scripts/check_links.py

stats: ## Print computed dataset statistics
	python scripts/verify_readme_stats.py --report

readme-check: ## Verify README headline numbers match the data
	python scripts/verify_readme_stats.py

release: build categories validate test readme-check ## Full pre-release gate
