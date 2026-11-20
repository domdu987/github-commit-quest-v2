#!/usr/bin/env python3
"""shot.py -- film 21 take s01 (the HOOK): shots 1-3, g 0..159 (+6 handle frames g160..165).  transition_in none, internal cuts g44, g89.
  shot 1 g0..43   hill_over   over the shoulders of the Scots, far bridge with the English column.  push + lateral slide.
  shot 2 g44..88  bridge_deck two English knights side by side on the deck (mounted cards, walking), rail post fg.
  shot 3 g89..165 hill_eye    the Scots line, arms folded on spears, Wallace calm, a grass-chewer; snap push on him at "ไม่ทำอะไรเลยสักอย่าง".
One location per process:   python3 shot.py probe|stills|final <1|2|3> <a:b[:step]> [out_dir] [samples]
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
RANGES = {1: (0, 43), 2: (44, 88), 3: (89, 165)}
G_SNAP = C.g_of(4.08) - 4            # snap push on "ไม่ทำอะไรเลยสักอย่าง" (4.08 s): starts just before the word
SNAP_N = 15
ANG = float(os.environ.get('ANG', '10.5'))


def bf(g): return g + 1


def dirs(pr):
    c, l = np.array(pr["cam"], float), np.array(pr["look"], float)
    f = l - c; fh = np.array([f[0], f[1], 0.0]); fh /= np.linalg.norm(fh)
    r = np.array([fh[1], -fh[0], 0.0])
    return c, l, fh, r


def cam_path(shot, g):
    """(loc, look, lens) of shot `shot` at film frame g."""
    pr = K.PRESETS[{1: "hill_over", 2: "bridge_deck", 3: "hill_eye"}[shot]]
    c, l, fh, r = dirs(pr)
    g0, g1 = RANGES[shot]; x = (g - g0) / float(g1 - g0 + 1); t = (g - g0) / 30.0
    u = 0.35 * sine(x) + 0.65 * x
    lens = pr["lens"]
    if shot == 1:        # push 9 %/s (lens + 0.5 m dolly) + slide left (camera trucks right)
        push = 0.30 * (g1 - g0 + 1) / 30.0 * u * 1.0
        c2 = c + fh * 0.30 * u + r * 0.15 * u; l2 = l + r * 0.15 * u
        return c2, l2, lens * (1 + 0.09 * (g - g0) / 30.0)
    if shot == 2:        # push 8 %/s with the knights' walk, camera trucks along the rail (+y), post passes the lens
        tk = np.array([0.10, 1.85, 0.0]) * x - dirs(pr)[3] * 0.32; c2 = c + tk + fh * 0.35 * u + np.array([0.0, 0.0, 0.0]); l2 = l + tk
        return c2, l2, lens * (1 + 0.08 * (g - g0) / 30.0)
    # shot 3: truck 0.28 m/s (~40 px/s at 5.5 m) + snap x1.4 on the grass-chewer
    tr = 0.28 * t
    l = l - np.array([0, 0, 1.4]); c2 = c + r * tr; l2 = l + r * tr
    s = clamp((g - G_SNAP) / float(SNAP_N)); e = 1 - (1 - s) ** 3 * (1 if s < 1 else 1)
    e = sine(s) * 0.5 + 0.5 * (1 - (1 - s) ** 2)
    zoom = lerp(1.0, 1.4, e)
    # pan the look toward the chewer (mark s2 is at x 265 px) as we zoom
    ang = math.radians(ANG) * e                        # rotate right-to-left: bring s2 to centre
    d = l2 - c2; ca, sa = math.cos(ang), math.sin(ang)
    d2 = np.array([d[0] * ca - d[1] * sa, d[0] * sa + d[1] * ca, d[2]])      # + angle = counter-clockwise = pan left (s2 is on the left)
    return c2, c2 + d2, lens * zoom * (1 + 0.04 * (g - g0) / 30.0)


# --------------------------------------------------------------------------- cast
def sway(p, g, k, amp=2.0, hz=0.35, roll=1.5):
    p = dict(p); p["lean"] = p.get("lean", 0) + amp * math.sin(2 * math.pi * hz * g / 30.0 + k)
    p["head_roll"] = p.get("head_roll", 0) + roll * math.sin(2 * math.pi * 0.27 * g / 30.0 + 1.7 * k)
    return p


def scot_pose(name, g, k, yaw=None, base=None):
    var = int(name.split("_v")[1]) if "_v" in name else 0; name = name.split("_v")[0]
    p = dict(ST[base or (name + "_fold_spear")][1])
    if var: p["variant21"] = var
    if yaw is not None: p["yaw"] = yaw
    p = sway(p, g, k)
    p["blink"] = blink(g, [17 * (k + 1) % 61 + 20, 17 * (k + 1) % 61 + 80])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot, work=WORK):
        self.shot = shot
        pn = {1: "hill_over", 2: "bridge_deck", 3: "hill_eye"}[shot]
        hide, extra = (), None
        if shot == 2:
            hide = ("fg_generic",)
            def extra(A): pass
            _unused = True
            def extra(A):
                pr = K.PRESETS["bridge_deck"]; B = K.Batch(96); x, y = K.at_px(pr, 1.9, 40)
                B.box("wood", (x, y, K.DECK_Z + 0.58), (0.11, 0.11, 1.12)); B.box("wood_dk", (x, y, K.DECK_Z + 1.18), (0.15, 0.15, 0.08)); B.finalize("fg_team")
        if shot == 3:
            hide = ("fg_generic_steel", "fg_generic_wood", "fg_generic_r_")
            def extra(A):
                pr = K.PRESETS["hill_eye"]; B = K.Batch(96); x, y = K.at_px(pr, 2.6, 690)
                K.spear(B, (x, y, K.ground(x, y)), tilt=(-0.45, 0.15), h=3.4); B.finalize("fg_team")
        C.Take.__init__(self, pn, work, hide=hide, extra=extra)
        self.cfg = self.setup_cast()

    def setup_cast(self):
        M = self.A["marks"]; sh = self.shot; cast = {}
        if sh == 1:
            for nm, who, k in (("s1", "scot_b", 0), ("s2", "wallace", 1), ("s3", "scot_c", 2), ("s4", "scot_a", 3), ("s5", "scot_a_v1", 4)):
                a = self.actor("c_" + nm, who.split("_v")[0], ppd=256); cast[nm] = (a, who, k, M[nm])
        elif sh == 2:
            for nm, who in (("k1", "knight_a_mtd"), ("k2", "knight_b_mtd")):
                self.actor("c_" + nm, who, ppd=192)
        else:
            for nm, who, k in (("s1", "scot_a", 0), ("s2", "scot_b", 1), ("w", "wallace", 2), ("s3", "scot_c", 3), ("s4", "scot_a", 4)):
                a = self.actor("c_" + nm, who, ppd=192); cast[nm] = (a, who, k, M[nm])
        return cast

    def pose_frame(self, g):
        f = bf(g); sh = self.shot; M = self.A["marks"]; used = []
        loc, look, lens = cam_path(sh, g)
        self.key_cam(f, loc, look, lens)
        if sh == 2:
            for nm, who, flip in (("k1", "knight_a_mtd", True), ("k2", "knight_b_mtd", True)):
                x, y, z, _, _ = M[nm]; t = (g - 44) / 30.0
                y += 1.3 * t * (1.0 if nm == "k1" else 1.05)               # they walk north along the deck (~1.3 m/s)
                self.place("c_" + nm, f, (x, y, z), flip=flip)
                p = dict(ST[{"k1": "knight_a_mounted", "k2": "knight_b_mounted"}[nm]][1]); p.update(gait=((g - 44 + (0 if nm == "k1" else 11)) / 40.0) % 1.0, yaw=-0.9, mirror=False)
                p["t"] = g / 70.0; p["blink"] = blink(g, [52, 79]) if nm == "k1" else blink(g, [60, 85]); p = sway(p, g, 0 if nm == "k1" else 2, amp=0.8, roll=1.0)
                self.pose("c_" + nm, f, p); used.append("c_" + nm)
        else:
            for nm, (a, who, k, m) in self.cfg.items():
                x, y, z = m[0], m[1], m[2]
                lat = LAT[sh].get(nm, 0.0); _, _, _, rr = dirs(K.PRESETS[{1: 'hill_over', 3: 'hill_eye'}[sh]]); x += rr[0] * lat; y += rr[1] * lat
                self.place(a.name, f, (x, y, z), scale=SC_FOR.get(who, C.SC))
                if sh == 1:
                    yaw = {"s1": 1.1, "s2": -1.0, "s3": -1.1, "s4": 1.0, "s5": 1.1}[nm]
                    base = {"s2": "wallace_fold_spear"}.get(nm)
                    p = scot_pose(who, g, k, yaw=yaw, base=base)
                else:
                    base = {"w": "wallace_calm", "s2": "scot_b_chew_grass"}.get(nm)
                    p = scot_pose(who, g, k, base=base)
                    if nm == "s1": p["yaw"] = 0.45
                    if nm == "s4": p["yaw"] = -0.4
                self.pose(a.name, f, p); used.append(a.name)
        return used


LAT = {1: {'s1': 0.55, 's4': 0.4, 's5': 0.7, 's2': -0.25, 's3': -0.15}, 3: {'s1': 0.3, 's3': -0.35, 's4': 0.35}}
SC_FOR = {"wallace": 0.54}


def main():
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw", "s%d" % shot)
    samples = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    os.makedirs(out, exist_ok=True)
    mode = "draft" if cmd in ("probe", "stills") else "final"
    T = Take(shot); K.setup_render(T.scene, "final" if cmd == "probe" else mode, 8)
    used = {g: T.pose_frame(g) for g in gs}
    T.sprites_for({n: [bf(g) for g in gs if n in used[g]] for n in T.actors})
    for g in gs:
        f = bf(g)
        K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        if cmd == "probe":
            print(g, T.heads(f), flush=True); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path) and os.path.exists(path[:-4] + ".json"): continue
        dt = T.render(f, path, samples=samples, mode=mode, used=used[g])
        json.dump(dict(g=g, wall=round(dt, 1), heads=T.heads(f), samples=samples), open(path[:-4] + ".json", "w"))
        print("shot %d g %d %.1f s heads %s" % (shot, g, dt, T.heads(f)), flush=True)


if __name__ == "__main__":
    main()
