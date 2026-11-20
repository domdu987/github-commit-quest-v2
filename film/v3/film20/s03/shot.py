#!/usr/bin/env python3
"""shot.py -- film 20 take s03 = shot 3 + shot 4 merged = BIGZOOM 1 (g 178..317; dissolve-in handle g 170..177; cut-out handle g 318..321).
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

G0, G1 = C.g_bound(5.93), C.g_bound(10.60)     # 178, 318 (shot = g 178..317)
H_IN, H_OUT = 8, 4                             # dissolve 13: 13/2 + 2 = 8.5 -> 8 frames (director's number); cut side 4
GF, G_LAST = G0 - H_IN, G1 + H_OUT - 1         # 170..321
GS = list(range(GF, G_LAST + 1))
G_WORD = C.cap_g("วิศวกรไอเฟล")                   # 268
G_LAND = G_WORD                                # the zoom lands on the medium at the word
RAISE = (G_WORD - 2, G_WORD + 6)               # arm rises to the point
G_SWAP = G_WORD + 2
PRESET, LIGHT, MARK = "site_table", "DAY", "eiffel_table"
PPD = 256
D0, D1 = 120.0, 4.6                            # camera distance to Eiffel (D): extreme wide -> medium
EL0, EL1 = 27.0, 7.0                           # elevation (deg): high over Paris -> low
AZ0, AZ1 = 228.0, 221.0                        # azimuth from the table (deg, 225 = the preset camera's side)
TILT1 = 9.0                                    # aim tilts UP by the end so the leg + scaffold fill the background


def smoother(u):
    u = clamp(u, 0.0, 1.0)
    return u * u * u * (u * (u * 6 - 15) + 10)


class ZoomPath(C.CamPath):
    """BIGZOOM: spherical path about Eiffel's body: distance D0 -> D1 (geometric), elevation EL0 -> EL1, azimuth AZ0 -> AZ1, all on one
    smootherstep over g 178..268 (ease in/out), then a slow drift (push 5 %/s, azimuth -3 deg/s) so it never parks."""

    def __init__(self, A):
        m = Vector(A["marks"][MARK])
        self.subj = m + Vector((0.0, 0.0, 1.7))
        C.CamPath.__init__(self, self.subj + Vector((1, 0, 0)), self.subj, GF, G_LAST, push=0, decay=0.0)

    def state(self, g):
        u = clamp((g - GF) / float(G_LAND - GF), 0.0, 1.0)
        s = 0.10 * u + 0.90 * smoother(u)          # ease in/out, but already moving on frame 0 (never parked)
        tau = max(0.0, (g - G_LAND) / 30.0)
        d = D0 * (D1 / D0) ** s * (1.0 - 0.05 * tau)
        el = lerp(EL0, EL1, s)
        az = lerp(AZ0, AZ1, s) - 3.0 * tau
        return d, el, az, lerp(8.0, TILT1, s)

    def at(self, g):
        d, el, az, tilt = self.state(g)
        e, a = math.radians(el), math.radians(az)
        off = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e))) * d
        loc = self.subj + off
        fwd = (self.subj - loc).normalized()
        r = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        from mathutils import Matrix
        aim = Matrix.Rotation(math.radians(tilt), 3, r) @ fwd
        return loc, loc + aim * d

    def tilt(self, g):
        return self.state(g)[3]


def cam_path(A):
    return ZoomPath(A)


def cam_path_static():
    import site20
    A = dict(marks={MARK: CO.W((50.7, -71.3, 0.0))})
    return cam_path(A)


EIF_A = cast20.STORY20["eiffel_blueprint"][1]
EIF_B = cast20.STORY20["eiffel_point_up"][1]


def pose_of(g):
    u = u_of(g, *RAISE) * (1.0 - u_of(g, 292, 302))                    # arm up g 266-274, held, down g 292-302 (hand on hip, proud)
    p = dict(puppet.lerp_pose("eiffel", EIF_A, EIF_B, u))
    p["expr"] = "determined" if g < G_SWAP else "proud"
    p["yaw"] = lerp(0.35, 0.45, u)
    p["lean"] = lerp(0.0, -3.0, u) + 1.2 * math.sin(g * 0.21)
    p["squash"] = (1.0, 1.0 + 0.010 * math.sin(g * 0.3))
    p["head_roll"] = 2.0 * math.sin(g * 0.17) + 3.0 * ez(u)
    p["blink"] = blink(g, [G_SWAP - 1, 300])
    p["t"] = g / 30.0
    return p


RIV = [("rv_a", "riveter_hammer", (57.0, -63.0), False), ("rv_b", "riveter_tongs", (66.0, -57.0), True), ("rv_c", "riveter_forge", (41.0, -50.0), False)]


def riv_pose(kind, g, k):
    ph = g * 0.7 + k * 1.9
    if kind == "riveter_hammer":
        a, b = cast20.STORY20["riveter_hammer_work"][1], cast20.STORY20["riveter_hammer_hit"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph), 0, 1) ** 2
    elif kind == "riveter_tongs":
        a, b = cast20.STORY20["riveter_tongs_work"][1], cast20.STORY20["riveter_tongs_throw"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.5), 0, 1)
    else:
        a, b = cast20.STORY20["riveter_forge_work"][1], cast20.STORY20["riveter_forge_lift"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.4), 0, 1)
    p = dict(puppet.lerp_pose(kind, a, b, u))
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.3 + k))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s03")
        self.A["marks"][MARK] = C.on_ground(self.A["marks"][MARK])
        for ob in C.bpy.data.objects:                               # the preset's near-black FG slabs (anchored to the preset camera): camera-invisible
            if ob.name in ("fg_redlead_sh", "fg_dark_sh", "fg_metal_sh"):
                ob.visible_camera = False
        self.path = cam_path(self.A)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"), contact=dict(width=1.4, depth=0.6, opacity=0.8),
                                                     cam=self.cam)
        self.riv = []
        for name, cast, xy, mirror in RIV:
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=dict(width=1.2, depth=0.5, opacity=0.8), cam=self.cam)
            self.actors[name] = a
            mk = C.on_ground(CO.W((xy[0], xy[1], 0.0)))
            self.riv.append((a, cast, mk, mirror))

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, mark)
            for a, cast, mk, mirror in self.riv:
                C.place(a, f, mk)
            self.key_set(f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, pose_of(g), camera=self.cam)
            for i, (a, cast, mk, mirror) in enumerate(self.riv):
                p = riv_pose(cast, g, i)
                if mirror:
                    p["mirror"] = True
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(self.eif, PPD)] + [(a, 160) for a, _, _, _ in self.riv], [bf(g) for g in gs])

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
