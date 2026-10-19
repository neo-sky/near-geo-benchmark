#!/bin/bash
set -u
E=$(cd "$(dirname "$0")/.." && pwd)
. "$E/../engines/env.sh"
set=$1
arm=$2
model=$3
tools=$4
rep=$5
id=$6
out="$E/runs/$arm/$id.r$rep.json"
[ -s "$out" ] && exit 0
mkdir -p "$E/runs/$arm" "$E/logs"
prompt=$(awk -F'\t' -v id="$id" '$1==id {print $3}' "$E/$set.tsv")
[ -z "$prompt" ] && { echo "no prompt for $id" >&2; exit 1; }
if [ "$tools" = web ]; then
  tool_flags=(--allowedTools WebSearch WebFetch)
else
  tool_flags=(--disallowedTools WebSearch WebFetch)
fi
bin=$CLAUDE
model_flags=()
[ "$model" != default ] && { bin=$CLAUDE_LATEST; model_flags=(--model "$model"); }
cd "$SANDBOXES/app-sandbox" || exit 1
timeout 420 "$bin" -p --safe-mode --strict-mcp-config --no-session-persistence \
  --output-format json --max-budget-usd 1.50 "${model_flags[@]}" "${tool_flags[@]}" \
  -- "$prompt" > "$out.tmp" 2> "$E/logs/$arm.$id.r$rep.err" && mv "$out.tmp" "$out"
