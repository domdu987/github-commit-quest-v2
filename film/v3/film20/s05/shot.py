#!/usr/bin/env python3
"""shot.py -- film 20 take s05 = shot 5 (g 318..403; cut in -> 4 in-handle frames g 314..317; cut out -> 4 out-handle frames g 404..407).
"สูง 300 เมตร สูงที่สุดในโลก": SITE site_leg_low / DAY / stage 0.  Low camera at the foot of the OUTER face of the front-left leg, tilting UP the
scaffolded leg to the sky (aim 13 -> 35 deg look-up, ends >= 35 % sky), riveters on the three cantilever platforms, Eiffel small at the foot
with his arm raised; SNAP up (extra tilt + push) on "สูงที่สุดในโลก" (event g 346).
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp] | hue g ..
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector, Matrix                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
import puppet                                            # noqa: E402

G0, G1 = C.g_bound(10.60), C.g_bound(13.47)   # 318, 404 (shot = g 318..403)
H_IN, H_OUT = 4, 4
GF, G_LAST = G0 - H_IN, G1 + H_OUT - 1         # 314..407
GS = list(range(GF, G_LAST + 1))
G_MOST = C.cap_g("สูงที่สุดในโลก")                # 346: snap up
SNAP = (G_MOST - 2, G_MOST + 13)               # 344..359
G_300 = C.cap_g("สูง 300 เมตร")                  # 321: Eiffel's arm goes up
PRESET, LIGHT = "site_leg_low", "DAY"
PPD_E, PPD_W = 256, 160
PITCH0, PITCH1 = 19.0, 27.0                    # drift aim pitch (deg, up from the horizon); + snap -> ends ~35
SNAP_PITCH = 11.0
RIVETERS = [("rv_a", "riveter_hammer", "leg_a", False), ("rv_b", "riveter_tongs", "leg_b", True), ("rv_c", "riveter_forge", "leg_c", False)]
EIF_MARK = "eiffel_leg"
FWD0 = 12.0
YAW = 9.0                                      # deg: aim turned toward Eiffel (screen-left)


class LegPath(C.CamPath):
    """camera at the foot of the leg: fixed yaw (the preset heading), pitch 12 -> 22 deg by drift (eased, moving on both ends) + a 12 deg
    SNAP up on "สูงที่สุดในโลก"; push 8 %/s toward the foot of the leg (the camera creeps closer) + 40 px/s lateral slide."""

    def __init__(self, A):
        c = A["cams"][PRESET]
        self.l0, self.k0 = Vector(c["loc"]), Vector(c["look_at"])
        hh = self.k0 - self.l0
        hh.z = 0.0
        self.l0 = self.l0 + hh.normalized() * FWD0                 # nearer the foot of the leg (Eiffel bigger, no pier wall behind)
        foot = Vector(A["marks"][EIF_MARK]) + Vector((0, 0, 1.5))
        C.CamPath.__init__(self, self.l0, foot, GF, G_LAST, push=0.08, slide_px=40.0, decay=0.3)
        h = self.k0 - self.l0
        self.h = Vector((h.x, h.y, 0.0)).normalized()
        self.rgt = Vector((self.h.y, -self.h.x, 0.0))

    def pitch(self, g):
        T = (G_LAST - GF) / 30.0
        t = (g - GF) / 30.0 / T
        u = 1.25 * t - 0.25 * t * t                      # eased out, still moving at the end
        return lerp(PITCH0, PITCH1, u) + SNAP_PITCH * C.snap_u(g, SNAP[0], SNAP[1], 1.7)

    def tilt(self, g):
        return self.pitch(g)

    def at(self, g):
        p = self._p(g)
        d = (self.subj0 - self.l0).length
        zoom = max(0.3, 1.0 + self.push * p)
        # push: the camera creeps toward the foot of the leg (horizontal only: it stays 1.4 m high)
        fwd = (self.subj0 - self.l0)
        fwd.z = 0.0
        fwd.normalize()
        loc = Vector(self.l0)
        loc += fwd * (d * (1.0 - 1.0 / zoom)) * 0.9
        loc += self.rgt * (self.slide_px * d / C.F_PX * p)
        s = C.snap_u(g, SNAP[0], SNAP[1], 1.7)
        loc += fwd * (0.8 * s)                           # a little extra push in the snap
        ang = math.radians(self.pitch(g))
        tt = (g - GF) / float(G_LAST - GF)
        hy = Matrix.Rotation(math.radians(YAW - 24.0 * tt), 3, 'Z') @ self.h      # the aim also pans right (parallax on the pier / scaffold)
        aim = hy * math.cos(ang) + Vector((0, 0, math.sin(ang)))
        return loc, loc + aim * 20.0


def cam_path(A):
    return LegPath(A)


def cam_path_static():
    import site20
    c = site20.CAMS_M[PRESET]
    A = dict(cams={PRESET: dict(loc=CO.W(c["loc"]), look_at=CO.W(c["look"]))}, marks={EIF_MARK: CO.W((-58.5, -70.5, 0.0))})
    return cam_path(A)


EIF_UP = cast20.STORY20["eiffel_point_up"][1]
EIF_CALM = cast20.STORY20["eiffel_calm"][1]


def eif_pose(g):
    u = u_of(g, G_300 - 2, G_300 + 6)
    p = dict(puppet.lerp_pose("eiffel", EIF_CALM, EIF_UP, u))
    p["expr"] = "proud"
    p["yaw"] = lerp(0.25, 0.4, u)
    p["lean"] = lerp(0.0, -4.0, u) + 1.2 * math.sin(g * 0.2)
    p["head_roll"] = 2.0 * math.sin(g * 0.15) + 2.0 * u
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.28))
    p["blink"] = blink(g, [335, 368])
    p["t"] = g / 30.0
    return p


def riv_pose(kind, g, k):
    ph = g * 0.45 + k * 1.9
    cast = kind
    if kind == "riveter_hammer":
        a, b = cast20.STORY20["riveter_hammer_work"][1], cast20.STORY20["riveter_hammer_hit"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph), 0, 1) ** 2
    elif kind == "riveter_tongs":
        a, b = cast20.STORY20["riveter_tongs_work"][1], cast20.STORY20["riveter_tongs_throw"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.5), 0, 1)
    else:
        a, b = cast20.STORY20["riveter_forge_work"][1], cast20.STORY20["riveter_forge_lift"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.4), 0, 1)
    p = dict(puppet.lerp_pose(cast, a, b, u))
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.3 + k))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s05")
        for ob in C.bpy.data.objects:
            if ob.name in ("fg_redlead_sh", "fg_dark_sh"):
                ob.visible_camera = False
        self.path = cam_path(self.A)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.eif_mark = C.on_ground(self.A["marks"][EIF_MARK])
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"), contact=dict(width=1.4, depth=0.6, opacity=0.8), cam=self.cam)
        self.riv = []
        for name, cast, mark, mirror in RIVETERS:
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=False, cam=self.cam)     # on a deck: no ground decal
            self.actors[name] = a
            self.riv.append((a, cast, tuple(self.A["marks"][mark]), mirror))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, self.eif_mark)
            for a, cast, mk, mirror in self.riv:
                C.place(a, f, mk)
            self.key_set(f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, eif_pose(g), camera=self.cam)
            for i, (a, cast, mk, mirror) in enumerate(self.riv):
                p = riv_pose(cast, g, i)
                if mirror:
                    p["mirror"] = True
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(self.eif, PPD_E)] + [(a, PPD_W) for a, _, _, _ in self.riv], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(self.path.pitch(g), 1), heads=C.head_report(self, f))

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
