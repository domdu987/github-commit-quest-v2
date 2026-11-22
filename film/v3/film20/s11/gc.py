#!/usr/bin/env python3
"""gc.py -- ground_check on the s11 scene: python3 gc.py [step]  -> GROUND.md"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import shot
import ground_check
import re as _re


def _sprite_path(node, frame):
    """the sprite sequences start at film frame G_FIRST (file name number = Blender frame): resolve by the name pattern"""
    p = ground_check.bpy.path.abspath(node.image.filepath)
    d, base = os.path.split(p)
    return os.path.join(d, _re.sub(r"\d+(?=\.png$)", "%04d" % int(frame), base))


ground_check._sprite_path = _sprite_path
step = int(sys.argv[1]) if len(sys.argv) > 1 else 6
gs = list(range(shot.G_FIRST, shot.G_LAST + 1, step)) + [shot.G_LAST]
Tk = shot.Take("preview")
Tk.pose(gs)
fl = ",".join(str(shot.bf(g)) for g in gs)
sys.exit(ground_check.run_cli(["--frame-list", fl, "--include", "fg_girder", "--gap", "0.02", "--out", os.path.join(HERE, "GROUND.md")]))
