#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static.

# Install Nginx
sudo apt-get update
sudo apt-get install nginx -y

# Create necessary directories and files
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo 'Hello from the other side :)' | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link `/data/web_static/current` linked to `/data/web_static/releases/test/`
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group, recursively.
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configurations to serve the content of `/data/web_static/current/` to `hbnb_static`
conf="\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "/server_name _;/a # new path\n$conf" /etc/nginx/sites-enabled/default

# restart nginx
sudo service nginx restart
