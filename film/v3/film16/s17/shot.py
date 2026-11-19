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


def morse_pose(g):
    p = dict(MO)
    u = u_of(g, G_BEAT - 6, G_BEAT + 6)                       # bag turned out (hand rises) then shaken
    shake = math.sin((g - G_BEAT) * 0.9) * 0.10 * u * (1.0 - u_of(g, G_BEAT + 14, G_BEAT + 30))
    p["arm_r"] = dict(MO["arm_r"], hand=(0.80 + 0.06 * shake * 3, 0.70 + shake))
    p.pop("prop_r", None)                                     # the bag is a 3D mesh (BAG, below): bigger, turned inside out
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.17)
    p["head_roll"] = -4 + 2.5 * math.sin(g * 0.13 + 1)
    p["blink"] = blink(g, [1090, 1112])
    p["t"] = g / 30.0
    return p


def worker_pose(base, g, ph, mirror):
    p = dict(base)
    p["lean"] = p.get("lean", 0) + 2.5 * math.sin(g * 0.15 + ph)
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.11 + ph)
    p["blink"] = blink(g, [1083 + int(ph * 7), 1104 + int(ph * 5)])
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
    """hangs from the grip at the origin (local x = screen right, z = up, -y toward the camera): tan sack body, the two cream LININGS turned out
    like ears at the sides, a limp drooping bottom, dark outlines behind (ink)."""
    ink, tan, tan2, cream = _flat_mat("bag_ink", "#2a1c16", 0.2), _flat_mat("bag_tan", "#d9b27a", 1.0), _flat_mat("bag_tan2", "#a67a46", 0.9), _flat_mat("bag_cream", "#f4ead0", 1.1)
    mb = K.MB("s17_bag")
    mb.T = Matrix.Identity(4)
    def E(m, c, r, rot=0.0):
        mb.ell(m, c, r, (14, 10))
    E(ink, (0.0, 0.05, -0.50), (0.35, 0.02, 0.50))                       # outlines (behind)
    E(ink, (-0.36, 0.05, -0.40), (0.20, 0.02, 0.27))
    E(ink, (0.36, 0.05, -0.40), (0.20, 0.02, 0.27))
    E(ink, (0.0, 0.05, -0.97), (0.22, 0.02, 0.10))
    E(tan, (0.0, 0.0, -0.50), (0.32, 0.02, 0.47))                        # body
    E(tan2, (0.0, -0.01, -0.80), (0.24, 0.02, 0.17))                     # shaded droop
    E(tan, (0.0, 0.0, -0.95), (0.19, 0.02, 0.08))                        # limp tip
    E(cream, (-0.36, -0.01, -0.40), (0.17, 0.02, 0.24))                  # linings turned out
    E(cream, (0.36, -0.01, -0.40), (0.17, 0.02, 0.24))
    E(tan2, (-0.36, -0.02, -0.40), (0.012, 0.02, 0.19))                  # seam lines
    E(tan2, (0.36, -0.02, -0.40), (0.012, 0.02, 0.19))
    for dx, dz in ((-0.12, -0.45), (0.05, -0.55), (0.14, -0.4)):             # wrinkles
        E(tan2, (dx, -0.015, dz), (0.012, 0.02, 0.16))
    E(tan2, (0.0, -0.02, -0.06), (0.15, 0.02, 0.045))                    # tied neck
    obs = mb.finish()
    for o in obs:
        o.visible_shadow = False
    return obs


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "line_trench_end", light="DUSK", quality=quality, name="cam_s17")
        self.key_cam(bf(GA), *CAM.at(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        mk = self.A["marks"]
        self.mk = mk
        self.bag = make_bag()
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
            u = u_of(g, G_BEAT - 6, G_BEAT + 6)
            sw = math.radians(28.0 * u * math.sin((g - G_BEAT) * 0.55) * (1.0 - u_of(g, G_BEAT + 16, G_BEAT + 34)) + 4.0 * math.sin(g * 0.3))
            M = Matrix.Translation(Vector(hand) + (cam - Vector(hand)).normalized() * -0.06 + Vector((0, 0, 0.03))) @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Rotation(sw, 4, "Y") @ Matrix.Scale(1.15, 4)
            loc, rot, sc = M.decompose()
            for ob in self.bag:
                ob.location, ob.rotation_euler, ob.scale = loc, rot.to_euler(), sc
                for pth in ("location", "rotation_euler", "scale"):
                    ob.keyframe_insert(pth, frame=f)
        self.sprites_for([(self.mor, 256), (self.wa, 256), (self.wb, 256)], [bf(g) for g in gs])

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
