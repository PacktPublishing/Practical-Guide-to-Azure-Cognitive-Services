#!/bin/bash

if [ ! "$ENVIRONMENT" == "development" ]; then
  # Collect static files
  echo "Collect static files"
  python manage.py collectstatic --noinput
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Load initial data into sqlite DB
# echo "Populate database with initial data"
# python manage.py loaddata initial

if [ "$ENVIRONMENT" == "development" ]; then
  # Create a superuser with default values in the dockerfile
  echo "Create local superuser"
  python manage.py createsuperuser --noinput
fi

# Start server
echo "Starting server"
if [ "$ENVIRONMENT" == "development" ]; then
  python manage.py runserver "0.0.0.0:$PORT"
else
  gunicorn -b "0.0.0.0:$PORT" --workers=2 --threads=4 --worker-class=gthread config.wsgi
fi
