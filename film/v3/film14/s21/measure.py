"""measure.py: hive-vs-post gaps MEASURED FROM RENDERED PNGs (not Blender data). usage: python3 measure.py g0 g1 -> prints table, writes measured_table.md
Per frame renders at 360x640 / 6 samples: A normal, B hive_1 hidden, C posts hidden. hive mask = |A-B|, post mask = |A-C| (windows around unit 1's two posts)."""
import sys, os, json
os.environ.setdefault('THREADS', '4'); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]] + sys.argv[1:]
import numpy as np
from PIL import Image
import shot as S
from shot import *
g0, g1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, -1)
d = S.Driver('preview', 4); bpy.context.scene.cycles.samples = 6
T = os.path.join(HERE, 'work_measure'); os.makedirs(T, exist_ok=True)
def ld(p): return np.asarray(Image.open(p).convert('RGB'), float)
def measure_frame(d, g):
    pa, pb, pc = [os.path.join(T, '%s_%d.png' % (k, g)) for k in 'abc']
    d.frame(g, pa); d.frame(g, pb, hide=('hive_1',)); d.frame(g, pc, hide=('posts_wood',))
    A, B, Cc = ld(pa), ld(pb), ld(pc)
    h1 = F.STATE['hive'][1]; c0 = h1.location
    P = [C.screen((c0.x + dx, c0.y, c0.z + dz)) for dx in (-d.hx, d.hx) for dz in (0.0, -0.8)]
    wx0 = int(min(p[0] for p in P) / 2) - 25; wx1 = int(max(p[0] for p in P) / 2) + 25; wy0 = int(min(p[1] for p in P) / 2) - 10; wy1 = int(max(p[1] for p in P) / 2) + 10
    dif = np.abs(A - B).sum(-1) > 60; mh = np.zeros_like(dif); mh[max(wy0, 0):wy1, max(wx0, 0):wx1] = dif[max(wy0, 0):wy1, max(wx0, 0):wx1]
    cols = mh.sum(0) >= 6; mh[:, ~cols] = False
    mp = np.abs(A - Cc).sum(-1) > 22
    ys, xs = np.nonzero(mh)
    if len(xs) == 0: return None
    ymid0, ymid1 = np.percentile(ys, 20), np.percentile(ys, 80); hx0, hx1 = int(xs.min()), int(xs.max())
    band = mp[int(ymid0):int(ymid1) + 1].sum(0) > 0.5 * (int(ymid1) - int(ymid0) + 1)
    cs = np.nonzero(band)[0]; cx = (hx0 + hx1) / 2; L = cs[cs < cx]; R = cs[cs > cx]
    return (g, hx0 * 2, hx1 * 2, None if not len(L) else int(L.max()) * 2, None if not len(R) else int(R.min()) * 2)

if __name__ == '__main__':
    rows = []
    for g in range(g0, g1 + 1):
        r = measure_frame(d, g); rows.append(r); print(r, flush=True)
    json.dump(rows, open(os.path.join(HERE, 'measured_table.json'), 'w'))
