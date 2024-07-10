#!/bin/bash


source /home/ubuntu/envnimbo/bin/activate

cd /home/ubuntu/nimbo-server/


# Perform Django migrations
python manage.py migrate

# Make Django migrations if needed
python manage.py makemigrations

ps aux | grep gunicorn
# Collect static files
python manage.py collectstatic --noinput

# Restart gunicorn and nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx
