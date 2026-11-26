"""gauge.py -- DEAD ZONE 09 gauge tubes: glossy glass meter tubes drawn as SVG (pure Python, no bpy), one family for
every on-screen graphic.  A gauge is a pure function of film time t.  See API.md.

    tr = Track(0.6, [(24.9, 0.55, "ramp"), (28.25, 0.24, "hit")])
    g  = Gauge("trust", tr, t_in=22.3, t_out=33.25, x=100, y=470, picto="heart", label="เชื่อใจ")
    svg = frame_svg([g], t, W, H)          # full-frame transparent SVG, or None when nothing is visible
"""
import math, base64, os

INK = "#1f1d24"          # the cast's line colour (v4/iconfx, v8/cast)
RIM = "#f4f1ea"          # off-white sticker rim, keeps the dark line readable on night backgrounds
GREEN, LIME, AMBER, ORANGE, RED = (40, 208, 104), (176, 222, 44), (255, 190, 26), (255, 122, 32), (238, 44, 54)
REF = 720.0              # positions are given for a frame whose SHORT side is 720 px


def f(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def mix(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


def rgb(c, a=None):
    c = [int(round(clamp(v, 0, 255))) for v in c]
    return "#%02x%02x%02x" % tuple(c) if a is None else "rgba(%d,%d,%d,%s)" % (c[0], c[1], c[2], f(a))


def ramp_color(bad):
    """badness 0..1 -> green, amber, red."""
    bad = clamp(bad)
    st = [(0.0, GREEN), (0.3, LIME), (0.55, AMBER), (0.78, ORANGE), (1.0, RED)]
    for (a0, c0), (a1, c1) in zip(st, st[1:]):
        if bad <= a1:
            return mix(c0, c1, (bad - a0) / (a1 - a0))
    return RED


def hash01(*k):
    x = math.sin(sum((i + 1) * 12.9898 * float(v) for i, v in enumerate(k))) * 43758.5453
    return x - math.floor(x)


# ------------------------------------------------------------------------------------------------ value over time
class Track(object):
    """value 0..1 over film seconds.  keys = [(t, v, kind[, kick])], kind:
       "ramp": glide linearly from the previous key to v, arriving at t (a slow drain or rise; shows a small arrow)
       "hit" : hold, then change to v AT t with a spring (overshoot + settle), flash, shake, droplets, arrow + delta
               number.  kick (0..1) forces the size of the fanfare, e.g. a hit that keeps the value (1.0 -> 1.0)."""

    def __init__(self, v0, keys=()):
        self.v0 = float(v0)
        self.keys = sorted([(k[0], float(k[1]), k[2], (k[3] if len(k) > 3 else None)) for k in keys], key=lambda k: k[0])

    def value(self, t):
        v, tp = self.v0, None
        for tk, vk, kind, _ in self.keys:
            if kind == "ramp":
                t0 = tp if tp is not None else tk
                if t < tk:
                    return v + (vk - v) * clamp((t - t0) / max(tk - t0, 1e-6)) if t > t0 else v
            elif t < tk:
                return v
            v, tp = vk, tk
        return v

    def rate(self, t, dt=1 / 24.0):
        """sign of a slow change in progress: +1 rising, -1 falling, 0 steady (ramps only)."""
        v, tp = self.v0, None
        for tk, vk, kind, _ in self.keys:
            if kind == "ramp" and tp is not None and tp <= t < tk and abs(vk - v) > 1e-4:
                return 1 if vk > v else -1
            v, tp = vk, tk
        return 0

    def hits(self, t, life=1.2):
        """[(age, dv, v_from, v_to, kick)] for hits younger than life."""
        out, v = [], self.v0
        for tk, vk, kind, kick in self.keys:
            if kind == "hit" and 0 <= t - tk < life:
                dv = vk - v
                out.append((t - tk, dv, v, vk, kick if kick is not None else clamp(abs(dv) * 2.2 + 0.25)))
            v = vk
        return out

    def display(self, t):
        """the value drawn: value(t) plus the spring of recent hits (about 15 % overshoot, settled in 0.4 s)."""
        v = self.value(t)
        for age, dv, _, _, _ in self.hits(t, 0.8):
            v -= dv * math.exp(-10.0 * age) * math.cos(2 * math.pi * 2.6 * age)
        return v


# ------------------------------------------------------------------------------------------------ pictograms
def _p(d, col="#ffffff", ow=0.13, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round" paint-order="stroke"%s/>' % (d, col, INK, f(ow), extra)


def _l(d, w, col="#ffffff", ow=0.13):
    s = '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (d, INK, f(w + 2 * ow * 0.75))
    return s + '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (d, col, f(w))


def picto(name, t=0.0, col=(255, 255, 255), base=(60, 60, 60), broken=False):
    """clean simple pictogram in a -1..1 box (white with a thin ink line); base = the badge colour for cut-outs."""
    c, b = rgb(col), rgb(base)
    if name == "bolt":
        return _p("M0.22,-0.95 L-0.62,0.14 L-0.08,0.14 L-0.24,0.95 L0.62,-0.2 L0.06,-0.2 Z", c)
    if name == "heart":
        h = "M0,0.82 C-1.32,-0.06 -0.78,-1.02 0,-0.4 C0.78,-1.02 1.32,-0.06 0,0.82 Z"
        if not broken:
            return _p(h, c)
        z = "M0.02,-0.42 L-0.2,-0.1 L0.14,0.12 L-0.12,0.42 L0.02,0.8"
        return ('<g transform="rotate(-9 0 0.8) translate(-0.07 0)"><clipPath id="hcL"><path d="%s L-1.5,0.9 L-1.5,-1.2 Z"/></clipPath>%s</g>'
                '<g transform="rotate(9 0 0.8) translate(0.07 0)"><clipPath id="hcR"><path d="%s L1.5,0.9 L1.5,-1.2 Z"/></clipPath>%s</g>') % (
            z, _p(h, c, extra=' clip-path="url(#hcL)"') + '<path d="%s" fill="none" stroke="%s" stroke-width="0.09" stroke-linejoin="round" clip-path="url(#hcL)"/>' % (z, INK),
            z, _p(h, c, extra=' clip-path="url(#hcR)"') + '<path d="%s" fill="none" stroke="%s" stroke-width="0.09" stroke-linejoin="round" clip-path="url(#hcR)"/>' % (z, INK))
    if name == "warn":
        return ('<path d="M0,-0.72 L0.84,0.66 L-0.84,0.66 Z" fill="%s" stroke="%s" stroke-width="0.46" stroke-linejoin="round"/>' % (c, INK) +
                '<path d="M0,-0.72 L0.84,0.66 L-0.84,0.66 Z" fill="%s" stroke="%s" stroke-width="0.24" stroke-linejoin="round"/>' % (c, c) +
                '<path d="M0,-0.34 L0,0.14" stroke="%s" stroke-width="0.24" stroke-linecap="round"/><circle cx="0" cy="0.46" r="0.13" fill="%s"/>' % (INK, INK))
    if name == "phone":       # a handset lying flat: missed / ended call
        d = "M-0.92,0.30 C-1.0,-0.62 1.0,-0.62 0.92,0.30 L0.86,0.46 L0.36,0.40 L0.30,0.02 C0.1,-0.06 -0.1,-0.06 -0.30,0.02 L-0.36,0.40 L-0.86,0.46 Z"
        return '<g transform="translate(0 0.02)">%s</g>' % _p(d, c)
    if name == "stopwatch":
        a = 2 * math.pi * (t % 1.0)
        return (_p("M-0.16,-0.98 h0.32 v0.22 h-0.32 Z", c) + '<circle cx="0" cy="0.14" r="0.74" fill="%s" stroke="%s" stroke-width="0.13"/>' % (c, INK) +
                '<circle cx="0" cy="0.14" r="0.5" fill="%s"/>' % b +
                '<path d="M0,0.14 L%s,%s" stroke="%s" stroke-width="0.15" stroke-linecap="round"/>' % (f(0.42 * math.sin(a)), f(0.14 - 0.42 * math.cos(a)), c))
    if name == "signal":
        s = '<circle cx="0" cy="0.62" r="0.2" fill="%s" stroke="%s" stroke-width="0.13" paint-order="stroke"/>' % (c, INK)
        for r in (0.56, 0.98):
            x, y = r * math.sin(math.radians(46)), 0.62 - r * math.cos(math.radians(46))
            s += _l("M%s,%s A%s,%s 0 0 1 %s,%s" % (f(-x), f(y), f(r), f(r), f(x), f(y)), 0.2, c)
        if broken:
            s += _l("M-0.78,0.78 L0.78,-0.78", 0.2, c)
        return s
    if name == "biohazard":
        s = '<mask id="bioM"><rect x="-1.2" y="-1.2" width="2.4" height="2.4" fill="black"/>'
        for k in range(3):
            a = math.radians(-90 + 120 * k)
            s += '<circle cx="%s" cy="%s" r="0.5" fill="white"/>' % (f(0.44 * math.cos(a)), f(0.44 * math.sin(a)))
        for k in range(3):
            a = math.radians(-90 + 120 * k)
            s += '<circle cx="%s" cy="%s" r="0.36" fill="black"/>' % (f(0.6 * math.cos(a)), f(0.6 * math.sin(a)))
            s += '<path d="M0,0 L%s,%s" stroke="black" stroke-width="0.1"/>' % (f(0.5 * math.cos(a)), f(0.5 * math.sin(a)))
        s += '<circle cx="0" cy="0" r="0.15" fill="black"/></mask>'
        s += '<rect x="-1.2" y="-1.2" width="2.4" height="2.4" fill="%s" mask="url(#bioM)"/>' % c
        s += '<circle cx="0" cy="0" r="0.36" fill="none" stroke="%s" stroke-width="0.1" stroke-dasharray="0.5 0.254" stroke-dashoffset="0.63"/>' % c
        return s
    return ""


# ------------------------------------------------------------------------------------------------ the gauge
class Gauge(object):
    """One gauge.  Positions and sizes are pixels of the 720-short-side reference frame.
       kind    "tube" | "badge" (a badge alone, e.g. the title mark) | "avatar" (round picture badge + sound arcs)
       orient  "v": x = tube axis, y = top of the glass, value rises upward, badge on top
               "h": x = left end of the glass, y = tube axis, value grows to the right, badge at the left
       w, length   tube thickness and glass length in px;  segments = n for discrete cells (0 = liquid)
       polarity    "good" (full is green, empty red) | "bad" (full is red) | a function v -> badness 0..1
       crit        badness at which the warning pulse starts (None = never)
       label       short text under a vertical tube; number = function t -> text (big, at the open end of an "h" tube,
                   or replaces the label of a "v" tube when label is None)
       side        +1 / -1: which side the arrow + delta number appear on
       quiet       [(t, scale, opacity)]: from t on the gauge sits back at that scale and opacity
       moves       [(t, dict(x=, y=, length=, orient=, w=))]: from t on the gauge is placed like this (use on a cut)"""

    def __init__(self, id, track=None, t_in=0.0, t_out=1e9, x=100, y=470, w=72, length=330, orient="v", kind="tube", segments=0,
                 polarity="good", crit=0.9, picto="bolt", label=None, number=None, side=1, quiet=(), delta_scale=100, delta_unit="",
                 image=None, level=None, pop_out=True, r=None, color=None, moves=()):
        self.id, self.track, self.t_in, self.t_out = id, track or Track(1.0), t_in, t_out
        self.x, self.y, self.w, self.length, self.orient, self.kind = x, y, w, length, orient, kind
        self.segments, self.polarity, self.crit, self.picto, self.label, self.number = segments, polarity, crit, picto, label, number
        self.side, self.quiet, self.delta_scale, self.delta_unit = side, list(quiet), delta_scale, delta_unit
        self.image, self.level, self.pop_out, self.r, self.color = image, level, pop_out, r, color
        self.moves = sorted(moves, key=lambda m: m[0])          # [(t, dict(x=, y=, length=, orient=, w=))]: re-place on a cut

    def at(self, t):
        """the gauge as placed at time t (moves applied): a shallow copy."""
        cur = None
        for tm, d in self.moves:
            if t >= tm:
                cur = d
        if not cur:
            return self
        import copy
        g = copy.copy(self); g.moves = ()
        for k, v in cur.items():
            setattr(g, k, v)
        return g

    # ---- state
    def badness(self, v):
        if callable(self.polarity):
            return clamp(self.polarity(v))
        return clamp(1 - v) if self.polarity == "good" else clamp(v)

    def visible(self, t):
        return self.t_in <= t < self.t_out

    def pop(self, t):
        """(scale, opacity, rotation deg): 7-frame overshoot in, 5-frame squeeze out, then the quiet steps."""
        a = t - self.t_in
        s, o, r = 1.0, 1.0, 0.0
        if a < 0.29:
            u = a / 0.29
            s = max(0.05, 1 - (1 - u) ** 3 + 0.22 * math.sin(math.pi * u) * (1 - u * 0.5))
            o = clamp(u * 3.5); r = -10 * (1 - u) ** 2
        z = self.t_out - t
        if self.pop_out and z < 0.21:
            u = 1 - z / 0.21
            s *= max(0.05, 1 + 0.10 * math.sin(math.pi * min(1, u * 2)) - u * u)
            o *= clamp((1 - u) * 2.5)
        for tq, sq, oq in self.quiet:
            k = smooth((t - tq) / 0.33)
            s *= 1 + (sq - 1) * k; o *= 1 + (oq - 1) * k
        return s, o, r

    def bbox(self, t=None):
        """(x0, y0, x1, y1) in reference px, everything included (rim, badge, label, number; not droplets)."""
        if t is not None and self.moves:
            return self.at(t).bbox()
        u = self.w / 100.0
        lw = 0.5 * 0.62 * 40 * u * len([c for c in ((self.label or "") + ("00 " if self.number else "")) if not ("\u0e30" < c < "\u0e3b" and c not in "\u0e32\u0e33") and not ("\u0e46" < c < "\u0e4f")])
        if self.kind != "tube":
            r = (self.r or 60) + 12 * u
            return (self.x - max(r, lw), self.y - r, self.x + max(r, lw), self.y + r + (52 * u if self.label else 0))
        e = 13 * u
        if self.orient == "v":
            return (self.x - max(62 * u, lw), self.y - 84 * u, self.x + max(62 * u, lw), self.y + self.length + e + (56 * u if (self.label or self.number) else 0))
        return (self.x - 84 * u, self.y - 62 * u, self.x + self.length + e + (175 * u if self.number else (2.2 * lw + 30 * u if self.label else 0)), self.y + 62 * u)


def _defs_filters():
    return ('<filter id="gB4" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>'
            '<filter id="gB9" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>'
            '<filter id="gB16" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="16"/></filter>')


def _badge(pid, r, col, pic, t, broken=False, image=None, wob=0.0, bump=1.0, rimcol=RIM):
    """round glass badge about (0, 0), design units."""
    lt, dk = mix(col, (255, 255, 255), 0.5), mix(col, (0, 0, 0), 0.42)
    s = '<g transform="rotate(%s) scale(%s)">' % (f(wob), f(bump))
    s += '<defs><radialGradient id="%sbg" cx="0.36" cy="0.28" r="0.85"><stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (pid, rgb(lt), rgb(col), rgb(dk))
    s += '<clipPath id="%sbc"><circle r="%s"/></clipPath></defs>' % (pid, f(r))
    s += '<circle r="%s" fill="%s"/><circle r="%s" fill="%s"/>' % (f(r + 12.5), rimcol, f(r + 8.5), INK)
    if image:
        s += '<circle r="%s" fill="#f4f1ea"/><image href="%s" x="%s" y="%s" width="%s" height="%s" clip-path="url(#%sbc)" preserveAspectRatio="xMidYMid slice"/>' % (
            f(r), image, f(-r), f(-r), f(2 * r), f(2 * r), pid)
    else:
        s += '<circle r="%s" fill="url(#%sbg)"/>' % (f(r), pid)
        s += '<circle r="%s" fill="none" stroke="%s" stroke-width="5" opacity="0.45"/>' % (f(r - 2.5), rgb(dk))
        s += '<g transform="scale(%s)">%s</g>' % (f(r * 0.6), picto(pic, t, base=mix(col, (0, 0, 0), 0.25), broken=broken))
    # gloss: a soft crescent on the upper left
    s += '<path d="M%s,%s A%s,%s 0 0 1 %s,%s A%s,%s 0 0 0 %s,%s Z" fill="#ffffff" opacity="%s" clip-path="url(#%sbc)"/>' % (
        f(-r * 0.86), f(-r * 0.18), f(r * 0.88), f(r * 0.88), f(r * 0.5), f(-r * 0.74), f(r * 1.25), f(r * 1.25), f(-r * 0.86), f(-r * 0.18), "0.22" if image else "0.34", pid)
    s += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#ffffff" opacity="0.75" transform="rotate(-38 %s %s)"/>' % (
        f(-r * 0.47), f(-r * 0.56), f(r * 0.17), f(r * 0.08), f(-r * 0.47), f(-r * 0.56))
    return s + "</g>"


def _text(x, y, s, size, fill="#ffffff", ow=7.0, anchor="middle", extra=""):
    return ('<text x="%s" y="%s" font-family="Kanit" font-weight="900" font-size="%s" text-anchor="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round" paint-order="stroke"%s>%s</text>') % (f(x), f(y), f(size), anchor, fill, INK, f(ow), extra, s)


def gauge_svg(G, t, uid="g"):
    """the gauge in its own design space (100 units = tube thickness; origin = G.x, G.y), already popped/shaken."""
    G = G.at(t)
    sc, op, rot = G.pop(t)
    tr = G.track
    v_true = tr.value(t)
    v = clamp(tr.display(t), -0.02, 1.03)
    bad = G.badness(v_true)
    col = G.color or ramp_color(bad)
    hits = tr.hits(t)
    crit = G.crit is not None and bad >= G.crit and t - G.t_in > 0.3
    pul = 0.5 + 0.5 * math.sin(2 * math.pi * 3.0 * t) if crit else 0.0
    flash = max([k * math.exp(-9.0 * a) for a, dv, _, _, k in hits] or [0.0])
    shx = sum(7.0 * k * math.exp(-6.5 * a) * math.sin(2 * math.pi * 13 * a) for a, dv, _, _, k in hits)
    shy = sum(3.0 * k * math.exp(-6.5 * a) * math.sin(2 * math.pi * 17 * a + 1) for a, dv, _, _, k in hits)
    bump = 1 + 0.2 * max([k * math.exp(-7.0 * a) * abs(math.cos(2 * math.pi * 2.2 * a)) for a, dv, _, _, k in hits] or [0.0]) + 0.06 * pul
    wob = (7.0 * math.sin(2 * math.pi * 6 * t) if crit else 0.0)
    if crit:
        shx += 1.6 * math.sin(2 * math.pi * 11 * t); sc *= 1 + 0.025 * pul
    rimcol = rgb(mix((244, 241, 234), (255, 70, 70), pul * 0.85)) if crit else RIM
    lt, dk = mix(col, (255, 255, 255), 0.55), mix(col, (0, 0, 0), 0.4)
    p = uid
    out = '<g transform="translate(%s %s) rotate(%s) scale(%s)" opacity="%s">' % (f(shx), f(shy), f(rot), f(sc), f(op))

    if G.kind in ("badge", "avatar"):
        r = (G.r or 60) * 100.0 / G.w
        out += '<circle r="%s" fill="#000" opacity="0.4" filter="url(#gB9)" transform="translate(0 7)"/>' % f(r + 10)
        if G.kind == "avatar":
            lev = G.level(t) if G.level else 0.0
            ph = (t * 2.2) % 1.0
            for i in range(3):
                q = (ph + i / 3.0) % 1.0
                rr = r + 22 + 44 * q * (0.85 + 0.5 * lev)
                x, y = rr * math.cos(math.radians(38)), rr * math.sin(math.radians(38))
                d = "M%s,%s A%s,%s 0 0 1 %s,%s" % (f(x), f(-y), f(rr), f(rr), f(x), f(y))
                out += '<g opacity="%s">%s</g>' % (f((1 - q) * (0.45 + 0.55 * min(1, lev * 2 + 0.15))), _l(d, 7.5, "#cfe0ff", 3.2))
            out += _badge(p, r, (244, 241, 234), None, t, image=G.image)
        else:
            out += '<circle r="%s" fill="%s" opacity="0.5" filter="url(#gB16)"/>' % (f(r + 10), rgb(col))
            out += _badge(p, r, col, G.picto, t, bump=bump)
        if G.label:
            out += _text(0, r + 50, G.label, 40)
        return out + "</g>"

    L = G.length * 100.0 / G.w
    horiz = G.orient == "h"
    # local frame of the glass: x -50..50 across, y 0 (open end, "full") .. L (base, "empty"); the badge sits on the
    # open end of a vertical tube and on the base of a horizontal one
    y_full, y_empty = (46.0, L - 11.0) if not horiz else (11.0, L - 46.0)
    ys = y_empty - clamp(v, 0, 1.0) * (y_empty - y_full)
    M = (lambda x, y: (x, y)) if not horiz else (lambda x, y: (L - y, x))
    body = ""
    body += '<defs><linearGradient id="%sgl" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="rgba(58,64,92,0.9)"/><stop offset="0.2" stop-color="rgba(26,28,44,0.84)"/><stop offset="0.8" stop-color="rgba(16,17,28,0.84)"/><stop offset="1" stop-color="rgba(44,48,72,0.9)"/></linearGradient>' % p
    body += '<linearGradient id="%slq" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="%s"/><stop offset="0.3" stop-color="%s"/><stop offset="0.62" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (
        p, rgb(mix(col, (0, 0, 0), 0.25)), rgb(mix(col, (255, 255, 255), 0.38)), rgb(col), rgb(dk))
    body += '<linearGradient id="%shl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.78"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.3"/><stop offset="1" stop-color="#fff" stop-opacity="0.1"/></linearGradient>' % p
    body += '<linearGradient id="%stp" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.34"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>' % p
    body += '<clipPath id="%scv"><rect x="-39" y="11" width="78" height="%s" rx="39"/></clipPath><clipPath id="%sbd"><rect x="-50" y="0" width="100" height="%s" rx="50"/></clipPath></defs>' % (p, f(L - 22), p, f(L))
    sdx, sdy = (0, 8) if not horiz else (8, 0)
    body += '<rect x="-56" y="-6" width="112" height="%s" rx="56" fill="#000" opacity="0.42" filter="url(#gB9)" transform="translate(%d %d)"/>' % (f(L + 12), sdx, sdy)
    body += '<rect x="-52" y="0" width="104" height="%s" rx="52" fill="%s" opacity="%s" filter="url(#gB16)"/>' % (f(L), rgb(col), f(0.3 + 0.45 * pul + 0.4 * min(1, flash)))
    body += '<rect x="-62.5" y="-12.5" width="125" height="%s" rx="62.5" fill="%s"/>' % (f(L + 25), rimcol)
    body += '<rect x="-58.5" y="-8.5" width="117" height="%s" rx="58.5" fill="%s"/>' % (f(L + 17), INK)
    body += '<rect x="-50" y="0" width="100" height="%s" rx="50" fill="#0b0c14"/><rect x="-50" y="0" width="100" height="%s" rx="50" fill="url(#%sgl)"/>' % (f(L), f(L), p)
    body += '<rect x="-39" y="11" width="78" height="%s" rx="39" fill="#05060b" opacity="0.6"/>' % f(L - 22)
    liq = ""
    if G.segments:
        n = G.segments
        gap = 7.0
        ch = (y_empty - y_full - gap * (n - 1)) / n
        lit = clamp(v, 0, 1) * n
        for i in range(n):
            y1 = y_empty - i * (ch + gap); y0 = y1 - ch
            a = clamp(lit - i)
            liq += '<rect x="-39" y="%s" width="78" height="%s" rx="9" fill="#ffffff" opacity="0.09"/>' % (f(y0), f(ch))
            if a > 0.02:
                young = min([ag for ag, dv, vf, vt, _ in hits if dv > 0 and vf * n - 0.01 <= i < vt * n + 0.01] or [9])
                k = 1 + 0.16 * math.exp(-9 * young) * math.cos(2 * math.pi * 2.6 * young)
                cy = (y0 + y1) / 2
                liq += '<g transform="translate(0 %s) scale(%s %s) translate(0 %s)" opacity="%s">' % (f(cy), f(k), f(k), f(-cy), f(min(1, a * 1.3)))
                liq += '<rect x="-39" y="%s" width="78" height="%s" rx="9" fill="url(#%slq)"/>' % (f(y0), f(ch), p)
                liq += '<rect x="-39" y="%s" width="78" height="%s" rx="9" fill="url(#%stp)"/>' % (f(y0), f(ch * 0.6), p)
                liq += '<rect x="-39" y="%s" width="78" height="%s" rx="9" fill="#fff" opacity="%s"/></g>' % (f(y0), f(ch), f(clamp(0.9 * math.exp(-8 * young))))
        glow = '<g clip-path="url(#%sbd)"><rect x="-39" y="%s" width="78" height="%s" fill="%s" opacity="0.55" filter="url(#gB9)"/></g>' % (
            p, f(y_empty - lit * (ch + gap)), f(max(0, lit * (ch + gap))), rgb(col)) if lit > 0.05 else ""
    else:
        tilt = sum(5.0 * k * math.exp(-5 * a) * math.sin(2 * math.pi * 3.2 * a) for a, dv, _, _, k in hits) + 1.2 * math.sin(2 * math.pi * 0.9 * t + 1.3)
        ry = 5.5 + 1.2 * math.sin(2 * math.pi * 1.3 * t)
        liq += '<path d="M-41,%s L41,%s L41,%s L-41,%s Z" fill="url(#%slq)"/>' % (f(ys + tilt), f(ys - tilt), f(L), f(L), p)
        liq += '<rect x="-41" y="%s" width="82" height="%s" fill="url(#%stp)"/>' % (f(ys), f(min(90, L - ys)), p)
        for i in range(6):                                   # bubbles rising in the liquid
            ph = (t * (0.32 + 0.2 * hash01(i, 3)) + hash01(i, 7)) % 1.0
            by = y_empty + 8 - ph * (y_empty + 8 - ys)
            if by > ys + 8:
                liq += '<circle cx="%s" cy="%s" r="%s" fill="#fff" opacity="%s"/>' % (
                    f(-26 + 52 * hash01(i, 11) + 3 * math.sin(2 * math.pi * (ph * 3 + i))), f(by), f(2.6 + 3.2 * hash01(i, 5)), f(0.3 * min(1, (by - ys) / 30)))
        if v > 0.012:
            liq += '<ellipse cx="0" cy="%s" rx="40" ry="%s" fill="%s" transform="rotate(%s 0 %s)"/>' % (f(ys), f(ry), rgb(lt), f(-math.degrees(math.atan2(tilt, 41))), f(ys))
        liq += '<rect x="-41" y="0" width="82" height="%s" fill="#fff" opacity="%s"/>' % (f(L), f(clamp(0.75 * flash)))
        glow = '<g clip-path="url(#%sbd)"><rect x="-39" y="%s" width="78" height="%s" fill="%s" opacity="0.6" filter="url(#gB9)"/></g>' % (p, f(ys), f(L - ys), rgb(col)) if v > 0.012 else ""
    body += glow + '<g clip-path="url(#%scv)">%s</g>' % (p, liq)
    # ticks (fine marks on the far wall), every 10 %, long at 0 / 50 / 100
    if not G.segments:
        for i in range(11):
            y = y_empty - i / 10.0 * (y_empty - y_full)
            lng = i % 5 == 0
            body += '<path d="M%s,%s H39" stroke="#fff" stroke-width="%s" stroke-linecap="round" opacity="%s" clip-path="url(#%scv)"/>' % (
                "13" if lng else "23", f(y), "3" if lng else "2.2", "0.8" if lng else "0.5", p)
    body += '<rect x="-39" y="11" width="78" height="%s" rx="39" fill="none" stroke="%s" stroke-width="3.5" opacity="0.7"/>' % (f(L - 22), INK)
    # glass highlights
    h0, h1 = (y_full + 6, L - 26) if not horiz else (26, y_empty - 6)
    body += '<rect x="-33" y="%s" width="12" height="%s" rx="6" fill="url(#%shl)"/>' % (f(h0), f(h1 - h0), p)
    body += '<rect x="-17" y="%s" width="4" height="%s" rx="2" fill="#fff" opacity="0.2"/>' % (f(h0 + 14), f((h1 - h0) * 0.55))
    body += '<rect x="30" y="%s" width="4.5" height="%s" rx="2.2" fill="#fff" opacity="0.16"/>' % (f(h0 + 8), f(h1 - h0 - 16))
    out += '<g transform="%s">%s</g>' % ("" if not horiz else "translate(%s 0) rotate(90)" % f(L), body)

    # ---- screen-facing parts (not rotated with the glass)
    sx, sy = M(0, ys)
    # droplets thrown from the surface on a hit
    for a, dv, vf, vt, k in hits:
        if a > 0.7 or k < 0.2:
            continue
        hx, hy = M(0, y_empty - clamp(vt) * (y_empty - y_full))
        n = int(6 + 8 * k)
        for i in range(n):
            ang = math.radians(-90 + (hash01(i, vt * 10 + 1) - 0.5) * 230)
            sp = (150 + 260 * hash01(i, 2.5)) * (0.5 + 0.7 * k)
            px_ = hx + math.cos(ang) * sp * a * (1 - 0.6 * a)
            py_ = hy + math.sin(ang) * sp * a + 520 * a * a
            rr = (4.5 + 5 * hash01(i, 9)) * max(0.0, 1 - a / 0.7)
            if rr > 0.6:
                out += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="2.6"/>' % (f(px_), f(py_), f(rr), rgb(lt), INK)
        if a < 0.3:                                           # ring burst
            rr = 40 + 240 * a
            out += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#fff" stroke-width="%s" opacity="%s"/>' % (f(hx), f(hy), f(rr), f(9 * (1 - a / 0.3)), f(0.8 * (1 - a / 0.3)))
    # arrow + delta number while changing
    arrow = None
    for a, dv, vf, vt, k in hits:
        if abs(dv) > 1e-4 and a < 1.05:
            arrow = (1 if dv > 0 else -1, a, dv)
    if arrow is None and tr.rate(t):
        arrow = (tr.rate(t), None, 0.0)
    if arrow:
        d, a, dv = arrow
        good = (d > 0) == (G.badness(0.0) > G.badness(1.0))
        ac = rgb(mix(GREEN if good else RED, (255, 255, 255), 0.18))
        if a is None:
            ao = 0.55 + 0.45 * math.sin(2 * math.pi * 1.6 * t) ** 2; drift = 7 * ((t * 1.6) % 1.0); big = 1.0
        else:
            ao = clamp(a * 12) * clamp((1.05 - a) * 4); drift = 26 * (1 - math.exp(-4 * a)); big = 1 + 0.35 * math.exp(-9 * a)
        if not horiz:
            ax, ay = G.side * 92, clamp(ys, y_full + 10, y_empty - 6) - d * drift
        else:
            ax, ay = clamp(sx, 60, L - 20), G.side * 96 - d * drift * 0.0
        tri = "M0,-17 L17,11 L-17,11 Z" if d > 0 else "M0,17 L17,-11 L-17,-11 Z"
        if horiz:
            tri = "M17,0 L-11,17 L-11,-17 Z" if d > 0 else "M-17,0 L11,17 L11,-17 Z"
            ax += d * drift
        g2 = '<g transform="translate(%s %s) scale(%s)" opacity="%s">' % (f(ax), f(ay), f(big), f(ao))
        g2 += '<path d="%s" fill="%s" stroke="%s" stroke-width="7" stroke-linejoin="round" paint-order="stroke"/>' % (tri, ac, INK)
        if a is not None:
            n = abs(dv) * G.delta_scale
            txt = ("+" if d > 0 else "−") + ("%d" % round(n)) + G.delta_unit
            if not horiz:
                g2 += _text(G.side * 24, 13, txt, 36, ac, 7, "start" if G.side > 0 else "end")
            else:
                g2 += _text(26, 13, txt, 36, ac, 7, "start")
        out += g2 + "</g>"
    # badge
    bx, by = M(0, -24) if not horiz else M(0, L + 24)
    out += '<g transform="translate(%s %s)">%s</g>' % (f(bx), f(by), _badge(p, 54, col, G.picto, t, broken=crit and G.picto in ("heart", "signal"), wob=wob, bump=bump, rimcol=rimcol))
    # label / number
    num = G.number(t) if G.number else None
    if not horiz:
        txt = G.label if G.label is not None else num
        if G.label is not None and num is not None:
            txt = "%s %s" % (num, G.label)
        if txt:
            out += _text(0, L + 56, txt, 40)
    elif num is not None:
        out += _text(L + 30, 30, num, 86, rgb(mix(col, (255, 255, 255), 0.72)), 10, "start")
    elif G.label:
        out += _text(L + 28, 16, G.label, 46, "#ffffff", 8, "start")
    return out + "</g>"


def frame_svg(gauges, t, W, H):
    """full-frame transparent SVG of every visible gauge at film time t (seconds); None when there is nothing."""
    vis = [g for g in gauges if g.visible(t)]
    if not vis:
        return None
    k = min(W, H) / REF
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>' % (W, H, W, H, _defs_filters())
    for i, g in enumerate(vis):
        g = g.at(t)
        s += '<g transform="translate(%s %s) scale(%s)">%s</g>' % (f(g.x * k), f(g.y * k), f(g.w / 100.0 * k), gauge_svg(g, t, "u%d" % i))
    return s + "</svg>"


def data_uri(png_path):
    return "data:image/png;base64," + base64.b64encode(open(png_path, "rb").read()).decode("ascii")
