"""Hook v2: the approved v1 conform (comp_finA) with the cut zoom removed. Only the frames that carried the zoom
(3 out + 3 in at every non-hard cut) are re-composited from the raw renders; every other frame is v1's, unchanged."""
import os, sys, shutil, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import finish as Fn, common as C, cues as Q
OLD = [0.04, 0.09, 0.15]
def old_amt(g):
    sid = C.shot_of(g); g0, g1 = C.shot_range(sid); i = C.SHOT_IDS.index(sid); a = 0.0
    if i + 1 < len(C.SHOT_IDS) and C.SHOT_IDS[i + 1] not in Q.HARD_CUTS and g1 - g <= 3: a = OLD[3 - (g1 - g)]
    if i > 0 and sid not in Q.HARD_CUTS and g - g0 < 3: a = max(a, OLD[2 - (g - g0)])
    return a
base = Fn.base_dir("final", 720, 1280)
A, N = os.path.join(base, "comp_finA"), os.path.join(base, "comp_nozoom")
os.makedirs(N, exist_ok=True)
J = [g for g in range(C.NF) if old_amt(g) > 0]
print("join frames:", len(J), J)
if "--check" in sys.argv:          # a non-join frame recomposited now must equal v1's
    for g in (100, 700, 900, 1250):
        im = np.asarray(Fn.comp_frame(base, g, 720, 1280).convert("RGB")); v1 = cv2.cvtColor(cv2.imread(os.path.join(A, "f_%04d.png" % (g + 1))), cv2.COLOR_BGR2RGB)
        print("check", g, "max diff", int(np.abs(im.astype(int) - v1).max()))
    sys.exit()
for g in range(C.NF):
    d = os.path.join(N, "f_%04d.png" % (g + 1))
    if g in J:
        im = Fn.comp_frame(base, g, 720, 1280)
        assert im is not None, "missing raw frame %d" % g
        im.save(d, compress_level=1)
    else:
        if os.path.exists(d): os.remove(d)
        os.link(os.path.join(A, "f_%04d.png" % (g + 1)), d)
Fn.icons().close()
print("built", N)
