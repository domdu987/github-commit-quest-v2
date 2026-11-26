#!/bin/sh
F=__PROJ__/v3/film
for t in s10 s11 s09; do
  cd $F/$t || exit 1
  rm -rf frames
  python3 shot.py render > work/render.log 2>&1 || { echo "$t render failed" >> $F/s10/work/chain.log; exit 1; }
  python3 shot.py post > work/post.log 2>&1
  python3 shot.py contact >> work/post.log 2>&1
  echo "$t done $(date)" >> $F/s10/work/chain.log
done
