#!/bin/bash
# usage: run2.sh g0 g1   (resumes: skips finished frames)
cd "$(dirname "$0")"
n=$(( $2 - $1 + 1 ))
until [ "$(for g in $(seq $1 $2); do [ -s frames/g_$g.png ] && echo 1; done | wc -l)" -ge $n ]; do python3 render_T7.py $1 $2 frames >> render_$1.log 2>&1; sleep 5; done
