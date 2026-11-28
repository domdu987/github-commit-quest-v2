#!/bin/bash
# backup.sh -- source + audio archive of the whole project, WITHOUT frame folders, under 150 MB.
#   bash backup.sh [label]        -> PROJ/ep1/backup/dz09_src_<date>_<label>.tar.gz  + .manifest.txt  + .sha256
# In:  every source / text file of the project (py, md, json, sh, txt, ass, svg, html, js, css, cfg), fonts, the user's
#      sheets (uploads/), code-drawn textures (tex/ folders), per-shot manifests and render logs (small), then audio in
#      this order while the budget allows: audio/narr_ohm (the paid takes and the mix), audio/ep1 (new takes), audio/sfx,
#      audio/ep1_hook, audio/narr_v1, audio/voice_pick, audio/th.
# Out: out/ tmp/ frames/ comp/ cache/ __pycache__/ folders, EXR passes, PNG / JPG / MP4 renders, anything else binary.
# Nothing is pushed anywhere: the archive stays on this disk until the user says where it goes.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(cd "$HERE/../.." && pwd)"
DEST="$PROJ/ep1/backup"
LIMIT_MB="${LIMIT_MB:-150}"
LABEL="${1:-daily}"
STAMP="$(date +%Y%m%d_%H%M)"
NAME="dz09_src_${STAMP}_${LABEL}"
mkdir -p "$DEST"
LIST="$(mktemp)"; trap 'rm -f "$LIST" "$LIST.a"' EXIT
cd "$PROJ"
PRUNE=( -name out -o -name tmp -o -name __pycache__ -o -name frames -o -name comp -o -name cache -o -name backup -o -name master_work -o -name .git )
# 1. source and text (small files only: a 50 MB json is a render artefact, not source)
find . \( "${PRUNE[@]}" \) -prune -o -type f \( -name '*.py' -o -name '*.md' -o -name '*.json' -o -name '*.sh' -o -name '*.txt' -o -name '*.ass' \
     -o -name '*.svg' -o -name '*.html' -o -name '*.js' -o -name '*.css' -o -name '*.cfg' -o -name '*.ttf' -o -name '*.otf' \) -size -3M -print > "$LIST"
# 2. the user's sheets and the code-drawn textures
find ./uploads -type f -print >> "$LIST" 2>/dev/null || true
find . \( "${PRUNE[@]}" \) -prune -o -type f -path '*/tex/*' -size -3M -print >> "$LIST"
# 3. shot manifests, signatures and per-frame logs from the out/ folders (text, small)
find . -type f \( -name 'manifest.json' -o -name 'sig.json' -o -name 'log_*.jsonl' \) -path '*/out/*' -size -3M -print >> "$LIST" 2>/dev/null || true
sort -u "$LIST" -o "$LIST"
size_mb() { tr '\n' '\0' < "$1" | du -c --files0-from=- 2>/dev/null | tail -n 1 | awk '{printf "%d", $1/1024}'; }
BASE_MB=$(size_mb "$LIST")
# 4. audio, most valuable first, while it fits (audio does not compress: count it at full size)
INCLUDED=""; SKIPPED=""
for d in audio/narr_ohm audio/ep1 audio/sfx audio/ep1_hook audio/narr_v1 audio/voice_pick audio/th; do
  [ -d "$d" ] || continue
  find "./$d" -type f \( -name '*.wav' -o -name '*.mp3' -o -name '*.m4a' -o -name '*.flac' -o -name '*.ogg' \) -print > "$LIST.a"
  [ -s "$LIST.a" ] || continue
  A_MB=$(size_mb "$LIST.a")
  if [ $((BASE_MB + A_MB)) -le $((LIMIT_MB - 10)) ]; then
    cat "$LIST.a" >> "$LIST"; BASE_MB=$((BASE_MB + A_MB)); INCLUDED="$INCLUDED $d(${A_MB}MB)"
  else
    SKIPPED="$SKIPPED $d(${A_MB}MB)"
  fi
done
sort -u "$LIST" -o "$LIST"
N=$(wc -l < "$LIST")
nice -n 10 tar -czf "$DEST/$NAME.tar.gz" -T "$LIST"
MB=$(du -m "$DEST/$NAME.tar.gz" | cut -f1)
{ echo "archive: $NAME.tar.gz   $MB MB   $N files   made $(date '+%Y-%m-%d %H:%M:%S')   root: $PROJ"
  echo "audio in:$INCLUDED"; echo "audio left out (over the ${LIMIT_MB} MB budget):${SKIPPED:- none}"
  echo "restore: mkdir dz09 && tar -xzf $NAME.tar.gz -C dz09"; echo "--- files"; cat "$LIST"; } > "$DEST/$NAME.manifest.txt"
( cd "$DEST" && sha256sum "$NAME.tar.gz" > "$NAME.sha256" )
echo "wrote $DEST/$NAME.tar.gz  $MB MB  $N files"
echo "audio in:$INCLUDED"
echo "audio left out:${SKIPPED:- none}"
if [ "$MB" -ge "$LIMIT_MB" ]; then echo "ERROR: archive is $MB MB, the limit is $LIMIT_MB MB" >&2; exit 3; fi
nice -n 10 tar -tzf "$DEST/$NAME.tar.gz" > /dev/null && echo "archive reads back"
