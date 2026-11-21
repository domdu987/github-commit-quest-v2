#!/usr/bin/env python3
"""deliver.py -- from raw/s1..s5 build frames/g_%04d.png (shot 4 -> 5 dissolve mixed in), meta.json, cues.json, contact.jpg,
compare.jpg (one final frame per shot beside its reference frame of ref/a at the same size).  python3 deliver.py"""
import os, sys, json, glob, shutil
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
from anim import smoothstep_mix

G_S2, G_S3, G_S4, G_S5, G_END, H_OUT, DISS = 39, 75, 111, 185, 256, 7, 10
D0 = G_S5 - DISS // 2            # 180: first mixed frame
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
BOUNDS = [(0, 1), (G_S2, 2), (G_S3, 3), (G_S4, 4)]


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


src = {}
for g in range(0, G_END + H_OUT):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if g < D0:
        s = max(sh for g0, sh in BOUNDS if g >= g0)
        shutil.copyfile(raw(s, g), dst); src[g] = "s%d" % s
    elif g < D0 + DISS:
        w = smoothstep_mix(g - D0 + 1, DISS)
        a = np.asarray(Image.open(raw(4, g)).convert("RGB"), dtype=np.float32)
        b = np.asarray(Image.open(raw(5, g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst); src[g] = "s4*%.3f+s5*%.3f" % (1 - w, w)
    else:
        shutil.copyfile(raw(5, g), dst); src[g] = "s5"

rows = {}
for s in (1, 2, 3, 4, 5):
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

meta = {"take": "s01", "shots": [1, 2, 3, 4, 5], "first_g": 0, "n_frames": G_END + H_OUT, "g0": 0, "g1": G_END,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "dissolve", "frames": 10, "note": "handle g 256..262 rendered in 3D (shot 5 camera continues)"},
        "transitions": [{"at": 0, "type": "open"},
                        {"at": G_S2, "type": "cut", "from_shot": 1, "to_shot": 2},
                        {"at": G_S3, "type": "cut", "from_shot": 2, "to_shot": 3},
                        {"at": G_S4, "type": "cut", "from_shot": 3, "to_shot": 4},
                        {"at": G_S5, "type": "dissolve", "frames": DISS, "mixed": [D0, D0 + DISS - 1], "from_shot": 4, "to_shot": 5,
                         "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 4 to g 191, shot 5 from g 178 (raw/)"},
                        {"at": G_END, "type": "dissolve_out", "frames": 10, "handle": [G_END, G_END + H_OUT - 1]}],
        "shot_ranges": {"1": [0, G_S2 - 1], "2": [G_S2, G_S3 - 1], "3": [G_S3, G_S4 - 1], "4": [G_S4, G_S5 - 1], "5": [G_S5, G_END - 1]},
        "set": "v3/set3d4/pagoda.py v2 (open base, warm interior, dressing in the set; shot.py adds the shot-5 balcony)", "dof": {"1": "kenta card, f 3.5", "2": "(0.2, -0.62, FOOT_Z+0.5), f 6.0", "3": "(-3.6, -3.4, 6.0), f 7.0", "4": "kenta card, f 6.0", "5": "off"}, "narration": "film4/audio/narration_bankky.wav", "light": "DAY",
        "cast": "v3/cast4: kenta (shots 1, 4, 5), merchant / woman2 / farmer (shots 4, 5)", "sway": 0.0,
        "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, G_S2, "inside the pagoda base: soft temple room tone, faint wind bells far above", "ambience")
for g in (4, 30):
    add(g, g + 10, "kenta pulls on the hanging iron chain: chain links clink and creak taut", "chain")
add(G_S2, G_S2, "hard cut to the ECU of the floating pillar foot", "cut")
add(G_S2, G_S3, "oil-lamp flame flutter, a low wooden creak of the hanging pillar (it does not touch the stone)", "ambience")
add(G_S3, G_S3, "hard cut: up the pagoda past the roof corner", "cut")
add(G_S3, G_S4, "wind over the eaves, a wind bell on the corner rings softly", "ambience")
add(G_S4, G_S4, "hard cut: kenta in front of the opened base", "cut")
add(G_S4, G_S5 + 5, "courtyard ambience: light chatter of the townspeople, birds", "ambience")
add(125, 133, "kenta flings his arm out and points into the pagoda (cloth whip of the happi sleeve)", "gesture")
add(136, 145, "townspeople turn their heads to look at him (small cloth rustle)", "gesture")
add(148, 156, "snap punch-in on kenta (short whoosh in), middle g 152 on 'hai wing'", "camera_snap", peak_frame=152, peak_time=t(152))
add(164, 174, "pointing jab toward the doorway on 'khao ma nai ni' (small accent)", "gesture", peak_frame=167)
add(D0, D0 + DISS, "dissolve to the high establishing wide", "dissolve")
add(G_S5 - 5, G_END + H_OUT, "high wide town ambience: wind, distant street voices, a temple bell far off", "ambience")
add(205, 205, "'Yipun' (old Japan) lands: optional soft koto / shakuhachi phrase start", "accent")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film4/audio/narration_bankky.wav at +0.10 s, captions_bankky.json", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 16 evenly spaced final frames, label strip above each picture
N = G_END + H_OUT
gs = [int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:14]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: per shot one final frame beside its reference frame (ref a, second s -> t(2s+1)), same size
PAIRS = [(1, 20, 1, "0 s"), (2, 60, 3, "1 s"), (3, 95, 5, "2 s"), (4, 167, 7, "3 s"), (5, 230, 31, "15 s")]
w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for shot, g, tref, sec in PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (shot, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
