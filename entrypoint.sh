#!/bin/sh

./manage.py collectstatic --noinput
./manage.py migrate --noinput

exec "$@"