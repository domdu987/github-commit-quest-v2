#!/usr/bin/env python3
"""deliver.py -- delivery for this take from raw/g_%04d.png: frames/, take.mkv, meta.json, cues.json, contact.jpg, framediff.json, qa_auto."""
import os, sys, json, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = os.path.basename(HERE)
CFG = {"s26": dict(shot=26, g0=1912, g1=1968, first=1908, last=1971, cut_in=1912, cut_out=1968, set="RESTO resto_view DAY 1889",
                   cues=[(1908, 1972, "ambience", "restaurant room tone (first-floor restaurant of the tower): murmur, cutlery, a faint string trio; open window air"),
                         (1912, 1928, "foley", "glass rises: cloth rustle of his sleeve, light glass ring", 1920),
                         (1939, 1951, "accent", "snap push on 'หอไอเฟล': soft airy whoosh + a tiny glass 'tink' as he lifts the glass to the view", 1941),
                         (1968, 1968, "cut", "hard cut to shot 27 (the last image): ambience swaps to wind + distant fair")]),
       "s27": dict(shot=27, g0=1968, g1=2046, first=1964, last=2045, cut_in=1968, cut_out=None, set="TOWER tower_window_pull DAY 1889",
                   cues=[(1964, 2046, "ambience", "wind at the tower's first floor swelling into open air, distant fair crowd and band, a pennant flapping"),
                         (1968, 2000, "accent", "crash pull-out: big falling whoosh with a doppler-like drop as the lit window shrinks into the lattice", 1974),
                         (2020, 2020, "accent", "last word 'สักครั้ง': one soft final note; tower hums, silence follows", 2020),
                         (2046, 2046, "cut", "hard cut to black on the last word (end of film)")])}[TAKE]
GRADE = (1.5, 1.2, 0.9) if TAKE == "s26" else None
G0, G1, FIRST, LAST = CFG["g0"], CFG["g1"], CFG["first"], CFG["last"]
N = LAST - FIRST + 1
RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows, pngs = [], []
for g in range(FIRST, LAST + 1):
    if GRADE:      # film-20 §7 colour gate: the bright cream/white interior scored sat 0.36 / luma 129 -> post grade (gain 0.9, gamma 1.2, sat x1.5)
        x = np.clip(np.asarray(Image.open(os.path.join(RAW, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32) / 255.0 * GRADE[2], 0, 1) ** GRADE[1]
        l = x.mean(-1, keepdims=True)
        Image.fromarray((np.clip(l + (x - l) * GRADE[0], 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(OUT, "g_%04d.png" % g))
    else:
        shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g)))); pngs.append(os.path.join(OUT, "g_%04d.png" % g))
prev, d = None, []
for i, p in enumerate(pngs):
    a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
    if prev is not None and FIRST + i >= G0 + 1 and FIRST + i < G1:      # pairs inside the shot only
        d.append(float(np.abs(a - prev).mean()))
    prev = a
nb = dict(method="mean abs diff of consecutive frames, grey, 90x160, in-shot pairs only (no handles)", median=round(float(np.median(d)), 2),
          p90=round(float(np.percentile(d, 90)), 2), min=round(min(d), 2), max=round(max(d), 2), target=dict(median=4.0, p90=12.0))
json.dump(dict(nb, per_pair=[round(v, 2) for v in d]), open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [r["heads"]["mau"] for r in rows if "mau" in r["heads"] and G0 <= r["g"] < G1]
meta = {"take": TAKE, "film": 20, "shots": [CFG["shot"]], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(CFG["shot"]): [G0, G1 - 1]}, "handle_in": G0 - FIRST, "handle_out": LAST - (G1 - 1),
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0, "at": G1},
        "set": CFG["set"], "dof": "none", "text": "none", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads), 1), round(max(h["w"] for h in heads), 1)],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
if TAKE == "s27":
    meta["note"] = "film ends on a hard cut at g 2046 (no out handle); in-handle g 1964..1967 renders the pull backwards-extended"
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
cues = []
for c in CFG["cues"]:
    e = dict(kind=c[2], t=round(c[0] / 30.0, 3), dur=round(max(0, c[1] - c[0]) / 30.0, 3), frame=c[0], end_frame=c[1], note=c[3])
    if len(c) > 4: e["peak_frame"] = c[4]
    cues.append(e)
json.dump(dict(take=TAKE, fps=30, note="t = film seconds (g/30)", cues=cues), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
w = 270; h = w * 16 // 9
S = Image.new("RGB", (8 * w, 2 * (h + 18)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i in range(16):
    g = int(round(i * (N - 1) / 15.0)); x, y = (i % 8) * w, (i // 8) * (h + 18)
    S.paste(Image.open(pngs[g]).convert("RGB").resize((w, h)), (x, y + 18))
    dr.line([(x, y + 18 + int(880 * h / 1280)), (x + w, y + 18 + int(880 * h / 1280))], fill=(0, 200, 220)); dr.text((x + 4, y + 3), "g %d" % (FIRST + g), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
cuts = [str(c) for c in (CFG["cut_in"], CFG["cut_out"]) if c]
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(cuts)], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames %.1f MB; s/frame wall %.2f cpu %.2f; framediff median %.2f p90 %.2f" % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
