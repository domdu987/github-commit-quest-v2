"""layer.py -- gauges -> RGBA frames through the persistent Chromium page (raster.py), composited with PIL.

    L = Layer(gauges, W, H)                 # W x H = the output frame; gauge positions are 720-short-side reference px
    im = L.image(t)                         # PIL RGBA (W x H) or None; identical SVGs are served from a small cache
    L.over(frame_rgb_or_rgba, t)            # alpha-composite onto a PIL image (returns RGBA)
    L.safe_report(t0, t1)                   # frames where a gauge leaves the safe area or touches the caption band
    close()
"""
import os, sys, hashlib, tempfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("gauge_raster", os.path.join(HERE, "raster.py"))
raster = _iu.module_from_spec(_sp); _sp.loader.exec_module(raster)
import gauge as G

# safe areas in fractions of the frame: (x0, y0, x1, y1) and the caption band (y0, y1)
SAFE = {"9:16": (0.05, 0.10, 0.85, 0.80), "16:9": (0.04, 0.06, 0.96, 0.90)}
CAPTION = {"9:16": (860 / 1280.0, 1010 / 1280.0), "16:9": (484 / 720.0, 568 / 720.0)}


class Layer(object):
    def __init__(self, gauges, W, H, tmp=None):
        self.gauges, self.W, self.H = list(gauges), W, H
        self.tmp = tmp or tempfile.mkdtemp(prefix="gauge_")
        os.makedirs(self.tmp, exist_ok=True)
        self._last = (None, None)

    def image(self, t):
        svg = G.frame_svg(self.gauges, t, self.W, self.H)
        if svg is None:
            return None
        h = hashlib.sha1(svg.encode("utf8")).hexdigest()[:16]
        if self._last[0] == h:
            return self._last[1]
        p = os.path.join(self.tmp, "g_%s.png" % h)
        raster.render([{"svg": svg, "w": self.W, "h": self.H, "out": p}])
        im = Image.open(p).convert("RGBA"); im.load()
        os.remove(p)
        self._last = (h, im)
        return im

    def over(self, frame, t):
        im = frame.convert("RGBA")
        lay = self.image(t)
        if lay is not None:
            im.alpha_composite(lay)
        return im

    def safe_report(self, fps=24, nf=1280):
        asp = "9:16" if self.H >= self.W else "16:9"
        k = min(self.W, self.H) / G.REF
        sx0, sy0, sx1, sy1 = SAFE[asp]; c0, c1 = CAPTION[asp]
        out, mx = [], 0
        for g in range(nf):
            t = g / float(fps)
            vis = [q for q in self.gauges if q.visible(t)]
            mx = max(mx, len([q for q in vis if q.kind == "tube"]))
            for q in vis:
                x0, y0, x1, y1 = [v * k for v in q.bbox()]
                bad = []
                if x0 < sx0 * self.W or x1 > sx1 * self.W or y0 < sy0 * self.H or y1 > sy1 * self.H: bad.append("safe area")
                if y1 > c0 * self.H and y0 < c1 * self.H: bad.append("caption band")
                if bad and not any(o[0] == q.id for o in out):
                    out.append((q.id, g, "+".join(bad), tuple(round(v) for v in (x0, y0, x1, y1))))
        return {"problems": out, "max_tubes_at_once": mx}


def close():
    raster.close()
