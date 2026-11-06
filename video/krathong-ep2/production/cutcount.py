"""Hard cuts in a rendered file vs the plan: ffmpeg select scene score (0-1) > threshold, detections within 0.1 s merged.
usage: python3 cutcount.py <scene.txt: 't score' per frame> <shotlist.json>"""
import json, sys
v = [tuple(map(float, l.split())) for l in open(sys.argv[1]) if len(l.split()) == 2]
sl = json.load(open(sys.argv[2]))["cuts"]
for th in (0.10, 0.15):
    m = []
    for x in (x for x in v if x[1] > th):
        if not m or x[0] - m[-1][0] > 0.1: m.append(x)
    hit = [c["n"] for c in sl[1:] if any(abs(x[0] - c["t"]) < 0.1 for x in m)]
    miss = [(c["n"], c["key"], c["t"]) for c in sl[1:] if c["n"] not in hit]
    extra = [round(x[0], 2) for x in m if all(abs(x[0] - c["t"]) > 0.1 for c in sl)]
    print(f"scene>{th:.2f}: {len(m)} hard cuts · plan {len(sl)} shots ({len(sl) - 1} cut points) · found {len(hit)} · missing {miss} · extra {extra}")
