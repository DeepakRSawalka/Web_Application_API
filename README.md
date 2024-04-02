## Project Title: Cloud-Native Web Application on AWS/GCP with Event-Driven Architecture

## Description
Developed RESTful API with (Python) Flask and deployed on an AWS EC2 instance, providing robust backend services with PostgreSQL database hosted on Amazon RDS. Emphasizing security, the API integrates Basic Authentication and utilizes SQLAlchemy as an ORM framework to interact seamlessly with the database. The project leverages Pulumi for infrastructure provisioning, integrates AWS services for event-driven operations, and employs GitHub Actions for CI/CD.

## Architecture Overview
Below is a detailed Architecture Diagram illustrating the comprehensive setup and flow of the project:


## Technical Stack & Features

**Python 3.11 & Flask**: Utilizes Object-Oriented Principles (OOP) for a scalable codebase and (web framework) Flask for efficient API development.

**SQLAlchemy & PostgreSQL**: ORM Framework for seamless database operations with PostgreSQL hosted on Amazon RDS, ensuring robust data management.

**Pulumi**: Infrastructure as Code (IaC) for consistent cloud infrastructure provisioning on AWS and GCP.

**Load Balancing & Auto-Scaling**: This project harnesses AWS Elastic Load Balancing and Auto Scaling to optimize the handling of incoming traffic and resource utilization. 

**AWS Lambda**: Utilized for creating an event-driven solution that responds to application events with automated processes.

**GitHub Actions**: Facilitates CI/CD pipelines for automated testing, building, and deployment.

**Bash Scripting**: Enables automation of deployment processes and environment setup.

**Postman**: Supports API testing to ensure endpoint functionality, reliability, and security.

**Systemd**: Facilitates automatic application startup and management, ensuring reliability.

**Hashicorp Packer**: Used for creating custom AMIs, streamlining deployment with pre-configured environments.

**CloudWatch**: Provides logging and monitoring, enabling efficient debugging and performance tracking.

**Custom Metrics with StatsD**: The project employs StatsD for custom metrics collection. This setup enables the generation of detailed insights into application operations, including custom events and performance metrics.

## SetUp and Installation

**Step 1**: Clone the Repository
```bash
git clone git@github.com:DeepakSawalka/Web_Application_API.git
```

AWS Configuration: Set up the AWS CLI and authenticate with your credentials.
GCP Configuration: Set up the gcloud CLI and authenticate with your GCP account.
Local Environment: Install Python, Flask, and SQLAlchemy for local development.
Step 2: Provision Infrastructure with Pulumi
Install Pulumi and configure it to use your AWS account.
Define your infrastructure as code with Pulumi, including EC2 instances, RDS database, SNS topics, Lambda functions, GCS buckets, and DynamoDB tables.
Deploy your infrastructure with Pulumi commands.
Step 3: Develop REST API
Develop REST APIs for assignment creation and submission using Flask.
Use SQLAlchemy ORM to interact with the PostgreSQL database.
Secure your APIs using Basic Authentication.
Step 4: Event-Driven Operations with AWS Services
Set up SNS topics to publish messages on assignment submission.
Create Lambda functions that trigger on SNS message publication to:
Download the file from the GitHub repository.
Store the file in GCS Bucket.
Send an email to the user regarding the status of the download.
Log email transactions in DynamoDB.
Step 5: Monitoring with Amazon CloudWatch
Configure CloudWatch to monitor your EC2 instances.
Set up logs management for your application and infrastructure logs.
Step 6: CI/CD Pipeline with GitHub Actions
Set up GitHub Actions for your repository.
Configure workflows for testing, building, and deploying your Flask application.
Integrate Packer to build custom AMIs with application dependencies.
Step 7: Application Deployment
Deploy your application to the provisioned AWS EC2 instances using the CI/CD pipeline.
Ensure the load balancer correctly routes traffic to your instances.
Verify the auto-scaling group scales your application based on the defined policies.
Monitoring and Logs
Use Amazon CloudWatch to monitor the application’s performance and health.
Set alarms for any metrics that indicate potential issues.
Additional Resources
Flask Documentation: Flask Official Documentation
SQLAlchemy Documentation: SQLAlchemy Official Documentation
Pulumi Documentation: Pulumi Docs
GitHub Actions Documentation: GitHub Actions Docs
Support
If you encounter any issues or have questions, please file an issue in the GitHub repository's issue tracker.

Conclusion
Thank you for choosing our Cloud-Native Web Application project. By following these steps, you should have a scalable, secure, and maintainable application running in the cloud. This setup empowers you to focus on developing features rather than managing infrastructure.