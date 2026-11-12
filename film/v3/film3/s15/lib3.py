#!/usr/bin/env python3
"""lib3.py -- shared helpers of render worker 3 (film 3 takes s11, s12, s13, s15).  The same file is copied into each take folder
(identical copies, so every take folder is self-contained).  Built on the film-2 take structure (v3/film2/s01/shot.py):

  * clock: g_of(t) = round((t + 0.1) * 30) for events; shot boundaries round(t * 30)
  * BaseTake: builds the harbor set (v3/set3d3/harbor.py) for one preset, the 22 mm camera keyed per frame (LINEAR), cast3 actors
    on cards, per-frame set changes through render_frames' on_frame (snowfall, drip, ghosts, ...), resumable final renders into
    raw/s<shot>/g_%04d.png + .json, stills, probe
  * runtime set fixes (harbor.py is never edited): shade-only foreground masses, an animated glossy drip, snowfall, snow heaps that
    settle or melt, wet melt puddles
  * deliver(): frames/ (dissolves mixed inside a take), take.mkv, contact.jpg, meta.json, cues.json
"""
import math, os, sys, time, json, glob, shutil, random, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d3"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402  (first: registers tommy, foreman, workers, kids)
import bpy                                              # noqa: E402
import numpy as np                                      # noqa: E402
from mathutils import Vector                            # noqa: E402
import harbor as H                                      # noqa: E402
import tower as T                                       # noqa: E402  (H's template; materials)
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp, smoothstep_mix   # noqa: E402,F401

FPS = 30


def g_of(t):
    """narration time -> film frame of an event"""
    return int(round((t + 0.10) * 30))


def gb(t):
    """plan time -> film frame of a shot boundary"""
    return int(round(t * 30))


def V(*a):
    return Vector(a[0]) if len(a) == 1 else Vector(a)


def sph(look, dist, yaw, pitch):
    """camera position at `dist` from `look`, looking along yaw (deg, clockwise from +y) and pitch (deg, + up)"""
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return Vector(look) - d * dist


def cam_basis(loc, look):
    f = (Vector(look) - Vector(loc)).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f).normalized()
    return f, r, u


def head_flip_for(loc, look):
    """key from screen-right -> True (thick head side lower-left).  The key travels along key_dir."""
    kd = Vector(H.STATE["P"]["key_dir"]).normalized()
    f, r, u = cam_basis(loc, look)
    return kd.dot(r) < 0.0          # light travelling toward screen-left = coming from screen-right


def mkeys(g, ks, lin=0.15):
    """eased keys mixed with a constant-speed share (the camera never parks inside a move)"""
    a = keys(g, ks)
    b = keys(g, [(f, v, "lin") for f, v, e in ks])
    return lerp(a, b, lin)


MOUTH_SEQ = ["talk_a", "talk_b", "talk_a", "flat", "talk_o", "talk_b", "talk_a", "talk_b", "flat", "talk_a", "talk_o", "talk_b"]


def mouth_at(g, g0, g1):
    """lip-sync cycle inside a quoted line [g0, g1]: a new drawing every 2 frames; None (closed, expr default) outside"""
    if g < g0 or g > g1:
        return None
    return MOUTH_SEQ[((g - g0) // 2) % len(MOUTH_SEQ)]


def walk_legs(g, phase=0.0, period=16, stride=0.75):
    """a two-drawing walk: legs alternate every half period, a little body bob"""
    s = math.sin(2 * math.pi * (g / float(period)) + phase)
    st = stride * (1 if s >= 0 else -1) * (0.55 + 0.45 * abs(s))
    return dict(preset="step", stride=st, lift_l=0.35 if s > 0.3 else 0.0, lift_r=0.35 if s < -0.3 else 0.0), abs(s)


# ----------------------------------------------------------------------------- geometry helpers
def box(name, lo, hi, mat, coll, uv_tile=2.0):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if abs(n.z) > 0.5:
                uv.data[li].uv = (co.x / uv_tile, co.y / uv_tile)
            elif abs(n.x) > 0.5:
                uv.data[li].uv = (co.y / uv_tile, co.z / uv_tile)
            else:
                uv.data[li].uv = (co.x / uv_tile, co.z / uv_tile)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [k.name for k in bpy.context.scene.collection.children]:
        bpy.context.scene.collection.children.link(c)
    return c


def tex(name):
    return H.STATE["tx"][name]


def shade_mat(name, image=None, color="#6a4a3a", gain=0.0, shade_mul=0.42):
    """a set material painted in the preset's blue-violet shade only (key gain 0): a foreground mass standing in shade"""
    return T.mat_lit("W3_" + name, color=color, image=image, gain=gain, shade_mul=shade_mul, form=(0.0, -0.05, 0.22))


def emit_mat(name, rgb, strength=1.0, alpha=1.0):
    """flat emission colour (linear rgb) mixed with transparent by alpha; alpha / colour can be changed per frame via
    m['alpha_node'] / m['emit_node']"""
    m = bpy.data.materials.get(name)
    if m is not None:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    em.inputs["Color"].default_value = (*rgb, 1.0); em.inputs["Strength"].default_value = strength
    mx.inputs[0].default_value = alpha
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    m["alpha_node"] = mx.name; m["emit_node"] = em.name
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    return m


def set_emit(m, rgb=None, alpha=None, strength=None):
    nt = m.node_tree
    if alpha is not None:
        nt.nodes[m["alpha_node"]].inputs[0].default_value = float(alpha)
    em = nt.nodes[m["emit_node"]]
    if rgb is not None:
        em.inputs["Color"].default_value = (*rgb, 1.0)
    if strength is not None:
        em.inputs["Strength"].default_value = float(strength)


def srgb_lin(c):
    c = c / 255.0 if c > 1 else c
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexlin(h):
    h = h.lstrip("#")
    return tuple(srgb_lin(int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4))


# ----------------------------------------------------------------------------- drip: a glossy elongated drop that falls into the bucket
class Drip(object):
    """The set's seep_drop (a dark dot) is hidden and replaced by an animated glossy drop: it swells at the end of the bucket
    strip, stretches, falls to the bucket rim (gravity), then the next one grows.  Every `period` frames, starting at `phase`."""

    def __init__(self, period=24, phase=0, r=0.045):
        H.STATE["drop"].hide_render = True
        H.STATE["drop"].animation_data_clear()
        mb = H.MB(); mb.sphere((0.0, 0.0, 0.0), r, H.STATE["M"]["seep"], seg=12, rings=8)
        self.ob = mb.obj("w3_drop", collection("W3_FX")); T.no_bounce(self.ob)
        self.top = H.wall_pt(H.TH_B, H.TANK_R + 0.07, 2.88 - 0.78 * max(0.3, H.STATE.get("seep_a", 0.6)) - 0.03)
        self.bot_z = H.BUCKET_H + 0.04
        self.period, self.phase = period, phase

    def fall_frame(self, g):
        return (g - self.phase) % self.period

    def update(self, g, floor_z=None):
        k = self.fall_frame(g); grow = self.period - 6
        if k < grow:                                   # swelling, hanging from the strip end
            u = k / float(grow)
            s = 0.5 + 0.75 * u
            self.ob.scale = (s, s, s * (1.5 + 1.0 * u))
            z = self.top.z - 0.045 * self.ob.scale[2]
        else:                                          # falling (accelerating), stretched
            u = (k - grow + 1) / 6.0
            bz = self.bot_z if floor_z is None else floor_z
            z = self.top.z - 0.06 - (self.top.z - 0.06 - bz) * u * u
            self.ob.scale = (0.95, 0.95, 2.8 + 1.6 * u)
        self.ob.location = (self.top.x, self.top.y, z)

    def impacts(self, g0, g1):
        return [g for g in range(g0, g1 + 1) if self.fall_frame(g) == self.period - 1]


# ----------------------------------------------------------------------------- snowfall
class Snowfall(object):
    """N flakes in a world box, falling with a wobble; one mesh of camera-facing quads rebuilt per frame (deterministic in g).
    Flake size grows with distance to the camera so far flakes stay visible and near ones never fill the frame."""

    def __init__(self, n, lo, hi, speed=1.4, seed=11, coll=None, near=1.5, size=(0.035, 0.0075), alpha=0.92):
        r = random.Random(seed)
        self.n = n; self.lo = Vector(lo); self.hi = Vector(hi); self.speed = speed; self.near = near; self.size = size
        self.p0 = [Vector((r.uniform(lo[0], hi[0]), r.uniform(lo[1], hi[1]), r.uniform(lo[2], hi[2]))) for _ in range(n)]
        self.sp = [r.uniform(0.7, 1.3) for _ in range(n)]
        self.ph = [r.uniform(0, 6.28) for _ in range(n)]
        self.sz = [r.uniform(0.7, 1.35) for _ in range(n)]
        me = bpy.data.meshes.new("snowfall")
        K = self.K = 8
        vs = [(0, 0, 0)] * (K * n); fs = [tuple(K * i + k for k in range(K)) for i in range(n)]
        me.from_pydata(vs, [], fs); me.update()
        self.mat = emit_mat("W3_snowflake", hexlin("#f4f6ff"), 1.0, alpha)
        me.materials.append(self.mat)
        self.ob = bpy.data.objects.new("snowfall", me)
        (coll or collection("W3_FX")).objects.link(self.ob)
        self.ob.visible_shadow = False; T.no_bounce(self.ob)

    def update(self, g, cam_loc, cam_look):
        f, r, u = cam_basis(cam_loc, cam_look)
        t = g / float(FPS)
        H_ = self.hi.z - self.lo.z
        K = self.K
        co = np.zeros((K * self.n, 3), dtype=np.float32)
        ring = [(math.cos(2 * math.pi * k / K), math.sin(2 * math.pi * k / K)) for k in range(K)]
        cl = Vector(cam_loc)
        for i in range(self.n):
            p = self.p0[i]
            z = self.lo.z + ((p.z - self.lo.z - self.speed * self.sp[i] * t) % H_)
            x = p.x + 0.35 * math.sin(1.3 * t + self.ph[i]) + 0.4 * t
            y = p.y + 0.25 * math.cos(0.9 * t + self.ph[i] * 1.7)
            q = Vector((x, y, z))
            d = (q - cl).dot(f)
            if d < self.near:
                co[K * i:K * i + K] = (0, 0, -50)
                continue
            s = (self.size[0] + self.size[1] * d) * self.sz[i]
            for k, (a, b) in enumerate(ring):
                v = q + r * (a * s * 0.5) + u * (b * s * 0.5)
                co[K * i + k] = (v.x, v.y, v.z)
        self.ob.data.vertices.foreach_set("co", co.ravel())
        self.ob.data.update()


# ----------------------------------------------------------------------------- snow heaps settle / melt
def snow_objects():
    return [o for o in (bpy.data.objects.get("snow_heaps"), bpy.data.objects.get("snow_patches")) if o is not None]


def set_snow_depth(k):
    """scale the kerb / sidewalk heaps in height (k 0.25..1.3), about z = 0"""
    o = bpy.data.objects.get("snow_heaps")
    if o is not None:
        o.scale = (1.0, 1.0, max(0.05, k))


class Puddles(object):
    """wet melt-water patches on the street and yard (dark glossy blue-grey blobs that grow): a WARM morning cue"""

    def __init__(self, centres, seed=5, coll=None):
        r = random.Random(seed)
        P = H.STATE["P"]
        m = H._add_gloss(T.mat_lit("W3_wet", "#6f86b8", gain=0.75, shade_mul=1.0, form=None), 0.6, 0.06, (1.0, 0.95, 0.85))
        self.obs = []
        for i, (cx, cy, z, rx, ry) in enumerate(centres):
            mb = H.MB()
            pts = []
            n = 14
            for j in range(n):
                a = 2 * math.pi * j / n; k = 1 + 0.22 * math.sin(3 * a + r.uniform(0, 6)) + r.uniform(-0.08, 0.08)
                pts.append((rx * k * math.cos(a), ry * k * math.sin(a), 0.0))
            mb.oface(pts, m, [(0, 0)] * n, (0, 0, 1))
            ob = mb.obj("wet_%d" % i, coll or collection("W3_FX"))
            ob.location = (cx, cy, z + 0.10)
            T.no_bounce(ob); ob.visible_shadow = False
            self.obs.append(ob)

    def update(self, k):
        for i, ob in enumerate(self.obs):
            s = max(0.02, clamp(k * 1.15 - 0.05 * i % 0.3))
            ob.scale = (s, s, 1.0)
            ob.hide_render = s < 0.05


# ----------------------------------------------------------------------------- the take base class
def bf(si, g):
    """Blender frame of (shot index si, film frame g): shots of one take overlap in their dissolves"""
    return 10000 * si + int(g) + 1


class BaseTake(object):
    PRESET = "WINTER"
    SHOTS = {}           # shot -> (first g rendered, last g rendered) incl. handles
    PAINT = 1.0
    SEEP = 0.6
    BUCKET = dict(fill=0.3, visible=True)

    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = H.build(self.PRESET)
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 16
        scene.frame_start, scene.frame_end = 1, 100000
        H.set_paint(self.PAINT); H.set_seep(self.SEEP); H.set_bucket(**self.BUCKET)
        self.camera = camrig.make_camera(scene, name="cam_w3")
        self.camera.data.clip_start = 0.02
        self.camera.data.clip_end = 600
        self.sd = os.path.join(HERE, "work", "sprites")
        self.actors = {}
        self.info = {}
        self.anch = {}
        self.fx = collection("W3_FX")
        self.setup()
        if verbose:
            print("%s: built %s in %.1f s" % (os.path.basename(HERE), self.PRESET, time.time() - t0), flush=True)

    # --- to override
    def setup(self):
        pass

    def cam(self, shot, g):
        raise NotImplementedError

    def cast_in(self, shot):
        """actor names visible in a shot"""
        return []

    def place(self, shot, name, g):
        raise NotImplementedError

    def pose(self, shot, name, g):
        raise NotImplementedError

    def hands(self, shot, name, g):
        return None

    def ppd(self, shot, name):
        return 256

    def per_frame(self, shot, g):
        pass

    def visible(self, shot):
        pass

    # --- machinery
    def actor(self, name, cast=None, contact=True):
        if name not in self.actors:
            a = actors.Actor(name, cast or name)
            a.build(sprites.DEFAULT_CANVAS[cast or name], self.sd, contact=contact)
            T.no_bounce(a.card)
            self.actors[name] = a
        return self.actors[name]

    def si(self, shot):
        return sorted(self.SHOTS).index(shot)

    def stage(self, shot, gs):
        si = self.si(shot)
        names = self.cast_in(shot)
        for n, a in self.actors.items():
            a.set_hidden(n not in names)
        self.visible(shot)
        for g in gs:
            f = bf(si, g)
            loc, look = self.cam(shot, g)
            camrig.key_camera(f, tuple(loc), tuple(look), cam=self.camera, interp="LINEAR", easing="AUTO")
            for n in names:
                self.actors[n].place(f, tuple(self.place(shot, n, g)))
        for n in names:
            a = self.actors[n]
            for g in gs:
                f = bf(si, g)
                self.scene.frame_set(f)
                hf = head_flip_for(*self.cam(shot, g))
                a.head_flip = hf
                p = self.pose(shot, n, g)
                h = self.hands(shot, n, g)
                _, inf = a.pose(f, p, hands=h, camera=self.camera) if h else a.pose(f, p, camera=self.camera)
                if h:
                    self.info.setdefault((shot, g), {})[n] = {k: round(v["error"], 3) for k, v in inf.items() if isinstance(v, dict) and "error" in v}
            fr = [bf(si, g) for g in gs]
            for f, r in zip(fr, a.render_sprites(self.ppd(shot, n), frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("WARNING sprite of %s clipped on frame %d" % (n, f), flush=True)
        self.staged = (shot, list(gs))

    def report(self, shot, g):
        si = self.si(shot); f = bf(si, g)
        self.scene.frame_set(f)
        loc, look = self.cam(shot, g)
        v = Vector(look) - Vector(loc)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for n in self.cast_in(shot):
            a = self.actors[n]
            if f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(n, f)]["head"]
            c = actors.local_to_screen(a, self.camera, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.camera, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.camera, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out.update(self.info.get((shot, g), {}))
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        si = self.si(shot)
        self.visible(shot)
        self.scene.cycles.samples = samples

        def on_frame(f):
            g = f - 1 - 10000 * si
            self.per_frame(shot, g)
        return render.render_frames([bf(si, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.camera, verbose=False, on_frame=on_frame)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(TakeCls, argv):
    """python3 shot.py probe <shot> a:b:step | stills <shot> a:b:step <out> [scale] [samples] | final <shot> [a:b] [scale] [samples]"""
    cmd = argv[1]; shot = int(argv[2])
    lo, hi = TakeCls.SHOTS[shot]
    if cmd == "probe":
        gs = [g for g in parse(argv[3]) if lo <= g <= hi]
        Tk = TakeCls()
        Tk.stage(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)))
    elif cmd == "stills":
        gs = [g for g in parse(argv[3]) if lo <= g <= hi]
        out = argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(argv[5]) if len(argv) > 5 else 0.5
        samples = int(argv[6]) if len(argv) > 6 else 6
        Tk = TakeCls()
        Tk.stage(shot, gs)
        for g in gs:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s wall %.1f cpu  %s" % (shot, g, st["wall"], st["cpu"], json.dumps(Tk.report(shot, g)["heads"])), flush=True)
    elif cmd == "final":
        gs = [g for g in (parse(argv[3]) if len(argv) > 3 and argv[3] != "-" else range(lo, hi + 1)) if lo <= g <= hi]
        out = os.path.join(HERE, "raw", "s%d" % shot); os.makedirs(out, exist_ok=True)
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
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
            Tk = TakeCls(quality="final")
            Tk.stage(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)


# ----------------------------------------------------------------------------- delivery
def deliver(take, plan, meta_extra, cue_list):
    """plan: list of segments in film order: ("raw", shot, g_from, g_to) copy, ("mix", shotA, shotB, g_from, n) dissolve of n frames
    starting at g_from (smoothstep, as film 2).  Writes frames/, take.mkv, meta.json, cues.json, contact.jpg."""
    from PIL import Image, ImageDraw
    RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    src = {}

    def raw(s, g):
        return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)
    for seg in plan:
        if seg[0] == "raw":
            _, s, a, b = seg
            for g in range(a, b + 1):
                shutil.copyfile(raw(s, g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "s%d" % s
        else:
            _, sa, sb, a, n = seg
            for i in range(n):
                g = a + i; w = smoothstep_mix(i + 1, n)
                A_ = np.asarray(Image.open(raw(sa, g)).convert("RGB"), dtype=np.float32)
                B_ = np.asarray(Image.open(raw(sb, g)).convert("RGB"), dtype=np.float32)
                Image.fromarray(np.clip(A_ * (1 - w) + B_ * w + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, "g_%04d.png" % g))
                src[g] = "s%d*%.3f+s%d*%.3f" % (sa, 1 - w, sb, w)
    gsorted = sorted(src)
    assert gsorted == list(range(gsorted[0], gsorted[-1] + 1)), "gap in frames"
    first, last = gsorted[0], gsorted[-1]
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    rows = [json.load(open(j)) for j in glob.glob(os.path.join(RAW, "s*", "g_*.json"))]
    walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
    meta = {"take": take}
    meta.update(meta_extra)
    meta.update({"first_g": first, "n_frames": last - first + 1, "samples": 12, "resolution": [720, 1280], "threads": 2,
                 "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
                 "frame_source": {str(g): src[g] for g in gsorted}})
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    ev = []
    for c in cue_list:
        g0, g1, label, kind = c[:4]; kw = c[4] if len(c) > 4 else {}
        e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
        e.update(kw); ev.append(e)
    json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    nshow = 16
    gs = [int(round(first + i * (last - first) / (nshow - 1.0))) for i in range(nshow)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:14]), fill=(255, 255, 255))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)
    print("delivered %s: g %d..%d (%d frames); mean wall %.2f s, cpu %.2f s" % (take, first, last, last - first + 1, np.mean(walls), np.mean(cpus)))
    return src


def sheet(d, out, cols=6, pattern="*.png"):
    from PIL import Image, ImageDraw
    fs = sorted(glob.glob(os.path.join(d, pattern)))
    w = 240; h = int(w * 16 / 9); lab = 16
    rows = (len(fs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * (h + lab)), (20, 16, 24)); dr = ImageDraw.Draw(S)
    for i, f in enumerate(fs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 3, y + 2), os.path.basename(f)[:-4], fill=(255, 255, 255))
    S.save(out, quality=88)
    return out


# ----------------------------------------------------------------------------- QA numbers
def qa(ranges, main=None, extra_rows=()):
    """print QA numbers: per shot head sizes / positions (raw json), heads below y 880, render cost, pops, near-stills,
    magenta / black frames, hue rows.  ranges: {shot: (a, b)} of FINAL in-shot frames; main: {shot: name}"""
    sys.path.insert(0, os.path.join(V3, "tools"))
    import hue_report as HR
    from PIL import Image
    for s, (a, b) in sorted(ranges.items()):
        rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s%d" % s, "g_*.json")))]
        rows = [r for r in rows if a <= r["g"] <= b]
        print("shot %d (g %d..%d, %d frames)" % (s, a, b, len(rows)))
        names = sorted({n for r in rows for n in r["heads"]})
        for n in names:
            hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
            vis = [(g, h) for g, h in hs if -h["w"] / 2 < h["x"] < 720 + h["w"] / 2]
            if not vis:
                continue
            w = [h["w"] for g, h in vis]; y = [h["y"] for g, h in vis]; x = [h["x"] for g, h in vis]
            low = [g for g, h in vis if h["y"] + h["w"] / 2 > 880]
            print("  %-8s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s%s"
                  % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280,
                     ("%d frames, first %s" % (len(low), low[:3])) if low else "none", "  (MAIN)" if main and main.get(s) == n else ""))
        print("  render: wall %.2f s, cpu %.2f s per frame (mean of %d)" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]), len(rows)))
        print("  retried frames:", [r["g"] for r in rows if r.get("retried")])
    fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
    prev = None; d = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    g0 = int(os.path.basename(fs[0])[2:6])
    pops = []
    for i, v in enumerate(d):
        p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
        if v > 1.8 * p and v > 1.8 * n and v > 1.0:
            pops.append((g0 + i, g0 + i + 1, round(v, 1)))
    print("popcheck: pops (g -> g+1, change):", pops)
    print("near-still transitions (< 0.35 levels):", [g0 + i for i, v in enumerate(d) if v < 0.35])
    bad = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or a.mean() < 8:
            bad.append(os.path.basename(f))
    print("magenta / black frames:", bad)
    print()
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
    for s, (a, b) in sorted(ranges.items()):
        HR.row("%s shot %d (g %d-%d)" % (os.path.basename(HERE), s, a, b), fr(a, b))
    HR.row("%s all frames" % os.path.basename(HERE), fs)
    for lab, files in extra_rows:
        HR.row(lab, files)
