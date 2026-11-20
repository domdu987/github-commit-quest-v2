import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P
# T6b staging: lights up (TAKE_OVER, lights only) and Bertillon clear of the pulled-out drawer front (dx/dy/dz in metres)
P.TAKE_OVER['T6']['archive'].update(json.loads(os.environ.get('T6OVER', '{"shade_mul":1.4,"fill_w":600,"gain":1.15}')))
B = json.loads(os.environ.get("BERT", "{\"dx\":0.4}"))
g = int(sys.argv[1]); out = sys.argv[2]; res = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (720, 1280); sm = int(sys.argv[5]) if len(sys.argv) > 5 else 16
for k in (1600, 1690):
    P.REAL_STILLS[('T6', k)]['bertillon'] = ('bertillon_holding_card', B)
dt, acts = P.real_still('T6', g, out, res, sm); print('still g%d %.1fs' % (g, dt))
