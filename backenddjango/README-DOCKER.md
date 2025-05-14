# CRM Loan Management System - Docker Deployment Guide

This guide explains how to deploy the CRM Loan Management System backend using Docker.

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (to clone the repository)

## Local Development Setup

### 1. Create Environment File

Copy the example environment file and modify it with your settings:

```bash
cp .env.example .env
```

Edit the `.env` file to set your environment-specific variables.

### 2. Build and Start the Containers

```bash
docker-compose up --build
```

This will:
- Build the Docker images
- Start the PostgreSQL database
- Start the Redis service
- Start the Django web server
- Start the Celery worker and beat scheduler

### 3. Access the Application

The application will be available at:
- API: http://localhost:8000/api/
- Admin interface: http://localhost:8000/admin/
- API documentation: http://localhost:8000/swagger/

## Docker Commands

### Start the Services

```bash
docker-compose up
```

### Start in Detached Mode

```bash
docker-compose up -d
```

### Stop the Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f
```

### View Logs for a Specific Service

```bash
docker-compose logs -f web
```

### Run Django Management Commands

```bash
docker-compose exec web python manage.py <command>
```

Examples:
```bash
# Create a superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test

# Make migrations
docker-compose exec web python manage.py makemigrations
```

## Production Deployment

For production deployment, consider the following:

1. Use a proper secret key
2. Set DEBUG=0
3. Configure proper ALLOWED_HOSTS
4. Set up HTTPS with a reverse proxy (Nginx or Traefik)
5. Configure email settings
6. Set up proper database credentials

## Deployment Options

### AWS Elastic Container Service (ECS)

1. Create an ECR repository for your Docker image
2. Push your Docker image to ECR
3. Create an ECS cluster
4. Define a task definition with your container
5. Create a service to run your task
6. Set up an Application Load Balancer
7. Configure auto-scaling

### AWS Elastic Beanstalk

1. Install the EB CLI
2. Initialize your EB application
3. Create an environment
4. Deploy your application

```bash
eb init
eb create
eb deploy
```

### Railway

1. Install the Railway CLI
2. Login to Railway
3. Link your project
4. Deploy your application

```bash
railway login
railway link
railway up
```

## Monitoring and Maintenance

- Set up CloudWatch or Prometheus for monitoring
- Configure log aggregation with ELK stack or CloudWatch Logs
- Set up database backups
- Configure auto-scaling based on load

## Security Considerations

- Use environment variables for sensitive information
- Implement proper authentication and authorization
- Set up a Web Application Firewall (WAF)
- Configure network security groups
- Regularly update dependencies
