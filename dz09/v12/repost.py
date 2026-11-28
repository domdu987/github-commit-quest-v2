"""repost.py [LEVEL=v ...] -- re-run post11 on the kept passes of the 6 proof stills -> v12/after/"""
import sys, os, glob, shutil, time
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in ("v4/set_expressway", "v11/set"): sys.path.insert(0, os.path.join(PROJ, p))
import render11, post11
kw = {a.split("=")[0]: float(a.split("=")[1]) for a in sys.argv[1:] if "=" in a}
tag = [a for a in sys.argv[1:] if "=" not in a]; tag = tag[0] if tag else "after"
src = os.path.join(PROJ, "v10/film/out/final_720x1280/stills_before")
dst = os.path.join(PROJ, "v12", tag); os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(src + "/S*_info.json")):
    o = f[:-len("_info.json")]
    if len(sys.argv) > 2 and sys.argv[-1].startswith("S") and os.path.basename(o)[:3] not in sys.argv[-1]: continue
    t = time.process_time(); render11.repost(o, **kw); print(os.path.basename(o), "post cpu %.1f" % (time.process_time() - t))
    shutil.copy(o + ".png", os.path.join(dst, os.path.basename(o) + ".png"))
