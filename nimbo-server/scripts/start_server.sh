#!/bin/bash

# Navigate to the project directory
cd /home/ubuntu/nimbo-server/nimbo-server

# Activate virtual environment
source venv/bin/activate

# Stop any running Gunicorn processes
pkill gunicorn

# Start Gunicorn (or any other WSGI server you are using)
gunicorn --workers 3 nimbo.wsgi:application --bind 0.0.0.0:8000
