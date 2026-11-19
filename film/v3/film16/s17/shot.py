#!/usr/bin/env python3
"""shot.py -- film 16 take s17 = shot 17 (LINE line_trench_end / DUSK): Morse turns out the empty money bag, two workers lean on shovels.
Shot g 1075..1118 (35.82-37.30 s), handles 9 f each side (g 1066..1127).  Hard cuts.  No mouths (expression mouths only).
Camera: own 22 mm eye-level medium three-shot from the -x side, wire coil / crate in the foreground (preset dressing), push 8 %/s + slide
50 px/s, still moving on every frame (shot < 2 s: no snap).  Beat: g_of(35.82) = 1078 "เงินก็หมดไป": the bag is turned out and shaken.
    python3 shot.py camreport | probe a:b | stills a:b out [scale] | final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
import bpy
from mathutils import Vector, Matrix, Euler
TG, K, cast16, actors = C.TG, C.K, C.cast16, C.actors
bf, u_of, lerp, blink = C.bf, C.u_of, C.lerp, C.blink
WORK = os.path.join(HERE, "work")
G0, G1 = C.g_bound(35.82), C.g_bound(37.30)      # 1075 .. 1118 (exclusive end 1119)
H = 9
GA, GZ = G0 - H, G1 + H - 1
GS = list(range(GA, GZ + 1))
G_BEAT = C.g_of(35.82)                            # 1078

SUBJ = Vector((119.0, -11.2, 2.55))
OFF = Vector((-4.0, 1.2, 0.25))                   # camera 4.9 D from Morse at g0 (before the push), a little to the +y side
CAM = C.CamPath(SUBJ + OFF * 1.0, SUBJ, GA, GZ, push=0.13, slide_px=40.0, arc_deg_s=20.0, decay=0.25,
                snaps=[dict(g=(1085, 1098), k=1.35, peak=1.9, shift=(0.28, -0.15))])

MO = cast16.STORY16["morse_empty_bag"][1]
WA = cast16.STORY16["worker_a_lean_shovel"][1]
WB = cast16.STORY16["worker_b_lean_shovel"][1]


SHAKES = [(1078, 1088), (1094, 1104)]               # two shakes of the empty sack (hopeful, then slumped)


def shake_env(g):
    """0..1 envelope of the shaking in progress (sin^2 bump per shake)"""
    e = 0.0
    for a_, b_ in SHAKES:
        if a_ <= g <= b_:
            e = max(e, math.sin(math.pi * (g - a_) / float(b_ - a_)) ** 2)
    return e


def shake_y(g):
    """vertical hand offset (puppet-local D): quick up-down while a shake runs"""
    for a_, b_ in SHAKES:
        if a_ <= g <= b_:
            return 0.16 * math.sin((g - a_) * 1.5) * math.sin(math.pi * (g - a_) / float(b_ - a_))
    return 0.0


def morse_pose(g):
    p = dict(MO)
    # holds the sack by its bottom corner at chest height in front of him, mouth DOWN; looks into it
    p["arm_r"] = dict(MO["arm_r"], hand=(0.58, 0.10 + shake_y(g)), bend=0.9)
    p.pop("prop_r", None)                                     # the sack is a 3D mesh (make_bag)
    p["expr"] = "worried" if g < 1092 else "sad"             # hopeful at the first shake, slumped at the second
    p["pitch"] = 0.40
    p["gaze"] = (0.30, 0.95)
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.17) + 4.0 * (1.0 if g > 1100 else 0.0)
    p["head_roll"] = -4 + 2.5 * math.sin(g * 0.13 + 1)
    p["blink"] = blink(g, [1091, 1112])
    p["t"] = g / 30.0
    return p


def worker_pose(base, g, ph, mirror):
    p = dict(base)
    p["lean"] = p.get("lean", 0) + 2.5 * math.sin(g * 0.15 + ph)
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.11 + ph)
    p["blink"] = blink(g, [1083 + int(ph * 7), 1104 + int(ph * 5)])
    e = shake_env(g)
    p["lean"] = p["lean"] + 7.0 * e                           # slump onto the shovel handle on each shake
    p["head_roll"] = p["head_roll"] + 9.0 * e
    p["squash"] = (1.0 + 0.03 * e, 1.0 - 0.06 * e)
    p["mirror"] = mirror
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the empty bag: a big sack turned inside out (3D, flat-lit like the cards)
def _flat_mat(name, col, emit=0.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out, df, em, mx = (nt.nodes.new(t) for t in ("ShaderNodeOutputMaterial", "ShaderNodeBsdfDiffuse", "ShaderNodeEmission", "ShaderNodeMixShader"))
    c = tuple(int(col[i:i + 2], 16) / 255.0 for i in (1, 3, 5)) + (1.0,)
    df.inputs["Color"].default_value = c
    em.inputs["Color"].default_value = c
    em.inputs["Strength"].default_value = emit
    mx.inputs[0].default_value = 0.92
    nt.links.new(df.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return m


def make_bag():
    """an EMPTY tied money sack held by its bottom corner, MOUTH DOWN (grip at the origin, hanging down: local x = screen right, z = up, -y toward the
    camera): tan limp body with wrinkles, a dark open mouth at the bottom and the cream lining flapping out of it (a separate object: it swings).
    Returns (body objects, lining objects)."""
    ink, dark = _flat_mat("bag_ink", "#2a1c16", 0.2), _flat_mat("bag_dark", "#1c1410", 0.1)
    tan, tan2, cream = _flat_mat("bag_tan", "#d9b27a", 1.0), _flat_mat("bag_tan2", "#a67a46", 0.9), _flat_mat("bag_cream", "#f4ead0", 1.1)
    mb = K.MB("s17_bag")
    mb.T = Matrix.Identity(4)
    def E(mb_, m, c, r):
        mb_.ell(m, c, r, (14, 10))
    E(mb, ink, (0.0, 0.05, -0.30), (0.25, 0.02, 0.34))                   # outlines (behind)
    E(mb, ink, (0.0, 0.05, -0.58), (0.35, 0.02, 0.30))
    E(mb, ink, (0.0, 0.04, -0.84), (0.36, 0.02, 0.09))
    E(mb, tan, (0.0, 0.0, -0.22), (0.22, 0.02, 0.26))                     # body, narrow at the fist, wide at the mouth
    E(mb, tan, (0.0, 0.0, -0.52), (0.32, 0.02, 0.30))
    E(mb, tan2, (0.0, -0.004, -0.74), (0.33, 0.02, 0.14))
    for dx, dz, hh in ((-0.14, -0.40, 0.18), (0.06, -0.50, 0.2), (0.17, -0.38, 0.15), (-0.05, -0.68, 0.12)):   # wrinkles
        E(mb, tan2, (dx, -0.016, dz), (0.011, 0.02, hh))
    E(mb, tan2, (0.0, -0.02, -0.03), (0.11, 0.02, 0.05))                  # twisted corner in the fist
    E(mb, dark, (0.0, -0.006, -0.84), (0.31, 0.02, 0.065))                # the open mouth
    obs = mb.finish()
    ml = K.MB("s17_lining")
    ml.T = Matrix.Identity(4)
    E(ml, ink, (0.0, 0.045, -0.24), (0.17, 0.02, 0.30))
    E(ml, cream, (0.0, -0.02, -0.22), (0.145, 0.02, 0.26))
    E(ml, tan2, (0.0, -0.035, -0.22), (0.010, 0.02, 0.2))
    lin = ml.finish()
    for o in obs + lin:
        o.visible_shadow = False
    return obs, lin


def make_bits():
    """dust puff (5 soft grey-cream blobs), one moth (two wings + body) and one button: they fall out of the sack."""
    dustm = _flat_mat("dust", "#d8c8a6", 0.9)
    wing, body, btn = _flat_mat("moth_wing", "#9a8a72", 0.7), _flat_mat("moth_body", "#3a2c22", 0.3), _flat_mat("button", "#2c2018", 0.3)
    puffs = []
    for i in range(5):
        mb = K.MB("s17_dust%d" % i)
        mb.T = Matrix.Identity(4)
        mb.ell(dustm, (0, 0, 0), (1.0, 0.4, 0.8), (10, 8))
        puffs.append(mb.finish()[0])
    mb = K.MB("s17_moth")
    mb.T = Matrix.Identity(4)
    mb.ell(wing, (-0.07, 0, 0.02), (0.075, 0.012, 0.05), (10, 6))
    mb.ell(wing, (0.07, 0, 0.02), (0.075, 0.012, 0.05), (10, 6))
    mb.ell(body, (0, 0, 0), (0.016, 0.016, 0.05), (6, 5))
    moth = mb.finish()
    mb = K.MB("s17_button")
    mb.T = Matrix.Identity(4)
    mb.ell(btn, (0, 0, 0), (0.05, 0.012, 0.05), (10, 6))
    button = mb.finish()
    for o in puffs + moth + button:
        o.visible_shadow = False
    return puffs, moth, button


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "line_trench_end", light="DUSK", quality=quality, name="cam_s17")
        self.key_cam(bf(GA), *CAM.at(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        mk = self.A["marks"]
        self.mk = mk
        self.bag, self.lining = make_bag()
        self.puffs, self.moth, self.button = make_bits()
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", sd, cam=self.cam)
        self.wa = self.actors["wa"] = C.make_actor("wa", cast16.key16("worker_a"), sd, cam=self.cam)
        self.wb = self.actors["wb"] = C.make_actor("wb", cast16.key16("worker_b"), sd, cam=self.cam)

    def pose(self, gs):
        mk = self.mk
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, (118.5, -11.3, 0.0))
            C.place(self.wa, f, (120.6, -9.9, 0.0))
            C.place(self.wb, f, (121.9, -13.2, 0.0))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, morse_pose(g), camera=self.cam)
            self.wa.pose(f, worker_pose(WA, g, 0.0, False), camera=self.cam)
            self.wb.pose(f, worker_pose(WB, g, 2.1, True), camera=self.cam)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            p = morse_pose(g)
            k = actors.upper_stretch(self.mor, self.cam, f, p)
            hip = C.sprites.hip_y("morse16", p)
            lx, ly = p["arm_r"]["hand"]
            hand = actors.local_to_world(self.mor, (lx, C.sprites.warp_y(ly, hip, k)), f, feet=C.sprites.feet_of("morse16", p), camera=self.cam)
            cam = Vector(self.cam.location)
            d = Vector(hand) - cam
            yaw = math.atan2(d.x, -d.y) + math.pi                               # local -y toward the camera
            e = shake_env(g)
            sw = math.radians(10.0 * e * math.sin(g * 1.9) + 3.0 * math.sin(g * 0.3))
            Rz = Matrix.Rotation(yaw, 4, "Z")
            M = Matrix.Translation(Vector(hand) + (cam - Vector(hand)).normalized() * 0.06 + Vector((0, 0, 0.1))) @ Rz @ Matrix.Rotation(sw, 4, "Y") @ Matrix.Scale(1.25, 4)
            self._key(self.bag, f, M, True)
            flap = math.radians(18.0 * math.sin(g * 1.3) * (0.4 + e) + 8.0 * math.sin(g * 0.45))
            ML = M @ Matrix.Translation((0.0, -0.01, -0.86)) @ Matrix.Rotation(flap, 4, "Y")
            self._key(self.lining, f, ML, True)
            mouth = M @ Vector((0.0, -0.04, -0.9))
            # dust puffs on each shake (rise a little, spread, fade by shrinking)
            for i, pf in enumerate(self.puffs):
                vis, loc, sc = False, mouth, 0.01
                for a_, b_ in SHAKES:
                    t0 = a_ + 3 + i
                    if t0 <= g <= t0 + 10:
                        u = (g - t0) / 10.0
                        ang = i * 1.9 + a_
                        loc = mouth + Vector((0.18 * u * math.cos(ang), 0.0, -0.10 - 0.25 * u * (0.6 + 0.2 * i)))
                        sc = (0.22 + 0.30 * u) * (1.0 - 0.6 * u) * (1.0 if a_ == SHAKES[0][0] else 0.75)
                        vis = True
                self._key([pf], f, Matrix.Translation(loc) @ Rz @ Matrix.Scale(max(sc, 0.01), 4), vis)
            # the moth flutters down from the first shake; the button drops on the second
            mv, mloc, mrot = False, mouth, 0.0
            if 1084 <= g <= 1122:
                u = (g - 1084) / 38.0
                mloc = mouth + Vector((0.22 * math.sin(u * 13.0) * (0.3 + u), 0.0, -0.95 * u ** 1.3))
                mv = True
            flapx = 0.35 + 0.65 * abs(math.sin(g * 1.1))
            self._key(self.moth, f, Matrix.Translation(mloc) @ Rz @ Matrix.Rotation(0.25 * math.sin(g * 0.4), 4, "Y") @ Matrix.Diagonal((flapx * 2.4, 2.4, 2.4, 1.0)), mv)
            bv, bl = False, mouth
            if 1100 <= g <= 1116:
                u = (g - 1100) / 16.0
                bl = mouth + Vector((0.05 * u, 0.0, -1.5 * u * u))
                bv = True
            self._key(self.button, f, Matrix.Translation(bl) @ Rz @ Matrix.Rotation(g * 0.7, 4, "Y") @ Matrix.Scale(2.0, 4), bv)
        self.sprites_for([(self.mor, 256), (self.wa, 256), (self.wb, 256)], [bf(g) for g in gs])

    def _key(self, obs, f, M, vis):
        loc, rot, sc = M.decompose()
        for ob in obs:
            ob.location, ob.rotation_euler, ob.scale = loc, rot.to_euler(), sc
            for pth in ("location", "rotation_euler", "scale"):
                ob.keyframe_insert(pth, frame=f)
        C.key_vis(obs, bool(vis), f)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print(rows[0], rows[-1]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                st = Tk.render([g], out, scale=scale, samples=6)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
