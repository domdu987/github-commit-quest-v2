#!/usr/bin/env python3
"""qa_write.py <take_dir> <title> "<camera move>" "<notes>"  -> QA.md (metrics, s/frame from the per-frame meta, heads / feet from the meta, files)"""
import os, sys, json, glob
td = os.path.abspath(sys.argv[1]); title, move, notes = sys.argv[2], sys.argv[3], (sys.argv[4] if len(sys.argv) > 4 else "")
meta = json.load(open(os.path.join(td, "meta.json")))
ms = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(td, "work", "meta", "g_*.json")))]
ms = [m for m in ms if meta["first_g"] <= m["g"] < meta["g1"]]
wall = [m["wall_total"] for m in ms]
heads, feet = [], []
for m in ms:
    for n, a in m["actors"].items():
        heads.append(a["head"][1] - a["hw"] / 2); feet.append(a["feet"][1])
met = open(os.path.join(td, "metrics.txt")).read().split("--- jitter ---")[0].strip()
jit = open(os.path.join(td, "metrics.txt")).read().split("--- jitter ---")[1].split("--- qa_auto ---")[0].strip()
txt = """# %s

## Scope
- g %d-%d (first_g %d, %d frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 %% + white-card shading pass 10 samples at 50 %%), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: %s
- Render: mean %.0f s wall per frame per process (2 processes x 2 threads running at the same time; min %.0f, max %.0f).

## light_metrics
```
%s
```
## qa_jitter
```
%s
```
## Framing numbers (from the per-frame meta)
- highest head top y %.0f px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y %.0f px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
%s
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
""" % (title, meta["g0"], meta["g1"] - 1, meta["first_g"], meta["n_frames"], move, sum(wall) / max(1, len(wall)), min(wall or [0]), max(wall or [0]), met, jit, min(heads or [0]), max(feet or [0]), notes)
open(os.path.join(td, "QA.md"), "w").write(txt)
print(txt[:400])
