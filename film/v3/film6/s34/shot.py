#!/usr/bin/env python3
"""shot.py -- film 6 take s34: shot 34 (the ending, next morning), bakery MORNING (the plan's "DAWN"), g 2959..3080
(6-frame handles; shot g 2965..3074 = plan 98.83-102.50 s).

    shot 34  At the counter, from the street (the s01 camera family): the customer's basket of 12 on the inside counter between kit
             (left, on his hidden stool) and Henry (right, behind the counter).  Three framings:
               A  g 2959..3002  two-shot: Henry counts the loaves himself, his index finger tapping along the rows (one finger up);
                                kit watches, worried                                                    "เช้าวันต่อมา ลุงเฮนรี่"
               B  g 3003..3045  punch-in on Henry + basket: he brings up the paler 13th loaf from under the counter, looks at it,
                                and puts it on the very top of the pile himself (lands g 3040)          "หยิบก้อนที่สิบสามใส่ตะกร้าเอง"
               C  g 3046..3080  two-shot, slow push toward kit: Henry turns and gives kit one slow nod; kit beams (grin, little hop)
Mouths: nobody speaks (no quoted line): static expression mouths.  The 13th loaf is the paler one (pale crust gradient on Henry's
held loaf and on the top loaf of the 13-loaf basket drawing).  NO depth of field anywhere (client rule).

    python3 shot.py probe 34 a:b[:step] | stills 34 a:b[:step] <out_dir> [scale] [samples] | final 34 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(98.83), C.g_bound(102.50)       # 2965, 3075
H = 6
RANGES = {34: (G0 - H, G1 + H - 1)}                 # 2959..3080
CUT_B, CUT_C = 3003, 3046
LAND = C.g_of(101.25)                               # 3041 -> the loaf lands on "สิบสามใส่"
RISE = (3014, 3024)                                 # loaf comes up from under the counter
LOOK = (3024, 3032)                                 # holds it up, looks at it
CARRY = (3032, LAND)                                # over to the basket
NOD = (3052, 3060, 3072)


def bf(shot, g):
    return int(g) - 2700


# ----------------------------------------------------------------------------- staging (bakery world D)
KIT, KIT_Z = (-0.40, 1.55), 0.62
HENRY = (1.80, 2.00)
BASKET = Vector((0.95, 0.95, 1.25))
BASKET_SCALE = 1.4
STEAM = 0.35
PICK = Vector((1.50, 1.20, 1.00))                   # under the counter top (hidden), Henry's side
LOAF = dict(type="loaf", scale=0.9)
LOAF_UP = 0.145 * 0.9
HOVER = 0.13
PALE = dict(light="#fff3d8", base="#f3d9a6", dark="#cfa46c", crust="#b88a52", score="#fff6e2", flour="#ffffff")

CAMS = {
    "A": [(RANGES[34][0], (0.82, -2.95, 2.78), (0.88, 1.6, 2.30), 24.0), (CUT_B - 1, (0.82, -2.60, 2.76), (0.88, 1.6, 2.32), 24.0)],
    "B": [(CUT_B, (1.32, -1.75, 2.55), (1.36, 1.6, 2.20), 28.0), (CUT_C - 1, (1.28, -1.55, 2.55), (1.32, 1.6, 2.22), 28.0)],
    "C": [(CUT_C, (0.70, -2.70, 2.75), (0.80, 1.6, 2.32), 24.0), (RANGES[34][1], (0.55, -2.25, 2.72), (0.70, 1.6, 2.36), 24.0)],
}


def framing(g):
    return "A" if g < CUT_B else ("B" if g < CUT_C else "C")


def cam_at(g):
    ks = CAMS[framing(g)]
    a, b = ks[0], ks[-1]
    u = ez((g - a[0]) / float(b[0] - a[0]), "sine")
    return Vector(lerp(a[1], b[1], u)), Vector(lerp(a[2], b[2], u)), lerp(a[3], b[3], u)


# ----------------------------------------------------------------------------- poses
def count_points(g):
    """A: the counting finger taps along the three rows of the pile, left to right (drawing coords on the basket card)."""
    taps = [(-0.29, 0.30), (-0.14, 0.30), (0.0, 0.30), (0.15, 0.30), (0.29, 0.30), (-0.22, 0.22), (-0.07, 0.22), (0.08, 0.22),
            (0.22, 0.22), (-0.14, 0.15), (0.0, 0.15), (0.14, 0.15)]
    g0, g1 = 2961, 3000
    u = clamp((g - g0) / float(g1 - g0)) * (len(taps) - 1)
    i = int(min(len(taps) - 2, math.floor(u))); fr = u - i
    a, b = taps[i], taps[i + 1]
    lift = 0.06 * math.sin(math.pi * fr)
    return (lerp(a[0], b[0], ez(fr)), lerp(a[1], b[1], ez(fr)) - 0.12 - lift)


def henry_hand(g, Tk):
    """(world point, kind) for Henry's screen-left hand: 'count' (finger), 'loaf' (carrying the pale loaf), 'rest'."""
    if g <= 3002:
        return Tk.basket.to_world(count_points(g)), "count"
    top = Tk.basket.to_world((0.02, 0.13 - HOVER))
    held = Vector((1.30, 1.05, 2.25))                           # loaf held up in front of his face, looking at it
    if RISE[0] <= g < LOOK[0]:
        u = ez((g - RISE[0]) / float(LOOK[0] - RISE[0]))
        return PICK.lerp(held, u), "loaf"
    if LOOK[0] <= g < CARRY[0]:
        return held + Vector((0, 0, 0.03 * math.sin((g - LOOK[0]) * 0.6))), "loaf"
    if CARRY[0] <= g <= LAND:
        u = ez((g - CARRY[0]) / float(LAND - CARRY[0]))
        apex = (held + top) / 2 + Vector((0, 0, 0.18))
        return (1 - u) ** 2 * held + 2 * (1 - u) * u * apex + u * u * top, "loaf"
    if LAND < g <= LAND + 8:
        u = ez((g - LAND) / 8.0)
        return top.lerp(Vector((1.50, 1.15, 1.45)), u), "rest"
    if g < RISE[0]:
        u = ez((g - 3003) / float(RISE[0] - 3003))
        start = Tk.basket.to_world(count_points(3002))
        return start.lerp(PICK, u), "rest"
    return Vector((1.50, 1.15, 1.45)), "rest"


def henry_pose(g):
    p = dict(yaw=-0.40, pitch=0.35, expr="neutral", head_roll=-4 + 2 * math.sin(g * 0.07), gaze=(-0.5, 0.7),
             arm_r=dict(hand=(0.40, 1.05), bend=0.9), legs="stand", lean=4, t=g / 30.0,
             blink=blink(g, [2975, 3010, 3047, 3076]))
    if g <= 3002:
        p.update(fingers_l=1, expr="unimpressed", pitch=0.45, gaze=(-0.6, 0.8))
    elif g < LAND + 2:
        lk = ez((g - LOOK[0]) / 6.0) * (1 - ez((g - CARRY[0]) / 6.0))
        p.update(expr="happy" if g >= LOOK[0] else "neutral", yaw=-0.40 + 0.15 * lk, pitch=0.35 - 0.35 * lk, gaze=(-0.5 + 0.3 * lk, 0.7 - 0.6 * lk))
    else:
        turn = ez((g - (LAND + 2)) / 8.0)
        nod = pulse(g, NOD[0], NOD[1], NOD[2], 1.0)
        p.update(expr="happy", yaw=lerp(-0.40, -0.70, turn), pitch=lerp(0.35, -0.05, turn) + 0.45 * nod,
                 gaze=(lerp(-0.5, -0.95, turn), lerp(0.7, 0.0, turn) + 0.3 * nod))
    return p


def kit_pose(g):
    beam = ez((g - (NOD[1] - 2)) / 6.0) if g >= NOD[1] - 2 else 0.0
    hop = pulse(g, NOD[1] + 2, NOD[1] + 6, NOD[1] + 13, 1.0)
    watch = ez((g - LOOK[0]) / 8.0) if g >= LOOK[0] else 0.0          # eyes follow the loaf, surprise
    look_h = ez((g - (LAND + 3)) / 6.0) if g >= LAND + 3 else 0.0
    expr = "worried"
    if g >= LOOK[0]:
        expr = "surprised"
    if g >= NOD[1] - 2:
        expr = "grinning"
    p = dict(yaw=0.35 + 0.05 * look_h, pitch=0.25 - 0.15 * watch - 0.20 * beam, expr=expr, head_roll=-3 + 2 * math.sin(g * 0.13) + 4 * beam,
             gaze=(0.6 + 0.3 * look_h, 0.5 - 0.5 * watch), lean=5,
             arm_l=dict(hand=(-0.30, 0.82), bend=0.6), arm_r=dict(hand=(0.30, 0.80), bend=-0.6), legs="stand",
             squash=(1 + 0.05 * hop, 1 - 0.05 * hop), blink=blink(g, [2985, 3030, NOD[1] - 4]), t=g / 30.0)
    if beam > 0.5:
        p["arm_l"] = dict(hand=(-0.55, -0.20 - 0.15 * hop), bend=-0.5, stretch=1.2)   # little fist up
        p["arm_r"] = dict(hand=(0.45, 0.85), bend=-0.6)
    return p


# ----------------------------------------------------------------------------- the take
def pale_basket_svg(uid, loaves=13):
    svg, an = cast6.basket_svg(uid, loaves=loaves)
    if loaves >= 13:
        pale = ('<radialGradient id="%s_pl" cx="0.36" cy="0.30" r="0.80"><stop offset="0" stop-color="#fff3d8"/>'
                '<stop offset="0.45" stop-color="#f3d9a6"/><stop offset="1" stop-color="#cfa46c"/></radialGradient>' % uid)
        svg = svg.replace("</defs>", pale + "</defs>", 1)
        svg = svg.replace('fill="url(#%s_lf)"' % uid, 'fill="url(#%s_pl)"' % uid, 1)
    return svg, an


CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=24.0, name="cam_s34")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        box = (-0.56, -0.06, 0.56, 0.72)
        items = [(pale_basket_svg("b34_%d" % n, n)[0], box, 512) for n in (12, 13)]
        pngs = C.svg_pngs(items, os.path.join(TMP, "props"))
        self.basket = C.PropCard("basket", pngs, box, scale=BASKET_SCALE, shadow=True)
        loc, look, lens = cam_at(RANGES[34][0])
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc)
        self.kind = {}
        import bpy
        self.hidden = [o.name for o in bpy.data.objects if o.name.startswith("small_") or "small_pan" in o.name]
        for n in self.hidden:                          # the hand balance would stand in front of Henry: off for this shot
            bpy.data.objects[n].hide_render = True
        print("s34: hidden", self.hidden, flush=True)

    def pose(self, shot, gs):
        kit, henry = self.actors["kit"], self.actors["henry"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(kit, f, KIT, KIT_Z)
            C.place(henry, f, HENRY, 0.0)
            self.basket.show(1 if g > LAND else 0, frame=f)
            self.key_set(f, steam=STEAM, oven=1.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            pt, kind = henry_hand(g, self)
            self.kind[g] = kind
            p = henry_pose(g)
            if kind == "loaf":
                p["prop_l"] = LOAF
                hands = C.held_on_palm(henry, self.cam, f, pt, up=LOAF_UP, side="l", bend=0.5, stretch=1.3)
            else:
                hands = {"l": {"hand": tuple(pt), "bend": 0.5, "stretch": 1.3}}
            henry.pose(f, p, hands=hands, camera=self.cam)
            kit.pose(f, kit_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 448)], fr)
        old = dict(cast6.BREAD)
        cast6.BREAD.update(PALE)                       # the 13th loaf in Henry's hand is the paler one
        try:
            self.sprites_for([(henry, 384)], fr)
        finally:
            cast6.BREAD.update(old)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        out = dict(shot=shot, g=g, framing=framing(g), cam=[round(c, 3) for c in loc], lens=round(lens, 2), heads=C.head_report(self, f),
                   loaves=13 if g > LAND else 12, hand=self.kind.get(g))
        pt, kind = henry_hand(g, self)
        out["hand_target_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(pt), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def main():
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)


if __name__ == "__main__":
    main()
