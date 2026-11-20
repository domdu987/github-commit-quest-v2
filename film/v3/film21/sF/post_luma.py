"""post_luma.py <raw_dir> <out_dir> <first_g> <last_g> [target]: one constant extra gamma per segment (equivalent to a higher VIVID gamma, API.md §9) so the mean luma of the
take lands at ~target (QA_TEAM §G/§I: 85-110).  Raw frames stay untouched."""
import sys, os, glob, numpy as np
from PIL import Image
raw, out, g0, g1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); tgt = float(sys.argv[5]) if len(sys.argv) > 5 else 100.0
os.makedirs(out, exist_ok=True)
fs = [os.path.join(raw, "g_%04d.png" % g) for g in range(g0, g1 + 1)]
def luma(gam):
    m = []
    for f in fs[::6]:
        a = np.asarray(Image.open(f).convert("RGB"), np.float32) / 255.0
        m.append((a ** gam).mean() * 255)
    return float(np.mean(m))
lo, hi = 1.0, 3.0
for _ in range(14):
    mid = (lo + hi) / 2
    if luma(mid) > tgt: lo = mid
    else: hi = mid
gam = (lo + hi) / 2; print("extra gamma %.3f -> luma %.1f (raw %.1f)" % (gam, luma(gam), luma(1.0)))
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB"), np.float32) / 255.0
    Image.fromarray((np.clip(a ** gam, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, os.path.basename(f)))
open(os.path.join(out, "gamma.txt"), "w").write("%.3f\n" % gam)
