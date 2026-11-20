#!/bin/bash
cd "$(dirname "$0")"
export RESUME=
python3 shot.py 20 stills 1135:1193 work/draft draft > work/d20.log 2>&1
python3 shot.py 21 stills 1194:1238 work/draft draft > work/d21.log 2>&1
python3 shot.py 22 stills 1239:1300 work/draft draft > work/d22.log 2>&1
echo done > work/draft_done
