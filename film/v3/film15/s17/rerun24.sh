#!/bin/bash
cd "$(dirname "$0")"
while [ $(ls work/f17 | wc -l) -lt 207 ]; do sleep 5; done
python3 shot.py final s24 1263:1334 work/f24 12 > work/log24d.txt 2>&1
