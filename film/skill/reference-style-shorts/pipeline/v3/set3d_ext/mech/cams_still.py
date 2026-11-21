import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate, office_mech as M
out = sys.argv[1]; names = sys.argv[2].split(','); os.makedirs(out, exist_ok=True)
A, PA, MA, sc = gate.setup(0.50, 0.5, 6)
M.set_speed_sign(1.0); M.set_picto('E', 1); M.set_picto('W', 1); M.set_wind(0.3, 1.0); M.set_wake(0.10, 0.1, 1.0)
M.set_spinner_fx(ring=0.8, drop=1.0)
for i in (1, 2, 3): M.set_ghost_spinner(i, 0.4, angle=20)
M.set_shell(1.0, 2)
for n in names:
    M.S.make_camera(M.cam(n)); M.S.render(os.path.join(out, n + '.png'))
