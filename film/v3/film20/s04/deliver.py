#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json, cues.json,
contact.jpg, framediff.json, then qa_auto.py.  No bpy.   python3 deliver.py | python3 deliver.py draft"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---- CONFIG (per take)
TAKE, SHOT = "s04", 4
G0, G1 = 265, 318
H_IN, H_OUT = 4, 4
TRANS_IN = {"type": "cut", "frames": 0}
NOTE = "SITE site_table DAY stage 0: Eiffel at the plan table points up proudly on 'วิศวกรไอเฟล' (arm up g 266-274); push + slide + arc + tilt"
CUES = [(265, 'ambience', 'building site: distant hammering, forge, wind', {}), (268, 'foley', "cloth rustle as his arm goes up, a proud 'hm'", {'peak_frame': 270}), (268, 'accent', "small bright sting on 'วิศวกรไอเฟล'", {})]
# ----
GF, GL = G0 - H_IN, G1 + H_OUT - 1
N = GL - GF + 1
MB_LIMIT = 45e6


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def numbers(d):
    ins = d[H_IN:H_IN + (G1 - G0) - 1]        # pairs (g-1,g) for g in G0+1 .. G1-1: in-shot only
    return dict(method="mean abs diff of consecutive frames, grey, 90x160 bilinear; pairs inside the shot (no handles)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = GF + k
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    d = framediff(src)
    nb = numbers(d)
    print("draft frame-diff median %.2f p90 %.2f" % (nb["median"], nb["p90"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(GF, GL + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(GF, GL + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
heads = [h for r in rows[H_IN:H_IN + G1 - G0] for h in r["heads"].values()]
meta = {"take": TAKE, "film": 20, "shots": [SHOT], "g0": G0, "g1": G1, "first_g": GF, "n_frames": N, "shot_ranges": {str(SHOT): [G0, G1 - 1]},
        "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TRANS_IN,
        "transition_out": {"type": "cut", "frames": 0, "at": G1, "note": "next shot is a hard cut; 4 handle frames rendered in 3D"},
        "note": NOTE, "dof": "none", "text": "none", "light": "DAY", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in CUES:
    g, kind, note, kw = c
    e = dict(kind=kind, t=round(g / 30.0, 3), frame=g, note=note)
    e.update(kw)
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note="t = film seconds (g / 30)", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GF), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GF), "--cuts", str(G1)], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
