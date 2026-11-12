#!/usr/bin/env python3
"""edge_setting_test.py -- which render setting matches the reference edge softness: dsf 1, or 2x supersampling scaled down.
Renders one frame SVG both ways, scales with ffmpeg, measures with tools/edge_soft.py -> out/edge_softness.json.
usage: python3 tools/edge_setting_test.py [svg]      (measuring only)"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.dirname(HERE); PROJ = os.path.dirname(V2)
sys.path.insert(0, HERE)
import edge_soft
svg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(V2, "out", "svg", "s03_0120.svg")
td = os.path.join(V2, "tmp", "edge"); os.makedirs(td, exist_ok=True)
res = []
for dsf in (1, 2):
    out = os.path.join(td, "d%d.png" % dsf)
    json.dump(dict(width=720, height=1280, frames=[dict(svg=svg, out=out, shot="x")]), open(os.path.join(td, "m.json"), "w"))
    subprocess.run(["node", os.path.join(V2, "render.js"), os.path.join(td, "m.json"), "--dsf", str(dsf)], check=True, stdout=subprocess.DEVNULL)
r = edge_soft.edge_width(os.path.join(td, "d1.png")); res.append(("deviceScaleFactor 1", (r["w50"], r["lap"])))
for flt in ("area", "bicubic", "bilinear"):
    o = os.path.join(td, "d2_%s.png" % flt)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(td, "d2.png"), "-vf", "scale=720:1280:flags=" + flt, o], check=True)
    r = edge_soft.edge_width(o); res.append(("deviceScaleFactor 2, scaled down %s" % flt, (r["w50"], r["lap"])))
vids = [("reference A, 46.5 s", "/root/.claude/uploads/e8b79665-ba86-5bba-9861-f4e29c068ae7/0e17f4fd-Why_Perfect_Railroads_Dont_Work.mp4", 46.5),
        ("reference A, 16.0 s", "/root/.claude/uploads/e8b79665-ba86-5bba-9861-f4e29c068ae7/0e17f4fd-Why_Perfect_Railroads_Dont_Work.mp4", 16.0),
        ("reference B, 24.5 s", "/root/.claude/uploads/e8b79665-ba86-5bba-9861-f4e29c068ae7/22ba206d-The_Ancient_Jar_That_Warned_an_Empire.mp4", 24.5),
        ("reference B, 17.0 s", "/root/.claude/uploads/e8b79665-ba86-5bba-9861-f4e29c068ae7/22ba206d-The_Ancient_Jar_That_Warned_an_Empire.mp4", 17.0)]
for name, v, t in vids:
    o = os.path.join(td, "ref_%s.png" % name.replace(" ", "_").replace(",", "").replace(".", "_"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", v, "-vframes", "1", o], check=True)
    r = edge_soft.edge_width(o); res.append((name, (r["w50"], r["lap"])))
json.dump(res, open(os.path.join(V2, "out", "edge_softness.json"), "w"), indent=1)
for k, v in res: print("%-44s rise %.2f px   laplacian var %.0f" % (k, v[0], v[1]))
