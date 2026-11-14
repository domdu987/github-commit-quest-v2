#!/usr/bin/env python3
"""shot.py -- film 6b take s13: shots 13-16 (plan 20.74-32.15 s = g 622..963) + 6 handle frames each side (g 616..969).

Internal shots (= plan shot numbers; Blender frame = common.bf(shot, g)):
  13  market MORNING  g 616..734  A (616..667): low push past a jeering farmer onto a row of THREE EMPTY pillories under the
                                  notice "ห้ามขายขาดน้ำหนัก!", guards at both ends ("แล้วร้านขนมปังในเมืองก็โดนจับทีละร้าน").
                                  B (668..734): frontal on the row; heads pop into the pillories one, two, three exactly on the
                                  spoken "หนึ่ง" (g 697) "สอง" (g 712) "สาม" (g 724), each with a yellow Thai count word popping
                                  above it and a camera bump toward it.
  14  market MORNING  g 735..796  CU truck along the pilloried bakers: crying, sweating, waving open hands, then punch-in on the
                                  middle baker, speech bubble "ชั่งเป๊ะ!" pops on "เป๊ะ" (g 787).  (the bakers swear)
  15  bakery MORNING  g 797..878  low MCU Henry behind the counter: belly laugh (eyes shut, tears, body bounce, mouth a still grin)
                                  797..841; punch-in to CU 842..878 with lip-sync on "พวกขี้โกงทั้งนั้น!" (28.0-29.2 s,
                                  talk_mouth g 842..874), smug half-lids, wagging finger.
  16  bakery MORNING  g 879..969  ECU along three customer baskets on the counter: Henry's hand plucks the PALE 13th loaf off
                                  the top of basket after basket (g 893, 914, 935); camera slides basket to basket; last beat
                                  widens to kit behind the counter at screen-right, deadpan, watching (g 945..969).
Mouths: only Henry's lip-sync in shot 15 moves; all other mouths are fixed drawings.  NO depth of field.

    python3 shot.py probe 13 616:734:10
    python3 shot.py stills 13 616:734:10 <out_dir> [scale] [samples]
    python3 shot.py final 13,14 616:969 [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
sys.path.insert(0, FILM6)
sys.path.insert(0, HERE)
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import signs                                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing (film 6b clock)
G0, G1 = 622, 964                  # plan 20.74 / 32.15 s
H = 6
RANGES = {13: (G0 - H, 734), 14: (735, 796), 15: (797, 878), 16: (879, G1 + H - 1)}
MARKET, BAKERY = (13, 14), (15, 16)
G_B = 668                          # shot 13 second framing
POPS = [697, 712, 724]             # หนึ่ง 23.12 s, สอง 23.63, สาม 24.02 (voiced onsets in narration.wav) -> +0.1 s
G_PUNCH14 = 772
G_PET = g_of(26.12)                # 787 "เป๊ะ"
G_LIP = (g_of(27.98), g_of(29.24)) # 842..874
PLUCK = [893, 914, 935]
G_KIT = 945

# ----------------------------------------------------------------------------- market staging
# the three pillories stand on a diagonal (far-left -> near-right as seen from the south-east), so the count builds toward us
ROW = [Vector((-5.9, 10.6)), Vector((-3.9, 9.4)), Vector((-1.9, 8.2))]
ROW_D = (ROW[2] - ROW[0]).normalized()                     # along the row (toward the camera side)
ROW_N = Vector((ROW_D.y, -ROW_D.x))                        # normal, pointing west-south-west (shot-14 camera side)
SIGN_AT = Vector((-4.0, 12.2))                             # beam + plank behind the far pillory
GUARDS = [("guard1", (-7.6, 12.9)), ("guard2", (0.5, 9.4))]
FARMER = (-1.9, 4.5)
WOMAN = (-7.4, 9.0)
B_CAM = Vector((-4.2, 2.8, 2.6)); B_LOOK = Vector((-3.9, 9.6, 2.95))


def cam13(g):
    if g < G_B:
        u = ez((g - RANGES[13][0]) / float(G_B - RANGES[13][0]), "sine")
        loc = lerp((2.2, 1.6, 1.55), (0.6, 4.0, 2.1), u)
        look = lerp((-3.7, 9.8, 2.9), (-3.9, 9.6, 2.85), u)
        return Vector(loc), Vector(look), 22.0
    u = ez((g - G_B) / float(734 - G_B), "sine")
    loc = B_CAM + (B_LOOK - B_CAM).normalized() * (0.6 * u)
    look = B_LOOK.copy()
    # punch: a quick 3-frame bump toward the popping head, eases back over 10 frames
    off = Vector((0, 0, 0)); aim = Vector((0, 0, 0))
    for k, p in enumerate(POPS):
        if p - 1 <= g < p + 13:
            a = (g - (p - 1)) / 3.0 if g < p + 2 else 1.0 - ez((g - (p + 2)) / 10.0)
            a = clamp(a)
            tgt = Vector((ROW[k].x, ROW[k].y, 2.7))
            off += (tgt - loc).normalized() * 0.55 * a
            aim += (tgt - look) * 0.25 * a
    return loc + off, look + aim, 22.0


def _row_pt(t):
    """point on the row line, t = 0 at pillory 1, 1 at pillory 2, 2 at pillory 3."""
    i = min(1, int(t)); f = t - i
    return ROW[i].lerp(ROW[i + 1], f)


def cam14(g):
    """CU truck along the bakers, camera on the east-north-east side of the row (billboards face it); punch-in on baker 2."""
    if g < G_PUNCH14:
        u = ez((g - 735) / float(G_PUNCH14 - 735), "sine")
        p = _row_pt(lerp(1.9, 1.2, u))
        c = p + ROW_N * 3.1
        return Vector((c.x, c.y, 2.74)), Vector((p.x, p.y, 2.66)), 24.0
    u = ez((g - G_PUNCH14) / 6.0, "back_out") if g < G_PUNCH14 + 6 else 1.0
    u2 = (g - G_PUNCH14) / float(796 - G_PUNCH14)
    p = ROW[1] + ROW_D * 0.22
    c = p + ROW_N * (lerp(2.4, 1.85, u) - 0.12 * u2)
    return Vector((c.x, c.y, 2.72)), Vector((p.x, p.y, 2.62)), 24.0


# ----------------------------------------------------------------------------- bakery staging
HENRY15 = (2.0, 2.05)
BASKET_X = [-0.9, 0.45, 1.8]
BASKET_Y = 1.05
BASKET_SC = 1.4
KIT16 = (3.05, 1.65)
KIT_Z = 0.98
AIM16 = Vector((-0.17, 0.0, 0.03))      # IK aim correction (measured: hand lands ~100 px screen-right of the target)


def cam15(g):
    if g < G_LIP[0]:
        u = ez((g - 797) / float(G_LIP[0] - 797), "sine")
        loc = lerp((2.45, -0.05, 1.66), (2.32, 0.30, 1.76), u)
        return Vector(loc), Vector((2.0, 2.05, 2.30)), 22.0
    u = ez((g - G_LIP[0]) / 5.0, "back_out") if g < G_LIP[0] + 5 else 1.0
    u2 = (g - G_LIP[0]) / float(878 - G_LIP[0])
    loc = lerp((2.30, 0.45, 1.95), (2.22, 0.62, 2.0), u2)
    return Vector(loc), Vector((2.0, 2.05, 2.48)), 22.0


def basket_focus(g):
    """which basket the camera centres on (float index): holds on k around its pluck, slides between."""
    if g < PLUCK[0] + 6:
        return 0.0
    if g < PLUCK[1] - 6:
        return ez((g - (PLUCK[0] + 6)) / float(PLUCK[1] - 12 - PLUCK[0]), "sine")
    if g < PLUCK[1] + 6:
        return 1.0
    if g < PLUCK[2] - 6:
        return 1.0 + ez((g - (PLUCK[1] + 6)) / float(PLUCK[2] - 12 - PLUCK[1]), "sine")
    return 2.0


def cam16(g):
    k = basket_focus(g)
    i = min(1, int(k)); f = k - i
    x = lerp(BASKET_X[i], BASKET_X[i + 1], f) if k < 2 else BASKET_X[2]
    loc = Vector((x + 0.18, -0.30, 2.62)); look = Vector((x, 1.2, 2.02))
    if g >= G_KIT:                                       # widen to the kit two-shot
        u = ez((g - G_KIT) / 8.0, "back_out") if g < G_KIT + 8 else 1.0
        u2 = (g - G_KIT) / float(RANGES[16][1] - G_KIT)
        loc = Vector(lerp(tuple(loc), (2.75 + 0.1 * u2, -0.45 + 0.12 * u2, 2.55), u)); look = Vector(lerp(tuple(look), (2.45, 1.3, 2.25), u))
    return loc, look, 22.0


CAMS = {13: cam13, 14: cam14, 15: cam15, 16: cam16}

# ----------------------------------------------------------------------------- poses
WRIST = cast6.PILLORY_WRIST_Y


def baker_pose(k, g):
    """baker k (0, 1, 2) in his pillory at film frame g."""
    base = dict(yaw=[0.12, -0.05, -0.15][k], pitch=0.15, legs="narrow", pillory=True, t=g / 30.0,
                arm_r=dict(hand=(0.56, WRIST), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, WRIST), bend=-0.6, stretch=1.3))
    if g < 735:                                           # shot 13: pop in, stunned
        dp = g - POPS[k]
        base.update(expr=["shocked", "stunned", "shocked"][k], head_roll=[-6, 4, 8][k], fx=["sweat"])
        if 0 <= dp < 3:
            base["squash"] = [(1.12, 0.88), (0.94, 1.08), (1.03, 0.97)][dp]
        if dp >= 6:
            base["expr"] = ["sad", "worried", "sad"][k]
            base["fx"] = ["tears"] if k != 1 else ["sweat"]
        base["blink"] = blink(g, [POPS[k] + 14])
        return base
    # shot 14: swearing -- crying, sweating, hands waving open in the wrist holes, heads shaking
    ph = g * 0.55 + k * 1.7
    base.update(expr=["sad", "worried", "sad"][k], fx=["tears", "sweat"], head_roll=8 * math.sin(ph) * (1 if k != 1 else 0.6),
                yaw=base["yaw"] + 0.10 * math.sin(ph * 0.5))
    for s, side in ((1, "arm_r"), (-1, "arm_l")):
        base[side] = dict(hand=(0.56 * s, WRIST), bend=-0.6, stretch=1.3)
        if math.sin(ph * 1.3 + s) > 0:
            base[side]["shape"] = "open"
    if k == 1 and g >= G_PET - 2:
        base.update(expr="determined", fx=["sweat"], head_roll=-4, pitch=-0.05)
    base["blink"] = blink(g, [748 + 9 * k, 780 + 5 * k])
    return base


def henry15_pose(g):
    if g < G_LIP[0]:                                      # belly laugh, mouth a still grin
        ph = (g - 797) * 0.95
        b = math.sin(ph)
        return dict(yaw=0.18, pitch=-0.42 + 0.06 * b, expr="laughing", blink=2, fx=["tears"], head_roll=10 + 4 * b, lean=-6,
                    head_dy=0.03 + 0.03 * abs(b), squash=(1.0 + 0.03 * abs(b), 1.0 - 0.03 * abs(b)), t=g / 30.0,
                    arm_r=dict(hand=(0.36, 1.10 - 0.04 * abs(b)), bend=0.9), arm_l=dict(hand=(-0.40, 1.06 - 0.04 * abs(b)), bend=0.9),
                    legs="wide")
    # "พวกขี้โกงทั้งนั้น!": smug half-lids, lip-sync, a finger wagging up by the face
    talking = G_LIP[0] <= g <= G_LIP[1]
    w = math.sin((g - G_LIP[0]) * 0.75)
    p = dict(yaw=0.22, pitch=-0.30, expr="smug", head_roll=-6 + 3 * w, lean=-3, t=g / 30.0, legs="wide",
             mouth=cast6.talk_mouth(g, 1.0, seed=15) if talking else "smirk",
             arm_l=dict(hand=(-0.40, 1.06), bend=0.9),
             arm_r=dict(hand=(0.62 + 0.10 * w, -0.30), shape="point", bend=-0.9, stretch=1.25), blink=blink(g, [G_LIP[1] + 2]))
    return p


def kit16_pose(g):
    return dict(yaw=-0.35, pitch=0.10, expr="unimpressed", head_roll=4, gaze=(-0.8, 0.35), t=g / 30.0, legs="stand",
                arm_l=dict(hand=(-0.30, 0.82), bend=0.6), arm_r=dict(hand=(0.30, 0.82), bend=-0.6),
                blink=blink(g, [955]))


# pale 13th loaf: cast6 draws loaves from BREAD; swap in paler colours while the 13th loaf is drawn
PALE = dict(light="#fff6dc", base="#f3dca8", dark="#cfa468", crust="#b98a4c", score="#fff4d8", flour="#ffffff")


class pale_bread(object):
    def __enter__(self):
        self.old = dict(cast6.BREAD); cast6.BREAD.update(PALE)

    def __exit__(self, *a):
        cast6.BREAD.update(self.old)


def pale_prop_patch():
    """henry's held loaf in shot 16 is always the pale 13th: wrap cast6._prop so the loaf prop draws pale."""
    if getattr(cast6, "_s13_patched", False):
        return
    orig = cast6._prop

    def _prop(k, kind, Hh, ang, sc=1.0):
        if kind == "loaf":
            with pale_bread():
                return orig(k, kind, Hh, ang, sc)
        return orig(k, kind, Hh, ang, sc)
    cast6._prop = _prop
    cast6._s13_patched = True


def basket_with_pale(uid, pale_on_top):
    svg, an = cast6.basket_svg(uid, loaves=12)
    if pale_on_top:
        with pale_bread():
            lf = cast6.loaf_svg(uid + "p", r=cast6.BASKET_LR, seed=4)
        svg += '<g transform="translate(0.02 %.4f) rotate(-8)">%s</g>' % (cast6.BASKET_HANDLE - 0.270, lf)
    return svg


# ----------------------------------------------------------------------------- takes
class MarketTake(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "MORNING", quality=quality, lens=22.0, name="cam_s13m")
        self.scene.frame_end = 20000
        for nm in ("pillory", "pillory_lamps", "pillory_lamp_glass", "pillory_halos"):
            ob = bpy.data.objects.get(nm)
            if ob is not None:
                ob.hide_render = True
        for ob in bpy.data.objects:
            if ob.name.startswith("pillory_lamp_") and ob.type == "LIGHT":
                ob.hide_render = True
        sd = os.path.join(TMP, "sprites_m")
        for k in range(3):
            self.actors["baker%d" % k] = C.make_actor("baker%d" % k, "baker2", sd)
        for nm, xy in GUARDS:
            self.actors[nm] = C.make_actor(nm, nm, sd)
        self.actors["man1"] = C.make_actor("man1", "man1", sd)
        self.actors["woman1"] = C.make_actor("woman1", "woman1", sd)
        # empty pillories (pillory_svg), the notice plank with its beam + posts, count words, speech bubble
        sv, self.pl_an = cast6.pillory_svg("pl13", post_h=2.30)
        box = (-0.95, -0.06, 0.95, 0.30 + 2.30 + 0.04)
        png = C.svg_pngs([(sv, box, 300)], os.path.join(TMP, "props"))
        self.empty = [C.PropCard("empty%d" % k, png, box, scale=1.0, shadow=True) for k in range(3)]
        sg = os.path.join(TMP, "signs"); os.makedirs(sg, exist_ok=True)
        w, h = signs.plank("ห้ามขายขาดน้ำหนัก!", os.path.join(sg, "plank.png"))
        sw = 3.6
        self.plank = C.PropCard("plank", [os.path.join(sg, "plank.png")], (-sw / 2, -sw * h / w, sw / 2, 0.0), shadow=True)
        beam_svg = ('<g><rect x="-2.25" y="0" width="4.5" height="0.16" rx="0.03" fill="#7a5230" stroke="#2a1a2e" stroke-width="0.03"/>'
                    '<rect x="-2.2" y="0" width="0.16" height="5.15" fill="#6a4628" stroke="#2a1a2e" stroke-width="0.03"/>'
                    '<rect x="2.04" y="0" width="0.16" height="5.15" fill="#6a4628" stroke="#2a1a2e" stroke-width="0.03"/>'
                    '<path d="M-1.4,0.16 L-1.4,0.42 M1.4,0.16 L1.4,0.42" stroke="#3a2a20" stroke-width="0.035"/></g>')
        bbox = (-2.27, -0.02, 2.27, 5.17)
        self.beam = C.PropCard("beam", C.svg_pngs([(beam_svg, bbox, 100)], os.path.join(TMP, "props")), bbox, shadow=True)
        self.pops = []
        for k, t in enumerate(("หนึ่ง!", "สอง!", "สาม!")):
            p = os.path.join(sg, "pop%d.png" % k); w, h = signs.pop(t, p)
            pw = 1.15
            self.pops.append(C.PropCard("pop%d" % k, [p], (-pw / 2, -pw * h / w, pw / 2, 0.0), shadow=False))
        p = os.path.join(sg, "bubble.png"); w, h = signs.bubble("ชั่งเป๊ะ!", p, tail="left")
        bw = 0.72
        self.bubble = C.PropCard("bubble", [p], (0.0, -bw * h / w, bw, 0.0), shadow=False)
        self.placed = False

    def place_props(self, f):
        """the empty pillory boards line up with the baker's drawn board (anchor pillory_top of a posed baker)."""
        cam = self.cam.location.copy()
        mw = self.cam.matrix_world
        right, up = Vector(mw.col[0][:3]).normalized(), Vector(mw.col[1][:3]).normalized()
        self.heads = []
        for k in range(3):
            a = self.actors["baker%d" % k]
            an = self.anch.get((a.name, f))
            top = actors.local_to_world(a, an["pillory_top"], f) if an and "pillory_top" in an else None
            hd = actors.local_to_world(a, an["head"], f) if an and "head" in an else Vector((ROW[k].x, ROW[k].y, 2.7))
            self.heads.append(hd)
            z = top.z if top is not None else 2.30
            self.empty[k].put((ROW[k].x, ROW[k].y - 0.01, z), face=cam)
            self.pops[k].put(hd + Vector((0, 0, 0.62)), face=cam)
        self.plank.put((SIGN_AT.x, SIGN_AT.y - 0.02, 3.96), face=(B_CAM.x, B_CAM.y, 3.0))
        self.beam.put((SIGN_AT.x, SIGN_AT.y + 0.03, 5.12), face=(B_CAM.x, B_CAM.y, 3.0))
        self.bubble.put(self.heads[1] + right * 0.12 + up * 0.52, face=cam)

    def cam_of(self, shot, g):
        return CAMS[shot](g)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = CAMS[shot](g)
            self.key_cam(f, loc, look, lens)
            for k in range(3):
                C.place(self.actors["baker%d" % k], f, tuple(ROW[k]))
            for nm, xy in GUARDS:
                C.place(self.actors[nm], f, xy)
            C.place(self.actors["man1"], f, FARMER)
            C.place(self.actors["woman1"], f, WOMAN)
            self.key_set(f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for k in range(3):
                self.actors["baker%d" % k].pose(f, baker_pose(k, g), camera=self.cam)
            gp = cast6.STORY6["guard_stand"][1]; gp2 = cast6.STORY6["guard_stand_guard2"][1]
            self.actors["guard1"].pose(f, dict(gp, yaw=0.35, blink=blink(g, [650, 760])), camera=self.cam)
            self.actors["guard2"].pose(f, dict(gp2, yaw=-0.35, mirror=True, blink=blink(g, [700])), camera=self.cam)
            mp = dict(cast6.STORY6["town_laugh_man1"][1]); mp.update(mirror=False, t=g / 30.0, head_roll=-10 + 4 * math.sin(g * 0.9), blink=2)
            self.actors["man1"].pose(f, mp, camera=self.cam)
            wp = dict(cast6.STORY6["town_point"][1]); wp.update(yaw=0.5, mouth="smirk", t=g / 30.0)
            self.actors["woman1"].pose(f, wp, camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(self.actors["baker%d" % k], 288 if shot == 14 else 192) for k in range(3)]
        jobs += [(self.actors[n], 144) for n in ("guard1", "guard2", "man1", "woman1")]
        self.sprites_for(jobs, fr)

    def set_visible(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        self.place_props(f)
        popped = [g >= p for p in POPS] if shot == 13 else [True] * 3
        for k in range(3):
            self.actors["baker%d" % k].set_hidden(not popped[k])
            self.empty[k].show(None if popped[k] else 0)
            # count words: pop with an overshoot, stay; hidden in shot 14
            if shot == 13 and g >= POPS[k]:
                d = g - POPS[k]
                s = [0.4, 1.25, 1.1, 1.0][min(d, 3)]
                self.pops[k].root.scale = (s, s, s); self.pops[k].show(0)
            else:
                self.pops[k].show(None)
        for nm in ("guard1", "guard2", "woman1"):
            self.actors[nm].set_hidden(shot == 14)
        self.actors["man1"].set_hidden(not (shot == 13 and g < G_B))
        self.plank.show(0 if shot == 13 else None)
        self.beam.show(0 if shot == 13 else None)
        if shot == 14 and g >= G_PET:
            d = g - G_PET
            s = [0.4, 1.2, 1.05, 1.0][min(d, 3)]
            self.bubble.root.scale = (s, s, s); self.bubble.show(0)
        else:
            self.bubble.show(None)

    def report(self, shot, g):
        f = bf(shot, g)
        self.set_visible(shot, g)
        loc, look, lens = CAMS[shot](g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        out = []
        for g in gs:
            self.set_visible(shot, g)
            out += C.Take.render(self, [bf(shot, g)], out_dir, scale=scale, samples=samples, threads=threads)
        return out


class BakeryTake(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=22.0, name="cam_s13b")
        self.scene.frame_end = 20000
        pale_prop_patch()
        sd = os.path.join(TMP, "sprites_b")
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        self.actors["kit"] = C.make_actor("kit", "kit", sd, (-1.5625, -3.875, 1.5625, 0.1875))
        box = (-0.56, -0.06, 0.56, 0.72)
        pngs = C.svg_pngs([(basket_with_pale("bk13", True), box, 512), (basket_with_pale("bk12", False), box, 512)],
                          os.path.join(TMP, "props"))
        self.baskets = [C.PropCard("basket%d" % k, pngs, box, scale=BASKET_SC, shadow=True) for k in range(3)]
        for ob in bpy.data.objects:                      # the hand balance would stand in front of henry: out of this take
            if ob.name.startswith("small_"):
                ob.hide_render = True
        self.cool_light()

    def cool_light(self):
        """complementary colour: a cool blue window fill from screen-right/street on the counter + henry (the warm bakery's
        counter-colour, DIRECTOR_REVIEW 7)."""
        ld = bpy.data.lights.new("s13_cool", "AREA")
        ld.energy = 900.0; ld.color = (0.40, 0.58, 1.0); ld.size = 2.5
        ob = bpy.data.objects.new("s13_cool", ld)
        self.scene.collection.objects.link(ob)
        ob.location = (5.2, -0.4, 3.4)
        d = Vector((1.6, 1.4, 1.8)) - ob.location
        ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

    def cam_of(self, shot, g):
        return CAMS[shot](g)

    def henry16_loc(self, g):
        """henry walks along behind the counter from basket to basket (x follows the next pluck)."""
        k = basket_focus(g)
        i = min(1, int(k)); f = k - i
        x = lerp(BASKET_X[i], BASKET_X[i + 1], f) if k < 2 else BASKET_X[2]
        return (x - 0.10, 1.62)

    def hand16(self, g):
        """(world point of the held loaf centre or None, holding?) for henry's screen-right hand."""
        for k, p in enumerate(PLUCK):
            top = self.baskets[k].to_world((0.02, cast6.BASKET_HANDLE - 0.270))
            if p - 5 <= g < p:                           # reach: from above down to just over the loaf (empty hand)
                u = ez((g - (p - 5)) / 5.0, "sine")
                return top + Vector((0.15 * (1 - u), -0.05, 0.60 * (1 - u) + 0.05)), False
            if p <= g < p + 12:                          # pluck: lifted up and out to screen-left, held there smugly
                u = ez((g - p) / 6.0, "back_out")
                return top + Vector((-0.28 * u, 0.10 * u, 0.30 * u)), True
            if p + 12 <= g < p + 16:                     # and dropped down behind the counter (out of the shot)
                u = ez((g - (p + 12)) / 4.0, "quad_in")
                return top + Vector((-0.28 - 0.1 * u, 0.10, 0.30 - 0.9 * u)), True
        return None, False

    def pose(self, shot, gs):
        henry, kit = self.actors["henry"], self.actors["kit"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = CAMS[shot](g)
            self.key_cam(f, loc, look, lens)
            if shot == 15:
                C.place(henry, f, HENRY15)
            else:
                C.place(henry, f, self.henry16_loc(g))
            C.place(kit, f, KIT16, KIT_Z)
            self.key_set(f, steam=0.35 if shot == 16 else 0.2)
        for k in range(3):
            self.baskets[k].put((BASKET_X[k], BASKET_Y, 1.25 + 0.66 * BASKET_SC), face=(BASKET_X[k], -6.0, 2.0))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 15:
                henry.pose(f, henry15_pose(g), camera=self.cam)
            else:
                pt, hold = self.hand16(g)
                p = dict(yaw=0.30, pitch=0.35, expr="smug", head_roll=-6 + 2 * math.sin(g * 0.2), lean=10, t=g / 30.0, legs="stand",
                         gaze=(0.3, 0.7), arm_l=dict(hand=(-0.40, 1.04), bend=0.6), blink=blink(g, [905, 948]))
                hands = None
                if pt is not None:
                    if hold:
                        p["prop_r"] = dict(type="loaf", scale=0.6)
                        hands = C.held_on_palm(henry, self.cam, f, pt + AIM16, up=C.LOAF_TIP * 0.6, bend=-0.5, stretch=1.45, layer="top")
                    else:
                        lx, ly = actors.world_to_local(henry, self.cam, tuple(pt + AIM16), f)
                        hands = {"r": dict(hand=(lx, ly + 0.05), bend=-0.5, stretch=1.45, shape="open", layer="top")}
                else:
                    p["arm_r"] = dict(hand=(0.40, 1.04), bend=-0.6)
                henry.pose(f, p, hands=hands, camera=self.cam)
                kit.pose(f, kit16_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        if shot == 15:
            self.sprites_for([(henry, 416)], fr)
        else:
            self.sprites_for([(henry, 320), (kit, 320)], fr)

    def count(self, k, g):
        return 1 if g >= PLUCK[k] else 0

    def set_visible(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        self.actors["kit"].set_hidden(shot != 16)
        for k in range(3):
            self.baskets[k].show(self.count(k, g) if shot == 16 else None)

    def report(self, shot, g):
        f = bf(shot, g)
        self.set_visible(shot, g)
        loc, look, lens = CAMS[shot](g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f))
        if shot == 16:
            pt, hold = self.hand16(g)
            if pt is not None:
                out["hand_target_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(pt), f)[:2]]
                an = self.anch.get(("henry", f))
                if an:
                    hx, hy = an["prop_tip_r"] if hold else an["hand_r"]
                    hp = actors.local_to_screen(self.actors["henry"], self.cam, (hx, hy), f)
                    out["hand_px"] = [round(hp[0], 1), round(hp[1], 1)]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        out = []
        for g in gs:
            self.set_visible(shot, g)
            out += C.Take.render(self, [bf(shot, g)], out_dir, scale=scale, samples=samples, threads=threads)
        return out


def make(shots, quality):
    return MarketTake(quality) if shots[0] in MARKET else BakeryTake(quality)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = make(shots, "preview")
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
        C.final_loop(lambda q: make(shots, q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
