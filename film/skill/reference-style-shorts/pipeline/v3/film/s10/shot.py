#!/usr/bin/env python3
"""Take s10 = shot 10 (20.317-23.129, film g 610..693, handles 7 + 7): office, office_day (INTERIOR_DAY).

(1) low angle on the chief alone at boss_mark (camera 1.2 D up, about 4 D away, looking up past him at the map), he bounces the
eraser in his palm; (2) snap 20.82-21.35 on '"ไอ้หนู': pull back, rise to 2.85 D and pan right into G, THE GLOAT FRAMING (chief far
at boss_mark, hero near at gloat_near, red line at screen left); (3) eased push through the quote, 30 -> 0 %/s, x1.3 (a zoom from
G's pose with a small truck right, so the near/far ratio of G is kept). The chief's mouth moves with the narration loudness only
inside the quote 21.07-23.13; 'เฮอริเคน' he drives the eraser up the red line (pinned), 'มันไม่ขึ้น' finger wag, 'ทางด่วนหรอก' lean
toward the hero and a held wink. The hero listens, frozen, unimpressed, blinks, one gaze shift; his mouth never moves.
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import otake as O                                       # noqa: E402
gf, gb, smooth, smoother, lerp = O.gf, O.gb, O.smooth, O.smoother, O.lerp
import acting as AC                                     # noqa: E402  (path set by otake)
import office3d as S                                    # noqa: E402
import office_props as X                                # noqa: E402

TAKE, SHOTS, VERSION, HI_MAP = 's10', [10], 3, False
G0, G1 = gb(20.317), gb(23.129)                         # 610, 694
H_IN, H_OUT = 7, 7                                      # 9-frame dissolves in and out: 4.5 + 2 -> 7
TRANSITION_IN = dict(type='dissolve', frames=9, note='quick continuity from s09 (corridor view) into the low angle on the chief')

SNAP = (gf(20.82), gf(21.35))                           # 627 -> 644 (17 f)
Q0, Q1 = 21.07, 23.13                                   # the quote (narration clock)
QG = gf(Q0)                                             # 635: frame 0 of the loudness list
LOUD = AC.loudness(Q0, Q1)
HURR = (gf(21.575), gf(21.956))                         # 650 - 662: eraser drives up the red line
WAG = (gf(21.956), gf(22.358))                          # 662 - 674
LEAN = gf(22.358)                                       # 674
WINK = (gf(22.95), gf(23.10))                           # 692 - 696
PATS = (gf(20.45), gf(20.75))                           # 617, 626: eraser pats in his palm

BOSS = (1.30, -0.42, 0.0)                               # boss_mark
HERO = (2.40, -1.70, 0.0)                               # gloat_near

L1 = ((0.30, -4.10, 1.20), (0.70, -0.42, 2.30))         # low single: chief at x 474, hero out of frame right, map at left
GC = ((1.55, -4.95, 2.85), (1.25, -0.40, 2.62))         # G (office_props)
GE = ((1.85, -4.95, 2.85), (1.45, -0.40, 2.62), 28.6)   # end of the push: x1.3 zoom, truck right 0.3


def cam(g):
    if g < SNAP[0]:
        u = (g - (G0 - H_IN)) / float(SNAP[0] - (G0 - H_IN))
        k = 0.035 * (0.4 * u + 0.6 * u * u)                 # slow push in that accelerates into the snap
        return lerp(L1[0], L1[1], k), L1[1], None, 22.0
    l0 = lerp(L1[0], L1[1], 0.035)
    if g < SNAP[1]:
        u = smoother((g - SNAP[0]) / float(SNAP[1] - SNAP[0]))
        ut = smoother(max(0.0, ((g - SNAP[0]) / float(SNAP[1] - SNAP[0]) - 0.06) / 0.94))   # the pan trails the rise a hair
        loc = lerp(l0, GC[0], u)
        loc = (loc[0], loc[1], loc[2] + 0.12 * math.sin(math.pi * u))                       # a little crane overshoot in the middle
        return loc, lerp(L1[1], GC[1], ut), None, 22.0
    x = (g - SNAP[1]) / float(G1 + H_OUT - 1 - SNAP[1])
    e = 1 - (1 - x) ** 2.2                                   # 30 %/s easing to 0
    lens = 22.0 * (GE[2] / 22.0) ** e
    return lerp(GC[0], GE[0], e), lerp(GC[1], GE[1], e), None, lens


# ----------------------------------------------------------------------------- props
def props(g, f):
    S.set_track(1.0, 0.0, frame=f)
    X.set_chalk(1.0, frame=f)
    for i in range(1, 7):
        X.set_ghost(i, 1.0, frame=f)
    X.set_tick(1.0, frame=f)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)


# ----------------------------------------------------------------------------- acting
def eraser_tip(g):
    """world target of the eraser face while he drives it up the line (toy car), None outside."""
    if g < HURR[0] - 6 or g > HURR[1] + 5:
        return None
    u = smooth(HURR[0], HURR[1], g)
    p = S.track_point(0.50 + 0.42 * u)
    hop = 0.012 * abs(math.sin((g - HURR[0]) * math.pi / 3.0))     # bumpy 'vroom'
    return (p[0], p[1] - 0.002, p[2] + hop)


def boss_pose(g):
    t = (g - QG) / 30.0
    if g < SNAP[0] + 4:                                          # eraser bounce in the near (left) palm, facing the lens/map
        tb = (g - (PATS[0] - 9)) / 30.0
        p = AC.boss_eraser_bounce(max(0.0, tb), yaw=-0.35, hz=1.0 / 0.30)
        return p, None
    if g < QG:                                                   # through the snap: smirk, eraser held low
        p = dict(yaw=-0.35, expr='smirk', arm_r='hip', legs='stand', pitch=0.1, head_roll=-3.0,
                 arm_l=dict(hand=(-0.48, 0.55), bend=0.3, shape='open'), prop_l=dict(type='eraser', angle=-90.0))
        return p, None
    tip = eraser_tip(g)
    if g < WAG[0]:                                               # '"ไอ้หนู' / 'เฮอริเคน': facing the map, drives the eraser up the line
        base = dict(yaw=-0.35, arm_r='hip', legs=dict(preset='stand', stride=-0.2), lean=-4.0 * smooth(HURR[0] - 6, HURR[0], g),
                    arm_l=dict(hand=(-0.48, 0.55), bend=0.3, shape='open'), prop_l=dict(type='eraser', angle=-90.0), expr='talking')
        p = AC.boss_talk(t, LOUD, base=base)
        hands = None
        if tip is not None:
            ang = -100.0 + 12.0 * math.sin((g - HURR[0]) * 0.9)
            hands = {'l': {'tip': tip, 'prop': 'eraser', 'angle': ang, 'stretch': 1.25, 'bend': -0.4}}
        return p, hands
    # 'มันไม่ขึ้น' then 'ทางด่วนหรอก': he has turned to the hero (screen right); eraser stays in the (now far) left hand
    turn = smooth(WAG[0] - 2, WAG[0] + 5, g)
    yaw = -0.35 + 0.75 * turn
    if g < LEAN:
        b = AC.boss_finger_wag((g - WAG[0]) / 30.0 + 0.0, t0=0.0, dur=0.32, yaw=0.40, wags=3)
    else:
        b = AC.boss_lean_wink((g - LEAN) / 30.0, t0=0.0, wink_at=(WINK[0] - LEAN) / 30.0, wink_len=(WINK[1] - WINK[0]) / 30.0, yaw=0.40)
    b['yaw'] = yaw
    b['arm_l'] = dict(hand=(-0.40, 0.62), bend=0.3)
    b['prop_l'] = dict(type='eraser', angle=-80.0)
    p = AC.boss_talk(t, LOUD, base=b)
    if tip is not None:                                          # still releasing the line at the start of the wag
        return p, {'l': {'tip': tip, 'prop': 'eraser', 'angle': -100.0, 'stretch': 1.25, 'bend': -0.4}}
    return p, None


def hero_pose(g):
    t = (g - G0) / 30.0
    bl = [(gf(x) - G0) / 30.0 for x in (21.4, 22.0, 22.8)]
    p = AC.hero_listener(t, yaw=0.6, expr='unimpressed', blinks_at=bl,
                         gaze_shift=((gf(22.6) - G0) / 30.0, (0.9, -0.1), (0.4, 0.15)))
    return p, None


ACTORS = [
    dict(name='boss10', cast='boss', place=lambda g: (BOSS, False), pose=boss_pose, ppd=lambda g: 256 if g < SNAP[0] else 320),
    dict(name='hero10', cast='hero', place=lambda g: (HERO, True), pose=hero_pose, ppd=384),
]

NOTES = ["Framing 1 is a low single from (0.30, -4.10, 1.20) looking at (0.70, -0.42, 2.30), 1.2 D up, +16.5 deg, not the props module's low_boss: from low_boss the near hero at gloat_near is in frame (x 577, head 273 px), so the chief would not be alone. Here the chief is alone (head 190 px at x 474, centre 0.40 H), with the map and the red line at screen left and the ceiling boards above. The snap then pulls back, rises 1.6 D and pans right into G as planned.", "The x1.3 push is a zoom (22 -> 28.6 mm) plus a 0.3 D truck right. A dolly alone would grow the near hero x1.47 and break the 1.36-1.46 near/far ratio. G at the snap end: chief 173 px (397, 594), hero 244 px (620, 694), ratio 1.41. At the end of the push: chief 223 px, hero 317 px, ratio 1.42; the right frame edge crops about 20 % of the hero's head at the end (under 10 % in G itself).", "The chief's mouth is driven by acting.loudness(21.07, 23.13) through boss_talk on g 635-696 only; before and after it holds the smirk / flat drawing. The hero's mouth never moves.", "The chief faces the map (yaw -0.35) for the eraser bounce and the 'vroom' up the line (eraser pinned on the track, u 0.50 -> 0.92, g 644-667), then turns to the hero (yaw +0.40) over 7 frames at the start of 'มันไม่ขึ้น'; finger wag with the near hand, then lean 0.12 D + held wink g 692-695.", "The hero has no pencil behind his ear: the acting library's hero_listener draws none, and no ear-pencil drawing exists."]

NOTES += ["Red line: the client's hand-drawn track (office3d TRACK_STYLE 'hand'); every frame of this take was rendered after 18 Nov 14:40 (version 3), no ruler anywhere. Everything that touches the line (eraser, pencil points, smudge halo, camera look-at points) is placed with S.track_point(u) of the hand-drawn track.",
          "Colour: the raw render measured red 43-44 % and dark 0.16 (the red wallpaper fills more of these framings). The delivered frames carry the mild band grade ../s10/grade.py (red family rotated 8 deg toward orange, tapered, the pure track red spared; shadows under V 0.28 lifted by up to 0.07), the same grade on s10, s11 and s09; the change is not visible side by side (work/raw keeps the ungraded render)."]

CUES = [
    (20.30, 0.35, 'step', 'heavy step and waistcoat creak (the chief plants himself at the map, low angle)'),
    (20.45, 0.15, 'pat', 'eraser pat in his palm'),
    (20.75, 0.15, 'pat', 'eraser pat in his palm'),
    (20.82, 0.53, 'whoosh', 'whoosh: snap pull-back, rise and pan right into G'),
    (21.575, 0.38, 'squeak', "eraser squeak 'vroom' up the red line, toy beep-beep at the top"),
    (21.956, 0.33, 'tick', 'finger-wag ticks (three wags)'),
    (22.50, 0.45, 'chuckle', 'chuckle under the narrator (non-verbal), he leans toward the hero'),
    (22.95, 0.15, 'ting', 'wink ting (held wink 22.95-23.10)'),
    (20.32, 2.8, 'music', 'music: the tuba answers the theme'),
]

if __name__ == '__main__':
    O.run(sys.modules[__name__], sys.argv[1:])
