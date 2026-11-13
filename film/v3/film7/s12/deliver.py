#!/usr/bin/env python3
"""deliver.py -- take s12 (shots 12-13): raw/s1 (gallery g 1108..1214) + raw/s2 (staircase g 1215..1341) -> frames/g_%04d.png,
meta.json, cues.json, contact.jpg, compare.jpg, work/qa.txt (heads, pops, magenta / black, hue rows) and take.mkv.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as HR

TAKE, SHOTS = "s12", [12, 13]
FIRST, LAST = 1108, 1341
G0, G1 = 1114, 1336
SHOT_RANGES = {"12": [1114, 1214], "13": [1215, 1335]}
CUTS = [(1160, "A1 -> A2 (gallery, low from the left)"), (1195, "A2 -> A3 (gallery, close low on the lift)"),
        (1215, "shot 12 -> 13: gallery -> service staircase"), (1256, "B1 -> B2 (crouched beside the empty frame)"),
        (1290, "B2 -> B3 (front medium: the panel goes under the smock)")]
SETUP = lambda g: 1 if g < 1215 else 2
SETUP_NAMES = {1: "gallery (louvre wall_eye area, GALLERY_DAY)", 2: "staircase (louvre staircase, STAIR_MORNING)"}
PAIRS = [(1205, 49, "gallery lift beside ref a t0049 (warm red interior, close)"), (1262, 85, "stair beside ref a t0085 (stone walls)")]

OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
rows, src = [], {}
for g in range(FIRST, LAST + 1):
    sid = SETUP(g)
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[str(g)] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = len(rows)
mean = lambda k, sel=None: round(float(np.mean([r[k] for r in rows if sel is None or r["shot"] == sel])), 2)

events = {
    "s12_walks_in_along_the_wall": [1108, 1147], "s12_stops_looks_up_at_her": [1148, 1161], "s12_glances_left_right": [1162, 1177],
    "s12_reaches_up_hands_on_frame": [1178, 1190], "s12_lift_off_hooks": [1197, 1211], "s12_hold_hooks_free": [1211, 1214],
    "s13_hurries_down_with_frame": [1215, 1255], "s13_frame_left_on_steps_panel_out": [1256, 1268], "s13_glance_up_stairs": [1276, 1289],
    "s13_stands_panel_to_belly": [1290, 1299], "s13_panel_under_smock_bulge": [1300, 1309], "s13_smirk_hands_press_bulge": [1312, 1341]}
meta = {"take": TAKE, "film": 7, "shots": SHOTS, "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1, "handle_in": G0 - FIRST,
        "handle_out": LAST + 1 - G1, "transition_in": "cut", "transition_out": "cut",
        "transition_note": "plan lists no dissolve between shots 11/12 and 13/14 (all louvre); 6-frame handles rendered in 3D on both ends",
        "shot_ranges": SHOT_RANGES, "cuts_inside": [{"at": g, "what": w} for g, w in CUTS],
        "setups": {"1": {"g": [FIRST, 1214], "set": SETUP_NAMES[1]}, "2": {"g": [1215, LAST], "set": SETUP_NAMES[2]}},
        "events": events,
        "set": "v3/set3d7/louvre.py. Gallery: wall_eye area, set_mona True + set_mona_lift 0 -> 0.32 keyed per frame (the real 3D painting "
               "comes off its four hooks; his hands are pinned to the frame's side edges), the two velvet-rope spans in front of her removed "
               "at runtime (Monday, rope unhooked: it crossed his face in the low angles), a dust sheet + bucket added. Staircase: "
               "set_frame_on_stairs False (B1, he carries it) -> True (B2-B3, the empty frame and glass box on the steps), bucket / rag / "
               "broom added. set_flames keyed every frame. Custom cameras 22-26 mm.",
        "cast": "v3/cast7 vincenzo_smock: walk cycle facing -1; reach with world-pinned hands (stretch to 2.0, on his toes); cycle walk "
                "facing +1 down the stairs with prop mona_framed (scale 1.85) at his side (wide canvas); crouch with prop mona_panel (scale "
                "2.0 = the set canvas size); bulge 0 -> 1 at g 1300-1309",
        "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "mouths": "no quoted line in shots 12-13: static expression mouths only",
        "denoiser": "OpenImageDenoise, prefilter FAST", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mean("wall"), "s_per_frame_cpu_mean": mean("cpu"),
        "s_per_frame_by_setup": {SETUP_NAMES[k].split(" ")[0]: {"wall": mean("wall", k), "cpu": mean("cpu", k)} for k in (1, 2)},
        "frame_source": src}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, 1215, "the Salon Carre on a closed Monday: big empty room tone, a far door, a clock ticking, his soft footsteps echoing", "ambience")
for g in range(1112, 1148, 14):
    add(g, g + 1, "soft hobnail footstep on parquet, smock rustle", "foley", peak_frame=g)
add(1162, 1178, "eyes dart left / right: two tiny tick accents", "accent", peak_frame=1162)
add(1178, 1191, "hands slide up onto the gilt frame (wood creak)", "foley", peak_frame=1188)
add(1197, 1211, "the frame lifts off the four iron hooks: metallic scrape + clink, a held breath", "prop", peak_frame=1199)
add(1215, 1215, "hard cut to the service staircase: the sound narrows to stone", "cut")
add(1215, LAST + 1, "service staircase: stone echo, gas jet hiss, morning birds through the landing window", "ambience")
for g in range(1218, 1256, 10):
    add(g, g + 1, "quick footstep down a stone step, the frame bumping", "foley", peak_frame=g)
add(1256, 1268, "the panel slides out of the frame: wood on wood, the empty frame clatters onto the steps", "prop", peak_frame=1258)
add(1276, 1289, "he freezes and glances up the stairs: tense string hold", "accent", peak_frame=1276)
add(1300, 1310, "the panel slides under the smock: cloth rustle, a soft thump against his belly", "prop", peak_frame=1302)
add(1312, LAST + 1, "a sly smirk: cheeky pizzicato", "accent", peak_frame=1313)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact: 16 frames, cyan line y 880
gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    sh = "12" if g < 1215 else "13"
    dr.text((x + 4, y + 3), "g %d %.2fs shot %s%s" % (g, g / 30.0, sh, " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm); x = 0
for g, tref, note in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d" % (TAKE, g), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d" % tref, fill=(255, 220, 160)); x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

# QA numbers
q = open(os.path.join(HERE, "work", "qa.txt"), "w")
def P(*a):
    print(*a); print(*a, file=q)
for sid in (1, 2):
    rr = [r for r in rows if SETUP(r["g"]) == sid]
    for nm in sorted({n for r in rr for n in r["heads"]}):
        hs = [(r["g"], r["heads"][nm], r.get("setup", "")) for r in rr if nm in r["heads"]]
        for su in sorted({s for _, _, s in hs}):
            hh = [(g, x) for g, x, s in hs if s == su and -50 < x["x"] < 770 and -50 < x["y"] < 1330]
            if not hh:
                continue
            ws = [x["w"] for g, x in hh]; ys = [x["y"] for g, x in hh]; xs = [x["x"] for g, x in hh]
            low = [g for g, x in hh if x["y"] + x["w"] / 2 > 880]
            P("%s %-4s %-4s head w %4.0f..%4.0f  x %4.0f..%4.0f  y %4.0f..%4.0f (%.2f..%.2f H)  bottom > 880: %s" % (
                SETUP_NAMES[sid].split(" ")[0], su, nm, min(ws), max(ws), min(xs), max(xs), min(ys), max(ys), min(ys) / 1280, max(ys) / 1280,
                (low[0], low[-1], len(low)) if low else "none"))
P("render wall %.2f s cpu %.2f s per frame; retried %s" % (mean("wall"), mean("cpu"), [r["g"] for r in rows if r.get("retried")]))
prev, d = None, []
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = [(FIRST + i, FIRST + i + 1, round(v, 1)) for i, v in enumerate(d)
        if v > 1.8 * (d[i - 1] if i else v) and v > 1.8 * (d[i + 1] if i + 1 < len(d) else v) and v > 1.0]
P("pops:", pops, " expected cuts:", [g for g, _ in CUTS])
P("near-still transitions (< 0.35):", [FIRST + i for i, v in enumerate(d) if v < 0.35])
P("frame change median %.2f max %.2f" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
P("magenta / black frames:", bad)
q.close()
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    HR.row("%s gallery (g %d-1214)" % (TAKE, FIRST), fs[:1215 - FIRST])
    HR.row("%s staircase (g 1215-%d)" % (TAKE, LAST), fs[1215 - FIRST:])
    HR.row("%s all" % TAKE, fs)
    for _, t, _n in PAIRS:
        HR.row("ref a t%04d" % t, [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % t)])
print(buf.getvalue()); open(os.path.join(HERE, "work", "qa.txt"), "a").write(buf.getvalue())

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
print("delivered %d frames g %d..%d + take.mkv" % (N, FIRST, LAST))
