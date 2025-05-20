#!/bin/sh
MODULE="audithub_client"
IMAGE_NAME="veridise/audithub-client"
IMAGE_TAG="latest"

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

.PHONY: image
image:
	docker build --platform=linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: push
push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: image-versioned
image-versioned:
	docker build --platform=linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(IMAGE_TAG) -t $(IMAGE_NAME):$(shell poetry version -s) .

.PHONY: push-versioned
push-versioned:
	docker push $(IMAGE_NAME):$(shell poetry version -s)

.PHONY: test
test:
	python -m unittest discover tests "*_test.py"