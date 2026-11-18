#!/bin/bash
# relaunch the two render processes; frames that already exist are skipped
cd "$(dirname "$0")"; export THREADS=2 SAMPLES=20
nohup python3 shot.py final 1043:1194 >> run_a3.log 2>&1 &
nohup python3 shot.py final 1195:1345 >> run_b3.log 2>&1 &
