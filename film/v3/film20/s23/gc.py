#!/usr/bin/env python3
"""gc.py -- ground_check on the s23 scene: python3 gc.py [step] -> GROUND.md"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import shot
import ground_check


def _sprite_path(node, frame):
    p = ground_check.bpy.path.abspath(node.image.filepath)
    d, base = os.path.split(p)
    return os.path.join(d, re.sub(r"\d+(?=\.png$)", "%04d" % int(frame), base))


ground_check._sprite_path = _sprite_path
step = int(sys.argv[1]) if len(sys.argv) > 1 else 6
gs = list(range(shot.GF, shot.G_LAST + 1, step)) + [shot.G_LAST]
Tk = shot.Take("preview")
Tk.pose(gs)
fl = ",".join(str(shot.bf(g)) for g in gs)
sys.exit(ground_check.run_cli(["--frame-list", fl, "--gap", "0.02", "--out", os.path.join(HERE, "GROUND.md")]))
