# CRM Loan Management System - Production Deployment Guide

This guide explains how to deploy the CRM Loan Management System to an AWS EC2 instance.

## Prerequisites

- An AWS account
- Basic knowledge of AWS EC2, SSH, and Docker
- A domain name (optional, but recommended for production)

## Step 1: Launch an EC2 Instance

1. Log in to the AWS Management Console
2. Navigate to EC2 and click "Launch Instance"
3. Choose Amazon Linux 2023 or Ubuntu Server 22.04
4. Select t2.medium or larger (2+ vCPUs, 4+ GB RAM)
5. Configure storage: Add at least 30GB of EBS storage
6. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
7. Launch the instance and download the key pair

## Step 2: Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

## Step 3: Set Up the EC2 Instance

Run the setup script:

```bash
# Copy the setup script to the EC2 instance
scp -i your-key.pem scripts/setup_ec2.sh ec2-user@your-ec2-public-ip:~/

# SSH into the instance
ssh -i your-key.pem ec2-user@your-ec2-public-ip

# Make the script executable and run it
chmod +x ~/setup_ec2.sh
~/setup_ec2.sh

# Log out and log back in for Docker group changes to take effect
exit
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

## Step 4: Transfer Your Project Files

```bash
# Create a zip archive of your project
cd /path/to/your/project
zip -r crm-backend.zip backenddjango

# Copy the zip file to the EC2 instance
scp -i your-key.pem crm-backend.zip ec2-user@your-ec2-public-ip:~/

# SSH into the instance and extract the files
ssh -i your-key.pem ec2-user@your-ec2-public-ip
unzip crm-backend.zip
mv backenddjango/* ~/crm-backend/
cd ~/crm-backend
```

## Step 5: Configure Production Environment

1. Create the production environment file:

```bash
cp .env.prod.example .env.prod
nano .env.prod
```

2. Update the following variables:
   - `SECRET_KEY`: Generate a secure random key
   - `SERVER_NAME`: Your domain name or EC2 public IP
   - `DB_PASSWORD`: Set a secure database password
   - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`: Your email credentials
   - `ALLOWED_HOSTS`: Your domain name and EC2 public IP
   - `CORS_ALLOWED_ORIGINS`: Your frontend domain(s)

## Step 6: Deploy the Application

Run the deployment script:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Step 7: Set Up SSL with Let's Encrypt (Optional)

If you have a domain name pointing to your EC2 instance:

```bash
# Install certbot
sudo yum install -y certbot

# Stop nginx
docker-compose -f docker-compose.prod.yml stop nginx

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Copy certificates to nginx directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ~/crm-backend/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ~/crm-backend/nginx/ssl/key.pem

# Restart nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

## Step 8: Set Up Automatic Backups

1. Create a cron job for daily backups:

```bash
crontab -e
```

2. Add the following line to run backups daily at 2 AM:

```
0 2 * * * cd ~/crm-backend && ./scripts/backup.sh
```

## Monitoring and Maintenance

### View Logs

```bash
# View logs for all services
docker-compose -f docker-compose.prod.yml logs

# View logs for a specific service
docker-compose -f docker-compose.prod.yml logs web
```

### Restart Services

```bash
# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Restart a specific service
docker-compose -f docker-compose.prod.yml restart web
```

### Update the Application

```bash
# Pull the latest changes
git pull

# Rebuild and restart the containers
docker-compose -f docker-compose.prod.yml up -d --build
```

## Troubleshooting

### Database Connection Issues

Check if the database is running:

```bash
docker-compose -f docker-compose.prod.yml ps db
```

### Web Server Issues

Check the web server logs:

```bash
docker-compose -f docker-compose.prod.yml logs web
```

### Nginx Issues

Check the Nginx logs:

```bash
docker-compose -f docker-compose.prod.yml logs nginx
```
