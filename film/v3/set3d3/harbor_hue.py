#!/usr/bin/env python3
"""harbor_hue.py files... : hue_report rows (v3/tools/hue_report.py stats and band) per file, per preset group, and the reference
rows for clip A frames 40/62 and clip B (whole clip, frames 10/30, exterior frames)."""
import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import hue_report as H
if __name__ == '__main__':
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
    H.row('reference A, whole clip', sorted(glob.glob(H.P + '/ref/a/*.jpg')))
    H.row('reference B, whole clip', sorted(glob.glob(H.P + '/ref/b/*.jpg')))
    H.row('ref a t0040 t0062 + ref b t0010 t0030', [H.P + '/ref/a/t0040.jpg', H.P + '/ref/a/t0062.jpg', H.P + '/ref/b/t0010.jpg', H.P + '/ref/b/t0030.jpg'])
    H.row('ref b t0010 t0030 (exteriors)', [H.P + '/ref/b/t0010.jpg', H.P + '/ref/b/t0030.jpg'])
    groups = {}
    for a in sys.argv[1:]:
        for f in H.files_of(a): groups.setdefault(os.path.basename(f).split('_')[0], []).append(f); H.row(os.path.basename(f), [f])
    for g, fl in groups.items(): H.row('ALL ' + g, fl)
