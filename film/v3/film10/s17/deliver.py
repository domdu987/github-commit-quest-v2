#!/usr/bin/env python3
"""deliver.py -- film 10 take builder: raw/sNN/g_%04d.png (+ json) -> frames/, meta.json, cues.json, contact.jpg, take.mkv, QA_AUTO.md,
phone_sheet.jpg.  Edit TAKE for the take.   python3 deliver.py [--no-qa]"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = json.load(open(os.path.join(HERE, "take.json")))
name, shots, ranges = TAKE["take"], TAKE["shots"], {int(k): v for k, v in TAKE["ranges"].items()}
g0, g1 = TAKE["g0"], TAKE["g1"]; H_IN, H_OUT = 6, 6
first, last = g0 - H_IN, g1 + H_OUT - 1
OUT = os.path.join(HERE, "frames"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
rows, src = [], {}
for g in range(first, last + 1):
    sid = [s for s in shots if ranges[s][0] <= g <= ranges[s][1]][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
n = last - first + 1
cpus = [m["cpu"] for m in rows]; walls = [m["wall"] for m in rows]
by = {s: [m["cpu"] for m in rows if m["shot"] == s] for s in shots}
meta = dict(take=name, film=10, shots=shots, first_g=first, n_frames=n, g0=g0, g1=g1, handle_in=H_IN, handle_out=H_OUT,
            transition_in=dict(type="cut", frames=0), transition_out=dict(type="cut", frames=0),
            shot_ranges={str(s): ranges[s] for s in shots}, cuts=TAKE["cuts"], setups=TAKE["setups"], events=TAKE["events"], light="SEA_DAY",
            set="v3/set3d10/harbour.py (sea)", dof="none", denoiser="OpenImageDenoise", samples=12, resolution=[720, 1280], threads=2, fps=30,
            narration="film10/audio/narration.wav at +0.10 s", s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2), s_per_frame_wall_mean=round(float(np.mean(walls)), 2),
            s_per_frame_cpu_by_shot={str(s): round(float(np.mean(v)), 2) for s, v in by.items()},
            frame_source={str(g): v for g, v in src.items()})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = [dict(time=round(g / 30.0, 3), duration=round((e - g) / 30.0, 3), frame=g, end_frame=e, kind=k, label=l) for g, e, k, l in TAKE["cues"]]
json.dump(dict(take=name, fps=30, note="time = film seconds (g / 30); narration film10/audio/narration.wav at +0.10 s", cues=cues), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
# contact sheet
gs = [int(round(first + i * (n - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, src[g], " handle" if (g < g0 or g >= g1) else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("take.mkv", os.path.getsize(mkv) // 1024, "KB,", n, "frames, first_g", first)
if "--no-qa" not in sys.argv:
    r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(first), "--cuts", ",".join(str(c) for c in TAKE["cuts"])])
    print("qa_auto exit", r.returncode)
