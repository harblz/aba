# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"


WORKDIR /app

RUN apk update

ARG DEBUG

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/app/.venv PATH="${VIRTUAL_ENV}/bin:${VIRTUAL_ENV}:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBUG=${DEBUG}

FROM base AS poetry-build

ENV POETRY_NO_INTERACTION=1 POETRY_VIRTUALENVS_IN_PROJECT=true POETRY_VIRTUALENVS_PATH=${VIRTUAL_ENV} \
    POETRY_VIRTUALENVS_CREATE=true POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add --no-cache libpq-dev gcc python3-dev musl-dev libffi-dev postgresql-dev graphviz graphviz-dev

RUN python3 -m venv ${VIRTUAL_ENV} \
	&& pip install -U pip setuptools \
	&& pip install poetry

RUN which pip

ENV POETRY_CACHE_DIR=/tmp/.cache

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=${POETRY_CACHE_DIR}
RUN if [ "$DEBUG" = "True" ]; then \
  poetry install --with dev; \
else \
  poetry install --with prod; \
fi

FROM node:23 AS npm-build

WORKDIR /app
COPY package.json package-lock.json webpack.config.js ./
COPY src/ ./src/
COPY staticfiles/ ./staticfiles/

RUN npm install --omit=dev \
    && npm run pack \
    && npm run build-bulma

FROM base AS run

ARG ALLOWED_HOSTS
ARG SECRET_KEY
ARG INTERNAL_IPS
ARG POSTGRES_NAME
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST

COPY --exclude="./src/" . .
COPY --from=poetry-build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=npm-build /app/staticfiles/js ./staticfiles/js
COPY --from=npm-build /app/staticfiles/css ./staticfiles/css


RUN apk add --no-cache libpq py3-gunicorn

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    abarocks \
    && chown -R abarocks:abarocks /app/

ENV ALLOWED_HOSTS=${ALLOWED_HOSTS} SECRET_KEY=${SECRET_KEY} INTERNAL_IPS=${INTERNAL_IPS} \
    DJANGO_SETTINGS_MODULE=abarocks.settings PYTHONPATH="/app/.venv/lib/python${PYTHON_VERSION}/site-packages:/app"
RUN touch .pg_service.conf \
    && touch .pgpass \
    && echo [aba.rocks] >> .pg_service.conf \
    && echo host=${POSTGRES_HOST} >> .pg_service.conf \
    && echo dbname=${POSTGRES_NAME} >> .pg_service.conf \
    && echo port=5432 >> .pg_service.conf \
    && echo "${POSTGRES_HOST}:5432:${POSTGRES_NAME}:${POSTGRES_USER}:${POSTGRES_PASSWORD}" >> .pgpass

RUN python manage.py collectstatic --noinput

USER abarocks


EXPOSE 8000

ENTRYPOINT [ "gunicorn", "abarocks.wsgi", "-b", "0.0.0.0:8000" ]