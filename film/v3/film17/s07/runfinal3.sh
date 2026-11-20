#!/bin/bash
cd "$(dirname "$0")"
(THREADS=2 python3 shot.py final 19 996:1023 1.0 16 work/F19 > work/fl19a.log 2>&1) &
(THREADS=2 python3 shot.py final 19 1024:1051 1.0 16 work/F19 > work/fl19b.log 2>&1) &
wait
