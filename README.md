# Weather Dashboard DevOps Project

A comprehensive DevOps project showcasing various tools and technologies:
- Flask Web Application
- AWS (EC2, S3)
- Docker
- Jenkins Pipeline
- Terraform
- GitHub Actions

## Project Structure
```
.
├── app/                    # Flask application
│   ├── static/            # Static files
│   ├── templates/         # HTML templates
│   └── app.py            # Main application file
├── terraform/             # Infrastructure as Code
│   ├── main.tf           # Main Terraform configuration
│   ├── variables.tf      # Variable definitions
│   └── outputs.tf        # Output definitions
├── Dockerfile            # Docker configuration
├── Jenkinsfile          # Jenkins pipeline
├── docker-compose.yml   # Docker compose configuration
└── README.md           # Project documentation
```

## Prerequisites
- AWS Account
- Jenkins Server
- Docker
- Terraform
- Python 3.x

## Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `python app/app.py`

## Infrastructure Deployment
1. Configure AWS credentials
2. Initialize Terraform: `terraform init`
3. Apply infrastructure: `terraform apply`

## CI/CD Pipeline
The Jenkins pipeline includes:
1. Code checkout from GitHub
2. Build Docker image
3. Run tests
4. Push to Docker Hub
5. Deploy to AWS EC2

## AWS Resources
- EC2 instance for application hosting
- S3 bucket for data storage
- Security groups and IAM roles