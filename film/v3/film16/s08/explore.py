import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector
TG, cast16 = C.TG, C.cast16
# usage: explore.py preset camname "locx,locy,locz" "lookx,looky,lookz" out.png  actors...
def V(s): return Vector([float(x) for x in s.split(",")])
Tk = C.Take("chamber_low", light="DAY", quality="preview")
A = Tk.A
cams = [("explore_a", V(sys.argv[1]), V(sys.argv[2]))]
Tk.key_cam(1, *cams[0][1:])
spec = json.loads(sys.argv[3])      # [[name, castkey, markname|[x,y,z], posename, mirror], ...]
for i,(nm, ck, mk, pn, mir) in enumerate(spec):
    a = C.make_actor(nm, ck, os.path.join(HERE,"work","sprites"), cam=Tk.cam)
    Tk.actors[nm]=a
    xyz = A["marks"][mk] if isinstance(mk,str) else mk
    C.place(a, 1, xyz)
    cast, pose = cast16.STORY16[pn]
    pose = dict(pose); pose["mirror"]=bool(mir)
    Tk.scene.frame_set(1)
    a.pose(1, pose, camera=Tk.cam)
Tk.sprites_for([(a,256) for a in Tk.actors.values()],[1])
print(C.head_report(Tk,1))
os.makedirs(os.path.join(HERE,"work","ex"),exist_ok=True)
st = Tk.render([1], os.path.join(HERE,"work","ex"), scale=0.5, samples=6)[0]
os.replace(st["path"], sys.argv[4])
