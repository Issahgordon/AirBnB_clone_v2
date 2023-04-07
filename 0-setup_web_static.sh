#!/usr/bin/env bash

# Install Nginx if it's not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake HTML file for testing
echo "<html><head></head><body>Holberton School is awesome!</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link and give ownership to ubuntu user and group
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
location_alias="location /hbnb_static {\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "/server_name _;/a $location_alias" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
