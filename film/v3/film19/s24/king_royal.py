"""king_royal.py -- s24-LOCAL royal look for king19 (QA-art final-gate finding: at phone size the King reads as another astronomer).
Applied in-process by shot.py (apply()); cast19.py and the cast files are NOT changed.  king19 gets
  * a red robe (coat + sleeves red) with white ermine lapels and an ermine hem, black ermine tails,
  * a small gold crown on the powdered wig (hat style 'royalwig19'),
  * a bolder blue sash and a bigger Garter star.
"""
import math
import cast19
import puppet as P
import cast_ext as CE

ROBE, ROBE_D = "#c2202e", "#7a1220"
ERMINE = "#f8f4ec"


def _tails(k, pts):
    o = []
    for (x, y) in pts:
        o.append('<path d="M%.4f,%.4f q0.014,-0.022 0.028,0 l-0.014,0.050 z" fill="#14101a"/>' % (x - 0.014, y))
    return "".join(o)


def _cos_royal19(k, C, m):
    inside, mid, ov = cast19._cos_georgian19(k, C, m)
    X = cast19._X(m)
    h = C["torso_h"]
    yB = cast19.TT + h
    hw = m.hwa
    a = max(1.0, hw / 0.70)
    extra = []
    # ermine lapel tails (black spots on the white fur facings)
    pts = []
    for s in (-1, 1):
        for i, y in enumerate((0.62, 0.78, 0.94, 1.10)):
            if y < yB - 0.16:
                x, yy = X(s * (0.245 + 0.01 * (i % 2)) * a, y)
                pts.append((x, yy))
    extra.append(_tails(k, pts))
    # bolder star (bigger silver Garter star over the small one)
    c = X(0.30 * a, 0.70)
    extra.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (
        P._poly_d(cast19._star(c[0], c[1], 0.19, 8, 0.50, -90)), k.c("#e4e8f2"), k.ink))
    extra.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (
        P._poly_d(cast19._star(c[0], c[1], 0.145, 8, 0.50, -67.5)), k.c("#f6f8ff"), k.ink))
    extra.append('<circle cx="%.4f" cy="%.4f" r="0.070" fill="#f4f0e6" stroke="%s" stroke-width="0.012"/>' % (c[0], c[1], k.ink))
    extra.append('<path d="M%.4f,%.4f h0.090 M%.4f,%.4f v0.090" stroke="#c0282a" stroke-width="0.024"/>' % (c[0] - 0.045, c[1], c[0], c[1] - 0.045))
    # ermine hem band on the skirt (white fur, black tails)
    hem = yB + C.get("coat_len", 0.46)
    b = hw + C.get("coat_flare", 0.12)
    y0, y1 = hem - 0.13, hem + 0.01
    band = [X(-b * 0.985, y0), X(b * 0.985, y0), X(b * 1.00, y1), X(-b * 1.00, y1)]
    hemsvg = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (P._poly_d(band), k.c(ERMINE), k.ink)
    hp = []
    for i in range(7):
        t = -0.84 + 0.28 * i
        x, yy = X(t * b, y0 + 0.045)
        hp.append((x, yy))
    hemsvg += _tails(k, hp)
    return inside + "".join(extra), mid, ov + hemsvg


def _hat_royal19(k, C, yaw):
    W = C["wig19"]
    col = C["hat_colors"]
    o, pts = cast19._wig_svg(k, C, yaw, W["style"], col, W.get("hair_dy", 0.0))
    cx = pts[2][0]
    top = min(p[1] for p in pts)
    by = top + 0.12
    gold, gold_d = k.c(cast19.GOLDC["base"]), k.c(cast19.GOLDC["dark"] if "dark" in cast19.GOLDC else "#a07818")
    cr = ('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
          % (cx - 0.26, by, cx - 0.30, by - 0.26, cx - 0.16, by - 0.13, cx - 0.08, by - 0.30, cx, by - 0.14, cx + 0.08, by - 0.30, cx + 0.16, by - 0.13, cx + 0.30, by - 0.26, cx + 0.26, by, gold, k.ink))
    cr += '<rect x="%.3f" y="%.3f" width="0.52" height="0.075" rx="0.012" fill="#b3202c" stroke="%s" stroke-width="0.016"/>' % (cx - 0.26, by - 0.075, k.ink)
    for (jx, col_) in ((-0.15, "#2a55d8"), (0.0, "#f4f0e6"), (0.15, "#2a55d8")):
        cr += '<circle cx="%.3f" cy="%.3f" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/>' % (cx + jx, by - 0.037, col_, k.ink)
    for (px, py) in ((-0.30, -0.26), (-0.08, -0.30), (0.08, -0.30), (0.30, -0.26)):
        cr += '<circle cx="%.3f" cy="%.3f" r="0.028" fill="#fff6dc" stroke="%s" stroke-width="0.010"/>' % (cx + px, by + py - 0.01, k.ink)
    cr += '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#fff3b0" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (cx - 0.20, by - 0.02, cx - 0.12, by - 0.10)
    o = '<g transform="rotate(%.3f)">%s%s</g>' % (C["hat_tilt"], o, cr)
    return o, (-0.03 * yaw, top - 0.30)


def apply():
    """re-skin king19 in this process only."""
    CE.COSTUMES["royal19"] = _cos_royal19
    CE.HATS["royalwig19"] = _hat_royal19
    K = P.CAST["king19"]
    K["costume"] = "royal19"
    K["hat_style"] = "royalwig19"
    K["colors"] = dict(K["colors"], base=ROBE, dark=ROBE_D, lapel=ERMINE, sash="#1b4fd8", sash_l="#8ab8ff")
    K["sleeve"] = dict(K["sleeve"], color=ROBE, dark=ROBE_D, cuff=ERMINE)
    return K
