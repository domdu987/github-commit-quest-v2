"""picto15.py -- DEAD ZONE 09 EP.1, status graphics v15: ONE big animated flat pictogram at the top-left.

    import picto15
    rgba = picto15.overlay(g, W, H, aspect='916')      # film frame g (0..1279) -> uint8 RGBA (H, W, 4), straight alpha
    rgb  = picto15.over(rgb_uint8, g)                   # composite over an RGB frame
    rows = picto15.cue_table()                          # [(pictogram, t_in, t_out, [(t, what), ...]), ...]

Same public API as v13/icons/icons13.py and v14/cards/cards14.py (overlay, over, cue_table, close, LAYOUT, T, DZ09_NARR).
User note this answers: "icons: less text, more picture, more movement, no background, easy on the eyes, prettier".
  * no panel / card / bar behind anything: the pictogram alone, flat, with one off-white keyline round its silhouette;
  * no words; a number only where the number is the story (missed-call badge 1-4, countdown 60-57);
  * one HERO pictogram (about 160 px at 720 wide) + at most one small companion;
  * every pictogram moves all the time (idle breathing) and acts out its story beat on the cue.
Cue times, easing, palette and the title mark come from icons13 (imported, not copied).  From T.TITLE - 1 frame on the
layer is icons13's own title mark, pixel for pixel.
Raster: SVG -> one headless Chromium page (raster_page.js), cached on disk by SVG hash.
"""
import atexit, hashlib, json, math, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
os.environ.setdefault("DZ09_NARR", "narr_ohm")
sys.path.insert(0, os.path.join(PROJ, "v13", "icons"))
import icons13 as IC                                      # cue times, easing, palette, title mark (read only)
from icons13 import (T, FPS, NF, F, INK, PAPER, RED, AMBER, GREEN, ORANGE, GREY, SLOT, BLUE, clamp, u, eio, eo, ei, back, spring, kick,
                     decay, seg, mix, rnd, shot_of, cap, level, trust_level, count_number)

NARR = IC.NARR
CACHE = os.path.join(HERE, "cache")
SICK = "#9fd356"                                          # the driver's sickly green (heartbeat trace)
SCREEN = "#232a40"                                        # dark glass (radio display, monitor)
DEEP = "#b3202f"                                          # the red, one step down (liquid behind, iris rim)
W1, W2, W3 = 4.6, 3.0, 1.9                                # the three stroke weights, pictogram units
KEY = 2.6                                                 # off-white keyline outside the silhouette, reference pixels
LUNGE_G = int(math.ceil((T.D_LUNGE + 2.0 / 24) * FPS - 1e-6))   # 1045: the film's own white / red frame (v10/film/cues.LUNGE_FLASH)

# ------------------------------------------------------------------------------------------------ layout
# reference frames 720x1280 (9:16) and 1280x720 (16:9).  (x0, y) = left edge / centre line of the hero pictogram,
# s = scale of the whole layer.  shift = {shot: (x0, y)} moves the pictogram for one whole shot; dodge = [(t0, t1, dx, dy)]
# glides it aside (reference px, eased over 6 frames) while a face is under it; fade = [(t0, t1, opacity)];
# out = leave times; title = (x, y, radius) of the title mark (icons13's).
LAYOUT = {
    # 9:16 shift S08 + S09: Kong's large foreground face fills the top-left of S09 (x 0-270), so the battery plays at x 292 (dark sky beside him)
    "916": dict(RW=720, RH=1280, x0=36, y=186, s=1.0, shift={"S08": (292, 186), "S09": (292, 186)}, dodge=[], fade=list(IC.LAYOUT["916"]["fade"]), title=IC.LAYOUT["916"]["title"],
                out=dict(radio=6.40, battery=19.30, calls=33.00, trust=33.00, danger=45.90)),
    "169": dict(RW=1280, RH=720, x0=64, y=120, s=0.64, shift={}, dodge=[], fade=[], title=IC.LAYOUT["169"]["title"],
                out=dict(radio=6.40, battery=19.30, calls=33.00, trust=33.00, danger=45.90)),
}
#            px per unit, centre offset from (x0, y) in px (at s = 1)
HERO = dict(radio=(1.75, 52, 6), battery=(1.72, 56, 6), calls=(1.70, 96, 11), trust=(1.80, 90, -5), danger=(2.0, 102, 2), countdown=(1.74, 74, 2))
COMP = dict(battery=(0.74, 236, 34), calls=(0.80, 214, 34))      # the small companion beside the next hero
LEAVE = dict(radio=(0, 12), battery=(28, 0), calls=(0, 18), trust=(0, 0), danger=(0, 12))   # where a pictogram drifts while it fades out


# ------------------------------------------------------------------------------------------------ svg helpers
def S(w=W1, c=INK):
    return 'stroke="%s" stroke-width="%.2f" stroke-linejoin="round" stroke-linecap="round"' % (c, w)


def rr(x, y, w, h, r, fill, sw=W1, c=INK):
    st = S(sw, c) if sw else ""
    return '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" %s/>' % (x, y, w, h, r, fill, st)


def ci(cx, cy, r, fill, sw=W1, c=INK):
    st = S(sw, c) if sw else ""
    return '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" %s/>' % (cx, cy, max(r, 0), fill, st)


def ln(x1, y1, x2, y2, sw=W1, c=INK):
    return '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" %s/>' % (x1, y1, x2, y2, S(sw, c))


def pa(d, fill="none", sw=W1, c=INK, extra=""):
    st = S(sw, c) if sw else ""
    return '<path d="%s" fill="%s" %s %s/>' % (d, fill, st, extra)


def ln2(x1, y1, x2, y2, col, w=4.0, o=3.0):
    """a coloured stroke with the ink outline round it"""
    return ln(x1, y1, x2, y2, w + o, INK) + ln(x1, y1, x2, y2, w, col)


def pa2(d, col, w=4.0, o=3.0):
    return pa(d, "none", w + o, INK) + pa(d, "none", w, col)


def G(inner, x=0.0, y=0.0, sx=1.0, sy=None, rot=0.0, op=None, px=0.0, py=0.0):
    """group: scale / rotate about the pivot (px, py), then move by (x, y)"""
    sy = sx if sy is None else sy
    o = ' opacity="%.3f"' % op if op is not None and op < 0.999 else ""
    return '<g%s transform="translate(%.2f %.2f) rotate(%.2f) scale(%.4f %.4f) translate(%.2f %.2f)">%s</g>' % (o, x + px, y + py, rot, sx, sy, -px, -py, inner)


def poly(pts, fill, sw=W3, c=INK):
    return '<polygon points="%s" fill="%s" %s/>' % (" ".join("%.2f,%.2f" % p for p in pts), fill, S(sw, c) if sw else "")


def fleck(x, y, r, rot, col, kind=0, sw=W3):
    """a small flat particle: diamond (0) or shard triangle (1)"""
    if r < 1.3:
        return ""
    r *= 1.45
    pts = [(0, -r), (0.72 * r, 0), (0, r), (-0.72 * r, 0)] if kind == 0 else [(0, -1.25 * r), (0.75 * r, 0.8 * r), (-0.7 * r, 0.55 * r)]
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return poly([(x + px * c - py * s, y + px * s + py * c) for px, py in pts], col, min(1.7, r * 0.3))


def drop(x, y, r, col, sw=W3):
    """teardrop, point up; (x, y) = centre of the round end"""
    if r < 0.5:
        return ""
    d = "M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f A%.2f %.2f 0 1 1 %.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f Z" % (
        x, y - 2.3 * r, x + 0.45 * r, y - 1.3 * r, x + r, y - 0.6 * r, x + r, y, r, r, x - r, y, x - r, y - 0.6 * r, x - 0.45 * r, y - 1.3 * r, x, y - 2.3 * r)
    return pa(d, col, min(sw, r * 0.8))


PARTS = []                                                # loose particles of the pictogram being drawn: laid over it WITHOUT the keyline


def sparks(t, t0, n, x0, y0, col, seed, a0=-70, a1=70, v=70.0, grav=110.0, life=0.42, r=4.2, col2=None, rx=0.0, ry=0.0, vy=1.0):
    """n flat flecks thrown from (x0, y0) into the angle range a0..a1 (deg, 0 = right, -90 = up); they fall and shrink away"""
    x = t - t0
    if x <= 0 or x >= life * 1.3:
        return ""
    s = ""
    for i in range(n):
        li = life * (0.75 + 0.25 * (rnd(seed, i) + 1))
        if x >= li:
            continue
        an = math.radians(a0 + (a1 - a0) * (i + 0.5 + 0.35 * rnd(seed + 3, i)) / n)
        vi = v * (0.7 + 0.3 * (rnd(seed + 5, i) + 1))
        dx = math.cos(an) * vi * (1 - math.exp(-3.2 * x)) / 3.2 * 1.9
        dy = vy * math.sin(an) * vi * (1 - math.exp(-3.2 * x)) / 3.2 * 1.9 + 0.5 * grav * x * x
        s += fleck(x0 + dx + rx * math.cos(an), y0 + dy + ry * math.sin(an), r * (0.75 + 0.25 * rnd(seed + 7, i)) * (1 - ei(x / li)), 200 * x * rnd(seed + 9, i) + 40 * i,
                   col2 if (col2 and i % 2) else col, i % 2)
    PARTS.append(s)
    return ""


def num(s, x, y, size, col, sw=0.0, anchor="middle"):
    """a digit readout (Kanit Black); sw > 0 puts the ink outline round the glyphs"""
    ex = 'stroke="%s" stroke-width="%.2f" stroke-linejoin="round" paint-order="stroke"' % (INK, sw) if sw > 0 else ""
    return '<text x="%.2f" y="%.2f" font-family="Kanit" font-weight="900" font-size="%.2f" text-anchor="%s" fill="%s" %s>%s</text>' % (x, y, size, anchor, col, ex, s)


def wob(t, f=0.45, k=0):
    """slow idle sway, -1..1"""
    return math.sin(2 * math.pi * (f * t + 0.31 * k))


# ------------------------------------------------------------------------------------------------ 1 radio
def radio(t):
    """walkie-talkie.  body x -27..22, y -51..48; the signal arcs run to x 66"""
    g = int(round(t * FPS))
    x = t - T.R_CUT
    dead = x >= 0
    lv = level(t)
    jit = 0.0 if dead else max(decay(t, T.R_WAIT, 3.2) * 0.6 * (t >= T.R_WAIT), decay(t, T.R_HEY, 2.6) * (t >= T.R_HEY))
    k = kick(t, T.R_WAIT, 5, 8) * 0.5 + kick(t, T.R_HEY, 5, 7) * 0.9 + kick(t, T.R_CUT, 4, 7)
    pin = clamp(spring(t, T.R_IN, 2.4, 6.5), 0, 1.06)
    hop = -8 * math.exp(-5 * max(t - T.R_IN, 0)) * abs(math.cos(2 * math.pi * 2.1 * (t - T.R_IN)))          # bounces as it lands
    droop = eio(u(x, 0.45, 1.25)) if dead else 0.0
    talk = 0.035 * lv * (0 if dead else 1)
    br = 0.012 * wob(t, 0.5)
    sx, sy = pin * (1 + 0.07 * k + br + talk), pin * (1 - 0.07 * k - br + talk)
    sig = mix(mix(PAPER, AMBER, u(t, T.R_WAIT, T.R_WAIT + 2 * F)), RED, u(t, T.R_HEY, T.R_HEY + 2 * F))
    wipe = eio(u(x, 0.55, 1.35)) if dead else 0.0                                 # the colour drains out, top to bottom

    def fills(col):
        s = rr(-22, -14, 44, 62, 9, col, 0)
        s += '<rect x="-22" y="34" width="44" height="14" fill="%s" clip-path="url(#rb)"/>' % mix(col, INK, 0.22)
        s += rr(-17.5, -9, 4.2, 40, 2.1, mix(col, PAPER, 0.42), 0)                # flat highlight
        return s

    # antenna: bends with every move, hangs over when dead
    aw = 5 * kick(t, T.R_IN + 0.1, 2.6, 4.5) + 5 * k + 3 * jit * rnd(g, 5) + 1.0 * wob(t, 0.7) + 15 * droop + 2.2 * droop * wob(t, 0.35)
    ax, ay = -11 + aw, -47 + 9 * droop + 0.12 * abs(aw)
    b = '<clipPath id="rb"><rect x="-22" y="-14" width="44" height="62" rx="9"/></clipPath>'
    b += pa("M-11 -13 Q-11 -31 %.2f %.2f" % (ax, ay), "none", 5.4)
    b += ci(ax, ay, 3.5, mix(ORANGE, GREY, wipe), W2)
    b += rr(3, -22, 12, 9, 2.5, INK, W2)                                          # channel knob
    b += rr(-27, 4, 6, 17, 2.4, INK, 0)                                           # push-to-talk key
    b += fills(ORANGE)
    if wipe > 0:
        b += '<clipPath id="rw"><rect x="-30" y="-20" width="60" height="%.2f"/></clipPath><g clip-path="url(#rw)">%s</g>' % (6 + 64 * wipe, fills(GREY))
    b += rr(-22, -14, 44, 62, 9, "none")
    # display: five level bars that follow the voice
    b += rr(-13, -7, 26, 17, 3.6, SCREEN, W2)
    bc = sig if sig != PAPER else GREEN
    for i in range(5):
        if dead:
            h = 1.6 + 5 * decay(t, T.R_CUT, 7) * abs(rnd(g, 60 + i))
            col = mix(RED, GREY, u(x, 0.5, 1.2))
        else:
            h = 1.8 + 9.5 * clamp(level(t - 0.03 * i) * (0.55 + 0.45 * abs(math.sin(1.7 * i + 7.0 * t))) + 0.5 * jit * abs(rnd(g, 70 + i)))
            col = bc
        b += '<rect x="%.2f" y="%.2f" width="2.9" height="%.2f" rx="1.2" fill="%s"/>' % (-9.6 + i * 4.1, 7.2 - h, h, col)
    for yy in (19, 26, 33):
        b += ln(-9, yy, 9, yy, W2)                                                 # speaker grille
    # the cut: a red slash snaps across the body
    if dead:
        pr = back(u(x, 2 * F, 5 * F), 1.4) if x < 5 * F else 1.0
        if pr > 0.02:
            A, B = (31.0, -34.0), (-31.0, 46.0)
            b += G(ln2(A[0], A[1], A[0] + (B[0] - A[0]) * pr, A[1] + (B[1] - A[1]) * pr, RED, 6.4, 3.2), rot=7 * kick(t, T.R_CUT + 4 * F, 4, 8), px=0, py=6)
    s = G(b, rnd(g, 1) * 2.0 * jit, hop + rnd(g, 2) * 2.0 * jit + 1.5 * droop, sx, sy, 5 * k + rnd(g, 3) * 2.5 * jit - 8 * droop, px=0, py=48)
    # ---- the signal: three arcs to the right, breathing with the voice
    cx, cy = 28.0, -5.0
    if not dead:
        ain = clamp(spring(t, T.R_IN + 4 * F, 2.4, 8), 0, 1.25)
        for i, r in enumerate((13, 25, 37)):
            lvi = level(t - 0.07 * i)                                              # the voice travels outwards
            w = 2.7 + 3.4 * lvi + 1.6 * jit
            rrad = r * ain * (0.93 + 0.10 * lvi) + rnd(g, 10 + i) * 3.0 * jit
            a = math.radians(40 + rnd(g, 20 + i) * 10 * jit)
            ox, oy = cx + rnd(g, 30 + i) * 2.5 * jit, cy + hop * 0.5 + rnd(g, 40 + i) * 3.5 * jit
            if rrad < 3:
                continue
            s += pa2("M%.2f %.2f A%.2f %.2f 0 0 1 %.2f %.2f" % (ox + rrad * math.cos(a), oy - rrad * math.sin(a), rrad, rrad,
                                                             ox + rrad * math.cos(a), oy + rrad * math.sin(a)), sig, w, 3.0)
    else:
        # the arcs shatter: twelve fragments fly off, tumble, fall and shrink away
        for i, r in enumerate((13, 25, 37)):
            for j in range(4):
                sd = i * 4 + j
                life = 0.50 + 0.14 * (rnd(sd, 1) + 1)
                if x >= life:
                    continue
                am = math.radians(-30 + 20 * j)
                hl = r * math.sin(math.radians(10)) * (1 - ei(x / life))
                vx, vy = math.cos(am) * (34 + 14 * rnd(sd, 2)), math.sin(am) * 36 - 26 + 16 * rnd(sd, 3)
                e = (1 - math.exp(-3.0 * x)) / 3.0 * 1.8
                px, py = cx + r * math.cos(am) + vx * e, min(cy + r * math.sin(am) + vy * e + 0.5 * 230 * x * x, 54)
                ro = am + math.pi / 2 + math.radians(420 * rnd(sd, 4) * x)
                if hl > 0.6:
                    PARTS.append(ln2(px - hl * math.cos(ro), py - hl * math.sin(ro), px + hl * math.cos(ro), py + hl * math.sin(ro), mix(RED, GREY, u(x, 0.25, 0.6)), 3.8, 2.2))
        # afterwards, about once a second, one small grey arc tries to get out and dies
        if x > 1.5:
            ph = ((x - 1.5) % 1.25) / 0.55
            if ph < 1:
                r = 8 + 9 * eo(ph)
                a = math.radians(38)
                s += G(pa2("M%.2f %.2f A%.2f %.2f 0 0 1 %.2f %.2f" % (r * math.cos(a), -r * math.sin(a), r, r, r * math.cos(a), r * math.sin(a)),
                           GREY, 3.2 * math.sin(math.pi * ph) ** 0.6, 2.4 * math.sin(math.pi * ph) ** 0.6), cx - 2, cy + 6, rot=-8)
    return s


# ------------------------------------------------------------------------------------------------ 2 battery
BOLT = [(3, -17), (-9, 2), (-1.5, 2), (-4, 17), (9, -3), (1.5, -3)]


def battery(t, small=0.0):
    """upright battery, three cells.  x -27..27, y -46..46"""
    tb = (T.B1, T.B2, T.B3)
    drop_in = 1 - eo(u(t, T.B_IN, T.B_IN + 5 * F))
    land = T.B_IN + 5 * F
    k = kick(t, land, 3.6, 8) * 1.2 + sum(kick(t, x, 4.5, 10) for x in tb[:2]) * 0.7 + kick(t, T.B3, 4, 8)
    jump = -7 * math.sin(math.pi * u(t, T.B3 + 0.22, T.B3 + 0.50)) ** 0.8                      # the satisfied hop
    k += 1.1 * kick(t, T.B3 + 0.50, 3.4, 8)
    br = 0.014 * wob(t, 0.5)
    jolt = sum(-3.5 * decay(t, x, 16) * (t >= x) for x in tb)
    b = rr(-10, -46, 20, 12, 3.5, INK, W2)                                         # terminal
    b += rr(-27, -37, 54, 83, 11, PAPER)
    b += rr(-21.5, -30, 3.6, 68, 1.8, "#ffffff", 0)                                # flat glass highlight
    for i in range(3):
        b += rr(-16, 19 - i * 24, 34, 20, 4, SLOT, 0)
    cells = ""
    for i in range(3):
        if t < tb[i] - 3 * F:
            continue
        fly = 1 - ei(u(t, tb[i] - 3 * F, tb[i]))                                    # slams in from the right
        q = decay(t, tb[i], 9) * math.cos(2 * math.pi * 3.4 * (t - tb[i])) if t >= tb[i] else -0.25 * (1 - fly) * 0
        c = rr(-16, 19 - i * 24, 34, 20, 4, GREEN, W2) + rr(-12.5, 22.5 - i * 24, 3.2, 13, 1.6, mix(GREEN, PAPER, 0.55), 0)
        cells += G(c, 36 * fly, 0, 1 - 0.24 * q, 1 + 0.20 * q, px=-16, py=29 - i * 24)
    b += cells
    full = t - T.B3
    if full > 0.08:                                                                 # the bolt: pops, blinks once, then breathes
        z = clamp(spring(t, T.B3 + 0.08, 3.0, 8), 0, 1.3) * (1 + 0.05 * wob(t, 0.8))
        on = not (0.38 <= full < 0.38 + 1.5 * F)
        if on:
            b += G(poly(BOLT, AMBER, W2), 1, 5, z, rot=-6 + 5 * kick(t, T.B3 + 0.08, 3, 6))
    s = G(b, jolt, -13 * drop_in + jump, 1 + 0.07 * k + br, 1 - 0.07 * k - br, px=0, py=46)
    for i in range(3):
        s += sparks(t, tb[i], 5 if i < 2 else 8, 22, 29 - i * 24, GREEN, 100 + i, a0=-60, a1=60, v=42 if i < 2 else 52, r=5.0, col2=mix(GREEN, PAPER, 0.55), rx=6)
        s += sparks(t, tb[i], 3, -20, 29 - i * 24, GREEN, 140 + i, a0=150, a1=215, v=60, r=4.4, rx=8)
    return s


# ------------------------------------------------------------------------------------------------ 3 missed calls
def phone(t, small=0.0):
    """smartphone with an incoming call on its screen and a red count badge.  body x -23..27, y -42..42; badge to y -54"""
    g = int(round(t * FPS))
    counts = (T.P1, T.P2, T.P3, T.P4)
    n = sum(1 for c in counts if t >= c)
    off = eio(u(t, T.H_END, T.H_END + 0.3))                                         # the call is over: the screen goes dark
    buzz = max([0.0] + [math.sin(math.pi * u(t, c - 0.05, c + 0.32)) for c in counts])
    buzz = max(buzz, 0.45 * math.sin(math.pi * u(t, T.P_IN + 0.02, T.P1 - 0.06)) ** 0.5)
    if T.P4 + 0.6 < t < T.H_IN - 0.25:                                               # it keeps ringing: a short buzz every 1.3 s
        buzz = max(buzz, 0.55 * math.sin(math.pi * clamp(((t - T.P4 - 0.6) % 1.3) / 0.42)))
    buzz *= 1 - small
    rot = 8.5 * buzz * math.sin(2 * math.pi * 6 * t)
    k = sum(kick(t, c, 4.5, 9) for c in counts) + 0.8 * kick(t, T.H_END, 3, 7)
    pin = clamp(spring(t, T.P_IN, 2.6, 8), 0, 1.12)
    br = 0.012 * wob(t, 0.5, 1)
    scr = mix(BLUE, SCREEN, off)
    b = rr(22, -22, 5, 14, 2, INK, 0)                                               # side key
    b += rr(-23, -42, 46, 84, 9.5, PAPER)
    b += '<clipPath id="ps"><rect x="-18" y="-33" width="36" height="62" rx="4"/></clipPath>'
    b += rr(-18, -33, 36, 62, 4, scr, 0)
    b += '<polygon points="-18,-33 0,-33 -18,3" fill="%s" clip-path="url(#ps)"/>' % mix(scr, PAPER, 0.30)      # flat glass highlight
    if off < 0.5:
        ring = 1 + 0.10 * math.sin(2 * math.pi * 1.6 * t) * (1 - small)
        b += '<clipPath id="pc"><circle cx="0" cy="-12" r="9"/></clipPath>' + ci(0, -12, 9.5, PAPER, 0) + ci(0, -15.2, 3.4, INK, 0)
        b += '<ellipse cx="0" cy="-3.2" rx="6.6" ry="5.2" fill="%s" clip-path="url(#pc)"/>' % INK + ci(0, -12, 9.5, "none", W3)   # the caller
        b += ci(-8.5, 15, 5.2, RED, W3) + G(ci(0, 0, 5.2, GREEN, W3), 8.5, 15, ring)
    b += rr(-18, -33, 36, 62, 4, "none", W2)
    b += ln(-5, -37.6, 5, -37.6, W3) + ln(-6, 35.6, 6, 35.6, W2)
    s = ""
    # vibration ticks and ring waves
    if buzz > 0.04:
        for sd in (-1, 1):
            for j, r in enumerate((31, 39)):
                if sd > 0 and j == 1:
                    continue
                a = math.radians(22 - 5 * j)
                w = 3.0 * clamp(buzz * 1.5) * (1 - 0.25 * j)
                if w > 0.5:
                    s += pa2("M%.2f %.2f A%.2f %.2f 0 0 %d %.2f %.2f" % (sd * r * math.cos(a), 8 - r * math.sin(a), r, r, 1 if sd > 0 else 0,
                                                                     sd * r * math.cos(a), 8 + r * math.sin(a)), PAPER, w, w * 0.8)
    if small < 0.5:
        for c in counts:
            xx = u(t, c, c + 0.5)
            if 0 < xx < 1:
                r, a = 34 + 22 * eo(xx), math.radians(30)
                w = 3.4 * (1 - xx) ** 0.8
                s += pa2("M%.2f %.2f A%.2f %.2f 0 0 0 %.2f %.2f" % (-r * math.cos(a), 4 - r * math.sin(a), r, r, -r * math.cos(a), 4 + r * math.sin(a)), RED, w, min(2.4, w * 0.5))
    s = G(b, 1.6 * buzz * math.sin(2 * math.pi * 6 * t + 1), 0, pin * (1 + 0.05 * k + br), pin * (1 - 0.05 * k - br), rot, px=0, py=10) + s
    # the badge: pops and flips its number on every count
    if n > 0:
        last = max(c for c in counts if t >= c)
        pop = 1 + 0.32 * decay(t, last, 10) * math.cos(2 * math.pi * 3.2 * (t - last))
        bx, by = 21.0, -39.5
        ra = math.radians(rot)
        bx, by = bx * math.cos(ra) - (by - 10) * math.sin(ra), 10 + bx * math.sin(ra) + (by - 10) * math.cos(ra)
        fl = u(t, last, last + 5 * F)
        d = '<clipPath id="pb"><circle r="10.8"/></clipPath>' + ci(0, 0, 12.6, RED, 4.0) + '<g clip-path="url(#pb)">'
        if fl < 1 and n > 1:
            d += num(str(n - 1), 0, 7.8 - 24 * ei(fl), 21.5, PAPER)
            d += num(str(n), 0, 7.8 + 24 * (1 - back(fl, 1.6)), 21.5, PAPER)
        else:
            d += num(str(n), 0, 7.8, 21.5, PAPER)
        d += '</g>'
        s += G(d, bx, by, pop, rot=rot * 0.5)
        s += sparks(t, T.P4 + F, 7, 22, -39, RED, 200, a0=-75, a1=60, v=50, grav=120, r=4.2, col2=mix(RED, PAPER, 0.45), rx=15, ry=12, vy=0.5) if small < 0.5 else ""
    return s


# ------------------------------------------------------------------------------------------------ 4 trust
HEART = IC.HEART
CRACK = IC.CRACK
_HP = None


def _drains():
    return [T.H_CASE + 0.05, T.H_WAIT, T.H_EVERY + 0.05, T.H_BACK, T.H_SILENT, T.H_END]


def _hbeat(t):
    """heart beat phase (cycles): the beat slows as the level falls and stops when the call ends"""
    global _HP
    if _HP is None:
        ts = np.arange(T.H_IN, T.H_END + 0.8, 1 / 240.0)
        rate = np.array([0.74 + 0.72 * trust_level(x) for x in ts]) * (1 - np.clip((ts - T.H_END) / 0.45, 0, 1))
        _HP = (ts, np.cumsum(rate) / 240.0)
    return float(np.interp(t, _HP[0], _HP[1]))


def heart(t):
    """a glass heart with red liquid.  x -45..45, y -41..38"""
    lv = trust_level(t)
    moving = clamp(abs(trust_level(t + 0.04) - trust_level(t - 0.04)) * 14)
    dead = eio(u(t, T.H_END, T.H_END + 0.35))
    col, col2 = mix(RED, GREY, dead), mix(DEEP, GREY, dead)
    face = mix(PAPER, SLOT, dead)
    ph = _hbeat(t) % 1.0
    beat = (math.exp(-((ph - 0.12) / 0.075) ** 2) + 0.55 * math.exp(-((ph - 0.40) / 0.085) ** 2)) * (1 - dead)
    k = kick(t, T.H_CRACK, 4, 8) + kick(t, T.H_END, 3.5, 8) * 0.7 - 0.5 * math.sin(math.pi * u(t, T.H_SPLIT - 4 * F, T.H_SPLIT))
    pin = clamp(spring(t, T.H_IN, 2.5, 7), 0, 1.10)
    sag = 0.04 * dead
    slosh = sum(kick(t, d + 0.04, 1.5, 2.4) * (0.6 if i in (1,) else 1.0) for i, d in enumerate(_drains()[:5])) + 0.5 * kick(t, T.H_IN + 0.15, 1.6, 2.6)
    sp = t - T.H_SPLIT
    inner = '<clipPath id="hc"><path d="%s"/></clipPath><path d="%s" fill="%s"/>' % (HEART, HEART, face)
    if lv > 0.004:
        ys = 38 - lv * 79
        amp = 1.5 + 3.6 * moving + 0.9 * beat
        tilt = math.tan(math.radians(clamp(13 * slosh, -16, 16)))
        liq = ""
        for layer, (c, phs, spd, dy) in enumerate(((col2, 1.9, -0.9, -2.6), (col, 0.0, 1.25, 0.0))):
            pts = ["-52 60"]
            for i in range(0, 27):
                xx = -52 + i * 4
                pts.append("%.2f %.2f" % (xx, ys + dy + xx * tilt * (0.8 if layer == 0 else 1) + amp * math.sin(2 * math.pi * (xx / 44.0 + t * spd) + phs)))
            pts.append("52 60")
            liq += '<path d="M%s Z" fill="%s"/>' % (" L".join(pts), c)
        for i in range(3):                                                           # bubbles
            cyc = (t * (0.33 + 0.05 * i) + 0.37 * i) % 1.0
            bx, by = -16 + 15 * i + 2.5 * math.sin(2 * math.pi * (t * 0.8 + i)), 34 - cyc * 62
            if by > ys + 6 and dead < 0.3:
                liq += ci(bx, by, (1.5 + 0.5 * i) * math.sin(math.pi * clamp(cyc * 4, 0, 0.5)), mix(col, PAPER, 0.45), 0)
        inner += '<g clip-path="url(#hc)">%s</g>' % liq
    inner += pa("M-34 -17 C-35 -27 -29 -34 -20 -34.5", "none", 4.0, "#ffffff", 'opacity="0.8"')        # flat glass highlight
    inner += ci(-35.5, -8, 1.9, "#ffffff", 0)
    inner += pa(HEART, "none", 5.0)
    # crack: grows from the notch, with two side branches
    cr = eo(u(t, T.H_CRACK, T.H_CRACK + 5 * F)) * 0.45 + eio(u(t, T.H_BACK, T.H_BACK + 0.5)) * 0.15 + eio(u(t, T.H_SILENT, T.H_SILENT + 0.5)) * 0.12 + eo(u(t, T.H_END, T.H_END + 5 * F)) * 0.28
    npt = cr * (len(CRACK) - 1)
    cp = []
    for i, p in enumerate(CRACK):
        if i <= npt:
            cp.append(p)
        elif i - 1 < npt:
            a, f = CRACK[i - 1], npt - (i - 1)
            cp.append((a[0] + (p[0] - a[0]) * f, a[1] + (p[1] - a[1]) * f))
    crack = pa("M" + " L".join("%.2f %.2f" % p for p in cp), "none", 3.6) if len(cp) > 1 else ""
    if npt > 1.3:
        f = clamp(npt - 1.3)
        crack += ln(-8, -13, -8 - 9 * f, -13 + 5 * f, W3 + 0.5)
    if npt > 2.4:
        f = clamp(npt - 2.4)
        crack += ln(6, -3, 6 + 8 * f, -3 + 6 * f, W3 + 0.5)
    s = ""
    if sp <= 0:
        sc = pin * (1 + 0.05 * beat - sag)
        s += G(inner + crack, 0, 2 * dead, sc * (1 + 0.07 * k), sc * (1 - 0.07 * k), rot=1.2 * wob(t, 0.3) * (1 - dead), px=0, py=38)
    else:
        # splits: the halves swing apart about the tip, hang, then drop
        zz = " ".join("%.2f,%.2f" % p for p in CRACK)
        sw = clamp(spring(t, T.H_SPLIT, 2.0, 5.5), 0, 1.6)
        fx = max(t - 32.74, 0.0)
        for sd, name in ((-1, "hl"), (1, "hr")):
            clip = '<clipPath id="%s"><polygon points="%s %d,70 %d,-70 0,-70"/></clipPath>' % (name, zz, sd * 80, sd * 80)
            half = '%s<g clip-path="url(#%s)">%s</g>%s' % (clip, name, inner, pa("M" + " L".join("%.2f %.2f" % p for p in CRACK), "none", 3.6))
            s += G(half, sd * (2.5 * sw + 12 * fx), 2 + 0.5 * 190 * fx * fx * (1.0 if sd < 0 else 0.8), 1 - sag,
                   rot=sd * (13 if sd < 0 else 9) * sw + sd * 90 * fx * fx + 1.5 * wob(t, 0.9, sd), px=0, py=38)
        s += sparks(t, T.H_SPLIT, 7, 0, -4, GREY, 330, a0=-160, a1=-20, v=70, grav=160, r=4.8, col2=SLOT, rx=10, ry=22, vy=0.5)
    s += sparks(t, T.H_CRACK, 5, 0, -24, PAPER, 310, a0=-150, a1=-30, v=55, grav=140, r=4.2, rx=9, ry=10, vy=0.4)
    # droplets leave the tip whenever the level falls
    for i, d in enumerate(_drains()):
        for j in range(2 if i in (1, 4) else 3):
            t0 = d + 0.12 + 0.30 * j
            xx = t - t0
            if 0 < xx < 0.58 and t < T.H_SPLIT:
                hang = eo(u(xx, 0, 0.22))
                fall = max(xx - 0.22, 0)
                yy = 40 + 3.0 * hang + 0.5 * 230 * fall * fall
                s += drop(rnd(i, j) * 2.5, yy, 3.4 * hang * (1 - ei(u(fall, 0.10, 0.34))), RED if d < T.H_END else GREY)
    return s


# ------------------------------------------------------------------------------------------------ 5 danger
HB = IC.HB                                                # the two heartbeat thumps of the mix (38.827, 40.827)
ECG = ([-0.17, -0.13, -0.08, -0.04, -0.022, 0.0, 0.030, 0.056, 0.13, 0.20, 0.28], [0, -3.2, 0, 0, 3.2, -22, 8.5, 0, 0, -5.5, 0])
SWEEP, SPAN = 1.6, 54.0                                   # the trace is drawn left to right once every SWEEP seconds


def _beats():
    """[(time, strength)]: the beat slows and weakens; the last two fall on the thumps of the mix"""
    t0 = T.D_IN + 0.62
    n = 5
    ts = [t0 + (HB[0] - t0) * i / float(n - 1) for i in range(n)]
    return list(zip(ts + [HB[1]], [1.0, 1.0, 0.90, 0.76, 0.58, 0.30]))


def _ecg(tt):
    v = 0.0
    for b, a in _beats():
        d = tt - b
        if -0.17 < d < 0.28:
            v += a * float(np.interp(d, ECG[0], ECG[1]))
    return v


def _almond(m, h, r=40.0):
    """outline: circle of radius r (m = 0) -> almond eye of half height h (m = 1)"""
    pts = []
    for i in range(72):
        th = 2 * math.pi * i / 72.0
        c, sn = math.cos(th), math.sin(th)
        x1, y1 = 47 * c, h * sn * abs(sn) * (1.0 if sn < 0 else 0.82)
        pts.append((r * c + (x1 - r * c) * m, r * sn + (y1 - r * sn) * m))
    return "M" + " L".join("%.2f %.2f" % p for p in pts) + " Z"


VEINS = [[(-46, 0), (-37, -5), (-30, -3), (-23, -7)], [(-44, 3), (-36, 7), (-29, 5)], [(-37, -5), (-33, -11), (-27, -13)],
         [(46, 1), (38, 6), (31, 4), (24, 8)], [(44, -3), (36, -8), (29, -7)], [(38, 6), (34, 12), (28, 13)]]


def _partial(pts, f):
    out = [pts[0]]
    n = f * (len(pts) - 1)
    for i in range(1, len(pts)):
        if i <= n:
            out.append(pts[i])
        elif i - 1 < n:
            a, q = pts[i - 1], n - (i - 1)
            out.append((a[0] + (pts[i][0] - a[0]) * q, a[1] + (pts[i][1] - a[1]) * q))
    return out


def danger_color(t):
    return mix(SICK, AMBER, eio(u(t, T.D_LEAN + 0.2, T.D_DRIVER)))


def danger(t):
    """a round heart monitor whose line goes flat, shuts into an eyelid and opens as the red eye.  r 40 / almond 94 x 56"""
    g = int(round(t * FPS))
    if t < T.D_EYE:
        return _monitor(t, g)
    return _eye(t, g)


def _monitor(t, g):
    col = danger_color(t)
    m = eio(u(t, T.D_EYE - 5 * F, T.D_EYE - 1 * F))                                   # disc -> closed lid
    pin = clamp(spring(t, T.D_IN, 2.5, 7), 0, 1.10)
    bt = _beats()
    pulse = sum(a * decay(t, b, 7) for b, a in bt if t >= b)
    last = max([b for b, a in bt if t >= b] or [-1e9])
    d = _almond(m, 7.0)
    face = mix(PAPER, PAPER, m)
    s = pa(d, face)
    if m < 1:
        k = 1 - m
        s += '<clipPath id="ms"><ellipse rx="%.2f" ry="%.2f"/></clipPath>' % (31.5 + 12 * m, 31.5 * k)
        s += '<ellipse rx="%.2f" ry="%.2f" fill="%s" %s/>' % (31.5 + 12 * m, 31.5 * k, mix(SCREEN, PAPER, ei(m)), S(W2))
        sc = '<g clip-path="url(#ms)">'
        grid = mix(SCREEN, col, 0.30)
        for yy in (-14, 0, 14):                                                       # faint dotted graticule
            sc += '<line x1="-30" y1="%d" x2="30" y2="%d" stroke="%s" stroke-width="1.3" stroke-dasharray="1.4 5.2" stroke-linecap="round"/>' % (yy, yy, grid)
        # the sweep: a head runs left to right and draws the trace; the part ahead of it is the oldest and is wiped
        fr_ = ((t - T.D_IN) / SWEEP) % 1.0
        xh = -27 + SPAN * fr_
        runs, cur = [], []
        x = -27.0
        while x <= 27.001:
            age = ((xh - x) % SPAN) / SPAN * SWEEP
            tt = t - age
            if age < 0.80 * SWEEP and tt >= T.D_IN + 0.30:
                cur.append((x, 3 + _ecg(tt) * 0.92 * k))
            elif cur:
                runs.append(cur); cur = []
            x += 0.45
        if cur:
            runs.append(cur)
        for run in runs:
            if len(run) > 1:
                dd = "M" + " L".join("%.2f %.2f" % p for p in run)
                sc += pa(dd, "none", 3.4, mix(col, INK, ei(m)))
        if t >= T.D_IN + 0.30 and m < 0.3:
            sc += ci(xh, 3 + _ecg(t) * 0.92, 2.6, PAPER, 0)                           # the head
        # a small heart blinks with each beat (gone once the line is flat)
        hb = decay(t, last, 5) if t - last < 1.6 else 0.0
        if hb > 0.03 and m == 0:
            sc += G('<path d="%s" fill="%s"/>' % (HEART, col), -15, -17, 0.105 * (0.7 + 0.5 * hb))
        s += sc + '</g>'
        s += '<ellipse rx="%.2f" ry="%.2f" fill="none" %s/>' % (31.5 + 12 * m, 31.5 * k, S(W2))
        if m < 0.5:                                                                   # bezel details: two screws, a knob
            q = 1 - 2 * m
            for a in (225, 315):
                s += ci(36 * math.cos(math.radians(a)), 36 * math.sin(math.radians(a)) * (1 - m), 1.5 * q, INK, 0)
            s += G(ci(0, 0, 3.4 * q, mix(col, PAPER, 0.0), W3 * q), 36 * math.cos(math.radians(135)), 36 * math.sin(math.radians(135)) * (1 - m))
    if m > 0:                                                                         # the flat line curls shut: lid line + lashes
        lx = 0.70 + 0.30 * m
        pts = ["%.2f %.2f" % (xx * lx, 1.5 + 4.6 * m * (1 - (xx / 44.0) ** 2)) for xx in range(-44, 45, 4)]
        s += pa("M" + " L".join(pts), "none", W1 * (0.6 + 0.4 * m), mix(col, INK, m))
        for i in range(5):
            xx = -26 + 13 * i
            yy = 1.5 + 4.6 * m * (1 - (xx / 44.0) ** 2)
            s += ln(xx, yy, xx + 0.12 * xx * m, yy + 7.5 * eo(u(m, 0.4, 1)), W2 * m)
    sc = pin * (1 + 0.035 * pulse * (1 - m) + 0.010 * wob(t, 0.5))
    return G(s, 0, 0, sc * (1 + 0.10 * m * (1 - m) * 4 * 0.5), sc)


def _look(t):
    """the pupil darts left, right, left, then locks forward"""
    x = t - T.D_EYE
    keys = [(0.10, -10.0), (0.36, 10.0), (0.60, -5.5), (0.80, 0.0)]
    v = 0.0
    for a, val in keys:
        if x > a:
            v = v + (val - v) * back(u(x, a, a + 2.6 * F), 1.2)
    return v


def _eye(t, g):
    lunge = t - T.D_LUNGE
    flash = g == LUNGE_G                                                             # ONE frame, on the film's own flash frame
    op = clamp(spring(t, T.D_EYE, 3.0, 9), 0, 1.3)
    sq = math.sin(math.pi * u(t, T.D_LUNGE - 4 * F, T.D_LUNGE)) * 0.5                # squint before the lunge
    wide = 0.06 * eo(u(lunge, 0, 3 * F)) * (1 - 0.5 * eio(u(lunge, 0.3, 1.2))) if lunge >= 0 else 0.0
    h = 7.0 + (27.5 - 7.0) * op * (1 - sq) * (1 + wide)
    look = _look(t)
    trem = 0.55 + 0.5 * decay(t, T.D_EYE, 3) + (1.6 * decay(t, T.D_LUNGE, 2.2) if lunge >= 0 else 0.0)
    tx, ty = trem * (0.6 * math.sin(2 * math.pi * 7.3 * t) + 0.4 * math.sin(2 * math.pi * 11.1 * t + 1)), trem * 0.6 * math.sin(2 * math.pi * 9.1 * t + 2)
    dil = eo(u(lunge, 0, 2.5 * F)) if lunge >= 0 else 0.0
    d = _almond(1, h)
    scl, iris, pup, rim, vein = (RED, PAPER, INK, INK, PAPER) if flash else (PAPER, RED, INK, DEEP, RED)
    s = '<clipPath id="de"><path d="%s"/></clipPath><path d="%s" fill="%s"/>' % (d, d, scl)
    e = '<g clip-path="url(#de)">'
    vg = eo(u(t, T.D_EYE + 0.12, T.D_EYE + 1.7))                                      # veins creep in from the corners
    if vg > 0.02:
        for i, v in enumerate(VEINS):
            f = clamp(vg * 1.25 - 0.08 * (i % 3))
            p = _partial(v, f)
            if len(p) > 1:
                e += pa("M" + " L".join("%.2f %.2f" % q for q in p), "none", 1.7 if i % 3 == 0 else 1.3, vein)
    ir = 17.5 * clamp(op, 0, 1.08) * (1 + 0.02 * math.sin(2 * math.pi * 0.9 * t))
    e += ci(look, 1, ir, iris, W2)
    e += ci(look, 1, ir - 3.4, "none", 2.2, rim)
    for i in range(10 if ir > 12 else 0):                                            # iris fibres
        a = 2 * math.pi * (i + 0.5) / 10.0
        e += ln(look + (ir - 6.5) * math.cos(a), 1 + (ir - 6.5) * math.sin(a), look + (ir - 9.5) * math.cos(a), 1 + (ir - 9.5) * math.sin(a), 1.5, rim)
    prx = (3.6 + 0.5 * math.sin(2 * math.pi * 0.7 * t)) * (1 - dil) + 10.5 * dil
    e += '<ellipse cx="%.2f" cy="1" rx="%.2f" ry="%.2f" fill="%s"/>' % (look * 1.12, prx * clamp(op), (11.5 + 0.5 * dil) * clamp(op), pup)
    e += ci(look * 0.75 - 6.5, -6, 2.9 * clamp(op), PAPER if not flash else RED, 0)   # flat highlight
    e += '</g>'
    s += e + pa(d, "none", W1)
    # upper lid: heavier line + lashes
    up = ["%.2f %.2f" % (47 * math.cos(a), -h * math.sin(a) ** 2) for a in [math.radians(x) for x in range(8, 173, 6)]]
    s += pa("M" + " L".join(up), "none", W1 + 1.6)
    for i in range(5):
        a = math.radians(42 + 24 * i)
        bx, by = 47 * math.cos(a), -h * math.sin(a) ** 2
        L = 6.5 * clamp(op) * (1 - 0.25 * abs(i - 2) / 2.0)
        s += ln(bx, by, bx + L * math.cos(a) * 0.9, by - L * (0.5 + 0.5 * math.sin(a)), W2)
    # the lunge: scale up fast (peak on the flash frame), then hold a little larger
    big = 0.0
    if lunge >= 0:
        tp = LUNGE_G / float(FPS)
        big = 0.36 * (ei(u(t, T.D_LUNGE - F, tp)) if t <= tp else 0.36 + 0.64 * math.exp(-7 * (t - tp)) * math.cos(2 * math.pi * 2.2 * (t - tp)))
    sc = 1 + big + 0.012 * wob(t, 0.6)
    out = G(s, tx + 20 * big, ty, sc)
    out += sparks(t, T.D_EYE, 10, 0, 0, RED, 500, a0=-200, a1=20, v=95, grav=60, life=0.46, r=5.6, col2=DEEP, rx=46, ry=22, vy=0.3)
    out += sparks(t, LUNGE_G / float(FPS) - 0.5 * F, 12, 10, 0, RED, 540, a0=-190, a1=10, v=90, grav=60, life=0.5, r=6.0, col2=DEEP, rx=60, ry=30, vy=0.2)
    # drips from the lower lid
    for i, (dx, t0) in enumerate(((-15, 0.42), (9, 0.86), (24, 1.34), (-3, 1.78))):
        xx = lunge - t0
        if 0 < xx < 0.75:
            hang = eo(u(xx, 0, 0.3))
            fall = max(xx - 0.3, 0)
            y0 = h * 0.82 * (1 - (dx / 47.0) ** 2) ** 1.0 * sc
            out += drop(dx * sc + 20 * big + tx, y0 + 3.5 * hang + 0.5 * 200 * fall * fall, 3.2 * hang * (1 - ei(u(fall, 0.10, 0.36))), RED)
    return out


# ------------------------------------------------------------------------------------------------ 6 countdown
def stopwatch(t, mm=0.0):
    """stopwatch + the big number to its right.  icons13's units (face radius 38 about (0, 4)), so the flight to the
    title mark ends on icons13's own drawing.  mm 0 .. 0.6: the details retract and the face floods amber."""
    if mm >= 0.6:
        return IC.stopwatch(t, 1, mm)[0]
    ticks = [T.C_T0 + i for i in (1, 2, 3)]
    alltk = [T.C_T0] + ticks
    k = sum(kick(t, tk, 5, 10) for tk in ticks) + 0.6 * kick(t, T.C_T0, 5, 10)
    steps = sum(clamp(spring(t, tk, 3, 11), 0, 1.2) for tk in ticks)
    rem = clamp(1 - 0.06 - 0.115 * steps - 0.022 * clamp(t - T.C_T0, 0, 9)) if t > T.C_IN + 0.2 else 1.0
    rem = 1 - (1 - rem) * eo(u(t, T.C_IN + 4 * F, T.C_IN + 12 * F))
    b_ = 1 - eio(u(mm, 0.0, 0.45))                                                   # details still out
    click = sum(decay(t, tk, 14) for tk in alltk if t >= tk)
    hop = -5 * math.exp(-6 * max(t - T.C_IN, 0)) * abs(math.cos(2 * math.pi * 2.2 * (t - T.C_IN)))
    s = ""
    if b_ > 0.02:
        s += rr(-4.5, -36 - 6 * b_, 9, 10, 1.5, INK, 0)                               # stem
        cy = -36 - 15 * b_ + 3.6 * click
        s += rr(-9.5, cy, 19, 9.5 * b_ + 0.5, 3.2, AMBER, W2)                          # crown, knurled; clicks down on every second
        for xx in (-3.4, 0, 3.4):
            s += ln(xx, cy + 2.6, xx, cy + 6.6 * b_, 1.5)
        s += ln(26, -21, 26 + 7.5 * b_, -21 - 7.5 * b_, 7.5)                           # side pusher
        s += ln(26 + 7.5 * b_ - 3, -21 - 7.5 * b_ - 3, 26 + 7.5 * b_ + 3, -21 - 7.5 * b_ + 3, 4.2)
        if click > 0.25:                                                              # two click marks beside the crown
            for sd in (-1, 1):
                s += ln(sd * 15, -50, sd * (15 + 5 * click), -50 - 4 * click, W3 * clamp(click * 2))
    R = 38
    s += ci(0, 4, R, mix(PAPER, AMBER, eio(u(mm, 0.15, 0.6))), W1 + (6.0 - W1) * eio(u(mm, 0, 0.5)))
    q = 1 - eio(u(mm, 0.25, 0.58))                                                    # ring, ticks and hand fade into the amber
    if q > 0.01:
        f = '<g opacity="%.3f">' % q
        rad, w = 26.5, 8.0
        f += '<circle cx="0" cy="4" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (rad, SLOT, w)
        if rem > 0.999:
            f += '<circle cx="0" cy="4" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (rad, AMBER, w)
        elif rem > 0.004:
            a0 = 2 * math.pi * (1 - rem)
            f += '<path d="M%.2f %.2f A%.2f %.2f 0 %d 1 0 %.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (
                rad * math.sin(a0), 4 - rad * math.cos(a0), rad, rad, 1 if rem > 0.5 else 0, 4 - rad, AMBER, w)
            f += ln(rad * math.sin(a0) * 0.86, 4 - rad * math.cos(a0) * 0.86, rad * math.sin(a0) * 1.14, 4 - rad * math.cos(a0) * 1.14, W3)
        for i in range(12):                                                           # minute marks
            a = 2 * math.pi * i / 12.0
            r0 = 32.6 if i % 3 else 31.6
            f += ln(r0 * math.sin(a), 4 - r0 * math.cos(a), 34.6 * math.sin(a), 4 - 34.6 * math.cos(a), 2.3 if i % 3 == 0 else 1.4)
        f += pa("M-15.5 -4.5 A17.5 17.5 0 0 1 -4 -12.6", "none", 2.8, SLOT)             # flat glass highlight
        ha = 2 * math.pi * (t - T.C_T0) if t >= T.C_T0 else 0.0                        # the hand: one turn a second, continuously
        hx, hy = math.sin(ha), -math.cos(ha)
        f += ln(-6 * hx, 4 - 6 * hy, 19.5 * hx, 4 + 19.5 * hy, 4.0)
        f += ci(0, 4, 4.6, AMBER, W3 + 0.4)
        s += f + '</g>'
    if mm > 0.3:
        z = back(u(mm, 0.3, 1.0), 2.2)
        s += G(IC.biohazard(INK), 0, 4, max(z, 0.01) * 1.02, rot=-120 * (1 - eo(u(mm, 0.3, 1.0))))
    s = G(s, 0, hop * (1 if mm == 0 else 0), 1 + 0.05 * k, 1 - 0.05 * k, rot=4 * k, px=0, py=42)
    # the number: flips on every second
    qn = eo(u(t, T.C_IN + 3 * F, T.C_IN + 9 * F)) * (1 - eio(u(mm, 0.0, 0.3)))
    if qn > 0.02:
        n = count_number(t)
        last = max([T.C_IN] + [tk for tk in ticks if t >= tk])
        x = u(t, last, last + 6 * F)
        nb = 1 + 0.10 * decay(t, last, 9) * math.cos(2 * math.pi * 3.4 * (t - last)) if last > T.C_IN else 1.0
        d = '<clipPath id="cn"><rect x="-52" y="-41" width="104" height="62"/></clipPath><g clip-path="url(#cn)">'
        if x < 1 and last > T.C_IN:
            d += num(str(n + 1), 0, 14 - 66 * ei(x), 58, AMBER, 6.4)
            d += num(str(n), 0, 14 + 66 * (1 - back(x, 1.5)), 58, AMBER, 6.4)
        else:
            d += num(str(n), 0, 14, 58, AMBER, 6.4)
        d += '</g>'
        s += G(d, 86 - 14 * (1 - qn), 8, qn * nb, qn * (2 - nb), op=qn)
    return s


# ------------------------------------------------------------------------------------------------ the layer
#        id          draw       joins
ITEMS = [("radio", radio, T.R_IN), ("battery", battery, T.B_IN), ("calls", phone, T.P_IN), ("trust", heart, T.H_IN),
         ("danger", danger, T.D_IN), ("countdown", stopwatch, T.C_IN)]
NEXT = dict(battery=T.P_IN, calls=T.H_IN)                  # when a pictogram hands over and becomes the companion


def _place(t, aspect):
    L = LAYOUT[aspect]
    g = int(round(t * FPS))
    x0, y0 = L["shift"].get(shot_of(g), (L["x0"], L["y"]))
    for a, b, dx, dy in L.get("dodge", []):
        q = eio(u(t, a - 6 * F, a)) * (1 - eio(u(t, b, b + 6 * F)))
        x0, y0 = x0 + dx * q, y0 + dy * q
    return x0, y0


def scene(t, aspect="916"):
    """-> (svg body in reference pixels, (y_top, y_bottom) of the rows that can hold ink) or (None, None)"""
    L = LAYOUT[aspect]
    Sg = L["s"]
    if t >= T.TITLE - 1 * F - 1e-9:                                                  # the title mark: icons13's own layer
        keep = IC.LAYOUT[aspect]["title"]
        IC.LAYOUT[aspect]["title"] = L["title"]
        try:
            return IC.scene(t, aspect)
        finally:
            IC.LAYOUT[aspect]["title"] = keep
    x0, y0 = _place(t, aspect)
    fade = 1.0
    for a, b, o in L["fade"]:
        fade *= 1 - (1 - o) * eio(u(t, a - 4 * F, a)) * (1 - eio(u(t, b, b + 5 * F)))
    out, parts = [], []
    for name, fn, t_in in ITEMS:
        if t < t_in:
            continue
        if name == "countdown":
            if t >= T.C_MORPH:
                continue
            pu, ox, oy = HERO[name]
            p = clamp(spring(t, T.C_IN, 2.6, 8), 0, 1.05)
            del PARTS[:]
            b_ = fn(t)
            for lst, inner in ((out, b_), (parts, "".join(PARTS))):
                if inner:
                    lst.append('<g opacity="%.3f"><g transform="translate(%.2f %.2f) scale(%.4f)">%s</g></g>' % (
                        fade * u(t, t_in, t_in + 2 * F), x0 + ox * Sg, y0 + oy * Sg, pu * Sg * p, inner))
            continue
        t_out = L["out"].get(name, 1e9)
        if t >= t_out + 8 * F:
            continue
        lv = u(t, t_out, t_out + 8 * F)
        op = fade * (1 - eio(lv)) * u(t, t_in, t_in + 2 * F)
        if op <= 0.004:
            continue
        pu, ox, oy = HERO[name]
        c = 0.0
        if name in NEXT:                                                             # hero -> small companion beside the next hero
            c = eio(u(t, NEXT[name] - 1 * F, NEXT[name] + 9 * F))
            cu, cx_, cy_ = COMP[name]
            hopc = -8 * math.sin(math.pi * c) if 0 < c < 1 else 0.0
            pu, ox, oy = pu + (cu - pu) * c, ox + (cx_ - ox) * c, oy + (cy_ - oy) * c + hopc
        ldx, ldy = LEAVE[name]
        del PARTS[:]
        b_ = fn(t, c) if name in NEXT else fn(t)
        for lst, inner in ((out, b_), (parts, "".join(PARTS))):
            if inner:
                lst.append('<g opacity="%.3f"><g transform="translate(%.2f %.2f) scale(%.4f)">%s</g></g>' % (
                    op, x0 + (ox + ldx * ei(lv)) * Sg, y0 + (oy + ldy * ei(lv)) * Sg, pu * Sg * (1 - 0.12 * ei(lv)), inner))
    body = ""
    if out:
        body = '<g filter="url(#kp)">%s</g>%s' % ("".join(out), "".join(parts))
    rows = (max(0, int(y0 - 150 * Sg)), min(L["RH"], int(y0 + 150 * Sg)))
    if t >= T.C_MORPH:                                                               # the flight to the title spot (icons13's path)
        mm = eio(u(t, T.C_MORPH, T.TITLE - 1 * F))
        pu, ox, oy = HERO["countdown"]
        sc0, cx0, cy0 = pu * Sg, x0 + ox * Sg, y0 + oy * Sg
        tx, ty, tr = L["title"]
        cx = cx0 + (tx - cx0) * mm
        cy = cy0 + (ty - 4 * tr / 38.0 - cy0) * mm - 46 * math.sin(math.pi * mm) * (1 if mm < 1 else 0)
        s1 = sc0 + (tr / 38.0 - sc0) * mm
        body += '<g filter="url(#%s)"><g transform="translate(%.2f %.2f) scale(%.4f)">%s</g></g>' % ("kp" if mm < 0.6 else "kl", cx, cy, s1, stopwatch(t, mm))
        rows = (max(0, int(min(rows[0], ty - tr * 1.9))), min(L["RH"], int(max(rows[1], ty + tr * 1.9))))
    if not body:
        return None, None
    return body, rows


def _kf(fid, r, col):
    return ('<filter id="%s" x="-30%%" y="-40%%" width="160%%" height="180%%"><feMorphology in="SourceAlpha" operator="dilate" radius="%.2f" result="d"/>'
            '<feFlood flood-color="%s"/><feComposite in2="d" operator="in" result="k"/><feMerge><feMergeNode in="k"/><feMergeNode in="SourceGraphic"/></feMerge>'
            '</filter>') % (fid, r, col)


# kl: icons13's own keyline (title mark); kp: the pictograms' off-white keyline
DEFS = IC.DEFS.replace("</defs>", _kf("kp", KEY, PAPER) + "</defs>")


def frame_svg(t, W, H, aspect="916", view=None):
    """-> (svg text, (x, y, w, h) in output pixels) or (None, None).  view = (x, y, w, h) in reference pixels (sheets)"""
    L = LAYOUT[aspect]
    body, rows = scene(t, aspect)
    if body is None:
        return None, None
    title = t >= T.TITLE - 1 * F - 1e-9
    k = W / float(L["RW"])
    if view is None:
        py0, py1 = int(math.floor(rows[0] * k)), min(H, int(math.ceil(rows[1] * k)))
        box = (0, py0, W, py1 - py0)
        vb = (0, py0 / k, W / k, (py1 - py0) / k)
    else:
        box = (0, 0, W, H)
        vb = view
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.4f %.4f %.4f %.4f">%s%s</svg>' % (
        box[2], box[3], vb[0], vb[1], vb[2], vb[3], IC.DEFS if title else DEFS, body)
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
    """the pictogram layer of film frame g at W x H: uint8 RGBA (H, W, 4), straight alpha, zeros where there is nothing"""
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
    """[(pictogram, joins, leaves, [(film s, event), ...]), ...]"""
    r = lambda x: round(x, 3)
    o = LAYOUT["916"]["out"]
    bt = _beats()
    return [
        ("radio", r(T.R_IN), o["radio"], [
            (r(T.R_IN), "walkie-talkie pops in bouncing, antenna whips; arcs and the display bars follow the voice"),
            (r(T.R_WAIT), "arcs jitter, amber"), (r(T.R_HEY), "arcs jitter harder, red"),
            (r(T.R_CUT), "arcs shatter into 12 fragments that tumble and fall; display dies"), (r(T.R_CUT + 2 * F), "red slash snaps across the body"),
            (r(T.R_CUT + 0.55), "colour drains to grey top to bottom, body droops, antenna hangs"),
            (r(T.R_CUT + 1.5), "every 1.25 s one small grey arc tries to get out and dies"), (o["radio"], "sinks and fades (8 frames)")]),
        ("battery", r(T.B_IN), o["battery"], [
            (r(T.B_IN), "empty shell drops in and squashes on landing"), (T.B1, "cell 1 slams in + green flecks"), (T.B2, "cell 2"), (T.B3, "cell 3, bigger burst"),
            (r(T.B3 + 0.08), "amber bolt pops (blinks once at +0.38)"), (r(T.B3 + 0.22), "satisfied hop"),
            (r(T.P_IN), "on the cut to S10: hops aside and shrinks to the companion beside the phone"), (o["battery"], "slides off to the right and fades")]),
        ("calls", r(T.P_IN), o["calls"], [
            (r(T.P_IN), "phone pops in, buzzing (rotation shake, vibration ticks)"), (r(T.P1), "badge 1 pops, red ring wave"), (r(T.P2), "badge flips to 2"),
            (r(T.P3), "3"), (r(T.P4), "4 + red flecks"), (r(T.P4 + 0.6), "keeps ringing: one short buzz every 1.3 s"),
            (r(T.H_IN), "hops aside and shrinks to the companion beside the heart (badge 4 stays)"),
            (T.H_END, "its screen goes dark"), (o["calls"], "sinks and fades")]),
        ("trust", r(T.H_IN), o["trust"], [
            (r(T.H_IN), "glass heart pops in, level 82 %, beating (beat slows with the level), liquid sloshes"),
            (r(T.H_CASE), "drains to 60 %, droplets fall"), (r(T.H_WAIT), "52 %"), (r(T.H_EVERY), "28 %"), (r(T.H_CRACK), "crack appears"),
            (r(T.H_BACK), "17 %, crack grows"), (r(T.H_SILENT), "7 %, crack grows"), (T.H_END, "empties, goes grey, beat stops, crack runs through"),
            (T.H_SPLIT, "splits: the halves swing apart about the tip"), (32.21, "whole layer at 35 % until 32.70 (Kong's head passes)"),
            (32.74, "halves drop"), (o["trust"], "fades")]),
        ("danger", r(T.D_IN), o["danger"], [
            (r(T.D_IN), "round heart monitor pops in; green trace drawn left to right every 1.6 s")] +
            [(r(b), "beat %d (strength %.2f)" % (i + 1, a)) for i, (b, a) in enumerate(bt)] + [
            (r(T.D_LEAN), "trace turns amber by %.2f" % T.D_DRIVER), (r(HB[1] + 0.3), "flat line"),
            (r(T.D_EYE - 5 * F), "disc squeezes shut into a closed eyelid with lashes"), (T.D_EYE, "eye snaps open: red iris, slit pupil, shards"),
            (r(T.D_EYE + 0.10), "pupil darts left / right / left, locks forward at +0.9; veins creep in until +1.7"),
            (r(T.D_LUNGE - 4 * F), "squint"), (T.D_LUNGE, "pupil dilates, eye lunges (scale 1.36 on the flash frame)"),
            (r(LUNGE_G / float(FPS)), "ONE inverted frame (red sclera, white iris) on the film's flash frame g %d + shards" % LUNGE_G),
            (r(T.D_LUNGE + 0.42), "four drips fall from the lower lid"), (o["danger"], "fades")]),
        ("countdown", r(T.C_IN), r(T.C_MORPH), [
            (r(T.C_IN), "stopwatch pops in bouncing, 60 slides out beside it"), (T.C_T0, "hand starts: one turn a second; crown clicks"),
            (T.C_T0 + 1, "59 flips in, tick bounce, crown clicks, ring steps down"), (T.C_T0 + 2, "58"), (T.C_T0 + 3, "57"),
            (T.C_MORPH, "number folds away, the stopwatch flies to the title spot (icons13's path) and becomes the biohazard mark"),
            (T.TITLE, "title mark lands + burst, holds to the end (icons13's pixels)")]),
    ]


if __name__ == "__main__":
    for row in cue_table():
        print(row[0], row[1], row[2])
        for e in row[3]:
            print("    %7.3f  %s" % e)
