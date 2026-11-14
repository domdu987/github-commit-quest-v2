#!/usr/bin/env python3
"""deliver.py -- from raw/s1..s7 build frames/g_%04d.png (4a -> 4b dissolve mixed in), meta.json, cues.json, contact.jpg,
compare.jpg (one final frame per shot beside its ref a frame).  python3 deliver.py"""
import os, sys, json, glob, shutil
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
from anim import smoothstep_mix

G_S2, G_S3, G_S4, G_END, H_OUT = 42, 81, 157, 315, 7
G_4B, G_4C, G_4D, DISS = 206, 251, 288, 12
D0 = G_4B - DISS // 2            # 200
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
BOUNDS = [(0, 1), (G_S2, 2), (G_S3, 3), (G_S4, 4), (G_4B, 5), (G_4C, 6), (G_4D, 7)]
NAME = {1: "1", 2: "2", 3: "3", 4: "4a", 5: "4b", 6: "4c", 7: "4d"}


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


src = {}
for g in range(0, G_END + H_OUT):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if D0 <= g < D0 + DISS:
        w = smoothstep_mix(g - D0 + 1, DISS)
        a = np.asarray(Image.open(raw(4, g)).convert("RGB"), dtype=np.float32)
        b = np.asarray(Image.open(raw(5, g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst); src[g] = "4a*%.3f+4b*%.3f" % (1 - w, w)
    else:
        s = max(sh for g0, sh in BOUNDS if g >= g0)
        shutil.copyfile(raw(s, g), dst); src[g] = NAME[s]

rows = {}
for s in range(1, 8):
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

meta = {"take": "s01", "film": 5, "shots": [1, 2, 3, 4], "first_g": 0, "n_frames": G_END + H_OUT, "g0": 0, "g1": G_END,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "dissolve_or_cut", "frames": 10, "note": "handle g 315..321 rendered in 3D (4d camera keeps moving)"},
        "transitions": [{"at": 0, "type": "open"},
                        {"at": G_S2, "type": "cut", "from_shot": 1, "to_shot": 2},
                        {"at": G_S3, "type": "cut", "from_shot": 2, "to_shot": 3},
                        {"at": 119, "type": "punch_in", "frames": 8, "shot": 3, "middle": 123},
                        {"at": G_S4, "type": "cut", "from_shot": 3, "to_shot": "4a"},
                        {"at": G_4B, "type": "dissolve", "frames": DISS, "mixed": [D0, D0 + DISS - 1], "from_shot": "4a", "to_shot": "4b",
                         "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: 4a to g 213, 4b from g 198 (raw/s4, raw/s5)"},
                        {"at": G_4C, "type": "cut", "from_shot": "4b", "to_shot": "4c"},
                        {"at": G_4D, "type": "cut", "from_shot": "4c", "to_shot": "4d"},
                        {"at": G_END, "type": "out", "handle": [G_END, G_END + H_OUT - 1]}],
        "shot_ranges": {"1": [0, G_S2 - 1], "2": [G_S2, G_S3 - 1], "3": [G_S3, G_S4 - 1], "4": [G_S4, G_END - 1],
                        "4a": [G_S4, G_4B - 1], "4b": [G_4B, G_4C - 1], "4c": [G_4C, G_4D - 1], "4d": [G_4D, G_END - 1]},
        "set": "v3/set3d5/mine.py: tunnel LAMP (shots 1-3, 4b-4d), pithead DUSK (4a); set cage carried (set_cage), gas 2.0-2.4 with a keyed drift of the haze pattern (4b-4d)",
        "dof": "none (client note: no depth of field anywhere; M.setup_dof(scene, None, None) before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST (ACCURATE tested: no visible gain, +12 CPU s)",
        "narration": "film5/audio/narration_bankky.wav at +0.10 s; captions film5/script/captions.json",
        "light": "LAMP / DUSK", "cast": "v3/cast5: alfie (1-3), miner1/2/3 (1), canary sprite on the 3D cage perch (1-3)",
        "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, G_S3, "deep mine tunnel room tone: distant drips, creak of timber props, faint hiss of the lamps", "ambience")
add(0, 14, "alfie lifts the brass cage: cage ring and wires jingle, a little swing", "prop")
add(4, G_S3, "the canary sings (bright chirping trills, continuous)", "bird_song")
add(20, 40, "miner2 digs: two soft shovel scrapes in coal", "work")
add(G_S2, G_S2, "hard cut to the ECU of the singing canary", "cut")
add(G_S2, G_S3, "canary song up close: a long trill of 5 notes (one per floating note)", "bird_song", notes=5)
add(G_S3, G_S3, "hard cut: low angle, alfie by the tub", "cut")
add(G_S3, G_S4, "the canary keeps singing softer in the background", "bird_song")
add(83, 92, "alfie points at the bird (sleeve swish)", "gesture", peak_frame=86)
add(119, 127, "snap punch-in on alfie (short whoosh in), middle g 123", "camera_snap", peak_frame=123, peak_time=t(123))
add(128, 140, "alfie flings his arm to point at the exit on 'hai wing' (cloth whip, small accent)", "gesture", peak_frame=135, peak_time=t(135))
add(G_S4, G_S4, "cut to the pithead at dusk", "cut")
add(G_S4, G_4B + 6, "pithead dusk ambience: wind, the winding wheels turning, far colliery hooter, crows", "ambience")
add(D0, D0 + DISS, "dissolve down into the tunnel (low whoosh / descending rumble of the cage)", "dissolve")
add(D0, G_END + H_OUT, "tunnel room tone, deeper, with a faint airy hiss (the gas)", "ambience")
add(G_4C, G_4C, "cut: the hanging lamp in the haze", "cut")
add(G_4C, G_4D, "lamp flame flutter close up, a soft gassy hiss", "lamp")
add(G_4D, G_4D, "cut: low under the roof lamps", "cut")
add(G_4D, G_END + H_OUT, "low ominous drone under the haze (the invisible gas)", "accent")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

N = G_END + H_OUT
gs = [int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s" % (g, g / 30.0, src[g][:14]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [("1", 30, 1, "0 s"), ("2", 66, 3, "1 s"), ("3", 140, 7, "3 s"), ("4a", 180, 31, "15 s"), ("4c", 270, 29, "14 s")]
w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for shot, g, tref, sec in PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (shot, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
