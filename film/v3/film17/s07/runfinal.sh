#!/bin/bash
cd "$(dirname "$0")"
(THREADS=2 python3 shot.py final 16 844:899 1.0 16 work/F16 > work/fl16.log 2>&1; THREADS=2 python3 shot.py final 18 948:995 1.0 16 work/F18 > work/fl18.log 2>&1) &
(THREADS=2 python3 shot.py final 17 900:947 1.0 16 work/F17 > work/fl17.log 2>&1; THREADS=2 python3 shot.py final 19 996:1051 1.0 16 work/F19 > work/fl19.log 2>&1) &
wait
