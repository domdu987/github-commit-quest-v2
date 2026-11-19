#!/bin/bash
cd "$(dirname "$0")"
python3 shot.py final s17 924:1013 work/f17 12 > work/log17e1.txt 2>&1
python3 shot.py final s17 1058:1130 work/f17 12 > work/log17e2.txt 2>&1
