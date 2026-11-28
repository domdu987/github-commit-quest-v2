import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bc_studio as ST
import blockcast as BC
kind = sys.argv[1]; out = sys.argv[2]
ST.reset(); ST.studio()
f = BC.Figure("f", kind, wet=(kind != "kong"), gloves=False); f.pose(dict())
c = f.head_c
ST.camera((0, -6.0, c.z + 0.05), (0, 0, c.z), ortho=0.75)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 360, 360; sc.cycles.samples = 12
from PIL import Image
ims = []
for ang in (0, -45, -90, 180):
    f.place((0, 0, 0), ang)
    sc.render.filepath = "/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/v16/block/out/_h.png"
    bpy.ops.render.render(write_still=True); ims.append(Image.open(sc.render.filepath).convert("RGB"))
W = Image.new("RGB", (360 * 4, 360))
for i, im in enumerate(ims): W.paste(im, (360 * i, 0))
W.save(out)
