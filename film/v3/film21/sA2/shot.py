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
G0, G1, GJ = 77, 159, 80
G_PUSH = C.g_of(4.08)            # 125 "อะไรเลยสักอย่าง"
PPD = 160
VW = ((445.0, 244.0, 361.0), (64.0, 44.0, 0.0), 22.0)

W = np.array([158.0, 148.0])
U = np.array([-158.0, -146.0]); U = U / np.linalg.norm(U)      # toward the bridge
R = np.array([U[1], -U[0]])                                     # screen-right of the view


def gz(p):
    return float(K.ground(p[0], p[1]))


def wpos(k, d=0.0):
    p = W + R * k + U * d
    return (float(p[0]), float(p[1]), gz(p))


def end_cam():
    e = W - U * 4.4 + R * 1.3
    loc = (float(e[0]), float(e[1]), gz(e) + 3.4)
    look = (float(W[0] + U[0] * 6), float(W[1] + U[1] * 6), gz(W) + 0.2)
    return loc, look


def push_cam():
    """x1.4 closer to the grass-chewer (offset -1.9 along R)"""
    (l0, k0) = end_cam()
    ch = np.array(wpos(-1.0)); l0 = np.array(l0); k0 = np.array(k0)
    nl = l0 + (ch + np.array([0, 0, 1.2]) - l0) * (1 - 1 / 1.4)
    nk = k0 + (ch + np.array([0, 0, 1.0]) - k0) * 0.55
    return tuple(nl), tuple(nk)


def keys():
    P_A = K.POSES["P_A"]
    a = np.array(P_A[0]); b = np.array(VW[0]); back = a + (b - a) / np.linalg.norm(b - a) * 9.0
    lb = np.array(P_A[1]) + (np.array(VW[1]) - np.array(P_A[1])) * 0.02
    el, ek = end_cam()
    return [(77, tuple(back), tuple(lb), 22.0), (80, P_A[0], P_A[1], 22.0),
            (101, (222.0, 178.0, 84.0), (150.0, 136.0, 38.0), 22.0),
            (114, (216.0, 178.0, 90.0), (el[0] - 10, el[1] - 10, 34.0), 22.0),
            (125, el, ek, 22.0)]


def cam_state(g):
    if g <= 125:
        r = K.cam_path(None, keys(), g)
        return r["loc"], r["look"], r["lens"], r["vivid"]
    # push 15 f x1.4 on the chewer, then a slow drift (never static)
    el, ek = end_cam(); pl, pk = push_cam()
    u = min((g - G_PUSH) / 15.0, 1.0)
    e = u * u * (3 - 2 * u) * 0.8 + 0.2 * u
    loc = np.array(el) + (np.array(pl) - np.array(el)) * e
    look = np.array(ek) + (np.array(pk) - np.array(ek)) * e
    t = max(g - (G_PUSH + 15), 0) / 30.0
    loc = loc + np.array([R[0], R[1], 0.0]) * 0.18 * t + np.array([U[0], U[1], 0.0]) * 0.22 * t
    look = look + np.array([R[0], R[1], 0.0]) * 0.10 * t
    return tuple(loc), tuple(look), 22.0, K.STATE.get("vivid")


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


class Seg(object):
    def __init__(self):
        t0 = time.time()
        self.A = K.build_world(["valley_wide", "hill_over"], fg=False)
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
