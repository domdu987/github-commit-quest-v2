"""audit8.py -- flat drawings of the cast in every view / key pose for the costume audit -> tmp/flat/audit_<name>.png
python3 audit8.py [kong|crew|driver|extras ...]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import draw8, raster8
from PIL import Image
CUT = {"type": "cutter", "bars": 3}
SETS = {
 "kong": [("kong", {"view": "front", "arm_r": "hold_cutter", "prop_r": CUT}), ("kong", {"view": "q", "arm_n": "hold_cutter", "prop_n": CUT}),
          ("kong", {"view": "side", "arm_n": "hold_cutter", "prop_n": CUT}), ("kong", {"view": "back"}),
          ("kong_wet", {"view": "front", "arm_r": "hold_cutter", "prop_r": dict(CUT, wet=True)})],
 "crew": [("crew", {"view": "front"}), ("crew", {"view": "q"}), ("crew", {"view": "side"}), ("crew", {"view": "back"}),
          ("crew", {"view": "front", "expr": "joy"}), ("crew_wet", {"view": "q", "expr": "shouting"})],
 "driver": [("driver", {"view": "front"}), ("driver", {"view": "q", "expr": "still", "head": (0, 14, 0, 0.06)}),
            ("driver", {"view": "q", "expr": "head_lift"}), ("driver", {"view": "side", "expr": "lunge", "arm_n": "claw", "arm_f": "claw_up", "legs": "lunge", "lean": 18}),
            ("driver", {"view": "q", "expr": "bite", "arm_n": "claw", "arm_f": "claw"}), ("driver", {"view": "back"})],
}
def sheet(name, ppd=150):
    ims = []
    if name == "extras":
        items = [(sp, {"view": "front" if i % 2 == 0 else "q"}) for i, sp in enumerate(draw8.extras(10, 0))]
    else:
        items = SETS[name]
    for spec, pose in items:
        fig = draw8.build(spec, pose)
        cv = draw8.canvas_for(fig["spec"], 0.6)
        p = raster8.flat_png(fig, cv, ppd, None, bg="#fdf3e8")
        ims.append(Image.open(p).convert("RGB"))
    W = sum(i.width for i in ims); H = max(i.height for i in ims)
    s = Image.new("RGB", (W, H), "#fdf3e8"); x = 0
    for i in ims: s.paste(i, (x, H - i.height)); x += i.width
    out = os.path.join(HERE, "tmp", "flat", "audit_%s.png" % name); s.save(out); print(out, s.size)
SHEET_POSE = {"kong": ("kong", {"view": "front", "s": 1, "arm_r": dict(hand=(0.26, 0.90), hand_shape="grip"),
                                 "prop_r": {"type": "cutter", "bars": 3, "angle": -20}, "legs": "wide"}),
              "james": ("crew", {"view": "front", "s": 1, "expr": "neutral"}),
              "tos": ("driver", {"view": "front", "s": 1, "expr": "still"})}


def sbs(Hh=700, ppd=190):
    """side_by_side.png: character sheet crop | our flat drawing (what flat mode puts on the cards), same total height."""
    import numpy as np
    from PIL import ImageDraw, ImageFont
    PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
    font = lambda z: ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), z)
    bg = np.array([253, 243, 232])
    def crop(im):
        arr = np.asarray(im).astype(int); m = np.abs(arr - bg).sum(-1) > 28
        m[:, m.mean(0) > 0.97] = False                # a full-height column is a canvas edge, not the figure
        ys, xs = np.nonzero(m)
        im = im.crop((max(0, xs.min() - 8), ys.min(), xs.max() + 9, ys.max() + 1))
        return im.resize((int(im.width * Hh / im.height), Hh), Image.LANCZOS)
    tiles = []
    for ref, l1, l2 in (("kong", "Kong (sheet)", "Kong (v8, flat cards)"), ("james", "James (sheet)", "crew (v8, neutral)"),
                        ("tos", "Khun Tos (sheet)", "infected driver (v8)")):
        a = crop(Image.open(os.path.join(PROJ, "spec", "sheet_measure", "%s_cut.png" % ref)).convert("RGB"))
        spec, pose = SHEET_POSE[ref]
        fig = draw8.build(spec, pose)
        rb = Image.open(raster8.flat_png(fig, draw8.canvas_for(fig["spec"], 0.8), ppd, None)).convert("RGBA")
        cb = Image.new("RGBA", rb.size, tuple(bg) + (255,)); cb.alpha_composite(rb)
        b = crop(cb.convert("RGB"))
        tiles.append((a, b, l1, l2))
    W = sum(a.width + b.width + 70 for a, b, _, _ in tiles) + 20
    S = Image.new("RGB", (W, Hh + 110), tuple(bg)); d = ImageDraw.Draw(S)
    d.text((14, 10), "Character sheet (left of each pair) vs v8 puppet as drawn on the flat cards (right), same total height %d px" % Hh, fill=(30, 30, 30), font=font(22))
    x = 20
    for a, b, l1, l2 in tiles:
        S.paste(a, (x, 60)); d.text((x, 60 + Hh + 8), l1, fill=(40, 40, 40), font=font(18))
        S.paste(b, (x + a.width + 20, 60)); d.text((x + a.width + 20, 60 + Hh + 8), l2, fill=(40, 40, 40), font=font(18))
        for yy in (60, 60 + Hh - 1): d.line([(x - 4, yy), (x - 4 + a.width + b.width + 32, yy)], fill=(200, 60, 60), width=2)
        x += a.width + b.width + 70
    S.save(os.path.join(HERE, "side_by_side.png")); print("side_by_side.png", S.size)


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["kong", "crew", "driver", "extras"]):
        sbs() if n == "sbs" else sheet(n)
    raster8.close()
