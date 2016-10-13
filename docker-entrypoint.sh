#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

# Prepare log files
touch /code/data/logs/gunicorn.log
touch /code/data/logs/gunicorn-access.log
touch /code/data/logs/nginx-access.log
touch /code/data/logs/nginx-error.log

# python manage.py runserver 0.0.0.0:8001
gunicorn malvo.wsgi:application --name malvo --bind 0.0.0.0:8001 --workers 3 \
    --log-file=/code/data/logs/gunicorn.log \
    --access-logfile=/code/data/logs/gunicorn-access.log \
    --reload
