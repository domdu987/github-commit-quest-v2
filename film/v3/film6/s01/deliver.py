#!/usr/bin/env python3
"""deliver.py -- from raw/s1 build frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg (final frames beside the
closest ref a frames) and take.mkv (libx264rgb crf 6, all frames g 0..69).  python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

G_END, H_OUT = 63, 7
N = G_END + H_OUT
RAW = os.path.join(HERE, "raw", "s1"); OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src = {}
for g in range(N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "1"
rows = [json.load(open(js)) for js in sorted(glob.glob(os.path.join(RAW, "g_*.json")))]
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

meta = {"take": "s01", "film": 6, "shots": [1], "first_g": 0, "n_frames": N, "g0": 0, "g1": G_END,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 2 (table_insert ECU) is a cut at g 63; handle g 63..69 rendered in 3D (push + grin continue) in case the conform dissolves"},
        "transitions": [{"at": 0, "type": "open"}, {"at": G_END, "type": "out", "handle": [G_END, N - 1]}],
        "shot_ranges": {"1": [0, G_END - 1]},
        "events": {"loaf_10_drops": 8, "loaf_11_drops": 21, "loaf_12_drops": 34, "look_to_lens": [36, 40], "wink": [40, 45],
                   "glance_back_at_henry": [46, 50], "slip_13th": [49, 56], "loaf_13_drops": 57, "grin": 58},
        "set": "v3/set3d6/bakery.py: bakery MORNING (the plan's 'DAWN' counter), steam 0.35, oven 1.0 flicker keyed per frame; custom street-side camera (24 mm) between the counter preset and the actors",
        "dof": "none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
        "light": "MORNING",
        "cast": "v3/cast6: kit (on a hidden stool behind the counter, held prop loaf x0.9), henry (background by the oven, squinting at a loaf); the customer's basket = cast6.basket_svg (9..13 loaves) on a 2D prop card (film6/common.py PropCard) standing on the counter, x1.4",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, N, "bakery at dawn, inside: the oven fire roaring low and crackling, a soft street murmur through the counter opening", "ambience")
for k, (g0, g1) in enumerate(((0, 7), (13, 20), (26, 33))):
    add(g1, g1 + 2, "loaf %d dropped onto the pile in the wicker basket: soft crusty thump + wicker creak" % (10 + k), "prop", peak_frame=g1 + 1)
add(40, 45, "kit winks at the camera: tiny bright 'ting' / sparkle accent", "accent", peak_frame=40)
add(46, 50, "quick glance over his shoulder at henry (short cloth swish)", "gesture", peak_frame=48)
add(49, 56, "the sneaky 13th loaf: tiptoe pizzicato pluck as it rises, thump on the top of the pile", "prop", peak_frame=57)
add(58, N, "kit grins at us (cheeky little musical sting)", "accent", peak_frame=58)
add(G_END, G_END, "plan: cut to shot 2, ECU of the extra loaf landing on the pile with a steam puff", "cut")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot 1%s" % (g, g / 30.0, " handle" if g >= G_END else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(56, 46, "45 s"), (42, 1, "0 s")]          # last frame of the action (13th lands) | the wink, beside the closest ref a frames
w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for g, tref, sec in PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot 1  g %d (%.2f s)" % (g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", "0", "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
