#!/usr/bin/env python3
"""sheet14.py -- builds film/v3/cast14/sheet.jpg (called by test_cast14.py sheet).  Temp files only in cast14/tmp/."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast14 as C   # noqa: E402
import puppet as P   # noqa: E402
from PIL import Image  # noqa: E402

TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
BG, GROUND, LINE = "#d9d5cf", "#b9b3aa", "#8a847c"
FONT = "DejaVu Sans, sans-serif"


def label(x, y, text, size=14, w=None):
    w = w or (0.60 * size * len(text) + 12)
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.86"/>'
            '<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>' % (x - w / 2, y - size - 3, w, size + 9, x, y + 1, FONT, size, text))


def title(x, y, text, size=20):
    return '<text x="%d" y="%d" font-family="%s" font-size="%d" font-weight="bold" fill="#2e2a2c">%s</text>' % (x, y, FONT, size, text)


def fig(cast, pose, uid, D, x, y, shadow=True):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = ""
    if shadow and cast not in ("bee", "swarm"):
        s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(0.9 if cast in C.PEOPLE14 else 4.0, uid + "s"))
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def raster(svg, W, H, name):
    sp = os.path.join(TMP, name + ".svg")
    open(sp, "w").write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, svg))
    out = os.path.join(TMP, name + ".png")
    P._raster(sp, out, W, H, 1)
    os.remove(sp)
    return out


def sec_scale(D=64):
    """the scale row: farmer 1.75 m, uncle, matriarch 3.3 m at the shoulder, with a metre ruler; then the rest of the herd and villagers."""
    W = 2000
    top = 80
    ground = top + int(6.9 * D)
    H = ground + 120
    o = ['<rect width="%d" height="%d" fill="%s"/><rect y="%d" width="%d" height="%d" fill="%s"/>' % (W, H, BG, ground - 6, W, H, GROUND)]
    o.append(title(16, 34, "cast14: scale row (head D = 1; farmer 1.75 m = 3.0 D; elephant shoulder 3.3 m = 5.66 D; 1 m = %.2f D)" % (1 / C.M_PER_D)))
    # ruler in metres on the left
    for m in range(0, 5):
        y = ground - m / C.M_PER_D * D
        o.append('<path d="M10,%.1f L38,%.1f" stroke="%s" stroke-width="2"/><text x="44" y="%.1f" font-family="%s" font-size="13" fill="#2e2a2c">%d m</text>' % (y, y, LINE, y + 5, FONT, m))
    row = [("farmer14", dict(expr="happy", yaw=0.0), "farmer 1.75 m", 190), ("uncle14", dict(expr="smug", arm_r="akimbo", arm_l="akimbo"), "uncle 1.8 m", 320),
           ("matriarch", dict(expr="calm"), "matriarch (shoulder 3.3 m)", 690), ("elephant_c", dict(expr="calm"), "elephant_c", 1340), ("calf", dict(expr="happy"), "calf (1.2 m)", 1750)]
    for i, (c, p, lb, x) in enumerate(row):
        s, f = fig(c, p, "sc%d" % i, D, x, ground)
        o.append(s)
        o.append(label(x, ground + 36, lb))
    # shoulder line of the matriarch
    sh = ground - 3.3 / C.M_PER_D * D
    o.append('<path d="M40,%.1f L%d,%.1f" stroke="#c0392b" stroke-width="1" stroke-dasharray="6 5"/><text x="%d" y="%.1f" font-family="%s" font-size="12" fill="#c0392b" text-anchor="end">3.3 m</text>' % (sh, W - 10, sh, W - 14, sh - 4, FONT))
    sh = ground - 1.75 / C.M_PER_D * D
    o.append('<path d="M40,%.1f L%d,%.1f" stroke="#2c7a4b" stroke-width="1" stroke-dasharray="6 5"/><text x="%d" y="%.1f" font-family="%s" font-size="12" fill="#2c7a4b" text-anchor="end">1.75 m</text>' % (sh, W - 10, sh, W - 14, sh - 4, FONT))
    return raster("".join(o), W, H, "sec_scale")


def grid(items, D, cw, ch, cols, top_pad, ground_frac, name, heading, W=None, scene_label_size=13):
    W = W or int(cols * cw)
    rows = (len(items) + cols - 1) // cols
    H = int(rows * ch + 50)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), title(16, 32, heading)]
    for i, (lb, c, p) in enumerate(items):
        x = (i % cols) * cw + cw / 2
        y0 = 50 + (i // cols) * ch
        g = y0 + ch * ground_frac
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="0.6"/>' % ((i % cols) * cw, g - 4, cw, ch * (1 - ground_frac) + 4, GROUND))
        s, f = fig(c, p, "g%d" % i, D, x, g)
        o.append(s)
        if p.get("lipsync_flag"):
            pass
        o.append(label(x, y0 + ch - 12, lb, scene_label_size))
    return raster("".join(o), W, H, name)


def sec_people(D=62):
    names = [n for n, (c, p) in C.STORY14.items() if c in C.PEOPLE14]
    items = []
    for n in names:
        c, p = C.STORY14[n]
        p = dict(p)
        if C.STORY14_META[n].get("lipsync") or n in C.LIPSYNC14:
            lb = n.replace("villager_", "v_") + " [lip-sync]"
        else:
            lb = n.replace("villager_", "v_")
        items.append((lb, c, p))
    return grid(items, D, 300, int(4.9 * D) + 60, 6, 0, 0.88, "sec_people", "People: every STORY14 pose (stool poses show the stool; lip-sync poses marked)", W=1800, scene_label_size=12)


def sec_elephants(D=34):
    names = [n for n, (c, p) in C.STORY14.items() if c in C.ELEPHANTS]
    items = []
    for n in names:
        c, p = C.STORY14[n]
        items.append((n, c, dict(p)))
    return grid(items, D, 7.8 * D * 1.5, 7.6 * D + 60, 5, 0, 0.90, "sec_eleph", "Elephants: walk (phase 0.10), stand, flee (run gait), trumpet, ears flared + turn + calm (front view), push, sniff", W=int(5 * 7.8 * D * 1.5), scene_label_size=12)


def sec_walk(D=24):
    """walk cycle strips: matriarch 8 phases (two rows of four), farmer and uncle."""
    W = 1800
    o = []
    H = 1000
    o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG))
    o.append(title(16, 28, "cycle(): walk strips (phases 0 .. 7/8); elephants D = %d px, people D = 62 px" % D))
    for row in range(2):
        base = 60 + 6.6 * D + row * (6.6 * D + 50)
        o.append('<rect y="%.1f" width="%d" height="10" fill="%s"/>' % (base - 4, W, GROUND))
        for j in range(4):
            i = row * 4 + j
            c, p = "matriarch", C.cycle("matriarch", i / 8.0, "walk", base=dict(expr="calm", trunk="sniff"))
            x = 270 + j * 440
            s, f = fig(c, p, "w%d" % i, D, x, base, shadow=False)
            o.append(s)
            o.append(label(x, base + 28, "matriarch ph %.3f" % (i / 8.0), 12))
    base2 = 60 + 2 * (6.6 * D + 50) + 3.4 * 62 + 30
    D2 = 62
    o.append('<rect y="%.1f" width="%d" height="10" fill="%s"/>' % (base2 - 4, W, GROUND))
    for i in range(8):
        cst = "farmer14" if i < 4 else "uncle14"
        ph = (i % 4) / 4.0 + 0.1
        p = C.cycle(cst, ph, "walk", base=dict(expr="happy" if cst == "farmer14" else "smug", prop_r=dict(type="stick14", angle=80) if cst == "uncle14" else None), arms="l")
        if p.get("prop_r") is None:
            p.pop("prop_r", None)
        s, f = fig(cst, p, "x%d" % i, D2, 120 + i * 220, base2, shadow=False)
        o.append(s)
        o.append(label(120 + i * 220, base2 + 30, "%s ph %.2f" % (cst[:5], ph), 12))
    H = int(base2 + 70)
    return raster("".join(o).replace('height="1000"', 'height="%d"' % H, 1), W, H, "sec_walk")


def sec_creatures(D=80):
    W = 1800
    H = 760
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), title(16, 30, "Bees, swarm, props (hammer is film 2's; the other props are cast14's)")]
    x = 90
    for i, (lb, c, p, DD) in enumerate((("bee_fly", "bee", dict(t=0.1, angle=-8, size=0.6), 160), ("bee t=0.35", "bee", dict(t=0.35, angle=10, size=0.6), 160),
                                       ("bee_rest", "bee", dict(rest=1.0, size=0.6), 160), ("bee real-size card 0.2 D", "bee", dict(t=0.2), 160))):
        s, f = fig(c, p, "b%d" % i, DD, x + i * 190, 150, shadow=False)
        o.append(s)
        o.append(label(x + i * 190, 215, lb, 12))
    sw = [("swarm_cloud", dict(n=48, radius=1.1, shape="cloud", seed=3.0, t=0.2)), ("swarm_burst", dict(n=70, radius=0.8, shape="stream", seed=5.0, t=0.4, length=3.6, angle=-35)),
          ("swarm_column", dict(n=60, radius=0.8, shape="column", seed=7.0, t=0.3, length=3.2)), ("swarm ring", dict(n=24, radius=1.0, shape="ring", seed=2.0, t=0.5))]
    for i, (lb, p) in enumerate(sw):
        s, f = fig("swarm", p, "sw%d" % i, 80, 900 + i * 230, 230 if i in (0, 3) else 330, shadow=False)
        o.append(s)
        o.append(label(900 + i * 230, 360, lb, 12))
    # props, on a ground
    gy = 660
    o.append('<rect y="%d" width="%d" height="%d" fill="%s"/>' % (gy, W, H - gy, GROUND))
    props = [("tophive (hung)", C.tophive_svg("p1"), 150, 330, 150), ("hive box (empty)", C.hivebox_svg("p2"), 150, 330, 150),
             ("wire coil", C.wirecoil_svg("p3"), 230, 380, 230), ("torch", C.torch_svg("p4", 0.2), 230, 530, 230), ("pot", C.pot_svg("p5"), 230, 550, 230), ("spoon", C.spoon_svg("p6"), 150, 600, 150),
             ("walking stick", C.stick_svg("p7"), 140, 750, 140)]
    # scale each prop so that all share one D
    DP = 150
    pos = [(150, 500), (410, 500), (640, 440), (700, 500), (1100, 500), (1260, 500), (1530, 500)]
    for (lb, svg, *_r), (px, py) in zip(props, pos):
        o.append('<g transform="translate(%d %d) scale(%d)">%s</g>' % (px, py, DP, svg))
        o.append(label(px + (20 if lb.startswith(("walking", "torch", "spoon")) else 0) + (60 if lb == 'torch' else 0), 630, lb, 12))
    o.append('<g transform="translate(1600 330) scale(%d) rotate(100) ">%s</g>' % (DP, ""))
    return raster("".join(o), W, H, "sec_creatures")


def head_clip(uid, x, y, D, svg, w=1.6):
    """show only the head and shoulders of a figure placed with its head centre at (x, y)."""
    return ('<clipPath id="%s_hcl"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath><g clip-path="url(#%s_hcl)"><g transform="translate(%d %d) scale(%d)">%s</g></g>'
            % (uid, x - w / 2 * D, y - 0.95 * D, w * D, 3.0 * D, uid, x, y, D, svg))


def sec_faces(D=120):
    W = 1800
    H = 1540
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    o.append(title(16, 30, "Faces: uncle nose_swell 0, .2, .4, .6, .8, 1 (the comic sting) and the uncle's lip-sync mouths; village faces; elephant expressions"))
    for i, n in enumerate((0.0, 0.2, 0.4, 0.6, 0.8, 1.0)):
        f = P.figure("uncle14", dict(expr="shocked", mouth="o" if n > 0.1 else "smirk", yaw=0.2, nose_swell=n, gaze=(0, 0.6) if n > 0.1 else 0, t=0.3), "n%d" % i)
        o.append(head_clip("n%d" % i, 100 + i * 190, 160, D, f["svg"]))
        o.append(label(100 + i * 190, 300, "nose_swell %.1f" % n, 12))
    for i, m in enumerate(["flat", "talk_a", "talk_b", "talk_o"]):
        f = P.figure("uncle14", dict(expr="smug", mouth=m, yaw=0.4, pitch=-0.2), "m%d" % i)
        o.append(head_clip("m%d" % i, 1290 + i * 150, 160, D, f["svg"]))
        o.append(label(1290 + i * 150, 300, "uncle " + m, 12))
    people = [("farmer14", "happy"), ("farmer14", "determined"), ("farmer14", "stunned"), ("woman14", "laughing"), ("kid14", "laughing"), ("oldman14", "laughing"), ("youth14", "shouting"), ("uncle14", "laughing")]
    for i, (c, ex) in enumerate(people):
        f = P.figure(c, dict(expr=ex, yaw=0.3), "pf%d" % i)
        o.append(head_clip("pf%d" % i, 100 + i * 215, 560, D, f["svg"], 1.7))
        o.append(label(100 + i * 215, 700, "%s %s" % (c[:-2], ex), 12))
    exs = ["calm", "happy", "curious", "alarmed", "trumpet", "shut", "grumpy", "calf happy"]
    for i, ex in enumerate(exs):
        r, cc = divmod(i, 4)
        e = ex.split()[-1]
        p = dict(view="side", expr=e, mouth_open=1.0 if e == "trumpet" else 0.0, trunk="raised" if e == "trumpet" else "hang", ear_flare=0.6 if e in ("alarmed", "trumpet") else 0.0)
        cast = "calf" if ex.startswith("calf") else "matriarch"
        DD = 56 if cast == "matriarch" else 80
        f = P.figure(cast, p, "ee%d" % i)
        gy = 1090 + r * 330
        x = 120 + cc * 440
        cy = gy - 150
        if cast == "calf":
            cy = gy - 110
        o.append('<clipPath id="ecl%d"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (i, x - 0.9 * DD, cy - 1.7 * DD, 4.4 * DD, 3.7 * DD))
        o.append('<g clip-path="url(#ecl%d)"><g transform="translate(%.1f %.1f) scale(%d)">%s</g></g>' % (i, x, cy, DD, f["svg"]))
        o.append(label(x + 1.6 * DD, cy + 2.2 * DD + 14, "%s %s" % (cast, e), 12))
    return raster("".join(o), W, H, "sec_faces")


def build():
    secs = [sec_scale(), sec_people(), sec_elephants(), sec_walk(), sec_creatures(), sec_faces()]
    ims = [Image.open(s).convert("RGB") for s in secs]
    W = max(i.width for i in ims)
    H = sum(i.height + 6 for i in ims)
    out = Image.new("RGB", (W, H), (60, 56, 60))
    y = 0
    for im in ims:
        out.paste(im, (0, y))
        y += im.height + 6
    p = os.path.join(HERE, "sheet.jpg")
    out.save(p, quality=90)
    print("wrote", p, out.size)


if __name__ == "__main__":
    build()
