#!/bin/bash
# qrun.sh <queue file> <pid to wait for or 0>   : runs the commands of the queue file one by one (each removed when started); waits for new lines
Q=$1; W=$2
[ "$W" != "0" ] && while kill -0 $W 2>/dev/null; do sleep 10; done
export SETPROJ=/tmp/claude-0/-home-user-github-commit-quest-v2/f179a70c-581e-5684-9961-eff4e8515831/scratchpad/snap/film
while true; do
  L=$(head -n1 "$Q" 2>/dev/null)
  if [ -z "$L" ]; then [ -f "$Q.stop" ] && exit 0; sleep 20; continue; fi
  sed -i '1d' "$Q"
  echo "$(date +%T) START $L" >> "$Q.log"
  bash -c "$L" >> "$Q.log" 2>&1
  echo "$(date +%T) DONE $L" >> "$Q.log"
done
