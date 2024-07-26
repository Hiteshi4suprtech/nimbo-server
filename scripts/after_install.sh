#!/bin/bash

# Navigate to the project directory
cd /home/ubuntu/nimbo-server

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    rm -rf venv
fi

# Create a new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
