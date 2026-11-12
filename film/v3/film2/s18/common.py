"""common.py -- helpers shared by takes s16, s17, s18 (film 2, render worker 4). A copy lives in each take folder.

Frame model: the Blender frame IS the film frame g. Nothing is keyframed: on_frame(g) sets the camera, the set controls and
every effect object directly before each render (render.render_frames calls it after frame_set)."""
import math, os, sys, json, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import camrig, render                                   # noqa: E402
from anim import ease, keys, lerp, clamp, pulse         # noqa: E402


def g_of(t):
    """narration time -> film frame of an in-shot event"""
    return int(round((t + 0.10) * 30))


def build(preset, quality):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    A = T.build(preset)
    T.setup_render(scene, quality)
    scene.frame_start, scene.frame_end = 1, 3000
    mk = bpy.data.objects.get("market")          # director (s01): the striped stall awning reads as a flag -> hidden
    if mk is not None:
        mk.hide_render = True
    cam = camrig.make_camera(scene, name="cam_w4")
    cam.data.clip_start = 0.02
    cam.data.clip_end = 400
    T.setup_render(scene, quality)               # make_camera resets the resolution percentage
    return scene, A, cam


def set_cam(cam, loc, look, roll=0.0):
    cam.location = Vector(loc)
    cam.rotation_euler = camrig.look_rotation(Vector(loc), Vector(look), roll)


def cam_track(g, ks, lin_share=0.15):
    """eased keys [(g, (x,y,z, lx,ly,lz), ease)] mixed with a constant-speed share so the camera never parks"""
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), lin_share)
    return Vector(k[:3]), Vector(k[3:6])


def emit_mat(name, color, strength, camera_only=True, additive=False):
    """unlit emission material with an adjustable Emission node called 'strength' (set per frame)"""
    return T.mat_emit(name, color, strength=strength, camera_only=camera_only, additive=additive)


def set_strength(mat, s):
    mat.node_tree.nodes["strength"].inputs["Strength"].default_value = float(s)


def curve(name, pts, radius, mat, radii=None, coll=None):
    coll = coll or bpy.context.scene.collection
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for i, (p, q) in enumerate(zip(sp.points, pts)):
        p.co = (q[0], q[1], q[2], 1.0)
        p.radius = radii[i] if radii else 1.0
    cu.bevel_mode = "ROUND"; cu.bevel_depth = radius; cu.bevel_resolution = 2; cu.use_fill_caps = True
    cu.bevel_factor_mapping_start = "SPLINE"; cu.bevel_factor_mapping_end = "SPLINE"
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu); coll.objects.link(ob)
    ob.visible_shadow = False
    T.no_bounce(ob)
    return ob


def reveal(ob, a, b):
    """show the part of the curve between fractions a..b of its length (hidden if empty)"""
    a, b = clamp(a), clamp(b)
    if b - a < 1e-4:
        ob.hide_render = True
        return
    ob.hide_render = False
    ob.data.bevel_factor_start = a
    ob.data.bevel_factor_end = b


def jag(pts, seed, amp, sub=4, taper_end=True):
    """jagged polyline through control points pts: every segment subdivided into `sub` pieces, random offsets
    perpendicular to the path (shrinking to 0 at both ends of the whole path)"""
    r = random.Random(seed)
    out = [Vector(pts[0])]
    P = [Vector(p) for p in pts]
    n_all = (len(P) - 1) * sub
    k = 0
    for a, b in zip(P[:-1], P[1:]):
        d = (b - a)
        s1 = d.cross(Vector((0.31, 0.17, 0.93))).normalized()
        s2 = d.cross(s1).normalized()
        for i in range(1, sub + 1):
            k += 1
            p = a.lerp(b, i / float(sub))
            if k < n_all:
                u = k / float(n_all)
                w = math.sin(math.pi * u) ** 0.6 if taper_end else 1.0
                p = p + (s1 * r.uniform(-1, 1) + s2 * r.uniform(-1, 1) * 0.6) * amp * w
            out.append(p)
    return [tuple(v) for v in out]


def path_len(pts):
    return sum((Vector(b) - Vector(a)).length for a, b in zip(pts[:-1], pts[1:]))


def point_at(pts, u):
    """point at fraction u of the polyline length"""
    L = path_len(pts) * clamp(u); acc = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = Vector(a), Vector(b); l = (b - a).length
        if acc + l >= L:
            return a.lerp(b, (L - acc) / max(l, 1e-9))
        acc += l
    return Vector(pts[-1])


def sphere(name, loc, r, mat, coll=None):
    coll = coll or bpy.context.scene.collection
    me = bpy.data.meshes.new(name)
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=r); bm.to_mesh(me); bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); ob.location = loc
    ob.visible_shadow = False; T.no_bounce(ob)
    return ob


def point_light(name, color, energy, radius=0.3):
    ld = bpy.data.lights.new(name, "POINT"); ld.color = color; ld.energy = energy; ld.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    return ob


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def run_cli(Take, RANGE, here):
    """python3 shot.py stills <a:b:s> <out> [scale] [samples] | final <a:b> [scale] [samples] | probe <a:b:s>"""
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "probe":
        tk = Take("preview")
        for g in gs:
            print(json.dumps(tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[3]
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        tk = Take("preview")
        for g in gs:
            st = tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        out = os.path.join(here, "raw")
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            tk = Take("final")
            for g in todo:
                st = tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)


class BaseTake(object):
    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames(list(gs), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    on_frame=self.on_frame, verbose=False, check=False, sync=False)

    def report(self, g):
        self.on_frame(g)
        loc, look = self.cam_at(g)
        v = look - loc
        out = dict(g=g, cam=[round(c, 3) for c in loc], look=[round(c, 3) for c in look],
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1))
        for nm, p in self.marks().items():
            s = render.world_to_screen(self.cam, tuple(p), g)
            out[nm] = [round(s[0], 1), round(s[1], 1)]
        out.update(self.state(g))
        return out
