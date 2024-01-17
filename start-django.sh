#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# python manage.py runserver # development
daphne -b 0.0.0.0 -p 8000 carsbay_project.asgi:application
# python -m gunicorn carsbay_project.asgi:application -k uvicorn.workers.UvicornWorker