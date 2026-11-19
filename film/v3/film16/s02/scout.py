import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector
TG=C.TG
preset, light, out = sys.argv[1], sys.argv[2], sys.argv[3]
T = C.Take(preset, light=light, quality="preview", name="scout")
A=T.A
print({k:[round(x,2) for x in v] for k,v in A["marks"].items() if k in("morse_wide","morse_ladder_foot","morse_rail","morse_wire","platform_a","platform_b","platform_c","platform_d")})
print(A["cam"])
print(TG.STATE.get("train") and TG.STATE["train"].get("front0"))
T.key_cam(1, *( (Vector(A["cam"]["loc"]) , Vector(A["cam"]["look_at"])) ))
st=T.render([1], out, scale=0.5, samples=4)[0]
os.replace(st["path"], os.path.join(out,"scout_%s.png"%preset))
