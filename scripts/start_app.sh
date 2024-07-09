#!/bin/bash

# Change directory to the home directory
cd /home/ubuntu/

# Create and activate a virtual environment
python -m venv venv

source /home/ubuntu/venv/bin/activate
cd /home/ubuntu/
# Install Django and other dependencies
python -m pip install Django
# Add any other dependencies you might have

# Set PYTHONPATH to include your Django project directory

# Change directory to your Django project directory
cd /nimbo-server/
pip install -r requirements.txt
# Perform Django migrations
python manage.py migrate

# Make Django migrations if needed
python manage.py makemigrations

# Collect static files
python manage.py collectstatic --noinput

# Restart gunicorn and nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx
