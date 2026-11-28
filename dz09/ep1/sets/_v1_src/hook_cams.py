"""hook_cams.py -- dump the hook's 24 cameras (first / middle / last frame of every shot) and the deck's vehicle layout,
without rendering: out/hook_cams.json, out/layout.json.  Used by check_hook.py to prove that EP.1 dressing is not in any
hook frame.  Imports v10/film read-only."""
import os, sys, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v10", "film"))
import common as C
import stage
import bpy
from mathutils import Vector

stage.Act.apply = lambda self, cam: None           # no rasterising: only the cameras are wanted
F = stage.Stage("draft", 360, 640, threads=1)
cams = []
for i in range(1, 25):
    sid = "S%02d" % i
    mod = importlib.import_module("shots." + sid.lower())
    try:
        F.begin(mod)
    except Exception as ex:
        print("begin failed", sid, ex)
    a, b = C.shot_range(sid)
    for g in sorted({a, (a + b) // 2, b - 1}):
        t = g / 24.0; u = (g - a) / float(max(b - a - 1, 1))
        F.g = g
        try:
            mod.frame(F, g, t, u)
        except Exception as ex:
            print("frame failed", sid, g, repr(ex))
        bpy.context.view_layer.update()
        cam = F.cam
        cams.append(dict(shot=sid, g=g, M=[list(r) for r in cam.matrix_world], lens=cam.data.lens, clip=cam.data.clip_start))
        print(sid, g, tuple(round(x, 2) for x in cam.location), cam.data.lens, flush=True)
json.dump(cams, open(os.path.join(HERE, "out", "hook_cams.json"), "w"))
lay = []
for ob in bpy.data.objects:
    if ob.parent is None and (ob.type == "EMPTY"):
        d = dict(name=ob.name, loc=[round(x, 3) for x in ob.matrix_world.translation], yaw=round(ob.rotation_euler[2], 4),
                 inst=ob.instance_collection.name if ob.instance_collection else None, coll=[c.name for c in ob.users_collection])
        lay.append(d)
A = F.A
anch = {k: (list(v) if isinstance(v, (tuple, list, Vector)) and len(v) <= 4 and all(isinstance(x, (int, float)) for x in v) else (v if isinstance(v, (int, float, str)) else None)) for k, v in A.items()}
lights = [dict(name=o.name, type=o.data.type, loc=[round(x, 2) for x in o.matrix_world.translation], energy=o.data.energy, hide=o.hide_render) for o in bpy.data.objects if o.type == "LIGHT"]
colls = {c.name: len(c.objects) for c in bpy.data.collections}
json.dump(dict(layout=lay, anchors=anch, lights=lights, colls=colls, extras=[list(x[:2]) for x in stage.Stage.EXTRA_SPOTS]), open(os.path.join(HERE, "out", "layout.json"), "w"), indent=0)
print("ok")
