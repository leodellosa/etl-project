# 🚀 Getting Started with the ETL Project

This guide will help you set up and run the Django project using Docker.
---
## 📦 Prerequisites
### Make sure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- Optional: [Git](https://git-scm.com/) for cloning the repo
---

## How to Run Locally
Follow the steps below to set up the project on your local machine.
## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x
- Node.js (for Tailwind CSS)
- Git (for version control)

### 1. Clone the Repository
#### First, clone the repository to your local machine.
- git clone https://github.com/leodellosa/etl-project.git
- cd etl-project

### 2. Set Up a Virtual Environment
#### Create and activate a Python virtual environment:
- python -m venv .venv
- source .venv/scripts/activate

### 3. Install Dependencies
#### Install Python dependencies via pip:
- pip install -r requirements.txt

### 4. Set Up Tailwind CSS
#### Since Tailwind CSS is used for styling, run the following to set up Tailwind:
- cd etl_project
- python manage.py tailwind install

### 5. Set Up the Database
#### Run the following commands to set up the database:
- python manage.py makemigrations
- python manage.py migrate

### 6. Create a superuser account to access the Django admin:
#### Follow the prompts to set up the superuser credentials.
- python manage.py createsuperuser

### 7. Collect Static Files
### Run the following to collect all static files:
- python manage.py collectstatic

### 8. Run the Development Server
#### Now, you can run the Django development server:
- python manage.py runserver
- The application will now be available at http://localhost:8000.

### 9. Tailwind CSS
#### For development with hot-reloading:
- open new gitbash terminal
- python manage.py tailwind start

#### If you're preparing for production:
- python manage.py tailwind build
- python manage.py collectstatic

### 10. Accessing Django Admin
-  Once the server is running, you can access the Django Admin by visiting http://localhost:8000/admin/ and logging in with the superuser credentials you just created.

### 11. Stopping the Application
- To stop the development server, simply press Ctrl+C in your terminal.



## How to run Via docker
### 1. Clone the Repository
#### First, clone the repository to your local machine.
- git clone https://github.com/leodellosa/etl-project.git

## 2. Go to project directory
- cd etl-project

## 3. Build the Docker Image
- docker build -t etl-project .

## 4. Run the Application
- docker run -d -p 8087:8087 etl-project

### This will:
- Apply migrations
- Start the Django development server at http://localhost:8087



## How to deploy to AWS ECS Fargate
- Go to AWS IAM then create user role
- Create security key
- Go to AWS ECR (https://ap-southeast-1.console.aws.amazon.com/ecr/private-registry/repositories?region=ap-southeast-1)
- Create repository name it test/ld then create
- Click on the created repository the View push commands in AWS ECR
- Click on Getting started with AWS ECR (https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html)
- Check AWS Command Line Interface installation 
- Download and run the AWS CLI MSI installer for Windows (64-bit)
- To check if successfully installed the aws cli
- Open windows powershell / cmd then type 
aws --version
- Then run this
aws configure
username - "Your desired username"
password- "Your desired password"
- Go back to AWS ECR insired your reposritory click and follow view push commands
- Copy and run all the push commands one by one in you powershell / cmd
- Refresh to check if successful deployed


## 🧭 Deploying Your ECR Image to ECS via the AWS Console
### ✅ 1. Open the ECS Console
- Go to: https://console.aws.amazon.com/ecs/
### ✅ 2. Create a Cluster
- Click “Clusters” in the left sidebar.
- Click “Create Cluster”.
- Give it a name (e.g., ld-cluster) 
- Choose AWS Fargate (serverless)
- and click “Create”.

### ✅ 3. Register a Task Definition
- Go to “Task Definitions”.
- Click “Create new Task Definition”.
- name it "task-definition-frontend"
- Fill in the form:
Infrastructure requirements
Launch type: AWS Fargate
Task role: You can skip or use ecsTaskExecutionRole
Operating system family: Linux
CPU: 0.25 vCPU
Memory: 0.5 GB
Container
Container name: ld-container
Image URI:
- Go to AWS ECR 
- Copy the Image URI of your uploaded image with image tag
Port mappings: 8087
Click Add, then Next, and Create the task definition.

### ✅ 4. Create a Service to Run the Task
- Go back to “Clusters” → ld-cluster → “Services” → Create.
- Service details
Task definition family: task-definition-frontend (The one you created earlier)
Task definition revision: 1 (Always choose the latest version)
Service name: ld-service
Number of tasks: 1
Capacity provider: FARGATE

### ✅ 5. Configure Networking
Choose a VPC, then:
Select 1 or more public subnets
Enable Auto-assign public IP

### ✅ 7. Review and Create
Click through the review screen and Create Service.

## Check security group inbound rules
https://ap-southeast-1.console.aws.amazon.com/ec2/home?region=ap-southeast-1#Overview:
- Go to EC2 → Security Groups → Your SG:
Edit inbound rule
- ✅ Inbound Rule
Add Rule
Type: Custom TCP
Port: 8087
Source: 0.0.0.0/0 (for public access)
-> Save Rules

### To check if your app is running go to
- Clusters -> Tasks -> Click the Task - > Go to Container details for ld-container -> Click the Network Bindigs
- Click the External link


