"""contact sheet: python3 sheet.py out.jpg pngs... (360x640 tiles, red line at the caption band y 880)"""
import sys
from PIL import Image, ImageDraw
fs = sys.argv[2:]; W, H = 360, 640; cols = min(7, len(fs)); rows = (len(fs) + cols - 1) // cols
c = Image.new("RGB", (W * cols, H * rows))
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((W, H)); d = ImageDraw.Draw(im)
    d.text((5, 5), f.split("/")[-1], fill="yellow"); d.line((0, 440, W, 440), fill="red")
    c.paste(im, ((i % cols) * W, (i // cols) * H))
c.save(sys.argv[1], quality=85)
