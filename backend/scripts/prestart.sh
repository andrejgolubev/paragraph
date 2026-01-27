#!/usr/bin/env bash 
set -e

echo "Run apply migrations.." 
alembic upgrade head 
echo "Migrations applied!"


echo "Downloading Chrome Browser for testing ..."
if [ -f /backend/chrome-linux64.zip ] && [ ! -d /backend/chrome-linux64 ]; then
  unzip /backend/chrome-linux64.zip -d /backend
  apt-get update
  while read pkg; do
    apt-get satisfy -y --no-install-recommends "${pkg}"
  done < /backend/chrome-linux64/deb.deps
  echo "Chrome Browser for testing downloaded!"
else
  echo "Chrome Browser for testing did not download"
fi


exec "$@" # выполняем всё что передано 
