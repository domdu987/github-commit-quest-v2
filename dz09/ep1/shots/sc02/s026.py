"""S026 (class C1)  '50 วินาที'  -- INSERT, drawn (no Cycles).  Kong's left wrist: the white forearm, the black glove cuff, a
round rescue watch strapped over the cuff.  Nothing to read but ONE red second hand and a drop of the junior's blood on
the 12 mark, where the hand stood at the bite.  The hand shows the real count (10-12 s after the bite: at the 2) and
jumps once a second; rain drops sit and run on the glass; the frame drifts with the arm and jolts twice with the shove.
The watch is the cast package's `draw9.watch_svg`; `watch_frame` in s025.py is also used by S036, S044, S047."""
from ep2d import *
import os, sys, math, importlib.util
import epcommon as E
C = E.C
from common import smooth, ramp


def lib():
    """the range's small library lives in s025.py (see its docstring)."""
    if "ep1_sc02_s025_lib" not in sys.modules:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s025.py")
        sp = importlib.util.spec_from_file_location("ep1_sc02_s025_lib", p); m = importlib.util.module_from_spec(sp)
        sys.modules["ep1_sc02_s025_lib"] = m; sp.loader.exec_module(m)
    return sys.modules["ep1_sc02_s025_lib"]


L = lib()
DEPS = [L.__file__]
CLASS = "C1"


def draw(ctx):
    sec = L.film_t(ctx.t) - L.BITE_FILM                      # seconds since the bite, on the episode clock
    j = {5: (0.10, -0.06), 6: (-0.06, 0.04), 21: (0.07, 0.05), 22: (-0.04, -0.02)}.get(ctx.k, (0.0, 0.0))     # the shove
    dr = (-0.12 + 0.24 * ctx.u + j[0], 0.07 * math.sin(ctx.u * math.pi) + j[1])
    return L.watch_frame(ctx, sec, smear=False, zoom=1.75, drift=dr, tilt=-14.0 + 3.0 * ctx.u, seed=3, drops=6)
