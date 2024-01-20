#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# python manage.py runserver # development
daphne -b 0.0.0.0 -p 8000 carsbay_project.asgi:application
# gunicorn carsbay_project.wsgi:application -b 0.0.0.0:8000