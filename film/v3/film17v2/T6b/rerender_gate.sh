#!/bin/bash
# TAKE-gate re-render of g1536-1674 into frames_new/ (copied over frames/ after QA). Two streams:
#  A: g1536-1575, one fresh process per frame (join lights: T6a2 setup eased into T6b's override, beam hidden) via join_one.sh (OUTDIR=frames_new)
#  B: g1576-1674 in 25-frame chunks (fresh Blender process per chunk)
cd "$(dirname "$0")"; export OUTDIR=frames_new
( seq 1536 1575 | xargs -n1 ./join_one.sh ) &
( for g0 in $(seq 1576 25 1674); do g1=$((g0+24)); [ $g1 -gt 1674 ] && g1=1674; python3 render_t6b.py frames_new $g0 $g1 >> render_new.log 2>&1; done; echo B_DONE >> render_new.log ) &
wait
echo ALLDONE_GATE >> render_new.log
