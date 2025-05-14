#!/bin/bash

# Exit on error
set -e

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create directories
echo "Creating project directories..."
mkdir -p ~/crm-backend/nginx/conf.d
mkdir -p ~/crm-backend/nginx/ssl

# Create self-signed SSL certificate (for testing)
echo "Creating self-signed SSL certificate..."
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ~/crm-backend/nginx/ssl/key.pem \
  -out ~/crm-backend/nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "========================================================"
echo "EC2 instance setup complete!"
echo "========================================================"
echo "Next steps:"
echo "1. Log out and log back in for Docker group changes to take effect"
echo "2. Copy your project files to ~/crm-backend/"
echo "3. Create .env.prod file from .env.prod.example"
echo "4. Start the application with: docker-compose -f docker-compose.prod.yml up -d"
echo "5. For a real SSL certificate, use Let's Encrypt with certbot"
echo "========================================================"