#!/usr/bin/env python3
"""deliver.py -- take s14 (shots 14-15): raw/s1 (corridor g 1330..1541) -> frames/g_%04d.png,
meta.json, cues.json, contact.jpg, compare.jpg, work/qa.txt (heads, pops, magenta / black, hue rows) and take.mkv.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as HR

TAKE, SHOTS = "s14", [14, 15]
FIRST, LAST = 1330, 1541
G0, G1 = 1336, 1536
SHOT_RANGES = {"14": [1336, 1433], "15": [1434, 1535]}
CUTS = [(1381, "C1 -> C2 (close: the sweat)"), (1434, "shot 14 -> 15: C3 wide, the plumber walks in"),
        (1465, "C3 -> C4 (insert: the key turns in the lock)"), (1495, "C4 -> C5 (two-shot: door open, the greeting)")]
SETUP = lambda g: 1
SETUP_NAMES = {1: "corridor (louvre exit_door, CORRIDOR_MORNING)"}
PAIRS = [(1400, 5, "sweat close-up beside ref a t0005 (interior close)"), (1520, 13, "two-shot beside ref a t0013 (two figures, interior)")]

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
    "s14_tugs_locked_door": [1338, 1369], "s14_door_rattles": [1340, 1370], "s14_sweat_close": [1381, 1433], "s14_weak_tug": [1396, 1403],
    "s14_gulp": [1410, 1417], "s14_eyes_flick_to_steps": 1422, "s15_plumber_walks_in": [1410, 1457], "s15_vincenzo_backs_off_grin": [1440, 1456],
    "s15_key_in_lock": 1458, "s15_key_turns": [1463, 1475], "s15_door_swings_open": [1484, 1520], "s15_plumber_greets_wave_smile": [1495, 1541]}
meta = {"take": TAKE, "film": 7, "shots": SHOTS, "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1, "handle_in": G0 - FIRST,
        "handle_out": LAST + 1 - G1, "transition_in": "cut", "transition_out": "cut",
        "transition_note": "plan lists no dissolve between shots 13/14 and 15/16 (all louvre); 6-frame handles rendered in 3D on both ends",
        "shot_ranges": SHOT_RANGES, "cuts_inside": [{"at": g, "what": w} for g, w in CUTS],
        "setups": {"1": {"g": [FIRST, LAST], "set": SETUP_NAMES[1]}},
        "events": events,
        "set": "v3/set3d7/louvre.py exit_door + s01's dress_corridor() (imported from ../s01/shot.py, read-only), the fanlight shaft sheet hidden, the corridor's two framed notices (news[2] / news[3] theft headlines) re-textured at runtime with the neutral choc / opera posters, set_door keyed every frame (0..0.9 deg rattle on the tugs, 0 -> 92 deg g 1484-1520), set_flames keyed every frame; custom cameras 20-28 mm.", "_x": ": wall_eye area, set_mona True + set_mona_lift 0 -> 0.32 keyed per frame (the real 3D painting "
               "comes off its four hooks; his hands are pinned to the frame's side edges), the two velvet-rope spans in front of her removed "
               "at runtime (Monday, rope unhooked: it crossed his face in the low angles), a dust sheet + bucket added. Staircase: "
               "set_frame_on_stairs False (B1, he carries it) -> True (B2-B3, the empty frame and glass box on the steps), bucket / rag / "
               "broom added. set_flames keyed every frame. Custom cameras 22-26 mm.",
        "cast": "v3/cast7 vincenzo_smock (vincenzo_sweat with the right hand pinned on the lock, then vincenzo_nervous_smile; bulge 1, sweat 0.55 -> 1, pale) and plumber (walk cycle facing -1, plumber_open_door with the key tip pinned in the lock turning 180 -> 90 deg, plumber_greet with a closed smile); sprites 320 px/D, 512 in C2 / C4", "_y": " with world-pinned hands (stretch to 2.0, on his toes); cycle walk "
                "facing +1 down the stairs with prop mona_framed (scale 1.85) at his side (wide canvas); crouch with prop mona_panel (scale "
                "2.0 = the set canvas size); bulge 0 -> 1 at g 1300-1309",
        "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "mouths": "no quoted line in shots 14-15 (the plumber greets with a closed smile + wave): static expression mouths only",
        "denoiser": "OpenImageDenoise, prefilter FAST", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mean("wall"), "s_per_frame_cpu_mean": mean("cpu"),
        "s_per_frame_by_setup": {SETUP_NAMES[k].split(" ")[0]: {"wall": mean("wall", k), "cpu": mean("cpu", k)} for k in (1,)},
        "frame_source": src}
meta.pop("_x", None); meta.pop("_y", None)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, LAST + 1, "service corridor: stone echo, gas jet hiss, muffled courtyard birds behind the door", "ambience")
for t in (1340, 1352, 1364):
    add(t - 2, t + 6, "he yanks the locked door: heavy rattle of the bolt in the frame", "prop", peak_frame=t)
add(1381, 1381, "cut close: a nervous heartbeat under the sound", "accent")
add(1396, 1404, "a weak last rattle", "prop", peak_frame=1398)
add(1410, 1417, "audible gulp", "gesture", peak_frame=1412)
for g in range(1414, 1458, 12):
    add(g, g + 1, "the plumber's footsteps approaching (and a cheerful hummed tune)", "foley", peak_frame=g)
add(1458, 1460, "key slides into the lock", "prop", peak_frame=1458)
add(1463, 1476, "the key turns: two-stage clack of the old lock", "prop", peak_frame=1474)
add(1484, 1520, "the oak door creaks open; daylight whoosh, courtyard birds and city murmur swell in", "prop", peak_frame=1488)
add(1495, LAST + 1, "the plumber's friendly greeting (a warm 'hm-hm!' hum, no words) and a tiny nervous laugh-breath from vincenzo", "gesture", peak_frame=1497)
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
    sh = "14" if g < 1434 else "15"
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
for sid in (1,):
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
    HR.row("%s shot 14 (g 1330-1433)" % TAKE, fs[:1434 - FIRST])
    HR.row("%s shot 15 (g 1434-1541)" % TAKE, fs[1434 - FIRST:])
    HR.row("%s all" % TAKE, fs)
    for _, t, _n in PAIRS:
        HR.row("ref a t%04d" % t, [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % t)])
print(buf.getvalue()); open(os.path.join(HERE, "work", "qa.txt"), "a").write(buf.getvalue())

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
print("delivered %d frames g %d..%d + take.mkv" % (N, FIRST, LAST))
