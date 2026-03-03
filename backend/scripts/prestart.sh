#!/usr/bin/env bash 
set -e

echo "Run apply migrations.." 
alembic upgrade head 
echo "Migrations applied!"


if [ -d /backend/chrome-linux64 ]; then 
  echo "chrome-linux64 is installed"


exec "$@" # выполняем всё что передано 
