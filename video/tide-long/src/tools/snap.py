"""Snapshot a 16:9 build at given times with video/longform/snapL.cjs and make contact sheets.

    python3 snap.py <build dir> <port> <out prefix> <schedule.json> [mode]

mode "cuts" (default): one frame per shot, at the middle of the shot (min 0.6 s in)
mode "t:1.0,2.5,..." : explicit times
Frames go to <out prefix>_frames/, sheets to <out prefix>_NN.jpg (2 columns of 960x540 tiles, 4 rows).
At most 18 frames per browser launch (longer sessions leave stale tiles, SKILL.md).
"""
import json
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
build, port, prefix, sched_path = sys.argv[1:5]
mode = sys.argv[5] if len(sys.argv) > 5 else "cuts"
S = json.load(open(sched_path))
shots = S["shots"]


def key_at(t):
    for s in shots:
        if s["start"] <= t < s["start"] + s["dur"]:
            return s["key"]
    return "?"


if mode == "cuts":
    times = [round(s["start"] + max(min(0.6, s["dur"] / 2), s["dur"] * 0.5), 2) for s in shots]
elif mode == "ends":   # each shot's first and last frame: the camera's widest framing is at one of them
    times = [round(x, 2) for s in shots for x in (s["start"] + 0.05, s["start"] + s["dur"] - 0.09)]
else:
    times = [float(x) for x in mode[2:].split(",")]
frames = prefix + "_frames"
os.makedirs(frames, exist_ok=True)
srv = subprocess.Popen(["python3", "-m", "http.server", str(port)], cwd=build, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
info = {}
try:
    env = {**os.environ, "NODE_PATH": "/opt/node22/lib/node_modules"}
    for i in range(0, len(times), 18):
        batch = [f"{t:.2f}" for t in times[i:i + 18]]
        out = subprocess.run(["node", os.path.join(HERE, "snapL.cjs"), str(port), frames, *batch], capture_output=True, text=True, env=env, timeout=900)
        for line in out.stdout.splitlines():
            if line.startswith("PAGEERROR"):
                print(line)
                continue
            parts = line.split(" ", 2)
            if len(parts) >= 2:
                info[float(parts[0])] = " ".join(parts[1:])
        if out.returncode:
            print(out.stderr[-2000:])
finally:
    srv.terminate()

font = ImageFont.truetype("/home/user/github-commit-quest-v2/video/tide-ep1/composition/assets/fonts/f2.ttf", 20 if mode == "ends" else 26)
TW, TH, LH, COLS, ROWS = (480, 270, 30, 4, 6) if mode == "ends" else (960, 540, 40, 2, 4)
for si in range(0, len(times), COLS * ROWS):
    chunk = times[si:si + COLS * ROWS]
    rows = (len(chunk) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * TW + (COLS - 1) * 8, rows * (TH + LH)), (18, 20, 22))
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(chunk):
        x, y = (k % COLS) * (TW + 8), (k // COLS) * (TH + LH)
        p = os.path.join(frames, f"t{t:.2f}.png")
        if os.path.exists(p):
            sheet.paste(Image.open(p).convert("RGB").resize((TW, TH), Image.LANCZOS), (x, y + LH))
        d.text((x + 8, y + 6), f"t={t:.2f}s  {key_at(t)}  {info.get(round(t, 2), '')}", fill=(240, 220, 160), font=font)
    out = f"{prefix}_{si // (COLS * ROWS) + 1:02d}.jpg"
    sheet.save(out, quality=88)
    print("sheet", out, len(chunk))
