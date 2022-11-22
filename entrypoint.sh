#!/bin/sh
pip install mysqlclient
cd infraction_core/
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
gunicorn infraction_core.wsgi:application --bind 0.0.0.0 --timeout 90