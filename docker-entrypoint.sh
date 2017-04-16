#!/bin/bash

python manage.py migrate

if [ "$MALVO_PLATFORM" == "prod" ]; then
    python manage.py collectstatic --noinput
elif [ "$MALVO_PLATFORM" == "dev" ]; then
    # Copy Admin static assets
    cp -r /usr/local/lib/python3.5/site-packages/django/contrib/admin/static/admin /code/malvo/static/admin
fi

python manage.py createadmin $MALVO_ADMIN_PASSWORD

gunicorn malvo.wsgi:application --name malvo --bind 0.0.0.0:8001 --workers 3 \
    --log-file=/code/data/logs/gunicorn/gunicorn.log \
    --access-logfile=/code/data/logs/gunicorn/access.log \
    --reload
