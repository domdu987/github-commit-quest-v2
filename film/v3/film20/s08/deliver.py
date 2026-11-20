#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json, cues.json,
contact.jpg, framediff.json, then qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE, SHOT = "s08", 8
G0, G1, H_IN, H_OUT = 513, 604, 4, 4
GA = G0 - H_IN
N = (G1 + H_OUT) - GA
TRANS_IN = {'type': 'cut', 'frames': 0}
CUTS_OUT = [G1]
EV = {'smoke_ramp': [513, 572], 'word_chimney': 572, 'snap': [570, 585], 'word_black': 590}
CAMERA = "custom 22 mm cafe_window start (0.9, -2.6, 2.4) D (preset (1.32, 0.38, 2.82)), aim +3 deg above the camera->window line (pitch ~6.5); c20.CamPath push 8 %/s toward the window + slide 18 px/s + snap x1.3 g 570..585 on 'เหมือนปล่อง'; decay 0.25"
CAST = 'v3/cast20 painter20 / composer20 / poet20 / architect20 outraged heads, pointing arms (finger jabs ~1.9 Hz toward the window, bigger on the snap), 3 Hz breathing bounce; architect + painter as BACK cards over-shoulder in the left foreground, poet flipped to face left; mouths held'
SET = 'v3/set3d20 CAFE cafe_window DAY, window view stub, smoke ramp 0 -> 1 over g 513..572 (17.10-18.96 s) then 1.0, keyed every frame'
CUES = [(509, 607, 'ambience', 'Café 1887: indignant murmur, gas-lamp hiss; through the window the distant clang of the building site'), (513, 572, 'foley', 'finger jabs at the window: quick cloth swishes, huffs of outrage (no words)', {'peak_frame': 540}), (513, 572, 'accent', 'forge smoke starts to rise from the tower stub: low rumbling swell building up to the chimney reveal', {'peak_frame': 572}), (570, 585, 'accent', "snap push on 'เหมือนปล่อง': whoosh + a dark ominous brass sting as the black smoke column stands full", {'peak_frame': 575}), (604, 604, 'cut', 'hard cut to shot 9 (Maupassant rises)')]
SOUND_NOTE = "t = film seconds (g / 30); narration PROJ/film20/audio/narration.wav at +0.10 s"
MB_LIMIT = 45e6
IN_SHOT = (G0 + 1, G1 - 1)                      # pairs (g-1 -> g) for g in this range


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d                                    # d[i] = pair (GA+i -> GA+i+1)


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[g]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        gg = GA + g
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "  handle" if (gg < G0 or gg >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
rows = []
for i in range(N):
    g = GA + i
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % (GA + i)) for i in range(N)]
d = framediff(pngs)
ins = [d[g - 1 - GA] for g in range(IN_SHOT[0], IN_SHOT[1] + 1)]
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs g-1->g for g %d..%d (in shot, no handles)" % IN_SHOT,
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2), max=round(float(max(ins)), 2),
          target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
hd = {}
for r in rows[H_IN:H_IN + (G1 - G0)]:
    for k, v in r.get("heads", {}).items():
        hd.setdefault(k, []).append(v)
heads = {k: dict(w=[round(min(x["w"] for x in v)), round(max(x["w"] for x in v))], y=[round(min(x["y"] for x in v)), round(max(x["y"] for x in v))],
                 bottom_max=round(max(x["bottom"] for x in v))) for k, v in hd.items()}
meta = {"take": TAKE, "film": 20, "shots": [SHOT], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N, "shot_ranges": {str(SHOT): [G0, G1 - 1]},
        "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TRANS_IN,
        "transition_out": {"type": "cut", "frames": 0, "at": G1, "note": "hard cut at g %d; out-handle g %d..%d rendered in 3D (the move continues)" % (G1, G1, G1 + H_OUT - 1)},
        "set": SET, "cast": CAST, "camera": CAMERA, "events": EV, "dof": "none", "text": "none", "light": "DAY", "year": 1887,
        "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "heads_px_in_shot": heads, "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in CUES:
    g0, g1, kind, note = c[:4]
    e = dict(kind=kind, t=round(g0 / 30.0, 3), dur=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, note=note)
    if len(c) > 4:
        e.update(c[4])
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note=SOUND_NOTE, cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv is %.1f MB: split into take.mkv.part*" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GA), "--cuts", ",".join(map(str, CUTS_OUT))], capture_output=True, text=True, cwd=HERE)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
