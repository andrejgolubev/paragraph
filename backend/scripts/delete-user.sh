#!/usr/bin/env bash
set -euo pipefail

EMAIL="${1?email required}"
API_KEY="${2?API key required}"
URL="${3:-https://localhost:8000}"

curl --fail --retry 3 --retry-delay 2 \
  -H "API-Key: ${API_KEY}" \
  "${URL}/admin/delete?email=${EMAIL}"

