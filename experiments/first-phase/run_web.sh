#!/bin/bash
set -u
E=$(cd "$(dirname "$0")/.." && pwd)
. "$E/../engines/env.sh"
search=$1
arm=$2
model=$3
rep=$4
id=$5
out="$E/runs/$arm/$id.r$rep.jsonl"
[ -s "$out" ] && exit 0
mkdir -p "$E/runs/$arm" "$E/logs"
prompt=$(awk -F'\t' -v id="$id" '$1==id {print $3}' "$E/prompts.tsv")
[ -z "$prompt" ] && { echo "no prompt for $id" >&2; exit 1; }
bin=$CLAUDE
model_flags=()
[ "$model" != default ] && { bin=$CLAUDE_LATEST; model_flags=(--model "$model"); }
rule_flags=()
[ "$search" = forced ] && rule_flags=(--append-system-prompt
  "Before answering, search the web at least once and base your answer on what you find.")
cd "$SANDBOXES/app-sandbox" || exit 1
timeout 480 "$bin" -p --safe-mode --strict-mcp-config --no-session-persistence \
  --output-format stream-json --verbose --max-budget-usd 2.00 "${model_flags[@]}" \
  --allowedTools WebSearch WebFetch "${rule_flags[@]}" \
  -- "$prompt" > "$out.tmp" 2> "$E/logs/$arm.$id.r$rep.err" && mv "$out.tmp" "$out"
