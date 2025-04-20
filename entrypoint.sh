#!/bin/sh

./manage.py collectstatic --noinput

exec "$@"