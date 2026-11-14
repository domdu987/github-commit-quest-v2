#!/usr/bin/env python3
"""deliver.py -- raw/s1 (wide cannon line, g 1035..1096) + raw/s2 (medium gunner, g 1097..1158) -> frames/g_%04d.png, meta.json, cues.json,
contact.jpg, take.mkv (libx264rgb crf 6), and QA numbers to work/qa.txt (pops, near-still runs, hue rows, s/frame).
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(V3, "tools"))

TAKE, SHOTS = "s14", [14]
G0, G1, H, G_CUT = 1041, 1153, 6, 1097
FIRST, LAST = G0 - H, G1 + H - 1
SRC = lambda g: 1 if g < G_CUT else 2
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(HERE, "work"), exist_ok=True)

rows = []
for g in range(FIRST, LAST + 1):
    raw = os.path.join(HERE, "raw", "s%d" % SRC(g))
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = LAST - FIRST + 1
mw = lambda s: round(float(np.mean([r["wall"] for r in rows if s is None or r["shot"] == s])), 2)
mc = lambda s: round(float(np.mean([r["cpu"] for r in rows if s is None or r["shot"] == s])), 2)

meta = {"take": TAKE, "film": 9, "shots": SHOTS, "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N, "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0, "note": "from shot 13 (wall_top RAIN); in-handle g 1035..1040 rendered in 3D (track continues)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "to shot 15 (mortar_macro): the ball fired here hits the plain mortar; out-handle g 1153..1158 = ball in flight, smoke, shake"},
        "transitions": [{"at": G0, "type": "cut"}, {"at": G_CUT, "type": "cut", "note": "set-up cut inside shot 14 (wide -> medium, same location / light) at 36.57 s, between 'ลากปืนใหญ่มา' and 'เรียงหน้า'"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"14": [G0, G1 - 1]},
        "setups": {"1": {"g": [FIRST, G_CUT - 1], "set": "wall.py cannon_line, BATTLE (army, smoke 1, lin 26 / gen 30 courses); preset camera, slow track right + crane up 1 D, 20 mm"},
                   "2": {"g": [G_CUT, LAST], "set": "same build; custom low medium behind-right of gun 3 (aimed at the general's section), 22 mm, slow push, shake on the shot"}},
        "events": {"gunners_crouch": [1078, 1098], "match_to_touch_hole": [1100, 1112], "fuse_sparks": [1112, 1139], "gunners_duck_cover_ears": [1126, 1137],
                   "gun_3_fires": 1140, "ball_in_flight": [1144, 1158]},
        "set": "v3/set3d9/wall.py: set_flames, set_smoke(1), set_army(True), set_wall_height lin 26 / general 30, set_cauldron_steam(0.4), set_impact('general', 0, t) (t 0.02 at g 1140, +1/60 per frame) keyed every frame; runtime: 9 emissive fuse sparks + a flickering point light at gun 3's touch hole (g 1112..1139)",
        "dof": "none", "denoiser": "OpenImageDenoise, prefilter FAST", "light": "BATTLE",
        "narration": "film9/audio/narration.wav at +0.10 s; captions film9/script/captions.json",
        "cast": "v3/cast9 gunner_a (gun 2, mirrored) + gunner_b (gun 3): gunner_stand -> gunner_light (linstock angle tweened, match_glow 1) -> gunner_ears; no mouths move",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mw(None), "s_per_frame_cpu_mean": mc(None),
        "s_per_frame_by_setup": {"1": {"wall": mw(1), "cpu": mc(1)}, "2": {"wall": mw(2), "cpu": mc(2)}}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, LAST + 1, "battlefield at smoky dusk: distant war drums, crackling fire pots and camp fires, wind, banners flapping, far shouts", "ambience")
add(FIRST, G_CUT, "heavy wooden gun carriages creak, a horn call far off", "foley", peak_frame=1050)
add(1078, 1098, "gunners crouch: leather and cloth rustle", "foley", peak_frame=1090)
add(G_CUT, G_CUT, "cut to the medium on the gunner", "cut")
add(1112, 1139, "the match touches the touch hole: a hissing, spitting fuse", "foley", peak_frame=1114)
add(1126, 1137, "gunners duck and cover their ears: a held breath, tension riser", "accent", peak_frame=1137)
add(1140, 1150, "BOOM: the cannon fires (deep blast, low-end thump), shake", "impact", peak_frame=1140)
add(1144, 1159, "the ball's whoosh flying away toward the wall", "foley", peak_frame=1150)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film9/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  set-up %d%s" % (g, g / 30.0, SRC(g), " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

# QA numbers
import hue_report as HR
q = open(os.path.join(HERE, "work", "qa.txt"), "w")
prev, d = None, []
for g in range(FIRST, LAST + 1):
    a = np.asarray(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None: d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = [(FIRST + i, round(v, 1)) for i, v in enumerate(d) if v > 1.8 * (d[i - 1] if i else v) and v > 1.8 * (d[i + 1] if i + 1 < len(d) else v) and v > 1.0]
still = [FIRST + i for i, v in enumerate(d) if v < 0.35]
run = best = 0
for v in d:
    run = run + 1 if v < 0.35 else 0; best = max(best, run)
print("pops (g -> g+1):", pops, file=q)
print("near-still transitions (< 0.35):", len(still), "longest run", best, file=q)
print("frame change median %.2f max %.2f" % (float(np.median(d)), max(d)), file=q)
print("s/frame wall %.2f cpu %.2f; by setup %s; mkv %.1f MB" % (mw(None), mc(None), meta["s_per_frame_by_setup"], os.path.getsize(mkv) / 1e6), file=q)
import glob
for nm in ("ga", "gb"):
    hs = [(r["g"], r["heads"][nm]) for r in rows if nm in r.get("heads", {}) and -40 < r["heads"][nm]["x"] < 760]
    if hs:
        print("%s head w %.0f..%.0f px, x %.0f..%.0f, y %.0f..%.0f; bottom below 880: %s" % (nm, min(h["w"] for g, h in hs), max(h["w"] for g, h in hs),
              min(h["x"] for g, h in hs), max(h["x"] for g, h in hs), min(h["y"] for g, h in hs), max(h["y"] for g, h in hs),
              [g for g, h in hs if h["y"] + h["w"] / 2 > 880]), file=q)
q.close()
sys.stdout = open(os.path.join(HERE, "work", "qa.txt"), "a")
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1, 2)]
HR.row("set-up 1 wide", fr(FIRST, G_CUT - 1)); HR.row("set-up 2 medium", fr(G_CUT, LAST)); HR.row("take all", fr(FIRST, LAST))
sys.stdout.close(); sys.stdout = sys.__stdout__
print(open(os.path.join(HERE, "work", "qa.txt")).read())
print("delivered", N, "frames", FIRST, "..", LAST)
