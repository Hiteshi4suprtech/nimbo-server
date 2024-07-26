#!/bin/bash

# Navigate to the project directory
cd /home/ubuntu/nimbo-server/nimbo-server

# Activate virtual environment (if you are using one)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
