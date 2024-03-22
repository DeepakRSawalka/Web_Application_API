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

# Unzip the web application
echo "Unzipping the web application"
unzip webapp.zip -d webapp

# Navigate to the webapp directory
echo "Navigating to the webapp directory"
cd webapp

# Create a virtual environment
echo "Creating a virtual environment"
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment"
source venv/bin/activate

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies"
pip3 install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Copy the systemd service file and start the service
echo "Setting up and starting the webapp service"
sudo cp /home/admin/webapp/packer/webapp.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start webapp.service
sudo systemctl enable webapp.service

echo "Script executed successfully!"
