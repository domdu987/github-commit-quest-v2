"""fx.py -- shared helpers of takes s19, s20, s22 (film 2, render team 5): rain, camera-attached flash card, per-frame resumable
render loop, contact sheet, take assembly.  No actors in these takes: every frame is set explicitly from Python (no keyframes),
so a frame renders the same whatever was rendered before it in the process.

Clock: g = round((t + 0.10) * 30) for in-shot events; shot boundaries round(t * 30)."""
import math, os, sys, json, time, random, glob, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)


def g_of(t):
    return int(round((t + 0.10) * 30))


def g_cut(t):
    return int(round(t * 30))


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


# ----------------------------------------------------------------------------- bpy helpers (import bpy lazily)
def emit_mat(name, rgb, strength=1.0, additive=True, camera_only=True, alpha=None):
    """Unlit emission; additive = transparent + emission (adds light over what is behind)."""
    import bpy
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'strength'
    emi.inputs['Color'].default_value = (*rgb, 1.0); emi.inputs['Strength'].default_value = strength
    last = emi.outputs['Emission']
    if additive:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); ad = nt.nodes.new('ShaderNodeAddShader')
        L(tr.outputs['BSDF'], ad.inputs[0]); L(last, ad.inputs[1]); last = ad.outputs['Shader']
    if camera_only:
        lp = nt.nodes.new('ShaderNodeLightPath'); tr2 = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


def no_bounce(ob):
    ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_volume_scatter = False
    ob.visible_shadow = False
    return ob


def set_cam(cam, loc, look, roll=0.0):
    from mathutils import Vector
    cam.location = Vector(loc)
    fwd = (Vector(look) - Vector(loc)).normalized()
    cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if roll:
        cam.rotation_euler.rotate_axis('Z', math.radians(roll))


class Rain(object):
    """Rain streaks as one mesh of camera-facing quads, rebuilt every frame in a world box that follows the camera.
    Deterministic in g. Emission, camera rays only, additive (pale blue)."""

    def __init__(self, n=1400, size=(14.0, 14.0, 16.0), ahead=6.5, speed=1.25, length=1.1, width=0.011, wind=(0.18, 0.06),
                 rgb=(0.55, 0.62, 1.0), strength=0.55, seed=7, near=1.2, name="rain"):
        import bpy
        r = random.Random(seed)
        self.p = [(r.random(), r.random(), r.random(), r.uniform(0.8, 1.2)) for _ in range(n)]
        self.size, self.ahead, self.speed, self.length, self.width, self.wind, self.near = size, ahead, speed, length, width, wind, near
        self.mat = emit_mat(name + "_m", rgb, strength)
        self.me = bpy.data.meshes.new(name); self.me.materials.append(self.mat)
        self.ob = bpy.data.objects.new(name, self.me); bpy.context.scene.collection.objects.link(self.ob); no_bounce(self.ob)

    def update(self, g, cam_loc, cam_look):
        from mathutils import Vector
        c = Vector(cam_loc); fwd = (Vector(cam_look) - c).normalized()
        centre = c + fwd * self.ahead; sx, sy, sz = self.size
        lo = centre - Vector((sx / 2, sy / 2, sz / 2))
        d = Vector((self.wind[0], self.wind[1], -1.0)).normalized()
        verts, faces = [], []
        for i, (a, b, h, k) in enumerate(self.p):
            v = self.speed * k
            p = Vector((((a * sx) + d.x * v * g) % sx, ((b * sy) + d.y * v * g) % sy, ((h * sz) + d.z * v * g) % sz)) + lo
            if (p - c).dot(fwd) < self.near:
                continue
            tail = p - d * self.length * k
            view = (p - c).normalized(); side = d.cross(view)
            if side.length < 1e-6:
                continue
            side = side.normalized() * self.width * (0.5 + 0.5 * (p - c).length / 6.0)
            j = len(verts)
            verts += [tuple(p - side), tuple(p + side), tuple(tail + side), tuple(tail - side)]
            faces.append((j, j + 1, j + 2, j + 3))
        self.me.clear_geometry(); self.me.from_pydata(verts, [], faces); self.me.update()


class FlashCard(object):
    """A white (or tinted) emission card just in front of the lens: strength 0 = invisible. Rendered, not a 2D post effect."""

    def __init__(self, cam, rgb=(1.0, 1.0, 1.0), name="flashcard"):
        import bpy
        me = bpy.data.meshes.new(name)
        z = -0.06; s = 0.2
        me.from_pydata([(-s, -s, z), (s, -s, z), (s, s, z), (-s, s, z)], [], [(0, 1, 2, 3)])
        self.mat = emit_mat(name + "_m", rgb, 0.0)
        me.materials.append(self.mat)
        self.ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(self.ob); no_bounce(self.ob)
        self.ob.parent = cam
        self.node = self.mat.node_tree.nodes['strength']

    def set(self, s, rgb=None):
        self.node.inputs['Strength'].default_value = float(s)
        if rgb is not None:
            self.node.inputs['Color'].default_value = (*rgb, 1.0)
        self.ob.hide_render = s <= 1e-4


def render_frame(scene, path, samples, scale, threads=2):
    import bpy
    scene.cycles.samples = samples
    scene.render.resolution_x, scene.render.resolution_y = 720, 1280
    scene.render.resolution_percentage = int(round(scale * 100))
    scene.render.threads_mode = 'FIXED'; scene.render.threads = threads
    scene.render.filepath = path
    t0 = time.time(); c0 = time.process_time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t0, time.process_time() - c0


def run_final(take_dir, sub, gs, build, apply, scale=1.0, samples=12, report=None):
    """Resumable: raw/<sub>/g_%04d.png + .json (json written after the PNG)."""
    out = os.path.join(take_dir, "raw", sub); os.makedirs(out, exist_ok=True)
    todo = []
    for g in gs:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
        ok = os.path.exists(png) and os.path.exists(js)
        if ok:
            m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok:
            todo.append(g)
    print("final %s: %d to render, %d done" % (sub, len(todo), len(gs) - len(todo)), flush=True)
    if not todo:
        return
    ctx = build()
    for g in todo:
        apply(ctx, g)
        png = os.path.join(out, "g_%04d.png" % g)
        wall, cpu = render_frame(ctx["scene"], png[:-4] + ".tmp.png", samples, scale)
        os.replace(png[:-4] + ".tmp.png", png)
        rep = dict(g=g, sub=sub, wall=round(wall, 2), cpu=round(cpu, 2), scale=scale, samples=samples)
        if report:
            rep.update(report(ctx, g))
        json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("%s g %d  %.1f s wall  %.1f s cpu" % (sub, g, wall, cpu), flush=True)


# ----------------------------------------------------------------------------- delivery
def contact(frames, out_jpg, n=16, cols=8, label=lambda g: ""):
    from PIL import Image, ImageDraw
    gs = sorted(frames)
    pick = [gs[int(round(i * (len(gs) - 1) / (n - 1.0)))] for i in range(n)]
    w, h, lab = 270, 480, 18
    rows = (len(pick) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(pick):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(frames[g]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, label(g)), fill=(255, 255, 255))
    S.save(out_jpg, quality=88)


def encode(take_dir, first_g):
    fr = os.path.join(take_dir, "frames")
    out = os.path.join(take_dir, "take.mkv")
    if os.path.exists(out):
        os.remove(out)
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(first_g), "-i",
                           os.path.join(fr, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", out])
    return out


def hue_rows(rows):
    """rows: [(label, [files])] -> text of hue_report rows (as s01/hue.py)."""
    import io, contextlib
    sys.path.insert(0, os.path.join(V3, "tools"))
    import hue_report as H
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for lab, fl in rows:
            if fl:
                H.row(lab, fl)
    return buf.getvalue()


def motion_stats(files):
    """camera-motion proxy: mean abs difference of consecutive frames (downscaled), and runs of near-identical frames."""
    import numpy as np
    from PIL import Image
    prev = None; d = []
    for f in files:
        a = np.asarray(Image.open(f).convert("L").resize((90, 160)), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d
