#!/usr/bin/env python3
"""deliver.py -- delivery of this take from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json,
contact.jpg (16 in-shot frames, cyan line = caption band y 880), framediff.json (in-shot, 90x160 grey), then qa_auto.py.  No bpy.
    python3 deliver.py            final delivery
    python3 deliver.py draft      look at a draft (work/draft): contact + frame-diff numbers, nothing delivered
The CONFIG block is the only thing that differs between takes."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ------------------------------------------------------------------ CONFIG
TAKE, SHOT = "s05", 5
G0, G1, H_IN, H_OUT = 256, 314, 9, 9               # shot = g G0..G1-1 ; handles G0-H_IN..G0-1 and G1..G1+H_OUT-1
TRANS_IN = {"type": "cut", "frames": 0, "at": G0, "note": "hard cut from shot 4 at g %d; handle g %d..%d continues the move" % (G0, G0 - H_IN, G0 - 1)}
TRANS_OUT = {"type": "cut", "frames": 0, "at": G1, "note": "hard cut to shot 6 (studio_door) at g %d; handle g %d..%d continues the move" % (G1, G1, G1 + H_OUT - 1)}
SET_NOTE = "v3/set3d16 STUDIO preset studio_easel, light DAY; runtime: preset FG hidden, own jars + brush pot FG (tg_studio.fg_dress); wife oval portrait on the side table in frame"
CAST_NOTE = "v3/cast16 morse16 young=1: STORY16 morse_young_paint with a painting cycle (brush hand to canvas / palette, 34 f), blinks, breathing; mouth still"
CAM_NOTE = "custom 22 mm, push 8 %/s + slide 80 px/s + arc 10 deg/s (c16.CamPath, decay 0.3); plus a short snap x1.5 with a 0.55 D pan on 'วาดรูปอยู่' g 283..296 (the shot is 1.9 s; added for the p90 frame-diff target)"
AMBIENCE = "Morse's painting room 1825, warm window light, distant street murmur, brush scratching canvas"
EV = {"snap": [283, 296], "word_draw": 286, "portrait_in_frame": [256, 313]}
CUES = [(256, 314, "foley", "brush strokes on canvas, palette tapped", 280), (283, 296, "accent", "soft whoosh on the push", 288)]
CUT_PLAN = [314]
# ------------------------------------------------------------------ end CONFIG
CFG = json.load(open(os.path.join(HERE, "take_cfg.json"))) if os.path.exists(os.path.join(HERE, "take_cfg.json")) else {}
for k, v in CFG.items():
    globals()[k] = v
GF, GL = G0 - H_IN, G1 + H_OUT - 1
N = GL - GF + 1
NSHOT = G1 - G0


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (NSHOT - 1) / 15.0)) + H_IN for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(idx):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = GF + k
        dr.text((x + 4, y + 3), "g %d  %.2f s" % (g, g / 30.0), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[H_IN:H_IN + NSHOT - 1]               # pairs (g-1, g) for g = G0+1 .. G1-1 : inside the shot, no handles
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs g-1->g for g %d..%d (in-shot, no handles)" % (G0 + 1, G1 - 1),
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    assert len(src) == N, "draft has %d of %d frames" % (len(src), N)
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src))
    json.dump(nb, open(os.path.join(HERE, "work", "draft_framediff.json"), "w"), indent=1)
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(GF, GL + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(GF, GL + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
ins_rows = rows[H_IN:H_IN + NSHOT]
heads = [h for r in ins_rows for h in r["heads"].values()]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
meta = {"take": TAKE, "film": 16, "shots": [SHOT], "g0": G0, "g1": G1, "first_g": GF, "n_frames": N, "shot_ranges": {str(SHOT): [G0, G1 - 1]},
        "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TRANS_IN, "transition_out": TRANS_OUT, "set": SET_NOTE, "cast": CAST_NOTE, "camera": CAM_NOTE,
        "events": EV, "dof": "none", "text": "none", "light": "DAY", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = [dict(time=round(GF / 30.0, 3), duration=round(N / 30.0, 3), frame=GF, end_frame=GL + 1, kind="ambience", label=AMBIENCE)]
for a, b, kind, label, pk in CUES:
    ev.append(dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label, peak_frame=pk))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GF), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GF), "--cuts", ",".join(map(str, CUT_PLAN))], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
mb = os.path.getsize(mkv) / 1e6
if mb > 45:
    subprocess.run("cd %s && split -b 40M take.mkv take.mkv.part && rm take.mkv" % HERE, shell=True, check=True)
print("delivered %d frames g %d..%d, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, GF, GL, mb, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
