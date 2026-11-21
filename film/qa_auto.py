"""Automatic every-frame QA (QA_TEAM.md section A). No model cost.
usage: python3 qa_auto.py <video> [--cuts g1,g2,...] [--first_g G] [--out DIR]
Writes DIR/QA_AUTO.md and DIR/phone_sheet.jpg (360x640 tiles, one per 0.5 s). Exit code 1 on FAIL."""
import sys, os, subprocess, json, argparse
import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("--cuts", default=""); ap.add_argument("--first_g", type=int, default=0)
ap.add_argument("--out", default=None)
a = ap.parse_args()
out = a.out or os.path.dirname(os.path.abspath(a.video)); os.makedirs(out, exist_ok=True)
cuts = [int(c) for c in a.cuts.split(",") if c.strip()]

W, H = 180, 320  # analysis size (keeps memory low, 1/4 of 720x1280)
probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=r_frame_rate", "-of", "json", a.video], capture_output=True, text=True).stdout)
num, den = map(int, probe["streams"][0]["r_frame_rate"].split("/")); fps = num / den
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
n = len(v); g = np.arange(n) + a.first_g
gray = v.astype(np.float32).mean(-1)

fails, notes = [], []
# 1. black / blank / magenta, frozen runs, pops
mean = gray.mean((1, 2)); std = gray.std((1, 2))
black = np.flatnonzero(mean < 8); blank = np.flatnonzero(std < 3)
r, gch, b = [v[..., i].astype(np.int16) for i in range(3)]
mag = ((r > 180) & (b > 180) & (gch < 80)).mean((1, 2))
magenta = np.flatnonzero(mag > 0.25)
diff = np.abs(np.diff(gray, axis=0)).mean((1, 2))
frozen = []; run = 0
for i, d in enumerate(diff):
    run = run + 1 if d < 0.05 else 0
    if run == 5: frozen.append(int(g[i - 4]))
med = np.median(diff) + 1e-6
spikes = [int(g[i + 1]) for i, d in enumerate(diff) if d > max(12, 8 * med)]
pops = [s for s in spikes if not any(abs(s - c) <= 2 for c in cuts)]
missing_cuts = [c for c in cuts if not any(abs(s - c) <= 2 for s in spikes)]
for name, arr in (("black", black), ("blank", blank), ("magenta", magenta)):
    if len(arr): fails.append(f"{name} frames: {[int(g[i]) for i in arr[:20]]}{' ...' if len(arr) > 20 else ''}")
if frozen: fails.append(f"frozen runs >= 6 frames starting at g {frozen[:20]}")
if pops: notes.append(f"pops outside planned cuts (check by eye): g {pops[:30]}")
if cuts and missing_cuts: notes.append(f"planned cuts with no visible change within +-2 frames: g {missing_cuts}")
# 2. sharpness (Laplacian variance vs median)
lap = np.abs(4 * gray[:, 1:-1, 1:-1] - gray[:, :-2, 1:-1] - gray[:, 2:, 1:-1] - gray[:, 1:-1, :-2] - gray[:, 1:-1, 2:]).var((1, 2))
soft = [int(g[i]) for i in np.flatnonzero(lap < 0.6 * np.median(lap))]
if len(soft) > 0.05 * n: fails.append(f"suspected blur on {len(soft)} frames, e.g. g {soft[:15]}")
elif soft: notes.append(f"soft frames (check by eye; motion streak allowed 1-3 frames): g {soft[:15]}")
# 4. colour: magenta share per second
mshare = float(mag.mean()); notes.append(f"magenta share {mshare*100:.1f} %")
if mshare > 0.10: fails.append(f"magenta share {mshare*100:.1f} % > 10 %")
# 5. phone sheet, one tile per 0.5 s at 360x640 -> shown at 180x320 in a grid, labelled with g
step = max(1, int(round(fps / 2))); idx = list(range(0, n, step)); cols = 10
rows = (len(idx) + cols - 1) // cols; sheet = Image.new("RGB", (cols * W, rows * (H + 14)), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for k, i in enumerate(idx):
    x, y = (k % cols) * W, (k // cols) * (H + 14)
    sheet.paste(Image.fromarray(v[i]), (x, y)); dr.text((x + 3, y + H), f"g{g[i]} {i/fps:.1f}s", fill=(230, 230, 230))
    dr.line([(x, y + int(H * 880 / 1280)), (x + W, y + int(H * 880 / 1280))], fill=(0, 200, 255))
sheet.save(os.path.join(out, "phone_sheet.jpg"), quality=88)

verdict = "FAIL" if fails else "PASS"
txt = [f"# QA_AUTO {verdict}  ({os.path.basename(a.video)}, {n} frames, {fps:.2f} fps, g {g[0]}-{g[-1]})", ""]
txt += ["## FAIL"] + [f"- {f}" for f in fails] if fails else []
txt += ["## Notes"] + [f"- {s}" for s in notes]
txt += ["", "Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it."]
open(os.path.join(out, "QA_AUTO.md"), "w").write("\n".join(txt) + "\n")
print("\n".join(txt)); sys.exit(1 if fails else 0)
