import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c19 as C
from mathutils import Vector
F = C.F_PX
def proj(P, loc, look):
    f, r, u = C._cam_basis(loc, look)
    d = Vector(P) - Vector(loc); z = d.dot(f)
    return (360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z, F / z, z)
PT = {"har": (-1.6, 2.85, 2.8), "mock": (1.6, 2.85, 2.9), "box": (0.37, 3.0, 1.9), "far": (0.0, 9.0, 2.5), "left": (-4.5, 6.0, 2.0)}
G0, GL, SN = 1747, 1865, (1818, 1834)
res = []
for cx, cz, slide, arc, rise, push, sx in itertools.product([-1.2, -0.6, 0.0, 0.6, 1.2], [2.5, 3.0], [-40, -20, 0, 20, 40], [-8, -4, 0, 4, 8], [0, 20, 40], [0.08, 0.10], [0.0, 0.3]):
    cam = C.CamPath((cx, -4.4, cz), (0.25, 2.9, 1.95), G0, GL, push=push, slide_px=slide, rise_px=rise, arc_deg_s=arc, decay=0.1,
                    snaps=[dict(g=SN, k=1.3, peak=1.5, shift=(sx, 0.0))])
    pen = 0; sp = 0; n = 0
    for g in range(G0, GL, 3):
        loc, look = cam.at(g)
        for nm in ("har", "mock"):
            x, y, s, z = proj(PT[nm], loc, look)
            hw = s * 0.7
            if x - hw < 5 or x + hw > 715: pen += 1
            if not (450 < y < 760): pen += 1
        x, y, s, z = proj(PT["box"], loc, look)
        if not (150 < x < 570): pen += 1
        a = [proj(P, loc, look) for P in PT.values()]; b = [proj(P, *cam.at(g + 3)) for P in PT.values()]
        sp += sum(math.hypot(p[0] - q[0], p[1] - q[1]) for p, q in zip(a, b)) / len(a) / 3; n += 1
    sp /= n
    res.append((round(pen - sp * 3, 2), round(sp, 2), cx, cz, slide, arc, rise, push, sx))
res.sort()
for r in res[:6]: print(r)
