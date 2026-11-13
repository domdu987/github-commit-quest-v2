#!/usr/bin/env python3
"""tk.py -- small take toolkit for film 5 takes s08 / s09 / s11 (team 2), built on the s01 worked example.

A take module defines SHOTS = {sid: Spec}.  Each Spec (dict) has:
    name      label used in meta (e.g. "8a")
    g         (g0, g1) inclusive render range INCLUDING any handle frames
    cam       f(g) -> (loc Vector, look Vector)
    actors    {name: dict(cast, canvas, ppd, place=f(g)->Vector, pose=f(g)->dict, hands=f(g)->dict|None)}
    cage      "nail" (the set's 3D cage on its nail, the canary sprite INSIDE on the perch) | "hidden" (a person holds the 2D cage)
    bird      f(g) -> canary pose dict (cage "nail" only), bird_ppd
    tally     None | 1 | 5 | 10   (chalk tally marks on the pit prop under the cage nail)
    lamps     f(T, g, f) -> {lamp_name: (pos, strength)}  (anchors of this frame in T.anch)
    lens      optional focal length (default 22)
NO depth of field anywhere (client rule): M.setup_dof(scene, None, None, cam=...) at build and before every render.
Blender frame of (sid, g) = 2000 * sid + g + 1 (sid >= 0).
"""
import math, os, sys, time, json, wave

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402  (first: registers alfie, gaffer, miners, canary)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TP = M.TP
LAMP_NAMES = ("lamp_a", "lamp_b", "lamp_c", "lamp_d", "lamp_e", "lamp_f")
CANVAS = {"alfie": (-1.875, -3.875, 1.875, 0.1875), "gaffer": (-2.125, -4.75, 2.125, 0.125),
          "miner1": (-1.9375, -4.875, 1.9375, 0.125), "miner2": (-2.0, -4.3125, 2.0, 0.125),
          "miner3": (-1.9375, -4.9375, 1.9375, 0.125), "canary": (-0.75, -1.25, 0.875, 0.125)}


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


def bf(sid, g):
    return 2000 * sid + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def lerpv(a, b, u):
    return a + (b - a) * u


def cam_keys(g, ks):
    """ks = [(g, (loc, look), ease_kind)] -> (loc, look) eased."""
    k = keys(g, [(a, tuple(l) + tuple(t), e) for a, (l, t), e in ks])
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- lip sync from the narration
_WAV = {}


def narration_level(t0, t1):
    """RMS (0..1) of the narration between narration seconds t0..t1."""
    if "x" not in _WAV:
        import array
        w = wave.open(os.path.join(PROJ, "film5", "audio", "narration_bankky.wav"))
        a = array.array("h", w.readframes(w.getnframes()))
        _WAV["x"], _WAV["sr"] = a, w.getframerate()
    a, sr = _WAV["x"], _WAV["sr"]
    i0, i1 = max(0, int(t0 * sr)), min(len(a), int(t1 * sr))
    if i1 <= i0:
        return 0.0
    s = 0.0
    for v in a[i0:i1:8]:
        s += v * v
    return math.sqrt(s / max(1, len(range(i0, i1, 8)))) / 32768.0


def lipsync(g, g_on, g_off):
    """mouth name for frame g of a quoted line spoken g_on..g_off (new drawing every 2 frames; silent = flat)."""
    if g < g_on or g > g_off:
        return None
    b = (g - g_on) // 2
    gb = g_on + 2 * b
    t = gb / 30.0 - 0.10
    lv = narration_level(t, t + 2 / 30.0)
    if lv < 0.012:
        return "flat"
    if b % 5 == 3:
        return "talk_o"
    return "talk_b" if lv > 0.05 else "talk_a"


# ----------------------------------------------------------------------------- chalk tally
def tally_png(n, path, px=512):
    """chalk tally marks (groups of four strokes + a diagonal), stacked groups, on a transparent strip 0.22 x 0.50 D."""
    from PIL import Image, ImageDraw, ImageFilter
    import random
    W, H = int(px * 0.22), int(px * 0.50)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    rnd = random.Random(1905 + n)
    col = (236, 232, 218, 235)
    gh = int(px * 0.17)                    # stroke height
    lw = max(3, int(px * 0.016))
    groups = []
    k = n
    while k > 0:
        groups.append(min(5, k)); k -= 5
    for gi, cnt in enumerate(groups):
        y0 = H - int(px * 0.04) - (gi + 1) * gh - gi * int(px * 0.05)
        xs = [int(W * (0.17 + 0.19 * i)) for i in range(4)]
        for i in range(min(cnt, 4)):
            x = xs[i] + rnd.randint(-2, 2)
            for j in range(3):             # a slightly rough chalk stroke: 3 thin passes
                dx0, dx1 = rnd.uniform(-1.5, 1.5), rnd.uniform(-2.5, 2.5)
                dr.line([(x + dx0, y0 + rnd.uniform(0, 3)), (x + dx1 + 2, y0 + gh - rnd.uniform(0, 3))], fill=col, width=lw - j)
        if cnt == 5:
            for j in range(3):
                dr.line([(xs[0] - int(px * 0.03), y0 + gh * 0.80 + rnd.uniform(-2, 2)),
                         (xs[3] + int(px * 0.03), y0 + gh * 0.22 + rnd.uniform(-2, 2))], fill=col, width=lw - j)
    # chalk grain: knock random holes out of the strokes
    px_ = im.load()
    for _ in range(W * H // 6):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g_, b, a = px_[x, y]
        if a:
            px_[x, y] = (r, g_, b, int(a * rnd.uniform(0.2, 0.8)))
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(path)
    return path


def make_tally(n, png_dir):
    """a plane shrink-wrapped onto the pit prop above the cage nail (leg of set 6, y ~16.35, its face at x ~-0.36), chalk image
    as a dim emission over the timber (chalk is matte: it takes a little of the lamp light through a diffuse mix)."""
    os.makedirs(png_dir, exist_ok=True)
    path = tally_png(n, os.path.join(png_dir, "tally_%d.png" % n))
    w, h = 0.22, 0.50
    yc, zc = 16.35, 3.70
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=12, y_subdivisions=24, size=1.0, location=(0.2, yc, zc))
    ob = bpy.context.active_object
    ob.name = "tally_%d" % n
    ob.rotation_euler = (math.radians(90), 0, math.radians(90))      # plane normal -> +x (faces into the tunnel)
    ob.scale = (w, h, 1)
    sw = ob.modifiers.new("wrap", "SHRINKWRAP")
    sw.target = bpy.data.objects["timber_sets"] if "timber_sets" in bpy.data.objects else [o for o in bpy.data.objects if o.name.startswith("timber_s")][0]
    sw.wrap_method = "PROJECT"; sw.use_negative_direction = True; sw.use_positive_direction = True
    sw.use_project_z = True; sw.offset = 0.004
    m = bpy.data.materials.new("tally_mat_%d" % n)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(path); tex.interpolation = "Cubic"
    tex.extension = "CLIP"
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 0.62
    em.inputs["Color"].default_value = (0.86, 0.85, 0.80, 1)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.blend_method = "BLEND"
    except Exception:
        pass
    ob.data.materials.append(m)
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_glossy = False
    ob.hide_render = True
    return ob


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, shots, tag, quality="preview", verbose=True):
        t0 = time.time()
        self.shots, self.tag = shots, tag
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = M.build("tunnel")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 30000
        self.cam = camrig.make_camera(scene, name="cam_" + tag)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        self.actors, self.anch, self.lamps = {}, {}, {}
        sd = os.path.join(HERE, "work", "sprites")
        need = {}
        for s in shots.values():
            for n, a in s.get("actors", {}).items():
                need[n] = a["cast"]
            if s.get("cage") == "nail":
                need["bird"] = "canary"
        for n, cast in sorted(need.items()):
            a = actors.Actor(n, cast)
            if n == "bird":
                a.build(CANVAS["canary"], sd, shadow=None)
            else:
                a.build(CANVAS[cast], sd, contact=True)
            a.head_flip = False
            M.no_bounce(a.card)
            self.actors[n] = a
        self.cage_obj = bpy.data.objects.get("canary_cage")
        c = self.A["cage"]
        self.perch = Vector(c["perch"])
        self._drop_cross_dowel()
        self.tallies = {}
        for s in shots.values():
            n = s.get("tally")
            if n and n not in self.tallies:
                self.tallies[n] = make_tally(n, os.path.join(HERE, "work"))
        if verbose:
            print("%s: built tunnel + %d actors in %.1f s" % (tag, len(self.actors), time.time() - t0), flush=True)

    def _drop_cross_dowel(self):
        """runtime (set file untouched): remove the cage's second wooden dowel (0.15 D above the perch, pointing at the camera in the
        inserts) so no bar cuts through the canary's body; the perch under its feet stays."""
        import bmesh
        ob = self.cage_obj
        if ob is None:
            return
        mw = ob.matrix_world
        zc = self.perch.z - 0.012 + 0.16
        bm = bmesh.new(); bm.from_mesh(ob.data)
        kill = []
        for v in bm.verts:
            w = mw @ v.co
            if abs(w.z - zc) < 0.011 and math.hypot(w.x - self.perch.x, w.y - self.perch.y) < 0.2375:
                kill.append(v)
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        bm.to_mesh(ob.data); bm.free()
        self.dowel_removed = len(kill)

    def visible(self, sid):
        s = self.shots[sid]
        on = set(s.get("actors", {}).keys())
        if s.get("cage") == "nail":
            on.add("bird")
        for n, a in self.actors.items():
            a.set_hidden(n not in on)
        if self.cage_obj is not None:
            self.cage_obj.hide_render = s.get("cage") != "nail"
        for n, ob in self.tallies.items():
            ob.hide_render = s.get("tally") != n
        self.cam.data.lens = s.get("lens", 22)

    def pose(self, sid, gs):
        s = self.shots[sid]
        self.visible(sid)
        for g in gs:
            f = bf(sid, g)
            loc, look = s["cam"](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            M.set_drips(f)
            M.set_gas(0.0, frame=f)
            M.set_cage(None, frame=f, swing=s.get("swing", lambda g: 0.0)(g))
            for n, a in s.get("actors", {}).items():
                self.actors[n].place(f, tuple(a["place"](g)))
            if s.get("cage") == "nail":
                self.actors["bird"].place(f, tuple(self.perch))
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            for n, a in s.get("actors", {}).items():
                hands = a["hands"](g) if a.get("hands") else None
                self.actors[n].pose(f, a["pose"](g), hands=hands, camera=self.cam)
            if s.get("cage") == "nail":
                self.actors["bird"].pose(f, s["bird"](g), camera=self.cam)
        fr = [bf(sid, g) for g in gs]
        jobs = [(self.actors[n], a["ppd"]) for n, a in s.get("actors", {}).items()]
        if s.get("cage") == "nail":
            jobs.append((self.actors["bird"], s.get("bird_ppd", 1024)))
        for a, ppd in jobs:
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("%s: WARNING sprite of %s clipped on frame %d" % (self.tag, a.name, f), flush=True)
        self.key_lamps(sid, gs)

    def world(self, name, sid, g, anchor):
        f = bf(sid, g)
        a = self.actors[name]
        return actors.local_to_world(a, self.anch[(name, f)][anchor], f)

    def key_lamps(self, sid, gs):
        s = self.shots[sid]
        for g in gs:
            f = bf(sid, g)
            self.scene.frame_set(f)
            on = s["lamps"](self, g, f) if s.get("lamps") else {}
            for name in LAMP_NAMES:
                pos, k = on.get(name, (Vector((0, -30, 1)), 0.0))
                self.lamps[name] = M.lamp_light(tuple(pos), k, frame=f, name=name)

    def report(self, sid, g):
        s = self.shots[sid]
        f = bf(sid, g)
        self.scene.frame_set(f)
        loc, look = s["cam"](g)
        v = look - loc
        out = dict(shot=s["name"], sid=sid, g=g, cam=[round(c, 3) for c in loc],
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads={})
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            hr = 0.5 if a.name != "bird" else 0.09
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - hr, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + hr, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if s.get("cage") == "nail":
            c = self.A["cage"]
            pts = {"perch": c["perch"], "hook": c["hook"]}
            out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(sid)
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(sid, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(SHOTS, tag, argv):
    """python3 shot.py probe|stills|final <sids> <g spec|all> [out_dir|scale] [scale] [samples]"""
    cmd = argv[1]
    sids = [int(s) for s in argv[2].split(",")]
    T = None
    if cmd in ("probe", "stills"):
        T = Take(SHOTS, tag, "preview")
        for sid in sids:
            g0, g1 = SHOTS[sid]["g"]
            gs = [g for g in parse(argv[3]) if g0 <= g <= g1] if argv[3] != "all" else []
            if not gs:
                gs = [g0, (g0 + g1) // 2, g1]
            T.pose(sid, gs)
            for g in gs:
                print(json.dumps(T.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(argv[5]) if len(argv) > 5 else 0.5
                    samples = int(argv[6]) if len(argv) > 6 else 6
                    st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "%s_g_%04d.png" % (SHOTS[sid]["name"], g)))
                    print("shot %s g %d  %.1f s wall %.1f cpu" % (SHOTS[sid]["name"], g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        for sid in sids:
            g0, g1 = SHOTS[sid]["g"]
            gs = [g for g in parse(argv[3]) if g0 <= g <= g1] if argv[3] != "all" else list(range(g0, g1 + 1))
            out = os.path.join(HERE, "raw", SHOTS[sid]["name"])
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %s, %d to render, %d done" % (SHOTS[sid]["name"], len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if T is None:
                T = Take(SHOTS, tag, "final")
            T.pose(sid, todo)
            for g in todo:
                st = T.render(sid, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = T.report(sid, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %s g %d  %.1f s wall  %.1f s cpu" % (SHOTS[sid]["name"], g, st["wall"], st["cpu"]), flush=True)
