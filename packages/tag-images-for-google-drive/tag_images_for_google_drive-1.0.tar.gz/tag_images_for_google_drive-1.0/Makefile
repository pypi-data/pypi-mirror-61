#!/usr/bin/env make

# WARNING: Use make >4.0
ifeq (0,$(shell echo "$(shell echo "$(MAKE_VERSION)" | sed -E 's/^([0-9]+).*/\1/') >= 4" | bc -l))
$(error Bad make version, please install make >= 4)
endif


SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

ifeq ($(OS),Windows_NT)
    OS := Windows
	EXE:=.exe
else
    OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
	EXE:=
endif
ifeq ($(shell uname -r | grep -q Microsoft && echo $$?),0)
BACKOS=Windows
else
BACKOS=$(OS)
endif

NPROC?=$(shell nproc)
SUDO?=

define BROWSER
	python -c '
	import os, sys, webbrowser
	from urllib.request import pathname2url

	webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])), autoraise=True)
	sys.exit(0)
	'
endef


ifneq ($(TERM),)
normal:=$(shell tput sgr0)
bold:=$(shell tput bold)
red:=$(shell tput setaf 1)
green:=$(shell tput setaf 2)
yellow:=$(shell tput setaf 3)
blue:=$(shell tput setaf 4)
purple:=$(shell tput setaf 5)
cyan:=$(shell tput setaf 6)
white:=$(shell tput setaf 7)
gray:=$(shell tput setaf 8)
endif

PRJ:=$(shell basename $(shell pwd))
VENV ?= $(PRJ)
DOCKER_REPOSITORY?=$(USER)
DOCKER_PARAMS?=--db descriptions.csv --tagfile tags.txt '**/*.png' '**/*.jpg'
DOCKER_GDRIVE_ROOT_FOLDER?=/Images
DOCKER_CRON_FREQUENCE?=* */12 * * *

PRJ_PACKAGE:=$(PRJ)
PYTHON_VERSION:=3.7

# Data directory (can be in other place, in VM or Docker for example)
export DATA?=data

# Conda environment
CONDA_BASE:=$(shell conda info --base)
CONDA_PACKAGE:=$(CONDA_PREFIX)/lib/python$(PYTHON_VERSION)/site-packages
CONDA_PYTHON:=$(CONDA_PREFIX)/bin/python
CONDA_ARGS?=

PIP_PACKAGE:=$(CONDA_PACKAGE)/$(PRJ_PACKAGE).egg-link
PIP_ARGS?=

EXTRA_INDEX:=--extra-index-url=https://pypi.anaconda.org/octo

.PHONY: help
.DEFAULT: help

## Print all majors target
help:
	@echo "$(bold)Available rules:$(normal)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=20 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

	echo -e "Use '$(cyan)make -jn ...$(normal)' for Parallel run"
	echo -e "Use '$(cyan)make -B ...$(normal)' to force the target"
	echo -e "Use '$(cyan)make -n ...$(normal)' to simulate the build"

.PHONY: dump-*
dump-%:
	@if [ "${${*}}" = "" ]; then
		echo "Environment variable $* is not set";
		exit 1;
	else
		echo "$*=${${*}}";
	fi

.git:
	@if [[ ! -d .git ]]; then
		git init -q
		git commit --allow-empty -m "Create project $(PRJ)"
	fi

.git/hooks/pre-push: | .git
	@# Add a hook to validate the project before a git push
	cat >.git/hooks/pre-push <<PRE-PUSH
	#!/usr/bin/env sh
	# Validate the project before a push
	if test -t 1; then
		ncolors=$$(tput colors)
		if test -n "\$$ncolors" && test \$$ncolors -ge 8; then
			normal="\$$(tput sgr0)"
			red="\$$(tput setaf 1)"
	        green="\$$(tput setaf 2)"
			yellow="\$$(tput setaf 3)"
		fi
	fi
	branch="\$$(git branch | grep \* | cut -d ' ' -f2)"
	if [ "\$${branch}" = "master" ] && [ "\$${FORCE}" != y ] ; then
		printf "\$${green}Validate the project before push the commit... (\$${yellow}make validate\$${green})\$${normal}\n"
		make validate
		ERR=\$$?
		if [ \$${ERR} -ne 0 ] ; then
			printf "\$${red}'\$${yellow}make validate\$${red}' failed before git push.\$${normal}\n"
			printf "Use \$${yellow}FORCE=y git push\$${normal} to force.\n"
			exit \$${ERR}
		fi
	fi
	PRE-PUSH
	chmod +x .git/hooks/pre-push

# Init git configuration
.gitattributes: | .git .git/hooks/pre-push  # Configure git
	@git config --local core.autocrlf input
	# Set tabulation to 4 when use 'git diff'
	@git config --local core.page 'less -x4'
ifeq ($(shell which daff >/dev/null ; echo "$$?"),0)
	# Add rules to manage diff with daff for CSV file
	@git config --local diff.daff-csv.command "daff.py diff --git"
	@git config --local merge.daff-csv.name "daff.py tabular merge"
	@git config --local merge.daff-csv.driver "daff.py merge --output %A %O %A %B"
	@[ -e .gitattributes ] && grep -v daff-csv .gitattributes >.gitattributes.new 2>/dev/null
	@[ -e .gitattributes.new ] && mv .gitattributes.new .gitattributes
	@echo "*.[tc]sv diff=daff-csv merge=daff-csv -text" >>.gitattributes
endif


CHECK_VENV=@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
  then ( echo -e "$(green)Use: $(cyan)conda activate $(VENV)$(green) before using 'make'$(normal)"; exit 1 ) ; fi

ACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate $(VENV) $(CONDA_ARGS)
DEACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda deactivate

VALIDATE_VENV=$(CHECK_VENV)
#VALIDATE_VENV=$(ACTIVATE_VENV)

# All dependencies of the project must be here

$(CONDA_PREFIX)/bin/exiftool:
	@conda install -y -c bioconda perl-image-exiftool

ifeq ($(OS),Darwin)
GCC=gcc
else
GCC=gcc_linux-64
endif
$(CONDA_PREFIX)/bin/$(GCC):
	@conda install -y -c anaconda make $(GCC)


.PHONY: requirements dependencies
REQUIREMENTS=$(PIP_PACKAGE) \
  $(CONDA_PREFIX)/bin/exiftool \
  $(CONDA_PREFIX)/bin/$(GCC) \
	.gitattributes
requirements: $(REQUIREMENTS)
dependencies: requirements


# Download dependencies for offline usage
~/.mypypi: setup.py
	pip download '.[dev,test]' --dest ~/.mypypi
# Download modules and packages before going offline
offline: ~/.mypypi
ifeq ($(OFFLINE),True)
CONDA_ARGS+=--use-index-cache --use-local --offline
PIP_ARGS+=--no-index --find-links ~/.mypypi
endif

# Rule to check the good installation of python in Conda venv
$(CONDA_PYTHON):
	@$(VALIDATE_VENV)
	conda install -q "python=$(PYTHON_VERSION).*" -y $(CONDA_ARGS)

# Rule to update the current venv, with the dependencies describe in `setup.py`
$(PIP_PACKAGE): $(CONDA_PYTHON) setup.py | .git # Install pip dependencies
	@$(VALIDATE_VENV)
	echo -e "$(cyan)Install setup.py dependencies ... (may take minutes)$(normal)"
	pip install $(PIP_ARGS) $(EXTRA_INDEX) -e '.[dev,test]' | grep -v 'already satisfied' || true
	# See https://github.com/pyinstaller/pyinstaller/issues/4265
	# which pyinstaller || pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
	echo -e "$(cyan)setup.py dependencies updated$(normal)"
	@touch $(PIP_PACKAGE)


.PHONY: configure
## Prepare the work environment (conda venv, kernel, ...)
configure:
	@conda create --name "$(VENV)" python=$(PYTHON_VERSION) -y $(CONDA_ARGS)
	@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
	then echo -e "Use: $(cyan)conda activate $(VENV)$(normal) $(CONDA_ARGS)" ; fi

.PHONY: remove-venv
remove-$(VENV):
	@$(DEACTIVATE_VENV)
	conda env remove --name "$(VENV)" -y 2>/dev/null
	echo -e "Use: $(cyan)conda deactivate$(normal)"
# Remove virtual environement
remove-venv : remove-$(VENV)

.PHONY: upgrade-venv
upgrade-$(VENV):
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not upgrade virtual env in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	conda update --all $(CONDA_ARGS)
	pip list --format freeze --outdated | sed 's/(.*//g' | xargs -r -n1 pip install $(EXTRA_INDEX) -U
	@echo -e "$(cyan)After validation, upgrade the setup.py$(normal)"
endif
# Upgrade packages to last versions
upgrade-venv: upgrade-$(VENV)

.PHONY: lint
.pylintrc:
	MYPYPATH=./stubs pylint --generate-rcfile > .pylintrc

.make-lint: $(REQUIREMENTS) $(PYTHON_SRC) | .pylintrc
	$(VALIDATE_VENV)
	@echo -e "$(cyan)Check lint...$(normal)"
	@echo "---------------------- FLAKE"
	@flake8 $(PRJ_PACKAGE)
	@echo "---------------------- PYLINT"
	@pylint $(PRJ_PACKAGE)
	touch .make-lint

## Lint the code
lint: .make-lint


$(CONDA_PREFIX)/bin/pytype:
	@pip install $(PIP_ARGS) -q pytype

pytype.cfg: $(CONDA_PREFIX)/bin/pytype
	@[[ ! -f pytype.cfg ]] && pytype --generate-config pytype.cfg || true
	touch pytype.cfg

.PHONY: typing
.make-typing: $(REQUIREMENTS) $(CONDA_PREFIX)/bin/pytype pytype.cfg $(PYTHON_SRC)
	$(VALIDATE_VENV)
	@echo -e "$(cyan)Check typing...$(normal)"
	MYPYPATH=./stubs/ mypy $(PRJ)
	touch .make-typing
## Check python typing
typing: .make-typing

## Add infered typing in module
add-typing: typing
	@find $(PRJ) -type f -name '*.py' -exec merge-pyi -i {} .pytype/pyi/{}i \;
	for phase in scripts/*
	do
	  ( cd $$phase ; find . -type f -name '*.py' -exec merge-pyi -i {} .pytype/pyi/{}i \; )
	done


.PHONY: docs
SPHINX_FLAGS=
# Generate API docs
docs/source: $(REQUIREMENTS) $(PYTHON_SRC)
	$(VALIDATE_VENV)
	sphinx-apidoc -f -o docs/source $(PRJ)/
	touch docs/source

# Build the documentation in specificed format (build/html, build/latexpdf, ...)
build/%: $(REQUIREMENTS) docs/source docs/* *.md | .git
	@$(VALIDATE_VENV)
	@TARGET=$(*:build/%=%)
ifeq ($(OFFLINE),True)
	if [ "$$TARGET" != "linkcheck" ] ; then
endif
	echo "Build $$TARGET..."
	LATEXMKOPTS=-silent sphinx-build -M $$TARGET docs build $(SPHINX_FLAGS)
	touch build/$$TARGET
ifeq ($(OFFLINE),True)
	else
		@echo -e "$(red)Can not to build '$$TARGET' in offline mode$(normal)"
	fi
endif

# Build all format of documentations
## Generate and show the HTML documentation
docs: build/html
	@$(BROWSER) build/html/index.html

.PHONY: sdist
dist/$(PRJ_PACKAGE)-*.tar.gz: $(REQUIREMENTS)
	@$(VALIDATE_VENV)
	./setup.py sdist

# Create a source distribution
sdist: dist/$(PRJ_PACKAGE)-*.tar.gz

.PHONY: bdist
dist/$(subst -,_,$(PRJ_PACKAGE))-*.whl: $(REQUIREMENTS)
	@$(VALIDATE_VENV)
	./setup.py bdist_wheel

# Create a binary wheel distribution
bdist: dist/$(subst -,_,$(PRJ_PACKAGE))-*.whl

.PHONY: dist

## Create a full distribution
dist: bdist sdist

.PHONY: check-twine
## Check the distribution before publication
check-twine: bdist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not check-twine in offline mode$(normal)"
else
	$(VALIDATE_VENV)
	twine check \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )
endif

.PHONY: test-twine
## Publish distribution on test.pypi.org
test-twine: bdist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not test-twine in offline mode$(normal)"
else
	$(VALIDATE_VENV)
	rm -f dist/*.asc
	twine upload --sign --repository-url https://test.pypi.org/legacy/ \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )
endif

.PHONY: release
## Publish distribution on pypi.org
release: clean dist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not release in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	[[ $$( find dist -name "*.dev*" | wc -l ) == 0 ]] || \
		( echo -e "$(red)Add a tag version in GIT before release$(normal)" \
		; exit 1 )
	rm -f dist/*.asc
	echo "Enter Pypi password"
	twine upload --sign \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )
endif

.PHONY: clean-pyc
# Clean pre-compiled files
clean-pyc:
	@/usr/bin/find . -type f -name "*.py[co]" -delete
	@/usr/bin/find . -type d -name "__pycache__" -delete

.PHONY: clean-build
# Remove build artifacts and docs
clean-build:
	@rm -fr build/
	@rm -fr dist/*
	@rm -fr *.egg-info
	@/usr/bin/find . -type f -name ".make-*" -delete
	@echo -e "$(cyan)Build cleaned$(normal)"


.PHONY: clean-pip
# Remove all the pip package
clean-pip:
	@$(VALIDATE_VENV)
	pip freeze | grep -v "^-e" | xargs pip uninstall -y
	@echo -e "$(cyan)Virtual env cleaned$(normal)"

.PHONY: clean-venv clean-$(VENV)
clean-$(VENV): remove-venv
	@conda create -y -q -n $(VENV) $(CONDA_ARGS)
	@touch setup.py
	@echo -e "$(yellow)Warning: Conda virtualenv $(VENV) is empty.$(normal)"
# Set the current VENV empty
clean-venv : clean-$(VENV)

.PHONY: clean
## Clean current environment
clean: clean-build clean-pyc

.PHONY: clean-all
# Clean all environments
clean-all: clean remove-venv

ifeq ($(BACKOS),Windows)
PYTEST_ARGS ?=
else
PYTEST_ARGS ?=-n 0
endif

.PHONY: test unittest functionaltest
.make-unit-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@$(VALIDATE_VENV)
	@echo -e "$(cyan)Run unit tests...$(normal)"
	python -m pytest  -s tests $(PYTEST_ARGS) -m "not functional"
	@date >.make-unit-test
# Run only unit tests
unit-test: .make-unit-test

.make-functional-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@$(VALIDATE_VENV)
	@echo -e "$(cyan)Run functional tests...$(normal)"
	python -m pytest  -s tests $(PYTEST_ARGS) -m "functional"
	@date >.make-functional-test
# Run only functional tests
functional-test: .make-functional-test

.make-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@echo -e "$(cyan)Run all tests...$(normal)"
	python -m pytest $(PYTEST_ARGS) -s tests
	#python setup.py test
	@date >.make-test
	@date >.make-unit-test
	@date >.make-functional-test
## Run all tests (unit and functional)
test: .make-test


.PHONY: validate
.make-validate: .make-test .make-lint .make-typing build/html build/linkcheck
	@date >.make-validate
## Validate the version before release
validate: .make-validate

$(CONDA_PREFIX)/bin/$(PRJ): $(REQUIREMENTS)
	python setup.py install

## Install the tools in conda env
install: $(CONDA_PREFIX)/bin/$(PRJ)

## Install the tools in conda env with 'develop' link
develop: $(REQUIREMENTS)
	python setup.py develop

## Install the tools in conda env
uninstall: $(CONDA_PREFIX)/bin/$(PRJ)
	pip uninstall $(PRJ)


ifeq ($(OS),Darwin)
PYINSTALLER_OPT=--hiddenimport _sysconfigdata_m_darwin_darwin
endif
dist/$(PRJ): .make-validate
	@PYTHONOPTIMIZE=2 && pyinstaller $(PYINSTALLER_OPT) --onefile $(PRJ)/$(PRJ).py
	touch dist/$(PRJ)
ifeq ($(BACKOS),Windows)
# Must have conda installed on windows with tag_images_for_google_drive env
	/mnt/c/WINDOWS/system32/cmd.exe /C 'conda activate $(PRJ) && python setup.py develop && pyinstaller --onefile tag_images_for_google_drive/tag_images_for_google_drive.py'
	touch dist/$(PRJ).exe
	echo -e "$(cyan)Executable is here 'dist/$(PRJ).exe'$(normal)"
endif
ifeq ($(OS),Darwin)
	ln -f "dist/$(PRJ)" "dist/$(PRJ).macos"
	echo -e "$(cyan)Executable is here 'dist/$(PRJ).macos'$(normal)"
else
	echo -e "$(cyan)Executable is here 'dist/$(PRJ)'$(normal)"
endif

## Build standalone executable for this OS
installer: dist/$(PRJ)


# Initialize and get a token API
gdfuse/default/state:
	[[ -e ~/.gdfuse ]] && mv ~/.gdfuse ~/.gdfuse.old
	google-drive-ocamlfuse -debug -config "$${PWD}/gdfuse/default/config"
	cp ~/.gdfuse/default/state gdfuse/default
	rm -Rf ~/.gdfuse
	[[ -e ~/.gdfuse.old ]] && mv ~/.gdfuse.old ~/.gdfuse


# Update the dockerfile with the setup datas and version
Dockerfile: setup.py
	@# Build docker image
	VERSION="$$(./setup.py --version)"
	DESCRIPTION="$$(./setup.py --description)"
	LICENSE="$$(./setup.py --license)"
	AUTHOR="$$(./setup.py --author)"
	AUTHOR_EMAIL="$$(./setup.py --author-email)"
	KEYWORDS="$$(./setup.py --keywords)"
	D='$$'

	cat >Dockerfile <<EOF
	# DO NOT ADD THIS FILE TO VERSION CONTROL!
	ARG OS_VERSION=latest

	FROM ubuntu:$${D}{OS_VERSION}
	ARG PARAMS
	ARG GDRIVE_ROOT_FOLDER
	ARG CRON_FREQUENCE="* */12 * * *"
	ENV _PARAMS="$${D}{PARAMS}"
	ENV _GDRIVE_ROOT_FOLDER="$${D}{GDRIVE_ROOT_FOLDER}"
	ENV _CRON_FREQUENCE="$${D}{CRON_FREQUENCE}"

	LABEL version="$${VERSION}"
	LABEL description="$${DESCRIPTION}"
	LABEL license="$${LICENSE}"
	LABEL keywords="$${KEYWORDS}"
	LABEL maintainer="$${AUTHOR}"

	COPY dist/tag_images_for_google_drive /
	RUN apt-get update && \
		apt-get install -y  exiftool software-properties-common cron gettext-base && \
		add-apt-repository ppa:alessandro-strada/ppa && \
		apt-get update && \
		apt-get install -y google-drive-ocamlfuse && \
		rm -rf /var/lib/apt/lists/* && \
		apt-get remove -y software-properties-common
	RUN mkdir -p /root/.gdfuse/default
	COPY gdfuse/default/config.template /root/.gdfuse/default/config.template
	RUN envsubst </root/.gdfuse/default/config.template >/root/.gdfuse/default/config
	COPY gdfuse/default/state /root/.gdfuse/default/state

	RUN echo "$${D}{_CRON_FREQUENCE} cd \"/gdrive\" && /tag_images_for_google_drive $${D}{_PARAMS} > /proc/1/fd/1 2>/proc/1/fd/2" >/etc/cron.d/crontab
	RUN /usr/bin/crontab /etc/cron.d/crontab
	CMD mkdir -p "/gdrive" && \
		google-drive-ocamlfuse -headless "/gdrive" && \
		/usr/sbin/cron -f
	EOF

# WARNING: never publish the container. The Google drive tokens are inside !
.make-docker-build: Dockerfile dist/$(PRJ)$(EXE) gdfuse/default/state
	@# Detect release version
	if [[ "$${VERSION}" =~ "^[0-9](\.[0-9])+$$" ]];
	then
		TAG_VERSION=-t "$(DOCKER_REPOSITORY)/$(PRJ):$${VERSION}"
	fi
	$(SUDO) docker build \
		-f Dockerfile \
		--build-arg OS_VERSION="latest" \
		--build-arg PARAMS="$(DOCKER_PARAMS)" \
		--build-arg GDRIVE_ROOT_FOLDER="$(DOCKER_GDRIVE_ROOT_FOLDER)" \
		--build-arg CRON_FREQUENCE="$(DOCKER_CRON_FREQUENCE)" \
		$${TAG_VERSION} \
		-t "$(DOCKER_REPOSITORY)/$(PRJ):latest" .
	echo -e "$(yellow)Never publish this image$(normal)"
	date >.make-docker-build

## Build the docker <PRJ>:latest
docker-build: .make-docker-build

# Reset and rebuild the container
docker-rebuild:
	@rm -f Dockerfile .make-docker-build
	$(MAKE) docker-stop docker-start

# Start and attach the container
docker-run: .cid_docker_daemon docker-attach

# Create a dedicated volume with the Google Drive cache
docker-volume:
	@$(SUDO) docker volume inspect "$(PRJ)" >/dev/null 2>&1 || \
	$(SUDO) docker volume create --name "$(PRJ)"
	echo -e "$(cyan)Docker volume '$(PRJ)' created$(normal)"

.cid_docker_daemon: .make-docker-build
	@$(SUDO) docker volume inspect "$(PRJ)" >/dev/null 2>&1 || $(MAKE) docker-volume
	$(SUDO) docker run \
		--detach \
		--cpus=0.5 --privileged \
		--cidfile ".cid_docker_daemon" \
		-v $(PRJ):/cache \
		-it "$(DOCKER_REPOSITORY)/$(PRJ):latest"
	echo -e "$(cyan)Docker daemon started$(normal)"

## Start a daemon container with the docker image
docker-start: .cid_docker_daemon

## Attach to the docker
docker-attach: .cid_docker_daemon
	@CID=$$(cat .cid_docker_daemon)
	$(SUDO) docker attach "$${CID}"

## Connect a bash in the container
docker-bash: .cid_docker_daemon
	@CID=$$(cat .cid_docker_daemon)
	$(SUDO) docker exec -i -t "$${CID}" /bin/bash

## Stop the container daemon
docker-stop:
	@if [[ -e ".cid_docker_daemon" ]] ; then
		CID=$$(cat .cid_docker_daemon)
		$(SUDO) docker stop "$${CID}" || true
		rm -f .cid_docker_daemon
		echo -e "$(cyan)Docker daemon stopped$(normal)"
	fi

docker-logs: .cid_docker_daemon
	@$(SUDO) docker container logs -f "$(PRJ)"

docker-top: .cid_docker_daemon
	@$(SUDO) docker container top "$(PRJ)"
