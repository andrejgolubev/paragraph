#!/bin/sh
set -e

if [ -f /backend/chrome-linux64.zip ] && [ ! -d /backend/chrome-linux64 ]; then
  unzip /backend/chrome-linux64.zip -d /backend
  apt-get update
  while read pkg; do
    apt-get satisfy -y --no-install-recommends "${pkg}"
  done < /backend/chrome-linux64/deb.deps
fi

exec "$@"