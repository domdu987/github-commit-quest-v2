#!/usr/bin/env python3
"""deliver.py (take s12): raw/s12 + raw/s13 -> frames/, meta.json, cues.json, contact.jpg, take.mkv.   python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE, FILM = "s12", 13
SHOTS = {12: (720, 842), 13: (843, 917)}
G0, G1 = 726, 912
FIRST, LAST = 720, 917
CUTS = [780, 843]
CUES = [  # (g0, g1, kind, label, peak)
    (FIRST, 843, "ambience", "Chicago street 1861 seen from high on the facade: wind past the cornice, a distant bustle of carts, hooves and voices far below, a lake gull", None),
    (726, 843, "foley", "the rich man leans out of the window above the street: cloth and wood creak, his mocking voice-over (narration) carries the quote", 750),
    (780, 781, "cut", "framing B (plan 26.0 s): push in on him, then the crane descends", None),
    (806, 843, "accent", "crane down the brick facade: a soft airy whoosh falling away, street sounds rising as the camera nears the ground", 825),
    (843, 844, "cut", "cut to the nickname crowd shot: the street murmur turns into a crowd", None),
    (843, LAST + 1, "ambience", "crowd of townsfolk laughing and jeering in the street, boots on planks, a horse, a cart far off", None),
    (843, 895, "foley", "Pullman's boots on the plank walk and the iron jack clanking on his shoulder as he strolls past, townsfolk giggling and pointing", 860),
    (893, 917, "accent", "the nickname lands (29.73 s, g 895): the whole crowd bursts into one big roaring laugh and cheers, feet stamping on the planks", 897),
]
os.chdir(HERE)
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows, src = [], {}
for g in range(FIRST, LAST + 1):
    sid = 12 if g <= 842 else 13
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
N = LAST - FIRST + 1
meta = {"take": TAKE, "film": FILM, "shots": sorted(SHOTS), "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": G0 - FIRST, "handle_out": LAST - G1 + 1,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "transitions": [{"at": G0, "type": "cut"}, {"at": 780, "type": "cut", "note": "framing B inside shot 12 (plan: 2nd framing at 26.0 s)"}, {"at": 843, "type": "cut", "note": "plan cut shot 12 -> 13 at 28.09 s, same location and light, new set-up"}, {"at": G1, "type": "cut"}],
        "shot_ranges": {str(k): list(v) for k, v in SHOTS.items()},
        "set": "v3/set3d13/chicago.py street (preset hotel_front build, state lift0, DAY); shot 12 custom cameras (in the air before the facade / crane down to the street, 22 mm), shot 13 crowd_street camera numbers (24 mm) + slow drift; runtime: the two burlap sacks of street_props removed in shot 13",
        "cast": "v3/cast13: shot 12 rich_mock_point at stand point top_window (talk_mouth through the whole shot, all inside Q1), pullman_look_up_confident at (-1.5,-17); shot 13 pullman walk cycle with the iron_jack on the shoulder + ~32 crowd cards from cast13 (town_laugh_point a/b/c, mirrored toward the lane, worker_cheer_a, gentleman/lady/town stand) bouncing on every frame, a bigger shared jump at g 895 (the nickname)",
        "lipsync": {"window_g": [720, 850], "note": "rich talk_mouth for every frame of shot 12 (Q1 runs to 28.09 s = g 843 +-0.15 s); nobody speaks in shot 13"},
        "events": {"framing_B": 780, "crane_down": [806, 842], "nickname_lands": 895},
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30, "dof": "none",
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
json.dump(meta, open("meta.json", "w"), indent=1)
ev = []
for (a, b, kind, label, pk) in CUES:
    e = dict(time=round(a / 30.0, 3), duration=round((b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label)
    if pk is not None: e["peak_frame"] = pk
    ev.append(e)
json.dump({"take": TAKE, "fps": 30, "note": "time = film seconds (g / 30); narration film13/audio/narration.wav at +0.10 s", "cues": ev}, open("cues.json", "w"), indent=1, ensure_ascii=False)
# contact sheet: one tile per 12 frames at 240x427
sel = list(range(FIRST, LAST + 1, 12)) + [LAST]
tw, th = 240, 427; cols = 6; rws = (len(sel) + cols - 1) // cols
sh = Image.new("RGB", (cols * tw, rws * th), (20, 20, 24)); d = ImageDraw.Draw(sh)
for i, g in enumerate(sel):
    im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((tw, th), Image.LANCZOS)
    x, y = (i % cols) * tw, (i // cols) * th
    sh.paste(im, (x, y)); d.line([(x, y + int(880 / 3)), (x + tw, y + int(880 / 3))], fill=(0, 255, 255), width=1); d.text((x + 4, y + 4), "g %d" % g, fill=(255, 255, 0))
sh.save("contact.jpg", quality=88)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", "take.mkv"], check=True)
sz = os.path.getsize("take.mkv"); print("take.mkv %.1f MB, %d frames" % (sz / 1e6, N))
if sz > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part && rm take.mkv", shell=True, check=True); print("split into parts")
