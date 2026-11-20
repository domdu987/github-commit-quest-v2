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
SILHOUETTE = {('s21', 'soldier'): 1, ('s22', 'soldier'): 1}

# ------------------------------------------------------------------ oxen
GAL = dict(state='dragon', view='three_quarter', gait='gallop', flame=1)
OXSPEC = dict(default=dict(state='dragon', view='three_quarter', gait='stand', flame=-1, theta=36),
              s02={'*': dict(gait='walk')}, s06={'*': dict(state='plain', gait='walk')},
              s07={'*': dict(state='plain', gait='walk', theta=30, state_fn=lambda i, m: 'dragon' if (i % 3 == 0) else 'plain')},
              s17={'*': dict(reed=True)}, s18={'*': dict(reed=True, lit_fn=lambda i, m: 1 + (i % 2) if i < 3 else -1)},
              s19={'*': dict(GAL)}, s20={'*': dict(GAL)}, s21={'*': dict(GAL, theta=38)}, s22={'*': dict(GAL, theta=34)}, s26={'*': dict(GAL, theta=34)})
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
    ph = (i * 3 + int(abs(p.x))) % 8; fl = spec['flame']; st = spec['state_fn'](i, m) if spec.get('state_fn') else spec['state']
    if fl >= 0: fl = 1 + (i + int(abs(p.y))) % 2 if spec.get('flame_vary') else fl
    if spec.get('lit_fn') is not None: fl = spec['lit_fn'](i, m)
    meta = CD.card('ox', state=st, view=spec['view'], gait=spec['gait'], phase=ph if spec['gait'] != 'stand' else 0, flame=fl, reed=1 if spec.get('reed') else 0)
    tint = spec.get('tint'); k = spec.get('k')
    ob = put_card(meta, tuple(p), yaw, sc, mirror=(fac < 0), name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)
    if fl >= 0: LIT.append((p, u * (-fac), sc))
    return ob
LIT = []

def lit_pools(cam, nlights=6):
    """Warm pool decals under every lit ox + real point lights at the tails of the nearest few (the herd lights its own ground)."""
    M = STATE['M']
    for (p, back, sc) in LIT:
        tail = p + back * (2.7 * sc) + V((0, 0, 2.2 * sc))
        sm = _shadow_quad('cpool', 1.0, 1.0)
        if not sm.materials: sm.materials.append(M['pool_w'])
        ob = bpy.data.objects.new('ph_pool', sm); STATE['SET'].objects.link(ob); ob.location = (tail.x, tail.y, 0.06); ob.scale = (2.3 * sc, 2.3 * sc, 1.0); ob.visible_shadow = False; J.no_bounce(ob); ob['placeholder'] = 1
    near = sorted(LIT, key=lambda a: (a[0] - cam).length)[:nlights]
    for (p, back, sc) in near:
        tail = p + back * (2.7 * sc) + V((0, 0, 2.2 * sc)); d = bpy.data.lights.new('ph_tail', 'POINT'); d.color = J.FIRE; d.energy = 520.0 * sc; d.shadow_soft_size = 0.5; d.use_shadow = False
        lo = bpy.data.objects.new('ph_tail', d); STATE['LIGHTS'].objects.link(lo); lo.location = tail; lo.visible_camera = False; lo['placeholder'] = 1

# ------------------------------------------------------------------ placeholders (cards at the marks)
def clear_placeholders():
    for ob in [o for o in bpy.data.objects if o.name.startswith('ph_')]: bpy.data.objects.remove(ob, do_unlink=True)

def placeholders(name, t=0.5, herd_max=400):
    clear_placeholders(); LIT.clear(); sh = S.SHOTS[name]; marks = S.marks_for(name); pose = S.pose_at(sh, t); cam = V(pose['loc']); n = 0
    for role, lst in marks.items():
        if isinstance(lst, str) or role == 'road': continue
        for i, m in enumerate(lst[:herd_max]):
            if role == 'ox' or role.startswith('herd'): ox_card(name, role, i, m, cam, oxspec(name, role))
            elif role in HEIGHT or role in ROLE_POSE: person_card(name, role, i, m, cam, t)
            n += 1
    lit_pools(cam)
    return n

# ------------------------------------------------------------------ build-time rules (called from jimo.brazier / oil_lamp / wall_dress)
SKIP = {                                                           # shot -> [(x, y, r)] circles where no fire bowl / lamp is built (kept out of the lens / the diggers)
    's16': [(44.0, 9.5, 2.0), (30.0, 9.0, 2.0), (14.0, 9.5, 2.0)],
    's23': [(-33.0, -2.0, 9.5)],
}
BSKIP = {'s13': [(0.0, -54.0, 19.0), (14.0, -62.0, 30.0)], 's24': [(-20.0, -60.0, 70.0)]}          # pennant poles near the lens (cut objects at the frame edge)
def bskipped(p):
    return any(math.hypot(p[0] - x, p[1] - y) < r for (x, y, r) in BSKIP.get(STATE.get('preset'), ()))
WARM_K = {'s21': 0.3, 's22': 0.3}                                  # dusk-free night: Jimo wall lamps dimmed so the herd comes out of the dark

def skipped(p):
    for (x, y, r) in SKIP.get(STATE.get('preset'), ()):
        if math.hypot(p[0] - x, p[1] - y) < r: return True
    return False

def warmk(): return WARM_K.get(STATE.get('preset'), 1.0)

# ------------------------------------------------------------------ per-shot tweaks after the build
def post_build(preset, location, light):
    fn = POST.get(preset)
    if fn: fn(preset)
    if preset in WARM_K: dim_wall_lights(WARM_K[preset])

def dim_wall_lights(k, ymin=-30.0):
    """Jimo wall / gate / bridge lamps to k: lights and flames with y > ymin (the camp stays), halo faces and pools of the wall removed."""
    for fi in STATE.get('fires', ()):
        ob = fi['ob']
        if ob.location.y > ymin:
            fi['E0'] = fi['E0'] * k; fi['k'] = fi.get('k', 1.0) * (0.55 if k < 1 else 1.0)
    for lo in STATE['LIGHTS'].objects:
        if lo.type == 'LIGHT' and lo.data.type == 'POINT' and lo.location.y > ymin and lo.location.y < 40: lo.data.energy *= k
    ob = STATE['objects']
    for nm in ('wallpools', 'tw_glow'):
        if nm in ob: ob[nm].hide_render = True
    h = ob.get('halos')
    if h is not None:
        import bmesh
        bm = bmesh.new(); bm.from_mesh(h.data); mw = h.matrix_world
        dl = [f for f in bm.faces if (mw @ f.calc_center_median()).y > ymin]
        bmesh.ops.delete(bm, geom=dl, context='FACES'); bm.to_mesh(h.data); bm.free()

def _rout_big(preset):
    for it in STATE.get('rout_items', ()):
        if it.get('ob') is not None: it['ob'].scale = (2.6, 2.6, 2.6)
POST = {'s24': _rout_big}

# ------------------------------------------------------------------ ground dressing (round 2)
DRESS_MAP = dict(stone='stone', hay='hay', silk='sack', rope='rope', basket='basket', pot='jar', plume='helmet', wheel='cart')      # old r2 kinds -> jimo_dress.LIB kinds (no flat strips, no blades)
def dress(x0, x1, y0, y1, n, seed, kinds=('stone', 'hay', 'silk', 'rope', 'basket', 'pot'), z=0.0, avoid=None, k=1.0):
    """Props scattered over a ground rectangle so bare ground is broken up. Since round 3 they are the warm, rounded, textured jimo_dress props (named dgr_*, one object each), about 40 %
    of the old count, kept 2.5 D away from the shot's stand marks; J.dress_ground() later removes any of them that would overlap an actor card or sit within 3 D of the lens."""
    import jimo_dress as DG; r = random.Random(seed); kc = DG.default_keep_clear() if STATE.get('preset') in S.SHOTS else []
    for i in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1); kind = DRESS_MAP.get(r.choice(kinds), 'stone'); keep = r.random() < DG.DENSITY0
        if not keep or (avoid and avoid(x, y)) or any(math.hypot(x - cx, y - cy) < cr + 1.0 for (cx, cy, cr) in kc): continue
        DG.place_prop(kind, x, y, seed * 1000 + i, z=z)

def furrows(x0, x1, y0, y1, step=1.1, seed=1, along='y', mat='tunnel'):
    """Dark furrow strips on a field (a thin quad per row): breaks the flat plane."""
    M = STATE['M']; r = random.Random(seed); Bk = J.Banks(); b = Bk('furrows', shadow=False); n0 = set(STATE['SET'].objects)
    x = x0
    while x < x1:
        w = r.uniform(0.18, 0.32); J.flat(b, V((x, y0, 0.05)), V((w, 0, 0)), V((0, y1 - y0, 0)), M[mat]); x += step * r.uniform(0.85, 1.2)
    Bk.flush(STATE['SET'])
    for ob in STATE['SET'].objects:
        if ob not in n0: J.no_bounce(ob)

def stake(x, y, h=3.0, light=0.0):
    M = STATE['M']; Bk = J.Banks(); b = Bk('stk', hull=0.0); n0 = set(STATE['SET'].objects)
    J.rod(b, V((x, y, 0)), V((x, y, h)), 0.14, M['wood_d'], seg=5); J.cyl(b, V((x, y, h)), 0.35, 0.3, M['iron'], seg=7, r1=0.45)
    J.live_flame(V((x, y, h + 0.3)), 1.4, 0.4, seed=int(x * 7 + y), n=3, light=light, name='stk%d' % int(abs(x * 3 + y)), warm=None)
    Bk.flush(STATE['SET'])
    for ob in STATE['SET'].objects:
        if ob not in n0: J.no_bounce(ob)

def _s02(p): dress(-38, -14, 7.0, 13.8, 16, 2, kinds=('silk', 'rope', 'hay', 'silk'), avoid=lambda x, y: abs(y - 10.6) < 1.0 and x > -22)
def _s19(p):
    furrows(-5, 50, -62, -34, 1.2, 4); dress(-6, 50, -62, -34, 40, 5, kinds=('stone', 'hay', 'stone', 'basket', 'rope')); stake(8.0, -36.0); stake(36.0, -44.0)
    if 'streaks' in STATE['objects']: STATE['objects']['streaks'].hide_render = True
def _s20(p):
    furrows(-25, 45, -120, -46, 1.3, 6); dress(-25, 45, -116, -48, 55, 7, kinds=('stone', 'hay', 'stone', 'basket', 'rope', 'pot')); stake(31.0, -70.0); stake(-10.0, -78.0); stake(34.0, -100.0)
    for ob in STATE['SET'].objects:
        if ob.name == 'streaks': ob.hide_render = True
def _s26(p):
    furrows(-10, 10, -100, -58, 1.0, 9, mat='bank'); dress(-9.5, 9.5, -100, -60, 22, 11, kinds=('plume', 'pot', 'hay', 'silk', 'stone', 'rope', 'wheel'), avoid=lambda x, y: abs(x) < 0.0)
    stake(-9.0, -66.0, 3.0); stake(-9.0, -84.0, 3.0); stake(9.0, -78.0, 3.0)
POST.update({'s02': _s02, 's19': _s19, 's20': _s20, 's26': _s26})

def _hide(*names):
    def f(p):
        for n in names:
            if n in STATE['objects']: STATE['objects'][n].hide_render = True
    return f
for _s in ('s09', 's10', 's14', 's15'): POST[_s] = _hide('scatter_x')
POST['s08'] = _hide('cloth')
