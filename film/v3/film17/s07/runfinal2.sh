#!/bin/bash
cd "$(dirname "$0")"
(THREADS=2 python3 shot.py final 17 900:947 1.0 16 work/F17 > work/fl17.log 2>&1) &
(THREADS=2 python3 shot.py final 19 996:1051 1.0 16 work/F19 > work/fl19.log 2>&1) &
wait
