"""stills_sheet.py -- final-tier stills with the v13 icon strip and the Ohm captions on them, as one sheet (2 rows x 3).

    python3 run.py --shots S01,S06,S13,S18,S23 --at 0.5 --tier final --size 720x1280 --tag v3
    python3 run.py --shots S20 --at 0.8 --tier final --size 720x1280 --tag v3
    python3 stills_sheet.py --tag v3 --out v3_stills_720.png
"""
import os, sys, glob, argparse, subprocess
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import common as C, finish as FN

ap = argparse.ArgumentParser(); ap.add_argument("--tag", default="v3"); ap.add_argument("--out", default="v3_stills_720.png")
ap.add_argument("--size", default="720x1280"); ap.add_argument("--tier", default="final"); ap.add_argument("--cols", type=int, default=3)
a = ap.parse_args()
W, H = [int(x) for x in a.size.split("x")]
d = os.path.join(HERE, "out", "%s_%dx%d" % (a.tier, W, H), "stills_" + a.tag)
tmp = os.path.join(d, "comp"); os.makedirs(tmp, exist_ok=True)
ims = []
for p in sorted(glob.glob(os.path.join(d, "S??_f????.png"))):
    sid = os.path.basename(p)[:3]; g = int(os.path.basename(p)[5:9]) - 1; t = g / float(C.FPS)
    im = FN.icons_over(Image.open(p), g)                    # v13 flat strip, drawn at the still's size
    q = os.path.join(tmp, os.path.basename(p)); im.save(q)
    o = q[:-4] + "_cap.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(C.FPS), "-i", q, "-vf",
                    "setpts=PTS+%.4f/TB,ass=%s:fontsdir=%s" % (t + 0.001, FN.ass_path(), C.FONTS), "-frames:v", "1", o], check=True)
    ims.append((sid, g, Image.open(o).convert("RGB")))
FN.icons().close()
cols = a.cols; rows = (len(ims) + cols - 1) // cols; lab = 34
S = Image.new("RGB", (cols * (W + 8), rows * (H + lab + 8)), (14, 14, 18)); dr = ImageDraw.Draw(S); f = FN.font(C.WORKS, 22)
for i, (sid, g, im) in enumerate(ims):
    x = (i % cols) * (W + 8); y = (i // cols) * (H + lab + 8)
    S.paste(im, (x, y + lab)); dr.text((x + 6, y + 5), "%s  %.2fs  f%d  %s tier %dx%d" % (sid, g / float(C.FPS), g, a.tier, W, H), font=f, fill=(232, 232, 236))
out = a.out if os.path.isabs(a.out) else os.path.join(HERE, a.out)
S.save(out); print("wrote", out, S.size)
