#!/usr/bin/env python3
"""shot.py -- film 25 rows 53+54: "กระสุน เด้งออกจากเหล็ก" g 1592-1635 (1636 exclusive), 53.08-54.55 s.
Medium on the hull side of the tank across the trench (set_crossing u 0.86, level, tracks stopped): a German MG nest in the
background puffs (muzzle flash bursts, smoke puffs); bullet pings spark off the riveted plates in the foreground (tank25.set_sparks,
bursts repeating every 16 frames from g 1605 to 1636), no holes.  PUSH 10 % + slight ARC.  Mild DOF (medium shot).
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
C, F = T.C, T.F
bpy = C.bpy
G0, G1 = 1592, 1636
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_ping"
U = 0.86
Y_T = 4.5
MG = (30.5, 11.0, -math.pi / 2 - 0.35)


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.10 * T.smooth(k)
    ang = math.radians(T.lerp(-12.0, 4.0, T.smooth(k)))                   # slight arc
    d = 27.0 / push
    cx = T.lerp(21.5, 22.5, k)
    loc = (cx + d * math.sin(ang), Y_T - d * math.cos(ang), 2.4)
    look = (cx, Y_T, 2.3)
    return loc, look, 26.0, (3.0, d)


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, U)
    t = ((g - 1605) % 16) / 30.0 if g >= 1605 else -1.0
    Tk.TK.set_sparks(Tk.H, t)
    fl = bpy.data.objects.get("mg_flash")
    if fl is not None:                                                         # muzzle flash: bursts of 2 frames on, 3 off
        fl.hide_render = not ((g % 5) < 2)


def report(Tk, g):
    c = cam_of(g)
    return dict(u=U, cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_hull", cards=[], cam=dict(loc=(26.0, -12.0, 2.4), look_at=(23.0, 4.5, 2.6), lens=26.0), dress_n=0.8, near=False,
               sun=None, fill=None, sparks=None, extras=[("mg", MG[0], MG[1], MG[2], True)], tune=dict(green_k=1.2, cloud_k=0.95),
               world=dict(F.PRESETS["cross_hull"].get("world", {}), crates=[], barrels=[], rocks=[], wire_coils=[]))
    for k in ("sun", "fill", "sparks"):
        F.PRESETS[PRESET].pop(k, None)
    Tk = T.Take(PRESET, cam_of, hooks)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
