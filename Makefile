.PHONY: validate capabilities contracts-hash verify-manifest preflight

validate:
	python scripts/validate_bundle.py

capabilities:
	python scripts/check_agent_capabilities.py --output capability_report.json

contracts-hash:
	python scripts/check_contract_freeze.py

verify-manifest:
	sha256sum -c MANIFEST.sha256

preflight: validate capabilities contracts-hash verify-manifest
