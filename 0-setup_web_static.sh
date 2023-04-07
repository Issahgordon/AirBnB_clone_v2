#!/usr/bin/env bash
# script to install and setup nginx
CONFIG_FILE="/etc/nginx/sites-available/default"
HOST_NAME=$(hostname)
MY_ID=496
STATIC=/data/web_static

# check if hostname is correct
if [[ $(hostname) =~ ^$MY_ID-web-[0-9]+ ]]; then
    echo 'hostname properly configured'
else
    (>&2 echo 'hostname not configured properly...')
    (>&2 echo 'please set hostname to pattern: 496-web-<server_id>...')
    (>&2 echo 'Example: sudo hostnamectl set-hostname 496-web-<insert_server_id_here>')
fi

# install nginx
apt-get -y update
apt-get -y install nginx

# update 404 error page
echo "Ceci n'est pas une page" > /usr/share/nginx/html/404.html

# create static directories and links
mkdir -p $STATIC/releases/test
mkdir -p $STATIC/shared
echo 'Holberton School Is Running!' > $STATIC/releases/test/index.html
ln -sfn $STATIC/releases/test $STATIC/current
sudo chown -f -R ubuntu:ubuntu /data/

# update config file to redirect
printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   $STATIC/current;
    index  index.html index.htm 8-index.html;
    add_header X-Served-By $HOST_NAME;
    location / {
        alias $STATIC/current/;
    }
    location /redirect_me {
        return 301 http://google.com/;
    }
    location /hbnb_static {
        alias $STATIC/current/;
    }
    error_page 404 /404.html;
    location /404 {
      root /usr/share/nginx/html;
      internal;
    }
}" > $CONFIG_FILE

# start nginx after reloading config
service nginx start
# if nginx was already running restart it
service nginx restart
