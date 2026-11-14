#!/usr/bin/env python3
"""Hue rows per frame and per location group through v3/tools/hue_report.py (stats/row), plus reference rows.
usage: python3 louvre_hue.py <png | folder ...>"""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
fs = [f for a in sys.argv[1:] for f in H.files_of(a)]
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
H.row("reference A, whole clip", sorted(glob.glob(H.P + "/ref/a/*.jpg")))
H.row("ref A interiors t0001 t0006 t0046 t0051", [H.P + "/ref/a/t%04d.jpg" % t for t in (1, 6, 46, 51)])
H.row("ref A day exteriors t0056 t0061 t0081", [H.P + "/ref/a/t%04d.jpg" % t for t in (56, 61, 81)])
groups = {}
for f in fs:
    H.row(os.path.basename(f)[:-4], [f]); k = 'all'; groups.setdefault(k, []).append(f)
for g, l in groups.items(): H.row('ALL ' + g, l)
