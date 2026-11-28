"""sheet7.py -- lookdev.png: per character, the character-sheet crop next to our neutral and night renders
(front / 3/4 / side), all scaled to the same head diameter; then wet, action poses, driver poses, faces, props."""
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out"); TMP = os.path.join(HERE, "tmp")
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
HD = 120.0                 # head diameter in every figure tile (px)
TW, TH = 300, 640          # figure tile; head centre at (TW/2, HY)
HY = 92
BG = (22, 22, 26); FG = (236, 232, 222); ACC = (240, 150, 70)
SHEET = {"kong": (112, 217, 125, "sheet: Kong"), "james": (575, 245, 122, "sheet: James (young face ref)"),
         "tos": (746, 235, 132, "sheet: Khun Tos (office ref)")}


def f(sz): return ImageFont.truetype(FONT, sz)


def lab(t, s, sz=17):
    d = ImageDraw.Draw(t); w = d.textlength(s, font=f(sz))
    d.rectangle([6, t.height - 30, 14 + w, t.height - 6], fill=(0, 0, 0)); d.text((10, t.height - 29), s, font=f(sz), fill=FG)


def tile(img, cx, cy, D, label, bg=(60, 60, 64), tw=TW, th=TH, hy=HY):
    s = HD / D
    im = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    t = Image.new("RGB", (tw, th), bg)
    t.paste(im, (int(tw / 2 - cx * s), int(hy - cy * s)))
    lab(t, label); return t


def ours(name, label, **kw):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        t = Image.new("RGB", (kw.get("tw", TW), kw.get("th", TH)), (40, 20, 20)); lab(t, "missing " + name); return t
    m = json.load(open(p + ".json")); im = Image.open(p).convert("RGB")
    k = im.width / m["W"]          # set renders run at 75 % and are saved upscaled by post
    return tile(im, m["head"][0] * k, m["head"][1] * k, m["D"] * k, label, **kw)


def sheet_tile(key, **kw):
    sh = Image.open(os.path.join(PROJ, "uploads", "character_sheet.webp")).convert("RGB")
    cx, cy, D, label = SHEET[key]
    return tile(sh, cx, cy, D, label, bg=(250, 244, 234), **kw)


def row(tiles, title, gap=6):
    W = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    H = max(t.height for t in tiles) + 44
    r = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(r)
    d.text((0, 6), title, font=f(26), fill=ACC)
    x = 0
    for t in tiles: r.paste(t, (x, 44)); x += t.width + gap
    return r


def main():
    rows = []
    names = {"kong": "Kong", "crew": "crew member", "driver": "infected driver"}
    refs = {"kong": ["kong"], "crew": ["kong", "james"], "driver": ["tos"]}
    for k in ("kong", "crew", "driver"):
        tl = [sheet_tile(r) for r in refs[k]]
        tl += [ours(f"n_{k}_{v}.png", f"neutral {vl}") for v, vl in (("front", "front"), ("q", "3/4"), ("side", "side"))]
        tl += [ours(f"x_{k}_{v}.png", f"night set {vl}") for v, vl in (("front", "front"), ("q", "3/4"), ("side", "side"))]
        rows.append(row(tl, f"{names[k]}: character sheet | v7 3D, neutral light | v7 3D in the v6 expressway set (night, wet, graded) - same head size"))
    tl = [ours("e_kong_wet_front.png", "Kong wet, 2 bars"), ours("e_kong_wet_q.png", "Kong wet 3/4")]
    tl += [ours(f"e_{n}.png", n.replace("_", " ")) for n in ("kong_phone", "kong_shout", "kong_alarmed", "crew_shout", "crew_scared")]
    rows.append(row(tl, "wet variant + action presets (neutral light)"))
    tl = [ours(f"e_{n}.png", n.replace("_", " "), th=560, hy=150) for n in ("driver_seated", "driver_head_lift", "driver_lunge")]
    pp = os.path.join(OUT, "e_props.png")
    if os.path.exists(pp):
        im = Image.open(pp).convert("RGB").resize((800, 450), Image.LANCZOS); t = Image.new("RGB", (800, 560), (60, 60, 64))
        t.paste(im, (0, 55)); lab(t, "cutter 3 / 2 / 1 bars + phone (inked, toon)"); tl.append(t)
    rows.append(row(tl, "driver in a seat stand-in: still / head-lift / lunge; props"))
    import faces7 as F
    ft = []
    for who, ex in F.EXPRS.items():
        for e in ex:
            p = os.path.join(TMP, f"face_{who}_{e}.png")
            if not os.path.exists(p): continue
            t = Image.open(p).convert("RGB").resize((200, 200), Image.LANCZOS)
            t2 = Image.new("RGB", (200, 232), (60, 60, 64)); t2.paste(t, (0, 0)); lab(t2, f"{who} {e}", 14); ft.append(t2)
    if ft:
        rows.append(row(ft[:7], "swappable face decals (head turned 16 deg: the decal wraps the sphere)"))
        rows.append(row(ft[7:], ""))
    W = max(r.width for r in rows) + 40
    H = sum(r.height for r in rows) + 20 * len(rows) + 80
    S = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(S)
    d.text((20, 18), "DEAD ZONE 09 - v7 cast lookdev: the character sheet built in 3D (toon + ink, real volumes)", font=f(34), fill=FG)
    y = 80
    for r in rows: S.paste(r, (20, y)); y += r.height + 20
    S.save(os.path.join(HERE, "lookdev.png")); print("lookdev.png", S.size)


if __name__ == "__main__":
    main()
