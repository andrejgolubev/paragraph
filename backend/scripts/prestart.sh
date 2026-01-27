#!/usr/bin/env bash 
set -e

echo "Run apply migrations.." 
alembic upgrade head 
echo "Migrations applied!"


echo "Downloading chromium..."
if [ -f /backend/chrome-linux64.zip ] && [ ! -d /backend/chrome-linux64 ]; then
  unzip /backend/chrome-linux64.zip -d /backend
  apt-get update
  while read pkg; do
    apt-get satisfy -y --no-install-recommends "${pkg}"
  done < /backend/chrome-linux64/deb.deps
fi
echo "Chromium downloaded!"

exec "$@" # выполняем всё что передано 
