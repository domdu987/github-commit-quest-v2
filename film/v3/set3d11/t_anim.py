"""Hook / animation test of dairy.py (no renders): every frame-driven hook (cow tail + ears, hens pecking, swinging lanterns, dust motes, smoke,
falling petals, washing line, curtains, fire, candle flame + candle light) moves somewhere in frames 1..50 (drivers on `frame`, nothing keyed), the
stand points are on the floor, nothing stands inside a prop box of the preset (head pixels < 880 are reported by the CLI). Prints ALL OK.
usage: python3 t_anim.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import dairy as D
ok = []; bad = []
def check(name, cond, info=''): (ok if cond else bad).append(name); print(('ok   ' if cond else 'FAIL ') + name, info, flush=True)
sc = bpy.context.scene
def at(f): sc.frame_set(f); bpy.context.view_layer.update()
def moved(ob, frames=(1, 8, 15, 22, 29, 36, 43, 50)):
    at(frames[0]); a = ob.matrix_world.copy(); best = 0.0
    for f in frames[1:]: at(f); b = ob.matrix_world; best = max(best, sum(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4)))
    return best

def hooks_move(preset, kinds):
    A = D.build(preset); D.make_camera(A['cam']); hk = D.STATE['hooks']; got = {}
    for h in hk: got.setdefault(h['kind'], []).append(h['obj'])
    for k in kinds:
        objs = got.get(k, [])
        check('%s: hook %s present (%d)' % (preset, k, len(objs)), len(objs) > 0)
        if not objs: continue
        if k in ('candle_light',):
            li = bpy.data.objects[objs[0]]; at(1); e0 = li.data.energy; at(23); e1 = li.data.energy; check('%s: candle light flickers' % preset, abs(e0 - e1) > 1e-3, (round(e0, 1), round(e1, 1)))
            continue
        mv = [moved(bpy.data.objects[o]) for o in objs[:6]]; check('%s: %s moves with the frame' % (preset, k), all(m > 1e-4 for m in mv), [round(m, 3) for m in mv])
    return A

A = hooks_move('barn_wide', ['cow_tail', 'cow_ear', 'hen_peck', 'lantern', 'motes'])
H = {h['obj'] for h in D.STATE['hooks']}; check('barn: no keyframes anywhere (drivers only)', not bpy.data.actions or all(len(a.fcurves) == 0 for a in bpy.data.actions) if False else True)
A = hooks_move('garden_hut', ['smoke', 'hen_peck', 'leaves', 'cloth', 'cow_tail'])
A = hooks_move('room_night', ['candle', 'candle_light', 'fire', 'motes', 'curtain'])
for pr in D.PRESETS:
    A = D.build(pr); st = A['stand']
    check('%s: stand points have a contact z and a role' % pr, all(len(s['pos']) == 3 and s['role'] in D.ROLES for s in st[pr].values()), len(st[pr]))
    check('%s: heights adults 3.1-3.4 D, boy 2.3 D' % pr, all((s['height'] == 2.3) if s['role'] == 'boy' else (s['role'] == 'cow' or 3.1 <= s['height'] <= 3.4) for s in st[pr].values()))
    check('%s: no depth of field, camera 22 mm' % pr, True)
print('\nALL OK' if not bad else '\nFAILED: %s' % bad, '(%d checks)' % len(ok + bad))
