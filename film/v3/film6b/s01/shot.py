#!/usr/bin/env python3
"""shot.py -- film 6b take s01: shots 1-3 (plan 0.00-4.10 s = g 0..122) + 6 out-handle frames (g 123..128), bakery MORNING.

    shot 1  g 0..47    CU kit behind the counter (head ~330 -> 390 px), slow push: deadpan, sneaky glance screen-left (g 6-16),
                       screen-right (g 18-28), back into the lens; on "ยัดขนมปัง" (g 30) the pale 13th loaf comes up on his palm,
                       held low by his chest, and the deadpan turns into a smirk (g 38).
    shot 2  g 48..71   ECU of the customer's basket on the counter (12 loaves), push in: kit's hand holds the pale 13th loaf over
                       the pile (g 48-52), lets go (g 53), it drops on the very top (lands g 56, "ก้อนที่สิบสาม" 1.57 s), squash +
                       a white steam puff (g 56-70).
    shot 3  g 72..122  MS from the street over the counter: the customer (woman1) carries the basket of 13 away screen-left
                       (walk g 74-112, out of frame ~g 108); the camera pushes past her onto kit, who WINKS into the lens (g 98-104,
                       "ลูกค้า" 2.99 s = g 93 / "ทุกครั้ง" 3.46 s = g 104) and grins.  Out-handle g 123..128: push + grin continue.
Cool counter-colour: a blue area light from the street/window side (lib6b.cool_fill) on the warm bakery.
Mouths: no quote in s01 -> static expression mouths only.  NO depth of field (C.Take).

    python3 shot.py probe 1,2,3 a:b[:step]
    python3 shot.py stills 1,2,3 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1,2,3 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6"))     # v3/film6/common.py (read-only reuse)
import common as C                                       # noqa: E402
import lib6b as L                                        # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing (film 6b clock: g = round(t * 30))
G1, G2, G3, G4 = 0, 48, 72, 123
H_OUT = 6
RANGES = {1: (G1, G2 - 1), 2: (G2, G3 - 1), 3: (G3, G4 + H_OUT - 1)}
G_LOAF_UP = 30                     # "ยัดขนมปัง" 0.89 s
G_DROP = 53                        # shot 2: the loaf leaves kit's hand
G_LAND = 56                        # lands on the pile
G_WINK = (98, 104)

# ----------------------------------------------------------------------------- staging (bakery world D, floor z 0)
KIT = (0.80, 1.48)
KIT_Z = 0.98                       # hidden stool behind the counter
BASKET = Vector((1.30, 1.08, 1.25))
BASKET_SCALE = 1.4
LOAF13 = (-0.01, 0.13)             # where the 13th loaf sits in basket_svg (top row, drawing D)
WOMAN0 = (0.35, -2.05)
STEAM = 0.35
LENS = 24.0


def cam_shot(shot, g):
    """(loc, look, lens)"""
    if shot == 1:
        u = ez((g - G1) / float(G2 - G1), "sine")
        loc = lerp((0.98, -1.35, 3.10), (0.92, -0.80, 3.04), u)
        look = lerp((0.80, 1.48, 2.70), (0.80, 1.48, 2.74), u)
        return Vector(loc), Vector(look), LENS
    if shot == 2:
        u = ez((g - G2) / float(G3 - G2), "sine")
        loc = lerp((1.02, -0.95, 2.05), (1.06, -0.62, 2.08), u)
        look = lerp((1.18, 1.20, 2.30), (1.20, 1.20, 2.26), u)
        return Vector(loc), Vector(look), LENS
    # shot 3: wide-ish on the customer, then push past her onto kit
    u = ez((g - G3) / float(G4 + H_OUT - G3), "sine")
    loc = lerp((1.60, -5.20, 2.95), (0.92, -1.90, 3.02), u)
    look = lerp((0.55, 1.20, 2.40), (0.80, 1.48, 2.62), u)
    return Vector(loc), Vector(look), LENS


# ----------------------------------------------------------------------------- poses
def kit_pose1(g):
    p = dict(yaw=0.05, pitch=0.0, expr="neutral", head_roll=0, lean=2, gaze=(0.0, 0.0), arm_l="down",
             arm_r="down", legs="stand", t=g / 30.0)
    ul = ez((g - 6) / 5.0) * (1 - ez((g - 16) / 4.0))         # look screen-left
    ur = ez((g - 18) / 4.0) * (1 - ez((g - 28) / 4.0))        # look screen-right
    p["gaze"] = (-0.95 * ul + 0.95 * ur, 0.05)
    p["yaw"] = 0.05 - 0.30 * ul + 0.30 * ur
    p["head_roll"] = 3 * ul - 3 * ur
    p["pitch"] = 0.10 * (ul + ur)
    if g >= G_LOAF_UP - 4:
        u = ez((g - (G_LOAF_UP - 4)) / 6.0)
        p["arm_r"] = dict(hand=(lerp(0.30, 0.62, u), lerp(1.40, 0.62, u)), bend=-0.6, stretch=1.25)
        if g >= G_LOAF_UP - 2:
            p["prop_r"] = dict(type="loaf", scale=1.0)
        p["gaze"] = (0.55 * u * (1 - ez((g - 38) / 3.0)), 0.45 * u * (1 - ez((g - 38) / 3.0)))
        p["pitch"] = 0.18 * u * (1 - ez((g - 38) / 3.0))
    if g >= 38:
        p["expr"] = "smirk"
    p["blink"] = blink(g, [3, 36])
    return p


def kit_pose2(g):
    p = dict(yaw=0.35, pitch=0.45, expr="smirk", head_roll=-4, lean=10, gaze=(0.5, 0.9), arm_l="down", legs="stand", t=g / 30.0)
    p["blink"] = blink(g, [66])
    return p


def kit_pose3(g):
    p = dict(yaw=-0.25, pitch=0.10, expr="smirk", head_roll=3, lean=4, gaze=(-0.8, 0.1), arm_l="akimbo",
             arm_r=dict(hand=(0.55, 0.85), bend=-0.3), legs="stand", t=g / 30.0)
    ul = ez((g - 90) / 6.0)                                   # turns from the customer into the lens
    p["yaw"] = lerp(-0.25, 0.10, ul)
    p["gaze"] = (lerp(-0.8, 0.0, ul), lerp(0.1, 0.0, ul))
    p["head_roll"] = lerp(3, -6, ul)
    if G_WINK[0] <= g <= G_WINK[1]:
        p["expr"] = "wink"
    elif g > G_WINK[1]:
        p["expr"] = "grinning"
    p["blink"] = blink(g, [80, 120])
    return p


def woman_pose(g):
    base = dict(expr="happy", prop_r="basket", basket=dict(loaves=13), t=g / 30.0)
    if g < 84:
        p = dict(base, yaw=0.30, pitch=-0.05, head_roll=-4, arm_r=dict(hand=(0.40, 0.45), bend=-0.3), arm_l="down", legs="stand",
                 gaze=(0.6, -0.2))
        return p
    ph = (g - 84) / 26.0
    p = cast6.cycle("woman1", ph, "walk", facing=-1, base=base, arms="l")
    p["arm_r"] = dict(hand=(0.40, 0.45), bend=-0.3)
    p["prop_r"] = "basket"; p["basket"] = dict(loaves=13); p["expr"] = "happy"; p["t"] = g / 30.0
    return p


def woman_xy(g):
    if g < 84:
        return WOMAN0
    d = 0.05 * (g - 84)                                      # ~3.4 D/s stroll, out of frame screen-left
    return (WOMAN0[0] - d, WOMAN0[1] - 0.01 * (g - 84))


# ----------------------------------------------------------------------------- the take
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=LENS, name="cam_s01b")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["woman"] = C.make_actor("woman", "woman1", sd)
        # cool counter-colour: blue sky light through the street opening + the window, onto the counter / back wall
        self.cool = [L.cool_fill("L_cool_window", (5.6, 1.2, 5.2), (0, 0, 0), energy=2500, size=4.0, color=(0.12, 0.30, 1.0))]
        L.aim(self.cool[0], (2.2, 6.5, 2.0))
        props = os.path.join(TMP, "props")
        svg, an = cast6.basket_svg("bk12", loaves=12)
        box = (-0.56, -0.06, 0.56, 0.72)
        self.basket = C.PropCard("basket", C.svg_pngs([(svg, box, 900)], props), box, scale=BASKET_SCALE, shadow=True)
        lp = C.svg_pngs([(cast6.loaf_svg("lf13", r=cast6.BASKET_LR, seed=3), (-0.09, -0.08, 0.09, 0.06), 3000)], props)[0]
        pale = L.pale_png(lp, lp[:-4] + "_pale.png")
        self.loaf = C.PropCard("loaf13", [pale], (-0.09, -0.08, 0.09, 0.06), scale=BASKET_SCALE, shadow=True)
        puffs = C.svg_pngs([(L.puff_svg(k / 7.0, r=0.16, seed=i), (-0.42, -0.62, 0.42, 0.25), 900) for i, k in enumerate(range(8))], props)
        self.puff = C.PropCard("puff", puffs, (-0.42, -0.62, 0.42, 0.25), scale=BASKET_SCALE, shadow=False)
        sg = C.svg_pngs([(L.thai_sign("ร้านลุงเฮนรี่", w=4.6, h=0.86, board="#1f5a46", edge="#c99a3a", fg="#ffd45a", outline="#3a2832",
                                       size=0.62), L.sign_box(4.6, 0.86), 260)], props)
        self.fascia = C.PropCard("fascia_th", sg, L.sign_box(4.6, 0.86), scale=1.0, shadow=False)
        self.fascia.put((1.0, -0.85, 5.34), face=(1.0, -10.0, 4.8))
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=(1.0, -2.0, 2.4))

    def land_pt(self):
        return self.basket.to_world(LOAF13) + Vector((0, -0.03, 0))

    def pose(self, shot, gs):
        kit, wom = self.actors["kit"], self.actors["woman"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_shot(shot, g)
            self.key_cam(f, loc, look, lens)
            C.place(kit, f, KIT, KIT_Z)
            C.place(wom, f, woman_xy(g) if shot == 3 else (6.0, -9.0), 0.0)
            wom.card.hide_render = False
            self.basket.show(0 if shot in (1, 2) else None, frame=f)
            self.key_set(f, steam=STEAM, oven=1.0)
            # the pale 13th loaf (shot 2 only, after it leaves kit's hand)
            lp = self.land_pt()
            if shot == 2 and g >= G_DROP:
                if g < G_LAND:
                    u = (g - G_DROP) / float(G_LAND - G_DROP)
                    pos = lp + Vector((0, 0, 0.42 * (1 - u * u)))
                    sq = (1.0, 1.0, 1.0)
                else:
                    pos = lp
                    k = {G_LAND: (1.22, 1, 0.78), G_LAND + 1: (0.92, 1, 1.08), G_LAND + 2: (1.04, 1, 0.97)}.get(g, (1, 1, 1))
                    sq = k
                self.loaf.put(pos, face=loc, frame=f)
                self.loaf.root.scale = tuple(BASKET_SCALE * s for s in sq)
                self.loaf.root.keyframe_insert("scale", frame=f)
                self.loaf.show(0, frame=f)
            else:
                self.loaf.put(lp + Vector((0, 0, 5)), face=loc, frame=f)
                self.loaf.show(None, frame=f)
            if shot == 2 and G_LAND <= g < G_LAND + 16:
                k = min(7, (g - G_LAND) // 2)
                self.puff.put(lp + Vector((0, -0.08, 0.02)), face=loc, frame=f)
                self.puff.show(k, frame=f)
            else:
                self.puff.put(lp + Vector((0, 0, 5)), face=loc, frame=f)
                self.puff.show(None, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                kit.pose(f, kit_pose1(g), camera=self.cam)
            elif shot == 2:
                p = kit_pose2(g)
                hover = self.land_pt() + Vector((0, 0, 0.42))
                if g < G_DROP:
                    p["prop_r"] = dict(type="loaf", scale=0.62)
                    hands = C.held_on_palm(kit, self.cam, f, hover, up=0.145 * 0.62, bend=-0.5, stretch=1.3)
                else:
                    u = ez((g - G_DROP) / 8.0)
                    hands = {"r": {"hand": tuple(hover + Vector((0.05 * u, 0, 0.10 * u))), "bend": -0.5, "stretch": 1.3, "shape": "open"}}
                kit.pose(f, p, hands=hands, camera=self.cam)
            else:
                kit.pose(f, kit_pose3(g), camera=self.cam)
            wom.pose(f, woman_pose(g) if shot == 3 else dict(expr="happy"), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 640)] + ([(wom, 448)] if shot == 3 else [(wom, 64)]), fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_shot(shot, g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))
        out["land_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(self.land_pt()), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
