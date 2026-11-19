#!/usr/bin/env python3
"""prove.py : stills, state strips, markers, timing and shadow report for office_props.py.
    python3 prove.py stills [cam,...] [--q 640] [--samples 8]
    python3 prove.py strips [prop,...]
    python3 prove.py markers
    python3 prove.py timing
    python3 prove.py shadow
    python3 prove.py probe            # projected head sizes / positions per new camera (no render)"""
import os, sys, json, time, math
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'cast')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import cast_ext                                              # noqa: F401  registers senior_a / senior_b in the v2 puppet
import bpy
from mathutils import Vector
import office3d as S, office_props as X
OUT = os.path.join(HERE, 'out')
HEAD_Z = dict(hero=2.46, boss=2.87, senior_a=2.71, senior_b=2.51)        # head centre above the feet (sprites.feet_of / cast heights)

def project(setup, p, W=720, H=1280):
    cam = bpy.context.scene.camera; bpy.context.view_layer.update()
    from bpy_extras.object_utils import world_to_camera_view
    co = world_to_camera_view(bpy.context.scene, cam, Vector(p)); return co.x * W, (1 - co.y) * H, co.z

def head_px(cam_loc, p):
    cam = bpy.context.scene.camera; fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1)); depth = (Vector(p) - cam.matrix_world.translation).dot(fwd)
    return 782.22 / depth

BOSS_NEAR = dict(yaw=-0.45, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand')
SENIOR_POSE = dict(yaw=0.45, expr='smug', arm_l='down', arm_r='hip', legs='stand')
SENIOR_POSE_L = dict(yaw=-0.45, expr='smug', arm_l='hip', arm_r='down', legs='stand')

# per camera: (prop state function, actors [(cast, mark key or xyz, pose or story key)])
def st_clean(): X.reset(); S.set_track(0, 0)
def st_spinner(): X.reset(); S.set_track(0, 0); X.set_spinner(u=0.0, angle=25, wobble=2)
def st_chalk(g=1.0): X.reset(); S.set_track(0, 0); X.set_spinner(u=0, angle=40); X.set_chalk(g); [X.set_ghost(i, 1.0) for i in range(1, 7)]; X.set_tick(1.0)
def st_ruler(): st_chalk(); S.set_track(0.62, 0); X.set_ruler(1.0)
def st_line(): st_chalk(); S.set_track(1, 0)
def st_label(): st_line(); X.set_label(1.0, res='hi')
def st_persist(): st_line(); X.set_smudge(3); X.set_crumbs(1); X.set_ruler(0.0)
def st_tt(): st_line(); X.set_teletype(feed=0.8, stamp=0, yaw_deg=-45)

ACT = {
    'calendar_cam': (lambda: (st_clean(), X.set_calendar(20, lift=0.35)), []),
    'spinner_rake': (st_spinner, []),
    'coast_rake': (st_spinner, []),
    'low_three': (st_spinner, [('senior_a', 'senior_a_row', SENIOR_POSE), ('boss', 'chief_row', BOSS_NEAR), ('senior_b', 'senior_b_row', SENIOR_POSE_L)]),
    'chalk_rake': (lambda: st_chalk(0.75), []),
    'chalk_wide': (st_chalk, []),
    'high_wide': (st_chalk, [('hero', 'hero_mark', 'hero_draw'), ('senior_a', 'senior_a_front', SENIOR_POSE), ('boss', 'chief_front', BOSS_NEAR), ('senior_b', 'senior_b_front', SENIOR_POSE_L)]),
    'insert_front': (st_ruler, []),
    'corridor_cam': (st_line, []),
    'low_boss': (st_line, [('boss', 'boss_mark', BOSS_NEAR)]),
    'G': (st_line, [('boss', 'boss_mark', BOSS_NEAR), ('hero', 'gloat_near', 'hero_draw')]),
    'G_prime': (st_label, [('boss', 'boss_mark', BOSS_NEAR), ('hero', 'gloat_near', 'hero_draw')]),
    'insert_rake_ny': (lambda: (st_line(), S.set_track(1, 0.6), X.set_smudge(1)), []),
    'low_two_wall': (lambda: (st_line(), S.set_track(1, 0.8), X.set_smudge(2)), [('hero', 'hero_mark', 'hero_draw'), ('boss', 'boss_mark', 'boss_rub')]),
    'high_two_shot': (st_persist, [('hero', 'hero_mark', 'hero_draw'), ('boss', 'boss_mark', BOSS_NEAR)]),
    'desk_fg': (lambda: (st_persist(), X.set_crumbs(0)), [('senior_a', 'senior_a_desk', SENIOR_POSE), ('senior_b', 'senior_b_desk', SENIOR_POSE_L), ('hero', 'hero_mark', 'hero_draw'), ('boss', 'chief_wall12', BOSS_NEAR)]),
    'label_insert': (st_label, []),
    'window_tt': (st_tt, [('hero', 'hero_tt', 'hero_draw'), ('boss', 'chief_tt', BOSS_NEAR)]),
    'sheet_full': (lambda: (st_tt(), X.set_teletype(show=0), X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], bow=0.3)), [('boss', 'chief_tt', BOSS_NEAR)]),
    'wide_high': (lambda: (st_clean(), X.set_teletype(feed=0.6, yaw_deg=-30)), [('hero', 'hero_mark', 'hero_draw'), ('boss', 'teletype_mark', BOSS_NEAR)]),
}

def setup(quality='preview', samples=8, hi_map=False):
    A = S.build('INTERIOR_DAY'); PA = X.build(A, hi_map=hi_map); sc = bpy.context.scene
    S.setup_render(sc, quality); sc.cycles.samples = samples
    if quality == 'preview': sc.render.threads = 2
    return A, PA, sc

def stage(A, PA, actors, cam_loc):
    S._clear_actors(bpy.context.scene); obs = []
    for i, (cast, mk, pose) in enumerate(actors):
        mark = PA['marks'].get(mk) or A.get(mk) if isinstance(mk, str) else mk
        if isinstance(pose, str): o = S.placeholder_actor(cast, pose, mark, face_to=cam_loc, name='actor_%s_%d' % (cast, i))
        else: o = S.placeholder_actor(cast, 'hero_draw', mark, face_to=cam_loc, name='actor_%s_%d' % (cast, i), pose=pose)
        o.location.y -= 0.0025 * i; obs.append((cast, mark, o))
    return obs

def cmd_stills(names=None, samples=8, quality='preview', outdir=None):
    outdir = outdir or os.path.join(OUT, 'stills'); os.makedirs(outdir, exist_ok=True); rep = {}
    A, PA, sc = setup(quality, samples); cams = X.all_cams(A, PA)
    for nm in (names or list(ACT)):
        fn, actors = ACT[nm]; cs = cams[nm]
        if nm == 'corridor_cam': X.set_map_res(True)
        fn(); cam = S.make_camera(cs); obs = stage(A, PA, actors, cs['loc'])
        heads = []
        for cast, mark, o in obs:
            hp = (mark[0], mark[1], HEAD_Z[cast]); x, y, z = project(cs, hp); heads.append(dict(cast=cast, x=round(x), y=round(y), px=round(head_px(cs['loc'], hp))))
        t0 = time.time(); S.render(os.path.join(outdir, nm + '.png')); dt = time.time() - t0
        rep[nm] = dict(cam=cs, heads=heads, seconds=round(dt, 1)); print(nm, json.dumps(heads), '%.1fs' % dt, flush=True)
        if nm == 'corridor_cam': X.set_map_res(False)
    json.dump(rep, open(os.path.join(outdir, 'stills.json'), 'w'), indent=1)

def cmd_probe():
    A, PA, sc = setup(); cams = X.all_cams(A, PA); out = {}
    for nm, (fn, actors) in ACT.items():
        cs = cams[nm]; S.make_camera(cs); hs = []
        for cast, mk, pose in actors:
            mark = PA['marks'].get(mk) or A.get(mk); hp = (mark[0], mark[1], HEAD_Z[cast]); x, y, z = project(cs, hp)
            hs.append('%s %dpx @(%d,%d)' % (cast, head_px(cs['loc'], hp), x, y))
        extra = {}
        for k, p in (('NY', S.track_point(1)), ('storm', S.track_point(0)), ('label_c', (0.125, -0.054, 3.27)), ('cal_c', (-1.84, -0.048, 4.12))):
            x, y, z = project(cs, p); extra[k] = (round(x), round(y)) if z > 0 else None
        print(nm, cs, hs, extra)

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else 'probe'
    if cmd == 'stills':
        names = a[1].split(',') if len(a) > 1 and not a[1].startswith('-') else None
        cmd_stills(names, samples=int(a[a.index('--samples') + 1]) if '--samples' in a else 8)
    elif cmd == 'probe': cmd_probe()

# ----------------------------------------------------------------------------- strips, markers, timing, shadow
STRIPS = {
    'spinner': ('spinner_rake', st_spinner, [lambda: X.set_spinner(u=0, show=0), lambda: X.set_spinner(u=0, angle=0, scale=1.3, pin_out=0.05),
                                            lambda: X.set_spinner(u=0, angle=90, wobble=3), lambda: X.set_spinner(u=0, angle=200, squash=1.4, fast=1),
                                            lambda: (X.set_spinner(u=0.25, angle=300), X.set_spinner(u=0, angle=10, which='ghost1'))]),
    'chalk_ghosts': ('chalk_wide', lambda: (st_chalk(0), X.set_tick(0), [X.set_ghost(i, 0.0) for i in range(1, 7)]), [lambda: X.set_chalk(0.2), lambda: X.set_chalk(0.5), lambda: (X.set_chalk(1.0), X.set_ghost(1, 1), X.set_ghost(2, 0.5)),
                                            lambda: (X.set_chalk(1.0), [X.set_ghost(i, 1, 0.35) for i in range(1, 7)], X.set_tick(1, 1.25)), lambda: (X.set_chalk(1, crumble=1), X.set_tick(1))]),
    'ruler': ('insert_front', lambda: (st_chalk(), S.set_track(0.3, 0)), [lambda: X.set_ruler(0.0), lambda: X.set_ruler(0.3), lambda: X.set_ruler(0.7), lambda: (X.set_ruler(1.0), S.set_track(0.95, 0)),
                                            lambda: (X.set_ruler(0.4), S.set_track(1, 0))]),
    'label': ('label_insert', st_line, [lambda: X.set_label(0), lambda: X.set_label(1, away=0.12, scale=1.08, pin=0), lambda: X.set_label(1, swing_deg=4, pin_out=0.05),
                                            lambda: X.set_label(1, curl=1.0), lambda: X.set_label(1, swing_deg=-8, flutter=1.0)]),
    'smudge_crumbs': ('insert_rake_ny', lambda: (st_line(), S.set_track(1, 0)), [lambda: X.set_smudge(0), lambda: (X.set_smudge(1), X.set_crumbs(0.25)), lambda: (X.set_smudge(2), X.set_crumbs(0.5)),
                                            lambda: (X.set_smudge(3), X.set_crumbs(1.0)), lambda: (S.set_track(1, 0.6), X.set_smudge(3), X.set_crumbs(1.0))]),
    'calendar': ('calendar_cam', st_clean, [lambda: X.set_calendar(20), lambda: X.set_calendar(20, lift=0.5), lambda: X.set_calendar(20, lift=0.3, flutter=1.0),
                                            lambda: X.set_calendar(20, tear=0.25, lift=0.6), lambda: X.set_calendar(21)]),
    'teletype': ('tt_close', st_clean, [lambda: X.set_teletype(0.0, yaw_deg=-45), lambda: X.set_teletype(0.35, yaw_deg=-45), lambda: X.set_teletype(0.7, yaw_deg=-45),
                                            lambda: (X.set_teletype(1.0, 1.0, yaw_deg=-45), X.set_stamp((3.0, -0.85, 2.4), face_dir=(0.7, 0.7, 0))), lambda: X.set_teletype(1.0, 1.0, yaw_deg=-45, show=0)]),
    'sheet': ('sheet_full', lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face']), [
        lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], word1=0, word2=0, stamp=0),
        lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], word1=0, word2=0, stamp=1),
        lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], word1=1, word2=0, pop1=1),
        lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], word1=1, word2=1, pop2=1, bow=0.6),
        lambda: X.set_sheet(X.STATE['PA']['sheet_hold'], facing=X.STATE['PA']['sheet_face'], word1=1, word2=1, bow=-0.6, roll_deg=4)]),
}

def cmd_strips(names=None, samples=8):
    od = os.path.join(OUT, 'strips'); os.makedirs(od, exist_ok=True); A, PA, sc = setup('preview', samples); cams = X.all_cams(A, PA)
    cams['tt_close'] = dict(loc=(1.9, -2.4, 2.25), look_at=(3.1, -0.75, 2.05), lens=22)
    sys.path.insert(0, HERE); import sheet as SH
    for nm in (names or list(STRIPS)):
        cam, base, states = STRIPS[nm]; S._clear_actors(sc); X.reset(); S.set_track(0, 0); base(); S.make_camera(cams[cam]); ps = []
        for i, f in enumerate(states):
            base(); f(); p = os.path.join(od, '%s_%d.png' % (nm, i)); S.render(p); ps.append(p)
        SH.sheet(os.path.join(od, 'strip_%s.jpg' % nm), ps, cols=5, h=560, labels=['%s state %d' % (nm, i) for i in range(5)]); print('strip', nm, flush=True)

def cmd_keyed():
    """Keyframed versions of the setters must equal the static states: key 3 frames, render frame 2 and the same state set statically."""
    od = os.path.join(OUT, 'keyed'); os.makedirs(od, exist_ok=True); A, PA, sc = setup('preview', 8); S.make_camera(X.all_cams(A, PA)['chalk_wide'])
    st_chalk(0)
    for f, g in ((1, 0.0), (2, 0.5), (3, 1.0)):
        X.set_chalk(g, frame=f); X.set_spinner(u=0, angle=120 * f, frame=f); X.set_ghost(1, g, frame=f); X.set_label(1 if f > 1 else 0, swing_deg=4 * f, frame=f); X.set_smudge(f, frame=f)
    sc.frame_set(2); S.render(os.path.join(od, 'keyed_f2.png'))
    X.set_chalk(0.5); X.set_spinner(u=0, angle=240); X.set_ghost(1, 0.5); X.set_label(1, swing_deg=8); X.set_smudge(2)
    for o in list(X.STATE['objects'].values()) + [X.STATE['ctl']]:
        if o.animation_data: o.animation_data_clear()
    for m in bpy.data.materials:
        pass
    sc.frame_set(2); S.render(os.path.join(od, 'static_f2.png'))
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(od, 'keyed_f2.png')), dtype=float); b = np.asarray(Image.open(os.path.join(od, 'static_f2.png')), dtype=float)
    print('KEYED vs STATIC max abs diff %.1f, mean %.3f' % (np.abs(a - b).max(), np.abs(a - b).mean()))

def cmd_markers():
    od = os.path.join(OUT, 'markers'); os.makedirs(od, exist_ok=True); A, PA, sc = setup('preview', 8); cams = X.all_cams(A, PA)
    st_label(); X.set_ruler(1); X.set_teletype(0.8, yaw_deg=-45); X.set_sheet(PA['sheet_hold'], facing=PA['sheet_face']); n = X.add_markers(PA); print('markers', n)
    sys.path.insert(0, HERE); import sheet as SH; ps = []
    for nm in ('chalk_wide', 'label_insert', 'wide_high', 'window_tt', 'calendar_cam', 'high_wide'):
        S.make_camera(cams[nm]); p = os.path.join(od, nm + '.png'); S.render(p); ps.append(p)
    SH.sheet(os.path.join(OUT, 'sheet_markers.jpg'), ps, cols=6, h=600)

def cmd_timing(threads=4, n=3):
    A, PA, sc = setup('fast', 12); sc.render.threads = threads; cs = X.all_cams(A, PA)['G_prime']
    st_label(); X.set_smudge(3); X.set_crumbs(1); X.set_ruler(1); X.set_teletype(0.8, 1, yaw_deg=-45); X.set_sheet(PA['sheet_hold'], facing=PA['sheet_face'])
    X.set_stamp((3.0, -0.85, 2.4), face_dir=(0.7, 0.7, 0)); X.set_calendar(20, lift=0.3); X.set_spinner(u=0, angle=30, which='ghost1')
    cam = S.make_camera(cs); stage(A, PA, [('boss', 'boss_mark', BOSS_NEAR), ('hero', 'gloat_near', 'hero_draw')], cs['loc']); res = []
    for i in range(n):
        cam.location.x += 0.01; w, c = S.render(os.path.join(OUT, 'timing_%d.png' % i)); res.append((w, c)); print('frame %d: %.2f s wall, %.2f s cpu, load %s' % (i, w, c, ' '.join('%.2f' % v for v in os.getloadavg())), flush=True)
    json.dump(dict(threads=threads, samples=12, res='720x1280', frames=res), open(os.path.join(OUT, 'timing.json'), 'w'))

def cmd_shadow():
    A, PA, sc = setup(); st_label(); out = {}
    for nm, acts in (('chief_boss_mark+hero_near_mark', [('boss', 'boss_mark', BOSS_NEAR), ('hero', 'near_mark', 'hero_draw')]),
                     ('G: chief_boss_mark+hero_gloat_near', [('boss', 'boss_mark', BOSS_NEAR), ('hero', 'gloat_near', 'hero_draw')]),
                     ('chief 0.2 D right of boss_mark (1.50,-0.42)', [('boss', (1.50, -0.42, 0.0), BOSS_NEAR), ('hero', 'gloat_near', 'hero_draw')]),
                     ('chief at boss_mark, label shifted 0.1 up (risk note 5)', [('boss', 'boss_mark', BOSS_NEAR)]),
                     ('hook: hero_mark+boss_mark (story poses)', [('hero', 'hero_mark', 'hero_draw'), ('boss', 'boss_mark', 'boss_rub')])):
        X.set_label(1, raise_d=0.1 if 'shifted' in nm else 0.0); stage(A, PA, acts, (1.5, -4.9, 2.6)); r = X.track_shadow_report(); out[nm] = r; print(nm, json.dumps(r))
    S._clear_actors(sc); out['no actors'] = X.track_shadow_report(); print('no actors', out['no actors'])
    json.dump(out, open(os.path.join(OUT, 'shadow_report.json'), 'w'), indent=1)

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else ''
    if cmd == 'strips': cmd_strips(a[1].split(',') if len(a) > 1 else None)
    elif cmd == 'markers': cmd_markers()
    elif cmd == 'timing': cmd_timing(int(a[1]) if len(a) > 1 else 4)
    elif cmd == 'shadow': cmd_shadow()
    elif cmd == 'keyed': cmd_keyed()
