#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final 900:923 1.0 28 > log_a1.txt 2>&1; python3 shot.py final 948:971 1.0 28 > log_a2.txt 2>&1; python3 shot.py final 996:1023 1.0 16 > log_a3.txt 2>&1 ) &
( python3 shot.py final 924:947 1.0 28 > log_b1.txt 2>&1; python3 shot.py final 972:995 1.0 28 > log_b2.txt 2>&1; python3 shot.py final 1024:1051 1.0 16 > log_b3.txt 2>&1 ) &
wait
