#!/bin/bash
# usage (in take folder): bash ../v2_report.sh <first_g> <cuts>   -> QA_V2.md pieces: qa_jitter, qa_auto, ground (GROUND.md must exist)
F=$1
python3 /home/user/github-commit-quest-v2/film/qa_jitter.py take.mkv > JITTER.txt 2>&1
python3 /home/user/github-commit-quest-v2/film/qa_auto.py take.mkv --first_g $F --cuts "${2:-}" 2>&1 | head -2
cat JITTER.txt
