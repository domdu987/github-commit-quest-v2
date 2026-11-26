"""base.py -- newest available picture for a film frame (draft frames without any v12 gauge on them)."""
import os
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(PROJ, "v10", "film", "out")
CUT = [0, 81, 138, 181, 223, 266, 303, 346, 389, 421, 457, 532, 599, 656, 695, 728, 802, 831, 903, 967, 1043, 1087, 1114, 1147, 1280]
def shot_of(g):
    for i in range(24):
        if CUT[i] <= g < CUT[i + 1]:
            return "S%02d" % (i + 1)
    return "S24"
def frame_path(g):
    s = shot_of(g)
    for d in ("draft_360x640", "draft_v1_360x640"):
        p = os.path.join(OUT, d, s, "f_%04d.png" % (g + 1))
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            return p, d
    return None, None
