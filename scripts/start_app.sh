#!/bin/bash
sudo mkdir -p /home/ubuntu/nimbo-server/staticfiles
sudo chown -R ubuntu:ubuntu /home/ubuntu/nimbo-server/staticfiles
sudo chmod -R 755 /home/ubuntu/nimbo-server/staticfiles


source /home/ubuntu/envnimbo/bin/activate

cd /home/ubuntu/nimbo-server/

python manage.py collectstatic
# # Perform Django migrations
# python manage.py migrate

# # Make Django migrations if needed
# python manage.py makemigrations

sudo systemctl status nginx.service
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx.service
sudo lsof -i :80
sudo lsof -i :443
sudo journalctl -xeu nginx.service


# ps aux | grep gunicorn
# # Collect static files


# # Restart gunicorn and nginx
# sudo systemctl restart gunicorn
# sudo systemctl restart nginx
