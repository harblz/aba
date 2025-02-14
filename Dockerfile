# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-alpine3.20 AS base
LABEL authors="nullandvoid"

WORKDIR /app

RUN apk update

ENV PYTHON_VERSION=3.12 \
	VENV_PATH=/app/.venv \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

FROM base AS poetry-build

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=true \
	POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add --no-cache libpq-dev gcc python3-dev musl-dev libffi-dev \
    && apk add postgresql-dev

RUN python3 -m venv ${VENV_PATH} \
	&& ${VENV_PATH}/bin/pip install -U pip setuptools \
	&& ${VENV_PATH}/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${VENV_PATH}/bin"
ENV POETRY_CACHE_DIR=/opt/.cache

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=${POETRY_CACHE_DIR}
RUN poetry install --no-root --with prod

FROM node:23 AS npm-build

WORKDIR /app
COPY package.json package-lock.json webpack.config.js ./
COPY src/ ./src/
COPY staticfiles/ ./staticfiles/

RUN npm install --omit=dev \
    && npm run pack \
    && npm run build-bulma

FROM base AS run

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
    appuser

ENV PATH="/app/.venv/bin:$PATH"
    DEBUG=False

RUN python manage.py collectstatic --noinput

USER appuser


EXPOSE 8000
ENTRYPOINT ["gunicorn", "abarocks.wsgi"]