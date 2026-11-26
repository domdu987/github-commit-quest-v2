"""S04  'บนทางด่วน รถชนกันเป็นแพ'  -- E3 lane fly-through: one-point dolly between the car rows past stranded people,
fast then easing, toward the wreck."""
from shots.base import *
ID = "S04"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale


def setup(F):
    F.hide_roots(["headlight_l2_b_-1", "headlight_l2_b_1", "cone_headlight_l2_b_-1", "cone_headlight_l2_b_1"])   # the SUV behind the wreck: its lamps sat next to the heads in this lens
    # the stranded drivers stand by their cars AHEAD of where the dolly stops (y 10), never beside the lens: the nearest
    # is 6 D from the camera at the end of the move, so every one reads as a whole figure
    for i, e in enumerate(F.extras[:6]):
        x0 = (-7.85, -5.25)[i % 2]; y0 = 16.0 + i * 3.6
        best = None
        for k in range(30):
            dx = (k % 5 - 2) * 0.3 * (1 if i % 2 else -1); dy = (k // 5) * 0.6
            if F.free(x0 + dx, y0 + dy, 0.5):
                best = (x0 + dx, y0 + dy); break
        e.loc = (best or (x0, y0)) + (0.0,)
        e.face = facing((0.5 if i % 2 == 0 else -0.5, -1.0))
    for e in F.extras[6:]:
        if abs(e.home[0] + 6.55) < 2.5 and -30 < e.home[1] < 14: e.visible = False


def cam(F, g, t, u):
    e = ease_out(u, 2.4)
    y = -9.0 + 20.0 * e                                    # v3: starts 17 D further up the lane and higher (was -26, 2.25): cars, tail lights and people from frame one
    loc = Vector((-6.55 + 0.25 * math.sin(u * 3.0), y, 3.25 - 0.85 * e + 0.15 * math.sin(u * 2.0)))
    look = Vector((-7.6, 36.0, 1.9))
    return F.camera(loc, look, F.pick(22, 18), focus=look, k=2.0, kmax=16, shake=hand_cam(t, 0.15, 1.2))


def frame(F, g, t, u):
    cam(F, g, t, u)
    kong_cutter(F, t, g); crew_pry(F, t, loc=F.P(DM0(F), 1.5, 1.3)); driver_seated(F, t)
    return {"exposure": 1.7, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        rescue_lamp(F, 1.0, 8000.0)
        F.shadows(F.K + Z(1.5))
