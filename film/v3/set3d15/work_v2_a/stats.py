"""stats.py : qa_stats2.py metrics on a still (same maths on a 90x160 frame: sat = mean (mx-mn)/(mx+1e-3), vivid = sat>0.5 share, luma = mean of channels, 0..255),
plus shade hue / magenta share from set15_hue.py.  usage: python3 stats.py a.png b.png ..."""
import sys, os, numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import set15_hue as H
def stats(p):
    im = Image.open(p).convert('RGB').resize((90, 160), Image.BILINEAR); a = np.asarray(im, np.float32)
    mx = a.max(-1); mn = a.min(-1); sp = (mx - mn) / (mx + 1e-3); g = a.mean(-1)
    hh, _, _ = H.stats([p]); sh, _ = H.shade_hue(p)
    return dict(sat=float(sp.mean()), vivid=float((sp > 0.5).mean() * 100), luma=float(g.mean()), shade_hue=float(sh), magenta=float(hh['magenta']))
if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = stats(p); print('%-34s sat %.3f vivid %5.1f luma %5.1f shade_hue %5.1f magenta %4.1f' % (os.path.basename(p), s['sat'], s['vivid'], s['luma'], s['shade_hue'], s['magenta']))
