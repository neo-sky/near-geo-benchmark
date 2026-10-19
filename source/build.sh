#!/bin/bash
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
X=$ROOT/experiments
S=$ROOT/source
B=$S/.build
mode=${1:-final}

mkdir -p "$B/fragments" "$B/figures"
cd "$X"
python3 analysis.py > results.json
python3 tables.py results.json "$B/fragments" "$B/figures"
cp "$S"/appendix/*.md "$B/fragments/"
python3 render.py "$S/near-geo-paper.md" "$B/fragments" "$B/near-geo-paper.md"
cp "$S/near-geo-proposal.md" "$B/"

if [ "$mode" = final ] && grep -n 'PENDING' "$B/near-geo-paper.md"; then
  echo "pending sections remain" >&2
  exit 1
fi
unlabelled=$(jq -r '[.arms | to_entries[] | select(.value.unlabelled > 0) | .key] | join(" ")' \
  results.json)
if [ "$mode" = final ] && [ -n "$unlabelled" ]; then
  echo "unlabelled runs in: $unlabelled" >&2
  exit 1
fi

cd "$B"
for doc in near-geo-paper near-geo-proposal; do
  pandoc "$doc.md" -f markdown-auto_identifiers-smart --no-highlight --dpi=200 \
    --reference-doc "$S/reference.docx" -o "$B/$doc.docx"
  python3 "$S/gdocs.py" "$B/$doc.docx" "$ROOT/$doc.docx"
  soffice --headless --convert-to pdf --outdir "$B" "$ROOT/$doc.docx" > /dev/null 2>&1
  echo "$doc.docx: $(pdfinfo "$B/$doc.pdf" | awk '/^Pages/ {print $2}') pages"
done
