#!/bin/bash
set -e  # Exit script if any command fails

# Update the system
echo "Updating the system"
sudo apt update -y
sudo apt upgrade -y

# Install Python3 and pip
echo "Installing Python and pip"
sudo apt install python3-pip -y

# Install unzip if not installed
echo "Installing unzip"
sudo apt-get install unzip -y

# Unzip the web application
echo "Unzipping the web application"
unzip webapp.zip -d /home/admin/webapp

# Navigate to the webapp directory
echo "Navigating to the webapp directory"
cd /home/admin/webapp

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Copy the systemd service file and start the service
echo "Setting up and starting the webapp service"
sudo cp /home/admin/webapp/packer/webapp.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start webapp.service
sudo systemctl enable webapp.service

echo "Script executed successfully!"
