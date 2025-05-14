#!/bin/bash

# Exit on error
set -e

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file with required environment variables"
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
docker-compose -f docker-compose.ec2-dev.yml up -d --build

# Apply migrations
echo "Applying database migrations..."
docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py collectstatic --noinput

echo "========================================================"
echo "Deployment complete!"
echo "========================================================"
echo "Your application should now be running at:"
echo "http://$(grep SERVER_NAME .env | cut -d '=' -f2)"
echo "========================================================"