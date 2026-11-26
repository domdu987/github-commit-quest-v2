#!/usr/bin/env python3
"""deliver_take.py <take dir> -- generic delivery for a film-24 take: reads <dir>/take.json
{take, shots:{id:[g0,g1]}, first_g, last_g, cuts:[g..], note}, copies raw/s<id>/g_*.png to frames/, writes meta.json, contact.jpg,
phone-ready 6 fps strips (work/strip_*.jpg), work/qa.txt and encodes take.mkv (split >45 MB)."""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.abspath(sys.argv[1]); cfg = json.load(open(os.path.join(HERE, "take.json")))
OUT = os.path.join(HERE, "frames"); WORK = os.path.join(HERE, "work"); os.makedirs(OUT, exist_ok=True); os.makedirs(WORK, exist_ok=True)
shots = {int(k): v for k, v in cfg["shots"].items()}; F0, F1 = cfg["first_g"], cfg["last_g"]
sid = lambda g: [s for s, (a, b) in shots.items() if a <= g <= b][0]
rows = []
for g in range(F0, F1 + 1):
    raw = os.path.join(HERE, "raw", "s%d" % sid(g))
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
mean = lambda v: round(float(np.mean(v)), 1)
wall, cpu = mean([r["wall"] for r in rows]), mean([r["cpu"] for r in rows])
meta = dict(take=cfg["take"], film=24, shots=list(shots), g0=cfg["g0"], g1=cfg["g1"], first_g=F0, n_frames=F1 - F0 + 1,
            handle_in=cfg["g0"] - F0, handle_out=F1 - cfg["g1"] + 1,
            transition_in=dict(type="cut", frames=0), transition_out=dict(type="cut", frames=0),
            shot_ranges={str(s): v for s, v in shots.items()}, cuts_in_take=cfg.get("cuts", []), note=cfg.get("note", ""),
            samples=cfg.get("samples", 24), resolution=[720, 1280], render_resolution=[540, 960], fps=30,
            s_per_frame_wall_mean=wall, s_per_frame_cpu_mean=cpu)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
if os.path.exists(os.path.join(HERE, "cues.src.json")):
    cues = json.load(open(os.path.join(HERE, "cues.src.json")))
    json.dump(dict(take=cfg["take"], fps=30, note="time = film seconds (g/30)", cues=cues), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)


def sheet(gs, path, w=270, cols=8, lab=18):
    h = w * 16 // 9; nrow = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, nrow * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d  %.2f s  shot-id %d" % (g, g / 30.0, sid(g)), fill=(255, 255, 255))
    S.save(path, quality=88)


N = F1 - F0 + 1
sheet([F0 + int(round(i * (N - 1) / 15.0)) for i in range(16)], os.path.join(HERE, "contact.jpg"))
allg = list(range(F0, F1 + 1, 5))
for i in range(0, len(allg), 32):
    sheet(allg[i:i + 32], os.path.join(WORK, "strip_%d.jpg" % (i // 32)), w=240)
for c in cfg.get("cuts", []):
    sheet(list(range(c - 3, c + 4)), os.path.join(WORK, "cut_%d.jpg" % c), w=240, cols=7)
with open(os.path.join(WORK, "qa.txt"), "w") as fo:
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [r["heads"][n] for r in rows if n in r["heads"]]
        fo.write("%-4s head w %.0f..%.0f px, centre y %.0f..%.0f, bottom max %.0f (band 880)\n" % (
            n, min(h["w"] for h in hs), max(h["w"] for h in hs), min(h["y"] for h in hs), max(h["y"] for h in hs), max(h["bottom"] for h in hs)))
    fo.write("render wall %.1f s / cpu %.1f s per frame\n" % (wall, cpu))
if "--no-encode" not in sys.argv:
    mkv = os.path.join(HERE, "take.mkv")
    for p in glob.glob(mkv + "*"):
        os.remove(p)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(F0), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    mb = os.path.getsize(mkv) / 1e6; print("take.mkv %.1f MB" % mb)
    if mb > 45:
        subprocess.run(["split", "-b", "40M", "take.mkv", "take.mkv.part"], check=True, cwd=HERE); os.remove(mkv)
print(json.dumps(meta)[:300])
