#!/bin/bash
# draftX.sh EP EVERY shot[:level]... : landscape draft frames of the EP.2-4 engine into raw_ep<EP>L_draft
cd "$(dirname "$0")"; export LT_EP=$1 LT_ORI=L; ev=$2; shift 2
for s in "$@"; do n=${s%%:*}; lv=""; [ "$n" != "$s" ] && lv="--level ${s#*:}"
  python3 lt_epx.py render $n --draft --every $ev $lv 2>&1 | grep -E "Error|rror:|Traceback|line [0-9]+" | grep -v CUEW | tail -4; echo "done $n"; done
echo DRAFT-END
