"""Real-frame fit sheets from a rendered long-form file: realsheet.py <video> <schedule.json> <out dir> [card keys…]
Every shot at 25% and 75% of its length; the listed card shots every 0.5 s. 480×270 cells labelled with time and shot, 4×5 per sheet."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
vid, sc, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]; cards = set(sys.argv[4:]); os.makedirs(out, exist_ok=True)
pts = []
for s in sc["shots"]:
    a, d = s["start"], s["dur"]
    ts = [a + d * f for f in (0.25, 0.75)]
    if s["key"] in cards: ts = [a + 0.1 + 0.5 * i for i in range(int((d - 0.15) / 0.5) + 1)]
    pts += [(round(t, 3), s["key"]) for t in ts]
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else None
cells = []
for i, (t, k) in enumerate(pts):
    f = os.path.join(out, f"c{i:04d}.jpg")
    if not os.path.exists(f):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", vid, "-frames:v", "1", "-vf", "scale=480:270", "-q:v", "4", f], check=True)
    im = Image.open(f).convert("RGB"); d = ImageDraw.Draw(im)
    lab = f"{int(t // 60)}:{t % 60:05.2f} {k}"; d.rectangle([0, 0, 8 + 11 * len(lab), 24], fill=(0, 0, 0)); d.text((4, 2), lab, fill=(255, 230, 0), font=font)
    cells.append(im)
for j in range(0, len(cells), 20):
    S = Image.new("RGB", (4 * 480, 5 * 270), "black")
    for i, im in enumerate(cells[j:j + 20]): S.paste(im, ((i % 4) * 480, (i // 4) * 270))
    S.save(os.path.join(out, f"sheet_{j // 20 + 1:02d}.jpg"), quality=78)
print(len(pts), "frames", (len(cells) + 19) // 20, "sheets")
