#!/usr/bin/env python3
"""s01.py -- the first 5.0 s of the film: three shots, 150 frames at 30 fps.

    0.00-1.70 s  s01  insert   the wall map close; an arm with the red pencil enters and draws the track north
    1.70-3.40 s  s02  medium   the hero at the map finishes the track with a jab at New York, turns to the viewer
    3.40-5.00 s  s03  two-shot the chief rubs the track out (far); the hero, pushed toward the lens, goes wide-eyed (near)

All times are OUTPUT frame numbers g (0-based, 30 fps).  A shot function may be asked for frames outside its own range:
those are the handles a transition needs (both shots keep moving through a dissolve).

Edit and camera grammar (see out/HOOK_STUDY.md for the reference beats this copies):
    g 10-24    snap push x1.50 onto the pencil            (clip B f21-30: whip-push onto the hand)
    g 46-62    snap pull-out x0.51, shot change hidden in it by a 9-frame smoothstep dissolve centred on g 51
               (clip B f58-80 pull back x0.46; clip A f276-277 cut hidden in a fast move; 9 frames = quick continuity)
    g 80-95    snap push x1.43 on the jab                  (clip A f1362-1380 push x1.38)
    g 99-104   whip pan with a cut inside it               (clip B f158-164)
    g 128-143  snap push x1.40 onto the wide-eyed hero with speed lines   (clip B f141-157 punch-in)
Between the snaps the camera drifts; it is never linear and never parked.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sets"))
sys.path.insert(0, os.path.join(HERE, "..", "puppet"))
from anim import ease, keys, cam_keys, blink, swap, pulse, lerp, clamp    # noqa: E402
import office                                                            # noqa: E402

FPS = 30
N_FRAMES = 150
TRACK = office.track_point            # u in 0..1 -> (x, y, heading)
STORM = office.TRACK[0]
NY = office.TRACK[-1]

SHOTS = [                             # out_start..out_end inclusive; head / tail = handle frames rendered beyond the range
    dict(name="s01", out_start=0, out_end=50, head=0, tail=5),
    dict(name="s02", out_start=51, out_end=101, head=4, tail=0),
    dict(name="s03", out_start=102, out_end=149, head=0, tail=0),
]
TRANSITIONS = [
    dict(kind="dissolve", a="s01", b="s02", first=47, frames=9),      # mix on g 47..55, smoothstep, centred on g 51 = 1.70 s
    dict(kind="whip", a="s02", b="s03", at=102),                      # hard cut inside a blurred pan (no mix)
]

# narration: "He drew a line on a weather map pointing straight at New York, and his boss erased it."  (18 words, 218 wpm)
CAPS = [
    (0.00, 0.40, "He drew"),
    (0.40, 0.80, "a line"),
    (0.80, 1.14, "on a"),
    (1.14, 1.70, "weather map"),
    (1.70, 2.20, "pointing"),
    (2.20, 2.80, "straight at"),
    (2.80, 3.40, "New York,"),
    (3.40, 3.95, "and his boss"),
    (3.95, 4.47, "erased"),
    (4.47, 4.95, "it."),
]


# ============================================================================= story state shared by the shots
def line_at(g):
    """how much of the red track is drawn (0..1).  One function for s01 and s02 so the line matches through the dissolve."""
    return keys(g, [(9, 0.0, "quad_in"), (16, 0.06, "lin"), (51, 0.75, "cubic_out"), (77, 0.92, "hold"),
                    (80, 0.92, "cubic_in"), (83, 1.0, "hold")])


def erase_at(g):
    """fraction of the track rubbed out from the New York end (s03)."""
    return keys(g, [(104, 0.0, "sine"), (116, 0.42, "sine"), (131, 1.0, "hold")])


def state(g):
    return dict(line=line_at(g), erase=erase_at(g), t=g / float(FPS))


# ============================================================================= cameras
# s01 follows the pencil: the two follow keys are built from where the pencil tip is on those frames.
def _follow(g, sx, sy, zoom):
    x, y, _ = TRACK(line_at(g))
    return (x - (sx - 360.0) / zoom, y - (sy - 640.0) / zoom, zoom)


CAM_PULL = (-0.31, -2.00, 176.0)          # end of the pull-out: medium on the hero at the map, feet and floor in frame
CAM_JAB = (-0.38, -2.36, 268.0)           # after the snap on the jab: head 238 px, New York beside it


def cam1(g):
    """s01 (and the first half of the pull-out it shares with s02)."""
    return cam_keys(g, [(0, (0.20, -2.06, 208.0), "quad_out"),          # opening drift, already moving on frame 0
                        (10, (0.19, -2.02, 220.0), "sine"),             # snap push x1.5 onto the pencil
                        (24, _follow(24, 388, 668, 330.0), "sine"),     # follow the pencil north, drifting in
                        (46, _follow(46, 372, 640, 348.0), "sine"),     # snap pull-out x0.51 (shared with s02)
                        (62, CAM_PULL, "hold")])


def cam2(g):
    if g <= 62:
        return cam1(g)                                                   # the same move on both sides of the dissolve
    c = cam_keys(g, [(62, CAM_PULL, "sine"),                             # drift in and slide
                     (80, (-0.325, -2.03, 188.0), "sine"),               # snap push x1.43 on the jab
                     (95, CAM_JAB, "sine"),
                     (101, (-0.385, -2.365, 271.0), "hold")])
    # whip pan off to the right on the last three frames (picture slides left), accelerating
    off = keys(g, [(98, 0.0, "quad_in"), (101, 1.62, "hold")])
    return (c[0] + off, c[1] - 0.03 * off, c[2])


CAM_TWO = (0.15, -2.24, 166.0)            # two-shot staged in depth
CAM_HERO = (-0.18, -2.305, 244.0)          # snap onto the wide-eyed hero, the smudge and the chief still in frame


def cam3(g):
    c = cam_keys(g, [(101, (0.15, -2.11, 118.0), "cubic_out"),           # arrives pushing in, easing out (clip B f164-169)
                     (115, CAM_TWO, "sine"),                             # drift
                     (128, (0.12, -2.255, 174.0), "sine"),               # snap push x1.40 onto the hero
                     (143, CAM_HERO, "quad_out"),
                     (149, (-0.184, -2.307, 246.5), "hold")])
    # whip pan on: the camera is still travelling right when the shot starts and brakes hard (two streaked frames)
    off = -2.4 * (1.0 - ease((g - 101) / 5.0, "quart_out"))
    return (c[0] + off, c[1] - 0.03 * off, c[2])


# ============================================================================= s01: insert, arm only
ARM_K = 1.8                     # the arm is drawn 1.8 x the set scale: the insert is a macro view (reference insert: limb
                                # 24 px, hand ball 56 px at 720 px width), the body stays off frame
PENCIL_ANGLE = -52.0


def shot1(g):
    cam = cam1(g)
    st = state(g)
    tx, ty, _ = TRACK(st["line"])
    # the hand comes in from the lower left and lands on the storm symbol at g 9
    e_in = 1.0 - ease(g / 9.0, "cubic_out")
    tip = (tx - 1.15 * e_in, ty + 0.80 * e_in)
    ang = PENCIL_ANGLE - 10.0 * e_in + 2.5 * math.sin(g * 0.45) * (1 - e_in)
    # shoulder just outside the left frame edge, a little below the hand: only the arm is in frame
    left = cam[0] - 360.0 / cam[2]
    hand_y = tip[1] + 0.36 * ARM_K * math.sin(math.radians(-ang))
    hand_x = tip[0] - 0.36 * ARM_K * math.cos(math.radians(ang))
    sh = (max(left - 0.14, hand_x - 1.40), hand_y + 0.58 + 0.25 * e_in)      # never farther than the arm can reach
    hero = dict(cast="hero", uid="h1", scale=ARM_K, place=dict(anchor="shoulder_r", at=sh), shadow=0,
                pose=dict(yaw=0.55, pitch=-0.3, expr="determined", arm_l="down", limb_w=0.054 * 0.80,
                          head_dx=-0.8, head_dy=0.25,          # head pushed off frame: only the arm may show in the insert
                          arm_r=dict(preset="reach_up", stretch=1.25, bend=-0.28, sharp=0.15)),
                hands={"r": {"tip": tip, "prop": "pencil", "angle": ang}})
    return dict(set="insert", state=st, cam=cam, actors=[hero])


# ============================================================================= s02: medium, the hero finishes the track
HERO_X = -0.82


def shot2(g):
    cam = cam2(g)
    st = state(g)
    tx, ty, _ = TRACK(st["line"])
    # --- body: draws, gathers (g 77-80), jabs (g 80-83) with a small overshoot, settles, turns to the viewer (g 84-92)
    turn = ease((g - 84) / 8.0, "sine")
    lean = keys(g, [(47, 4.0, "sine"), (66, 4.0, "sine"), (74, 5.5, "sine"), (76, 5.5, "sine"), (80, 2.0, "back_out"),
                    (84, 9.0, "sine"), (93, 3.5, "hold")])
    roll = keys(g, [(47, 7.0, "sine"), (64, 7.0, "sine"), (72, 13.0, "sine"), (76, 13.0, "sine"), (80, 8.0, "back_out"),
                    (84, 17.0, "sine"), (92, -10.0, "hold")])
    crouch = pulse(g, 76, 80, 83, 0.07)
    sq = pulse(g, 76, 80, 82, 1.0)                 # gather: wider and shorter
    st_ = pulse(g, 80, 83, 89, 1.0, "cubic_in")    # jab: taller and thinner, then settle
    squash = (1.0 + 0.025 * sq - 0.02 * st_, 1.0 - 0.03 * sq + 0.03 * st_)
    yaw = 0.55 + (-0.10 - 0.55) * turn
    pitch = -0.4 + 0.35 * turn
    hdx = 0.05 * pulse(g, 80, 84, 92, 1.0, "cubic_in")
    bl = blink(g, [59, 87])
    pose = dict(yaw=yaw, pitch=pitch, head_roll=roll, lean=lean, head_dx=hdx, squash=squash, expr="determined", blink=bl,
                gaze=(0.85 * (1 - turn), -0.45 * (1 - turn)), arm_l="hip",
                legs=dict(preset="stand", crouch=crouch),
                arm_r=dict(preset="reach_up", stretch=1.12))
    # --- right hand: the pencil point is ON the end of the red line until the jab has landed, then the hand comes away
    away = ease((g - 85) / 8.0, "sine")
    ang = -60.0 + 4.0 * pulse(g, 76, 80, 83, 1.0) - 26.0 * away
    rest = (HERO_X + 0.66, -2.47 + 0.10)            # where the pencil point rests when he turns: up beside his head
    tip = (tx + (rest[0] - tx) * away, ty + (rest[1] - ty) * away - 0.10 * math.sin(math.pi * away))
    hero = dict(cast="hero", uid="h2", x=HERO_X, y=0.0, pose=pose, shadow=0.9,
                hands={"r": {"tip": tip, "prop": "pencil", "angle": ang}})
    return dict(set="office", state=st, cam=cam, actors=[hero])


# ============================================================================= s03: two-shot in depth, the chief rubs it out
BOSS_X0, BOSS_X1 = 0.97, 0.84
HERO3 = dict(x=-1.05, y=1.20, scale=1.40)          # pushed toward the lens: 1.40 x the chief, feet lower on the floor
SHOCK_AT = 123                                     # the closed frame of the hero's blink: determined -> shocked


def shot3(g):
    cam = cam3(g)
    st = state(g)
    er = st["erase"]
    keep = st["line"] * (1.0 - er)
    # --- the chief: the eraser scrubs across the line while it travels down it; his body follows the eraser
    done = ease((g - 131) / 9.0, "sine")               # after the last stroke he straightens up and looks at the hero
    ex, ey, hd = TRACK(min(1.0, keep + 0.055))
    ph = (g - 102) * 2 * math.pi / 5.0                 # one scrub stroke every 5 frames
    amp = 0.055 * (1 - done) * clamp((g - 101) / 3.0)
    nx, ny = math.cos(math.radians(hd + 90)), math.sin(math.radians(hd + 90))
    lx, ly = math.cos(math.radians(hd)), math.sin(math.radians(hd))
    e_tip = (ex + nx * amp * math.sin(ph) + lx * 0.018 * math.cos(ph), ey + ny * amp * math.sin(ph) + ly * 0.018 * math.cos(ph))
    lift = (0.42, -1.72)                               # where the eraser ends up when he is done (held up, off the map)
    e_tip = (e_tip[0] + (lift[0] - e_tip[0]) * done, e_tip[1] + (lift[1] - e_tip[1]) * done - 0.06 * math.sin(math.pi * done))
    e_ang = -140.0 + 9.0 * math.sin(ph) * (1 - done) + 25.0 * done
    bx = BOSS_X0 + (BOSS_X1 - BOSS_X0) * er - 0.02 * done
    b_pose = dict(yaw=-0.5 + 0.28 * done, head_roll=keys(g, [(102, -8.0, "sine"), (116, -8.0, "sine"), (122, -14.0, "sine"),
                                                            (131, -14.0, "sine"), (140, 9.0, "hold")]),
                  lean=-3.0 - 8.0 * er + 7.0 * done, expr="smug", blink=blink(g, [112, 134]),
                  gaze=(-0.7 + 0.3 * done, 0.5 * er * (1 - done)),
                  legs=dict(preset="stand", crouch=0.07 * er * (1 - 0.7 * done)),
                  arm_r="hip", arm_l=dict(preset="rub", stretch=1.18, bend=-0.5))
    boss = dict(cast="boss", uid="b3", x=bx, y=0.0, pose=b_pose, shadow=0.95,
                hands={"l": {"tip": e_tip, "prop": "eraser", "angle": e_ang}})
    # --- the hero: frozen (under 0.04 D), blinks, and changes drawing on the closed frame of the second blink
    shocked = g >= SHOCK_AT
    sq = pulse(g, SHOCK_AT - 1, SHOCK_AT + 1, SHOCK_AT + 5, 1.0)
    h_pose = dict(yaw=0.62, pitch=-0.15, head_roll=-7.0 - 2.0 * (1 if shocked else 0), lean=2.0,
                  squash=(1.0 + 0.012 * sq, 1.0 - 0.012 * sq),
                  expr="shocked" if shocked else "determined", blink=blink(g, [108, SHOCK_AT - 1, 142]),
                  gaze=(0.9, -0.15), fx=(["sweat"] if shocked else []),
                  arm_l="down", arm_r=dict(hand=(0.50, 0.54), bend=-0.6, sharp=0.3),
                  prop_r=dict(type="pencil", angle=-76.0), legs="stand")
    hero = dict(cast="hero", uid="h3", pose=h_pose, shadow=0.95, **HERO3)
    # background defocus only once the snap has made this a close-up (hero head over 300 px): set layers only
    spec = dict(set="office", state=st, cam=cam, actors=[boss, hero], bg_blur=3.2 * ease((g - 130) / 13.0, "sine"))
    if shocked:                                        # speed lines from the swap on, redrawn every frame (clip B f143-157)
        spec["focus_actor"] = "h3"
        spec["focus"] = dict(seed=g, r0=1.15, n=36, opacity=0.7 * clamp((g - SHOCK_AT + 1) / 2.0))
    return spec


SHOT_FN = dict(s01=shot1, s02=shot2, s03=shot3)
CAM_FN = dict(s01=cam1, s02=cam2, s03=cam3)


def frames_of(shot):
    return range(shot["out_start"] - shot["head"], shot["out_end"] + shot["tail"] + 1)


def source_of(g):
    """which raw frame(s) make output frame g: [(shot name, g)] or [(a, g), (b, g), weight_of_b]."""
    for tr in TRANSITIONS:
        if tr["kind"] == "dissolve" and tr["first"] <= g < tr["first"] + tr["frames"]:
            i = g - tr["first"] + 1
            p = i / float(tr["frames"] + 1)
            return [(tr["a"], g), (tr["b"], g), p * p * (3 - 2 * p)]
    for s in SHOTS:
        if s["out_start"] <= g <= s["out_end"]:
            # inside a dissolve handled above; otherwise the owning shot.  Frames before a dissolve midpoint belong to a.
            return [(s["name"], g)]
    raise ValueError(g)
