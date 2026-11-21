#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/set3d22
: > _contact_b.log
for sh in s03 s09 s10 s11 s12 s13 s14; do
 for w in start mid end; do
  
  while pgrep -f "beck.py shot" >/dev/null 2>&1 && [ -z "$MINE" ]; do sleep 3; done
  python3 beck.py shot $sh $w contact/B_${sh}_$w.png 2>&1 | grep -E "frame|total|Traceback|Error" >> _contact_b.log
 done
done
echo DONE >> _contact_b.log
