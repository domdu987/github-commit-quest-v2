"""cab.py -- the rescue truck's crew cab from INSIDE (set CAB), with the equipment wall behind the rear bench (gear.py).

    R = cab.build(A, at="x2" | "x1" | None)     the cab is parented to the rescue truck's root, so it stands wherever
                                                the truck is and travels with x2.move_truck(); the pickup's exterior is
                                                hidden while the cab is shown (cab.exterior(True) brings it back)
    cab.drive(A, s, o, yaw=0)                   move cab + truck lights along the deck (the two travelling shots)
    cab.switch("siren" | "beacon" | "flood" | "radio", on)    rocker tilts, its LED and its glow light up
    cab.wipers(t)                               t seconds -> both blades (0.9 s per sweep there and back); None parks them
    cab.mirror(k, gain=1)                       wing-mirror plate k = 0, 1, 2: the horde as silhouettes through rain; None = empty road
    cab.crack(level)                            0, 1 (one crack from the corner), 2 (branched) on the rear left side window
    cab.fog(level, win)                         breath fog on a right-hand side window (0..1; "driver" or "rear_right")
    cab.dome(on)   cab.dash(gain)               the roof lamp (off in the film until someone needs it), the instrument glow
    cab.seat(name, actor_legs_bu) -> soles point for a seated puppet (hip on the cushion): "drv", "pas", "rl", "rr"

The cab is sized for four FULL-SIZE seated puppets (2.86 BU figures): interior 3.5 wide, 5.0 long, 3.3 high; that is taller
than the pickup the hook shows from outside, which is why it is only ever seen from inside or through its own windscreen.
Right-hand drive: the driver sits on +X (the median side when the truck heads +s).
"""
import math, random
import bpy
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, tex, hexlin

C = "EP1_CAB"
F = 0.50                    # floor height above the road (a standing figure's head is level with the side glass)
HW = 1.75                   # half inner width
Y0, Y1 = -2.55, 2.45        # equipment wall face .. windscreen base
ZR = F + 3.3                # inner roof
CUSH = F + 0.95             # top of the seat cushions (hip point height)
SEATS = dict(drv=(0.85, 0.55), pas=(-0.85, 0.55), rr=(0.82, -1.55), rl=(-0.82, -1.55))
LIFT = 0.95                 # the truck's beacon lights are raised by this while the cab is shown (they would sit inside it)
OFF_Y = 0.75                # cab origin in the truck's frame
_S = {}


# --------------------------------------------------------------------------------------------------------- textures
ROCKER_OFF, ROCKER_ON = 0.22, 0.65
AMBIENT_W, CONSOLE_W = 48.0, 22.0      # checker: 9 / 9 W left faces and switches unreadable on a phone


def _cluster_tex():
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(4, 6, 8, 255))
        for cx, r, n, col in ((W * 0.30, H * 0.40, 9, (120, 235, 215)), (W * 0.72, H * 0.34, 7, (120, 235, 215))):
            cy = H * 0.52
            d.arc((cx - r, cy - r, cx + r, cy + r), 140, 400, fill=col + (255,), width=6)
            for k in range(n):
                a = math.radians(140 + 260 * k / (n - 1))
                d.line((cx + math.cos(a) * r * 0.80, cy + math.sin(a) * r * 0.80, cx + math.cos(a) * r * 0.97, cy + math.sin(a) * r * 0.97), fill=(230, 245, 240, 255), width=5)
            a = math.radians(170 if cx < W / 2 else 250)
            d.line((cx, cy, cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78), fill=(255, 70, 40, 255), width=7)
            d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(230, 245, 240, 255))
        for k, col in enumerate(((255, 60, 40), (255, 170, 30), (60, 220, 90), (255, 170, 30))):       # warning lamps: plain dots
            d.ellipse((W * 0.42 + k * 26, H * 0.80, W * 0.42 + k * 26 + 16, H * 0.80 + 16), fill=col + (255,))
        for k in range(6):                                                                              # fuel bars
            d.rectangle((W * 0.47 + k * 12, H * 0.16, W * 0.47 + k * 12 + 8, H * 0.28), fill=(120, 235, 215, 255) if k < 4 else (30, 60, 55, 255))
    return K.draw_tex("cab_cluster", (512, 256), fn)


def _label_tex(name, text, fg=(20, 20, 24), bg=(232, 228, 210), size=(256, 96), fs=64, tilt=0.0):
    """a strip of cloth tape with a marker-written word (Thai through raqm, Kanit)."""
    def fn(d, im):
        from PIL import Image, ImageDraw
        W, H = im.size
        t = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(t)
        dd.rounded_rectangle((4, 10, W - 4, H - 10), 6, fill=bg + (255,))
        k = fs                                    # shrink until the word and its vowel / tone marks fit inside the tape
        while True:
            f = K.font(k)
            bb = dd.textbbox((0, 0), text, font=f)
            if (bb[2] - bb[0] <= W - 36 and bb[3] - bb[1] <= H - 30) or k <= 20: break
            k -= 2
        dd.text((W / 2 - (bb[0] + bb[2]) / 2, H / 2 - (bb[1] + bb[3]) / 2), text, font=f, fill=fg + (255,))
        if tilt: t = t.rotate(tilt, resample=Image.BICUBIC)
        return t
    return K.draw_tex("label_" + name, size, fn)


def _radio_tex():
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(10, 12, 14, 255))
        d.rectangle((W * 0.08, H * 0.18, W * 0.62, H * 0.60), fill=(30, 110, 60, 255))
        for k in range(9):
            h = (3, 6, 9, 5, 8, 4, 7, 9, 2)[k]
            d.rectangle((W * 0.12 + k * 26, H * 0.56 - h * 9, W * 0.12 + k * 26 + 16, H * 0.56), fill=(170, 255, 190, 255))
        for k in range(4):
            d.ellipse((W * 0.70 + (k % 2) * 60, H * 0.20 + (k // 2) * 70, W * 0.70 + (k % 2) * 60 + 40, H * 0.20 + (k // 2) * 70 + 40), fill=(60, 64, 70, 255))
        d.ellipse((W * 0.10, H * 0.72, W * 0.10 + 22, H * 0.72 + 22), fill=(255, 60, 40, 255))
    return K.draw_tex("cab_radio", (512, 256), fn)


def _horde_tex(k):
    """wing-mirror plate: the road behind through rain, headlights of the jam as blurred discs, and the horde as
    black upper bodies with raised arms coming between the cars (code-drawn, three variants for on-twos jitter)."""
    def fn(d, im):
        from PIL import Image, ImageDraw, ImageFilter
        import random as rr
        g = rr.Random(100 + k)
        W, H = im.size
        base = Image.new("RGB", (W, H), (6, 10, 26)); bd = ImageDraw.Draw(base)
        for y in range(H):
            t = y / H
            bd.line((0, y, W, y), fill=(int(8 + 10 * t), int(12 + 16 * t), int(30 + 40 * t)))
        glow = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glow)
        for i in range(9):                                   # headlights and hazards of the jam behind
            x = g.randrange(20, W - 20); y = int(H * g.uniform(0.38, 0.62)); r = g.randrange(8, 20)
            col = g.choice(((255, 236, 200), (255, 236, 200), (255, 150, 40), (255, 40, 30)))
            gd.ellipse((x - r, y - r, x + r, y + r), fill=col)
        glow = glow.filter(ImageFilter.GaussianBlur(9))
        base = Image.blend(base, glow, 0.0); base = Image.fromarray(__import__("numpy").clip(__import__("numpy").asarray(base, dtype="int16") + __import__("numpy").asarray(glow, dtype="int16"), 0, 255).astype("uint8"))
        bd = ImageDraw.Draw(base)
        bd.polygon([(0, H), (W, H), (W, H * 0.60), (0, H * 0.66)], fill=(4, 6, 14))             # wet road, dark
        n = 11
        for i in range(n):                                   # the horde: far to near
            t = i / (n - 1)
            x = int(W * (0.12 + 0.76 * ((i * 0.37 + 0.13 * k) % 1.0))) + g.randrange(-8, 9)
            s = 0.45 + 0.9 * t + g.uniform(-0.05, 0.05)
            y = int(H * (0.50 + 0.20 * t)) + (k % 2) * int(3 * s)
            hr = int(15 * s); sh = int(26 * s)
            col = (0, 0, 2)
            bd.ellipse((x - hr, y - hr * 2, x + hr, y), fill=col)
            bd.polygon([(x - sh, y + int(60 * s)), (x - sh, y + int(8 * s)), (x - hr, y - 2), (x + hr, y - 2), (x + sh, y + int(8 * s)), (x + sh, y + int(60 * s))], fill=col)
            for sg in (-1, 1):
                if g.random() < 0.75:
                    ex = x + sg * int((30 + g.uniform(0, 14)) * s); ey = y - int(g.uniform(-6, 40) * s)
                    bd.line((x + sg * sh, y + int(12 * s), ex, ey), fill=col, width=max(3, int(10 * s)))
                    bd.line((ex, ey, ex + sg * int(6 * s), ey - int(26 * s)), fill=col, width=max(3, int(8 * s)))
        rain = ImageDraw.Draw(base)
        for i in range(160):
            x = g.randrange(W); y = g.randrange(H); ln = g.randrange(10, 34)
            rain.line((x, y, x - 3, y + ln), fill=(120, 140, 190), width=1)
        base = base.filter(ImageFilter.GaussianBlur(0.6))
        return base.convert("RGBA")
    return K.draw_tex("cab_horde_%d" % k, (384, 512), fn)


def _road_mirror_tex():
    def fn(d, im):
        W, H = im.size
        for y in range(H):
            t = y / H
            d.line((0, y, W, y), fill=(int(8 + 10 * t), int(12 + 16 * t), int(30 + 40 * t), 255))
        d.polygon([(0, H), (W, H), (W, H * 0.60), (0, H * 0.66)], fill=(4, 6, 14, 255))
        for x, y, col in ((90, 260, (255, 236, 200)), (250, 250, (255, 40, 30)), (180, 270, (255, 150, 40))):
            d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col + (255,))
    return K.draw_tex("cab_mirror_road", (384, 512), fn)


def _fog_tex():
    def fn(d, im):
        from PIL import Image, ImageFilter, ImageDraw
        W, H = im.size
        a = Image.new("L", (W, H), 0); ad = ImageDraw.Draw(a)
        ad.ellipse((W * 0.18, H * 0.22, W * 0.82, H * 0.86), fill=230)
        a = a.filter(ImageFilter.GaussianBlur(38))
        out = Image.new("RGBA", (W, H), (214, 222, 235, 0)); out.putalpha(a)
        return out
    return K.draw_tex("cab_fog", (256, 256), fn)


def _crack_tex(level):
    def fn(d, im):
        import random as rr
        from PIL import ImageFilter
        g = rr.Random(7)
        W, H = im.size

        def run(x, y, ang, ln, w, depth):
            pts = [(x, y)]
            for i in range(int(ln / 22)):
                ang += g.uniform(-0.28, 0.28); x += math.cos(ang) * 22; y += math.sin(ang) * 22; pts.append((x, y))
                if depth and level > 1 and g.random() < 0.28:
                    run(x, y, ang + g.choice((-1, 1)) * g.uniform(0.5, 1.0), ln * 0.45, max(1, w - 1), depth - 1)
            d.line(pts, fill=(235, 242, 255, 255), width=w, joint="curve")
        run(W * 0.94, H * 0.92, math.radians(205), W * 0.85, 4, 2)
        if level > 1:
            run(W * 0.94, H * 0.92, math.radians(250), H * 0.7, 3, 2)
            run(W * 0.94, H * 0.92, math.radians(180), W * 0.5, 3, 1)
            d.ellipse((W * 0.90, H * 0.86, W * 0.99, H * 0.98), fill=(235, 242, 255, 230))
    return K.draw_tex("cab_crack_%d" % level, (512, 512), fn)


# -------------------------------------------------------------------------------------------------------------- build
def _seat(name, x, y, root, c, bench=False, w=1.15):
    sm = K.simple("cab_seat", "#2a2c33", 0.9); sm2 = K.simple("cab_seat_side", "#c8581b", 0.8)
    wd = 3.2 if bench else w
    K.box(name + "_base", (wd * 0.92, 1.0, CUSH - F - 0.28), (x, y, F + (CUSH - F - 0.28) / 2), K.simple("cab_trim_dark", "#141518", 0.7), root, c=c)
    K.box(name + "_cush", (wd, 1.15, 0.28), (x, y + 0.05, CUSH - 0.14), sm, root, bevel=0.08, c=c)
    hb = 0.60 if bench else 1.75
    K.box(name + "_back", (wd, 0.26, hb), (x, y - 0.62, CUSH + hb / 2 - 0.1), sm, root, bevel=0.08, rot=(math.radians(-8), 0, 0), c=c)
    if not bench:
        K.box(name + "_rest", (0.62, 0.20, 0.36), (x, y - 0.80, CUSH + 1.95), sm, root, bevel=0.08, c=c)
        for dx in (-0.14, 0.14): K.cyl(name + "_restpost", 0.02, 0.3, (x + dx, y - 0.78, CUSH + 1.72), V.mat("chrome"), root, c=c, segs=6)
        K.box(name + "_stripe", (0.16, 0.27, hb * 0.8), (x, y - 0.615, CUSH + hb / 2 - 0.1), sm2, root, rot=(math.radians(-8), 0, 0), c=c)
    else:
        for dx in (-0.82, 0.82): K.box(name + "_stripe", (0.16, 0.27, hb * 0.8), (x + dx, y - 0.615, CUSH + hb / 2 - 0.1), sm2, root, rot=(math.radians(-8), 0, 0), c=c)


def build(A, at="x2", with_gear=True):
    c = K.coll(C)
    truck = bpy.data.objects[A["rescue_truck"]]
    root = K.empty("cab_root", (0, OFF_Y, 0), truck, c)
    trim = K.simple("cab_trim", "#23252b", 0.75); dark = K.simple("cab_trim_dark", "#141518", 0.7)
    head = K.simple("cab_headliner", "#4b4f58", 0.95); white = V.paint("pickup", "#e9e9e6")
    rub = V.mat("rubber"); ch = V.mat("chrome"); pl = V.mat("plastic")
    G = K.glass_clear("ep1_glass_wet", wet=True, bump=0.6, scale=2.2)
    G2 = K.glass_clear("ep1_glass_screen", wet=True, bump=0.45, scale=3.0, gloss=0.05)
    P = []
    add = P.append
    T = 0.10
    # floor, mats, tunnel, firewall, roof, outer skin
    add(K.box("cab_floor", (2 * HW + 0.3, Y1 - Y0 + 1.4, 0.10), (0, (Y0 + Y1) / 2 - 0.5, F - 0.05), dark, root, c=c))
    for sx in (-1, 1):
        add(K.box("cab_mat", (1.2, 1.3, 0.03), (sx * 0.85, 1.35, F + 0.015), rub, root, bevel=0.01, c=c))
    add(K.box("cab_tunnel", (0.5, 3.6, 0.42), (0, 0.4, F + 0.21), trim, root, bevel=0.06, c=c))
    add(K.box("cab_roof", (2 * HW + 0.3, Y1 - Y0 + 1.0, T), (0, (Y0 + Y1) / 2 - 0.75, ZR + T / 2), head, root, c=c))
    add(K.box("cab_roof_skin", (2 * HW + 0.36, Y1 - Y0 + 1.1, 0.05), (0, (Y0 + Y1) / 2 - 0.75, ZR + T + 0.025), white, root, c=c, idx=3))
    for y in (-1.0, 0.6):
        add(K.box("cab_roofbow", (2 * HW, 0.14, 0.05), (0, y, ZR - 0.025), trim, root, c=c))
    # side walls: door panel below the belt, pillars, top rail; panes in between
    BELT, TOPW = F + 1.42, F + 2.72
    wins = {}
    for sx, sd in ((1, "r"), (-1, "l")):
        x = sx * (HW + T / 2)
        add(K.box(f"cab_door_{sd}", (T, Y1 - Y0 + 0.9, BELT - F), (x, (Y0 + Y1) / 2 - 0.45, (F + BELT) / 2), trim, root, c=c))
        add(K.box(f"cab_doorskin_{sd}", (0.04, Y1 - Y0 + 0.9, BELT - F + 0.5), (x + sx * 0.07, (Y0 + Y1) / 2 - 0.45, (F + BELT) / 2 - 0.25), white, root, c=c, idx=3))
        add(K.box(f"cab_toprail_{sd}", (T, Y1 - Y0 + 0.9, ZR - TOPW), (x, (Y0 + Y1) / 2 - 0.45, (TOPW + ZR) / 2), trim, root, c=c))
        for (ya, yb, nm) in ((Y0 - 0.9, -2.45, "c"), (-0.72, -0.44, "b"), (1.52, 1.82, "a")):
            add(K.box(f"cab_pillar_{nm}_{sd}", (T, yb - ya, TOPW - BELT), (x, (ya + yb) / 2, (BELT + TOPW) / 2), trim, root, c=c))
        for (ya, yb, nm) in ((-2.45, -0.72, "rear"), (-0.44, 1.52, "front")):
            q = K.quad(f"cab_win_{nm}_{sd}", yb - ya, TOPW - BELT, (x, (ya + yb) / 2, (BELT + TOPW) / 2), "+X" if sx > 0 else "-X", G, root, c=c)
            q.visible_shadow = False; add(q); wins[f"{nm}_{sd}"] = q
        # the quarter light ahead of the A post (triangular in life; a small pane here)
        q = K.quad(f"cab_win_quarter_{sd}", Y1 - 1.82, (TOPW - BELT) * 0.62, (x, (1.82 + Y1) / 2, BELT + (TOPW - BELT) * 0.31), "+X" if sx > 0 else "-X", G, root, c=c)
        q.visible_shadow = False; add(q)
        add(K.box(f"cab_quarter_top_{sd}", (T, Y1 - 1.82, (TOPW - BELT) * 0.38), (x, (1.82 + Y1) / 2, TOPW - (TOPW - BELT) * 0.19), trim, root, c=c))
        # arm rest, door pull, window crank, door card pocket, grab handle above the door, belt reel
        add(K.box(f"cab_armrest_{sd}", (0.16, 1.1, 0.10), (sx * (HW - 0.08), 0.55, F + 1.12), dark, root, bevel=0.03, c=c))
        add(K.box(f"cab_armrest_r_{sd}", (0.16, 1.0, 0.10), (sx * (HW - 0.08), -1.55, F + 1.12), dark, root, bevel=0.03, c=c))
        add(K.box(f"cab_pocket_{sd}", (0.10, 1.2, 0.30), (sx * (HW - 0.05), 0.7, F + 0.35), dark, root, bevel=0.03, c=c))
        add(K.cyl(f"cab_pull_{sd}", 0.03, 0.26, (sx * (HW - 0.02), 1.15, F + 1.25), ch, root, rot=(math.pi / 2, 0, 0), c=c, segs=8))
        for y in (0.6, -1.5):
            add(K.tube(f"cab_grab_{sd}", [(sx * (HW - 0.02), y - 0.3, ZR - 0.12), (sx * (HW - 0.12), y - 0.25, ZR - 0.20), (sx * (HW - 0.12), y + 0.25, ZR - 0.20), (sx * (HW - 0.02), y + 0.3, ZR - 0.12)], 0.025, dark, root, c=c, segs=6))
        add(K.box(f"cab_beltreel_{sd}", (0.08, 0.14, 0.22), (sx * (HW - 0.04), -0.58, F + 2.2), dark, root, bevel=0.02, c=c))
        add(K.box(f"cab_belt_{sd}", (0.012, 0.07, 1.5), (sx * (HW - 0.06), -0.50, F + 1.5), K.simple("cab_belt", "#3b3d44", 0.9), root, rot=(math.radians(8), 0, 0), c=c))
    # dashboard: lower block, top pad, binnacle with the cluster, centre stack with the switch panel and the radio
    DT = F + 1.50
    add(K.box("cab_dash_low", (2 * HW, 0.75, 1.0), (0, 2.08, F + 0.75), trim, root, bevel=0.06, c=c))
    add(K.box("cab_dash_top", (2 * HW, 1.0, 0.24), (0, 2.02, DT - 0.10), dark, root, bevel=0.07, c=c))
    add(K.box("cab_firewall", (2 * HW + 0.3, 0.1, DT - F + 0.3), (0, Y1 + 0.30, (F + DT) / 2), dark, root, c=c))
    xd = SEATS["drv"][0]
    add(K.box("cab_binnacle", (1.15, 0.42, 0.34), (xd, 1.70, DT + 0.12), dark, root, bevel=0.07, c=c))
    cm = K.image_mat("cab_cluster", _cluster_tex(), rough=0.3, emit_strength=2.2)
    q = K.quad("cab_cluster", 0.95, 0.42, (xd, 1.485, DT + 0.10), "-Y", cm, root, c=c); q.rotation_euler = (math.radians(-12), 0, 0); add(q)
    # steering column and wheel (rim, three spokes, boss)
    col_a = Vector((xd, 1.55, DT - 0.15)); col_b = Vector((xd, 0.98, DT + 0.22))
    add(K.tube("cab_column", [col_a, col_b], 0.07, dark, root, c=c))
    sw = K.lathe("cab_steer", [(0.42, -0.035), (0.455, 0.0), (0.42, 0.035), (0.385, 0.0)], pl, root, loc=tuple(col_b), c=c, segs=28, axis="Y", cap=False)
    tilt = math.atan2(col_b.z - col_a.z, col_a.y - col_b.y)
    sw.rotation_euler = (tilt, 0, 0); add(sw)
    hub = K.cyl("cab_steer_boss", 0.12, 0.08, tuple(col_b), pl, root, rot=(math.pi / 2 + tilt, 0, 0), c=c); add(hub)
    for k in range(3):
        ang = math.radians(90 + 120 * k)
        sp = K.box("cab_spoke", (0.40, 0.03, 0.06), (0, 0, 0), pl, sw, c=c)
        sp.location = (0.21 * math.cos(ang), 0, 0.21 * math.sin(ang)); sp.rotation_euler = (0, -ang, 0); add(sp)
    for sx in (-1, 1):
        add(K.tube("cab_stalk", [(xd, 1.25, DT + 0.02), (xd + sx * 0.5, 1.2, DT + 0.06)], 0.02, dark, root, c=c, segs=6))
    # centre stack, tilted to the driver: switch panel on top, radio below, vents, glove box, cup of the hand brake
    # (checker) at y 1.58 the switch plate leaned back INTO cab_dash_top (y from 1.52, z DT-0.22..DT+0.02): all four rockers
    # were buried in the dash slab and could not be seen from anywhere; the stack now stands 0.26 clear of it
    stack = K.empty("cab_stack", (0.0, 1.32, DT - 0.42), root, c, rot=(math.radians(-22), 0, math.radians(10)))
    add(K.box("cab_stack_body", (0.95, 0.20, 1.05), (0, 0.10, 0), dark, stack, bevel=0.04, c=c))
    add(K.box("cab_switchplate", (0.86, 0.02, 0.40), (0, -0.01, 0.28), K.simple("cab_plate", "#2f3238", 0.35, 0.7), stack, c=c))
    sw_defs = [("siren", -0.30, (1.0, 0.10, 0.06), "ไซเรน"), ("beacon", -0.10, (0.10, 0.25, 1.0), "ไฟวับวาบ"), ("flood", 0.10, (1.0, 0.85, 0.5), "สปอตไลต์"), ("radio", 0.30, (0.2, 1.0, 0.4), "วิทยุ")]
    switches = {}
    for nm, x, col, txt in sw_defs:
        # (checker) back-lit rockers: as plain plastic they rendered black in the S84 insert, whatever light was in the cab
        body_m = K.emit("cab_rockerlit_" + nm, tuple(c_ * 0.8 + 0.04 for c_ in col), ROCKER_OFF if nm in ("siren", "beacon") else ROCKER_OFF * 0.45)
        piv = K.empty("cab_sw_" + nm, (x, -0.03, 0.34), stack, c, rot=(math.radians(12), 0, 0))
        add(K.box("cab_rocker_" + nm, (0.13, 0.05, 0.19), (0, 0, 0), body_m, piv, bevel=0.015, c=c))
        led = K.emit("cab_led_" + nm, col, 0.05)
        add(K.box("cab_led_" + nm, (0.05, 0.012, 0.035), (0, -0.028, 0.05), led, piv, c=c))
        add(K.box("cab_swbezel_" + nm, (0.17, 0.02, 0.24), (x, -0.012, 0.34), pl, stack, c=c))
        lm = K.image_mat("label_" + nm, _label_tex(nm + "b", txt, size=(384, 96), fs=46, tilt=random.Random(nm).uniform(-3, 3)), rough=0.8, emit_strength=0.12, alpha=True)
        ql = K.quad("cab_label_" + nm, 0.19, 0.071, (x, -0.022, 0.165), "-Y", lm, stack, c=c); add(ql)
        Lg = K.point("cab_glow_" + nm, (x, -0.16, 0.36), 0.0, col, 0.03, parent=stack, glossy=False); Lg.hide_render = True
        switches[nm] = dict(pivot=piv, led=led, light=Lg, on=False, body=body_m)
    rm = K.image_mat("cab_radio", _radio_tex(), rough=0.3, emit_strength=1.4)
    add(K.box("cab_radio_body", (0.80, 0.06, 0.34), (0, -0.01, -0.14), pl, stack, bevel=0.01, c=c))
    add(K.quad("cab_radio_face", 0.74, 0.30, (0, -0.045, -0.14), "-Y", rm, stack, c=c))
    add(K.box("cab_mic", (0.14, 0.09, 0.22), (0.52, -0.03, -0.10), pl, stack, bevel=0.03, c=c))
    cord = [(0.52, -0.03, -0.22)] + [(0.52 + 0.035 * math.cos(k * 1.6), -0.03 + 0.035 * math.sin(k * 1.6), -0.22 - 0.022 * k) for k in range(1, 16)] + [(0.30, 0.0, -0.50)]
    add(K.tube("cab_mic_cord", cord, 0.012, pl, stack, c=c, segs=5))
    for x in (-1.25, -0.55, 1.45):
        for k in range(4):
            add(K.box("cab_vent", (0.42, 0.03, 0.022), (x, 1.515, DT - 0.26 + k * 0.045), pl, root, c=c, rot=(math.radians(20), 0, 0)))
    add(K.box("cab_glovebox", (1.05, 0.02, 0.36), (-0.95, 1.70, F + 0.86), dark, root, c=c))
    add(K.box("cab_glovelatch", (0.14, 0.03, 0.05), (-0.95, 1.685, F + 1.0), ch, root, c=c))
    add(K.tube("cab_handbrake", [(0.0, 0.25, F + 0.42), (0.0, 0.05, F + 0.62), (0.0, -0.35, F + 0.78)], 0.03, pl, root, c=c))
    add(K.tube("cab_gearstick", [(0.0, 0.9, F + 0.42), (0.03, 0.82, F + 1.0)], 0.022, ch, root, c=c)); add(K.lathe("cab_gearknob", [(0.001, -0.06), (0.06, -0.03), (0.07, 0.03), (0.001, 0.07)], pl, root, loc=(0.03, 0.82, F + 1.02), c=c, segs=10))
    # things lying about: a helmet on the dash, a clipboard, a water bottle, a torch in a clip (shapes only)
    add(K.lathe("cab_dash_helmet", [(0.001, 0.34), (0.20, 0.31), (0.30, 0.17), (0.32, 0.0), (0.28, 0.0)], K.simple("helmet_white", "#d9d9d4", 0.3, 0.0, 0.5), root, loc=(-1.05, 2.0, DT + 0.03), c=c))
    add(K.box("cab_clipboard", (0.42, 0.56, 0.02), (-0.25, 2.08, DT + 0.035), K.simple("clipboard", "#6a4a2a", 0.6), root, rot=(0, 0, 0.3), c=c))
    add(K.box("cab_clip_paper", (0.36, 0.48, 0.006), (-0.25, 2.08, DT + 0.05), K.simple("paper_wet", "#c4c1b6", 0.5), root, rot=(0, 0, 0.3), c=c))
    add(K.cyl("cab_bottle", 0.07, 0.42, (0.22, 0.45, F + 0.63), K.simple("bottle", "#2a6fa8", 0.2, 0.0, 0.6), root, c=c))
    # windscreen: raked pane, header, pillars along its edges, sun visors, the interior mirror
    wb = Vector((0, Y1, DT + 0.05)); wt = Vector((0, 1.70, ZR - 0.12))
    rake = math.atan2(wb.y - wt.y, wt.z - wb.z); wl = (wt - wb).length
    ws = K.quad("cab_windscreen", 2 * HW, wl, tuple((wb + wt) / 2), "+Y", G2, root, c=c); ws.rotation_euler = (rake, 0, 0); ws.visible_shadow = False; add(ws)
    add(K.box("cab_header", (2 * HW + 0.3, 0.9, 0.16), (0, 1.36, ZR - 0.06), trim, root, c=c))
    for sx in (-1, 1):
        ap = K.box("cab_apost", (0.16, 0.16, wl + 0.2), (sx * (HW + 0.02), (wb.y + wt.y) / 2, (wb.z + wt.z) / 2), trim, root, c=c); ap.rotation_euler = (rake, 0, 0); add(ap)
        vz = K.box("cab_visor", (1.2, 0.03, 0.34), (sx * 0.85, 1.52, ZR - 0.22), dark, root, bevel=0.02, c=c); vz.rotation_euler = (math.radians(-70), 0, 0); add(vz)
    add(K.box("cab_mirror_in", (0.62, 0.04, 0.17), (0, 1.62, ZR - 0.34), dark, root, bevel=0.03, c=c))
    add(K.box("cab_mirror_in_glass", (0.56, 0.01, 0.13), (0, 1.597, ZR - 0.34), K.simple("mirror_dark", "#0a0c12", 0.03, 0.0, 1.0), root, c=c))
    add(K.cyl("cab_mirror_in_stem", 0.02, 0.2, (0, 1.66, ZR - 0.22), dark, root, c=c, segs=6))
    # wipers: two arms on pivots just outside the glass; local Z of each pivot is the glass normal
    wip = []
    nrm = Vector((0, math.cos(rake), math.sin(rake)))
    for i, x in enumerate((0.95, -0.55)):
        base = wb + Vector((x, 0.06, 0.02)) + nrm * 0.03
        pv = K.empty(f"cab_wiper_{i}", tuple(base), root, c)
        pv.rotation_euler = (math.pi / 2 + rake, 0, 0)          # local Z -> into the glass, local Y -> up the glass
        pv["rest"] = pv.rotation_euler[:]
        arm = K.box(f"cab_wiper_arm_{i}", (0.03, 1.45, 0.025), (0, 0.72, 0), pl, pv, c=c)
        bl = K.box(f"cab_wiper_blade_{i}", (0.045, 1.25, 0.03), (0.0, 0.9, -0.02), rub, pv, c=c)
        add(arm); add(bl); wip.append(pv)
    # outside, seen through the glass: the bonnet with its crease and washer jets, wing mirrors on arms
    bn = K.box("cab_bonnet", (2 * HW + 0.2, 2.9, 0.5), (0, Y1 + 1.75, DT - 0.42), white, root, bevel=0.14, rot=(math.radians(-4), 0, 0), c=c, idx=3); add(bn)
    add(K.box("cab_bonnet_crease", (0.05, 2.7, 0.02), (0, Y1 + 1.75, DT - 0.15), K.simple("seam_dark", "#0b0c0e", 0.6), root, rot=(math.radians(-4), 0, 0), c=c))
    add(K.box("cab_scuttle", (2 * HW, 0.3, 0.06), (0, Y1 + 0.20, DT - 0.02), pl, root, c=c))
    for sx in (-0.6, 0.6): add(K.box("cab_jet", (0.08, 0.05, 0.03), (sx, Y1 + 0.75, DT - 0.14), pl, root, c=c))
    mirrors = {}
    road_m = K.image_mat("cab_mirror_road", _road_mirror_tex(), rough=0.2, emit_strength=0.9)
    for sx, sd in ((1, "r"), (-1, "l")):
        mx = sx * (HW + 0.62)
        add(K.tube(f"cab_wing_arm_{sd}", [(sx * (HW + 0.1), 1.78, BELT + 0.25), (mx, 1.72, BELT + 0.30), (mx, 1.72, BELT + 0.95), (sx * (HW + 0.1), 1.78, BELT + 1.0)], 0.022, pl, root, c=c, segs=6))
        add(K.box(f"cab_wing_{sd}", (0.46, 0.08, 0.78), (mx, 1.74, BELT + 0.62), pl, root, bevel=0.03, rot=(0, 0, sx * math.radians(-14)), c=c))
        q = K.quad(f"cab_wing_glass_{sd}", 0.40, 0.70, (mx - sx * 0.01, 1.69, BELT + 0.62), "-Y", road_m, root, c=c); q.rotation_euler = (0, 0, sx * math.radians(-14))
        q.data.materials.clear(); q.data.materials.append(road_m); add(q); mirrors[sd] = q
    horde = [K.image_mat("cab_horde_%d" % k, _horde_tex(k), rough=0.2, emit_strength=0.9) for k in range(3)]
    # overlays on the side glass: breath fog (driver's window), the crack (rear left window)
    fm = K.alpha_card("cab_fog", _fog_tex(), (1, 1, 1), strength=0.10, alpha_mul=0.0)
    fq = K.quad("cab_fog", 1.2, 1.0, (HW + T / 2 + 0.006, 0.6, (BELT + TOPW) / 2), "-X", fm, root, c=c); fq.visible_shadow = False; fq.hide_render = True; add(fq)
    cq = []
    for lv in (1, 2):
        cmat = K.alpha_card("cab_crack_%d" % lv, _crack_tex(lv), (0.9, 0.95, 1.0), lit=True, rough=0.25)
        q = K.quad("cab_crack_%d" % lv, 1.6, 1.2, (-(HW + T / 2) + 0.012, -1.58, (BELT + TOPW) / 2), "+X", cmat, root, c=c); q.visible_shadow = False; q.hide_render = True; add(q); cq.append(q)
    # seats
    for nm in ("drv", "pas"): _seat("cab_seat_" + nm, SEATS[nm][0], SEATS[nm][1], root, c)
    _seat("cab_bench", 0.0, SEATS["rr"][1], root, c, bench=True)
    # practicals: instrument glow (teal), a warm dome lamp (off), a faint cool spill that stands for the wet glass glow
    lights = {}
    lights["cab_dash"] = K.point("cab_dash", (xd, 1.25, DT + 0.12), 40.0, (0.45, 1.0, 0.86), 0.12, parent=root, glossy=False)
    lights["cab_dome"] = K.point("cab_dome", (0, -0.2, ZR - 0.14), 0.0, (1.0, 0.82, 0.58), 0.14, parent=root, glossy=False)
    lights["cab_dome"].hide_render = True
    add(K.box("cab_dome_lens", (0.34, 0.22, 0.05), (0, -0.2, ZR - 0.03), K.emit("cab_dome_lens", (1.0, 0.82, 0.58), 0.03), root, bevel=0.015, c=c))
    lights["cab_ambient"] = K.point("cab_ambient", (0, 0.4, ZR - 0.5), AMBIENT_W, (0.50, 0.62, 1.0), 0.6, parent=root, glossy=False)   # the wet glass's own glow: no fixture
    lights["cab_console"] = K.point("cab_console", (0.22, 1.05, DT + 0.30), CONSOLE_W, (0.45, 1.0, 0.86), 0.05, parent=root, glossy=False)        # the cluster's spill on the switch panel
    lights["cab_radio"] = K.point("cab_radio_glow", (0.0, 1.3, DT - 0.55), 3.0, (0.3, 1.0, 0.5), 0.08, parent=root, glossy=False)
    for o in P:
        if o.type == "MESH" and o.pass_index == 0: o.pass_index = 4
    R = dict(root=root, parts=P, wins=wins, wipers=wip, switches=switches, mirrors=mirrors, horde=horde, road_m=road_m, fog=fq, cracks=cq, lights=lights,
             glass=[G, G2])
    _S["R"] = R; _S["A"] = A
    if with_gear:
        import gear
        R["gear"] = gear.build(root, c)
    exterior(False)
    bpy.context.view_layer.update()
    R["anchors"] = anchors()
    K.REG["cab"] = R
    return R


def anchors():
    R = _S["R"]; M = R["root"].matrix_world
    bpy.context.view_layer.update()
    M = R["root"].matrix_world

    def W(p): return tuple(M @ Vector(p))
    BELT, TOPW, DT = F + 1.42, F + 2.72, F + 1.50
    a = dict(fwd=tuple((M.to_3x3() @ Vector((0, 1, 0))).normalized()), right=tuple((M.to_3x3() @ Vector((1, 0, 0))).normalized()),
             floor_z=F, hip_z=CUSH, roof_z=ZR,
             win_driver=W((HW, 0.54, (BELT + TOPW) / 2)), win_rear_right=W((HW, -1.58, (BELT + TOPW) / 2)),
             win_passenger=W((-HW, 0.54, (BELT + TOPW) / 2)), win_rear_left=W((-HW, -1.58, (BELT + TOPW) / 2)),
             outside_driver=W((HW + 0.55, 0.54, 0.0)), outside_rear_left=W((-HW - 0.55, -1.58, 0.0)),
             windscreen=W((0, 2.08, F + 2.2)), bonnet=W((0, Y1 + 1.8, DT - 0.1)), console=W((0.0, 1.50, DT - 0.10)),
             wheel=W((SEATS["drv"][0], 0.98, DT + 0.22)), mirror_r=W((HW + 0.62, 1.69, BELT + 0.62)),
             mirror_l=W((-HW - 0.62, 1.69, BELT + 0.62)), gear_wall=W((0, Y0, F + 2.05)), shutter_handle=W((0, Y0 + 0.05, F + 1.25)),
             between_seats=W((0, 0.2, F + 2.2)), footwell_driver=W((SEATS["drv"][0] - 0.45, 1.3, F)))
    for nm, sw in R["switches"].items():
        a["switch_" + nm] = tuple(sw["pivot"].matrix_world.translation)
    for nm, (x, y) in SEATS.items():
        a["hip_" + nm] = W((x, y, CUSH)); a["head_" + nm] = W((x, y - 0.15, CUSH + 1.45))
    return a


def seat(name, legs_bu):
    """soles point for a seated flat puppet on seat `name`: the hook's driver formula (hip on the cushion, the drawing's
    seated legs hang legs_bu below the hip: Actor8.spec["legs"] + 0.06 times Actor8.sc)."""
    R = _S["R"]; M = R["root"].matrix_world
    x, y = SEATS[name]
    return tuple(M @ Vector((x, y + 0.30, CUSH + 0.17 - legs_bu)))


def exterior(on):
    """show / hide the pickup's own body while the cab interior is in use, and lift its beacon lights over the cab roof."""
    A = _S["A"]; truck = bpy.data.objects[A["rescue_truck"]]; R = _S["R"]
    mine = set(K.tree(R["root"]))
    for o in K.tree(truck):
        if o in mine: o.hide_render = on
        elif o.type == "MESH": o.hide_render = not on
    want = 0.0 if on else LIFT
    cur = _S.get("lift", 0.0)
    if abs(want - cur) > 1e-6:
        for ob in bpy.data.objects:
            if ob.parent is None and ob.name.startswith(("beacon_", "cone_beacon_")):
                M = ob.matrix_world.copy(); M.translation.z += want - cur; ob.matrix_world = M
        _S["lift"] = want


def drive(A, s, o, yaw=0.0):
    import x2
    return x2.move_truck(A, s, o, yaw)


def switch(name, on=True):
    sw = _S["R"]["switches"][name]
    sw["pivot"].rotation_euler = (math.radians(-12 if on else 12), 0, 0)
    K.set_emit(sw["led"], 5.0 if on else 0.05)
    K.set_emit(sw["body"], (ROCKER_ON if on else ROCKER_OFF) * (1.0 if name in ("siren", "beacon") else 0.45))
    sw["light"].data.energy = 5.0 if on else 0.0; sw["light"].hide_render = not on
    sw["on"] = on


def wipers(t=None, period=0.9, sweep_deg=96.0):
    for i, pv in enumerate(_S["R"]["wipers"]):
        r = list(pv["rest"])
        ph = 0.0 if t is None else 0.5 - 0.5 * math.cos(2 * math.pi * (t / period))
        base = math.radians(84.0)                         # parked: lying along the scuttle, tips toward -X
        pv.rotation_euler = (r[0], r[1], 0.0)
        pv.rotation_mode = "XYZ"
        ang = base - math.radians(sweep_deg) * ph
        pv.rotation_euler = (Matrix.Rotation(r[0], 3, "X") @ Matrix.Rotation(ang, 3, "Z")).to_euler()


def mirror(k=None, gain=1.0):
    R = _S["R"]
    m = R["road_m"] if k is None else R["horde"][k % 3]
    for q in R["mirrors"].values():
        q.data.materials[0] = m
    for nd in m.node_tree.nodes:
        if nd.type == "BSDF_PRINCIPLED": nd.inputs["Emission Strength"].default_value = 0.9 * gain


def crack(level=0):
    for i, q in enumerate(_S["R"]["cracks"]): q.hide_render = (i + 1) != level


def fog(level=0.0, win="driver"):
    """breath fog on a right-hand side window: "driver" or "rear_right"."""
    q = _S["R"]["fog"]; q.hide_render = level <= 0
    q.location.y = 0.54 if win == "driver" else -1.58
    m = q.data.materials[0]
    nd = m.node_tree.nodes.get("AMUL")
    if nd: nd.inputs[1].default_value = 0.85 * level


def dome(on=True, energy=38.0):
    L = _S["R"]["lights"]["cab_dome"]; L.hide_render = not on; L.data.energy = energy if on else 0.0
    K.set_emit("cab_dome_lens", 6.0 if on else 0.03)


def ambient(watts=AMBIENT_W, console=CONSOLE_W):
    """the cab's base light: the cool glow of the wet glass (no fixture) and the cluster's spill on the switch panel."""
    L = _S["R"]["lights"]; L["cab_ambient"].data.energy = watts; L["cab_console"].data.energy = console


def dash(gain=1.0):
    _S["R"]["lights"]["cab_dash"].data.energy = 40.0 * gain


def clear_shoulder(s0, s1):
    """hide the instanced jam cars standing on the hard shoulder between s0 and s1 (the cab drives there)."""
    return K.hide_rows(lambda x, y, n: s0 <= y <= s1 and x < -17.6)
