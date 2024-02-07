# syntax=docker/dockerfile:1
FROM --platform="linux/amd64" python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y build-essential python3-dev && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get install -y vim

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./start-django.sh /start-django
RUN chmod +x /start-django

COPY . /code/
