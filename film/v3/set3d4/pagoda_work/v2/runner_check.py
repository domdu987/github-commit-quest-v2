"""runner_check.py : 360x640 stills of the runner fix: s01 shot 4 camera (g 140, 167) with cast4 actors, street_eye, pagoda_low (DAY)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 's01_v2.py')).read().split("if __name__ == '__main__':")[0])
OUTR = os.path.join(HERE, 'runner'); os.makedirs(OUTR, exist_ok=True)
Tk = S.Take(quality='final')
for g in (140, 167):
    Tk.pose(4, [g]); Tk.scene.frame_set(S.bf(4, g)); Tk.scene.camera = Tk.cam
    foc, fs = dof_for(Tk, 4); G.setup_dof(Tk.scene, foc, fs, cam=Tk.cam)
    st = Tk.render(4, [g], OUTR, scale=0.5, samples=12)[0]; os.replace(st['path'], os.path.join(OUTR, 's4_g%04d.png' % g))
import bpy
A = G.build('DAY'); sc = bpy.context.scene; G.setup_render(sc, 'preview'); sc.cycles.samples = 12
for nm in ('street_eye', 'pagoda_low', 'two_buildings'):
    G.apply_cam_state(nm, 'DAY'); G.make_camera(A['cams'][nm]); G.apply_dof(nm); G.stage_placeholders(A, G.STAGING[nm], A['cams'][nm]['loc'])
    G.render(os.path.join(OUTR, 'DAY_%s.png' % nm))
