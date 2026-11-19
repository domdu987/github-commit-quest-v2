#!/usr/bin/env python3
"""rmeasure.py : reviewer's own image measurements (no bpy). Used on reference frames and on our renders alike.
  pair(img, lit_rect, shade_rect)        -> same-surface shadow/lit luminance ratio, colours and hue of both sides
  edge(img, p0, p1, half=4)              -> 10-90 percent edge width in px along the line p0->p1 (put it perpendicular to the edge)
  halo(img, centre, r_max)               -> bloom: core radius (luma >= 0.97), radius where the excess over the surround falls to 10 percent
  tone(img)                              -> saturation mean, luma percentiles, darkest-tenth colour and hue, Canny density, featureless blocks
"""
import sys, colorsys, math
import numpy as np, cv2

def load(p):
    im = cv2.imread(p, cv2.IMREAD_COLOR); return cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
def luma(a): return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
def hexs(c): return '#%02x%02x%02x' % tuple(int(round(max(0, min(1, float(x))) * 255)) for x in c)
def hsv(c): h, s, v = colorsys.rgb_to_hsv(*[float(x) for x in c]); return h * 360.0, s, v
def lin(c): c = np.asarray(c, dtype=np.float64); return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def pair(a, lit, shade):
    """rects (x0, y0, x1, y1). Median colour of each; ratio of display luma and of linear luminance."""
    def med(r): x0, y0, x1, y1 = r; return np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0)
    L, S = med(lit), med(shade); yl, ys = luma(L), luma(S)
    Yl = float(np.dot(lin(L), (0.2126, 0.7152, 0.0722))); Ys = float(np.dot(lin(S), (0.2126, 0.7152, 0.0722)))
    return dict(lit=hexs(L), shade=hexs(S), ratio_display=float(ys / yl), ratio_linear=Ys / Yl, hue_lit=hsv(L)[0], hue_shade=hsv(S)[0], sat_lit=hsv(L)[1], sat_shade=hsv(S)[1], v_ratio=hsv(S)[2] / hsv(L)[2])

def profile(a, p0, p1, half=4, n=None):
    p0 = np.array(p0, float); p1 = np.array(p1, float); d = p1 - p0; L = np.linalg.norm(d); d /= L; nrm = np.array([-d[1], d[0]])
    n = n or int(L * 4) + 1; t = np.linspace(0, L, n); Y = luma(a); out = np.zeros(n)
    for k in range(-half, half + 1):
        pts = p0[None, :] + t[:, None] * d[None, :] + k * nrm[None, :]
        out += cv2.remap(Y, pts[:, 0].astype(np.float32).reshape(-1, 1), pts[:, 1].astype(np.float32).reshape(-1, 1), cv2.INTER_LINEAR).ravel()
    return t, out / (2 * half + 1)

def edge(a, p0, p1, half=4):
    """10-90 percent width (px) of the luminance step along p0 -> p1. Plateaus = median of the first and last fifth."""
    t, y = profile(a, p0, p1, half); n = len(y); k = max(3, n // 5)
    lo, hi = np.median(y[:k]), np.median(y[-k:])
    if abs(hi - lo) < 0.02: return None
    u = (y - lo) / (hi - lo)                       # 0 at the start plateau, 1 at the end plateau
    # last crossing of 0.1 before the first crossing of 0.9
    i9 = next((i for i in range(n) if u[i] >= 0.9), None)
    if i9 is None: return None
    i1 = next((i for i in range(i9, -1, -1) if u[i] <= 0.1), 0)
    def cross(i, lev):                               # linear interpolation between samples i and i+1
        if i + 1 >= n or u[i + 1] == u[i]: return t[i]
        return t[i] + (lev - u[i]) / (u[i + 1] - u[i]) * (t[i + 1] - t[i])
    return dict(width=float(cross(max(i9 - 1, 0), 0.9) - cross(i1, 0.1)), start=float(lo), end=float(hi), ratio=float(min(lo, hi) / max(lo, hi)))

def halo(a, c, r_max=90, core_level=0.97):
    """Radial luma profile around an emitter at c = (x, y). core = radius where the mean luma drops below core_level;
    r10 = radius where (luma - surround) drops below 10 percent of (core luma - surround); surround = median over the last sixth of radii.
    The profile uses the median over the angle, so occluders on one side do not matter much."""
    Y = luma(a); h, w = Y.shape; yy, xx = np.mgrid[0:h, 0:w]; r = np.hypot(xx - c[0], yy - c[1]); prof = []
    for k in range(int(r_max)):
        m = (r >= k) & (r < k + 1); prof.append(float(np.percentile(Y[m], 60)) if m.any() else 0.0)
    prof = np.array(prof); sur = float(np.median(prof[-max(4, r_max // 6):])); top = float(prof[:3].mean())
    core = next((k for k in range(len(prof)) if prof[k] < core_level), len(prof))
    r10 = next((k for k in range(core, len(prof)) if (prof[k] - sur) < 0.10 * (top - sur)), len(prof))
    r50 = next((k for k in range(core, len(prof)) if (prof[k] - sur) < 0.50 * (top - sur)), len(prof))
    return dict(core=core, r50=r50, r10=r10, halo=r10 - core, surround=sur, top=top, profile=prof)

def tone(a, mask_caption=False):
    """Frame statistics on display values. mask_caption removes the burned-in caption band (y 850..960) of reference frames."""
    b = a
    if mask_caption: b = np.concatenate([a[:850], a[960:]], axis=0)
    px = b.reshape(-1, 3); Y = luma(px); mx = px.max(1); mn = px.min(1); S = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    order = np.argsort(Y); d10 = px[order[:len(order) // 10]].mean(0); h, s, v = hsv(d10)
    g = (luma(b) * 255).astype(np.uint8); ed = cv2.Canny(g, 60, 140); dens = float((ed > 0).mean())
    # featureless 40 px blocks: luma std after a sigma-12 high-pass below 0.012 and no Canny edge pixel share above 0.5 percent
    hp = luma(b) - cv2.GaussianBlur(luma(b), (0, 0), 12); H, W = hp.shape; fl = 0; nb = 0
    for y0 in range(0, H - 39, 40):
        for x0 in range(0, W - 39, 40):
            nb += 1
            if hp[y0:y0 + 40, x0:x0 + 40].std() < 0.012 and (ed[y0:y0 + 40, x0:x0 + 40] > 0).mean() < 0.005: fl += 1
    return dict(sat_mean=float(S.mean()), sat_p90=float(np.percentile(S, 90)), luma_p1=float(np.percentile(Y, 1)), luma_p5=float(np.percentile(Y, 5)), luma_p50=float(np.percentile(Y, 50)), luma_p95=float(np.percentile(Y, 95)),
                v_gt_095=float((mx > 0.95).mean()), dark10=hexs(d10), dark10_hue=h, dark10_sat=s, canny=dens, featureless=fl / nb)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        t = tone(load(p)); print(p.split('/')[-2] + '/' + p.split('/')[-1], ' '.join('%s=%s' % (k, ('%.3f' % v) if isinstance(v, float) else v) for k, v in t.items()))
