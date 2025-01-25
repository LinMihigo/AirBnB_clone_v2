#!/usr/bin/env bash
# sets up web servers for deployment of web_static
apt-get -y update
apt-get install -y nginx

directories=("/data/web_static/shared/" "/data/web_static/releases/test/")
mkdir -p "${directories[@]}"

echo "Nginx!!!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data
chgrp -R ubuntu /data/

sudo sed -i '/server {/a \	location /hbnb_static {\n		alias /data/web_static/current;\n		index index.html index.htm;\n	}' /etc/nginx/sites-available/default
nginx -t && nginx -s reload
