"""S06  'ก้อง เจ้าหน้าที่กู้ภัย'  -- E4 low lateral track on the hero: Kong braced with the cutter, wheel in the foreground."""
from shots.base import *
ID = "S06"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1


def setup(F):
    F.hide_roots(["bike_a"])


def cam(F, u):
    K = F.K
    to_cam = Vector((4.4, -8.4, 0)).normalized(); side = Vector((-to_cam.y, to_cam.x, 0))
    d = F.pick(3.5, 5.6) - 0.35 * ease_out(u)
    loc = K + to_cam * d + side * (0.55 - 0.55 * u) + Vector((0, 0, 0.90 + 0.10 * u))
    look = K + Vector((0, 0, 1.62 + 0.20 * u)) + side * F.pick(-0.55, -1.2)      # v3: tilts up a little as it closes in, so his face stays under the icon strip
    return F.camera(loc, look, F.pick(28, 24), focus=K + Vector((0, 0, 2.4)), k=7.0, kmax=22), to_cam, side


def frame(F, g, t, u):
    c, to_cam, side = cam(F, u)
    tt = C.on_twos(t)
    # he settles his grip, then looks up from the tool toward the wreck
    T_NAME = C.word("เจ้าหน้าที่กู้ภัย")                       # Ohm 11.535 (v1 11.43)
    lookup = smooth(ramp(tt, T_NAME + 0.05, T_NAME + 0.55))
    kong_cutter(F, t, g, face=facing(to_cam) - 25, view="q", head=(0, 8 - 14 * lookup, 0, 0), lean=6,
                gaze=(0.3 * lookup, -0.1 * lookup), jaw=1.0)
    # v3: the young crew member is back, standing by on the far side of the door, clear of Kong (screen-left, smaller)
    cl = F.K - side * 1.30 - to_cam * 0.15                   # by the rear wheel, on the camera side of the car (further back he was inside the body)
    crew_ready(F, t, loc=cl, face=facing(F.K - cl), view="q", s=1)
    driver_seated(F, t)
    return {"sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        K = F.K; to_cam = Vector((4.4, -8.4, 0)).normalized(); side = Vector((-to_cam.y, to_cam.x, 0))
        F.foreground("wheel", side="left", cover=F.pick(0.34, 0.22), depth=1.6)
        F.lamp(K - to_cam * 5.5 + side * F.pick(5.2, 6.5), K + Vector((0, 0, 1.0)), 9000.0, heads=[F.kong.head(), F.crew.head()])
        F.shadows(K + Vector((0, 0, 1.5)))
        F.kong.a.set_glow(WARM, 0.28)
