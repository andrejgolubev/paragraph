#!/usr/bin/env bash 
set -e

echo "Run apply migrations.." 
alembic upgrade head 
echo "Migrations applied!"


echo "Downloading Chrome Browser for testing ..."
# curl -L -o chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chrome-linux64.zip
if [ -f /backend/chrome-linux64.zip ] && [ ! -d /backend/chrome-linux64 ]; then
  unzip /backend/chrome-linux64.zip -d /backend
  apt-get update
  while read pkg; do
    apt-get satisfy -y --no-install-recommends "${pkg}"
  done < /backend/chrome-linux64/deb.deps
  # export PATH="/backend/chrome-linux64:$PATH"
  echo "Chrome Browser for testing downloaded!"
else
  echo "Chrome Browser for testing did not download"
fi


exec "$@" # выполняем всё что передано 
