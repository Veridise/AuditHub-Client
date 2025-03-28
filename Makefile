#!/bin/sh
MODULE="audithub_client"

.PHONY:all
all: check

.PHONY:check
check: black isort ruff mypy

.PHONY:black
black:
	black --check $(MODULE)

.PHONY:black-fix
black-fix:
	black $(MODULE)

.PHONY:isort
isort:
	isort --check $(MODULE)

.PHONY:isort-fix
isort-fix:
	isort $(MODULE)

.PHONY:mypy
mypy:
	mypy $(MODULE)

.PHONY:ruff
ruff:
	ruff check $(MODULE)

.PHONY:ruff-fix
ruff-fix:
	ruff check --fix $(MODULE)

.PHONY: mypy-types
mypy-types:
	mypy --install-types --non-interactive

.PHONY: fix
fix: isort-fix black-fix ruff-fix
