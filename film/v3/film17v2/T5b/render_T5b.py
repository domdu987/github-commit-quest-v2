# T5b render driver (film 17 v2, g1211-1383). usage: python3 -I render_T5b.py still <g> <out.png> | full
import sys, os
sys.path.insert(0, "film/v3/set3d17"); import prefecture17 as P, bpy
take = 'T5'; OUT = 'film/v3/film17v2/T5b/frames'
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
if OV.get('light'):   # day lights only: scale the ARCHIVE_DAY preset the set_light_mix lands on (lights, no haze, no desaturation)
    m = OV['light']['mul']; D = P.K.LIGHTS['ARCHIVE_DAY']
    for key in ('shade', 'tint'): D[key] = tuple(x * m for x in D[key])
    for key in ('gain', 'fill_w', 'vault_w', 'sun_k', 'lamp_k'): D[key] = D[key] * m
assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
A = P.world_build(take); P.key_take(take); RES = tuple(int(x) for x in os.environ.get('RES', '720x1280').split('x')); P.setup_render2(RES, samples=16, threads=2)
def one(g, path):
    bpy.context.scene.frame_set(g + 1); P.stage_cast2(take, g, assign_for(g))
    bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True); P.grade2(path)
if sys.argv[1] == 'still': one(int(sys.argv[2]), sys.argv[3])
else:
    os.makedirs(OUT, exist_ok=True)
    for g in range(1211, 1384):
        p = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(p) and os.path.getsize(p) > 50000: continue
        one(g, p)
