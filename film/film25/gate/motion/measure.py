#!/usr/bin/env python3
"""measure.py -- measured camera move per shot from the per-frame reports (frames/g_%04d.json):
subject scale change (head width on screen, first -> last frame of the shot, and the punch-in part), the subject's screen pan
(% of frame width per second, head centre x), and the render time.  python3 measure.py [frames_dir]"""
import os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
FR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "frames")
ROWS = [(19, 522, 552, "PUNCH 20 % g 522-529, then drift", 529), (20, 552, 602, "PUSH 10 %", None),
        (21, 602, 626, "PUNCH 20 % g 602-609, then drift", 609), (22, 626, 676, "over-shoulder PUSH 8 %", None)]
J = {int(os.path.basename(p)[2:6]): json.load(open(p)) for p in glob.glob(os.path.join(FR, "g_*.json"))}
print("| row | g | move (spec) | head w px first -> last | scale | punch part | head x pan, % W per s | heads y (0-1 H) |")
print("|---|---|---|---|---|---|---|---|")
for r, a, b, spec, pk in ROWS:
    gs = [g for g in range(a, b) if g in J]
    if len(gs) < 2:
        continue
    h = lambda g: J[g]["heads"]["gen"]
    w0, w1 = h(gs[0])["w"], h(gs[-1])["w"]
    punch = ("%+.1f %% (g %d-%d)" % ((h(pk)["w"] / w0 - 1) * 100, gs[0], pk)) if pk in J else "-"
    pan = (h(gs[-1])["x"] - h(gs[0])["x"]) / 720.0 * 100 / ((gs[-1] - gs[0]) / 30.0)
    ys = [h(g)["y"] / 1280 for g in gs]
    print("| %d | %d-%d | %s | %.0f -> %.0f | %+.1f %% | %s | %+.1f | %.2f-%.2f |" % (r, a, b - 1, spec, w0, w1, (w1 / w0 - 1) * 100, punch, pan, min(ys), max(ys)))
ws = [J[g]["wall"] for g in J if "wall" in J[g]]
cs = [J[g]["cpu"] for g in J if "cpu" in J[g]]
if ws:
    print("\nframes %d, wall %.1f s/frame mean (min %.1f, max %.1f), cpu %.1f s/frame mean, samples %s, scale %s"
          % (len(ws), sum(ws) / len(ws), min(ws), max(ws), sum(cs) / len(cs), J[min(J)].get("samples"), J[min(J)].get("scale")))
