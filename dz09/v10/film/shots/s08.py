"""S08  'ในมือคือ เครื่องตัดไร้สาย'  -- T1 prop macro on the modelled cutter at the door seam: the jaws bite at 15.05
(sound cue), sparks, recoil; Kong out of focus behind."""
from shots.base import *
ID = "S08"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale


def cam(F, g, t, u):
    jaw = Vector(F.A["cutter_jaw"])
    k = max(0.0, 1 - (t - BITE_T) / 0.5) if t >= BITE_T else 0.0
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.15, 1.5), hand_cam(t, 1.2 * k, 9.0)))
    p = smooth(u)
    loc = jaw + F.fwd * (1.95 - 0.60 * p) + F.right * (1.70 - 0.42 * p) + Z(0.62 - 0.14 * p)     # v3: a real push onto the jaws (was 0.25 / 0.15)
    look = jaw + F.right * 0.50 + Z(0.05)
    return F.camera(loc, look, F.pick(50, 40), focus=jaw + F.right * 0.3, k=F.pick(24, 20), kmax=30, clip=0.03, shake=sh)


def frame(F, g, t, u):
    cam(F, g, t, u)
    # v3: the jaws work: they feel for the seam (open -> half), bite shut on the sound cue (15.05), ease, bite again
    B2 = BITE_T + 0.62
    g0, _ = C.shot_range(ID); ts = g0 / 24.0
    jaw = 1.0 - 0.45 * smooth(ramp(t, ts + 0.1, BITE_T - 0.06))
    if t >= BITE_T: jaw = 0.55 * (1 - ease_out(ramp(t, BITE_T, BITE_T + 0.14), 2.5)) + 0.30 * smooth(ramp(t, BITE_T + 0.25, BITE_T + 0.52))
    if t >= B2: jaw = 0.30 * (1 - ease_out(ramp(t, B2, B2 + 0.12), 2.5))
    F.cutter3d(True, jaw=jaw, bars=3)
    amt = 0.0 if t < BITE_T else max(1.0 - (t - BITE_T) / 0.6, (0.8 - (t - B2) / 0.7) if t >= B2 else 0.0, 0.0)
    F.sparks_at(Vector(F.A["cutter_jaw"]) + F.right * 0.05, g, amt, away=F.right * 0.8 + F.fwd * 0.6)
    F.kong.set(loc=F.K - F.fwd * 0.2 + F.right * 0.5, face=door_dir(F), view="q", s=1, expr="serious", blink=C.blink("kong", t),
               arm_n=dict(hand=(0.5, 0.6), elbow=None, hidden_hand=True), arm_f=dict(hand=(0.4, 0.7), elbow=None, hidden_hand=True), legs="wide", lean=14, head=(0, 12, 0, 0))
    driver_seated(F, t)
    return {"exposure": 1.05, "tilt": 0.0}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), -6.0, 5.0), F.K + Z(1.0), 4000.0, heads=[F.kong.head()])
        F.shadows(F.K + Z(1.5))
