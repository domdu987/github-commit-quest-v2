#!/usr/bin/env python3
"""shot.py -- film 21 segment H2a (plan v3), g 1345..1392 (D6 in) + 3 handle frames before (1342-1344: H1's move continued into P_NECK) and 3 after (1393-1395: the
drift continued).  World K.build_world(['bridge_end_north','valley_loop']).  Starts EXACTLY at K.POSES['P_NECK'] (g 1345), CRANES up fast (~1 s) while backing south
to K.POSES['P_TOP'] (g 1392) and hold-drifts: the bottle-and-cork image (English in crimson boxed in the loop, the Scots spear wall with blue saltire banners at the
bridge mouth, the other half waiting on the south bank).
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [draft|final] [samples] | final a:b[:step] [samples] [threads]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C                                              # noqa: E402
import numpy as np                                           # noqa: E402
from mathutils import Vector                                 # noqa: E402
K, bpy, cast21, actors, sprites = C.K, C.bpy, C.cast21, C.actors, C.sprites
TMP = os.path.join(HERE, 'work')
G_A, G_B = 1345, 1392                                        # P_NECK / P_TOP
G0, G1 = 1342, 1395
NECK, TOP = K.POSES["P_NECK"], K.POSES["P_TOP"]
KEYS = [(1342, (-2.3, 53.0, 5.6), (0.0, 22.0, 1.9), 22.0),        # H1 move continued into P_NECK (descending toward the bridge mouth)
        (G_A,) + NECK,
        (1356, (-3.5, 38.0, 34.0), (0.0, 30.0, 1.0), 22.0),       # the crane: straight up, fast
        (1366, (-6.0, 4.0, 82.0), (0.0, 55.0, 0.0), 22.0),
        (G_B,) + TOP,
        (1400, (-11.2, -44.0, 123.0), (0.0, 81.0, 0.0), 22.0)]    # the drift continues past the join
def cam_at(g): return K.cam_path(None, KEYS, g)

def _hm(cast, pose_name, hm):
    """metres per head-D for a cast card: standing height hm / (feet - head_top) of the drawing."""
    p = cast21.STORY21[pose_name][1]; a = sprites.sprite_svg(cast, p, 64)[1]["anchors"]
    return hm / (a["feet"][1] - a["head_top"][1])

class Take(object):
    def __init__(self):
        self.A = K.build_world(["bridge_end_north", "valley_loop"])
        for o in [o for o in bpy.data.objects if o.name.startswith(("crowd_", "spear_wall", "troops_causeway"))]: bpy.data.objects.remove(o, do_unlink=True)
        # the army: meadow rows only BEHIND the camera start (y >= 60: nobody at the lens), the half on the south bank, the rest of the column on the bridge
        items = K.place_troops(self.A, "meadow", 280, seed=1, cb=lambda it: None)
        mead = [it for it in items if it[1] >= 60.0]
        K.stage_crowd(mead, cam=bpy.context.scene.camera)
        K.place_troops(self.A, "south", 45, seed=2)
        K.place_troops(self.A, "bridge", 10, seed=1)
        self.cam = bpy.context.scene.camera; self.cam.data.dof.use_dof = False; self.cam.data.clip_end = 9000
        # cast: the 12 English on the causeway (stunned, helmets wobbling) and the Scots spear wall (two ranks, blue saltire banners built by the set)
        cz = K.place_troops(self.A, "causeway", 12, seed=3, cb=lambda it: None)
        self.eng = []
        for i, (x, y, z, kind, sc) in enumerate(cz):
            cast = ("footman_a", "footman_b")[i % 2]
            self.eng.append((C.make_actor("en%d" % i, cast, os.path.join(TMP, "sprites")), cast, (x, y, z), _hm(cast, cast + "_worried", 1.68)))
        self.scots = []
        n = 0
        for rank in range(2):
            for k in range(14):
                x = -9.0 + 18.0 * k / 13.0 + (0.6 if rank else 0.0); y = 27.0 + 1.1 * rank; cast = ("scot_a", "scot_b", "scot_c")[(k + rank) % 3]
                self.scots.append((C.make_actor("sc%d" % n, cast, os.path.join(TMP, "sprites")), cast, (x, y, float(K.ground(x, y))), _hm(cast, cast + "_spear_wall", 1.70), n)); n += 1
    def pose_en(self, i, cast, g):
        p = dict(cast21.STORY21[cast + ("_bump" if (g + 7 * i) % 40 < 7 else "_worried")][1])
        p["head_roll"] = p.get("head_roll", 0) + 5.0 * math.sin(g * 0.45 + i); p["lean"] = 2.0 * math.sin(g * 0.3 + 1.7 * i)
        p["blink"] = C.blink(g, [1350 + 9 * i % 40, 1380 + 5 * i % 30]); return K.with_rim(p)
    def pose_sc(self, n, cast, g):
        p = dict(cast21.STORY21[cast + "_spear_wall"][1]); p["lean"] = 1.5 * math.sin(g * 0.2 + n); p["head_roll"] = 2.0 * math.sin(g * 0.13 + n)
        p["blink"] = C.blink(g, [1350 + 11 * n % 37, 1382 + 3 * n % 20]); return K.with_rim(p)
    def key(self, gs):
        for g in gs:
            r = cam_at(g); C.key_cam(self.cam, g, r["loc"], r["look"])
        allc = [(a, c, xyz, hm, 128, "en") for (a, c, xyz, hm) in self.eng] + [(a, c, xyz, hm, 128, n) for (a, c, xyz, hm, n) in self.scots]
        for (a, c, xyz, hm, ppd, n) in allc:
            for g in gs: a.place(C.bf(g), xyz, scale=hm)
        for g in gs:
            f = C.bf(g); bpy.context.scene.frame_set(f)
            for i, (a, c, xyz, hm) in enumerate(self.eng): a.pose(f, self.pose_en(i, c, g), camera=self.cam)
            for (a, c, xyz, hm, n) in self.scots: a.pose(f, self.pose_sc(n, c, g), camera=self.cam)
        for (a, c, xyz, hm, ppd, n) in allc: a.render_sprites(ppd, frames=[C.bf(g) for g in gs])
    def hooks(self, g):
        t = g / 30.0; K.set_flow(t); K.set_smoke(t); K.set_flutter(t)
    def render(self, g, out, mode="draft", samples=None, threads=2):
        sc = bpy.context.scene; sc.frame_set(C.bf(g)); self.hooks(g); r = cam_at(g)
        for a in actors.REGISTRY: a.sync(self.cam, sc)
        sc.camera = self.cam; K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.cycles.denoising_prefilter = "FAST"
        return K.render(out, mode, samples)
if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    if cmd == "probe":
        Tk = Take()
        for g in gs: r = cam_at(g); print(g, [round(v, 1) for v in r["loc"]], [round(v, 1) for v in r["look"]], [round(v, 2) for v in r["vivid"]])
    else:
        Tk = Take(); Tk.key(gs)
        if cmd == "stills":
            out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"; smp = int(sys.argv[5]) if len(sys.argv) > 5 else None
            os.makedirs(out, exist_ok=True)
            for g in gs: print("g", g, "%.1fs" % Tk.render(g, os.path.join(out, "g_%04d.png" % g), mode, smp), flush=True)
        elif cmd == "final":
            smp = int(sys.argv[3]) if len(sys.argv) > 3 else 32; th = int(sys.argv[4]) if len(sys.argv) > 4 else 2
            out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
            for g in gs:
                png = os.path.join(out, "g_%04d.png" % g)
                if os.path.exists(png + ".ok"): continue
                dt = Tk.render(g, png, "final", smp, th); open(png + ".ok", "w").write("%d %.1f" % (smp, dt)); print("g", g, "%.1fs" % dt, flush=True)
