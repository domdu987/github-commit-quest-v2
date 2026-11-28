"""S903 (dummy, class C1)  '30 วินาที'  -- a DRAWN insert, no Cycles: Kong's wrist, a square rescue watch over the glove
cuff, no digits, one red second hand sweeping away from a drop of blood on the 12 mark.  The hand ticks on the cut
table's cue "tick" (a word + 0.25 s), the frame drifts with the arm and jolts for two frames.
A sketch of the plan's watch card (S26 / S36 / S44 / S47), drawn to prove the C1 path, not the approved design."""
import math
from PIL import Image, ImageDraw
from ep2d import *
CLASS = "C1"
ORANGE, ORANGE_D, GLOVE, STEEL, FACE, RED, BLOOD = (238, 122, 31), (176, 82, 20), (24, 24, 28), (150, 158, 168), (236, 234, 226), (226, 59, 48), (150, 16, 22)


def draw(ctx):
    ss = max(2, ctx.ss)
    W, H = ctx.W * ss, ctx.H * ss
    u = W / 720.0                                           # layout unit: 1 = one pixel of a 720-wide frame
    im = Image.new("RGB", (W, H), (9, 12, 20)); d = ImageDraw.Draw(im)
    lw = lambda px: max(1, int(round(px * u)))
    # the arm drifts 20 px through the shot; a 2-frame jolt at the tick
    k_tick = int(round((ctx.scene.cue("tick") - ctx.scene.t_of(0)) * 24)) - ctx.shot["f0"]
    jolt = {0: (9, -6), 1: (-5, 3)}.get(ctx.k - k_tick, (0, 0))
    ox = (-10 + 20 * ctx.u + jolt[0]) * u; oy = (6 * math.sin(ctx.u * math.pi) + jolt[1]) * u
    cx, cy = W * 0.5 + ox, H * 0.47 + oy
    # wet deck behind, out of focus: two bands of beacon colour
    for i, (col, y0) in enumerate((((30, 44, 86), 0.0), ((70, 30, 34), 0.62))):
        d.rectangle([0, int(H * y0), W, int(H * (y0 + 0.38))], fill=col)
    im = im.filter(ImageFilter.GaussianBlur(40 * u)); d = ImageDraw.Draw(im)
    # sleeve (orange, from the left), glove (black, to the right): one forearm across the frame, tilted
    ang = math.radians(-14)
    ax, ay = math.cos(ang), math.sin(ang); nx, ny = -ay, ax

    def P(a, n):
        return (cx + (a * ax + n * nx) * u, cy + (a * ay + n * ny) * u)

    d.polygon([P(-520, -150), P(-60, -150), P(-60, 150), P(-520, 150)], fill=ORANGE, outline=INK)
    d.line([P(-520, -150), P(-60, -150)], fill=INK, width=lw(7)); d.line([P(-520, 150), P(-60, 150)], fill=INK, width=lw(7))
    d.polygon([P(-520, 70), P(-60, 70), P(-60, 150), P(-520, 150)], fill=ORANGE_D)
    d.polygon([P(-150, -150), P(-110, -150), P(-110, 150), P(-150, 150)], fill=(232, 236, 240), outline=INK)   # reflective band
    d.polygon([P(-60, -158), P(520, -140), P(520, 140), P(-60, 158)], fill=GLOVE, outline=INK)
    d.line([P(-60, -158), P(-60, 158)], fill=INK, width=lw(8))
    for a in (40, 120, 200):
        d.line([P(a, -150), P(a + 16, 150)], fill=(46, 46, 52), width=lw(5))
    # strap and the square case
    d.polygon([P(-112, -190), P(112, -190), P(112, 190), P(-112, 190)], fill=(34, 34, 40), outline=INK)
    c0, c1 = P(-150, -150), P(150, 150)
    box = [min(c0[0], c1[0]) - 30 * u, min(c0[1], c1[1]) - 10 * u, max(c0[0], c1[0]) + 30 * u, max(c0[1], c1[1]) + 10 * u]
    mx, my = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    R = 150 * u
    d.rounded_rectangle([mx - R - 26 * u, my - R - 26 * u, mx + R + 26 * u, my + R + 26 * u], radius=int(40 * u), fill=STEEL, outline=INK, width=lw(8))
    d.rounded_rectangle([mx - R, my - R, mx + R, my + R], radius=int(26 * u), fill=FACE, outline=INK, width=lw(6))
    for i in range(12):                                    # hour marks, no digits
        a = math.radians(i * 30)
        r0, r1 = (0.74, 0.90) if i % 3 == 0 else (0.82, 0.90)
        d.line([(mx + math.sin(a) * R * r0, my - math.cos(a) * R * r0), (mx + math.sin(a) * R * r1, my - math.cos(a) * R * r1)], fill=INK, width=lw(9 if i % 3 == 0 else 5))
    # a drop of blood on the 12 mark, where the hand stood at the bite
    bx, by = mx, my - R * 0.86
    d.ellipse([bx - 15 * u, by - 13 * u, bx + 15 * u, by + 19 * u], fill=BLOOD, outline=INK, width=lw(3))
    d.ellipse([bx - 8 * u, by - 7 * u, bx - 2 * u, by - 1 * u], fill=(214, 70, 70))
    # the second hand: at the 6 (30 s gone), one tick per cue; it moves in ONE frame, like a quartz hand
    sec = 30 + (1 if ctx.k >= k_tick else 0)
    a = math.radians(sec * 6)
    d.line([(mx - math.sin(a) * R * 0.18, my + math.cos(a) * R * 0.18), (mx + math.sin(a) * R * 0.80, my - math.cos(a) * R * 0.80)], fill=INK, width=lw(12))
    d.line([(mx - math.sin(a) * R * 0.18, my + math.cos(a) * R * 0.18), (mx + math.sin(a) * R * 0.80, my - math.cos(a) * R * 0.80)], fill=RED, width=lw(7))
    d.ellipse([mx - 13 * u, my - 13 * u, mx + 13 * u, my + 13 * u], fill=RED, outline=INK, width=lw(4))
    # rain drops sitting on the glass, a glint
    for i in range(7):
        hx = mx + (E.C.hash01(i, 1) - 0.5) * 1.6 * R; hy = my + (E.C.hash01(i, 2) - 0.5) * 1.6 * R + 6 * u * ctx.u * (1 + i % 3)
        d.ellipse([hx - 7 * u, hy - 9 * u, hx + 7 * u, hy + 9 * u], outline=(120, 140, 170), width=lw(3))
    d.line([(mx - R * 0.78, my - R * 0.55), (mx - R * 0.40, my - R * 0.86)], fill=(255, 255, 255), width=lw(8))
    im = rain(im, ctx.k, 0.2)
    im = vignette(im, 0.5)
    return im.resize((ctx.W, ctx.H), Image.LANCZOS)
# (touched to prove the stale purge)
