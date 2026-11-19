#!/usr/bin/env python3
"""Re-measurable colour/lighting statistics for the 'color_light_post' spec.

Usage:
  python3 measure_color.py IMAGE [IMAGE ...]            # table of global stats
  python3 measure_color.py --palette IMAGE [IMAGE ...]  # + k-means palette (k=8, Lab)
  python3 measure_color.py --json out.json IMAGE ...

All statistics are computed on the 720x1280 frame with the burned-in caption
band masked out (y 850..950, x 120..600). sRGB-encoded values are used as-is
(what a viewer sees); 'luma' is Rec.709 luma of the encoded values, 0..1.
"""
import sys, json, os
import numpy as np
import cv2

CAP = (850, 950, 120, 600)  # y0,y1,x0,x1 caption band to ignore

def load(path):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit('cannot read ' + path)
    if im.shape[:2] != (1280, 720):
        im = cv2.resize(im, (720, 1280), interpolation=cv2.INTER_AREA)
    return im

def mask_for(im):
    m = np.ones(im.shape[:2], bool)
    y0, y1, x0, x1 = CAP
    m[y0:y1, x0:x1] = False
    return m

def hexof(bgr):
    b, g, r = [int(round(float(v))) for v in bgr]
    return '#%02x%02x%02x' % (r, g, b)

def stats(im, m=None):
    if m is None:
        m = mask_for(im)
    f = im.astype(np.float32) / 255.0
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)  # H 0..360, S 0..1, V 0..1
    H, S, V = hsv[..., 0][m], hsv[..., 1][m], hsv[..., 2][m]
    B, G, R = f[..., 0][m], f[..., 1][m], f[..., 2][m]
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    # Hasler-Suesstrunk colourfulness (0..~110+ on 8-bit scale)
    rg = (R - G) * 255; yb = (0.5 * (R + G) - B) * 255
    cf = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2Lab)
    C = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2)[m]
    p = lambda a, q: float(np.percentile(a, q))
    sat_w = S > 0.15
    warm = ((H < 70) | (H >= 330)) & sat_w          # red/orange/yellow
    cool = ((H >= 170) & (H < 290)) & sat_w         # cyan/blue/violet
    green = ((H >= 70) & (H < 170)) & sat_w
    mag = ((H >= 290) & (H < 330)) & sat_w
    out = dict(
        S_mean=float(S.mean()), S_p10=p(S, 10), S_p50=p(S, 50), S_p90=p(S, 90),
        V_mean=float(V.mean()), V_p5=p(V, 5), V_p50=p(V, 50), V_p95=p(V, 95),
        Y_mean=float(Y.mean()), Y_p5=p(Y, 5), Y_p50=p(Y, 50), Y_p95=p(Y, 95),
        Y_contrast=p(Y, 95) - p(Y, 5),
        chroma_mean=float(C.mean()), chroma_p90=p(C, 90),
        colourfulness=cf,
        frac_S_gt_50=float((S > 0.5).mean()), frac_S_lt_15=float((S < 0.15).mean()),
        frac_V_gt_95=float((V > 0.95).mean()), frac_Y_lt_10=float((Y < 0.10).mean()),
        frac_clip_white=float(((R > 0.98) & (G > 0.98) & (B > 0.98)).mean()),
        warm=float(warm.mean()), cool=float(cool.mean()), green=float(green.mean()), magenta=float(mag.mean()),
        mean_rgb=hexof([B.mean() * 255, G.mean() * 255, R.mean() * 255]),
    )
    # tonal tints: black point and mean colour of the darkest 10 %, the 40-60 % band, the brightest 10 %
    import colorsys
    p10, p40, p60, p90 = np.percentile(Y, [10, 40, 60, 90])
    out['Y_p1'] = p(Y, 1)
    for key, sel in (('dark10', Y <= p10), ('mid', (Y > p40) & (Y < p60)), ('bright10', Y >= p90)):
        c = (float(R[sel].mean()), float(G[sel].mean()), float(B[sel].mean()))
        h, s_, v = colorsys.rgb_to_hsv(*c)
        out[key + '_hex'] = hexof([c[2] * 255, c[1] * 255, c[0] * 255])
        out[key + '_hue'] = h * 360.0; out[key + '_sat'] = s_
    return out

def palette(im, k=8, m=None, seed=7):
    if m is None:
        m = mask_for(im)
    small = cv2.resize(im, (180, 320), interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m.astype(np.uint8), (180, 320), interpolation=cv2.INTER_NEAREST).astype(bool)
    lab = cv2.cvtColor(small.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)
    X = lab[ms].reshape(-1, 3).astype(np.float32)
    cv2.setRNGSeed(seed)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.2)
    _, labels, centers = cv2.kmeans(X, k, None, crit, 5, cv2.KMEANS_PP_CENTERS)
    labels = labels.ravel()
    res = []
    for i in range(k):
        share = float((labels == i).mean())
        c = centers[i].reshape(1, 1, 3).astype(np.float32)
        bgr = cv2.cvtColor(c, cv2.COLOR_Lab2BGR)[0, 0]
        bgr = np.clip(bgr, 0, 1) * 255
        res.append((share, hexof(bgr)))
    res.sort(reverse=True)
    return res

if __name__ == '__main__':
    args = sys.argv[1:]
    want_pal = False; jpath = None
    if args and args[0] == '--palette':
        want_pal = True; args = args[1:]
    if args and args[0] == '--json':
        jpath = args[1]; args = args[2:]
    allr = {}
    cols = ['S_mean', 'S_p50', 'S_p90', 'V_mean', 'V_p5', 'V_p95', 'Y_p5', 'Y_p50', 'Y_p95', 'Y_contrast', 'chroma_mean', 'colourfulness', 'frac_S_gt_50', 'frac_S_lt_15']
    print('%-28s ' % 'frame' + ' '.join('%8s' % c[:8] for c in cols))
    for a in args:
        im = load(a)
        s = stats(im)
        name = '/'.join(a.split('/')[-2:])
        print('%-28s ' % name + ' '.join('%8.3f' % s[c] for c in cols))
        print('    tones: black point luma p1 %.3f | darkest 10%% %s (H%.0f S%.2f) | mid 40-60%% %s (H%.0f) | brightest 10%% %s | near-white share (V>0.95) %.3f' % (
            s['Y_p1'], s['dark10_hex'], s['dark10_hue'], s['dark10_sat'], s['mid_hex'], s['mid_hue'], s['bright10_hex'], s['frac_V_gt_95']))
        if want_pal:
            pal = palette(im)
            s['palette'] = pal
            print('    palette: ' + '  '.join('%s %.0f%%' % (h, sh * 100) for sh, h in pal))
        allr[name] = s
    if jpath:
        json.dump(allr, open(jpath, 'w'), indent=1)
