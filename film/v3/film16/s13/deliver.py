#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg,
framediff.json, then qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.
    python3 deliver.py          final delivery          python3 deliver.py draft     look at the draft in work/draft (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE, SHOT = "s13", 13
G0, G1, H_IN, H_OUT = 831, 892, 9, 9                   # shot = g 831..891; take = 822..900
TRANS_IN = {"type": "dissolve", "frames": 15}
CUTS_OUT = [892]                                       # planned cut g list for qa_auto (the hard cut out to shot 14)
GA = G0 - H_IN
N = G1 + H_OUT - GA
SET_NOTE = "v3/set3d16/telegraph.py LINE preset line_trench, light DAY; per-frame hooks set_trench / set_pipe (plough front 0.50 -> 0.57, pipe 0.035 behind); runtime foreground dressing (grass blades, crate, shovel) at three points of the camera path"
CAST_NOTE = "v3/cast16: mule x2 (cycle pull, harness 1, 0.25 phase offset), cornell (cornell_plough + walk legs), worker16_a / worker16_b (shovel poses + walk legs), morse16 (walk) following; nobody speaks"
CAM_NOTE = "custom 22 mm, 10 D off the furrow on the road side, 3.4 D up, tracking the plough; drift push 7 %/s + slide 30 px/s + arc 3 deg/s; snap x1.2 with a 13 D pan from the mules back to Cornell and the pipe on 'ตะกั่วใต้ดิน' (g 868-881, 13 f, peak 1.6)"
EV = dict(snap=[868, 881], word_ta_kua=870)
CUES = [(0, "ambience", "Maryland countryside beside the railway: wind in the wheat, a distant cow, harness creak", None),
        (GA, "foley", "mule hooves on dirt and the creak of the plough, jingling harness", 840),
        (831, "accent", "dissolve in: the scene settles on the working team", 831),
        (868, "accent", "snap pan from the mules to Cornell and the pipe: airy whoosh", 872),
        (870, "prop", "lead pipe unrolling into the furrow: low metallic rolling clank on 'ตะกั่ว'", 870)]


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


def numbers(d):
    ins = d[H_IN:H_IN + (G1 - G0) - 1]                 # pairs (g-1, g) for g in shot, first shot frame onward
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; in-shot pairs only (no handle)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2), max=round(float(max(ins)), 2),
                target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


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
for g in range(GA, GA + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(GA, GA + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
ins = rows[H_IN:H_IN + G1 - G0]
hd = [h for r in ins for nm, h in r["heads"].items() if nm not in ("mule_a", "mule_b")]
meta = {"take": TAKE, "film": 16, "shots": [SHOT], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N, "shot_ranges": {str(SHOT): [G0, G1 - 1]},
        "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TRANS_IN,
        "transition_out": {"type": "cut", "frames": 0, "at": G1, "note": "out-handle g %d..%d rendered in 3D" % (G1, G1 + H_OUT - 1)},
        "set": SET_NOTE, "cast": CAST_NOTE, "camera": CAM_NOTE, "events": EV, "dof": "none", "text": "none", "light": "DAY", "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30, "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]}, "narration": "film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for g, kind, label, peak in CUES:
    ev.append(dict(time=round(g / 30.0, 3), frame=g, kind=kind, label=label, peak_frame=peak))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GA), "--cuts", ",".join(map(str, CUTS_OUT))], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f" % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
