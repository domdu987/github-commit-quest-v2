"""sheet.py -- sheet.png: every pictogram's key states, 1.2x film size (720-wide reference), on a dark and on a light background."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import picto15 as P
T = P.T
ROWS = [("radio", [("0.25 pop-in", 0.25), ("1.2 voice", 1.2), ("2.25 amber jitter", 2.25), ("2.75 red", 2.75), ("3.33 shatter", 3.33), ("3.55 slash", 3.55), ("4.2 draining", 4.2), ("5.6 dead", 5.6)]),
        ("battery", [("15.98 drops in", 15.98), ("16.25 cell 1 flying", 16.25), ("16.33 cell 1", 16.33), ("16.54 cell 2", 16.54), ("16.72 cell 3", 16.72), ("16.85 bolt", 16.85), ("17.05 hop", 17.05), ("17.4 full", 17.4)]),
        ("calls", [("17.62 pop-in + battery aside", 17.62), ("17.84 badge 1", 17.84), ("18.3 badge 2", 18.3), ("18.72 badge 3", 18.72), ("19.17 badge 4", 19.17), ("20.0 ringing", 20.0), ("21.0", 21.0), ("21.95 hand-over", 21.95)]),
        ("trust", [("22.3 82 %", 22.3), ("25.4 draining", 25.4), ("26.9 52 %", 26.9), ("28.0 crack", 28.0), ("29.6 17 %", 29.6), ("31.2 7 %", 31.2), ("31.95 empty", 31.95), ("32.15 split", 32.15), ("32.9 halves drop", 32.9)]),
        ("danger", [("33.75 pop-in", 33.75), ("34.4 beat 1", 34.4), ("36.6", 36.6), ("38.9 weak, turning", 38.9), ("40.9 last beat", 40.9), ("41.3 flat", 41.3), ("41.56 shutting", 41.56), ("41.63 lid", 41.63)]),
        ("danger (eye)", [("41.70 snaps open", 41.70), ("41.83 darts left", 41.83), ("42.1 darts right", 42.1), ("42.9 locked, veins", 42.9), ("43.40 squint", 43.40), ("43.50 lunge", 43.50), ("43.542 FLASH frame", 1045 / 24.0), ("43.63", 43.63), ("44.6 drips", 44.6)]),
        ("countdown", [("46.5 pop-in", 46.5), ("47.2 60", 47.2), ("47.80 flip", 47.80), ("48.4 59", 48.4), ("49.82 flip 57", 49.82), ("50.1 57", 50.1), ("50.34 flight", 50.34), ("50.5 flight", 50.5)])]
SC = 1.2
VW, VH = 420, 250
CW, CH = int(VW * SC), int(VH * SC)
COLS = 9
f = ImageFont.truetype(os.path.join(P.PROJ, "fonts", "WorkSans-Black.ttf"), 15)
BG = [("#101221", (16, 18, 33)), ("#d9d6cb", (217, 214, 203))]
S = Image.new("RGB", (COLS * CW, len(ROWS) * 2 * (CH + 22)), (8, 8, 12)); d = ImageDraw.Draw(S)
for r, (name, sts) in enumerate(ROWS):
    for b, (bg, rgb) in enumerate(BG):
        for i, (lab, t) in enumerate(sts):
            view = (0, 60, VW, VH)
            if name == "countdown" and t > T.C_MORPH:
                view = (0, 60, VW * 1.6, VH * 1.6)
            svg, _ = P.frame_svg(t, CW, CH, "916", view=view)
            x, y = i * CW, (r * 2 + b) * (CH + 22)
            if svg is None:
                im = Image.new("RGB", (CW, CH), rgb)
            else:
                im = Image.fromarray(P.raster(svg, CW, CH, bg=bg)).convert("RGB")
            S.paste(im, (x, y + 22))
            d.text((x + 6, y + 3), "%s  %s" % (name, lab), font=f, fill=(255, 205, 90))
S.save(os.path.join(P.HERE, "sheet.png")); print(S.size)
P.close()
