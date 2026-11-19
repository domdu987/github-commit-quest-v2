#!/usr/bin/env python3
"""deliver.py -- generic film-16 take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6, split if > 45 MB),
meta.json, cues.json, contact.jpg (16 frames, cyan line = y 880), framediff.json, QA_AUTO.md + phone_sheet.jpg.  No bpy.
Edit the TAKE block only.  Usage: python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---------------------------------------------------------------------------- TAKE
TAKE, SHOT = 's27', 27
G0, G1 = 1767, 1805
GA, GB = 1758, 1813
CUTS = [1767, 1805]
TRANS_IN = {'type': 'cut', 'frames': 0, 'note': 'hard cut from shot 26'}
LIGHT, PRESET = 'DAY', 'line_rail'
SET_NOTE = 'v3/set3d16 LINE line_rail DAY, platform area, train arriving from the right (x 138 -> 112)'
CAM_NOTE = 'custom 22 mm on the rail looking across at the platform; CamPath pull-back 12 %/s + slide 35 px/s, still moving at the end'
CAST_NOTE = 'messenger_wave, worker_a_wave, congressman_b_wave, congressman_c_wave on the platform (own marks near the bench), hands waving 3 Hz'
CUES = [(1758, 'ambience', 'station platform, steam, distant cheering'), (1780, 'accent', 'train whistle, people cheering')]
HEAD_ACTOR = 'msg'
# ---------------------------------------------------------------------------- /TAKE
N = GB - GA + 1


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        d.append(None if prev is None else float(np.abs(a - prev).mean()))
        prev = a
    return d


RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
gs = list(range(GA, GB + 1))
rows = []
for g in gs:
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in gs]
d = framediff(pngs)
ins = [d[g - GA] for g in range(G0, G1) if g - GA >= 1 and d[g - GA] is not None]      # in-shot pairs (g-1 -> g), g in the shot
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255; in-shot pairs only (no handle)",
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2), max=round(float(max(ins)), 2),
          target=dict(median=4.0, p90=12.0), per_pair={str(GA + i): (None if v is None else round(v, 2)) for i, v in enumerate(d)})
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

walls = [r["wall"] for r in rows]
cpus = [r["cpu"] for r in rows]
hd = [h for r in rows for k, h in r["heads"].items()] or [dict(w=0, y=0, bottom=0)]
meta = {"take": TAKE, "film": 16, "shots": [SHOT], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N, "shot_ranges": {str(SHOT): [G0, G1 - 1]},
        "handle_in": G0 - GA, "handle_out": GB - (G1 - 1), "transition_in": TRANS_IN, "set": SET_NOTE, "camera": CAM_NOTE, "cast": CAST_NOTE,
        "dof": "none", "text": "none", "light": LIGHT, "preset": PRESET, "samples": rows[0].get("samples"), "resolution": [720, 1280], "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in hd)), round(max(h["w"] for h in hd))],
        "head_centre_y": [round(min(h["y"] for h in hd)), round(max(h["y"] for h in hd))],
        "head_bottom_max_y": round(max(h["bottom"] for h in hd)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30)", cues=[dict(time=round(g / 30.0, 3), frame=g, kind=k, label=l) for g, k, l in CUES]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

w, h, cols = 270, 480, 8
S = Image.new("RGB", (cols * w, 2 * (h + 18)), (16, 12, 20))
dr = ImageDraw.Draw(S)
for i in range(16):
    g = GA + int(round(i * (N - 1) / 15.0))
    x, y = (i % cols) * w, (i // cols) * (h + 18)
    S.paste(Image.open(pngs[g - GA]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + 18))
    dr.line([(x, y + 18 + int(880 * h / 1280)), (x + w, y + 18 + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "" if G0 <= g < G1 else "  handle"), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
for old in glob.glob(mkv + "*"):
    os.remove(old)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
size = os.path.getsize(mkv)
if size > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True)
    os.remove(mkv)
    print("split into parts")
vid = mkv if os.path.exists(mkv) else None
if vid is None:       # qa_auto needs the whole file: rebuild a temp copy
    vid = os.path.join(HERE, "work", "tmp_take.mkv")
    os.makedirs(os.path.dirname(vid), exist_ok=True)
    subprocess.run("cat take.mkv.part* > work/tmp_take.mkv", shell=True, cwd=HERE, check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), vid, "--first_g", str(GA), "--cuts", ",".join(map(str, CUTS)), "--out", HERE],
                   capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-500:])
print("delivered %d frames %.1f MB; s/frame wall %.2f cpu %.2f; frame-diff median %.2f p90 %.2f; heads %s px"
      % (N, size / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"], meta["head_px"]))
