#!/usr/bin/env python3
"""layout.py -- ONE staging for the hero crossing rows 46, 47-49, 50, 51 (director, 28 Nov 16:25): the trench runs LEFT-RIGHT across the
frame as a dark band with low sandbag lips across the lower third; the camera is low (about 1 D) on the near (east) side looking west, slightly
up; the tank crosses at YAW toward the camera, so the 3/4 view shows the rhomboid side, the track loop and the nose lifting over the band to grab the near lip.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F
YAW = float(os.environ.get("T2_YAW", -38.0))        # heading of the tank (deg): +x is west->east; negative = toward the camera's side (south-east)
X0, Y0 = 0.0, 4.5
S_A, S_B = -5.0, 27.0
TRENCH = [(0.0, -45.0), (0.0, 20.0), (7.0, 27.0), (31.0, 27.0)]
HEAD = (math.cos(math.radians(YAW)), math.sin(math.radians(YAW)))


def corridor(yaw=YAW):
    h = (math.cos(math.radians(yaw)), math.sin(math.radians(yaw)))
    return dict(o=(X0, Y0), h=h, s0=-40, s1=50, flat=4.8, blend=6.8, dz=0.0)


def preset(name, base="cross_hero", **over):
    w = dict(F.PRESETS["cross_hero"]["world"], wire_belts=[], wire_coils=[], crates=[], barrels=[], corridors=[corridor()])
    d = dict(cards=[], dress_n=0.25, near=False, tune=dict(green_k=1.2, cloud_k=0.95),
             trench0=dict(poly=TRENCH, mw=0.35, me=0.35, sb_layers=(2, 2)), world=w)
    d.update(over)
    return T.register(name, base, **d)


def regime(Tk):
    """re-solve the crossing along the new heading (the set built it for yaw 0)"""
    Tk.TK.setup_crossing(Tk.H, (X0, Y0), YAW, S_A, S_B)


def front_xy(Tk, u):
    p = Tk.TK.crossing_pose(Tk.H, u)
    return p["pos"][0], p["pos"][1], p


def add_lip(x=14.0, y0=-3.0, y1=13.0, layers=2):
    """a low sandbag wall across the near (east) foreground: the near trench lip in the lower third, plus a few iron wire stakes"""
    mb = F.MB()
    F.sandbag_row(mb, Vector((x, y0, F.gh(x, y0))), Vector((x, y1, F.gh(x, y1))), F.gh, layers, seed=31)
    F.mkobj(mb, "near_lip", smooth=True)
    sb = F.MB()
    for (sx, sy) in ((x + 0.3, y0 + 1.5), (x + 0.2, y1 - 1.5)):
        F.rod(sb, Vector((sx, sy, F.gh(sx, sy))), Vector((sx + 0.05, sy, F.gh(sx, sy) + 1.6)), 0.05, F.S["M"]["steel"], 6)
    F.mkobj(sb, "near_stakes")


def cam(g, c0=(20.0, 5.0, 1.2), c1=(17.5, 4.0, 1.4), lens=24.0, lead=2.0, lookz=2.4, g0=1424, g1=1493, Tk=None, easing=None):
    """low camera on the east side, looking at the tank's front point (led back by `lead` D along the heading); position eased c0 -> c1 over g0..g1"""
    k = min(max((g - g0) / float(g1 - 1 - g0), 0.0), 1.0)
    e = T.smooth(0.2 * k + 0.8 * k * k * (3 - 2 * k)) if easing is None else easing(k)
    loc = tuple(T.lerp(a, b, e) for a, b in zip(c0, c1))
    fx, fy, p = front_xy(Tk, T.umap(g))
    look = (fx - lead * HEAD[0], fy - lead * HEAD[1], lookz)
    return loc, look, lens
