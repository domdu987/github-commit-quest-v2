#!/usr/bin/env python3
"""shot_C.py -- film 24 version C take s08C: the build-up, preset build_dock (yard slipway at dusk), g 734..1125 (g1 = 1126 exclusive)
+ 6 handle frames each side (728..1131).  No cast.  J.set_build_g(g, f) every frame, camera J.build_cam((g-734)/392), build_anchors.json.
Blender frame = 7000 + g + 1.    JOSEON_LOOK=C python3 shot_C.py probe a:b[:s] | stills a:b[:s] <out> [scale] [samples] | final a:b [scale] [samples] | anchors
"""
import os, sys, json, math
os.environ.setdefault("JOSEON_LOOK", "C")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
J = C.J
G0, G1, H = 734, 1127, 6                                 # g1 exclusive (s09 starts at 1127)
RANGES = {8: (G0 - H, G1 + H - 1)}
U_SPAN = 392.0                                            # camera u = (g - 734) / 392 (unchanged path)
# word-locked stage windows (director: each part LOCKS on its narration word): keel slam 785, ribs locked 795, planks 807, oars 836, guns 869-885,
# roof 912, spikes ~930/939/948, gwimyeon 980, dragon 1009, mouth-gun flash ~1043, hero from 1109
J.BUILD_G[:] = [('0', 734, 780), ('1', 781, 807), ('2', 808, 836), ('3', 837, 885), ('4', 886, 921), ('5', 922, 952), ('6a', 953, 1004),
                ('6b', 1005, 1019), ('6c', 1020, 1108), ('7', 1109, 1126)]
G_ROOF, G_DRAG = 912, 1009
SHOT = 8


def bfr(g):
    return C.bf(SHOT, g)


def cam_at(g):
    """J.build_cam, tightened a little on stages 2 (oars) and 3 (guns); plus an intro slide (g < 806, decaying to 0) so the slow-easing start of the orbit is never static;
    the in-handle (g < 734) is the same slide continued."""
    from mathutils import Vector
    c = dict(J.build_cam(max(0.0, (g - G0) / U_SPAN)))
    w = C.ez((g - 815) / 15.0) * (1.0 - C.ez((g - 888) / 15.0))
    loc, look = Vector(c["loc"]), Vector(c["look_at"])
    loc = loc + (look - loc) * (0.18 * w)
    r = (look - loc).cross(Vector((0, 0, 1))); r.z = 0; r.normalize()
    slide = 2.4 * (1.0 - math.sin(math.pi / 2 * min(1.0, (g - 728) / 78.0))) if g < 806 else 0.0         # D, toward the camera's left at the start, ending at the nominal camera
    c["loc"] = tuple(loc - r * slide); c["look_at"] = tuple(look - r * slide)
    return c


BASE_OAR_PITCH = -26.0                                    # deg: deployed oars dip down and out toward the water (the yard rig tilts them UP by +12)
GUN_SCALE = 1.8


def _sl(u):
    return J._slam(u)


class Take(C.Take):
    def __init__(self, shot=8):
        C.Take.__init__(self, "build_dock", name="cam_s08C")
        if J.LOOK != "C":
            J.set_look("C")
        import bpy
        from mathutils import Vector, Matrix
        for o in bpy.data.objects:                       # director note: the rigging gobos cast a thin dark vertical shaft through the haze above the ship
            if o.name.startswith("gobo_rig"):
                o.visible_shadow = False
        self.B = B = J._build_rig(); sh = self.sh = J.S["turtle"]; M_ = J.S["M"]; ride = sh["ride"]; K = J.K
        K.use(J.S["coll"])
        # keel on the hull bottom (local z -1.5..-0.95) instead of floating 2 D above it
        mb = K.MB(); mb.beam((-16.0, 0, -1.22), (17.2, 0, -1.22), 0.7, 0.55, M_["wood_d"])
        tmp = K.obj(mb, "fix_keel_tmp", ride); B["keel"].data = tmp.data; bpy.data.objects.remove(tmp)
        # ribs: a proper U round the keel (the stock profile starts at its centre 1.45 high = a bow-tie zig-zag), bottom point touches the keel top
        prof = [(0.0, -0.95), (0.42, -0.9), (0.8, -0.35), (0.965, 0.65), (1.0, 1.55), (1.012, 2.2), (0.995, 2.45)]
        for i, r_ in enumerate(B["ribs"]):
            x = -14.0 + 2.0 * i; b = J.t_b(x) * 0.97; mb = K.MB()
            pts = [Vector((x, -f * b, z)) for f, z in reversed(prof)] + [Vector((x, f * b, z)) for f, z in prof[1:]]
            for a_, b_ in zip(pts[:-1], pts[1:]):
                mb.beam(a_, b_, 0.22, 0.26, M_["wood_d"])
            tmp = K.obj(mb, "fix_rib_tmp", ride); r_.data = tmp.data; bpy.data.objects.remove(tmp)
        # keel blocks: a row on the slipway under the keel (local z -2.39 slipway .. -1.5 keel bottom), visible from the start
        blocks = K.MB()
        for x in [-15.0 + 3.0 * k for k in range(11)]:
            blocks.box((x, 0, -1.95), 0.55, 0.75, 0.46, M_["wood_d"])
        self.blocks = K.obj(blocks, "fix_keel_blocks", ride)
        self.eave = [o for o in B["hull"] if o.name.endswith("_eave")]
        base = {k_: (Vector(v[0]), None if v[1] is None else Vector(v[1])) for k_, v in B["base"].items()}
        for o in sh["oars"]:                              # deployed pose: dip outward and down
            i = int(o.name.split("_")[-2]); sg = 1 if o.name.endswith("_p") else -1
            o.rotation_euler = (math.radians(BASE_OAR_PITCH), 0, 0 if sg > 0 else math.pi)
            B["base"][o.name] = (Vector(o.location), Vector(o.rotation_euler))
        for mz, sg in B["guns"]:
            mz.scale = (GUN_SCALE,) * 3
        # iron barrels readable in the backlit shade: dark steel with a faint warm edge glow, and a bronze muzzle ring
        iron = bpy.data.materials["J_cannon"]; pb = [n for n in iron.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
        pb.inputs["Base Color"].default_value = (0.04, 0.045, 0.055, 1); pb.inputs["Metallic"].default_value = 0.15; pb.inputs["Roughness"].default_value = 0.6
        for nm in ("Emission Color", "Emission"):
            if nm in pb.inputs:
                pb.inputs[nm].default_value = (0.9, 0.5, 0.25, 1); break
        if "Emission Strength" in pb.inputs:
            pb.inputs["Emission Strength"].default_value = 0.0
        bronze = bpy.data.materials.new("J_bronze"); bronze.use_nodes = True
        bp = [n for n in bronze.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
        bp.inputs["Base Color"].default_value = (0.55, 0.32, 0.09, 1); bp.inputs["Metallic"].default_value = 0.9; bp.inputs["Roughness"].default_value = 0.3
        import bmesh
        for d in {mz.data for mz, sg in B["guns"]}:
            d.materials.append(bronze); mi = len(d.materials) - 1
            bm = bmesh.new(); bm.from_mesh(d)
            n0 = len(bm.faces)
            bmesh.ops.create_cone(bm, cap_ends=False, segments=16, radius1=0.47, radius2=0.47, depth=0.18,
                                  matrix=Matrix.Translation((0, 0.66, 0)) @ Matrix.Rotation(math.pi / 2, 4, "X"))
            for fc in list(bm.faces)[n0:]:
                fc.material_index = mi
            bm.to_mesh(d); bm.free()

    def fixes(self, g, f):
        """called after J.set_build_g(g, f): the word-locked / readable parts (oars, gun barrels, roof, eave, dragon) are keyed here (later key wins)."""
        import bpy
        from mathutils import Vector, Matrix
        B, sh, J_ = self.B, self.sh, J
        base = B["base"]
        # oars: ripple out bow -> stern from 808, all locked by 836 (10 frames of glide each, 2 frames apart); they stay out
        n = len(sh["oars"]) // 2
        for o in sh["oars"]:
            i = int(o.name.split("_")[-2]); rank = (n - 1) - i
            u = max(0.0, min(1.0, (g - (808 + 2 * rank)) / 10.0)); lo, ro = base[o.name]
            ax = Matrix.Rotation(ro.z, 3, "Z") @ Matrix.Rotation(ro.x, 3, "X") @ Vector((0, 1, 0))
            J_._bk(o, f, loc=lo - ax * 5.8 * (1.0 - J_._ez(u)), rot=ro, vis=u > 0.0)
        # guns: the barrels (x1.8) slide out bow -> stern, first locks 869, last ~885; a glint as each seats; they stay
        ng = len(B["guns"]) // 2
        for j, ((mz, sg), gl) in enumerate(zip(B["guns"], B["glints"])):
            i = j // 2; rank = (ng - 1) - i; lock = 869 + 1.6 * rank
            u = max(0.0, min(1.0, (g - (lock - 8)) / 8.0)); lo = Vector(base[mz.name][0])
            J_._bk(mz, f, loc=lo - Vector((0, sg * 2.9 * (1.0 - J_._ez(u)), 0)), vis=u > 0.0)
            mz.scale = (GUN_SCALE,) * 3; J_.key_attr(mz, "scale", f)
            J_.show(gl, lock - 1 <= g <= lock + 3, f)
        # keel dust at the new keel height, roof and eave land on the word "หลังคา" (g 912), posts / eave hidden until the roof drops
        J_._dust(B, "keel", Vector((2.0, 0, -1.1)), (g - 785) / 30.0, f, 2.0)
        u = (g - (G_ROOF - 14)) / 14.0 * 0.7 if g < G_ROOF else 1.0
        off = _sl(max(0.0, min(1.0, u))) if g >= G_ROOF - 14 else 1.0
        for o in B["roof"] + self.eave:
            lo = Vector(base[o.name][0]); J_._bk(o, f, loc=lo + Vector((0, 0, 4.5 * off)), vis=g >= G_ROOF - 14)
        for i, x in enumerate((-10.0, -2.0, 6.0)):
            for sg in (-1, 1):
                J_._dust(B, "eave%d%d" % (i, sg), Vector((x, sg * J_.t_ye(x), J_.Z_EAVE)), (g - G_ROOF) / 30.0, f, 1.2)
        # dragon head: bolts on, locks on the word "หัวมังกร" (g 1009), jaw opens after, eyes glint at the lock
        u = (g - (G_DRAG - 15)) / 15.0 * 0.7 if g < G_DRAG else 1.0
        off = _sl(max(0.0, min(1.0, u))); vis = g >= G_DRAG - 15
        for o in sh["dragonC"]:
            if o is sh["jaw"]:
                continue
            J_._bk(o, f, loc=Vector(base[o.name][0]) + Vector((3.5 * off, 0, 2.0 * off)), vis=vis)
        jo = max(0.0, min(1.0, (g - (G_DRAG + 4)) / 14.0)); jaw = sh["jaw"]
        J_._bk(jaw, f, loc=Vector(base[jaw.name][0]) + Vector((3.5 * off, 0, 2.0 * off)), rot=(0, -math.radians(14) * (1 - J_._ez(jo)), 0), vis=vis)
        if B["jaw_lteeth"] is not None:
            J_.show(B["jaw_lteeth"], vis, f)
        J_.K._setv(bpy.data.materials["K_e_eyeglint"], "k", 40.0 * (1.0 + 6.0 * max(0.0, 1 - abs(g - (G_DRAG + 3)) / 8.0)), f)
        J_._dust(B, "head", Vector((18.0, 0, 2.6)), (g - G_DRAG) / 30.0, f, 1.0)

    def pose(self, shot, gs):
        self.stage = {}
        for g in gs:
            f = bfr(g); self.scene.frame_set(f)
            c = cam_at(g)
            self.key_cam(f, c["loc"], c["look_at"], lens=c["lens"])
            self.key_set(f, spikes=None, ports=None, dragon_smoke=0.0)
            self.stage[g] = J.set_build_g(g, f)[0]
            self.fixes(g, f)

    def anchor(self, g):
        f = bfr(g); self.scene.frame_set(f); self.scene.camera = self.cam
        a = J.build_anchor(self.stage[g] if g in self.stage else J.build_at(g)[0])
        return dict(g=g, stage=J.build_at(g)[0], x=None if a is None else a[0], y=None if a is None else a[1])

    def report(self, shot, g):
        f = bfr(g); self.scene.frame_set(f); c = cam_at(g)
        return dict(shot=8, g=g, cam=[round(v, 3) for v in c["loc"]], lens=c["lens"], stage=J.build_at(g)[0], anchor=self.anchor(g))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bfr(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if RANGES[8][0] <= g <= RANGES[8][1]]
        Tk = Take(); Tk.pose(8, gs)
        for g in gs:
            print(json.dumps(Tk.report(8, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                os.makedirs(out, exist_ok=True)
                st = Tk.render(8, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s8_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        C.final_loop(lambda s_: Take(), [8], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
