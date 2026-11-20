#!/bin/bash
cd "$(dirname "$0")"
export RESUME=1
python3 shot.py 20 stills 1135:1193 work/frames final 24 > work/f20.log 2>&1
python3 shot.py 21 stills 1194:1238 work/frames final 24 > work/f21.log 2>&1
python3 shot.py 22 stills 1239:1300 work/frames final 24 > work/f22.log 2>&1
echo done > work/final_done
