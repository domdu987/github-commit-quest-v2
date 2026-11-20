import sys, glob, numpy as np
from PIL import Image
def luma(f): return float(np.asarray(Image.open(f).convert('RGB').resize((90, 160), Image.BILINEAR), float).mean())
if __name__ == '__main__':
    fs = sorted(glob.glob('frames/g_*.png')); v = [luma(f) for f in fs]
    print(len(v), 'frames g%s-g%s' % (fs[0][-8:-4], fs[-1][-8:-4]), 'mean %.1f min %.1f max %.1f' % (np.mean(v), min(v), max(v)))
    print(' '.join('%s:%.0f' % (f[-8:-4], x) for f, x in list(zip(fs, v))[::3]))
