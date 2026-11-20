"""r2measure.py : numbers for round 2.   usage: r2measure.py caption <dir> | diff <dir> (needs sNN_0.png, sNN_1.png) | heads (builds every shot, prints head rows) """
import sys, os, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def caption(d, names):
    out = {}
    for n in names:
        im = np.asarray(Image.open(os.path.join(d, n + '.png')).convert('RGB'), 'float32'); H = im.shape[0]; k = H / 1280.0
        band = im[int(880 * k):int(950 * k)]; y = 0.2126 * band[..., 0] + 0.7152 * band[..., 1] + 0.0722 * band[..., 2]; v = band.max(-1) / 255
        out[n] = dict(mean=round(float(y.mean()), 1), bright200=round(float((y > 200).mean() * 100), 2), v70_px=int((v > 0.7).sum() / (k * k)), peak=int(y.max()))
    return out
def diff(d, names):
    out = {}
    for n in names:
        a = np.asarray(Image.open(os.path.join(d, n + '_0.png')).convert('L'), 'float32'); b = np.asarray(Image.open(os.path.join(d, n + '_1.png')).convert('L'), 'float32')
        df = np.abs(a - b); out[n] = dict(mean=round(float(df.mean()), 2), frac_gt20=round(float((df > 20).mean() * 100), 1))
    return out
if __name__ == '__main__':
    cmd, d = sys.argv[1], sys.argv[2]; names = sys.argv[3:] or ['s%02d' % i for i in range(1, 27)]
    r = caption(d, names) if cmd == 'caption' else diff(d, names)
    for k, v in r.items(): print(k, v)
