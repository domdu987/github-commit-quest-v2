import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P
g = int(sys.argv[1]); out = sys.argv[2]
dt, acts = P.real_still('T6', g, out); print('still g%d %.1fs' % (g, dt))
