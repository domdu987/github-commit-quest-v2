#!/usr/bin/env python3
"""deliver.py <sNN>: after `shot.py final all`: take.mkv, meta.json (g0,g1,g1_render,first_g,n_frames,transition_in), qa_auto + qa_jitter + frame-diff stats +
shade hue + contact.jpg, written to QA_NUMBERS.json (QA.md is written by hand from it).   usage: python3 deliver.py   (run inside the take folder)"""
import os, sys, json, glob, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PROJ = "/home/user/github-commit-quest-v2/film"
sys.path.insert(0, PROJ + "/v3/set3d23")
import importlib.util
spec = importlib.util.spec_from_file_location("shot", os.path.join(HERE, "shot.py"))
# only need the clock numbers: do not build the scene
import ast
src = open(os.path.join(HERE, "shot.py")).read()
SID = [l for l in src.splitlines() if l.strip().startswith("SID = ")][0].split('"')[1]
D_IN = int([l for l in src.splitlines() if l.strip().startswith("D_IN = ")][0].split("=")[1].split("#")[0])
import math as _m
sys.path.insert(0, PROJ + "/v3/set3d23")
import ghost_shots as SH
sh = SH.SHOTS[SID]
g0, g1 = int(round(sh["t0"] * 30)), int(round(sh["t1"] * 30))
gr = g0 + int(_m.ceil((g1 - g0) * 1.25))
h_in = (int(_m.ceil(D_IN / 2.0)) + 2) if D_IN else 0
first = g0 - h_in
n = gr - first + 1
raw = HERE + "/raw"
fr = sorted(glob.glob(raw + "/g_*.png"))
assert len(fr) == n, (len(fr), n)
out = {}
if not os.path.exists(HERE + "/take.mkv") and not glob.glob(HERE + "/take.mkv.part*"):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", raw + "/g_%04d.png", "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow",
                    HERE + "/take.mkv"], check=True)
sz = os.path.getsize(HERE + "/take.mkv") if os.path.exists(HERE + "/take.mkv") else 0
out["take_mb"] = round(sz / 1e6, 1)
if sz > 45e6:
    subprocess.run("split -b 40M -d take.mkv take.mkv.part && rm take.mkv", shell=True, cwd=HERE, check=True)
vid = HERE + "/take.mkv" if os.path.exists(HERE + "/take.mkv") else None
if vid is None:   # split: qa on a temporary concat
    subprocess.run("cat take.mkv.part* > /tmp/claude-0/_tmp_%s.mkv" % SID, shell=True, cwd=HERE, check=True); vid = "/tmp/claude-0/_tmp_%s.mkv" % SID
meta = dict(take=os.path.basename(HERE), film=23, shots=[sh["n"]], first_g=first, n_frames=n, g0=g0, g1=g1, g1_render=gr, handle_in=h_in, tail_frames=gr - g1,
            transition_in=dict(type="dissolve" if D_IN else "cut", frames=D_IN), fps=30, size=[720, 1280], samples=12, location=sh["loc"], light=sh["light"], split=(sz > 45e6))
json.dump(meta, open(HERE + "/meta.json", "w"), indent=1)
# qa_auto (cuts: none inside the take)
r = subprocess.run(["python3", PROJ + "/qa_auto.py", vid, "--first_g", str(first), "--out", HERE], capture_output=True, text=True)
out["qa_auto_rc"] = r.returncode; out["qa_auto_tail"] = r.stdout[-1500:]
r = subprocess.run(["python3", PROJ + "/qa_jitter.py", vid], capture_output=True, text=True)
out["qa_jitter"] = r.stdout.strip()
open(HERE + "/QA_JITTER.txt", "w").write(r.stdout)
# frame diffs on 90x160 grey, in-shot frames g0 .. gr
gs = []
for p in fr:
    g = int(os.path.basename(p)[2:6])
    if g0 <= g <= gr:
        gs.append(np.asarray(Image.open(p).convert("L").resize((90, 160), Image.BILINEAR), dtype=np.float32))
d = np.array([np.abs(a - b).mean() for a, b in zip(gs[:-1], gs[1:])])
out["fdiff_median"] = round(float(np.median(d)), 2); out["fdiff_p90"] = round(float(np.percentile(d, 90)), 2); out["fdiff_min"] = round(float(d.min()), 2)
# shade hue on first / mid / last frame
import ghost_hue as GHU
hs = {}
for lab, g in (("first", first), ("mid", (g0 + g1) // 2), ("last", gr)):
    p = raw + "/g_%04d.png" % g
    h, fr_ = GHU.shade_hue(p); hs[lab] = dict(g=g, hue=round(h, 1), shaded_frac=round(fr_, 3))
out["shade_hue"] = hs
# heads from the report jsons
heads = {}
for p in fr:
    j = json.load(open(p[:-4] + ".json"))
    for k, v in j.get("heads", {}).items():
        t = heads.setdefault(k, dict(ymax=-1e9, ymin=1e9, xmin=1e9, xmax=-1e9, wmax=0))
        t["ymax"] = max(t["ymax"], v["y"]); t["ymin"] = min(t["ymin"], v["y"]); t["xmin"] = min(t["xmin"], v["x"]); t["xmax"] = max(t["xmax"], v["x"]); t["wmax"] = max(t["wmax"], v["w"])
out["heads"] = heads
walls = [json.load(open(p[:-4] + ".json")).get("wall", 0) for p in fr]
out["s_per_frame_wall_mean"] = round(float(np.mean(walls)), 1)
out["cpu_s_per_frame_mean"] = round(float(np.mean([json.load(open(p[:-4] + ".json")).get("cpu", 0) for p in fr])), 1)
# contact sheet: 16 frames, cyan line at y 880
idx = np.linspace(0, len(fr) - 1, 16).astype(int)
tiles = []
for i in idx:
    im = Image.open(fr[i]).convert("RGB").resize((180, 320)); dr = ImageDraw.Draw(im); y = int(880 / 4)
    dr.line([(0, y), (180, y)], fill=(0, 255, 255), width=1); dr.text((3, 3), "g%d" % (first + i), fill=(255, 255, 0)); tiles.append(im)
sheet = Image.new("RGB", (180 * 8, 320 * 2))
for k, t in enumerate(tiles): sheet.paste(t, ((k % 8) * 180, (k // 8) * 320))
sheet.save(HERE + "/contact.jpg", quality=88)
json.dump(out, open(HERE + "/QA_NUMBERS.json", "w"), indent=1)
print(json.dumps(out, indent=1, ensure_ascii=False))
