#!/bin/bash
# renders every contact tile (720x1280, 12 samples), 2 in parallel; log in final_log.txt
cd "$(dirname "$0")/.."
mkdir -p work/final; : > work/final_log.txt
cut -d'|' -f1 work/contact_order.txt | xargs -P2 -I{} sh -c 'python3 chicago.py final "{}" 2>&1 | grep " wall " >> work/final_log.txt'
sort work/final_log.txt -o work/final_log.txt
