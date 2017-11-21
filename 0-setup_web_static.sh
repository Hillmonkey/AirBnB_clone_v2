#!/usr/bin/env bash
# this script sets up webservers for deployment of static website

sudo apt-get update
sudo apt-get -y install nginx
sudo service nginx start

sudo mkdir --parents /data/web_static/releases/test
sudo mkdir /data/web_static/shared
echo "Testing, testing, testing" | sudo tee /data/web_static/releases/test/index.html
# maybe ln --force will cause replacement of preexisting file
sudo ln --force -s -T /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo rm /etc/nginx/site-available/default
wget https://raw.githubusercontent.com/Hillmonkey/AirBnB_clone_v2/master/default
sudo mv default /etc/nginx/sites-available/default
sudo service nginx restart
