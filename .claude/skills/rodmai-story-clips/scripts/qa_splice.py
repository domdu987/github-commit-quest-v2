"""QA a spliced episode: for each key grab frames inside the shot (early/mid/late) and 1 frame either side of its edges.
usage: python3 qa_splice.py <video> <out.jpg> key…   (run inside the episode folder)"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
vid, out, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
S = {s["key"]: s for s in json.load(open("schedule.json"))["shots"]}
FR = 1 / 60
rows = []
for k in keys:
    s0, d = S[k]["start"], S[k]["dur"]
    ts = [("edge-", s0 - FR), ("edge+", s0 + FR), ("early", s0 + 0.6), ("mid", s0 + d * 0.55), ("late", s0 + d - 0.3), ("end-", s0 + d - FR), ("end+", s0 + d + FR)]
    rows.append((k, [(n, max(0, t)) for n, t in ts]))
W, H = 216, 384
fnt = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "..", "hf", "jkcov", "assets", "fonts", "f2.ttf"), 20)
sheet = Image.new("RGB", (7 * (W + 6) + 6, len(rows) * (H + 30) + 6), "#222")
dr = ImageDraw.Draw(sheet)
for r, (k, ts) in enumerate(rows):
    for c, (n, t) in enumerate(ts):
        f = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"qa_{k}_{c}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", vid, "-frames:v", "1", f], check=True)
        im = Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)
        x, y = 6 + c * (W + 6), 6 + r * (H + 30)
        sheet.paste(im, (x, y + 24)); dr.text((x + W / 2, y + 11), f"{k} {n} {t:.2f}", fill="#fff", font=fnt, anchor="mm"); os.remove(f)
sheet.save(out, quality=86); print("qa", out)
