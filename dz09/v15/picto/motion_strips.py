"""motion_strips.py -- motion_strips.png: 10 consecutive film frames of the 8 biggest events, 1:1 (720-wide reference), dark background."""
import os
from PIL import Image, ImageDraw, ImageFont
import picto15 as P
T = P.T
fr = lambda t: int(round(t * 24))
EV = [("radio cut  (T.R_CUT 3.243)", fr(T.R_CUT) - 1, 36), ("battery cell 3  (T.B3 16.70)", fr(T.B3) - 3, 292), ("badge 4  (T.P4)", fr(T.P4) - 1, 36),
      ("heart drain 82 -> 60 %  (T.H_CASE), every 2nd frame", fr(T.H_CASE) + 1, 36), ("heart split  (32.05)", fr(T.H_SPLIT) - 2, 36), ("eye opens  (T.D_EYE 41.657)", fr(T.D_EYE) - 4, 36),
      ("lunge  (T.D_LUNGE 43.445, flash frame g 1045)", 1041, 36), ("stopwatch flip 60 -> 59  (47.78)", fr(T.C_T0 + 1) - 2, 36)]
VW, VH, N = 400, 250, 10
f = ImageFont.truetype(os.path.join(P.PROJ, "fonts", "WorkSans-Black.ttf"), 15)
S = Image.new("RGB", (N * VW, len(EV) * (VH + 22)), (8, 8, 12)); d = ImageDraw.Draw(S)
for r, (lab, g0, x0) in enumerate(EV):
    step = 2 if "every 2nd" in lab else 1
    for i in range(N):
        g = g0 + i * step
        svg, _ = P.frame_svg(g / 24.0, VW, VH, "916", view=(x0 - 36, 60, VW, VH))
        im = Image.new("RGB", (VW, VH), (16, 18, 33)) if svg is None else Image.fromarray(P.raster(svg, VW, VH, bg="#101221")).convert("RGB")
        S.paste(im, (i * VW, r * (VH + 22) + 22))
        d.text((i * VW + 6, r * (VH + 22) + 3), ("%s   " % lab if i == 0 else "") + "g %d" % g, font=f, fill=(255, 205, 90))
S.save(os.path.join(P.HERE, "motion_strips.png")); print(S.size)
for r in range(len(EV)):
    for h in range(2):
        S.crop((h * 5 * VW, r * (VH + 22), (h + 1) * 5 * VW, (r + 1) * (VH + 22))).save(os.path.join(P.HERE, "tmp", "ms_%d_%d.png" % (r, h)))
P.close()
