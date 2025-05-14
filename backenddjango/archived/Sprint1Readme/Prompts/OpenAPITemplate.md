
Based on my investigation of the project files, I can 
provide you with a comprehensive guide on how to deploy 
the CRM Loan Management System to an EC2 instance. Here's 
a step-by-step process:

## Deploying to EC2 (Development Environment without HTTPS
)

### Step 1: Launch an EC2 Instance
1. Launch an Amazon EC2 instance (Amazon Linux 2 or Ubuntu
)
2. Configure the security group to allow:
   • TCP port 80 (HTTP)
   • TCP port 443 (HTTPS - for future use)
   • TCP port 22 (SSH)

### Step 2: Connect to Your EC2 Instance
bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip


### Step 3: Run the Setup Script
1. Copy the setup script to your EC2 instance:
bash
scp -i your-key.pem /Users/hongyuanfan/Downloads/lianV3-501a294797023b7f3fa802ddb963f1a4b1577785/backenddjango/scripts/setup_ec2_dev.sh ec2-user@your-ec2-public-ip:~


2. Make the script executable and run it:
bash
chmod +x setup_ec2_dev.sh
./setup_ec2_dev.sh


3. Log out and log back in for Docker group changes to 
take effect:
bash
exit
ssh -i your-key.pem ec2-user@your-ec2-public-ip


### Step 4: Copy Project Files to EC2
1. Create the project directory:
bash
mkdir -p ~/crm-backend


2. Copy the project files to your EC2 instance:
bash
scp -i your-key.pem -r /Users/hongyuanfan/Downloads/lianV3-501a294797023b7f3fa802ddb963f1a4b1577785/backenddjango/* ec2-user@your-ec2-public-ip:~/crm-backend/


### Step 5: Create Environment File
1. Create a .env file in the project root:
bash
cd ~/crm-backend
nano .env


2. Add the following content (adjust values as needed):
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
SERVER_NAME=your-ec2-public-ip


### Step 6: Create Required Directories
bash
mkdir -p ~/crm-backend/nginx/conf.d
mkdir -p ~/crm-backend/logs


### Step 7: Deploy the Application
1. Make the deployment script executable:
bash
chmod +x ~/crm-backend/scripts/deploy_ec2_dev.sh


2. Run the deployment script:
bash
cd ~/crm-backend
./scripts/deploy_ec2_dev.sh


This script will:
• Build and start the Docker containers
• Apply database migrations
• Collect static files

### Step 8: Access the Application
Your application will be available at:
http://your-ec2-public-ip/


Admin interface:
http://your-ec2-public-ip/admin/


## Troubleshooting

### Check container logs
bash
docker-compose -f docker-compose.ec2-dev.yml logs -f


### Check specific service logs
bash
docker-compose -f docker-compose.ec2-dev.yml logs web
docker-compose -f docker-compose.ec2-dev.yml logs nginx


### Check Nginx configuration
bash
docker-compose -f docker-compose.ec2-dev.yml exec nginx nginx -t


### Restart services
bash
docker-compose -f docker-compose.ec2-dev.yml restart


### Rebuild and restart
bash
docker-compose -f docker-compose.ec2-dev.yml up -d --build


## Important Notes
• This deployment is configured for development/testing 
purposes only
• HTTP traffic is allowed without HTTPS redirection
• No SSL certificate is required
• Django's security settings are configured to allow HTTP 
traffic
• Do NOT use this configuration for production 
environments

The deployment uses the settings_ec2.py configuration 
which disables HTTPS enforcement and sets ALLOWED_HOSTS to
accept connections from any host, making it suitable for 
development and testing but not for production use.
