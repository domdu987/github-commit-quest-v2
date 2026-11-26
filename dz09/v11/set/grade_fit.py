"""grade_fit.py -- fit per-shot grade (exposure, toe) on kept passes so p95 luma ~0.78 and deep-shadow share
(L < 0.05) ~0.12 (ref D night 0.09-0.24). Writes look/grade_fit.json and re-posts the frames in look/out.
Needs bpy (EXR reading): python3 grade_fit.py [tags]"""
import os, sys, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [HERE, os.path.join(PROJ, "v4", "set_expressway")]
import render9, measure9
O = os.path.join(HERE, "look", "out") + "/"
T = os.path.join(HERE, "look", "tmp_fit") + "/"; os.makedirs(T, exist_ok=True)
P95, DEEP = 0.78, 0.12

def trial(tag, ex, toe):
    p = render9.repost(T + tag, exposure=ex, toe=toe)
    m = measure9.metrics(p); return m["L_p95"], m["deep_shadow"], m

def fit(tag):
    for ext in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_info.json", "_shafts.pkl", "_raw.png"):
        shutil.copy(O + tag + ext, T + tag + ext)
    ex0 = json.load(open(O + tag + "_info.json")).get("exposure", 1.5)
    toe = 0.014
    lo, hi = 0.4 * ex0, 1.4 * ex0
    for _ in range(5):                                   # exposure for p95
        ex = (lo + hi) / 2; p95, deep, _ = trial(tag, ex, toe)
        if p95 > P95: hi = ex
        else: lo = ex
    ex = (lo + hi) / 2
    tlo, thi = 0.005, 0.08
    for _ in range(5):                                   # toe for deep shadow share
        toe = (tlo + thi) / 2; p95, deep, _ = trial(tag, ex, toe)
        if deep < DEEP: tlo = toe
        else: thi = toe
    toe = (tlo + thi) / 2
    p95, deep, m = trial(tag, ex, toe)
    return dict(exposure=round(ex, 3), toe=round(toe, 4), p95=round(p95, 3), deep=round(deep, 3), L_mean=round(m["L_mean"], 3))

if __name__ == "__main__":
    tags = sys.argv[1].split(",") if len(sys.argv) > 1 else ["s06_916", "s09_916", "s13_916", "s18_916", "s20_916", "s24_916", "s06_169", "s24_169"]
    fp = os.path.join(HERE, "look", "grade_fit.json")
    R = json.load(open(fp)) if os.path.exists(fp) else {}
    for t in tags:
        R[t] = fit(t); print(t, R[t], flush=True)
        render9.repost(O + t, exposure=R[t]["exposure"], toe=R[t]["toe"])
    json.dump(R, open(fp, "w"), indent=1)
    shutil.rmtree(T, ignore_errors=True)
