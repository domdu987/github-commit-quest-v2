"""jimo_r2.py : round 2 of the film-18 set: real 2D cast cards at the stand marks (people + ox cards from cast18, rasterised by jimo_cards), contact shadows, per-shot
tweaks (post_build), ox card yaw (3/4 toward the camera). Placeholder cards exist ONLY for the stills / contact sheet (ACTORS=0 leaves them out)."""
import os, math, random
import numpy as np
import bpy
from mathutils import Vector as V, Matrix
import jimo as J
import jimo_shots as S
import jimo_cards as CD
T = J.T; STATE = J.STATE

# ------------------------------------------------------------------ card materials / meshes
_MAT = {}; _MESH = {}
def _card_mat(path, tint, k, name):
    key = (path, tuple(round(x, 3) for x in tint), round(k, 3), STATE.get('pre'))
    if key in _MAT and bpy.data.materials.get(_MAT[key]) is not None: return bpy.data.materials[_MAT[key]]
    m = bpy.data.materials.new('JM_card_%s_%d' % (name, len(_MAT))); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); t = N('ShaderNodeTexImage')
    t.image = T._img(path); t.interpolation = 'Linear'; t.extension = 'CLIP'; t.image.alpha_mode = 'STRAIGHT'
    mm = N('ShaderNodeMix'); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs[0].default_value = 1.0; mm.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
    L(t.outputs['Color'], mm.inputs[6]); L(mm.outputs[2], em.inputs['Color']); em.inputs['Strength'].default_value = k
    L(t.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; _MAT[key] = m.name; return m

def _shadow_png():
    p = os.path.join(CD.CARDS, 'contact_shadow.png')
    if not os.path.exists(p):
        from PIL import Image
        n = 128; yy, xx = np.mgrid[0:n, 0:n]; r = np.hypot((xx - n / 2) / (n / 2), (yy - n / 2) / (n / 2)); a = np.clip(1.0 - r, 0, 1) ** 0.8 * 0.62
        im = np.zeros((n, n, 4), np.uint8); im[..., 3] = (a * 255).astype(np.uint8); im[..., :3] = (10, 8, 20); Image.fromarray(im, 'RGBA').save(p)
    return p

def _quad(name, u0, u1, z0, z1):
    if bpy.data.meshes.get(name) is not None and name in _MESH: return bpy.data.meshes[name]
    me = bpy.data.meshes.new(name); me.from_pydata([(u0, 0, z0), (u1, 0, z0), (u1, 0, z1), (u0, 0, z1)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    _MESH[name] = 1; return me

def _shadow_quad(name, w, d):
    if bpy.data.meshes.get(name) is not None and name in _MESH: return bpy.data.meshes[name]
    me = bpy.data.meshes.new(name); me.from_pydata([(-w, -d, 0.04), (w, -d, 0.04), (w, d, 0.04), (-w, d, 0.04)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    _MESH[name] = 1; return me

LIGHT_TINT = dict(NIGHT=((0.70, 0.76, 1.0), 0.62), DUSK=((1.0, 0.92, 0.84), 0.95), DAWN=((1.0, 0.93, 0.86), 0.95))
def _tint(extra=None, warm=0.0):
    tn, k = LIGHT_TINT[STATE['light']]; tn = np.array(tn)
    if warm: tn = tn * (1 - warm) + np.array((1.0, 0.72, 0.5)) * warm
    if extra is not None: tn = tn * np.array(extra)
    return tuple(tn), k

def put_card(meta, pos, yaw_deg, scale=1.0, mirror=False, name='ph', tint=None, k=None, shadow=True, sw=1.6):
    """A card (textured alpha quad, bottom at the feet) at pos: yaw about z (the quad faces -y at yaw 0), uniform scale, optional mirror in u."""
    tn, kk = _tint(); tn = tint or tn; kk = k if k is not None else kk
    me = _quad('cq_%s_%.3f' % (os.path.basename(meta['path']), scale), meta['x0'] * scale, (meta['x0'] + meta['w']) * scale, -(meta['h'] - meta['feet']) * scale, meta['feet'] * scale)
    if not me.materials: me.materials.append(_card_mat(meta['path'], tn, kk, name))
    else: me.materials[0] = _card_mat(meta['path'], tn, kk, name)
    ob = bpy.data.objects.new('ph_%s' % name, me); STATE['SET'].objects.link(ob)
    ob.location = pos; ob.rotation_euler = (0, 0, math.radians(yaw_deg)); ob.scale = (-1.0 if mirror else 1.0, 1.0, 1.0)
    ob.visible_shadow = False; J.no_bounce(ob); ob['placeholder'] = 1
    if shadow:
        sm = _shadow_quad('csh_%.2f' % sw, 1.0, 0.5)
        if not sm.materials: sm.materials.append(_card_mat(_shadow_png(), (1, 1, 1), 0.0, 'shadow'))
        so = bpy.data.objects.new('ph_sh_%s' % name, sm); STATE['SET'].objects.link(so); so.location = (pos[0], pos[1], pos[2]); so.rotation_euler = (0, 0, math.radians(yaw_deg) + math.pi / 2 * 0)
        so.scale = (sw * scale, sw * scale, 1.0); so.visible_shadow = False; J.no_bounce(so); so['placeholder'] = 1
    return ob

# ------------------------------------------------------------------ people
HEIGHT = J.HEIGHT
ROLE_POSE = dict(tiandan=['tiandan_stand'], general=['general_stand'], soldier=['soldier_laugh_point_a', 'soldier_laugh_point_b', 'soldier_laugh_point_c'],
                 townsfolk=['old_man_dig', 'woman_dig', 'old_man_stand', 'woman_stand'], child=['child_stand'], envoy=['envoy_bow'], qi_soldier=['qi_run'], sentry=['soldier_stand_a'],
                 party_crowd=['soldier_cheer_cup_a', 'soldier_cheer_cup_b', 'soldier_cheer_cup_c'])
SHOT_POSE = {
    's01': dict(tiandan=['tiandan_tug_cloth']), 's02': dict(tiandan=['tiandan_tie_blade']), 's05': dict(tiandan=['tiandan_accept_sash'], townsfolk=['old_man_stand', 'woman_stand', 'old_man_stand']),
    's06': dict(tiandan=['tiandan_walk'], townsfolk=['woman_stand', 'old_man_stand', 'woman_stand', 'old_man_stand']),
    's08': dict(general=['general_laugh'], soldier=['soldier_laugh_point_a', 'soldier_laugh_point_b']), 's09': dict(general=['general_arms_wide'], soldier=['soldier_laugh_point_a', 'soldier_laugh_point_b', 'soldier_laugh_point_c']),
    's10': dict(general=['general_boast'], soldier=['soldier_laugh_point_a', 'soldier_laugh_point_b']), 's11': dict(soldier=['soldier_mock_moo_a', 'soldier_mock_moo_b', 'soldier_mock_moo_c'], general=['general_laugh']),
    's12': dict(townsfolk=['old_man_worried', 'woman_worried']), 's14': dict(general=['general_toast'], soldier=['soldier_laugh_point_a', 'soldier_laugh_point_b']),
    's15': dict(general=['general_carve'], soldier=['soldier_laugh_point_a']), 's16': dict(townsfolk=['old_man_dig', 'woman_dig', 'old_man_carry_basket', 'woman_carry_basket'], child=['child_carry_basket']),
    's17': dict(townsfolk=['old_man_stand', 'woman_stand'], tiandan=['tiandan_point']), 's18': dict(tiandan=['tiandan_raise_torch']),
    's21': dict(soldier=['soldier_freeze_a', 'soldier_freeze_b', 'soldier_freeze_c']), 's22': dict(soldier=['soldier_freeze_a']),
    's23': dict(townsfolk=['old_man_beat', 'woman_beat'], child=['child_beat']), 's24': dict(soldier=['soldier_flee_a', 'soldier_flee_b', 'soldier_flee_c']), 's26': dict(general=['general_run']),
}
def _pose(shot, role, i):
    lst = SHOT_POSE.get(shot, {}).get(role) or ROLE_POSE.get(role) or ['tiandan_stand']; return lst[i % len(lst)]

def person_card(shot, role, i, m, camloc, t):
    p = V(m[:3]); pose = _pose(shot, role, i); meta = CD.card('person', pose=pose); h = HEIGHT.get(role, 3.0 if role != 'party_crowd' else 3.2); sc = h / meta['height']
    d = camloc - p; yaw = math.degrees(math.atan2(d.x, -d.y)); tint = None; k = None
    if SILHOUETTE.get((shot, role)): tint = (0.12, 0.12, 0.18); k = 0.9
    if role == 'qi_soldier': tint = (0.35, 0.35, 0.5)
    return put_card(meta, tuple(p), yaw, sc, name='%s%d' % (role, i), tint=tint, k=k, sw=0.9 * h / 3.0)
SILHOUETTE = {}

# ------------------------------------------------------------------ oxen
OXSPEC = dict(default=dict(state='dragon', view='three_quarter', gait='stand', flame=-1, theta=36))
def oxspec(shot, role):
    return dict(OXSPEC['default'], **OXSPEC.get(shot, {}).get(role, OXSPEC.get(shot, {}).get('*', {})))

def ox_card(shot, role, i, m, camloc, spec, travel=None):
    p = V(m[:3]); sc = (m[4] if len(m) > 4 else 1.0) * 1.08; yawm = travel if travel is not None else (m[3] if len(m) > 3 else 0.0)
    dvec = V((math.cos(math.radians(yawm)), math.sin(math.radians(yawm)), 0.0)); c = camloc - p; c.z = 0.0; c.normalize()
    best = None; rr = random.Random(int(abs(p.x * 7) + abs(p.y * 13) + i))
    th0 = spec.get('theta', 36); th = th0 + rr.uniform(-6, 6)
    for sgn in (1, -1):
        a = math.radians(sgn * th); n = V((c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a), 0.0))   # card normal (toward the viewer side)
        u = V((-n.y, n.x, 0.0))                                                                                             # card right as seen from the viewer
        for fac in (1, -1):
            score = (u * fac).dot(dvec)
            if best is None or score > best[0] + 1e-4 or (abs(score - best[0]) <= 1e-4 and rr.random() < 0.5): best = (score, n, u, fac)
    _, n, u, fac = best
    # quad: local +x = card right, faces -y: normal (0,-1,0) rotated by yaw -> (sin yaw, -cos yaw); want normal = n  ->  yaw = atan2(n.x, -n.y)
    yaw = math.degrees(math.atan2(n.x, -n.y))
    ph = (i * 3 + int(abs(p.x))) % 8; fl = spec['flame']
    if fl >= 0: fl = 1 + (i + int(abs(p.y))) % 2 if spec.get('flame_vary') else fl
    if spec.get('lit_fn') is not None: fl = spec['lit_fn'](i, m)
    meta = CD.card('ox', state=spec['state'], view=spec['view'], gait=spec['gait'], phase=ph if spec['gait'] != 'stand' else 0, flame=fl, reed=1 if spec.get('reed') else 0)
    tint = spec.get('tint'); k = spec.get('k')
    return put_card(meta, tuple(p), yaw, sc, mirror=(fac < 0), name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)

# ------------------------------------------------------------------ placeholders (cards at the marks)
def clear_placeholders():
    for ob in [o for o in bpy.data.objects if o.name.startswith('ph_')]: bpy.data.objects.remove(ob, do_unlink=True)

def placeholders(name, t=0.5, herd_max=400):
    clear_placeholders(); sh = S.SHOTS[name]; marks = S.marks_for(name); pose = S.pose_at(sh, t); cam = V(pose['loc']); n = 0
    for role, lst in marks.items():
        if isinstance(lst, str) or role == 'road': continue
        for i, m in enumerate(lst[:herd_max]):
            if role == 'ox' or role.startswith('herd'): ox_card(name, role, i, m, cam, oxspec(name, role))
            elif role in HEIGHT or role in ROLE_POSE: person_card(name, role, i, m, cam, t)
            n += 1
    return n
