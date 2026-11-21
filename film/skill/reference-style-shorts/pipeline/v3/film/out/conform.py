#!/usr/bin/env python3
"""conform.py -- build-order step 12: join the hook and the 23 takes into the 1965 picture frames of the film.

    python3 conform.py [g0 g1]      writes out/frames/g_%04d.png (no captions) and out/work/joins.json

Sources: hook = PROJ/v3/out/frames/f_%04d.png (f_0001 = g 0, g 0..149); takes = PROJ/v3/film/sNN/frames/g_%04d.png.
Transitions (plan, shot_plan.md 'Transition in'):
  dissolve L : smoothstep cross-dissolve centred on the boundary gb, frames gb - L//2 .. gb - L//2 + L - 1,
               weight of the incoming take = smoothstep((g - a + 1) / (L + 1)), mixed from the handle frames of both
               takes (a missing handle frame is extended in 2D from the last two frames' fitted camera motion).
  cut / hidden_cut_in_whip / hard_cut / punch_in : straight cut (speed lines of the punch-in are inside s13).
  wipe 6     : the wave's foam sheet (2D layer) crosses the lens left to right over g 1785-1790; s24 ahead of its
               leading edge, s25 behind its trailing edge.
  flash      : 5 frames to white at the end of s25 (g 1868-1872), 4 frames out (g 1873-1876).
Overlays added here (simple 2D layers): speed lines in s20 (launch) and s24 (crash pull-out), focus lines on the
shocked faces at the hard cut into s24.
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
PROJ = os.path.normpath(os.path.join(FILM, "..", ".."))
HOOK = os.path.join(PROJ, "v3", "out", "frames")
OUT = os.path.join(HERE, "frames")
W, H, N = 720, 1280, 1965
TAKES = ["s%02d" % n for n in range(4, 27)]


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- takes and joins
def load_takes():
    tk = [dict(take="hook", shots=[1, 2, 3], g0=0, g1=129, transition_in=None)]
    for t in TAKES:
        m = json.load(open(os.path.join(FILM, t, "meta.json")))
        tk.append(dict(take=t, shots=m["shots"], g0=m["g0"], g1=m["g1"], transition_in=m.get("transition_in"),
                       handle_in=m.get("handle_in", 0), handle_out=m.get("handle_out", 0)))
    for a, b in zip(tk, tk[1:]):
        assert a["g1"] == b["g0"], (a["take"], b["take"])
    assert tk[-1]["g1"] == N
    return tk


def joins(tk):
    out = []
    for a, b in zip(tk, tk[1:]):
        ti = b["transition_in"] or {}
        typ, L = ti.get("type", "cut"), int(ti.get("frames", 0) or 0)
        gb = b["g0"]
        if typ == "dissolve":
            lo = gb - L // 2
            rng = (lo, lo + L - 1)
            kind = "dissolve"
        elif typ in ("wipe", "object_wipe"):
            rng = (gb - 3, gb + 2); kind = "wipe"; L = 6
        elif typ == "flash":
            rng = (gb - 5, gb + 3); kind = "flash"; L = 9
        else:
            rng = (gb, gb); kind = {"hidden_cut_in_whip": "hidden cut in whip", "punch_in": "punch-in cut (speed lines in s13)",
                                    "hard_cut": "hard cut", "cut": "hard cut"}.get(typ, typ)
        out.append(dict(a=a["take"], b=b["take"], gb=gb, kind=kind, frames=L, range=list(rng), plan_type=typ))
    return out


def src_path(take, g):
    if take == "hook":
        return os.path.join(HOOK, "f_%04d.png" % (g + 1))
    return os.path.join(FILM, take, "frames", "g_%04d.png" % g)


_ext_log = []


def load(take, g):
    """frame g of a take as float32 RGB; a missing frame is a 2D continuation of the last camera motion."""
    p = src_path(take, g)
    if os.path.exists(p):
        return np.asarray(Image.open(p).convert("RGB"), np.float32)
    # 2D extension: nearest two existing frames, fitted similarity, extrapolated
    import cv2
    # nearest existing frame (n1) and its neighbour inside the take (n0)
    cands = [h for h in range(g - 40, g + 41) if os.path.exists(src_path(take, h))]
    n1 = min(cands, key=lambda h: abs(h - g))
    n0 = n1 - 1 if n1 > g else n1 + 1
    A = np.asarray(Image.open(src_path(take, n1)).convert("RGB"))
    if not os.path.exists(src_path(take, n0)):
        _ext_log.append((take, g, "hold", n1)); return A.astype(np.float32)
    B = np.asarray(Image.open(src_path(take, n0)).convert("RGB"))
    ga, gb_ = cv2.cvtColor(B, cv2.COLOR_RGB2GRAY), cv2.cvtColor(A, cv2.COLOR_RGB2GRAY)
    pts = cv2.goodFeaturesToTrack(ga, 400, 0.01, 12)
    M = np.eye(2, 3)
    if pts is not None:
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(ga, gb_, pts, None)
        ok = st.ravel() == 1
        if ok.sum() > 8:
            m, _ = cv2.estimateAffinePartial2D(pts[ok], nxt[ok])
            if m is not None:
                M = m
    steps = abs(g - n1)
    M3 = np.vstack([M, [0, 0, 1]])
    Mk = np.linalg.matrix_power(M3, steps)[:2]
    out = cv2.warpAffine(A, Mk, (W, H), borderMode=cv2.BORDER_REFLECT)
    _ext_log.append((take, g, "2D extension", n1))
    return out.astype(np.float32)


# ---------------------------------------------------------------- overlays
def speed_lines(img, cx, cy, strength, seed, n=46, r_in=260, retreat=0.0):
    """white radial wedges from outside the frame in toward radius r_in around (cx, cy)."""
    if strength <= 0.01:
        return img
    rs = np.random.RandomState(seed)
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    R = 1600
    r0 = r_in * (1 + retreat)
    for k in range(n):
        a = rs.uniform(0, 2 * math.pi)
        w = rs.uniform(0.004, 0.014)
        ri = r0 * rs.uniform(0.85, 1.45)
        p_tip = (cx + ri * math.cos(a), cy + ri * math.sin(a))
        p1 = (cx + R * math.cos(a - w), cy + R * math.sin(a - w))
        p2 = (cx + R * math.cos(a + w), cy + R * math.sin(a + w))
        d.polygon([p_tip, p1, p2], fill=int(255 * rs.uniform(0.55, 1.0)))
    lay = lay.filter(ImageFilter.GaussianBlur(0.8))
    al = np.asarray(lay, np.float32)[..., None] / 255.0 * strength
    return img * (1 - al) + 255.0 * al


def focus_lines(img, cx, cy, rx, ry, strength, seed, n=70):
    """dark-ink manga focus lines from the frame edge toward an ellipse around the faces."""
    if strength <= 0.01:
        return img
    rs = np.random.RandomState(seed)
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    for k in range(n):
        a = rs.uniform(0, 2 * math.pi)
        w = rs.uniform(0.003, 0.010)
        f = rs.uniform(1.0, 1.35)
        tip = (cx + rx * f * math.cos(a), cy + ry * f * math.sin(a))
        R = 1800
        d.polygon([tip, (cx + R * math.cos(a - w), cy + R * math.sin(a - w)), (cx + R * math.cos(a + w), cy + R * math.sin(a + w))],
                  fill=int(255 * rs.uniform(0.6, 1.0)))
    al = np.asarray(lay.filter(ImageFilter.GaussianBlur(0.6)), np.float32)[..., None] / 255.0 * strength
    ink = np.array([24, 18, 40], np.float32)
    return img * (1 - al) + ink * al


_foam_cache = {}


def foam_texture():
    if "t" in _foam_cache:
        return _foam_cache["t"]
    rs = np.random.RandomState(7)
    base = np.zeros((H, W), np.float32)
    for s, amp in ((160, 0.5), (60, 0.3), (20, 0.2)):
        small = rs.rand(H // s + 3, W // s + 3).astype(np.float32)
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((W + 2 * s, H + 2 * s), Image.BICUBIC)
        base += amp * np.asarray(im, np.float32)[s:s + H, s:s + W] / 255.0
    # bubbles
    bub = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(bub)
    for k in range(260):
        x, y, r = rs.uniform(0, W), rs.uniform(0, H), rs.uniform(3, 18)
        d.ellipse([x - r, y - r, x + r, y + r], outline=255, width=2)
    bub = np.asarray(bub.filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255.0
    _foam_cache["t"] = (base, bub)
    return base, bub


def foam_wipe(A, B, i):
    """frame i (0..5) of the 6-frame foam-sheet wipe: A = s24 (ahead of the sheet), B = s25 (behind it)."""
    base, bub = foam_texture()
    u = (i + 0.5) / 6.0
    lead = -0.2 + 1.75 * smooth(u / 0.62)          # leading edge, fraction of the width
    trail = -0.75 + 1.95 * smooth((u - 0.38) / 0.62)  # trailing edge
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    yn = yy / H
    # diagonal, scalloped edges (the sheet leans: top ahead of the bottom, like a breaking crest)
    sc_l = 0.035 * np.sin(yn * 23.0 + i * 0.9) + 0.02 * np.sin(yn * 61.0 + 1.3)
    sc_t = 0.03 * np.sin(yn * 19.0 - i * 0.7) + 0.02 * np.sin(yn * 47.0 + 0.4)
    xl = (lead + 0.22 * (0.5 - yn) + sc_l) * W
    xt = (trail + 0.22 * (0.5 - yn) + sc_t) * W
    soft = 10.0
    in_front = np.clip((xl - xx) / soft + 0.5, 0, 1)      # 1 where the sheet's leading edge has passed
    behind = np.clip((xt - xx) / soft + 0.5, 0, 1)         # 1 where the trailing edge has passed (s25 revealed)
    sheet = in_front * (1 - behind)
    # foam colour: pale lilac to white, translucent near the trailing edge, bright crest at the leading edge
    c1 = np.array([199, 175, 222], np.float32); c2 = np.array([238, 242, 254], np.float32)
    tmix = np.clip(base[..., None] * 1.1, 0, 1)
    foam = c1 * (1 - tmix) + c2 * tmix
    foam = foam * (1 - 0.25 * bub[..., None]) + 255 * 0.25 * bub[..., None]
    edge_glow = np.exp(-((xl - xx) / 18.0) ** 2)[..., None]
    foam = foam * (1 - 0.5 * edge_glow) + 255 * 0.5 * edge_glow
    dens = np.clip(0.80 + 0.35 * base - 0.45 * np.clip((xx - xt) / (0.35 * W), 0, 1) * 0, 0, 1)
    pic = A * (1 - behind[..., None]) + B * behind[..., None]
    a = (sheet * dens)[..., None]
    # thin trail of spray just behind the trailing edge
    spray = np.clip(1 - (xt - xx) / 60.0, 0, 1) * behind * (base > 0.55)
    a = np.maximum(a, (0.5 * spray)[..., None])
    return pic * (1 - a) + foam * a


# ---------------------------------------------------------------- per frame
FLASH_IN = {1868: 0.15, 1869: 0.35, 1870: 0.6, 1871: 0.85, 1872: 1.0}
FLASH_OUT = {1873: 0.85, 1874: 0.55, 1875: 0.3, 1876: 0.12}


def build(g, tk, js):
    own = next(t for t in tk if t["g0"] <= g < t["g1"])
    img = None
    note = None
    for j in js:
        a, b = j["range"]
        if not (a <= g <= b) or j["kind"] not in ("dissolve", "wipe"):
            continue
        A, B = load(j["a"], g), load(j["b"], g)
        if j["kind"] == "dissolve":
            w = smooth((g - a + 1) / (j["frames"] + 1.0))
            img = A * (1 - w) + B * w
            note = "dissolve %s>%s w=%.3f" % (j["a"], j["b"], w)
        else:
            img = foam_wipe(A, B, g - a)
            note = "foam wipe %s>%s i=%d" % (j["a"], j["b"], g - a)
    if img is None:
        img = load(own["take"], g)
    # overlays
    if 1442 <= g <= 1472:        # s20: launch after the flung spinner (snap 47.95-48.45 and the chase)
        k = (g - 1442) / 30.0
        st = 0.55 * smooth(min(1, (g - 1441) / 4.0)) * (1 - smooth((k - 0.55) / 0.45))
        img = speed_lines(img, 360, 470, st, 1000 + g, n=42, r_in=230, retreat=0.6 * k)
    if 1730 <= g <= 1748:        # s24: crash pull-out on 'กำแพงน้ำ'
        k = (g - 1730) / 18.0
        st = 0.45 * smooth(min(1, (g - 1729) / 3.0)) * (1 - smooth((k - 0.5) / 0.5))
        img = speed_lines(img, 330, 520, st, 2000 + g, n=40, r_in=300, retreat=0.5 * k)
    if 1720 <= g <= 1722:        # s24: 3 frames of focus lines on the shocked faces
        img = focus_lines(img, 300, 470, 300, 330, [0.85, 0.7, 0.45][g - 1720], 3000 + g)
    if g in FLASH_IN:
        w = FLASH_IN[g]; img = img * (1 - w) + 255.0 * w; note = (note or "") + " flash %.2f" % w
    if g in FLASH_OUT:
        w = FLASH_OUT[g]; img = img * (1 - w) + 255.0 * w; note = (note or "") + " flash %.2f" % w
    out = np.clip(img + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(OUT, "g_%04d.png" % g), compress_level=3)
    return g, own["take"], note


def worker(args):
    g0, g1 = args
    tk = load_takes(); js = joins(tk)
    res = [build(g, tk, js) for g in range(g0, g1)]
    return res, list(_ext_log)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    tk = load_takes(); js = joins(tk)
    json.dump(dict(takes=tk, joins=js), open(os.path.join(HERE, "work", "joins.json"), "w"), indent=1)
    g0, g1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, N)
    from multiprocessing import Pool
    chunks = [(a, min(g1, a + 40)) for a in range(g0, g1, 40)]
    log, ext = [], []
    with Pool(3) as P:
        for r, e in P.imap_unordered(worker, chunks):
            log += r; ext += e
    log.sort()
    json.dump(dict(frames=[dict(g=g, take=t, note=n) for g, t, n in log], extensions=ext),
              open(os.path.join(HERE, "work", "conform_log_%d_%d.json" % (g0, g1)), "w"), indent=0)
    print("wrote %d frames, %d 2D-extended source frames" % (len(log), len(ext)))
