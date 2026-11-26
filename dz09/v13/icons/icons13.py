"""icons13.py -- DEAD ZONE 09 EP.1, icon system v13: one flat status strip along the top-left of the frame.

    import icons13
    rgba = icons13.overlay(g, W, H, aspect='916')      # film frame g (0..1279) -> uint8 RGBA (H, W, 4), straight alpha
    rows = icons13.cue_table()                          # [(icon, t_in, t_active_end, [(t, what), ...]), ...]

Flat 2D only: solid fills, one thick ink outline, a thin flat light keyline outside it; no gradients, no shadows, no
gloss, no depth.  Icons join a single row from the top-left in story order (radio, battery, calls, trust, danger,
countdown); the one whose beat is playing is drawn 1.43x and carries its horizontal value (arcs, cells, name tag, bar,
number); afterwards it settles back as a small quiet status item.  Everything is a pure function of the film frame.
Raster: SVG -> one headless Chromium page (raster_page.js, Kanit Black from PROJ/fonts), cached on disk by SVG hash.
"""
import atexit, hashlib, json, math, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
FPS, NF = 24, 1280
CACHE = os.path.join(HERE, "cache")
OFF = 0.30                                               # film time = caption time + 0.30

# ------------------------------------------------------------------------------------------------ palette (flat)
INK, PAPER = "#1d1b24", "#f6f1e7"
RED, AMBER, GREEN, ORANGE = "#e63946", "#ffb703", "#35c75a", "#f26a1b"
GREY, SLOT, BLUE = "#a9a5a0", "#cfc9bd", "#55c2f5"
SW = 6.0                                                 # outline, icon units (icon box = 100 units)
YLIM = 60.0                                              # bursts stay within +-YLIM units of the row centre line
KEY = 2.0                                                # light keyline outside the ink, reference pixels

# ------------------------------------------------------------------------------------------------ layout
# reference frames: 720x1280 (9:16) and 1280x720 (16:9).  x0 = left end of the row, y = row centre line,
# q / a = pixels per icon unit for a quiet / the active icon (icon box 100 units), gap between items,
# m = scale of an item two beats old, shift = {shot: x0}, fade = [(t0, t1, opacity)] while a head passes the strip, title = (x, y, radius) of the title mark.
LAYOUT = {
    # film v3 (director): keep = how many quiet items stay in the row beside the current one (older ones fade and leave),
    # which lets the quiet ones be larger: q 0.78 -> 0.96, m 0.50 -> 0.88 (the radio, the narrowest, is 44 / 40 px wide
    # at 720; it was 36 / 23).  title mark 92 -> 118 px radius, centre y 372 -> 350.  Before: keep=None, q=0.78, m=0.50, title=(360, 372, 92).
    "916": dict(RW=720, RH=1280, x0=36, y=172, q=0.96, a=1.12, m=0.88, gap=16, band=112, shift={}, fade=[(32.21, 32.70, 0.35)],
                title=(360, 350, 118), keep=None,
                # user (ref clip): an icon leaves once its story beat is done; nothing stays as a permanent row
                out=dict(radio=6.40, battery=19.30, calls=33.00, trust=33.00, danger=45.90)),
    "169": dict(RW=1280, RH=720, x0=64, y=106, q=0.73, a=1.04, m=0.47, gap=15, band=104, shift={}, fade=[], title=(640, 190, 70)),
}
CUT = [0, 81, 138, 181, 223, 266, 303, 346, 389, 421, 457, 532, 599, 656, 695, 728, 802, 831, 903, 967, 1043, 1087,
       1114, 1147, 1280]                                  # first frame of S01..S24 (v4/animatic/timing.py)


def shot_of(g):
    for i in range(24):
        if g < CUT[i + 1]:
            return "S%02d" % (i + 1)
    return "S24"


# ------------------------------------------------------------------------------------------------ cue times
def _captions(narr):
    p = os.path.join(PROJ, "audio", narr, "captions_timing.json")
    return dict((c["text"], c["t0"] + OFF) for c in json.load(open(p, encoding="utf-8")))


NARR = os.environ.get("DZ09_NARR", "narr_ohm")           # the take the word-synced cues follow
try:
    CAP = _captions(NARR)
except Exception:                                        # frozen copy of narr_ohm (+0.30), used if the file is gone
    CAP = {}
_DEF = {"เดี๋ยว!": 2.151, "เฮ้ย!": 2.623, "ก็เงียบไป": 4.219, "แบตเต็ม 3 ขีด": 16.146, "โทรศัพท์สั่น": 17.548, "4 สาย": 19.126,
        "น้ำเหนือ": 21.251, "พ่อ": 22.169, "พ่อมีเคสด่วนลูก": 24.944, "รออีกแป๊บเดียว": 26.335, "ทุกครั้งเลย...": 27.34,
        "เดี๋ยวพ่อ": 28.956, "ปลายสายเงียบไป": 30.347, "แล้วก็วางสาย": 31.595, "ในรถ": 34.613, "น้องในทีม": 37.618,
        "แล้วคนขับ": 40.281, "อีก 60 วินาที": 46.448}


def cap(text):
    return CAP.get(text, _DEF[text])


class T:                                                 # film seconds
    # radio
    R_IN, R_WAIT, R_HEY, R_CUT, R_QUIET = 0.10, cap("เดี๋ยว!"), cap("เฮ้ย!"), 3.243, 5.30
    # battery: the three LEDs of the cutter (picture cue, fixed)
    B_IN, B1, B2, B3, B_QUIET = 15.92, 16.30, 16.50, 16.70, 17.04
    # missed calls: the phone buzzes from the cut to S10; the 4th count lands on "4 สาย"
    P_IN = 421 / 24.0 + 0.01
    P4 = cap("4 สาย")
    P1, P2, P3 = P4 - 3 * 0.44, P4 - 2 * 0.44, P4 - 0.44
    P_NAME = cap("น้ำเหนือ") - 0.17
    P_QUIET = cap("พ่อ") - 0.22
    # trust
    H_IN = cap("พ่อ") - 0.17
    H_CASE, H_WAIT, H_EVERY, H_BACK, H_SILENT = cap("พ่อมีเคสด่วนลูก"), cap("รออีกแป๊บเดียว"), cap("ทุกครั้งเลย..."), cap("เดี๋ยวพ่อ"), cap("ปลายสายเงียบไป")
    H_CRACK = H_EVERY + 0.62
    H_END = 31.75                                         # the screen goes dark (picture cue)
    H_SPLIT, H_QUIET = 32.05, 32.30
    # danger
    D_IN = 33.62
    D_LEAN, D_DRIVER = cap("น้องในทีม"), cap("แล้วคนขับ")
    D_EYE = 41.657                                        # the driver lifts his head (picture cue)
    D_LUNGE, D_QUIET = 43.445, 43.70
    # countdown
    C_IN = 1114 / 24.0 + 0.01                             # the cut to S23, "อีก 60 วินาที" follows 1 frame later
    C_T0 = 46.78                                          # 60 is said; 59 / 58 / 57 at +1 / +2 / +3 s
    C_MORPH, TITLE = 50.22, 50.72


def cue_table():
    """[(icon, joins the row, settles to quiet, [(film s, event), ...]), ...]"""
    r = lambda x: round(x, 3)
    return [
        ("radio", r(T.R_IN), r(T.R_QUIET), [(r(T.R_IN), "walkie-talkie pops in, arcs follow the voice"), (r(T.R_WAIT), "arcs jitter, amber"),
                                            (r(T.R_HEY), "arcs jitter harder, red"), (r(T.R_CUT), "arcs collapse to a noisy then flat line, red cut mark"),
                                            (r(T.R_CUT + 0.85), "body goes grey"), (r(T.R_QUIET), "settles: small grey radio with the cut mark")]),
        ("battery", r(T.B_IN), r(T.B_QUIET), [(r(T.B_IN), "empty battery pops in"), (T.B1, "cell 1"), (T.B2, "cell 2"), (T.B3, "cell 3 + burst"),
                                              (r(T.B_QUIET), "settles: small full battery, stays to the title")]),
        ("calls", r(T.P_IN), r(T.P_QUIET), [(r(T.P_IN), "phone pops in, buzzing"), (r(T.P1), "badge 1"), (r(T.P2), "badge 2"), (r(T.P3), "badge 3"),
                                            (r(T.P4), "badge 4 + burst"), (r(T.P_NAME), "badge stretches into the name tag น้ำเหนือ"),
                                            (r(T.P_QUIET), "tag folds back into the badge, settles: phone with 4")]),
        ("trust", r(T.H_IN), r(T.H_QUIET), [(r(T.H_IN), "heart pops in where the tag was, level 82 %"), (r(T.H_CASE), "sinks to 60 %"), (r(T.H_WAIT), "sinks to 52 %"),
                                            (r(T.H_EVERY), "sinks to 28 %"), (r(T.H_CRACK), "crack"), (r(T.H_BACK), "sinks to 17 %"), (r(T.H_SILENT), "sinks to 7 %"),
                                            (T.H_END, "empties, goes grey, crack runs through"), (T.H_SPLIT, "splits, halves drop apart"),
                                            (r(T.H_QUIET), "settles: small grey broken heart")]),
        ("danger", r(T.D_IN), r(T.D_QUIET), [(r(T.D_IN), "green heartbeat badge pops in, bar 12 %"), (r(T.D_LEAN), "beat speeds up, green to amber, bar to 55 %"),
                                             (r(T.D_EYE - 0.2), "trace flattens, badge squeezes into a closed lid"), (T.D_EYE, "red eye snaps open, bar full red + burst"),
                                             (T.D_LUNGE, "one flat red flash + shake"), (r(T.D_QUIET), "settles: small red eye")]),
        ("countdown", r(T.C_IN), r(T.C_MORPH), [(r(T.C_IN), "stopwatch pops in with 60"), (T.C_T0 + 1, "59"), (T.C_T0 + 2, "58"), (T.C_T0 + 3, "57"),
                                                (T.C_MORPH, "row fades, the stopwatch flies to the title spot and turns into the biohazard mark"),
                                                (T.TITLE, "title mark lands + burst, holds to the end")]),
    ]


# ------------------------------------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def u(t, t0, t1):
    return clamp((t - t0) / (t1 - t0))


def eio(x):
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2.0


def eo(x):
    return 1 - (1 - x) ** 3


def ei(x):
    return x * x * x


def back(x, s=1.9):
    x -= 1
    return 1 + (s + 1) * x * x * x + s * x * x


def spring(t, t0, f=2.6, d=9.0):
    """0 before t0, settles on 1 with a small overshoot"""
    x = t - t0
    return 0.0 if x <= 0 else 1 - math.exp(-d * x) * math.cos(2 * math.pi * f * x)


def kick(t, t0, f=4.0, d=9.0):
    """impulse that starts at 0, swings and dies"""
    x = t - t0
    return 0.0 if x <= 0 else math.exp(-d * x) * math.sin(2 * math.pi * f * x)


def decay(t, t0, d=9.0):
    x = t - t0
    return 0.0 if x < 0 else math.exp(-d * x)


def seg(t, v0, keys):
    """value track: keys [(t_start, t_end, value)], eased in-out from the value before"""
    v = v0
    for a, b, val in keys:
        if t <= a:
            break
        v = v + (val - v) * eio(u(t, a, b))
    return v


def rnd(i, k=0):
    x = math.sin(i * 127.1 + k * 311.7) * 43758.5453
    return (x - math.floor(x)) * 2 - 1


def mix(c0, c1, k):
    k = clamp(k)
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


F = 1.0 / FPS

# ------------------------------------------------------------------------------------------------ narration level
_ENV = None


def envelope():
    """narration level per film frame, 0..1 (narr_ohm/narr_final.wav at +0.30 s); cached in env.npy"""
    global _ENV
    if _ENV is None:
        p = os.path.join(HERE, "env.npy")
        if not os.path.exists(p):
            import wave
            w = wave.open(os.path.join(PROJ, "audio", "narr_ohm", "narr_final.wav"))
            sr, ch = w.getframerate(), w.getnchannels()
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            a = a.reshape(-1, ch).mean(1)
            e = np.zeros(NF, np.float32)
            for g in range(NF):
                i0 = int((g * F - OFF - 0.02) * sr)
                i1 = int((g * F - OFF + 0.03) * sr)
                if i1 > 0 and i0 < len(a):
                    e[g] = np.sqrt(np.mean(a[max(i0, 0):i1] ** 2) + 1e-9)
            e = np.clip(e / (np.percentile(e, 97) + 1e-6), 0, 1) ** 0.7
            np.save(p, e)
        _ENV = np.load(p)
    return _ENV


def level(t):
    e = envelope()
    x = clamp(t * FPS, 0, NF - 1.001)
    i = int(x)
    return float(e[i] + (e[i + 1] - e[i]) * (x - i))


# ------------------------------------------------------------------------------------------------ svg helpers
def st(w=SW, c=INK):
    return 'stroke="%s" stroke-width="%.2f" stroke-linejoin="round" stroke-linecap="round"' % (c, w)


def xf(x=0, y=0, sx=1, sy=None, rot=0):
    sy = sx if sy is None else sy
    return 'transform="translate(%.2f %.2f) rotate(%.2f) scale(%.4f %.4f)"' % (x, y, rot, sx, sy)


def line2(x1, y1, x2, y2, col, w=5.0, o=3.6):
    """a flat stroke with the ink outline around it"""
    p = 'x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"' % (x1, y1, x2, y2)
    return '<line %s %s/><line %s %s/>' % (p, st(w + o, INK), p, st(w, col))


def path2(d, col, w=5.0, o=3.6):
    return '<path d="%s" fill="none" %s/><path d="%s" fill="none" %s/>' % (d, st(w + o, INK), d, st(w, col))


def burst(t, t0, n=8, r0=40, r1=64, col=PAPER, w=4.5, dur=9 * F, rot=0.0, cx=0, cy=0, a0=0, a1=360, clampy=True):
    """one-time flat burst: n short strokes shoot out and shrink to nothing"""
    x = u(t, t0, t0 + dur)
    if x <= 0 or x >= 1:
        return ""
    ro, ri = r0 + (r1 - r0) * eo(x), r0 + (r1 - r0) * x * x
    if ro - ri < 0.6:
        return ""
    s = ""
    for i in range(n):
        an = math.radians(rot + a0 + (a1 - a0) * (i / float(n) if a1 - a0 >= 360 else i / float(max(n - 1, 1))))
        c, sn = math.cos(an), math.sin(an)
        a, b = ri, ro
        if clampy and abs(sn) > 1e-6:                         # keep every stroke inside the strip (+-YLIM units)
            lim = (YLIM - w / 2.0 - 1.5 - (cy if sn > 0 else -cy)) / abs(sn)
            b = min(b, lim)
        if b - a < 1.0:
            continue
        s += line2(cx + c * a, cy + sn * a, cx + c * b, cy + sn * b, col, w, 3.0)
    return s


def hbar(x0, L, frac, col, h=22, track=PAPER, sq=0.0, uid="b"):
    """flat horizontal bar: x0 = left end, centred on y = 0"""
    hh = h * (1 - 0.25 * sq)
    r = hh / 2.0
    w = clamp(frac) * L
    s = '<clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f"/></clipPath>' % (uid, x0, -r, L, hh, r)
    s += '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>' % (x0, -r, L, hh, r, track)
    if w > 0.3:
        s += '<g clip-path="url(#%s)"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (uid, x0, -r, w, hh, col)
        s += '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" %s/></g>' % (x0 + w, -r, x0 + w, r, st(4.0))
    s += '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="none" %s/>' % (x0, -r, L, hh, r, st())
    return s


def text(s, x, y, size, col=PAPER, anchor="middle", extra=""):
    return '<text x="%.2f" y="%.2f" font-family="Kanit" font-weight="900" font-size="%.2f" text-anchor="%s" fill="%s" %s>%s</text>' % (
        x, y, size, anchor, col, extra, s)


# ------------------------------------------------------------------------------------------------ 1 radio
def radio(t, act):
    """walkie-talkie; arcs run to the right.  returns (svg, extension in units)"""
    dead = t >= T.R_CUT
    grey = eio(u(t, T.R_CUT + 0.85, T.R_CUT + 1.25))
    body = mix(ORANGE, GREY, grey)
    jit = max(decay(t, T.R_WAIT, 3.2) * 0.6, decay(t, T.R_HEY, 2.6)) if not dead else 0.0
    g = int(round(t * FPS))
    k = kick(t, T.R_WAIT, 5, 8) * 0.5 + kick(t, T.R_HEY, 5, 7) * 0.9 + kick(t, T.R_CUT, 4, 7)
    s = '<g %s>' % xf(rnd(g, 1) * 2.2 * jit, rnd(g, 2) * 2.2 * jit, 1 + 0.07 * k, 1 - 0.07 * k, rot=5 * k + rnd(g, 3) * 3 * jit)
    s += '<line x1="-9" y1="-18" x2="-9" y2="-43" %s/>' % st(8.5)
    s += '<rect x="3" y="-25" width="10" height="10" rx="2" fill="%s" %s/>' % (INK, st(3))
    s += '<rect x="-19" y="-17" width="38" height="62" rx="8" fill="%s" %s/>' % (body, st())
    s += '<rect x="-12" y="-9" width="24" height="14" rx="3" fill="%s" %s/>' % (PAPER, st(3.5))
    for y in (16, 24, 32):
        s += '<line x1="-9" y1="%d" x2="9" y2="%d" %s/>' % (y, y, st(4))
    s += '</g>'
    # --- the signal, to the right of the body
    cx, cy = 22, -3
    ext = 0.0
    if not dead:
        lv = level(t)
        col = mix(mix(PAPER, AMBER, u(t, T.R_WAIT, T.R_WAIT + 2 * F)), RED, u(t, T.R_HEY, T.R_HEY + 2 * F))
        pin = spring(t, T.R_IN + 3 * F, 2.4, 9)
        for i, r in enumerate((13, 25, 37)):
            ph = math.sin(2 * math.pi * (t * 3.2 - i * 0.22))
            w = 4.2 + (1.0 + 2.6 * lv) * max(0.0, ph) + 1.2 * lv
            rr = r * pin * (1 + 0.05 * lv * ph) + rnd(g, 10 + i) * 3.0 * jit
            a = math.radians(40 + rnd(g, 20 + i) * 10 * jit)
            ox, oy = cx + rnd(g, 30 + i) * 2.5 * jit, cy + rnd(g, 40 + i) * 3.5 * jit
            if rr < 3:
                continue
            d = "M%.2f %.2f A%.2f %.2f 0 0 1 %.2f %.2f" % (ox + rr * math.cos(a), oy - rr * math.sin(a), rr, rr, ox + rr * math.cos(a), oy + rr * math.sin(a))
            s += path2(d, col, w, 3.6)
        ext = 44.0
    else:
        x = t - T.R_CUT
        # arcs fold into one line: noisy for the 3 static frames, then flat; the line stays while active
        q = 1 - eio(u(t, T.R_QUIET - 2 * F, T.R_QUIET + 8 * F))        # leaves when the icon settles
        L = 40 * eo(u(x, 0, 4 * F)) * q
        amp = 9 * decay(t, T.R_CUT, 9) * (1 if x < 0.5 else 0)
        if L > 2:
            pts = []
            n = 9
            for i in range(n + 1):
                yy = cy + (rnd(g * 7 + i, 5) * amp if 0 < i < n else 0)
                pts.append("%.2f %.2f" % (cx + L * i / n, yy))
            s += path2("M" + " L".join(pts), mix(RED, PAPER, u(x, 0.15, 0.6)), 4.6, 3.6)
        # cut mark: a red X at the end of the line; on settling it moves onto the radio's shoulder
        xs = spring(t, T.R_CUT + 3 * F, 3.0, 10)
        if xs > 0:
            mx, my = 16 + (cx + L - 16 + 6) * q, -20 + (cy + 20) * q
            r = 7.5 * xs * (0.8 + 0.2 * q)
            s += '<g %s>' % xf(mx, my, 1, rot=90 * (1 - min(xs, 1)))
            s += line2(-r, -r, r, r, RED, 5.0, 3.6) + line2(-r, r, r, -r, RED, 5.0, 3.6) + '</g>'
        s += burst(t, T.R_CUT + 3 * F, 6, 12, 26, RED, 4, cx=cx + 46, cy=cy)
        ext = (44.0 + 12 * u(x, 0, 4 * F)) * q
    return s, ext


# ------------------------------------------------------------------------------------------------ 2 battery
def battery(t, act):
    lit = [spring(t, tb, 3.0, 11) for tb in (T.B1, T.B2, T.B3)]
    k = sum(kick(t, tb, 4.5, 10) for tb in (T.B1, T.B2)) * 0.6 + kick(t, T.B3, 4, 8)
    s = '<g %s>' % xf(0, -2.5 * abs(k), 1 + 0.06 * k, 1 - 0.06 * k)
    s += '<rect x="31" y="-11" width="13" height="22" rx="4" fill="%s" %s/>' % (INK, st(3))
    s += '<rect x="-42" y="-25" width="76" height="50" rx="10" fill="%s" %s/>' % (PAPER, st())
    for i in range(3):
        x = -34 + i * 21.0
        s += '<rect x="%.2f" y="-16" width="17" height="32" rx="3.5" fill="%s"/>' % (x, SLOT)
        v = lit[i]
        if v > 0:
            h = 32 * clamp(v, 0, 1.25)
            col = mix(PAPER, GREEN, u(t, (T.B1, T.B2, T.B3)[i], (T.B1, T.B2, T.B3)[i] + 2.5 * F))
            s += '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="3.5" fill="%s" %s/>' % (
                x - 1.5 * max(v - 1, 0) * 4, 16 - h, 17 + 3 * max(v - 1, 0) * 4, h, col, st(3.2))
    s += '</g>'
    s += burst(t, T.B3 + 1 * F, 10, 40, 60, GREEN, 4.5, rot=18)
    s += burst(t, T.B1, 3, 30, 44, GREEN, 4, cx=-25.5, cy=0, a0=-120, a1=-60)
    s += burst(t, T.B2, 3, 30, 44, GREEN, 4, cx=-4.5, cy=0, a0=-120, a1=-60)
    return s, 0.0


# ------------------------------------------------------------------------------------------------ 3 missed calls
TAGC = "#d6336c"


def phone(t, act):
    counts = (T.P1, T.P2, T.P3, T.P4)
    n = sum(1 for c in counts if t >= c)
    # buzz: a burst of shake on every count, calm after the 4th
    buzz = max([0.0] + [math.sin(math.pi * u(t, c - 0.05, c + 0.30)) for c in counts])
    buzz = max(buzz, 0.35 * (1 - u(t, T.P_IN, T.P1)) * spring(t, T.P_IN, 2, 9))
    rot = 9 * buzz * math.sin(2 * math.pi * 13 * t)
    k = sum(kick(t, c, 4.5, 9) for c in counts)
    s = '<g transform="translate(-7 0)"><g %s>' % xf(0, 0, 1 + 0.05 * k, 1 - 0.05 * k, rot)
    s += '<rect x="-21" y="-38" width="42" height="76" rx="9" fill="%s" %s/>' % (PAPER, st())
    s += '<rect x="-14" y="-28" width="28" height="48" rx="3" fill="%s" %s/>' % (BLUE, st(3.2))
    s += '<circle cx="0" cy="29" r="3.2" fill="%s"/>' % INK
    s += '</g>'
    # buzz marks either side
    if buzz > 0.05:
        for sd in (-1, 1):
            for j, r in enumerate((30, 39)):
                if j == 1:
                    continue                                   # the badge sits on that side
                a = math.radians(24)
                d = "M%.2f %.2f A%.2f %.2f 0 0 %d %.2f %.2f" % (sd * r * math.cos(a), 6 - r * math.sin(a), r, r, 1 if sd > 0 else 0,
                                                              sd * r * math.cos(a), 6 + r * math.sin(a))
                s += '<g opacity="%.3f">%s</g>' % (clamp(buzz * 1.6), path2(d, PAPER, 3.6, 3.2))
    # badge -> name tag -> badge
    ext = 0.0
    if n > 0:
        m = eio(u(t, T.P_NAME, T.P_NAME + 9 * F)) * (1 - eio(u(t, T.P_QUIET - 2 * F, T.P_QUIET + 7 * F)))
        mb = m + 0.10 * kick(t, T.P_NAME + 7 * F, 3.2, 9)
        last = max(c for c in counts if t >= c)
        pop = 1 + 0.42 * decay(t, last, 11) * math.cos(2 * math.pi * 3.2 * (t - last))
        bx, by, hw, hh = 20 + (74 - 20) * m, -29 + 29 * m, 15 + (50 - 15) * mb, 15 + 7.5 * m
        br = math.radians(rot) * (1 - m)
        bx, by = bx * math.cos(br) - by * math.sin(br), bx * math.sin(br) + by * math.cos(br)
        col = mix(RED, TAGC, m)
        s += '<g %s>' % xf(bx, by, pop if m < 0.02 else 1)
        s += '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" %s/>' % (-hw, -hh, 2 * hw, 2 * hh, hh, col, st(4.6))
        if m < 0.45:
            s += '<g opacity="%.3f">%s</g>' % (1 - u(m, 0.1, 0.45), text(str(n), 0, 8.2, 23))
        if m > 0.5:
            s += '<g opacity="%.3f" %s>%s</g>' % (u(m, 0.5, 0.9), xf(0, 0, 0.8 + 0.2 * u(m, 0.5, 1.0)), text("น้ำเหนือ", 0, 10, 25))
        s += '</g>'
        s += burst(t, T.P4 + F, 7, 20, 36, RED, 4, cx=20, cy=-29, rot=10)
        ext = 68.0 * m
    return s + '</g>', ext


# ------------------------------------------------------------------------------------------------ 4 trust
HEART = "M0 38 C-18 24 -45 5 -45 -16 C-45 -32 -33 -41 -21 -41 C-11 -41 -4 -35 0 -27 C4 -35 11 -41 21 -41 C33 -41 45 -32 45 -16 C45 5 18 24 0 38 Z"
CRACK = [(0, -27), (-8, -13), (6, -3), (-6, 9), (4, 21), (0, 38)]


def trust_level(t):
    return seg(t, 0.82, [(T.H_CASE + 0.05, T.H_CASE + 0.95, 0.60), (T.H_WAIT, T.H_WAIT + 0.7, 0.52), (T.H_EVERY + 0.05, T.H_EVERY + 1.25, 0.28),
                         (T.H_BACK, T.H_BACK + 1.2, 0.17), (T.H_SILENT, T.H_SILENT + 1.0, 0.07), (T.H_END, T.H_END + 0.3, 0.0)])


def heart(t, act):
    lv = trust_level(t)
    moving = abs(trust_level(t + 0.04) - trust_level(t - 0.04)) * 12
    dead = eio(u(t, T.H_END, T.H_END + 0.35))
    col = mix(RED, GREY, dead)
    face = mix(PAPER, SLOT, dead)
    k = kick(t, T.H_CASE + 0.1, 3, 6) * 0.5 + kick(t, T.H_CRACK, 4, 8) + kick(t, T.H_END, 3.5, 8) * 0.7 - 0.5 * math.sin(math.pi * u(t, T.H_SPLIT - 4 * F, T.H_SPLIT))
    sp = t - T.H_SPLIT
    inner = '<path d="%s" fill="%s"/>' % (HEART, face)
    if lv > 0.004:
        ys = 38 - lv * 79
        amp = 1.2 + 4.0 * clamp(moving) + 1.3 * level(t) * (1 if t < T.H_CASE else 0)
        pts = ["-50 60"]
        for i in range(0, 21):
            x = -50 + i * 5
            pts.append("%.2f %.2f" % (x, ys + amp * math.sin(2 * math.pi * (x / 46.0 + t * 1.3))))
        pts.append("50 60")
        inner += '<clipPath id="hc"><path d="%s"/></clipPath><path d="M%s Z" fill="%s" clip-path="url(#hc)"/>' % (HEART, " L".join(pts), col)
    inner += '<path d="%s" fill="none" %s/>' % (HEART, st())
    cr = eo(u(t, T.H_CRACK, T.H_CRACK + 5 * F)) * 0.55 + eo(u(t, T.H_END, T.H_END + 5 * F)) * 0.45
    npt = cr * (len(CRACK) - 1)
    cp = []
    for i, p in enumerate(CRACK):
        if i <= npt:
            cp.append(p)
        elif i - 1 < npt:
            a, f = CRACK[i - 1], npt - (i - 1)
            cp.append((a[0] + (p[0] - a[0]) * f, a[1] + (p[1] - a[1]) * f))
    crack = '<path d="M%s" fill="none" %s/>' % (" L".join("%.2f %.2f" % p for p in cp), st(4.2)) if len(cp) > 1 else ""
    s = ""
    if sp <= 0:
        s += '<g %s>%s%s</g>' % (xf(0, 0, 1 + 0.07 * k, 1 - 0.07 * k), inner, crack)
    else:
        # two halves drop apart and settle (they stay as the quiet status)
        zz = " ".join("%.2f,%.2f" % p for p in CRACK)
        fall = eo(u(sp, 0, 0.45)) + 0.12 * kick(t, T.H_SPLIT + 0.28, 3, 8)
        for sd, name in ((-1, "hl"), (1, "hr")):
            clip = '<clipPath id="%s"><polygon points="%s %d,60 %d,-60 0,-60"/></clipPath>' % (name, zz, sd * 70, sd * 70)
            s += '<g %s>%s<g clip-path="url(#%s)">%s</g><path d="M%s" fill="none" %s/></g>' % (
                xf(sd * 7.5 * fall, 5 * fall * (1 if sd < 0 else 0.4), 1, rot=sd * (9 if sd < 0 else 6) * fall), clip, name, inner,
                " L".join("%.2f %.2f" % p for p in CRACK), st(4.2))
    s += burst(t, T.H_CRACK, 5, 30, 46, PAPER, 4, cx=0, cy=-22, a0=-150, a1=-30)
    s += burst(t, T.H_SPLIT, 8, 40, 60, GREY, 4.5, rot=22)
    # the level as a bar along the strip
    bq = eo(u(t, T.H_IN + 3 * F, T.H_IN + 11 * F)) * (1 - eio(u(t, T.H_SPLIT - 1 * F, T.H_SPLIT + 9 * F)))
    ext = 0.0
    if bq > 0.02:
        L = 92 * bq
        s += hbar(54, L, lv, col, 22, face, sq=0.5 * abs(k), uid="hb")
        ext = 8 + L
    return s, ext + 10 * eo(u(sp, 0, 0.4))


# ------------------------------------------------------------------------------------------------ 5 danger
_PHI = None
HB = (38.68 + 0.147, 40.68 + 0.147)                     # heartbeat_low.wav starts at 38.68 / 40.68, its thump is 0.147 s in


def _phase(t):
    """heartbeat phase (beats) and rate at t"""
    global _PHI
    if _PHI is None:
        # (time, phase, rate): the beat (phase = n + 0.40, the spike) falls on the two heartbeat thumps of the mix
        keys = [(T.D_IN, 0.0, 0.90), (HB[0], 5.40, 1.20), (HB[1], 8.40, 1.90), (T.D_EYE + 0.5, 11.20, 2.60)]
        ts = np.arange(T.D_IN, T.D_EYE + 0.5, 1 / 240.0)
        ph = np.zeros(len(ts))
        for (t0, p0, r0), (t1, p1, r1) in zip(keys[:-1], keys[1:]):
            m = (ts >= t0) & (ts <= t1)
            h = t1 - t0
            x = (ts[m] - t0) / h
            ph[m] = (2 * x ** 3 - 3 * x ** 2 + 1) * p0 + (x ** 3 - 2 * x ** 2 + x) * h * r0 + (-2 * x ** 3 + 3 * x ** 2) * p1 + (x ** 3 - x ** 2) * h * r1
        _PHI = (ts, ph, np.gradient(ph, 1 / 240.0))
    return float(np.interp(t, _PHI[0], _PHI[1])), float(np.interp(t, _PHI[0], _PHI[2]))


def _ecg(v):
    v -= math.floor(v)
    if 0.10 < v < 0.22:
        return -5 * math.sin(math.pi * (v - 0.10) / 0.12)
    if 0.30 <= v < 0.35:
        return 6 * (v - 0.30) / 0.05
    if 0.35 <= v < 0.42:
        return 6 - 34 * (v - 0.35) / 0.07
    if 0.42 <= v < 0.49:
        return -28 + 42 * (v - 0.42) / 0.07
    if 0.49 <= v < 0.54:
        return 14 - 14 * (v - 0.49) / 0.05
    if 0.62 < v < 0.80:
        return -7 * math.sin(math.pi * (v - 0.62) / 0.18)
    return 0.0


def danger_value(t):
    v = seg(t, 0.12, [(T.D_IN + 0.8, T.D_LEAN - 3.0 + 2.0, 0.22), (T.D_LEAN, T.D_LEAN + 2.2, 0.40), (T.D_DRIVER - 0.4, T.D_DRIVER + 1.0, 0.58)])
    return v + (1 - v) * clamp(spring(t, T.D_EYE, 2.6, 9), 0, 1.06)


def danger_color(t):
    c = mix(GREEN, AMBER, eio(u(t, T.D_LEAN + 0.2, T.D_DRIVER)))
    return mix(c, RED, u(t, T.D_EYE - 1 * F, T.D_EYE + 2 * F))


def _shape(m, h):
    """outline: rounded square (m = 0) -> almond eye of half height h (m = 1), 72 points"""
    pts = []
    for i in range(72):
        th = 2 * math.pi * i / 72.0
        c, sn = math.cos(th), math.sin(th)
        x0 = 42 * math.copysign(abs(c) ** 0.42, c)
        y0 = 42 * math.copysign(abs(sn) ** 0.42, sn)
        x1 = 47 * c
        y1 = h * sn * abs(sn) * (1.0 if sn < 0 else 0.82)
        pts.append((x0 + (x1 - x0) * m, y0 + (y1 - y0) * m))
    return "M" + " L".join("%.2f %.2f" % p for p in pts) + " Z"


def danger(t, act):
    g = int(round(t * FPS))
    col = danger_color(t)
    m = eio(u(t, T.D_EYE - 5 * F, T.D_EYE - 1 * F))                       # badge -> closed lid
    op = clamp(spring(t, T.D_EYE, 3.0, 10), 0, 1.3)                       # lid snaps open
    lunge = t - T.D_LUNGE
    sq = math.sin(math.pi * u(t, T.D_LUNGE - 3 * F, T.D_LUNGE)) * 0.45    # squint before the lunge
    h = 4 + (30 - 4) * op * (1 - sq)
    s = ""
    if t < T.D_EYE:
        phi, rate = _phase(t)
        beat = math.exp(-6.0 * ((phi - 0.40) % 1.0))
        sc = 1 + (0.04 + 0.03 * u(rate, 1, 2.6)) * beat * (1 - m)
        fill = mix(col, PAPER, m * 0.0)
        d = _shape(m, 4)
        s += '<g %s><path d="%s" fill="%s" %s/>' % (xf(0, 0, sc), d, fill, st())
        Lb = 54 - 22 * u(rate, 0.95, 2.6)
        A = (0.72 + 0.34 * u(rate, 0.95, 2.6)) * (1 - m)
        pts = []
        x = -33.0
        while x <= 33.01:
            pts.append("%.2f %.2f" % (x, 2 + A * _ecg(phi - (33 - x) / Lb)))
            x += 1.0
        tr = "M" + " L".join(pts)
        s += '<clipPath id="dc"><path d="%s"/></clipPath><g clip-path="url(#dc)">' % d if m > 0 else '<g>'
        s += '<path d="%s" fill="none" %s/><path d="%s" fill="none" %s/></g></g>' % (tr, st(8.6 - 3 * m), tr, st(3.8 * (1 - m), PAPER))
    else:
        fl = 1 if 0 <= lunge < 2.5 * F else 0                                # flat red flash, 2 frames
        big = 0.5 * math.sin(math.pi * u(lunge, 0, 5 * F)) ** 0.7 if lunge >= 0 else 0
        shx = rnd(g, 7) * 7 * decay(t, T.D_LUNGE, 14) if lunge >= 0 else rnd(g, 8) * 0.5
        shy = rnd(g, 9) * 5 * decay(t, T.D_LUNGE, 14) if lunge >= 0 else rnd(g, 6) * 0.5
        d = _shape(1, h)
        look = 5 * math.sin(2 * math.pi * 0.45 * (t - T.D_EYE)) * u(t, T.D_EYE + 0.4, T.D_EYE + 0.9) * (0 if lunge >= 0 else 1)
        s += '<g %s><clipPath id="de"><path d="%s"/></clipPath>' % (xf(shx, shy, 1 + big), d)
        s += '<path d="%s" fill="%s"/>' % (d, RED if fl else PAPER)
        ir = 17.5 * clamp(op) * (1.12 if fl else 1)
        s += '<g clip-path="url(#de)"><circle cx="%.2f" cy="1" r="%.2f" fill="%s" %s/>' % (look, ir, PAPER if fl else RED, st(4.4))
        s += '<ellipse cx="%.2f" cy="1" rx="%.2f" ry="%.2f" fill="%s"/></g>' % (look, 4.6 * clamp(op), 10.5 * clamp(op), INK)
        s += '<path d="%s" fill="none" %s/></g>' % (d, st())
        s += burst(t, T.D_EYE, 9, 50, 72, RED, 4.5, rot=10)
        s += burst(t, T.D_LUNGE, 12, 56, 84, RED, 6, dur=7 * F, rot=5)
    # bar
    bq = eo(u(t, T.D_IN + 3 * F, T.D_IN + 11 * F)) * (1 - eio(u(t, T.D_LUNGE + 3 * F, T.D_LUNGE + 10 * F)))
    ext = 0.0
    if bq > 0.02:
        L = 92 * bq
        s += hbar(56, L, danger_value(t), col, 22, PAPER, sq=abs(kick(t, T.D_EYE, 4, 8)) + abs(kick(t, T.D_LUNGE, 4, 8)), uid="db")
        ext = 8 + L
    return s, ext


# ------------------------------------------------------------------------------------------------ 6 countdown / title mark
def biohazard(col=INK, uid="bz"):
    """the title's mark, flat: unit radius 30 (classic construction)"""
    s = '<mask id="%s" maskUnits="userSpaceOnUse" x="-32" y="-32" width="64" height="64"><rect x="-32" y="-32" width="64" height="64" fill="#000"/>' % uid
    cs = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (-90, 30, 150)]
    for c, sn in cs:
        s += '<circle cx="%.2f" cy="%.2f" r="15" fill="#fff"/>' % (11 * c, 11 * sn)
    for c, sn in cs:
        s += '<circle cx="%.2f" cy="%.2f" r="10.5" fill="#000"/>' % (15 * c, 15 * sn)
    s += '<clipPath id="%sc">' % uid + "".join('<circle cx="%.2f" cy="%.2f" r="9.3"/>' % (15 * c, 15 * sn) for c, sn in cs) + '</clipPath>'
    s += '<circle r="11.6" fill="none" stroke="#fff" stroke-width="3.6" clip-path="url(#%sc)"/>' % uid
    s += '<circle r="3.4" fill="#000"/>'
    for c, sn in cs:
        s += '<line x1="0" y1="0" x2="%.2f" y2="%.2f" stroke="#000" stroke-width="1.5"/>' % (6.5 * c, 6.5 * sn)
    s += '</mask><rect x="-32" y="-32" width="64" height="64" fill="%s" mask="url(#%s)"/>' % (col, uid)
    return s


def count_number(t):
    return 60 - sum(1 for i in (1, 2, 3) if t >= T.C_T0 + i)


def stopwatch(t, act, mm=0.0):
    """mm 0..1: stopwatch -> title mark (ring floods the face amber, buttons retract, the mark grows in)"""
    ticks = [T.C_T0 + i for i in (1, 2, 3)]
    k = sum(kick(t, tk, 5, 10) for tk in ticks)
    steps = sum(clamp(spring(tk and t, tk, 3, 11), 0, 1.2) for tk in ticks)
    rem = clamp(1 - 0.06 - 0.115 * steps - 0.022 * clamp(t - T.C_T0, 0, 9)) if t > T.C_IN + 0.2 else 1.0
    rem = 1 - (1 - rem) * eo(u(t, T.C_IN + 4 * F, T.C_IN + 12 * F))
    s = '<g %s>' % xf(0, 0, 1 + 0.05 * k, 1 - 0.05 * k, rot=4 * k)
    b = 1 - eio(u(mm, 0.0, 0.45))
    if b > 0.02:
        s += '<rect x="-7" y="%.2f" width="14" height="14" rx="3" fill="%s" %s/>' % (-34 - 13 * b, INK, st(3))
        s += '<line x1="27" y1="-22" x2="%.2f" y2="%.2f" %s/>' % (27 + 7 * b, -22 - 7 * b, st(8))
    R = 38
    s += '<circle cx="0" cy="4" r="%d" fill="%s" %s/>' % (R, mix(PAPER, AMBER, eio(u(mm, 0.15, 0.6))), st())
    if mm < 0.6:
        rr, w = 26.5, 9.0
        s += '<circle cx="0" cy="4" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (rr, SLOT, w)
        if rem > 0.004:
            a0 = 2 * math.pi * (1 - rem)
            x0, y0 = rr * math.sin(a0), 4 - rr * math.cos(a0)
            colr = mix(AMBER, RED, 0.0)
            if rem > 0.999:
                s += '<circle cx="0" cy="4" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (rr, colr, w)
            else:
                s += '<path d="M%.2f %.2f A%.2f %.2f 0 %d 1 0 %.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (
                    x0, y0, rr, rr, 1 if rem > 0.5 else 0, 4 - rr, colr, w)
            # the hand: sweeps once a second
            ha = 2 * math.pi * ((t - T.C_T0) % 1.0)
            ha = 2 * math.pi * (math.floor(t - T.C_T0) + eio(clamp(((t - T.C_T0) % 1.0) / 0.92))) if t >= T.C_T0 else 0.0
            s += '<line x1="0" y1="4" x2="%.2f" y2="%.2f" %s/>' % (19 * math.sin(ha), 4 - 19 * math.cos(ha), st(5.5))
            s += '<circle cx="0" cy="4" r="5" fill="%s"/>' % INK
    if mm > 0.3:
        z = back(u(mm, 0.3, 1.0), 2.2)
        s += '<g %s>%s</g>' % (xf(0, 4, max(z, 0.01) * 1.02, rot=-120 * (1 - eo(u(mm, 0.3, 1.0)))), biohazard(INK))
    s += '</g>'
    # number + bar to the right
    q = eo(u(t, T.C_IN + 3 * F, T.C_IN + 10 * F)) * (1 - eio(u(mm, 0.0, 0.3)))
    ext = 0.0
    if q > 0.02:
        n = count_number(t)
        last = max([T.C_IN] + [tk for tk in ticks if t >= tk])
        x = u(t, last, last + 6 * F)
        s += '<clipPath id="cn"><rect x="44" y="-40" width="90" height="52"/></clipPath><g clip-path="url(#cn)" opacity="%.3f">' % q
        tx = 'stroke="%s" stroke-width="7" stroke-linejoin="round" paint-order="stroke"' % INK
        if x < 1 and last > T.C_IN:
            s += '<g opacity="%.3f">%s</g>' % (1 - x, text(str(n + 1), 82, 8 - 46 * ei(x), 50, PAPER, extra=tx))
            s += text(str(n), 82, 8 + 46 * (1 - back(x, 1.4)), 50, PAPER, extra=tx)
        else:
            s += text(str(n), 82, 8, 50, PAPER, extra=tx)
        s += '</g>'
        s += hbar(50, 66 * q, rem, AMBER, 16, PAPER, uid="cb").replace('<rect', '<rect transform="translate(0 28)"').replace('<line', '<line transform="translate(0 28)"')
        ext = 8 + 68 * q
    return s, ext


# ------------------------------------------------------------------------------------------------ the row
#        id          draw       width (units)  joins     settles to quiet
ITEMS = [("radio", radio, 46, T.R_IN, T.R_QUIET),
         ("battery", battery, 90, T.B_IN, T.B_QUIET),
         ("calls", phone, 68, T.P_IN, T.P_QUIET),
         ("trust", heart, 100, T.H_IN, T.H_QUIET),
         ("danger", danger, 100, T.D_IN, T.D_QUIET),
         ("countdown", stopwatch, 82, T.C_IN, 1e9)]
QUIET_OPACITY = 0.92


def scene(t, aspect="916"):
    """-> (svg body in reference pixels, (y_top, y_bottom) of the rows that can hold ink) or (None, None)"""
    L = LAYOUT[aspect]
    g = int(round(t * FPS))
    x = float(L["shift"].get(shot_of(g), L["x0"]))
    y = L["y"]
    mm = eio(u(t, T.C_MORPH, T.TITLE - 1 * F))                              # stopwatch -> title mark
    row_op = 1 - eio(u(t, T.C_MORPH - 2 * F, T.C_MORPH + 8 * F))             # the quiet row leaves under the title
    out, used = [], False
    for a, b, o in L["fade"]:
        row_op *= 1 - (1 - o) * eio(u(t, a - 4 * F, a)) * (1 - eio(u(t, b, b + 5 * F)))
    for idx, (name, fn, wu, t_in, t_q) in enumerate(ITEMS):
        if t < t_in:
            break
        old = eio(u(t, ITEMS[idx + 2][3], ITEMS[idx + 2][3] + 14 * F)) if idx + 2 < len(ITEMS) else 0.0
        keep = L.get("keep")                                # LAYOUT keep = n: an item leaves the row once n + 1 newer ones have joined
        gone = eio(u(t, ITEMS[idx + keep + 1][3] - 2 * F, ITEMS[idx + keep + 1][3] + 10 * F)) if keep is not None and idx + keep + 1 < len(ITEMS) else 0.0
        t_out = (L.get("out") or {}).get(name)
        shut = gone
        if t_out is not None:                               # fade first, close the gap afterwards (no sliding over a neighbour)
            gone = max(gone, eio(u(t, t_out, t_out + 8 * F)))
            shut = max(shut, eio(u(t, t_out + 8 * F, t_out + 13 * F)))
        p = clamp(spring(t, t_in, 2.6, 10), 0, 1.25)
        pw = eo(u(t, t_in, t_in + 6 * F))
        act = 1 - eio(u(t, t_q, t_q + 10 * F))
        sc = L["q"] + (L["a"] - L["q"]) * act + (L["m"] - L["q"]) * old
        if name == "countdown":
            body, ext = fn(t, act, mm)
            tx, ty, tr = L["title"]
            cx0 = x + wu * sc / 2.0
            land = 1 + 0.10 * kick(t, T.TITLE, 3.2, 7)
            cx = cx0 + (tx - cx0) * mm
            cy = y + (ty - 4 * tr / 38.0 - y) * mm - 46 * math.sin(math.pi * mm) * (1 if mm < 1 else 0)
            s1 = sc + (tr / 38.0 - sc) * mm
            item = '<g %s>%s%s</g>' % (xf(cx, cy, s1 * p * land, s1 * p * (2 - land)), body,
                                       burst(t, T.TITLE, 12, 46, 70, AMBER, 5, dur=10 * F, rot=15, cy=4, clampy=False))
            out.append('<g filter="url(#kl)">%s</g>' % item)
            used = True
            break
        body, ext = fn(t, act)
        op = (QUIET_OPACITY + (1 - QUIET_OPACITY) * act) * row_op * u(t, t_in, t_in + 2 * F) * (1 - gone)
        cx = x + wu * sc / 2.0
        if op > 0.004:
            out.append('<g filter="url(#kl)" opacity="%.3f"><g %s>%s</g></g>' % (op, xf(cx, y, sc * p), body))
            used = True
        x += pw * (1 - shut) * ((wu + ext) * sc + L["gap"] * (1 - 0.4 * old))
    if not used:
        return None, None
    y0, y1 = y - L["band"], y + L["band"]
    if t >= T.C_MORPH:
        y1 = L["title"][1] + L["title"][2] * 1.9
        y0 = min(y0, L["title"][1] - L["title"][2] * 1.9)
    return "".join(out), (max(0, int(y0)), min(L["RH"], int(y1)))


DEFS = ('<defs><filter id="kl" x="-25%%" y="-40%%" width="150%%" height="180%%"><feMorphology in="SourceAlpha" operator="dilate" radius="%.2f" result="d"/>'
        '<feFlood flood-color="%s"/><feComposite in2="d" operator="in" result="k"/><feMerge><feMergeNode in="k"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter></defs>') % (KEY, PAPER)


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
class _Page(object):
    def __init__(self):
        self.proc, self.n = None, 0

    def request(self, job):
        if self.proc is None or self.proc.poll() is not None:
            env = dict(os.environ)
            env.setdefault("NODE_PATH", "/usr/local/lib/node_modules_global")
            self.proc = subprocess.Popen(["node", os.path.join(HERE, "raster_page.js")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         cwd=HERE, text=True, bufsize=1, env=env)
        self.n += 1
        self.proc.stdin.write(json.dumps(dict(job, id=self.n)) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("raster_page.js exited")
        rep = json.loads(line)
        if not rep.get("ok"):
            raise RuntimeError("raster failed: %s" % rep.get("error"))

    def stop(self):
        if self.proc is not None and self.proc.poll() is None:
            try:
                self.proc.stdin.write(json.dumps({"cmd": "quit"}) + "\n")
                self.proc.stdin.flush()
                self.proc.wait(timeout=10)
            except Exception:
                self.proc.kill()
        self.proc = None


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
    """the icon layer of film frame g at W x H: uint8 RGBA (H, W, 4), straight alpha, zeros where there is nothing"""
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


if __name__ == "__main__":
    for row in cue_table():
        print(row[0], row[1], row[2])
        for e in row[3]:
            print("    %7.3f  %s" % e)
