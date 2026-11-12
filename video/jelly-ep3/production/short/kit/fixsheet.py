"""Sheet of chosen frames (label · time) from the vertical build at 360×640.  usage: python3 fixsheet.py <port> <out.jpg> <cols> label=t ..."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
port, out, cols = sys.argv[1], sys.argv[2], int(sys.argv[3]); items = [a.rsplit("=", 1) for a in sys.argv[4:]]
d = os.path.join(os.path.dirname(os.path.abspath(out)), "fsnap"); os.makedirs(d, exist_ok=True)
subprocess.run(["node", os.path.join(J, "snap.cjs"), port, d, "40.00"] + [f"{float(t):.2f}" for _, t in items], check=True, capture_output=True)
F = ImageFont.truetype(os.path.join(J, "hf/brc/assets/fonts/f3.ttf"), 20); W, H = 360, 640
rows = (len(items) + cols - 1) // cols; sh = Image.new("RGB", (cols * W, rows * (H + 30)), "black"); g = ImageDraw.Draw(sh)
for i, (lab, t) in enumerate(items):
    x, y = (i % cols) * W, (i // cols) * (H + 30)
    sh.paste(Image.open(os.path.join(d, f"t{float(t):.2f}.png")).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + 30)); g.text((x + 6, y + 5), f"{lab} · {float(t):.2f}s", fill="#fd6", font=F)
sh.save(out, quality=86)
for f in os.listdir(d):
    if f.endswith(".png"): os.remove(os.path.join(d, f))
print(out, sh.size)
