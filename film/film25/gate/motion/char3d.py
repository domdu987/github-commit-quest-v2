#!/usr/bin/env python3
"""char3d.py -- ONE still of row 20 with the 3D toon cast (v3/cast3d25/toon25.py): general25 waist-up pointing his stick at the
tank, mouth talk_b, 2 D in front of the plain riveted side plate (his cast shadow on it); tommy_a25 small in the background.
    python3 char3d.py draft|final        -> work/char3d/<mode>/ (beauty raw + mask raw) + <mode>.json
Then char3d_post.py grades the background only (post25 gentle grade) and leaves the characters ungraded (mask pass)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c25 as C                                          # noqa: E402
import motion as M                                       # noqa: E402
import depth as D                                        # noqa: E402  (same mark, camera and sun recipe as the depth still)
from mathutils import Vector                             # noqa: E402
F, bpy = C.F, C.bpy
sys.path.insert(0, os.path.join(C.PROJ, "v3", "cast3d25"))
import toon25 as T                                       # noqa: E402
G = D.G
WORK = os.path.join(HERE, "work", "char3d"); os.makedirs(WORK, exist_ok=True)
TURN = float(os.environ.get("TURN", "40"))              # deg: + turns him toward screen-left (his stick arm, the right, extends to screen-left)
CAM_D, CAM_Z, LOOK_Z, LENS = 6.4, 2.6, 2.3, 45.0


class Take(C.Take):
    def __init__(self):
        C.F.OVR.update(haze=M.HAZE)
        C.Take.__init__(self, M.PRESET)
        H = F.S["tank"]; bpy.context.view_layer.update()
        w = H.root.matrix_world @ Vector((D.LOCAL[0], D.LOCAL[1], 0.0))
        self.feet = Vector((w.x, w.y, F.gh(w.x, w.y)))
        a = math.radians(F.S["mark"]["face_deg"])
        right = Vector((math.cos(a + math.pi / 2), math.sin(a + math.pi / 2), 0))      # screen-RIGHT direction seen from the camera
        self.loc = Vector((w.x + math.cos(a) * CAM_D, w.y + math.sin(a) * CAM_D, self.feet.z + CAM_Z))
        self.look = Vector((w.x, w.y, self.feet.z + LOOK_Z)) + right * 0.45
        F.S["sun"].data.angle = math.radians(0.5); F.S["sun"].data.energy = D.SUN_E
        for n in bpy.context.scene.world.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = D.SKY_K
        import tank25 as TK
        TK.set_stencil(H, 0)
        # characters
        self.gen = T.build_general("gen"); self.tom = T.build_tommy("tom")
        d = self.loc - self.feet
        yaw = math.atan2(d.x, -d.y)
        self.gen.root.location = self.feet; self.gen.root.rotation_euler = (0, 0, yaw + math.radians(TURN))
        tp = self.feet + right * 2.5 + Vector((math.cos(a), math.sin(a), 0)) * -0.4         # Tommy: off to screen-left, a step nearer the plate
        tp.z = F.gh(tp.x, tp.y); self.tom.root.location = tp
        dt = self.loc - tp; self.tom.root.rotation_euler = (0, 0, math.atan2(dt.x, -dt.y) + math.radians(25))
        self.gen.set_pose("point_stick", shoulder_r=(62, 8, 0), elbow_r=(30, 0, 0), shoulder_l=(-10, 35, 0), elbow_l=(0, -85, 0)); self.gen.set_mouth("talk_b")
        self.tom.set_pose("stand", shoulder_r=(10, 12, 0), elbow_r=(60, 0, 0)); self.tom.set_mouth("talk_o")
        self.chars = [o for o in bpy.data.objects if o.name.startswith(("gen_", "tom_"))]
        for o in self.chars:
            o.pass_index = 7
        self.key_cam(G, self.loc, self.look, LENS)
        self.scene.frame_set(G)
        D.Take.aim_sun(self, self.loc, self.look)
        dof = self.cam.data.dof; dof.use_dof = True; dof.aperture_fstop = 2.2; dof.focus_distance = (self.loc - self.feet - Vector((0, 0, 2.3))).length

    def on_frame(self, f):
        D.Take.aim_sun(self, self.loc, self.look)

    def mask_pass(self, scale):
        """characters only, film transparent: alpha = character mask (for the ungraded composite)"""
        hide = [o for o in bpy.data.objects if o.type in ("MESH", "CURVE") and o not in self.chars and not o.hide_render]
        for o in hide:
            o.visible_camera = False
        sc = self.scene; sc.render.film_transparent = True; sc.cycles.samples = 4; self.cam.data.dof.use_dof = False
        sc.render.resolution_percentage = int(scale * 100); out = os.path.join(WORK, "mask_%d.png" % int(scale * 100))
        sc.render.filepath = out; bpy.ops.render.render(write_still=True)
        for o in hide:
            o.visible_camera = True
        sc.render.film_transparent = False; self.cam.data.dof.use_dof = True
        return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "draft"
    scale, samples, thr = (0.4, 12, 0.05) if mode == "draft" else (1.0, 64, 0.012)
    Tk = Take()
    toms = [o for o in Tk.chars if o.name.startswith("tom_")]
    for o in toms:                                                            # main still: the general alone (the Tommy gets his own still below)
        o.hide_render = True
    st = Tk.render([G], os.path.join(WORK, mode), scale=scale, samples=samples, threshold=thr)[0]
    mk = Tk.mask_pass(scale)
    from bpy_extras.object_utils import world_to_camera_view
    hc = world_to_camera_view(Tk.scene, Tk.cam, Tk.gen.head.matrix_world.translation)
    he = world_to_camera_view(Tk.scene, Tk.cam, Tk.gen.head.matrix_world @ Vector((0.5, 0, 0)))
    rep = dict(mode=mode, beauty_raw=os.path.join(WORK, mode, "raw", "f_%04d.png" % G), mask=mk, wall=round(st["wall"], 1),
               head_px=[hc.x * 720, (1 - hc.y) * 1280], head_w_px=abs(he.x - hc.x) * 720 * 2, turn=TURN)
    # a second small still of the Tommy model (full figure, same light): camera 6 D in front of him
    tp = Tk.tom.root.matrix_world.translation; ya = Tk.tom.root.rotation_euler.z
    fwd = Vector((math.sin(ya), -math.cos(ya), 0))                                      # his facing (-Y local)
    tl = tp + fwd * 6.5 + Vector((0, 0, 1.9)); tk = tp + Vector((0, 0, 1.6))
    for o in toms:
        o.hide_render = False
    Tk.gen.root.hide_render = True
    for o in Tk.chars:
        if o.name.startswith("gen_"):
            o.hide_render = True
    Tk.loc, Tk.look = tl, tk; Tk.key_cam(G, tl, tk, 40.0); Tk.cam.data.dof.use_dof = False
    st2 = Tk.render([G], os.path.join(WORK, mode + "_tommy"), scale=scale, samples=samples, threshold=thr)[0]
    rep["tommy_still"] = st2["path"]
    json.dump(rep, open(os.path.join(WORK, mode + ".json"), "w"))
    print(json.dumps(rep), flush=True)
