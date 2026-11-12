#!/usr/bin/env python3
"""Head detection and outline measurement used by score.py.

A head is a large, near-circular, pale (bright, low-saturation) blob that is
ringed by a dark ink line and carries dark face features.  Detection is kept
deliberately lenient (shaded or tinted heads are still found) so that the
measurements, not the detector, decide the score.
"""
import math
import numpy as np
import cv2

W, H = 720, 1280
LEVELS = (200, 140)          # thresholds on min(R,G,B) for the pale-blob mask
SAT_MAX = 0.30               # (max-min)/max of a pale pixel
N_RAYS = 120                 # one ray every 3 degrees; 0 deg = 3 o'clock, 90 deg = down


_LUMA_M = np.array([[0.0722, 0.7152, 0.2126]], np.float32)


def luma_of(bgr):
    """Rec.709 luma of the encoded values, float32 0..255."""
    return cv2.transform(bgr, _LUMA_M).astype(np.float32)


def minmax_of(bgr):
    b, g, r = cv2.split(bgr)
    return cv2.min(cv2.min(b, g), r), cv2.max(cv2.max(b, g), r)


def _circumcircles(p1, p2, p3):
    ax, ay = p1[:, 0], p1[:, 1]
    bx, by = p2[:, 0], p2[:, 1]
    cx, cy = p3[:, 0], p3[:, 1]
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    d = np.where(np.abs(d) < 1e-6, np.nan, d)
    a2 = ax * ax + ay * ay; b2 = bx * bx + by * by; c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d
    r = np.hypot(ax - ux, ay - uy)
    return ux, uy, r


def _lsq_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x * x + y * y
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    r2 = c[2] + c[0] ** 2 + c[1] ** 2
    return float(c[0]), float(c[1]), float(math.sqrt(max(r2, 1e-6)))


def fit_circle(pts, rmin, rmax, rng, iters=140):
    """RANSAC circle through contour points; returns (cx, cy, r, coverage, inlier share) or None."""
    n = len(pts)
    if n < 12:
        return None
    idx = rng.integers(0, n, (iters, 3))
    ux, uy, r = _circumcircles(pts[idx[:, 0]], pts[idx[:, 1]], pts[idx[:, 2]])
    ok = np.isfinite(r) & (r >= rmin) & (r <= rmax)
    if not ok.any():
        return None
    ux, uy, r = ux[ok], uy[ok], r[ok]
    d = np.abs(np.hypot(pts[None, :, 0] - ux[:, None], pts[None, :, 1] - uy[:, None]) - r[:, None])
    tol = np.maximum(1.5, 0.03 * r)[:, None]
    inl = d < tol
    # score = angular coverage (36 bins) rather than raw count: a dense flat edge must not win
    ang = np.arctan2(pts[None, :, 1] - uy[:, None], pts[None, :, 0] - ux[:, None])
    bins = ((ang + math.pi) / (2 * math.pi) * 36).astype(np.int32) % 36
    occ = np.zeros((len(r), 36), bool)
    rows = np.broadcast_to(np.arange(len(r))[:, None], bins.shape)
    occ[rows[inl], bins[inl]] = True
    cov = occ.sum(1)
    best = int(np.argmax(cov + 0.001 * inl.sum(1)))
    cx, cy, rr = float(ux[best]), float(uy[best]), float(r[best])
    for _ in range(3):
        dd = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - rr)
        m = dd < max(1.5, 0.035 * rr)
        if m.sum() < 8:
            return None
        cx, cy, rr = _lsq_circle(pts[m])
    dd = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - rr)
    m = dd < max(1.5, 0.035 * rr)
    if m.sum() < 8 or not (rmin <= rr <= rmax):
        return None
    a = np.arctan2(pts[m, 1] - cy, pts[m, 0] - cx)
    b72 = np.unique(((a + math.pi) / (2 * math.pi) * 72).astype(np.int32) % 72)
    return cx, cy, rr, len(b72) / 72.0, float(m.mean())


_RAY_ANG = np.deg2rad(np.arange(N_RAYS) * (360.0 / N_RAYS))
_RAY_COS = np.cos(_RAY_ANG).astype(np.float32)
_RAY_SIN = np.sin(_RAY_ANG).astype(np.float32)


def measure_rays(Y, cx, cy, r):
    """Walk N_RAYS rays outward through the fill edge and the ink line.

    Returns arrays per ray: r_in (fill/ink half-maximum radius), width (ink width, nan when the
    outer side is not bounded by a lighter background), has_ink (a dark line or dark background
    follows the fill), r_min (radius of the darkest ink sample)."""
    step = 0.5
    radii = np.arange(0.62 * r, 1.42 * r + 1.0, step, dtype=np.float32)
    mx = cx + _RAY_COS[:, None] * radii[None, :]
    my = cy + _RAY_SIN[:, None] * radii[None, :]
    Pm = cv2.remap(Y, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=-1.0)
    n = len(radii)
    i_a = int((0.80 * r - radii[0]) / step); i_b = int((0.92 * r - radii[0]) / step)
    i_s = int((0.90 * r - radii[0]) / step)
    r_in = np.full(N_RAYS, np.nan); width = np.full(N_RAYS, np.nan)
    r_min = np.full(N_RAYS, np.nan); has_ink = np.zeros(N_RAYS, bool); offframe = np.zeros(N_RAYS, bool)
    edge = np.full(N_RAYS, np.nan)     # 10 to 90 percent width of the fill-to-ink edge, px
    lf_all = np.median(Pm[:, i_a:i_b + 1], axis=1)
    lf_glob = float(np.percentile(lf_all[lf_all >= 0], 70)) if (lf_all >= 0).any() else 0.0
    wmax = 0.24 * r            # an ink line is never wider than 0.11 D
    kmax = int(wmax / step)
    for k in range(N_RAYS):
        p = Pm[k]
        if p[min(n - 1, i_s + int(0.2 * r / step))] < 0:
            offframe[k] = True
            continue
        lf = float(lf_all[k])
        if lf < 0.6 * lf_glob:         # hair, hat or a feature sits on the rim here
            continue
        thr = lf - max(45.0, 0.30 * lf)
        seg = p[i_s:]
        below = np.nonzero(seg < thr)[0]
        if len(below) == 0:
            continue
        j0 = int(below[0])
        # first trough: follow the profile down until it rises again by more than 12 levels
        j = j0; lmin = seg[j]; jmin = j
        jend = min(len(seg) - 1, j0 + kmax)
        while j < jend:
            j += 1
            v = seg[j]
            if v < 0:
                break
            if v < lmin:
                lmin = v; jmin = j
            elif v > lmin + 12.0:
                break
        if lmin > 0.42 * lf:
            continue
        has_ink[k] = True
        half_in = 0.5 * (lf + lmin)
        ji = jmin
        while ji > 0 and seg[ji] < half_in:
            ji -= 1
        a, b = seg[ji], seg[min(ji + 1, len(seg) - 1)]
        frac = (a - half_in) / (a - b) if a != b else 0.0
        rin = radii[i_s] + (ji + min(max(frac, 0.0), 1.0)) * step
        r_in[k] = rin
        r_min[k] = radii[i_s] + jmin * step
        # edge softness: distance between the 10 and the 90 percent point of the fall from fill to ink
        l10 = lf - 0.10 * (lf - lmin); l90 = lf - 0.90 * (lf - lmin)
        j9 = jmin
        while j9 > 0 and seg[j9 - 1] < l90:
            j9 -= 1
        j1 = j9
        while j1 > 0 and seg[j1] < l10:
            j1 -= 1
        if j9 > 0 and j1 < j9 and seg[j1] >= l10:
            a9, b9 = seg[j9 - 1], seg[j9]
            p90 = (j9 - 1) + ((a9 - l90) / (a9 - b9) if a9 != b9 else 0.0)
            a1, b1 = seg[j1], seg[j1 + 1]
            p10 = j1 + ((a1 - l10) / (a1 - b1) if a1 != b1 else 0.0)
            if p90 > p10:
                edge[k] = (p90 - p10) * step
        # outer side: background within 0.10 D after the trough must be clearly lighter
        j2 = min(len(seg) - 1, jmin + int(0.20 * r / step))
        out = seg[jmin:j2 + 1]
        if (out < 0).any() or len(out) < 3:
            continue
        lout = float(out.max())
        if lout - lmin < max(35.0, 0.25 * (lf - lmin)):
            continue
        half_out = 0.5 * (lout + lmin)
        up = np.nonzero(out >= half_out)[0]
        jo = int(up[0])
        a, b = out[jo - 1], out[jo]
        frac = (half_out - a) / (b - a) if b != a else 0.0
        rout = radii[i_s] + (jmin + jo - 1 + min(max(frac, 0.0), 1.0)) * step
        w = rout - rin
        if 0.012 * r <= w <= wmax:
            width[k] = w
    return dict(r_in=r_in, width=width, has_ink=has_ink, r_min=r_min, offframe=offframe, lf=lf_all, edge=edge)


def _pale_base(mn, mx):
    """uint8 image: min channel where the pixel is low in saturation, else 0."""
    lim = cv2.multiply(mx, 1.0 - SAT_MAX)            # mn must exceed (1 - SAT_MAX) * mx
    ok = cv2.compare(mn, lim, cv2.CMP_GT)
    return cv2.bitwise_and(mn, ok)


def detect_heads(bgr, Y=None, min_d=44, rng=None, want_limbs=False):
    """Find heads in a 720x1280 BGR frame.  Returns a list of dicts.

    Keys: cx, cy, r_fill (fitted fill circle), D (outer diameter, ink to ink), thin, thick
    (ink width / D on the thin and thick side), ink_bgr, fill_bgr, flat (luma p95 - p5 of the
    fill, 0..1), outline_ok (enough rays with a bounded ink line), cov (visible arc share),
    eyes (the face test of has_eyes; the caller decides what to do with blobs that fail it)."""
    if rng is None:
        rng = np.random.default_rng(1234)
    if Y is None:
        Y = luma_of(bgr)
    hh, ww = bgr.shape[:2]
    mn, mx = minmax_of(bgr)
    base = _pale_base(mn, mx)
    base[850:960, :] = 0                        # caption band: white text is not a head
    cands = []
    k3 = np.ones((3, 3), np.uint8)
    for level in LEVELS:
        m = cv2.compare(base, level, cv2.CMP_GT)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k3)
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            if len(c) < 60:
                continue
            x, y, w, h = cv2.boundingRect(c)
            if max(w, h) < 0.7 * min_d or w * h < 0.5 * min_d * min_d:
                continue
            area = cv2.contourArea(c)
            if area < 0.45 * math.pi * (min_d / 2) ** 2:
                continue
            pts = c.reshape(-1, 2).astype(np.float64)
            keep = (pts[:, 0] > 1) & (pts[:, 0] < ww - 2) & (pts[:, 1] > 1) & (pts[:, 1] < hh - 2)
            keep &= ~((pts[:, 1] >= 846) & (pts[:, 1] <= 963))
            pts = pts[keep]
            if len(pts) < 40:
                continue
            if len(pts) > 220:
                pts = pts[np.linspace(0, len(pts) - 1, 220).astype(int)]
            fit = fit_circle(pts, 0.42 * min_d, 0.75 * max(w, h) + 4, rng)
            if fit is None:
                continue
            cx, cy, r, cov, inl = fit
            if cov < 0.36:
                continue
            # the blob must fill most of the fitted disc and not be much bigger than it
            if area < 0.45 * math.pi * r * r or area > 1.6 * math.pi * r * r:
                continue
            dup = False
            for o in cands:
                if math.hypot(cx - o['cx'], cy - o['cy']) < 0.06 * r and abs(r - o['r']) < 0.06 * r:
                    dup = True
                    if cov > o['cov']:
                        o.update(cx=cx, cy=cy, r=r, cov=cov, inl=inl, level=level, area=area)
                    break
            if not dup:
                cands.append(dict(cx=cx, cy=cy, r=r, cov=cov, inl=inl, level=level, area=area))
    ver = []
    for c in cands:
        hd = _verify(bgr, Y, mn, mx, c)
        if hd is not None:
            ver.append(hd)
    # overlapping detections: the better-measured one wins, except that a much smaller circle
    # inside a head (an eye ring, a button) always loses to the head
    ver.sort(key=lambda d: -(d['n_valid'] / N_RAYS + d['cov'] + d['ink_share']))
    out = []
    for h in ver:
        drop = False
        for i, o in enumerate(out):
            if math.hypot(h['cx'] - o['cx'], h['cy'] - o['cy']) < max(h['r_fill'], o['r_fill']):
                if h['r_fill'] > 1.8 * o['r_fill']:
                    out[i] = None
                else:
                    drop = True
        out = [o for o in out if o is not None]
        if not drop:
            out.append(h)
    for h in out:
        h['eyes'] = has_eyes(Y, h)
        if want_limbs:
            h['limb'] = limb_width(Y, mn, mx, h)
    return out


def _verify(bgr, Y, mn, mx, c):
    cx, cy, r = c['cx'], c['cy'], c['r']
    hh, ww = Y.shape
    x0 = int(max(0, cx - r)); x1 = int(min(ww, cx + r + 1)); y0 = int(max(0, cy - r)); y1 = int(min(hh, cy + r + 1))
    if x1 - x0 < 10 or y1 - y0 < 10:
        return None
    sub = bgr[y0:y1, x0:x1]; subY = Y[y0:y1, x0:x1]
    smn = mn[y0:y1, x0:x1].astype(np.int16); smx = mx[y0:y1, x0:x1].astype(np.int16)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    rr = np.hypot(xx - cx, yy - cy) / r
    disc = rr < 0.90
    if disc.sum() < 200:
        return None
    pale = (smn > 135) & ((smx - smn) < SAT_MAX * smx)
    pale_share = float(pale[disc].mean())
    if pale_share < 0.50:
        return None
    lf = float(np.median(subY[disc & pale]))
    dark = subY < min(110.0, 0.5 * lf)
    feat_share = float(dark[rr < 0.80].mean())
    if feat_share < 0.004 or feat_share > 0.42:
        return None
    rays = measure_rays(Y, cx, cy, r)
    onframe = ~rays['offframe']
    if onframe.sum() < 0.45 * N_RAYS:
        return None
    # refine the circle on the measured inner ink edge (the pale blob misses a wide crescent)
    k_ink = np.nonzero(rays['has_ink'] & np.isfinite(rays['r_in']))[0]
    if len(k_ink) >= 24:
        ep = np.c_[cx + _RAY_COS[k_ink] * rays['r_in'][k_ink], cy + _RAY_SIN[k_ink] * rays['r_in'][k_ink]].astype(np.float64)
        fit = fit_circle(ep, 0.85 * r, 1.35 * r, np.random.default_rng(7), iters=80)
        if fit is not None and fit[3] >= max(0.33, 0.8 * c['cov']) and math.hypot(fit[0] - cx, fit[1] - cy) < 0.35 * r:
            if abs(fit[2] - r) > 0.012 * r or math.hypot(fit[0] - cx, fit[1] - cy) > 0.012 * r:
                cx, cy, r = fit[0], fit[1], fit[2]
                rays = measure_rays(Y, cx, cy, r)
                onframe = ~rays['offframe']
                rr = np.hypot(xx - cx, yy - cy) / r
                disc = rr < 0.90
    rin = rays['r_in']
    oncirc = np.isfinite(rin) & (np.abs(rin - r) < 0.07 * r)
    ink_share = float((rays['has_ink'] & oncirc).sum() / max(1, onframe.sum()))
    if ink_share < 0.33:
        return None
    wv = np.where(oncirc, rays['width'], np.nan)
    valid = np.isfinite(wv)
    # drop the two rays at each end of every measured arc: there the ink runs into a hat brim or hair
    v2 = valid.copy()
    for o in (1, 2):
        v2 &= np.roll(valid, o) & np.roll(valid, -o)
    if valid.all():
        v2 = valid
    wv = np.where(v2, wv, np.nan)
    valid = v2
    nvalid = int(valid.sum())
    D0 = 2 * r / 0.91
    if nvalid < 0.15 * N_RAYS and D0 < 110:
        return None        # small blob without a measurable ink ring: not accepted as a head
    inkm = cv2.dilate(dark.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    fillm = disc & pale & ~inkm          # fill only: coloured hair and hats are not part of it
    if fillm.sum() < 100:
        return None
    fp = sub[fillm].astype(np.float32)
    fill_bgr = np.median(fp, axis=0)
    fY = subY[fillm]
    flat = float(np.percentile(fY, 95) - np.percentile(fY, 5)) / 255.0
    hd = dict(cx=float(cx), cy=float(cy), r_fill=float(r), cov=float(c['cov']), level=int(c['level']),
              pale_share=pale_share, feat_share=feat_share, ink_share=ink_share, n_valid=nvalid,
              fill_bgr=[float(v) for v in fill_bgr], flat=flat,
              thin=float('nan'), thick=float('nan'), ink_bgr=None, D=float(D0), outline_ok=False,
              thick_angle=float('nan'), partial=bool(onframe.sum() < N_RAYS), limb=float('nan'), edge_px=float('nan'))
    # edge softness on rays whose ink line is at least 3 px wide (a thinner line never reaches full ink darkness)
    ev = rays['edge'][valid & (wv >= 3.0)] if valid.any() else np.array([])
    ev = ev[np.isfinite(ev)]
    if len(ev) >= 8:
        hd['edge_px'] = float(np.median(ev))
    hd['_rays'] = dict(r_in=rin, width=wv, r_min=rays['r_min'])
    if nvalid >= 0.15 * N_RAYS:
        ws = wv.copy()
        for k in np.nonzero(valid)[0]:
            nb = [wv[(k + o) % N_RAYS] for o in (-1, 0, 1)]
            nb = [v for v in nb if np.isfinite(v)]
            ws[k] = float(np.median(nb))
        w = ws[valid]
        thin = float(np.percentile(w, 10)); thick = float(np.percentile(w, 90))
        opp = []
        for k in np.nonzero(valid)[0]:
            k2 = (k + N_RAYS // 2) % N_RAYS
            if valid[k2]:
                opp.append(ws[k] + ws[k2])
        ink2 = float(np.median(opp)) if len(opp) >= 6 else thin + thick
        D = 2 * r + ink2
        hd['D'] = float(D)
        hd['thin'] = thin / D; hd['thick'] = thick / D
        hd['outline_ok'] = True
        ang = _RAY_ANG[valid]
        dev = w - np.median(w)
        hd['thick_angle'] = float(np.degrees(math.atan2(float(np.sum(dev * np.sin(ang))), float(np.sum(dev * np.cos(ang))))) % 360)
        ks = np.nonzero(valid)[0]
        wide = w >= 2.5                 # only strokes at least 2.5 px wide give a clean centre colour
        if wide.sum() >= 5:
            ks = ks[wide]
            px = np.clip(np.round(cx + _RAY_COS[ks] * rays['r_min'][ks]).astype(int), 0, ww - 1)
            py = np.clip(np.round(cy + _RAY_SIN[ks] * rays['r_min'][ks]).astype(int), 0, hh - 1)
            hd['ink_bgr'] = [float(v) for v in np.median(bgr[py, px].astype(np.float32), axis=0)]
    return hd


def has_eyes(Y, hd):
    """Face test: does the fill carry a pair of eyes?

    Dark connected components inside the fill that do not touch the rim (those are hat, hair or
    outline) are candidates when 0.035-0.30 D wide and 0.012-0.30 D tall.  A face has two of them
    at the same height (within 0.10 D), 0.13-0.45 D apart and of similar size, or one wide
    component with two holes (two ring eyes that touch, or glasses).  Clock faces, calendar pages
    and sheets of text fail this test."""
    cx, cy, r = hd['cx'], hd['cy'], hd['r_fill']
    D = hd['D']
    hh, ww = Y.shape
    x0 = int(max(0, cx - r)); x1 = int(min(ww, cx + r + 1)); y0 = int(max(0, cy - r)); y1 = int(min(hh, cy + r + 1))
    if x1 - x0 < 12 or y1 - y0 < 12:
        return False
    sub = Y[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1]
    rr = np.hypot(xx - cx, yy - cy) / r
    inner = rr < 0.85
    if inner.sum() < 100:
        return False
    lf = float(np.percentile(sub[inner], 75))
    dark = ((sub < 0.55 * lf) & (rr < 0.90)).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
    cands = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < max(4, 0.0004 * D * D):
            continue
        m = lab[y:y + h, x:x + w] == i
        if rr[y:y + h, x:x + w][m].max() > 0.885:
            continue
        wd, hd_ = w / D, h / D
        if 0.30 <= wd <= 0.56 and 0.10 <= hd_ <= 0.30 and wd >= 1.6 * hd_:
            cnts, hier = cv2.findContours(m.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            holes = 0
            if hier is not None:
                for c, hr in zip(cnts, hier[0]):
                    if hr[3] >= 0 and cv2.contourArea(c) >= 0.002 * D * D:
                        holes += 1
            if holes >= 2:
                return True
        if 0.035 <= wd <= 0.30 and 0.012 <= hd_ <= 0.30:
            cands.append((cen[i][0], cen[i][1], wd, hd_, float(a)))
    for i in range(len(cands)):
        for j in range(i + 1, len(cands)):
            a, b = cands[i], cands[j]
            dx = abs(a[0] - b[0]) / D; dy = abs(a[1] - b[1]) / D
            if 0.13 <= dx <= 0.45 and dy <= 0.10 and 0.33 <= a[4] / b[4] <= 3.0 and max(a[2], b[2]) / min(a[2], b[2]) < 2.2:
                return True
    return False


def limb_width(Y, mn, mx, hd, debug=False):
    """Best-effort limb stroke width / D.

    In the body area under the head, take the dark, low-chroma (ink) mask, its distance
    transform and the ridge of that transform (local maxima): each ridge pixel carries the local
    stroke width 2 * dt - 0.5.  Limbs are long strokes of one constant width, so they make a
    sharp peak in the histogram of ridge widths.  The peak between 0.045 and 0.105 D is the limb
    width, accepted only when at least 0.6 D of ridge lies within 0.01 D of it.  nan otherwise."""
    D = hd['D']
    if D < 95 or D > 330 or not hd.get('outline_ok', False):
        return float('nan')
    hh, ww = Y.shape
    x0 = int(max(0, hd['cx'] - 1.0 * D)); x1 = int(min(ww, hd['cx'] + 1.0 * D))
    y0 = int(max(0, hd['cy'] + 0.50 * D)); y1 = int(min(hh, hd['cy'] + 3.1 * D))
    if y1 - y0 < 1.0 * D or x1 - x0 < 1.2 * D:
        return float('nan')
    sy = Y[y0:y1, x0:x1]
    chroma = cv2.subtract(mx[y0:y1, x0:x1], mn[y0:y1, x0:x1])
    m = ((sy < 80) & (chroma < 55)).astype(np.uint8)
    cy0 = max(0, 846 - y0); cy1 = min(y1 - y0, 964 - y0)
    if cy1 > cy0:
        m[cy0:cy1, :] = 0
    if m.mean() > 0.40:
        return float('nan')
    dt = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    dil = cv2.dilate(dt, np.ones((3, 3), np.uint8))
    ridge = (dt >= dil - 1e-4) & (dt >= 1.5)
    wd = (2.0 * dt[ridge] - 0.5) / D
    edges = np.arange(0.030, 0.1301, 0.005)
    hist = np.histogram(wd, bins=edges)[0].astype(float)
    cen = 0.5 * (edges[:-1] + edges[1:])
    inband = (cen >= 0.045) & (cen <= 0.105)
    sm = np.convolve(np.where(inband, hist, 0.0), [0.5, 1.0, 0.5], mode='same')
    if debug:
        print('   ridge widths (w/D: px/D):', ' '.join('%.3f:%.2f' % (a, b / D) for a, b in zip(cen, hist)))
    if not inband.any():
        return float('nan')
    p = int(np.argmax(np.where(inband, sm, -1)))
    sel = (np.abs(wd - cen[p]) <= 0.010) & (wd >= 0.045)
    if sel.sum() < 0.6 * D:
        return float('nan')
    return float(np.mean(wd[sel]))


def draw_head(vis, hd, scale=1.0, ox=0, oy=0):
    """Overlay: fitted fill circle (green), measured inner and outer ink edge points (cyan, orange)."""
    cx, cy, r = hd['cx'], hd['cy'], hd['r_fill']
    c = (int(round((cx - ox) * scale)), int(round((cy - oy) * scale)))
    col = (60, 220, 60) if hd['outline_ok'] else (0, 200, 255)
    cv2.circle(vis, c, int(round(r * scale)), col, max(1, int(round(scale))), cv2.LINE_AA)
    rays = hd.get('_rays')
    if rays is not None:
        for k in range(N_RAYS):
            ri, w = rays['r_in'][k], rays['width'][k]
            if np.isfinite(w):
                for rad, cc in ((ri, (255, 255, 0)), (ri + w, (0, 120, 255))):
                    p = (int(round((cx + _RAY_COS[k] * rad - ox) * scale)), int(round((cy + _RAY_SIN[k] * rad - oy) * scale)))
                    cv2.circle(vis, p, max(1, int(round(scale * 0.8))), cc, -1, cv2.LINE_AA)
    return vis
