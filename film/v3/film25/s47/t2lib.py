#!/usr/bin/env python3
"""t2lib.py -- render-team T2 helpers for the FRONT takes of film 25 (tank-only crossing shots and friends).

  * umap(g)            the ONE continuous set_crossing u over g 1396..1558 (word locks of WORKER25.md)
  * Take               c25.Take for a front preset registered at runtime (never edits the set), hooks keyed every frame in on_frame
  * post_tank          film grade for frames without a puppet: the set's sharpen + clarity, then post25's gentle background grade
                       (soft shoulder, warm-key white balance, gamma 0.95, vibrance, darker near edge); exposure / white balance are
                       solved per frame, then SMOOTHED over the take so the grade never flickers
  * run(...)           resumable draft / final loop with per-frame json logs
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageFilter
import c25 as C
F, bpy = C.F, C.bpy
from mathutils import Vector

# ----------------------------------------------------------------------------- the crossing clock
# (g, u) anchors: u 0 at g 1396; nose lift from g 1424; grip at g 1493; rear leaves the near lip at ~g 1526; u 1 at g 1558
U_ANCH = [(1396, 0.0), (1424, 0.26), (1493, 0.40), (1526, 0.60), (1558, 1.0)]


def mono_hermite(xs, ys):
    """Fritsch-Carlson monotone cubic Hermite interpolant (C1, no overshoot) as a callable"""
    xs = np.array(xs, float); ys = np.array(ys, float); h = np.diff(xs); d = np.diff(ys) / h
    m = np.zeros(len(xs)); m[1:-1] = (d[:-1] + d[1:]) / 2
    m[0] = d[0]; m[-1] = d[-1]
    for i in range(len(d)):
        if d[i] == 0:
            m[i] = m[i + 1] = 0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]; s = a * a + b * b
            if s > 9:
                t = 3 / math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]

    def f(x):
        x = min(max(x, xs[0]), xs[-1]); i = int(min(len(h) - 1, max(0, np.searchsorted(xs, x) - 1))); t = (x - xs[i]) / h[i]
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1; h10 = t ** 3 - 2 * t ** 2 + t; h01 = -2 * t ** 3 + 3 * t ** 2; h11 = t ** 3 - t ** 2
        return float(h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1])
    return f


_U = mono_hermite([a for a, _ in U_ANCH], [b for _, b in U_ANCH])


def umap(g):
    return _U(g)


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * u * (u * (6.0 * u - 15.0) + 10.0)


def lerp(a, b, t):
    return a + (b - a) * t


def vlerp(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


# ----------------------------------------------------------------------------- take
SUN_DISC = 0.5          # deg: crisp cast shadows (Look A)


def register(name, base="cross_hero", **over):
    d = dict(F.PRESETS[base]); d.update(over); F.PRESETS[name] = d
    return name


class Take(C.Take):
    """one front preset; on_frame(f) = per-frame state (tank, hooks, sun); cam_of(g) = (loc, look, lens, dof) supplied by the shot"""
    def __init__(self, preset, cam_of, hooks=None, sun_az_off=0.0, haze=0.0006):
        C.F.OVR.update(haze=haze)
        C.Take.__init__(self, preset)
        F.S["sun"].data.angle = math.radians(SUN_DISC)
        self.cam_of = cam_of
        self.hooks = hooks or (lambda g, T: None)
        self.sun_off = sun_az_off
        import tank25 as TK
        self.TK = TK
        self.H = F.S.get("tank")

    def pose(self, gs):
        for g in gs:
            loc, look, lens = self.cam_of(g)[:3]
            self.key_cam(g, loc, look, lens)

    def on_frame(self, f):
        self.hooks(f, self)
        loc, look, lens = self.cam_of(f)[:3]
        az, el = F.sun_for_camera(dict(loc=tuple(loc), look_at=tuple(look)), F.S.get("sun_elev", 28.0))
        F.set_sun(az + self.sun_off, el)
        dof = self.cam_of(f)[3] if len(self.cam_of(f)) > 3 else None
        d = self.cam.data.dof
        if dof:
            d.use_dof = True; d.aperture_fstop = dof[0]; d.focus_distance = dof[1]
        else:
            d.use_dof = False


# ----------------------------------------------------------------------------- post (puppet-free frames)
GAMMA, VIB = 0.95, 1.25
WB_T = (2.0, 4.5)
SAT_T = 0.445
W709 = np.array([0.2126, 0.7152, 0.0722], np.float32)
to_lin = lambda x: np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
to_srgb = lambda x: np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)


def lab_ab(rgb):
    lin = to_lin(rgb); M = np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]], np.float32)
    xyz = (lin @ M) / np.array([0.95047, 1.0, 1.08883], np.float32); f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return float((500 * (f[..., 0] - f[..., 1])).mean()), float((200 * (f[..., 1] - f[..., 2])).mean())


def rgb2hsv(a):
    mx = a.max(2); mn = a.min(2); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(d < 1e-6, 0, np.where(mx == r, ((g - b) / np.maximum(d, 1e-6)) % 6, np.where(mx == g, (b - r) / np.maximum(d, 1e-6) + 2, (r - g) / np.maximum(d, 1e-6) + 4)))
    return h, s, mx


def hsv2rgb(h, s, v):
    c = v * s; x = c * (1 - np.abs(h % 2 - 1)); m = v - c; hi = np.floor(h).astype(int) % 6; z = np.zeros_like(c)
    r = np.choose(hi, [c, x, z, z, x, c]); g = np.choose(hi, [x, c, c, x, z, z]); b = np.choose(hi, [z, z, x, c, c, x]); return np.stack([r + m, g + m, b + m], -1)


def vibrance(a, k=VIB):
    h, s, v = rgb2hsv(a)
    w = np.where(s < 0.5, np.maximum(4 * s * (1 - s), (1 - s) ** 1.5), 4 * s * (1 - s)); s2 = np.clip(s * (1 + (k - 1) * w), 0, 1)
    return hsv2rgb(h, s2, v)


def sharpen(raw_path):
    raw = Image.open(raw_path).convert("RGB")
    if raw.size != (720, 1280):
        raw = raw.resize((720, 1280), Image.LANCZOS)
    sh = raw.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)).filter(ImageFilter.UnsharpMask(radius=5, percent=40, threshold=1))
    return np.asarray(sh).astype(np.float32) / 255


def _tone(lin, e, gains, gam=GAMMA):
    y = lin * gains * e
    L = np.maximum(y @ W709, 1e-6)[..., None]; k = 0.70
    Ly = np.where(L > k, k + (0.97 - k) * np.tanh((L - k) / (0.97 - k)), L); y = y * (Ly / L)
    mx = y.max(-1, keepdims=True); y = y * np.minimum(1.0, 0.985 / np.maximum(mx, 1e-6))
    return np.power(np.clip(to_srgb(y), 1e-5, 1), gam)


def solve(a, luma_t=float(os.environ.get("LUMA_T", 0.50)), wb_t=WB_T, vib=VIB, exp_max=2.8):
    """exposure + white-balance gains for a sharpened linear-able frame a (0..1 sRGB)"""
    lin = to_lin(a); gains = np.ones(3, np.float32); e = 1.0; sm = (slice(None, None, 4), slice(None, None, 4)); ls = lin[sm]
    for it in range(7):
        lo, hi = 0.6, exp_max
        for _ in range(16):
            e = (lo + hi) / 2
            if (vibrance(_tone(ls, e, gains), vib) @ W709).mean() > luma_t + 0.005: hi = e
            else: lo = e
        bgv = vibrance(_tone(ls, e, gains), vib); am, bm = lab_ab(bgv[None])
        gains[2] *= np.exp(0.025 * (bm - wb_t[1])); gains[1] *= np.exp(0.02 * (am - wb_t[0]))
        gains /= float(gains @ W709); gains = np.clip(gains, 0.5, float(os.environ.get("WB_CLIP", 1.45)))
    return dict(e=float(e), gains=[float(x) for x in gains])


def apply(a, p, vib=VIB, edge=0.18):
    lin = to_lin(a); gains = np.array(p["gains"], np.float32)
    b = vibrance(_tone(lin, p["e"], gains), vib)
    h, sa, v = rgb2hsv(b)                                                # sky stays neutral clear blue: hues 215-330 deg (lavender / purple drift) are pulled back to 212-218 deg
    deg = h * 60.0
    drift = (deg > 215.0) & (deg < 330.0) & (sa > 0.05)
    deg = np.where(drift, 212.0 + 6.0 * np.clip((deg - 215.0) / 115.0, 0, 1) * 0.0 + np.minimum(deg - 215.0, 6.0) * 0.0 + 3.0, deg)
    b = hsv2rgb(deg / 60.0, sa, v)
    yy = np.linspace(0, 1, 1280, dtype=np.float32)[:, None, None]
    b = b * (1 - edge * np.clip((yy - 0.86) / 0.14, 0, 1) ** 1.5)
    return np.clip(b, 0, 1)


def smooth_params(P, sigma=4.0):
    """gaussian smoothing of per-frame exposure / gains over the frame sequence (list in frame order) -> no grade flicker"""
    if len(P) < 3:
        return P
    k = np.exp(-0.5 * (np.arange(-3 * int(sigma), 3 * int(sigma) + 1) / sigma) ** 2); k /= k.sum(); pad = 3 * int(sigma)
    def sm(v):
        v = np.array(v); out = np.zeros_like(v, dtype=float)
        for c in range(v.shape[1] if v.ndim > 1 else 1):
            x = v[:, c] if v.ndim > 1 else v
            xp = np.pad(x, (pad, pad), mode="edge"); y = np.convolve(xp, k, "valid")
            if v.ndim > 1: out[:, c] = y
            else: out = y
        return out
    e = sm([p["e"] for p in P]); gs = sm([p["gains"] for p in P])
    return [dict(e=float(e[i]), gains=[float(x) for x in gs[i]]) for i in range(len(P))]


def post_take(frames, raw_dir, out_dir, cache=None):
    """frames = list of g in order; reads raw_dir/f_%04d.png, writes out_dir/g_%04d.png (grade params smoothed over the take)"""
    os.makedirs(out_dir, exist_ok=True)
    P = []; A = {}
    for g in frames:
        a = sharpen(os.path.join(raw_dir, "f_%04d.png" % g)); P.append(solve(a)); A[g] = a if len(frames) < 12 else None
    P = smooth_params(P)
    def msat(img):
        sm_ = img[::4, ::4]; mx_, mn_ = sm_.max(2), sm_.min(2); return float(np.where(mx_ > 0, (mx_ - mn_) / np.maximum(mx_, 1e-6), 0).mean())
    idx = list(range(0, len(frames), max(1, len(frames) // 6)))
    smp = [(sharpen(os.path.join(raw_dir, "f_%04d.png" % frames[i])), P[i]) for i in idx]
    lo, hi = VIB, 5.0
    if np.mean([msat(apply(a, p, VIB)) for a, p in smp]) < SAT_T:          # raise the vibrance just enough: take mean sat SAT_T (gate 0.40-0.50)
        for _ in range(9):
            mid = (lo + hi) / 2
            if np.mean([msat(apply(a, p, mid)) for a, p in smp]) < SAT_T: lo = mid
            else: hi = mid
        vib = hi
    else:
        vib = VIB
    ab = np.mean([lab_ab(apply(a, p, vib)[::4, ::4][None]) for a, p in smp], 0)
    print("post_take vibrance %.2f  a* %.1f b* %.1f" % (vib, ab[0], ab[1]), flush=True)
    if abs(ab[1]) > 4.8 or abs(ab[0]) > 4.8:                              # vibrance pushes the cast: re-solve the white balance so the finished take sits at a* +2.5, b* +3.5
        tgt = (WB_T[0] + (2.5 - ab[0]), WB_T[1] + (3.5 - ab[1]))
        P = smooth_params([solve(a_, wb_t=tgt) for a_ in [sharpen(os.path.join(raw_dir, "f_%04d.png" % g)) for g in frames]])
        print("post_take re-solved WB target", tgt, flush=True)
    for g, p in zip(frames, P):
        a = A[g] if A[g] is not None else sharpen(os.path.join(raw_dir, "f_%04d.png" % g))
        Image.fromarray((apply(a, p, vib) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out_dir, "g_%04d.png" % g))
    return P


# ----------------------------------------------------------------------------- loops
SCALE, SAMPLES, THRESH = 0.75, 20, 0.02


def run(Tk, mode, gs, root, report=None, scale=None, samples=None):
    """mode draft -> root/work/draft/f_%04d.png (+ post); final -> root/frames/raw/f_%04d.png + json, resumable"""
    Tk.pose(gs)
    if mode == "draft":
        out = os.path.join(root, "work", "draft"); sc, sm, th = (scale or 0.4), (samples or 8), 0.05
    else:
        out = os.path.join(root, "frames"); sc, sm, th = (scale or SCALE), (samples or SAMPLES), THRESH
    os.makedirs(out, exist_ok=True)
    for g in gs:
        js = os.path.join(out, "g_%04d.json" % g)
        if mode == "final" and os.path.exists(js) and os.path.exists(os.path.join(out, "raw", "f_%04d.png" % g)):
            continue
        st = Tk.render([g], out, scale=sc, samples=sm, threshold=th, keep_raw=True, post=False)[0]
        rep = dict(g=g, wall=round(st["wall"], 1), cpu=round(st["cpu"], 1), samples=sm, scale=sc, threshold=th)
        if report:
            rep.update(report(Tk, g))
        json.dump(rep, open(js + ".tmp", "w"), default=float); os.replace(js + ".tmp", js)
        print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
    return out
