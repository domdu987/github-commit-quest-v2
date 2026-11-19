import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate, office_mech as M
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
A, PA, MA, sc = gate.setup(0.50, 0.5, 6); M.set_speed_sign(0)
for n in sys.argv[2].split(','):
    M.S.make_camera(M.cam(n)); M.S.render(os.path.join(out, n + '.png'))
