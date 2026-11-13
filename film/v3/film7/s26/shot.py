#!/usr/bin/env python3
"""shot.py -- film 7 take s26: shots 26-27 (85.77-91.49 s, g 2573..2744) + 6-frame handles (g 2567..2750), the Florence dealer's shop
(room / dealer_shop, SHOP_DAY, 1913).  Plan: 26 vincenzo_offer unwraps the panel on the dealer's desk, dealer_inspect; 27 dealer_signal,
police burst in, vincenzo_arrested.  Dissolve in (from shot 25, the attic).  Four set-ups (framing change every 1.4-1.6 s):

    id 1  g 2567..2614  two-shot over the desk: vincenzo (normal clothes, smug) pulls the wrapping cloth off the panel lying on the desk
                        (g 2586..2596), presents it with an open palm; the dealer behind the desk leans in.  Slow push.
    id 2  g 2615..2657  closer on the dealer (CUT on "เสนอขาย" 87.07): he holds the panel up at arm's length and inspects it through
                        his pince-nez (dealer_inspect); vincenzo in the right foreground, smug.  Slow push.
    id 3  g 2658..2700  shot 27 (CUT at 88.60): the panel back on the desk, vincenzo gloats down at it; behind his back the dealer winks and
                        beckons to screen-right (dealer_signal, the secret sign).  Slow push on the dealer.
    id 4  g 2701..2750  wide, the shop window on Florence (CUT on "แล้วพาตำรวจ" 90.01): two police agents burst in from screen-right,
                        the first grabs vincenzo's arm (police_arrest), vincenzo startled -> arrested (hands behind, head down); the dealer
                        stands by the panel.  A 4-frame bump of the camera on the burst.
Mouths: no quoted line in shots 26-27 -> no lip-sync; static expression mouths ('mouth' keys of the STORY poses are dropped).
NO depth of field anywhere (client rule): C.Take switches it off.

    python3 shot.py probe 1,2,3,4 a:b[:step]
    python3 shot.py stills 1,2,3,4 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2|3|4 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7, bpy = C.L, C.actors, C.camrig, C.cast7, C.bpy
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(85.77)              # 2573
G27 = C.g_bound(88.60)             # 2658
G1 = C.g_bound(91.49)              # 2745
H = 6
G_B = C.g_of(87.07 - 0.10)         # 2615 cut to the dealer on "เสนอขาย"
G_D = C.g_of(90.01 - 0.10) - 2     # 2701 police burst in on "แล้วพาตำรวจ"
RANGES = {1: (G0 - H, G_B - 1), 2: (G_B, G27 - 1), 3: (G27, G_D - 1), 4: (G_D, G1 + H - 1)}
UNWRAP = (2586, 2597)              # the cloth comes off (on "เขาเอาไป" 86.48 = g 2597 the panel is bare)
LIFT_B = (G_B, G_B + 8)            # setup 2 opens with the panel coming up into his hands
WINK = (2676, 2690)
GRAB = 2716

# ----------------------------------------------------------------------------- world (shop x -6..6, y 0..9; desk (-1.2, 3.4) top z 1.66)
DESK = Vector((-1.2, 3.4, 1.66))
PANEL_C = Vector((-1.2, 3.33, 1.82))      # centre of the panel lying on the desk (tilted up toward -y)
VIN = Vector((0.75, 2.8, 0.0))
DEALER = Vector((-1.35, 4.75, 0.0))
POL1_IN, POL2_IN = Vector((5.3, 1.2, 0.0)), Vector((5.5, 0.6, 0.0))
POL1_AT, POL2_AT = Vector((2.3, 1.5, 0.0)), Vector((2.8, 0.95, 0.0))
VIN4 = Vector((1.1, 2.2, 0.0))

CAMS = {   # (loc0, look0, loc1, look1, lens)
    1: ((0.0, 0.2, 3.2), (0.1, 4.6, 2.2), (-0.04, 0.5, 3.16), (0.02, 4.6, 2.15), 18.0),
    2: ((-0.05, 1.35, 3.35), (-1.75, 4.6, 2.6), (-0.2, 1.65, 3.33), (-1.8, 4.6, 2.6), 24.0),
    3: ((-0.35, 0.65, 3.05), (-1.15, 4.6, 2.75), (-0.50, 1.10, 3.02), (-1.25, 4.6, 2.78), 22.0),
    4: ((-3.1, 0.75, 3.15), (1.9, 3.5, 2.3), (-2.8, 0.95, 3.1), (1.9, 3.5, 2.3), 20.0),
}


def cam_of(shot, g):
    a, b = RANGES[shot]
    u = ez((g - a) / float(b - a), "sine")
    l0, k0, l1, k1, lens = CAMS[shot]
    loc, look = Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u))
    if shot == 4:                                   # bump on the door bursting open
        k = pulse(g, G_D, G_D + 1, G_D + 5, 1.0)
        loc += Vector((0.0, 0.0, 0.05 * k * math.sin(g * 2.7)))
        look += Vector((0.06 * k * math.sin(g * 1.9), 0.0, 0.04 * k))
    return loc, look, lens


def nomouth(p):
    p = dict(p); p.pop("mouth", None); return p


# ----------------------------------------------------------------------------- the cloth bundle (runtime prop, set module untouched)
def make_cloth():
    M = L.STATE['M']; SET = L.STATE['SET']
    mb = L.MB()
    # a folded wrapping cloth over the panel: a slightly bigger slab + a lumpy fold at the near edge
    mb.box((-0.62, -0.66, 0.0), (0.62, 0.52, 0.06), M['rag'], tile=(1, 1))
    L.lumpy(mb, (0.0, -0.62, 0.05), 0.14, M['rag'], 41, seg=10, rings=4, rough=0.2, squash=0.6)
    L.lumpy(mb, (0.45, 0.3, 0.07), 0.12, M['rag'], 42, seg=8, rings=4, rough=0.2, squash=0.5)
    ob = L._obj(mb, 's26_cloth', SET, hull=0.01)
    L.no_bounce(ob)
    ob.rotation_euler = (math.atan2(0.27, 0.95), 0.0, 0.0)       # same tilt as the panel (up toward -y)
    return ob


def key_cloth(ob, g, f):
    u = ez((g - UNWRAP[0]) / float(UNWRAP[1] - UNWRAP[0]), "sine")
    base = Vector((-1.2, 3.33, 1.84))
    if g < UNWRAP[0]:
        loc, rot, s = base, (math.atan2(0.27, 0.95), 0.0, 0.0), 1.0
    else:
        loc = base + Vector((1.85 * u, -0.55 * u, 0.55 * math.sin(math.pi * min(1.0, u * 1.2)) - 0.3 * u * u))
        rot = (math.atan2(0.27, 0.95) * (1 - u), -0.9 * u, 0.25 * u)
        s = lerp(1.0, 0.55, u)
    ob.location = loc; ob.rotation_euler = rot; ob.scale = (s, s * lerp(1.0, 0.6, u if g >= UNWRAP[0] else 0.0), 1.0)
    ob.hide_render = g > UNWRAP[1] + 1
    for path in ("location", "rotation_euler", "scale", "hide_render"):
        ob.keyframe_insert(path, frame=f)
    return loc


# ----------------------------------------------------------------------------- poses
def vin_pose(shot, g):
    t = g / 30.0
    if shot in (1, 2):
        p = dict(yaw=0.45, pitch=-0.05, expr="smug", head_roll=-4 + 1.5 * math.sin(g * 0.2), gaze=(0.85, 0.15),
                 arm_l=dict(hand=(-0.2, 0.82), bend=0.6), legs="stand", lean=1.5 * math.sin(g * 0.15))
        if shot == 1 and g >= UNWRAP[1] + 2:                      # presents the bare panel with the open palm
            u = ez((g - UNWRAP[1] - 2) / 6.0)
            p["arm_r"] = dict(hand=(lerp(0.3, 0.62, u), lerp(0.55, 0.32, u)), shape="open", bend=-0.4, stretch=1.2)
            p["expr"] = "grinning" if g > UNWRAP[1] + 4 else "smug"
        elif shot == 2:
            p["arm_r"] = dict(hand=(0.25, 0.72), bend=0.5)
            p["arm_l"] = dict(hand=(-0.05, 0.62), bend=0.8)   # rubbing his hands at the belly
            p["gaze"] = (0.8, -0.25)
            p["blink"] = blink(g, [2632])
        p["blink"] = p.get("blink", blink(g, [2578, 2604]))
    elif shot == 3:
        p = dict(yaw=0.4, pitch=0.35, expr="smug", head_roll=-6 + 2 * math.sin(g * 0.18), gaze=(0.5, 0.8),
                 arm_r=dict(hand=(0.25, 0.7), bend=0.5), arm_l=dict(hand=(-0.18, 0.75), bend=0.6), legs="stand",
                 lean=3.0 + 1.0 * math.sin(g * 0.15))
        p["blink"] = blink(g, [2668, 2694])
    else:
        if g < G_D + 4:
            p = dict(yaw=0.4, pitch=0.3, expr="smug", gaze=(0.5, 0.8), head_roll=-6, arm_r=dict(hand=(0.25, 0.7), bend=0.5),
                     arm_l=dict(hand=(-0.18, 0.75), bend=0.6), legs="stand", lean=3.0)
        elif g < GRAB:                                         # startled: turns to the police (screen-right)
            u = ez((g - G_D - 4) / 4.0)
            p = dict(yaw=lerp(0.4, -0.35, u), pitch=-0.1, expr="shocked", gaze=(lerp(0.5, -0.9, u), 0.0), head_roll=4,
                     arm_r=dict(hand=(0.42, 0.25), shape="open", bend=-0.6), arm_l=dict(hand=(-0.42, 0.25), shape="open", bend=-0.6),
                     legs="narrow", sweat=0.7, lean=-4 * u)
            p["mirror"] = False
        else:
            p = nomouth(cast7.STORY7["vincenzo_arrested"][1])
            p["sweat"] = 0.6
            p["head_roll"] = 6 + 1.5 * math.sin(g * 0.3)
            p["mirror"] = False
            p["blink"] = blink(g, [2730])
        if g < G_D + 4 or "mirror" not in p:
            p["mirror"] = True
    if shot in (1, 2, 3):
        p["mirror"] = True                                     # faces screen-left, toward the dealer
    if shot == 4 and g < G_D + 4:
        p["mirror"] = True
    p["t"] = t
    return p


def dealer_pose(shot, g):
    t = g / 30.0
    if shot == 1:
        p = nomouth(cast7.STORY7["dealer_smile"][1])
        p["mirror"] = True                                     # faces screen-right (vincenzo)
        if g >= UNWRAP[1] - 2:                                 # leans in over the bare panel, stunned
            u = ez((g - UNWRAP[1] + 2) / 8.0)
            p.update(expr="stunned", pitch=lerp(-0.1, 0.35, u), lean=lerp(0, 9, u), gaze=(0.3, 0.8),
                     arm_l=dict(hand=(lerp(-0.6, -0.35, u), lerp(0.3, 0.55, u)), shape="open", bend=-0.4),
                     arm_r=dict(hand=(0.35, 0.55), shape="open", bend=-0.4))
        p["blink"] = blink(g, [2580])
    elif shot == 2:
        p = nomouth(cast7.STORY7["dealer_inspect"][1])
        p["prop_l"] = dict(type="mona_panel", scale=1.35)
        p["head_roll"] = 6 + 2.0 * math.sin(g * 0.12)
        p["lean"] = 6 + 1.5 * math.sin(g * 0.1)
        if g < LIFT_B[1]:                                       # the panel comes up into view
            u = ez((g - LIFT_B[0]) / float(LIFT_B[1] - LIFT_B[0]))
            p["arm_l"] = dict(p["arm_l"], hand=(lerp(-0.45, -0.58, u), lerp(0.75, 0.3, u)))
        p["blink"] = blink(g, [2640])
        p["mirror"] = False
    elif shot == 3:
        p = nomouth(cast7.STORY7["dealer_signal"][1])
        u = clamp((g - WINK[0]) / 4.0)
        if g < WINK[0]:                                        # straightens up, a polite smile at vincenzo
            p.update(expr="happy", yaw=-0.3, gaze=(-0.6, 0.2), arm_r=dict(hand=(0.3, 0.6), bend=0.5),
                     arm_l=dict(hand=(-0.25, 0.6), bend=0.5))
            p["mirror"] = True
        else:
            beck = math.sin((g - WINK[0]) * 0.9)
            p["arm_r"] = dict(p["arm_r"], hand=(0.75, 0.28 - 0.12 * beck))   # the beckoning fingers
            p["expr"] = "wink" if g < WINK[1] + 6 else "smirk"
            p["mirror"] = False
        p["blink"] = blink(g, [2664])
    else:
        p = nomouth(cast7.STORY7["dealer_smile"][1])
        p.update(expr="smirk", arm_l=dict(hand=(-0.3, 0.55), bend=0.5), arm_r="akimbo", yaw=0.3)
        p["mirror"] = False
        p["blink"] = blink(g, [2712, 2740])
    if shot == 1:
        p["mirror"] = True
    p["t"] = t
    return p


def pol_pos(k, g):
    a, b = (POL1_IN, POL1_AT) if k == 1 else (POL2_IN, POL2_AT)
    g0 = G_D - 1 + (0 if k == 1 else 4)
    u = clamp((g - g0) / 13.0)
    u = 1 - (1 - u) ** 2                                       # runs in, brakes
    return a.lerp(b, u)


def pol_pose(k, g):
    g0 = G_D - 1 + (0 if k == 1 else 4)
    arrived = g >= g0 + 13
    if not arrived:
        base = dict(expr="determined", yaw=0.7)
        p = cast7.cycle("police", (g - g0) / 16.0 + 0.25 * k, "run", facing=-1, base=base, speed=1.0)
    elif k == 1:
        p = nomouth(cast7.STORY7["police_arrest"][1])
        p["mirror"] = False
        p["arm_r"] = dict(hand=(0.35, -0.45), shape="point", bend=-1.0, stretch=1.2)
    else:
        p = nomouth(cast7.STORY7["police_stand"][1])
        p.update(yaw=-0.45, arm_l=dict(hand=(-0.55, 0.45), shape="open", bend=-0.5), mirror=False)
    p["blink"] = blink(g, [2735 + 3 * k])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "room", "dealer_shop", quality=quality, lens=CAMS[shot][4], name="cam_s26_%d" % shot)
        self.shot = shot
        sd = os.path.join(TMP, "sprites")
        self.cloth = make_cloth() if shot == 1 else None
        self.actors["vin"] = C.make_actor("vin", "vincenzo", sd)
        self.actors["dealer"] = C.make_actor("dealer", "dealer", sd)
        if shot == 4:
            self.actors["pol1"] = C.make_actor("pol1", "police", sd)
            self.actors["pol2"] = C.make_actor("pol2", "police", sd)

    def pose(self, shot, gs):
        assert shot == self.shot
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            panel_on_desk = not (shot == 2)
            self.key_set(f, panel=panel_on_desk)
            C.place(A["vin"], f, VIN4 if shot == 4 else VIN)
            C.place(A["dealer"], f, DEALER if shot != 2 else DEALER + Vector((0.25, -0.2, 0)))
            if shot == 1:
                key_cloth(self.cloth, g, f)
            if shot == 4:
                C.place(A["pol1"], f, pol_pos(1, g)); C.place(A["pol2"], f, pol_pos(2, g))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            hands = None
            vp = vin_pose(shot, g)
            if shot == 1 and UNWRAP[0] - 3 <= g <= UNWRAP[1]:        # his hand on the cloth's near corner, pulling it off
                cl = self.cloth.matrix_world @ Vector((0.45, -0.55, 0.06))
                hands = {"r": {"hand": tuple(cl)}}
                vp["arm_r"] = dict(hand=(0.4, 0.5), shape="ball", bend=-0.3)
            A["vin"].pose(f, vp, hands=hands, camera=self.cam)
            A["dealer"].pose(f, dealer_pose(shot, g), camera=self.cam)
            if shot == 4:
                hp = None
                if g >= GRAB:                                         # the agent's open hand grips vincenzo's upper arm
                    hp = {"l": {"hand": tuple(VIN4 + Vector((0.25, -0.05, 1.45)))}}
                A["pol1"].pose(f, pol_pose(1, g), hands=hp, camera=self.cam)
                A["pol2"].pose(f, pol_pose(2, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 320) for a in A.values()], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
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
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: shot)
