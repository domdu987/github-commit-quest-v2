import sys, os, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c19 as C
from mathutils import Vector
F = C.F_PX
def proj(P, loc, look):
    f, r, u = C._cam_basis(loc, look)
    d = Vector(P) - Vector(loc); z = d.dot(f)
    return (360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z, F / z, z)
HEAD = {"mock": (-2.3, 1.7, 2.85), "bb": (-2.3, 3.5, 2.9), "cc": (2.3, 2.4, 2.5), "bd": (2.3, 4.2, 2.9)}
HAR = (0.0, -5.0, 2.8)
G0, GL, SN = 764, 871, (843, 857)
res = []
for cx, cz, slide, arc, rise, k, sy, push in itertools.product([-0.6, 0.0, 0.6, 1.2], [3.6, 4.4], [-40, -20, 0, 20], [-8, 0, 8], [0, 25], [3.0], [0, -0.3, -0.6], [0.08, 0.10]):
    cam = C.CamPath((cx, 9.4, cz), (0.0, -5.0, 2.0), G0, GL, push=push, slide_px=slide, rise_px=rise, arc_deg_s=arc, decay=0.05,
                    snaps=[dict(g=SN, k=k, peak=1.6, shift=(0.0, sy))])
    pen = 0; sp = 0; n = 0
    for g in range(G0, 840, 3):
        loc, look = cam.at(g)
        vis = 0
        for nme, P in HEAD.items():
            x, y, s, z = proj(P, loc, look)
            if z > 0.5 and 50 < x < 670 and y < 800: vis += 1
        pen += max(0, 3 - vis) * 0.5
        x, y, s, z = proj(HAR, loc, look)
        if not (60 < x < 660 and 400 < y < 760): pen += 1
        a = proj(HAR, loc, look); b = proj(HAR, *cam.at(g + 3))
        sp += math.hypot(a[0]-b[0], a[1]-b[1]) / 3 + sum(math.hypot(proj(P, loc, look)[0]-proj(P, *cam.at(g+3))[0], proj(P, loc, look)[1]-proj(P, *cam.at(g+3))[1]) for P in HEAD.values()) / 3 / 4; n += 1
    sp /= n
    l2, k2 = cam.at(858); x, y, s, z = proj(HAR, l2, k2)
    pen += abs(x - 360) / 40 + abs(y - 620) / 40 + max(0, 240 - s) / 30
    if l2.y < -0.5: pen += 3
    res.append((round(pen - sp, 2), round(sp, 2), cx, cz, slide, arc, rise, push, sy, round(x), round(y), round(s)))
res.sort()
for r in res[:6]: print(r)
print("---")
cam = C.CamPath((0.0, 9.4, 3.6), (0.0, -5.0, 2.0), G0, GL, push=0.10, slide_px=0, rise_px=0, arc_deg_s=8, decay=0.05, snaps=[dict(g=SN, k=3.0, peak=1.6, shift=(0.0, 0))])
for g in (764, 800, 830, 843, 850, 858, 871):
    loc, look = cam.at(g)
    print(g, [round(v, 2) for v in loc], {n: tuple(round(v) for v in proj(P, loc, look)[:3]) for n, P in list(HEAD.items()) + [("har", HAR)]})
