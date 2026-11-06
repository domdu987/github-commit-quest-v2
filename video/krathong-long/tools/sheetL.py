"""Contact sheet of 16:9 stills: python3 sheetL.py <dir with t*.png> <out.jpg> <cols> [label file: 't label' per line]"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
d, out, cols = sys.argv[1], sys.argv[2], int(sys.argv[3])
lab = {}
if len(sys.argv) > 4:
    for l in open(sys.argv[4], encoding="utf-8"):
        t, *r = l.rstrip("\n").split(" ", 1); lab[f"{float(t):.2f}"] = r[0] if r else ""
fs = sorted(glob.glob(os.path.join(d, "t*.png")), key=lambda f: float(os.path.basename(f)[1:-4]))
W, H = 640, 360
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
except Exception: font = None
rows = (len(fs) + cols - 1) // cols
im = Image.new("RGB", (cols * W, rows * H), "black")
for i, f in enumerate(fs):
    k = os.path.basename(f)[1:-4]; t = Image.open(f).convert("RGB").resize((W, H)); dr = ImageDraw.Draw(t)
    txt = f"{k}s {lab.get(k, '')}"; dr.rectangle([0, 0, 12 + 10 * len(txt), 26], fill="black"); dr.text((5, 3), txt, fill="yellow", font=font)
    im.paste(t, ((i % cols) * W, (i // cols) * H))
im.save(out, quality=84); print(out, len(fs))
