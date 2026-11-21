#!/bin/sh
while kill -0 2174 2>/dev/null; do sleep 10; done
cd __PROJ__/v3/film/s13 && python3 shot.py render > work/render.log 2>&1
echo "s13 render exit $? $(date)" >> work/chain.log
