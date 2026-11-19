"""proof_close.py : the wall map from very close (0.75 D and 0.45 D, as shots 19-22) in the three presets, final quality,
plus the cost of a lightning frame (office_storm, flash 1.0, eye_two_shot, placeholders, 4 threads)."""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, office_light as OL
S = OL.S; od = os.path.join(HERE, 'proof', 'close'); os.makedirs(od, exist_ok=True)
A = S.build('INTERIOR_DAY'); sc = bpy.context.scene; S.setup_render(sc, 'fast'); sc.render.threads = 2; S.set_track(1, 0)
views = dict(rake075=dict(loc=(-0.55, -0.75, 2.0), look_at=(0.2, -0.05, 2.15), lens=22), plan045=dict(loc=(0.15, -0.5, 2.15), look_at=(0.15, -0.05, 2.15), lens=22))
for pr in OL.PRESETS:
    OL.apply(pr)
    for nm, v in views.items():
        S.make_camera(v); S.render(os.path.join(od, '%s_%s.png' % (pr, nm))); print(pr, nm, flush=True)
OL.apply('office_storm'); sc.render.threads = 4
cs = A['cams']['eye_two_shot']; S.make_camera(cs); S.stage_placeholders(A, 'two_shot', cs['loc']); OL.tint_cards()
res = {}
for a in (0.0, 1.0, 1.0):
    OL.flash(a); c0 = time.process_time(); w0 = time.time(); S.render(os.path.join(od, 'flashcost_%.1f.png' % a))
    res['flash_%.1f' % a] = dict(wall=round(time.time() - w0, 2), cpu=round(time.process_time() - c0, 2), load1=round(os.getloadavg()[0], 2))
print(res); json.dump(res, open(os.path.join(HERE, 'proof', 'timing_flash.json'), 'w'), indent=1)
