# EC2 Development Deployment Guide

This guide provides instructions for deploying the Django backend to an EC2 instance for development/testing purposes with HTTP traffic allowed and no HTTPS enforcement.

## Prerequisites

1. An AWS EC2 instance with:
   - Ubuntu 20.04 or later
   - Docker and Docker Compose installed
   - Port 80 open in the security group

2. Your project code on the EC2 instance

## Security Group Configuration

1. Open the AWS Console and navigate to EC2 > Security Groups
2. Select the security group associated with your EC2 instance
3. Add the following inbound rules:
   - Type: HTTP (80), Source: 0.0.0.0/0
   - Type: HTTPS (443), Source: 0.0.0.0/0
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0 (optional, for direct Django access)

## Deployment Steps

1. SSH into your EC2 instance:
   ```
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. Clone the repository (if not already done):
   ```
   git clone <your-repository-url> ~/crm-backend
   cd ~/crm-backend
   ```

3. Create the .env file with your environment variables:
   ```
   nano .env
   ```
   
   Add the following variables (adjust as needed):
   ```
   # Database settings
   DB_NAME=crm_db
   DB_USER=crm_user
   DB_PASSWORD=your_secure_password
   DB_HOST=db
   
   # Redis settings
   REDIS_HOST=redis
   REDIS_PORT=6379
   
   # Email settings
   EMAIL_HOST=your_smtp_server
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your_email@example.com
   
   # Server settings
   SERVER_NAME=your_ec2_ip_or_domain
   ```

4. Create the necessary directories:
   ```
   mkdir -p ~/crm-backend/nginx/conf.d
   ```

5. Deploy the application using Docker Compose:
   ```
   cd ~/crm-backend
   docker-compose -f docker-compose.ec2-dev.yml up -d
   ```

6. Check if all services are running:
   ```
   docker-compose -f docker-compose.ec2-dev.yml ps
   ```

7. Create a superuser (if needed):
   ```
   docker-compose -f docker-compose.ec2-dev.yml exec web python manage.py createsuperuser
   ```

## Accessing the Application

- Web application: http://your-ec2-ip/
- Django admin: http://your-ec2-ip/admin/

## Troubleshooting

### Check logs

```
# Django logs
docker-compose -f docker-compose.ec2-dev.yml logs web

# Nginx logs
docker-compose -f docker-compose.ec2-dev.yml logs nginx

# Database logs
docker-compose -f docker-compose.ec2-dev.yml logs db
```

### Check Nginx configuration

```
docker-compose -f docker-compose.ec2-dev.yml exec nginx nginx -t
```

### Restart services

```
docker-compose -f docker-compose.ec2-dev.yml restart web nginx
```

## Security Notice

This configuration is intended for development and testing purposes only. It deliberately disables security features like HTTPS enforcement to facilitate easier development and testing. Do not use this configuration in a production environment.