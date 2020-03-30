####################################################
# Dot Targets
####################################################

.DEFAULT_GOAL := default
.PHONY: clean default freeze parser run style test venv

####################################################
# Constants
####################################################

GEN_DIR := tight/_gen

ANTLR4_OPTS := -Dlanguage=Python3 -o $(GEN_DIR)
GRAMMAR_SRC := $(shell pwd)/grammar/Tight.g4
PY_BIN := venv/bin
REQUIREMENTS_DEST := requirements.txt

####################################################
# Phony Targets
####################################################

clean:
	-rm -rf tight/_gen
	-rm -rf venv

default:
	$(error Please specify an explicit target.)

freeze:
	@$(PY_BIN)/pip3 freeze | grep -v "pkg-resources" > $(REQUIREMENTS_DEST)

parser: $(GEN_DIR)/__init__.py

run: venv parser
	@$(PY_BIN)/python3 -m tight

style: venv
	@$(PY_BIN)/python3 -m pycodestyle --exclude=$(GEN_DIR)/* tight test

test: venv parser
	@$(PY_BIN)/python3 -m unittest

venv: $(PY_BIN)/activate

####################################################
# Actual Targets
####################################################

$(GEN_DIR)/__init__.py: $(GRAMMAR_SRC)
	@antlr4 $(ANTLR4_OPTS) $(GRAMMAR_SRC)
	@touch tight/_gen/__init__.py

$(PY_BIN)/activate: $(REQUIREMENTS_DEST)
	@test -d venv || python3 -m venv venv
	@$(PY_BIN)/pip3 install --upgrade pip
	@$(PY_BIN)/pip3 install -r $(REQUIREMENTS_DEST)
	@touch $(PY_BIN)activate
