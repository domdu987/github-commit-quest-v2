#!/bin/bash
# relaunch loop: if fewer than 2 shot.py workers are alive and frames are missing, restart the missing ranges (shot.py skips finished frames)
cd "$(dirname "$0")"
while true; do
  n=$(ls work/frames 2>/dev/null | grep -c 'png$')
  [ "$n" -ge 254 ] && break
  if [ "$(pgrep -fc 'python3 shot.py')" -lt 2 ]; then
    for r in "11 753:820" "13 864:929" "12 821:863" "14 930:1006"; do
      set -- $r; [ "$(pgrep -fc 'python3 shot.py')" -ge 2 ] && break
      python3 shot.py $1 $2 work/frames final >> work/log_wd_$1.txt 2>&1 &
    done
  fi
  sleep 60
done
