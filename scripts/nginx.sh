#!/usr/bin/bash

# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Remove the default symbolic link if it exists
sudo rm -f /etc/nginx/sites-enabled/default

# Copy the Nginx configuration file to the sites-available directory
sudo cp /home/ubuntu/nimbo-server/nginx/nginx.conf /etc/nginx/sites-available/nimboproject

# Remove existing symbolic link for nimboproject if it exists
sudo rm -f /etc/nginx/sites-enabled/nimboproject

# Create a new symbolic link for the Nimboproject
sudo ln -s /etc/nginx/sites-available/nimboproject /etc/nginx/sites-enabled/

# Add the ubuntu user to the www-data group
sudo gpasswd -a www-data ubuntu

# Test the Nginx configuration for any syntax errors
sudo nginx -t

# Check the exit status of the nginx -t command
if [ $? -eq 0 ]; then
    # Restart the Nginx service if the configuration is valid
    sudo systemctl restart nginx
else
    echo "Nginx configuration test failed. Please check the configuration file."
fi
