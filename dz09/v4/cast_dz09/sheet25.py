"""sheet25.py -- contact sheet of the 2.5D cast beside a crop of uploads/character_sheet.webp and a reference
puppet from ref/c at the same head size.   python3 sheet25.py  -> out/contact_sheet.png (+ out/layers_exploded.png)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import draw25d, raster25, phone25, cast25
import puppet

T = os.path.join(HERE, "tmp", "sheet")
os.makedirs(T, exist_ok=True)
FONT = ImageFont.truetype(phone25.FONT, 20, layout_engine=ImageFont.Layout.RAQM)
FONT_S = ImageFont.truetype(phone25.FONT, 15, layout_engine=ImageFont.Layout.RAQM)
BG = "#d8d2c6"
PPD = 96                      # px per D in the body tiles (head 96 px)
BODY = (-1.7, -1.05, 1.7, 3.0)


def tile(name, pose, canvas=BODY, ppd=PPD, bg=BG, label=""):
    f = draw25d.build(name, pose)
    p = os.path.join(T, "%s_%d.png" % (name, abs(hash(repr(sorted(pose.items(), key=str)))) % 10 ** 8))
    raster25.flat_png(f, canvas, ppd, p, bg=bg)
    im = Image.open(p).convert("RGB")
    if label:                                     # label in its own strip under the tile, never over the drawing
        lab = Image.new("RGB", (im.width, im.height + 24), (40, 40, 48))
        lab.paste(im, (0, 0))
        d = ImageDraw.Draw(lab)
        d.text((6, im.height + 3), label, font=FONT_S, fill=(236, 232, 220))
        im = lab
    return im


def row(ims, gap=6):
    W = sum(i.width for i in ims) + gap * (len(ims) - 1)
    H = max(i.height for i in ims)
    r = Image.new("RGB", (W, H), (40, 40, 48))
    x = 0
    for i in ims:
        r.paste(i, (x, 0))
        x += i.width + gap
    return r


def exploded(name, pose, ppd=80):
    """the layer stack pulled apart: each layer shifted right/up by its depth so the stack order reads."""
    f = draw25d.build(name, pose)
    parts = []
    for i, L in enumerate(f["layers"]):
        dx, dy = i * 0.55, -i * 0.10
        parts.append('<g transform="translate(%.3f %.3f)" opacity="0.97">%s</g>' % (dx, dy, L["svg"]))
        parts.append('<text x="%.3f" y="%.3f" font-size="0.16" font-family="DejaVu Sans" fill="#222">%s z%+.1f</text>' % (
            -0.6 + dx, 3.25 + dy + (0.2 if i % 2 else 0), L["name"], L["z"]))
    canvas = (-1.8, -1.6, 1.8 + 0.55 * len(f["layers"]), 3.7)
    p = os.path.join(T, "exploded_%s.png" % name)
    svg, W, H = draw25d.doc("".join(parts), canvas, ppd, BG)
    raster25.png(svg, W, H, p)
    return Image.open(p).convert("RGB")


def main():
    cut = {"type": "cutter", "angle": 96, "bars": 3}
    r1 = [tile("kong", {"yaw": 0, "arm_l": "hold", "prop_l": cut, "expr": "determined"}, label="Kong front"),
          tile("kong", {"yaw": 0.5, "arm_l": "hold", "prop_l": cut, "expr": "determined"}, label="3/4 (+)"),
          tile("kong", {"yaw": 1.0, "arm_l": "hold", "prop_l": cut, "expr": "determined"}, label="side (+)"),
          tile("kong", {"yaw": -0.5, "arm_r": "hold", "prop_r": cut, "expr": "determined"}, label="3/4 (-)"),
          tile("kong", {"yaw": -1.0, "arm_r": "hold", "prop_r": cut, "expr": "determined"}, label="side (-)"),
          tile("kong_wet", {"yaw": 0.5, "arm_l": "hold", "prop_l": dict(cut, bars=2), "expr": "tired"}, label="WET 3/4"),
          tile("kong_wet", {"yaw": 0.0, "expr": "alarmed"}, label="WET front")]
    HEAD = (-0.75, -0.85, 0.75, 0.62)
    exprs = [("kong", e) for e in ("determined", "tired", "guilty", "alarmed", "shouting", "talk", "blink")] + \
            [("crew", e) for e in ("neutral", "alarmed", "shouting", "pain")] + \
            [("driver", e) for e in ("still", "head_lift", "lunge")] + [("namnuea", "smile")]
    r2 = [tile(n, {"expr": e, "yaw": 0.25 if n != "driver" else 0.0}, HEAD, 120, label="%s %s" % (n, e)) for n, e in exprs]
    r2b = r2[8:]
    r2 = r2[:8]
    scr = phone25.screen_png(os.path.join(T, "screen.png"), 270, 500)
    uri = phone25.data_uri(scr)
    story = []
    for k in ("dz_kong_cutter", "dz_kong_phone", "dz_kong_call", "dz_kong_shout", "dz_crew_shout", "dz_driver_still",
              "dz_driver_lift", "dz_infected_lunge"):
        n, p = cast25.STORY[k]
        p = dict(p)
        for side in ("r", "l"):
            pr = p.get("prop_" + side)
            if pr == "phone" or (isinstance(pr, dict) and pr.get("type") == "phone"):
                p["prop_" + side] = {"type": "phone", "screen_png": uri}
        cv = (-2.1, -2.7, 2.1, 3.0)           # tall enough for a raised crowbar
        story.append(tile(n, p, cv, 80, label=k[3:]))
    props = []
    for b in (3, 2, 1):
        props.append(tile("kong", {"arm_l": "hold", "prop_l": dict(cut, bars=b, angle=0), "yaw": 0.5}, (-1.3, 0.4, 2.3, 2.3), 100,
                          label="cutter %d bars" % b))
    props.append(tile("kong", {"arm_r": "raise", "prop_r": {"type": "crowbar", "angle": -70}, "yaw": -0.5, "expr": "shouting"},
                      (-1.6, -3.0, 1.8, 1.4), 80, label="crowbar"))
    ins = Image.open(os.path.join(HERE, "out", "phone_insert.png")).convert("RGBA")
    ins = ins.resize((int(ins.width * 300 / ins.height), 300))
    pi = Image.new("RGB", (ins.width + 20, 320), (216, 210, 198))
    pi.paste(ins, (10, 10), ins)
    props.append(pi)
    ex = exploded("kong", {"yaw": 0.5, "arm_l": "hold", "prop_l": cut, "expr": "determined"})
    ex.save(os.path.join(HERE, "out", "layers_exploded.png"))
    # references: crop of the character sheet (Kong + Namnuea) and a ref/c puppet, scaled to head ~96 px
    cs = Image.open(os.path.join(PROJ, "uploads", "character_sheet.webp")).convert("RGB")
    cs = cs.crop((0, 120, 345, 690))                 # Kong and Namnuea, head ~150 px wide
    cs = cs.resize((int(cs.width * 96 / 150), int(cs.height * 96 / 150)))
    rf = Image.open(os.path.join(PROJ, "ref", "c", "frames2", "f_014.png")).convert("RGB").crop((230, 520, 420, 860))     # stops above the burned-in caption
    rf = rf.resize((int(rf.width * 96 / 127), int(rf.height * 96 / 127)))
    refs = row([cs, rf])
    rows = [("Kong: front / 3/4 / side drawings swap with yaw (stage maps camera yaw: 3/4 from 18 deg, side from 48 deg); wet variant", row(r1)),
            ("Expressions: Kong (determined tired guilty alarmed shouting talk blink), crew", row(r2)),
            ("crew pain, infected still / head-lift / lunge, Namnuea", row(r2b)),
            ("EP.1 hook poses (flat composite of the layers)", row(story)),
            ("Props as separate cards: cutter battery 3/2/1 bars, crowbar, phone (Thai screen)", row(props)),
            ("Layer stack (back -> front) of Kong 3/4, z = depth in gap units", ex),
            ("Reference: character_sheet.webp crop (Kong, Namnuea) and ref/c f_014 puppet, both scaled to head 96 px", refs)]
    W = max(r.width for _, r in rows) + 40
    H = sum(r.height + 44 for _, r in rows) + 60
    sheet = Image.new("RGB", (W, H), (24, 24, 30))
    d = ImageDraw.Draw(sheet)
    d.text((20, 14), "DEAD ZONE 09 - 2.5D cast (v4/cast_dz09)  head D = 96 px in body tiles", font=FONT, fill=(255, 220, 120))
    y = 54
    for lab, r in rows:
        d.text((20, y), lab, font=FONT_S, fill=(230, 230, 236))
        sheet.paste(r, (20, y + 22))
        y += r.height + 44
    out = os.path.join(HERE, "out", "contact_sheet.png")
    sheet.save(out)
    print(out, sheet.size)
    raster25.close()


if __name__ == "__main__":
    main()
