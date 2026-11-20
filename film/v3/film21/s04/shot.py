#!/usr/bin/env python3
"""shot.py -- film 21 take s04 (the MOCKER): shots 10-12, g 542..793 (+7 handle frames before, +6 after).
  table  g 535..641  shot 10 (camp_table, D11 in at 542): Cressingham counts coins into the chest, looks up across the river, bursts out
                     laughing on "หัวเราะลั่นว่า" (20.29 -> g 612, laugh pose + 3 Hz bounce, no lip-sync).  Push + slide, a reframe, a snap at the laugh.
  bank   g 642..799  shots 11 (642..706) + 12 (707..793, + handle 794..799) (camp_bank): lip-sync 21.29-26.26 (g 642..791) only.
    11: low two-shot, Cressingham points across the river, Surrey listens.  12: snap push-in on the purse slap + arm flung at the bridge, chin up.
    python3 shot.py table|bank draft|final a:b[:step] [out_dir]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                           # noqa: E402
from c21 import K, cast21, Vector, lerp, blink            # noqa: E402

S = cast21.STORY21
G_ENTER, G_CUT11, G_CUT12, G_END = 542, 642, 707, 793
RANGES = {"table": (G_ENTER - 7, G_CUT11 - 1), "bank": (G_CUT11, G_END + 6)}
G_LAUGH = C.g_of(20.29)          # 612
G_SPEAK = (C.g_of(21.29) - 0, C.g_of(26.26))       # 642..791 (+-0.15 s window)
HIDE = {"table": 596, "bank": 0}


def sway(g, ph=0.0, a=1.0):
    return dict(lean=a * 1.2 * math.sin(g * 0.11 + ph), head_roll=a * 1.6 * math.sin(g * 0.083 + ph * 1.7))


# ------------------------------------------------------------------ table (shot 10)
TABLE_M = (-13.0, -26.0)


def table_cam(g):
    wps = [(535, (-13.50, -30.60, 2.10), (-13.30, -26.5, 1.52)),
           (581, (-13.10, -30.00, 2.05), (-13.15, -26.5, 1.50)),
           (596, (-12.80, -29.70, 1.95), (-12.95, -26.45, 1.48)),     # reframe: look up across the river
           (611, (-12.98, -29.55, 1.92), (-13.0, -26.4, 1.52)),
           (626, (-13.05, -28.85, 1.85), (-13.0, -26.3, 1.74)),       # snap push on the laugh (x1.3)
           (641, (-12.85, -28.55, 1.82), (-12.95, -26.3, 1.78))]
    return C.path(g, wps, mix=0.45)


def cress_table(g):
    if g < 590:
        p = dict(S["cressingham_counting"][1])
        d = 0.5 + 0.5 * math.sin(g * 0.42)                       # the coin dips into the chest and comes up
        p["arm_r"] = dict(p["arm_r"], hand=(0.78 - 0.1 * d, 1.0 + 0.16 * d))
        p["gaze"] = (0.3 + 0.1 * math.sin(g * 0.2), 0.9)
        p.update(sway(g))
        p["blink"] = blink(g, [556, 584])
    elif g < G_LAUGH:                                            # looks up across the river
        u = min(1.0, (g - 590) / 8.0)
        p = dict(S["cressingham_counting"][1])
        p.update(pitch=lerp(0.55, -0.45, u), gaze=(lerp(0.3, 0.6, u), lerp(0.9, -0.2, u)), yaw=lerp(0.45, 0.3, u), lean=lerp(7, 0, u),
                 head_roll=3 * u * math.sin(g * 0.2))
        p["arm_r"] = dict(p["arm_r"], hand=(0.78, lerp(1.0, 1.25, u)))
        p["blink"] = blink(g, [G_LAUGH - 2])
    else:
        p, _ = cast21.laugh(S["cressingham_laughing"][1], g)
        p["blink"] = blink(g, [G_LAUGH + 22])
    p["t"] = g / 30.0
    return p


def stage_table(T, gs):
    A = T.A
    cre = T.add("cre", "cressingham")
    z = float(K.ground(*TABLE_M))
    sc = C.SCALE["cressingham"]
    for g in gs:
        loc, look = table_cam(g)
        T.key_cam(g, loc, look)
        dy = cast21.laugh(S["cressingham_laughing"][1], g)[1] if g >= G_LAUGH else 0.0
        T.place(cre, g, (TABLE_M[0], TABLE_M[1], z + dy * sc), sc)
    T.poses([(cre, cress_table)], gs)

    def on_frame(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        K.set_chest_lid(A, 72)
        K.set_scale_tip(A, 7.0 * math.sin(g * 0.12) if g < G_LAUGH else 14.0 * math.sin(g * 0.9))   # the scale jiggles while he laughs
    return on_frame


# ------------------------------------------------------------------ bank (shots 11, 12)
BC = Vector(K.PRESETS["camp_bank"]["cam"]) if False else None


def bank_axes():
    pr = K.PRESETS["camp_bank"]
    cam = Vector(pr["cam"]); look = Vector(pr["look"])
    f = Vector((look.x - cam.x, look.y - cam.y, 0)).normalized()
    r = Vector((f.y, -f.x, 0))
    return cam, look, f, r


CRESS_M = None


def cress_head():
    m = CRESS_M or K.PRESETS["camp_bank"]["_cress"]
    return Vector((m[0], m[1], m[2] + 1.55))


def bank_cam(g):
    """camera = base preset position + (right, up, fwd); look = Cressingham's head + R * L + (0, 0, tilt): orbit-like slide, subjects stay framed."""
    cam, look, f, r = bank_axes()
    hd = cress_head()

    def w(gg, right, up, fwd, xd, yd=600.0):
        d = 3.6 - fwd                                   # distance to Cressingham along the view; xd, yd = where his head sits (px) -> look offsets
        L = (360.0 - xd) * d / 924.4
        tilt = (yd - 640.0) * d / 924.4
        return (gg, tuple(cam + r * right + f * fwd + Vector((0, 0, up))), tuple(hd + r * L + Vector((0, 0, tilt))))
    if g < G_CUT12:        # shot 11: slow push + slide (the camera orbits right), low
        wps = [w(642, -0.30, 0.0, -0.2, 395, 620), w(676, 0.0, 0.05, 0.40, 405, 610), w(706, 0.30, 0.0, 0.85, 415, 600)]
        return C.path(g, wps, mix=0.4)
    wps = [w(707, 0.10, 0.0, 0.35, 390, 610),
           w(727, 0.30, 0.1, 1.45, 400, 590),                        # snap push-in x1.5 on the slap
           w(760, 0.10, 0.15, 1.75, 410, 570),
           w(775, -0.05, 0.25, 1.85, 400, 560),                      # chin-up reframe
           w(799, 0.15, 0.30, 2.05, 415, 565)]
    return C.path(g, wps, mix=0.4)


def cress_bank(g):
    sp = G_SPEAK[0] <= g <= G_SPEAK[1]
    if g < G_CUT12:
        p = dict(S["cressingham_pointing"][1])
        u = min(1.0, (g - 642) / 7.0)
        p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.5, 1.18, u), lerp(0.8, 0.18, u) + 0.03 * math.sin(g * 0.5)))
        p.update(sway(g))
        p["head_roll"] = 6 + 2 * math.sin(g * 0.13)
        p["blink"] = blink(g, [655, 689])
    elif g < 745:
        p = dict(S["cressingham_purse_slap"][1])
        jolt = max(0.0, 1 - (g - 709) / 6.0) if g >= 709 else 0.0          # the slap on the purse
        p["head_dy"] = 0.05 * jolt
        p["lean"] = -5 - 4 * jolt
        p["arm_l"] = dict(p["arm_l"], hand=(0.4, 1.55 - 0.1 * jolt))
        p["arm_r"] = dict(p["arm_r"], hand=(1.12, -0.05 + 0.04 * math.sin(g * 0.5)))
        p["head_roll"] = 2 * math.sin(g * 0.12)
        p["blink"] = blink(g, [724, 740])
    elif g < 772:
        p = dict(S["cressingham_pointing"][1])
        p["arm_r"] = dict(p["arm_r"], hand=(1.18, 0.15 + 0.04 * math.sin(g * 0.5)))
        p["pitch"] = -0.6
        p.update(sway(g, 1.0))
        p["blink"] = blink(g, [756, 770])
    else:
        p = dict(S["cressingham_smug_belt"][1])                              # chin up, thumbs in the belt
        p["pitch"] = -0.8
        p.update(sway(g, 2.0, 0.8))
        p["blink"] = blink(g, [790])
    if sp:
        p = cast21.speak(p, g)
    else:
        p["mouth"] = "smirk"
    p["t"] = g / 30.0
    return p


def surrey_bank(g):
    p = dict(S["surrey_listening"][1])
    p.update(sway(g, 0.7, 0.7))
    p["blink"] = blink(g, [668, 735])
    p["t"] = g / 30.0
    return p


def extra_pose(name, ph):
    def f(g):
        p = dict(S[name][1]); p.update(sway(g, ph, 0.9)); p["blink"] = blink(g, [int(640 + 37 * (ph + 1)) % 800, int(700 + 29 * (ph + 1)) % 800]); p["t"] = g / 30.0
        return p
    return f


def rel_pos(lat, dep):
    cam, look, f, r = bank_axes()
    c = Vector(CRESS_M[:3]); p = c + r * lat + f * dep
    return (p.x, p.y, float(K.ground(p.x, p.y)))


# (name, cast, lat, dep) offsets from Cressingham, per shot; None = not in this shot
SURREY = {11: (-1.0, 1.3), 12: (-0.8, 1.4)}
REF = {11: 676, 12: 740}
# extras placed relative to the camera of a reference frame: (name, cast, story, x px, distance m)
EXTRAS = {11: [("e1", "footman_b", "footman_b_stand", 575, 8.0), ("e2", "knight_b", "knight_b_stand_arms_down", 560, 10.5),
               ("e3", "footman_a", "footman_a_stand", 130, 9.0), ("e4", "footman_b", "footman_b_stand_arms_down", 95, 8.0)],
          12: [("e1", "footman_b", "footman_b_stand", 560, 7.0), ("e2", "knight_b", "knight_b_stand_arms_down", 560, 10.0)]}


def cam_pos(sh, x_px, d):
    loc, look = bank_cam(REF[sh])
    fwd = Vector((look.x - loc.x, look.y - loc.y, 0)).normalized(); right = Vector((fwd.y, -fwd.x, 0))
    p = loc + fwd * d + right * ((x_px - 360.0) * d / 924.4)
    return (p.x, p.y, float(K.ground(p.x, p.y)))


def stage_bank(T, gs):
    A = T.A
    global CRESS_M
    CRESS_M = A["marks"]["cress"]
    K.PRESETS["camp_bank"]["_cress"] = CRESS_M
    cre = T.add("cre", "cressingham"); sur = T.add("sur", "surrey")
    jobs = [(cre, cress_bank), (sur, surrey_bank)]
    ext = {}
    if os.environ.get("EXTRAS", "1") == "1":
        for sh in (11, 12):
            for nm, cast, story, xp, dd in EXTRAS[sh]:
                if nm + cast not in ext:
                    a = T.add(nm + "_" + cast, cast); ext[nm + cast] = a; jobs.append((a, extra_pose(story, len(ext) * 1.1)))
    for g in gs:
        loc, look = bank_cam(g)
        T.key_cam(g, loc, look)
        sh = 11 if g < G_CUT12 else 12
        m = CRESS_M
        T.place(cre, g, (m[0], m[1], m[2]), C.SCALE["cressingham"])
        T.place(sur, g, rel_pos(*SURREY[11]) if sh == 11 else cam_pos(12, 150, 3.9), C.SCALE["surrey"])
        shown = {nm + cast for nm, cast, _, _, _ in EXTRAS[sh]}
        for sh2 in (11, 12):
            for nm, cast, story, xp, dd in EXTRAS[sh2]:
                a = ext[nm + cast]
                if sh2 == sh:
                    T.place(a, g, cam_pos(sh2, xp, dd), C.SCALE[cast])
                    T.hide(a, g, False)
                elif (nm + cast) not in shown:
                    T.place(a, g, cam_pos(sh2, xp, dd), C.SCALE[cast]); T.hide(a, g, True)
    T.poses(jobs, gs)

    def on_frame(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
    return on_frame


# ------------------------------------------------------------------ main
if __name__ == "__main__":
    which, mode, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw", which)
    lo, hi = RANGES[which]
    gs = [g for g in C.parse(spec) if lo <= g <= hi]
    preset = "camp_table" if which == "table" else "camp_bank"
    samples = int(os.environ.get("SAMPLES", "6" if mode == "draft" else "24"))
    T = C.Take21(preset, os.path.join(HERE, "work"), quality="draft" if mode == "draft" else "final", samples=samples)
    if mode == "check":
        gs = [g for g in gs if g % int(os.environ.get("STEP", "3")) == 0 or g in (G_CUT11, G_CUT12, hi)]
        (stage_table if which == "table" else stage_bank)(T, gs)
        bad = 0
        for g in gs:
            h = T.heads(g)
            for k, v in h.items():
                x, y, w = v["x"], v["y"], v["w"]
                msg = []
                if x - w * 0.5 < -2 < x + w * 0.5 or x - w * 0.5 < 722 < x + w * 0.5:
                    msg.append("CUT by side edge")
                if k in ("cre", "sur") and not (450 <= y <= 760):
                    msg.append("centre y %.0f outside 450-760" % y)
                if y + w * 0.55 > 880 and 0 < x < 720:
                    msg.append("head bottom %.0f > 880" % (y + w * 0.55))
                if w > 0.35 * 1280:
                    msg.append("face too big")
                if os.environ.get("VERBOSE"):
                    print(g, k, round(x), round(y), round(w))
                if msg:
                    bad += 1; print("g %d %s x %.0f y %.0f w %.0f: %s" % (g, k, x, y, w, "; ".join(msg)))
        print("check done, %d issues over %d frames" % (bad, len(gs)))
        sys.exit(0)
    # frames already done are skipped in final mode
    if mode == "final":
        gs = [g for g in gs if not os.path.exists(os.path.join(out, "f_%04d.png" % g))]
    on_frame = (stage_table if which == "table" else stage_bank)(T, gs)
    for g in gs[:1]:
        print(json.dumps(dict(g=g, heads=T.heads(g))), flush=True)
    for g in gs:
        st = T.render([g], out, on_frame)[0]
        print("g %d %.1f s wall  heads %s" % (g, st["wall"], json.dumps(T.heads(g))), flush=True)
