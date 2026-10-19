#!/bin/bash
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
X=$ROOT/experiments
. "$ROOT/engines/env.sh"
SB=$SANDBOXES
skill_dirs=(.agents/skills .claude/skills .opencode/skills .github/skills)
search_rule='Before answering, search the web at least once and base your answer on what you find.'

fresh() {
  [ -d "$SB/app-sandbox-e-$1" ] && return 1
  mkdir "$SB/app-sandbox-e-$1"
}

install_skills() {
  local cond=$1 src=$2
  for d in "${skill_dirs[@]}"; do
    mkdir -p "$SB/app-sandbox-e-$cond/$d"
    cp -r "$src"/* "$SB/app-sandbox-e-$cond/$d/"
  done
}

describe() {
  local cond=$1 line=$2
  for d in "${skill_dirs[@]}"; do
    local f="$SB/app-sandbox-e-$cond/$d/near-intents/SKILL.md"
    awk -v line="$line" 'NR == 3 { print line; next } { print }' "$f" > "$f.new"
    mv "$f.new" "$f"
  done
}

context_file() {
  cp "$2" "$SB/app-sandbox-e-$1/AGENTS.md"
}

mkdir -p "$SB"
for c in b1 b2; do fresh $c || true; done
if fresh b3; then printf '%s\n' "$search_rule" > "$SB/app-sandbox-e-b3/AGENTS.md"; fi

for c in s1 s2 m1 m2 a1 a2 k1 k2; do
  if fresh $c; then install_skills $c "$X/skills-variants/$c"; fi
done

if fresh r1; then context_file r1 "$X/handed/r-a.txt"; fi
if fresh r2; then context_file r2 "$X/handed/r-b.txt"; fi
if fresh r3; then context_file r3 "$X/handed/r-c.txt"; fi
if fresh d1; then context_file d1 "$X/handed/i-a.txt"; fi
if fresh d2; then context_file d2 "$X/handed/i-b.txt"; fi

if fresh c1; then
  install_skills c1 "$X/skills-variants/s1"
  install_skills c1 "$X/skills-competitors"
fi
if fresh c2; then
  install_skills c2 "$X/skills-variants/s2"
  install_skills c2 "$X/skills-competitors"
fi
if fresh l1; then
  install_skills l1 "$X/skills-variants/s2"
  describe l1 "$(cat "$X/skills-variants/l1-description.txt")"
fi
for c in t1 t2 t3; do
  if fresh $c; then printf '%s\n' "$search_rule" > "$SB/app-sandbox-e-$c/AGENTS.md"; fi
done
[ -d "$SB/geo-sandbox" ] || mkdir "$SB/geo-sandbox"

ls -d "$SB"/app-sandbox-e-*
