#!/bin/bash


# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start Gunicorn
# exec gunicorn trryFixBackend.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 
