#!/bin/bash
# Usage: PROJ=<project dir> WF_DIR=<folder that holds the workflow run folders> bash watch_polish.sh <run id>
# Run it in the background; it is a wake-up call, it changes nothing. WF_DIR: see watch_prod.sh.
# Exits when the polish run looks stalled (nothing written for 30 min) or after 110 min (heartbeat).
P=${PROJ:?set PROJ to the project folder}
W=${WF_DIR:?set WF_DIR to the folder that holds the workflow run folders}/$1
status() {
  for f in $W/agent-*.jsonl; do [ -f "$f" ] && printf "%s age=%ss | " "$(basename $f .jsonl | cut -c7-13)" $(( $(date +%s) - $(stat -c %Y $f) )); done; echo
  grep -o '"label":"[^"]*"' $W/journal.jsonl 2>/dev/null | tr '\n' ' '; echo
  printf "graded=%s " $(ls $P/v3/film/out_v11/graded 2>/dev/null | wc -l); echo
  ls $P/v3/film/out_v11 2>/dev/null | tr '\n' ' '; echo
}
start=$(date +%s)
while true; do
  now=$(date +%s); newest=0
  for f in $W/agent-*.jsonl; do [ -f "$f" ] && t=$(stat -c %Y $f) && [ $t -gt $newest ] && newest=$t; done
  t=$(find $P/v3/film $P/v3/out $P/deliver -type f -mmin -30 2>/dev/null | head -1)
  if [ -z "$t" ] && [ $(( now - newest )) -gt 1800 ]; then echo "STALL nothing written for 30 min"; status; exit 0; fi
  if [ $(( now - start )) -gt 6600 ]; then echo "HEARTBEAT 110 min"; status; exit 0; fi
  sleep 120
done
