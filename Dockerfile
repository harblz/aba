# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"

WORKDIR /usr/src/app

RUN apk update

ENV PYTHON_VERSION=3.12 VIRTUAL_ENV=/.venv PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM ghcr.io/astral-sh/uv:python3.12-alpine AS uv-build

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_PROJECT_ENVIRONMENT=${VIRTUAL_ENV} \
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
      uv sync --no-dev --group prod --locked --no-install-project; \
    fi

FROM node:23 AS npm-build

WORKDIR /usr/src/app

COPY package.json package-lock.json webpack.config.js ./
COPY src/ ./src/
COPY staticfiles/ ./staticfiles/

RUN npm install --omit=dev \
    && ./node_modules/.bin/webpack --mode development \
    && ./node_modules/.bin/sass --load-path=node_modules src/scss/aba-bulma.scss staticfiles/css/aba-bulma.css

FROM base AS run

RUN mkdir -p /usr/src/app

ARG UID=10001
RUN adduser -D -H -h "/usr/src/app" -s "/sbin/nologin" -u "${UID}" abarocks

COPY --chown=abarocks --chmod=755 . .
COPY --from=uv-build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=npm-build /usr/src/app/staticfiles/js/. ./staticfiles/js
COPY --from=npm-build /usr/src/app/staticfiles/css/. ./staticfiles/css

RUN --mount=type=secret,id=secret_key \
    --mount=type=secret,id=allowed_hosts \
    --mount=type=secret,id=internal_ips \
    --mount=type=secret,id=debug \
    chown abarocks:abarocks /usr/src/app \
    && apk add --no-cache libpq py3-gunicorn

ENV DJANGO_SETTINGS_MODULE=abarocks.settings \
    PYTHONPATH=${VIRTUAL_ENV}/lib/python${PYTHON_VERSION}/site-packages:/usr/src/app/abarocks \
    PATH=/usr/bin:${VIRTUAL_ENV}/bin:/bin:$PATH

USER abarocks

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD [ "gunicorn", "abarocks.wsgi", "--ssl-version", "SSLv3", "--bind", "0.0.0.0:8000" ]