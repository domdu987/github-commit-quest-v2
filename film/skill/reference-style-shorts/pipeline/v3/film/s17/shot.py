#!/usr/bin/env python3
"""Take s17 = shot 17 (36.185-37.422, film g 1086..1122, handle in 9): office, office_grey (the dull drizzle morning).

Low camera (0.7 -> 0.9 D above the rug, 4.5 D from the map wall, +16 deg) trucking left with the chief and panning with him.
The chief strolls in from the window side behind the slumped hero (near-profile walk: bob 0.47 D, period 0.68 s, sway 0.13 D),
hands behind his back, pointer under his arm, whistling: ONE held round mouth (eyes shut, brows up), three note glyphs float off
(36.5, 36.8, 37.1); he reaches boss_mark and the camera settles over the last 6 frames.  The hero stands at gloat_near,
three-quarter to the lens, slumped and sad, turning the pencil stub; one blink at 37.0.  Map: red line with its smudge halo,
chalk curve, old tracks, the Thai label pinned (not featured), calendar leaf 21, rain running down the window.
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import otake as O                                       # noqa: E402
gf, gb, smooth, smoother, lerp = O.gf, O.gb, O.smooth, O.smoother, O.lerp
import acting as AC                                     # noqa: E402
import office3d as S                                    # noqa: E402
import office_props as X                                # noqa: E402

TAKE, SHOTS, VERSION, HI_MAP, LIGHT = 's17', [17], 2, False, 'office_grey'
G0, G1 = gb(36.185), gb(37.422)                         # 1086, 1123
H_IN, H_OUT = 9, 0                                      # dissolve 14 in (7 + 2); hard cut out into s18
TRANSITION_IN = dict(type='dissolve', frames=14, note='change of place: from the beach (s16, grey drizzle) into the grey office')
R0 = G0 - H_IN

BOSS = (1.30, -0.42, 0.0)                               # boss_mark
HERO = (2.40, -1.70, 0.0)                               # gloat_near
START = (2.20, -0.82, 0.0)                              # where the stroll is at t = 0 (window side, behind the hero)
_d = (BOSS[0] - START[0], BOSS[1] - START[1]); _L = math.hypot(*_d)
DIRW = (_d[0] / _L, _d[1] / _L)
ARRIVE = 1116                                           # he plants on boss_mark here (6 frames before the cut)
TW = 2 * 0.68                                           # two steps of the cycle: arrives on a contact phase
SPEED = _L / TW
GW = ARRIVE - TW * 30.0                                 # walk clock zero
NOTES = tuple((gf(x) - GW) / 30.0 for x in (36.5, 36.8, 37.1))
BLINK = gf(37.0)

C0 = (1.40, -4.50, 0.70)
C1 = (0.80, -4.50, 0.90)


def tw(g):
    return (g - GW) / 30.0


def boss_pose_raw(g):
    t = tw(g)
    if t < TW:
        return AC.boss_whistle_stroll(t, notes_at=NOTES, speed=SPEED, facing=-1)
    p = AC.boss_whistle_stroll(TW, notes_at=NOTES, speed=SPEED, facing=-1)
    p = dict(p)
    e = smooth(ARRIVE, ARRIVE + 5, g)
    legs = dict(p['legs']); legs['crouch'] = legs['crouch'] * (1 - e); p['legs'] = legs
    p['_lift'] = p['_lift'] * (1 - e); p['_adv'] = SPEED * TW
    p['lean'] = p['lean'] * (1 - 0.6 * e)
    p['head_dx'] = p.get('head_dx', 0.0) * (1 - e)
    p['_notes'] = [(t - a, i) for i, a in enumerate(NOTES) if 0.0 <= t - a < 1.1]
    return p


def boss_place(g):
    p = boss_pose_raw(g)
    a = p.get('_adv', 0.0)
    return ((START[0] + DIRW[0] * a, START[1] + DIRW[1] * a, p.get('_lift', 0.0)), False)


def boss_pose(g):
    return boss_pose_raw(g), None


def boss_notes(frame, p):
    q = boss_pose_raw(frame - 1)
    if not q.get('_notes'):
        return ''
    fig = AC.P.figure('boss', q, 'n')
    return AC.note_glyphs_svg(q['_notes'], fig['anchors']['mouth'], -1)


def hero_pose(g):
    t = (g - R0) / 30.0
    return AC.hero_slumped(t, yaw=0.5, blinks_at=((BLINK - R0) / 30.0,)), None


def _boss_canvas():
    import sprites
    ps = [dict(boss_pose_raw(g)) for g in range(R0, G1)] + [{}]
    c = sprites.canvas_for('boss', ps, margin=0.12)
    return (c[0] - 0.875, c[1] - 1.0, c[2] + 0.25, c[3])     # room ahead (screen-left) and above for the note glyphs


def cam(g):
    """truck left with the chief 0.6 D and rise 0.2 D on an ease that never parks; pan 11.6 -> 15.4 deg right (keeps the hero right of centre);
    settles over the last 6 frames (still moving 1-2 px per frame at the cut)."""
    x = (g - R0) / float(ARRIVE + 3 - R0)
    u = 0.82 * smooth(0.0, 1.0, x) + 0.18 * x if x < 1 else 1.0 + 0.004 * (g - ARRIVE - 3)
    loc = lerp(C0, C1, u)
    yaw = math.radians(11.6 + 3.8 * u)
    pitch = math.radians(14.5)
    d = 4.0
    look = (loc[0] + d * math.sin(yaw) * math.cos(pitch), loc[1] + d * math.cos(yaw) * math.cos(pitch), loc[2] + d * math.sin(pitch))
    return loc, look, None, 22.0


def props(g, f):
    S.set_track(1.0, 0.0, frame=f)
    X.set_smudge(3.0, frame=f)
    X.set_chalk(1.0, frame=f)
    for i in range(1, 7):
        X.set_ghost(i, 1.0, frame=f)
    X.set_tick(1.0, frame=f)
    X.set_label(1.0, frame=f)
    X.set_calendar(day=21, frame=f)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)


ACTORS = [
    dict(name='boss17', cast='boss', place=boss_place, pose=boss_pose, ppd=320, overlay=boss_notes),
    dict(name='hero17', cast='hero', place=lambda g: (HERO, True), pose=hero_pose, ppd=384),
]


def post_build(T):
    pass


def setup(T):
    for d in ACTORS:
        if d['cast'] == 'boss':
            d['canvas'] = _boss_canvas()


NOTES_QA = []

CUES = [
    (36.10, 3.5, 'bed', 'rain on the office window (bed), drizzle running down the panes'),
    (36.20, 1.2, 'whistle', 'jaunty whistled tune (the theme, non-verbal): the chief strolls in, held whistle mouth, three note glyphs'),
    (36.42, 0.08, 'heel', 'heel click on wood (contact of the walk cycle)'),
    (37.10, 0.08, 'heel', 'heel click on wood (he plants on boss_mark)'),
    (37.30, 0.08, 'heel', 'soft heel settle'),
    (37.00, 0.6, 'thunder', 'very distant thunder'),
]

QA_NOTES = [
    "Camera: lens 0.70 -> 0.90 D above the floor, 4.5 D from the map wall, truck left 0.6 D (the plan's 0.6 D/s over the whole take would be 0.9 D; 0.6 D keeps the near hero right of centre), pitch +14.5 deg (plan +16: lowered 1.5 deg so the head centres sit near 0.35 H), pan from 11.6 to 15.4 deg right of the wall normal. The plan's 20 -> 10 deg, read with these marks, puts the hero left of centre and the chief at the frame edge, so the pan turns the other way while the camera trucks left; the parallax still carries the chief right to left across the frame. Settles over the last 6 frames (ease, then 0.4 %/frame creep: never parked).",
    'Chief: acting.boss_whistle_stroll (held whistle drawing: eyes shut, brows up, round pucker; never flapping), hands behind his back, pointer tucked under the near arm, step 0.68 s, bob 0.47 D, sway 0.13 D, 0.72 D/s on a diagonal from (2.20, -0.82) to boss_mark, planted on a contact phase at g 1116, then the knees and the bob settle over 5 frames. He starts 0.82 D off the wall (plan 1.3 D) and emerges from behind the hero during the dissolve: from this low lens any path 1.3 D off the wall stays hidden behind the near hero for half the take. His head is 175-195 px (plan about 230): 230 px would put him 3.4 D from a lens that must also hold the hero at gloat_near.',
    'Three note glyphs (acting.note_glyphs_svg) leave the mouth at 36.5, 36.8, 37.1 (g 1098, 1107, 1116), drawn in the sprite overlay on an extended canvas.',
    'Hero at gloat_near, three-quarter to the lens facing the map side: acting.hero_slumped (lean 4 deg, head down, sad_down, turning the pencil stub), one blink at 37.0 (g 1113); his mouth never moves.',
    'Map state: red line complete with arrow head, smudge halo level 3, chalk curve, six old tracks, tick, Thai label pinned (not featured, top left), spinner at the storm symbol (0.5 rev/s); calendar leaf 21 set but off frame. The window wall is just outside the right frame edge in this framing, so the rain card is not seen; the rain remains a sound bed.',
    "Heel clicks in cues.json are at the walk's real contact frames (36.42, 37.10, settle 37.30), not the plan's 0.35 s spacing: the cycle steps every 0.68 s as the plan's walk numbers ask.",
    'qa_motion flags one near-constant-speed run g 1092-1101 (speed change under 2 %/frame): it is the peak of the smoothstep truck, not a linear move; left as is rather than re-render the take.',
    'Colour: grey light (special light per the plan). Orange 43.4 and dark share 0.17 are above the day band: the low lens fills the lower third with the warm plank floor and the dark under-ceiling; shade still reads blue-violet, magenta 2.9.',
]

if __name__ == '__main__':
    O.run(sys.modules[__name__], sys.argv[1:])
