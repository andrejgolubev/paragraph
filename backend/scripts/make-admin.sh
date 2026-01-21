#!/usr/bin/env bash
set -euo pipefail

EMAIL="${1?email required}"
GROUPS="${2?groups required}"
API_KEY="${3?API key required}"

URL="${4:-https://localhost:8000}"

curl --fail --retry 3 --retry-delay 2 \
  -H "API-Key: ${API_KEY}" \
  "${URL}/admin/make-admin/?email=${EMAIL}&groups_to_admin=${GROUPS}"

