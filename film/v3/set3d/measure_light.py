#!/usr/bin/env python3
"""measure_light.py [cam] [staging] : lit-to-shadow ratio and shadow edge width of the set, measured on our own render.

Method: the same frame is rendered twice, key light on and key light off (pure ambient). For every pixel the key reaches,
  ratio = luma(off) / luma(on)        = how dark that very surface is when it falls into shadow (display luma, Rec.601)
and the key visibility v = (on - off) / (lit - off) gives the penumbra: edge width (10-90 percent) = 0.8 / |grad v| on the v = 0.5 line.
Writes v3/tmp/set3d/measure_<cam>_{on,off}.png and prints a table."""
import sys, os, json
import numpy as np, cv2, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import office3d as S

def luma(a): return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
def lin(a): a = a / 255.0; return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)

def run(cam='eye_two_shot', staging='two_shot', quality='final', threads=2, verbose=True):
    A = S.build(); sc = bpy.context.scene; S.setup_render(sc, quality); sc.render.threads = threads; S.set_track(1.0, 0.0)
    cs = A['cams'][cam]; S.make_camera(cs)
    if staging != 'none': S.stage_placeholders(A, staging, cs['loc'])
    sc.cycles.samples = 32
    on_p = os.path.join(S.TMP, 'measure_%s_on.png' % cam); off_p = os.path.join(S.TMP, 'measure_%s_off.png' % cam)
    S.render(on_p); sun = S.STATE['sun']; sun.hide_render = True; S.render(off_p); sun.hide_render = False
    on = cv2.cvtColor(cv2.imread(on_p), cv2.COLOR_BGR2RGB).astype(np.float64); off = cv2.cvtColor(cv2.imread(off_p), cv2.COLOR_BGR2RGB).astype(np.float64)
    Lon, Loff = luma(on), luma(off); d = Lon - Loff
    # fully lit pixels: the local maximum of (on - off) relative to the ambient value, per pixel -> visibility needs the lit value of THAT surface;
    # use the linear ratio: lit_lin = off_lin * (1 + g) with g constant per material, so estimate g from the 95th percentile in a 31 px neighbourhood
    lon, loff = lin(on).sum(2), lin(off).sum(2) + 1e-4; r = lon / loff - 1.0
    rmax = cv2.dilate(r.astype(np.float32), np.ones((41, 41), np.uint8)); v = np.clip(r / np.maximum(rmax, 1e-3), 0, 1)
    litmask = (r > 0.25) & (v > 0.92)
    ratio = Loff[litmask] / np.maximum(Lon[litmask], 1.0)
    ratio_lin = (loff[litmask]) / (lon[litmask])
    res = dict(cam=cam, lit_fraction=float(litmask.mean()), ratio_luma=dict(p10=float(np.percentile(ratio, 10)), median=float(np.median(ratio)), p90=float(np.percentile(ratio, 90))),
               ratio_linear_median=float(np.median(ratio_lin)))
    # hue of shade vs lit on those pixels
    def mean_hsv(img, m):
        c = img[m].mean(0) / 255.0; h = cv2.cvtColor(np.uint8([[c * 255]]), cv2.COLOR_RGB2HSV)[0, 0]; return ('#%02x%02x%02x' % tuple(int(x * 255) for x in c), int(h[0]) * 2, round(h[1] / 255.0, 2))
    res['lit_mean'] = mean_hsv(on, litmask); res['same_pixels_in_shade'] = mean_hsv(off, litmask)
    # edge width where the surface around the edge is lit on one side (rmax well above 0)
    vs = cv2.GaussianBlur(v.astype(np.float32), (0, 0), 0.6); gx = cv2.Sobel(vs, cv2.CV_32F, 1, 0, ksize=3) / 8.0; gy = cv2.Sobel(vs, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    g = np.hypot(gx, gy); edge = (np.abs(vs - 0.5) < 0.12) & (rmax > 0.5) & (g > 0.02)
    wpx = 0.8 / g[edge]
    if wpx.size: res['edge_width_px'] = dict(n=int(wpx.size), p10=float(np.percentile(wpx, 10)), median=float(np.median(wpx)), p90=float(np.percentile(wpx, 90)))
    res['frame'] = dict(luma_p5=float(np.percentile(Lon, 5) / 255), luma_p50=float(np.percentile(Lon, 50) / 255), luma_p95=float(np.percentile(Lon, 95) / 255))
    hsv = cv2.cvtColor(on.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float64); res['frame']['sat_mean'] = float((hsv[..., 1] / 255).mean())
    ed = cv2.Canny(cv2.cvtColor(on.astype(np.uint8), cv2.COLOR_RGB2GRAY), 60, 140); res['frame']['edge_density'] = float((ed > 0).mean())
    dark = Lon <= np.percentile(Lon, 10); res['frame']['darkest_tenth'] = mean_hsv(on, dark)
    cv2.imwrite(os.path.join(S.TMP, 'measure_%s_vis.png' % cam), (v * 255).astype(np.uint8))
    if verbose: print(json.dumps(res, indent=1))
    return res

if __name__ == '__main__':
    a = sys.argv[1:]; run(a[0] if a else 'eye_two_shot', a[1] if len(a) > 1 else 'two_shot', a[2] if len(a) > 2 else 'final')
