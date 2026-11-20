#!/usr/bin/env python3
"""shot.py -- film 21 segment D2 (the MOCKER), g 642..793 + 3 handle frames (794..796); plan v3 (QA_TEAM §I).
ONE travelling camera in the world built by K.build_world(['camp_bank']):
  g 642-647  WHIP IN (6 frames of fast pan settling into the shot), then the camera FOLLOWS Cressingham (side tracking) as he waddles
             about 4.5 m along the bank toward the screen-left, pointing across the river at the Scots on the hill; Surrey trails behind, tired.
  g 756-778  CU1 on "เร็วดี ประหยัดดี!" (25.11-26.26): fast push into his face as he slaps the purse.
  g 778-793  the camera eases back out to EXACTLY P_BANK (K.POSES['P_BANK']); 794-796 handle continues the pull-out (D6 join to team 7's E1).
Lip-sync (cast21.speak) ONLY g 642..791 (narration 21.29-26.26).
    python3 shot.py draft [step] | final a:b[:step]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                            # noqa: E402
from c21 import K, cast21, Vector, lerp, blink             # noqa: E402

S = cast21.STORY21
G0, G1, GH = 642, 793, 796
G_SPEAK = (642, 791)
G_STOP, G_PUSH, G_CU, G_OUT = 750, 756, 778, 793
WALK_D = 4.5
WALK_DS = 2.4
P_LOC, P_LOOK, P_LENS = K.preset_pose("P_BANK")
SC = C.SCALE


def sm(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def pw(g, pts):
    """piecewise smooth interpolation of [(g, value)]"""
    if g <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if g <= b:
            x = (g - a) / float(b - a); u = 0.5 * sm(x) + 0.5 * x
            return lerp(va, vb, u)
    return pts[-1][1]


def axes():
    loc, look = Vector(P_LOC), Vector(P_LOOK)
    f = Vector((look.x - loc.x, look.y - loc.y, 0)).normalized()
    return loc, look, f, Vector((f.y, -f.x, 0))


# ------------------------------------------------------------------ cast motion
def walk_u(g, lag=0):
    x = (g - lag - 648) / float(G_STOP - 648)
    return 0.4 * sm(x) + 0.6 * max(0.0, min(1.0, x)) if x < 1 else 1.0   # eased but never dead-still while walking


def cress_xy(g, M, R):
    u = walk_u(g)
    return Vector((M[0], M[1], 0)) + R * (WALK_D * (1 - u))


PT_L = dict(hand=(-1.05, 0.05), shape="point", bend=-0.5, stretch=1.3, layer="front")        # unmirrored: pointing up-left (about 35 deg) at the Scots
PURSE_HAND = (0.55, 1.80)                                                                      # on the purse (stretch 1.5 reaches it)
G_SLAP = 758


def slap_hand(g):
    """right hand: ready beside the belt -> up -> DOWN onto the purse at g 758 -> bounce -> pressed on the purse to g 780."""
    pts = [(750, (0.62, 0.95), 1.0), (754, (0.75, 0.85), 1.1), (756, (0.80, 0.70), 1.2), (G_SLAP, PURSE_HAND, 1.5), (760, (0.60, 1.50), 1.3), (762, PURSE_HAND, 1.5), (781, PURSE_HAND, 1.5)]
    for (a, ha, sa), (b, hb, sb) in zip(pts, pts[1:]):
        if g <= b:
            x = max(0.0, (g - a) / float(b - a)); u = x if b - a <= 2 else x * x * (3 - 2 * x)
            return (lerp(ha[0], hb[0], u), lerp(ha[1], hb[1], u)), lerp(sa, sb, u)
    return PURSE_HAND, 1.5


def cress_pose(g):
    sp = G_SPEAK[0] <= g <= G_SPEAK[1]
    if g < G_STOP:
        base = dict(S["cressingham_pointing"][1])
        base["arm_r"] = dict(base["arm_r"], hand=(1.05, -0.20 + 0.03 * math.sin(g * 0.45)))   # raised ~30 deg more: the finger line runs to the Scots
        p = cast21.cycle("cressingham", (g - 648) / 34.0, "walk", -1, base=base, arms="l", speed=0.85)
        p["legs"] = dict(p["legs"], spread=0.12)                      # the waddle: wide stance
        p["lean"] = p.get("lean", 0) + 3 * math.sin((g - 648) / 34.0 * 2 * math.pi)
        p["blink"] = blink(g, [655, 700, 735])
    elif g < 781:
        p = dict(S["cressingham_purse_slap"][1])                       # UNMIRRORED: arm_l points up-left at the hill, arm_r slaps the purse (screen-right hip)
        p["arm_l"] = dict(PT_L, hand=(-1.05, 0.05 + 0.03 * math.sin(g * 0.5)))
        h, st = slap_hand(g)
        p["arm_r"] = dict(hand=h, bend=0.1, stretch=st, shape="open", layer="front")
        jolt = max(0.0, 1 - (g - G_SLAP) / 4.0) if g >= G_SLAP else 0.0
        p["head_dy"] = 0.05 * jolt; p["lean"] = -5 - 5 * jolt
        p["head_roll"] = 3 * math.sin(g * 0.35); p["blink"] = blink(g, [751, 772])     # the facing swap at g 750 sits behind the blink
    else:
        p = dict(S["cressingham_smug_belt"][1]); p["pitch"] = -0.7     # chin up, thumbs in the belt
        p["head_roll"] = -4 + 2 * math.sin(g * 0.3); p["lean"] = 1.5 * math.sin(g * 0.2); p["blink"] = blink(g, [790])
    p = cast21.speak(p, g) if sp else dict(p, mouth="smirk")
    p["t"] = g / 30.0
    return K.with_rim(p)


def glint_svg(g):
    """gold coin glint + two coins hopping off the purse for 2-5 frames after the slap (puppet-local D)."""
    k = g - G_SLAP
    if not (0 <= k <= 6): return ""
    r = 0.10 + 0.05 * min(k, 3)
    cx, cy = 0.62, 1.62
    star = '<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="#fff6c0" stroke="#e0a010" stroke-width="0.012"/>' % (
        cx, cy - 2 * r, cx + 0.3 * r, cy - 0.3 * r, cx + 2 * r, cy, cx + 0.3 * r, cy + 0.3 * r, cx, cy + 2 * r, cx - 0.3 * r, cy + 0.3 * r, cx - 2 * r, cy, cx - 0.3 * r, cy - 0.3 * r)
    coins = "".join('<circle cx="%.3f" cy="%.3f" r="0.045" fill="#f2c030" stroke="#8a5a10" stroke-width="0.012"/>' % (cx + dx * (0.05 + 0.05 * k), cy - 0.10 * k - 0.05 + dy) for dx, dy in ((-1, 0.0), (1, -0.05)))
    return star + coins


def surrey_pose(g):
    u = walk_u(g, lag=4)
    base = dict(S["surrey_tired"][1])
    if u < 1:
        p = cast21.cycle("surrey", (g - 648) / 40.0, "walk", -1, base=base, arms="none", speed=0.6)
        p["head_roll"] = p.get("head_roll", 0) + 4; p["lean"] = p.get("lean", 0) + 4
    else:
        p = dict(base); p["mirror"] = True; p["lean"] = 3 + 1.2 * math.sin(g * 0.1); p["head_roll"] = 5 + 2 * math.sin(g * 0.08)
    p["blink"] = blink(g, [680, 745]); p["t"] = g / 30.0
    return K.with_rim(p)


def extra_pose(name, ph):
    def f(g):
        p = dict(S[name][1]); p.update(lean=1.2 * math.sin(g * 0.11 + ph), head_roll=1.8 * math.sin(g * 0.083 + ph * 1.7))
        p["blink"] = blink(g, [int(650 + 37 * (ph + 1)) % 796, int(720 + 29 * (ph + 1)) % 796]); p["t"] = g / 30.0
        if int(g / 40 + ph) % 3 == 0:                                     # a shift of weight / look: nobody is frozen
            p["yaw"] = -0.3
        return K.with_rim(p)
    return f


# ------------------------------------------------------------------ camera
def herm(g, g0, g1, p0, p1, m0, m1):
    """cubic Hermite, slopes m in units per frame"""
    t = (g - g0) / float(g1 - g0); d = g1 - g0
    return ((2 * t**3 - 3 * t**2 + 1) * p0 + (t**3 - 2 * t**2 + t) * d * m0 + (-2 * t**3 + 3 * t**2) * p1 + (t**3 - t**2) * d * m1)


PULL = 0.06                      # m per frame the pull-out is still moving at P_BANK (the handle g 794-796 continues it)


def camera_at(g, M):
    loc0, look0, f, R = axes()
    if g > G1:                                                   # handle: the pull-out continues at the same speed (and the camera slides a little)
        k = g - G1
        return loc0 - f * (PULL * k) + R * (0.01 * k), Vector(look0)
    cx = cress_xy(g, M, R)
    gz = float(K.ground(cx.x, cx.y))
    if g < G_CU:
        fwd = pw(g, [(642, -0.7), (700, 0.2), (748, 0.45), (G_PUSH, 0.6), (G_PUSH + 9, 2.60), (G_CU, 2.50)])
        up = pw(g, [(642, 0.25), (700, 0.3), (748, 0.0), (G_PUSH + 9, -0.3), (G_CU, -0.2)])
        rt = pw(g, [(642, 0.8), (700, 0.3), (748, -0.3), (G_PUSH + 9, 0.0), (G_CU, 0.0)])
    else:                                                        # pull out, arriving at P_BANK at speed PULL
        fwd = herm(g, G_CU, G_OUT, 2.50, 0.0, -0.02, -PULL)
        up = herm(g, G_CU, G_OUT, -0.2, 0.0, 0.0, 0.0)
        rt = 0.0
    xd = pw(g, [(642, 330), (700, 240), (725, 190), (748, 200), (G_PUSH + 9, 330), (G_OUT, 330)])        # head x: the bridge enters on the right by g ~725
    yd = pw(g, [(642, 665), (700, 665), (748, 650), (G_PUSH + 9, 395), (G_CU, 395), (G_OUT, 585)])      # tilt up 4-6 deg: sand < 30 %; CU: head centre y 452 so the belt + purse stay in shot
    loc = Vector((loc0.x + (cx.x - M[0]), loc0.y + (cx.y - M[1]), loc0.z)) + f * fwd + R * rt + Vector((0, 0, up))
    hd = Vector((cx.x, cx.y, gz + 1.55))
    d = max(0.8, (Vector((hd.x, hd.y, 0)) - Vector((loc.x, loc.y, 0))).length)
    foc = 1280.0 * P_LENS / 36.0
    look = hd + R * ((360.0 - xd) * d / foc) + Vector((0, 0, (yd - 640.0) * d / foc))
    s = 0.0
    if g >= G_CU:
        s = herm(g, G_CU, G_OUT, 0.0, 1.0, 0.0, 0.0)
    dt_, d0_ = (look - loc).normalized(), (look0 - loc0).normalized()         # blend the VIEW DIRECTION (look points are far away)
    dv = dt_.lerp(d0_, s).normalized(); look = loc + dv * 12.0
    if g == G1: loc, look = Vector(loc0), Vector(look0)                        # exactly P_BANK
    if g <= 647:                                                 # whip in: fast pan settling (6 frames)
        a = math.radians([34.0, 16.0, 7.0, 3.0, 1.2, 0.4][g - 642])
        v = look - loc; c, sn = math.cos(a), math.sin(a)
        look = loc + Vector((v.x * c - v.y * sn, v.x * sn + v.y * c, v.z))
    return loc, look


def surrey_xy(g, M, R, sf, loc_of):
    """Surrey trails Cressingham (tired), steps in BEHIND him for CU1 (hidden by his head, so nothing is cut by a frame edge), then steps out to his P_BANK mark."""
    us = walk_u(g, lag=4)
    track = Vector((sf[0] + R.x * WALK_DS * (1 - us), sf[1] + R.y * WALK_DS * (1 - us), 0))
    c = cress_xy(g, M, R)
    loc = loc_of(g)
    ax = Vector((c.x - loc.x, c.y - loc.y, 0)).normalized()
    behind = Vector((c.x, c.y, 0)) + ax * 1.0
    if g < 738: return track
    if g < 756: w = herm(g, 738, 756, 0.0, 1.0, 0.0, 0.0); return track.lerp(behind, w)
    if g < 781: return behind
    w = herm(g, 781, G_OUT, 0.0, 1.0, 0.0, 0.0)
    return behind.lerp(Vector((sf[0], sf[1], 0)), w)


def near_props(A, M, R, f, loc0):
    """near-ground dressing along the follow track (QA-art: no bare sand) + a grey strongbox instead of the red barrel, placed to wipe through fast."""
    import numpy as np
    rs = np.random.RandomState(31)
    def at(u, lat, dep):                                          # u along the walk, lat = along R, dep = along f from the line of the track
        c = Vector((M[0], M[1], 0)) + R * (WALK_D * (1 - u))
        p = c + R * lat + f * dep
        return (p.x, p.y, float(K.ground(p.x, p.y)))
    B = K.Batch(91)
    K.sacks(B, at(0.10, 1.6, -1.5), 5, rs); K.sacks(B, at(0.62, 2.2, -1.2), 4, rs)
    K.weapon_rack(B, at(0.30, 2.0, -0.4), 20.0, rs, n=6)
    K.spear(B, at(0.82, 1.9, -1.3), tilt=(0.06, -0.1), h=3.0); K.spear(B, at(0.84, 2.2, -1.1), tilt=(-0.05, -0.12), h=3.0)
    for k in range(7):                                            # tent pegs and rope stubs in the sand
        x, y, z = at(0.05 + 0.13 * k, rs.uniform(-1.8, 2.8), rs.uniform(-1.8, -0.4))
        B.rod("wood", (x, y, z), (x + 0.05, y, z + 0.28), 0.03, seg=5)
    # a grey-blue strongbox with iron bands and a gold lock (not red), 1.2 m toward the camera of the old barrel's line
    x, y, z = at(0.37, 1.25, -2.0)
    B.box("iron", (x, y, z + 0.28), (0.95, 0.55, 0.56)); B.box("wood", (x, y, z + 0.30), (0.88, 0.5, 0.52))
    for dx in (-0.3, 0.3): B.box("iron", (x + dx, y, z + 0.30), (0.07, 0.56, 0.56))
    B.box("gold", (x, y - 0.28, z + 0.38), (0.12, 0.03, 0.14))
    B.finalize("d2_props", shadow=True)


# ------------------------------------------------------------------ staging
def stage(T, gs):
    import bpy
    A = T.A
    for o in bpy.data.objects:
        if o.name in ("flag_gold.021", "flag_wood.021", "flag_t_gold.014", "flag_t_red.015", "fg_bank_barrel"):
            o.hide_render = True                                 # fg banner pole (crossed his head) and the red barrel (covered him)
    marks = A["marks"]["camp_bank"]
    M = marks["cress"]
    loc0, look0, f, R = axes()
    near_props(A, M, R, f, loc0)
    # the far Scots: 2.7x bigger, and their saltire flags, so a phone viewer finds them
    for o in bpy.data.objects:
        if o.name.startswith("scots_line_") and "." not in o.name: o.hide_render = True
        if o.name.startswith("flag_t_saltire") or o.name in ("flag_wood.022", "flag_wood.023", "flag_wood.024", "flag_wood.025", "flag_gold.022", "flag_gold.023", "flag_gold.024", "flag_gold.025"):
            o.scale = (2.5, 2.5, 2.5)
    import numpy as np
    K.scots_slope_line(22, 1, 3.9, np.random.RandomState(8), spear_h=6.5, a0=200, a1=250, hh0=7.0)
    cre = T.add("cre", "cressingham"); sur = T.add("sur", "surrey")
    sf = K.mark_px(P_LOC, P_LOOK, P_LENS, 5.8, 570, "surrey")            # Surrey at cx ~570 at P_BANK (QA: the banner pole is at x >= 640)
    jobs = [(cre, cress_pose), (sur, surrey_pose)]
    ext = []
    for k, (key, cast, story) in enumerate((("e1", "footman_b", "footman_b_stand"),)):
        a = T.add("x" + key, cast); jobs.append((a, extra_pose(story, 1.3 * k))); ext.append((a, marks[key], cast))
    loc_of = lambda gg: camera_at(gg, M)[0]
    for g in gs:
        loc, look = camera_at(g, M)
        T.key_cam(g, loc, look, P_LENS)
        c = cress_xy(g, M, R)
        T.place(cre, g, (c.x, c.y, float(K.ground(c.x, c.y))), SC["cressingham"])
        sp = surrey_xy(g, M, R, sf, loc_of)
        T.place(sur, g, (sp.x, sp.y, float(K.ground(sp.x, sp.y))), SC["surrey"])
        for a, m, cast in ext:
            T.place(a, g, (m[0], m[1], m[2]), SC[cast])
    cu = [g for g in gs if G_PUSH + 2 <= g <= G_CU + 6]
    rest = [g for g in gs if g not in cu]
    if rest: T.poses(jobs, rest, ppd=256)
    if cu:
        T.poses(jobs[1:], cu, ppd=256)
        for g in cu:                                              # the CU frames: bigger sprites, plus the coin glint on the slap frames
            T.poses_overlay(cre, cress_pose, g, 448, glint_svg(g))

    def on_frame(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
    return on_frame


def check(T, gs):
    bad = 0
    for g in gs:
        h = T.heads(g)
        for k, v in h.items():
            x, y, w = v["x"], v["y"], v["w"]
            msg = []
            if x - w * 0.5 < -2 < x + w * 0.5 or x - w * 0.5 < 722 < x + w * 0.5: msg.append("CUT by side edge")
            if k in ("cre", "sur") and not (450 <= y <= 760): msg.append("centre y outside 450-760")
            if y + w * 0.55 > 880 and 0 < x < 720: msg.append("head bottom > 880")
            if w > 0.35 * 1280: msg.append("face too big")
            if os.environ.get("VERBOSE"): print(g, k, round(x), round(y), round(w))
            if msg: bad += 1; print("g %d %s x %.0f y %.0f w %.0f: %s" % (g, k, x, y, w, "; ".join(msg)))
    print("check done, %d issues over %d frames" % (bad, len(gs)))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "draft":
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 3; gs = list(range(G0, GH + 1, step)); out = os.path.join(HERE, "raw_d")
        q = "draft"
    elif mode == "check":
        gs = list(range(G0, GH + 1, int(sys.argv[2]) if len(sys.argv) > 2 else 2)); q = "final"; out = None
    else:
        gs = C.parse(sys.argv[2]); out = os.path.join(HERE, "raw"); q = "final"
    if os.environ.get("DRAFT"): q = "draft"; out = os.path.join(HERE, "raw_t")
    samples = int(os.environ.get("SAMPLES", "6" if q == "draft" else "32"))
    T = C.Take21("camp_bank", os.path.join(HERE, "work"), quality=q, samples=samples, world=["camp_bank"])
    if mode == "final":
        gs = [g for g in gs if G0 <= g <= GH and not os.path.exists(os.path.join(out, "f_%04d.png" % g))]
    on_frame = stage(T, gs)
    if mode == "check":
        check(T, gs); sys.exit(0)
    for g in gs:
        st = T.render([g], out, on_frame)[0]
        print("g %d %.1f s wall heads %s" % (g, st["wall"], json.dumps(T.heads(g))), flush=True)
