"""overlay.py -- icons as SCREEN-SPACE overlays on finished frames (for icons that explain a rule: stopwatch, battery,
phone badge...).  One transparent full-frame SVG per film frame, rasterised by Chromium, laid over the frame with PIL.

    from overlay import Placement, frame_svg, render_layer, composite, safe_report
    from anim import Cue
    P = [Placement("stopwatch", Cue(30, hold=60), x=560, y=300, px=170, kw={"speed": 20}),
         Placement("sound_rings", Cue(10, hold=40), x=lambda g: 200 + g, y=520, px=260, kw={"mode": "arcs"})]
    render_layer(P, g, "/abs/ovl/o_%04d.png" % g)          # transparent 720x1280 PNG (None if nothing visible)
    composite("/abs/frame.png", "/abs/ovl/o_0001.png", "/abs/out.png")
    print(safe_report(P))                                  # caption band / edge problems, frame by frame

x, y (pixels of the 720x1280 frame) and px (pixels per 100 design units) may be numbers or functions of g, so an
overlay can follow a projected world point (blender_card.project gives the pixel of a world point per frame).
"""
import os
from PIL import Image

import icons as I
import raster
from anim import pop_state

W, H = 720, 1280
CAPTION_BAND = (860, 1010)      # captions sit at y 900 of 1280: keep icons out of this band
EDGE = 16                       # side gutter

# Frame presets.  Every shot is planned in 9:16 AND 16:9 (plan/BRIEF_camera_and_icons.md).  The caption band is
# kept at the same fraction of the frame height (860/1280 .. 1010/1280) in both, and the gutter stays 16 px.
FRAMES = {"9:16": (720, 1280), "16:9": (1280, 720), "9:16@0.5": (360, 640), "16:9@0.5": (640, 360)}


def frame_size(frame=None):
    """(w, h) of a preset name, a (w, h) tuple, or None (= 9:16 720x1280)."""
    if frame is None:
        return W, H
    if isinstance(frame, str):
        return FRAMES[frame]
    return int(frame[0]), int(frame[1])


def caption_band(h):
    return CAPTION_BAND[0] * h / float(H), CAPTION_BAND[1] * h / float(H)


class Placement(object):
    def __init__(self, name, cue, x, y, px=160, kw=None, rim=None, shadow=None):
        self.name, self.cue, self.x, self.y, self.px = name, cue, x, y, px
        self.kw = kw or {}
        self.rim, self.shadow = rim, shadow

    def at(self, g):
        v = lambda a: a(g) if callable(a) else a
        return v(self.x), v(self.y), v(self.px)


def frame_svg(placements, g, w=W, h=H):
    """x, y, px of each placement are in pixels of THIS w x h frame (place 16:9 icons in 1280x720 pixels)."""
    parts = []
    for p in placements:
        st = pop_state(p.cue, g)
        if not st.visible:
            continue
        ic = I.make(p.name, st.t, **p.kw)
        x, y, px = p.at(g)
        parts.append(I.placed(ic, x, y, px, st.scale, st.rot_deg, st.opacity, p.name, p.rim, p.shadow))
    if not parts:
        return None
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s%s</svg>' % (w, h, I.defs(), "".join(parts))


def render_layer(placements, g, out, w=W, h=H, frame=None):
    if frame is not None:
        w, h = frame_size(frame)
    s = frame_svg(placements, g, w, h)
    if s is None:
        return None
    raster.render([{"svg": s, "w": w, "h": h, "out": out}])
    return out


def composite(base, layer, out):
    b = Image.open(base).convert("RGBA")
    if layer:
        o = Image.open(layer).convert("RGBA")
        if o.size != b.size:
            # same aspect (e.g. a 720x1280 layer on a 360x640 test frame): scale it.  A different aspect (a 9:16
            # layer on a 16:9 frame) used to be stretched silently; that is an error now.
            ra, rb = o.size[0] / float(o.size[1]), b.size[0] / float(b.size[1])
            if abs(ra - rb) > 0.01:
                raise ValueError("overlay layer %dx%d does not match the frame %dx%d: render the layer with "
                                 "frame=(w, h) of that frame" % (o.size + b.size))
            o = o.resize(b.size, Image.LANCZOS)
        b.alpha_composite(o)
    b.convert("RGB").save(out)
    return out


def bbox(p, g, scale=1.15):
    """pixel box of the icon at frame g at the largest pop scale (+ rim and shadow, about 4 units)."""
    st = pop_state(p.cue, g)
    ic = I.make(p.name, max(st.t, 0.0), **p.kw)
    x, y, px = p.at(g)
    k = px / 100.0 * scale
    ax, ay = ic.anchor
    return (x - (ax + 4) * k, y - (ay + 4) * k, x + (ic.w - ax + 5) * k, y + (ic.h - ay + 6) * k)


def safe_report(placements, w=W, h=H, frame=None):
    """frames where an icon enters the caption band or the side gutter (band scaled to the frame height)."""
    if frame is not None:
        w, h = frame_size(frame)
    band = caption_band(h)
    out = []
    for p in placements:
        for g in p.cue.frames():
            if not pop_state(p.cue, g).visible:
                continue
            x0, y0, x1, y1 = bbox(p, g)
            why = []
            if y1 > band[0] and y0 < band[1]:
                why.append("caption band")
            if x0 < EDGE or x1 > w - EDGE or y0 < 0 or y1 > h:
                why.append("edge")
            if why:
                why = ",".join(why)
                if out and out[-1][0] == p.name and out[-1][3] == why and out[-1][2] == g - 1:
                    out[-1][2] = g
                else:
                    out.append([p.name, g, g, why, tuple(int(v) for v in (x0, y0, x1, y1))])
    return [tuple(o) for o in out]      # (icon, first g, last g, problem, box at the first g)
