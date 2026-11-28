"""neutral8.py -- a neutral lookdev stage: grey floor, soft key, cool fill sky, warm/red rim practical."""
import math, bpy
from mathutils import Vector


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build(res=(720, 1280), samples=32, threads=4, rim=True, key_power=650.0):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.threads_mode = "FIXED"; sc.render.threads = threads
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.cycles.transparent_max_bounces = 32
    sc.cycles.max_bounces = 4
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W_neutral"); sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.58, 0.66, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.10
    me = bpy.data.meshes.new("floor"); me.from_pydata([(-30, -30, 0), (30, -30, 0), (30, 30, 0), (-30, 30, 0)], [], [(0, 1, 2, 3)])
    fl = bpy.data.objects.new("floor", me); sc.collection.objects.link(fl)
    m = bpy.data.materials.new("floor_m"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.42, 0.42, 0.44, 1); b.inputs["Roughness"].default_value = 0.8
    fl.data.materials.append(m)
    # backdrop
    me2 = bpy.data.meshes.new("bd"); me2.from_pydata([(-30, 12, 0), (30, 12, 0), (30, 12, 30), (-30, 12, 30)], [], [(0, 1, 2, 3)])
    bd = bpy.data.objects.new("backdrop", me2); sc.collection.objects.link(bd); bd.data.materials.append(m)
    def light(name, typ, loc, power, col=(1, 1, 1), size=1.0, rot=None):
        ld = bpy.data.lights.new(name, typ); ld.energy = power; ld.color = col
        if typ == "AREA": ld.size = size
        else: ld.shadow_soft_size = size
        ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob); ob.location = loc
        if rot: ob.rotation_euler = rot
        return ob
    key = light("key", "AREA", (-3.5, -5.5, 6.0), key_power, (1.0, 0.97, 0.92), 2.5)
    aim(key, (0, 0, 1.6))
    fill = light("fill", "AREA", (5, -4, 3), key_power * 0.18, (0.75, 0.82, 1.0), 4.0); aim(fill, (0, 0, 1.5))
    lights = dict(key=key, fill=fill)
    if rim:
        r = light("rim", "POINT", (2.2, 2.2, 2.6), 380.0, (1.0, 0.35, 0.12), 0.15)
        lights["rim"] = r
    return lights


def aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=50, ortho=None):
    cd = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cd); bpy.context.scene.collection.objects.link(cam)
    cam.location = loc; aim(cam, target); cd.lens = lens
    if ortho:
        cd.type = "ORTHO"; cd.ortho_scale = ortho
    bpy.context.scene.camera = cam
    return cam
