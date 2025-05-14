#!/bin/bash

set -e

# Wait for the database to be ready
if [ "$DATABASE_URL" ]; then
  echo "Waiting for database to be ready..."
  python -m scripts.wait_for_db
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Generate OpenAPI schema files
echo "Generating OpenAPI schema files..."
python manage.py spectacular --file schema.yml
python manage.py spectacular --file schema.yaml
python manage.py spectacular --file schema.json --format openapi-json

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn crm_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
