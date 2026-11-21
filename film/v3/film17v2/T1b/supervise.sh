#!/bin/bash
# usage: supervise.sh <g0> <g1> [rev]  -- restarts render.py until every frame g0..g1 exists (> 50 kB)
cd "$(dirname "$0")"; g0=$1; g1=$2; dir=$3
while true; do
  miss=0; for g in $(seq $g0 $g1); do f=$(printf 'frames/g_%04d.png' $g); [ -s "$f" ] && [ $(stat -c %s "$f") -gt 50000 ] || { miss=1; break; }; done
  [ $miss = 0 ] && break
  python3 render.py full $g0 $g1 $dir >> render_$g0.log 2>&1
done
