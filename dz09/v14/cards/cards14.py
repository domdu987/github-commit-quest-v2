"""cards14.py -- DEAD ZONE 09 EP.1, status graphics v14: one flat INFO CARD at the top-left (+ a chip row above it).

    import cards14
    rgba = cards14.overlay(g, W, H, aspect='916')      # film frame g (0..1279) -> uint8 RGBA (H, W, 4), straight alpha
    rgb  = cards14.over(rgb_uint8, g)                   # composite over an RGB frame
    rows = cards14.cue_table()                          # [(card, t_in, t_out, [(t, what), ...]), ...]

Same public API as v13/icons/icons13.py (overlay, over, cue_table, close, LAYOUT, T, DZ09_NARR), so finish.py switches
by importing this module instead.  The animated icon drawings and every cue time are imported from icons13 (not
copied); here each icon sits in the dark medallion of a paper card that carries a small label, a big value and
sometimes a sub-line.  A card arrives when the narration reaches its subject, its value changes with the story, an
older card of the same subject shrinks into a chip above the current one, and the group leaves when the subject is
over.  Flat only: solid fills, ink outline, thin light keyline; no shadow, gradient, gloss or grain.
Raster: SVG -> one headless Chromium page (raster_page.js, Kanit Black from PROJ/fonts), cached on disk by SVG hash.
"""
import atexit, hashlib, json, math, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
os.environ.setdefault("DZ09_NARR", "narr_ohm")
sys.path.insert(0, os.path.join(PROJ, "v13", "icons"))
import icons13 as IC                                      # icon drawings, cue times, easing, palette (read only)
from icons13 import (T, FPS, NF, F, INK, PAPER, RED, AMBER, GREEN, GREY, SLOT, clamp, u, eio, eo, ei, back, spring, kick, decay,
                     mix, rnd, xf, st, shot_of, cap)

NARR = IC.NARR
CACHE = os.path.join(HERE, "cache")
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
NAVY = "#141a2b"                                          # panel: the film's night blue
ORANGE = IC.ORANGE                                        # rescue orange (Kong's vest)
DIM = "#c3c2c6"                                           # label / unit / sub-line (paper, one step down)
DEADTXT = "#8f8d96"                                       # "hung up" value
STYLE = os.environ.get("DZ09_CARD", "A")                  # A: navy tag with a stencil tab; B: orange header band on navy (HEAD px taller)
HEAD = 28
TAB_LEFT = ("radio",)                                     # cards whose zone tab sits at the left end (S01: Kong's mouth is behind the right end; no chip above this card)
KEY = 2.0                                                 # light keyline outside the ink, card pixels

# ------------------------------------------------------------------------------------------------ layout
# reference frames 720x1280 (9:16) and 1280x720 (16:9).  x0, y = top-left of the card; s = scale of the whole layer
# (1 = the sizes below in reference pixels); chips sit above the card.  fade = [(t0, t1, opacity)], out = leave times,
# title = (x, y, radius) of the title mark (same as icons13), shift = {shot: (x0, y)} moves the card for one shot.
LAYOUT = {
    # 9:16 shift S01: Kong's face rises to y 20-130 behind the card's right end in the last second of the shot, so the card sits 26 px lower there
    "916": dict(RW=720, RH=1280, x0=36, y=110, s=1.0, shift={"S01": (36, 136)}, fade=list(IC.LAYOUT["916"]["fade"]), title=IC.LAYOUT["916"]["title"],
                out=dict(radio=6.40, battery=19.30, calls=33.00, trust=33.00, danger=45.90)),
    "169": dict(RW=1280, RH=720, x0=64, y=86, s=0.80, shift={}, fade=[], title=IC.LAYOUT["169"]["title"],
                out=dict(radio=6.40, battery=19.30, calls=33.00, trust=33.00, danger=45.90)),
}
CH = 132                                                  # card height
BAR = 14                                                  # accent bar
MCX, MCY, MR = 64, 66, 41                                 # medallion centre / radius inside the card
TX = 120                                                  # text column
PADR = 18
MAXW = 446                                                # 62 % of 720
CHIP_H, CHIP_GAP = 44, 8                                  # chip row: y - 52 .. y - 8
LABEL_FS, SUB_FS, UNIT_FS, TEXT_FS, NUM_FS, BIG_FS = 25, 23, 28, 54, 60, 68
T_DAUGHTER = IC.CAP.get("จากลูกสาว", 20.49)             # "from his daughter" (the name follows at T.P_NAME)

# ------------------------------------------------------------------------------------------------ text metrics
_FT = {}


def tw(s, size):
    """advance width of a string in Kanit Black (the same file Chromium draws with)"""
    from PIL import ImageFont
    if size not in _FT:
        try:
            _FT[size] = ImageFont.truetype(FONT, 100, layout_engine=ImageFont.Layout.RAQM)
        except Exception:
            _FT[size] = ImageFont.truetype(FONT, 100)
    return _FT[size].getlength(s) * size / 100.0


def txt(s, x, y, size, col=PAPER, anchor="start", thin=0.0, extra=""):
    """Kanit Black; thin > 0 lays a paper-coloured stroke over the glyph edges (reads as a lighter weight on the card)"""
    th = 'stroke="%s" stroke-width="%.2f" stroke-linejoin="round"' % (NAVY, thin) if thin > 0 else ""
    return '<text x="%.2f" y="%.2f" font-family="Kanit" font-weight="900" font-size="%.2f" text-anchor="%s" fill="%s" %s %s>%s</text>' % (
        x, y, size, anchor, col, th, extra, s)


# ------------------------------------------------------------------------------------------------ icons from icons13
class _patched(object):
    """call an icons13 drawing without its strip extras (value bar, number, name tag): the card carries those as
    text.  icons13 is not edited; three module names are swapped for the length of one call and put back."""

    def __init__(self, no_text=False, no_tag=False):
        self.no_text, self.no_tag = no_text, no_tag

    def __enter__(self):
        self.keep = (IC.hbar, IC.text, T.P_NAME)
        IC.hbar = lambda *a, **k: ""
        if self.no_text:
            IC.text = lambda *a, **k: ""
        if self.no_tag:
            T.P_NAME = 1e9

    def __exit__(self, *a):
        IC.hbar, IC.text, T.P_NAME = self.keep


def icon_svg(name, t, mm=0.0):
    if name == "radio":
        with _patched():
            return IC.radio(t, 1)[0]
    if name == "battery":
        with _patched():
            return IC.battery(t, 1)[0]
    if name == "calls":                                   # red badge without the count (the card shows it), no name tag
        with _patched(no_text=True, no_tag=True):
            return IC.phone(t, 1)[0]
    if name == "trust":
        with _patched():
            return IC.heart(t, 1)[0]
    if name == "danger":
        with _patched():
            return IC.danger(t, 1)[0]
    with _patched(no_text=True):
        return IC.stopwatch(t, 1, mm)[0]


#          px per icon unit in the medallion, offset of the icon origin from the medallion centre (units); chip scale, chip icon width (units)
ICON = dict(radio=(0.66, -18, 0), battery=(0.74, 0, 0), calls=(0.80, 4, 0), trust=(0.72, 0, 2), danger=(0.68, 0, 0), countdown=(0.80, 0, -1))
CHIP_ICON = dict(battery=(0.36, 92, 0, 0), calls=(0.40, 62, 4, 0))


# ------------------------------------------------------------------------------------------------ card states
def _keys(name):
    """[(film s, value, unit)] of a card, in order"""
    if name == "radio":
        return [(T.R_IN, "กำลังติดต่อ", ""), (T.R_CUT, "สัญญาณขาด", "")]
    if name == "battery":
        return [(T.B_IN, "0/3", "ขีด"), (T.B1, "1/3", "ขีด"), (T.B2, "2/3", "ขีด"), (T.B3, "3/3", "ขีด")]
    if name == "calls":
        return [(T.P_IN, "0", "สาย"), (T.P1, "1", "สาย"), (T.P2, "2", "สาย"), (T.P3, "3", "สาย"), (T.P4, "4", "สาย")]
    if name == "danger":
        return [(T.D_IN, "ชีพจรอ่อน", ""), (T.D_LEAN, "ไม่ตอบสนอง", ""), (T.D_EYE, "ติดเชื้อ!", "")]
    if name == "countdown":
        return [(T.C_IN, "60", "วินาที"), (T.C_T0 + 1, "59", "วินาที"), (T.C_T0 + 2, "58", "วินาที"), (T.C_T0 + 3, "57", "วินาที")]
    return []


#         id          label                  kind    joins    next card of the same subject (this one becomes a chip)
CARDS = [("radio", "วิทยุกู้ภัย", "text", T.R_IN, None),
         ("battery", "เครื่องตัดไร้สาย", "num", T.B_IN, "calls"),
         ("calls", "สายที่ไม่ได้รับ", "num", T.P_IN, "trust"),
         ("trust", "ความเชื่อใจของลูก", "num", T.H_IN, None),
         ("danger", "คนขับ", "text", T.D_IN, None),
         ("countdown", "เหลือเวลา", "big", T.C_IN, None)]
JOIN = dict((c[0], c[3]) for c in CARDS)
SUBS = dict(battery=["แบตเต็ม"], calls=["ลูกสาว · น้ำเหนือ"])
T_TRUST_CRIT = T.H_EVERY + 1.25                           # the level has sunk to 28 %


def trust_pct(t):
    return int(round(IC.trust_level(t) * 100))


def state(name, t):
    """(value colour, ring colour, bar: None = hazard stripes | solid colour, outline colour)"""
    if name == "radio":
        k = u(t, T.R_CUT, T.R_CUT + 1 * F)
        return (mix(PAPER, RED, k), mix(ORANGE, RED, k), RED if k >= 1 else None, PAPER)
    if name == "battery":
        k = u(t, T.B3, T.B3 + 2 * F)
        return (mix(PAPER, GREEN, k), mix(ORANGE, GREEN, k), GREEN if k >= 1 else None, PAPER)
    if name == "calls":
        k = u(t, T.P1, T.P1 + 2 * F)
        return (mix(PAPER, RED, k), mix(ORANGE, RED, k), RED if k > 0 else None, PAPER)
    if name == "trust":
        k, d = eio(u(t, T_TRUST_CRIT - 0.4, T_TRUST_CRIT)), eio(u(t, T.H_END, T.H_END + 0.35))
        return (mix(mix(PAPER, RED, k), DEADTXT, d), mix(RED, GREY, d), GREY if d > 0.5 else (RED if k >= 1 else None), PAPER)
    if name == "danger":
        c = IC.danger_color(t)
        return (c, c, RED if t >= T.D_EYE else None, RED if t >= T.D_EYE else PAPER)       # the outline snaps to red with the eye
    p = max([0.0] + [1 - u(t, T.C_T0 + i, T.C_T0 + i + 8 * F) for i in range(0, 4) if t >= T.C_T0 + i])   # one amber pulse a second
    return (AMBER, AMBER, None, mix(PAPER, AMBER, p))


def accent(name, t):
    return state(name, t)[1]


def card_width(name, label, kind):
    """one fixed width per card (the widest of its states), so nothing jitters while a value counts"""
    w = tw(label, LABEL_FS)
    if name == "trust":
        w = max(w, tw("82", NUM_FS) + 6 + tw("%", UNIT_FS + 6), tw("วางสาย", TEXT_FS))
    for _, v, un in _keys(name):
        fs = dict(text=TEXT_FS, num=NUM_FS, big=BIG_FS)[kind]
        w = max(w, tw(v, fs) + (8 + tw(un, UNIT_FS) if un else 0))
    for s in SUBS.get(name, []):
        w = max(w, tw(s, SUB_FS))
    return min(MAXW, TX + math.ceil(w) + PADR)


def _value(name, kind, t, col=None):
    """value line with the tick: the old value lifts and fades, the new one comes up from below (no clip, so no Thai mark is cut)"""
    fs = dict(text=TEXT_FS, num=NUM_FS, big=BIG_FS)[kind]
    base = dict(text=104, num=82, big=102)[kind]
    col = col or state(name, t)[0]
    if name == "trust":
        x = u(t, T.H_END, T.H_END + 5 * F)
        pct = "%d" % trust_pct(min(t, T.H_END))
        num = txt(pct, TX, base, NUM_FS, col) + txt("%", TX + tw(pct, NUM_FS) + 6, base, UNIT_FS + 6, DIM)
        if x <= 0:
            return num
        new = '<g opacity="%.3f" transform="translate(0 %.2f)">%s</g>' % (u(x, 0.2, 0.6), 12 * (1 - back(x, 1.6)), txt("วางสาย", TX, base, TEXT_FS, col)) if x > 0.2 else ""
        return ('<g opacity="%.3f" transform="translate(0 %.2f)">%s</g>' % (1 - u(x, 0, 0.4), -10 * x, num) if x < 0.4 else "") + new
    ks = [k for k in _keys(name) if t >= k[0]]
    if not ks:
        return ""

    def one(k):
        s = txt(k[1], TX, base, fs, col)
        if k[2]:
            s += txt(k[2], TX + tw(k[1], fs) + 8, base, UNIT_FS, DIM, thin=0.9)
        return s
    cur = ks[-1]
    if name == "radio" and 0 <= t - T.R_CUT < 3 * F - 1e-6:               # signal glitch: 3 frames of offset slices of the value
        g, s = int(round(t * FPS)), ""
        for i in range(6):
            y = base - 62 + i * 13
            which = cur if (i + g) % 3 else ks[-2]
            s += '<clipPath id="c14g%d"><rect x="%d" y="%d" width="%d" height="13"/></clipPath><g clip-path="url(#c14g%d)"><g transform="translate(%.1f 0)">%s</g></g>' % (
                i, TX - 30, y, MAXW, i, rnd(g, 50 + i) * 20, txt(which[1], TX, base, fs, RED if which is cur else PAPER))
        return s
    x = u(t, cur[0], cur[0] + 5 * F)
    if len(ks) == 1 or x >= 1:
        return one(cur)
    old = '<g opacity="%.3f" transform="translate(0 %.2f)">%s</g>' % (1 - u(x, 0, 0.4), -10 * x, one(ks[-2])) if x < 0.4 else ""
    new = '<g opacity="%.3f" transform="translate(0 %.2f)">%s</g>' % (u(x, 0.2, 0.6), 12 * (1 - back(x, 1.6)), one(cur)) if x > 0.2 else ""
    return old + new


def _divider(x1, k):
    return '<line x1="%d" y1="92" x2="%.2f" y2="92" stroke="%s" stroke-width="2.2" stroke-dasharray="6 5" stroke-linecap="butt"/>' % (
        TX, TX + (x1 - TX) * k, mix(NAVY, PAPER, 0.45))


def _sub(name, t, W):
    x1 = W - PADR
    if name == "battery":
        k = eo(u(t, T.B3 + 2 * F, T.B3 + 8 * F))
        if k <= 0:
            return ""
        return _divider(x1, k) + '<g opacity="%.3f" transform="translate(%.2f 0)">%s</g>' % (k, -8 * (1 - k), txt("แบตเต็ม", TX, 119, SUB_FS, DIM, thin=0.8))
    if name == "calls":
        k = eo(u(t, T_DAUGHTER, T_DAUGHTER + 6 * F))
        if k <= 0:
            return ""
        s = _divider(x1, k) + '<g opacity="%.3f" transform="translate(%.2f 0)">%s</g>' % (k, -8 * (1 - k), txt("ลูกสาว", TX, 119, SUB_FS, DIM, thin=0.8))
        k2 = eo(u(t, T.P_NAME, T.P_NAME + 6 * F))
        if k2 > 0:
            s += '<g opacity="%.3f" transform="translate(%.2f 0)">%s</g>' % (k2, -8 * (1 - k2), txt("· น้ำเหนือ", TX + tw("ลูกสาว ", SUB_FS), 119, SUB_FS, PAPER))
        return s
    if name == "trust":
        k = eo(u(t, T.H_IN + 3 * F, T.H_IN + 10 * F))
        if k <= 0:
            return ""
        L, lv = (x1 - TX) * k, IC.trust_level(t)
        s = _divider(x1, k)
        s += '<rect x="%d" y="104" width="%.2f" height="12" rx="6" fill="%s"/>' % (TX, L, INK)
        if lv * L > 1:
            s += '<rect x="%d" y="104" width="%.2f" height="12" rx="6" fill="%s"/>' % (TX, max(12, lv * L), state(name, t)[1])
        s += '<rect x="%d" y="104" width="%.2f" height="12" rx="6" fill="none" %s/>' % (TX, L, st(2.4, PAPER))
        return s
    return ""


def zone_mark(x, y, r, disc, mark, uid):
    """the series mark, small: flat disc + the title's biohazard drawing from icons13"""
    return '<g transform="translate(%.2f %.2f)"><circle r="%.2f" fill="%s"/><g transform="scale(%.4f)">%s</g></g>' % (x, y, r, disc, r / 34.0, IC.biohazard(mark, uid))


def hazard(x0, w, y0, y1, bar):
    """the left bar: diagonal rescue-orange / ink stripes, or one solid colour"""
    if bar:
        return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, y1 - y0, bar)
    s = '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, y1 - y0, ORANGE)
    y = y0 - 10
    while y < y1 + w:
        s += '<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s"/>' % (x0, y, x0 + w, y - w, x0 + w, y - w + 9, x0, y + 9, INK)
        y += 20
    return s


def card_svg(name, label, kind, t, W):
    """the card in its own pixels: origin = top-left, CH high, W wide (style B: an orange header band of HEAD px above y 0)"""
    vcol, ring, bar, line = state(name, t)
    flash = name == "danger" and 0 <= t - T.D_LUNGE < 1 * F - 1e-6         # the lunge: ONE frame, white card with a red outline
    face = PAPER if flash else NAVY
    if flash:
        vcol, line = RED, RED
    top = -HEAD if STYLE == "B" else 0
    s = '<g filter="url(#kd)"><rect x="0" y="%d" width="%.2f" height="%d" rx="20" fill="%s" %s/></g>' % (top, W, CH - top, face, st(5.0, line))
    s += '<clipPath id="c14%s"><rect x="2.5" y="%.1f" width="%.2f" height="%.1f" rx="17.5"/></clipPath><g clip-path="url(#c14%s)">' % (name, top + 2.5, W - 5, CH - top - 5, name)
    s += hazard(0, BAR + 2, top, CH, bar)
    s += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" %s/>' % (BAR + 3.5, top, BAR + 3.5, CH, st(3.0, line))
    if STYLE == "B":                                                       # B: rescue-orange header band with the zone stencil
        s += '<rect x="%d" y="%d" width="%.2f" height="%d" fill="%s"/><line x1="%d" y1="-1.5" x2="%.2f" y2="-1.5" %s/>' % (BAR + 5, top, W, HEAD, ORANGE, BAR + 5, W, st(3.0, line))
        s += zone_mark(BAR + 26, top + HEAD / 2.0 + 1, 9.5, INK, ORANGE, "c14z" + name)
        s += txt("เขต 09", BAR + 42, top + HEAD / 2.0 + 7.5, 19, INK, extra='letter-spacing="1.5"')
        s += txt("DEAD ZONE", W - 16, top + HEAD / 2.0 + 6.5, 15, INK, anchor="end", extra='letter-spacing="1.5"')
    s += '</g>'
    if STYLE == "A":                                                       # A: a small stencil tab on the top edge, right end
        tw_ = 34 + tw("เขต 09", 17) + 6 + 12
        x = BAR + 12 if name in TAB_LEFT else W - 16 - tw_
        s += '<rect x="%.2f" y="-22" width="%.2f" height="25" rx="6" fill="%s" %s/>' % (x, tw_, face, st(3.0, line))
        s += zone_mark(x + 17, -9.5, 8.5, AMBER, INK, "c14z" + name)
        s += txt("เขต 09", x + 31, -3, 17, RED if flash else PAPER, extra='letter-spacing="1"')
    s += '<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3.5"/>' % (MCX, MCY, MR, INK, ring)
    s += txt(label, TX, 33, LABEL_FS, RED if flash else DIM, thin=0.0 if flash else 0.9)
    s += _value(name, kind, t, vcol) + _sub(name, t, W)
    if name != "countdown" or t < T.C_MORPH:                              # from the morph on the stopwatch is its own layer
        sc, dx, dy = ICON[name]
        s += '<g filter="url(#kl)"><g %s>%s</g></g>' % (xf(MCX + dx * sc, MCY + dy * sc, sc), icon_svg(name, t))
    return s


def chip_svg(name, t):
    """small tag: icon + final value.  -> (svg with origin top-left, width)"""
    val = _keys(name)[-1][1]
    sc, wu, dx, dy = CHIP_ICON[name]
    wi = wu * sc
    W = 12 + wi + 8 + tw(val, 27) + 14
    s = '<g filter="url(#kd)"><rect x="0" y="0" width="%.2f" height="%d" rx="12" fill="%s" %s/></g>' % (W, CHIP_H, NAVY, st(4.0, PAPER))
    s += '<g filter="url(#k1)"><g %s>%s</g></g>' % (xf(12 + wi / 2.0 + dx * sc, CHIP_H / 2.0 + dy * sc, sc), icon_svg(name, t))
    s += txt(val, 12 + wi + 8, 32, 27, state(name, t)[0])
    return s, W


# ------------------------------------------------------------------------------------------------ the layer
def scene(t, aspect="916"):
    """-> (svg body in reference pixels, (y_top, y_bottom) of the rows that can hold ink) or (None, None)"""
    L = LAYOUT[aspect]
    g = int(round(t * FPS))
    S = L["s"]
    x0, y0 = L["shift"].get(shot_of(g), (L["x0"], L["y"]))
    fade = 1.0
    for a, b, o in L["fade"]:
        fade *= 1 - (1 - o) * eio(u(t, a - 4 * F, a)) * (1 - eio(u(t, b, b + 5 * F)))
    out, chips_x = [], 0.0
    hd = HEAD if STYLE == "B" else 0
    for name, label, kind, t_in, nxt in CARDS:
        t_out = L["out"].get(name, 1e9)
        if t < t_in or t >= t_out + 8 * F:
            continue
        if name == "countdown" and t >= T.C_MORPH + 9 * F:
            continue
        W = card_width(name, label, kind)
        leave = eio(u(t, t_out, t_out + 7 * F))
        op = fade * (1 - leave) * u(t, t_in, t_in + 2.5 * F)
        lx = -26 * ei(u(t, t_out, t_out + 7 * F))                         # leaves to the left
        if name == "countdown":
            op *= 1 - eio(u(t, T.C_MORPH - 1 * F, T.C_MORPH + 7 * F))     # dissolves under the flying stopwatch
        tn = JOIN[nxt] if nxt else 1e9
        shr = eio(u(t, tn - 7 * F, tn + 2 * F))                           # 0 card .. 1 chip
        if shr > 0:
            csvg, cw = chip_svg(name, t)
            k = eo(u(shr, 0.45, 1.0))
            pop = 1 + 0.10 * kick(t, tn + 1 * F, 3.2, 9)
            cop = op * u(shr, 0.45, 0.8)
            if cop > 0.004:
                out.append('<g opacity="%.3f"><g %s>%s</g></g>' % (cop, xf(chips_x + lx, -(CHIP_H + CHIP_GAP + hd) + CHIP_H / 2.0 * (1 - pop), 1, pop), csvg))
            chips_x += (cw + 10) * k
        if shr < 0.8:
            p = clamp(spring(t, t_in, 2.6, 10), 0, 1.07)                 # small overshoot only: the widest card must stay left of x 490
            sc = (0.72 + 0.28 * p) * (1 + (CHIP_H / float(CH) - 1) * shr)
            sh = decay(t, T.D_LUNGE, 14) * 7 if name == "danger" and t >= T.D_LUNGE else 0.0
            sh += 5 * decay(t, T.R_CUT, 12) if name == "radio" and t >= T.R_CUT else 0.0
            if name == "countdown":                                       # one small pulse a second with the amber outline
                sc *= 1 + 0.025 * sum(kick(t, T.C_T0 + i, 3.5, 10) for i in range(0, 4))
            # pops from its left edge, vertical centre; shrinks toward the chip row
            ax, ay = 0.0, CH / 2.0
            ty = -(CHIP_H + CHIP_GAP + hd) * shr
            cop = op * (1 - u(shr, 0.3, 0.8))
            if cop > 0.004:
                out.append('<g opacity="%.3f"><g transform="translate(%.2f %.2f) scale(%.4f) translate(%.2f %.2f)">%s</g></g>' % (
                    cop, ax + lx + rnd(g, 3) * sh, ay * (1 - shr) + ty + rnd(g, 4) * sh * 0.6, sc, -ax, -ay * (1 - shr), card_svg(name, label, kind, t, W)))
    body = ""
    if out:
        body = '<g transform="translate(%.2f %.2f) scale(%.4f)">%s</g>' % (x0, y0, S, "".join(out))
    rows = (max(0, int(y0 - 96 * S)), int(y0 + (CH + 36) * S))
    # the stopwatch leaves its medallion and flies to the title spot (icons13's flight; same end state, pixel for pixel)
    if t >= T.C_MORPH:
        mm = eio(u(t, T.C_MORPH, T.TITLE - 1 * F))
        sc0, dx, dy = ICON["countdown"]
        sc0 *= S
        cx0, cy0 = x0 + (MCX + dx * ICON["countdown"][0]) * S, y0 + (MCY + dy * ICON["countdown"][0]) * S
        tx, ty, tr = L["title"]
        p = clamp(spring(t, T.C_IN, 2.6, 10), 0, 1.25)
        land = 1 + 0.10 * kick(t, T.TITLE, 3.2, 7)
        cx = cx0 + (tx - cx0) * mm
        cy = cy0 + (ty - 4 * tr / 38.0 - cy0) * mm - 46 * math.sin(math.pi * mm) * (1 if mm < 1 else 0)
        s1 = sc0 + (tr / 38.0 - sc0) * mm
        item = '<g %s>%s%s</g>' % (xf(cx, cy, s1 * p * land, s1 * p * (2 - land)), icon_svg("countdown", t, mm),
                                   IC.burst(t, T.TITLE, 12, 46, 70, AMBER, 5, dur=10 * F, rot=15, cy=4, clampy=False))
        body += '<g filter="url(#kl)">%s</g>' % item
        rows = (min(rows[0], max(0, int(ty - tr * 1.9))), int(ty + tr * 1.9))
        if not out:                                                       # card gone: the same raster box as icons13, so the mark is identical
            rows = IC.scene(t, aspect)[1]
    if not body:
        return None, None
    return body, (rows[0], min(L["RH"], rows[1]))


def _kf(fid, r, col):
    return ('<filter id="%s" x="-25%%" y="-40%%" width="150%%" height="180%%"><feMorphology in="SourceAlpha" operator="dilate" radius="%.2f" result="d"/>'
            '<feFlood flood-color="%s"/><feComposite in2="d" operator="in" result="k"/><feMerge><feMergeNode in="k"/><feMergeNode in="SourceGraphic"/></feMerge>'
            '</filter>') % (fid, r, col)


# kl: icons13's light keyline (icons, title mark); kd: dark keyline outside the panel's paper outline (bright shots); k1: thin light keyline (chip icons)
DEFS = IC.DEFS.replace("</defs>", _kf("kd", 2.0, INK) + _kf("k1", 1.3, PAPER) + "</defs>")


def frame_svg(t, W, H, aspect="916", view=None):
    """-> (svg text, (x, y, w, h) in output pixels) or (None, None).  view = (x, y, w, h) in reference pixels (sheet)"""
    L = LAYOUT[aspect]
    body, rows = scene(t, aspect)
    if body is None:
        return None, None
    k = W / float(L["RW"])
    if view is None:
        py0, py1 = int(math.floor(rows[0] * k)), min(H, int(math.ceil(rows[1] * k)))
        box = (0, py0, W, py1 - py0)
        vb = (0, py0 / k, W / k, (py1 - py0) / k)
    else:
        box = (0, 0, W, H)
        vb = view
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.4f %.4f %.4f %.4f">%s%s</svg>' % (
        box[2], box[3], vb[0], vb[1], vb[2], vb[3], DEFS, body)
    return svg, box


# ------------------------------------------------------------------------------------------------ raster (Chromium)
class _Page(IC._Page):
    def request(self, job):
        if self.proc is None or self.proc.poll() is not None:
            env = dict(os.environ)
            env.setdefault("NODE_PATH", "/usr/local/lib/node_modules_global")
            self.proc = subprocess.Popen(["node", os.path.join(HERE, "raster_page.js")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         cwd=HERE, text=True, bufsize=1, env=env)
        IC._Page.request(self, job)


_PAGE = _Page()
atexit.register(_PAGE.stop)


def close():
    _PAGE.stop()


def raster(svg, w, h, bg=None):
    """SVG text -> RGBA uint8 (h, w, 4); cached in cache/<md5>.png"""
    from PIL import Image
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(("%s|%d|%d|%s" % (svg, w, h, bg)).encode("utf-8")).hexdigest()
    p = os.path.join(CACHE, key + ".png")
    if not os.path.exists(p):
        tmp = os.path.join(CACHE, "%s_%d.tmp.png" % (key, os.getpid()))
        _PAGE.request({"svg": svg, "w": w, "h": h, "out": tmp, "bg": bg})
        os.replace(tmp, p)
    return np.asarray(Image.open(p).convert("RGBA"))


def overlay(g, W, H, aspect="916"):
    """the card layer of film frame g at W x H: uint8 RGBA (H, W, 4), straight alpha, zeros where there is nothing"""
    out = np.zeros((H, W, 4), np.uint8)
    svg, box = frame_svg(g / float(FPS), W, H, aspect)
    if svg is not None:
        out[box[1]:box[1] + box[3], box[0]:box[0] + box[2]] = raster(svg, box[2], box[3])
    return out


def over(rgb, g, aspect=None):
    """composite the layer over an RGB uint8 frame (H, W, 3) -> RGB uint8"""
    H, W = rgb.shape[:2]
    aspect = aspect or ("916" if H > W else "169")
    svg, box = frame_svg(g / float(FPS), W, H, aspect)
    if svg is None:
        return rgb
    o = raster(svg, box[2], box[3]).astype(np.float32)
    out = rgb.copy()
    reg = out[box[1]:box[1] + box[3], box[0]:box[0] + box[2]].astype(np.float32)
    a = o[..., 3:4] / 255.0
    out[box[1]:box[1] + box[3], box[0]:box[0] + box[2]] = (reg * (1 - a) + o[..., :3] * a + 0.5).astype(np.uint8)
    return out


# ------------------------------------------------------------------------------------------------ cue table
def cue_table():
    """[(card, joins, leaves, [(film s, event), ...]), ...]"""
    r = lambda x: round(x, 3)
    o = LAYOUT["916"]["out"]
    return [
        ("radio", r(T.R_IN), o["radio"], [(r(T.R_IN), "card in: วิทยุกู้ภัย / กำลังติดต่อ, arcs follow the voice, green bar"),
                                          (r(T.R_CUT), "value -> สัญญาณขาด (red), bar red, card shakes, flat line + cut mark"), (o["radio"], "card leaves")]),
        ("battery", r(T.B_IN), o["battery"], [(r(T.B_IN), "card in: เครื่องตัดไร้สาย / 0/3 ขีด, green bar"), (T.B1, "1/3"), (T.B2, "2/3"), (T.B3, "3/3 + sub-line แบตเต็ม"),
                                              (r(T.P_IN - 7 * F), "shrinks into the chip [battery 3/3]"), (o["battery"], "chip leaves")]),
        ("calls", r(T.P_IN), o["calls"], [(r(T.P_IN), "card in: สายที่ไม่ได้รับ / 0 สาย, phone buzzes, red bar"), (r(T.P1), "1"), (r(T.P2), "2"), (r(T.P3), "3"),
                                          (r(T.P4), "4 (red)"), (r(T_DAUGHTER), "sub-line ลูกสาว"), (r(T.P_NAME), "sub-line ลูกสาว · น้ำเหนือ"),
                                          (r(T.H_IN - 7 * F), "shrinks into the chip [phone 4]"), (o["calls"], "chip leaves with the trust card")]),
        ("trust", r(T.H_IN), o["trust"], [(r(T.H_IN), "card in: ความเชื่อใจของลูก / 82 % + level bar"), (r(T.H_CASE), "sinks to 60 %"), (r(T.H_WAIT), "52 %"),
                                          (r(T.H_EVERY), "28 %"), (r(T.H_CRACK), "heart cracks"), (r(T.H_BACK), "17 %"), (r(T.H_SILENT), "7 %"),
                                          (T.H_END, "0 % -> value วางสาย (grey), bar and heart grey"), (T.H_SPLIT, "heart splits"),
                                          (32.21, "whole layer at 35 % until 32.70 (Kong's head passes)"), (o["trust"], "card + chip leave")]),
        ("danger", r(T.D_IN), o["danger"], [(r(T.D_IN), "card in: คนขับ / ชีพจรอ่อน, green heartbeat"), (r(T.D_LEAN), "value -> ไม่ตอบสนอง, bar and badge go amber"),
                                            (T.D_EYE, "value -> ติดเชื้อ! (red), red eye snaps open + burst"), (T.D_LUNGE, "card flashes red, shakes"),
                                            (o["danger"], "card leaves")]),
        ("countdown", r(T.C_IN), r(T.C_MORPH), [(r(T.C_IN), "card in: เหลือเวลา / 60 วินาที, amber bar"), (T.C_T0 + 1, "59"), (T.C_T0 + 2, "58"), (T.C_T0 + 3, "57"),
                                                (T.C_MORPH, "card dissolves, the stopwatch flies to the title spot and turns into the biohazard mark"),
                                                (T.TITLE, "title mark lands + burst, holds to the end")]),
    ]


if __name__ == "__main__":
    for row in cue_table():
        print(row[0], row[1], row[2])
        for e in row[3]:
            print("    %7.3f  %s" % e)
