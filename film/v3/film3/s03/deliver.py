#!/usr/bin/env python3
"""deliver.py -- from raw/s3 (g 114..210), raw/s4 (g 197..332), raw/s5 (g 319..428) build frames/g_%04d.png with the two internal
10-frame dissolves mixed in (3 -> 4 at g 204: g 199..208; 4 -> 5 at g 326: g 321..330), take.mkv, meta.json, cues.json,
contact.jpg.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "v2", "shots"))
from anim import smoothstep_mix

G_S3, G_S4, G_S5, G_S6, H_IN, H_OUT, DISS = 122, 204, 326, 422, 8, 7, 10
FIRST, LAST = G_S3 - H_IN, G_S6 + H_OUT - 1
D34, D45 = G_S4 - DISS // 2, G_S5 - DISS // 2          # 199, 321: first mixed frames
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


def mix(a, b, g, d0, dst):
    w = smoothstep_mix(g - d0 + 1, DISS)
    A = np.asarray(Image.open(raw(a, g)).convert("RGB"), dtype=np.float32)
    B = np.asarray(Image.open(raw(b, g)).convert("RGB"), dtype=np.float32)
    Image.fromarray(np.clip(A * (1 - w) + B * w + 0.5, 0, 255).astype(np.uint8)).save(dst)
    return "s%d*%.3f+s%d*%.3f" % (a, 1 - w, b, w)


src = {}
for g in range(FIRST, LAST + 1):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if g < D34:
        shutil.copyfile(raw(3, g), dst); src[g] = "s3"
    elif g < D34 + DISS:
        src[g] = mix(3, 4, g, D34, dst)
    elif g < D45:
        shutil.copyfile(raw(4, g), dst); src[g] = "s4"
    elif g < D45 + DISS:
        src[g] = mix(4, 5, g, D45, dst)
    else:
        shutil.copyfile(raw(5, g), dst); src[g] = "s5"

rows = {}
for s in (3, 4, 5):
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(LAST - FIRST + 1), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

meta = {"take": "s03", "shots": [3, 4, 5], "g0": G_S3, "g1": G_S6, "first_g": FIRST, "n_frames": LAST - FIRST + 1,
        "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": "dissolve", "frames": 12, "note": "handle g 114..121 rendered in 3D (shot 3 camera and train run back)"},
        "transition_out": {"type": "dissolve", "frames": 10, "note": "handle g 422..428 rendered in 3D (shot 5 camera continues)"},
        "internal": [{"at": G_S4, "type": "dissolve", "frames": DISS, "mixed": [D34, D34 + DISS - 1], "from_shot": 3, "to_shot": 4,
                      "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 3 to g 210, shot 4 from g 197 (raw/)"},
                     {"at": G_S5, "type": "dissolve", "frames": DISS, "mixed": [D45, D45 + DISS - 1], "from_shot": 4, "to_shot": 5,
                      "mix": "smoothstep; raw handles: shot 4 to g 332, shot 5 from g 319 (raw/)"}],
        "shot_ranges": {"3": [G_S3, G_S4 - 1], "4": [G_S4, G_S5 - 1], "5": [G_S5, G_S6 - 1]},
        "set": "v3/set3d3/harbor.py", "light": "WINTER", "paint": 0, "seep": 0.6, "samples": 12, "resolution": [720, 1280],
        "threads": 2, "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, D34 + DISS, "Boston harbour 1919 from above: wind, gulls, a far steamer horn (one long blast around g 150), city murmur", "ambience")
add(FIRST, D34 + DISS, "El train on the steel trestle: rolling clatter of wheels on rail joints, steel girders humming; passes under the camera at the start and runs away toward the tank (fades by g 205)", "train")
add(150, 150, "far steamer horn (the freighter, optional)", "horn", impact_frame=150)
add(D34, D34 + DISS, "dissolve to the tank wall", "dissolve")
add(D34, D45 + DISS, "tank: low metallic groan under the tilt (swells toward the rim g 255), wind higher up", "groan")
add(200, 320, "worker climbing the caged ladder: boots on iron rungs, one clank every 18 frames (soft, high up)", "ladder")
add(255, 255, "the rim lands against the sky ('สูงกว่าตึกห้าชั้น'): wind gust", "accent")
add(260, 281, "reframe right onto the filling pipe: short whoosh; a gurgle of molasses inside the pipe from g 279 ('กากน้ำตาล')", "pipe", peak_frame=279)
add(D45, D45 + DISS, "dissolve to the street", "dissolve")
add(D45, LAST + 1, "street ambience: kids laughing and shouting in the snow, a horse snorting and stamping in the stable (off screen right), harness jingle, distant El rumble", "ambience")
add(340, 420, "worker walking across the cobbles behind the kids (boot steps every 7 frames)", "footsteps")
add(366, 372, "kid winds up and throws a snowball (whoosh at g 372)", "throw", impact_frame=372)
add(384, 384, "snowball puffs past the girl's hat; she squeals and ducks (laugh)", "snow_puff", impact_frame=384)
json.dump(dict(take="s03", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(i * (LAST - FIRST) / 15.0)) + FIRST for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:16]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
