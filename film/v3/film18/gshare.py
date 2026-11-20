#!/usr/bin/env python3
"""bare-ground share on RENDERED frames: python3 gshare.py dir first last horizon_y
bare = pixels below the horizon whose colour is within tolerance of the dominant (modal) field colour of that frame and locally smooth (no outlines/props/ox)."""
import sys, os, numpy as np, cv2
d, a, b, hy = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
out = []
for g in range(a, b + 1, 3):
    im = cv2.imread(os.path.join(d, 'g_%04d.png' % g));
    if im is None: continue
    reg = im[hy:].astype(np.int32)
    q = (reg // 12).reshape(-1, 3); key = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
    k = np.bincount(key - key.min()).argmax() + key.min(); mode = np.array([k // 10000, (k // 100) % 100, k % 100]) * 12 + 6
    dist = np.abs(reg - mode).max(2); near = dist < 34
    sm = cv2.blur(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32), (5, 5)); loc = np.abs(cv2.GaussianBlur(sm, (0, 0), 3) - sm)[hy:]
    smooth = cv2.blur(loc, (9, 9)) < 3.0
    out.append(float((near & smooth).mean()))
print('ground bare share median %.2f max %.2f (n=%d)' % (np.median(out), max(out), len(out)))
