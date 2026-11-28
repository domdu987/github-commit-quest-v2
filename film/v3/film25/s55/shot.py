#!/usr/bin/env python3
"""shot.py -- film 25 row 55: "ทหารเยอรมัน" g 1636-1658 (1659 exclusive), 54.55-55.29 s.  PUPPET close (Look A pipeline, s47/pup.py).
german_b25 waist-up, plain grey-olive plate 2 D behind him (crisp cast shadow), mild DOF; his round glasses slide down his nose (glasses_dy25 0 -> 1) and his
jaw drops; a blink; PUNCH 15 % on the jaw drop (g 1642-1649).  Mouth holds (he is not the general).
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
import pup
from mathutils import Vector
C, F = T.C, T.F
cast25 = C.cast25
G0, G1 = 1636, 1659
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_german"
POS = (0.0, 6.0); FACE = 90.0
CAM_D, CAM_Z, LOOK_Z, LENS = 3.9, 2.9, 2.75, 42.0
GZ = [0.0]


def pose_of(g):
    import json as _j
    c, p = cast25.STORY25["german_b25_glasses_slip"]
    p = _j.loads(_j.dumps(p))
    w = T.smooth((g - 1640) / 8.0)
    p["glasses_dy25"] = round(w, 3)                                         # glasses slide down the nose
    k = g - 1641
    p["squash"] = [1.0, 1.0] if not (0 <= k < 6) else {0: [1.07, 0.94], 1: [1.08, 0.92], 2: [1.03, 0.98], 3: [0.98, 1.04], 4: [1.0, 1.01], 5: [1.0, 1.0]}[k]
    p["yaw"] = round(0.15 * math.sin((g - G0) / 9.0), 3)
    p["blink"] = 1 if g in (1655, 1657) else 0
    p["light25"] = -1; p["rim25"] = 0.6
    return p


def feet_of(g):
    return (POS[0], POS[1], GZ[0])


def cam_of(g):
    pk = C.out_cubic((g - 1642) / 8.0) if g >= 1642 else 0.0                    # PUNCH 15 % on the jaw drop
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    d = CAM_D / (1.0 + 0.15 * pk) / (1.0 + 0.03 * T.smooth(k))
    a = math.radians(FACE)
    loc = (POS[0] + math.cos(a) * d + 0.25 * (k - 0.5), POS[1] + math.sin(a) * d, GZ[0] + CAM_Z)
    look = (POS[0], POS[1], GZ[0] + LOOK_Z)
    return loc, look, LENS, (2.4, d)


def report(Tk, g):
    return {}


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "front_close_germantrench", cards=[], cast=[], extras=[], dress_n=0.1, near=False, clamp=False, tune=dict(green_k=1.0, cloud_k=0.95))
    Tk = pup.PupTake(PRESET, cam_of)
    GZ[0] = F.gh(*POS)
    pup.backdrop(POS, FACE, dist=2.0, gz=GZ[0])
    sd = os.path.join(HERE, "work", "sprites"); os.makedirs(sd, exist_ok=True)
    Tk.add("gen", "german_b25", pose_of, feet_of, sd)
    Tk.pose(gs)
    out = os.path.join(HERE, "work", "draft") if cmd == "draft" else os.path.join(HERE, "frames")
    os.makedirs(out, exist_ok=True)
    scale, samples = (0.5, 8) if cmd == "draft" else (T.SCALE, T.SAMPLES)
    for g in gs:
        js = os.path.join(out, "g_%04d.json" % g)
        if cmd == "final" and os.path.exists(js):
            continue
        rep = Tk.render_frame(g, out, scale=scale, samples=samples)
        json.dump(rep, open(js, "w"), default=float)
        print("g %d %.1f s" % (g, rep["wall"]), flush=True)
        st = pup.post_frame(g, out, rep, [sd], ["gen"])
        a = __import__("numpy").asarray(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(out, "post", "g_%04d.png" % g)).convert("RGB")).reshape(-1, 3)
        print("   face px #fef7f6:", int(((a == [254, 247, 246]).all(1)).sum()), flush=True)
