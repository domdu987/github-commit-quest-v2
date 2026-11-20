#!/usr/bin/env python3
"""shot.py -- film 20 take s03 = shot 3 (g 178..264; in-handle g 169..177 for the 13-frame dissolve, out-handle g 265..268 for the cut).
"ปารีส ปี 1887": SITE site_wide / DAY / stage 0 -- the building site seen from the visitors' crane gantry: four curved iron legs rising out of
timber scaffolds, forges + smoke, carts, Paris beyond.  High crane DOWN with a push and a 40 px/s slide, one eased SNAP push on "ปี 1887".
Six riveters (cast20 cards) work at the marks worker_a..g (hammer swings, tong turns, forge lifts: nobody frozen).
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

G0, G1 = C.g_bound(5.93), C.g_bound(8.84)      # 178, 265 (shot = g 178..264)
H_IN, H_OUT = 9, 4                             # dissolve 13 -> 13/2 + 2 = 9 (8.5 up); cut side 4
GF, G_LAST = G0 - H_IN, G1 + H_OUT - 1         # first_g 169, last 268
GS = list(range(GF, G_LAST + 1))
G_SNAP_W = C.cap_g("ปี 1887")                   # 215: the year lands -> snap push
SNAP = (G_SNAP_W - 2, G_SNAP_W + 13)
PRESET, LIGHT = "site_wide", "DAY"
PPD = 128
EXT = 1.0                                      # the crane-down runs 2.6x the preset's end-pose travel (the preset pair is only 3 m apart)
ARC = -3.0                                     # deg/s orbit about the yard (parallax)
SLIDE = 45.0                                   # px/s
WSCALE = 1.9                                   # riveter cards enlarged (wide camera, set rule: hand props x1.6-2.4); heads 45-55 px
BASE_PITCH = 3.5                               # deg UP: horizon + legs sit lower, the empty ground slab shrinks to <= 25 %
SNAP_TRUCK = 8.0                               # D: the snap trucks the camera sideways (visible speed-up) +
SNAP_PUSH = 0.12                               # of the yard distance
#                                  # px/s
WORKERS = [("w_a", "riveter_tongs", "worker_a", False), ("w_b", "riveter_hammer", "worker_b", True), ("w_c", "riveter_forge", "worker_c", False),
           ("w_d", "riveter_tongs", "worker_d", True), ("w_e", "riveter_hammer", "worker_e", False), ("w_g", "riveter_forge", "worker_g", True)]


class CranePath(C.CamPath):
    """crane DOWN: the preset site_wide camera -> the site_wide_end camera (9 m up, 12 m closer), extended 5 % past the end for the
    out-handle, eased so it is still moving on the first and last frame; + 40 px/s lateral slide at the yard depth and one eased
    SNAP push (x1.25 closer) on "ปี 1887"."""

    def __init__(self, A):
        self.l0, self.k0 = Vector(A["cams"]["site_wide"]["loc"]), Vector(A["cams"]["site_wide"]["look_at"])
        self.l1, self.k1 = Vector(A["cams"]["site_wide_end"]["loc"]), Vector(A["cams"]["site_wide_end"]["look_at"])
        yard = Vector(A["marks"]["worker_c"])
        C.CamPath.__init__(self, self.l0, yard, GF, G_LAST, push=0, decay=0.0)
        v = (self.k0 - self.l0).normalized()
        self.rgt = Vector((v.y, -v.x, 0.0)).normalized()
        self.depth = (yard - self.l0).length

    def at(self, g):
        T = (G1 - GF) / 30.0
        t = (g - GF) / 30.0 / T
        u = 1.43 * t - 0.43 * t * t
        loc = self.l0.lerp(self.l1, u * EXT)
        look = self.k0.lerp(self.k1, u * EXT)
        slide = SLIDE * self.depth / C.F_PX * (g - GF) / 30.0               # px/s at the yard depth -> D
        loc, look = loc + self.rgt * slide, look + self.rgt * slide
        from mathutils import Matrix as _M
        R = _M.Rotation(math.radians(ARC * (g - GF) / 30.0), 3, "Z")        # orbit about the yard: parallax on the barrels / forges
        loc = self.subj0 + R @ (loc - self.subj0)
        look = self.subj0 + R @ (look - self.subj0)
        s = C.snap_u(g, SNAP[0], SNAP[1], 1.7)
        fw = (look - loc).normalized()
        loc = loc + fw * (SNAP_PUSH * self.depth * s) + self.rgt * (SNAP_TRUCK * s)
        look = look + fw * (SNAP_PUSH * self.depth * s) + self.rgt * (SNAP_TRUCK * s)
        v = look - loc
        r = Vector((v.y, -v.x, 0.0)).normalized()
        from mathutils import Matrix
        ang = self.pitch(g)
        return loc, loc + Matrix.Rotation(math.radians(ang), 3, r) @ v

    def pitch(self, g):
        """aim DOWN 4 deg (tilt up would sink the yard into the caption band), -7 more during the snap push (heads stay < 880)"""
        return BASE_PITCH - 4.0 * C.snap_u(g, SNAP[0], SNAP[1], 1.7)

    def tilt(self, g):
        return self.pitch(g)


def cam_path(A):
    return CranePath(A)


def cam_path_static():
    import site20
    A = dict(cams={n: dict(loc=CO.W(site20.CAMS_M[n]["loc"]), look_at=CO.W(site20.CAMS_M[n]["look"])) for n in ("site_wide", "site_wide_end")},
             marks={"worker_c": CO.W((-37.9, -164.2, 0.0))})
    return cam_path(A)


def worker_pose(kind, g, k):
    cast = kind
    """riveter cards at work: hammer swings (period 14 f), tongs turn, forge lift; breathing; never frozen."""
    ph = (g * 0.9 + k * 1.7)
    if kind == "riveter_hammer":
        a, b = cast20.STORY20["riveter_hammer_work"][1], cast20.STORY20["riveter_hammer_hit"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph), 0, 1) ** 2
        p = puppet.lerp_pose(cast, a, b, u)
    elif kind == "riveter_tongs":
        a, b = cast20.STORY20["riveter_tongs_work"][1], cast20.STORY20["riveter_tongs_throw"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.5), 0, 1)
        p = puppet.lerp_pose(cast, a, b, u)
    else:
        a = cast20.STORY20["riveter_forge_work"][1]
        b = cast20.STORY20["riveter_forge_lift"][1]
        p = puppet.lerp_pose(cast, a, b, clamp(0.5 - 0.5 * math.cos(ph * 0.4), 0, 1))
    p = dict(p)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.3 + k))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s03")
        for ob in C.bpy.data.objects:                               # the preset's black hook/block FG slab is a near-black mass: camera-invisible
            if ob.name in ("fg_dark_sh", "fg_metal_sh", "fg_redlead_sh"):
                ob.visible_camera = False
        self.path = cam_path(self.A)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.work = []
        for name, cast, mark, mirror in WORKERS:
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=dict(width=1.1, depth=0.5, opacity=0.8), cam=self.cam)
            self.actors[name] = a
            self.work.append((a, cast, C.on_ground(self.A["marks"][mark]), mirror))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            self.key_set(f)
            for a, cast, mk, mirror in self.work:
                C.place(a, f, mk, scale=WSCALE)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for i, (a, cast, mk, mirror) in enumerate(self.work):
                p = worker_pose(cast, g, i)
                if mirror:
                    p["mirror"] = True
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(a, PPD) for a, _, _, _ in self.work], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
        for r in rows[::6]:
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
