#!/usr/bin/env python3
"""shot.py -- film 13 take s24: shot 24 (aha wide), g 1537..1602 + 6 handle frames each side (1531..1608). DAY, lift 0.9.
Side-on wide of the hotel high on its cribbing (copy of team7's shot-28 camera idea, front_stair build, stair cut short with void);
6-8 tiny cast13 workers stand INSIDE the gap among the cribbing (one cheers). No machine, no lamp halos.
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]   |   python3 shot.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C
from mathutils import Vector
B, bpy, camrig, cast13 = C.B, C.bpy, C.camrig, C.cast13
lerp, clamp, ez = C.lerp, C.clamp, C.ez
S13 = cast13.STORY13
SHOT = 24
G0, G1 = C.g_bound(51.13), C.g_bound(53.30) - 1 + 1          # filled below
G0 = C.g_of(51.13); G1 = C.g_of(53.30) - 1
H = 6
RANGE = (G0 - H, G1 + H)
LIFT_H = 0.9
LENS = float(os.environ.get("S24_LENS", "15"))
CAM0 = eval(os.environ.get("S24_CAM0", "((0.0,-14.0,4.9),(0.0,0.0,4.9))"))
CAM1 = eval(os.environ.get("S24_CAM1", "((0.0,-15.0,5.4),(0.0,0.0,5.4))"))
LIFT = B.LIFT_MAX * LIFT_H

def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0])); u = 0.3 * ez(x) + 0.7 * x
    return [Vector([lerp(CAM0[k][i], CAM1[k][i], u) for i in range(3)]) for k in (0, 1)]

def cut_stair():
    import bmesh
    st = bpy.data.objects["stair"]; bm = bmesh.new(); bm.from_mesh(st.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -6.2], context="VERTS"); bm.to_mesh(st.data); bm.free()
    for n in ("puddles", "scum"):
        if n in bpy.data.objects: bpy.data.objects[n].hide_render = True

def swap_cast():
    T = B.T; P = lambda k: dict(S13[k][1])
    for s in "abc":
        T.PH["ws_" + s] = ("worker13_" + s, dict(P("worker_stand_" + s), expr="neutral", mouth="smile"), 3.2)
        T.PH["wc_" + s] = ("worker13_" + s, dict(P("worker_cheer_" + s), expr="neutral", mouth="smile"), 3.2)
    T.PH.update(worker=("worker13_a", P("worker_stand_a"), 3.2), foreman=("foreman13", P("foreman_stand"), 3.3), rich=("rich", P("rich_look_window_smug"), 3.4),
        maid=("town_b", P("town_stand_b"), 3.0), clerk=("worker13_b", P("worker_stand_b"), 3.2), kid=("town_c", P("town_stand_c"), 2.5),
        towns_m=("town_a", P("town_stand_a"), 3.2), towns_f=("town_b", P("town_stand_b"), 3.0), towns_o=("worker13_c", P("worker_stand_c"), 3.1))

# workers: (x, y, kind, scale)  inside the gap, in front of the first jack row (y 1.3), between crib piers
WORKERS = eval(os.environ.get("S24_WORKERS", "[(-8.00,-1.2,'ws_a',0.92),(-5.70,-0.6,'wc_c',0.92),(-3.40,-1.2,'ws_b',0.92),(-1.10,-0.6,'ws_c',0.92),(1.20,-1.2,'wc_b',0.92),(3.50,-0.6,'ws_a',0.92),(5.80,-1.2,'ws_b',0.92),(8.10,-0.6,'ws_c',0.92)]"))

class Take(object):
    def __init__(self, quality="preview"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        swap_cast()
        self.A = B.build("front_stair", light="DAY", state="lift%s" % LIFT_H)
        B.clear_keys()
        B.setup_render(scene, quality); cut_stair()
        scene.cycles.denoising_prefilter = "FAST"; scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name="cam_s24", lens=LENS)
        self.cam.data.clip_start, self.cam.data.clip_end = 0.05, 6000; self.cam.data.dof.use_dof = False
        scene.camera = self.cam
        self.hide_halos()
        gz = B._gnd()
        self.cards = []
        for i, (x, y, k, s) in enumerate(WORKERS):
            self.cards += B.crowd(1, None, seed=i, kinds=[k], ground=0.0, points=[(x, y)], scale=(s, s))
        # distant townsfolk on the street (tiny)
        self.cards += B.crowd(8, [(-30, 30, -40, -22)], seed=5, kinds=['towns_m', 'towns_f', 'towns_o', 'maid'], ground=gz, min_dist=5.0, scale=(0.95, 1.05))

    def hide_halos(self):
        for ob in list(bpy.data.objects):
            n = ob.name.lower()
            if "halo" in n or "glow" in n or "lamp" in n and "halo" in n:
                ob.hide_render = True
        for n in ("lamps_glass", "street_furniture", "under_lamps", "street_planks", "street_props", "pile_a", "pile_b", "pile_c", "pile_d", "pile_e", "mound_side"):
            if n in bpy.data.objects: bpy.data.objects[n].hide_render = True
        for ob in bpy.data.objects:
            if ob.name.startswith("L_gap"): ob.data.energy *= float(os.environ.get("S24_GAPE", "0.3"))

    def pose(self, gs):
        for g in gs:
            f = C.bf(SHOT, g); loc, look = cam_of(g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
            B.set_lift(LIFT_H, frame=f)

    def report(self, g):
        loc, look = cam_of(g); return dict(shot=SHOT, g=g, cam=[round(c, 2) for c in loc])

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam; self.cam.data.dof.use_dof = False; self.scene.cycles.samples = samples
        import render
        return render.render_frames([C.bf(SHOT, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "stills":
        out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s24_g_%04d.png" % g)); print(g, "%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), sys.argv[2], RANGE, HERE, SHOT, scale=scale, samples=samples)
