import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bc_studio as ST
import blockcast as BC
ST.reset(); ST.studio()
t0 = time.time()
k = BC.Figure("kong", "kong", wet=False, gloves=False); k.place((-0.8, 0, 0), 0); k.pose(dict(expr="determined"))
z = BC.Figure("zoff", "z_office", wet=True); z.place((0.8, 0, 0), 0); z.pose(dict(expr="idle"))
print("built in %.1f s" % (time.time() - t0), sum(len(o.data.vertices) for o in bpy.data.objects if o.type == "MESH"))
ang = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
k.place((-0.8, 0, 0), ang); z.place((0.8, 0, 0), ang)
ST.camera((0, -9.0, 0.95), (0, 0, 0.92), ortho=2.3)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 640, 640; sc.cycles.samples = 16
sc.render.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "quick_%d.png" % int(ang))
t0 = time.time(); bpy.ops.render.render(write_still=True); print("render %.1f s" % (time.time() - t0))
