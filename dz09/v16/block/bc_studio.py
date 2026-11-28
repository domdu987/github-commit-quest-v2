"""bc_studio.py -- cream studio for the turnaround and face proofs: cream cyclorama, soft key, fill, rim (Cycles CPU)."""
import math, os
import bpy
from mathutils import Vector


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.render.threads_mode = "FIXED"; sc.render.threads = int(os.environ.get("BC_THREADS", "2"))
    sc.cycles.samples = 32; sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"; sc.view_settings.exposure = -0.85
    sc.render.image_settings.file_format = "PNG"
    return sc


def studio(cream=(0.62, 0.53, 0.43), key=1100.0, size=4.5):
    sc = bpy.context.scene
    w = bpy.data.worlds.new("studio"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = tuple(c * 0.9 for c in cream) + (1,); bg.inputs[1].default_value = 0.35
    # cyclorama: floor + curved back
    import bmesh
    me = bpy.data.meshes.new("cyc"); bm = bmesh.new()
    prof = [(0, -14.0, 0.0), (0, 2.0, 0.0)] + [(0, 2.0 + 1.2 * math.sin(a), 1.2 - 1.2 * math.cos(a)) for a in [math.radians(k * 10) for k in range(1, 10)]] + [(0, 3.2, 8.0)]
    rows = []
    for x in (-8.0, 8.0):
        rows.append([bm.verts.new((x, y, z)) for _, y, z in prof])
    for i in range(len(prof) - 1):
        bm.faces.new((rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new("cyc", me); sc.collection.objects.link(ob)
    m = bpy.data.materials.new("cream"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = cream + (1,); b.inputs["Roughness"].default_value = 0.9
    me.materials.append(m)
    def area(name, loc, look, power, sz, col=(1, 1, 1)):
        L = bpy.data.lights.new(name, "AREA"); L.energy = power; L.size = sz; L.color = col
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        d = Vector(look) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        return o
    area("key", (-2.6, -3.4, 3.6), (0, 0, 1.0), key, size, (1.0, 0.96, 0.90))
    area("fill", (3.2, -2.6, 1.8), (0, 0, 0.9), key * 0.14, size * 1.2, (0.92, 0.95, 1.0))
    area("rim", (1.5, 3.0, 3.2), (0, 0, 1.2), key * 0.55, 2.0, (1.0, 0.95, 0.9))
    return ob


def camera(loc, look, lens=85.0, ortho=None):
    sc = bpy.context.scene
    c = bpy.data.cameras.new("cam"); o = bpy.data.objects.new("cam", c); sc.collection.objects.link(o)
    sc.camera = o; c.lens = lens; c.sensor_fit = "VERTICAL"; c.sensor_height = 24.0
    if ortho: c.type = "ORTHO"; c.ortho_scale = ortho
    o.location = loc; o.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.clip_start = 0.05; c.clip_end = 200
    return o
