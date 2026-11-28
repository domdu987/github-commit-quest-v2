"""Hook v3 = v2 (comp_nozoom) with the biohazard title mark removed: frames from the title hit on are re-composited
from the raw renders (finish.SHOW_TITLE = False, so no title dim either); every earlier frame is v2's, unchanged."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import finish as Fn, common as C, noicons
base = Fn.base_dir("final", 720, 1280)
A, N = os.path.join(base, "comp_nozoom"), os.path.join(base, "comp_notitle")
os.makedirs(N, exist_ok=True)
for g in range(C.NF):
    d = os.path.join(N, "f_%04d.png" % (g + 1))
    if os.path.exists(d): os.remove(d)
    if g >= noicons.G_TITLE:
        im = Fn.comp_frame(base, g, 720, 1280); assert im is not None, g
        im.save(d, compress_level=1)
    else:
        os.link(os.path.join(A, "f_%04d.png" % (g + 1)), d)
print("built", N)
