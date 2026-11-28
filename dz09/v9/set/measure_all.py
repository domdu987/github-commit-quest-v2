"""measure_all.py -- writes look/measure.json: v6 vs v9 look shots vs ref D night/interior/day frames."""
import os, json, glob
import measure9 as M
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
R = {}
for n in (76, 80, 82, 36, 115):
    R[f"ref_f{n:03d}"] = M.metrics(os.path.join(PROJ, "ref", "d", "frames2", f"f_{n:03d}.png"), ref=True)
for s in ("s06", "s09", "s13", "s18", "s20", "s24"):
    R[f"v6_{s}"] = M.metrics(os.path.join(PROJ, "v6", "look", "out", f"{s}_916.png"))
    R[f"p1_{s}"] = M.metrics(os.path.join(HERE, "look", "pass1", f"{s}_916.png"))
    R[f"v9_{s}"] = M.metrics(os.path.join(HERE, "look", "out", f"{s}_916.png"))
for s in ("s06", "s24"):
    R[f"p1_{s}_169"] = M.metrics(os.path.join(HERE, "look", "pass1", f"{s}_169.png"))
    R[f"v9_{s}_169"] = M.metrics(os.path.join(HERE, "look", "out", f"{s}_169.png"))
R["times"] = json.load(open(os.path.join(HERE, "look", "out", "times.json")))
json.dump(R, open(os.path.join(HERE, "look", "measure.json"), "w"), indent=1)
keys = ["L_mean", "deep_shadow", "L_p95", "blue", "orange", "red", "magenta", "violet", "shade_hue", "edges", "local_contrast"]
print(f"{'':14s}" + "".join(f"{k[:9]:>10s}" for k in keys))
for k, v in R.items():
    if k == "times": continue
    print(f"{k:14s}" + "".join(f"{v[x]:10.3f}" for x in keys))
