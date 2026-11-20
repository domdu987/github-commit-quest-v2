#!/bin/bash
# usage: tune.sh first last   -> 0.25 scale draft + frame-diff numbers (in-shot = G0..G1-1)
cd "$(dirname "$0")"; rm -rf work/draft
for k in 0 1; do python3 shot.py final $(( $1 + k )):$2:2 0.25 4 > work_draft_$k.log 2>&1 & done; wait
python3 - "$@" <<'P'
import glob,sys,re
sys.path.insert(0,'.')
import c19 as C, numpy as np
import shot as S
fs=sorted(glob.glob('work/draft/g_*.png'))
m,p,d=C.framediff(fs); a=S.G0-S.G_FIRST; b=S.G1-S.G_FIRST
ins=d[a:b-1]
print(len(fs), "median %.2f p90 %.2f min %.2f max %.2f"%(np.median(ins), np.percentile(ins,90), min(ins), max(ins)))
print([round(x,1) for x in ins])
P
