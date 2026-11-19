#!/usr/bin/env python3
"""frame-diff numbers: python3 fd.py dir first last  -> median / p90 of mean abs diff x255 on 90x160 grey frames"""
import sys, os, numpy as np, cv2
d, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
fr = []
for g in range(a, b + 1):
    p = os.path.join(d, 'g_%04d.png' % g)
    if os.path.exists(p): fr.append(cv2.resize(cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2GRAY), (90, 160), interpolation=cv2.INTER_AREA).astype(np.float32))
df = [float(np.abs(x - y).mean()) for x, y in zip(fr[1:], fr[:-1])]
print('n=%d median %.2f p90 %.2f min %.2f max %.2f' % (len(df), np.median(df), np.percentile(df, 90), min(df), max(df)))
