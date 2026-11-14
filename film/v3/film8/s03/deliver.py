#!/usr/bin/env python3
"""deliver.py -- from raw/s3..s7 (g 172..613) build frames/g_%04d.png (shot 3 gets a faint heat shimmer in the far street band),
meta.json, cues.json, contact.jpg, compare.jpg and take.mkv (libx264rgb crf 6, all frames g 172..613).   python3 deliver.py"""
import os, sys, json, subprocess, math
import numpy as np
import cv2
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

G0, G1, H_IN, H_OUT = 178, 608, 6, 6
B4, B5, B6, B7 = 258, 358, 432, 541
FIRST, LAST = G0 - H_IN, G1 + H_OUT - 1
RANGES = {3: (FIRST, B4 - 1), 4: (B4, B5 - 1), 5: (B5, B6 - 1), 6: (B6, B7 - 1), 7: (B7, LAST)}
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)


def shot_of(g):
    return [s for s, (a, b) in RANGES.items() if a <= g <= b][0]


def shimmer(img, g):
    """heat haze: a <= 0.9 px horizontal + 0.4 px vertical wobble, strongest in the far street band (y 0.30..0.62 H), off elsewhere."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = np.clip(1.0 - np.abs(yy / h - 0.46) / 0.16, 0.0, 1.0) ** 1.5
    t = g / 30.0
    dx = 0.9 * band * np.sin(yy * 0.11 + t * 9.0 + np.sin(xx * 0.03 + t * 3.0))
    dy = 0.4 * band * np.sin(xx * 0.07 - t * 7.0)
    return cv2.remap(img, xx + dx, yy + dy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


rows, src = [], {}
for g in range(FIRST, LAST + 1):
    s = shot_of(g)
    raw = os.path.join(HERE, "raw", "s%d" % s)
    im = cv2.imread(os.path.join(raw, "g_%04d.png" % g), cv2.IMREAD_UNCHANGED)
    if s == 3:
        im = shimmer(im, g)
    cv2.imwrite(os.path.join(OUT, "g_%04d.png" % g), im)
    src[g] = str(s)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = len(src)
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = {str(s): dict(wall=round(float(np.mean([m["wall"] for m in rows if m["shot"] == s])), 2),
                   cpu=round(float(np.mean([m["cpu"] for m in rows if m["shot"] == s])), 2)) for s in RANGES}

meta = {"take": "s03", "film": 8, "shots": [3, 4, 5, 6, 7], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": "dissolve", "frames": 8, "note": "dissolve from the desert night (s01 shot 2) into the bazaar at noon; in-handle g 172..177 rendered in 3D (the crane is higher, continuing the move)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 8 (desert_ice DAWN, wall_low) follows at g 608; out-handle g 608..613 rendered in 3D (walk + push continue)"},
        "transitions": [{"at": G0, "type": "dissolve_in", "handle": [FIRST, G0 - 1]},
                        {"at": B4, "type": "cut"}, {"at": B5, "type": "cut"}, {"at": B6, "type": "cut"}, {"at": B7, "type": "cut"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"3": [G0, B4 - 1], "4": [B4, B5 - 1], "5": [B5, B6 - 1], "6": [B6, B7 - 1], "7": [B7, G1 - 1]},
        "setups": {"3": {"g": [FIRST, B4 - 1], "set": "bazaar NOON, bazaar_wide crane down: camera (0.2,-14.5,13) -> (0.4,-12,6.6) looking north down the street, 20 mm; faint heat shimmer (post, far street band)"},
                   "4": {"g": [B4, B5 - 1], "set": "bazaar NOON, well_eye area: eye level in the square, push + orbit (-3.7,24.6,2.3) -> (-2.3,27.5,2.45), 22 mm"},
                   "5": {"g": [B5, B6 - 1], "set": "bazaar NOON, merchant_stall area: push in on the merchant on his takht over the giant jars, 22 mm"},
                   "6": {"g": [B6, B7 - 1], "set": "bazaar NOON, low medium two-shot from the north-west of the stall (z 1.9, pitch up 9-10), 19 mm, slow push"},
                   "7": {"g": [B7, LAST], "set": "bazaar NOON, street-level wide looking north to the iwan, slow push, 20 mm"}},
        "events": {"crane_down": [FIRST, B4 - 1], "boy_hops_hot_ground": [B4, B5 - 1], "fanning": [B4, B5 - 1], "merchant_laughs": [B5, B6 - 1],
                   "merchant_quote_lipsync": [435, 540], "point_up": [434, 446], "madman_jab": [476, 488], "farid_calm_blinks": [455, 500, 532],
                   "townsfolk_point_and_laugh": [B7, LAST], "nickname_caption": 584},
        "lipsync": "merchant only, g 435..540 (14.4-17.9 s): mouth ('open', w, h) driven by the narration RMS envelope per frame (+0.10 s), 'flat' in pauses",
        "set": "v3/set3d8/desert.py bazaar, NOON (sun from the south-west, west arcade in blue shade); set_flames + set_stars keyed per frame; no runtime set changes (the street is already dense)",
        "dof": "none (client rule: cam.data.dof.use_dof False + D.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json",
        "light": "NOON",
        "cast": "v3/cast8: merchant (laugh, mock + lip-sync), farid (calm smile arms folded, walk), woman (jar walk, fan, laugh), oldman (stick, fan, point), boy (run, hop, laugh), a second woman (walk, point)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_shot": by,
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, G0 + 2, "dissolve from the cold desert night into the blazing noon bazaar: night ambience crossfades into the town", "transition")
add(FIRST, LAST + 1, "Persian bazaar at blazing noon: distant crowd murmur, a copper hammer tinkling far off, a donkey bray, cicada-like heat buzz, soft wind flapping awnings", "ambience")
add(FIRST, B4, "crane down: a warm swelling oud / santur phrase, a high shimmering heat tone", "music")
add(B4, B5, "fans flapping (soft papery whoosh every ~4 frames), townsfolk sigh in the heat", "foley")
add(318, B5, "the boy hops on the burning ground: quick 'ow-ow' hops, bare feet slapping hot paving", "foley", peak_frame=340)
add(B5, B6, "the merchant's huge belly laugh (booming, echoing off the arcade), jars ring faintly", "foley", peak_frame=380)
add(434, 446, "the merchant's ringed finger snaps up to point: a jangle of rings", "foley", peak_frame=440)
add(476, 488, "'ไอ้บ้า!' jab: a comic sting", "accent", peak_frame=480)
add(500, 503, "farid's calm blink: a tiny soft tick", "accent", peak_frame=500)
add(B7, LAST + 1, "the whole bazaar jeers and laughs, overlapping voices, pointing", "foley", peak_frame=584)
add(G1, G1, "plan: cut to shot 8, the desert at dawn (wall_low)", "cut")
json.dump(dict(take="s03", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    hd = " handle" if (g < G0 or g >= G1) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, shot_of(g), hd), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(230, 69, "a"), (480, 33, "b")]      # bright establishing of a lit set | two-shot medium in daylight
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, rs in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (shot_of(g), g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref %s t%04d" % (rs, tref), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", N, "frames + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))
