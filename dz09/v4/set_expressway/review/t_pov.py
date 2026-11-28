import sys, os, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X, standins
from mathutils import Vector
A = X.build(); X.setup_render(quality="preview"); acts = standins.place(A)
th=A["hero_heading"]; fwd=Vector((-math.sin(th), math.cos(th), 0)); right=Vector((math.cos(th), math.sin(th), 0))
ws=Vector(A["windscreen"])
C,W = X._STATE["cams"]
for i,(r,z,f) in enumerate([(-0.25,0.55,2.35),(0.35,0.95,2.35),(-0.35,0.35,2.0)]):
    C["pov_windscreen"]["loc"]=tuple(ws+fwd*f+Vector((0,0,z))+right*r)
    cam=X.use_camera("pov_windscreen","9:16",scale=0.5); bpy.context.view_layer.update(); standins.pose_all(acts,cam)
    X.render_still(os.path.join(HERE,"review","out",f"pov_t{i}"),frame=7)
