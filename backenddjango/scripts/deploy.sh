#!/bin/bash

# Exit on error
set -e

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "Error: .env.prod file not found!"
    echo "Please create .env.prod file from .env.prod.example"
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Apply migrations
echo "Applying database migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo "========================================================"
echo "Deployment complete!"
echo "========================================================"
echo "Your application should now be running at:"
echo "https://$(grep SERVER_NAME .env.prod | cut -d '=' -f2)"
echo "========================================================"
