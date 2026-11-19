#!/bin/bash
# Usage: PROJ=<project dir> WF_DIR=<folder that holds the workflow run folders> [FILM=deliver/<film>.mp4] [REVIEW=deliver/<review>.md] \
#        bash watch_prod.sh <run id> [<run id> ...]
# Run it in the background; it is a wake-up call, it changes nothing. WF_DIR is the subagents/workflows folder of
# this conversation, ~/.claude/projects/<project folder slug>/<conversation id>/subagents/workflows (each run folder
# wf_<id>/ holds agent-*.jsonl transcripts and journal.jsonl). FILM and REVIEW are the delivery files the finishing
# workflow writes, relative to PROJ; the defaults are film 1's names (deliver/film_v1_thai.mp4, deliver/QA_film.md).
# Exits when: the film exists, production looks stalled (nothing written for 30 min), or after 110 min (heartbeat).
P=${PROJ:?set PROJ to the project folder}
W=${WF_DIR:?set WF_DIR to the folder that holds the workflow run folders}
RUNS="$@"
FILM=${FILM:-deliver/film_v1_thai.mp4}
REVIEW=${REVIEW:-deliver/QA_film.md}
status() {
  for d in $P/v3/film/s??; do n=$(ls $d/frames 2>/dev/null | wc -l); m=$([ -f $d/meta.json ] && echo meta || echo -); q=$([ -f $d/QA.md ] && echo QA || echo -); printf "%s:%s:%s:%s " $(basename $d) $n $m $q; done; echo
  for r in $RUNS; do for f in $W/$r/agent-*.jsonl; do [ -f "$f" ] && printf "%s age=%ss | " "$(basename $f .jsonl | cut -c1-12)" $(( $(date +%s) - $(stat -c %Y $f) )); done; done; echo
  ls $P/v3/film/out 2>/dev/null | tr '\n' ' '; echo
}
start=$(date +%s)
while true; do
  now=$(date +%s)
  if [ -f "$P/$FILM" ] && [ -f "$P/$REVIEW" ]; then echo "DONE film and review exist"; status; exit 0; fi
  newest=0
  for f in $(ls -t $W/*/agent-*.jsonl 2>/dev/null | head -3); do t=$(stat -c %Y $f); [ $t -gt $newest ] && newest=$t; done
  t=$(find $P/v3/film $P/v3/set3d_ext $P/deliver -type f -mmin -30 2>/dev/null | head -1)
  if [ -z "$t" ] && [ $(( now - newest )) -gt 1800 ]; then echo "STALL nothing written for 30 min"; status; exit 0; fi
  if [ $(( now - start )) -gt 6600 ]; then echo "HEARTBEAT 110 min"; status; exit 0; fi
  sleep 120
done
