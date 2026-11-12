#!/usr/bin/env python3
"""measure.py -- re-measure our own Chromium render against the spec ranges (QA only; uses numpy + Pillow).
Usage: python3 measure.py     (writes tmp/measure_*.png, prints a table)"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import puppet

D = 400.0
BG = (0, 255, 0)
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)


def render(name, cast, pose, w=3.2, h=4.2, cx=1.6, cy=0.9):
    f = puppet.figure(cast, pose, "m")
    W, H = int(w * D), int(h * D)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><rect width="%d" height="%d" fill="#00ff00"/>'
           '<g transform="translate(%.1f %.1f) scale(%.1f)">%s</g></svg>' % (W, H, W, H, cx * D, cy * D, D, f["svg"]))
    p = os.path.join(TMP, "measure_%s.svg" % name)
    open(p, "w").write(svg)
    out = os.path.join(TMP, "measure_%s.png" % name)
    subprocess.run(["node", os.path.join(HERE, "raster.js"), p, out, str(W), str(H)], check=True, stdout=subprocess.DEVNULL)
    im = np.asarray(Image.open(out).convert("RGB")).astype(int)
    return im, f, (cx * D, cy * D)


def is_bg(im):
    return (im[..., 1] > 200) & (im[..., 0] < 90) & (im[..., 2] < 90)


def is_ink(im):
    d = np.abs(im - np.array(puppet._rgb(puppet.INK))).sum(-1)
    return d < 70


def is_white(im):
    return (im[..., 0] > 215) & (im[..., 1] > 200) & (im[..., 2] > 200)


def run(mask_row):
    idx = np.where(mask_row)[0]
    return (idx.min(), idx.max()) if len(idx) else (None, None)


rows = []


def rec(name, val, lo, hi, unit="D"):
    ok = (lo <= val <= hi)
    rows.append((name, val, lo, hi, ok))
    print("%-52s %8.4f   spec %.3f .. %.3f %s  %s" % (name, val, lo, hi, unit, "ok" if ok else "OUT"))


for cast in ("hero", "boss"):
    C = puppet.CAST[cast]
    bald = dict(C, hat=None, ear_pencil=False, hair=dict(C["hair"], front=0.0, grow=0.0), moustache=False)
    puppet.CAST["_bald"] = bald
    # ---------------- head disc: outline width per 30 degree bin, D, wobble
    im, f, (ox, oy) = render(cast + "_bald", "_bald", dict(expr="neutral", arm_r="behind", arm_l="behind"), 2.0, 1.6, 1.0, 0.75)
    ink, white, bg = is_ink(im), is_white(im), is_bg(im)
    fx, fy = ox + puppet.FC[0] * D, oy + puppet.FC[1] * D
    bins = {}
    rin = []
    for deg in range(-120, 211, 2):               # skip the top, hidden by a hat in the reference, and the neck is included at 90
        a = math.radians(deg)
        c, s_ = math.cos(a), math.sin(a)
        r = 0.30 * D
        while r < 0.7 * D and not ink[int(round(fy + s_ * r)), int(round(fx + c * r))]:
            r += 0.25
        r0 = r
        while r < 0.7 * D and ink[int(round(fy + s_ * r)), int(round(fx + c * r))]:
            r += 0.25
        rin.append((deg, r0 / D))
        if 60 < deg < 120:                        # the torso touches the chin: ink run continues into the torso contour
            continue
        bins.setdefault((deg % 360) // 30 * 30, []).append((r - r0) / D)
    rowm = im[int(round(oy))]
    xs = np.where(~is_bg(rowm[None])[0])[0]
    rec(cast + " head outer D (ink to ink, centre row)", (xs.max() - xs.min() + 1) / D, 0.97, 1.03)
    spec = {0: (0.044, 0.067), 30: (0.054, 0.078), 120: (0.020, 0.044), 150: (0.020, 0.044), 180: (0.015, 0.028)}
    for b in sorted(bins):
        v = float(np.median(bins[b]))
        if b in spec:
            rec(cast + " head outline width, bin %3d deg" % b, v, spec[b][0], spec[b][1])
        else:
            print("%-52s %8.4f   (top of the head: hidden by hats in the reference)" % (cast + " head outline width, bin %3d deg" % b, v))
    rr = np.array([r for d_, r in rin if -30 <= d_ <= 60 or 120 <= d_ <= 210])
    rec(cast + " fill radius / D (median)", float(np.median(rr)), 0.45, 0.49)
    rec(cast + " inner-edge wobble rms (lower arc, % D)", float(np.std(rr)) * 100, 0.2, 1.5, "%")
    # head fill colours
    px = im[int(round(fy - 0.02 * D)), int(round(fx - 0.25 * D))]
    print("   head fill lit side: #%02x%02x%02x (spec #fef7f6)" % tuple(px))
    a = math.radians(50)
    px = im[int(round(fy + math.sin(a) * 0.435 * D)), int(round(fx + math.cos(a) * 0.435 * D))]
    print("   head shadow crescent at 50 deg, r = 0.94 R: #%02x%02x%02x (spec #e9dceb)" % tuple(px))
    # crescent inner edge: radius where the fill has moved half way to the shade colour
    for deg, lo, hi in ((0, 0.80, 0.90), (45, 0.75, 0.86), (90, 0.76, 0.88), (135, 0.85, 0.95)):
        a = math.radians(deg)
        base = np.array([254, 247, 246]); sh = np.array([233, 220, 235])
        r = 0.2 * D
        while r < 0.47 * D:
            p = im[int(round(fy + math.sin(a) * r)), int(round(fx + math.cos(a) * r))]
            if p.sum() > 500 and np.abs(p - base).sum() > 0.5 * np.abs(sh - base).sum():      # skip ink (eyes, mouth)
                break
            r += 0.5
        rec(cast + " crescent half-way edge r/R_fill at %3d deg" % deg, r / D / 0.463, lo, hi, "R")
    # ---------------- eyes (half-lid), brows, mouth
    eyes = []
    lab = ink.copy()
    # connected components of ink inside the face disc
    from collections import deque
    Hh, Ww = lab.shape
    seen = np.zeros_like(lab, bool)
    yy0, yy1, xx0, xx1 = int(fy - 0.30 * D), int(fy + 0.36 * D), int(fx - 0.33 * D), int(fx + 0.33 * D)
    comps = []
    for y in range(yy0, yy1):
        for x in range(xx0, xx1):
            if lab[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True
                pts = []
                while q:
                    cy_, cx_ = q.popleft(); pts.append((cy_, cx_))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy_ + dy, cx_ + dx
                        if yy0 <= ny < yy1 and xx0 <= nx < xx1 and lab[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
                pts = np.array(pts)
                if len(pts) > 40:
                    comps.append(((pts[:, 1].min() + pts[:, 1].max()) / 2, (pts[:, 0].min() + pts[:, 0].max()) / 2,
                                  pts[:, 1].max() - pts[:, 1].min() + 1, pts[:, 0].max() - pts[:, 0].min() + 1))
    comps.sort(key=lambda c_: (c_[1], c_[0]))
    # eyes = the two components whose centre is closest to the expected eye line
    ey = fy + C["eye_y"] * D
    ee = sorted(comps, key=lambda c_: abs(c_[1] - ey))[:2]
    ee.sort()
    rec(cast + " eye spacing (bbox centres)", (ee[1][0] - ee[0][0]) / D, 0.252, 0.269)
    rec(cast + " half-lid eye width", ee[0][2] / D, 0.168, 0.181)
    rec(cast + " half-lid eye height", ee[0][3] / D, 0.092, 0.104)
    rec(cast + " eye line v (fill-centre frame)", ((ee[0][1] + ee[1][1]) / 2 - fy) / D, -0.07, 0.06)
    mm = [c_ for c_ in comps if c_[1] > ey + 0.10 * D]
    if mm:
        m0 = min(mm, key=lambda c_: abs(c_[0] - fx))
        rec(cast + " eye line to mouth centre", (m0[1] - (ee[0][1] + ee[1][1]) / 2) / D, 0.167, 0.205)
        if cast == "hero":
            rec(cast + " dash mouth width", m0[2] / D, 0.097, 0.105)
            rec(cast + " dash mouth height", m0[3] / D, 0.030, 0.037)
        else:
            rec(cast + " arch frown width", m0[2] / D, 0.115, 0.130)
    bb = [c_ for c_ in comps if c_[1] < ey - 0.07 * D]
    if bb:
        rec(cast + " brow above eye centre", ((ee[0][1] + ee[1][1]) / 2 - np.mean([b_[1] for b_ in bb])) / D, 0.11, 0.145)
        rec(cast + " brow length", bb[0][2] / D, 0.15, 0.17)
    # ---------------- body: arms up so the torso sides are free
    im, f, (ox, oy) = render(cast + "_body", cast, dict(expr="neutral", arm_r=dict(hand=(1.2, -0.2)), arm_l=dict(hand=(-1.2, -0.2)),
                             legs=dict(preset="stand", spread=0.0)), 3.2, 4.2, 1.6, 0.95)
    bg, ink = is_bg(im), is_ink(im)
    yB = puppet.TORSO_TOP + C["torso_h"]
    wmax = 0
    for yv in np.arange(0.62, yB - 0.2, 0.01):
        r = int(round(oy + yv * D))
        seg = ~bg[r, int(ox - 0.7 * D):int(ox + 0.7 * D)]
        x0, x1 = run(seg)
        wmax = max(wmax, x1 - x0 + 1)
    tw = {"hero": (0.54, 0.60), "boss": (0.96, 1.03)}[cast]
    rec(cast + " torso max width", wmax / D, tw[0], tw[1])
    col = ~bg[:, int(round(ox + 0.35 * C["torso_w"] * D * 0.5))]          # a column inside the torso, away from the legs' centre
    # chin = bottom of the head on the centre column; torso bottom = last non-bg pixel between the legs
    cc = ~bg[:, int(round(ox))]
    ys = np.where(cc)[0]
    bottom = ys.max()
    chin = oy + 0.508 * D
    rec(cast + " torso visible height (chin to bottom)", (bottom - chin) / D, 0.84, 0.95)
    # torso contour left / right at the widest row
    r = int(round(oy + (puppet.TORSO_TOP + C["torso_h"] * 0.55) * D))
    line = ink[r, int(ox - 0.7 * D):int(ox + 0.7 * D)]
    idx = np.where(line)[0]
    left_w = 0
    i = idx.min()
    while line[i]:
        left_w += 1; i += 1
    right_w = 0
    i = idx.max()
    while line[i]:
        right_w += 1; i -= 1
    rec(cast + " torso contour, left", left_w / D, 0.018, 0.032)
    rec(cast + " torso contour, right", right_w / D, 0.030, 0.047)
    # trouser bowl height (dark fill below the garment on the centre column... use column at 0.3 half-width)
    # limb width: straight vertical leg, row at mid leg
    r = int(round(oy + (yB + 0.5 * C["leg"]) * D))
    line = ink[r]
    idx = np.where(line)[0]
    segs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    # review: limb weight is per cast now (anatomy 2.3 measures hero limbs 0.040-0.065 D and boss limbs 0.058-0.089 D)
    lim = (0.045, 0.065) if cast == "hero" else (0.058, 0.089)
    rec(cast + " leg stroke width", float(np.mean([len(s_) for s_ in segs])) / D, lim[0], lim[1])
    rec(cast + " hip spacing (leg centres)", (segs[-1].mean() - segs[0].mean()) / D, {"hero": 0.40, "boss": 0.25}[cast], {"hero": 0.47, "boss": 0.33}[cast])
    # arm width: horizontal arm, column through the forearm
    A_ = f["anchors"]
    hx = f["anchors"]["hand_r"][0]
    cx_ = int(round(ox + (hx - 0.18) * D))
    colm = ink[:int(oy + 0.9 * D), cx_]
    idx = np.where(colm)[0]
    segs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    ca = abs(A_["hand_r"][0] - A_["elbow_r"][0]) / math.hypot(A_["hand_r"][0] - A_["elbow_r"][0], A_["hand_r"][1] - A_["elbow_r"][1])
    rec(cast + " arm stroke width (forearm, perpendicular)", min(len(s_) for s_ in segs) / D * ca, lim[0], lim[1])
    # hand ball diameter: column through the hand centre
    cx_ = int(round(ox + hx * D))
    hy = int(round(oy + f["anchors"]["hand_r"][1] * D))
    colm = ink[hy - 60:hy + 60, cx_]
    # review: the hand ball follows the limb weight (hero about 0.12, boss 0.13-0.145; anatomy 2.3)
    rec(cast + " hand ball diameter", colm.sum() / D, 0.110, 0.146)
    A = f["anchors"]
    arm_len = math.hypot(A["elbow_r"][0] - A["shoulder_r"][0], A["elbow_r"][1] - A["shoulder_r"][1]) + math.hypot(A["hand_r"][0] - A["elbow_r"][0], A["hand_r"][1] - A["elbow_r"][1])
    rec(cast + " arm length shoulder-elbow-hand", arm_len, 0.71, 0.79)
    rec(cast + " leg length hip-ankle", A["foot_r"][1] - A["hip"][1], {"hero": 1.05, "boss": 1.40}[cast], {"hero": 1.15, "boss": 1.55}[cast])
    # total height head top (-0.5) to feet, foot stub
    rec(cast + " height, head top to soles", f["feet_y"] + 0.507, 2.9, 3.4)
    r = int(round(oy + (f["feet_y"] - 0.035) * D))
    idx = np.where(ink[r])[0]
    segs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    rec(cast + " foot stub length (incl. the leg's own width)", max(len(s_) for s_ in segs) / D - puppet.LW, 0.12, 0.20)
    # ---------------- hat extents on the normal figure
    im, f, (ox, oy) = render(cast + "_hat", cast, dict(expr="neutral", arm_r="behind", arm_l="behind"), 2.0, 1.8, 1.0, 0.95)
    bg = is_bg(im)
    ys = np.where((~bg).any(1))[0]
    top = (ys.min() - oy) / D
    if cast == "hero":
        rec("hero cap top y", top, -0.62, -0.47)
        r = int(round(oy - 0.42 * D)); x0, x1 = run(~bg[r])
        rec("hero cap width at y = -0.42", (x1 - x0 + 1) / D, 0.84, 0.94)
    else:
        rec("boss hat top y", top, -0.76, -0.66)
        r = int(round(oy - 0.55 * D)); x0, x1 = run(~bg[r])
        rec("boss crown width at y = -0.55", (x1 - x0 + 1) / D, 0.80, 0.90)
        w = max((run(~bg[int(round(oy + yv * D))])[1] - run(~bg[int(round(oy + yv * D))])[0] + 1) for yv in np.arange(-0.42, -0.30, 0.01))
        rec("boss brim width", w / D, 1.08, 1.18)
del puppet.CAST["_bald"]
bad = [r for r in rows if not r[4]]
print("\n%d measurements, %d outside the spec range" % (len(rows), len(bad)))
for r in bad:
    print("  OUT:", r[0], "%.4f" % r[1], "spec", r[2], r[3])
