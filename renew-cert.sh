#!/bin/bash

APP_DIR="/opt/newapp"

cd $APP_DIR
docker compose run --rm certbot renew --webroot -w /var/www/certbot >> ${APP_DIR}/certbot-renew.log 2>&1 && docker compose kill -s SIGHUP nginx