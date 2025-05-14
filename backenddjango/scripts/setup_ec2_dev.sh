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

# Configure EC2 Security Group
echo "========================================================"
echo "IMPORTANT: Configure EC2 Security Group"
echo "========================================================"
echo "Please ensure your EC2 security group allows:"
echo "- TCP port 80 from 0.0.0.0/0"
echo "- TCP port 443 from 0.0.0.0/0"
echo "- TCP port 22 from your IP (for SSH access)"
echo ""
echo "AWS CLI commands to set this up:"
echo "aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0"
echo "aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 443 --cidr 0.0.0.0/0"
echo "========================================================"

echo "========================================================"
echo "EC2 instance setup complete!"
echo "========================================================"
echo "Next steps:"
echo "1. Log out and log back in for Docker group changes to take effect"
echo "2. Copy your project files to ~/crm-backend/"
echo "3. Create .env file with your environment variables"
echo "4. Start the application with: docker-compose -f docker-compose.ec2.yml up -d"
echo "========================================================"