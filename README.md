## Project Title: Cloud-Native Web Application on AWS/GCP with Event-Driven Architecture
## Introduction
Developed a full-fledged RESTful API with (Python) Flask and deployed on an AWS EC2 instance, providing robust backend services with PostgreSQL database hosted on Amazon RDS. Emphasizing security, the API integrates Basic Authentication and utilizes SQLAlchemy as an ORM framework to interact seamlessly with the database. The project leverages Pulumi for infrastructure provisioning, integrates AWS services for event-driven operations, and employs GitHub Actions for CI/CD.

Architecture Overview
Our application follows a microservices architecture that allows for independent scaling and deployment of service components. It consists of:

REST APIs built with Flask, running on AWS EC2 instances.
PostgreSQL database for persistent storage, with SQLAlchemy as the ORM.
Load Balancer and Auto Scaling Group for handling traffic and ensuring high availability.
SNS topics and AWS Lambda functions for asynchronous processing.
Google Cloud Storage (GCS) bucket for file storage.
DynamoDB for logging email transaction records.
Amazon CloudWatch for monitoring and logs management.
A CI/CD pipeline built with GitHub Actions for automated testing and deployment.
Prerequisites
Before starting, ensure you have the following prerequisites:

AWS Account with access to EC2, RDS, SNS, Lambda, DynamoDB, CloudWatch.
GCP Account with access to GCS Buckets.
GitHub Account for source code management and actions.
Pulumi Account for infrastructure as code.
Basic understanding of Flask, PostgreSQL, AWS, GCP, and CI/CD concepts.
Step-by-Step Guide
Step 1: Setup Development Environment
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