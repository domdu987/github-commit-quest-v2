"""S047 (class C1)  (tick, tick, tick)  -- INSERT, drawn: the watch, tighter still.  The red hand's tip ticks 55, 56, 57 toward
the blood spot on the 12 mark (episode clock, real time).  Locked; the wrist jolts on each tick."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sc02b_lib as L
CLASS = "C1"
_WL, _WP = L.watch_lib()
DEPS = [L.LIB, _WP]
TILT = -12.0


def _drift(p):
    """drift (D) that brings the dial point p (y down) to the middle of the frame under the card tilt."""
    c, s = math.cos(math.radians(TILT)), math.sin(math.radians(TILT))
    return (-(p[0] * c - p[1] * s), -(p[0] * s + p[1] * c))


def draw(ctx):
    sec = L.since_bite(ctx.g)
    k_tick = (sec - math.floor(sec)) * 24.0
    j = {0: (0.004, -0.003), 1: (-0.002, 0.002)}.get(int(k_tick), (0.0, 0.0))
    d0 = _drift((-0.13, -0.48))
    return _WL.watch_frame(ctx, sec, smear=True, zoom=7.0, drift=(d0[0] + j[0], d0[1] + j[1] + 0.04), tilt=TILT, seed=11, drops=5)
