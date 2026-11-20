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


def cress_pose(g):
    sp = G_SPEAK[0] <= g <= G_SPEAK[1]
    if g < G_STOP:
        base = dict(S["cressingham_pointing"][1])
        base["arm_r"] = dict(base["arm_r"], hand=(1.18, 0.18 + 0.03 * math.sin(g * 0.45)))
        p = cast21.cycle("cressingham", (g - 648) / 34.0, "walk", -1, base=base, arms="l", speed=0.85)
        p["legs"] = dict(p["legs"], spread=0.12)                      # the waddle: wide stance
        p["lean"] = p.get("lean", 0) + 3 * math.sin((g - 648) / 34.0 * 2 * math.pi)
        p["blink"] = blink(g, [655, 700, 735])
    elif g < G_PUSH + 2:
        p = dict(S["cressingham_pointing"][1]); p["mirror"] = True
        p["head_roll"] = 4 * math.sin(g * 0.3); p["blink"] = blink(g, [753])
    elif g < 781:
        p = dict(S["cressingham_purse_slap"][1]); p["mirror"] = True
        jolt = max(0.0, 1 - (g - 758) / 6.0) if g >= 758 else 0.0     # the slap on the purse (g 758)
        p["head_dy"] = 0.05 * jolt; p["lean"] = -5 - 4 * jolt
        p["arm_l"] = dict(p["arm_l"], hand=(0.4, 1.55 - 0.1 * jolt))
        p["arm_r"] = dict(p["arm_r"], hand=(1.12, -0.05 + 0.05 * math.sin(g * 0.6)))
        p["head_roll"] = 3 * math.sin(g * 0.35); p["blink"] = blink(g, [770])
    else:
        p = dict(S["cressingham_smug_belt"][1]); p["mirror"] = True; p["pitch"] = -0.7     # chin up, thumbs in the belt
        p["head_roll"] = -4 + 2 * math.sin(g * 0.3); p["lean"] = 1.5 * math.sin(g * 0.2); p["blink"] = blink(g, [790])
    p = cast21.speak(p, g) if sp else dict(p, mouth="smirk")
    p["t"] = g / 30.0
    return K.with_rim(p)


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
def camera_at(g, M):
    loc0, look0, f, r = axes()
    R = r
    if g > G1:                                                   # handle: keep pulling out along the last motion
        a_loc, a_look = camera_at(G1, M); b_loc, b_look = camera_at(G1 - 1, M)
        return a_loc + (a_loc - b_loc) * (g - G1), a_look + (a_look - b_look) * (g - G1)
    cx = cress_xy(g, M, R)
    gz = float(K.ground(cx.x, cx.y))
    fwd = pw(g, [(642, -0.7), (700, 0.2), (748, 0.45), (G_PUSH, 0.6), (G_PUSH + 9, 2.35), (G_CU, 2.2), (G_OUT, 0.0)])
    up = pw(g, [(642, 0.25), (700, 0.3), (748, 0.0), (G_PUSH + 9, -0.2), (G_CU, -0.1), (G_OUT, 0.0)])
    rt = pw(g, [(642, 0.8), (700, 0.3), (748, -0.3), (G_PUSH + 9, 0.0), (G_OUT, 0.0)])
    xd = pw(g, [(642, 330), (700, 270), (748, 230), (G_PUSH + 9, 400), (G_OUT, 395)])
    yd = pw(g, [(642, 610), (700, 600), (748, 590), (G_PUSH + 9, 560), (G_CU, 570), (G_OUT, 585)])
    loc = Vector((loc0.x + (cx.x - M[0]), loc0.y + (cx.y - M[1]), loc0.z)) + f * fwd + R * rt + Vector((0, 0, up))
    hd = Vector((cx.x, cx.y, gz + 1.55))
    d = max(0.8, (Vector((hd.x, hd.y, 0)) - Vector((loc.x, loc.y, 0))).length)
    foc = 1280.0 * P_LENS / 36.0
    look = hd + R * ((360.0 - xd) * d / foc) + Vector((0, 0, (yd - 640.0) * d / foc))
    s = pw(g, [(G_CU, 0.0), (G_OUT, 1.0)]) if g >= G_CU else 0.0
    if g >= G_CU:
        x = (g - G_CU) / float(G_OUT - G_CU); s = 0.5 * sm(x) + 0.5 * x
    dt_, d0_ = (look - loc).normalized(), (look0 - loc0).normalized()         # blend the VIEW DIRECTION (look points are far away)
    loc = loc.lerp(loc0, s); dv = dt_.lerp(d0_, s).normalized(); look = loc + dv * 12.0
    if s >= 1.0: look = Vector(look0)
    if g <= 647:                                                 # whip in: fast pan settling (6 frames)
        a = math.radians([34.0, 16.0, 7.0, 3.0, 1.2, 0.4][g - 642])
        v = look - loc; c, sn = math.cos(a), math.sin(a)
        look = loc + Vector((v.x * c - v.y * sn, v.x * sn + v.y * c, v.z))
    return loc, look


# ------------------------------------------------------------------ staging
def stage(T, gs):
    A = T.A
    marks = A["marks"]["camp_bank"]
    M = marks["cress"]
    loc0, look0, f, R = axes()
    cre = T.add("cre", "cressingham"); sur = T.add("sur", "surrey")
    sf = K.mark_px(P_LOC, P_LOOK, P_LENS, 5.8, 570, "surrey")            # Surrey at cx ~570 at P_BANK (QA: the banner pole is at x >= 640)
    jobs = [(cre, cress_pose), (sur, surrey_pose)]
    ext = []
    for k, (key, cast, story) in enumerate((("e1", "footman_b", "footman_b_stand"), ("e2", "knight_b", "knight_b_stand_arms_down"))):
        a = T.add("x" + key, cast); jobs.append((a, extra_pose(story, 1.3 * k))); ext.append((a, marks[key], cast))
    for g in gs:
        loc, look = camera_at(g, M)
        T.key_cam(g, loc, look, P_LENS)
        c = cress_xy(g, M, R)
        T.place(cre, g, (c.x, c.y, float(K.ground(c.x, c.y))), SC["cressingham"])
        us = walk_u(g, lag=4)
        sx, sy = sf[0] + R.x * WALK_DS * (1 - us), sf[1] + R.y * WALK_DS * (1 - us)
        T.place(sur, g, (sx, sy, float(K.ground(sx, sy))), SC["surrey"])
        for a, m, cast in ext:
            T.place(a, g, (m[0], m[1], m[2]), SC[cast])
    cu = [g for g in gs if G_PUSH + 2 <= g <= G_CU + 6]
    rest = [g for g in gs if g not in cu]
    if rest: T.poses(jobs, rest, ppd=256)
    if cu: T.poses(jobs[:1], cu, ppd=448); T.poses(jobs[1:], cu, ppd=256)

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
            if w * 1.15 > 0.35 * 1280: msg.append("face too big")
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
