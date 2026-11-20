#!/usr/bin/env python3
"""shot.py -- film 20 take s04 = shot 4 (g 265..317; cut in -> 4 in-handle frames g 261..264; cut out -> 4 out-handle frames g 318..321).
"วิศวกรไอเฟล" (event g 268): SITE site_table / DAY / stage 0.  EIFFEL at the plank plan table under a front leg, a rolled blueprint in hand,
looks at the plan, then points UP proudly (arm raises g 266..274, expression determined -> proud on the closed frame of a blink).
Camera: the preset lowered ~0.4 m and tilted up ~8 deg so the curved leg + scaffold (not the blank pier wall) fill the background; push 8 %/s
toward his head + 40 px/s slide; girder end FG in the nearest 15 %.   (1.77 s: no snap needed, < 2 s)
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp] | hue g ..
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
import puppet                                            # noqa: E402

G0, G1 = C.g_bound(8.84), C.g_bound(10.60)     # 265, 318 (shot = g 265..317)
H_IN, H_OUT = 4, 4
GF, G_LAST = G0 - H_IN, G1 + H_OUT - 1         # 261..321
GS = list(range(GF, G_LAST + 1))
G_WORD = C.cap_g("วิศวกรไอเฟล")                   # 268
RAISE = (G_WORD - 2, G_WORD + 6)               # 266..274 arm rises to the point
G_SWAP = G_WORD + 2                            # expression swap on the closed frame of the blink 269..271
PRESET, LIGHT, MARK = "site_table", "DAY", "eiffel_table"
HEAD_Z = 2.6
PPD = 256
CAMERA_DROP = 0.75                             # D (0.4 m lower)
CAM_FWD = 7.0                                  # D toward him
TILT0 = 7.5                                    # deg above the camera -> head line; + drift tilt
TILT_RATE = 1.5


def cam_path(A):
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"]) - Vector((0.0, 0.0, CAMERA_DROP))
    c = c + (subj - c).normalized() * CAM_FWD                           # closer: his head ~110 px instead of 56
    return C.CamPath(c, subj, GF, G_LAST, push=0.05, slide_px=55.0, rise_px=0.0, arc_deg_s=-16.0, tilt0=TILT0, tilt_deg_s=TILT_RATE,
                     decay=0.2, snaps=[dict(g=(G_WORD - 2, G_WORD + 11), k=1.4, peak=1.7, shift=(-0.4, 0.0), tilt=1.0)])


def cam_path_static():
    import site20
    cam = site20.CAMS_M[PRESET]
    A = dict(marks={MARK: CO.W((50.7, -71.3, 0.0))}, cams={PRESET: dict(loc=CO.W(cam["loc"]))})
    return cam_path(A)


EIF_A = cast20.STORY20["eiffel_blueprint"][1]
EIF_B = cast20.STORY20["eiffel_point_up"][1]


def pose_of(g):
    u = u_of(g, *RAISE) * (1.0 - u_of(g, 288, 298))                    # arm up 266-274, held, back down 288-298
    p = dict(puppet.lerp_pose("eiffel", EIF_A, EIF_B, u))
    p["expr"] = "determined" if g < G_SWAP else "proud"
    p["yaw"] = lerp(0.35, 0.45, u)
    p["lean"] = lerp(0.0, -3.0, u) + 1.2 * math.sin(g * 0.21)
    p["squash"] = (1.0, 1.0 + 0.010 * math.sin(g * 0.3))
    p["head_roll"] = 2.0 * math.sin(g * 0.17) + 3.0 * ez(u)
    p["blink"] = blink(g, [G_SWAP - 1, 288])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s04")
        self.A["marks"][MARK] = C.on_ground(self.A["marks"][MARK])
        for ob in C.bpy.data.objects:                               # the preset's girder-end FG is a near-black slab: camera-invisible
            if ob.name in ("fg_redlead_sh", "fg_dark_sh"):
                ob.visible_camera = False
        self.path = cam_path(self.A)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"), contact=dict(width=1.4, depth=0.6, opacity=0.8),
                                                     cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, mark)
            self.key_set(f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.eif, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
        for r in rows[::5]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (max 6)" % worst)
        sys.exit(0)
    if cmd == "hue":
        gs = [int(v) for v in sys.argv[2:]]
        Tk = Take("final"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], os.path.join(WORK, "hue"))[0]
            print(g, json.dumps(C.hue_frame(st["path"])), flush=True)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
