#!/usr/bin/env python3
"""deliver.py (take s10): raw/s10 + raw/s11 -> frames/, meta.json, cues.json, contact.jpg, take.mkv.   python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE, FILM = "s10", 13
SHOTS = {10: (585, 649), 11: (650, 731)}
G0, G1 = 591, 726
FIRST, LAST = 585, 731
CUTS = [650]
CUES = [  # (g0, g1, kind, label, peak)
    (FIRST, LAST + 1, "ambience", "top-floor hotel suite, day: a soft room tone, muffled street murmur and a distant cart far below through the open window, a faint chandelier tinkle", None),
    (585, 600, "prop", "porcelain cup and saucer: a small calm clink as the rich man holds his tea", 590),
    (606, 614, "accent", "he hears the plan: a short surprised intake, a pizzicato 'huh?'", 611),
    (612, 650, "foley", "big belly-laugh (his own voice, hearty, wheezing): the cup rattles on its saucer in time with the shaking belly", 618),
    (650, 654, "cut", "cut to shot 11: same room, the laugh dies down into the mocking line (narration voice-over carries the quote)", None),
    (654, 731, "foley", "fabric / waistcoat creak and a small pompous cough as he points down at the street", 690),
]
os.chdir(HERE)
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows, src = [], {}
for g in range(FIRST, LAST + 1):
    sid = 10 if g <= 649 else 11
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
N = LAST - FIRST + 1
meta = {"take": TAKE, "film": FILM, "shots": sorted(SHOTS), "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": G0 - FIRST, "handle_out": LAST - G1 + 1,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "transitions": [{"at": G0, "type": "cut"}, {"at": 650, "type": "cut", "note": "plan cut shot 10 -> 11 at 21.68 s, same location, new set-up"}, {"at": G1, "type": "cut"}],
        "shot_ranges": {str(k): list(v) for k, v in SHOTS.items()},
        "set": "v3/set3d13/chicago.py suite (preset suite_room build, state tea0, SUITE light, DAY-blue sky); custom cameras in the room, 22 mm, no DOF",
        "cast": "v3/cast13 rich: shot 10 rich_look_window_smug (cup + saucer) -> rich_laugh_big (cup kept in the left hand, belly squash 4-frame loop); shot 11 rich_mock_point with talk_mouth lip-sync inside Q1 (g %d..%d)" % (650, 850),
        "lipsync": {"window_g": [650 - 3, 850], "note": "talk_mouth only for g >= %d (Q1 21.68 s - 0.15 s); flat before; the laugh pose keeps its own held laugh mouth" % 649},
        "events": {"hears": [606, 614], "laugh_burst": 612, "cut_to_mock": 650, "lip_sync_start": 649},
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
