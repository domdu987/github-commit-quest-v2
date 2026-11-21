#!/usr/bin/env python3
"""shot.py -- film 21 segment A2 (BIGZOOM 1, second half): g 77..159 (3 handle frames g 77-79 continue team 1's A1 move into P_A at g 80).
D6 in at P_A, CUT out at g 159.  Swoop from P_A down over the crag, through the Scots pines and a light shaft, to a MEDIUM shot of the Scots
line on the shelf seen from behind-side (Wallace centre, arms folded on his spear), the bridge with knights far below (g 125); then a 15 f push
x1.4 onto the grass-chewer on "อะไรเลยสักอย่าง" (g 125).

    python3 shot.py path <out.mp4>              10 fps 360x640 path draft (with the cast)
    python3 shot.py stills a:b[:step] <dir> [draft|final] [samples]
    python3 shot.py final a:b[:step] [samples]
"""
import math, os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                          # noqa: E402
import cast21, bpy, numpy as np                          # noqa: E402,E401
from c21 import K, actors, Vector, lerp, ez              # noqa: E402

TMP = os.path.join(HERE, "work")
G0, G1, GJ = 80, 159, 80       # v4: A1 -> A2 is a HARD CUT at g80, no handle frames
G_PUSH = C.g_of(4.08)            # 125 "อะไรเลยสักอย่าง"
PPD = 160
VW = ((-60.0, -260.0, 230.0), (60.0, 60.0, 0.0), 22.0)       # P_HOOK: where A1 starts; A1 arrives at P_A from there

W = np.array([158.0, 148.0])
U = np.array([-158.0, -146.0]); U = U / np.linalg.norm(U)      # toward the bridge
R = np.array([U[1], -U[0]])                                     # screen-right of the view


def gz(p):
    return float(K.ground(p[0], p[1]))


def wpos(k, d=0.0):
    p = W + R * k + U * d
    return (float(p[0]), float(p[1]), gz(p))


def push_cam():
    """x1.4 closer to the grass-chewer (offset -1.9 along R)"""
    (l0, k0) = end_cam()
    ch = np.array(wpos(-1.0)); l0 = np.array(l0); k0 = np.array(k0)
    nl = l0 + (ch + np.array([0, 0, 1.2]) - l0) * (1 - 1 / 1.4)
    nk = k0 + (ch + np.array([0, 0, 1.0]) - k0) * 0.55
    return tuple(nl), tuple(nk)


G_SPL = 112          # the summit pass; from here the dive to the medium pose is an eased Hermite (arrives at g125 with a small forward velocity, never a stop)
E_BACK, E_LAT, E_UP = 6.0, -0.5, 5.0
MID = (212.0, 162.0, 96.0)
WPS = [(96, (120.0, 104.0, 70.0), (160.0, 148.0, 40.0)), (106, (172.0, 150.0, 92.0), (150.0, 130.0, 30.0)), (G_SPL, (206.0, 172.0, 100.0), None)]


def end_cam():
    e = W - U * E_BACK + R * E_LAT
    loc = (float(e[0]), float(e[1]), gz(e) + E_UP)
    look = (float(W[0] + U[0] * 6), float(W[1] + U[1] * 6), gz(W) + 0.2)
    return loc, look


def keys():
    P_A = K.POSES["P_A"]
    el, ek = end_cam()
    ks = [(80, P_A[0], P_A[1], 22.0)]
    for g, loc, look in WPS:
        ks.append((g, loc, look if look else (el[0] - 10, el[1] - 10, 34.0), 22.0))
    dv = np.array(ek) - np.array(el); dv /= np.linalg.norm(dv)
    ks.append((119, MID, (el[0] - 6, el[1] - 6, 36.0), 22.0))          # a high mid-waypoint: ray-cast clearance >= 3 m from every pine crown (g118 was inside one)
    ks.append((G_PUSH, el, ek, 22.0))
    ks.append((G_PUSH + 6, tuple(np.array(el) + dv * 1.2), ek, 22.0))   # a key past E: the camera arrives at g125 still moving (ease-out belongs to this last segment)
    return ks


def _herm(p0, m0, p1, m1, t):
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + (-2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1


def cam_state(g):
    if g <= G_PUSH:
        r = K.cam_path(None, keys(), g)
        return r["loc"], r["look"], r["lens"], r["vivid"]
    viv = K.STATE.get("vivid"); el, ek = end_cam(); el = np.array(el); ek = np.array(ek)
    pl, pk = push_cam(); dirv = ek - el; dirv /= np.linalg.norm(dirv)
    u = min((g - G_PUSH) / 15.0, 1.0)
    e = 0.012 * 15 * u / (0.8 * 15 * 0.1 + 1e-9) * 0.0 + (u * u * (3 - 2 * u)) * 0.85 + 0.15 * u                  # smoothstep + a linear part: starts with the drift velocity
    loc = el + (np.array(pl) - el) * e; look = ek + (np.array(pk) - ek) * e
    t = max(g - (G_PUSH + 15), 0) / 30.0
    loc = loc + np.array([R[0], R[1], 0.0]) * 0.18 * t + np.array([U[0], U[1], 0.0]) * 0.22 * t
    look = look + np.array([R[0], R[1], 0.0]) * 0.10 * t
    return tuple(loc), tuple(look), 22.0, viv


# ---------------------------------------------------------------------------- cast
LINE = [("s2", "scot_b", "scot_b_chew_grass", -1.0, 0.0, 0.8), ("w", "wallace", "wallace_fold_spear", 0.1, 0.4, 1.5),
        ("s3", "scot_a", "scot_a_fold_spear", 1.05, 0.0, 2.2), ("s1", "scot_c", "scot_c_fold_spear", -2.0, 1.7, 0.4),
        ("s4", "scot_a_v1", "scot_a_stand_still", 1.9, 1.9, 3.0), ("s5", "scot_c_v1", "scot_c_stand_still", -0.5, 1.7, 3.7),
        ("s6", "scot_b_v1", "scot_b_fold_spear", 0.55, 2.3, 4.4)]


def S(name):
    cast, pose = cast21.STORY21[name]
    return cast, dict(pose)


def pose_of(e, g):
    nm, cast, pname, k, d, ph = e
    _, p = S(pname)
    p = dict(p)
    p["yaw"] = -0.9 if True else p.get("yaw", 0.3)         # three-quarter from behind-side: they look toward the bridge (screen left)
    sh = math.sin(g * 0.075 + ph * 2.0)                       # weight shifts
    p["lean"] = p.get("lean", 0.0) + 2.2 * sh
    p["head_roll"] = p.get("head_roll", 0.0) + 2.0 * math.sin(g * 0.11 + ph)
    p["blink"] = cast21.blink_at(g, 90 + int(ph * 9), int(ph * 31))
    p["t"] = g / 30.0
    if nm == "s2":
        p["head_roll"] += 3.0 * math.sin(g * 0.45)          # chewing
    return K.with_rim(p)



TRAVEL = 1.0


def build_column():
    """A1's column (team 1 sA1/shot.py): the whole bridge deck and both causeways full of knight PAIRS, crimson/white caparisons, one gold pennon per pair."""
    rs = np.random.RandomState(5); B = K.Batch(88); B2 = K.Batch(87); S = 1.4
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
    from mathutils import Vector as V3

    def support(x, y):
        hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, V3((x, y, 14.0)), V3((0, 0, -1)))
        return float(loc.z) if hit else float(K.ground(x, y))
    for i, y in enumerate(np.arange(-56.0, 66.0, 4.2)):
        zs = []; deck = -30.0 <= y <= 34.0; Bc = B if deck else B2
        if deck and any(abs(support(K.BRIDGE_X + s_, y + TRAVEL) - support(K.BRIDGE_X + s_, y)) > 0.02 for s_ in (-0.95, 0.95)): continue
        for sx in (-0.95, 0.95):
            x = K.BRIDGE_X + sx; z = support(x, y); zs.append(z)
            m = (("t_red", "t_white"), ("t_red", "t_cream"))[(i + (sx > 0)) % 2]
            K.horse(Bc, (x, y, z), 90.0, coat=["horse", "horse_dk", "horse"][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.9 + 0.2 * rs.rand(), rider=(m[0],), scale=S)
        xm, zm = K.BRIDGE_X, float(np.mean(zs))
        Bc.rod("wood", (xm, y, zm + 3.2), (xm, y, zm + 6.2), 0.05, seg=4); Bc.box("gold", (xm + 0.0, y + 0.55, zm + 5.8), (0.05, 1.1, 0.7))
    B2.finalize("troops_cws")
    return B.finalize("troops_col")



class Seg(object):
    def __init__(self):
        t0 = time.time()
        self.A = K.build_world(["valley_wide", "hill_over"], fg=False, shafts=False, scots_wide=False)
        K.scots_wide_line(n=26, banners=5, scale=2.2, toward=(120.0, -300.0))                 # A1's exact call
        for o in [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]: bpy.data.objects.remove(o, do_unlink=True)
        self.knights = build_column()                                                          # A1's knight-pair column (same code, same start)
        self.scene = bpy.context.scene; self.cam = self.scene.camera; self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 2000
        self.acts = {}
        for nm, cast, pname, k, d, ph in LINE:
            self.acts[nm] = C.make_actor(nm, cast, os.path.join(TMP, "sprites"))
        self.fg()
        print("A2: built world in %.1f s" % (time.time() - t0), flush=True)

    def fg(self):
        el, ek = end_cam(); rs = np.random.RandomState(11)
        B = K.Batch(96); Bg = K.Batch(97); Br = K.Batch(98)
        e = np.array(el)
        for (d, lat, s) in [(2.3, -1.0, 0.6), (2.0, 1.1, 0.55), (3.1, 2.6, 0.7)]:
            p = e[:2] + U * d + R * lat; K.gorse(Bg, (p[0], p[1], gz(p)), s, rs)
        B.finalize("fg_a2"); Bg.finalize("fg_a2_g", ink=False); Br.finalize("fg_a2_r", ink=False)

    def plan(self, gs):
        cam = self.cam
        self.viv = {}
        for g in gs:
            f = g + 1
            loc, look, lens, viv = cam_state(g)
            self.viv[g] = viv
            cam.location = loc; cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
            cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam.data.keyframe_insert("lens", frame=f)
            for nm, cast, pname, k, d, ph in LINE:
                x, y, z = wpos(k, d)
                sc = C.SCALE.get(cast.split("_v")[0], C.CS)
                self.acts[nm].place(f, (x, y, z), scale=sc)
        for g in gs:
            f = g + 1; self.scene.frame_set(f)
            for e in LINE:
                self.acts[e[0]].pose(f, pose_of(e, g), camera=cam)
        for nm, a in self.acts.items():
            a.render_sprites(PPD, frames=[g + 1 for g in gs])

    def render_one(self, g, out, mode="final", samples=32):
        self.scene.frame_set(g + 1); bpy.context.view_layer.update()
        actors.sync_all(self.scene, self.cam)
        for o in self.knights: o.location.y = TRAVEL * g / 83.0            # A1: the same function of g, so the walk continues across the cut
        K.show_all_banners()
        if g >= 112: K.hide_near_banners([(float(W[0]), float(W[1]), 45.0)], 32.0, smoke=False)     # only once the camera is past them: the cloth that would block the bridge view
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        if self.viv.get(g): K.STATE["vivid"] = self.viv[g]
        return K.render(out, mode, samples)

    def report(self, g):
        self.scene.frame_set(g + 1); K.setup_render(self.scene, "final"); bpy.context.view_layer.update()
        out = {}
        for nm, cast, pname, k, d, ph in LINE:
            x, y, z = wpos(k, d); H = 1.7 if nm != "w" else 1.92
            px, py, dz = K.project(self.cam, (x, y, z + H * 0.9)); out[nm] = (round(px), round(py), round(dz, 1))
        loc = self.cam.location
        return dict(g=g, cam=[round(v, 1) for v in loc], heads=out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "path":
        gs = list(range(G0, G1 + 1, 3)); out = sys.argv[2]
    else:
        gs = C.parse(sys.argv[2]); gs = [g for g in gs if G0 <= g <= G1]
    Tk = Seg(); Tk.plan(gs)
    if cmd == "path":
        d = os.path.join(HERE, "work", "pathdraft"); os.makedirs(d, exist_ok=True)
        for i, g in enumerate(gs):
            Tk.render_one(g, os.path.join(d, "p_%03d.png" % i), "draft", 8); print(json.dumps(Tk.report(g)), flush=True)
        subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", "10", "-i", os.path.join(d, "p_%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out])
    elif cmd == "stills":
        out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        os.makedirs(out, exist_ok=True)
        for g in gs:
            dt = Tk.render_one(g, os.path.join(out, "a2_g_%04d.png" % g), mode, samples); print(json.dumps(Tk.report(g)), "%.1fs" % dt, flush=True)
    elif cmd == "final":
        samples = int(sys.argv[3]) if len(sys.argv) > 3 else 32
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png) and os.path.exists(png[:-4] + ".json"): continue
            dt = Tk.render_one(g, png, "final", samples); rep = Tk.report(g); rep.update(wall=round(dt, 1), samples=samples)
            json.dump(rep, open(png[:-4] + ".json", "w")); print("A2 g %d %.1f s" % (g, dt), flush=True)
