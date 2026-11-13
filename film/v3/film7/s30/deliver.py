#!/usr/bin/env python3
"""deliver.py -- raw/s1 (side angle, g 2974..3038) + raw/s2 (reverse over the crowd, g 3039..3101) -> frames/, meta.json, cues.json,
contact.jpg, compare.jpg, take.mkv (libx264rgb crf 6, all frames g 2974..3101).   python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
G0, G1, H, G_CUT = 2980, 3096, 6, 3039
FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for g in range(FIRST, LAST + 1):
    sid = 1 if g < G_CUT else 2
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = len(src)
mean = lambda k, s=None: round(float(np.mean([r[k] for r in rows if s is None or r["shot"] == s])), 2)
meta = {"take": "s30", "film": 7, "shots": [30], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1, "handle_in": H, "handle_out": H,
        "transition_in": "dissolve",
        "transition_in_detail": {"type": "dissolve", "frames": 9, "note": "from shot 29 (louvre empty_wall_queue -> wall_eye); in-handle g 2974..2979 rendered in 3D (crane continues)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "to shot 31 (take s31, the push to her glass); out-handle g 3096..3101 rendered in 3D (crane continues)"},
        "transitions": [{"at": G0, "type": "dissolve in"}, {"at": G_CUT, "type": "cut", "note": "inside the take: side angle -> reverse over the crowd, just before 'ละหลายหมื่นคน' (101.27 s = g 3041)"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"30": [G0, G1 - 1]},
        "setups": {"1": {"g": [FIRST, G_CUT - 1], "set": "louvre empty_wall_queue build, GALLERY_DAY, mona True, queue True; camera from the right side 13 D back, 32 mm, crane-in"},
                   "2": {"g": [G_CUT, LAST], "set": "same area; reverse from beside her frame looking down the gallery, 20 mm, crane up + back"}},
        "events": {"queue_to_her": [G0, G_CUT - 1], "cut_reverse_tens_of_thousands": G_CUT},
        "set": "v3/set3d7/louvre.py gallery (empty_wall_queue preset) with set_mona(True) + set_queue(True) keyed per frame (she is back), set_flames keyed per frame; runtime crowd of 107 / 149 actor cards (105 / 146 shown after the cull) (lady, gentleman, newsboy, coworker1/2, painter, plumber) packed in the queue lane and the room; anyone whose real head bottom falls below y 875 on any frame of the set-up is hidden for the whole set-up (2 + 3 people); cycles.transparent_max_bounces 160 (stacked cards)",
        "dof": "none (C.Take: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "cast": "v3/cast7 crowd_stare / crowd_point (+_gentleman/_newsboy) poses, turned toward her (mirror / yaw / gaze computed from each spot), idle head-roll steps every 11 frames, blinks; no mouths move",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mean("wall"), "s_per_frame_cpu_mean": mean("cpu"),
        "s_per_frame_by_setup": {"side": {"wall": mean("wall", 1), "cpu": mean("cpu", 1)}, "reverse": {"wall": mean("wall", 2), "cpu": mean("cpu", 2)}},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, LAST + 1, "a packed gallery: the murmur of a huge crowd, shuffling feet on parquet, a guard's low 'avancez, s'il vous plait', echo under the skylight", "ambience")
add(G0, G0 + 9, "dissolve in from shot 29: the crowd murmur swells", "transition")
add(G_CUT, G_CUT, "hard cut to the reverse: the crowd sound opens wide (bigger room tone)", "cut", peak_frame=G_CUT)
add(G_CUT + 2, G_CUT + 30, "a soft rising string swell under 'ละหลายหมื่นคน' (tens of thousands)", "music", peak_frame=G_CUT + 20)
add(G1, G1, "cut to shot 31: her face behind glass, the crowd sound drops away", "cut")
json.dump(dict(take="s30", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s %s%s" % (g, g / 30.0, "side" if g < G_CUT else "reverse", " handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
PAIRS = [(3010, 40, "40 s"), (3080, 46, "46 s")]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm); x = 0
for g, tref, sec in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab)); dr.text((x + 4, 4), "shot 30  g %d" % g, fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab)); dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
print("delivered", N, "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
