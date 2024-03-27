#!/bin/bash
set -e  # Exit script if any command fails

# Update the system
echo "Updating the system"
sudo apt update -y
sudo apt upgrade -y

# Install Python3 and pip
echo "Installing Python and pip"
sudo apt install python3-pip python3-venv -y

# Install unzip if not installed
echo "Installing unzip"
sudo apt-get install unzip -y

sudo groupadd ec2-group
sudo useradd -s /bin/false -g ec2-group -d /home/ec2-user -m ec2-user

# Unzip the web application
echo "Unzipping the web application"
unzip webapp.zip -d webapp

# Navigate to the webapp directory
echo "Navigating to the webapp directory"
cd webapp

# Create a virtual environment
echo "Creating a virtual environment"
python3 -m venv venv

# Create a virtual environment and install dependencies
echo " Installing Python dependencies"
venv/bin/pip install -r requirements.txt

cd ..
sudo mv /home/admin/webapp /home/ec2-user
cd /home/ec2-user
sudo chown -R ec2-user:ec2-group /home/ec2-user/webapp
sudo chmod 755 /home/ec2-user/webapp
# Copy the systemd service file and start the service
echo "Setting up and starting the webapp service"
sudo cp /home/ec2-user/webapp/packer/webapp.service /etc/systemd/system

sudo chown -R ec2-user:ec2-group /etc/systemd/system/webapp.service

sudo systemctl daemon-reload
sudo systemctl enable webapp.service
sudo systemctl start webapp.service

# Download and install the CloudWatch Agent
echo "Downloading and installing the CloudWatch Agent"
sudo wget https://s3.amazonaws.com/amazoncloudwatch-agent/debian/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb

# Copy the CloudWatch Agent configuration file
echo "Copying the CloudWatch Agent configuration file"
sudo cp /home/ec2-user/webapp/cloud-watch/config.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

# Configure the CloudWatch Agent to start on boot
echo "Configuring the CloudWatch Agent to start on boot"
sudo systemctl enable amazon-cloudwatch-agent

# Start the CloudWatch Agent
echo "Starting the CloudWatch Agent..."
sudo systemctl start amazon-cloudwatch-agent

echo "Script executed successfully!"
