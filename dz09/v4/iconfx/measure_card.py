"""measure_card.py -- checks of blender_card in Cycles (one process, small renders):
  1. colour: a stopwatch card (image sequence) filling an orthographic camera, under a strong orange key and a red
     point light: rendered pixels vs the baked PNG over black (mean / max abs difference, levels 0-255);
  2. sequence: for 4 frames, which baked PNG the render matches best (must be the PNG of the same frame);
  3. pop: the card's rendered width per frame vs the pop profile.
    python3 measure_card.py [out_dir]   -> prints JSON, writes out_dir/measure_card.json
"""
import json, math, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import blender_card as BC
from anim import Cue, pop_state

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "measure")
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.render.threads_mode = "FIXED"
sc.render.threads = 2
sc.cycles.samples = 16
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.film_transparent = False
sc.render.filter_size = 0.01
w = bpy.data.worlds.new("w")
sc.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
for col, loc, e in (((1, 0.55, 0.18), (1, -2, 2), 3000), ((1, 0.05, 0.05), (-1, -1, 0.5), 2000)):
    L = bpy.data.lights.new("l", "POINT")
    L.color, L.energy = col, e
    o = bpy.data.objects.new("l", L)
    o.location = loc
    sc.collection.objects.link(o)

cue = Cue(10, hold=20)
bk = BC.bake("sw", "stopwatch", {"speed": 30.0}, cue, os.path.join(OUT, "tex"), px=200, pad=0.25)
cd = bpy.data.cameras.new("c")
cd.type = "ORTHO"
cam = bpy.data.objects.new("c", cd)
sc.collection.objects.link(cam)
sc.camera = cam
cam.location = (0, -5, 0)
cam.rotation_euler = (math.pi / 2, 0, 0)
k = 1.0 / bk.px                                          # height 1.0 -> world units per pixel
cd.ortho_scale = max(bk.w_px, bk.h_px) * k
sc.render.resolution_x, sc.render.resolution_y = bk.w_px, bk.h_px
ob = BC.add_card(bk, height=1.0, location=(0, -1, 0), facing="camera", camera=cam)
# centre the card in the camera: the origin is the anchor
ax, ay = bk.anchor_px
cam.location = (ob.location.x + (bk.w_px / 2 - ax) * k, -5, ob.location.z - (bk.h_px / 2 - ay) * k)
BC.key_pop(ob, cue)

res = {"colour": [], "sequence": [], "pop_width": []}
def over_black(fn):
    a = np.asarray(Image.open(fn).convert("RGBA")).astype(float)
    return a[..., :3] * (a[..., 3:] / 255.0)
for g in (cue.g_hold + 1, cue.g_hold + 6, cue.g_hold + 12, cue.g_hold + 18):
    sc.frame_set(g + 1)
    fn = os.path.join(OUT, "r_%04d.png" % g)
    sc.render.filepath = fn
    bpy.ops.render.render(write_still=True)
    r = np.asarray(Image.open(fn).convert("RGB")).astype(float)
    diffs = {}
    for f2 in sorted(bk.files):
        ref = over_black(f2)
        if ref.shape != r.shape:
            continue
        diffs[os.path.basename(f2)] = float(np.abs(r - ref).mean())
    best = min(diffs, key=diffs.get)
    ref = over_black(os.path.join(os.path.dirname(bk.files[0]), "sw_%04d.png" % (g + 1)))
    d = np.abs(r - ref)
    opaque = np.asarray(Image.open(os.path.join(os.path.dirname(bk.files[0]), "sw_%04d.png" % (g + 1))))[..., 3] == 255
    res["colour"].append({"g": g, "mean_abs": round(float(d.mean()), 2), "opaque_mean_abs": round(float(d[opaque].mean()), 2),
                          "opaque_p99": round(float(np.percentile(d[opaque], 99)), 1)})
    res["sequence"].append({"g": g, "expected": "sw_%04d.png" % (g + 1), "best": best, "ok": best == "sw_%04d.png" % (g + 1)})
# pop widths (16 samples is plenty for a silhouette)
sc.cycles.samples = 4
for g in range(cue.g_in, cue.g_hold + 1):
    sc.frame_set(g + 1)
    fn = os.path.join(OUT, "p_%04d.png" % g)
    sc.render.filepath = fn
    bpy.ops.render.render(write_still=True)
    a = np.asarray(Image.open(fn).convert("RGB")).astype(float).max(-1) > 30
    xs = np.nonzero(a.any(0))[0]
    res["pop_width"].append({"g": g, "width_px": int(xs.max() - xs.min() + 1) if len(xs) else 0,
                             "expected_scale": pop_state(cue, g).scale})
full = res["pop_width"][-1]["width_px"] or 1
for e in res["pop_width"]:
    e["ratio"] = round(e["width_px"] / float(full), 3)
json.dump(res, open(os.path.join(OUT, "measure_card.json"), "w"), indent=1)
print(json.dumps(res))
