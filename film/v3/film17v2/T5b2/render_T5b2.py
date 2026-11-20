# T5b render driver (film 17 v2, g1211-1383). usage: python3 -I render_T5b.py still <g> <out.png> | full
import sys, os
sys.path.insert(0, "film/v3/set3d17"); import prefecture17 as P, bpy
take = 'T5'; OUT = 'film/v3/film17v2/T5b2/frames'
def assign_for(g):
    if g < 1274:   # 5c escort march, inspector smirks and follows
        return {'bertillon': ('bertillon_tired', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_held', {}),
                'gend_a': ('gendarme_escort_a', {}), 'gend_b': ('gendarme_escort_b', {})}
    if g < 1345:   # 5d three-shot: dupont's innocent shrug, inspector grins
        return {'bertillon': ('bertillon_neutral', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_innocent', {}),
                'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
    return {'bertillon': ('bertillon_measuring', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_innocent', {}),
            'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
# director fix (a)+(b): local camera override for g>=1250 (raised to eye/chest height, less down-tilt), eased in from the original path over g1250-1274; day lights lowered
import json
OV = json.load(open('film/v3/film17v2/T5b/override.json'))
ks = [k for k in P.TAKES[take]['keys'] if k['g'] < 1250]
ks.append(P._k(1250, (19.42, 19.38, 2.19), (16.67, 20.74, 1.58)))
for k in OV['keys']: ks.append(P._k(k['g'], tuple(k['loc']), tuple(k['look']), hold=k.get('hold', False)))
P.TAKES[take]['keys'] = ks
P.K.LIGHTS['ARCHIVE_NIGHT'].update(fill_w=230, lamp_k=1.0, gasolier_k=0.7)   # = T5a's t5a_override.apply() (410265b): same night state at the start of the g1196-1211 mix
for _k in ('ARCHIVE_NIGHT', 'ARCHIVE_DAY'): P.K.LIGHTS[_k]['beam_k'] = 0.0   # director: beam FX (skylight beam volume) = 0 for g>=1218, i.e. the whole T5b2 range
import copy
DAY0 = copy.deepcopy(P.K.LIGHTS['ARCHIVE_DAY']); MUL = OV['light']['mul'] if OV.get('light') else 1.0
def day_scale(g):   # director: 1.0 at g1211 (matches T5a's last frame), smoothstep down to MUL by g1241. lights only: no haze, no desaturation
    u = max(0.0, min(1.0, (g - 1211) / 30.0)); u = u * u * (3 - 2 * u); return 1.0 + (MUL - 1.0) * u
def set_day(g):
    m = day_scale(g); D = P.K.LIGHTS['ARCHIVE_DAY']
    for key in ('shade', 'tint'): D[key] = tuple(x * m for x in DAY0[key])
    for key in ('gain', 'fill_w', 'vault_w', 'sun_k', 'lamp_k'): D[key] = DAY0[key] * m
    mx = P.TAKES[take]['mix']; P.set_light_mix(mx[2], mx[3], 1.0, g + 1); P.set_flicker2(1.0, frame=g + 1)
assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
A = P.world_build(take); P.key_take(take); RES = tuple(int(x) for x in os.environ.get('RES', '720x1280').split('x')); P.setup_render2(RES, samples=16, threads=2)
def clear_cast():   # director fix (render17v2/T3 e86e676): stage_cast2 never removes old actors; stale shadow proxies pile up into black slabs
    sys.path.insert(0, 'film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
import sys as _s; _s.path.insert(0, 'film/v3/cast17'); import cast17 as _c17; _LEAN0 = _c17.STORY17['inspector_arms_crossed'][1].get('lean', 0.0)
def _ss(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def stage_fix(g, a):   # director TAKE-gate fix (staging only, camera untouched): inspector eased 0.5 m screen-right (+y) over g1335-1355; gend_a eased 1.3 m screen-right (+y) out of frame over g1300-1320
    if os.environ.get('STAGE_FIX', '1') == '0': return a
    import math, sys; sys.path.insert(0, 'film/v3/cast17'); import cast17
    mv = 1.0 if 1335 <= g <= 1355 else 0.0   # director OK: shuffle bob 0.035 m at 2 Hz (15-frame period) + a small lean into the move, same pose, over the move
    bob = mv * 0.035 * (0.5 - 0.5 * math.cos(2 * math.pi * (g - 1335) / 15.0)); lean = mv * 3.0 * math.sin(math.pi * (g - 1335) / 20.0)
    cast17.STORY17['inspector_arms_crossed'][1]['lean'] = _LEAN0 + lean
    a = dict(a); pose, o = a['inspector']; a['inspector'] = (pose, dict(o, dy=0.5 * _ss((g - 1335) / 20.0), dz=bob))
    pose, o = a['gend_a']; a['gend_a'] = (pose, dict(o, dy=1.3 * _ss((g - 1300) / 20.0))); return a
def one(g, path):
    set_day(g); bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, stage_fix(g, assign_for(g)))
    bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True); P.grade2(path)
if sys.argv[1] == 'still': one(int(sys.argv[2]), sys.argv[3])
else:
    os.makedirs(OUT, exist_ok=True)
    G0, G1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1211, 1383)   # usage: full [g0 g1]
    for g in range(G0, G1 + 1):
        p = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(p) and os.path.getsize(p) > 50000: continue
        one(g, p)
