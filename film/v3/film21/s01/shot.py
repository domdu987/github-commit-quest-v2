#!/usr/bin/env python3
"""shot.py -- film 21 take s01 (the HOOK, QA §H BIGZOOM): shots 1-2, g 0..159 (+6 handle frames g160..165).  transition_in none, internal cut g125.
  shot 1 g0..124   BIGZOOM: one eased camera move from EXTREME WIDE high over the Forth valley (like valley_wide: loop, bridge with the English column,
                   camp, Abbey Craig, the Scots tiny on the slope) swooping down over the crag to a MEDIUM of the Scots line on the shelf (PAD2), seen from
                   the uphill side: Wallace centre, arms folded, the bridge far below behind them.  Hybrid preset 'bigzoom' (valley scene + hill detail).
  shot 2 g125..165 hill_eye: the Scots line, a grass-chewer; snap push (15 f, x1.4) on him on "อะไรเลยสักอย่าง".
One location per process:   python3 shot.py probe|stills|final <1|2> <a:b[:step]> [out_dir] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C
import numpy as np
from mathutils import Vector
import stirling as K
import cast21
lerp, clamp, sine, blink = C.lerp, C.clamp, C.sine, C.blink
ST = cast21.STORY21
WORK = os.path.join(HERE, "work")
RANGES = {1: (0, 124), 2: (125, 165)}
G_SNAP = 127                         # shot 2: snap push on the grass-chewer, "อะไรเลยสักอย่าง" (4.08 s = g 125)
SNAP_N = 15
ANG = float(os.environ.get("ANG", "10.5"))
SC = C.SC
V_START, V_END = (1.11, 1.63), (0.8, 1.31)        # valley_wide / hill_eye VIVID entries (gamma, sat)


def bf(g): return g + 1


# ---------------------------------------------------------------------------- the Scots' stand points (identical in both shots)
HE = K.PRESETS["hill_eye"]
MARK_SPEC = {"s1": (5.2, 150), "s2": (6.0, 265), "w": (5.6, 370), "s3": (6.4, 500), "s4": (5.4, 590)}
WHO = {"s1": ("scot_a", 0), "s2": ("scot_b", 1), "w": ("wallace", 2), "s3": ("scot_c", 3), "s4": ("scot_a", 4)}
LAT = {"s1": 0.3, "s3": -0.35, "s4": 0.35}          # lateral shifts (m, along the screen-right of hill_eye) used for the shot-2 framing
HE_DIR = np.array(HE["look"][:2], float) - np.array(HE["cam"][:2], float); HE_DIR /= np.linalg.norm(HE_DIR)
HE_R = np.array([HE_DIR[1], -HE_DIR[0]])


def mark_xy(nm, shot=2):
    d, xp = MARK_SPEC[nm]; x, y = K.at_px(HE, d, xp); x += HE_R[0] * LAT.get(nm, 0.0); y += HE_R[1] * LAT.get(nm, 0.0)
    if shot == 1 and nm in ("s1", "s4"):             # medium shot from the uphill side shows Wallace, s2, s3: the outer two stand just out of frame
        wx, wy = K.at_px(HE, *MARK_SPEC["w"]); lat = (x - wx) * HE_R[0] + (y - wy) * HE_R[1]; push = (1.0 if lat > 0 else -1.0) * 0.9
        x += HE_R[0] * push; y += HE_R[1] * push
    return x, y, float(K.ground(x, y))


# ---------------------------------------------------------------------------- BIGZOOM path (shot 1)
S_CAM = np.array([445.0, 244.0, 361.0]); S_LOOK = np.array([64.0, 44.0, 0.0])
Wx, Wy, Wz = mark_xy("w")
V3 = np.array([HE_DIR[0], HE_DIR[1], 0.0])            # unit vector toward the hill (NE)
E_CAM = np.array([Wx, Wy, 0.0]) + V3 * 3.6; E_CAM[2] = float(K.ground(E_CAM[0], E_CAM[1])) + 1.55
E_DIR = -V3 * math.cos(math.radians(5)) + np.array([0, 0, -math.sin(math.radians(5))])
M_CAM = np.array([250.0, 168.0, 160.0])
S_DIR = (S_LOOK - S_CAM) / np.linalg.norm(S_LOOK - S_CAM)


def _speed(x):
    if x < 0.2: return 0.25 + 0.75 * sine(x / 0.2)
    if x < 0.5: return 1.0
    return 0.10 + 0.90 * (1 - sine((x - 0.5) / 0.5))


_XS = np.linspace(0, 1, 2001); _CUM = np.cumsum([_speed(x) for x in _XS]); _CUM = (_CUM - _CUM[0]) / (_CUM[-1] - _CUM[0])


def zoom_path(g):
    x = clamp(g / float(RANGES[1][1] + 1 - 0.0))
    u = float(np.interp(x, _XS, _CUM))                 # arc-length-ish progress: gentle start, fast swoop, long ease-out
    p = (1 - u) ** 2 * S_CAM + 2 * u * (1 - u) * M_CAM + u * u * E_CAM
    if u > 0.85:
        tt = (1 - u) / 0.15; f = tt * tt * (3 - 2 * tt); p[2] = E_CAM[2] + (p[2] - E_CAM[2]) * f * 0.6 + (p[2] - E_CAM[2]) * 0.4 * tt * tt * tt
    w = clamp((u - 0.05) / 0.78); w = w * w * (3 - 2 * w)
    d = (1 - w) * S_DIR + w * E_DIR; d /= np.linalg.norm(d)
    right = np.array([d[1], -d[0], 0.0]); right /= np.linalg.norm(right)
    p = p + right * (6.0 * math.sin(math.pi * u) * (1 - u) + 0.45 * (1 - clamp((x - 0.65) / 0.35)))      # swoop curve, then a slow truck that ends centred on Wallace
    lens = lerp(22.0, 26.0, clamp((u - 0.55) / 0.45))
    return p, p + d * 100.0, lens, u


def vivid_of(g, shot):
    if shot == 2: return K.VIVID["hill_eye"]
    u = zoom_path(g)[3]; w = sine(clamp((u - 0.45) / 0.55))
    return (lerp(V_START[0], V_END[0], w), lerp(V_START[1], V_END[1], w))


def cam_path(shot, g):
    if shot == 1:
        p, l, lens, _ = zoom_path(g); return p, l, lens
    pr = HE
    c = np.array(pr["cam"], float); l = np.array(pr["look"], float)
    c[2] = float(K.ground(c[0], c[1])) + 1.75
    r = np.array([HE_DIR[1], -HE_DIR[0], 0.0])
    t = (g - RANGES[2][0]) / 30.0
    tr = 0.28 * t + 0.35
    l = l - np.array([0, 0, 1.4]); c2 = c + r * tr; l2 = l + r * tr
    s = clamp((g - G_SNAP) / float(SNAP_N))
    e = sine(s) * 0.5 + 0.5 * (1 - (1 - s) ** 2)
    zoom = lerp(1.0, 1.4, e)
    ang = math.radians(ANG) * e
    d = l2 - c2; ca, sa = math.cos(ang), math.sin(ang)
    d2 = np.array([d[0] * ca - d[1] * sa, d[0] * sa + d[1] * ca, d[2]])
    push = 1 + 0.06 * max(0.0, (g - G_SNAP - SNAP_N)) / 30.0            # slow push after the snap, so the hold keeps moving
    return c2, c2 + d2, 22.0 * zoom * push


# ---------------------------------------------------------------------------- cast
def sway(p, g, k, amp=2.0, hz=0.35, roll=1.5):
    p = dict(p); p["lean"] = p.get("lean", 0) + amp * math.sin(2 * math.pi * hz * g / 30.0 + k)
    p["head_roll"] = p.get("head_roll", 0) + roll * math.sin(2 * math.pi * 0.27 * g / 30.0 + 1.7 * k)
    return p


def scot_pose(nm, g, shot):
    cast, k = WHO[nm]
    base = {"w": "wallace_calm", "s2": "scot_b_chew_grass"}.get(nm, cast + "_fold_spear")
    p = dict(ST[base][1])
    if nm == "s4": p["variant21"] = 1
    if shot == 1:                                   # seen from the uphill side: face the bridge side a little, nearly still
        p["yaw"] = {"s1": -0.35, "s2": -0.2, "w": 0.0, "s3": 0.3, "s4": 0.35}[nm]
        p = sway(p, g, k, amp=0.8, roll=0.6)
    else:
        if nm == "s1": p["yaw"] = 0.45
        if nm == "s4": p["yaw"] = -0.4
        p = sway(p, g, k)
    p["blink"] = blink(g, [17 * (k + 1) % 61 + 20, 17 * (k + 1) % 61 + 80, 17 * (k + 1) % 61 + 140])
    p["t"] = g / 30.0
    return p


def add_bigzoom_preset():
    pr = dict(K.PRESETS["valley_wide"])
    pr.pop("scots_line", None)
    veg = dict(HE["veg"]); veg["seed"] = 11
    pr.update(cam=tuple(E_CAM), look=tuple(E_CAM + E_DIR * 60.0), lens=22.0, sd=12.0, veg=veg, dress_min=6.0, hill2=True,
              heather_n=900, gorse_n=420, crag_n=140, pine_n=90, troops=dict(bridge=14, meadow=60, causeway=10))
    K.PRESETS["bigzoom"] = pr


class Take(C.Take):
    def __init__(self, shot, work=WORK):
        self.shot = shot; hide, extra = (), None
        if shot == 1:
            add_bigzoom_preset(); pn = "bigzoom"
            def extra(A):
                rs = np.random.RandomState(3)
                K.scots_slope_line(14, 3, 1.0, rs, spear_h=4.0, a0=188.0, a1=214.0); K.scots_slope_line(14, 3, 1.0, rs, spear_h=4.0, a0=236.0, a1=258.0)
        else:
            pn = "hill_eye"; hide = ("fg_generic_steel", "fg_generic_wood", "fg_generic_r_")
            def extra(A):
                B = K.Batch(96); x, y = K.at_px(HE, 2.6, 690)
                K.spear(B, (x, y, K.ground(x, y)), tilt=(-0.45, 0.15), h=3.4); B.finalize("fg_team")
        C.Take.__init__(self, pn, work, hide=hide, extra=extra)
        for nm, (cast, k) in WHO.items(): self.actor("c_" + nm, cast, ppd=192)

    def pose_frame(self, g):
        f = bf(g); sh = self.shot
        loc, look, lens = cam_path(sh, g)
        self.key_cam(f, loc, look, lens)
        for nm in WHO:
            x, y, z = mark_xy(nm, sh)
            self.place("c_" + nm, f, (x, y, z), scale=0.54)
            self.pose("c_" + nm, f, scot_pose(nm, g, sh))
        return ["c_" + nm for nm in WHO]

    def per_frame_set(self, g):
        K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        K.STATE["vivid"] = vivid_of(g, self.shot)
        if self.shot == 1:
            for o in bpy_objects("troops_bridge"): o.location.y = 1.3 * g / 30.0


def bpy_objects(prefix):
    import bpy
    return [o for o in bpy.data.objects if o.name.startswith(prefix)]


def main():
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw", "s%d" % shot)
    samples = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    os.makedirs(out, exist_ok=True)
    mode = "draft" if cmd in ("probe", "stills") else "final"
    T = Take(shot); K.setup_render(T.scene, "final" if cmd == "probe" else mode, 8)
    used = {g: T.pose_frame(g) for g in gs}
    T.sprites_for({n: [bf(g) for g in gs] for n in T.actors}, vivid=lambda f: vivid_of(f - 1, shot)[0])
    for g in gs:
        f = bf(g)
        T.per_frame_set(g)
        if cmd == "probe":
            p, l, lens = cam_path(shot, g); print(g, np.round(p, 1), round(lens, 1), T.heads(f), flush=True); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path) and os.path.exists(path[:-4] + ".json"): continue
        dt = T.render(f, path, samples=samples, mode=mode, used=used[g])
        json.dump(dict(g=g, wall=round(dt, 1), heads=T.heads(f), samples=samples), open(path[:-4] + ".json", "w"))
        print("shot %d g %d %.1f s heads %s" % (shot, g, dt, T.heads(f)), flush=True)


if __name__ == "__main__":
    main()
