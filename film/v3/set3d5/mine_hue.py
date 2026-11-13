#!/usr/bin/env python3
"""Hue rows per frame and per group, through v3/tools/hue_report.py (its stats/row; its 'reference A interiors' row has a broken
file pattern, so it is not called). usage: python3 mine_hue.py <png ...>"""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
fs = [f for a in sys.argv[1:] for f in H.files_of(a)]
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
H.row("reference A, whole clip", sorted(glob.glob(H.P + "/ref/a/*.jpg")))
H.row("ref A t0077 + t0089 (night lamps)", [H.P + "/ref/a/t0077.jpg", H.P + "/ref/a/t0089.jpg"])
H.row("ref A t0001 (interior, torches)", [H.P + "/ref/a/t0001.jpg"])
groups = {}
for f in fs:
    H.row(os.path.basename(f)[:-4], [f]); groups.setdefault(os.path.basename(f).split('_')[0], []).append(f)
for g, l in groups.items(): H.row('ALL ' + g, l)
