"""smoke test: sets.register() + stage_ep.build("CAB") on the hook's Stage, begin() of a dummy shot, one staged frame (no render)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sets
SE = sets.register()
import epcommon as E
F = SE.build("CAB", "draft", 360, 640, threads=1)
print("SMOKE location", F.loc_key, sorted(F.sets), len(F.sets["cab"]["anchors"]), "cab anchors;", len(F.sets["x2"]["anchors"]), "x2 anchors")
import cab, gear, x2
cab.switch("siren", True); cab.wipers(0.3); cab.mirror(1); gear.shutter(1.0); gear.take("crowbar"); x2.beacons(False); cab.crack(2); cab.fog(0.5)
print("SMOKE setters ok")
