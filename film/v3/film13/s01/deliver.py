#!/usr/bin/env python3
"""deliver.py (take s01 = plan shot 1, hook): raw/s1 -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, phone_sheet.jpg, take.mkv (g 0..68)."""
import os, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE, FILM, SHOTS = "s01", 13, [1]
G0, G1, H_IN, H_OUT = 0, 62, 0, 6            # shot 1 = g 0..62 (plan 0.00-2.10 s); out handle g 63..68
FIRST, LAST = G0 - H_IN, G1 + H_OUT
SEGS = [(1, 0, 68)]                          # (id, g_from, g_to)
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = []
for sid, a, b in SEGS:
    for g in range(a, b + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
        rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
meta = {"take": TAKE, "film": FILM, "shots": SHOTS, "first_g": FIRST, "n_frames": LAST - FIRST + 1, "g0": G0, "g1": G1 + 1, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": "cut", "frames": 0, "note": "film opens on this shot"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 2 (suite_two) at g 63; out-handle g 63..68 = the same hotel_front crane continues (h 0.65 -> 0.66)"},
        "shot_ranges": {"1": [G0, G1]},
        "setups": {"1": {"g": [G0, LAST], "set": "street hotel_front DAY, worm's-eye 17 mm, crane up 0.45 -> 1.35 D + tilt, lift keyed 0.55 -> 0.65 (continues in the handle); crib pier + spare jacks left foreground; dust motes trickle from the base"}},
        "events": {"lift": [0, 62], "crane_up": [0, 68]},
        "set": "v3/set3d13/chicago.py hotel_front, DAY (set_lift + dust motes keyed per frame)",
        "dof": "none", "denoiser": "OpenImageDenoise (set default)",
        "light": "DAY", "cast": "v3/cast13: pullman_look_up_confident (centre, idle sway + blinks), worker_stand_a/b/c",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(0, 63, "HOOK: low rumble of a huge weight rising: slow timber creaks and a deep brick-and-iron groan under a calm warm bed (flash-forward, no rain)", "ambience")
add(5, 60, "fine dust and grit trickling down from the base of the hotel: soft sandy hiss, a few pebbles", "foley", peak_frame=30)
add(0, 63, "faint iron ratchet clicks far below (jacks), slow, unhurried", "foley", peak_frame=20)
add(63, 63, "cut to the suite window (shot 2): the groan drops away to a hush", "cut")
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film13/audio/narration.wav at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
def sheet(path, w, h, n, cols, gs):
    S = Image.new("RGB", (cols * w, ((len(gs) + cols - 1) // cols) * (h + 18)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + 18)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + 18))
        dr.line([(x, y + 18 + int(880 * h / 1280)), (x + w, y + 18 + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d %.2fs" % (g, g / 30.0), fill=(255, 255, 255))
    S.save(path, quality=88)
sheet(os.path.join(HERE, "contact.jpg"), 270, 480, 16, 8, [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)])
sheet(os.path.join(HERE, "phone_sheet.jpg"), 180, 320, 0, 8, list(range(FIRST, LAST + 1, 5)))
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                       "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")])
print("take.mkv", os.path.getsize(os.path.join(HERE, "take.mkv")) // 1024, "KB")
