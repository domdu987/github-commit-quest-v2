cd "$(dirname "$0")"
rm -rf raw_draft
python3 shot.py 15 draft 878:937 6 > log_d15.txt 2>&1
python3 shot.py 16 draft 938:985 6 > log_d16.txt 2>&1
python3 shot.py 17 draft 986:1050 6 > log_d17.txt 2>&1
echo done > draft_done.txt
