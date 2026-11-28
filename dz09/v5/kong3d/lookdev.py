"""lookdev.py -- Kong alone on a grey floor, 4 views (front, 3/4, side, back), for model checks. out/lookdev.png"""
import os, sys, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
import kong3d as K, kit
sc = bpy.context.scene
expr = sys.argv[1] if len(sys.argv) > 1 else "determined"
kind = sys.argv[2] if len(sys.argv) > 2 else "kong"
k = K.Figure3D("kong", kind, wet=False, cutter=(kind == "kong"))
if kind == "kong":
    k.pose(expr=expr, head=(10, 0, 0), cutter=dict(at=(-0.30, -0.42, 1.05), fwd=(0.55, -0.25, 0.80), up=(0.2, -0.9, 0.1),
                                                  pole_r=(-1.0, 0.3, 0.6), pole_l=(1.0, -0.2, 0.3)))
else:
    k.pose(expr=expr)
fl = bpy.data.meshes.new("floor"); fl.from_pydata([(-20,-20,0),(20,-20,0),(20,20,0),(-20,20,0)],[],[(0,1,2,3)])
fo = bpy.data.objects.new("floor", fl); sc.collection.objects.link(fo); fl.materials.append(kit.m_simple("floorm", "#55575e", 0.6))
for nm, loc, e, col, sz in (("key", (-4, -5, 7), 2500, (1, 0.88, 0.72), 2.0), ("fill", (6, -3, 3), 500, (0.55, 0.65, 1.0), 4.0),
                             ("rim", (2, 6, 5), 1500, (0.7, 0.8, 1.0), 1.0)):
    ld = bpy.data.lights.new(nm, "AREA"); ld.energy = e; ld.color = col; ld.size = sz
    lo = bpy.data.objects.new(nm, ld); sc.collection.objects.link(lo); lo.location = loc
    lo.rotation_euler = (Vector((0, 0, 1.6)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.06, 0.09, 1)
cd = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 50; cd.sensor_width = 36
sc.render.engine = "CYCLES"; sc.cycles.samples = 16; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 400, 600
sc.render.threads_mode = "FIXED"; sc.render.threads = 4
os.makedirs(HERE + "/out/lookdev", exist_ok=True)
from PIL import Image
tiles = []
for i, ang in enumerate((0, 35, 90, 180)):
    a = math.radians(ang); d = 9.0
    cam.location = (d * math.sin(a), -d * math.cos(a), 1.8)
    cam.rotation_euler = (Vector((0, 0, 1.55)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    p = f"{HERE}/out/lookdev/v{i}.png"; sc.render.filepath = p
    t = time.time(); bpy.ops.render.render(write_still=True); print("render", time.time() - t)
    tiles.append(Image.open(p).convert("RGB"))
sh = Image.new("RGB", (1600, 600))
for i, t in enumerate(tiles): sh.paste(t, (400 * i, 0))
sh.save(f"{HERE}/out/lookdev_{kind}_{expr}.png")
