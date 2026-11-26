"""measure9.py -- the sheet proportions re-measured on the new puppets (front drawing, flat layer rasters at 250 px / D;
flat-mode cards are undistorted, so this is what the camera gets).  Bands = sheet value +/- 6 % (spec/sheet_proportions.md;
Praew's sheet values were read for this pass from 4x gridded crops, tmp/praew_grid_*.png).
python3 measure9.py -> out/measure9.json, out/measure9_table.md, out/measure/<name>_measured.png"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rast9 as R, draw9 as D9, draw8 as D
import raster8
import cv2
PPD = 250
SHEET = json.load(open(os.path.join(R.PROJ, "spec", "sheet_measure", "sheet_measure.json")))
PRAEW = dict(head_over_total=0.223, head_with_hair_over_total=0.258, heads_tall=4.48, hair_above_skull_over_D=0.16, shoulder_over_D=0.92,
             torso_over_total=0.320, torso_over_D=1.43, leg_over_total=0.421, leg_over_D=1.88, leg_w_over_D=0.32, boot_h_over_D=0.33)
KEYS = [("head_over_total", "bare head D / total"), ("head_with_hair_over_total", "hair top to chin / total"), ("heads_tall", "figure height in bare heads"),
        ("hair_above_skull_over_D", "hair above skull / D"), ("hair_extent_over_D", "hair vertical extent / D"), ("hair_w_over_D", "hair width / D"),
        ("shoulder_over_D", "shoulder width / D"), ("torso_over_total", "torso chin-crotch / total"), ("torso_over_D", "torso / D"),
        ("leg_over_total", "legs crotch-sole / total"), ("leg_over_D", "legs / D"), ("leg_w_over_D", "trouser leg width / D"),
        ("boot_h_over_D", "boot/shoe height / D"), ("outline_over_D", "head outline median / D")]
WHO = [("praew", "praew", PRAEW, "Praew"), ("tos", "tos", SHEET["tos"], "Tos"), ("james", "james", SHEET["james"], "James"),
       ("james_helmet", "james_helmet", SHEET["james"], "James"), ("crew_infected", "crew_infected", SHEET["james"], "James"), ("guard", "guard", None, None)]


def fit(xs, ys):
    A = np.c_[2 * xs, 2 * ys, np.ones(len(xs))]
    c, *_ = np.linalg.lstsq(A, xs ** 2 + ys ** 2, rcond=None)
    return c[0], c[1], math.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)


def measure(name, spec):
    sp = D.get_spec(spec)
    fig = D9.build(spec, dict(view="front", s=1, expr="neutral"))
    cv = D.canvas_for(sp)
    L = raster8.layer_pngs(fig, cv, PPD, os.path.join(HERE, "tmp", "layers"), name)
    W, H = int(round((cv[2] - cv[0]) * PPD)), int(round((cv[3] - cv[1]) * PPD))
    M = {}
    for nm, info in L.items():
        a = np.asarray(Image.open(info["color"]).convert("RGBA"))
        x0 = int(round((info["box"][0] - cv[0]) * PPD)); y0 = int(round((info["box"][1] - cv[1]) * PPD))
        m = np.zeros((H, W), bool)
        m[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a[..., 3] > 127
        M[nm] = m; info["rgba"] = a; info["org"] = (x0, y0)
    sil = np.zeros((H, W), bool)
    for m in M.values(): sil |= m
    ys = np.nonzero(sil.any(1))[0]; top, sole = ys.min(), ys.max(); total = sole - top + 1
    head = M["head"]
    hy = np.nonzero(head.any(1))[0]; chin = hy.max(); hcy = (hy.min() + hy.max()) / 2
    h8 = head.astype(np.uint8); bd = (h8 - cv2.erode(h8, np.ones((3, 3), np.uint8))) > 0
    by, bx = np.nonzero(bd); sel = by > hcy
    cx, cy, r = fit(bx[sel].astype(float), by[sel].astype(float))
    widest = max(np.ptp(np.nonzero(head[y])[0]) + 1 for y in hy)
    Dp = (2 * r + widest) / 2
    hair = M["hair"]; hry, hrx = np.nonzero(hair)
    hair_top = min(hry.min(), top); skull_top = cy - Dp / 2
    cxp = int(round((fig["anchors"]["crotch"][0] - cv[0]) * PPD))
    col = sil[:, cxp - 1:cxp + 2].any(1)
    yy = sole - 2
    while yy > top and col[yy]: yy -= 1
    while yy > top and not col[yy]: yy -= 1
    crotch = yy
    band = slice(int(chin + 0.05 * Dp), int(chin + 0.45 * Dp))
    sh = (M["torso"] | M["arm_R"] | M["arm_L"])[band]
    shx = np.nonzero(sh.any(0))[0]; shoulder = np.ptp(shx) + 1
    leg = L["leg_R"]; a = leg["rgba"].astype(int); alr = a[..., 3] > 127
    def hexv(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])
    isb = (np.abs(a[..., :3] - hexv(sp["col"]["boot"])).sum(-1) <= 8) & alr
    ist = (np.abs(a[..., :3] - hexv(sp["col"]["trouser"])).sum(-1) <= 8) & alr
    rb = np.nonzero(isb.sum(1) > 3)[0]; rt = np.nonzero(ist.sum(1) > 3)[0]
    sole_row = np.nonzero(alr.any(1))[0].max()
    boot_top = rb[rb > rt.max() - 2].min() if len(rt) and (rb > rt.max() - 2).any() else rb.min()
    boot_h = sole_row - boot_top + 1
    row = crotch + int(0.25 * PPD) - leg["org"][1]
    rw = np.nonzero(alr[row])[0]; leg_w = np.ptp(rw) + 1
    hd = L["head"]; a3 = hd["rgba"].astype(int); ink = (a3[..., :3].sum(-1) < 120) & (a3[..., 3] > 128)
    c3 = (cx - hd["org"][0], cy - hd["org"][1]); th = []
    for k in range(72):
        ang = 2 * math.pi * k / 72; run = 0
        for rr in np.arange(0.40 * PPD, 0.53 * PPD, 0.5):
            x = int(round(c3[0] + rr * math.cos(ang))); y = int(round(c3[1] + rr * math.sin(ang)))
            if 0 <= x < ink.shape[1] and 0 <= y < ink.shape[0] and ink[y, x]: run += 0.5
        th.append(run)
    res = dict(total_px=int(total), D_px=round(Dp, 1), head_over_total=Dp / total, head_with_hair_over_total=(chin - hair_top) / total, heads_tall=total / Dp,
               hair_above_skull_over_D=(skull_top - hair_top) / Dp, hair_extent_over_D=(hry.max() - hair_top) / Dp, hair_w_over_D=(np.ptp(hrx) + 1) / Dp,
               shoulder_over_D=shoulder / Dp, torso_over_total=(crotch - chin) / total, torso_over_D=(crotch - chin) / Dp, leg_over_total=(sole - crotch) / total,
               leg_over_D=(sole - crotch) / Dp, leg_w_over_D=leg_w / Dp, boot_h_over_D=boot_h / Dp, outline_over_D=float(np.median(th)) / Dp)
    res = {k: (round(float(v), 3) if not isinstance(v, int) else v) for k, v in res.items()}
    im, _, _ = R.flat(spec, dict(view="front", s=1, expr="neutral"), PPD)
    pil = R.over((253, 243, 232), im); d = ImageDraw.Draw(pil)
    for y, c, t in ((hair_top, (255, 0, 0), "hair top"), (skull_top, (255, 128, 0), "skull"), (chin, (255, 0, 255), "chin"), (crotch, (0, 150, 0), "crotch"), (sole, (255, 0, 0), "sole")):
        d.line([(0, y), (W, y)], fill=c, width=2); d.text((4, y - 12), t, fill=c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 180, 255), width=2)
    d.line([(shx.min(), band.start), (shx.max(), band.start)], fill=(0, 180, 180), width=3)
    os.makedirs(os.path.join(HERE, "out", "measure"), exist_ok=True)
    pil.save(os.path.join(HERE, "out", "measure", name + "_measured.png"))
    return res


if __name__ == "__main__":
    out = {}
    for name, spec, ref, rn in WHO:
        m = measure(name, spec)
        chk = []
        for k, lab in KEYS:
            t = ref.get(k) if ref else None
            v = m.get(k)
            chk.append(dict(measure=lab, sheet=t, ours=v, ok=(None if t is None else bool(t * 0.94 <= v <= t * 1.06))))
        out[name] = dict(measured=m, ref=rn, check=chk)
    json.dump(out, open(os.path.join(HERE, "out", "measure9.json"), "w"), indent=1)
    names = [w[0] for w in WHO]
    lines = ["| measure | " + " | ".join("%s (vs %s sheet)" % (n, out[n]["ref"]) if out[n]["ref"] else n + " (no sheet figure)" for n in names) + " |", "|---|" + "---|" * len(names)]
    for i, (k, lab) in enumerate(KEYS):
        cells = []
        for n in names:
            c = out[n]["check"][i]
            cells.append("%.3f%s" % (c["ours"], "" if c["sheet"] is None else " / %.3f %s" % (c["sheet"], "ok" if c["ok"] else "**OUT**")))
        lines.append("| %s | %s |" % (lab, " | ".join(cells)))
    open(os.path.join(HERE, "out", "measure9_table.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    R.close()
