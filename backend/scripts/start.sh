#!/bin/sh
set -e

export PYTHONPATH=/
exec gunicorn backend.api.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000