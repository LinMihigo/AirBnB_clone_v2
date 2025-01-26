#!/usr/bin/env bash
# sets up web servers for deployment of web_static
apt-get -y update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo '<html>
	<head>
	</head>
	<body>
ALX
	</body>
</html>' | tee /data/web_static/releases/test/index.html >/dev/null
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data

CONFIG=$(cat <<EOF
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	add_header X-Served-By $HOSTNAME;

	root /var/www/html;
	index index.html index.htm;

	error_page 404 /404.html;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
	location = /404.html {
		internal;
	}
}
EOF
)

echo "$CONFIG" | tee /etc/nginx/sites-available/default >/dev/null

nginx -t && service nginx restart
exit 0
