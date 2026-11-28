"""dbg_hook.py -- stage one hook frame with the blocky cast, print geometry facts (driver head vs roof), render a draft still."""
import os, sys, math
HC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hookcopy"); sys.path.insert(0, HC); os.chdir(HC)
import common as C, importlib
import stage
import bpy
from mathutils import Vector
gs = [int(x) for x in sys.argv[1].split(",")]; outp = sys.argv[2]; hide = sys.argv[3].split(",") if len(sys.argv) > 3 else []
F = stage.Stage("draft", 360, 640, threads=2)
for g in gs:
  out = outp + "_%d" % g
  sid = C.shot_of(g); mod = importlib.import_module("shots." + sid.lower())
  F.begin(mod); post = F.frame(mod, g)
  for a in F.cast:
      if a.name in hide: a.fig.hide(True)
  bpy.context.view_layer.update()
  dg = bpy.context.evaluated_depsgraph_get()
  for a in F.cast:
      if not a.visible: continue
      h = a.head(); f = a.fig
      top = f.root.matrix_world @ Vector((0, 0, f.H)) if False else None
      mine = set(o.name for o in f.objects); p = Vector(h); hit = False; top = None
      for _ in range(30):
          hit, loc, n, i, ob, m = F.sc.ray_cast(dg, p, Vector((0, 0, 1)))
          if not hit: break
          if ob.name in mine: top = loc.z; p = loc + Vector((0, 0, 1e-3)); continue
          break
      print("  hair/head top z", top)
      print("ACTOR", a.name, "head", tuple(round(x, 3) for x in h), "face_used", round(getattr(a, "face_used", a.face), 1), "screen", tuple(round(x, 3) for x in F.screen(h)),
            "roof above head+0.6:", (round(loc.z, 3), ob.name) if hit else None)
  r = F.render(out, g, post)
  print("render", r.get("wall_render"))
