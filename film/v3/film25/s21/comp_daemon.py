#!/usr/bin/env python3
"""comp_daemon.py -- composes every rendered frame (work/meta json present, frames/g png missing) of every take folder, one at a time, low priority."""
import os, sys, glob, time, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.nice(12)
import post_d as PD
B = os.path.dirname(HERE)
while True:
    did = False
    for td in sorted(glob.glob(os.path.join(B, "s*"))):
        for mp in sorted(glob.glob(os.path.join(td, "work", "meta", "g_*.json"))):
            g = int(re.findall(r"g_(\d+)", mp)[0]); out = os.path.join(td, "frames", "g_%04d.png" % g)
            if not os.path.exists(out) and os.path.exists(os.path.join(td, "work", "beauty", "f_%04d.png" % g)):
                try:
                    kw = {}
                    if os.path.basename(td) in ("s27", "s26"): kw = dict(vib=2.0, sat=1.5, wb=(0.0, 2.5))
                    if os.path.basename(td) == "s64": kw = dict(vib=2.0, wb=(-2.0, 3.5), sat=1.12, gamma=0.84)
                    if os.path.basename(td) == "s66": kw = dict(vib=1.8, wb=(-3.0, 3.5), gamma=0.95, sat=1.1)
                    if os.path.basename(td) == "s67": kw = dict(vib=2.4, wb=(-1.0, 5.0), gamma=0.9)
                    if os.path.basename(td) == "s23": kw = dict(gamma=0.9, wb=(-1.0, 5.0), vib=2.0)
                    if os.path.basename(td) in ("s18", "s25"): kw = dict(gamma=0.95, wb=(-3.0, 4.0), vib=(1.4 if os.path.basename(td) == "s25" else 1.8))
                    PD.compose(g, os.path.join(td, "work"), os.path.join(td, "frames"), **kw); did = True
                except Exception as e:
                    print("compose fail", td, g, e, flush=True)
    if not did:
        time.sleep(10)
