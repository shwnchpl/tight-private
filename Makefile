.DEFAULT_GOAL := default

ANTLR4_OPTS := -Dlanguage=Python3 -o tight/_gen
GRAMMAR_SRC := $(shell pwd)/grammar/Tight.g4
REQUIREMENTS_DEST := requirements.txt

.PHONY: freeze

clean:
	-rm -r tight/_gen

default:
	$(error Please specify an explicit target.)

freeze:
	@pip3 freeze | grep -v "pkg-resources" > $(REQUIREMENTS_DEST)

parser:
	@antlr4 $(ANTLR4_OPTS) $(GRAMMAR_SRC)
	@touch tight/_gen/__init__.py

run:
	@python3 -m tight
