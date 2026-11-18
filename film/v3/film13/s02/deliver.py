#!/usr/bin/env python3
"""deliver.py (take s02 = plan shots 2 + 3): raw/s2 (g 57..107) + raw/s3 (g 108..164) -> frames, meta.json, cues.json, contact.jpg, phone_sheet.jpg, take.mkv (g 57..164)."""
import os, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE, FILM, SHOTS = "s02", 13, [2, 3]
G0, G1, H_IN, H_OUT = 63, 158, 6, 6          # shots 2+3 = g 63..158 (plan 2.10-5.30 s); handles g 57..62 and 159..164
FIRST, LAST = G0 - H_IN, G1 + H_OUT
SEGS = [(2, 57, 107), (3, 108, 164)]         # (id, g_from, g_to)
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = []
for sid, a, b in SEGS:
    for g in range(a, b + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
        rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
meta = {"take": TAKE, "film": FILM, "shots": SHOTS, "first_g": FIRST, "n_frames": LAST - FIRST + 1, "g0": G0, "g1": G1 + 1, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": "cut", "frames": 0, "note": "from shot 1 (hotel_front); in-handle g 57..62 is the suite_two set-up continued backwards"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 4 (street_wide RAIN) at g 159; out-handle g 159..164 = tea_close push continues"},
        "transitions": [{"at": 63, "type": "in", "handle": [57, 62]}, {"at": 108, "type": "cut", "note": "plan cut shot 2 -> 3 at 3.60 s inside the take (same suite, new set-up)"}, {"at": 159, "type": "out", "handle": [159, 164]}],
        "shot_ranges": {"2": [63, 107], "3": [108, 158]},
        "setups": {"2": {"g": [57, 107], "set": "suite suite_two SUITE: lady in the teal armchair + gentleman sip tea at the window; camera 8.0 -> 7.0 D back, 22 mm, slow push"},
                   "3": {"g": [108, 164], "set": "suite tea_close SUITE: cup + saucer, tea ripple 0 keyed every frame; 40 mm slow push + pan; the street/rooftops outside are lowered by drift(g) per frame"}},
        "events": {"lady_sips": [78, 122], "gentleman_sips": [102, 146], "street_drift": [57, 164]},
        "set": "v3/set3d13/chicago.py suite (drift: every object outside the room lowered by (h-0.65)*3.6*2.0 D, h 0.65 -> 0.80 over g 63..159, continuing shot 1)",
        "dof": "none", "denoiser": "OpenImageDenoise (set default)", "light": "SUITE",
        "cast": "v3/cast13: lady_sip_tea (lady13_seat), gentleman13 (stand + teacup_saucer, sips); no mouth lip-sync",
        "samples": 20, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(63, 158, "hush of a rich room: a quiet clock tick, a distant muffled street far below, a calm warm string pad (hook flash-forward, nothing is wrong)", "ambience")
add(78, 122, "the lady lifts her cup: a tiny china clink as it meets the saucer, a soft sip", "foley", peak_frame=100)
add(102, 146, "the gentleman sips: soft sip, cup settles on its saucer", "foley", peak_frame=124)
add(63, 158, "very faint wood creak and brick groan from the rising building under the calm (barely audible, builds slightly)", "foley", peak_frame=140)
add(108, 108, "cut to the tea close-up (shot 3)", "cut")
add(108, 158, "the tea lies perfectly still: a single high crystal tone, a stretched glassy silence", "accent", peak_frame=130)
add(159, 159, "cut to shot 4: rain (pivot, 1861 Chicago)", "cut")
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
