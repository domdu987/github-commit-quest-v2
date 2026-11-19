#!/usr/bin/env python3
"""Take s14 = shot 14 (28.922-31.853, film g 868..955, handles 8 in / 9 out): office, office_day.

(a) window_tt (window_side re-aimed at the teletype): hero near and low at left (hero_tt), worried, frozen, one blink at 29.6;
    the chief beside the teletype, three-quarter; the teletype feeds the official forecast up (28.95-29.80); drift push 8 %/s
    with a 0.3 D truck right.  The chief brings a rubber stamp down on the sheet's header on 'ทางการ' (29.82, stamp tip
    registered on the teletype sheet), tears the sheet off (29.95) and thrusts it at the lens (30.10), smug nod.
(b) crash push x3 29.85-30.30 (14 f) onto the sheet: the hi-res sheet quad takes over from the puppet's paper inside the push
    (the puppet's paper is hidden from that frame) and is thrust toward the lens until it fills the frame.
(c) on the 3D sheet: drift tilt down from header and stamp to the two typed lines (about 10 %/s, easing out), the words pop
    (4-frame scale 1.08 + ink bloom) at 30.85 and 31.30, near still from 31.6.  Two finger balls (the chief's ink hands) at the
    bottom edge; the paper trembles (bow + tiny roll) so the window-bar shadows slide across it.
The last framing matches the first frames of s15 (paper to paper match dissolve): 'ฝนตก' about 450 px wide centred near y 600.
    python3 shot.py probe|still|final|deliver   (see otake.py, copied from s04)"""
import math, os, sys
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import otake as O                                       # noqa: E402
from otake import Vector, gf, bf, ease, lerp, clamp, blink, X, S, acting   # noqa: E402

TAKE, SHOTS, LIGHT, SET, VERSION = 's14', [14], 'office_day', 'office', 1
G0, G1 = 868, 956                                       # round(28.922 * 30), round(31.853 * 30)
H_IN, H_OUT = 8, 9                                      # dissolve 11 in (5.5 + 2 -> 8); dissolve 13 out (6.5 + 2 -> 9)
TRANSITION_IN = dict(type='dissolve', frames=11, note='from shot 13 (label insert)')
TRANSITION_OUT = dict(type='dissolve', frames=13, note='match dissolve paper to paper into s15 (kitchen, next morning)')
R0, R1 = G0 - H_IN, G1 + H_OUT

FEED = (gf(28.95), gf(29.80))                           # 872 -> 897
BLINK = gf(29.60)                                       # 891
STAMP = gf(29.82)                                       # 898
TEAR = gf(29.95)                                        # 902
THRUST = gf(30.10)                                      # 906
CRASH = (gf(29.85), gf(30.30))                          # 899 -> 912 (14 f)
QUAD = THRUST - 1                                       # 905: the sheet quad takes over from the puppet's paper
POP1, POP2 = gf(30.85), gf(31.30)                       # 928, 942
STILL = gf(31.60)                                       # 951

WT_LOC, WT_LOOK = Vector((-3.2, -2.6, 2.1)), Vector((2.6, -1.0, 1.85))
HERO_MARK = (-0.45, -1.25, 0.0)                         # hero_tt moved 0.7 D away from the lens: he stays in frame through the push
CHIEF_MARK = (2.35, -1.75, 0.0)                         # beside the machine, 1.7 D clear of the map wall
SHEET_N = Vector((-0.6, -0.8, 0.0)).normalized()        # the props module's sheet_face direction (lit by the window)
SHEET_C = Vector((1.90, -2.00, 2.05))                   # sheet_hold moved with the chief (+0.15, +0.20)
SHEET_W, SHEET_H = 1.08, 1.40
TT_SLOT = Vector((3.17, -0.685, 1.88))
TT_YAW = -45.0
_ax = Vector((math.cos(math.radians(TT_YAW)), math.sin(math.radians(TT_YAW)), 0.0))
STAMP_W = TT_SLOT + _ax * ((0.7915 - 0.5) * 0.54) + Vector((0, 0, 0.70 * (1 - 0.1535)))   # stamp spot on the teletype header
FILL_D = 782.22 * SHEET_W / (720 * 0.86)                # sheet_fill_camera distance, fill 0.86 (the second line stays inside the frame)


def _right(loc, look):
    f = (look - loc); f.z = 0; f.normalize()
    return Vector((f.y, -f.x, 0.0))


RIGHT = _right(WT_LOC, WT_LOOK)


def cam_a(g):
    """window_tt: truck right 0.3 D + push 8 %/s, a slow start gathering into the crash."""
    u = (g - R0) / float(CRASH[0] - R0)
    tr = 0.30 * (0.6 * ease(u, 'sine') + 0.4 * u)
    pan = -0.55 * (0.6 * ease(u, 'sine') + 0.4 * u)   # the aim stays on the pair while the lens trucks
    d = (WT_LOOK - WT_LOC).length
    push = 0.08 * d * (g - R0) / 30.0 * (0.7 + 0.6 * u)
    fwd = (WT_LOOK - WT_LOC).normalized()
    return WT_LOC + RIGHT * tr + fwd * push, WT_LOOK + RIGHT * pan + Vector((0, 0, 0.10 * u))


def sheet_look(g):
    """look point on the sheet in part c: from the header and stamp (0.20 D above centre) down to the typed lines."""
    if g <= CRASH[1]:
        k = 0.0
    else:
        u = clamp((g - CRASH[1]) / float(STILL - CRASH[1]))
        k = 0.9 * (1 - (1 - u) ** 2.2) + 0.1 * u
    dz = 0.26 - 0.195 * k
    if g > STILL:
        dz -= 0.004 * (g - STILL) / 10.0              # near still: a slow creep, never parked
    return SHEET_C + Vector((0, 0, dz))


def cam_c(g):
    loc = SHEET_C + SHEET_N * FILL_D
    if g > CRASH[1]:                                    # a little push after landing (dies away)
        t = (g - CRASH[1]) / 30.0
        loc = loc - SHEET_N * (0.04 * (1 - math.exp(-t * 1.5)) + 0.004 * t)
    return loc + Vector((0, 0, 0.05)), sheet_look(g)


def cam(g):
    if g <= CRASH[0]:
        return cam_a(g)
    if g >= CRASH[1]:
        return cam_c(g)
    u = (g - CRASH[0]) / float(CRASH[1] - CRASH[0])
    e = 0.8 * ease(u, 'quint') + 0.2 * ease(u, 'sine')
    la, ka = cam_a(CRASH[0])
    lc, kc = cam_c(CRASH[1])
    el = ease(min(1.0, u * 1.15), 'quint')
    loc = la.lerp(lc, e) + Vector((0, 0, 0.10)) * math.sin(math.pi * e)
    return loc, ka.lerp(kc, el)


# ----------------------------------------------------------------------------- props
def feed(g):
    if g < FEED[0]:
        return 0.25
    u = clamp((g - FEED[0]) / float(FEED[1] - FEED[0]))
    step = math.floor(u * 18) / 18.0                    # the platen clacks the paper up in steps
    return 0.25 + 0.75 * (0.6 * step + 0.4 * u)


def quad_state(g):
    """(centre, scale, roll, bow) of the sheet quad: thrust from the chief's hand to the hold, then trembling."""
    hand = Vector((2.20, -1.30, 2.30))
    if g < THRUST + 5:
        u = clamp((g - QUAD) / float(THRUST + 5 - QUAD))
        e = ease(u, 'cubic_out')
        c = hand.lerp(SHEET_C, e)
        sc = 0.55 + 0.45 * e
        return c, sc, -6.0 * (1 - e), 0.25 * (1 - e)
    k = g - (THRUST + 5)
    tr = math.sin(k * 2.1) * 0.5 + math.sin(k * 1.27 + 1.0) * 0.5
    c = SHEET_C + Vector((0.006 * math.sin(k * 0.9), 0.0, 0.004 * tr)) + SHEET_N.cross(Vector((0, 0, 1))) * (0.012 * math.sin(k / 9.0))
    return c, 1.0, 0.5 * tr, 0.06 + 0.035 * tr


def _pop(g, at):
    k = g - at
    if k < 0 or k > 4:
        return 0.0
    return 1.0 - k / 4.0


HANDS = {}


def _hand_png(path, ppd=256):
    """an ink ball hand (puppet _hand: ink circle + pale highlight) on a short ink arm running down out of frame."""
    from PIL import Image, ImageDraw
    W, H = int(0.30 * ppd), int(0.80 * ppd)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = (0x3a, 0x28, 0x32, 255)
    cx, cy, r = W / 2, 0.10 * ppd, 0.07 * ppd
    d.line([(cx, cy), (cx + 0.03 * ppd, H)], fill=ink, width=int(0.075 * ppd))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ink)
    hx, hy = cx - 0.34 * r, cy - 0.40 * r
    d.ellipse([hx - 0.17 * r, hy - 0.11 * r, hx + 0.17 * r, hy + 0.11 * r], fill=(0xb7, 0xa9, 0xb3, 180))
    im.save(path)
    return W / float(ppd), H / float(ppd)


def build_hands():
    import bpy
    p = os.path.join(DIR, 'work', 'hand_ball.png')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    w, h = _hand_png(p)
    m = X._lit('s14_hand', image=p, gain=0.6, alpha=True)
    root = X.STATE['objects']['sheet_root']
    for i, sx in enumerate((-0.30, 0.33)):
        q = X._grid_quad('s14_hand_%d' % i, w, h, m, origin=(w / 2, 0.10))
        q.parent = root
        q.location = (sx * SHEET_W, -0.03, -0.5 * SHEET_H + 0.085)      # the balls grip the bottom edge
        q.rotation_euler = (0, math.radians(-8 if sx < 0 else 6), 0)
        q.visible_shadow = False
        S.no_bounce(q)
        HANDS[i] = q


def keys(T):
    build_hands()
    for g in range(T.R0, T.R1):
        f = bf(g)
        # map state between shots 13 and 17: red line, smudge halo, crumbs, chalk + ghosts + tick, label, spinner
        S.set_track(1.0, 0.0, frame=f)
        X.set_smudge(3.0, frame=f)
        X.set_crumbs(1.0, frame=f)
        X.set_chalk(1.0, frame=f)
        for i in range(1, 7):
            X.set_ghost(i, 1.0, frame=f)
        X.set_tick(1.0, frame=f)
        X.set_label(1.0, frame=f)
        a, w = X.spinner_angle(g / 30.0)
        X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)
        on_tt = g < TEAR
        X.set_teletype(feed=feed(g), stamp=1.0 if g >= STAMP else 0.0, yaw_deg=TT_YAW, show=1.0 if on_tt else 0.0, frame=f)
        if g >= QUAD:
            c, sc, roll, bow = quad_state(g)
            X.set_sheet(loc=tuple(c), facing=tuple(c + SHEET_N * 3.0), roll_deg=roll, show=1.0, scale=sc,
                        pop1=_pop(g, POP1), pop2=_pop(g, POP2), bow=bow, frame=f)
        else:
            X.set_sheet(loc=tuple(SHEET_C), facing=tuple(SHEET_C + SHEET_N), show=0.0, frame=f)
        X.set_stamp(show=0.0, frame=f)


# ----------------------------------------------------------------------------- actors
ACTORS = [dict(name='hero14', cast='hero', contact=True), dict(name='chief14', cast='boss', contact=True)]


def _ppd(g, feet, h=2.9):
    loc, look = cam(g)
    head = Vector(feet) + Vector((0, 0, h))
    f = (look - loc).normalized()
    z = max(0.3, (head - loc).dot(f))
    px = 782.0 / z
    return int(min(768, max(256, math.ceil(1.6 * px / 64.0) * 64)))


def stamp_target(g):
    """world point of the stamp face: ready above the header, then down onto it at STAMP (4 frames, cubic in)."""
    t = (g - STAMP) / 30.0
    up = Vector((0, 0, 1))
    toward = (Vector(CHIEF_MARK) + Vector((0, 0, 2.2)) - STAMP_W)
    toward.z = 0
    toward.normalize()
    ready = STAMP_W + up * 0.32 + toward * 0.12
    if g <= STAMP - 10:
        return ready + up * (0.02 * math.sin((g - R0) / 5.0))
    if g < STAMP - 4:
        u = (g - (STAMP - 10)) / 6.0
        return ready + up * (0.08 * ease(u, 'sine'))           # anticipation: lift
    if g < STAMP:
        u = (g - (STAMP - 4)) / 4.0
        return (ready + up * 0.08).lerp(STAMP_W, ease(u, 'cubic_in'))
    return STAMP_W + up * (0.015 * min(1.0, (g - STAMP) / 2.0))


def perform(T, g):
    t = (g - R0) / 30.0
    out = {}
    if g < CRASH[0] + 7:
        p = acting.hero_listener(t, yaw=0.5, expr='worried', blinks_at=((BLINK - R0) / 30.0,),
                                 gaze_shift=((TEAR - R0) / 30.0, (0.8, -0.15), (0.6, -0.05)), pencil_ear=True)
        p['head_roll'] = 3.0
        out['hero14'] = dict(feet=HERO_MARK, pose=p, ppd=_ppd(g, HERO_MARK))
    else:
        out['hero14'] = None
    p = acting.boss_stamp_thrust(t, stamp_at=(STAMP - R0) / 30.0, tear_at=(TEAR - R0) / 30.0, thrust_at=(THRUST - R0) / 30.0, yaw=-0.35)
    p['blink'] = blink(g, [R0 + 9, STAMP + 12])
    hands = None
    if g < TEAR:
        hands = {'l': {'tip': tuple(stamp_target(g)), 'prop': 'stamp', 'angle': 90.0}}
    if g >= QUAD:
        p.pop('prop_l', None)                           # the hi-res sheet quad has taken over
    out['chief14'] = dict(feet=CHIEF_MARK, pose=p, hands=hands, ppd=_ppd(g, CHIEF_MARK, 3.2))
    return out


def plate_ok(T, g):
    return True


def map_hi(g):
    return False


def report_extra(T, g):
    from otake import render
    f = bf(g)
    out = dict(stamp_px=[round(v) for v in render.world_to_screen(T.cam, STAMP_W, f)[:2]])
    if g >= QUAD:
        c, sc, roll, bow = quad_state(g)
        # word centres on the sheet (SHEET_WORD_C), roll ignored
        xa = SHEET_N.cross(Vector((0, 0, 1))).normalized() * -1
        for k, (cx, cy) in (('word1', (0.4985, 0.4305)), ('word2', (0.4985, 0.608)), ('top', (0.5, 0.0)), ('bottom', (0.5, 1.0))):
            w = c + xa * ((cx - 0.5) * SHEET_W * sc) + Vector((0, 0, (0.5 - cy) * SHEET_H * sc))
            out[k + '_px'] = [round(v) for v in render.world_to_screen(T.cam, w, f)[:2]]
        l = c + xa * (-0.5 * SHEET_W * sc); r = c + xa * (0.5 * SHEET_W * sc)
        a = render.world_to_screen(T.cam, l, f); b = render.world_to_screen(T.cam, r, f)
        out['sheet_w_px'] = round(abs(b[0] - a[0]))
    return out


CUES = [
    (28.82, 0.3, 'whoosh', 'soft whoosh (dissolve in, window_side drift)'),
    (28.95, 0.85, 'clatter', 'teletype clatter: the official forecast feeds up out of the machine'),
    (29.60, 0.3, 'bell', 'teletype carriage bell'),
    (29.82, 0.15, 'thump', "rubber-stamp thump on the sheet's header ('ทางการ')"),
    (29.95, 0.2, 'tear', 'paper tear: the chief tears the sheet off the machine'),
    (30.05, 0.3, 'whoosh', 'crash whoosh in onto the sheet thrust at the lens, paper snap'),
    (30.85, 0.3, 'clack', "heavy typebar clack and bell: 'ฝนตก' pops"),
    (31.30, 0.2, 'clack', "clack: 'ลมกระโชก' pops"),
    (31.50, 0.6, 'rain', 'soft rain pre-lap'),
    (31.50, 0.4, 'music', 'snare roll, cymbal choke at 31.8'),
]

if __name__ == '__main__':
    O.main(sys.modules[__name__], sys.argv[1:])
