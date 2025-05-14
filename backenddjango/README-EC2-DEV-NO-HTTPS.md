# EC2 Development Deployment Guide (No HTTPS)

This guide explains how to deploy the CRM Loan Management System to an EC2 instance for development purposes without HTTPS enforcement.

## Prerequisites

- An AWS EC2 instance running Amazon Linux 2 or Ubuntu
- Docker and Docker Compose installed on the EC2 instance
- Basic knowledge of AWS EC2 and Docker

## Step 1: Configure EC2 Security Group

Ensure your EC2 security group allows:
- TCP port 80 from 0.0.0.0/0 (for HTTP access)
- TCP port 443 from 0.0.0.0/0 (for future HTTPS if needed)
- TCP port 22 from your IP (for SSH access)

AWS CLI commands to set this up:
```bash
aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
```

## Step 2: Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

## Step 3: Install Docker and Docker Compose

For Amazon Linux 2:
```bash
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

For Ubuntu:
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Log out and log back in for the group changes to take effect.

## Step 4: Clone the Repository

```bash
mkdir -p ~/crm-backend
cd ~/crm-backend
git clone https://github.com/your-username/your-repo.git .
```

## Step 5: Create Directory Structure

```bash
mkdir -p ~/crm-backend/nginx/conf.d
mkdir -p ~/crm-backend/logs
```

## Step 6: Create Environment File

Create a `.env` file in the project root:

```bash
cat > .env << EOF
# Database settings
DB_NAME=crm_db
DB_USER=crm_user
DB_PASSWORD=your_secure_password
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
```

Edit the file to set your actual values.

## Step 7: Deploy the Application

```bash
cd ~/crm-backend
./scripts/deploy_ec2_dev.sh
```

This script will:
1. Build and start the Docker containers
2. Apply database migrations
3. Collect static files

## Step 8: Access the Application

Your application will be available at:
```
http://your-ec2-public-ip/
```

Admin interface:
```
http://your-ec2-public-ip/admin/
```

## Important Notes

- This deployment is configured for development/testing purposes only
- HTTP traffic is allowed without redirection to HTTPS
- No SSL certificate is required
- Django's security settings are configured to allow HTTP traffic
- Do NOT use this configuration for production environments

## Useful Commands

View logs:
```bash
docker-compose -f docker-compose.ec2-dev.yml logs -f
```

Restart services:
```bash
docker-compose -f docker-compose.ec2-dev.yml restart
```

Rebuild and restart:
```bash
docker-compose -f docker-compose.ec2-dev.yml up -d --build
```

Check service status:
```bash
docker-compose -f docker-compose.ec2-dev.yml ps
```