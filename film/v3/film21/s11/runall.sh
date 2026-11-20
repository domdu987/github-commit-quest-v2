#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film21/s11
python3 shot.py low final 1821:1848 raw/low 24 > log_low.txt 2>&1
python3 shot.py camp final 1633:1708 raw/camp 24 > log_camp.txt 2>&1
python3 shot.py bank final 1709:1820 raw/bank 24 > log_bank.txt 2>&1
