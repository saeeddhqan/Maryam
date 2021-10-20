
first: help


# ------------------------------------------------------------------------------
# Build

install:  ## Install package
	python3 setup.py install


build:  ## Build package by sdist
	python3 setup.py sdist


build-default:  ## Build package by build (recommended)
	python3 -m build


uninstall:  ## Uninstall package
	pip uninstall maryam
	bash uninstall.sh

upload-pypi:  ## Upload package to PyPI
	python3 -m twine upload dist/*.tar.gz


upload-test:  ## Upload package to test PyPI
	python3 -m twine upload --repository test dist/*.tar.gz


# ------------------------------------------------------------------------------
# Testing

check:  ## Check linting
	flake8
	isort . --project maryam --check-only --diff
	black . --check


fmt:  ## Format source
	isort . --project maryam
	black .

# ------------------------------------------------------------------------------
# Other

clean:  ## Clean build files
	rm -rf build dist site .pytest_cache .eggs
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf *.egg-info
	rm -r docs/build

help:  ## Show this help menu
	@grep -E '^[0-9a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'
