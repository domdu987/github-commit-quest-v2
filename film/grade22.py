"""Film 22 final grade toward the client's COLOUR_SPEC.md: conform grade only (no re-render), like film 21.
For each shot (film22/qa/shot_ranges.json):
  1. spec pre-grade (film22/spec_grade.py): only when the shot's hue shares are out of band (blue > 30 %, violet > 5 % or
     magenta > 10 %). It remaps violet to blue and magenta to crimson, trims blue saturation and adds the lamp warmth.
  2. the v1.1 grade (grade_v11.py, the skill's grade, as film 21 uses it): one S-curve, saturation x1.18, bloom on hot
     spots, red and white protection, ceiling 0.985. Its stage-1 SHOT values are solved per shot toward the spec centre
     (brightness V 0.54, saturation 0.43) and clamped, as film 21's grade21.py does.
usage: python3 grade22.py <frames_dir> [jobs]   (grades f_%04d.png in place; writes <frames_dir>/../grade22.json)
"""
import json, os, sys, glob, numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, HERE + "/film22"); sys.path.insert(0, HERE + "/v3/tools")
import grade_v11 as G, spec_grade as SG, hue_report as H
TV, TS = 0.54, 0.43
RANGES = json.load(open(HERE + "/film22/qa/shot_ranges.json"))


def _sv(ims):
    S, V = [], []
    for a in ims:
        x = np.concatenate([a[:1060], a[1200:]]).astype(np.float32) / 255
        mx, mn = x.max(-1), x.min(-1)
        S.append(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0).mean()); V.append(mx.mean())
    return float(np.mean(S)), float(np.mean(V))


def _hues(ims, tmp):
    os.makedirs(tmp, exist_ok=True)
    fl = []
    for i, a in enumerate(ims):
        f = f"{tmp}/h{i:03d}.png"; Image.fromarray(a).save(f); fl.append(f)
    h, s, v, dk = H.stats(fl)
    return h


def setup(fr):
    G.TAKES = [(n, a) for n, a, b in RANGES]; G.JOINS = []; G.FOG_G0, G.FOG_G1 = 10 ** 9, -1
    G.SHOT = {}; plan = {}
    for n, a, b in RANGES:
        gs = list(range(a, b, 10)) or [a]
        ims = [np.asarray(Image.open(f"{fr}/f_{g:04d}.png").convert("RGB")) for g in gs]
        h = _hues(ims, fr + "/../_hue_tmp")
        pre = h["blue"] > 30 or h["violet"] > 5 or h["magenta"] > 10
        if pre: ims = [SG.grade(x) for x in ims]
        p = dict(gain=1.0, gamma=1.0, sat=1.0)
        for _ in range(4):
            G.SHOT[n] = p
            s, v = _sv([G.grade_array(x, g) for x, g in zip(ims, gs)])
            p = dict(p)
            if v > TV: p["gain"] = float(np.clip(p["gain"] * TV / v, 0.70, 1.15)); p["gamma"] = 1.0
            else: p["gamma"] = float(np.clip(p["gamma"] * np.log(TV) / np.log(max(v, 0.05)), 0.85, 1.25))
            p["sat"] = float(np.clip(p["sat"] * TS / max(s, 1e-3), 0.55, 1.25))
        G.SHOT[n] = p; plan[n] = {"pre": bool(pre), "hues_before": {k: round(float(x), 1) for k, x in h.items()}, **p}
    return plan


def _work(args):
    f, g, pre, shot = args
    G.SHOT.update(shot)
    a = np.asarray(Image.open(f).convert("RGB"))
    if pre: a = SG.grade(a)
    Image.fromarray(np.asarray(G.grade_array(a, g))).save(f)
    return g


if __name__ == "__main__":
    fr = sys.argv[1]; jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    plan = setup(fr)
    json.dump(plan, open(os.path.dirname(fr.rstrip("/")) + "/grade22.json", "w"), indent=1)
    pre_of = {}
    for n, a, b in RANGES:
        for g in range(a, b): pre_of[g] = plan[n]["pre"]
    tasks = [(f, int(f[-8:-4]), pre_of.get(int(f[-8:-4]), False), G.SHOT) for f in sorted(glob.glob(fr + "/f_*.png"))]
    # resolve symlinks first so source take frames are never overwritten
    for f, *_ in tasks:
        if os.path.islink(f):
            im = Image.open(f).copy(); os.remove(f); im.save(f)
    with ProcessPoolExecutor(jobs) as ex:
        for i, g in enumerate(ex.map(_work, tasks, chunksize=8)):
            if i % 200 == 0: print("graded", i, "/", len(tasks), flush=True)
    print("grade22 done", json.dumps({k: (v["pre"], round(v["sat"], 2), round(v["gain"], 2), round(v["gamma"], 2)) for k, v in plan.items()}))
