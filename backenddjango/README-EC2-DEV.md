# EC2 Development Deployment Guide

This guide provides instructions for deploying the Django backend project to an EC2 instance for development/testing purposes, with HTTP allowed and no HTTPS enforcement.

## Prerequisites

- An AWS account with EC2 access
- An EC2 instance running Amazon Linux 2
- Basic knowledge of AWS EC2 and security groups

## Setup Instructions

### 1. Configure EC2 Security Group

Allow traffic on ports 80 and 443 from anywhere:

```bash
# Replace YOUR_SECURITY_GROUP_ID with your actual security group ID
aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id YOUR_SECURITY_GROUP_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
```

Or use the AWS Management Console:
1. Go to EC2 > Security Groups
2. Select your security group
3. Edit inbound rules
4. Add rules for HTTP (80) and HTTPS (443) with source 0.0.0.0/0

### 2. Set Up the EC2 Instance

SSH into your EC2 instance and run the setup script:

```bash
# Copy the setup script to your EC2 instance
scp -i your-key.pem scripts/setup_ec2_dev.sh ec2-user@your-ec2-instance-ip:~

# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-instance-ip

# Make the script executable and run it
chmod +x setup_ec2_dev.sh
./setup_ec2_dev.sh
```

### 3. Deploy the Application

```bash
# Log out and log back in for Docker group changes to take effect
exit
ssh -i your-key.pem ec2-user@your-ec2-instance-ip

# Create project directory
mkdir -p ~/crm-backend

# Copy project files to EC2
scp -i your-key.pem -r ./* ec2-user@your-ec2-instance-ip:~/crm-backend/

# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-instance-ip

# Navigate to project directory
cd ~/crm-backend

# Create .env file with your environment variables
# Example:
cat > .env << EOL
DB_NAME=crm_db
DB_USER=crm_user
DB_PASSWORD=your_secure_password
DB_HOST=db
REDIS_HOST=redis
SERVER_NAME=your-ec2-instance-ip
EOL

# Start the application
docker-compose -f docker-compose.ec2.yml up -d
```

### 4. Access the Application

Once deployed, you can access the application at:

```
http://your-ec2-instance-ip
```

## Important Notes

- This deployment is configured for development/testing purposes only
- HTTP traffic is allowed without HTTPS redirection
- No SSL certificate is required
- `DEBUG` is set to `False` as requested, but all security settings related to HTTPS are disabled
- `ALLOWED_HOSTS` is set to `['*']` to accept connections from any host

## Troubleshooting

### Check container logs

```bash
docker-compose -f docker-compose.ec2.yml logs -f
```

### Check Nginx configuration

```bash
docker-compose -f docker-compose.ec2.yml exec nginx nginx -t
```

### Restart services

```bash
docker-compose -f docker-compose.ec2.yml restart
```