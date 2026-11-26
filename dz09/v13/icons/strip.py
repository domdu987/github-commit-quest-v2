"""strip.py -- strip.png: one frame per icon change, icons over the newest draft frames (top part of the frame)."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
import icons13 as I, base
TIMES = [0.5, 1.3, 2.25, 2.75, 3.29, 3.6, 5.0, 6.5, 16.2, 16.36, 16.56, 16.76, 17.2, 17.9, 18.4, 19.2, 20.5, 21.6, 22.1, 22.6, 25.6, 28.1, 28.5,
         30.2, 31.9, 32.15, 32.6, 34.2, 37.0, 39.6, 41.2, 41.62, 41.72, 42.6, 43.48, 44.2, 46.6, 47.9, 49.9, 50.4, 50.6, 50.8, 52.0]
def comp(g, W=720, H=1280):
    p, d = base.frame_path(g)
    im = np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS))
    return I.over(im, g)
if __name__ == "__main__":
    times = [float(a) for a in sys.argv[2:]] or TIMES
    out = sys.argv[1] if len(sys.argv) > 1 else "strip.png"
    cols = 6; cw, ch = 720, 520
    rows = (len(times) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cw, rows * (ch + 34)), (16, 16, 20))
    dr = ImageDraw.Draw(sh); f = ImageFont.truetype(base.PROJ + "/fonts/WorkSans-Black.ttf", 24)
    for i, t in enumerate(times):
        g = int(round(t * 24))
        im = Image.fromarray(comp(g)).crop((0, 0, cw, ch))
        x, y = (i % cols) * cw, (i // cols) * (ch + 34)
        sh.paste(im, (x, y + 34)); dr.text((x + 8, y + 3), "%.2f s  f%d  %s" % (g / 24.0, g, base.shot_of(g)), font=f, fill=(255, 220, 90))
    sh.save(out); print(out, sh.size)
