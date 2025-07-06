# syntax=docker/dockerfile:1.7-labs
FROM python:3.12.3-bookworm AS base
LABEL authors="nullandvoid"

ADD ../ /workspace/abarocks
WORKDIR /workspace/abarocks

RUN apt-get update 

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/venv PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM base AS workspace

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get install -y gcc python3-dev musl-dev libffi-dev libpq-dev graphviz  \
    graphviz-dev libjpeg-dev zlib1g zlib1g-dev g++ libfreetype6-dev \
    libturbojpeg0-dev gunicorn


ENV DJANGO_SETTINGS_MODULE=abarocks.settings \
    PYTHONPATH=${VIRTUAL_ENV}/python${PYTHON_VERSION}/site-packages:/workspace/abarocks \
    PATH=${VIRTUAL_ENV}/bin:/usr/bin:/bin:/home/abarocks:$PATH \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=${VIRTUAL_ENV} UV_CACHE_DIR=/home/abarocks/uv-cache/

CMD ["uv", "run", "python", "manage.py", "runserver_plus", "0.0.0.0:8000"]
