#!/usr/bin/env python3
"""shot.py -- film 6 take s01: shot 1 only (g 0..62 + 7 out-handle frames, g 63..69), bakery MORNING (the "dawn" counter).

    shot 1  g 0..62   medium at the counter, from the street: kit (on a hidden stool behind the inside counter) counts loaves
                      into the customer's basket standing on the counter: each loaf is lifted from below the counter, held
                      just above its spot and dropped onto the pile (loaf 10 drops g 8, 11 g 21, 12 g 34; one small nod each),
                      looks up into the lens and WINKS (g 40..45), glances back over his shoulder at Henry (g 46..50, Henry in
                      the background by the roaring oven, squinting at a loaf, unaware), then slips the 13th loaf on top (held
                      g 49..56, drops g 57, on "แต่ยัดก้อน" 1.58 s = g 50..67) and grins at us (g 58).  Slow push the whole shot.
                      Handle g 63..69: the push and the grin continue (rendered in 3D).
Mouths: nobody speaks (no quoted line in shot 1): kit's mouth is the static mouth of each expression, henry's closed.
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

Internal shot id 1.  Blender frame of film frame g = g + 1.

    python3 shot.py probe 1 a:b[:step]
    python3 shot.py stills 1 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402  (paths, cast6 first, bpy, bakery, stage)
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_END = C.g_bound(2.10)            # 63: shot 2 starts here
H_OUT = 7                          # out-handle g 63..69
RANGES = {1: (0, G_END + H_OUT - 1)}
LAND = [7, 20, 33, 56]             # loaves 10, 11, 12 and the 13th land on the pile
RISE = [7, 7, 7, 7]                # frames from below the counter to the pile
G_LOOK = (36, 40)                  # turns up to the lens
G_WINK = (40, 45)                  # wink drawing held 6 frames
G_BACK = (46, 50)                  # glance back at henry (screen-left)
G_GRIN = 58                        # after the 13th: grin into the lens
G_SLIP = C.g_of(1.58)              # 50 "แต่ยัดก้อน"

# ----------------------------------------------------------------------------- staging (bakery world D, floor z 0)
KIT = (0.80, 1.48)
KIT_Z = 0.98                       # hidden stool behind the counter: head + chest + apron bib above the counter top (z 1.25)
HENRY = (-1.95, 5.55)
BASKET = Vector((1.30, 1.08, 1.25))     # base of the customer's basket on the inside counter top
BASKET_SCALE = 1.4
CAM_A = ((0.80, -2.80, 2.80), (0.66, 1.6, 2.32))
CAM_B = ((0.74, -2.42, 2.78), (0.66, 1.6, 2.34))
LENS = 24.0
STEAM = 0.35                       # thin wisps only: full steam crosses kit's face at this distance (the motif is planted at 21 s)
LOAF_UP = 0.145 * 0.9                   # cast6 PROP_TIP of 'loaf': loaf centre above the hand
LOAF = dict(type="loaf", scale=0.9)  # 0.9: the same size as the loaves drawn in the basket (x 1.2)
HOVER = 0.13                       # drawing units (x BASKET_SCALE): the loaf is dropped the last ~0.18 D
PICK = Vector((0.92, 1.12, 1.05))       # below the counter top (hidden): where the loaves come from


def cam1(g):
    u = ez(g / float(RANGES[1][1] + 1), "sine")
    loc = Vector(lerp(CAM_A[0], CAM_B[0], u)); look = Vector(lerp(CAM_A[1], CAM_B[1], u))
    return loc, look


# ----------------------------------------------------------------------------- poses
def count_at(g):
    """loaves in the basket at film frame g (the variant switches the frame after the landing)."""
    n = 9
    for k, L in enumerate(LAND):
        if g > L:
            n = 10 + k
    return n


def hand_path(g, top):
    """kit's screen-right hand: (world point, carrying loaf?).  top(k) = world point where loaf k lands."""
    for k, L in enumerate(LAND):
        r = RISE[k]
        if L - r <= g <= L + 1:                                     # carrying: up from below the counter, arc over to the pile
            u = ez((g - (L - r)) / float(r), "sine") if g <= L else 1.0
            B1 = top(k)
            apex = Vector(((PICK.x + B1.x) / 2 - 0.05, (PICK.y + B1.y) / 2, B1.z + 0.42))
            p = (1 - u) ** 2 * PICK + 2 * (1 - u) * u * apex + u * u * B1
            return p, True
        if L + 1 < g < L + 8 and (k + 1 >= len(LAND) or g < LAND[k + 1] - RISE[k + 1]):   # empty hand back down
            u = ez((g - (L + 1)) / 6.0, "sine")
            return top(k) + (PICK - top(k)) * u + Vector((0, 0, 0.12 * math.sin(math.pi * u))), False
    return PICK, False


def kit_pose(g):
    p = dict(yaw=0.38, pitch=0.30, expr="happy", head_roll=-3, lean=6, gaze=(0.55, 0.55),
             arm_l=dict(hand=(-0.42, 0.80), bend=0.5), legs="stand", t=g / 30.0)
    nod = sum(pulse(g, L - 1, L + 1, L + 5, 1.0) for L in LAND[:3])
    p["pitch"] = 0.30 + 0.25 * nod
    p["head_roll"] = -3 + 2 * math.sin(g * 0.15)
    # look up to the lens + wink
    ul = ez((g - G_LOOK[0]) / float(G_LOOK[1] - G_LOOK[0])) if g >= G_LOOK[0] else 0.0
    ub = ez((g - G_BACK[0]) / float(G_BACK[1] - G_BACK[0])) if g >= G_BACK[0] else 0.0
    us = ez((g - (LAND[3] - RISE[3])) / float(RISE[3])) if g >= LAND[3] - RISE[3] else 0.0
    ug = ez((g - G_GRIN) / 6.0) if g >= G_GRIN else 0.0
    yaw = lerp(lerp(lerp(lerp(0.38, 0.08, ul), -0.62, ub), 0.40, us), 0.12, ug)
    pitch = lerp(lerp(lerp(p["pitch"], -0.05, ul), 0.0, ub), 0.30, us)
    pitch = lerp(pitch, -0.10, ug)
    gx = lerp(lerp(lerp(lerp(0.55, 0.0, ul), -0.95, ub), 0.6, us), 0.05, ug)
    gy = lerp(lerp(lerp(lerp(0.55, 0.0, ul), -0.15, ub), 0.5, us), 0.0, ug)
    p.update(yaw=yaw, pitch=pitch, gaze=(gx, gy))
    if G_WINK[0] <= g <= G_WINK[1]:
        p["expr"] = "wink"
    elif g >= G_BACK[0] and g < G_GRIN:
        p["expr"] = "smirk"
    elif g >= G_GRIN:
        p["expr"] = "grinning"
    p["blink"] = blink(g, [14, G_GRIN - 2, 67])          # expression changes into the grin behind a blink
    p["lean"] = 6 + 6 * us * (1 - ug) - 2 * ul
    return p


def henry_pose(g):
    return dict(yaw=-0.45, pitch=-0.25, expr="unimpressed", head_roll=4 + 2 * math.sin(g * 0.08), gaze=(-0.5, -0.45),
                arm_l=dict(hand=(-0.62 - 0.03 * math.sin(g * 0.1), -0.32), bend=-0.7, stretch=1.25), prop_l="loaf",
                arm_r="akimbo", legs="wide", blink=blink(g, [24, 61]), t=g / 30.0)


# ----------------------------------------------------------------------------- the take
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=LENS, name="cam_s01")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        # the customer's basket: 5 drawings (9..13 loaves) on one card standing on the counter
        items = []
        for n in range(9, 14):
            svg, an = cast6.basket_svg("bk%d" % n, loaves=n)
            items.append((svg, (-0.56, -0.06, 0.56, 0.72), 512))
        self.basket_an = an
        pngs = C.svg_pngs(items, os.path.join(TMP, "props"))
        self.basket = C.PropCard("basket", pngs, (-0.56, -0.06, 0.56, 0.72), scale=BASKET_SCALE, shadow=True)
        self.place_basket(1)

    def place_basket(self, f):
        loc, _ = cam1(0)
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc)

    def top(self, k):
        """world point (on the basket card) where loaf k (0 = the 10th, 3 = the 13th) is put down: just above the pile."""
        x, y = [(-0.154, 0.192), (-0.013, 0.19), (0.131, 0.19), (0.014, 0.114)][k]   # = where that loaf is drawn in the next variant
        y -= HOVER                     # held just above its spot (the hand ball shows above the pile), dropped in on the swap
        return self.basket.to_world((x, y))

    def cam_of(self, shot, g):
        return cam1(g)

    def pose(self, shot, gs):
        kit, henry = self.actors["kit"], self.actors["henry"]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam1(g)
            self.key_cam(f, loc, look)
            C.place(kit, f, KIT, KIT_Z)
            C.place(henry, f, HENRY, 0.0)
            self.basket.show(count_at(g) - 9, frame=f)
            self.key_set(f, steam=STEAM, oven=1.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            pt, carry = hand_path(g, self.top)
            p = kit_pose(g)
            if carry:
                p["prop_r"] = LOAF
                hands = C.held_on_palm(kit, self.cam, f, pt, up=LOAF_UP, bend=-0.5, stretch=1.3)   # pin the hand, not the prop tip
            else:
                hands = {"r": {"hand": tuple(pt), "bend": -0.4, "stretch": 1.3}}
            _, inf = kit.pose(f, p, hands=hands, camera=self.cam)
            if os.environ.get("S01_DEBUG"):
                print("hand", g, carry, {k: (v.get("target"), v.get("reached"), v.get("error")) for k, v in inf.items() if isinstance(v, dict)}, flush=True)
            henry.pose(f, henry_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 448), (henry, 192)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam1(g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads=C.head_report(self, f), loaves=count_at(g))
        pt, carry = hand_path(g, self.top)
        out["hand_target_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(pt), f)[:2]]
        out["basket_rim_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(self.basket.to_world((0, 0.40))), f)[:2]]
        an = self.anch.get(("kit", f))
        if an:
            hx, hy = an["prop_tip_r"] if carry else an["hand_r"]
            hp = actors.local_to_screen(self.actors["kit"], self.cam, (hx, hy), f, self.actors["kit"].feet.get(f))
            out["hand_px"] = [round(hp[0], 1), round(hp[1], 1)]
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
