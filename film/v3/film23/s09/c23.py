#!/usr/bin/env python3
"""c23.py -- shared helpers for the film-23 take scripts (render team 2).  Adapted from v3/film8/common.py: cast23 + set3d23 (ghost.py).

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
    import c23 as C

* clock: g0/g1 from the plan (round(t*30)), render g0 .. g0 + ceil((g1-g0)*1.25), + in-handle frames.  Blender frame f = g - first_g + 1.
* Take: GH.build(shot, cards=False) (one location per process), our own camera keying (set3d23 move model, with the camera extrapolated
  backwards for the in-handle), stage Actors (real cast23 cards), contact shadows through GH.contact_shadow, per-frame sprites.
* final_loop: resumable raw/g_%04d.png + .json.
"""
import math, os, sys, json, time, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)) if os.path.basename(os.path.dirname(HERE)) == "film23" else os.path.dirname(HERE)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast23"), os.path.join(V3, "stage"), os.path.join(V3, "set3d23")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast23                                         # noqa: E402  (before sprites / actors)
import puppet                                         # noqa: E402,F401
import bpy                                            # noqa: E402
from mathutils import Vector                          # noqa: E402
import ghost as GH                                    # noqa: E402
import ghost_shots as SH                              # noqa: E402
import actors, camrig, render, sprites                # noqa: E402

FPS = 30


def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)


def lerp(a, b, t):
    return a + (b - a) * t


def sm(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def seg(g, a, b):
    """smoothstep progress of g between frames a and b."""
    return sm((g - a) / float(b - a)) if b > a else (1.0 if g >= b else 0.0)


def clock(sid, d_in=0):
    """the take's frame budget from the plan: g0, g1, g1_render (x1.25 tail), in-handle, first_g, n_frames, cam frames n."""
    sh = SH.SHOTS[sid]
    g0, g1 = int(round(sh["t0"] * FPS)), int(round(sh["t1"] * FPS))
    gr = g0 + int(math.ceil((g1 - g0) * 1.25))
    h_in = (int(math.ceil(d_in / 2.0)) + 2) if d_in else 0
    first = g0 - h_in
    return dict(g0=g0, g1=g1, g1_render=gr, h_in=h_in, first_g=first, n_frames=gr - first + 1, n_cam=SH.frames(sid))


# ----------------------------------------------------------------------------- the camera
def cam_pose_ext(sid, i, n):
    """camera pose at shot-local frame i (i < 0: the in-handle, linear extrapolation backwards from the start velocity)."""
    if i >= 0:
        return SH.pose(sid, min(i, n) / float(n) * 1.25)
    k = 3
    p0, p1 = SH.pose(sid, 0.0), SH.pose(sid, k / float(n) * 1.25)
    a = i / float(k)
    f = lambda u, v: tuple(x + (y - x) * a for x, y in zip(u, v))
    return dict(loc=f(p0["loc"], p1["loc"]), look_at=f(p0["look_at"], p1["look_at"]), lens=p0["lens"] + (p1["lens"] - p0["lens"]) * a)


def key_camera(sid, clk, tail_extra=0):
    """key the eased move on the scene camera (LINEAR keys, one per frame) from the in-handle to g1_render; frame = i + h_in + 1."""
    n = clk["n_cam"]
    cam = GH.shot_camera(sid, 0.0)
    cam.animation_data_clear()
    cd = cam.data
    prev = None
    for i in range(-clk["h_in"], clk["n_frames"] - clk["h_in"] + tail_extra):
        c = cam_pose_ext(sid, i, n)
        f = i + clk["h_in"] + 1
        cam.location = c["loc"]
        fwd = (Vector(c["look_at"]) - Vector(c["loc"])).normalized()
        cam.rotation_euler = fwd.to_track_quat("-Z", "Y").to_euler()
        if prev is not None:
            cam.rotation_euler.make_compatible(prev)
        prev = cam.rotation_euler.copy()
        cd.lens = c["lens"]
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("lens", frame=f)
    GH.STATE["PR"]._lin(cam)
    GH.STATE["PR"]._lin(cd)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, clk["n_frames"]
    sc.camera = cam
    return cam


# ----------------------------------------------------------------------------- actors
def make_actor(name, cast, sprite_dir, canvas=None):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=False, shadow="proxy")
    a.head_flip = False
    GH.no_bounce(a.card)
    a.card["gc_role"] = "card"
    return a


def place(a, f, xyz, scale=1.0, flip=False):
    a.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale, flip=flip)


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w)} head centre in screen px (720x1280) of every visible actor at Blender frame f."""
    out = {}
    take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch:
            continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, take.cam, (hx - radius, hy), f, res)
        r = actors.local_to_screen(a, take.cam, (hx + radius, hy), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
    return out


def gz(x, y, default=0.0, sink=0.035):
    """world height of the set surface under (x, y) (GH.ground_z), `sink` D into the grass (wheel contact rows read ~2 cm high otherwise)."""
    z = GH.ground_z(x, y)
    return (default if z is None else z) - sink


def tint_for(light):
    return dict(tint="#c8ccf0", ink="#1e142e") if light in ("NIGHT", "NIGHT_R", "PREDAWN") else {}


class Take(object):
    """one shot: build (no placeholders), camera keys, actors; subclasses implement staging(self, gs) which poses everything."""

    SID = None
    D_IN = 0

    def __init__(self, quality="preview", work=None):
        t0 = time.time()
        self.sid = self.SID
        self.tweak()
        self.clk = clock(self.sid, self.D_IN)
        self.A = GH.build(self.sid, cards=False)
        self.scene = bpy.context.scene
        GH.quality(None, "final" if quality == "final" else "preview")
        self.cam = key_camera(self.sid, self.clk)
        self.work = work or os.path.join(HERE, "work")
        self.sprite_dir = os.path.join(self.work, "sprites")
        os.makedirs(self.sprite_dir, exist_ok=True)
        self.actors, self.anch = {}, {}
        self.marks = GH.marks(self.sid)
        self.light = GH.STATE["light"]
        self.origin = Vector(GH.loc_origin())
        print("take %s: built in %.1f s" % (self.sid, time.time() - t0), flush=True)

    def tweak(self):
        """runtime changes to the shot table (camera end points, marks) before the build; override."""

    # frame helpers --------------------------------------------------------
    def f_of(self, g):
        return g - self.clk["first_g"] + 1

    def g_of(self, f):
        return f + self.clk["first_g"] - 1

    def local_i(self, g):
        return g - self.clk["g0"]

    def add(self, name, cast, canvas=None, shadow_r=0.9, shadow_d=0.42):
        a = make_actor(name, cast, self.sprite_dir, canvas)
        self.actors[name] = a
        return a

    def shadow_all(self):
        self.scene.frame_set(1)
        bpy.context.view_layer.update()
        for a in self.actors.values():
            if getattr(a, "no_shadow", False):
                continue
            GH.contact_shadow(a.card, 0.9, 0.42, follow=True)

    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            res = a.render_sprites(ppd, frames=frames)
            for f, r in zip(frames, res):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def run(TakeCls, argv=None):
    """CLI: probe a:b[:s] | stills a:b[:s] out_dir [scale] [samples] | final a:b[:s] [scale] [samples]   (a:b = film frames g; 'all' = whole take)"""
    argv = argv or sys.argv[1:]
    cmd = argv[0]
    clk = clock(TakeCls.SID, TakeCls.D_IN)
    spec = argv[1]
    gs = list(range(clk["first_g"], clk["g1_render"] + 1)) if spec == "all" else [g for g in parse(spec)]
    gs = [g for g in gs if clk["first_g"] <= g <= clk["g1_render"]]
    scale = float(argv[3]) if cmd == "final" and len(argv) > 3 else (float(argv[3]) if len(argv) > 3 else 0.5)
    samples = int(argv[4]) if len(argv) > 4 else (12 if cmd == "final" else 6)
    Tk = TakeCls("final" if cmd == "final" else "preview")
    if cmd == "ground":
        allg = list(range(clk["first_g"], clk["g1_render"] + 1))
        gs = [g for g in allg if (Tk.f_of(g) - 1) % 10 == 0 or g == allg[-1]]
        Tk.staging(gs)
        sys.path.insert(0, os.path.join(V3, "tools"))
        import ground_check as GC
        outp = os.path.join(TakeCls.HERE_DIR, "GROUND.md")
        extra = argv[2:] if len(argv) > 2 else []
        return GC.run_cli(["--every", "10", "--frame-list", ",".join(str(Tk.f_of(g)) for g in gs), "--out", outp] + extra)
    here = TakeCls.HERE_DIR if hasattr(TakeCls, "HERE_DIR") else HERE
    if cmd == "final":
        scale = float(argv[2]) if len(argv) > 2 else 1.0
        samples = int(argv[3]) if len(argv) > 3 else 12
        out = os.path.join(here, "raw")
        os.makedirs(out, exist_ok=True)
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js))
                ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
        if not todo:
            return
        Tk.staging(todo)
        GH.quality(None, "final")
        for g in todo:
            st = Tk.render([Tk.f_of(g)], out, scale=scale, samples=samples)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = Tk.report(g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
            json.dump(rep, open(png[:-4] + ".json.tmp", "w"))
            os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
        return
    Tk.staging(gs)
    for g in gs:
        print(json.dumps(Tk.report(g)), flush=True)
        if cmd == "stills":
            outd = argv[2]
            os.makedirs(outd, exist_ok=True)
            GH.quality(None, "preview", scale=scale, samples=samples)
            st = Tk.render([Tk.f_of(g)], outd, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(outd, "g_%04d.png" % g))
            print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
