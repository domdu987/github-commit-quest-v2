"""Contact sheet of a landscape page: one mid frame per shot (plus extra times), 3 columns."""
import json, subprocess, sys, os
from PIL import Image, ImageDraw
port, sched, out = sys.argv[1], sys.argv[2], sys.argv[3]
extra = [float(x) for x in sys.argv[4:]]
S = json.load(open(sched))["shots"]
times = [(s["key"], round(s["start"] + s["dur"] * 0.55, 2)) for s in S] + [(f"t{t}", t) for t in extra]
tmp = os.path.join(os.path.dirname(out), "sheetL_tmp"); os.makedirs(tmp, exist_ok=True)
for k, t in times:
    f = os.path.join(tmp, f"{k}.png")
    subprocess.run(["timeout", "120", "node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapq.cjs"), port, "", f, str(t), "1920", "1080"], capture_output=True)
w, h = 640, 360; cols = 3; rows = (len(times) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, (h + 22) * rows), "black"); d = ImageDraw.Draw(sheet)
for i, (k, t) in enumerate(times):
    f = os.path.join(tmp, f"{k}.png")
    if os.path.exists(f): sheet.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * (h + 22) + 22))
    d.text(((i % cols) * w + 6, (i // cols) * (h + 22) + 4), f"{k} @{t}", fill="white")
sheet.save(out, quality=86); print("sheet", out, len(times), "frames")
