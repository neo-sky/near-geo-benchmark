#!/bin/bash
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
. "$ROOT/engines/env.sh"
cap=${1:-15}
watch_pid=$2
log=$ROOT/experiments/logs/router-spend.log
while kill -0 "$watch_pid" 2>/dev/null; do
  key=$(openrouter_key)
  spent=$(curl -s -m 20 -H "Authorization: Bearer $key" https://openrouter.ai/api/v1/key \
    | jq -r '.data.usage // empty')
  unset key
  echo "$(date -u +%FT%TZ) spent=$spent cap=$cap" >> "$log"
  if [ -n "$spent" ] && awk -v s="$spent" -v c="$cap" 'BEGIN { exit !(s >= c) }'; then
    touch "$ENGINE_HOME/router.stop"
    echo "$(date -u +%FT%TZ) cap reached, router runs stopped" >> "$log"
    exit 0
  fi
  sleep 300
done
