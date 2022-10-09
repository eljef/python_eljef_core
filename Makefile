VERSION := 1.6.1

# all runs help
all : help

# help lists out targets
help :
	$(info $(NULL))
	$(info ** Available Targets **)
	$(info $(NULL))
	$(info $(NULL)	build        - builds a python egg for installation)
	$(info $(NULL)	clean        - removes build directories)
	$(info $(NULL)	depsinstall  - installs dependencies via pip)
	$(info $(NULL)	depsupdate   - upgrades dependencies via pip)
	$(info $(NULL)	help         - prints this message)
	$(info $(NULL)	install      - installs the project onto the system)
	$(info $(NULL)	lint         - runs linting for the project)
	$(info $(NULL)	test         - runs tests for the project)
	$(info $(NULL)	testcoverage - runs test coverage reports for the project)
	$(info $(NULL)	versionget   - returns the current project version)
	$(info $(NULL)	versionset   - updates the project version in all version files)
	$(info $(NULL))
	@:

build:
	python3 setup.py build

clean:
	rm -rf build dist eljef_core.egg-info \
		eljef/__pycache__ eljef/core/__pycache__ \
		tests/__pycache__ tests/_trial_temp \
		.pytest_cache .coverage

depsinstall:
	pip install -r requirements.txt

depsupdate:
	pip install --upgrade -r requirements.txt

install:
	python3 setup.py install

lint:
	flake8 eljef/core
	pylint eljef/core

test:
	pytest

testcoverage:
	pytest --cov=eljef/ tests/

versionget:
	@echo $(VERSION)

versionset:
	@$(eval OLDVERSION=$(shell cat setup.py | awk -F"[=,]" '/version=/{gsub("\047", ""); print $$2}'))
	@sed -i -e "s/$(OLDVERSION)/$(VERSION)/" eljef/core/__version__.py
	@sed -i -e "s/version = '$(OLDVERSION)'/version = '$(VERSION)'/" \
	        -e "s/release = '$(OLDVERSION)'/release = '$(VERSION)'/" docs/source/conf.py
	@sed -i -e "s/version='$(OLDVERSION)'/version='$(VERSION)'/" setup.py
	@sed -i -e "s/pkgver=$(OLDVERSION)/pkgver=$(VERSION)/" packaging/linux/arch/PKGBUILD
