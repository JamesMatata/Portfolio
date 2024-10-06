#!/bin/bash

# Exit on any error
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Create a superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'jamesmatatamule@gmail.com', '1810muleJAMES');
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
