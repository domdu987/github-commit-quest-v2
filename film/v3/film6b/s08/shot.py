#!/usr/bin/env python3
"""shot.py -- film 6b take s08: shots 8-12 (g 314..621) + 6 handle frames each side (g 308..627), bakery MORNING.

    shot  8  g 314..359  low CU Henry introduced: huge from below, holding a loaf up to one squinting eye; hanging board
                         "ร้านลุงเฮนรี่" above him; slow push up.                         ("เจ้านายของเขา / ลุงเฮนรี่")
    shot  9  g 360..398  ECU hand balance: loaf pan + tag "500 ก.", beam wobbles and settles dead level on "เป๊ะ" (g 392);
                         Henry's big squinting face peers over the beam behind.             ("ชั่งทุกก้อน เป๊ะ")
    shot 10  g 399..465  MCU Henry behind the balance: drops a crumb on the loaf pan (beam tips), picks it back off (level),
                         punch-in g 438 to CU: finger wag to the lens on "ไม่ขาด ไม่เกิน".
    shot 11  g 466..533  CU kit + basket: kit slips the pale 13th loaf on top (drops g 480); Henry behind turns, eyes on it;
                         SNAP ZOOM g 494..499 onto Henry's face, eyes wide (shocked), creeping in.
    shot 12  g 534..621  low CU Henry YELLS at kit (screen-left foreground, cowering, cap blown back): purple face ramps up,
                         steam out of his ears, lip-sync on the quote (narration envelope, g 536..621); punch-in g 592 to an
                         ECU of the purple face on "ข้าเจ๊งเหรอ!".  Handle g 622..627 continues (mouth closed after the quote).
Mouths move ONLY on Henry's quote (shot 12). NO depth of field (C.Take). Cool counter-colour: blue skylight from the street
side + a cool rim on the back wall (see COOL below).

    python3 shot.py probe a:b[:step]
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
sys.path.insert(0, FILM6)
sys.path.insert(0, HERE)
import common as C                                       # noqa: E402  (paths, cast6 first, bpy, bakery, stage)
import signs                                             # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6, sprites = C.B, C.actors, C.camrig, C.cast6, C.sprites
lerp, clamp, blink, pulse, ez, keys = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.keys
TMP = os.path.join(HERE, "work")
PROJ = C.PROJ
NARR = os.path.join(PROJ, "film6b", "audio", "narration.wav")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing (film 6b clock)
G0, G1 = 314, 622                  # [g0, g1): shot 8 starts at round(10.48*30), shot 13 at round(20.74*30)
H = 6
GA, GB = G0 - H, G1 + H - 1        # rendered g 308..627
S9, S10, S11, S12 = 360, 399, 466, 534
P10 = 438                          # shot 10 punch-in
SNAP = (494, 499)                  # shot 11 snap zoom kit -> henry
P12 = 592                          # shot 12 punch-in
G_PEH = g_of(12.96)                # 392 "เป๊ะ": the beam settles level
G_CRUMB_ON, G_CRUMB_OFF = 418, 436
G_WAG = g_of(14.28)                # 431 "ไม่ขาด"
G_DROP13 = 480                     # 13th loaf lands in the basket
G_SPOT = g_of(16.22)               # 490 "ที่สิบสาม"
Q0, Q1 = g_of(17.78) - 1, 621      # 536..621: Henry's quote (lip-sync)
RANGES = {1: (GA, GB)}


def shot_of(g):
    return 8 if g < S9 else 9 if g < S10 else 10 if g < S11 else 11 if g < S12 else 12


def bfr(g):
    return int(g) + 1


# ----------------------------------------------------------------------------- staging (bakery world D, floor z 0)
HENRY = (2.15, 1.50)               # behind the counter (top z 1.25), behind the balance (shots 9, 10); head centre z ~2.47
HENRY8 = (1.0, 2.0)                # shot 8: left of the balance (nothing in front of his face)
HENRY12 = (1.25, 2.0)
SCALE_X, SCALE_Y = 2.4, 0.75       # small balance foot (set): loaf pan at x 1.9, weights 2.9, beam z 2.2, pans 0.62 below
KIT11 = (0.55, 1.70); KIT_Z = 0.98 # kit on a hidden stool (s01)
HENRY11 = (2.75, 3.05)
KIT12 = (0.15, 1.45)
BASKET = Vector((1.05, 0.95, 1.25)); BASKET_SCALE = 1.25
STEAM = 0.30
COOL = [float(v) for v in os.environ.get('S08_COOL', '0,4500,5000').split(',')]   # W: sky fill, back wall, upper back wall
LOAF = dict(type="loaf", scale=0.9)
LOAF_UP = 0.145 * 0.9


# ----------------------------------------------------------------------------- cameras  (loc, look, lens) per g
def _lp(a, b, u):
    return tuple(lerp(a, b, u))


def cam_at(g):
    s = shot_of(g)
    if s == 8:            # low CU: from just above the counter, looking up at henry; slow push + rise
        u = ez((g - GA) / float(S9 - GA))
        return _lp((0.70, -0.20, 1.45), (0.80, 0.30, 1.55), u), _lp((1.0, 2.0, 2.62), (0.98, 2.0, 2.58), u), lerp(22.0, 23.0, u)
    if s == 9:            # ECU of the loaf pan + tag, henry's face behind the beam; slow arc to the right
        u = ez((g - S9) / float(S10 - S9))
        return _lp((1.52, -0.42, 1.98), (1.70, -0.30, 1.92), u), _lp((1.98, 0.75, 1.92), (2.02, 0.75, 1.90), u), lerp(30.0, 33.0, u)
    if s == 10:
        if g < P10:       # MCU: balance in the foreground, henry behind, push in
            u = ez((g - S10) / float(P10 - S10))
            return _lp((2.20, -1.05, 2.62), (2.18, -0.80, 2.60), u), _lp((2.20, 1.6, 2.05), (2.18, 1.6, 2.10), u), 22.0
        u = ez((g - P10) / float(S11 - P10))        # CU: face + wagging finger, drift left
        return _lp((2.05, -0.35, 2.55), (1.95, -0.25, 2.55), u), _lp((2.15, 2.05, 2.30), (2.12, 2.05, 2.32), u), 26.0
    if s == 11:
        if g < SNAP[0]:   # CU kit + basket, slow push
            u = ez((g - S11) / float(SNAP[0] - S11))
            return _lp((0.95, -1.30, 2.55), (0.95, -1.05, 2.52), u), _lp((0.80, 1.5, 2.05), (0.82, 1.5, 2.08), u), 24.0
        a = ((0.95, -1.05, 2.52), (0.82, 1.5, 2.08), 24.0)
        b = ((2.30, 0.55, 2.62), (2.75, 3.05, 2.50), 30.0)
        if g <= SNAP[1]:  # snap zoom: whip to henry (5 frames, ease in-out cubic)
            u = ez((g - SNAP[0]) / float(SNAP[1] - SNAP[0]), "cubic")
            return _lp(a[0], b[0], u), _lp(a[1], b[1], u), lerp(a[2], b[2], u)
        u = ez((g - SNAP[1]) / float(S12 - SNAP[1]))  # creep in on his wide eyes, tiny settle shake
        sh = 0.012 * math.exp(-(g - SNAP[1]) / 4.0) * math.sin((g - SNAP[1]) * 2.4)
        return _lp(b[0], (2.38, 0.85, 2.60), u), tuple(v + (sh if i == 2 else 0) for i, v in enumerate(_lp(b[1], (2.75, 3.05, 2.50), u))), lerp(30.0, 32.0, u)
    # shot 12: low CU, henry yelling at kit (screen-left foreground); shake grows with the anger; punch-in on "ข้าเจ๊งเหรอ!"
    shake = 0.010 * clamp((g - S12) / 40.0) * math.sin(g * 2.1) + 0.006 * math.sin(g * 3.7)
    if g < P12:
        u = ez((g - S12) / float(P12 - S12))
        loc = _lp((0.62, -0.50, 1.55), (0.72, -0.25, 1.60), u); look = _lp((0.62, 2.0, 2.62), (0.70, 2.0, 2.64), u); lens = 21.0
    else:
        u = ez((g - P12) / float(GB + 1 - P12))
        loc = _lp((1.05, 0.10, 1.95), (1.10, 0.30, 1.98), u); look = _lp((1.25, 2.0, 2.50), (1.25, 2.0, 2.52), u); lens = 24.0
    return loc, (look[0] + shake, look[1], look[2] + shake * 0.6), lens


# ----------------------------------------------------------------------------- the balance (small_scale) per g
def beam_at(g):
    if g < S9:
        return 0.0
    if g < S10:          # wobble, settle dead level on "เป๊ะ"
        if g >= G_PEH:
            return 0.0
        u = (g - S9) / float(G_PEH - S9)
        return 6.0 * (1 - u) ** 1.5 * math.cos(u * 3.0 * math.pi)
    if g < S11:          # crumb on -> loaf pan dips (+), crumb off -> level
        return keys(g, [(S10, 0.0, "sine"), (G_CRUMB_ON, 0.0, "back_out"), (G_CRUMB_ON + 5, 4.5, "sine"),
                        (G_CRUMB_OFF, 4.5, "back_out"), (G_CRUMB_OFF + 6, 0.0, "sine")])
    return 0.0


# ----------------------------------------------------------------------------- lip-sync envelope (narration at +0.10 s)
_ENV = None


def env(g):
    global _ENV
    if _ENV is None:
        w = wave.open(NARR); sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch).mean(1) / 32768.0
        _ENV = (a, sr)
    a, sr = _ENV
    s = int((g / 30.0 - 0.10) * sr)
    seg = a[max(0, s):max(0, s) + sr // 30]
    return float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0


def mouth_at(g):
    if not (Q0 <= g <= Q1):
        return None
    gg = g - (g - Q0) % 2                   # a new drawing every 2 frames
    e = max(env(gg), env(gg + 1))
    if e < 0.035:
        return "clench"
    if e < 0.11:
        return "talk_a"
    return "talk_o" if (gg // 2) % 5 == 3 else "talk_b"


# ----------------------------------------------------------------------------- poses
def henry_pose(g):
    s = shot_of(g)
    t = g / 30.0
    if s == 8:            # squinting at a loaf held up to his eye (screen-left hand)
        u = ez((g - GA) / 30.0)
        return dict(yaw=-0.15, pitch=-0.20 + 0.05 * math.sin(g * 0.2), expr="unimpressed", head_roll=6 + 2 * math.sin(g * 0.13),
                    gaze=(-0.75, -0.2), lean=-2, squash=(1.0, 1.0),
                    arm_l=dict(hand=(lerp(-0.62, -0.55, u), lerp(0.45, 0.30, u)), bend=-0.6, stretch=1.2), prop_l="loaf",
                    arm_r="akimbo", legs="wide", blink=blink(g, [326, 352]), t=t)
    if s == 9:            # peering down at the pan (behind the beam)
        return dict(yaw=-0.12, pitch=0.35, expr="unimpressed", head_roll=-4 + 2 * math.sin(g * 0.15), gaze=(-0.35, 0.85),
                    arm_l="akimbo", arm_r="akimbo", legs="wide", blink=blink(g, [372]), t=t,
                    head_dy=0.0)
    if s == 10:
        p = dict(yaw=-0.10, pitch=0.25, expr="determined", head_roll=-3, gaze=(-0.45, 0.75), arm_r="akimbo", legs="wide", t=t,
                 blink=blink(g, [410, 452]))
        if g >= G_CRUMB_ON + 5 and g < G_CRUMB_OFF + 6:
            p["expr"] = "unimpressed"
        if g >= P10 - 2:   # finger wag to the lens, smug
            u = ez((g - (P10 - 2)) / 6.0)
            wag = math.sin((g - P10) * 0.75)
            p.update(yaw=lerp(-0.10, 0.05, u), pitch=lerp(0.25, -0.15, u), expr="smug", gaze=(0.0, 0.0), head_roll=-4 + 5 * wag * u,
                     arm_r=dict(hand=(0.30 + 0.12 * wag, -0.05), bend=-0.9, shape="point", stretch=1.0))
        return p
    if s == 11:
        if g < G_SPOT - 4:
            return dict(yaw=0.30, pitch=0.30, expr="unimpressed", head_roll=4, gaze=(0.6, 0.5), arm_l="akimbo", arm_r="akimbo",
                        legs="wide", blink=blink(g, [470]), t=t)
        u = ez((g - (G_SPOT - 4)) / 6.0)
        p = dict(yaw=lerp(0.30, -0.30, u), pitch=lerp(0.30, 0.10, u), expr="unimpressed", head_roll=lerp(4, -2, u),
                 gaze=(lerp(0.6, -0.8, u), lerp(0.5, 0.4, u)), arm_l="akimbo", arm_r="akimbo", legs="wide", t=t)
        if g >= SNAP[0] + 1:          # eyes go WIDE (shocked) as the camera lands
            k = ez((g - SNAP[0] - 1) / 4.0)
            p.update(expr="shocked", mouth="clench", squash=(lerp(1.0, 0.96, k), lerp(1.0, 1.05, k)), head_dy=-0.03 * k,
                     gaze=(-0.75, 0.35), fx=[dict(type="anger_fill", level=0.15 * clamp((g - 510) / 20.0))] if g > 510 else [],
                     arm_l=dict(hand=(-0.55, 0.45), bend=-0.6, shape="open", stretch=1.2),
                     arm_r=dict(hand=(0.55, 0.45), bend=-0.6, shape="open", stretch=1.2))
        return p
    # shot 12: the YELL (cast6 henry_yell: pointing at kit, screen-left)
    lvl = keys(g, [(S12, 0.25, "quad_out"), (S12 + 10, 0.55, "sine"), (P12, 0.8, "quad_out"), (P12 + 8, 1.0, "sine")])
    sq = 0.03 * math.sin(g * 1.3) if Q0 <= g <= Q1 else 0.0
    p = dict(yaw=-0.40, pitch=-0.45 + 0.08 * math.sin(g * 0.9), expr="furious", fx=[dict(type="steam", t=t * 1.6), dict(type="anger_fill", level=lvl)],
             head_roll=-8 + 3 * math.sin(g * 0.7), lean=-4 + 3 * clamp((g - S12) / 6.0), squash=(1.0 + sq, 1.0 - sq),
             arm_l=dict(hand=(-0.98, 0.10 + 0.06 * math.sin(g * 1.1)), shape="point", bend=-0.6, stretch=1.3), arm_r="akimbo", legs="wide", t=t)
    m = mouth_at(g)
    p["mouth"] = m if m else "clench"
    return p


def kit_pose(g):
    s = shot_of(g)
    t = g / 30.0
    if s == 11:           # slips the 13th loaf in, smirk at the lens, then notices henry looking
        p = dict(yaw=0.40, pitch=0.30, expr="smirk", head_roll=4, gaze=(0.6, 0.6), lean=8, arm_l=dict(hand=(-0.42, 0.80), bend=0.5),
                 legs="stand", t=t, blink=blink(g, [470, 486]))
        if g > G_DROP13 + 1:
            u = ez((g - G_DROP13 - 1) / 5.0)
            p.update(yaw=lerp(0.40, 0.10, u), pitch=lerp(0.30, -0.05, u), gaze=(lerp(0.6, 0.0, u), lerp(0.6, 0.0, u)), expr="grinning")
        if g >= G_SPOT:
            p.update(expr="worried", gaze=(0.9, -0.1), yaw=0.35)
        return p
    # shot 12: cowering in the blast, leaning away (screen-left), cap blown back
    k = clamp((g - S12) / 10.0)
    return dict(yaw=0.55, pitch=0.25, expr="worried", fx=["sweat"], head_roll=lerp(4, 14, k) + 3 * math.sin(g * 1.7), lean=lerp(-2, -12, k),
                squash=(1.03, 0.96), gaze=(0.9, -0.3), arm_l=dict(hand=(-0.35, 0.55), bend=0.6), arm_r=dict(hand=(0.35, 0.45), bend=-0.7, shape="open"),
                legs="stand", blink=blink(g, [560, 600]), t=t)


def kit_cap_tilt(g):
    if shot_of(g) != 12:
        return -5.0
    return lerp(-5.0, 38.0, ez((g - S12) / 14.0)) + 5.0 * math.sin(g * 1.9) * clamp((g - S12) / 14.0)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=24.0, name="cam_s08")
        sd = os.path.join(TMP, "sprites")
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        self.actors["kit"] = C.make_actor("kit", "kit", sd, (-1.5625, -3.875, 1.5625, 0.1875))
        pd = os.path.join(TMP, "props")
        # signs: shop board above henry, "500 ก." tag on the loaf pan
        a = signs.board_svg("ร้านลุงเฮนรี่", 2.3, 0.62, 0.40)
        b = signs.tag_svg("500 ก.", 0.70, 0.28, 0.19)
        pa, pb = signs.rasterise([(a[0], a[1], 300), (b[0], b[1], 640)], pd)
        self.board = C.PropCard("board", [pa], a[1], scale=1.0, shadow=True)
        self.tag = C.PropCard("tag", [pb], b[1], scale=0.42, shadow=False)
        # the customer's basket (12 / 13 loaves) for shot 11
        items = []
        for n in (12, 13):
            svg, an = cast6.basket_svg("bk%d" % n, loaves=n)
            items.append((svg, (-0.56, -0.06, 0.56, 0.72), 512))
        self.basket = C.PropCard("basket", C.svg_pngs(items, pd), (-0.56, -0.06, 0.56, 0.72), scale=BASKET_SCALE, shadow=True)
        # crumb (shot 10)
        crumb = ('<path d="M-0.05 0.01 Q-0.04 -0.04 0.0 -0.045 Q0.05 -0.03 0.05 0.01 Q0.02 0.04 -0.02 0.035 Z" fill="#d79a52" '
                 'stroke="#2a1630" stroke-width="0.012"/><circle cx="-0.01" cy="-0.015" r="0.012" fill="#f3d39c"/>')
        self.crumb = C.PropCard("crumb", C.svg_pngs([(crumb, (-0.07, -0.07, 0.07, 0.07), 1024)], pd), (-0.07, -0.07, 0.07, 0.07),
                                scale=2.2, shadow=False)
        self.cool_light()

    def cool_light(self):
        """complementary colour (DIRECTOR_REVIEW 7): a cold sky-blue fill from the street side + a blue wash on the back wall."""
        sc = self.scene
        for nm, loc, rot, size, en, col in (
                ("L_cool_sky", (1.0, -2.5, 5.5), (math.radians(50), 0, 0), 5.0, COOL[0], (0.12, 0.32, 1.0)),
                ("L_cool_back", (4.5, 4.0, 5.8), (math.radians(60), 0, math.radians(60)), 3.0, COOL[1], (0.12, 0.30, 1.0)),
                ("L_cool_wall", (0.5, 4.5, 6.2), (math.radians(40), 0, 0), 4.0, COOL[2], (0.10, 0.28, 1.0))):
            ld = bpy.data.lights.new(nm, "AREA"); ld.energy = en; ld.color = col; ld.size = size
            ob = bpy.data.objects.new(nm, ld); ob.location = loc; ob.rotation_euler = rot
            sc.collection.objects.link(ob)

    def pose(self, shot, gs):
        hen, kit = self.actors["henry"], self.actors["kit"]
        for g in gs:
            f = bfr(g); s = shot_of(g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(hen, f, {8: HENRY8, 11: HENRY11, 12: HENRY12}.get(s, HENRY), 0.0)
            C.place(kit, f, KIT11 if s == 11 else KIT12 if s == 12 else (-6.0, 9.0), KIT_Z if s in (11, 12) else 0.0)
            kit.card.hide_render = s not in (11, 12); kit.card.keyframe_insert("hide_render", frame=f)
            B.set_scale(beam_at(g), frame=f)
            self.key_set(f, steam=STEAM, oven=1.0)
            bx = {8: HENRY8[0]}.get(s, 2.05)
            self.board.put((bx, 3.0, 5.0 if s == 8 else 4.25), face=loc, frame=f)
            self.board.show(0 if (s in (8, 9) or (s == 10 and g < P10)) else None, frame=f)
            self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc, frame=f)
            self.basket.show((1 if g > G_DROP13 else 0) if s == 11 else None, frame=f)
        for ob in [kit.card]:
            fc = C._fcurve(ob, "hide_render")
            if fc:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"
        for g in gs:
            f = bfr(g); s = shot_of(g)
            self.scene.frame_set(f)
            loc, look, lens = cam_at(g)
            # tag rides on the loaf pan (pan pivot = beam end; pan top 0.57 below it)
            pe = B.STATE["small"]["pans"][0]
            pp = pe.matrix_world.to_translation()
            self.tag.put((pp.x - 0.06, pp.y - 0.22, pp.z - 0.62 + 0.02), face=loc, frame=f)
            self.tag.show(0 if s in (9, 10) else None, frame=f)
            # crumb
            cp, hand_l = self.crumb_at(g, pp)
            if cp is not None:
                self.crumb.put(cp, face=loc, frame=f)
            self.crumb.show(0 if cp is not None else None, frame=f)
            hp = henry_pose(g)
            hands = None
            if s == 10 and hand_l is not None and g < P10 - 2:
                hands = {"l": {"hand": tuple(actors.world_to_local(hen, self.cam, tuple(hand_l + Vector((0, 0, 0.05))), f)), "bend": -0.6, "stretch": 1.3}}
            _, inf = hen.pose(f, hp, hands=hands, camera=self.cam)
            if hands and os.environ.get('S08_DEBUG'):
                print('reach', g, {k: (v.get('reached'), v.get('error')) for k, v in inf.items() if isinstance(v, dict)}, flush=True)
            if s == 11:
                kp = kit_pose(g)
                hands = None
                if g <= G_DROP13:
                    u = ez((g - S11) / float(G_DROP13 - S11))
                    top = self.basket.to_world((0.014, 0.114 - lerp(0.30, 0.10, u)))
                    kp["prop_r"] = LOAF
                    hands = C.held_on_palm(kit, self.cam, f, top, up=LOAF_UP, bend=-0.5, stretch=1.3)
                kit.pose(f, kp, hands=hands, camera=self.cam)
            elif s == 12:
                kit.pose(f, kit_pose(g), camera=self.cam)
            else:
                kit.pose(f, dict(expr="neutral"), camera=self.cam)
        # sprites: resolution by shot (big faces need more pixels)
        ppd_h = {8: 512, 9: 448, 10: 512, 11: 448, 12: 512}
        for s in sorted({shot_of(g) for g in gs}):
            fr = [bfr(g) for g in gs if shot_of(g) == s]
            pp = ppd_h[s] if s != 12 else 576
            self.sprites_for([(hen, pp)], fr)
            if s == 11:
                self.sprites_for([(kit, 448)], fr)
            elif s == 12:
                CAST = sprites.puppet.CAST
                for f in fr:
                    CAST["kit"]["hat_tilt"] = kit_cap_tilt(f - 1)
                    self.sprites_for([(kit, 448)], [f])
                CAST["kit"]["hat_tilt"] = -5.0
            else:
                self.sprites_for([(kit, 64)], fr)

    def crumb_at(self, g, pan):
        """(crumb world position or None, henry's left-hand world target or None) in shot 10.  The hand never goes below
        ~0.45 D above the pan: lower, its point on henry's card falls behind the counter (2D card).  So he lets the crumb
        DROP onto the pan, and on removal the crumb hops up into his pinch."""
        if shot_of(g) != 10 or g >= P10 + 2:
            return None, None
        on = Vector((pan.x + 0.10, pan.y - 0.05, pan.z - 0.62 + 0.10))       # on the pan rim, beside the loaf
        hov = Vector((pan.x + 0.08, pan.y - 0.05, pan.z - 0.62 + 0.55))
        start = Vector((1.45, 0.75, 2.45))
        if g < G_CRUMB_ON - 4:
            u = ez((g - S10) / float(G_CRUMB_ON - 4 - S10))
            p = start + (hov - start) * u
            return p, p
        if g < G_CRUMB_ON:                                                   # falls
            u = ((g - (G_CRUMB_ON - 4)) / 4.0) ** 2
            return hov + (on - hov) * u, hov
        hand = hov + Vector((0, 0, 0.10 * math.sin(math.pi * clamp((g - G_CRUMB_ON) / float(G_CRUMB_OFF - G_CRUMB_ON)))))
        if g < G_CRUMB_OFF:
            return on, hand
        if g < G_CRUMB_OFF + 3:                                              # hops up into the pinch
            u = ez((g - G_CRUMB_OFF) / 3.0, "quad_out")
            return on + (hov - on) * u, hov
        u = ez((g - G_CRUMB_OFF - 3) / 6.0)
        p = hov + (start - hov) * u
        return p, p

    def report(self, shot, g):
        f = bfr(g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        out = dict(shot=shot_of(g), g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1), beam=round(beam_at(g), 2),
                   mouth=mouth_at(g), heads=C.head_report(self, f))
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bfr(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
        Tk.pose(1, gs)
        for g in gs:
            print(json.dumps(Tk.report(1, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render(1, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), [1], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
