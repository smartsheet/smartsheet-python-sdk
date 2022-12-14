.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 smartsheet tests

test:
	python setup.py test

coverage:
	coverage run --source smartsheet setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs-source/smartsheet.rst
	rm -f docs-source/modules.rst
	sphinx-apidoc -o docs-source/ smartsheet
	$(MAKE) -C docs-source clean
	$(MAKE) -C docs-source html
	rm -rf docs
	cp -r docs-source/_build/html docs
	cp .nojekyll docs
	open docs/index.html

install: clean
	python setup.py install
