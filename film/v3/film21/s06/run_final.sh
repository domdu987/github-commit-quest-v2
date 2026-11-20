cd "$(dirname "$0")"
python3 shot.py 15 final 878:937 24 > log_f15.txt 2>&1
python3 shot.py 16 final 938:985 24 > log_f16.txt 2>&1
python3 shot.py 17 final 986:1050 24 > log_f17.txt 2>&1
echo done > final_done.txt
