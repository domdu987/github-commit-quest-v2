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
N_LEAD = 10                   # "ข้ามมาสิบคน": ten men already out on the causeway
N_WALK = 100                  # "ข้ามมาร้อยคน": ~100 in view at g938 (queue on the bridge + the fan beyond the mouth)
N_MEAD = int(os.environ.get('N_MEAD', 280))
POP = 985                     # "เป็นพัน": the meadow fills with hundreds on this frame
LENS = 20.0
SUN_K = float(os.environ.get('SUN_K', 1.3))
GAMMA0 = float(os.environ.get('GAMMA0', 1.55))
_CAST = [("footman_a", 0)]
# camera travel keys: (g, loc, look, lens): camera on the WEST bank looking ENE, the column crosses the frame, the hill (Scots) is in the upper third
KEYS = [(885, (-8.0, 42.5, 1.7), (22.0, 49.0, 1.8), LENS),
        (912, (-8.5, 43.0, 2.5), (23.0, 50.0, 2.2), LENS),
        (938, (-14.0, 37.0, 8.0), (90.0, 56.0, 6.0), LENS),
        (975, (-18.0, 41.0, 11.0), (80.0, 74.0, 8.0), LENS),
        (1000, (-22.0, 44.0, 27.0), (60.0, 86.0, 10.0), 22.0),
        (1044, (-26.0, 46.0, 44.0), (40.0, 90.0, 12.0), 24.0)]


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
    if i < N_LEAD:
        y = 40.5 + 0.85 * (N_LEAD - 1 - i) + 0.06 * (g - G0)
        x = 0.2 + 1.7 * math.sin(i * 2.1)
    else:
        k = i - N_LEAD; row, col = divmod(k, 3)
        x = (-0.9, 0.0, 0.9)[col] + 0.06 * math.sin(i * 1.7)
        y = 37.4 - 1.0 * row - 0.25 * col + 0.095 * (g - G0)
        if y > 38.5:                                  # beyond the bridge mouth the pack fans out onto the meadow
            kf = ez((y - 38.5) / 12.0)
            x = x * (1 + 4.0 * kf) + 1.5 * kf * math.sin(i * 2.3)
    return x, y


def z_at(x, y):
    """the deck ends at y 38.25 (its top is DECK_Z); the men step down onto the terrain there (no ramp: nothing hovers)."""
    return float(K.DECK_Z) if y < 38.25 else float(K.ground(x, y))


def mead_slots():
    out = []; rs = np.random.RandomState(7)
    for r in range(60):
        for c in range(40):
            x = -8.0 + 2.3 * c + (1.15 if r % 2 else 0.0) + rs.uniform(-0.5, 0.5); y = 50.0 + 2.2 * r + rs.uniform(-0.5, 0.5)
            if math.hypot(x - K.LOOP_C[0], y - K.LOOP_C[1]) < K.LOOP_R - 14 and float(K.sd_at(x, y)) > 3 and y > 50:
                out.append((x, y))
    # the nearest first so a trimmed list keeps the crowd in front of the lens
    out.sort(key=lambda p: (p[0] - 8) ** 2 + (p[1] - 72) ** 2)
    return out[:N_MEAD]


def mead_arrive(m):
    return POP - 6 + (m * 7919) % 15


def mead_pose(m, g):
    cast, var = _CAST[m % len(_CAST)]
    p = dict(STORY[cast + "_stand"][1]); p["variant21"] = var
    p["lean"] = 2.5 * math.sin(g * 0.2 + m); p["head_dy"] = 0.03 * math.sin(g * 0.37 + m); p["head_roll"] = 4 * math.sin(g * 0.13 + m)
    if m % 5 == 0:
        p["gaze"] = (0.9, -0.5); p["expr"] = "worried"
    p["blink"] = blink(g, m * 11); p["t"] = g / 30.0
    return K.with_rim(p)


def pose_of(i, g):
    cast, var = _CAST[i % len(_CAST)]
    ph = (g + 5 * i) / 20.0
    p = cast21.walk_spear(cast, ph, -1, "march")
    glance = ez((g - (895 + 2 * i)) / 8.0) * (1 - ez((g - (950 + i)) / 10.0)) if i % 3 == 0 else 0.0     # one in three glances up at the hill
    if glance > 0:
        p.update(expr="worried", gaze=(-0.9, -0.6), pitch=-0.3 * glance)
    p["variant21"] = var
    p["blink"] = blink(g, i * 17)
    p["t"] = g / 30.0
    return K.with_rim(p)


def _terrain_z(x, y):
    """z of the terrain mesh under (x, y) if the first thing hit from above is the terrain (not a rock / tree), else None."""
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, Vector((x, y, 300.0)), Vector((0, 0, -1)))
    return float(loc.z) if hit and ob.name.startswith("terrain") else None


def scot_slots(n=10):
    out = []; a0, a1 = 196.0, 240.0
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * (k + 0.5) / n)
        for r_ in np.arange(30, 120, 1.0):
            x = K.HILL_C[0] + r_ * math.cos(a) * 1.05; y = K.HILL_C[1] + r_ * 0.9 * math.sin(a)
            if float(K.hill_h(np.array([x]), np.array([y]))[0][0]) < 26.0 + 1.5 * (k % 2): break
        for dr in (0, 1.5, -1.5, 3, -3, 4.5, -4.5, 6, -6, 8, -8):         # step off a rock onto bare terrain
            xx = x + dr * math.cos(a + 1.57); yy = y + dr * math.sin(a + 1.57); z = _terrain_z(xx, yy)
            if z is not None:
                x, y = xx, yy; break
        out.append((x, y, z if z is not None else float(K.ground(x, y))))
    return out


SCOT_SCALE = 8.0
_SCOT_POSES = ["scot_a_fold_spear", "scot_a_chew_grass", "scot_a_scratch_nose", "scot_a_stand_still"]


def scot_pose(k, g):
    p = dict(STORY[_SCOT_POSES[k % 4]][1])
    p["lean"] = 2.0 * math.sin(g * 0.11 + k * 1.3); p["head_dy"] = 0.02 * math.sin(g * 0.3 + k); p["blink"] = blink(g, k * 29); p["t"] = g / 30.0
    p["mouth"] = "flat"
    return K.with_rim(p)


GCMODE = bool(os.environ.get('GC'))


def _sp(T, items):
    if not GCMODE:
        T.sprites_for(items)


def run(quality, gs, samples, out):
    work = os.path.join(HERE, "work", "E2_" + quality)
    T = C.Take(['bridge_end_north', 'valley_loop'], work, quality, fg=['bridge_end_north'], over=dict(sun_k=SUN_K))
    A = T.A
    # clear the preset troops / crowd: our cast cards replace them
    K.place_troops(A, 'bridge', 0); K.place_troops(A, 'causeway', 0); K.place_troops(A, 'meadow', 0)
    for o in list(bpy.data.objects):
        if o.name.startswith("crowd") or o.name.startswith("bridge_knights"):
            bpy.data.objects.remove(o, do_unlink=True)
    # the Scots wait on the hill: oversized saltire banners (set) + idle cast cards on the slope
    Bp = K.Batch(89); rs_ = np.random.RandomState(13)
    for (x, y, z) in scot_slots(3):
        K.banner(Bp, (x, y, z), 34.0, 215.0 + 90.0, 't_saltire', 't_white', 'saltire', rs_, size=(18.0, 11.0))
    Bp.finalize('scots_wide_banners')
    # near-ground dressing for the opening (camp clutter): barrels, a stack of spears, gorse tufts, boulders
    Bd = K.Batch(66); rd = np.random.RandomState(5)
    for (x, y) in [(6.4, 40.2), (7.2, 43.0), (6.6, 46.5), (-6.0, 47.5), (-5.8, 45.0)]:
        K.barrel(Bd, (x, y, float(K.ground(x, y))), rs=rd)
    for (x, y, sz) in [(-6.6, 38.6, 0.9), (6.5, 38.8, 0.8), (-5.8, 39.8, 1.0), (7.4, 49.0, 1.0), (-6.4, 52.0, 1.1), (6.8, 54.0, 1.1), (-6.2, 36.6, 0.8), (-6.0, 41.8, 0.45), (-5.6, 44.2, 0.4), (-6.8, 44.6, 0.5)]:
        K.gorse(Bd, (x, y, float(K.ground(x, y))), sz, rd)
    for (x, y, sz) in [(-5.6, 41.0, 0.7), (6.0, 44.5, 0.8), (-6.2, 43.6, 0.35)]:
        K.boulder(Bd, x, y, float(K.ground(x, y)), sz, rd)
    for (x, y) in [(6.0, 38.9), (6.3, 39.2), (6.6, 38.8)]:
        K.spear(Bd, (x, y, float(K.ground(x, y))), tilt=(0.25, -0.2), h=2.4)
    Bd.finalize('dress_e2')
    os.makedirs(out, exist_ok=True)
    acts = [(T.make_actor("w%d" % i, "footman_a"), "footman_a") for i in range(N_WALK)]
    slots = mead_slots()
    mact = [(T.make_actor("m%d" % m, "footman_a"), "footman_a") for m in range(len(slots))]
    sslots = scot_slots(10)
    scots = [T.make_actor("s%d" % k, "scot_a") for k in range(len(sslots))]
    paths = {}
    for g in gs:
        r = K.cam_path(None, KEYS, g)
        paths[g] = r
        T.key_cam(g, r["loc"], r["look"], r["lens"])
    for i, (a, cast) in enumerate(acts):
        for g in gs:
            x, y = walker_xy(i, g)
            T.place(a, g, (x, y, z_at(x, y)), cast)
            T.pose(a, g, pose_of(i, g))
        _sp(T, [(a, 48 if i < 30 else 32, gs)])
    s0 = C.REAL_H["footman_a"] / C.PUPPET_H["footman_a"]
    for m, (a, cast) in enumerate(mact):
        x, y = mead_xy_ = slots[m]
        for g in gs:
            pop = ez((g - mead_arrive(m)) / 6.0) if g >= mead_arrive(m) else 0.0
            a.place(C.bf(g), (x, y, float(K.ground(x, y))), scale=s0 * max(pop, 0.02))
            T.pose(a, g, mead_pose(m, g))
        _sp(T, [(a, 32, gs)])
    ss0 = C.REAL_H["scot_a"] / C.PUPPET_H["scot_a"] * SCOT_SCALE
    for k, a in enumerate(scots):
        x, y, zs = sslots[k]
        for g in gs:
            a.place(C.bf(g), (x, y, zs), scale=ss0)
            T.pose(a, g, scot_pose(k, g))
        _sp(T, [(a, 48, gs)])

    if GCMODE:                                            # ground check (QA_TEAM §K): every card must touch the ground in every sampled frame
        sys.path.insert(0, os.path.join(HERE, "..", "..", "set3d21")); import ground_check21 as GC

        def set_frame(g):
            bpy.context.scene.frame_set(C.bf(g))
            for m, (a, cast) in enumerate(mact):
                hid = g < mead_arrive(m)
                for ob in (a.card, a.proxy, a.contact):
                    if ob is not None: ob.hide_render = hid
        # cards carry transparent padding under the soles, so the check is made at each actor's FOOT point (the xyz it is placed at)
        from mathutils import Vector
        feet = {}
        for i, (a, _c) in enumerate(acts): feet[a.name] = (a, lambda g, i=i: (lambda xy: (xy[0], xy[1], z_at(*xy)))(walker_xy(i, g)), None)
        for m, (a, _c) in enumerate(mact): feet[a.name] = (a, lambda g, m=m: (slots[m][0], slots[m][1], float(K.ground(*slots[m]))), m)
        for k, a in enumerate(scots): feet[a.name] = (a, lambda g, k=k: sslots[k], None)
        rows = []; fail = 0; sunk = 0
        for g in gs:
            set_frame(g); bpy.context.view_layer.update()
            sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
            for nm, (a, fn, m) in feet.items():
                if m is not None and g < mead_arrive(m) + 7: continue
                x, y, z = fn(g); own = GC._own(a.card); org = Vector((x, y, z + 0.5)); gap = None
                for dy in (0.0, 0.15, -0.15):                      # three rays: a plank seam must not read as a gap
                    org = Vector((x, y + dy, z + 0.5))
                    for _ in range(12):
                        hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, org, Vector((0, 0, -1)))
                        if not hit: break
                        if ob.name in own or ob.name.startswith(("contact", "shadow", "proxy")) or ob.hide_render:
                            org = loc + Vector((0, 0, -1e-3)); continue
                        gg = z - loc.z
                        gap = gg if gap is None else min(gap, gg); break
                if gap is None or gap > GC.TOL:
                    fail += 1; rows.append((g, nm, "FAIL", "nothing below" if gap is None else "%.1f cm above" % (gap * 100)))
                elif gap < -GC.SINK:
                    sunk += 1; rows.append((g, nm, "SUNK", "%.1f cm below" % (-gap * 100)))
        lines = ["# GROUND check (QA §K) - %s" % ("PASS" if fail == 0 else "FAIL"), "",
                 "Foot-point ray cast (cards have transparent padding under the soles; each actor is placed AT its foot point). frames sampled: %d; actors: %d (%d walkers, %d meadow cards, %d Scots); FAIL %d; SUNK %d; tolerance 2 cm." % (len(gs), len(feet), len(acts), len(mact), len(scots), fail, sunk),
                 "All cards have contact=True shadows. Barrels, gorse, boulders, spears and banner poles are placed with K.ground() at their base.", ""]
        if rows:
            lines += ["| g | item | result | gap |", "|---|---|---|---|"] + ["| %d | %s | %s | %s |" % r for r in rows]
        open(os.path.join(HERE, "GROUND.md"), "w").write("\n".join(lines) + "\n")
        rep = dict(fail=fail, sunk=sunk)
        print("GC", rep.get("fail"), rep.get("sunk"), flush=True)
        return

    def hook(g):
        K.cam_path(None, KEYS, g)
        v0, v1 = (GAMMA0, K.VIVID['bridge_end_north'][1], 1.0), tuple(K.VIVID['valley_loop']); v1 = v1 + (1.0,) * (3 - len(v1)); u = ez((g - 940) / 80.0)
        K.STATE['vivid'] = (math.exp(lerp(math.log(v0[0]), math.log(v1[0]), u)), lerp(v0[1], v1[1], u), lerp(v0[2], v1[2], u))
        K.set_flow(g / 30.0); K.set_flutter(g / 30.0); K.set_smoke(g / 30.0)
        for m, (a, cast) in enumerate(mact):
            hid = g < mead_arrive(m)
            for ob in (a.card, a.proxy, a.contact):
                if ob is not None: ob.hide_render = hid
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
