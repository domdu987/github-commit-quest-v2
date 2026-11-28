"""flat9_measure.py -- the refE_measure sampling on our flat-mode v9 frames -> out/flat9/measure.json"""
import numpy as np, colorsys, json, os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
S = {"s06": dict(face=(324, 400), cloth=(250, 575), crew_face=(691, 583), wall=(520, 216)),
     "s13": dict(face=(400, 520), cloth=(371, 756), wall=(630, 972)),
     "s20": dict(face=(395, 640), cloth=(350, 730), wall=(120, 250)),
     "cal": dict(face=(400, 540), cloth=(371, 700), wall=(630, 972))}
out = {}
for k, d in S.items():
    im = np.asarray(Image.open(H + "/out/flat9/%s_916.png" % k).convert("RGB")).astype(float) / 255
    L = im @ [0.2126, 0.7152, 0.0722]
    r = dict(frame_L_mean=round(float(L.mean()), 3), frame_L_med=round(float(np.median(L)), 3))
    for n, (x, y) in d.items():
        w = im[y - 15:y + 16, x - 15:x + 16].reshape(-1, 3); l = w @ [0.2126, 0.7152, 0.0722]
        p = np.median(w[l >= np.percentile(l, 55)], 0)
        h, s, v = colorsys.rgb_to_hsv(*p)
        r[n] = dict(rgb=[int(round(c * 255)) for c in p], L=round(float(p @ [0.2126, 0.7152, 0.0722]), 3), hue=round(h * 360), sat=round(s, 3))
    out[k] = r; print(k, json.dumps(r))
json.dump(out, open(H + "/out/flat9/measure.json", "w"), indent=1)
