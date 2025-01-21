#!/usr/bin/env bash
set -o errexit
pip install --upgrade pip
pip install -r requirements_py311.txt
python manage.py collectstatic --no-input
python manage.py migrate
