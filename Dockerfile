# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"

WORKDIR /usr/src/app

RUN apk update

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/usr/src/app/.venv PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


FROM base AS pg-config

ARG POSTGRES_HOST
ENV POSTGRES_HOST=${POSTGRES_HOST}

RUN --mount=type=secret,id=postgres_db \
    --mount=type=secret,id=postgres_password \
    --mount=type=secret,id=postgres_user \
    --mount=type=secret,id=postgres_port \
    --mount=type=secret,id=postgres_host \
    POSTGRES_DB="$(cat /run/secrets/postgres_db)" \
    && POSTGRES_PASSWORD="$(cat /run/secrets/postgres_password)" \
    && POSTGRES_USER=$(cat /run/secrets/postgres_user) \
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

FROM ghcr.io/astral-sh/uv:python3.12-alpine AS uv-build

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_PROJECT_ENVIRONMENT=./.venv \
    UV_CACHE_DIR=/opt/uv-cache/

RUN apk add --no-cache gcc python3-dev musl-dev libffi-dev postgresql-dev postgresql-libs graphviz  \
    graphviz-dev jpeg-dev zlib-dev g++ freetype-dev jpeg-dev libjpeg

RUN --mount=type=secret,id=debug \
    --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    if [ "$(cat /run/secrets/debug)" = "True" ] ; then \
      uv sync --locked --no-install-project; \
    else \
      uv sync --no-dev --locked --no-install-project; \
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

RUN mkdir -p /usr/src/app

ARG UID=10001
RUN adduser -D -H -h "/usr/src/app" -s "/sbin/nologin" -u "${UID}" abarocks

COPY --chown=abarocks --chmod=755 . .
COPY --from=uv-build /.venv ${VIRTUAL_ENV}
COPY --from=npm-build /usr/src/app/staticfiles/js/. ./staticfiles/js
COPY --from=npm-build /usr/src/app/staticfiles/css/. ./staticfiles/css

COPY --chown=abarocks --chmod=600 --from=pg-config /usr/src/app/.pg_service.conf ./
COPY --chown=abarocks --chmod=600 --from=pg-config /usr/src/app/.pgpass ./

RUN --mount=type=secret,id=secret_key \
    --mount=type=secret,id=allowed_hosts \
    --mount=type=secret,id=internal_ips \
    --mount=type=secret,id=debug \
    chown abarocks:abarocks /usr/src/app

RUN apk add --no-cache libpq py3-gunicorn && pwd

ENV DJANGO_SETTINGS_MODULE=abarocks.settings \
    PYTHONPATH=/usr/src/app/.venv/lib/python${PYTHON_VERSION}/site-packages:/usr/src/app/abarocks \
    PATH=/usr/src/app/.venv/bin:/usr/bin:/bin:$PATH

RUN pip list

USER abarocks

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "gunicorn", "abarocks.wsgi", "--bind", "0.0.0.0:8000" ]