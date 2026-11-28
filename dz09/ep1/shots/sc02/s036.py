"""S036 (class C1)  '30 วินาที'  -- INSERT, drawn.  The watch again, frontal and closer, locked with a 2 px hand tremor.  The red
hand passes the 6, straight down: half way round to the blood.  A smear of the junior's blood on the glass now (Kong's
gloves have been on the wound); one rain drop cuts a clean line through it."""
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
    sec = L.film_t(ctx.t) - L.BITE_FILM
    k = ctx.k // 2                                           # tremor on twos, about 2 px of a 720 frame
    dr = ((C.hash01(k, 1) - 0.5) * 0.03, (C.hash01(k, 2) - 0.5) * 0.03)
    streak = smooth(ramp(ctx.u, 0.30, 0.85))
    return L.watch_frame(ctx, sec, smear=True, zoom=2.3, drift=dr, tilt=-4.0, seed=7, drops=4, streak=streak)
