#!/usr/bin/env python3
"""char3d_b2.py -- B2 still of row 20 with the 3D toon cast (toon25 B2 build): the general waist-up pointing his stick, mouth talk_b,
in front of a calm grey-olive riveted plate (runtime set dressing, 1.6 D behind him) that takes his big dark cast shadow; the Tommy
behind his shoulder (like R11's painter); a separate small Tommy still.
    python3 char3d_b2.py draft|final   -> work/char3d_b2/<mode>/..., <mode>.json ; then char3d_post.py <mode> out.png b2"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c25 as C                                          # noqa: E402
import motion as M                                       # noqa: E402
import depth as D                                        # noqa: E402
from mathutils import Vector                             # noqa: E402
F, bpy = C.F, C.bpy
sys.path.insert(0, os.path.join(C.PROJ, "v3", "cast3d25"))
import toon25 as T                                       # noqa: E402
G = D.G
WORK = os.path.join(HERE, "work", "char3d_b2"); os.makedirs(WORK, exist_ok=True)
TURN = float(os.environ.get("TURN", "12"))               # + turns the general toward screen-right (his stick points there)
CAM_D, CAM_Z, LOOK_Z, LENS = float(os.environ.get("CAM_D", "4.8")), 2.6, 2.55, 45.0
PLATE_BACK = 1.6                                         # D behind him (about 0.85 m)
SUN_COL = (1.0, 0.98, 0.96)                              # less warm key: khaki stays khaki, not yellow


def plate(c, X, Y, w=18.0, h=8.0):
    """calm grey-olive riveted plate: X = along the plate (screen-right), Y = its normal toward the camera; c = bottom centre"""
    import bmesh
    M_ = T.mat_toon("plate", "#6b7887", 0.7, 0.0); Ms = T.mat_toon("plate_seam", "#535e6a", 0.6, 0.0); Mr = T.mat_toon("plate_rivet", "#7a8592", 0.45, 0.0)   # cool steel grey (R11-like): balances the warm khaki cast (frame b* <= 6)
    Z = Vector((0, 0, 1))
    def box(name, cen, hx, hy, hz, mat):
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=2.0)
        for v in bm.verts:
            v.co = cen + X * (v.co.x * hx) + Y * (v.co.y * hy) + Z * (v.co.z * hz)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
        ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob
    box("plate_main", c + Z * (h / 2), w / 2, 0.15, h / 2, M_)
    pw, ph = 2.8, 2.2
    rv = []
    for i in range(-3, 4):                                                    # vertical seams + rivet rows
        x = i * pw + 0.6
        box("seam_v%d" % i, c + X * x + Y * 0.17 + Z * (h / 2), 0.04, 0.03, h / 2, Ms)
        for k in range(int(h / 0.42)):
            for o in (-0.16, 0.16):
                rv.append(c + X * (x + o) + Y * 0.17 + Z * (0.2 + k * 0.42))
    for j in range(1, 4):                                                     # horizontal seams
        z = j * ph
        box("seam_h%d" % j, c + Y * 0.17 + Z * z, w / 2, 0.03, 0.04, Ms)
        for k in range(int(w / 0.42)):
            rv.append(c + X * (-w / 2 + k * 0.42) + Y * 0.17 + Z * (z + 0.16))
    bm = bmesh.new()
    for p in rv:
        r = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.065)
        for v in r["verts"]:
            v.co = Vector((v.co.x, v.co.y, v.co.z)) + p
    me = bpy.data.meshes.new("rivets"); bm.to_mesh(me); bm.free(); me.materials.append(Mr)
    ob = bpy.data.objects.new("rivets", me); bpy.context.scene.collection.objects.link(ob)
    for p_ in me.polygons:
        p_.use_smooth = True


class Take(C.Take):
    def __init__(self):
        C.F.OVR.update(haze=M.HAZE)
        C.Take.__init__(self, M.PRESET)
        H = F.S["tank"]; bpy.context.view_layer.update()
        w = H.root.matrix_world @ Vector((D.LOCAL[0], D.LOCAL[1], 0.0))
        self.feet = Vector((w.x, w.y, F.gh(w.x, w.y)))
        a = math.radians(F.S["mark"]["face_deg"])
        out = Vector((math.cos(a), math.sin(a), 0))                          # from the plate toward the camera
        right = Vector((math.cos(a + math.pi / 2), math.sin(a + math.pi / 2), 0))      # screen-right
        self.loc = self.feet + out * CAM_D + Vector((0, 0, CAM_Z))
        self.look = self.feet + Vector((0, 0, LOOK_Z)) + right * 0.35
        pc = self.feet - out * PLATE_BACK; pc.z = F.gh(pc.x, pc.y) - 0.3
        plate(pc, right, out)
        def kids(o):
            for c_ in o.children:
                yield c_; yield from kids(c_)
        for o in kids(H.root):                                                # the tank's sponson would poke through the near plate: hide the tank (the plate IS the hull here)
            o.hide_render = True
        F.S["sun"].data.angle = math.radians(0.5); F.S["sun"].data.energy = D.SUN_E; F.S["sun"].data.color = SUN_COL
        for n in bpy.context.scene.world.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = D.SKY_K
        self.gen = T.build_general("gen", stick_hand="l"); self.tom = T.build_tommy("tom")
        d = self.loc - self.feet
        self.gen.root.location = self.feet; self.gen.root.rotation_euler = (0, 0, math.atan2(d.x, -d.y) + math.radians(TURN))
        tp = self.feet - right * 0.95 - out * 1.15                               # the Tommy behind his (screen-left) shoulder
        tp.z = F.gh(tp.x, tp.y); self.tom.root.location = tp
        dt = self.loc - tp; self.tom.root.rotation_euler = (0, 0, math.atan2(dt.x, -dt.y) + math.radians(20))
        self.gen.set_pose("point_stick", shoulder_l=(30, 118, 0), elbow_l=(10, 0, 0), shoulder_r=(-10, 30, 0), elbow_r=(0, -85, 0))   # stick in the screen-right hand, other fist on the hip; self.gen.set_mouth("talk_b")
        self.tom.set_pose("stand", shoulder_r=(15, 10, 0), elbow_r=(70, 0, 0), shoulder_l=(0, 12, 0)); self.tom.set_mouth("flat")
        self.gen.look_at(self.loc); self.tom.look_at(self.loc)
        self.chars = [o for o in bpy.data.objects if o.name.startswith(("gen_", "tom_"))]
        self.key_cam(G, self.loc, self.look, LENS)
        self.scene.frame_set(G)
        D.Take.aim_sun(self, self.loc, self.look)
        dof = self.cam.data.dof; dof.use_dof = True; dof.aperture_fstop = 2.8; dof.focus_distance = (self.loc - self.feet - Vector((0, 0, 2.3))).length

    def on_frame(self, f):
        D.Take.aim_sun(self, self.loc, self.look)

    def mask_pass(self, scale, tag):
        hide = [o for o in bpy.data.objects if o.type in ("MESH", "CURVE") and o not in self.chars and not o.hide_render]
        for o in hide:
            o.visible_camera = False
        sc = self.scene; sc.render.film_transparent = True; sc.cycles.samples = 4; dof = self.cam.data.dof.use_dof; self.cam.data.dof.use_dof = False
        sc.render.resolution_percentage = int(scale * 100); out = os.path.join(WORK, "mask_%s.png" % tag)
        sc.render.filepath = out; bpy.ops.render.render(write_still=True)
        for o in hide:
            o.visible_camera = True
        sc.render.film_transparent = False; self.cam.data.dof.use_dof = dof
        return out


def head_info(Tk, ch):
    from bpy_extras.object_utils import world_to_camera_view
    hc = world_to_camera_view(Tk.scene, Tk.cam, ch.head.matrix_world.translation)
    he = world_to_camera_view(Tk.scene, Tk.cam, ch.head.matrix_world.translation + Tk.cam.matrix_world.to_3x3() @ Vector((0.5, 0, 0)))
    return [hc.x * 720, (1 - hc.y) * 1280], abs(he.x - hc.x) * 720 * 2


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "draft"
    scale, samples, thr = (0.4, 12, 0.05) if mode == "draft" else (1.0, 64, 0.012)
    Tk = Take()
    st = Tk.render([G], os.path.join(WORK, mode), scale=scale, samples=samples, threshold=thr)[0]
    mk = Tk.mask_pass(scale, mode)
    hp, hw = head_info(Tk, Tk.gen)
    rep = dict(mode=mode, beauty_raw=os.path.join(WORK, mode, "raw", "f_%04d.png" % G), mask=mk, wall=round(st["wall"], 1), head_px=hp, head_w_px=hw, turn=TURN)
    # separate small Tommy still (full figure), general hidden
    for o in Tk.chars:
        if o.name.startswith("gen_"):
            o.hide_render = True
    tp = Tk.tom.root.matrix_world.translation; ya = Tk.tom.root.rotation_euler.z
    fwd = Vector((math.sin(ya), -math.cos(ya), 0))
    Tk.loc, Tk.look = tp + fwd * 6.0 + Vector((0, 0, 1.9)), tp + Vector((0, 0, 1.65)); Tk.key_cam(G, Tk.loc, Tk.look, 40.0)
    Tk.tom.look_at(Tk.loc); Tk.cam.data.dof.use_dof = False
    st2 = Tk.render([G], os.path.join(WORK, mode + "_tommy"), scale=scale, samples=samples, threshold=thr)[0]
    mk2 = Tk.mask_pass(scale, mode + "_tommy")
    hp2, hw2 = head_info(Tk, Tk.tom)
    rep["tommy"] = dict(beauty_raw=os.path.join(WORK, mode + "_tommy", "raw", "f_%04d.png" % G), mask=mk2, head_px=hp2, head_w_px=hw2)
    json.dump(rep, open(os.path.join(WORK, mode + ".json"), "w"))
    print(json.dumps(rep), flush=True)
