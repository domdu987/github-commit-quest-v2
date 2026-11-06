import sys, os, glob, json
from PIL import Image, ImageDraw, ImageFont
d, sched, out = sys.argv[1], sys.argv[2], sys.argv[3]
sh = json.load(open(sched))["shots"]
key = lambda t: next((s["key"] for s in sh if s["start"] <= t < s["start"] + s["dur"]), "?")
fs = sorted(glob.glob(d + "/t*.png"), key=lambda f: float(os.path.basename(f)[1:-4]))
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception: font = ImageFont.load_default()
W, H, C, N = 360, 640, 5, 10
for p in range(0, len(fs), N):
    ch = fs[p:p + N]; rows = (len(ch) + C - 1) // C
    im = Image.new("RGB", (C * W + 8 * (C + 1), rows * (H + 40) + 8), "#1e1a16"); dr = ImageDraw.Draw(im)
    for i, f in enumerate(ch):
        x, y = 8 + (i % C) * (W + 8), 8 + (i // C) * (H + 40)
        t = float(os.path.basename(f)[1:-4])
        im.paste(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + 36)); dr.text((x + 4, y + 6), f"{t:6.1f}s  {key(t)}", fill="#f2c230", font=font)
    im.save(f"{out}-{p // N + 1}.jpg", quality=88)
print(len(fs), "frames")
