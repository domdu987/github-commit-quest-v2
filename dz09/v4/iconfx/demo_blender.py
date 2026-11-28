"""demo_blender.py -- proof that the cards work in a lit 3D night world: a small stand-in of the EP.1 expressway (wet
asphalt, lane paint, stalled cars, concrete barriers, a sodium lamp, a pulsing red beacon) with world-anchored icon
cards (red X marks popping in sequence over a row of cars, red sound rings over the rescue truck, the red-pupil eye
over a far car, a measuring tape lying on the road) and one screen-space overlay (the 60 s stopwatch).

    python3 demo_blender.py [out_dir] [--frames 0:48] [--scale 0.5] [--samples 10]
-> out_dir/raw/f_%04d.png (Blender), out_dir/ovl/o_%04d.png (overlay layer), out_dir/comp/f_%04d.png, demo_3d.mp4
The set here is a stand-in for the test only; it is not the film's expressway set.
"""
import math, os, sys, subprocess, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import blender_card as BC
import overlay as OV
from anim import Cue

args = sys.argv[1:]
OUT = args[0] if args and not args[0].startswith("--") else os.path.join(HERE, "out", "demo3d")
def opt(k, d):
    return args[args.index(k) + 1] if k in args else d
FR = [int(x) for x in opt("--frames", "0:48").split(":")]
SCALE = float(opt("--scale", "0.5"))
SAMPLES = int(opt("--samples", "10"))
ASPECT = opt("--aspect", "9:16")                  # "9:16" (720x1280) or "16:9" (1280x720): same set, same camera path
RW, RH = OV.frame_size(ASPECT)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.render.threads_mode = "FIXED"
sc.render.threads = 2
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
try:
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception:
    pass
sc.cycles.max_bounces = 3
sc.cycles.diffuse_bounces = 1
sc.cycles.glossy_bounces = 2
sc.cycles.transparent_max_bounces = 16
sc.cycles.sample_clamp_indirect = 3.0
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.render.resolution_percentage = int(SCALE * 100)
sc.render.fps = 30
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.film_transparent = False

w = bpy.data.worlds.new("night")
sc.world = w
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.012, 0.018, 0.05, 1)
bg.inputs["Strength"].default_value = 1.0


def mat(name, col, rough=0.5, emit=None, estr=0.0, metal=0.0):
    m = bpy.data.materials.new(name)
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = BC._hex_lin(col) if isinstance(col, str) else col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if emit:
        p.inputs["Emission Color"].default_value = BC._hex_lin(emit)
        p.inputs["Emission Strength"].default_value = estr
    return m


def asphalt():
    m = bpy.data.materials.new("wet_asphalt")
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (0.018, 0.019, 0.024, 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.35
    nz.inputs["Detail"].default_value = 6.0
    cr = nt.nodes.new("ShaderNodeMapRange")
    cr.inputs["From Min"].default_value = 0.45
    cr.inputs["From Max"].default_value = 0.6
    cr.inputs["To Min"].default_value = 0.42
    cr.inputs["To Max"].default_value = 0.06
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], cr.inputs["Value"])
    nt.links.new(cr.outputs["Result"], p.inputs["Roughness"])
    return m


def box(name, loc, dims, m, bevel=0.0, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = dims
    o.rotation_euler = (0, 0, rot)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        bm = o.modifiers.new("bev", "BEVEL")
        bm.width = bevel
        bm.segments = 2
    o.data.materials.append(m)
    return o


# road (one unit = one head diameter; a car is about 4.4 x 1.8 x 1.4 m -> we use metres here, icons sized to match)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 40, 0))
road = bpy.context.active_object
road.scale = (16, 120, 1)
road.data.materials.append(asphalt())
paint = mat("paint", "#d9d6cc", 0.6)
for x in (-3.6, 0.0, 3.6):
    for k in range(16):
        box("lane", (x, 2 + k * 7, 0.005), (0.14, 3.0, 0.01), paint)
conc = mat("concrete", "#6d6f78", 0.85)
for x in (-7.6, 7.6):
    box("barrier", (x, 40, 0.5), (0.5, 120, 1.0), conc)

bodies = ["#5d6470", "#8b8f99", "#2f3a52", "#7a2f2b", "#c8c6c0", "#3b4740"]
glass = mat("glass", "#0b0e16", 0.08)
tail = mat("tail", "#300806", 0.4, "#ff2a1a", 6.0)
head = mat("headl", "#fff6e0", 0.3, "#ffe6b8", 3.0)
cars = []
import random
rnd = random.Random(9)
lanes = (-5.4, -1.8, 1.8, 5.4)
for i in range(18):
    x = lanes[i % 4] + rnd.uniform(-0.3, 0.3)
    y = 6 + (i // 4) * 7.5 + rnd.uniform(-1.5, 1.5)
    yaw = math.radians(rnd.uniform(-14, 14))
    if abs(x - 2.0) < 2.0 and abs(y - 9.5) < 5.5:
        continue
    bm = mat("car%d" % i, bodies[i % len(bodies)], 0.25, metal=0.3)
    c = box("car%d" % i, (x, y, 0.55), (1.8, 4.3, 0.75), bm, 0.12, yaw)
    box("cab%d" % i, (x, y + 0.2, 1.15), (1.55, 2.2, 0.55), glass, 0.08, yaw)
    box("tl%d" % i, (x - 0.65 * math.cos(yaw) - 2.16 * math.sin(-yaw), y - 2.16 * math.cos(yaw), 0.72), (0.35, 0.06, 0.12), tail, 0, yaw)
    box("tr%d" % i, (x + 0.65 * math.cos(yaw) - 2.16 * math.sin(-yaw), y - 2.16 * math.cos(yaw), 0.72), (0.35, 0.06, 0.12), tail, 0, yaw)
    cars.append((x, y))
# rescue truck with a red beacon
box("truck", (2.0, 9.5, 1.0), (2.2, 5.5, 1.8), mat("truck", "#d8d2c4", 0.35, metal=0.1), 0.1)
bcn = box("beacon", (2.0, 9.0, 2.0), (0.9, 0.3, 0.18), mat("bcn", "#400404", 0.3, "#ff1d10", 30.0))

# lights: sodium lamp, red beacon (pulse 2 Hz), cool moon
pole = mat("pole", "#2a2c33", 0.6)
for (x, y) in ((-6.8, 14.0), (6.8, 34.0), (-6.8, 54.0)):
    box("pole", (x, y, 4.5), (0.18, 0.18, 9.0), pole)
    L = bpy.data.lights.new("sodium", "POINT")
    L.color = (1.0, 0.55, 0.18)
    L.energy = 2600
    L.shadow_soft_size = 0.4
    o = bpy.data.objects.new("sodium", L)
    o.location = (x * 0.8, y, 8.7)
    sc.collection.objects.link(o)
R = bpy.data.lights.new("red", "POINT")
R.color = (1.0, 0.08, 0.05)
R.shadow_soft_size = 0.2
ro = bpy.data.objects.new("red", R)
ro.location = (2.0, 9.0, 2.6)
sc.collection.objects.link(ro)
for g in range(FR[0], FR[1] + 1):
    R.energy = 300 + 1700 * (0.5 + 0.5 * math.cos(2 * math.pi * 2.0 * g / 30.0)) ** 3
    R.keyframe_insert("energy", frame=g + 1)
S = bpy.data.lights.new("moon", "SUN")
S.color = (0.55, 0.62, 1.0)
S.energy = 0.25
so = bpy.data.objects.new("moon", S)
so.rotation_euler = (math.radians(55), 0, math.radians(-30))
sc.collection.objects.link(so)

# camera: 22 mm, low behind the truck, dolly forward a little (cards must stay locked to the world)
cd = bpy.data.cameras.new("cam")
cd.lens = 22
cd.sensor_fit = "AUTO"
cd.sensor_width = 36.0
cd.dof.use_dof = True
cd.dof.aperture_fstop = 1.6
cam = bpy.data.objects.new("cam", cd)
sc.collection.objects.link(cam)
sc.camera = cam
tgt = bpy.data.objects.new("tgt", None)
sc.collection.objects.link(tgt)
cd.dof.focus_object = tgt
tc = cam.constraints.new("TRACK_TO")
tc.target = tgt
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"
for g in range(FR[0], FR[1] + 1):
    u = (g - FR[0]) / max(1, FR[1] - FR[0])
    cam.location = (-1.6 + 0.6 * u, -7.5 + 2.0 * u, 4.2 + 0.3 * u)
    cam.keyframe_insert("location", frame=g + 1)
    tgt.location = (-0.4, 12.0, 0.6)
    tgt.keyframe_insert("location", frame=g + 1)

# ---- icon cards ------------------------------------------------------------------------------------------------------
TEX = os.path.join(OUT, "tex")
t0 = time.time()
sc.frame_set(FR[0] + 1)
row = sorted([c for c in cars if c[0] < -3 and c[1] > 8], key=lambda c: c[1])[:4]
CARDS = []                                        # (object, kind) for the readability report
# Sizes are set in screen pixels at the first frame (BC.height_for_px), not guessed in metres: the reference's X marks
# are ~100 px tall on 720x1280; the first version used 1.3 m and got ~30 px (unreadable on a phone).
# one WORLD height for the whole row (sized so the nearest X is 110 px), so the row shrinks with depth as the
# reference's chain of X marks does, instead of fusing into one same-size lump
x_h = BC.height_for_px(sc, cam, (row[0][0], row[0][1], 2.9), 110)
for i, (x, y) in enumerate(row):
    cue = Cue(4 + 4 * i, hold=60, profile="brief", pop_out=False)
    bk = BC.bake("x%d" % i, "x_mark", {}, cue, TEX, px=192, animated=False)
    loc = (x, y, 2.9)
    ob = BC.add_card(bk, height=x_h, location=loc, facing="camera", camera=cam)
    BC.key_pop(ob, cue)
    CARDS.append((ob, "symbol"))
cue_r = Cue(2, hold=60, pop_out=False)
bk = BC.bake("rings", "sound_rings", {"mode": "arcs", "period": 0.8}, cue_r, TEX, px=256)
ob = BC.add_card(bk, height=BC.height_for_px(sc, cam, (2.0, 9.0, 3.9), 150), location=(2.0, 9.0, 3.9),
                 facing="camera", camera=cam)
BC.key_pop(ob, cue_r)
CARDS.append((ob, "symbol"))
far = max(cars, key=lambda c: c[1] if abs(c[0]) < 3 else -1)
cue_e = Cue(18, hold=60, pop_out=False)
bk = BC.bake("eye", "eye", {}, cue_e, TEX, px=256)
loc = (far[0], far[1], 5.2)                       # above the X row, not inside it
ob = BC.add_card(bk, height=BC.height_for_px(sc, cam, loc, 110), location=loc, facing="camera", camera=cam)
BC.key_pop(ob, cue_e)
CARDS.append((ob, "symbol"))
cue_t = Cue(8, hold=60, pop_out=False, profile="snap")
bk = BC.bake("tape", "tape", {"length": 200, "grow": 0.8}, cue_t, TEX, px=128)
ob = BC.add_card(bk, height=1.6, location=(0.0, -1.0, 0.02), facing="flat", yaw=math.radians(90))
BC.key_pop(ob, cue_t, roll=False)
cue_l = Cue(30, hold=60, pop_out=False)
bk = BC.bake("label", "tape_label", {"label": "ระยะ 30 ม.", "family": "Kanit"}, cue_l, TEX, px=256, animated=False)
loc = (-0.4, 4.0, 2.3)
# Kanit cap/x-height is ~0.70 of the font size; size 24 -> ~17 design units of text height per 100 units
ob = BC.add_card(bk, height=BC.height_for_px(sc, cam, loc, 30 / 0.17), location=loc, facing="camera", camera=cam)
ob["iconfx_cap"] = 0.17
BC.key_pop(ob, cue_l)
CARDS.append((ob, "text_cap"))
bake_s = time.time() - t0

# ---- render ---------------------------------------------------------------------------------------------------------
RAW = os.path.join(OUT, "raw")
os.makedirs(RAW, exist_ok=True)
times = []
proj = {}
for g in range(FR[0], FR[1]):
    sc.frame_set(g + 1)
    sc.render.filepath = os.path.join(RAW, "f_%04d.png" % g)
    t1 = time.time()
    bpy.ops.render.render(write_still=True)
    times.append(time.time() - t1)
    proj[g] = BC.project(sc, cam, (2.0, 9.0, 3.9))
    print("frame", g, "%.1fs" % times[-1], flush=True)

# ---- screen-space overlay + composite -------------------------------------------------------------------------------
SW = {"9:16": (560, 230, 190), "16:9": (1120, 170, 190)}[ASPECT]
P = [OV.Placement("stopwatch", Cue(22, hold=60, pop_out=False), x=SW[0], y=SW[1], px=SW[2], kw={"speed": 24.0})]
OVL, COMP = os.path.join(OUT, "ovl"), os.path.join(OUT, "comp")
os.makedirs(OVL, exist_ok=True)
os.makedirs(COMP, exist_ok=True)
for g in range(FR[0], FR[1]):
    lay = OV.render_layer(P, g, os.path.join(OVL, "o_%04d.png" % g), frame=ASPECT)
    OV.composite(os.path.join(RAW, "f_%04d.png" % g), lay, os.path.join(COMP, "f_%04d.png" % g))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FR[0]), "-i",
                os.path.join(COMP, "f_%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                os.path.join(OUT, "demo_3d.mp4")], check=True)
json.dump({"bake_s": bake_s, "render_s": times, "mean_s": sum(times) / len(times), "aspect": ASPECT, "safe": OV.safe_report(P, frame=ASPECT),
           "too_small_on_phone": BC.readability_report(sc, cam, CARDS, range(FR[0] + 1, FR[1] + 1)),
           "rings_px": {g: proj[g] for g in proj}}, open(os.path.join(OUT, "demo_stats.json"), "w"), indent=1, default=list)
print("bake %.1fs, render mean %.2fs/frame" % (bake_s, sum(times) / len(times)))
