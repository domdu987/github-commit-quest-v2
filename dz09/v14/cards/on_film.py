"""on_film.py -- on_film.png: 12 moments over clean draft frames (out/draft_360x640 scaled to 720x1280, finish.py's own comp with the card layer)."""
import os, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cards14 as C
sys.path.insert(0, os.path.join(C.PROJ, "v10", "film"))
import finish as FN
FN._IC["m"] = C                                            # the one-line switch, done from outside (finish.py is not edited)
base = FN.base_dir("draft", 360, 640)
TS = [2.0, 4.5, 16.6, 18.5, 20.5, 26.0, 31.9, 36.0, 42.0, 43.6, 47.5, 50.9]
S = Image.new("RGB", (6 * 724, 2 * 1310), (14, 14, 18)); d = ImageDraw.Draw(S)
f = ImageFont.truetype(os.path.join(C.PROJ, "fonts", "WorkSans-Black.ttf"), 20)
for i, t in enumerate(TS):
    g = int(round(t * 24))
    im = FN.comp_frame(base, g, 720, 1280)
    x, y = (i % 6) * 724, (i // 6) * 1310
    S.paste(im, (x, y + 30)); d.text((x + 6, y + 4), "%.1f s  f%d  %s" % (t, g, C.shot_of(g)), font=f, fill=(230, 230, 236))
    im.crop((0, 0, 720, 520)).save(os.path.join(C.HERE, "tmp", "top_%02d.png" % i))
S.save(os.path.join(C.HERE, "on_film.png")); print(S.size)
