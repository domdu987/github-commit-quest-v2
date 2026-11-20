#!/usr/bin/env python3
"""deliver.py -- delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json (cfg.json +
measured numbers), cues.json, contact.jpg (16 frames, cyan = caption band y 880), framediff.json (in-shot, 90x160 grey), qa_auto.
    python3 deliver.py            final        python3 deliver.py draft     work/draft -> contact + numbers only"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CFG = json.load(open(os.path.join(HERE, "cfg.json")))
G0, G1, H_IN, H_OUT = CFG["g0"], CFG["g1"], CFG["h_in"], CFG["h_out"]
FIRST = G0 - H_IN
N = G1 + H_OUT - FIRST
MB_LIMIT = 45e6


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d                                       # d[i] = diff between frame i and i+1 (index from FIRST)


def numbers(d):
    ins = d[H_IN:H_IN + (G1 - G0) - 1]              # pairs inside the shot only: g0..g1-1
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs inside g%d..g%d (handles excluded)" % (G0, G1 - 1),
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i in range(16):
        k = int(round(i * (len(pngs) - 1) / 15.0))
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = FIRST + k
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    assert len(src) == N, "draft has %d of %d" % (len(src), N)
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src))
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(FIRST, FIRST + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, FIRST + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
meta = dict(CFG["meta"])
meta.update({"take": CFG["take"], "film": 20, "shots": CFG.get("shots", [CFG["shot"]]), "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
             "shot_ranges": CFG.get("shot_ranges", {str(CFG["shot"]): [G0, G1 - 1]}), "handle_in": H_IN, "handle_out": H_OUT,
             "transition_in": {"type": "cut", "frames": 0, "handle_frames": H_IN, "note": "hard cut in from shot 20; handle g %d..%d rendered in 3D" % (FIRST, G0 - 1)},
             "transition_out": {"type": "dissolve", "frames": 13, "at": G1, "handle_frames": H_OUT, "note": "dissolve 13 into shot 23 (T23); handle g %d..%d rendered in 3D" % (G1, G1 + H_OUT - 1)},
             "dof": "none", "text": "none", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
             "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
             "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
             "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"})
hr = [{k: h for k, h in r["heads"].items() if 0 < h["x"] < 720 and 0 < h["y"] < 1280} for r in rows[H_IN:H_IN + G1 - G0] if r.get("heads")]
hr = [h for h in hr if h]
if hr:
    ws = [h["w"] for hh in hr for h in hh.values()]
    ys = [h["y"] for hh in hr for h in hh.values()]
    bs = [h["bottom"] for hh in hr for h in hh.values()]
    meta.update(head_px=[round(min(ws)), round(max(ws))], head_centre_y=[round(min(ys)), round(max(ys))], head_bottom_max_y=round(max(bs)))
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
cues = [dict(kind=c[0], t=round(c[1] / 30.0, 3), dur=round((c[2] - c[1]) / 30.0, 3), frame=c[1], end_frame=c[2], note=c[3]) for c in CFG["cues"]]
json.dump(dict(take=CFG["take"], fps=30, note="t = film seconds (g / 30); narration film20/audio/narration.wav at +0.10 s", cues=cues),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv %.1f MB: split into take.mkv.part*" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", str(G0)],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, %.1f MB; s/frame wall %.2f cpu %.2f; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
