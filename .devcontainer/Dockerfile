# syntax=docker/dockerfile:1.7-labs
FROM python:3.12.3-bookworm AS base
LABEL authors="nullandvoid"

ADD ../ /workspace/abarocks
WORKDIR /workspace/abarocks

RUN apt-get update

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/venv PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/venv UV_CACHE_DIR=/opt/uv-cache

FROM base AS pg-config

ARG POSTGRES_HOST
ENV POSTGRES_HOST=${POSTGRES_HOST}
WORKDIR /root

RUN --mount=type=secret,id=postgres_db \
    --mount=type=secret,id=postgres_password \
    --mount=type=secret,id=postgres_user \
    --mount=type=secret,id=postgres_port \
    --mount=type=secret,id=postgres_host \
    POSTGRES_DB="$(cat /run/secrets/postgres_db)" \
    && POSTGRES_PASSWORD="$(cat /run/secrets/postgres_password)" \
    && POSTGRES_USER="$(cat /run/secrets/postgres_user)" \
    && POSTGRES_PORT="$(cat /run/secrets/postgres_port)" \
    && touch .pg_service.conf \
    && touch .pgpass \
    && echo "[aba.rocks]" >> .pg_service.conf \
    && echo "host=${POSTGRES_HOST}" >> .pg_service.conf \
    && echo "user=${POSTGRES_USER}" >> .pg_service.conf \
    && echo "dbname=${POSTGRES_DB}" >> .pg_service.conf \
    && echo "port=${POSTGRES_PORT}" >> .pg_service.conf \
    && echo "${POSTGRES_HOST}:${POSTGRES_PORT}:${POSTGRES_DB}:${POSTGRES_USER}:${POSTGRES_PASSWORD}" >> .pgpass \
    && chmod 600 .pgpass \
    && chmod 600 .pg_service.conf

FROM base AS workspace

COPY --from=pg-config /root/.pg_service.conf /root
COPY --from=pg-config /root/.pgpass /root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get install -y gcc python3-dev musl-dev libffi-dev libpq-dev graphviz  \
    graphviz-dev libjpeg-dev zlib1g zlib1g-dev g++ libfreetype6-dev \
    libturbojpeg0-dev gunicorn

ENV DJANGO_SETTINGS_MODULE=abarocks.settings \
    PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages:/workspace/abarocks \
    PATH=/venv/bin:/usr/bin:/bin:$PATH
