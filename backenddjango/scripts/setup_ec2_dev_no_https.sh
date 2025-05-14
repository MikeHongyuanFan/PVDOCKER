#!/bin/bash

# Setup script for EC2 development environment without HTTPS enforcement
# This script should be run on the EC2 instance

set -e

# Create directory structure
echo "Creating directory structure..."
mkdir -p ~/crm-backend
cd ~/crm-backend

# Clone the repository if it doesn't exist
if [ ! -d ".git" ]; then
  echo "Cloning repository..."
  git clone https://github.com/your-username/your-repo.git .
fi

# Create necessary directories
echo "Creating Nginx directories..."
mkdir -p ~/crm-backend/nginx/conf.d
mkdir -p ~/crm-backend/logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
  echo "Creating .env file..."
  cat > .env << EOF
# Database settings
DB_NAME=crm_db
DB_USER=crm_user
DB_PASSWORD=change_this_password
DB_HOST=db

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Email settings
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@example.com

# Server settings
SERVER_NAME=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
EOF
  echo "Created .env file. Please edit it with your actual settings."
fi

# Deploy with Docker Compose
echo "Deploying with Docker Compose..."
docker-compose -f docker-compose.ec2-dev.yml up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py migrate

# Create superuser if needed
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Creating superuser..."
  docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py createsuperuser
fi

# Print success message
echo "======================================================"
echo "Setup complete!"
echo "Your application is now running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/"
echo "Admin interface: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/admin/"
echo "======================================================"
echo "To view logs:"
echo "docker-compose -f docker-compose.ec2-dev.yml logs -f"
echo "======================================================"