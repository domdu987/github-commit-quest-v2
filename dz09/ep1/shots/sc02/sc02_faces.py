"""sc02_faces.py -- the turned junior's SNARL for scene 02 (director's note on the first draft: in S049 he "grins with fangs
and may read comic, he must read frightening: open snarl, white eyes, no smile").

draw8's `snarl` / `bite` mouths are a D shape (flat top, round bottom: the shape of a laugh) with a pink tongue and two
fangs, which reads as a grin.  This adds, WITHOUT changing any existing expression (several workers share a process, so an
existing expression must draw the same whatever shot ran before):
    mouth kind  "snarl_z"   an arch: the upper lip pulled UP in the middle, the corners pulled DOWN, the lower lip dropped;
                            black-red inside, a jagged upper and lower row of teeth, no tongue; snarl creases at the corners
    expressions "z_snarl"   white snapped eyes (z_snap: veins, red pin pupils), brows hard down at the nose, snarl_z
                "z_snarl_o" the same, mouth wider open (the moment the head comes up)
Import and call install() in a shot module and list this file in the module's DEPS.
"""
import os, sys, math
import epcommon as E
for _p in (os.path.join(E.EP1, "cast"),):
    if _p not in sys.path: sys.path.insert(0, _p)
if os.path.join(E.PROJ, "v8", "cast") not in sys.path:
    sys.path.append(os.path.join(E.PROJ, "v8", "cast"))
import draw9 as D9                                         # (puts nothing on sys.path itself: v8/cast is appended above)
import draw8 as D8

FILE = os.path.abspath(__file__)
TEETH = "#ece6d2"
INSIDE = "#24070a"
GUM = "#7c1c22"


def _f(v):
    return D8.f(v) if hasattr(D8, "f") else ("%.4f" % v)


def snarl_svg(x, y, W, amt, ink):
    """W = mouth width scale (draw8's mouth_w x foreshortening), amt 0..1 = how far open."""
    hw = W * 0.62
    up = 0.030 + 0.040 * amt                                  # the middle of the upper lip above the corners
    dn = 0.060 + 0.085 * amt                                  # the lower lip below the corners
    cy = y + 0.035                                            # the corners
    f = _f
    d = "M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z" % (
        f(x - hw), f(cy),
        f(x - hw * 0.70), f(cy - up * 1.25), f(x + hw * 0.70), f(cy - up * 1.25), f(x + hw), f(cy),
        f(x + hw * 0.55), f(cy + dn * 1.05), f(x - hw * 0.55), f(cy + dn * 1.05), f(x - hw), f(cy))
    cid = "sz%d" % (abs(hash((round(x, 3), round(y, 3), round(W, 3), round(amt, 3)))) % 99999)
    o = '<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d)
    o += D8.path(d, INSIDE)
    body = ""
    # gums, then a jagged upper row (two long fangs), a jagged lower row
    top = cy - up * 0.95
    body += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x - hw), f(top - 0.03), f(2 * hw), f(0.045), GUM)
    n = 7
    pts = [(x - hw, top - 0.02)]
    for i in range(n + 1):
        xx = x - hw + 2 * hw * i / n
        pts.append((xx, top + 0.022))
        if i < n:
            long_ = i in (1, n - 2)
            pts.append((xx + hw / n, top + (0.075 if long_ else 0.045) * (0.6 + 0.4 * amt)))
    pts.append((x + hw, top - 0.02))
    body += D8.path(D8.pts_d(pts), TEETH)
    bot = cy + dn * 0.80
    pts = [(x - hw, bot + 0.04)]
    m = 6
    for i in range(m + 1):
        xx = x - hw * 0.8 + 1.6 * hw * i / m
        pts.append((xx, bot))
        if i < m:
            pts.append((xx + 0.8 * hw / m, bot - 0.035 * (0.6 + 0.4 * amt)))
    pts.append((x + hw, bot + 0.04))
    body += D8.path(D8.pts_d(pts), TEETH)
    o += '<g clip-path="url(#%s)">%s</g>' % (cid, body)
    o += D8.path(d, "none", ink, 0.030)
    # snarl creases: down and out of each corner, and two short marks over the upper lip
    for sd in (-1, 1):
        o += D8.line((x + sd * (hw + 0.012), cy - 0.005), (x + sd * (hw + 0.045), cy + 0.050), ink, 0.020)
        o += D8.line((x + sd * hw * 0.30, cy - up * 1.25 - 0.035), (x + sd * hw * 0.55, cy - up * 1.25 - 0.010), ink, 0.016)
    return o


_installed = False


def install():
    global _installed
    if _installed:
        return
    m0 = D9._mouth9

    def mouth(kind, amt, x, y, fs, sp, level=None, shape="a", ink=D9.INK, s=1):
        if kind == "snarl_z":
            W = sp["face"]["mouth_w"] * max(fs, 0.45)
            return snarl_svg(x, y, W * 1.15, amt, ink)
        return m0(kind, amt, x, y, fs, sp, level=level, shape=shape, ink=ink, s=s)

    D9._mouth9 = mouth
    D8.EXPR.setdefault("z_snarl", dict(eyes="z_snap", brows=(34, -0.035), mouth=("snarl_z", 0.65)))
    D8.EXPR.setdefault("z_snarl_o", dict(eyes="z_snap", brows=(34, -0.035), mouth=("snarl_z", 1.0)))
    _installed = True
