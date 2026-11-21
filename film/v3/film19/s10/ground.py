#!/usr/bin/env python3
"""ground.py -- 'nothing floats' check of this take with film/v3/tools/ground_check.py (QA_TEAM_film13 / client rule).
Builds the take's scene (shot.Take), poses the sampled frames, then runs ground_check.run_cli.   python3 ground.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shot                                              # noqa: E402
TOOLS = os.path.join(shot.C.V3, "tools")
sys.path.insert(0, TOOLS)
import ground_check                                      # noqa: E402

gs = sorted(set(list(range(shot.G0, shot.G1, 10)) + [shot.G1 - 1, shot.G_FIRST, shot.G_LAST]))
Tk = shot.Take("preview", )
Tk.pose(gs)
fl = ",".join(str(shot.bf(g)) for g in gs)            # Blender frames
rc = ground_check.run_cli(["--frame-list", fl, "--gap", "0.02", "--out", os.path.join(HERE, "GROUND.md")])
print("ground_check exit:", rc)
