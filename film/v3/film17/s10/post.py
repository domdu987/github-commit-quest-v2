#!/usr/bin/env python3
"""post.py <raw_dir> <frames_dir> [scale]: directional motion blur from the camera speed (whips + snaps), frames g 1336..1520.
The blur length follows the screen speed of a reference world point (part M: dupont's head; part R: the drawer front)."""
import os, sys, math
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shot as S

raw, out = sys.argv[1], sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
os.makedirs(out, exist_ok=True)
FOC = 782.2


def proj(loc, look, P):
    f = np.array(look, float) - np.array(loc, float); f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    d = np.array(P, float) - np.array(loc, float); z = d @ f
    z = max(z, 0.05)
    return np.array([360 + FOC * (d @ r) / z, 640 - FOC * (d @ u) / z])


REF_M, REF_R = (0.45, 2.25, 1.28), (-0.4, 0.5, 1.2)


def pos(g):
    if g <= S.G_M_END:
        return proj(*S.cam_M(g), REF_M)
    return proj(*S.cam_R(g), REF_R)


def kernel(L, ang):
    n = int(L) | 1
    n = max(n, 3)
    k = np.zeros((n, n), np.float32)
    c = n // 2
    dx, dy = math.cos(ang) * (n - 1) / 2, math.sin(ang) * (n - 1) / 2
    cv2.line(k, (int(round(c - dx)), int(round(c - dy))), (int(round(c + dx)), int(round(c + dy))), 1.0, 1, cv2.LINE_AA)
    return k / k.sum()


tab = {}
for g in range(S.FIRST, S.LAST + 1):
    lo = g - 1 if g - 1 != S.G_M_END and g != S.G_M_END + 1 else g          # one-sided at the part junction
    hi = g + 1 if g != S.G_M_END and g + 1 != S.G_M_END + 1 else g
    if g == S.G_M_END:
        lo, hi = g - 1, g
    if g == S.G_M_END + 1:
        lo, hi = g, g + 1
    lo, hi = max(lo, S.FIRST), min(hi, S.LAST)
    d = (pos(hi) - pos(lo)) / max(hi - lo, 1)
    L = float(np.hypot(*d))
    tab[g] = (L, math.atan2(d[1], d[0]))
    Lb = min(0.55 * L, 170.0) * scale
    src = os.path.join(raw, "g_%04d.png" % g)
    if not os.path.exists(src):
        continue
    im = cv2.imread(src)
    if Lb >= 4:
        if False:                      # long streaks: also a soft ghost of the unblurred frame is not wanted
            pass
        im = cv2.filter2D(im, -1, kernel(Lb, tab[g][1]), borderType=cv2.BORDER_REPLICATE)
    cv2.imwrite(os.path.join(out, "g_%04d.png" % g), im)
big = [(g, round(v[0])) for g, v in tab.items() if v[0] > 40]
print("blurred frames (g, px/frame):", big)
