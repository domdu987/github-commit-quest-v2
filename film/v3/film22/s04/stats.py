import sys, glob, os, numpy as np
from PIL import Image
import colorsys
d = sys.argv[1]
fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))
S = []; Vv = []; Lm = []; T3 = []; HS = []; MG = []
for f in fs:
    a = np.asarray(Image.open(f).convert('RGB').resize((90, 160)), dtype=np.float32)
    mx = a.max(-1); mn = a.min(-1); sat = (mx - mn) / (mx + 1e-3)
    S.append(sat.mean()); Vv.append((sat > 0.5).mean()); lum = a.mean(-1); Lm.append(lum.mean()); T3.append(lum[:53].mean())
    # shade hue: dark-ish pixels hue
    hsv = np.array([colorsys.rgb_to_hsv(*(p / 255)) for p in a.reshape(-1, 3)[::7]])
    dark = hsv[(hsv[:, 2] < 0.45) & (hsv[:, 1] > 0.25)]
    h = np.median(dark[:, 0]) * 360 if len(dark) else -1; HS.append(h)
    magenta = ((hsv[:, 0] > 0.80) & (hsv[:, 0] < 0.92) & (hsv[:, 1] > 0.4)).mean(); MG.append(magenta)
print('frames', len(fs), 'sat %.3f vivid %.1f%% luma %.1f top3 %.1f shade-hue-in-band %.0f%% median %.0f magenta %.1f%%' % (np.mean(S), np.mean(Vv) * 100, np.mean(Lm), np.mean(T3), 100 * np.mean([(240 <= h <= 260) for h in HS]), np.median(HS), np.mean(MG) * 100))
for f, s, v, l, h in zip(fs, S, Vv, Lm, HS): print(os.path.basename(f)[2:6], 'sat %.2f vivid %.0f luma %.0f hue %.0f' % (s, v * 100, l, h))
