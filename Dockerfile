# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"


WORKDIR /app

RUN apk update

ARG DEBUG

ENV PYTHON_VERSION=3.12
ENV VENV_PATH=/app/.venv
ENV PATH="${VENV_PATH}/bin:${VENV_PATH}:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=${DEBUG}

FROM base AS poetry-build

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add --no-cache libpq-dev gcc python3-dev musl-dev libffi-dev postgresql-dev graphviz graphviz-dev

RUN python3 -m venv ${VENV_PATH} \
	&& ${VENV_PATH}/bin/pip install -U pip setuptools \
	&& ${VENV_PATH}/bin/pip install poetry==${POETRY_VERSION}

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
ARG PG_HOST
ARG PG_PORT
ARG PG_NAME
ARG PG_USER
ARG PG_PASSWORD

COPY --exclude="./src/" . .
COPY --from=poetry-build ${VENV_PATH} ${VENV_PATH}
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

ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV SECRET_KEY=${SECRET_KEY}
ENV INTERNAL_IPS=${INTERNAL_IPS}
ENV DJANGO_SETTINGS_MODULE=abarocks.settings
ENV PYTHONPATH="/app/.venv/lib/python${PYTHON_VERSION}/site-packages:/app"
ENV PG_HOST=${PG_HOST}
ENV PG_PORT=${PG_PORT}
ENV PG_NAME=${PG_NAME}
ENV PG_USER=${PG_USER}
ENV PG_PASSWORD=${PG_PASSWORD}


RUN python manage.py collectstatic --noinput

USER abarocks


EXPOSE 8000

ENTRYPOINT [ "gunicorn", "abarocks.wsgi", "-b", "0.0.0.0:8000" ]