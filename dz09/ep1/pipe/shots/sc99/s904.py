"""S904 (dummy, class A)  narrator: 'ภาพผ่านท่อ ครบแล้ว'  -- the hook's S06 low lateral on Kong with the cutter.  The line is
the NARRATOR's: talk("kong", g) returns nothing and his mouth stays shut although he is in close-up."""
from epbase import *
CLASS = "A"
LOC = "X1"


def setup(F):
    F.hide_roots(["bike_a"])


def _cam(F, u):
    K = F.K
    to_cam = Vector((4.4, -8.4, 0)).normalized(); side = Vector((-to_cam.y, to_cam.x, 0))
    d = F.pick(3.5, 5.6) - 0.25 * ease_out(u)
    loc = K + to_cam * d + side * (0.35 - 0.35 * u) + Vector((0, 0, 0.95))
    look = K + Vector((0, 0, 1.72)) + side * F.pick(-0.55, -1.2)
    return F.camera(loc, look, F.pick(28, 24), focus=K + Vector((0, 0, 2.4)), k=7.0, kmax=22), to_cam, side


def frame(F, g, t, u):
    c, to_cam, side = _cam(F, u)
    tt = C.on_twos(t)
    lookup = smooth(ramp(tt, W("ครบแล้ว") - 0.05, W("ครบแล้ว") + 0.25))
    kong_cutter(F, t, g, face=facing(to_cam) - 25, view="q", head=(0, 8 - 14 * lookup, 0, 0), lean=6, gaze=(0.3 * lookup, -0.1 * lookup), jaw=1.0,
                **talk("kong", g))
    cl = F.K - side * 1.30 - to_cam * 0.15
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
