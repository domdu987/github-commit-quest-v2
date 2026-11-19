#!/bin/sh
# usage: runloop.sh log a:b  (retries; skips finished frames)
for i in 1 2 3 4 5 6; do python3 shot.py final 18 $2 frames >> $1 2>&1 && break; echo retry >> $1; done
