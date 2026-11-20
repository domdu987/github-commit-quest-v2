cd "$(dirname "$0")"
python3 shot.py final 885:1044 32 > log_final.txt 2>&1
echo done > final_done.txt
