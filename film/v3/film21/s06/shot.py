#!/usr/bin/env python3
"""shot.py -- film 21 take s06 (the count): shots 15-17, g 885..1044 + 7 handle frames before (878..884) and 6 after (1045..1050).
  15  g 878..937   bridge_end_north  ten English footmen step off the bridge onto the causeway, glance up at the hill. push 8 %/s + slide, snap
  16  g 938..985   hill_eye          the Scots still silent, one scratches his nose; snap pull-out (15 f, x0.7) on the cut + drift
  17  g 986..1050  valley_loop       the loop meadow fills with troops; stepped pull-out (14 f) at the start, then drift pull-out
One location per process:  python3 shot.py <15|16|17> <draft|final> a:b[:step] [samples]   -> raw/s<id>/g_%04d.png"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
from c21 import K, cast21, bf, ez, lerp
import numpy as np, bpy
from mathutils import Vector

RANGES = {15: (878, 937), 16: (938, 985), 17: (986, 1050)}
PRESET = {15: "bridge_end_north", 16: "hill_eye", 17: "valley_loop"}
STORY = cast21.STORY21


def blink(g, off):
    return 1 if ((g + off) % 83) < 3 else 0


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else [a[0]]
    return out


# ============================================================================ shot 15
_XS = [(-1.9, 0.0, 1.2), (-2.0, 0.6, 1.5), (-2.6, -0.8, 1.0), (-2.2, 0.2, 1.3)]
_CAST = [("footman_a", 0), ("footman_b", 1), ("footman_a", 2), ("footman_b", 3), ("footman_a", 1), ("footman_b", 2), ("footman_a", 3), ("footman_b", 0), ("footman_a", 0), ("footman_b", 1)]
FOOT = []
for _i in range(10):
    _r, _c = divmod(_i, 3)
    _ex = 0.66 * (_XS[_r][_c if _c < 3 else 2] + (0.35 if _i % 2 else -0.3))
    _ey = 40.8 - 1.45 * _r + (0.3 if _c == 1 else 0.0)
    FOOT.append((_CAST[_i][0], _CAST[_i][1], (0.7 if _i % 2 else -0.7, _ey - 6.5), (_ex, _ey), 4 * _r + _c))
G_GLANCE = 915


def foot_state(i, g):
    cast, var, p0, p1, dl = FOOT[i]
    u = (g - 878 - dl) / 40.0
    ux = ez(max(0.0, min(1.0, u)))
    return p0, p1, max(0.0, min(1.0, u))


def z_at(x, y):
    zg = float(K.ground(x, y))
    if y < 39.5:                                   # deck (z 1.75) down the end ramp onto the causeway
        zg = lerp(K.DECK_Z, zg, ez((y - 37.0) / 2.5))
    return zg


def pose15(i, g):
    cast, var, p0, p1, dl = FOOT[i]
    u = max(0.0, min(1.0, (g - 878 - dl) / 40.0))
    x = lerp(p0[0], p1[0], u); y = lerp(p0[1], p1[1], u)
    # the walk eases to a stop; on arrival: nervous tiptoe glance up at the hill (screen-left, up)
    glance = ez((g - (878 + dl + 40) - 3) / 8.0) if u >= 1.0 else 0.0
    face = 1 if p1[0] > p0[0] else -1
    if u < 1.0:
        ph = (g + 3 * i) / 20.0
        p = cast21.walk_spear(cast, ph, face, "march")
    else:
        p = dict(STORY[cast + "_stand"][1]); p["head_dy"] = 0.012 * math.sin(g * 0.4 + i)
    if u >= 1.0 and glance > 0:
        t = dict(STORY[cast + "_tiptoe"][1]); p.update(yaw=lerp(p.get("yaw", 0.3), -0.7, glance), expr="worried", gaze=(-0.9, -0.5), pitch=-0.3 * glance)
        p["arm_l"] = t["arm_l"]; p["legs"] = t["legs"]
    p["variant21"] = var
    p["blink"] = blink(g, i * 17)
    p["t"] = g / 30.0
    return p, (x, y), u


# ============================================================================ shot 16
SC16 = [("s1", "scot_a", 0, "fold_spear"), ("s2", "scot_b", 0, "fold_spear"), ("w", "wallace", 0, "calm"),
        ("s3", "scot_c", 0, "scratch_nose"), ("s4", "scot_a", 1, "fold_spear")]


def pose16(k, g):
    nm, cast, var, base = SC16[k]
    p = dict(STORY["%s_%s" % (cast, base)][1])
    if cast.startswith("scot") and var:
        p["variant21"] = var
    p["lean"] = p.get("lean", 0) + 2.6 * math.sin(g * 0.14 + k) 
    p["head_roll"] = p.get("head_roll", 0) + 3.5 * math.sin(g * 0.19 + 2 * k)
    p["head_dy"] = 0.01 * math.sin(g * 0.2 + k)
    p["blink"] = blink(g, k * 23)
    p["t"] = g / 30.0
    if nm == "s3":                                   # the nose-scratcher: hand to the nose with a little rub
        p["arm_l"] = dict(p["arm_l"]); h = p["arm_l"]["hand"]; p["arm_l"]["hand"] = (h[0] + 0.03 * math.sin(g * 0.9), h[1] + 0.02 * math.cos(g * 0.9))
    return p


def run(shot, quality, gs, samples):
    pr_name = PRESET[shot]
    work = os.path.join(HERE, "work", "s%d_%s" % (shot, quality))
    T = C.Take(pr_name, work, quality, fg=True)
    A, pr = T.A, T.pr
    lens = pr.get("lens", 22.0)
    out = os.path.join(HERE, "raw_" + quality, "s%d" % shot); os.makedirs(out, exist_ok=True)
    hook = None
    if shot == 15:
        T.hide("fg_generic_steel", "fg_generic_wood")
        K.place_troops(A, "causeway", 0); K.place_troops(A, "bridge", 6, seed=2)
        rig = C.Rig((-0.9, 52.4, 4.7), (0.3, 22.0, 0.2), 14.0, 885, push=0.10, slide_px=12, snaps=[(900, 13, 1.25), (G_GLANCE, 13, 1.3)])
        acts = []
        for i, f_ in enumerate(FOOT):
            a = T.make_actor("f%d" % i, f_[0]); acts.append((a, f_[0]))
    elif shot == 16:
        T.hide("fg_generic_steel", "fg_generic_wood", "fg_generic_r_heather")
        B = K.Batch(96); x, y = K.at_px(pr, 2.6, 690); K.spear(B, (x, y, float(K.ground(x, y))), tilt=(-0.25, 0.1), h=3.4); B.finalize('fg_team')
        rig = C.Rig(pr["cam"], pr["look"], 5.0, 938, push=-0.12, slide_px=60, snaps=[(938, 15, 1.0 / 0.7), (962, 13, 0.78)])
        acts = []
        for k, (nm, cast, var, base) in enumerate(SC16):
            acts.append((T.make_actor(nm, cast), cast))
    else:
        for o in list(bpy.data.objects):
            if o.name.startswith("crowd_") or o.name.startswith("crowd"):
                bpy.data.objects.remove(o, do_unlink=True)
        rig = C.Rig(pr["cam"], pr["look"], 250.0, 986, push=-0.16, slide_px=-100, snaps=[(986, 14, 1.0 / 0.76), (1016, 12, 1.12)], lens=lens)
        acts = []

        def hook(g):
            n = int(lerp(30, 266, ez((g - 986) / 70.0)))
            def cb(items):
                its = [(x * 2.2, 46.0 + (y - 46.0) * 1.8, float(K.ground(x * 2.2, 46.0 + (y - 46.0) * 1.8)), k, 2.6) for (x, y, z, k, s) in items]
                for o in K.stage_crowd(its, cam=T.cam): o.name = "troops_meadow_" + o.name
            K.place_troops(A, "meadow", n, seed=3, cb=cb)
            nc = int(lerp(10, 30, ez((g - 986) / 70.0)))
            K.place_troops(A, "causeway", nc, seed=5, cb=lambda items: [setattr(o, "name", "troops_causeway_" + o.name) for o in K.stage_crowd([(x, y, z, k, 2.1) for (x, y, z, k, s) in items], cam=T.cam)])
    # ---- cameras + placements + poses
    for g in gs:
        loc, look = rig.at(g)
        T.key_cam(g, loc, look, lens)
    marks = A["marks"]
    cam0 = Vector(rig.at(gs[0])[0])
    if shot == 15:
        for i, (a, cast) in enumerate(acts):
            for g in gs:
                p, (x, y), u = pose15(i, g)
                T.place(a, g, (x, y, z_at(x, y)), cast, flip=False)
        for i, (a, cast) in enumerate(acts):
            for g in gs:
                p, (x, y), u = pose15(i, g); T.pose(a, g, p)
            d = (Vector(FOOT[i][3] + (1.5,)) - cam0).length
            T.sprites_for([(a, T.ppd_for(cast, d - 2.0), gs)])
    elif shot == 16:
        for k, (a, cast) in enumerate(acts):
            m = marks[SC16[k][0]]
            for g in gs:
                T.place(a, g, (m[0], m[1], m[2]), cast)
        for k, (a, cast) in enumerate(acts):
            m = marks[SC16[k][0]]
            for g in gs:
                T.pose(a, g, pose16(k, g))
            d = (Vector(m[:3]) - cam0).length
            T.sprites_for([(a, T.ppd_for(cast, d * 0.8), gs)])
    # ---- render
    def full_hook(g):
        K.set_flow(g / 30.0); K.set_flutter(g / 30.0); K.set_smoke(g / 30.0)
        if hook: hook(g)
    rep = {}
    for g in gs:
        path = os.path.join(out, "g_%04d.png" % g)
        t0 = time.time()
        dt = T.render(g, path, samples, hook=full_hook)
        rep[g] = T.heads(g) if acts else {}
        print("shot %d g %d  %.1f s  heads %s" % (shot, g, time.time() - t0, rep[g]), flush=True)
        json.dump(rep[g], open(path[:-4] + ".json", "w"))


if __name__ == "__main__":
    shot = int(sys.argv[1]); quality = sys.argv[2]; spec = sys.argv[3]
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else (8 if quality == "draft" else 24)
    lo, hi = RANGES[shot]
    gs = [g for g in parse(spec) if lo <= g <= hi]
    run(shot, quality, gs, samples)
