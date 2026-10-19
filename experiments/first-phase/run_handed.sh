#!/bin/bash
set -u
E=$(cd "$(dirname "$0")/.." && pwd)
. "$E/../engines/env.sh"
model=$1
variant=$2
rep=$3
id=$4
arm=handed-$variant
bin=$CLAUDE
model_flags=()
if [ "$model" != default ]; then
  arm=handed55-$variant
  bin=$CLAUDE_LATEST
  model_flags=(--model "$model")
fi
out="$E/runs/$arm/$id.r$rep.jsonl"
[ -s "$out" ] && exit 0
mkdir -p "$E/runs/$arm" "$E/logs"
prompt=$(awk -F'\t' -v id="$id" '$1==id {print $3}' "$E/prompts.tsv")
[ -z "$prompt" ] && { echo "no prompt for $id" >&2; exit 1; }
cd "$SANDBOXES/app-sandbox-$variant" || exit 1
timeout 420 "$bin" -p "${model_flags[@]}" --safe-mode --strict-mcp-config --no-session-persistence \
  --output-format stream-json --verbose --max-budget-usd 1.50 \
  --disallowedTools WebSearch WebFetch \
  --append-system-prompt "$(cat "$E/handed/$variant.txt")" \
  -- "$prompt" > "$out.tmp" 2> "$E/logs/$arm.$id.r$rep.err" && mv "$out.tmp" "$out"
