#!/usr/bin/env bash
# sets up web servers for deployment of web_static
sudo apt-get -y update
sudo apt-get install -y nginx
directories=("/data/web_static/shared/", "/data/web_static/releases/test/")
sudo mkdir -p "${directories[@]}"

echo "Nginx!!!" > /data/web_static/releases/test/index.html
ln -sf "/data/web_static/releases/test/" "/data/web_static/current"
chown -R ubuntu:group /data
sudo sed -i '/server {/a \    location /hbnb_static {\n\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default  
sudo nginx -t && sudo service -s reload nginx
