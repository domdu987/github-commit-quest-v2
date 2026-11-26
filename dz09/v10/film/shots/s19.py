"""S19  'น้องในทีม ค่อยๆ ยื่นหน้า เข้าไปใกล้'  -- E4 low lateral track from Kong's side: the crew member walks to the open
door (walk cycle, planted feet) and slowly leans in toward the still driver."""
from shots.base import *
import gait8
ID = "S19"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
T0 = 37.618
PERIOD = 22.0 / 24.0                                        # the walk loops on whole frames
G = None


def path(F, t):
    """root position and walk clock: he starts 2.3 BU out and stops at the door after two and a half steps."""
    global G
    if G is None: G = gait8.Gait("crew_wet", "walk", T=PERIOD)
    sc = F.crew.a.sc
    stop = PERIOD * 1.5 + 0.05 * PERIOD                      # ends in double support
    tw = min(max(t - T0, 0.0), stop)
    start = F.P(DM0(F), -0.55, 3.25)
    return start - F.right * (G.v * sc * tw), tw, (t - T0) >= stop, stop


def cam(F, g, t, u):
    b = DM0(F)
    r = path(F, t)[0]; rr = (r - b).dot(F.right)
    loc = F.P(b, -4.9 + 0.3 * u, rr + 0.9, 1.25)
    look = F.P(b, -0.5, rr - 0.25, 1.85)
    return F.camera(loc, look, F.pick(32, 26), focus=F.P(b, -0.55, rr, 2.0), k=6.0, kmax=20, shake=hand_cam(t, 0.12, 1.2))


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    loc, tw, stopped, stop = path(F, t)
    a = F.crew.a
    rel = a._cam_rel(F.cam) if a.root.location.length > 0 else 90.0
    a.root.location = loc; a.facing = facing(-F.right)
    rel = a._cam_rel(F.cam)
    a.walk_lock = 90.0 if rel >= 0 else -90.0
    base = dict(expr="neutral", blink=C.blink("crew", t))
    pose = G.pose(tw, s=-1, view="side", base=base)
    if stopped:
        tt = C.on_twos(t)
        k = smooth(ramp(tt, T0 + stop + 0.1, T0 + stop + 1.25))        # the slow lean-in
        pose["lean"] = 4 + 26 * k
        pose["head"] = (0, 6 * k, 0.10 * k, 0.03 * k)
        pose["arm_n"] = dict(hand=lerp((0.05, 1.0), (0.62, 0.55), k), elbow=None, hand_shape="open")
        pose["arm_f"] = dict(hand=lerp((0.05, 1.0), (0.45, 0.75), k), elbow=None, hand_shape="open")
    pose.pop('view', None); pose.pop('s', None)
    F.crew.set(loc=loc, face=facing(-F.right), view="side", s=-1, **pose)
    driver_seated(F, t)
    F.kong.hide()
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        cam(F, g, 0, 0.5)
        F.lamp(F.P(DM0(F), 6.0, 6.5), F.P(DM0(F), -0.5, 1.5, 1.2), 9000.0, heads=[F.crew.head()])
        F.shadows(F.P(DM0(F), -0.5, 1.5, 1.5))
        F.crew.a.set_glow(WARM, 0.28)
        cam(F, g, t, u)
