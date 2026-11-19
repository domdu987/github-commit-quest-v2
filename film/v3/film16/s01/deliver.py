#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg,
framediff.json, then qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.   python3 deliver.py [draft]"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---- CONFIG (per take) ------------------------------------------------------------------------------------------------------------
TAKE, SHOTS = "s01", [1]
G0, G1, H_IN, H_OUT = 0, 69, 0, 6
TR_IN = {"type": "cut", "frames": 0, "note": "film opens here"}
TR_OUT = {"type": "cut", "frames": 0}
CUTS = [69]
LIGHT, PRESET = "DAY", "line_close"
SET = "set3d16 telegraph.py LINE line_close DAY; runtime: clear dense glass material, per-frame slack wire, bottle copy switched to the set glass at contact (g 47), wrap ring + spans at g 65"
CAST = "cast16 morse16 (mirror) morse_cap_peg / morse_drape_wire; stands one rung lower along the ladder (mark shift -0.25,-0.22,-0.6); happy from the pose swap g 52"
CAMERA = "custom 22 mm, higher (z 5.3, pitch 25 deg) so ground and poles fill the first second; drift push 6 %/s + slide 75 px/s + arc 24 deg/s + snap x2.4 with pan on the word at g 22..35"
EVENTS = {}
CUELIST = [(0, 75, "ambience", "Maryland countryside, sunny day 1844: light breeze in the grass, larks; faint creak of the leaning ladder"), (22, 35, "accent", "snap push on 'คอขวดเบียร์': airy whoosh"), (24, 31, "accent", "sun glint on the green glass: bright tiny ting"), (47, 50, "prop", "GLASS CLINK as the inverted bottle seats on the pole top (the hook's sound)"), (55, 64, "foley", "wire flicked up over the glass: whippy swish, light tick as it settles"), (65, 69, "accent", "Morse's small pleased smile: soft pluck")]
# -----------------------------------------------------------------------------------------------------------------------------------
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
N = G_LAST - G_FIRST + 1


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d                                         # d[j] = pair into frame j+1


def numbers(d):
    ins = d[G0 - G_FIRST: G1 - G_FIRST - 1]          # pairs into frames G0+1 .. G1-1 (in-shot, no handles)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g %d..%d (in-shot, no handles)" % (G0 + 1, G1 - 1),
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(idx):
        g = G_FIRST + k
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


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
for g in range(G_FIRST, G_LAST + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(G_FIRST, G_LAST + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [r["heads"]["mor"] for r in rows if r.get("heads", {}).get("mor")]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
meta = {"take": TAKE, "film": 16, "shots": SHOTS, "g0": G0, "g1": G1, "first_g": G_FIRST, "n_frames": N,
        "shot_ranges": {str(SHOTS[0]): [G0, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": TR_IN, "transition_out": TR_OUT, "set": SET, "cast": CAST, "camera": CAMERA, "events": EVENTS,
        "dof": "none", "text": "none", "light": LIGHT, "preset": PRESET, "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json"}
if heads:
    meta["head_px"] = [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))]
    meta["head_centre_y"] = [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))]
    meta["head_bottom_max_y"] = round(max(h["bottom"] for h in heads))
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for (a, b, kind, label) in CUELIST:
    ev.append(dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(G_FIRST), "--cuts", ",".join(map(str, CUTS))], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
