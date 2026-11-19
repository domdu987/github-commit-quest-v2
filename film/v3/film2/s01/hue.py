#!/usr/bin/env python3
"""hue.py label=glob ... : rows of v3/tools/hue_report.py (its __main__ crashes on missing reference names; this calls row())."""
import sys, glob, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import hue_report as H
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
for a in sys.argv[1:]:
    lab, pat = a.split("=", 1) if "=" in a else (a, a)
    fl = sorted(glob.glob(pat))
    if fl: H.row(lab, fl)
