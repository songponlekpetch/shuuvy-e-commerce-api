#!/bin/sh
set -e

if [ "$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
fi


gunicorn -b 0.0.0.0:$PORT app.wsgi --timeout 120
