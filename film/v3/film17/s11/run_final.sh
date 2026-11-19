#!/bin/bash
cd "$(dirname "$0")"
(python3 shot.py 27 final 1509:1578 final 20 > log_a1.txt 2>&1; python3 shot.py 28 final 1579:1615 final 20 > log_a2.txt 2>&1) &
python3 shot.py 28 final 1616:1700 final 20 > log_b.txt 2>&1
wait
