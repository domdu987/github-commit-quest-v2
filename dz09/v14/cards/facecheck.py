"""facecheck.py -- tmp/faces_*.png: top 320 px of the frame every 0.5 s while a card is up (card over the clean draft), for the face check."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import cards14 as C
sys.path.insert(0, os.path.join(C.PROJ, "v10", "film"))
import finish as FN
FN._IC["m"] = C
base = FN.base_dir("draft", 360, 640)
ts = [x / 2.0 for x in range(1, 14)] + [16 + x / 2.0 for x in range(0, 35)] + [34 + x / 2.0 for x in range(0, 34)]
def sheet(ts, name, cols=6, hcrop=320, sc=0.5):
    w, h = int(720 * sc), int(hcrop * sc)
    S = Image.new("RGB", (cols * w, ((len(ts) + cols - 1) // cols) * (h + 16)), (0, 0, 0)); d = ImageDraw.Draw(S)
    for i, t in enumerate(ts):
        g = int(round(t * 24)); im = FN.comp_frame(base, g, 720, 1280).crop((0, 0, 720, hcrop)).resize((w, h), Image.LANCZOS)
        x, y = (i % cols) * w, (i // cols) * (h + 16); S.paste(im, (x, y + 16)); d.text((x + 3, y + 2), "%.2f %s f%d" % (t, C.shot_of(g), g), fill=(255, 255, 255))
    S.save(os.path.join(C.HERE, "tmp", name))
sheet(ts[:42], "faces_0.png"); sheet(ts[42:], "faces_1.png")
tr = [17.25 + i / 24.0 for i in range(0, 12)] + [21.70 + i / 24.0 for i in range(0, 12)] + [50.18 + i / 24.0 for i in range(0, 12, 1)] + [6.38 + i / 24.0 for i in range(0, 9)] + [3.2 + i / 24.0 for i in range(0, 3)]
sheet(tr, "trans.png", cols=6, hcrop=420)
