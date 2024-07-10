#!/bin/sh

ssh root@184.72.78.226 <<EOF
  cd blogprojectdrf
  git pull 
  source envnimbo/bin/activate
  ./manage.py migrate
  sudo systemctl restart nginx
  sudo service gunicorn restart
  sudo service nginx restart
  exit
EOF