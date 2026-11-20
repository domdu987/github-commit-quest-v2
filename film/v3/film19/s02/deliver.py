#!/usr/bin/env python3
"""deliver.py -- s02 delivery (film 19, shot 2) from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json,
contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot frame-diff, 90x160 grey), then qa_auto.py.  No bpy.
    python3 deliver.py            final delivery
    python3 deliver.py draft      work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---- take config -----------------------------------------------------------------------------------------------------------
TAKE, SHOT = "s02", 2
SHOTS = [2, 3]                                            # s02 absorbs the old shot 3 (s03 is dropped)
T0, T1 = 1.91, 6.37
H_IN, H_OUT = 9, 9
G0, G1 = int(round(T0 * 30)), int(round(T1 * 30))        # shot = g G0..G1-1 (57..190, 134 frames)
FIRST = G0 - H_IN
N = (G1 + H_OUT) - FIRST
TR_IN = dict(type="cut", frames=0, note="hard cut in from s01 (WORKSHOP shop_bench) at g %d; %d handle frames before it rendered in 3D" % (G0, H_IN))
TR_OUT = dict(type="dissolve", frames=13, at=G1, note="dissolve 13 f into s04 (SHIP ship_rocks STORM_DUSK) centred on g %d; handle g %d..%d rendered in 3D" % (G1, G1, G1 + H_OUT - 1))
CUTS = [G0]                                               # planned cuts for qa_auto
SET = "v3/set3d19/h19.py SHIP preset ship_aerial, light NOON (colour-fixed set, merge of film19/main ff204d3); set_sea(g/30) + set_roll(g/30) keyed on every frame; sea grid re-fitted at runtime to a 3x farther / higher virtual camera (1500x2000 vertices; no set module edited); gulls hidden; captain19 and astro19_c ride ship_root (c19.ride_ship) on the quarterdeck, camera rides the deck (c19.on_ship); no caption_shade"
CAMERA = "BIGZOOM, one continuous camera move in the ship rest frame (Catmull-Rom spline through 4 key poses, smootherstep ease in / out + 22 % linear so it never parks), g 57..177: from extreme wide high above and behind the ship (ship small, characters ~6 px) descending and pushing in, passing the spanker sail at ~2 D (parallax), to a MEDIUM on the quarterdeck by 5.9 s (g 177); then a slow push to the end of the handle"
EV = dict(bigzoom=[G0, G1 - 1], arrive_medium=177, astro_scratch=[146, 166], blinks_captain=[70, 128, 171], blinks_astro=[92, 150, 188])
CUES = [
    (0, N, "ambience", "open sea far from land: steady wind over water, a long swell, rigging creak that grows as the camera drops to the deck", {}),
    (G0 - FIRST, 177 - FIRST, "accent", "descending whoosh: the long eased zoom from the sky down to the deck (wind rising, canvas flutter as it passes the sail)", {}),
    (146 - FIRST, 166 - FIRST, "foley", "astro19_c's head-scratch: wig rustle (no voice)", {}),
    (G1 - FIRST, N, "cut", "dissolve into the storm: deck creak, wind darkens", {}),
]
# --------------------------------------------------------------------------------------------------------------------------------


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
    """d[i-1] = diff of frames i-1 -> i (index in the take); in-shot pairs = frame i with G0 < FIRST+i < G1 (g G0+1 .. G1-1)"""
    ins = [d[i - 1] for i in range(1, N) if G0 < FIRST + i < G1]
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; in-shot pairs only (no handle)",
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
for i in range(N):
    g = FIRST + i
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % (FIRST + i)) for i in range(N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
meta = {"take": TAKE, "film": 19, "shots": SHOTS, "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {"2": [G0, G1 - 1], "3": "absorbed (merged into this take)"}, "bigzoom": [G0, G1 - 1], "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TR_IN, "transition_out": TR_OUT,
        "set": SET, "cast": "captain19 (captain_peer_chart: holds a blank sea chart) and astro19_c (squints through the quadrant at the sky, scratches his head g 146-166), no mouth movement", "camera": CAMERA, "events": EV, "dof": "none", "text": "none",
        "caption_shade": "none", "light": "NOON", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for a, b, kind, label, kw in CUES:
    e = dict(time=round((FIRST + a) / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=FIRST + a, end_frame=FIRST + b, kind=kind, label=label)
    e.update(kw)
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, CUTS))],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))
