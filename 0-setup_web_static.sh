#!/usr/bin/env bash
# Setting a web server from web_static.

# Update the package list
sudo apt-get update

# Install nginx web server, with the "-y" flag assuming yes to prompts
sudo apt-get -y install nginx

# Allow Nginx HTTP traffic through the firewall using ufw
sudo ufw allow 'Nginx HTTP'

# Create directories for the web application
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html

# Write basic HTML content to the index.html file
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create a symbolic link named "current" pointing to the test release directory
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data directory and its contents to user "ubuntu"
sudo chown -R ubuntu:ubuntu /data/
chgrp -R ubuntu /data/

# Modify the default Nginx configuration file
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart the Nginx service to apply the configuration changes
sudo service nginx restart
