#!/bin/bash
# T6b full render g1536-1701, 30-frame chunks (fresh Blender process each: no cast leak), resumable (render_t6b.py skips frames > 50 kB)
cd "$(dirname "$0")"
for g0 in $(seq 1536 30 1701); do
  g1=$((g0+29)); [ $g1 -gt 1701 ] && g1=1701
  python3 render_t6b.py frames $g0 $g1 >> render.log 2>&1
done
echo ALLDONE >> render.log
