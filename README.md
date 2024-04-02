## Project Title: Cloud-Native Web Application on AWS/GCP with Event-Driven Architecture

## Description
Developed RESTful API with (Python) Flask and deployed on an AWS EC2 instance, providing robust backend services with PostgreSQL database hosted on Amazon RDS. Emphasizing security, the API integrates Basic Authentication and utilizes SQLAlchemy as an ORM framework to interact seamlessly with the database. The project leverages Pulumi for infrastructure provisioning, integrates AWS services for event-driven operations, and employs GitHub Actions for CI/CD.

## Architecture Overview
Below is a detailed Architecture Diagram illustrating the comprehensive setup and flow of the project:


## Features 
1. **Programming Language:**
    
    [Python](https://docs.python.org/3.11/) : Emphasizing Object oriented Principles (OOP) principles for a clean modular, and scalable codebase.

2. **Web Framework:**
    
    [Flask](https://flask.palletsprojects.com/en/latest/) : A lightweight WSGI web application framework that enables rapid development and easy integration of web services, making it ideal for building efficient APIs.

3. **ORM Framework:**

    [SQLAlchemy][] : Utilized as the database toolkit and ORM for Python, facilitating efficient and high-level database operations, which enhances the interaction between the application and the PostgreSQL database.

4. **Database:**

    [PostgreSQL][]: Chosen for its advanced features, reliability, and compatibility with SQLAlchemy, ensuring seamless application integration and robust data management.

5. **Infrastructure as Code:**

    [Pulumi][]: Leveraged to provision and manage cloud infrastructure on platforms like AWS and GCP, ensuring consistent deployments, configurations, and infrastructure versioning.

6. **Event-Driven Architecture:**

    [AWS Lambda][]: Utilized for creating an event-driven solution that responds to application events with automated processes, such as file downloads, notifications, and database updates.

7. **Continuous Integration/Continuous Deployment (CI/CD):**

    [GitHub Actions][]: Implements CI/CD pipelines for automated testing, building, and deployment, enhancing development workflows and ensuring high-quality code.

8. **Scripting:**

    [Bash Scripting][]: Employed for various automation tasks, demonstrating the application of shell scripting in system administration, deployment processes, and environment setup.

9.  **API Testing:**

    [Postman][]: Utilized for comprehensive API testing, allowing for the simulation of client requests and responses. It aids in verifying the functionality, reliability, and security of the REST API endpoints throughout the development process.

    

Python: Emphasizing OOP principles for a clean, modular, and scalable codebase. The use of Python extends beyond OOP to include general-purpose scripting, showcasing the versatility of Python for different aspects of backend development.
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