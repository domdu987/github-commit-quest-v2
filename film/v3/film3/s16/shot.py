#!/usr/bin/env python3
"""shot.py -- film 3 take s16: shots 16 and 17 (NOON, the seam swells), harbor set NOON, painted brown.

    shot 16  g 1462..1581  10-frame dissolve in (handle g 1455..1461).  Raking close along the wall at the bucket seam: the plate
                           swells out of the wall line (fx bulge, groan pulses g 1495 / 1540 / 1570 with camera tremor), a
                           glossy drop forms and falls into the bucket; snap reframe on the groan g 1495; at "ดันผนังเหล็ก"
                           (g 1532) the camera cranes back and down to a low angle up the wall (the swelling plate low on the
                           five-storey tank), then a slow tilt up.
    shot 17  g 1582..1675  9-frame dissolve 16 -> 17 mixed in this take (g 1578..1586).  Close on the straining rivets of the
                           seam, one rivet trembles and creeps out; the camera pulls back g 1600..1617 and tommy's worried face
                           lands in the near foreground on "ทุกวัน" (53.8 s, g 1617); slow push, a second groan g 1650.
                           Hard cut out to s18 at g 1676 (no handle).

Blender frame of (shot s, film frame g) = 1000 * (s - 15) + g - 1400 (the shots overlap in the dissolve).
Set changes at runtime (fx.py, harbor.py untouched): a fine bulging copy of the hero patch (tank_patch hidden), 3D rivet heads over
the painted ones, an elongated glossy drip (the set's dot drop hidden).

    python3 shot.py probe 16|17 a:b:step
    python3 shot.py stills 16|17 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 16|17 a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d3"), os.path.join(PROJ, "v2", "shots"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402  (first: registers tommy & co)
import bpy                                              # noqa: E402
from mathutils import Vector, Quaternion               # noqa: E402
import fx                                               # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

H = fx.H
U = fx.HT.SEAM_U
TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G16, G17, G18 = 1462, 1582, 1676                 # round(t * 30) of 48.75, 52.75, 55.85
DISS_IN, DISS = 10, 9
H_IN = DISS_IN // 2 + 2                          # 7
HD = DISS // 2 + 2                               # 6
RANGES = {16: (G16 - H_IN, G17 + HD - 1), 17: (G17 - HD, G18 - 1)}
GROANS = [1495, 1540, 1570, 1610, 1650]
G_EXPAND = g_of(50.203)                          # 1509 "ขยายตัว"
G_PUSH = g_of(50.955)                            # 1532 "ดันผนังเหล็ก"
G_THIN = g_of(51.577)                            # 1550 "ที่บางเกินไป"
G_FACE = g_of(53.8)                              # 1617 tommy's face in the near foreground
G_RIVET = g_of(54.32)                            # 1633 "คือเสียงหมุด"
DRIPS = [(1455, 1500), (1500, 1548), (1548, 1592), (1592, 1636), (1636, 1680)]


def bf(shot, g):
    return 1000 * (shot - 15) + int(g) - 1400


# ----------------------------------------------------------------------------- state
def groan(g):
    return sum(pulse(g, s - 3, s + 2, s + 22, 1.0) for s in GROANS)


def bulge_amp(g):
    a = keys(g, [(1455, 0.04, "sine"), (G_EXPAND, 0.12, "sine"), (G_THIN, 0.30, "sine"), (1676, 0.44, "hold")])
    return a + 0.035 * groan(g)


def ridge(g):
    return 0.30 * bulge_amp(g) + 0.02 * groan(g)


def drip_phase(g):
    for a, b in DRIPS:
        if a <= g < b:
            return (g - a) / float(b - a)
    return 0.0


TREMBLE = None                                   # index of the trembling rivet (row of seam 1, just right of the bucket seam)


def rivet_fn(g):
    def fn(i, rv):
        if i != TREMBLE or g < 1590:
            return Vector((0, 0, 0)), None, True
        k = clamp((g - 1590) / 60.0) + 0.6 * groan(g)
        out = rv["n"] * (0.012 + 0.03 * clamp((g - 1590) / 85.0))
        jit = Vector((math.sin(g * 2.7), math.cos(g * 3.3), math.sin(g * 4.1 + 1))) * 0.006 * k
        q = Quaternion(Vector((math.sin(g * 1.9), math.cos(g * 2.3), 0)).normalized(), 0.18 * k * math.sin(g * 3.7))
        return out + jit, q, True
    return fn


# ----------------------------------------------------------------------------- cameras
def tremor(g, amp):
    k = amp * (0.25 + groan(g))
    return Vector((math.sin(g * 1.7) * 0.6 + math.sin(g * 3.1 + 2), 0.0, math.cos(g * 2.3) * 0.7 + math.sin(g * 4.3))) * k


def W(u, z, r=0.0):
    return fx.wall(U + u, z, fx.R + r)


CAM16 = [  # frame, loc, look, ease of the segment that starts here
    (1455, W(-3.15, 2.25, 1.65), W(0.35, 3.05), "sine"),
    (1490, W(-2.85, 2.35, 1.55), W(0.30, 3.05), "quint"),
    (1503, W(-2.45, 2.55, 1.45), W(0.15, 3.15), "sine"),
    (G_PUSH - 2, W(-2.30, 2.60, 1.42), W(0.12, 3.15), "quint"),
    (G_PUSH + 20, W(-1.10, 0.95, 6.2), W(0.35, 8.0), "sine"),
    (1588, W(-0.80, 0.90, 5.8), W(0.45, 10.2), "hold"),
]


def cam16(g):
    ks_l = [(f, tuple(l) + tuple(k), e) for f, l, k, e in CAM16]
    v = lerp(keys(g, ks_l), keys(g, [(f, x, "lin") for f, x, e in ks_l]), 0.15)
    loc, look = Vector(v[:3]), Vector(v[3:])
    d = (look - loc).length
    return loc + tremor(g, 0.0035 * d), look


TOMMY = None                                     # placed in Take (world feet point)


def cam17(g):
    rc = (W(-0.20, 3.02, 1.65), W(0.12, 3.0))                        # close on the rivets of the bucket seam
    rc2 = (W(-0.15, 3.02, 1.50), W(0.12, 3.0))
    face_l = W(-0.80, 1.95, 3.30); face_k = W(-0.52, 1.80, 0.0)
    ks = [(1576, tuple(rc[0]) + tuple(rc[1]), "sine"),
          (1601, tuple(rc2[0]) + tuple(rc2[1]), "quint"),
          (G_FACE, tuple(face_l) + tuple(face_k), "sine"),
          (1648, tuple(W(-0.83, 1.97, 3.22)) + tuple(W(-0.52, 1.83, 0.0)), "sine"),
          (1676, tuple(W(-0.85, 1.99, 3.15)) + tuple(W(-0.50, 1.86, 0.0)), "hold")]
    v = lerp(keys(g, ks), keys(g, [(f, x, "lin") for f, x, e in ks]), 0.15)
    loc, look = Vector(v[:3]), Vector(v[3:])
    d = (look - loc).length
    return loc + tremor(g, 0.0035 * d), look


CAMS = {16: cam16, 17: cam17}
TOMMY_FEET = W(-1.0, 0.0, 1.2)


def tommy_pose(g):
    cast, pose = cast3.STORY3["tommy_worried"]
    p = dict(pose)
    sh = groan(g)
    p["gaze"] = (0.55, -0.85)
    p["head_roll"] = 8 + 3 * math.sin(g * 0.13) + 4 * sh
    p["pitch"] = 0.45
    p["yaw"] = 0.25
    p["blink"] = blink(g, [1606, 1641, 1668])
    if g >= 1642:                                  # alarm grows: ring eyes from behind the blink at g 1641..1643
        p["expr"] = "stunned"
    p["squash"] = (1.0 - 0.02 * sh, 1.0 + 0.02 * sh)
    return p


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        global TREMBLE
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = H.build("NOON")
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 3000
        H.set_paint(1.0); H.set_seep(1.0); H.set_bucket(fill=0.72, visible=True); H.set_flood(0.0)
        fx.init(rivets=True, span=3.2, tracers=0, haze=0)
        best = None
        for i, rv in enumerate(fx.S["rivets"]):
            if rv["kind"] == "row1" and rv["z"] > 3 and rv["u"] > U + 0.15:
                if best is None or rv["u"] < fx.S["rivets"][best]["u"]:
                    best = i
        TREMBLE = best
        self.cam = camrig.make_camera(scene, name="cam_s16")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.tommy = actors.Actor("tommy", "tommy")
        self.tommy.build(sprites.DEFAULT_CANVAS["tommy"], sd, contact=True)
        self.tommy.head_flip = True                     # key from screen-right (the sun is behind the camera, a little right)
        H.T.no_bounce(self.tommy.card)
        self.anch = {}
        if verbose:
            print("s16: built in %.1f s" % (time.time() - t0), flush=True)

    def state(self, shot, g):
        fx.set_bulge(bulge_amp(g), ridge(g))
        fx.place_rivets(rivet_fn(g))
        fx.drip(drip_phase(g), k=0, land_z=0.035 + (H.BUCKET_H - 0.05) * 0.72)

    def key(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.tommy.place(f, tuple(TOMMY_FEET))

    def pose(self, shot, gs):
        self.key(shot, gs)
        self.tommy.set_hidden(shot != 17)
        if shot != 17:
            return
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.tommy.pose(f, tommy_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        for f, r in zip(fr, self.tommy.render_sprites(384, frames=fr)):
            self.anch[("tommy", f)] = r["anchors"]
            if r.get("clipped"):
                print("s16: WARNING tommy sprite clipped on frame %d" % f, flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[shot](g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   amp=round(bulge_amp(g), 3), heads={})
        a = self.tommy
        if self.tommy_visible(shot, g) and f in a.poses:
            res = a.feet.get(f)
            hx, hy = self.anch[("tommy", f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"]["tommy"] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if TREMBLE is not None:
            out["tremble_rivet"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(fx.S["rivets"][TREMBLE]["ob"].location), f)[:2]]
        out["seam"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(W(0, 3.0)), f)[:2]]
        return out

    def tommy_visible(self, shot, g):
        if shot != 17:
            return False
        loc, look = CAMS[shot](g)
        return (loc - fx.wall(U - 1.0, loc.z)).length > 1.75 and g >= 1600

    def render(self, shot, g, out_dir, scale=1.0, samples=12, threads=2):
        self.tommy.set_hidden(not self.tommy_visible(shot, g))
        self.scene.cycles.samples = samples
        self.scene.frame_set(bf(shot, g))
        self.state(shot, g)
        return render.render_frames([bf(shot, g)], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False, on_frame=lambda f: self.state(shot, g))[0]


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd == "probe":
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)))
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            st = Tk.render(shot, g, out, scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(quality="final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, g, out, scale=scale, samples=samples)
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
