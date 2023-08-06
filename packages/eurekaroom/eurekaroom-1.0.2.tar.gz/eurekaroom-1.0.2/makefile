# ====  HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help. Typical usage `make build test` and then `make publish` after testing it thoroughly
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

publish: build  ## Build and publish this package to PyPi using Twine
	python -m twine check dist/*
	python -m twine upload dist/*

build: clean ## Build this application
	python -m pip install --upgrade --quiet setuptools wheel twine
	pipenv lock --requirements > requirements.txt	
	python setup.py --quiet sdist bdist_wheel

clean: ## Clean and prune old build artifacts from the source tree
	rm -rf build dist *.egg-info || true

test: ## Test this package before using or publishing
	python -m unittest discover -s './tests' -p '*_test.py'
