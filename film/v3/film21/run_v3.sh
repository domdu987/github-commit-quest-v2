#!/bin/bash
cd "$(dirname "$0")"
export RESUME=1
(cd sG && python3 shot.py frames 1141:1238 work/frames final 32 >> work/f5.log 2>&1)
(cd sJ1 && python3 shot.py frames 1640:1708 work/frames final 32 >> work/f5.log 2>&1)
echo done > run_v3_done
