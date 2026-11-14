#!/usr/bin/env python3
"""lib6b.py -- small film-6b helpers for the takes of render team 1 (s01, s04; each take folder carries its own copy).

  thai_sign(text, ...)   SVG fragment of a hanging / standing sign board with Thai text in Kanit Black (font embedded as a data
                         URI so headless Chromium shapes the Thai marks itself), thick ink outline like the set.  Rasterise with
                         common.svg_pngs and stand it in the set with common.PropCard (box = sign_box(w, h)).
  puff_svg(k)            a white steam puff (k 0..1 = grow + fade) for a loaf landing.
  pale_png(path)         lighten a rasterised loaf drawing (the 13th loaf is the paler one).
  cool_fill(...)         a blue area light: the cool counter-colour the formula asks for in the warm bakery.
"""
import os, base64, math

FILM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
KANIT = os.path.join(FILM, "fonts", "Kanit_900Black.ttf")
INK = "#3a2832"
_FONT = None


def _font_css():
    global _FONT
    if _FONT is None:
        _FONT = base64.b64encode(open(KANIT, "rb").read()).decode()
    return "<style>@font-face{font-family:'K6b';src:url(data:font/ttf;base64,%s) format('truetype');}</style>" % _FONT


def sign_box(w, h, chains=0.0):
    """drawing box of thai_sign (origin = top centre of the board, y down); chains > 0 adds hanging cords above."""
    return (-w / 2 - 0.08, -chains - 0.08, w / 2 + 0.08, h + 0.10)


def thai_sign(text, w=1.6, h=0.55, board="#f3e2b8", edge="#a8743a", fg="#c8202a", outline="#ffffff", size=None,
              chains=0.0, nail=True, tilt=0.0, lines=None):
    """board w x h (D), top centre at (0, 0).  Text fitted to the board width (textLength).  lines: list of texts (multi-line)."""
    sw = 0.045
    o = [_font_css()]
    o.append('<g transform="rotate(%.2f 0 %.3f)">' % (tilt, h / 2))
    if chains > 0:
        for sx in (-0.32 * w, 0.32 * w):
            o.append('<line x1="%.3f" y1="0" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%.3f"/>' % (sx, sx * 0.4, -chains, INK, 0.035))
    # board: plank with wobbly ends, darker edge band, wood grain
    o.append('<rect x="%.3f" y="0" width="%.3f" height="%.3f" rx="%.3f" fill="%s" stroke="%s" stroke-width="%.3f"/>'
             % (-w / 2, w, h, 0.06, edge, INK, sw))
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f" fill="%s"/>' % (-w / 2 + 0.05, 0.05, w - 0.10, h - 0.10, 0.04, board))
    for i in range(3):
        yy = h * (0.25 + 0.25 * i)
        o.append('<path d="M%.3f,%.3f q%.3f,%.3f %.3f,0" fill="none" stroke="%s" stroke-width="0.008" opacity="0.35"/>'
                 % (-w / 2 + 0.08, yy, w * 0.3, 0.02 * (1 - i), w - 0.16, edge))
    if nail:
        for sx in (-w / 2 + 0.10, w / 2 - 0.10):
            o.append('<circle cx="%.3f" cy="%.3f" r="0.025" fill="%s"/>' % (sx, 0.09, INK))
    lines = lines or [text]
    n = len(lines)
    fs = size or min(h * 0.62 / n, 0.5)
    for i, t in enumerate(lines):
        cy = h * (i + 0.5) / n + fs * 0.42
        tl = w - 0.26
        common = ('x="0" y="%.3f" font-family="K6b" font-weight="900" font-size="%.3f" text-anchor="middle" textLength="%.3f" '
                  'lengthAdjust="spacingAndGlyphs"' % (cy, fs, tl))
        o.append('<text %s fill="none" stroke="%s" stroke-width="%.3f" stroke-linejoin="round">%s</text>' % (common, INK, fs * 0.22, t))
        if outline:
            o.append('<text %s fill="none" stroke="%s" stroke-width="%.3f" stroke-linejoin="round">%s</text>' % (common, outline, fs * 0.10, t))
        o.append('<text %s fill="%s">%s</text>' % (common, fg, t))
    o.append('</g>')
    return "".join(o)


def puff_svg(k, r=0.30, seed=0):
    """steam puff: a cluster of soft white circles, k 0..1: grows 0.5 -> 1.4 and fades out."""
    s = 0.5 + 0.9 * k
    a = max(0.0, 1.0 - k) ** 1.2 * 0.85
    o = ['<defs><radialGradient id="pf%d"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/>'
         '<stop offset="0.6" stop-color="#f4f6ff" stop-opacity="0.7"/><stop offset="1" stop-color="#e8eeff" stop-opacity="0"/></radialGradient></defs>' % seed]
    for i, (dx, dy, rr) in enumerate(((0, 0, 1.0), (-0.55, 0.15, 0.7), (0.55, 0.12, 0.75), (-0.2, -0.5, 0.8), (0.3, -0.55, 0.65),
                                      (0.0, -1.0, 0.55))):
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="url(#pf%d)" opacity="%.3f"/>'
                 % (dx * r * s, (dy - 0.6 * k) * r * s, rr * r * s, seed, a))
    return "".join(o)


def pale_png(path, out, k=0.45):
    """lighten (towards cream) every opaque pixel of a loaf PNG: the paler 13th loaf."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    import numpy as np
    a = np.asarray(im).astype(float)
    cream = np.array([255, 240, 205], float)
    rgb = a[..., :3]
    lum = rgb.mean(axis=2, keepdims=True)
    dark = lum < 70                      # keep the ink outline
    new = rgb * (1 - k) + cream * k
    a[..., :3] = np.where(dark, rgb, new)
    Image.fromarray(a.clip(0, 255).astype("uint8")).save(out)
    return out


def cool_fill(name, loc, rot, energy=400.0, size=6.0, color=(0.35, 0.55, 1.0)):
    """blue area light (no shadow from the actors: they are emission cards)."""
    import bpy
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.size = size
    ld.color = color
    ob = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def aim(ob, target):
    from mathutils import Vector
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
