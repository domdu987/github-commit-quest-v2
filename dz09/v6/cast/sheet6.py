"""sheet6.py -- builds lookdev.png: v6 renders next to same-scale ref D crops (head D scaled to our 164 px)
and the character sheet. python3 sheet6.py"""
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out"); TMP = os.path.join(HERE, "tmp")
REF = os.path.join(PROJ, "ref", "d", "frames2")
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
TW, TH = 400, 760          # tile; head centre sits at (200, 230), head D = 164 px
HEAD_Y = 230; OUR_D = 164.0
BG = (24, 24, 28); FG = (236, 232, 222); ACC = (240, 150, 70)


def f(sz): return ImageFont.truetype(FONT, sz)


def tile_from(img, cx, cy, D, label):
    s = OUR_D / D
    im = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    t = Image.new("RGB", (TW, TH), (60, 60, 64))
    t.paste(im, (int(TW / 2 - cx * s), int(HEAD_Y - cy * s)))
    lab(t, label); return t


def lab(t, s):
    d = ImageDraw.Draw(t); w = d.textlength(s, font=f(20))
    d.rectangle([8, TH - 40, 18 + w, TH - 10], fill=(0, 0, 0)); d.text((13, TH - 37), s, font=f(20), fill=FG)


def ours(name, label, head_y=443):
    im = Image.open(os.path.join(OUT, name)).convert("RGB")
    t = im.crop((160, head_y - HEAD_Y, 160 + TW, head_y - HEAD_Y + TH)); lab(t, label); return t


def row(tiles, title, gap=8):
    W = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    H = max(t.height for t in tiles) + 52
    r = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(r)
    d.text((0, 6), title, font=f(30), fill=ACC)
    x = 0
    for t in tiles: r.paste(t, (x, 52)); x += t.width + gap
    return r


def main():
    R = lambda n: Image.open(os.path.join(REF, "f_%03d.png" % n)).convert("RGB")
    sheet = Image.open(os.path.join(PROJ, "uploads", "character_sheet.webp")).convert("RGB")
    refs = [tile_from(R(115), 420, 625, 166, "ref f2_115 (D 166)"),
            tile_from(R(32), 137, 570, 150, "ref f2_032 left"),
            tile_from(R(32), 543, 515, 158, "ref f2_032 right"),
            tile_from(R(87), 490, 652, 225, "ref f2_087 (x0.73)"),
            tile_from(R(100), 276, 612, 200, "ref f2_100 walk"),
            tile_from(sheet, 113, 213, 134, "character sheet: Kong")]
    rows = [row(refs, "Reference D (look only) + our character sheet, all scaled to the same head diameter (164 px)")]
    rows.append(row([ours("ld_kong_front.png", "Kong front"), ours("ld_kong_q.png", "Kong 3/4"),
                     ours("ld_kong_side.png", "Kong side"), ours("ld_kong_wet_front.png", "Kong wet, 2 bars"),
                     ours("ld_kong_wet_q.png", "Kong wet 3/4"), ours("ld_kong_night.png", "night check, 1 bar")],
                    "v6 Kong: sphere head + face decal, flat inked spiky hair, jacket bean, matte noodle limbs (720x1280 renders, crop)"))
    rows.append(row([ours("ld_crew_front.png", "crew front"), ours("ld_crew_q.png", "crew 3/4"),
                     ours("ld_crew_side.png", "crew side"), ours("ld_driver_front.png", "driver front"),
                     ours("ld_driver_q.png", "driver 3/4"), ours("ld_driver_side.png", "driver side")],
                    "v6 young crew member + infected driver"))
    dp = []
    for nm, lb in (("driver_seated", "driver seated (still)"), ("driver_head_lift", "head-lift"),
                   ("driver_lunge", "lunge")):
        im = Image.open(os.path.join(OUT, f"ld_{nm}.png")).convert("RGB")
        t = im.crop((160, 300, 160 + TW, 300 + TH)); lab(t, lb); dp.append(t)
    props = Image.open(os.path.join(OUT, "ld_props.png")).convert("RGB")
    pt = props.resize((int(props.width * TH / props.height * 0.75), int(TH * 0.75)))
    pt2 = Image.new("RGB", (pt.width, TH), BG); pt2.paste(pt, (0, 60)); lab(pt2, "cutter 3 / 2 / 1 bars + phone (no ink on props)")
    rows.append(row(dp + [pt2], "Driver poses in a seat stand-in, props"))
    # faces
    faces = []
    import faces6 as F
    for who in ("kong", "crew", "driver"):
        for e in F.EXPRS[who]:
            p = os.path.join(TMP, f"face_{who}_{e}.png")
            if not os.path.exists(p): continue
            t = Image.open(p).convert("RGB").resize((232, 232))
            d = ImageDraw.Draw(t); d.rectangle([4, 204, 8 + d.textlength(f"{who} {e}", font=f(16)), 228], fill=(0, 0, 0))
            d.text((6, 206), f"{who} {e}", font=f(16), fill=FG); faces.append(t)
    r42 = R(42); ft = tile_from(r42, 350, 715, 234, "")
    ft = r42.crop((350 - 160, 715 - 160, 350 + 160, 715 + 160)).resize((232, 232))
    d = ImageDraw.Draw(ft); d.rectangle([4, 204, 150, 228], fill=(0, 0, 0)); d.text((6, 206), "ref f2_042", font=f(16), fill=FG)
    faces = [ft] + faces
    per = 7
    fr = [row(faces[i:i + per], "Swappable face decals (head turned 18 deg: the decal wraps the sphere)" if i == 0 else "")
          for i in range(0, len(faces), per)]
    rows += fr
    W = max(r.width for r in rows) + 40
    H = sum(r.height for r in rows) + 20 * len(rows) + 90
    out = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(out)
    d.text((20, 18), "DEAD ZONE 09 - v6 cast lookdev (ref D construction, character-sheet identity)", font=f(44), fill=FG)
    y = 90
    for r in rows: out.paste(r, (20, y)); y += r.height + 20
    p = os.path.join(HERE, "lookdev.png"); out.save(p); print(p, out.size)


if __name__ == "__main__":
    main()
