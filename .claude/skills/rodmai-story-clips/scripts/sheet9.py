"""Portrait contact sheets, 3x3 cells of 360x640 (readable in the viewer): python3 sheet9.py <port> <schedule.json> <out prefix> [key=frac ...]
One frame per shot at 55% of its length, plus extra beats given as key=frac (e.g. b03=0.9). Frames are shot three at a time."""
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
port, sched, out = sys.argv[1], sys.argv[2], sys.argv[3]
S = json.load(open(sched))["shots"]; byk = {s["key"]: s for s in S}
times = [(s["key"], round(s["start"] + s["dur"] * 0.55, 2)) for s in S]
for a in sys.argv[4:]:
    k, f = a.split("="); s = byk[k]; times.append((f"{k}x{f}", round(s["start"] + s["dur"] * float(f), 2)))
times.sort(key=lambda kt: kt[1])
tmp = out + "_tmp"; os.makedirs(tmp, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
def snap(kt):
    k, t = kt; f = os.path.join(tmp, f"{k}.png")
    r = subprocess.run(["timeout", "150", "node", os.path.join(here, "snapq.cjs"), port, "", f, str(t)], capture_output=True, text=True)
    return k, r.stdout.strip()
with ThreadPoolExecutor(3) as ex:
    for k, err in ex.map(snap, times):
        if err: print(k, err[:300])
w, h = 360, 640
for n in range(0, len(times), 9):
    chunk = times[n:n + 9]; rows = (len(chunk) + 2) // 3
    sheet = Image.new("RGB", (w * 3, (h + 22) * rows), "black"); d = ImageDraw.Draw(sheet)
    for i, (k, t) in enumerate(chunk):
        f = os.path.join(tmp, f"{k}.png")
        if os.path.exists(f): sheet.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % 3) * w, (i // 3) * (h + 22) + 22))
        d.text(((i % 3) * w + 6, (i // 3) * (h + 22) + 4), f"{k} @{t}", fill="white")
    sheet.save(f"{out}{n // 9 + 1}.jpg", quality=86)
print("sheets", (len(times) + 8) // 9, "frames", len(times))
