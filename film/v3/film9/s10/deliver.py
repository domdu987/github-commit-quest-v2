#!/usr/bin/env python3
"""deliver.py -- raw/s1 + raw/s2 -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, take.mkv (libx264rgb crf 6; split into
take.mkv.part* with split -b 40M when over 45 MB).  The take-specific numbers live in take_conf.py next to this file.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import take_conf as K                                      # noqa: E402

FIRST, LAST = K.FIRST, K.LAST
N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for g in range(FIRST, LAST + 1):
    sid = 1 if g < K.G_CUT else 2
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = {}
for sid in (1, 2):
    w = [m["wall"] for m in rows if m["shot"] == sid]; c = [m["cpu"] for m in rows if m["shot"] == sid]
    by[K.SETUPS[sid]["name"]] = {"wall": round(float(np.mean(w)), 2), "cpu": round(float(np.mean(c)), 2)}

meta = {"take": K.TAKE, "film": 9, "shots": K.SHOTS, "g0": K.G0, "g1": K.G1, "first_g": FIRST, "n_frames": N,
        "handle_in": K.G0 - FIRST, "handle_out": LAST + 1 - K.G1,
        "transition_in": {"type": "cut", "frames": 0, "note": "plan cut from the previous shot at g %d; in-handle g %d..%d rendered in 3D" % (K.G0, FIRST, K.G0 - 1)},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan cut to the next shot at g %d; out-handle g %d..%d rendered in 3D" % (K.G1, K.G1, LAST)},
        "transitions": [{"at": K.G0, "type": "in", "handle": [FIRST, K.G0 - 1]},
                        {"at": K.G_CUT, "type": "cut", "note": "plan cut shot %d -> shot %d inside the take (same location and light, new set-up)" % tuple(K.SHOTS)},
                        {"at": K.G1, "type": "out", "handle": [K.G1, LAST]}],
        "shot_ranges": {str(K.SHOTS[0]): [K.G0, K.G_CUT - 1], str(K.SHOTS[1]): [K.G_CUT, K.G1 - 1]},
        "setups": {str(K.SHOTS[i - 1]): {"g": [FIRST if i == 1 else K.G_CUT, K.G_CUT - 1 if i == 1 else LAST], "set": K.SETUPS[i]["set"]} for i in (1, 2)},
        "events": K.EVENTS, "set": K.SET, "cast": K.CAST, "mouths": K.MOUTHS,
        "dof": "none (cam.data.dof.use_dof False + wall.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, prefilter FAST", "narration": "film9/audio/narration.wav at +0.10 s; captions film9/script/captions.json",
        "light": K.LIGHT, "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": by}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
for g0, g1, kind, label, peak in K.CUES:
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    if peak is not None:
        e["peak_frame"] = int(peak)
    ev.append(e)
json.dump(dict(take=K.TAKE, fps=30, note="time = film seconds (g / 30); narration film9/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    tag = " handle" if g < K.G0 or g >= K.G1 else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, K.SHOTS[0] if g < K.G_CUT else K.SHOTS[1], tag), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
for p in glob.glob(mkv + ".part*"):
    os.remove(p)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
size = os.path.getsize(mkv)
if size > 45 * 1024 * 1024:
    subprocess.run(["split", "-b", "40M", "take.mkv", "take.mkv.part"], cwd=HERE, check=True)
    os.remove(mkv)
    print("take.mkv %.1f MB -> split into" % (size / 1048576.0), sorted(os.path.basename(p) for p in glob.glob(mkv + ".part*")))
print("delivered", N, "frames g %d..%d; mean wall %.2f s, cpu %.2f s" % (FIRST, LAST, np.mean(walls), np.mean(cpus)))
