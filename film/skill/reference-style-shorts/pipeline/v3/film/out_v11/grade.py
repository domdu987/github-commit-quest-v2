"""grade.py - the v1.1 grade (BRIEF_POLISH.md section 3).

Entry point: grade_frame(img, g) -> img
    img: PIL RGB 720x1280 (a conformed frame, no captions), g: film frame 0..1964.
    Returns a PIL RGB 720x1280 image. Stateless and deterministic: every frame can be graded on its own,
    in any order and in any number of processes (see GRADE.md for the parallel runner).

Stages (in order; GRADE.md has the parameters and the numbers):
  1. per-shot correction   exposure / lift / gamma / pre-contrast / saturation / white balance, warm key on the
                           pale walls of the map-as-terrain shots (s19-s21), darker lower frame for s16.
                           Settings are per take and cross-fade over every dissolve, wipe and flash with the
                           conform's own weight, so nothing jumps at a join.
  2. tone curve            one gentle S-curve on luma for the whole film (hue preserving), white end 0.985.
  3. saturation            global x SAT_GLOBAL, vibrance style (pale colours get more, saturated ones less,
                           near-white fills none).
  4. haze                  exteriors (s08, s16, s23): warm airlight on the far pixels (sky / sea / horizon, i.e. close
                           to the colour that dominates their row) round the horizon height.
  5. bloom                 hot sources (lamps, windows, sun patches; faces ringed by ink get 15 %) with three radii,
                           plus a weak wide glow of every bright area; quarter size, screen blend; suppressed inside
                           bright areas so print on paper and signs is not lifted. Fixed thresholds, no
                           frame-adaptive normalisation: no pumping.
  6. fog bank              s23 only: a pale (#c9bfd0) soft band on the horizon, 40 -> 120 px over g1677-1719,
                           keyed by colour behind everything that is not sky / glow / hills / sea.
  7. red protect           strong reds (the hand-drawn line, the red print) keep their v1 hue and saturation.
  8. white protect         flat near-white fills (faces, hands, paper, lamp globes) keep their v1 colour and value.
  9. soft ceiling          per pixel, hue preserving: max channel above 0.965 is rolled into 0.965..0.993.
"""
import numpy as np
import cv2
from PIL import Image

cv2.setNumThreads(1)          # one thread per process; run several processes in parallel (GRADE.md)

W, H = 720, 1280
QW, QH = 180, 320             # quarter size for bloom / haze masks

# ------------------------------------------------------------------------------------------------
# film clock: takes, shots and joins (copied from PROJ/v3/film/out/work/joins.json, frozen with the edit)
# ------------------------------------------------------------------------------------------------
TAKES = [("hook", 0), ("s04", 129), ("s05", 199), ("s06", 271), ("s07", 336), ("s08", 401), ("s09", 505),
         ("s10", 610), ("s11", 694), ("s12", 792), ("s13", 839), ("s14", 868), ("s15", 956), ("s16", 1013),
         ("s17", 1086), ("s18", 1123), ("s19", 1189), ("s20", 1419), ("s21", 1516), ("s22", 1571),
         ("s23", 1664), ("s24", 1720), ("s25", 1788), ("s26", 1873)]
# (incoming take, kind, first, last) of every mixed join; weight of the incoming take:
#   dissolve: smoothstep((g - a + 1) / (L + 1)) exactly as conform.py; wipe / flash: linear over the range.
JOINS = [("s04", "d", 123, 134), ("s06", "d", 265, 277), ("s07", "d", 331, 340), ("s08", "d", 394, 408),
         ("s09", "d", 499, 511), ("s10", "d", 606, 614), ("s11", "d", 690, 698), ("s12", "d", 787, 797),
         ("s14", "d", 863, 873), ("s15", "d", 950, 962), ("s16", "d", 1007, 1019), ("s17", "d", 1079, 1092),
         ("s19", "d", 1183, 1194), ("s20", "d", 1415, 1423), ("s21", "d", 1511, 1520), ("s22", "d", 1564, 1577),
         ("s23", "d", 1656, 1672), ("s25", "l", 1785, 1790), ("s26", "l", 1868, 1876)]

# ------------------------------------------------------------------------------------------------
# settings
# ------------------------------------------------------------------------------------------------
# global tone curve on luma: (input, output) knots, monotone cubic.  p5 ~0.15 -> 0.11, p95 ~0.65 -> 0.75
CURVE = [(0.0, 0.0), (0.06, 0.052), (0.15, 0.118), (0.35, 0.400), (0.65, 0.785), (0.85, 0.938), (1.0, 0.985)]
SAT_GLOBAL = 1.18
# bloom, two sources:
#  hot  = light sources: pixels at the top of the range in the INPUT frame (max channel 0.955..0.985), grouped
#         into blobs; a blob ringed by dark ink (a face, a hand, a white card with an outline) keeps only
#         BLOOM_FACE of its glow, a blob with a soft or mid-grey rim (lamp globe, window, sun, sky) keeps all.
#  area = every bright area (max channel 0.78..0.97 after the tone curve), a weak wide glow (paper, sky, walls).
HOT_T0, HOT_T1 = 0.955, 0.985
HOT_SIG = (8.0, 26.0, 80.0)              # full-size px
HOT_GAIN = (0.80, 0.70, 0.30)
HOT_INSIDE = (0.60, 0.92)                # hot glow fades out only deep inside large hot areas
PALE = 0.80                              # blobs are grouped on max channel > PALE
INK_LUMA = 0.30                          # a rim pixel darker than this (quarter size) counts as ink outline
INK_FRAC = (0.12, 0.28)                  # share of ink in a blob's rim: glow x1 below 0.12, x BLOOM_FACE above 0.28
BLOOM_FACE = 0.15
AREA_T0, AREA_T1 = 0.78, 0.97
AREA_SIG = (40.0, 130.0)
AREA_GAIN = (0.07, 0.07)
BLOOM_TINT = (1.0, 0.94, 0.84)           # lamp warm
BLOOM_INSIDE_SIG = 18.0                  # density of bright pixels around a pixel (full-size px)
BLOOM_INSIDE = (0.42, 0.78)              # glow fades out where that density goes from 0.42 to 0.78 (text on paper, inside faces)
CEIL_KNEE, CEIL_MAX = 0.965, 0.993
# v1.1 fix round (review faults 1, 4, 5):
HOT_SAT = (0.20, 0.35)                   # hot source weight x (1 - smoothstep(S)): saturated sun on the floor is not a lamp
FILL_V, FILL_S = 0.85, 0.15              # near-white fill (input frame): max > 0.85, S < 0.15
FILL_HOLE = 20000                        # enclosed dark features up to this area (full-size px) count as inside the fill
FILL_CLOSE, FILL_ERODE, FILL_BLUR = 61, 5, 2.0   # closed over 61 px features (smeared eyes), eroded 5 px, feathered sigma 2 px

DEFAULT = dict(gain=1.0, lift=0.0, gamma=1.0, con=1.0, sat=1.0, wr=1.0, wg=1.0, wb=1.0,
               walls=0.0, lamp_g=0.85, lamp_b=0.77, lowdark=0.0, bloom=1.0, haze=0.0, haze_y=0.42, red=0.8, wprot=1.0, wsat=0.30)
SHOT = {
    # sunny beach: sky glow + warm haze in the distance
    "s08": dict(gain=0.93, sat=0.94, bloom=0.55, haze=0.16, haze_y=0.40),
    # grey beach drizzle: washed out -> more contrast, more saturation, darker foreground, a little haze
    "s16": dict(gain=0.88, con=1.30, sat=1.60, wr=1.04, wb=0.95, lowdark=0.22, gamma=1.08, haze=0.10, haze_y=0.38, bloom=0.7, wsat=0.13),
    # map as terrain: warm key on the pale walls, warmer overall, more saturation
    "s19": dict(wprot=0.0, walls=0.80, sat=1.12, wr=1.03, wb=0.95),
    "s20": dict(wprot=0.0, walls=0.85, sat=1.32, wr=1.05, wb=0.93),
    "s21": dict(wprot=0.0, walls=0.75, lamp_g=0.87, lamp_b=0.69, sat=1.60, wr=1.05, wb=0.92, con=1.06),
    # kitchen: already all warm, do not push it further
    "s15": dict(sat=0.93),
    # violet beach: a little warm haze
    "s23": dict(haze=0.10, haze_y=0.44),
    # night wave: leave the night, keep its bloom modest
    "s24": dict(bloom=0.8),
    # climax: lift the murk (shadows +0.06, gamma 0.9), lightning stays on top
    "s25": dict(lift=0.06, gamma=0.88, gain=1.04, sat=1.40),
}


def _params(take):
    p = dict(DEFAULT)
    p.update(SHOT.get(take, {}))
    return p


def take_weights(g):
    """[(take, weight)] for film frame g; two entries inside a mixed join."""
    cur = [t for t, a in TAKES if a <= g][-1]
    for inc, kind, a, b in JOINS:
        if a <= g <= b:
            prev = TAKES[[t for t, _ in TAKES].index(inc) - 1][0]
            if kind == "d":
                L = b - a + 1
                x = (g - a + 1) / (L + 1)
                w = x * x * (3 - 2 * x)
            else:
                w = (g - a + 1) / (b - a + 2)
            return [(prev, 1 - w), (inc, w)]
    return [(cur, 1.0)]


def params_at(g):
    out = {k: 0.0 for k in DEFAULT}
    for t, w in take_weights(g):
        p = _params(t)
        for k in out:
            out[k] += w * p[k]
    return out


# ------------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------------
def _ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _mono_lut(pts, n=4096):
    xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float)
    d = np.diff(ys) / np.diff(xs)
    m = np.zeros_like(xs)
    m[1:-1] = np.where(d[:-1] * d[1:] > 0, 2.0 / (1.0 / np.where(d[:-1] == 0, 1e-9, d[:-1]) + 1.0 / np.where(d[1:] == 0, 1e-9, d[1:])), 0.0)
    m[0] = d[0]; m[-1] = d[-1]
    x = np.linspace(0, 1, n)
    i = np.clip(np.searchsorted(xs, x) - 1, 0, len(xs) - 2)
    h = xs[i + 1] - xs[i]; t = (x - xs[i]) / h
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1; h10 = t ** 3 - 2 * t ** 2 + t; h01 = -2 * t ** 3 + 3 * t ** 2; h11 = t ** 3 - t ** 2
    y = h00 * ys[i] + h10 * h * m[i] + h01 * ys[i + 1] + h11 * h * m[i + 1]
    return np.maximum.accumulate(y).astype(np.float32)


_LUT = _mono_lut(CURVE)
_YY = (np.arange(H, dtype=np.float32) / H)[:, None]


def _mx(x):
    return np.maximum(np.maximum(x[..., 0], x[..., 1]), x[..., 2])


def _mn(x):
    return np.minimum(np.minimum(x[..., 0], x[..., 1]), x[..., 2])


def _luma(x):
    return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]


def _apply_luma_curve(x, lut):
    Y = _luma(x)
    Yn = lut[np.clip((Y * (len(lut) - 1)).astype(np.int32), 0, len(lut) - 1)]
    r = Yn / np.maximum(Y, 1e-4)
    out = x * r[..., None]
    mx = _mx(out)
    over = mx > 1.0                      # keep hue: scale the pixel down instead of clipping a channel
    out[over] /= mx[over][:, None]
    return out


def _sat(x, s):
    """saturation x s around luma; near-white low-saturation fills (faces, hands, paper) keep theirs."""
    if abs(s - 1.0) < 1e-4:
        return x
    mx = _mx(x); mn = _mn(x)
    S = (mx - mn) / np.maximum(mx, 1e-4)
    white = _ss(0.78, 0.92, mx) * (1.0 - _ss(0.06, 0.16, S))
    damp = (1.0 - 0.65 * np.clip(S, 0, 1)) if s > 1.0 else 1.0     # already saturated colours get less
    k = (1.0 + (s - 1.0) * (1.0 - white) * damp)[..., None]
    Y = _luma(x)[..., None]
    return np.clip(Y + (x - Y) * k, 0.0, 1.0)


def _hsv_parts(x):
    mx = _mx(x); mn = _mn(x); d = mx - mn
    S = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0.0)
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    dd = np.maximum(d, 1e-6)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) * 60.0
    return h, S, mx


def _far_mask(xq):
    """quarter-size weight of 'distance' pixels: close to the colour that dominates their row (sky, sea, haze)."""
    med = np.median(xq, axis=1, keepdims=True)
    d = np.sqrt(((xq - med) ** 2).sum(-1))
    m = np.exp(-(d / 0.085) ** 2).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), 1.2)


# ------------------------------------------------------------------------------------------------
# stages
# ------------------------------------------------------------------------------------------------
def stage_shot(x, p):
    if p['gain'] != 1.0:
        x = x * p['gain']
    if p['wr'] != 1.0 or p['wg'] != 1.0 or p['wb'] != 1.0:
        # white balance on the mid and dark tones only: near-white low-saturation fills keep their colour
        h, S, V = _hsv_parts(x)
        keep = (_ss(0.86, 0.97, V) * (1.0 - _ss(0.04, 0.14, S)))[..., None]
        wb = np.array([p['wr'], p['wg'], p['wb']], np.float32)
        x = x * (keep + (1.0 - keep) * wb)
    if p['walls'] > 0:
        # warm key on pale blue-grey / lavender surfaces (the high-pressure walls), shade stays cool
        h, S, V = _hsv_parts(x)
        hue_w = _ss(185, 205, h) * (1.0 - _ss(275, 300, h))
        w = p['walls'] * hue_w * (1.0 - _ss(0.22, 0.42, S)) * _ss(0.35, 0.75, V)
        Y = _luma(x)
        lamp = np.array([1.0, p['lamp_g'], p['lamp_b']], np.float32)
        lamp = lamp / (0.2126 * lamp[0] + 0.7152 * lamp[1] + 0.0722 * lamp[2])
        tgt = np.clip(Y[..., None] * lamp, 0, 1)
        x = x + (tgt - x) * w[..., None]
    if p['lift'] != 0.0:
        x = x + p['lift'] * (1.0 - x) * (1.0 - _ss(0.3, 0.9, x))
    if p['gamma'] != 1.0:
        x = np.power(np.clip(x, 0, 1), p['gamma'])
    if p['con'] != 1.0:
        Y = _luma(x)
        Yn = np.clip(0.42 + (Y - 0.42) * p['con'], 0.0, 1.0)
        x = x * (Yn / np.maximum(Y, 1e-4))[..., None]
    if p['lowdark'] > 0:
        f = 1.0 - p['lowdark'] * _ss(0.55, 1.0, _YY)
        x = x * f[..., None]
    if p['sat'] != 1.0:
        x = _sat(x, p['sat'])
    return np.clip(x, 0.0, 1.0)


def stage_haze(x, p, xq):
    if p['haze'] <= 0.005:
        return x
    far = _far_mask(xq)
    yq = (np.arange(QH, dtype=np.float32) / QH)[:, None]
    hy = p['haze_y']
    prof = np.exp(-((yq - hy) / 0.16) ** 2) * (yq < hy) + np.exp(-((yq - hy) / 0.07) ** 2) * (yq >= hy)
    w = (p['haze'] * far * prof).astype(np.float32)
    w = cv2.resize(w, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    Y = _luma(x)[..., None]
    air = np.array([1.0, 0.90, 0.76], np.float32) * np.clip(Y * 0.5 + 0.55, 0, 0.98)
    return x + (air - x) * w


def _hot_weight(x0q):
    """per-pixel weight of the hot (light source) bloom source, quarter size.
    The pale regions (max channel > PALE) are grouped into blobs; the share of dark ink in the 1-px (4 full-size px)
    rim round each blob decides whether its hot pixels glow fully (lamp globe, window, sun patch with a soft rim)
    or only at BLOOM_FACE (a face or hand inside its ink outline)."""
    mx = _mx(x0q)
    hot = _ss(HOT_T0, HOT_T1, mx).astype(np.float32)
    pale = (mx > PALE).astype(np.uint8)
    n, lab = cv2.connectedComponents(pale, connectivity=4)
    if n <= 1:
        return hot
    lab_d = cv2.dilate(lab.astype(np.float32), np.ones((3, 3), np.uint8), iterations=1).astype(np.int32)
    rim = (pale == 0) & (lab_d > 0)
    ink = rim & (_luma(x0q) < INK_LUMA)
    tot = np.bincount(lab_d[rim], minlength=n).astype(np.float32)
    nin = np.bincount(lab_d[ink], minlength=n).astype(np.float32)
    frac = nin / np.maximum(tot, 1.0)
    wcomp = (1.0 - (1.0 - BLOOM_FACE) * _ss(INK_FRAC[0], INK_FRAC[1], frac)).astype(np.float32)
    wcomp[0] = 1.0
    # v1.1 fix: only pale sources are hot (lamp globes, windows, white sun patches).  Sun on the saturated orange floor
    # sits right on HOT_T0..HOT_T1 and its per-frame blob test flickered (s11 g774-788, hook g86-90).
    S = (mx - _mn(x0q)) / np.maximum(mx, 1e-4)
    return hot * wcomp[lab] * (1.0 - _ss(HOT_SAT[0], HOT_SAT[1], S)).astype(np.float32)


def _fill_inner(x0):
    """v1.1 fix: full-size weight of the inside of near-white flat fills (faces, hands, paper, globes), closed over their
    dark features (eyes, brows, moustaches, mouths) so no glow lands on the ink inside a face."""
    mx = _mx(x0)
    S = (mx - _mn(x0)) / np.maximum(mx, 1e-4)
    fill = ((mx > FILL_V) & (S < FILL_S)).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (FILL_CLOSE, FILL_CLOSE))
    closed = cv2.morphologyEx(fill, cv2.MORPH_CLOSE, k)
    # features larger than the closing (a close-up eye, 70 x 90 px) are holes: non-fill components that the fill
    # encloses (they do not touch the frame edge) and that are smaller than FILL_HOLE px
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - closed, connectivity=4)
    x, y, w, h, area = st[:, 0], st[:, 1], st[:, 2], st[:, 3], st[:, 4]
    hole = (x > 0) & (y > 0) & (x + w < W) & (y + h < H) & (area < FILL_HOLE)
    hole[0] = False
    closed = np.maximum(closed, hole[lab].astype(np.uint8))
    inner = cv2.erode(closed, np.ones((FILL_ERODE, FILL_ERODE), np.uint8)).astype(np.float32)
    return cv2.GaussianBlur(inner, (0, 0), FILL_BLUR)[..., None]


def stage_bloom(x, p, x0):
    xq = cv2.resize(x, (QW, QH), interpolation=cv2.INTER_AREA)
    x0q = cv2.resize(x0, (QW, QH), interpolation=cv2.INTER_AREA)
    hot = _hot_weight(x0q)
    area = _ss(AREA_T0, AREA_T1, _mx(xq)).astype(np.float32)
    hotglow = np.zeros_like(xq)
    src = xq * hot[..., None]
    for s, a in zip(HOT_SIG, HOT_GAIN):
        hotglow += a * cv2.GaussianBlur(src, (0, 0), s / 4.0)
    dens_hot = cv2.GaussianBlur(hot, (0, 0), BLOOM_INSIDE_SIG / 4.0)
    hotglow *= (1.0 - _ss(HOT_INSIDE[0], HOT_INSIDE[1], dens_hot))[..., None]
    glow = np.zeros_like(xq)
    src = xq * area[..., None]
    for s, a in zip(AREA_SIG, AREA_GAIN):
        glow += a * cv2.GaussianBlur(src, (0, 0), s / 4.0)
    inside = cv2.GaussianBlur(area, (0, 0), BLOOM_INSIDE_SIG / 4.0)
    glow *= (1.0 - _ss(BLOOM_INSIDE[0], BLOOM_INSIDE[1], inside))[..., None]
    glow += hotglow
    glow *= np.array(BLOOM_TINT, np.float32) * p['bloom']
    glow = cv2.resize(glow, (W, H), interpolation=cv2.INTER_CUBIC)
    glow = np.clip(glow, 0.0, 0.9)
    y = 1.0 - (1.0 - x) * (1.0 - glow)
    return x + (y - x) * (1.0 - _fill_inner(x0))      # v1.1 fix: no glow inside near-white fills


FOG_G0, FOG_G1 = 1677, 1719          # 55.9 s .. 57.3 s
FOG_COL = np.array([0xc9, 0xbf, 0xd0], np.float32) / 255.0


def _horizon_q(xq):
    """quarter-size row of the sea horizon in s23: the strongest change of the row colour in the band 0.38..0.55 H."""
    med = np.median(xq, axis=1)
    lo, hi = int(0.38 * QH), int(0.55 * QH)
    dif = np.abs(np.diff(med, axis=0)).sum(-1)
    return lo + int(np.argmax(dif[lo:hi]))


def _fog_matte(xs):
    """weight (full size, on a strip of rows) of what the fog may cover in s23: violet sky, the pink-yellow horizon
    glow, the far hills and the sea (mid value, mid or low saturation). Everything else is a near object and stays in
    front: ink, poles and houses (dark), the face (bright), the straw hat and the hair (warm and saturated), the navy
    stripes (very saturated). Dark and bright objects are grown by 2 px so their anti-aliased edges stay clean."""
    h, S, V = _hsv_parts(xs)
    warm = ((h > 18) & (h < 200)).astype(np.float32)
    hard = np.maximum(1.0 - _ss(0.33, 0.38, V), _ss(0.84, 0.90, V)).astype(np.float32)
    hard = cv2.dilate(hard, np.ones((5, 5), np.uint8), iterations=1)
    near = np.maximum.reduce([hard, _ss(0.58, 0.64, S), warm * _ss(0.42, 0.50, S)]).astype(np.float32)
    return cv2.GaussianBlur(1.0 - near, (0, 0), 1.0)


def stage_fog(x, g, x0):
    if not (FOG_G0 - 6 <= g <= FOG_G1):
        return x
    t = np.clip((g - FOG_G0) / float(FOG_G1 - FOG_G0), 0.0, 1.0)
    e = t * t * (3 - 2 * t)
    a_in = _ss(FOG_G0 - 6, FOG_G0 + 4, g)
    # horizon follows the camera push: measured on v1 (row 600 at g1677 -> 612 at g1719)
    hz = 600.0 + 12.0 * e
    height = 40.0 + 80.0 * e
    yy = np.arange(H, dtype=np.float32)
    top = hz - height
    band = _ss(top - 0.45 * height - 10, top + 0.35 * height, yy) * (1.0 - _ss(hz + 2, hz + 16, yy))
    r0, r1 = 400, 680                                     # the band never leaves these rows
    far = np.zeros((H, W), np.float32)
    far[r0:r1] = _fog_matte(x0[r0:r1])
    alpha = (0.80 * a_in * band[:, None] * far)[..., None]
    # a little texture along x so it reads as a bank, not a ruled stripe (static in x, drifts slowly)
    xx = np.arange(W, dtype=np.float32)
    wav = 1.0 + 0.10 * np.sin(xx / 47.0 + 0.02 * g) + 0.06 * np.sin(xx / 19.0 - 0.05 * g)
    alpha = np.clip(alpha * wav[None, :, None], 0, 0.9)
    return x + (FOG_COL - x) * alpha


def stage_red_protect(x, x0, p):
    """strong reds (the hand-drawn line, the red print): v1 hue and saturation, graded luminance."""
    h, S, V = _hsv_parts(x0)
    red = (1.0 - _ss(10, 22, np.minimum(h, 360 - h))) * _ss(0.45, 0.65, S) * _ss(0.15, 0.35, V)
    red = cv2.GaussianBlur(red.astype(np.float32), (0, 0), 1.5)
    Y0 = _luma(x0); Y1 = _luma(x)
    tgt = x0 * (Y1 / np.maximum(Y0, 1e-4))[..., None]
    mx = _mx(tgt)
    over = mx > 1.0
    tgt[over] /= mx[over][:, None]
    w = (p['red'] * red)[..., None]
    return x + (tgt - x) * w


def stage_white_protect(x, x0, p):
    """flat near-white fills (faces, hands, white paper, lamp globes) keep their v1 colour and value (the soft ceiling
    then brings 1.0 down to 0.985): no per-shot tint, saturation, curve lift or glow cast lands on them, they stay flat,
    and paper under the captions does not get brighter than in v1. Glow that a lamp throws onto them from outside is
    kept up to +0.02."""
    mx0 = _mx(x0); mn0 = _mn(x0)
    S0 = (mx0 - mn0) / np.maximum(mx0, 1e-4)
    wm = p['wprot'] * _ss(0.74, 0.86, mx0) * (1.0 - _ss(p['wsat'] - 0.08, p['wsat'], S0))
    wm = cv2.GaussianBlur(wm.astype(np.float32), (0, 0), 1.0)[..., None]
    tgt = np.maximum(x0, np.minimum(x, x0 + 0.02))
    return x + (tgt - x) * wm


def stage_ceiling(x):
    mx = _mx(x)
    k, c = CEIL_KNEE, CEIL_MAX
    over = mx > k
    if over.any():
        m = mx[over]
        nm = k + (c - k) * (1.0 - np.exp(-(m - k) / (c - k)))
        x[over] *= (nm / m)[:, None]
    return x


def grade_array(a, g):
    """a: HxWx3 uint8 RGB -> HxWx3 uint8 RGB"""
    x0 = a.astype(np.float32) / 255.0
    p = params_at(g)
    x = stage_shot(x0, p)
    x = _apply_luma_curve(x, _LUT)
    x = _sat(x, SAT_GLOBAL)
    xq = None
    if p['haze'] > 0.005:
        xq = cv2.resize(x, (QW, QH), interpolation=cv2.INTER_AREA)
    x = stage_haze(x, p, xq)
    x = stage_bloom(x, p, x0)
    x = stage_fog(x, g, x0)
    x = stage_red_protect(x, x0, p)
    x = stage_white_protect(x, x0, p)
    x = stage_ceiling(np.clip(x, 0.0, 1.5))
    return (np.clip(x, 0, 1) * 255.0 + 0.5).astype(np.uint8)


def grade_frame(img, g):
    if img.mode != "RGB":
        img = img.convert("RGB")
    a = np.asarray(img)
    if a.shape[0] != H or a.shape[1] != W:
        raise ValueError("expected 720x1280, got %dx%d" % (a.shape[1], a.shape[0]))
    return Image.fromarray(grade_array(a, int(g)), "RGB")


if __name__ == "__main__":
    # python3 grade.py SRC_DIR DST_DIR [first last [step]]  : grade g_%04d.png frames (resumable)
    import os, sys, time
    src, dst = sys.argv[1], sys.argv[2]
    g0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    g1 = int(sys.argv[4]) if len(sys.argv) > 4 else 1964
    st = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    os.makedirs(dst, exist_ok=True)
    t0 = time.time(); n = 0
    for g in range(g0, g1 + 1, st):
        o = os.path.join(dst, "g_%04d.png" % g)
        if os.path.exists(o):
            continue
        im = grade_frame(Image.open(os.path.join(src, "g_%04d.png" % g)), g)
        im.save(o + ".tmp.png"); os.replace(o + ".tmp.png", o); n += 1
    print("graded %d frames in %.1f s" % (n, time.time() - t0))
