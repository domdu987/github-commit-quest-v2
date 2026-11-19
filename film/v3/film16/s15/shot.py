#!/usr/bin/env python3
"""shot.py -- film 16 take s15 = shot 15 (g 958..1006, plan 31.93-33.57 s) + handles 9 each side (g 949..1015).
"แต่พอลอง ส่งข่าว เงียบกริบ" -- LINE line_trench_end / DUSK: Morse at the test key on the crate at the furrow's end presses it; the register stays
silent; Cornell and the workers lean in, waiting.  On "เงียบกริบ" (g 988) the picture dips to x0.75 brightness for 0.4 s (bible device).
DIS in, DIS out (shot 16 is a cut-away: handles are for a dissolve or cut).  Camera: slow push 6 %/s + slide, crate + coil in the foreground.
Mouths: nobody speaks.  NO depth of field, NO text.
    python3 shot.py probe a:b | stills a:b out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

TG, K, LN, cast16 = C.TG, C.K, C.LN, C.cast16
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(31.93), C.g_bound(33.57)            # 958, 1007: shot = g 958..1006
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 + H_OUT - 1                      # 949 .. 1015
GS = list(range(GA, GB + 1))
G_TRY = C.g_of(32.41)                                   # 975: "ส่งข่าว" of the false sentence (cap_g would match the hook's first "ส่งข่าว" at g 422)
G_SIL = C.cap_g("เงียบกริบ")                            # 988: silence, brightness dip
DIP = (G_SIL - 2, G_SIL + 10)                           # 0.4 s
PRESS = (G_TRY, G_TRY + 6)
PRESS2 = (G_SIL - 6, G_SIL - 1)
PRESS3 = (996, 1002)                                  # one more press inside the end close
CAM_NEAR = 0.72
CAM_UP = 1.2
CAM_NEAR, CAM_UP = 0.72, 1.2
PRESET, LIGHT = "line_trench_end", "DUSK"
DIP_K = 0.58                                            # brightness at the bottom of the dip (director: 0.55-0.6)

def dip(g):
    a, b = DIP
    if g <= a or g >= b:
        return 1.0
    u = (g - a) / float(b - a)
    return 1.0 - (1.0 - DIP_K) * math.sin(math.pi * u)

def key_press(g):
    v = 0.0
    for a, b in (PRESS, PRESS2, PRESS3):
        if a <= g <= b:
            v = max(v, math.sin(math.pi * (g - a) / float(b - a)))
    return v

STORY = cast16.STORY16
def story(name):
    return dict(STORY[name][1])

ACTORS = dict(morse=("morse16", "morse_key_wait", None), cornell=("cornell", "cornell_wait", "worker_key_c"),
              worker_a=("worker16_a", "worker_a_lean_shovel", "worker_key_a"), worker_b=("worker16_b", "worker_b_lean_shovel", "worker_key_b"))
CANVAS = dict(worker_a=(-2.6875, -4.375, 2.6875, 0.375), worker_b=(-2.6875, -4.625, 2.6875, 0.1875), cornell=(-2.6875, -4.1875, 2.6875, 0.1875),
              morse=(-2.375, -4.375, 2.375, 0.1875))

# ---- the set's test key (tg_line.key_station): crate frame = KEYCRATE, yaw 0.5, scale 1.6; lever pivot / rod end / knob in crate-local metres
KC, KYAW, KSC = LN.KEYCRATE, 0.5, 1.6
def key_pt(lx, ly, lz):
    c, s_ = math.cos(KYAW), math.sin(KYAW)
    return Vector(K.W((KC[0] + (c * lx - s_ * ly) * KSC, KC[1] + (s_ * lx + c * ly) * KSC, lz * KSC)))
PIV = lambda: key_pt(0.12, -0.2, 0.70)
ROD_END = lambda: key_pt(0.30, -0.2, 0.75)
KNOB = lambda: key_pt(0.31, -0.2, 0.76)
PRESS_DEG = 16.0
LEVER_RIGHT = lambda: (Vector(ROD_END()) - Vector(PIV())).normalized()

def lever_rot(g):
    d = LEVER_RIGHT()
    return Matrix.Rotation(math.radians(PRESS_DEG * key_press(g)), 3, Vector((0, 0, 1)).cross(d))

def knob_world(g):
    p = Vector(PIV())
    return p + lever_rot(g) @ (Vector(KNOB()) - p)

CREW = dict(cornell=lambda: (Vector(KNOB()).x + 2.4, Vector(KNOB()).y - 2.0, 0.0), worker_a=lambda: (Vector(KNOB()).x + 4.4, Vector(KNOB()).y - 1.6, 0.0),
            worker_b=lambda: (Vector(KNOB()).x + 3.4, Vector(KNOB()).y - 2.9, 0.0))

def morse_at():
    k = Vector(KNOB())
    return (k.x - 0.95, k.y - 0.55, 0.0)         # beside the key (crate end), reaching left to the knob

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        A = self.A
        self.make_lever()
        self.make_dressing()
        k = Vector(KNOB())
        look0 = Vector((k.x - 0.2, k.y - 0.6, 2.6))
        loc0 = look0 + Vector((-2.0, 6.2, 1.6))
        self.cp = C.CamPath(loc0, look0, GA, GB, push=0.12, slide_px=20.0, arc_deg_s=-15.0, decay=0.25,
                            snaps=[dict(g=(G_SIL - 2, G_SIL + 11), k=2.2, peak=1.8, shift=(-0.25, -0.4))])
        self.key_cam(bf(GA), *self.cp.at(GA))
        self.scene.frame_set(bf(GA))
        self.base_exp = self.scene.view_settings.exposure
        sd = os.path.join(WORK, "sprites")
        self.act = {}
        for nm, (cast, pose, mark) in ACTORS.items():
            self.actors[nm] = self.act[nm] = C.make_actor(nm, cast, sd, canvas=CANVAS.get(nm), contact=True, cam=self.cam)

    def make_lever(self):
        """replace the set's static lever + knob with an animated copy (rod and knob pivot about the lever's hinge)"""
        import bmesh, bpy
        inv = K.frame_mat().inverted()
        piv, end, knob = Vector(PIV()), Vector(ROD_END()), Vector(KNOB())
        for name in ("work_brass", "work_dark"):
            ob = bpy.data.objects.get(name)
            if ob is None:
                continue
            bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
            bad = []
            for v in bm.verts:
                w = mw @ v.co
                if name == "work_brass" and (w - piv).length < 0.8 and w.z > piv.z - 0.03 and (w - Vector((piv.x, piv.y, w.z))).length > 0.0:
                    # rod verts: close to the segment piv -> end
                    t = max(0.0, min(1.0, (w - piv).dot(end - piv) / (end - piv).length_squared))
                    if (w - (piv + (end - piv) * t)).length < 0.07:
                        bad.append(v)
                if name == "work_dark" and (w - knob).length < 0.25:
                    bad.append(v)
            bmesh.ops.delete(bm, geom=bad, context="VERTS"); bm.to_mesh(ob.data); bm.free()
        M = TG.STATE["M"]
        mb = K.MB("s15_lever")
        mb.rod(M["brass"], tuple(inv @ piv), tuple(inv @ end), 0.019, 0.019, 8)
        mb.ell(M["dark"], tuple(inv @ knob), (0.055, 0.055, 0.05), (10, 6))
        self.lever = mb.finish()

    def make_dressing(self):
        """period look for the register (brass frame + still white tape strip over the box front) and a warm lantern with a light pool on the crate"""
        import bpy
        from mathutils import Euler
        M = TG.STATE["M"]
        tape = TG._emit_mat("s15_tape", "#f4f0e2", 0.55)
        glow = TG._emit_mat("s15_lantern_glass", "#ffb45a", 6.0)
        mb = K.MB("s15_dress")
        c = (KC[0], KC[1], 0.0)
        mb.push(Matrix.Translation(c) @ Euler((0, 0, KYAW)).to_matrix().to_4x4() @ Matrix.Diagonal((KSC, KSC, KSC, 1)))
        mb.push(Matrix.Translation((0, 0, 0.6)))
        for sy in (-0.07, 0.07):
            mb.cyl(M["brass"], (-0.28, 0.1 + sy, 0.10), 0.062, 0.03, "z", 14, True)   # brass collars on the coils
        mb.box(M["brass"], (0.15, 0.15, 0.225), (0.36, 0.26, 0.015))              # brass top on the register box
        mb.cyl(M["brass"], (0.08, 0.15, 0.24), 0.095, 0.02, "y", 18)              # brass flange on the paper drum
        mb.box(tape, (0.37, 0.15, 0.20), (0.20, 0.07, 0.006), ry=-0.2)            # white tape strip out of the register ...
        mb.box(tape, (0.47, 0.15, 0.13), (0.04, 0.07, 0.10))                        # ... hanging over the edge, not moving
        mb.cyl(M["brass"], (-0.45, -0.18, 0.04), 0.07, 0.06, "z", 14, True)       # lantern: brass base, glowing glass, roof
        mb.cyl(glow, (-0.45, -0.18, 0.13), 0.055, 0.12, "z", 14, True)
        mb.cyl(M["brass"], (-0.45, -0.18, 0.21), 0.075, 0.025, "z", 14, True)
        mb.ell(M["brass"], (-0.45, -0.18, 0.24), (0.03, 0.03, 0.03), (8, 6))
        mb.pop(); mb.pop()
        self.dress = mb.finish()
        lp = key_pt(-0.45, -0.18, 0.73)
        ld = bpy.data.lights.new("s15_lantern", "POINT")
        ld.energy = 600.0; ld.color = (1.0, 0.66, 0.32); ld.shadow_soft_size = 0.25
        lo = bpy.data.objects.new("s15_lantern", ld); lo.location = lp
        self.scene.collection.objects.link(lo)
        self.lantern = lo

    def pose(self, gs):
        for g in gs:
            self.key_cam(bf(g), *self.cp.at(g))
        piv = Vector(PIV())
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.scene.view_settings.exposure = self.base_exp + math.log2(dip(g))
            self.scene.view_settings.keyframe_insert("exposure", frame=f)
            R = lever_rot(g)
            ang = math.radians(PRESS_DEG * key_press(g))
            ax = Vector((0, 0, 1)).cross(LEVER_RIGHT()).normalized()
            for ob in self.lever:
                ob.rotation_mode = "AXIS_ANGLE"
                ob.rotation_axis_angle = (ang, ax.x, ax.y, ax.z)
                ob.location = piv - R @ piv
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_axis_angle", frame=f)
            for nm, (cast, pose, mark) in ACTORS.items():
                p = story(pose)
                mk = morse_at() if nm == "morse" else CREW[nm]()
                hands = None
                if nm == "morse":
                    kp = key_press(g)
                    p["key_press"] = 0.0
                    p.pop("prop_r", None)                  # the set shows the key
                    p["expr"] = "determined" if g < 982 else "worried"
                    p["gaze"] = (1.0, 0.9); p["mirror"] = True; p["pitch"] = 0.6
                    kw = knob_world(g)
                    hands = {"r": {"hand": (kw.x, kw.y, kw.z + 0.18), "layer": "front"}}
                else:
                    p["arm_r"] = "down"; p["arm_l"] = "down"          # no folded arms: they bend toward the register
                    p["yaw"] = 0.95; p["pitch"] = 0.35
                    p["gaze"] = (1.0, 0.7)
                    p["lean"] = p.get("lean", 0.0) + 11.0 + 3.0 * math.sin(g * 0.13 + len(nm))      # lean in toward the register
                p["lean"] = p.get("lean", 0.0) + 1.2 * math.sin(g * 0.17 + len(nm))
                p["head_roll"] = p.get("head_roll", 0.0) + 1.5 * math.sin(g * 0.11 + 2 * len(nm))
                p["blink"] = blink(g, [960 + 29 * (len(nm) % 4), 1000 + 3 * len(nm)])
                p["t"] = g / 30.0
                C.place(self.act[nm], f, mk)
                _, info = self.act[nm].pose(f, p, hands=hands, camera=self.cam)
                if hands:
                    self.herr = info["r"].get("error", 0.0)
        self.sprites_for([(a, 256) for a in self.act.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.cp.at(g)
        return dict(g=g, dip=round(dip(g), 3), press=round(key_press(g), 2), herr=round(getattr(self, "herr", 0.0), 3), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = Tk.cp.report(GS[:-1])
        print("longest run under 0.25 px/frame:", worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g %d %.1f s" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
