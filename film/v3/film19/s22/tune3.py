import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c19 as C
from mathutils import Vector
F = C.F_PX
def proj(P, loc, look):
    f, r, u = C._cam_basis(loc, look)
    d = Vector(P) - Vector(loc); z = d.dot(f)
    return (360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z, F / z, z)
HAR = (-1.6, 2.85, 2.8); MOCK = (1.6, 2.85, 2.9); BOX = (0.37, 3.0, 1.9)
G0, GL, SN = 1747, 1865, (1818, 1834)
res = []
for cx, cz, slide, arc, rise, sx, sy, k in itertools.product([-1.2, -0.6, 0.0, 0.6, 1.2], [2.5, 3.0], [-40, -20, 0, 20, 40], [-8, -4, 0, 4, 8], [0, 20, 40], [0.0, 0.4, 0.8, 1.2], [-0.2, 0.0, 0.2], [1.6, 2.0]):
    cam = C.CamPath((cx, -4.4, cz), (0.25, 2.9, 1.95), G0, GL, push=0.10, slide_px=slide, rise_px=rise, arc_deg_s=arc, decay=0.1,
                    snaps=[dict(g=SN, k=k, peak=1.5, shift=(sx, sy))])
    pen = 0; sp = 0; n = 0
    for g in range(G0, GL, 3):
        loc, look = cam.at(g)
        if g < 1815:
            for P in (HAR, MOCK):
                x, y, s, z = proj(P, loc, look)
                if z < 1 or x - s * 0.6 < 5 or x + s * 0.6 > 715 or not (450 < y < 760): pen += 1
        x, y, s, z = proj(BOX, loc, look)
        if z < 1 or not (100 < x < 620): pen += 1
        a = [proj(P, loc, look) for P in (HAR, MOCK, BOX)]; b = [proj(P, *cam.at(g + 3)) for P in (HAR, MOCK, BOX)]
        sp += sum(min(12, math.hypot(p[0] - q[0], p[1] - q[1])) for p, q in zip(a, b)) / 3 / 3; n += 1
        if min(p[3] for p in a) < 1.5: pen += 5
    x, y, s, z = proj(MOCK, *cam.at(1860)); xb, yb, sb, zb = proj(BOX, *cam.at(1860))
    pen += abs(xb - 340) / 40 + max(0, abs(x - 600) - 80) / 40 + (3 if not (500 < y < 700) else 0) + (2 if sb < 150 else 0) + (3 if x + s * 0.6 > 715 else 0)
    res.append((round(pen - sp, 2), round(sp / n, 2), cx, cz, slide, arc, rise, sx, sy, k, round(x), round(xb), round(sb)))
res.sort()
for r in res[:6]: print(r)
