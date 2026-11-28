"""sheet.py -- gauge_sheet.png: every film gauge at 6 values / states, large, on a dark and on a bright background.
    python3 sheet.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
import gauge as G, layer as LY
T = G.Track
FONT = os.path.join(HERE, "..", "..", "fonts", "WorkSans-Black.ttf")


def cell(kind, i):
    """one gauge instance (drawn at t = 5) for column i of 6."""
    t = 5.0
    if kind == "signal":
        v = [1, 0.75, 0.5, 0.25, 0.0, 0.5][i]
        tr = T(v) if i < 5 else T(1.0, [(t - 0.10, 0.5, "hit")])
        return G.Gauge("s", tr, 0, 99, picto="signal", segments=4, label="สัญญาณ", delta_scale=4), ["4/4", "3/4", "2/4", "1/4", "0 critical", "hit -2 (+0.10 s)"][i]
    if kind == "battery":
        v = [0, 1 / 3., 2 / 3., 1, 1, 2 / 3.][i]
        tr = T(v) if i != 5 else T(1 / 3., [(t - 0.06, 2 / 3., "hit")])
        q = [(0, 0.74, 0.82)] if i == 4 else []
        return G.Gauge("b", tr, 0, 99, picto="bolt", segments=3, label="แบต", crit=None, delta_scale=3, quiet=q), ["0/3", "1/3", "2/3", "3/3", "quiet (S10)", "hit +1 (+0.06 s)"][i]
    if kind == "calls":
        v = [0, 0.25, 0.5, 0.75, 1, 1][i]
        tr = T(v) if i != 5 else T(0.75, [(t - 0.08, 1.0, "hit", 0.9)])
        return G.Gauge("c", tr, 0, 99, picto="phone", segments=4, label="สาย", number=lambda t, v=v: "%d" % round(v * 4), polarity="bad", crit=0.99, delta_scale=4), ["0", "1", "2", "3", "4 critical", "hit +1 (+0.08 s)"][i]
    if kind == "trust":
        v = [1.0, 0.62, 0.38, 0.24, 0.02, 0.24][i]
        tr = T(v) if i != 5 else T(0.38, [(t - 0.12, 0.24, "hit")])
        if i == 2:
            tr = T(0.42, [(4.0, 0.42, "ramp"), (7.0, 0.30, "ramp")])
        return G.Gauge("t", tr, 0, 99, picto="heart", label="เชื่อใจ"), ["100", "62", "draining (arrow)", "24", "2 critical", "hit -14 (+0.12 s)"][i]
    if kind == "danger":
        v = [0.10, 0.36, 0.6, 0.82, 1.0, 1.0][i]
        tr = T(v) if i != 5 else T(0.6, [(t - 0.08, 1.0, "hit", 1.0)])
        if i == 1:
            tr = T(0.3, [(4.0, 0.3, "ramp"), (7.0, 0.42, "ramp")])
        return G.Gauge("d", tr, 0, 99, picto="warn", label="อันตราย", polarity="bad"), ["10", "rising (arrow)", "60", "82", "100 critical", "hit +40 (+0.08 s)"][i]
    if kind == "pop":
        g = G.Gauge("p", T(0.5), 4.9, 5.4, picto="heart", label="เชื่อใจ")
        dt = [0.04, 0.125, 0.21, 0.33, 0.42, 0.46][i]
        g.t_in = t - dt; g.t_out = g.t_in + 0.5
        return g, ["pop in +1 f", "+3 f", "+5 f", "hold", "pop out -2 f", "-1 f"][i]


def hcell(kind, i):
    t = 5.0
    pol = lambda v: 0.42 + (1 - v) * 2.4
    if kind == "count":
        n = [60, 59, 57, 52, 45, 58][i]
        v = 1 - 0.045 * (60 - n)
        tr = T(v) if i != 5 else T(v + 0.045, [(t - 0.08, v, "hit", 0.45)])
        return G.Gauge("h", tr, 0, 99, orient="h", w=64, length=330, picto="stopwatch", number=lambda t, n=n: "%d" % n, polarity=pol, crit=None, delta_scale=1 / 0.045), "%d%s" % (n, " hit" if i == 5 else "")
    v = [0.9, 0.5, 0.24, 0.14, 0.03, 0.14][i]
    tr = T(v) if i != 5 else T(0.24, [(t - 0.1, 0.14, "hit")])
    return G.Gauge("h", tr, 0, 99, orient="h", w=60, length=330, picto="heart", label="เชื่อใจ"), "lying trust %d" % round(v * 100)


def main(out=os.path.join(HERE, "gauge_sheet.png")):
    SS = 1.5                                       # drawn at 2x the 720 reference: a tube is 144 px wide on the sheet
    rows = ["signal", "battery", "calls", "trust", "danger", "pop"]
    CW, CH, HH = 330, 500, 150
    Wd = 6 * CW
    Hd = len(rows) * CH + 2 * HH * 2 + 230
    gs, labels = [], []
    for r, kind in enumerate(rows):
        for i in range(6):
            g, lab = cell(kind, i)
            g.x, g.y, g.length = i * CW + CW / 2 - 40, r * CH + 100, 330
            gs.append(g); labels.append((i * CW + 12, r * CH + 10, "%s: %s" % (kind, lab)))
    y0 = len(rows) * CH
    for r, kind in enumerate(["count", "trusth"]):
        for i in range(3):
            for j in range(2):
                k = i + 3 * j
                g, lab = hcell(kind, k)
                g.x, g.y = i * (Wd / 3) + 90, y0 + (r * 2 + j) * HH + 80
                gs.append(g); labels.append((i * (Wd / 3) + 12, y0 + (r * 2 + j) * HH + 6, lab))
    y1 = y0 + 4 * HH
    here_tex = os.path.join(HERE, "..", "..", "v10", "film", "tex", "avatar.png")
    gs.append(G.Gauge("v", None, 0, 99, x=150, y=y1 + 95, r=62, kind="avatar", image=G.data_uri(here_tex), level=lambda t: 0.7, label="น้ำเหนือ"))
    gs.append(G.Gauge("m", None, 0, 99, x=400, y=y1 + 110, r=92, kind="badge", picto="biohazard", color=G.AMBER))
    px = 420
    for nm in ["bolt", "heart", "phone", "warn", "stopwatch", "signal", "biohazard"]:
        px += 190
        gs.append(G.Gauge("x" + nm, None, 0, 99, x=px, y=y1 + 110, r=62, kind="badge", picto=nm, color=G.ramp_color((px % 570) / 570.0)))
    labels.append((12, y1 + 4, "voice badge, title mark, the pictograms"))
    half = []
    for name, col in (("dark", None), ("bright", (226, 220, 204))):
        W, H = int(Wd * SS), int(Hd * SS)
        if col is None:
            bg = Image.new("RGB", (W, H), (22, 26, 48))
            import glob
            fr = sorted(glob.glob(os.path.join(HERE, "..", "..", "v10", "film", "out", "draft_360x640", "S19", "f_*.png")))
            fr = [f for f in fr if "depth" not in f]
            if fr:
                tile = Image.open(fr[len(fr) // 2]).convert("RGB").resize((W, int(W * 640 / 360 * 0.5)), Image.BICUBIC)
                for yy in range(0, H, tile.height): bg.paste(tile, (0, yy))
        else:
            bg = Image.new("RGB", (W, H), col)
            fr = os.path.join(HERE, "..", "..", "v10", "film", "out", "draft_360x640", "S09", "f_0400.png")
            if os.path.exists(fr):
                tile = Image.open(fr).convert("RGB").crop((200, 150, 360, 400)).resize((W, int(W * 250 / 160)), Image.BICUBIC)
                tile = Image.blend(tile, Image.new("RGB", tile.size, col), 0.45)
                for yy in range(0, H, tile.height): bg.paste(tile, (0, yy))
        im = render(gs, 5.0, W, H, SS, bg)
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(FONT, 26)
        for x, y, s in labels:
            d.text((x * SS, y * SS), s, font=f, fill=(255, 255, 255) if col is None else (20, 20, 24), stroke_width=3, stroke_fill=(0, 0, 0) if col is None else (255, 255, 255))
        half.append(im)
    S = Image.new("RGB", (half[0].width * 2 + 20, half[0].height), (0, 0, 0))
    S.paste(half[0], (0, 0)); S.paste(half[1], (half[0].width + 20, 0))
    S.save(out); print("wrote", out, S.size)
    LY.close()


def render(gs, t, W, H, SS, bg):
    """like Layer.image but with an explicit scale (SS x the 720 reference) on a page of any size."""
    import gauge
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>' % (W, H, W, H, gauge._defs_filters())
    for i, g in enumerate(gs):
        s += '<g transform="translate(%s %s) scale(%s)">%s</g>' % (g.x * SS, g.y * SS, g.w / 100.0 * SS, gauge.gauge_svg(g, t, "u%d" % i))
    s += "</svg>"
    p = os.path.join(HERE, "tmp", "_sheet.png")
    LY.raster.render([{"svg": s, "w": W, "h": H, "out": p}])
    im = bg.convert("RGBA"); im.alpha_composite(Image.open(p).convert("RGBA"))
    return im.convert("RGB")


if __name__ == "__main__":
    main()
