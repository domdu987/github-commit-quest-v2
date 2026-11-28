"""S044 (class C1)  (three ticks) '10 วินาที'  -- INSERT, drawn: Kong's watch, extreme close on the red hand's tip climbing the
left side of the dial; the blood spot on the 12 mark is in the top of the frame.  4 % zoom in.  The hand jumps once a
second on the EPISODE clock (seconds since the bite, real time): this shot holds 49, 50, 51."""
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
    e = ctx.u
    z = 5.2 * (1 + 0.04 * e)
    k_tick = (sec - math.floor(sec)) * 24.0                  # frames since the last tick: the wrist jolts 2 px for two frames
    j = {0: (0.004, -0.003), 1: (-0.002, 0.002)}.get(int(k_tick), (0.0, 0.0))
    tr = (0.0025 * math.sin(ctx.t * 9.0), 0.0025 * math.sin(ctx.t * 7.3 + 1.0))
    d0 = _drift((-0.25, -0.36))
    return _WL.watch_frame(ctx, sec, smear=True, zoom=z, drift=(d0[0] + j[0] + tr[0], d0[1] + j[1] + tr[1] + 0.04), tilt=TILT, seed=11, drops=5)
