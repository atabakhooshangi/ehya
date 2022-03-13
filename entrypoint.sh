#!/bin/sh







python manage.py makemigrations --noinput && python manage.py migrate --noinput &&  python manage.py collectstatic --noinput && supervisord -c supervisord.conf && python manage.py collectstatic








