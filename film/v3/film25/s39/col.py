"""col.py -- shared by s39 / s40: a column of Mark I tanks crawling north (heading +y) in the front location.
Tank i starts at (x_i, y_i) and crawls at v D/s along its heading; every frame: tank25.pose_on_ground (rests it on the heightfield) + set_drive (links scroll, tail wheels roll)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
C, F = T.C, T.F


def mover(spec, g0, v=1.3):
    """spec = [(x, y, yaw_deg)]; returns a hooks(g, Tk) for the take (tanks in F.S['tanks_h'] order)"""
    def hooks(g, Tk):
        t = (g - g0) / 30.0
        for H, (x, y, yaw) in zip(F.S["tanks_h"], spec):
            d = v * t
            h = (math.cos(math.radians(yaw)), math.sin(math.radians(yaw)))
            Tk.TK.pose_on_ground(H, x + h[0] * d, y + h[1] * d, yaw)
            Tk.TK.set_drive(H, d)
    return hooks
