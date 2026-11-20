#!/usr/bin/env python3
"""shot.py -- film 21 segment E2 (the count), g 885..1044, CUT in, no handles.  ONE continuous camera travel (plan v3):
   g 885  ride-along beside the first English footmen stepping off the bridge onto the north causeway (camera on the east side, they walk
          screen-right), they glance up at the hill nervously ("บนเนินเงียบ"),
   g 936  ("ร้อยคน" 31.17) the camera rises as more pour over the bridge mouth (still silent),
   g 986  ("เป็นพัน" 32.75) the camera CRANES UP to ~40 m over the meadow, angled back toward the hill: hundreds of troops fill the meadow,
          the Scots (blue saltire banners) on Abbey Craig have not moved.
World: K.build_world(['bridge_end_north', 'valley_loop']).   python3 shot.py <draft|final> a:b[:step] [samples] [outdir]"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
from c21 import K, cast21, ez, lerp
import numpy as np, bpy
from mathutils import Vector

G0, G1 = 885, 1044
STORY = cast21.STORY21
# camera travel keys: (g, loc, look, lens)
KEYS = [(885, (0.7, 42.0, 3.1), (0.0, 34.5, 1.5), 22.0),
        (936, (0.9, 47.5, 7.0), (0.0, 38.5, 1.0), 22.0),
        (986, (1.0, 52.0, 17.0), (0.0, 43.0, 0.6), 22.0),
        (1044, (-20.0, 44.0, 44.0), (88.0, 118.0, 8.0), 22.0)]
N_WALK = 40
SUN_K = float(os.environ.get('SUN_K', 1.3))
GAMMA0 = float(os.environ.get('GAMMA0', 1.55))
SPEED = 0.075                 # m per frame (1.7 m/s march)
_CAST = [("footman_a", 0)]   # crimson only: blue is reserved for the Scots (footman_b base is blue)


def lerp_(a, b, t):
    return a + (b - a) * t


def blink(g, off):
    return 1 if ((g + off) % 83) < 3 else 0


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else [a[0]]
    return out


def walker_xy(i, g):
    r, c = divmod(i, 2)
    x = (-0.65 if c == 0 else 0.65) + 0.08 * math.sin(i * 1.7)
    y0 = 36.3 - 1.5 * r - (0.35 if c else 0.0)
    y = y0 + SPEED * (g - G0)
    # beyond the bridge end the column spreads out onto the causeway
    if y > 38.5:
        k = ez((y - 38.5) / 6.0)
        x = x * (1 + 2.2 * k) + 0.9 * k * math.sin(i * 2.3)
    return x, y


def z_at(x, y):
    zg = float(K.ground(x, y))
    if y < 39.5:
        zg = lerp(K.DECK_Z, zg, ez((y - 37.0) / 2.5))
    return zg


N_MEAD = 120


def mead_xy(m):
    r, c = divmod(m, 15)
    return -24.0 + 3.3 * c + (1.6 if r % 2 else 0.0) + 0.5 * math.sin(m * 2.1), 58.0 + 3.3 * r + 0.6 * math.cos(m * 1.3)


def mead_arrive(m):
    r, c = divmod(m, 15)
    return 955 + 9 * r + int(2.0 * ((c * 7) % 15))


def mead_pose(m, g):
    cast, var = _CAST[m % len(_CAST)]
    p = dict(STORY[cast + "_stand"][1]); p["variant21"] = var
    p["lean"] = 2.0 * math.sin(g * 0.2 + m); p["head_dy"] = 0.02 * math.sin(g * 0.37 + m); p["head_roll"] = 3 * math.sin(g * 0.13 + m)
    p["blink"] = blink(g, m * 11); p["t"] = g / 30.0
    return K.with_rim(p)


def pose_of(i, g):
    cast, var = _CAST[i % len(_CAST)]
    ph = (g + 5 * i) / 20.0
    p = cast21.walk_spear(cast, ph, 1, "march")
    glance = ez((g - (902 + i)) / 8.0) * (1 - ez((g - (945 + i)) / 10.0)) if i < 8 else 0.0     # the first men glance up at the hill
    if glance > 0:
        p.update(expr="worried", gaze=(0.9, -0.6), pitch=-0.3 * glance)
    p["variant21"] = var
    p["blink"] = blink(g, i * 17)
    p["t"] = g / 30.0
    return K.with_rim(p)


def run(quality, gs, samples, out):
    work = os.path.join(HERE, "work", "E2_" + quality)
    T = C.Take(['bridge_end_north', 'valley_loop'], work, quality, fg=['bridge_end_north'], over=dict(sun_k=SUN_K))
    K.scots_wide_line(n=30, banners=4, scale=1.5, toward=(-20.0, 44.0), hh0=22.0)   # the Scots stand still on the hill: blue figures + saltire banners
    A = T.A
    # clear the preset troops / crowd: our cast and the staged meadow crowd replace them
    K.place_troops(A, 'bridge', 0); K.place_troops(A, 'causeway', 0); K.place_troops(A, 'meadow', 0)
    for o in list(bpy.data.objects):
        if o.name.startswith("crowd") or o.name.startswith("bridge_knights"):
            bpy.data.objects.remove(o, do_unlink=True)
    os.makedirs(out, exist_ok=True)
    acts = [(T.make_actor("w%d" % i, _CAST[i % len(_CAST)][0]), _CAST[i % len(_CAST)][0]) for i in range(N_WALK)]
    mact = [(T.make_actor("m%d" % m, _CAST[m % len(_CAST)][0]), _CAST[m % len(_CAST)][0]) for m in range(N_MEAD)]
    paths = {}
    for g in gs:
        r = K.cam_path(None, KEYS, g)
        paths[g] = r
        T.key_cam(g, r["loc"], r["look"], r["lens"])
    for i, (a, cast) in enumerate(acts):
        for g in gs:
            x, y = walker_xy(i, g)
            T.place(a, g, (x, y, z_at(x, y)), cast)
    for i, (a, cast) in enumerate(acts):
        for g in gs:
            T.pose(a, g, pose_of(i, g))
        T.sprites_for([(a, 64, gs)])
    for m, (a, cast) in enumerate(mact):
        x, y = mead_xy(m)
        for g in gs:
            T.place(a, g, (x, y, float(K.ground(x, y))), cast)
            T.pose(a, g, mead_pose(m, g))
        T.sprites_for([(a, 32, gs)])

    def hook(g):
        K.cam_path(None, KEYS, g)                            # re-sets the camera
        v0, v1 = (GAMMA0, K.VIVID['bridge_end_north'][1], 1.0), tuple(K.VIVID['valley_loop']); v1 = v1 + (1.0,) * (3 - len(v1)); u = ez((g - 940) / 80.0)
        K.STATE['vivid'] = (math.exp(lerp(math.log(v0[0]), math.log(v1[0]), u)), lerp(v0[1], v1[1], u), lerp(v0[2], v1[2], u))   # eases into the set's valley_loop grade
        K.set_flow(g / 30.0); K.set_flutter(g / 30.0); K.set_smoke(g / 30.0)
        for m, (a, cast) in enumerate(mact):
            hid = g < mead_arrive(m)
            for ob in (a.card, a.proxy, a.contact):
                if ob is not None: ob.hide_render = hid
        if g >= 955:                                          # the meadow fills (placeholders: tiny at this height)
            n = int(lerp(10, 380, ez((g - 955) / 85.0)))
            def cb(items):
                its = []
                for (x, y, z, k, s) in items:
                    xx, yy = x * 1.7, 90.0 + (y - 46.0) * 0.9
                    its.append((xx, yy, float(K.ground(xx, yy)), "knight", 2.08))   # crimson only
                for o in K.stage_crowd(its, cam=T.cam): o.name = "troops_meadow_" + o.name
            K.place_troops(A, "meadow", n, seed=3, cb=cb)
    for g in gs:
        path = os.path.join(out, "g_%04d.png" % g)
        t0 = time.time()
        T.render(g, path, samples, hook=hook)
        h = T.heads(g)
        json.dump(dict(cam=paths[g]["loc"], look=paths[g]["look"], heads=h), open(path[:-4] + ".json", "w"), default=float)
        print("g %d  %.1f s  cam %s" % (g, time.time() - t0, tuple(round(v, 1) for v in paths[g]["loc"])), flush=True)


if __name__ == "__main__":
    quality = sys.argv[1]; spec = sys.argv[2]
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else (8 if quality == "draft" else 32)
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw_" + quality)
    run(quality, [g for g in parse(spec) if G0 <= g <= G1], samples, out)
