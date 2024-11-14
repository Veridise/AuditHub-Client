#!/bin/sh
MODULE="audithub_client"

.PHONY:all
all: check

.PHONY:check
check: isort mypy ruff

.PHONY:isort
isort:
	isort $(MODULE)

.PHONY:mypy
mypy:
	mypy $(MODULE)

.PHONY:ruff
ruff:
	ruff check $(MODULE)

.PHONY:stubs
stubs:
	stubgen -p audithub_client -o stubs

.PHONY: mypy-types
mypy-types:
	mypy --install-types --non-interactive
