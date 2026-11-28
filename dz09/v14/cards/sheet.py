"""sheet.py -- sheet.png: every card state 1:1 (720-wide scale) on a dark background (some cells light), chips, and the
two panel alternatives A / B on the same film frames.  contrast.png: the cards on the darkest and brightest shots."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cards14 as C
sys.path.insert(0, os.path.join(C.PROJ, "v10", "film"))
import finish as FN


class _None(object):                                       # finish.py's comp without any status layer
    @staticmethod
    def over(rgb, g, aspect=None):
        return rgb


FN._IC["m"] = _None
base = FN.base_dir("draft", 360, 640)
STATES = [("radio 1.20 on air", 1.2), ("radio 3.29 glitch (3 frames)", 3.29), ("radio 3.60 cut", 3.6),
          ("battery 16.10", 16.1), ("battery 16.48", 16.48), ("battery 16.68", 16.68), ("battery 17.10 full", 17.1),
          ("calls 17.70", 17.70), ("calls 18.50 (chip: battery)", 18.5), ("calls 19.60", 19.6), ("calls 20.90", 20.9), ("calls 21.60", 21.6),
          ("trust 22.60 (chip: calls)", 22.6), ("trust 26.00", 26.0), ("trust 28.50", 28.5), ("trust 31.00", 31.0), ("trust 32.04 hung up", 32.04), ("trust 32.90 split", 32.9),
          ("danger 36.00", 36.0), ("danger 39.50", 39.5), ("danger 42.00", 42.0), ("danger 43.46 lunge flash (1 frame)", 43.46), ("danger 44.50", 44.5),
          ("countdown 46.70", 46.7), ("countdown 47.80 pulse", 47.80), ("countdown 50.10", 50.1), ("radio 5.80 quiet", 5.8)]
CW, CHH, COLS = 500, 270, 3
rows = (len(STATES) + COLS - 1) // COLS
ALT = [("S18 f864 (dark)", 864, 864), ("S14 f672 (headlights)", 672, 672)]
S = Image.new("RGB", (COLS * CW, rows * CHH + 40 + len(ALT) * 470), (16, 18, 30))
d = ImageDraw.Draw(S)
f = ImageFont.truetype(os.path.join(C.PROJ, "fonts", "WorkSans-Black.ttf"), 15)
for i, (lab, t) in enumerate(STATES):
    g = int(round(t * 24))
    o = C.overlay(g, 720, 1280)[36:36 + CHH - 24, 0:CW].astype(np.float32)
    x, y = (i % COLS) * CW, (i // COLS) * CHH
    bg = np.zeros((CHH - 24, CW, 3), np.float32) + np.float32([16, 18, 30])
    if (i // COLS) % 2 == 1 and i % COLS == 2:
        bg[:] = np.float32([215, 215, 205])                                # one light cell per second row
    a = o[..., 3:4] / 255.0
    S.paste(Image.fromarray((bg * (1 - a) + o[..., :3] * a).astype(np.uint8)), (x, y + 24))
    d.text((x + 8, y + 4), lab + "   f%d" % g, font=f, fill=(200, 205, 215))
y0 = rows * CHH + 10
d.text((8, y0), "PANEL ALTERNATIVES on the same film frame:  A = navy tag + stencil tab (used in demo.mp4)   |   B = rescue-orange header band on navy (28 px taller)", font=f, fill=(255, 190, 60))
for r, (lab, gf, gc) in enumerate(ALT):
    fr = np.asarray(FN.comp_frame(base, gf, 720, 1280).convert("RGB"))
    for k, sty in enumerate("AB"):
        C.STYLE = sty
        im = Image.fromarray(C.over(fr, gc)).crop((0, 0, 720, 440))
        S.paste(im, (20 + k * 740, y0 + 30 + r * 470)); d.text((28 + k * 740, y0 + 34 + r * 470), "%s   %s" % (sty, lab), font=f, fill=(255, 255, 255))
C.STYLE = "A"
S.save(os.path.join(C.HERE, "sheet.png")); print(S.size)
# contrast: darkest and brightest shots (film frame, card frame); shots without a card of their own borrow one
CON = [("S02 f100", 100, 100), ("S04 f200 (card borrowed)", 200, 864), ("S18 f880", 880, 880), ("S19 f940", 940, 940),
       ("S08 f386", 386, 386), ("S14 f672", 672, 672), ("S09 f410", 410, 410), ("S16 f760", 760, 760), ("S24 f1180", 1180, 1180)]
K = Image.new("RGB", (3 * 724, 3 * 444), (0, 0, 0)); dk = ImageDraw.Draw(K)
for i, (lab, gf, gc) in enumerate(CON):
    fr = np.asarray(FN.comp_frame(base, gf, 720, 1280).convert("RGB"))
    K.paste(Image.fromarray(C.over(fr, gc)).crop((0, 0, 720, 440)), ((i % 3) * 724, (i // 3) * 444)); dk.text(((i % 3) * 724 + 8, (i // 3) * 444 + 6), lab, font=f, fill=(255, 255, 255))
K.save(os.path.join(C.HERE, "contrast.png")); print(K.size)
