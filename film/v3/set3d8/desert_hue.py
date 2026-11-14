#!/usr/bin/env python3
"""Hue rows per frame and per light group through v3/tools/hue_report.py (stats/row), plus reference rows.
usage: python3 desert_hue.py <png | folder ...>"""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
fs = [f for a in sys.argv[1:] for f in H.files_of(a)]
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
H.row("reference A, whole clip", sorted(glob.glob(H.P + "/ref/a/*.jpg")))
H.row("ref A night t0069 t0073 t0077 t0081", [H.P + "/ref/a/t%04d.jpg" % t for t in (69, 73, 77, 81)])
H.row("ref A day exteriors t0056 t0061 t0081", [H.P + "/ref/a/t%04d.jpg" % t for t in (56, 61, 81)])
H.row("ref B desert day t0029 t0033 t0037", [H.P + "/ref/b/t%04d.jpg" % t for t in (29, 33, 37)])
groups = {}
for f in fs:
    H.row(os.path.basename(f)[:-4], [f]); n = os.path.basename(f)
    k = next((L for L in ('NIGHT', 'DAWN', 'NOON', 'SUMMER') if '_' + L in n), 'other'); groups.setdefault(k, []).append(f)
for g, l in groups.items(): H.row('ALL ' + g, l)
H.row('ALL', fs)
