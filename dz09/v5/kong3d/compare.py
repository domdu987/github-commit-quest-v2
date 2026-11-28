"""compare.py -- out/../compare.png: row 1 reference d (f_015, f_024 crops), row 2 our 3D Kong shots, row 3 the same
shot 2 with the current 2.5D card Kong next to the 3D one. Also prints the hue report rows and the head shade hue."""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
TH = 640
W = 4 * 360 + 5 * 12


def tile(path, crop=None, h=TH):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def label(d, xy, txt, f):
    x, y = xy
    bb = d.textbbox((x, y), txt, font=f)
    d.rectangle([bb[0] - 6, bb[1] - 4, bb[2] + 6, bb[3] + 4], fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=(255, 255, 255))


def main():
    ref = os.path.join(PROJ, "ref", "d", "frames")
    rows = [
        ("Reference d (look only): real 3D bodies, lit heads, close lens, macro insert with the face soft behind",
         [(tile(os.path.join(ref, "f_015.png"), (0, 380, 720, 1280)), "ref d f_015 (crop)"),
          (tile(os.path.join(ref, "f_024.png"), (0, 0, 720, 860)), "ref d f_024 (crop)")]),
        ("v5/kong3d: 3D Kong in the v4 expressway set, 720x1280 final (shown at half size)",
         [(tile(os.path.join(OUT, n + ".png")), lab) for n, lab in
          (("low", "1 low close"), ("mcu", "2 eye-level MCU"), ("ots", "3 over the shoulder"), ("macro", "4 macro insert"))]),
        ("Same shot 2: current 2.5D card Kong (v4/cast_dz09) vs 3D Kong",
         [(tile(os.path.join(OUT, "mcu25.png")), "2.5D cards (v4)"), (tile(os.path.join(OUT, "mcu.png")), "3D (v5)")]),
    ]
    f = ImageFont.truetype(FONT, 22); fh = ImageFont.truetype(FONT, 26)
    H = sum(TH + 60 for _ in rows) + 12
    sheet = Image.new("RGB", (W, H), (22, 22, 28)); d = ImageDraw.Draw(sheet)
    y = 12
    for title, tiles in rows:
        d.text((12, y), title, font=fh, fill=(240, 200, 120)); y += 44
        x = 12
        for im, lab in tiles:
            sheet.paste(im, (x, y)); label(d, (x + 10, y + TH - 40), lab, f); x += im.width + 12
        y += TH + 16
    p = os.path.join(HERE, "compare.png"); sheet.save(p); print(p, sheet.size)


def hue():
    sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
    from hue_report import stats
    rows = {}
    for n in ("low", "mcu", "ots", "macro", "mcu25"):
        p = os.path.join(OUT, n + ".png")
        if not os.path.exists(p): continue
        h, s, v, dk = stats([p])
        rows[n] = dict({k: round(x, 1) for k, x in h.items()}, sat=round(s, 3), val=round(v, 3), dark=round(dk, 3))
    # shade hue of the head: the darker half of Kong's head pixels (white albedo), from the object index is not
    # separable, so sample low-saturation-white-ish pixels in the head box measured from the render
    return rows


def head_shade(png, box):
    """mean hue of the shaded part of the white head inside box (x0, y0, x1, y1) at 720x1280."""
    import colorsys
    im = np.asarray(Image.open(png).convert("RGB").crop(box), np.float32) / 255
    mx = im.max(-1); mn = im.min(-1)
    sel = (mx > 0.12) & (mx < 0.55)      # shaded side, not the lit side, not the ink
    px = im[sel]
    if len(px) == 0: return None
    m = px.mean(0)
    h, s, v = colorsys.rgb_to_hsv(*m)
    hs = [colorsys.rgb_to_hsv(*p)[0] * 360 for p in px[:: max(1, len(px) // 4000)]]
    return dict(mean_rgb=[round(float(x), 3) for x in m], hue_of_mean=round(h * 360, 1), median_hue=round(float(np.median(hs)), 1),
                sat=round(s, 3), n=int(sel.sum()))


if __name__ == "__main__":
    main()
    r = hue()
    print(json.dumps(r, indent=1))
    json.dump(r, open(os.path.join(OUT, "hue.json"), "w"), indent=1)
