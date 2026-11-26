import sys, os, time, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X, standins
t=time.time(); A = X.build(); print("build", time.time()-t, len(bpy.data.objects))
X.setup_render(quality="draft", threads=2)
acts = standins.place(A)
names = sys.argv[1].split(",") if len(sys.argv)>1 else ["eye"]
asp = sys.argv[2] if len(sys.argv)>2 else "9:16"
fr = int(sys.argv[3]) if len(sys.argv)>3 else 7
for n in names:
    cam = X.use_camera(n, asp, scale=0.5); bpy.context.view_layer.update(); standins.pose_all(acts, cam, hide=("kong",) if n=="macro_cutter" else ())
    r = X.render_still(os.path.join(HERE, "review", "out", f"{n}_{asp.replace(':','')}_f{fr}"), frame=fr)
    print(n, {k: r[k] for k in ("cpu_render","wall_render","cpu_post")}, flush=True)
