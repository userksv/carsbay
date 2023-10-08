#!/usr/bin/env bash
# exit on error
set -o errexit

python3 manage.py collectstatic 