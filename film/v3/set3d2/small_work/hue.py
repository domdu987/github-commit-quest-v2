"""hue.py <label=glob> ... : rows of v3/tools/hue_report.py (imported, same stats and band) without its interior reference rows,
which point at files that do not exist (ref/a/t27.0.jpg; the reference frames are named tNNNN.jpg)."""
import sys, glob
sys.path.insert(0, '/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/tools')
import hue_report as H
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
for a in sys.argv[1:]:
    lab, g = a.split('=', 1) if '=' in a else (a, a)
    fl = sorted(sum([glob.glob(x) for x in g.split(',')], []))
    if fl: H.row(lab, fl)
