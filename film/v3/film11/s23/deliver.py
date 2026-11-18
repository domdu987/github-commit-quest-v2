#!/usr/bin/env python3
"""deliver.py <take dir name sNN> <shot id> <first_g> <last_g> <g0> <g1> <transition cut|dissolve> <ambience label> -- encode take.mkv, meta.json, cues.json,
contact.jpg, heads check (raw json), qa_auto (QA_AUTO.md + phone_sheet.jpg)."""
import os, sys, json, subprocess, glob
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
take, shot, a, b, g0, g1, tr, amb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7], sys.argv[8]
raw = os.path.join(HERE, "raw", "s%d" % shot)
fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
for g in range(a, b + 1):
    d = os.path.join(fr, "g_%04d.png" % g)
    if not os.path.exists(d):
        os.symlink(os.path.join(raw, "g_%04d.png" % g), d)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(a), "-i", os.path.join(fr, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6",
                "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(HERE, "take.mkv"))
if sz > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True)
meta = dict(take=take, film=11, shots=[shot], first_g=a, n_frames=b - a + 1, g0=g0, g1=g1, handle_in=g0 - a, handle_out=b - (g1 - 1),
            transition_in=dict(type=tr, frames=8 if tr == "dissolve" else 0), transition_out=dict(type="cut", frames=0), size_bytes=sz)
# heads / wall time
heads_min = 9999; walls = []; cpus = []; worst = None
for g in range(a, b + 1):
    j = json.load(open(os.path.join(raw, "g_%04d.json" % g)))
    walls.append(j["wall"]); cpus.append(j["cpu"])
    for k, v in j["heads"].items():
        top = v["y"] + v["w"] * 0.5     # head centre y + radius = chin (px)
        if worst is None or top > worst[0]:
            worst = (top, g, k)
meta["s_per_frame_wall"] = round(sum(walls) / len(walls), 2); meta["s_per_frame_cpu"] = round(sum(cpus) / len(cpus), 2)
meta["max_head_chin_y"] = [round(worst[0], 1), worst[1], worst[2]]
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration film11/audio/narration.wav at +0.10 s",
               cues=[dict(time=round(g0 / 30.0, 3), duration=round((g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind="ambience", label=amb)]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)
# contact sheet: 6 fps -> every 5th frame, 360x640 tiles, cyan line at y 880
idx = list(range(a, b + 1, 5)); cols = 8; W, H = 180, 320
rows = (len(idx) + cols - 1) // cols
sh = Image.new("RGB", (cols * W, rows * (H + 12)), (20, 20, 20)); dr = ImageDraw.Draw(sh)
for k, g in enumerate(idx):
    im = Image.open(os.path.join(raw, "g_%04d.png" % g)).convert("RGB").resize((W, H), Image.LANCZOS)
    x, y = (k % cols) * W, (k // cols) * (H + 12)
    sh.paste(im, (x, y)); dr.text((x + 3, y + H), "g%d" % g, fill=(230, 230, 230)); dr.line([(x, y + int(H * 880 / 1280)), (x + W, y + int(H * 880 / 1280))], fill=(0, 200, 255))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
r = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "..", "qa_auto.py"), os.path.join(HERE, "take.mkv"), "--first_g", str(a), "--cuts", "", "--out", HERE],
                   capture_output=True, text=True)
print(r.stdout[-2500:]); print(json.dumps(meta))
