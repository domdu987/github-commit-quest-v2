#!/usr/bin/env python3
"""shot.py -- film 17 take s10 = shots 24-26, THE REVEAL.  Film frames g 1342..1514 (+6 handle each side: first_g 1336, last 1520).

  part M  (location 'measure', measure_chair)  g 1336..1374   calipers on dupont's head, then the whip-off to the right
  part R  (location 'reveal')                  g 1375..1520   whip-on to drawer_big (drawer yanked out 0->1), snap-push to drawer_box
                                                              (box lid opens), snap to card_hero (card rises 0->1), push-in.
Narration clock (film = narration + 0.10 s): "หัวยาวระดับนี้" 44.72 -> g1343, "เปิดลิ้นชัก" 45.64 -> g1371, "นิ้วขนาดนี้" 46.78 -> g1406,
"เหลือกล่อง" 47.58 -> g1430, "หูขนาดนี้" 48.60 -> g1461, "เหลือการ์ดใบเดียว" 49.2 -> g1479.
One location per process:   python3 shot.py <M|R> probe|stills|final a:b[:step] [out_dir] [scale] [samples]
"""
import math, os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    sys.path.insert(0, p)
import cast17                                   # noqa: E402 (before sprites)
import bpy                                      # noqa: E402
from mathutils import Vector                    # noqa: E402
import bertillon as K                           # noqa: E402
import actors, camrig, render, sprites          # noqa: E402

TMP = os.path.join(HERE, "work")
FIRST, LAST = 1336, 1520
G_M_END = 1374                                  # part M last frame; part R starts 1375
LENS = 22.0


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sine(u):
    u = clamp(u)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ease_peak(u, k=1.9):
    """snap easing: in-out with a sharp middle (k ~ peak speed / mean speed): smoothstep blended with quintic."""
    u = clamp(u)
    q = 16 * u ** 5 if u < 0.5 else 1 - 16 * (1 - u) ** 5 if False else (16 * u ** 5 if u < .5 else 1 - ((-2 * u + 2) ** 5) / 2)
    s = u * u * (3 - 2 * u)
    return lerp(s, q, clamp((k - 1.5) / 0.6))


def seg(g, a, b, ease=sine):
    return ease((g - a) / float(b - a))


def blink_at(g, starts, n=4):
    for s in starts:
        if s <= g < s + n:
            return 1.0 if s + 1 <= g < s + 3 else 0.5
    return 0.0


def vlerp(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


# ----------------------------------------------------------------------------- cameras  (loc, look) per frame
# part M: measure_chair.  chair (0.7, 2.3), dupont's head (0.7, 2.3, 1.22); bertillon on 'clerk' (1.45, 1.95).
M_A = ((2.15, 0.70, 1.42), (0.45, 2.28, 1.28))
M_B = ((1.35, 1.35, 1.40), (0.40, 2.25, 1.28))
G_WHIP_M = (1367, 1374)                          # camera whips off to the right (pan), blurred in post


def cam_M(g):
    if mode_of(g) != 'head':
        return cam_ins(g)
    u = seg(g, FIRST, G_WHIP_M[0], lambda x: 0.4 * sine(x) + 0.6 * x)
    loc, look = vlerp(M_A[0], M_B[0], u), vlerp(M_A[1], M_B[1], u)
    # lateral slide sway on top of the push (screen-right drift, a small arc)
    loc = (loc[0] + 0.10 * math.sin(g * 0.11), loc[1], loc[2] + 0.025 * math.sin(g * 0.17))
    kick = max(0.0, 1.0 - abs(g - 1344.5) / 2.2)                      # 2-3 frame tighten on "ระดับนี้" (g1343): a small push-in
    loc = (loc[0] + (look[0] - loc[0]) * 0.16 * kick, loc[1] + (look[1] - loc[1]) * 0.16 * kick, loc[2] + (look[2] - loc[2]) * 0.16 * kick)
    if g > G_WHIP_M[0]:
        w = seg(g, G_WHIP_M[0], G_WHIP_M[1] + 1, lambda x: x ** 2.2)
        look = (look[0] + 3.4 * w, look[1] - 0.8 * w, look[2])           # pan right, fast
    return loc, look


# part R: reveal room.  wall y 0, camera side y > 0.  drawer front centre (0.15, 0, 1.2), pulls out toward +y (travel 0.78).
R_DB0 = ((-0.15, 3.0, 1.9), (-0.50, 0.5, 1.2))          # drawer_big start (landing of the whip)
R_DB1 = ((-0.22, 2.40, 1.8), (-0.48, 0.5, 1.2))           # drawer_big end
R_BX0 = ((0.52, 1.36, 2.20), (0.14, 0.55, 1.18))         # box beat start: all the boxes in frame
R_BX1 = ((0.06, 1.12, 1.78), (-0.12, 0.62, 1.30))         # box beat end: the one lit box, hand at the lid
R_CH0 = ((0.32, 1.52, 1.90), (-0.13, 0.66, 1.40))           # card_hero preset
R_CH1 = ((0.20, 1.32, 1.82), (-0.15, 0.68, 1.50))           # push-in ~9 %/s + slide
G_WHIP_R = (1375, 1383)           # whip-on: pan settles into drawer_big
G_FING = (1406, 1419)             # insert: calipers on dupont's raised finger ("นิ้ว")   (measure room)
G_BOX = 1420                      # box beat starts (reveal room)
G_EAR = (1459, 1473)              # insert: calipers on dupont's ear ("หู")  (measure room)
G_CARD = 1474                     # card_hero: snap + card rises
SNAP = 10


def part_of(g):
    return "M" if (FIRST <= g <= G_M_END or G_FING[0] <= g <= G_FING[1] or G_EAR[0] <= g <= G_EAR[1]) else "R"


def mode_of(g):
    return "finger" if G_FING[0] <= g <= G_FING[1] else ("ear" if G_EAR[0] <= g <= G_EAR[1] else "head")


def cam_R(g):
    if g < G_FING[0]:                                                       # shot 24b: drawer_big
        u = seg(g, G_WHIP_R[0], G_FING[0], lambda x: 0.3 * sine(x) + 0.7 * x)
        loc, look = vlerp(R_DB0[0], R_DB1[0], u), vlerp(R_DB0[1], R_DB1[1], u)
        loc = (loc[0] + 0.05 * math.sin(g * 0.13), loc[1], loc[2])
        if g < G_WHIP_R[1]:                                                 # whip-on: start panned away to the left, brake into place
            w = 1 - seg(g, G_WHIP_R[0] - 1, G_WHIP_R[1], lambda x: 1 - (1 - x) ** 2.2)
            look = (look[0] - 3.4 * w, look[1] + 0.6 * w, look[2])
        return loc, look
    if g < G_CARD:                                                          # box beat: drift + slide, snap-push into the box at the end of the beat
        u = seg(g, G_BOX, G_EAR[0], lambda x: 0.3 * sine(x) + 0.7 * x)
        loc, look = vlerp(R_BX0[0], R_BX1[0], u), vlerp(R_BX0[1], R_BX1[1], u)
        return (loc[0] + 0.045 * math.sin(g * 0.15), loc[1], loc[2] + 0.02 * math.sin(g * 0.11)), look
    e = seg(g, G_CARD, G_CARD + SNAP, lambda x: ease_peak(x, 2.0))           # card shot: snap from the wide box view to card_hero, then push-in
    if g < G_CARD + SNAP:
        return vlerp(R_BX1[0], R_CH0[0], e), vlerp(R_BX1[1], R_CH0[1], e)
    u = seg(g, G_CARD + SNAP, 1521, lambda x: 0.2 * sine(x) + 0.8 * x)
    loc, look = vlerp(R_CH0[0], R_CH1[0], u), vlerp(R_CH0[1], R_CH1[1], u)
    return (loc[0] + 0.04 * math.sin(g * 0.14), loc[1], loc[2]), look


# measuring-room inserts (copied from team 1's approved S3A ear framing for the ear)
F_A = ((1.75, 0.80, 1.32), (0.30, 2.05, 1.14))
F_B = ((1.40, 1.12, 1.28), (0.28, 2.05, 1.14))
S3A = (((-0.58, 1.46, 1.02), (0.58, 2.20, 1.24)), ((-0.14, 1.80, 1.06), (0.74, 2.20, 1.24)))


def cam_ins(g):
    if mode_of(g) == "finger":
        u = seg(g, G_FING[0], G_FING[1] + 1, lambda x: 0.3 * sine(x) + 0.7 * x)
        a, b = F_A, F_B
    else:
        u = seg(g, G_EAR[0], G_EAR[1] + 1, lambda x: 0.25 * sine(x) + 0.75 * x)
        a, b = S3A
    return vlerp(a[0], b[0], u), vlerp(a[1], b[1], u)


# ----------------------------------------------------------------------------- hooks (reveal)
def drawer_t(g):
    return seg(g, 1376, 1398, lambda x: ease_peak(x, 1.8))


def lid_t(g):
    return seg(g, 1442, 1457)


def lift_t(g):
    return seg(g, G_CARD + 2, 1500, lambda x: ease_peak(x, 1.6))


BS = 0.7                                                      # the hero box is scaled to the size of the others
BW, BD, BH = 0.34 * BS, 0.24 * BS, 0.28 * BS
BZ = -0.175 + 0.12                                           # the boxes stand on a ledger slab so they sit near the drawer rim
SLOT = {"hero": (-0.28, -0.14), "bxA": (0.0, -0.14), "bxB": (0.28, -0.14), "bxC": (-0.28, -0.38), "bxD": (0.0, -0.38), "bxE": (0.28, -0.38)}
DARK_AT = {"bxA": 1422, "bxB": 1426, "bxC": 1430, "bxD": 1434, "bxE": 1438}      # hard switch-off, one every 4 frames; the hero box stays lit
EXTRA = {k: (SLOT[k], BW, BD, BH, 5 + i) for i, k in enumerate(("bxA", "bxB", "bxC", "bxD", "bxE"))}


LAMP_DB, LAMP_CARD = 28.0, 20.0             # box_lamp watts (card lowered so the card reads, no near-white bloom)


def lamp_w(g):
    return lerp(LAMP_DB, LAMP_CARD, seg(g, G_CARD, G_CARD + SNAP + 8))


# ----------------------------------------------------------------------------- actors
def mk_actor(name, cast, extra_scale=1.0):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(TMP, "sprites"), contact=True)
    a.head_flip = True
    if cast == "dupont":
        a.jobs = (lambda orig: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"])[0], overlay=ears_svg(j["pose"])[1]) for j in orig(px, frames, overlay)]))(a.jobs)
    return a


def pose_with(story, g, mirror=False, expr=None, rim=True, sway=1.0, phase=0.0, **over):
    cast, pose = cast17.STORY17[story]
    pose = dict(pose)
    if expr:
        pose = cast17.with_expr(pose, expr)
    pose = cast17.silent(pose)
    pose["seat17"] = None
    if mirror:
        pose["mirror"] = True
    if rim and cast in K.RIM_FOR:
        pose["rim"] = K.RIM_FOR[cast]; pose["rim_opacity"] = 0.55; pose["rim_w"] = 0.02
    pose["head_roll"] = pose.get("head_roll", 0) + sway * 2.2 * math.sin(g * 0.19 + phase)
    pose["lean"] = pose.get("lean", 0) + sway * 1.6 * math.sin(g * 0.13 + phase * 2)
    pose["blink"] = blink_at(g, [1352 + int(phase * 5), 1402, 1447, 1493 + int(phase * 3)])
    pose.update(over)
    return cast, pose


SLIDE = [0.46]


def _calipers_body(k):
    """cast17's calipers with an adjustable sliding jaw (SLIDE[0]) so the jaws can close (copied from team 1 s01)."""
    c17 = cast17; dx = SLIDE[0] - 0.46
    g = c17._lin(k, "cb", c17.STEEL["light"], c17.STEEL["base"], c17.STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(c17.STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.30 L0.835,0.33 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(c17.STEEL["base"]), k.ink))
    o.append('<path d="M%.3f,-0.050 L%.3f,-0.050 L%.3f,0.30 L%.3f,0.33 L%.3f,0.034 L%.3f,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (0.40 + dx, 0.52 + dx, 0.52 + dx, 0.485 + dx, 0.46 + dx, 0.40 + dx, k.c(c17.STEEL["light"]), k.ink))
    o.append('<circle cx="%.3f" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (0.46 + dx, k.c(c17.BRASS["base"]), k.ink))
    return "".join(o)


cast17._calipers_body = _calipers_body
_orig_svg = sprites.sprite_svg


def slide_of(g):
    m = mode_of(g)
    if m == "ear":
        return lerp(0.30, 0.50, seg(g, G_EAR[0] + 2, G_EAR[0] + 12))
    if m == "finger":
        return lerp(0.30, 0.50, seg(g, G_FING[0] + 2, G_FING[0] + 12))
    return 0.0 + 0.05 * max(0.0, 1.0 - abs(g - 1344.5) / 2.2) + 0.012 * math.sin(g * 0.5)      # head: jaws open to the skull's width, squeeze on the kick


def _svg(cast, pose, *a, **kw):
    t = (pose or {}).get("t", None)
    if t is not None and cast == "bertillon":
        SLIDE[0] = slide_of(int(round(t * 30)))
    return _orig_svg(cast, pose, *a, **kw)


sprites.sprite_svg = _svg


def theta_of(yaw):
    return math.radians(min(abs(yaw), 1.2) * 70.0)


def ears_svg(pose):
    """cartoon ears (the puppet has none) -> (underlay, overlay) SVG (team 1 s01)."""
    if not pose.get("ears17"):
        return "", ""
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill = "#3a2832", "#f4d4cb"
    c = math.cos(theta_of(yw)); prof = abs(yw) > 0.5

    def ear(x, sx, big):
        rx, ry = (0.19, 0.27) if big else (0.15, 0.25)
        return ('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, 0, sx, rx, ry, fill, ink, ink))
    under = ear(0.52 * c, 1, False) + ear(-0.52 * c, 1, False) if not prof else ear(0.52 * c, 1, False)
    over = ear(-0.52 * c, 1, True) if prof else ""
    wrap = lambda gg: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, gg) if gg else ""
    return wrap(under), wrap(over)


def hand_svg(an):
    """a visible forearm (lighter sleeve), white cuff and skin hand gripping the beam (team 1 s01)."""
    ex, ey = an["elbow_r"]; hx, hy = an["hand_r"]
    dx, dy = hx - ex, hy - ey; L = math.hypot(dx, dy) or 1.0; ux, uy = dx / L, dy / L
    cx, cy = hx - ux * 0.13, hy - uy * 0.13
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.17" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#46598f" stroke-width="0.125" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.155" stroke-linecap="butt" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#fbf3ee" stroke-width="0.115" stroke-linecap="butt" fill="none"/>'
            '<circle cx="%.3f" cy="%.3f" r="0.105" fill="#f4d4cb" stroke="#3a2832" stroke-width="0.03"/>'
            '<path d="M%.3f,%.3f q0.05,-0.02 0.09,0.03" stroke="#3a2832" stroke-width="0.02" fill="none"/></g>'
            % (ex, ey, hx, hy, ex, ey, hx, hy, cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045,
               cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045, hx, hy, hx - 0.04, hy - 0.01))


class Take(object):
    def __init__(self, part, quality="draft"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.part = part
        self.A = K.build(preset="measure_chair" if part == "M" else "card_hero")
        self.scene = sc = bpy.context.scene
        K.clear_keys()
        self.cam = camrig.make_camera(sc, name="cam_s10", lens=LENS)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        self.cam.data.dof.use_dof = False
        sc.camera = self.cam
        sc.frame_start, sc.frame_end = 1, 9000
        for o in bpy.data.objects:                    # director fix: the additive light shafts wash over the cards
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])):
                o.hide_render = True
        self.acts = {}
        self.anch = {}
        self.A_marks = self.A["marks"]
        if part == "R":
            self.lamp = bpy.data.objects["box_lamp"]
            K.STATE["hero_z0"] = 0.12
            self.build_extras()
        print("take %s built in %.1f s" % (part, time.time() - t0), flush=True)

    # one actor card on a mark (seated 'chair' or standing); scale so the true height is CAST_H
    def put(self, key, cast, mark, dx=0.0, dy=0.0, dz=0.0):
        a = self.acts.get(key) or mk_actor("c_" + key, cast)
        self.acts[key] = a
        x, y, z, fz, who = self.A_marks[mark]
        sc = K.CAST_H[cast] / K.CAST_HD[cast]
        a.root_scale = sc
        return a, (x + dx, y + dy, z + dz), sc

    def pose_frames(self, gs):
        sc = self.scene
        f_of = lambda g: g - FIRST + 1
        for g in gs:
            f = f_of(g)
            loc, look = (cam_M if self.part == "M" else cam_R)(g)
            camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
            if self.part == "R":
                K.set_drawer("big", drawer_t(g), frame=f)
                K.set_box_lid("box", lid_t(g), frame=f)
                self.key_boxes(g, f)
                self.key_hand(g, f)
                self.key_hero(g, f)
                self.lamp.data.energy = lamp_w(g) * K.LAMP_W * K.STATE["P"]["lamp_k"]
                self.lamp.data.keyframe_insert("energy", frame=f)
            K.set_flicker(1.0, frame=f); K.set_dust(0.4, frame=f); K.set_smoke(1.0, frame=f)
            if self.part == "M":
                K.set_pendulum(frame=f)
        self.stage(gs)

    def stage(self, gs):
        cam = self.cam
        if self.part == "M":
            self.stage_M(gs)
        else:
            self.stage_R(gs)

    # ---- part M: dupont seated in the measuring chair, bertillon (mirrored) holds the calipers on his head
    # ---- measuring-room staging: three modes (head: calipers on the skull; finger: on the raised finger; ear: on the near ear)
    def stage_M(self, gs):
        d_cast, b_cast = "dupont", "bertillon"
        da, dpos, dsc = self.put("dup", d_cast, "chair", dy=-0.22)
        ba, bpos, bsc = self.put("ber", b_cast, "clerk", dx=-1.0, dy=-0.15)
        _, dpose0 = pose_with("dupont_innocent", 1)
        fx, fy = sprites.feet_of(d_cast, dpose0)
        dzz = K.HEAD_Z["chair"] - dsc * fy
        for g in gs:
            f = g - FIRST + 1
            m = mode_of(g)
            dp_xy = (0.70, 2.16) if m == "ear" else (dpos[0], dpos[1])
            bp_xy = {"head": (0.58, 1.84), "finger": (-0.15, 2.0), "ear": (0.30, 2.42)}[m]
            da.place(f, (dp_xy[0], dp_xy[1], dzz), scale=dsc)
            ba.place(f, (bp_xy[0], bp_xy[1], 0.0), scale=bsc)
        for g in gs:                                              # dupont first (his anchors give the calipers' target)
            f = g - FIRST + 1
            self.scene.frame_set(f)
            m = mode_of(g)
            _, dp = pose_with("dupont_innocent", g, expr="worried", phase=1.0, sway=0.6)
            dp["legs"] = "stand"
            if m == "head":
                dp["ears17"] = True
            if m == "finger":                                       # the left hand (screen-left, toward Bertillon) comes up with one finger
                u = seg(g, G_FING[0], G_FING[0] + 6)
                dp["arm_l"] = dict(hand=(lerp(-0.74, -0.88, u), lerp(0.60, 0.30, u)), bend=0.4, shape="point", sharp=1.0, layer="front")
                dp["ears17"] = True
            elif m == "ear":
                dp.update(yaw=0.88, pitch=0.0, gaze=(0.9, 0.05), arm_l=dict(preset="shrug"), arm_r=dict(preset="shrug"))
                dp["ears17"] = True
            da.pose(f, dp, camera=self.cam)
        self.sprites_group(da, gs, 320, 512)
        for g in gs:
            if mode_of(g) != "finger":
                continue
            f = g - FIRST + 1
            self.scene.frame_set(f)
            hw = actors.local_to_world(da, self.anch[(da.name, f)]["hand_l"], f, camera=self.cam)
            u = seg(g, G_FING[0], G_FING[1] + 1, lambda x: 0.3 * sine(x) + 0.7 * x)
            off = Vector((lerp(0.46, 0.34, u), lerp(-0.46, -0.38, u), lerp(0.14, 0.08, u)))
            camrig.key_camera(f, hw + off, hw + Vector((-0.02, 0.0, 0.0)), cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
        for g in gs:                                              # bertillon: jaws pinned
            f = g - FIRST + 1
            self.scene.frame_set(f)
            m = mode_of(g)
            bp_cast, bp = pose_with("bertillon_measuring", g, mirror=False, sway=0.5)
            bp["prop_r"] = dict(bp["prop_r"], angle=-10 + 6 * math.sin(g * 0.3)); bp["gaze"] = (0.95, 0.35); bp["pitch"] = 0.25
            bp["t"] = g / 30.0
            if m == "head":
                u0 = seg(g, FIRST, 1350, lambda x: 1 - (1 - clamp(x)) ** 2)            # calipers rise from low and close across the skull by g1350, then hold
                bp["yaw"] = 0.35
                lc, lk = cam_M(g)                                              # camera right vector: the far jaw goes to the right edge of the skull
                fw = Vector(lk) - Vector(lc); rt = fw.cross(Vector((0, 0, 1))); rt.normalize()
                head_c = Vector((0.70, 2.08, K.HEAD_Z["chair"]))
                tip = head_c + rt * (0.40 + 0.5 * (1 - u0)) + Vector((0, 0, 0.12 - 0.55 * (1 - u0)))
                _p, _i = ba.pose(f, bp, hands={"r": {"tip": tuple(tip), "prop": "calipers", "angle": 0, "prop_scale": 1.35, "stretch": 1.15}}, camera=self.cam)
                continue
            else:
                an = self.anch[(da.name, f)]
                if m == "finger":
                    hx, hy = an["hand_l"]
                    k = 1.0 - seg(g, G_FING[0], G_FING[0] + 7)
                    loc_t = (hx - 0.02 - 0.5 * k, hy - 0.10 + 0.9 * k + 0.012 * math.sin(g * 0.9))
                    ang, psc = -4, 0.9
                else:
                    hx, hy = an["head"]
                    ex = hx - 0.52 * math.cos(theta_of(0.88))
                    k = 1.0 - seg(g, G_EAR[0], G_EAR[0] + 6)
                    loc_t = (ex - 0.5 * k, hy + 0.02 + 1.0 * k + 0.015 * math.sin(g * 0.8))
                    ang, psc = -4, 0.8
                w = actors.local_to_world(da, loc_t, f, camera=self.cam)
                hands = {"r": {"tip": w, "prop": "calipers", "angle": ang, "prop_scale": psc, "stretch": 1.15}}
            ba.pose(f, bp, hands=hands, camera=self.cam)
        self.sprites_group(ba, gs, 320, 512, hand_overlay=True)

    def sprites_group(self, a, gs, ppd_lo, ppd_hi, hand_overlay=False):
        lo = [g - FIRST + 1 for g in gs if mode_of(g) == "head"]
        hi = [g - FIRST + 1 for g in gs if mode_of(g) != "head"]
        for frames, ppd in ((lo, ppd_lo), (hi, ppd_hi)):
            if not frames:
                continue
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
            if hand_overlay and frames is hi:
                ov = lambda f, pose: hand_svg(self.anch[(a.name, f)])
                a.render_sprites(ppd, frames=frames, overlay=ov)

    # ---- reveal-room runtime dressing: extra boxes (lit -> dark one by one), Bertillon's hand at the lid, the hero card
    def build_extras(self):
        slide = K.STATE["anim"]["big"]["slide"]
        self.twin = {}
        for nm in ("box2",):                                    # the old second box and the ledger riser go away
            for o in K.STATE["anim"][nm]["objs"]:
                o.hide_render = True
        for o in bpy.data.objects:
            if o.name.startswith("riser"):
                o.hide_render = True
        root = K.STATE["anim"]["box"]["root"]
        root.scale = (BS, BS, BS)
        root.location = (SLOT["hero"][0], SLOT["hero"][1], BZ)
        root.rotation_euler = (0, 0, 0)
        hero = K.STATE["anim"]["hero"]["root"]
        hero.scale = (1.0 / BS,) * 3
        for nm, (xy, w, d, h, seed) in EXTRA.items():
            K.card_box(nm, (xy[0], xy[1], BZ), rot_z=0, w=w, d=d, h=h, lid=0.0, cards=8, seed=seed, parent=slide, mat="box_ochre", lining="walnut")
            K.card_box(nm + "_d", (xy[0], xy[1], BZ), rot_z=0, w=w, d=d, h=h, lid=0.0, cards=8, seed=seed, parent=slide, mat="dark", lining="dark")
        Bs = K.Batch(23); Bs.box("navy", (0.0, -0.27, -0.175 + 0.06), (0.86, 0.62, 0.12)); Bs.finalize("slab", parent=slide, ink_t=K.STATE["ink_t"] * 0.8)
        K.point((0.2, 1.0, 1.9), color=(1.0, 0.82, 0.55), watts=45, radius=0.1, name="box_fill", flicker=False)
        B = K.Batch(21)                                         # the hand: local +x points back along the forearm, the hand is at the origin
        B.cyl("cloth", (0.38, 0, 0), 0.048, 0.62, axis="x", seg=12)
        B.cyl("cream", (0.075, 0, 0), 0.052, 0.05, axis="x", seg=12)
        B.sphere("cardedge", (0.0, 0, 0), 0.05, scale=(1.0, 1.0, 0.8))
        for k in (-1, 0, 1):
            B.cyl("cardedge", (-0.065, 0.026 * k, 0.0), 0.012, 0.09, axis="x", seg=8)
        B.sphere("cardedge", (-0.02, -0.055, -0.01), 0.02)
        root = bpy.data.objects.new("hand_root", None)
        bpy.context.scene.collection.objects.link(root)
        B.finalize("hand", parent=root, ink_t=K.STATE["ink_t"] * 0.7)
        self.hand = root

    def objs_of(self, nm):
        a = K.STATE["anim"][nm]
        return list(a["objs"])

    def key_boxes(self, g, f):
        for nm, tg in DARK_AT.items():
            dark = g >= tg
            for o in self.objs_of(nm):
                o.hide_render = dark; o.keyframe_insert("hide_render", frame=f)
            for o in self.objs_of(nm + "_d"):
                o.hide_render = not dark; o.keyframe_insert("hide_render", frame=f)

    def lid_grip(self, t):
        """world point of the hero box's lid front edge (+ a little in front) for lid-open amount t."""
        th = math.radians(110 * t)
        px, py, pz = 0.15 + SLOT["hero"][0], 0.78 + SLOT["hero"][1], 1.2 + BZ
        hy, hz = py - BD / 2, pz + BH
        return Vector((px, hy + BD * math.cos(th) + 0.03, hz + BD * math.sin(th) + 0.015))

    def key_hand(self, g, f):
        t = lid_t(g)
        grip = self.lid_grip(t)
        arr = seg(g, 1430, 1442)                                # comes in from the right / back
        lv = seg(g, 1457, 1459)
        away = Vector((-0.65, 0.22, 0.16))                      # off-screen toward the right (-x), a little back and up
        pos = grip + away * ((1 - arr) + 0.35 * lv)
        self.hand.location = pos
        v = (away * -1.0)                                       # local +x points from the hand back along the forearm = toward 'away'
        self.hand.rotation_euler = (-1.0 * away).to_track_quat("-X", "Z").to_euler() if False else away.to_track_quat("X", "Z").to_euler()
        vis = 1430 <= g <= 1458
        for o in self.hand.children_recursive:
            o.hide_render = not vis; o.keyframe_insert("hide_render", frame=f)
        self.hand.keyframe_insert("location", frame=f); self.hand.keyframe_insert("rotation_euler", frame=f)

    def key_hero(self, g, f):
        t = lift_t(g)
        a = K.STATE["anim"]["hero"]["root"]
        a.location = (0.03 * t / BS, (0.02 + 0.14 * t) / BS, (0.12 + 0.45 * t) / BS)         # box-local units (the box root is scaled by BS)
        a.rotation_euler = (math.radians(22 * t), 0, math.radians(-9 * t))
        a.keyframe_insert("location", frame=f); a.keyframe_insert("rotation_euler", frame=f)

    # ---- part R: bertillon at the drawer (yanks it out and steps back); nobody else is staged (the camera is on the drawer)
    def stage_R(self, gs):
        ba, bpos, bsc = self.put("ber", "bertillon", "drawer_r")
        for g in gs:
            f = g - FIRST + 1
            t = drawer_t(g)
            ba.place(f, (-0.47, 1.12 + 0.22 * t, 0.0) if g < G_FING[0] else (60.0, 60.0, -60.0), scale=bsc)   # leaves during the snap peak (no floating hand in shots 25-26)
        for g in gs:
            f = g - FIRST + 1
            self.scene.frame_set(f)
            t = drawer_t(g)
            _, bp = pose_with("bertillon_neutral", g, mirror=True, sway=0.7, expr="determined" if g < 1395 else "proud"); bp["lean"] = bp.get("lean", 0) - 16 * min(1.0, t * 1.5) + 2.5 * math.sin(g * 0.8) * (1.0 if g < 1406 else 0.0)
            hand = (0.14, t * 0.78 + 0.03, 1.10)
            ba.pose(f, bp, hands={"r": {"hand": hand}}, camera=self.cam)
        for a, ppd in ((ba, 256),):
            for f, r in zip([g - FIRST + 1 for g in gs], a.render_sprites(ppd, frames=[g - FIRST + 1 for g in gs])):
                self.anch[(a.name, f)] = r["anchors"]

    def heads(self, g):
        f = g - FIRST + 1
        self.scene.frame_set(f)
        out = {}
        for a in self.acts.values():
            if (a.name, f) not in self.anch:
                continue
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            out[a.name] = (round(c[0]), round(c[1]))
        return out

    def render(self, gs, out_dir, scale=1.0, samples=12):
        sc = self.scene
        K.setup_render(sc, "final", samples)
        sc.camera = self.cam
        self.cam.data.dof.use_dof = False
        res = []
        for g in gs:
            f = g - FIRST + 1
            st = render.render_frames([f], out_dir, scale=scale, threads=int(os.environ.get("THREADS", "2")), scene=sc, camera=self.cam, verbose=False)[0]
            png = os.path.join(out_dir, "g_%04d.png" % g)
            os.replace(st["path"], png)
            K.grade(png, scale=scale)
            res.append((g, st["wall"], self.heads(g)))
            print("g %d  %.1f s  heads %s" % (g, st["wall"], res[-1][2]), flush=True)
        return res


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    part, cmd, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw")
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    gs = [g for g in parse(spec) if FIRST <= g <= LAST and part_of(g) == part]
    os.makedirs(out, exist_ok=True)
    if cmd == "final":
        gs = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
    if not gs:
        print("nothing to do"); sys.exit(0)
    T = Take(part)
    T.pose_frames(gs)
    T.render(gs, out, scale=scale, samples=samples)
