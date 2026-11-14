#!/usr/bin/env python3
"""deliver.py -- raw/s15 (plain macro, g 1147..1283) + raw/s16 (rice macro, g 1284..1418) -> frames/g_%04d.png, meta.json, cues.json,
contact.jpg, take.mkv (libx264rgb crf 6), and QA numbers to work/qa.txt (pops, near-still runs, hue rows, s/frame).
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(V3, "tools"))

TAKE, SHOTS = "s15", [15, 16]
G0, G1, H, G_CUT = 1153, 1413, 6, 1284
FIRST, LAST = G0 - H, G1 + H - 1
SRC = lambda g: 15 if g < G_CUT else 16
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
        "transition_in": {"type": "cut", "frames": 0, "note": "from shot 14 (cannon_line, the gun fires); in-handle g 1147..1152 = the calm macro before"},
        "transition_out": {"type": "cut", "frames": 0, "note": "to shot 17 (site_wide DAWN); out-handle g 1413..1418 = the web settling, push continues"},
        "transitions": [{"at": G0, "type": "cut"}, {"at": G_CUT, "type": "cut", "note": "plan cut shot 15 (plain) -> shot 16 (rice) at 42.80 s, inside the take; same camera angle on purpose (1:1 comparison)"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"15": [G0, G_CUT - 1], "16": [G_CUT, G1 - 1]},
        "setups": {"15": {"g": [FIRST, G_CUT - 1], "set": "wall.py mortar_macro (plain), BATTLE; custom oblique along the joint from the front-left (preset macro_plain moved), 22 mm, push ~2.1 D, jolt on the hit"},
                   "16": {"g": [G_CUT, LAST], "set": "wall.py mortar_macro_rice, BATTLE; same oblique, closer start, push ~2.7 D, jolt on the hit; runtime radial reveal of the web material (the web spreads over the face g 1290..1337)"}},
        "events": {"plain_ball_flies_in": [1180, 1207], "plain_hit": 1207, "plain_crack_races": [1207, 1262], "shards_dust": [1207, 1230],
                   "cut_to_rice": G_CUT, "web_spreads": [1290, 1337], "rice_ball_flies_in": [1352, 1380], "rice_hit": 1380,
                   "web_flexes_and_holds": [1380, 1405], "ball_bounces_off": [1385, 1413]},
        "set": "v3/set3d9/wall.py macro area: set_macro(t) + set_flames keyed every frame; shot 16 adds a keyed radial transparent mix + glow scale on the web material (shot.py web_reveal_nodes / key_web)",
        "dof": "none", "denoiser": "OpenImageDenoise, prefilter FAST", "light": "BATTLE",
        "narration": "film9/audio/narration.wav at +0.10 s; captions film9/script/captions.json", "cast": "none on screen",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mw(None), "s_per_frame_cpu_mean": mc(None),
        "s_per_frame_by_setup": {"15": {"wall": mw(15), "cpu": mc(15)}, "16": {"wall": mw(16), "cpu": mc(16)}}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, G_CUT, "inside the plain mortar joint: muffled distant battle rumble, low tense drone, faint crackle of the fire light", "ambience")
add(1180, 1207, "a heavy cannonball whoosh growing from behind the listener's left shoulder", "foley", peak_frame=1204)
add(1207, 1215, "HIT: deep stony thud + bright flash crack", "impact", peak_frame=1207)
add(1207, 1262, "brittle crack racing: a fast dry splitting / ice-crackle sweeping left and right, shards skittering", "foley", peak_frame=1215)
add(1225, 1270, "the ball drops away, grit and dust patter", "foley", peak_frame=1240)
add(G_CUT, G_CUT, "cut to the rice mortar: same place, the drone turns warm", "cut")
add(G_CUT, LAST + 1, "inside the rice mortar joint: warm low drone, soft glowing hum", "ambience")
add(1290, 1337, "the golden web spreads and wraps the crystals: a rising shimmering, sticky-stretchy sparkle", "accent", peak_frame=1320)
add(1352, 1380, "cannonball whoosh again", "foley", peak_frame=1377)
add(1380, 1386, "HIT: a dull rubbery 'thoomp' (no crack)", "impact", peak_frame=1380)
add(1380, 1405, "the web stretches and springs back: elastic boing-wobble, a glow swell", "accent", peak_frame=1384)
add(1386, 1413, "the ball bounces off and away, a light thud far off", "foley", peak_frame=1395)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film9/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, SRC(g), " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
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
q.close()
sys.stdout = open(os.path.join(HERE, "work", "qa.txt"), "a")
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1, 2)]
HR.row("shot 15 plain", fr(FIRST, G_CUT - 1)); HR.row("shot 16 rice", fr(G_CUT, LAST)); HR.row("take all", fr(FIRST, LAST))
sys.stdout.close(); sys.stdout = sys.__stdout__
print(open(os.path.join(HERE, "work", "qa.txt")).read())
print("delivered", N, "frames", FIRST, "..", LAST)
