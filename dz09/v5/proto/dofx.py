"""dofx.py -- stronger depth-of-field for the v5 proto (replaces the set post's dof(), which caps sigma at 10 px).

Layered, mask-normalised gather:
  * signed CoC sigma c = K * (1 - z_f / z) (px at 1280 long side), far > 0, near < 0, |c| <= cap (up to 30+ px);
  * pixels are split over blur levels with triangular weights; far and near slices are blurred with their own weight
    masks (premultiplied) so a sharp subject never bleeds into the blurred background (no halo) and the background
    hidden behind the subject is filled from a wide normalised blur of the far field;
  * the in-focus layer is laid back per pixel (subject edges stay clean); near slices are composited OVER everything,
    so out-of-focus foreground (debris, cone, car edge) spreads soft over the subject like a real lens;
  * highlights above 1.0 in slices of sigma >= 5 px use a disc kernel (round bokeh).
Wide blurs run on downsampled copies (cost ~1-2 s per 720x1280 frame).
"""
import numpy as np
import cv2

CFG = dict(cap=10.0, actor_sharp=False, levels=(0, 1.0, 2.0, 3.5, 5.5, 8.0, 11.0, 15.0, 20.0, 26.0, 33.0),
           near_gain=1.0, bokeh=0.9)


def _blur(a, sigma, disc=False):
    if sigma <= 0.05: return a
    H, W = a.shape[:2]
    f = 1.0
    if sigma > 4.0:
        f = sigma / 4.0
        sm = cv2.resize(a, (max(1, int(round(W / f))), max(1, int(round(H / f)))), interpolation=cv2.INTER_AREA)
        sg = 4.0
    else:
        sm, sg = a, sigma
    if disc:
        r = max(1, int(round(sg * 2.0)))
        k = np.zeros((2 * r + 1, 2 * r + 1), np.float32); cv2.circle(k, (r, r), r, 1.0, -1, cv2.LINE_AA); k /= k.sum()
        out = cv2.filter2D(sm, -1, k, borderType=cv2.BORDER_REFLECT)
    else:
        ks = int(sg * 3) * 2 + 1
        out = cv2.GaussianBlur(sm, (ks, ks), sg, borderType=cv2.BORDER_REFLECT)
    if f != 1.0:
        out = cv2.resize(out, (W, H), interpolation=cv2.INTER_LINEAR)
    return out


def tri_weights(a, lv):
    ws = []
    n = len(lv)
    for i in range(n):
        if i == 0:
            w = np.clip(1 - a / lv[1], 0, 1)
        elif i == n - 1:
            w = np.clip((a - lv[i - 1]) / (lv[i] - lv[i - 1]), 0, 1)
        else:
            up = np.clip((a - lv[i - 1]) / (lv[i] - lv[i - 1]), 0, 1) * (a <= lv[i])
            dn = np.clip((lv[i + 1] - a) / (lv[i + 1] - lv[i]), 0, 1) * (a > lv[i])
            w = up + dn
        ws.append(w.astype(np.float32))
    return ws


def dof(rgb, z, idx, s, focus_z, K, cfg=None):
    cfg = dict(CFG, **(cfg or {}))
    cap = cfg["cap"] * s
    zf = max(focus_z, 0.02)
    c = K * s * (1 - zf / np.maximum(z, 1e-3))
    c = np.clip(c, -cap, cap).astype(np.float32)
    if cfg["actor_sharp"]:
        c = np.where(np.abs(idx - 2) < 0.5, 0.0, c)
    a = np.abs(c)
    lv = [l * s for l in cfg["levels"] if l * s <= cap + 1e-6]
    if lv[-1] < cap - 0.5: lv.append(cap)
    if len(lv) < 2: return rgb, c
    ws = tri_weights(np.minimum(a, lv[-1]), lv)
    far = (c > 0).astype(np.float32); near = 1.0 - far
    hi = np.maximum(rgb - 1.0, 0) * cfg["bokeh"]
    lo = rgb - hi
    # far field
    fC = np.zeros_like(rgb); fA = np.zeros(a.shape, np.float32)
    nC = np.zeros_like(rgb); nA = np.zeros(a.shape, np.float32)
    for i in range(1, len(lv)):
        for side, C, Aacc in ((far, fC, fA), (near, nC, nA)):
            w = ws[i] * side
            if w.max() <= 1e-4: continue
            sg = lv[i]
            prem = rgb * w[..., None]
            if sg >= 5 * s and hi.max() > 0:
                b = _blur(lo * w[..., None], sg) + _blur(hi * w[..., None], sg, disc=True)
            else:
                b = _blur(prem, sg)
            C += b
            Aacc += _blur(w, sg)
    # fill: what the far field looks like behind in-focus / near objects
    fm = far * (1 - ws[0])
    big = lv[-1]
    fill_den = _blur(fm, big)
    fill = _blur(rgb * fm[..., None], big) / np.maximum(fill_den, 1e-4)[..., None]
    fallback = _blur(rgb, big)
    fill = np.where((fill_den > 1e-3)[..., None], fill, fallback)
    D = np.clip(1 - fA, 0, 1)
    far_img = (fC + fill * D[..., None]) / np.maximum(fA + D, 1e-4)[..., None]
    w0 = ws[0]
    out = rgb * w0[..., None] + far_img * (1 - w0)[..., None]
    # near field over everything
    nA2 = np.clip(nA * cfg["near_gain"], 0, None)
    scale = np.where(nA2 > 1, 1.0 / np.maximum(nA2, 1e-4), 1.0)
    nCn = nC * (scale * cfg["near_gain"])[..., None]
    nAn = np.clip(nA2 * scale, 0, 1)
    # near pixels themselves: their own far/focus contribution must be replaced by the near layer
    out = nCn + out * (1 - nAn)[..., None]
    return out.astype(np.float32), c
