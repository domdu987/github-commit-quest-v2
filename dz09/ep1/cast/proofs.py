"""proofs.py -- side_by_side.png, lookdev.png, crowd.png (flat drawings on the sheet's paper; no Cycles).
python3 proofs.py sbs | lookdev | crowd | all"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rast9 as R, draw9 as D9, draw8 as D
PROJ = R.PROJ
PAPER = (253, 243, 232)
NIGHT = (22, 28, 46)
MINW = 132
FONT = os.path.join(PROJ, "fonts")


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def fig_img(spec, pose, h_px=None, ppd=150, bg=PAPER, pad=6):
    im = R.crop(R.flat(spec, pose, ppd)[0], pad)
    pil = R.over(bg, im)
    if h_px:
        pil = pil.resize((max(1, round(pil.width * h_px / pil.height)), h_px), Image.LANCZOS)
    return pil


def row(cells, gap=14, bg=PAPER, label_h=34, fsz=15, valign="bottom"):
    """cells: list of (PIL image, label)."""
    H = max(c[0].height for c in cells)
    fo = font(fsz)
    # checker: a cell is at least as wide as its label, so labels no longer run into the next cell
    wid = [max(c[0].width, MINW, max(int(fo.getlength(ln)) for ln in str(c[1]).split("\n")) + 6) for c in cells]
    W = sum(wid) + gap * (len(cells) + 1)
    out = Image.new("RGB", (W, H + label_h), bg)
    d = ImageDraw.Draw(out); x = gap
    for (im, lab), cw in zip(cells, wid):
        out.paste(im, (x, H - im.height if valign == "bottom" else 0))
        col = (40, 40, 40) if sum(bg) > 380 else (230, 230, 230)
        for k, ln in enumerate(str(lab).split("\n")):
            d.text((x, H + 2 + k * (fsz + 1)), ln, fill=col, font=fo)
        x += cw + gap
    return out


def stack(rows, bg=PAPER, title=None, gap=10):
    W = max(r.width for r in rows)
    th = 40 if title else 0
    H = sum(r.height for r in rows) + gap * (len(rows) + 1) + th
    out = Image.new("RGB", (W, H), bg)
    y = gap + th
    if title:
        ImageDraw.Draw(out).text((14, 8), title, fill=(40, 40, 40) if sum(bg) > 380 else (235, 235, 235), font=font(24))
    for r in rows:
        if r.mode == "RGB" and r.getpixel((0, 0)) != bg:
            pass
        out.paste(r, (0, y)); y += r.height + gap
    return out


SHEET_BOX = {"kong": (4, 130, 197, 677), "praew": (334, 177, 500, 677), "james": (490, 150, 685, 677), "tos": (676, 166, 830, 676)}


def sbs():
    sheet = Image.open(os.path.join(PROJ, "uploads", "character_sheet.webp")).convert("RGB")
    Hh = 760
    cells = []
    def ref(name):
        c = sheet.crop(SHEET_BOX[name])
        return c.resize((round(c.width * Hh / c.height), Hh), Image.LANCZOS)
    def ours(spec, pose, frac=1.0):
        return fig_img(spec, pose, h_px=round(Hh * frac), ppd=260)
    # Praew: sheet figure 179..675 of the crop 177..677 -> our figure fills 0.992 of the crop height
    cells += [(ref("praew"), "sheet: Dr. Praew"), (ours("praew", dict(view="front", s=1, expr="calm", arm_r=dict(hand=(-0.05, 0.98), elbow=None), prop_r=dict(type="medbag"),
                                                                 arm_l=dict(hand=(-0.42, 0.62), elbow=None)), 0.985), "ours: praew (calm)\n+ small red pouch"),
              (ours("praew_wet", dict(view="q", s=1, expr="focused"), 0.985), "praew_wet, 3/4\nfocused")]
    cells += [(ref("tos"), "sheet: Khun Tos"), (ours("tos", D9.poses("tos", "tos_cross", view="front"), 0.99), "ours: tos\narms crossed"),
              (ours("tos_torn", D9.poses("tos_torn", "tos_cross", view="q", s=-1, expr="evasive"), 0.99), "tos_torn, 3/4\nevasive, holds the cuff"),
              (ours("driver", dict(view="front", expr="head_lift"), 0.99), "NOT Tos: the infected\ndriver (hook)")]
    cells += [(ref("james"), "sheet: James"), (ours("james", dict(view="front", s=1, expr="cheerful", arm_l=dict(hand=(0.62, -0.20), elbow=1, hand_shape="point"),
                                                              arm_r="carry", prop_r=dict(type="helmet9")), 0.93), "ours: james (bare head,\nhelmet carried; no box)"),
              (ours("james_wet", dict(view="q", s=1, expr="urgent", arm_n="point"), 0.90), "james_wet: EP.1 look,\nhelmet on, visor up")]
    cells += [(ours("crew_wet", dict(view="front", expr="neutral")), "hook: the junior\n(crew_wet)"),
              (ours("crew_bitten", dict(dict(view="q", s=-1, expr="pain"), **D9.press_wound("q", -1))), "crew_bitten\nhand on the bite"),
              (ours("crew_infected", dict(view="q", s=-1, expr="snap_open", arm_n="claw", arm_f="hang")), "crew_infected")]
    r = row(cells, gap=18, label_h=46, fsz=17)
    out = stack([r], title="DEAD ZONE 09 EP.1 cast: the user's sheet (left of each group) beside the code-drawn puppet, same height")
    out.save(os.path.join(HERE, "side_by_side.png")); print("side_by_side", out.size)


def lookdev():
    rows = []
    h = 300
    def cell(spec, pose, lab, hh=h, bg=PAPER):
        return (fig_img(spec, pose, h_px=hh, ppd=150, bg=bg), lab)
    def head(spec, pose, lab, ppd=230):
        im, cv, fig = R.flat(spec, pose, ppd)
        hc = fig["anchors"]["head"]
        x = (hc[0] - cv[0]) * ppd; y = (hc[1] - cv[1]) * ppd; r = 0.92 * ppd
        c = R.over(PAPER, im[int(max(0, y - r)):int(y + r * 0.86), int(max(0, x - r)):int(x + r)])
        return (c.resize((150, round(150 * c.height / c.width)), Image.LANCZOS), lab)
    # 1 Praew
    rows.append(row([cell("praew_wet", dict(view="front", expr=e), e) for e in ("focused", "alarmed", "shouting", "doubtful")] +
                    [cell("praew_wet", dict(view="q", s=-1, expr="focused", arm_n=dict(hand=(0.1, 0.95), elbow=None), prop_n=dict(type="medbag")), "3/4 + pouch"),
                     cell("praew_wet", dict(view="side", s=1, expr="alarmed"), "side"), cell("praew", dict(view="back"), "back (dry)"),
                     cell("praew", dict(view="front", expr="calm"), "dry, calm")] +
                    [head("praew_wet", dict(view="front", expr="focused", mouth=m, blink=b), "mouth %.1f blink %d" % (m, b)) for m, b in ((0.0, 0), (0.3, 0), (0.6, 1), (1.0, 2))]))
    # 2 Tos
    rows.append(row([cell("tos_wet", dict(view="front", expr=e), e) for e in ("arrogant", "panicked", "shouting", "evasive")] +
                    [cell("tos_wet", D9.poses("tos_wet", "tos_cross", view="front"), "jacket intact\n(scene 03)"),
                     cell("tos_torn", D9.poses("tos_torn", "tos_cross", view="front", expr="evasive"), "tos_torn: holds\nthe cuff shut"),
                     cell("tos_torn", dict(view="front", expr="panicked", arm_l=dict(hand=(0.35, 0.30), elbow=None, hand_shape="open")), "tos_torn: the tear\n(S111-S112)"),
                     cell("tos_soaked", D9.poses("tos_soaked", "tos_cross", view="q", s=-1, expr="evasive"), "tos_soaked 3/4\n(S120)"),
                     cell("tos_bleed", D9.poses("tos_bleed", "tos_cross", view="front", expr="evasive"), "tos_bleed: drips\n(scene 06)"),
                     cell("tos_bleed", D9.poses("tos_bleed", "tos_cross", view="side", s=-1, expr="panicked"), "side"), cell("tos_wet", dict(view="back"), "back")] +
                    [head("tos_wet", dict(view="front", expr="arrogant", mouth=m, blink=b), "mouth %.1f blink %d" % (m, b)) for m, b in ((0.3, 0), (1.0, 2))]))
    # 3 James
    rows.append(row([cell("james_wet", dict(view="front", expr=e), e) for e in ("cheerful", "terrified", "shouting")] +
                    [cell("james_wet", dict(view="q", s=1, expr="urgent", arm_n="point"), "pointing"),
                     cell("james_wet", dict(view="q", s=-1, expr="terrified", visor="down"), "visor down\n(to S74)"),
                     cell("james_wet", dict(view="side", s=1, expr="shouting", arm_n="shout"), "side"), cell("james_wet", dict(view="back"), "back"),
                     cell("james_bare_wet", dict(view="front", expr="scared", arm_r="carry", prop_r=dict(type="helmet9")), "helmet off\n(not used in EP.1)")] +
                    [head("james_wet", dict(view="front", expr="urgent", mouth=m, blink=b), "mouth %.1f blink %d" % (m, b)) for m, b in ((0.0, 0), (0.3, 0), (0.6, 1), (1.0, 2))]))
    # 4 junior
    pw = lambda v, s_: D9.press_wound(v, s_)
    rows.append(row([cell("crew_bitten", dict(view="front", expr="scared", mouth=("o", 0.8)), "crew_bitten\nwound open"),
                     cell("crew_bitten", dict(dict(view="front", expr="pain"), **pw("front", 1)), "hand pressed"),
                     cell("crew_treated", dict(dict(view="q", s=-1, expr="pain"), **pw("q", -1)), "3/4, gauze under\nthe hand"),
                     cell("crew_treated", dict(view="q", s=-1, expr="pain"), "crew_treated\ngauze"),
                     cell("crew_grey1", D9.poses("crew_grey1", "sit_wheel", s=-1, slump=0.2), "sit, grey 1\nshivering (S37)", 250),
                     cell("crew_grey2", D9.poses("crew_grey2", "sit_wheel", s=-1, slump=0.5, expr="fading"), "grey 2 (S38)", 250),
                     cell("crew_dying", dict(D9.poses("crew_dying", "sit_wheel", s=-1, slump=1.0, limp=True), blink=2), "crew_dying\neyes shut (S42)", 250),
                     cell("crew_bitten", dict(view="q", s=1, expr="pain"), "facing right:\nwound on far side")] +
                    [head("crew_dying", dict(view="q", s=-1, expr="fading", blink=b), "eyes closing %d" % b) for b in (0, 1, 2)]))
    rows.append(row([cell("crew_infected", dict(view="front", expr=e, arm_r=a, arm_l=b), lab) for e, a, b, lab in
                     (("snap_open", "hang", "hang", "eyes snap open"), ("searching", "hang", "claw", "searching"), ("lunging", "claw_up", "claw", "lunging"))] +
                    [cell("crew_infected", dict(view="q", s=-1, expr="lunging", legs="lunge", lean=24, arm_n="claw", arm_f="claw_up"), "lunge 3/4"),
                     cell("crew_infected", dict(view="side", s=1, expr="searching", head=(0, -8, 0, 0)), "side"), cell("crew_infected", dict(view="back"), "back"),
                     cell("crew_infected", D9.poses("crew_infected", "bang_glass", s=1), "bang on glass")] +
                    [head("crew_infected", dict(view="front", expr=e), e, 260) for e in ("snap_open", "searching", "lunging")] +
                    [head("crew_wet", dict(view="front", expr="neutral"), "(hook: alive)", 260)]))
    # 5 Kong kit
    K2, K4, K6 = "kong_ep1_02", "kong_ep1_04", "kong_ep1_06b"
    rows.append(row([cell("kong_ep1_clean", dict(view="front", expr="serious", arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True)), "S26: watch on the\nleft wrist"),
                     cell(K2, dict(view="front", expr="grief", arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True)), "from S35: blood on\ngloves, right forearm"),
                     cell(K4, dict(view="front", expr="serious", arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True),
                                   arm_l=dict(hand=(0.10, 0.95), elbow=None), prop_l=dict(type="medbag")), "scene 04 set: cutter,\ncrowbar on pack,\nradio, red pouch"),
                     cell(K4, dict(view="q", s=1, expr="serious", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True)), "3/4"),
                     cell(K4, dict(view="back"), "back: hook over\nthe left shoulder"),
                     cell(K4, D9.poses(K4, "phone_chest"), "phone glowing,\nhidden on the chest"),
                     cell(K4, dict(view="q", s=1, expr="shouting", arm_n=dict(hand=(0.55, -0.65), elbow=None, hand_shape="grip"), prop_n=dict(type="flare", lit=True, angle=20), arm_f="down"), "flare, lit"),
                     cell(K4, dict(view="q", s=1, expr="serious", arm_n=dict(hand=(0.30, 0.55), elbow=None, hand_shape="grip"), prop_n=dict(type="flare", lit=False, angle=-70), arm_f="down"), "flare, unlit"),
                     cell(K6, dict(view="q", s=1, expr="resolve", lean=-4, arm_n=dict(hand=(-0.30, -0.92), elbow=None, hand_shape="grip"), prop_n=dict(type="crowbar", angle=200),
                                   arm_f=dict(hand=(-0.12, -0.84), elbow=None, hand_shape="grip"), z={"arm_f": 2.4}), "crowbar raised\n(S161)", 360),
                     cell(K4, D9.poses(K4, "crouch_hide", s=1), "crouch-hide, glove\nover the mouth")]))
    # 6 props + watch + guard
    def prop_cell(kind, lab, w=150, **kw):
        fr = D9.prop9(kind, dict(dict(at=(0, 0), angle=0.0), **kw))
        im = R.crop(R.svg_png(fr, (-1.1, -1.1, 1.1, 1.9), 150), 8)
        return (R.over(PAPER, im), lab)
    def watch_cell(sec, lab, **kw):
        im = R.svg_png(D9.watch_svg(sec, **kw), (-1.35, -1.0, 1.35, 1.0), 110)
        return (R.over((60, 60, 64), im), lab)
    bars = fig_img("guard", dict(view="front", expr="wary", arm_r=dict(hand=(-0.05, 0.9), elbow=None, hand_shape="grip"), prop_r=dict(type="torch")), h_px=h, ppd=150, bg=NIGHT)
    gs = R.crop(R.flat("guard", dict(view="q", s=-1, expr="shouting", arm_n=dict(hand=(0.05, 0.9), elbow=None, hand_shape="grip"), prop_n=dict(type="torch")), 150)[0], 6)
    sil = R.over((70, 84, 110), R.silhouette(gs, (12, 15, 24), rim=((150, 170, 205), 2)))
    sil = sil.resize((round(sil.width * h / sil.height), h), Image.LANCZOS)
    for im_ in (bars, sil):
        d = ImageDraw.Draw(im_)
        for x in range(8, im_.width, 34):
            d.rectangle([x, 0, x + 7, im_.height], fill=(8, 9, 12))
        d.rectangle([0, 40, im_.width, 48], fill=(8, 9, 12)); d.rectangle([0, im_.height - 60, im_.width, im_.height - 52], fill=(8, 9, 12))
    rows.append(row([watch_cell(10.5, "watch insert S26\nhand at the 2"), watch_cell(30.5, "S36: at the 6,\nblood smear", smear=True), watch_cell(49.5, "S44: passing 10", smear=True),
                     watch_cell(57.0, "S47: touching\nthe blood", smear=True),
                     prop_cell("crowbar", "crowbar"), prop_cell("medbag", "red pouch,\nwrist loop"), prop_cell("flare", "flare unlit"),
                     prop_cell("flare", "flare lit", lit=True), prop_cell("torch", "torch (off)"), prop_cell("helmet9", "helmet"),
                     prop_cell("gauze", "gauze, soaked", soak=0.9),
                     (fig_img("guard", dict(view="front", expr="wary"), h_px=h, ppd=150), "guard (lit, for\nreference)"), (bars, "guard behind bars"),
                     (sil, "guard silhouette\n(as staged, S136+)")], label_h=52))
    cab = lambda sp, role, lab, **kw: cell(sp, D9.poses(sp, "seated_cab", role=role, **kw), lab, 230)
    rows.append(row([cab("kong_ep1_03", "driver", "cab: Kong drives\n(right-hand drive)", expr="serious"), cab("james_wet", "front", "James, front seat", expr="terrified"),
                     cab("praew_wet", "rear", "Praew, rear bench", expr="alarmed"), cab("tos_wet", "rear", "Tos, rear bench", expr="panicked"),
                     cab("kong_ep1_03", "driver", "driver, 3/4", view="q", s=1, expr="shouting"), cab("praew_wet", "rear", "passenger, 3/4", view="q", s=-1, expr="focused"),
                     cell("tos_wet", D9.poses("tos_wet", "pulled", s=1), "Tos 'pulled' pose\n(card is rolled 80 deg\non stage)", 300),
                     cell("kong_ep1_03", D9.poses("kong_ep1_03", "pull", s=-1), "Kong pulling", 300),
                     cell("crew_treated", D9.poses("crew_treated", "sit_wheel", s=1, slump=0.2), "sit, facing right", 230)], label_h=62))
    out = stack(rows, title="EP.1 cast lookdev: expressions, variants, props (flat drawings on the sheet's paper)")
    out.save(os.path.join(HERE, "lookdev.png")); print("lookdev", out.size)


def crowd():
    specs = D9.infected_crowd(14)
    sig = D9.check_unique9(specs)
    h = 330
    cells = []
    for i, sp in enumerate(specs):
        v, s_ = ("front", 1) if i % 3 == 0 else ("q", 1 if i % 2 else -1)
        ep = sp["extra_pose"]
        pose = dict(view=v, s=s_, expr=sp["default_expr"])
        pose.update(ep if v == "front" else dict(arm_n=ep["arm_r"], arm_f=ep["arm_l"]))
        if i % 4 == 1:
            pose.update(legs="lunge", lean=18)
        cells.append((fig_img(sp, pose, h_px=round(h * (sp["legs"] + sp["torso"] + 1.15) / 4.45), ppd=150), "%02d %s" % (i, sp["role"].replace(", ", "\n", 1))))
    r1 = row(cells[:7], label_h=44, fsz=14); r2 = row(cells[7:], label_h=44, fsz=14)
    # far silhouettes: flat single colour, rim-lit, on a night backdrop
    import gait9
    sc = []
    for k in range(12):
        sp = specs[(k * 5) % 14]
        G = gait9.Sprint(sp, phase=k * 0.17)
        p = G.pose(0.04 * k + 0.11 * (k % 3), s=1 if k % 4 else -1, view="side")
        p.pop("_planted", None)
        im = R.crop(R.flat(sp, p, 60)[0], 3)
        hh = 120 + (k % 3) * 22
        pil = R.over(NIGHT, R.silhouette(im, (7, 9, 15), rim=((120, 140, 180), 1)))
        sc.append((pil.resize((round(pil.width * hh / pil.height), hh), Image.LANCZOS), ""))
    r3 = row(sc, bg=NIGHT, label_h=6)
    cap = Image.new("RGB", (r1.width, 30), PAPER)
    ImageDraw.Draw(cap).text((14, 4), "far silhouettes (stage9.Sil: one flat card each, any infected spec in any sprint phase)", fill=(40, 40, 40), font=font(17))
    out = stack([r1, r2, cap, r3], title="Infected crowd: 14 distinct designs (face, hair, clothes, wounds all differ pairwise: check_unique9 passed)")
    # paste r3 on a night band
    out.save(os.path.join(HERE, "crowd.png")); print("crowd", out.size)
    # pairwise proof
    n = len(specs); S = [D9.signature(s) for s in specs]
    pairs = [(i, j, [k for k in ("face", "hair", "clothes", "wounds") if S[i][k] == S[j][k]]) for i in range(n) for j in range(i + 1, n)]
    bad = [p for p in pairs if p[2]]
    json.dump(dict(n=n, pairs=len(pairs), pairs_sharing_any_key=bad, roles=[s["role"] for s in specs],
                   signatures=[{k: str(v) for k, v in s.items()} for s in S]), open(os.path.join(HERE, "out", "crowd_unique.json"), "w"), indent=1)
    print("crowd pairs", len(pairs), "sharing a key:", len(bad))


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    if m in ("sbs", "all"): sbs()
    if m in ("lookdev", "all"): lookdev()
    if m in ("crowd", "all"): crowd()
    R.close()
