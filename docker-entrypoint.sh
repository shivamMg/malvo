#!/bin/bash

python manage.py migrate

if [ "$MALVO_PLATFORM" == "prod" ]; then
    python manage.py collectstatic --noinput
fi

python manage.py createadmin $MALVO_ADMIN_PASSWORD

gunicorn malvo.wsgi:application --name malvo --bind 0.0.0.0:8001 --workers 3 \
    --log-file=/code/data/logs/gunicorn/gunicorn.log \
    --access-logfile=/code/data/logs/gunicorn/access.log \
    --reload
