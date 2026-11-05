# tile the fit frames of the three chapters into labelled sheets (global film time + shot key), 4×4 per sheet at 640×360
import json, glob, os, sys
from PIL import Image, ImageDraw, ImageFont
L = sys.argv[1]; out = sys.argv[2]; os.makedirs(out, exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
off = 0.0; items = []
for E in (1, 2, 3):
    s = json.load(open(f"{L}/long/ch{E}.json"))
    for f in sorted(glob.glob(f"{L}/fit/c{E}/t*.png"), key=lambda f: float(os.path.basename(f)[1:-4])):
        t = float(os.path.basename(f)[1:-4]); key = next((x["key"] for x in s["shots"] if x["start"] <= t < x["start"] + x["dur"]), "?")
        g = off + t; items.append((f, f"{int(g // 60)}:{g % 60:05.2f} {key}"))
    off += s["total"]
W, H, C = 640, 360, 4
for k in range(0, len(items), 16):
    ch = items[k:k + 16]; R = (len(ch) + C - 1) // C
    cs = Image.new("RGB", (W * C, H * R))
    for i, (f, lab) in enumerate(ch):
        im = Image.open(f).convert("RGB").resize((W, H)); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 11 * len(lab) + 8, 24), fill=(0, 0, 0)); d.text((4, 2), lab, fill=(255, 255, 0), font=font)
        cs.paste(im, ((i % C) * W, (i // C) * H))
    cs.save(f"{out}/fit_{k // 16:02d}.jpg", quality=80)
print(len(items), "frames")
