#!/usr/bin/env bash
set -euo pipefail

USER_EMAIL="${1?email required}"
GROUPS_TO_ADMIN="${2?groups required}" 
# ни в коем случае ни GROUPS, иначе значение переменной будет всегда 1000

API_KEY="${3?API key required}"

BASE_URL="${4:-https://api.paragraph-schedule.ru}"

curl --fail-with-body --retry 3 --retry-delay 2 -L --insecure \
  --request POST \
  -H "API-Key: ${API_KEY}" \
  "${BASE_URL}/admin/make-admin/?user_email=${USER_EMAIL}&groups_to_admin=${GROUPS_TO_ADMIN}"
