#!/usr/bin/env python3
"""Take s11 = shot 11 (23.129-26.406, film g 694..791, handles 7 + 8): office, office_day. The erase-and-redraw running gag as
ONE stepped pull-out (persist_steps).
(a) insert_rake_ny on the N.Y. end: the chief's hand rubs three times (erase 0 -> 0.6), the smudge halo grows;
(b) same framing, the camera slides down 0.4 D and back up with the pencil: the hero's hand redraws the same bold stroke
    freehand along the hand-drawn track (erase 0.6 -> 0); no ruler (client change);
(c) snap out 24.35-24.82 to the low two-shot at the wall (low_two_wall): the chief rubs with big strokes (erase 0.8), steam,
    reddening; 'ลากอีก' the hero redraws in one 8-frame swipe with a pencil stub; the chief freezes, purple, eye twitching;
(d) snap out and up 25.33-25.80 to high_two_shot: bold red line in a halo of pink smudges, crumbs on the ledge, the chief pants
    with a worn nub, the hero at ease, chin up, the pencil stub in his hand; near still 26.0-26.27, then drift.
Hands in the insert are hand cards (the take-A method: a card facing the lens, standing just in front of the contact point,
scaled x1.8 so the elbow and the body are outside the frame); the bodies appear in the snap of (c).
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(DIR), 's10'))
import otake as O                                       # noqa: E402
import numpy as np                                      # noqa: E402
gf, gb, smooth, smoother, lerp = O.gf, O.gb, O.smooth, O.smoother, O.lerp
import acting as AC                                     # noqa: E402
import office3d as S                                    # noqa: E402
import office_props as X                                # noqa: E402

TAKE, SHOTS, VERSION, HI_MAP = 's11', [11], 3, False
G0, G1 = gb(23.129), gb(26.406)                         # 694, 792
H_IN, H_OUT = 7, 8                                      # dissolve in 9 f (4.5 + 2 -> 7), out 11 f (5.5 + 2 -> 8)
TRANSITION_IN = dict(type='dissolve', frames=9, note="the chief's hand already swinging in")

RUBS = (gf(23.15), gf(23.60))                           # 698 - 711: three rubs, erase 0 -> 0.6
CLACK = gf(23.68)                                       # 714 the hero's hand arrives at the map (no ruler)
DRAW = (gf(23.75), gf(24.30))                           # 716 - 732 pencil redraw, erase 0.6 -> 0
SNAP_C = (gf(24.35), gf(24.82))                         # 733 - 747
FRANTIC = (gf(24.75), gf(24.75) + 10)                   # 746 - 756: four frantic rubs, erase 0 -> 0.8
SWIPE = gf(25.25)                                       # 761: 8-frame swipe redraw, erase 0.8 -> 0
SNAP_D = (gf(25.33), gf(25.80))                         # 763 - 777
STILL = (gf(26.0), gf(26.27))                           # 783 - 791 near still
R0, R1 = G0 - H_IN, G1 + H_OUT                          # 687, 800

HERO = (-0.55, -0.42, 0.0)                              # hero_mark
BOSS = (1.30, -0.42, 0.0)                               # boss_mark

IA = ((-1.30, -0.66, 2.55), (0.30, -0.05, 2.74))        # insert_rake_ny
IB = ((-1.30, -0.66, 2.15), (0.30, -0.05, 2.49))        # persist step b: 0.4 D lower
LW = ((0.40, -3.70, 1.20), (0.40, 0.0, 2.12))           # low_two_wall
HT = ((1.80, -5.90, 3.70), (1.35, -0.60, 1.55))         # high_two_shot


def push(c, k):
    return lerp(c[0], c[1], k), c[1]


def cam_base(g):
    if g < SNAP_C[0]:
        # (a) a slow push in following the eraser down a little; (b) down 0.4 D by the pencil's start, back up with it
        d = smooth(R0 + 14, DRAW[0] + 1, g) - 0.9 * smooth(DRAW[0] + 1, SNAP_C[0] + 3, g)
        k = 0.012 * (g - R0) / 30.0 * 3.0
        loc, look = lerp(IA[0], IB[0], d), lerp(IA[1], IB[1], d)
        return lerp(loc, look, k), look
    endb = cam_base(SNAP_C[0] - 1)
    if g < SNAP_C[1]:
        u = smoother((g - SNAP_C[0] + 1) / float(SNAP_C[1] - SNAP_C[0] + 1))
        return lerp(endb[0], LW[0], u), lerp(endb[1], LW[1], u)
    if g < SNAP_D[0]:                                    # drift push 8 %/s
        k = 0.08 * (g - SNAP_C[1]) / 30.0 * (1 + 0.15 * math.sin((g - SNAP_C[1]) / 6.0))
        return push(LW, k)
    endc = push(LW, 0.08 * (SNAP_D[0] - SNAP_C[1]) / 30.0)
    if g < SNAP_D[1]:
        u = smoother((g - SNAP_D[0]) / float(SNAP_D[1] - SNAP_D[0]))
        loc = lerp(endc[0], HT[0], u)
        return (loc[0], loc[1], loc[2] + 0.25 * math.sin(math.pi * u)), lerp(endc[1], HT[1], smoother(min(1, u * 1.08)))
    # settle: an eased creep into the near still (hold 1), then a drift push
    if g < STILL[0]:
        x = (g - SNAP_D[1]) / float(STILL[0] - SNAP_D[1])
        k = 0.012 * (1 - (1 - x) ** 2)
    elif g < STILL[1]:
        k = 0.012 + 0.0007 * (g - STILL[0])
    else:
        k = 0.012 + 0.0007 * (STILL[1] - STILL[0]) + 0.0007 * (g - STILL[1]) + 0.03 * ((g - STILL[1]) / 30.0) ** 1.5
    return push(HT, k)


def cam(g):
    loc, look = cam_base(g)
    return loc, look, None, 22.0


# ----------------------------------------------------------------------------- story state
def erase_at(g):
    if g < RUBS[0]:
        return 0.0
    if g <= RUBS[1] + 2:
        k = (g - RUBS[0]) / 4.0                          # one rub every 4 frames: a quick bite then a hold
        n, fr = int(k), k - int(k)
        return min(0.6, 0.2 * (n + smoother(min(1.0, fr * 2.0))))
    if g < DRAW[0]:
        return 0.6
    if g <= DRAW[1]:
        return 0.6 * (1 - smoother((g - DRAW[0]) / float(DRAW[1] - DRAW[0])))
    if g < FRANTIC[0]:
        return 0.0
    if g <= FRANTIC[1]:
        k = (g - FRANTIC[0]) / 2.5
        n, fr = int(k), k - int(k)
        return min(0.8, 0.2 * (n + smoother(min(1.0, fr * 1.6))))
    if g < SWIPE:
        return 0.8
    if g <= SWIPE + 8:
        return 0.8 * (1 - smoother((g - SWIPE) / 8.0))
    return 0.0


def props(g, f):
    S.set_track(1.0, erase_at(g), frame=f)
    X.set_chalk(1.0, frame=f)
    for i in range(1, 7):
        X.set_ghost(i, 1.0, frame=f)
    X.set_tick(1.0, frame=f)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)
    X.set_smudge(1.0 * smooth(RUBS[0], RUBS[1] + 3, g) + 1.0 * smooth(FRANTIC[0], FRANTIC[1] + 4, g) + 1.0 * smooth(SNAP_D[0], SNAP_D[1], g), frame=f)
    X.set_crumbs(0.45 * smooth(FRANTIC[0], FRANTIC[1] + 4, g) + 0.55 * smooth(SNAP_D[0] + 4, SNAP_D[1] + 6, g), frame=f)
    X.set_ruler(0.0, frame=f)                            # client change: no ruler anywhere in the film


# ----------------------------------------------------------------------------- hand cards of the insert
HS = 1.5                                                 # hand card scale


def _basis(g):
    c = cam(g)
    fw, r, u = O.cam_basis(c[0], c[1], None)
    fh = np.array([fw[0], fw[1], 0.0]); fh /= np.linalg.norm(fh)
    rh = np.array([r[0], r[1], 0.0]); rh /= np.linalg.norm(rh)
    return np.asarray(c[0]), fh, rh


def tp(u):
    p = S.track_point(u)
    return np.array([p[0], p[1] - 0.003, p[2]])


def boss_hand_tip(g):
    """world target of the eraser face in the insert (rubs at the erase front), with the swing in and the exit."""
    e = erase_at(g)
    u = min(1.0, 1.0 - e + 0.03)
    p = tp(u)
    loc, fh, rh = _basis(g)
    ph = (g - RUBS[0]) * 2 * math.pi / 4.0
    on = smooth(RUBS[0] - 2, RUBS[0], g) * (1 - smooth(RUBS[1], RUBS[1] + 3, g))
    p = p + np.array([0.05, 0, 0.012]) * math.sin(ph) * on
    appr = 1 - smooth(R0, RUBS[0] - 1, g)               # swings in from the lower right
    away = smooth(RUBS[1] + 2, RUBS[1] + 9, g)
    return p + (rh * 0.55 - np.array([0, 0, 0.35])) * appr + (rh * 0.75 + np.array([0, 0, -0.25])) * away


def hero_hand_tip(g):
    e = erase_at(g)
    p = tp(1.0 - e + 0.004)
    loc, fh, rh = _basis(g)
    appr = 1 - smooth(CLACK - 4, DRAW[0], g)
    away = smooth(DRAW[1] + 1, DRAW[1] + 8, g)
    if g < DRAW[0]:
        p = tp(0.4 + 0.004)
    return p + (rh * 0.6 - np.array([0, 0, 0.4])) * appr + (rh * 0.8 + np.array([0, 0, -0.3])) * away


def hand_place(tipfn, shoulder, lateral, drop):
    """feet of a hand card: just in front of the tip along the view, `lateral` D to screen-right, shoulder `drop` above it."""
    def place(g):
        if g >= SNAP_C[0]:
            g = SNAP_C[0] - 1
        loc, fh, rh = _basis(g)
        t = tipfn(g)
        f = t - fh * 0.05 + rh * lateral
        f = np.array([f[0], f[1], t[2] + drop - shoulder * HS])
        return tuple(float(x) for x in f), False, HS
    return place


def boss_hand_pose(g):
    p = dict(yaw=-0.5, expr='smug', arm_r='hip', arm_l='hip', legs='stand')
    ang = -150.0 + 10.0 * math.sin((g - RUBS[0]) * 2 * math.pi / 4.0)
    return p, {'l': {'tip': tuple(boss_hand_tip(g)), 'prop': 'eraser', 'angle': ang, 'stretch': 1.25, 'bend': -0.4}}


def hero_hand_pose(g):
    p = dict(yaw=-0.5, expr='determined', arm_r='hip', arm_l='hip', legs='stand')
    return p, {'l': {'tip': tuple(hero_hand_tip(g)), 'prop': 'pencil', 'angle': -128.0, 'stretch': 1.25, 'bend': -0.3}}


# ----------------------------------------------------------------------------- full bodies, (c) and (d)
WHOLE_STREAK = range(SNAP_C[0] + 3, SNAP_C[0] + 10)    # the bodies enter inside the snap: those frames are streaked whole
REVEAL = SNAP_C[0] + 6                                   # bodies appear inside the snap


def boss_tip_c(g):
    e = erase_at(g)
    u = min(1.0, 1.0 - e + 0.04)
    p = tp(u)
    ph = (g - FRANTIC[0]) * 2 * math.pi / 2.5
    on = smooth(FRANTIC[0] - 2, FRANTIC[0], g) * (1 - smooth(FRANTIC[1], FRANTIC[1] + 3, g))
    p = p + np.array([0.08, 0, 0.02]) * math.sin(ph) * on
    pre = 1 - smooth(REVEAL, FRANTIC[0] - 1, g)
    post = smooth(FRANTIC[1] + 1, FRANTIC[1] + 6, g)
    return p + np.array([0.30, -0.05, 0.25]) * pre + np.array([0.28, -0.05, -0.10]) * post


def boss_pose(g):
    if g < SNAP_D[0] + 8:
        if g <= FRANTIC[1] + 6:
            t = (g - (FRANTIC[0] - 4)) / 30.0
            p = AC.boss_rub_furious(max(0.0, t), t0=0.0, stroke=0.083, fill_len=0.35, yaw=-0.5)
            p['arm_r'] = 'hip'
            ang = -40.0 + 12.0 * math.sin((g - FRANTIC[0]) * 2 * math.pi / 2.5) - 100.0
            return p, {'l': {'tip': tuple(boss_tip_c(g)), 'prop': 'eraser', 'angle': ang, 'stretch': 1.22, 'bend': -0.5}}
        p = AC.boss_frozen_purple((g - SWIPE) / 30.0, twitch_every=0.27, yaw=-0.5)
        p['arm_l'] = dict(hand=(-0.50, 0.45), bend=0.4); p['prop_l'] = dict(type='eraser', angle=-120.0)
        return p, None
    t = (g - (SNAP_D[1] + 1)) / 30.0
    p = AC.boss_pant(max(0.0, t), pants_at=(max(0.0, (gf(25.9) - SNAP_D[1] - 1) / 30.0), (gf(26.25) - SNAP_D[1] - 1) / 30.0), yaw=-0.45, nub=True)
    return p, None


def hero_tip_c(g):
    u = 0.2 + 0.8 * smoother((g - SWIPE) / 8.0)
    return tp(min(1.0, u + 0.004))


def hero_pose(g):
    if g < SWIPE - 4:
        t = (g - REVEAL) / 30.0
        p = AC.hero_listener(t, yaw=0.55, expr='unimpressed', blinks_at=((gf(24.95) - REVEAL) / 30.0,), gaze_shift=(99.0, (0.9, -0.1), (0.9, -0.1)))
        return p, None
    if g <= SWIPE + 10:
        p = AC.hero_redraw((g - SWIPE) / 30.0, t0=0.0, swipe=8, yaw=0.55, stub=True)
        p['arm_l'] = 'hip'
        return p, {'r': {'tip': tuple(hero_tip_c(min(g, SWIPE + 8))), 'prop': 'stub', 'angle': -55.0, 'stretch': 1.15, 'bend': -0.3}}
    t = (g - (SWIPE + 11)) / 30.0
    p = dict(yaw=0.5, expr='neutral', pitch=-0.3, head_roll=-4.0, blink=AC.blinks(t, ((gf(26.05) - SWIPE - 11) / 30.0,)), legs='stand',
             arm_r=dict(hand=(0.34, 0.80), bend=0.6), prop_r=dict(type='stub', angle=-70.0), arm_l='down',
             head_dy=0.004 * math.sin(t * 2.0))                 # at ease, chin up, the pencil stub in hand (no ruler)
    return p, None


ACTORS = [
    dict(name='bossH11', cast='boss', canvas=(-1.9375, -3.625, 0.5, -1.25), contact=False, shadow=None,
         place=hand_place(boss_hand_tip, 2.44, 1.50, 0.50), pose=boss_hand_pose, ppd=512,
         hidden=lambda g: g > RUBS[1] + 9),
    dict(name='heroH11', cast='hero', canvas=(-1.8125, -3.125, 0.5, -0.875), contact=False, shadow=None,
         place=hand_place(hero_hand_tip, 1.92, 1.25, 0.45), pose=hero_hand_pose, ppd=512,
         hidden=lambda g: g < CLACK - 4 or g > DRAW[1] + 8),
    dict(name='boss11', cast='boss', place=lambda g: (BOSS, False), pose=boss_pose, ppd=320, hidden=lambda g: g < REVEAL),
    dict(name='hero11', cast='hero', place=lambda g: (HERO, False), pose=hero_pose, ppd=320, hidden=lambda g: g < REVEAL),
]


NOTES = ["Hands in the insert (a, b) are hand cards, the take-A method: the chief's and the hero's puppets at scale 1.5, facing the lens, standing 0.05 D in front of the contact point, so the drawn eraser face and pencil point register on the map. Their heads and bodies lie outside the frame and the elbows leave it at the right edge. These cards cast no shadow, because their scaled bodies would darken the map. Both hands enter from the room side (screen right): the insert lens stands where the hero's body is (hero_mark is 0.8 D in front of it).", "The full bodies are hidden in (a, b) and enter inside the snap of (c) at g 739, while the camera moves 100-200 px per frame; g 736-742 are streaked as whole frames so the entry does not pop. Physically the chief at boss_mark would stand in the insert's background at x of about 560: an accepted deviation.", 'Erase states: 0 -> 0.6 in three 4-frame bites (g 698-711), 0.6 -> 0 with the pencil (g 716-732), 0 -> 0.8 in four frantic rubs (g 746-756), 0.8 -> 0 in one 8-frame swipe with the pencil stub (g 761-769). The smudge halo grows 0 -> 1 -> 2 -> 3; crumbs 0 -> 0.45 -> 1 on the ledge. No ruler (client change): the hero redraws the same bold stroke freehand, his pencil point pinned on the hand-drawn track (track_point).', "The chief stays 'frozen purple' through the start of the snap (d) and swaps to the panting drawing (worn eraser nub, prop scale 0.6) at g 771 inside the snap. In (d) the hero stands at ease, chin up, the pencil stub in his near hand (no ruler).", 'In (d) the heads are 138-148 px (the reviewed high_two_shot, wide, as planned). The hero stands at x of about 100.']

NOTES += ["Red line: the client's hand-drawn track (office3d TRACK_STYLE 'hand'); every frame of this take was rendered after 18 Nov 14:40 (version 3), no ruler anywhere. Everything that touches the line (eraser, pencil points, smudge halo, camera look-at points) is placed with S.track_point(u) of the hand-drawn track.",
          "Colour: the ungraded render sits inside the office_day band (red 33.0, orange 37.4, dark 0.14), so this take is delivered ungraded. (s10 and s09 carry the mild band grade ../s10/grade.py because their framings hold more red wallpaper; a test of that grade here pushed red to 29 and orange to 41, out of band.)",
          "Registration: the hand cards and the chief's eraser are pinned on the erase front of the hand-drawn track (0.0 px in the inserts). In the four frantic rubs of (c) the chief's arm reaches its limit at the end of strokes: 4.7-10.3 px on g 751-754, 29 px on g 756 and 21 px on g 759 (the release stroke, the eraser leaving the paper); g 740 (heroH11 56 px) is a whole-streaked snap frame in which the hand card leaves."]

CUES = [
    (23.13, 3.25, 'music', 'music: wood-block ostinato, speeding up'),
    (23.15, 0.15, 'squeak', 'eraser squeak 1'), (23.28, 0.15, 'squeak', 'eraser squeak 2'), (23.42, 0.18, 'squeak', 'eraser squeak 3'),
    (23.75, 0.55, 'zip', 'pencil zip, freehand up the red line, rising'),
    (24.35, 0.47, 'whoosh', 'whoosh: snap out to the low two-shot'),
    (24.75, 0.45, 'rub', 'four frantic rubs with a kettle whistle (steam)'),
    (25.25, 0.27, 'zip', 'fast zip, higher (one 8-frame swipe with the pencil stub)'),
    (25.33, 0.47, 'whoosh', 'whoosh: snap out and up to the high two-shot'),
    (25.80, 0.3, 'ding', 'ta-da ding: bold red line in its halo of smudges'),
    (25.90, 0.5, 'pant', 'chief panting (two pants), crumbs pattering on the ledge'),
]

if __name__ == '__main__':
    O.run(sys.modules[__name__], sys.argv[1:])
