"""sheet.py -- sheet.png: every icon in its key states (active size, 2.4 px per unit = 2.1x film size), dark and bright."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import icons13 as I
T = I.T
S = [("radio", I.radio, [(0.6, "voice"), (T.R_WAIT + 0.08, "jitter"), (T.R_HEY + 0.08, "jitter, red"), (T.R_CUT + 0.05, "cut: static"),
                         (T.R_CUT + 0.4, "flat line + cut mark"), (4.8, "silent (grey)"), (9.0, "quiet status")]),
     ("battery", I.battery, [(16.1, "empty"), (16.36, "1"), (16.56, "2"), (16.75, "3 + burst"), (17.2, "full"), (20.0, "quiet status")]),
     ("calls", I.phone, [(T.P_IN + 0.15, "buzz"), (T.P1 + 0.1, "1"), (T.P3 + 0.1, "3"), (T.P4 + 0.08, "4 + burst"), (20.4, "4"),
                         (T.P_NAME + 0.2, "badge to tag"), (21.7, "name tag"), (25.0, "quiet status")]),
     ("trust", I.heart, [(23.0, "82 %"), (26.0, "60 %"), (27.0, "52 %"), (T.H_CRACK + 0.06, "crack"), (28.8, "28 %"), (31.3, "7 %"),
                         (31.95, "empty, grey"), (T.H_SPLIT + 0.12, "split"), (35.0, "quiet status")]),
     ("danger", I.danger, [(34.5, "calm"), (37.3, "22 %"), (39.2, "faster, turning"), (41.2, "amber, fast"), (T.D_EYE - 0.06, "lid"),
                           (T.D_EYE + 0.07, "snaps open"), (42.6, "red eye"), (T.D_LUNGE + 0.05, "lunge flash"), (45.0, "quiet status")]),
     ("countdown", I.stopwatch, [(47.2, "60"), (T.C_T0 + 1.08, "tick"), (48.4, "59"), (50.0, "57"), (50.42, "to the mark"), (50.56, ""),
                                 (50.76, "title hit"), (52.0, "title mark")])]
U, CW, CH = 2.4, 250, 180                                                    # px per unit, cell in units

def cell(fn, name, t, bg, quiet):
    act = 0.0 if quiet else 1.0
    if name == "countdown":
        mm = I.eio(I.u(t, T.C_MORPH, T.TITLE - I.F))
        body, ext = fn(t, act, mm)
        body += I.burst(t, T.TITLE, 12, 46, 70, I.AMBER, 5, dur=10 * I.F, rot=15, cy=4)
        sc = 1 + 0.5 * mm
    else:
        body, ext = fn(t, act)
        sc = 1.0
    sc *= 0.7 if quiet else 1.0
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="-70 -94 %d %d">%s<g filter="url(#kl)"><g transform="scale(%.3f)">%s</g></g></svg>'
           % (CW * U, CH * U, CW, CH, I.DEFS.replace('radius="%.2f"' % I.KEY, 'radius="%.2f"' % (I.KEY / 1.12)), sc, body))
    return Image.fromarray(I.raster(svg, int(CW * U), int(CH * U), bg)).convert("RGB")

if __name__ == "__main__":
    cols = max(len(s[2]) for s in S)
    w, h = int(CW * U), int(CH * U)
    sh = Image.new("RGB", (cols * w, len(S) * 2 * h), (20, 20, 24))
    dr = ImageDraw.Draw(sh); f = ImageFont.truetype(I.PROJ + "/fonts/Kanit_900Black.ttf", 26)
    for r, (name, fn, states) in enumerate(S):
        for b, bg in enumerate(("#141b36", "#e7e0d0")):
            for c, (t, lab) in enumerate(states):
                im = cell(fn, name, t, bg, lab == "quiet status")
                x, y = c * w, (r * 2 + b) * h
                sh.paste(im, (x, y))
                dr.text((x + 10, y + 6), "%s  %.2f s  %s" % (name, t, lab), font=f, fill=(255, 214, 90) if b == 0 else (40, 40, 60))
    sh.save("sheet.png"); print(sh.size)
