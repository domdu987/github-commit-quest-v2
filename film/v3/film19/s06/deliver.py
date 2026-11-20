#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg,
framediff.json, qa_auto (QA_AUTO.md + phone_sheet.jpg).  No bpy.
    python3 deliver.py          final delivery
    python3 deliver.py draft    work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = "s06"
SHOTS = [6]
G0, G1 = 356, 466
H_IN, H_OUT = 9, 9
FIRST = G0 - H_IN                      # 101
LAST = G1 + H_OUT - 1                  # 199
N = LAST - FIRST + 1
TRANS_IN = dict(type="dissolve", frames=13, note="DIS 13 from shot 5 (SHIP ship_rocks); 9 handle frames g 347..355 rendered in 3D (half dissolve 6.5 + 2)")
TRANS_OUT = dict(type="cut", frames=0, at=466, note="CUT to shot 7; 9 handle frames g 466..474 rendered in 3D")
CUTS = [G0 - FIRST]                    # qa_auto: planned cut index (frame index of the cut in the mkv)
SET = 'v3/set3d19/h19.py HALL preset hall_table, light DAY; set_moneybag none -> full keyed at g 378 (bag pivot keyed to fall, bounce, squash and settle), set_candles(1.0) on every frame; no caption_shade'
CAST = 'v3/cast19 astro19 (left, faces right) and astro19_b (right, mirrored): lean in toward the bag, excited, eyes on it; expression mouths only'
CAMERA = "custom 22 mm, c19.CamPath: push 6 %/s + arc, SNAP x1.7 (15 f) pushing in on the bag at 'สองหมื่นปอนด์' (g 447)"
EVENTS = dict(bag_drop=378, snap=[439, 454], word_20000_g=447)
AMB = [(356, 466, "ambience", "hall, afternoon: quiet room tone, distant clock tick"),
       (378, 392, "accent", "money bag drops onto the baize: heavy thud, coin jingle, a small bounce"),
       (439, 454, "accent", "snap push-in on 'สองหมื่นปอนด์': short airy whoosh with a coin glint"),
       (466, 466, "cut", "hard cut to shot 7 (hall window, the telescope)")]
DUR = G1 - G0


def framediff(pngs, skip=()):
    prev, d = None, []
    for i, p in enumerate(pngs):
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None and i not in skip:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[g]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        gg = FIRST + g
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "  handle" if (gg < G0 or gg >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[H_IN: H_IN + (G1 - G0) - 1]        # pairs (g-1, g) for g G0+1..G1-1: inside the shot only
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; in-shot pairs only (no handles)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = [os.path.join(HERE, "work", "draft", "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
    assert all(os.path.exists(p) for p in src), "draft incomplete"
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src))
    json.dump(nb, open(os.path.join(HERE, "work", "draft_framediff.json"), "w"), indent=1)
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(FIRST, LAST + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [h for r in rows for h in r["heads"].values()]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

meta = {"take": TAKE, "film": 19, "shots": SHOTS, "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(SHOTS[0]): [G0, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": TRANS_IN, "transition_out": TRANS_OUT,
        "set": SET, "cast": CAST, "camera": CAMERA, "events": EVENTS, "dof": "none", "text": "none", "caption_shade": "none",
        "light": "DAY", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []
for a, b, kind, label in AMB:
    ev.append(dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, [G0]))],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
