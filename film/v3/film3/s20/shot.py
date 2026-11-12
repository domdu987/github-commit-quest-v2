#!/usr/bin/env python3
"""shot.py -- film 3 take s20: shot 20 (the end), harbor set NOON, painted brown, after the flood.

    shot 20  g 1856..1967  15-frame dissolve in (handle g 1847..1855, rendered in 3D).  Quiet: low and close on tommy's small
                           tin bucket, still in its place at the foot of the burst seam, brim-full and overflowing (dribbles down
                           its sides, a glossy puddle) in a sheet of molasses that covers the yard; the swollen plate and the
                           dark split seam above it; glossy elongated drops keep falling into it (ring on the surface each time).
                           Slow eased push in (with a constant-speed share: never static) to the last frame g 1967.

Blender frame = g - 1800.

    python3 shot.py stills 20 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 20 a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "set3d3"), os.path.join(V3, "stage"), os.path.join(PROJ, "v2", "shots"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import fx                                               # noqa: E402
import camrig, render                                   # noqa: E402
from anim import ease, keys, lerp, clamp                # noqa: E402

H = fx.H
U = fx.HT.SEAM_U


def g_of(t):
    return int(round((t + 0.10) * 30))


G20, N = 1856, 1968
H_IN = 15 // 2 + 2                               # 9
RANGES = {20: (G20 - H_IN, N - 1)}
DRIPS = [(1840, 1872), (1872, 1902), (1902, 1931), (1931, 1960), (1960, 1990)]
FILL_Z = 0.035 + (H.BUCKET_H - 0.05) * 1.0


def bf(shot, g):
    return int(g) - 1800


def W(u, z, r=0.0):
    return fx.wall(U + u, z, fx.R + r)


CAM = [(1847, W(-1.50, 2.05, 3.40), W(-0.05, 0.95, 0.45), "sine"),
       (g_of(63.196), W(-1.25, 1.85, 2.70), W(-0.02, 0.90, 0.45), "sine"),       # "ยังวางอยู่" 1899
       (1968, W(-1.00, 1.70, 2.05), W(0.0, 0.86, 0.45), "hold")]


def cam(g):
    ks = [(f, tuple(l) + tuple(k), e) for f, l, k, e in CAM]
    v = lerp(keys(g, ks), keys(g, [(f, x, "lin") for f, x, e in ks]), 0.35)
    return Vector(v[:3]), Vector(v[3:])


def drip_phase(g):
    for a, b in DRIPS:
        if a <= g < b:
            return (g - a) / float(b - a)
    return 0.0


def build_after(M):
    S = {}
    # molasses sheet over the yard round the foot of the wall (irregular edge), glossy
    M['sheet'] = fx.mat_glossy('S20_sheet', '#52200a', gloss=0.04, rough=0.2, rim=0.35)
    r = random.Random(20); c = H.wall_pt(H.TH_B, fx.R + 3.0); pts = []
    for i in range(72):
        a = 2 * math.pi * i / 72; rr = 7.0 * (1 + 0.12 * math.sin(3 * a + 1) + 0.06 * math.sin(7 * a)) + r.uniform(-0.3, 0.3)
        pts.append(Vector((c.x + rr * math.cos(a), c.y + rr * math.sin(a), 0.03)))
    mb = H.MB(); mb.oface(pts, M['sheet'], [(0, 0)] * len(pts), (0, 0, 1)); sh = mb.obj('s20_sheet', fx._coll()); fx.T.no_bounce(sh)
    # the concrete foot ring of the tank drowned in molasses (a glossy collar over it)
    mb = H.MB(); cc = H.TANK_C
    mb.frustum((cc[0], cc[1], -0.02), (cc[0], cc[1], 0.40), fx.R + 0.62, fx.R + 0.50, M['sheet'], seg=160, cap0=False, cap1=True)
    o = mb.obj('s20_collar', fx._coll(), smooth=True); fx.T.no_bounce(o)
    # puddle blobs on the sheet (slightly raised rims catch the light)
    for k in range(10):
        p = c + Vector((r.uniform(-5, 5), r.uniform(-5, 5), 0)); rr = r.uniform(0.3, 0.9)
        q = [Vector((p.x + rr * math.cos(2 * math.pi * i / 14) * r.uniform(0.85, 1.1), p.y + rr * 0.7 * math.sin(2 * math.pi * i / 14), 0.045)) for i in range(14)]
        mb = H.MB(); mb.oface(q, M['sheet'], [(0, 0)] * 14, (0, 0, 1)); o = mb.obj('s20_pud_%d' % k, fx._coll()); fx.T.no_bounce(o)
    # the split seam (dark jagged crack on the swollen plate)
    rr = random.Random(7); n = 26
    pts = [(0.25 + 6.5 * j / n, (0.05 if j % 2 else -0.05) + rr.uniform(-0.04, 0.04)) for j in range(n + 1)]
    co = []
    for z, du in pts:
        ww = 0.30 * (0.4 + 0.6 * math.sin(math.pi * clamp(z / 6.8)) ** 0.5)
        co.append(fx.wall_bulged(U + du - ww / 2, z, 0.02)); co.append(fx.wall_bulged(U + du + ww / 2, z, 0.02))
    me = bpy.data.meshes.new('s20_crack'); me.from_pydata([tuple(v) for v in co], [], [(2 * j, 2 * j + 1, 2 * j + 3, 2 * j + 2) for j in range(n)]); me.update()
    me.materials.append(M['crack']); o = bpy.data.objects.new('s20_crack', me); fx._coll().objects.link(o); fx.T.no_bounce(o)
    # the bucket's molasses (fill, dribbles, its puddle) in the same brown as the sheet (the set's reads magenta here)
    B = H.STATE['bucket']
    for ob in (B['fill'], B['over']):
        for i in range(len(ob.data.materials)): ob.data.materials[i] = M['sheet']
    return S


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = H.build("NOON")
        H.setup_render(scene, quality)
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 400
        H.set_paint(1.0); H.set_seep(1.0); H.set_bucket(fill=1.0, visible=True); H.set_flood(0.0)
        M = fx.init(rivets=True, span=3.2)
        fx.set_bulge(0.66, 0.2)
        r = random.Random(3)
        self.gone = set(i for i, rv in enumerate(fx.S["rivets"]) if abs(rv["u"] - U) < 2.2 and (abs(rv["z"] - 3) < 0.4 or rv["kind"] == "col") and r.random() < 0.85)
        fx.place_rivets(lambda i, rv: (Vector((0, 0, 0)), None, i not in self.gone))
        self.S = build_after(M)
        self.cam = camrig.make_camera(scene, name="cam_s20")
        self.cam.data.clip_start = 0.02
        if verbose:
            print("s20: built in %.1f s" % (time.time() - t0), flush=True)

    def state(self, g):
        fx.drip(drip_phase(g), k=0, land_z=FILL_Z)
        # a slow second drip running down the bucket's outside (overflow keeps coming)
        fx.S['drip'][1].hide_render = True

    def key(self, gs):
        for g in gs:
            loc, look = cam(g)
            camrig.key_camera(bf(20, g), loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")

    def report(self, g):
        loc, look = cam(g)
        f = bf(20, g); self.scene.frame_set(f)
        return dict(shot=20, g=g, cam=[round(c, 3) for c in loc],
                    bucket=[round(x, 1) for x in render.world_to_screen(self.cam, tuple(H.BUCKET_MARK), f)[:2]],
                    rim=[round(x, 1) for x in render.world_to_screen(self.cam, (H.BUCKET_MARK[0], H.BUCKET_MARK[1], H.BUCKET_H), f)[:2]])

    def render(self, g, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([bf(20, g)], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False, on_frame=lambda f: self.state(g))[0]


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
    gs = [g for g in parse(sys.argv[3]) if RANGES[20][0] <= g <= RANGES[20][1]]
    if cmd == "probe":
        Tk = Take(); Tk.key(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take(); Tk.key(gs)
        for g in gs:
            st = Tk.render(g, out, scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "s20_g_%04d.png" % g))
            print("shot 20 g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s20")
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
        print("final: shot 20, %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.key(todo)
            for g in todo:
                st = Tk.render(g, out, scale=scale, samples=samples)
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot 20 g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
