import sys, os, time
ROOT = '/home/user/github-commit-quest-v2'
sys.path.insert(0, ROOT + '/film/v3/set3d17'); os.chdir(ROOT + '/film/v3/set3d17')
import prefecture17 as P, bpy
take = 'T3'
# director final offsets (T3b adf5f05): constant offset of the measuring chair + its sitter. Applies over the whole part.
CHAIR_D = (-0.4, 0.0); PRIS_D = (-0.15, 0.0)
_kc = P.K.measuring_chair
P.K.measuring_chair = lambda B, c, **kw: _kc(B, (c[0] + CHAIR_D[0], c[1] + CHAIR_D[1]), **kw) if abs(c[0] - 0.7) < 1e-6 and abs(c[1] - 2.4) < 1e-6 else _kc(B, c, **kw)
# ---- director TAKE-gate fix list (items 1, 2, 3) ----
# item 3: the gasolier at room-local (-0.35, 1.0) (world 8.85, 13.0; lamps at z 3.9) hangs in front of the green gendarme `gend_b` (10.5, 10.5) from the g741-761 cameras.
# ONE constant, shared with T3b: raise that gasolier by GAS_DZ (its pendant drop 1.45 -> 1.45-GAS_DZ). The other gasolier (1.0, -1.4) is untouched.
GAS_DZ = 0.6
_kg = P.K.gasolier
P.K.gasolier = lambda B, c, **kw: _kg(B, c, **dict(kw, drop=kw.get('drop', 1.45) - GAS_DZ)) if abs(c[0] + 0.35) < 1e-6 and abs(c[1] - 1.0) < 1e-6 else _kg(B, c, **kw)
import math
from mathutils import Vector, Matrix
def _lookrot_smooth(loc, look, up_hint=(0, 1, 0)):
    # item 1: the stock _lookrot switches the camera up vector from +y to world-Z when |f.z| crosses 0.995 (g664): the roll jumps ~9 deg in one frame.
    # Blend the two perpendicular up directions smoothly over |f.z| 0.9990 (g645, same as before) -> 0.9866 (g675, pure world-Z up). Below 0.9866 identical to stock.
    f = (Vector(look) - Vector(loc)).normalized(); d = abs(f.z)
    def perp(a): a = Vector(a); a = a - f * a.dot(f); return a.normalized()
    t = max(0.0, min(1.0, (d - 0.9866) / (0.9990 - 0.9866))); w = t * t * (3 - 2 * t)
    if d > 0.9999: u = perp(up_hint)
    else: u = (perp(up_hint) * w + perp((0, 0, 1)) * (1 - w)).normalized()
    rgt = f.cross(u).normalized(); u = rgt.cross(f); return Matrix((rgt, u, -f)).transposed().to_quaternion()
P._lookrot = _lookrot_smooth
Z_DIP_A, Z_DIP_G0, Z_DIP_G1 = 0.85, 700, 745   # item 2: camera z lowered by A*sin^2(pi*(g-700)/45) (zero value and slope at both ends): it passes below the ceiling slab (z 5.25) at ~g722 instead of g736
_pt = P.path_take
def _path_take(take):
    fr = _pt(take)
    if take != 'T3': return fr
    for f in fr:
        if Z_DIP_G0 < f['g'] < Z_DIP_G1:
            l = list(f['loc']); l[2] -= Z_DIP_A * math.sin(math.pi * (f['g'] - Z_DIP_G0) / (Z_DIP_G1 - Z_DIP_G0)) ** 2; f['loc'] = tuple(l)
    prev = None
    for f in fr:
        q = P._lookrot(f['loc'], f['look'])
        if prev is not None and q.dot(prev) < 0: q.negate()
        prev = q; f['rot'] = tuple(q)
    return fr
P.path_take = _path_take
OUT = os.environ.get('OUT', ROOT + '/film/v3/film17v2/T3/frames')
def assign_for(g):
    a = {'bertillon': ('bertillon_measuring', {'mirror': True}),
         'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
         'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'}),
         'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'})}
    if g < 725:   # 3a: whole room laughs
        a['inspector'] = ('inspector_laughing', {}); a['gend_a'] = ('gendarme_laughing_a', {})
        a['gend_b'] = ('gendarme_laughing_b', {}); a['prankster'] = ('gendarme_laughing_b', {})
    else:         # 3b/3c: room back to work, prefect in
        a['inspector'] = ('inspector_arms_crossed', {}); a['gend_a'] = ('gendarme_standing_a', {})
        a['gend_b'] = ('gendarme_standing_b', {}); a['prankster'] = ('gendarme_standing_b', {})
        a['prefect'] = ('prefect_finger_up_three', {}) if g < 792 else ('prefect_stern', {})
    a['prisoner_chair'] = (a['prisoner_chair'][0], dict(a['prisoner_chair'][1], dx=PRIS_D[0], dy=PRIS_D[1]))
    return a
def clear_cast():
    # stage_cast2 builds NEW actors every call and never removes the old ones: stale shadow proxies/cards pile up (black slabs by ~g660). Remove them first.
    sys.path.insert(0, ROOT + '/film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
RAMP_LO, RAMP_G0, RAMP_G1 = 0.4, 750, 800   # lights x0.4 through g750, easing to x1.0 at g800 (high bird's-eye views run luma 120-135, the low g800 view ~95)
def ramp_f(g): return RAMP_LO if g <= RAMP_G0 else 1.0 if g >= RAMP_G1 else RAMP_LO + (1 - RAMP_LO) * (g - RAMP_G0) / (RAMP_G1 - RAMP_G0)
def apply_ramp():
    # every light's energy keys x ramp_f(frame-1); lights with no animation get a key per frame inside the ramp. Lights only: no haze, no saturation.
    for o in [o for o in bpy.data.objects if o.type == 'LIGHT']:
        d = o.data; ad = d.animation_data
        if ad and ad.action:
            for ly in ad.action.layers:
                for st in ly.strips:
                    for cb in st.channelbags:
                        for fc in cb.fcurves:
                            if fc.data_path != 'energy': continue
                            for kp in fc.keyframe_points:
                                f = ramp_f(int(round(kp.co.x)) - 1); kp.co.y *= f; kp.handle_left.y *= f; kp.handle_right.y *= f
                            fc.update()
        else:
            e = d.energy
            for g in range(645, RAMP_G1 + 3): d.energy = e * ramp_f(g); d.keyframe_insert('energy', frame=g + 1)
def main(gs):
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=int(os.environ.get('SAMPLES', 16)), threads=2)
    if min(gs) <= RAMP_G1: apply_ramp()
    for g in gs:
        fn = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(fn) and os.path.getsize(fn) > 50000: continue
        t0 = time.time(); bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = fn; bpy.ops.render.render(write_still=True); P.grade2(fn)
        print('g%d %.1fs' % (g, time.time() - t0), flush=True)
if __name__ == '__main__':
    a = sys.argv[1:]
    gs = [int(x) for x in a[0].split(',')] if ',' in a[0] or len(a) == 1 else range(int(a[0]), int(a[1]) + 1)
    main(gs)
