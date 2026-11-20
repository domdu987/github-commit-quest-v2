import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c19 as C
from mathutils import Vector
F = C.F_PX
def proj(P, loc, look):
    f, r, u = C._cam_basis(loc, look)
    d = Vector(P) - Vector(loc); z = d.dot(f)
    return (360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z, F / z, z)
B = [(-2.6, 3.4, 2.85), (-1.5, 0.5, 2.9), (1.9, 0.5, 2.5)]
HAR = (0.0, -5.0, 2.8)
G0, GL, SN = 764, 871, (843, 857)
res = []
for cx, slide, arc, rise, push, sx in itertools.product([-0.6, 0.0, 0.6], [-20, 0, 20, 40], [-6, -3, 0, 3, 6], [0, 25], [0.04, 0.06, 0.08], [0.0, 0.5, 1.0]):
    cam = C.CamPath((cx, 9.4, 3.6), (0.0, -5.0, 2.0), G0, GL, push=push, slide_px=slide, rise_px=rise, arc_deg_s=arc, decay=0.05,
                    snaps=[dict(g=SN, k=3.0, peak=1.6, shift=(sx, 0.7))])
    pen = 0; sp = 0; n = 0
    for g in range(G0, 825, 3):
        loc, look = cam.at(g)
        for P in B:
            x, y, s, z = proj(P, loc, look)
            if z < 1 or x - s * 0.7 < 0 or x + s * 0.7 > 720: pen += 1
        pr = [proj(P, loc, look) for P in B]
        for i in range(3):
            for j in range(i + 1, 3):
                if abs(pr[i][0] - pr[j][0]) < 0.6 * (pr[i][2] + pr[j][2]) * 0.5 + 60: pen += 1
        a = [proj(P, loc, look) for P in B + [HAR]]; b = [proj(P, *cam.at(g + 3)) for P in B + [HAR]]
        sp += sum(min(12, math.hypot(p[0] - q[0], p[1] - q[1])) for p, q in zip(a, b)) / 4 / 3; n += 1
    l, k = cam.at(858); x, y, s, z = proj(HAR, l, k)
    pen += abs(x - 360) / 40 + abs(y - 640) / 40 + max(0, 215 - s) / 20
    res.append((round(pen - 3 * sp / n, 2), round(sp / n, 2), cx, slide, arc, rise, push, sx, round(x), round(y), round(s)))
res.sort()
for r in res[:6]: print(r)
