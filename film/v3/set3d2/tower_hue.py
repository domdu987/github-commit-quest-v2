#!/usr/bin/env python3
"""tower_hue.py files... : the rows of v3/tools/hue_report.py (its stats and band, imported) for each file and for each group
(the tool's own __main__ fails on missing reference file names, so this calls its row() directly)."""
import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import hue_report as H
if __name__ == '__main__':
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
    H.row('reference A, whole clip', sorted(glob.glob(H.P + '/ref/a/*.jpg')))
    H.row('ref a t0040 t0062 t0072 t0080 t0096', [H.P + '/ref/a/t%04d.jpg' % t for t in (40, 62, 72, 80, 96)])
    groups = {}
    for a in sys.argv[1:]:
        for f in H.files_of(a): groups.setdefault(os.path.basename(f).split('_')[0] if not os.path.basename(f).startswith('NIGHT') else '_'.join(os.path.basename(f).split('_')[:2]), []).append(f); H.row(os.path.basename(f), [f])
    for g, fl in groups.items(): H.row('ALL ' + g, fl)
