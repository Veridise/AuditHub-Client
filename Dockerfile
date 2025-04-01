FROM python:3.13-alpine AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Stage - builder
FROM python:3.13-alpine AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=2.1.2

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --no-root --only main

COPY . .
RUN . /venv/bin/activate && poetry build

# Stage - release
FROM base AS release

# add new user
ENV USER=appuser
RUN adduser -D $USER

ENV PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv
RUN chown -hR $USER /venv

COPY --from=builder /app/dist .
RUN . /venv/bin/activate && pip install *.whl && rm *.whl *.tar.gz

USER $USER

ENTRYPOINT ["ah"]