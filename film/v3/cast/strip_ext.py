#!/usr/bin/env python3
"""strip_ext.py -- the pop check of v2 test_puppet.py --strip, run on every new cast member: 30 frames, yaw -1 -> +1 while
the right arm rises (and a prop swings for the members that hold one); largest frame-to-frame pixel change must stay under
2.2 x the median change, anchors may not jump more than 0.12 D.  Writes v3/tmp/cast/strip_<name>.png."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast_ext
import puppet
import test_puppet as T

PROPS = {"clerk": "mug", "beach_kid": "bucket", "senior_a": "forecast", "beach_man": "newspaper"}


def run(name, n=30, D=150):
    a = {"yaw": -1.0, "arm_r": "down", "arm_l": "down", "expr": "neutral"}
    b = {"yaw": 1.0, "arm_r": "reach_up", "arm_l": "shade", "expr": "neutral"}
    if name in PROPS:
        a["prop_r"] = b["prop_r"] = {"type": PROPS[name], "angle": 80.0}
        b["prop_r"] = {"type": PROPS[name], "angle": -60.0}
    poses = [puppet.lerp_pose(name, a, b, i / float(n - 1)) for i in range(n)]
    cw, ch, cols = int(2.6 * D), int(4.2 * D), 10
    rows = (n + cols - 1) // cols
    body = []
    for i, p in enumerate(poses):
        f = puppet.figure(name, p, "s%d" % i)
        x, y = (i % cols) * cw, (i // cols) * ch
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#a8663f"/>' % (x, y, cw, ch))
        body.append('<g transform="translate(%.1f %.1f) scale(%d)">%s</g>' % (x + cw * 0.45, y + ch - 0.2 * D - f["feet_y"] * D, D, f["svg"]))
    W, H = cols * cw, rows * ch
    sp = os.path.join(cast_ext.TMP, "strip_%s.svg" % name)
    out = os.path.join(cast_ext.TMP, "strip_%s.png" % name)
    open(sp, "w").write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(body)))
    jp = os.path.join(cast_ext.TMP, "_strip_jobs.json")
    json.dump([dict(svg=sp, out=out, w=W, h=H, bg="#a8663f")], open(jp, "w"))
    subprocess.run(["node", os.path.join(cast_ext.V2P, "raster_multi.js"), jp], check=True, stdout=subprocess.DEVNULL)
    im = np.asarray(Image.open(out).convert("RGB")).astype(np.float32)
    cells = [im[(i // cols) * ch:(i // cols + 1) * ch, (i % cols) * cw:(i % cols + 1) * cw] for i in range(n)]
    diffs = [float(np.abs(cells[i] - cells[i - 1]).mean()) for i in range(1, n)]
    med = sorted(diffs)[len(diffs) // 2]
    w = max(range(len(diffs)), key=lambda i: diffs[i])
    figs = [puppet.figure(name, p, "s") for p in poses]
    for f in figs:
        f["anchors"] = dict((k, v) for k, v in f["anchors"].items() if not k.startswith("prop_tip"))
    d, k, i = T.max_step(figs)
    ok = diffs[w] <= 2.2 * med and d <= 0.12
    print("%-12s pixel change median %.2f max %.2f (frame %d->%d) ratio %.2f | anchor step %.3f D (%s)  %s"
          % (name, med, diffs[w], w, w + 1, diffs[w] / med, d, k, "ok" if ok else "POP"))
    return ok


if __name__ == "__main__":
    res = [run(n) for n in cast_ext.NEW]
    sys.exit(0 if all(res) else 1)
