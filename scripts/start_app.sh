#!/bin/bash

# Change directory to the home directory
cd /home/ubuntu/

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Django and other dependencies
python3 -m pip install Django
# Add any other dependencies you might have

# Change directory to your Django project directory
cd /home/ubuntu/nimbo-server/

# Perform Django migrations
python3 manage.py migrate

# Make Django migrations if needed
python3 manage.py makemigrations

# Collect static files
python3 manage.py collectstatic --noinput

# Restart gunicorn and nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx
