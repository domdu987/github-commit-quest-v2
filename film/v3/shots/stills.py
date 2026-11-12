#!/usr/bin/env python3
"""stills.py -- blocking helper: render chosen output frames small.  python3 stills.py A 0,7,19 [scale] [samples] [outdir]"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
take = sys.argv[1]
frames = []
for part in sys.argv[2].split(","):
    if ":" in part:
        a = [int(v) for v in part.split(":")]
        frames += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    else:
        frames.append(int(part))
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
samples = int(sys.argv[4]) if len(sys.argv) > 4 else 6
out = sys.argv[5] if len(sys.argv) > 5 else os.path.join(film.TMP, "stills")
threads = int(os.environ.get("THREADS", "2"))
F = film.Film(take)
F.pose(frames)
for g in frames:
    i = F.info.get(g, {})
    for who, inf in i.items():
        if isinstance(inf, dict):
            for side, d in inf.items():
                if "screen" in d:
                    print("g %3d %s %s err %.4f  reg %.2f px  %s" % (g, who, side, d["error"],
                          ((d["screen"][0] - d["want"][0]) ** 2 + (d["screen"][1] - d["want"][1]) ** 2) ** 0.5,
                          ("clear %.3f" % d["clear"]) if "clear" in d else ""))
st = F.render(frames, out, scale=scale, threads=threads, samples=samples)
print("mean wall %.2f s  cpu %.2f s" % (sum(s["wall"] for s in st) / len(st), sum(s["cpu"] for s in st) / len(st)))
