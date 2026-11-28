"""measure_sheets.py -- proportions of Kong and the office zombie, measured with PIL / numpy on the sheet turnarounds.
Silhouette extents and widths come from a background-distance mask; internal lines (chin, belt, crotch, hem, boot top)
are landmark rows read off 3x gridded crops (out/g_*.png) and drawn back onto out/proportions_annot.png for checking."""
import json, numpy as np, cv2
from PIL import Image, ImageDraw
P = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/sheets_v3/'
OUT = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/v16/block/'

SHEETS = {
    "kong": dict(file="kong.png", height_m=1.80, rows=(82, 394),
                 views=dict(front=(322, 528), q45=(530, 708), side=(712, 836), back=(845, 1056), back45=(1060, 1216)),
                 # landmark rows (sheet px, front view) read from out/g_kong_front.png / out/g_kong_side.png
                 lm=dict(chin=162, shoulder_top=176, sleeve_cuff=245, belt=250, crotch=306, hem=345, hand_top=247, hand_bot=292, brow=128, eye=134, mouth=144)),
    "z_office": dict(file="z_office.png", height_m=1.75, rows=(8, 486),
                     views=dict(front=(234, 562), q45=(565, 816), side=(820, 1010), back=(1012, 1292), back45=(1294, 1536)),
                     lm=dict(chin=145, shoulder_top=158, sleeve_cuff=278, belt=290, crotch=335, hem=448, hand_top=270, hand_bot=340, brow=72, eye=80, mouth=118)),
}


def mask_of(a):
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV).astype(np.float32)
    S, V = hsv[..., 1] / 255, hsv[..., 2] / 255
    af = a.astype(np.float32) / 255
    cand = (V > 0.80) & (S < 0.20)
    bg = np.zeros((a.shape[0], 1, 3), np.float32)
    for r in range(a.shape[0]):
        c = af[r][cand[r]]
        bg[r, 0] = np.median(c, 0) if len(c) > 20 else (bg[r - 1, 0] if r else (.92, .86, .8))
    d = np.abs(af - bg).sum(2)
    m = ((d > 0.13) | (V < 0.55)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - m, 4)       # fill small holes only (tape, buttons)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 900: m[lab == i] = 1
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)          # keep the figure: the largest component
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return (lab == k).astype(np.uint8)


def extent(m, y, x0=0):
    xs = np.nonzero(m[y])[0]
    return (int(xs[0]) + x0, int(xs[-1]) + x0) if len(xs) else (None, None)


def measure(name):
    S = SHEETS[name]
    im = np.asarray(Image.open(P + S["file"]).convert("RGB"))
    y0, y1 = S["rows"]
    res = {}
    annot = Image.fromarray(im[y0:y1].copy()); dr = ImageDraw.Draw(annot)
    for v, (x0, x1) in S["views"].items():
        m = mask_of(im[y0:y1, x0:x1].copy())
        # the ground shadow: drop thin rows at the bottom (shadow is low-contrast, removed by d threshold mostly)
        rows = np.nonzero(m.sum(1) > 4)[0]
        hsv = cv2.cvtColor(im[y0:y1, x0:x1].copy(), cv2.COLOR_RGB2HSV)
        dark = (hsv[..., 2] < 150) & (m > 0)                     # shoes / boots: the ground shadow is light, the soles are dark
        drows = np.nonzero(dark.sum(1) > 6)[0]
        top, bot = int(rows[0]) + y0, int(drows[-1]) + y0
        res_dark = dark
        res[v] = dict(top=top, bottom=bot, H=bot - top, m=m, x0=x0, dark=dark)
        dr.rectangle([x0, top - y0, x1, bot - y0], outline=(0, 120, 255))
    L = S["lm"]; F = res["front"]; Sd = res["side"]; H = F["H"]; mm = S["height_m"] * 1000.0 / H
    w = lambda r, y: (lambda e: e[1] - e[0] if e[0] is not None else 0)(extent(r["m"], y - y0, r["x0"]))
    def band_max(r, ya, yb):
        best = 0
        for y in range(ya, yb): best = max(best, w(r, y))
        return best
    top = F["top"]
    out = dict(px_per_m=round(H / S["height_m"], 1), mm_per_px=round(mm, 2), total_px=H)
    # head cube: width at eye level on the front view (the hair hangs beside the cube above the brows)
    head_w = w(F, L["chin"] - 7); hair_w = band_max(F, top, L["eye"])
    out.update(
        hair_top_to_chin=(L["chin"] - top) / H,
        head_cube_w=head_w / H, hair_w=hair_w / H,
        head_cube_depth_side=w(Sd, L["chin"] - 7) / H,
        shoulder_span=band_max(F, L["shoulder_top"] + 8, L["sleeve_cuff"]) / H,
        hands_span=band_max(F, L["hand_top"], L["hand_bot"]) / H,
        chin_to_crotch=(L["crotch"] - L["chin"]) / H, crotch_to_sole=(F["bottom"] - L["crotch"]) / H,
        chin_to_belt=(L["belt"] - L["chin"]) / H,
        shoe_h=(F["bottom"] - L["hem"]) / H, hand_h=(L["hand_bot"] - L["hand_top"]) / H,
        leg_span_at_shin=w(F, L["hem"] - 12) / H,
        foot_len_side=max(int(np.ptp(np.nonzero(Sd["dark"][y - y0])[0])) for y in range(Sd["bottom"] - 14, Sd["bottom"] - 2) if Sd["dark"][y - y0].any()) / H,
        torso_depth_side=w(Sd, (L["shoulder_top"] + L["belt"]) // 2) / H,
        side_H=Sd["H"] / H,
    )
    out = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()}
    # runs of the figure on the hand row: fist | (gap) | body | (gap) | fist
    yh = (L["hand_top"] + L["hand_bot"]) // 2
    row = F["m"][yh - y0]; xs = np.nonzero(np.diff(np.r_[0, row, 0]))[0].reshape(-1, 2)
    out["hand_row_runs_px"] = [[int(a) + F["x0"], int(b) + F["x0"]] for a, b in xs]
    out["metres"] = {k: round(v * S["height_m"], 3) for k, v in out.items() if isinstance(v, float) and k not in ("side_H", "px_per_m", "mm_per_px")}
    x0, x1 = S["views"]["front"]
    for k, y in L.items():
        dr.line([(x0, y - y0), (x1, y - y0)], fill=(255, 0, 0)); dr.text((x1 + 2, y - y0 - 6), k, fill=(255, 0, 0))
    for v in res.values(): v.pop("m"); v.pop("dark")
    out["views"] = res
    return out, annot


if __name__ == "__main__":
    allr = {}
    ims = []
    for n in SHEETS:
        r, a = measure(n); allr[n] = r; ims.append(a)
    json.dump(allr, open(OUT + "out/proportions.json", "w"), indent=1)
    W = max(i.width for i in ims); Hh = sum(i.height for i in ims)
    c = Image.new("RGB", (W, Hh), "white"); y = 0
    for i in ims: c.paste(i, (0, y)); y += i.height
    c.save(OUT + "out/proportions_annot.png")
    for n, r in allr.items():
        print(n, {k: v for k, v in r.items() if k not in ("views", "metres")})
        print("  views", {k: (v["top"], v["bottom"], v["H"]) for k, v in r["views"].items()})
        print("  metres", r["metres"])
