#!/bin/bash

# Change directory to the home directory
cd /home/ubuntu/nimbo-server/

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
