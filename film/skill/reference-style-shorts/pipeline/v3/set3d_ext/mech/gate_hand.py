"""gate_hand.py : the build-step-2 gate again, for the HAND-DRAWN line (walls and lane follow the track points).
    python3 gate_hand.py <out_dir> <scale> <samples> name[,name..]
names: corridor_cam (auto lens), corridor_a0 (lens straight behind on the line), corridor_far, plan_debug (square-on 1.6 D), or any M.cam name."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gate, office_mech as M
out = sys.argv[1]; scale = float(sys.argv[2]); smp = int(sys.argv[3]); names = sys.argv[4].split(',')
os.makedirs(out, exist_ok=True)
A, PA, MA, sc = gate.setup(0.50, scale, smp); M.set_speed_sign(0)
log = {}
for n in names:
    if n == 'corridor_a0': cs = M.corridor(a=0.0)
    elif n == 'plan_debug': cs = M.plan(0.5, 1.75)
    else: cs = M.cam(n)
    M.S.make_camera(cs); t = time.time(); M.S.render(os.path.join(out, n + '.png')); log[n] = dict(cam=cs, s=round(time.time() - t, 1))
print(json.dumps(log))
json.dump(log, open(os.path.join(out, 'log.json'), 'w'), indent=1)
