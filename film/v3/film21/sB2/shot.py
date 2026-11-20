#!/usr/bin/env python3
"""shot.py -- film 21 segment B2: g 295..418 (3 handle frames g 295-297 continue team 2's B1 move into P_CAMP at g 298).  D6 in at P_CAMP, CUT out at g 418.
From the knights' parade (P_CAMP = camp_wide) the camera CRANES UP over the pavilions, flies north-east across the river (glitter, the bridge on the left), and
climbs to Abbey Craig; it lands LOW looking up at the Scots spearmen on foot against the sky (P_HILL = hill_low raised 0.8 m, light shafts through the pines).
They shift their spears; one leans on his.

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
G0, G1, GJ = 295, 418, 298
PPD = 128
STAND = [("s1", "scot_b", "scot_b_fold_spear", "s1", 0.0), ("s2", "scot_a", "scot_a_fold_spear", "s2", 1.1),
         ("horn", "scot_horn", "scot_horn_lower", "horn", 2.0), ("w", "wallace", "wallace_fold_spear", "w", 0.6),
         ("s3", "scot_c", "scot_c_stand_still", "s3", 2.9)]


def p_hill():
    loc, look, lens = K.preset_pose("hill_low")
    return (loc[0], loc[1], loc[2] + 0.8), look, lens


def keys():
    pc = K.preset_pose("camp_wide"); ph = p_hill()
    loc = np.array(pc[0]); look = np.array(pc[1]); fwd = look - loc; fwd[2] = 0; fwd /= np.linalg.norm(fwd)
    back = loc - fwd * 5.0 + np.array([0, 0, 2.4])
    over = np.array(ph[0]) + (np.array(ph[0]) - np.array(look)) * 0.0
    end_beyond = np.array(ph[0]) + (np.array(ph[1]) - np.array(ph[0])) * 0.06
    return [(295, tuple(back), tuple(look + np.array([0, 0, 0.3])), 22.0), (298, pc[0], pc[1], 22.0),
            (322, (-50.0, -76.0, 38.0), (12.0, -38.0, 10.0), 22.0),
            (348, (6.0, -42.0, 46.0), (60.0, 22.0, 6.0), 22.0),
            (376, (64.0, 12.0, 36.0), (118.0, 90.0, 12.0), 22.0),
            (398, (104.0, 84.0, K_g(104, 84) + 14.0), (140.0, 130.0, 16.0), 22.0),
            (418, ph[0], ph[1], 22.0),
            (430, tuple(end_beyond), ph[1], 22.0)]


def K_g(x, y):
    return float(K.ground(x, y))


def cam_state(g):
    r = K.cam_path(None, keys(), g)
    return r["loc"], r["look"], r["lens"], r["vivid"]


def pose_of(e, g):
    nm, cast, pname, mk, ph = e
    c, p = cast21.STORY21[pname]; p = dict(p)
    p["yaw"] = 0.3
    sh = math.sin(g * 0.09 + ph * 2.1)
    p["lean"] = p.get("lean", 0.0) + 2.4 * sh
    p["head_roll"] = p.get("head_roll", 0.0) + 2.0 * math.sin(g * 0.12 + ph)
    p["blink"] = cast21.blink_at(g, 92 + int(ph * 11), int(ph * 29))
    p["t"] = g / 30.0
    if nm in ("s1", "s3"):                       # shift the spear: the whole figure rocks a little more, the head follows
        p["lean"] += 3.0 * math.sin(g * 0.21 + ph)
    if nm == "s2":                               # leans on his spear: a steady lean into it
        p["lean"] = p.get("lean", 0.0) + 7.0 + 1.5 * math.sin(g * 0.07)
    return K.with_rim(p)


class Seg(object):
    def __init__(self):
        t0 = time.time()
        self.A = K.build_world(["camp_wide", "hill_low"], fg=["hill_low"], over=dict(shaft_k=1.0))
        self.scene = bpy.context.scene; self.cam = self.scene.camera; self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 2000
        self.acts = {}
        for ob in bpy.data.objects:                       # no fg spear shaft crossing the Scots' faces
            if ob.name.startswith(("fg_generic_steel", "fg_generic_wood")): ob.hide_render = True
        ph = p_hill(); pr2 = dict(cam=ph[0], look=ph[1], lens=22.0)      # stand points for the RAISED camera (heads at y ~ 650-740)
        self.marks = {}
        for mk, d, xp in (("s1", 8.2, 100), ("s2", 9.4, 250), ("horn", 7.8, 395), ("w", 10.5, 520), ("s3", 8.8, 640)):
            x, y = K.at_px(pr2, d, xp); self.marks[mk] = (x, y, float(K.ground(x, y)))
        for nm, cast, pname, mk, ph in STAND:
            self.acts[nm] = C.make_actor(nm, cast, os.path.join(TMP, "sprites"))
        print("B2: built world in %.1f s" % (time.time() - t0), flush=True)

    def plan(self, gs):
        cam = self.cam; self.viv = {}
        for g in gs:
            f = g + 1
            loc, look, lens, viv = cam_state(g); self.viv[g] = viv
            cam.location = loc; cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
            cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam.data.keyframe_insert("lens", frame=f)
            for nm, cast, pname, mk, ph in STAND:
                x, y, z = self.marks[mk][:3]
                self.acts[nm].place(f, (x, y, z), scale=C.SCALE.get(cast, C.CS))
        for g in gs:
            f = g + 1; self.scene.frame_set(f)
            for e in STAND:
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
        for nm, cast, pname, mk, ph in STAND:
            x, y, z = self.marks[mk][:3]; H = 1.7 if nm != "w" else 1.92
            px, py, dz = K.project(self.cam, (x, y, z + H * 0.9)); out[nm] = (round(px), round(py), round(dz, 1))
        return dict(g=g, cam=[round(v, 1) for v in self.cam.location], heads=out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "path":
        gs = list(range(G0, G1 + 1, 3)); out = sys.argv[2]
    else:
        gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
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
            dt = Tk.render_one(g, os.path.join(out, "b2_g_%04d.png" % g), mode, samples); print(json.dumps(Tk.report(g)), "%.1fs" % dt, flush=True)
    elif cmd == "final":
        samples = int(sys.argv[3]) if len(sys.argv) > 3 else 32
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png) and os.path.exists(png[:-4] + ".json"): continue
            dt = Tk.render_one(g, png, "final", samples); rep = Tk.report(g); rep.update(wall=round(dt, 1), samples=samples)
            json.dump(rep, open(png[:-4] + ".json", "w")); print("B2 g %d %.1f s" % (g, dt), flush=True)
