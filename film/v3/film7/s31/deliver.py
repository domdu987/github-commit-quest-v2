#!/usr/bin/env python3
"""deliver.py -- raw/s1 (g 3090..3218) -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv (libx264rgb crf 6).
python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
G0, G1, H, G_CUT = 3096, 3219, 6, 99999
FIRST, LAST = G0 - H, G1 - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for g in range(FIRST, LAST + 1):
    sid = 1
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = len(src)
mean = lambda k, s=None: round(float(np.mean([r[k] for r in rows if s is None or r["shot"] == s])), 2)
meta = {"take": "s31", "film": 7, "shots": [31], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1, "handle_in": H, "handle_out": 0,
        "transition_in": "cut",
        "transition_in_detail": {"type": "cut", "frames": 0, "note": "from shot 30 (take s30, same gallery); in-handle g 3090..3095 rendered in 3D (the push starts there) in case the conform dissolves"},
        "transition_out": {"type": "end", "frames": 0, "note": "g 3218 is the last frame of the film (N 3219); no out-handle"},
        "transitions": [{"at": G0, "type": "cut in"}, {"at": G1, "type": "end"}],
        "shot_ranges": {"31": [G0, G1 - 1]},
        "setups": {"1": {"g": [FIRST, LAST], "set": "louvre wall_eye build, GALLERY_DAY, mona True, queue True; 24 mm push from the rope (y 16.3) to 1.9 D from her glass"}},
        "events": {"reflection_fade_in": [3134, 3146], "reflection_hold": [3146, 3176], "reflection_smile": 3150, "reflection_blink": 3160, "reflection_fade_out": [3176, 3192]},
        "set": "v3/set3d7/louvre.py gallery (wall_eye preset) with set_mona(True) + set_queue(True) + set_flames keyed per frame; runtime reflection: a vincenzo actor card (scale 0.40, 0.012 D in front of her glass) whose card material multiplies the sprite alpha by a keyed opacity (peak 0.34), tints it toward a cool glass sheen and masks it to the glass rectangle in world x/z",
        "dof": "none (C.Take: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "cast": "v3/cast7 vincenzo (normal clothes, flat cap) as the reflection only: neutral -> small proud smile at g 3150, blink g 3160; no mouths move",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mean("wall"), "s_per_frame_cpu_mean": mean("cpu"),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
ev = []
def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
add(FIRST, LAST + 1, "the gallery hush close to her: the crowd murmur far behind, falling away as we push in", "ambience")
add(G0, LAST + 1, "a gentle closing theme (music box / soft strings) carrying to the end", "music")
add(3134, 3146, "the reflection appears: a faint glassy shimmer / chime", "accent", peak_frame=3140)
add(3150, 3160, "his small proud smile: a tiny warm pizzicato", "accent", peak_frame=3150)
add(3176, 3192, "the reflection fades: the chime decays", "accent", peak_frame=3184)
add(3200, LAST + 1, "final note held to the end of the film", "music", peak_frame=LAST)
json.dump(dict(take="s31", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s %s%s" % (g, g / 30.0, "refl" if 3134 < g < 3192 else "", " handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
PAIRS = [(3110, 51, "51 s"), (3160, 6, "6 s")]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm); x = 0
for g, tref, sec in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab)); dr.text((x + 4, 4), "shot 31  g %d" % g, fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab)); dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
print("delivered", N, "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
