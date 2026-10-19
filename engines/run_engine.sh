#!/bin/bash
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
E=$ROOT/experiments
G=$ROOT/engines
. "$G/env.sh"
BIN=$ENGINE_HOME/cli/node_modules/.bin

engine=$1
cond=$2
rep=$3
id=$4
arm="$engine-$cond"
out="$E/runs/$arm/$id.r$rep.jsonl"
[ -s "$out" ] && exit 0
mkdir -p "$E/runs/$arm" "$E/logs"
prompt=$(awk -F'\t' -v id="$id" '$1==id {print $3}' "$E/prompts.tsv" "$E/prompts2.tsv" \
  "$E/probes.tsv" "$G/canary.tsv")
[ -z "$prompt" ] && { echo "no prompt for $id" >&2; exit 1; }
case $cond in
  p) sb=$SANDBOXES/app-sandbox-e-b1 ;;
  n1) sb=$SANDBOXES/geo-sandbox ;;
  *) sb=$SANDBOXES/app-sandbox-e-$cond ;;
esac
log="$E/logs/$arm.$id.r$rep.err"
case $cond in b2|b3) web=on ;; *) web=off ;; esac

case $cond in t1) set=r-a ;; t2) set=r-b ;; t3) set=r-c ;; *) set= ;; esac
search_binds=()
if [ -n "$set" ]; then
  pos=$(( ($(printf '%s' "$id" | cksum | cut -d' ' -f1) + rep) % 4 + 1 ))
  echo "$pos" > "$E/logs/$arm.$id.r$rep.pos"
  srv=("$NODE/bin/node" "$G/mock-search.mjs" "$E/handed/$set.txt" "$pos")
  search_binds=(--ro-bind "$G/mock-search.mjs" "$G/mock-search.mjs"
    --ro-bind "$E/handed" "$E/handed")
  mcp_std=$(jq -nc --arg c "${srv[0]}" --arg a "${srv[1]}" --arg b "${srv[2]}" --arg p "${srv[3]}" \
    '{mcpServers: {search: {type: "local", command: $c, args: [$a, $b, $p], tools: ["*"]}}}')
fi

jail() {
  bwrap --dev-bind / / --tmpfs "$HOME" --tmpfs /tmp \
    --ro-bind "$NODE" "$NODE" --ro-bind "$ENGINE_HOME/cli" "$ENGINE_HOME/cli" \
    --ro-bind "$sb" "$sb" "${search_binds[@]}" "${binds[@]}" --clearenv \
    --setenv HOME "$HOME" --setenv LANG C.UTF-8 --setenv TERM dumb \
    --setenv PATH "$NODE/bin:/usr/local/bin:/usr/bin:/bin" \
    "${envs[@]}" --chdir "$sb" -- "$@"
}

binds=()
envs=()
case $engine in
  codex|codexthink)
    [ "$web" = on ] && ws=live || ws=disabled
    extra=(-c features.apps=false)
    [ "$engine" = codexthink ] && extra+=(-m gpt-6-chat-thinking)
    [ -n "$set" ] && extra+=(-c "mcp_servers.search.command=\"${srv[0]}\""
      -c "mcp_servers.search.args=[\"${srv[1]}\",\"${srv[2]}\",\"${srv[3]}\"]"
      -c 'mcp_servers.search.default_tools_approval_mode="approve"')
    binds=(--bind "$ENGINE_HOME/codex" "$HOME/.codex" --ro-bind "$CODEX_DIR" "$CODEX_DIR")
    jail timeout 600 "$CODEX_DIR/codex" exec --json --skip-git-repo-check --ephemeral -s read-only \
      -c "web_search=\"$ws\"" "${extra[@]}" -C "$sb" -- "$prompt" < /dev/null > "$out.tmp" 2> "$log"
    ;;
  claude)
    allow=(Bash Read Glob Grep Skill TodoWrite)
    deny=(Write Edit NotebookEdit)
    if [ "$web" = on ]; then allow+=(WebSearch WebFetch); else deny+=(WebSearch WebFetch); fi
    extra=()
    [ -n "$set" ] && { extra=(--mcp-config "$mcp_std"); allow+=(mcp__search__web_search); }
    binds=(--ro-bind "$CLAUDE_DIR" "$CLAUDE_DIR")
    envs=(--setenv CLAUDE_CODE_OAUTH_TOKEN "$(claude_token)"
      --setenv DISABLE_AUTOUPDATER 1 --setenv CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC 1)
    claude_bin=$CLAUDE_DIR/node_modules/@anthropic-ai/claude-code/bin/claude.exe
    jail timeout 600 "$claude_bin" -p "$prompt" --output-format stream-json --verbose \
      --no-session-persistence --strict-mcp-config "${extra[@]}" \
      --allowedTools "${allow[@]}" --disallowedTools "${deny[@]}" \
      < /dev/null > "$out.tmp" 2> "$log"
    ;;
  deepseek|glm|qwen|kimi|grok|gemini)
    case $engine in
      deepseek) model=router/deepseek/deepseek-v4.1-flash ;;
      glm) model=router/z-ai/glm-5.3-flash ;;
      qwen) model=router/qwen/qwen3.8-flash ;;
      kimi) model=router/moonshotai/kimi-k2.5 ;;
      grok) model=router/x-ai/grok-build-0.1 ;;
      gemini) model=router/google/gemini-3.7-flash ;;
    esac
    [ -e "$ENGINE_HOME/router.stop" ] && { echo "router budget reached" >&2; exit 3; }
    key=$(openrouter_key)
    [ "$web" = on ] && cfg=$G/opencode/web-on.json || cfg=$G/opencode/web-off.json
    if [ -n "$set" ]; then
      mkdir -p "$ENGINE_HOME/cfg"
      run_cfg="$ENGINE_HOME/cfg/$arm.$id.r$rep.json"
      jq --arg c "${srv[0]}" --arg a "${srv[1]}" --arg b "${srv[2]}" --arg p "${srv[3]}" \
        '. + {mcp: {search: {type: "local", command: [$c, $a, $b, $p], enabled: true}}}' \
        "$cfg" > "$run_cfg"
      cfg=$run_cfg
    fi
    binds=(--ro-bind "$G/opencode/config" "$HOME/.config/opencode"
      --ro-bind "$cfg" "$HOME/.oc-run.json"
      --bind "$ENGINE_HOME/oc-cache" "$HOME/.cache/opencode"
      --tmpfs "$HOME/.local/share/opencode")
    [ -d "$sb/.opencode" ] && binds+=(--tmpfs "$sb/.opencode"
      --ro-bind "$sb/.opencode/skills" "$sb/.opencode/skills")
    envs=(--setenv ROUTER_API_KEY "$key" --setenv OPENCODE_DISABLE_CLAUDE_CODE 1
      --setenv OPENCODE_CONFIG "$HOME/.oc-run.json")
    [ "$web" = on ] && envs+=(--setenv OPENCODE_ENABLE_EXA 1)
    jail timeout 600 "$BIN/opencode" run --format json -m "$model" "$prompt" \
      < /dev/null > "$out.tmp" 2> "$log"
    ;;
  copilot)
    deny=(--deny-tool write)
    [ "$web" = off ] && deny+=(--excluded-tools web_fetch web_search)
    extra=()
    [ -n "$set" ] && extra=(--additional-mcp-config "$mcp_std")
    envs=(--setenv GH_TOKEN "$(gh auth token)")
    jail timeout 600 "$BIN/copilot" -p "$prompt" --allow-all-tools "${deny[@]}" "${extra[@]}" \
      --disable-builtin-mcps --output-format json < /dev/null > "$out.tmp" 2> "$log"
    ;;
  *)
    echo "unknown engine $engine" >&2; exit 1 ;;
esac
status=$?
[ $status -eq 0 ] && [ -s "$out.tmp" ] && mv "$out.tmp" "$out"
exit $status
