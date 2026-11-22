"""usage: r2draft.py out_png_dir quality(preview|final) spec... : render specs to out dir (not touching set_work/final)"""
import sys, os
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J
out, q = sys.argv[1:3]
for sp in sys.argv[3:]: J.render_spec(sp, q, outdir=out, tag=sp.replace('@', '_').replace(':', '_'))
