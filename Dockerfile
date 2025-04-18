# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"


WORKDIR /usr/src/app

RUN apk update


ARG DEBUG

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/usr/src/app/.venv PATH="${VIRTUAL_ENV}/bin:${VIRTUAL_ENV}:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBUG=${DEBUG}

FROM base AS pg-config

RUN --mount=type=secret,id=postgres_db \
    --mount=type=secret,id=postgres_password \
    --mount=type=secret,id=postgres_user \
    --mount=type=secret,id=postgres_port \
    --mount=type=secret,id=postgres_host

ENV POSTGRES_HOST="$(cat /run/secrets/POSTGRES_HOST"
ENV POSTGRES_DB="$(cat /run/secrets/POSTGRES_DB"
ENV POSTGRES_PORT="$(cat /run/secrets/POSTGRES_PORT"
ENV POSTGRES_USER="$(cat /run/secrets/POSTGRES_USER"
ENV POSTGRES_PASSWORD="$(cat /run/secrets/POSTGRES_PASSWORD"

RUN mkdir pgconf \
    && touch ./pgconf/.pg_service.conf \
    && touch ./pgconf/.pgpass \
    && echo [aba.rocks] >> ./pgconf/.pg_service.conf \
    && echo host=${POSTGRES_HOST} >> ./pgconf/.pg_service.conf \
    && echo dbname=${POSTGRES_DB} >> ./pgconf/.pg_service.conf \
    && echo port=${POSTGRES_PORT} >> ./pgconf/.pg_service.conf \
    && echo "${POSTGRES_HOST}:${POSTGRES_PORT}:${POSTGRES_DB}:${POSTGRES_USER}:${POSTGRES_PASSWORD}" >> ./pgconf/.pgpass


FROM base AS poetry-build

ENV POETRY_NO_INTERACTION=1 POETRY_VIRTUALENVS_IN_PROJECT=true POETRY_VIRTUALENVS_PATH=${VIRTUAL_ENV} \
    POETRY_VIRTUALENVS_CREATE=true POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add --no-cache gcc python3-dev musl-dev libffi-dev postgresql-dev graphviz graphviz-dev jpeg-dev zlib-dev g++ \
    freetype-dev jpeg-dev

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

WORKDIR /usr/src/app

COPY package.json package-lock.json webpack.config.js ./
COPY src/ ./src/
COPY staticfiles/ ./staticfiles/

RUN npm install --omit=dev
RUN npm run pack
RUN npm run build-bulma


FROM base AS run

COPY --exclude="./src/" . .
COPY --from=pg-config /usr/src/app/pgconf ./
COPY --from=poetry-build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=npm-build /usr/src/app/staticfiles/js ./staticfiles/js
COPY --from=npm-build /usr/src/app/staticfiles/css ./staticfiles/css

RUN --mount=type=secret,id=debug \
    --mount=type=secret,id=secret_key \
    --mount=type=secret,id=allowed_hosts \
    --mount=type=secret,id=internal_ips

RUN apk add --no-cache libpq py3-gunicorn && pwd

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/usr/src/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    abarocks \
    && chown -R abarocks:abarocks /usr/src/app/

ENV DJANGO_SETTINGS_MODULE=abarocks.settings PYTHONPATH=/usr/src/app/.venv/lib/python${PYTHON_VERSION}/site-packages:/app

RUN python manage.py collectstatic --noinput

USER abarocks


EXPOSE 8000

CMD [ "gunicorn", "abarocks.wsgi", "-b", "0.0.0.0:8000" ]