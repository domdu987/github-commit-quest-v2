#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final s17 975:1130 work/f17 12 > work/log17c.txt 2>&1 ) &
( python3 shot.py final s24 1263:1334 work/f24 12 > work/log24c.txt 2>&1 ) &
wait
