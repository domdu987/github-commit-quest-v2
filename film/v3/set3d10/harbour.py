#!/usr/bin/env python3
"""harbour.py : set of film 10 ("ไอ้ช่างม้าลาย", dazzle camouflage, WWI Britain 1917) as a real 3D Blender set (bpy 5.x, Cycles CPU).
Two locations, built by preset (the preset picks the location, default light, camera and set state):

    import harbour as H
    A = H.build('harbour', 'hull_side', light='DAY')     # harbour: harbour_wide | hull_side | quay_low | hull_plank      (DAY | DUSK)
    A = H.build('sea', 'topdown_sea')                    # sea: convoy_wide | periscope_close | periscope_pov | topdown_sea
                                                         #      torpedo_chase | bridge_deck                               (SEA_DAY)
    cam = H.make_camera(A['cam'])                        # use THIS make_camera (far clip, periscope overlay follow)
    H.set_stripes(2)                 # the berth ship: 0 grey .. 1 zigzag .. 2 + staircase .. 3 full dazzle (fractions paint stern -> bow)
    H.set_harbour_dazzle(1.0)        # the moored / roads ships turn dazzle one by one (0..1)
    H.set_convoy(s, frame=n)         # sea: s seconds of convoy sailing (+x, 4 D/s); the ghost sails the other way
    H.set_torpedo(u, frame=n); H.set_ghost(k); H.set_lead_marker(k); H.set_aim_lines(true_k, ghost_k)
    H.set_uboat(dive, frame=n); H.set_hit(t, frame=n); H.set_smoke(k, frame=n); H.periscope_overlay(on)

World: 1 unit = 1 D (head), Z up. HARBOUR: quay top z 0 (x -130..150, quay edge y 0, the land at y < 0), water z -2.4; the berth
ship lies along the quay (bow +x, centre y 6.9); warehouses y -26..-44; the basin y > 0, a breakwater at y 104 with the lighthouse at
its end (150, 104). SEA: water z 0 (animated swell), the convoy sails +x. NO depth of field anywhere. Built on v3/set3d9/wall.py (+
its templates tower / mine / bakery / pagoda / desert): helpers are imported, not copied. See API.md.
CLI: python3 harbour.py stills | final [spec ...] | digest <preset>     spec = preset[:LIGHT[:state[:cam]]]"""
import os, sys, math, json, time, random
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'),
          os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import desert as D                                         # noqa: E402
import wall as W9                                          # noqa: E402  (film-9 set: air / beams compositor, cartoon billows, keys)
import harbour_tex as HX                                   # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, catenary, chain_rod, _obj, _untoon, _glossy   # noqa: E402,F401
WORK = os.path.join(HERE, 'harbour_work')
STATE = T.STATE
digest = G.digest; Frame = BK.Frame; _halo = BK._halo
set_flames = D.set_flames; _keyval = D._keyval; _keyp = W9._keyp

def _rnd(seed): return random.Random(seed)
FIRE = (1.0, 0.58, 0.26); LAMP = (1.0, 0.66, 0.36)
WZ = -2.4                                      # harbour water level (quay top z 0)
SEA_V = 2.5                                    # convoy speed, D / s
T_RUN = 10.0                                   # torpedo run time to the course line, s
PERI_R = 0.13

# ----------------------------------------------------------------------------- light presets
_kdaz = W9._kdaz
_B = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.6, wet=0.0, lamps=1.0, refl_k=0.75)
LIGHTS = dict(
    DAY=dict(_B, key=(1.95, 1.42, 0.82), key_dir=_kdaz(235, 32), sun_elev=32, shade=(0.105, 0.10, 0.31), shade_tint=(0.10, 0.095, 0.33), shade_mix=0.55,
             grade_offset=(-0.006, -0.01, -0.014), lift=(0.008, 0.008, 0.02), sky='DAY', sky_k=0.95, pano='HARB_DAY', pano_k=0.95, grade_saturation=1.2,
             lamps=0.0, bounce=(1.0, 0.62, 0.34, 0.26), beams=0.05, air=('#f2c88c', 0.34, 40.0, 420.0), smoke_rgb=(0.62, 0.6, 0.62), water='#3a5292'),
    DUSK=dict(_B, key=(1.85, 1.0, 0.52), key_dir=_kdaz(300, 10), sun_elev=10, sun_angle=0.8, shade=(0.095, 0.105, 0.35), shade_tint=(0.088, 0.1, 0.39), shade_mix=0.8,
              grade_offset=(-0.006, -0.008, -0.004), lift=(0.014, 0.01, 0.03), sky='DUSK', sky_k=1.0, pano='HARB_DUSK', pano_k=0.95, grade_saturation=1.12,
              lamps=1.0, bounce=(1.0, 0.55, 0.3, 0.2), beams=0.035, air=('#f0a070', 0.3, 40.0, 420.0), smoke_rgb=(0.48, 0.38, 0.42), water='#2e3c78'),
    SEA_DAY=dict(_B, key=(1.95, 1.34, 0.74), key_dir=_kdaz(250, 18), sun_elev=18, sun_angle=0.6, shade=(0.105, 0.098, 0.31), shade_tint=(0.102, 0.09, 0.335), shade_mix=0.6,
                 grade_offset=(-0.006, -0.009, -0.012), lift=(0.008, 0.008, 0.02), sky='SEA_DAY', sky_k=0.95, pano=None, grade_saturation=1.18,
                 lamps=0.3, bounce=(1.0, 0.62, 0.36, 0.22), beams=0.05, air=('#f0c898', 0.42, 90.0, 1500.0), smoke_rgb=(0.5, 0.48, 0.52), water='#2f8e98', water_far='#2c5592', refl_k=0.22, sea_warm=0.2),
)
LIGHT_KEYS = list(LIGHTS)
LOC_LIGHTS = dict(harbour=['DAY', 'DUSK'], sea=['SEA_DAY'])

PRESETS = dict(
    harbour_wide=dict(loc='harbour', light='DAY', cam='harbour_wide', stripes=1.0),
    hull_side=dict(loc='harbour', light='DAY', cam='hull_side', stripes=1.0),
    quay_low=dict(loc='harbour', light='DAY', cam='quay_low', stripes=0.6),
    hull_plank=dict(loc='harbour', light='DAY', cam='hull_plank', stripes=0.47),
    beauty_harbour=dict(loc='harbour', light='DUSK', cam='beauty_harbour', stripes=3.0, state='hd0.5'),
    convoy_wide=dict(loc='sea', light='SEA_DAY', cam='convoy_wide', state='dive1'),
    periscope_close=dict(loc='sea', light='SEA_DAY', cam='periscope_close', state=''),
    periscope_pov=dict(loc='sea', light='SEA_DAY', cam='periscope_pov', state='dive1,pov1'),
    topdown_sea=dict(loc='sea', light='SEA_DAY', cam='topdown_sea', state='dive1,peri0,lead1'),
    torpedo_chase=dict(loc='sea', light='SEA_DAY', cam='torpedo_chase', state='dive1,peri0,s3.5'),
    bridge_deck=dict(loc='sea', light='SEA_DAY', cam='bridge_deck', state=''),
    beauty_sea=dict(loc='sea', light='SEA_DAY', cam='beauty_sea', state='dive1,peri0'),
)
LOC_PRESETS = dict(harbour=[k for k, v in PRESETS.items() if v['loc'] == 'harbour'], sea=[k for k, v in PRESETS.items() if v['loc'] == 'sea'])

# ----------------------------------------------------------------------------- build
def build(location=None, preset=None, clear=True, dress=True, light=None):
    """Build a location for a preset (LOC_PRESETS) into the current scene: its light (light= overrides: harbour DAY | DUSK, sea
    SEA_DAY), world, render settings, grade, denoiser and the preset's set state. Returns the anchors dict (API.md); A['cam'] is the
    preset camera (build it with harbour.make_camera)."""
    preset = preset or ('harbour_wide' if location in (None, 'harbour') else 'convoy_wide')
    assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; location = PR['loc']; lkey = light or PR['light']
    assert lkey in LOC_LIGHTS[location], 'light %s: %s has %s' % (lkey, location, LOC_LIGHTS[location])
    scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location; STATE['area'] = location; STATE['light'] = lkey
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_pov_follow', '_sun_screen', '_cards_face'): h.remove(f)
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('HB_'): bpy.data.node_groups.remove(ng)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('HB_', 'ink')): bpy.data.materials.remove(m)
    tx = HX.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_harbour') or bpy.data.worlds.new('W_harbour'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'HB_%s_%s_' % (location, lkey); FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, glow=None, glow_k=0.0):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s_%g' % (pre, name, gain, _k(sm), form, alpha, smix, glow_k), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                               alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    STATE.update(C=C, TX=TX, pre=pre)
    M = _materials(P, C, TX, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    if P.get('bounce'):
        br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
        d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
        o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    STATE.update(flames=[], flame_mats=list(M['_flame_mats']), marks={}, ships={}, smoke=[], gulls=[])
    if location == 'harbour': _harbour(SET, P, M, dress)
    else: _sea(SET, P, M, dress)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    setup_grade(scene)
    W9._air_comp(scene, P)
    W9._billow_round(SET)
    for ob in SET.objects:
        no_bounce(ob)
        if location == 'harbour' and ob.name.startswith(('hull_', 'quay', 'warehouses', 'cranes', 'lighthouse', 'scaffold', 'tug', 'flag_', 'bgcard_')): ob.visible_glossy = True
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        if _cards_face not in h: h.append(_cards_face)
    set_flames(1.0)
    apply_preset_state(preset)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """= mine.setup_render: final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light, OIDN; transparent bounces 24."""
    MN.setup_render(scene, quality); scene.cycles.transparent_max_bounces = 24
    if STATE.get('loc') == 'harbour': scene.cycles.glossy_bounces = 1          # the calm harbour water mirrors ships and quay

def apply_dof(*a, **k):
    """Client rule: no depth of field at all (kept for API symmetry)."""
    return None

def make_camera(setup, name='cam', scene=None):
    """tower.make_camera (loc / look_at / lens / up / roll) + far clip 6000 (sea horizon); the periscope overlay follows it."""
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 6000.0; ob.data.dof.use_dof = False
    _pov_follow(bpy.context.scene); _cards_face(bpy.context.scene); return ob

# ============================================================================= materials
def _tex_node(m): return [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]

def _mat_paint(name, P, tx, base, layers, L, stage=0.0):
    """Ship paint, projected from the side in ship space (Object coords: u = x / L + 0.5, v = (z - ZP0) / (ZP1 - ZP0); faces turned
    toward +-x take y instead of x). Value 'stage': each layer (image, k) shows where its alpha is, and once stage > k - 1 it is
    revealed from the stern (u 0) toward the bow (u 1): fully at stage >= k."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, image=tx[base], form=tuple(P['form']))); nt = m.node_tree; N = nt.nodes.new; L_ = nt.links.new
    tex = _tex_node(m); tex.extension = 'EXTEND'; links0 = list(tex.outputs['Color'].links)
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L_(tc.outputs['Object'], sp.inputs[0])
    geo = N('ShaderNodeNewGeometry'); sn = N('ShaderNodeSeparateXYZ'); L_(geo.outputs['Normal'], sn.inputs[0])
    ab = N('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L_(sn.outputs['X'], ab.inputs[0])
    gk = N('ShaderNodeMath'); gk.operation = 'GREATER_THAN'; gk.inputs[1].default_value = 0.86; L_(ab.outputs[0], gk.inputs[0])
    ux = N('ShaderNodeMix'); ux.data_type = 'FLOAT'; L_(gk.outputs[0], ux.inputs[0]); L_(sp.outputs['X'], ux.inputs[2]); L_(sp.outputs['Y'], ux.inputs[3])
    u = N('ShaderNodeMath'); u.operation = 'MULTIPLY_ADD'; u.inputs[1].default_value = 1.0 / L; u.inputs[2].default_value = 0.5; L_(ux.outputs[0], u.inputs[0])
    v = N('ShaderNodeMath'); v.operation = 'MULTIPLY_ADD'; v.inputs[1].default_value = 1.0 / (HX.ZP1 - HX.ZP0); v.inputs[2].default_value = -HX.ZP0 / (HX.ZP1 - HX.ZP0); L_(sp.outputs['Z'], v.inputs[0])
    cb = N('ShaderNodeCombineXYZ'); L_(u.outputs[0], cb.inputs[0]); L_(v.outputs[0], cb.inputs[1]); L_(cb.outputs[0], tex.inputs['Vector'])
    st = D._value(nt, 'stage', stage); last = tex.outputs['Color']
    for img, k in layers:
        t2 = N('ShaderNodeTexImage'); t2.image = T._img(tx[img]); t2.extension = 'EXTEND'; L_(cb.outputs[0], t2.inputs['Vector'])
        vk = N('ShaderNodeMath'); vk.operation = 'SUBTRACT'; vk.use_clamp = True; vk.inputs[1].default_value = k - 1.0; L_(st.outputs[0], vk.inputs[0])
        vm = N('ShaderNodeMath'); vm.operation = 'MULTIPLY'; vm.inputs[1].default_value = 1.02; L_(vk.outputs[0], vm.inputs[0])
        gt = N('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; L_(vm.outputs[0], gt.inputs[0]); L_(u.outputs[0], gt.inputs[1])
        fa = N('ShaderNodeMath'); fa.operation = 'MULTIPLY'; L_(t2.outputs['Alpha'], fa.inputs[0]); L_(gt.outputs[0], fa.inputs[1])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L_(fa.outputs[0], mx.inputs[0]); L_(last, mx.inputs[6]); L_(t2.outputs['Color'], mx.inputs[7]); last = mx.outputs[2]
    pl = N('ShaderNodeTexImage'); pl.image = T._img(tx['plates']); pl.extension = 'REPEAT'
    px = N('ShaderNodeMath'); px.operation = 'MULTIPLY'; px.inputs[1].default_value = 0.25; L_(ux.outputs[0], px.inputs[0])
    cb2 = N('ShaderNodeCombineXYZ'); L_(px.outputs[0], cb2.inputs[0]); L_(v.outputs[0], cb2.inputs[1]); L_(cb2.outputs[0], pl.inputs['Vector'])
    mp = N('ShaderNodeMix'); mp.data_type = 'RGBA'; mp.blend_type = 'MULTIPLY'; mp.inputs[0].default_value = 1.0; L_(last, mp.inputs[6]); L_(pl.outputs['Color'], mp.inputs[7]); last = mp.outputs[2]
    for l in links0: to = l.to_socket; nt.links.remove(l); L_(last, to)
    return m

def _mat_sea(name, P, base, ripple=0.0, refl=None):
    """Sea: faceted lit water (Lambert on the swell facets: they catch the low sun) + the painted sky mirrored along the reflected
    view ray x a Fresnel term x refl_k + a warm GGX glint lobe for the key (sparkle on the facets). ripple adds a noise normal (flat
    harbour water)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, base, form=None, gain=1.25)); tx = STATE['tx']; rk = P.get('refl_k', 0.7) if refl is None else refl
    nt = m.node_tree; bumpN = None
    if STATE.get('loc') == 'sea':                              # small chop / ripple detail: a noise bump on every shading normal
        tcb = nt.nodes.new('ShaderNodeTexCoord'); nzb = nt.nodes.new('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 1.4; nzb.inputs['Detail'].default_value = 0.0
        nt.links.new(tcb.outputs['Object'], nzb.inputs['Vector']); bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.22; bp.inputs['Distance'].default_value = 0.2
        nt.links.new(nzb.outputs['Fac'], bp.inputs['Height']); bumpN = bp.outputs['Normal']
        dif = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfDiffuse'][0]; nt.links.new(bumpN, dif.inputs['Normal'])
    STATE['sea_bumpN'] = bumpN
    if P.get('water_far') and STATE.get('loc') == 'sea':      # turquoise-teal near the camera -> deeper blue far off (view distance)
        nt = m.node_tree; rgb = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeRGB'][0]; links0 = list(rgb.outputs[0].links)
        cd = nt.nodes.new('ShaderNodeCameraData'); mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 40.0; mr.inputs['From Max'].default_value = 420.0
        nt.links.new(cd.outputs['View Distance'], mr.inputs['Value'])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; nt.links.new(mr.outputs['Result'], mx.inputs[0]); nt.links.new(rgb.outputs[0], mx.inputs[6]); mx.inputs[7].default_value = (*T.hex_lin(P['water_far']), 1)
        art = mx.outputs[2]
        # whitecap flecks on the crests: swell height (world z) x a spotty noise -> soft white foam in the albedo
        gp = nt.nodes.new('ShaderNodeNewGeometry'); spz = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(gp.outputs['Position'], spz.inputs[0])
        cr = nt.nodes.new('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.34; cr.inputs['From Max'].default_value = 0.56; nt.links.new(spz.outputs['Z'], cr.inputs['Value'])
        tcw = nt.nodes.new('ShaderNodeTexCoord'); nzw = nt.nodes.new('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 0.9; nzw.inputs['Detail'].default_value = 0.0; nt.links.new(tcw.outputs['Object'], nzw.inputs['Vector'])
        sp2 = nt.nodes.new('ShaderNodeMapRange'); sp2.inputs['From Min'].default_value = 0.5; sp2.inputs['From Max'].default_value = 0.62; nt.links.new(nzw.outputs['Fac'], sp2.inputs['Value'])
        wc = nt.nodes.new('ShaderNodeMath'); wc.operation = 'MULTIPLY'; wc.use_clamp = True; nt.links.new(cr.outputs['Result'], wc.inputs[0]); nt.links.new(sp2.outputs['Result'], wc.inputs[1])
        mw = nt.nodes.new('ShaderNodeMix'); mw.data_type = 'RGBA'; nt.links.new(wc.outputs[0], mw.inputs[0]); nt.links.new(art, mw.inputs[6]); mw.inputs[7].default_value = (0.86, 0.92, 0.9, 1)
        for l in links0: to = l.to_socket; nt.links.remove(l); nt.links.new(mw.outputs[2], to)
    def make(nt):
        N = nt.nodes.new; L = nt.links.new
        geo = N('ShaderNodeNewGeometry'); neg = N('ShaderNodeVectorMath'); neg.operation = 'SCALE'; neg.inputs['Scale'].default_value = -1.0; L(geo.outputs['Incoming'], neg.inputs[0])
        nrm = geo.outputs['Normal']
        if ripple > 0:
            tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], nz.inputs['Vector'])
            sub = N('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5); L(nz.outputs['Color'], sub.inputs[0])
            sc = N('ShaderNodeVectorMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = (ripple, ripple, 0.0); L(sub.outputs[0], sc.inputs[0])
            nn = N('ShaderNodeVectorMath'); nn.operation = 'ADD'; L(sc.outputs[0], nn.inputs[0]); L(nrm, nn.inputs[1])
            nm = N('ShaderNodeVectorMath'); nm.operation = 'NORMALIZE'; L(nn.outputs[0], nm.inputs[0]); nrm = nm.outputs[0]
        if STATE.get('sea_bumpN') is not None: nrm = STATE['sea_bumpN']
        rf = N('ShaderNodeVectorMath'); rf.operation = 'REFLECT'; L(neg.outputs[0], rf.inputs[0]); L(nrm, rf.inputs[1])
        t = D._sky_lookup(nt, tx['sky_' + P['sky']], rf.outputs[0])
        fr = N('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = 0.3
        f2 = N('ShaderNodeMath'); f2.operation = 'MULTIPLY_ADD'; f2.inputs[1].default_value = 1.0; f2.inputs[2].default_value = 0.08; L(fr.outputs['Fresnel'], f2.inputs[0])
        k2 = N('ShaderNodeMath'); k2.operation = 'MULTIPLY'; k2.inputs[1].default_value = rk; L(f2.outputs[0], k2.inputs[0])
        em = N('ShaderNodeEmission'); L(k2.outputs[0], em.inputs['Strength'])
        if STATE.get('loc') == 'sea':                          # mostly a flat pale-sky tint: lighter at grazing angles, no soft cloud blobs
            fm = N('ShaderNodeMix'); fm.data_type = 'RGBA'; fm.inputs[0].default_value = 0.7; L(t.outputs['Color'], fm.inputs[6]); fm.inputs[7].default_value = (0.62, 0.78, 0.84, 1)
            L(fm.outputs[2], em.inputs['Color'])
        else: L(t.outputs['Color'], em.inputs['Color'])
        out = em.outputs['Emission']
        wk = P.get('sea_warm', 0.0)
        if wk > 0:                              # warm peach light on the swell faces turned to the low sun (troughs stay blue-violet)
            kd = Vector(P['key_dir']).normalized(); dp = N('ShaderNodeVectorMath'); dp.operation = 'DOT_PRODUCT'; dp.inputs[1].default_value = tuple(-kd); L(geo.outputs['Normal'], dp.inputs[0])
            sm = N('ShaderNodeMapRange'); sm.interpolation_type = 'SMOOTHSTEP'; sm.inputs['From Min'].default_value = math.sin(math.radians(P['sun_elev'])) + 0.07
            sm.inputs['From Max'].default_value = math.sin(math.radians(P['sun_elev'])) + 0.095; L(dp.outputs['Value'], sm.inputs['Value'])   # crisp cel band, no soft wash
            km = N('ShaderNodeMath'); km.operation = 'MULTIPLY'; km.inputs[1].default_value = wk; L(sm.outputs['Result'], km.inputs[0])
            ew = N('ShaderNodeEmission'); ew.inputs['Color'].default_value = (1.0, 0.72, 0.42, 1); L(km.outputs[0], ew.inputs['Strength'])
            ad = N('ShaderNodeAddShader'); L(out, ad.inputs[0]); L(ew.outputs[0], ad.inputs[1]); out = ad.outputs[0]
        return out
    MN._append_shader(m, make)
    if STATE.get('loc') == 'sea':
        _glossy(m, (1.0, 0.8, 0.5), 1.8, 0.1)                                   # sharp warm glitter on the bumped facets
        gl = [n for n in m.node_tree.nodes if n.bl_idname in ('ShaderNodeBsdfGlossy', 'ShaderNodeBsdfAnisotropic')][-1]; m.node_tree.links.new(STATE['sea_bumpN'], gl.inputs['Normal'])
    else:
        _glossy(m, (0.7, 0.74, 0.78), 0.55, 0.06)                               # harbour: a calm mirror that reflects ships and quay (glossy bounce)
    return m

def _mat_ghost(name):
    """The ghost ship: pale cyan, emissive, translucent (camera only, casts no shadow); a brighter rim; Value 'gk' = opacity 0..1."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.4
    gk = D._value(nt, 'gk', 1.0)
    D._value(nt, 'op', 1.0)                                                      # (unused: lets the ghost smoke share _billows)
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY_ADD'; a.inputs[1].default_value = 0.3; a.inputs[2].default_value = 0.34; L(lw.outputs['Fresnel'], a.inputs[0])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; a2.use_clamp = True; L(a.outputs[0], a2.inputs[0]); L(gk.outputs[0], a2.inputs[1])
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; L(lw.outputs['Fresnel'], cm.inputs[0]); cm.inputs[6].default_value = (0.42, 0.86, 1.0, 1); cm.inputs[7].default_value = (0.85, 1.0, 1.0, 1)
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = 0.95; L(cm.outputs[2], em.inputs['Color'])
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(a2.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx2 = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2]); L(mx2.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_ghost_rim(name):
    """Emissive pale-cyan silhouette line of the ghost (inverted hull: back faces only, camera rays only); Value 'gk' = opacity."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); lp = N('ShaderNodeLightPath'); gk = D._value(nt, 'gk', 1.0)
    f = N('ShaderNodeMath'); f.operation = 'MULTIPLY'; L(geo.outputs['Backfacing'], f.inputs[0]); L(lp.outputs['Is Camera Ray'], f.inputs[1])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5                      # only near the silhouette (grazing faces)
    ed = N('ShaderNodeMapRange'); ed.interpolation_type = 'SMOOTHSTEP'; ed.inputs['From Min'].default_value = 0.6; ed.inputs['From Max'].default_value = 0.85; L(lw.outputs['Facing'], ed.inputs['Value'])
    f1 = N('ShaderNodeMath'); f1.operation = 'MULTIPLY'; L(f.outputs[0], f1.inputs[0]); L(ed.outputs['Result'], f1.inputs[1])
    f2 = N('ShaderNodeMath'); f2.operation = 'MULTIPLY'; L(f1.outputs[0], f2.inputs[0]); L(gk.outputs[0], f2.inputs[1])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.7, 0.98, 1.0, 1); em.inputs['Strength'].default_value = 2.4
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(f2.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _mat_ghost_foam(name, image):
    """The ghost's own foam: pale-cyan emission x the foam image alpha x 'gk' (camera only)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx_ = N('ShaderNodeTexImage'); tx_.image = T._img(image); gk = D._value(nt, 'gk', 1.0); lp = N('ShaderNodeLightPath')
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY'; L(tx_.outputs['Alpha'], a.inputs[0]); L(gk.outputs[0], a.inputs[1])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; L(a.outputs[0], a2.inputs[0]); L(lp.outputs['Is Camera Ray'], a2.inputs[1])
    a3 = N('ShaderNodeMath'); a3.operation = 'MULTIPLY'; a3.inputs[1].default_value = 0.85; L(a2.outputs[0], a3.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.72, 0.97, 1.0, 1); em.inputs['Strength'].default_value = 1.1
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(a3.outputs[0], mx.inputs['Fac']); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _mat_wake(name, P, image, k=1.0):
    """Lit white foam with alpha from a foam image, Values 'head' / 'tail' / 'wk' (u along the wake): shows where u < head, fading
    out over `tail` behind it, x wk."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, image=STATE['tx'][image], alpha=True, form=None, gain=1.0, shade_mul=(1.3, 1.3, 1.25), glow=STATE['tx'][image], glow_k=0.55)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); l = tex.outputs['Alpha'].links[0]; to = l.to_socket; nt.links.remove(l)
    uv = N('ShaderNodeUVMap'); sp = N('ShaderNodeSeparateXYZ'); L(uv.outputs['UV'], sp.inputs[0])
    hd = D._value(nt, 'head', 1.0); tl = D._value(nt, 'tail', 2.0); wk = D._value(nt, 'wk', k)
    dd = N('ShaderNodeMath'); dd.operation = 'SUBTRACT'; L(hd.outputs[0], dd.inputs[0]); L(sp.outputs['X'], dd.inputs[1])
    g = N('ShaderNodeMath'); g.operation = 'GREATER_THAN'; g.inputs[1].default_value = 0.0; L(dd.outputs[0], g.inputs[0])
    fd = N('ShaderNodeMath'); fd.operation = 'DIVIDE'; L(dd.outputs[0], fd.inputs[0]); L(tl.outputs[0], fd.inputs[1])
    f1 = N('ShaderNodeMath'); f1.operation = 'SUBTRACT'; f1.use_clamp = True; f1.inputs[0].default_value = 1.0; L(fd.outputs[0], f1.inputs[1])
    a1 = N('ShaderNodeMath'); a1.operation = 'MULTIPLY'; L(tex.outputs['Alpha'], a1.inputs[0]); L(g.outputs[0], a1.inputs[1])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; L(a1.outputs[0], a2.inputs[0]); L(f1.outputs[0], a2.inputs[1])
    a3 = N('ShaderNodeMath'); a3.operation = 'MULTIPLY'; a3.use_clamp = True; L(a2.outputs[0], a3.inputs[0]); L(wk.outputs[0], a3.inputs[1]); L(a3.outputs[0], to)
    return m

def _mat_black(name, rgb=(0.004, 0.005, 0.007)):
    """Pure flat black for the periscope vignette and crosshair (unlit, camera only)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = 1.0; nt.links.new(em.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _materials(P, C, TX, tx, pre):
    lk = P.get('lamps', 1.0)
    M = dict(setts=TX('setts', form=False), kerb=TX('kerb'), slate=TX('slate'), planks=TX('planks'), deck=TX('deck', form=False), crate=TX('crate'), steel=TX('steel', form=False),
             brick=TX('brick_bay', glow='glow_bay', glow_k=1.6 * lk), brick_b=TX('brick_bay_b', glow='glow_bay', glow_k=1.3 * lk), brick_side=TX('brick_side'),
             wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b8925e'), rope=C('#c8a868'), iron=_glossy(C('#2e3036', 1.0, 1.1), (1.0, 0.85, 0.7), 0.3, 0.3),
             rust=C('#7a4a32'), dark=C('#1a1a1e', 1.0, 0.5, form=False), white=C('#ece8de'), red=C('#b02a22', 1.0, (1.4, 0.8, 0.7), smix=0.25), red_d=C('#7a2420', 1.0, (1.4, 0.8, 0.7), smix=0.25),
             cream=C('#e6d8b8'), green=C('#3e5a3a'), stone=C('#a8a296'), stone_d=C('#7e7a72'), canvas=C('#c8b48a'), tarp=C('#5a5e3e'), coal=C('#26262a', 1.0, 0.8),
             black_p=_glossy(C('#141416'), (1.0, 0.9, 0.8), 0.4, 0.15), white_p=_glossy(C('#f2f2ec'), (1.0, 0.95, 0.9), 0.3, 0.15), grey_p=_glossy(C('#8a9098'), (1.0, 0.95, 0.9), 0.3, 0.15),
             bucket=C('#6e7276'), brass=_glossy(C('#b08a3a', 1.0, (2.0, 1.4, 0.6), smix=0.2), (1.0, 0.8, 0.5), 0.5, 0.25), gull=C('#f4f2ee', 1.0, 1.2), gull_g=C('#9aa0a8'),
             gull_y=C('#e8b030'), lh_white=C('#f0ece4'), lh_red=C('#b8302a', 1.0, (1.4, 0.8, 0.7), smix=0.25), sub=C('#4a5250', 1.0, 1.0), sub_d=C('#33393a'),
             ship_grey=C('#8b9299'), ship_dgrey=C('#5a6068'), funnel_top=C('#1c1d20', 1.0, 0.6), window=C('#22262e', 1.0, 0.6, form=False), boat=C('#d8d2c2'),
             ensign=TX('flag_ensign', form=False, smix=0.3), pennant=TX('flag_red', form=False, smix=0.3), torp=_glossy(C('#26282c', 1.0, 0.7), (1.0, 0.8, 0.55), 0.8, 0.18), torp_nose=mat_emit(pre + 'e_torpnose', '#ffc070', strength=4.0),
             paint_b=C('#101012', 1.0, 0.5), paint_w=C('#f6f6f0'), paint_g=C('#7e858c'),
             lamp_glass=mat_emit(pre + 'e_lampglass', '#ffd890', strength=3.2 * max(0.15, lk)), win_glow=mat_emit(pre + 'e_win', '#ffb060', strength=1.4 * lk),
             lh_lamp=mat_emit(pre + 'e_lhlamp', '#fff0c0', strength=1.0 + 6.0 * lk), buoy_glow=mat_emit(pre + 'e_buoyglow', '#ffb840', strength=6.0),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.6, 0.3), 0.6 * lk), halo_gold=BK._mat_add(pre + 'halo_gold', tx['pool'], (1.0, 0.7, 0.25), 1.4, node='gold_k'), halo_cyan=BK._mat_add(pre + 'halo_cyan', tx['pool'], (0.5, 0.9, 1.0), 1.2, node='cyan_k'),
             buoy_cyan=mat_emit(pre + 'e_buoycyan', '#a8f4ff', strength=5.0), ghost_rim=_mat_ghost_rim(pre + 'ghost_rim'),
             ghost_foam=_mat_ghost_foam(pre + 'ghost_foam', tx['foam_wake']), ghost_foam_bow=_mat_ghost_foam(pre + 'ghost_foam_bow', tx['foam_bow']),
             ghost=_mat_ghost(pre + 'ghost'), cyan_line=mat_emit(pre + 'e_cyan', '#7ae8ff', strength=1.8), gold_line=mat_emit(pre + 'e_gold', '#ffc040', strength=2.2),
             smoke=W9._mat_dust(pre + 'smoke', P['smoke_rgb'], 1.0), plume=W9._mat_dust(pre + 'plume', (0.95, 0.96, 0.97), 1.0),
             fire=MN._mat_fire(pre + 'fire'), vignette=_mat_black(pre + 'vignette'), spray=C('#f4f8f6', 1.15, (1.5, 1.5, 1.4)), quaywall=TX('quaywall'),
             net=TX('net', alpha=True, smix=0.3), shallow=BK._mat_add(pre + 'shallow', tx['shallow'], (0.16, 0.6, 0.52), 0.32, node='sh_k'),
             awning=C('#c0603e', 1.0, (1.3, 0.9, 0.8), smix=0.3), awning2=C('#3e6a8a'), cloth_w=C('#f0ece0'), cloth_b=C('#5a7aa8'), cloth_r=C('#c04a3a', 1.0, (1.3, 0.9, 0.8), smix=0.3),
             horse=C('#7a4a2a'), horse_d=C('#4a2c1a'), sail=C('#efe4cc'), buoy_g=C('#3a8a4a'), flag_y=C('#e8b830'), flag_b=C('#2e4a9a'), reticle=_mat_black(pre + 'reticle', (0.006, 0.008, 0.01)), bezel=_mat_black(pre + 'bezel', (0.03, 0.035, 0.045)))
    M['foam'] = TX('foam_wake', alpha=True, form=False, sm=(1.3, 1.3, 1.25), glow='foam_wake', glow_k=0.55); M['foam_bow'] = TX('foam_bow', alpha=True, form=False, sm=(1.3, 1.3, 1.25), glow='foam_bow', glow_k=0.55)
    M['_flame_mats'] = [M['lamp_glass'], M['win_glow'], M['lh_lamp']]
    M['sky'] = D._mat_sky(pre + 'sky_' + P['sky'], dict(P, star_k=0.0), tx['sky_' + P['sky']], P['sky_k'])
    M['water'] = _mat_sea(pre + 'water', P, P['water'], ripple=0.12 if STATE['loc'] == 'harbour' else 0.0)
    return M

# ============================================================================= sky
def _sky(SET, P, M, R):
    """Sky dome of radius R (sky-dome UV, the film-9 painted sky) and, in the harbour, the painted backdrop ring (R HX.PANO_R)."""
    mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o
    if P.get('pano'):
        mb = MB(); Rp = HX.PANO_R; seg = 192; pm = mat_emit(STATE['pre'] + 'e_pano', image=STATE['tx']['pano_' + P['pano']], strength=P['pano_k'], alpha=True)
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
            mb.face([Vector((Rp * math.cos(a0), Rp * math.sin(a0), HX.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), HX.PANO_Z0)),
                     Vector((Rp * math.cos(a1), Rp * math.sin(a1), HX.PANO_Z1)), Vector((Rp * math.cos(a0), Rp * math.sin(a0), HX.PANO_Z1))], pm, [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
        _obj(mb, 'backdrop', SET, shadow=False)

# ============================================================================= ships
SHIP = dict(warship=dict(B=11.0, Dk=8.6, sheer=2.4), merchant=dict(B=10.5, Dk=6.8, sheer=3.0), far=dict(B=10.0, Dk=7.0, sheer=2.0))
TS = [-1.0, -0.97, -0.9, -0.7, -0.4, -0.1, 0.25, 0.5, 0.7, 0.84, 0.94, 1.0]

def _sec(t, L, B, Dk, sheer):
    """Hull section at station t (-1 stern .. 1 bow): [(x, half breadth, z)] from the keel to the deck edge."""
    deck = Dk + sheer * max(0.0, (t - 0.2) / 0.8) ** 2 + 0.6 * max(0.0, (-t - 0.75) / 0.25)
    if t > 0.25: f = max(0.0, 1 - ((t - 0.25) / 0.75) ** 1.7)
    elif t < -0.7: f = 0.6 + 0.4 * (1 - ((-t - 0.7) / 0.3) ** 2)
    else: f = 1.0
    out = []
    for z, g in ((-3.0, 0.16), (-1.6, 0.7), (0.0, 0.92), (2.6, 0.99), (5.2, 1.02), (deck, 1.05)):
        zn = (z + 3.0) / (deck + 3.0); x = t * L / 2
        if t > 0.8: x -= (1 - zn) * 3.2 * ((t - 0.8) / 0.2)
        if t < -0.85: x += (1 - zn) * 4.0 * ((-t - 0.85) / 0.15); g *= (0.35 + 0.65 * zn) if z < 0.5 else 1.0
        out.append((x, B / 2 * f * g, z))
    return out

def _hull(mb, L, B, Dk, sheer, paint, deckm):
    S = [_sec(t, L, B, Dk, sheer) for t in TS]
    for sg in (-1, 1):
        for i in range(len(TS) - 1):
            for j in range(len(S[0]) - 1):
                a, b, c, d = S[i][j], S[i + 1][j], S[i + 1][j + 1], S[i][j + 1]
                pts = [Vector((p[0], sg * p[1], p[2])) for p in (a, b, c, d)]
                mb.oface(pts, paint, [(0, 0)] * 4, (0, sg, 0))
    st = S[0]; mb.oface([Vector((p[0], -p[1], p[2])) for p in st] + [Vector((p[0], p[1], p[2])) for p in st[::-1]], paint, [(0, 0)] * (2 * len(st)), (-1, 0, 0))
    for i in range(len(TS) - 1):
        a, b = S[i][-1], S[i + 1][-1]
        pts = [Vector((a[0], -a[1], a[2])), Vector((b[0], -b[1], b[2])), Vector((b[0], b[1], b[2])), Vector((a[0], a[1], a[2]))]
        mb.oface(pts, deckm, [(p.x / 4, p.y / 4) for p in pts], (0, 0, 1))
    return S

def _windows(mb, x0, x1, y0, y1, z0, z1, glass, frame, w=0.55, gap=0.22):
    """Bridge / house windows: a light frame band with dark panes on the front (+x) and both sides."""
    mb.box((x0 - 0.03, y0 - 0.03, z0 - 0.12), (x1 + 0.03, y1 + 0.03, z1 + 0.12), frame)
    n = max(1, int((y1 - y0 + gap) / (w + gap)))
    for k in range(n):
        y = y0 + (y1 - y0 - n * (w + gap) + gap) / 2 + k * (w + gap); mb.box((x1, y, z0), (x1 + 0.08, y + w, z1), glass)
    n = max(1, int((x1 - x0 + gap) / (w + gap)))
    for k in range(n):
        x = x0 + (x1 - x0 - n * (w + gap) + gap) / 2 + k * (w + gap)
        for (ya, yb) in ((y0 - 0.08, y0), (y1, y1 + 0.08)): mb.box((x, ya, z0), (x + w, yb, z1), glass)

def _cowl(mb, base, h, s, body, inner):
    """Ventilator cowl: a pipe, a flared bell turned forward, red inside."""
    b = Vector(base); top = b + Vector((0, 0, h)); mouth = top + Vector((0.55 * s, 0, 0.45 * s))
    rod(mb, b, top, 0.26 * s, body, seg=8); rod(mb, top - Vector((0, 0, 0.1)), mouth, 0.3 * s, body, seg=10, r1=0.58 * s)
    ax = (mouth - top).normalized(); mb.frustum(mouth - ax * 0.06, mouth - ax * 0.02, 0.5 * s, 0.5 * s, inner, seg=10, cap0=False)

def _anchor(mb, S, L, sg, mat):
    """A stocked bower anchor hanging at the hawse pipe on the bow flare."""
    x = L / 2 - 3.6; y = sg * (_deck_hb(S, x) * 0.98 + 0.12); z = 7.0
    rod(mb, (x, y, z), (x - 0.3, y, z - 1.9), 0.12, mat, seg=6)
    rod(mb, (x - 0.9, y, z - 1.6), (x + 0.6, y, z - 2.1), 0.11, mat, seg=6)
    for d in (-1, 1): rod(mb, (x - 0.3, y, z - 1.9), (x - 0.3 + 0.75 * d, y, z - 1.3), 0.13, mat, seg=6, r1=0.06)

def _deck_z(S, x):
    """Deck height at ship x (linear between stations)."""
    xs = [s[-1][0] for s in S]; zs = [s[-1][2] for s in S]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]: t = (x - xs[i]) / max(1e-6, xs[i + 1] - xs[i]); return zs[i] * (1 - t) + zs[i + 1] * t
    return zs[0] if x < xs[0] else zs[-1]

def _deck_hb(S, x):
    xs = [s[-1][0] for s in S]; hs = [s[-1][1] for s in S]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]: t = (x - xs[i]) / max(1e-6, xs[i + 1] - xs[i]); return hs[i] * (1 - t) + hs[i + 1] * t
    return 0.0

def _rails(mb, S, M, h=1.0, step=2.4, x0=None, x1=None):
    xs = [s[-1][0] for s in S]; x0 = xs[0] + 0.6 if x0 is None else x0; x1 = xs[-1] - 1.0 if x1 is None else x1; n = max(2, int((x1 - x0) / step))
    for sg in (-1, 1):
        pts = []
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n; z = _deck_z(S, x); y = sg * (_deck_hb(S, x) - 0.12); pts.append(Vector((x, y, z + h)))
            rod(mb, (x, y, z), (x, y, z + h), 0.05, M['dark'], seg=4)
        chain_rod(mb, pts, 0.05, M['dark'], seg=4); chain_rod(mb, [p - Vector((0, 0, h * 0.5)) for p in pts], 0.035, M['dark'], seg=4)

def _boat(mb, c, l, w, M, yaw=0.0):
    """Ship's lifeboat: a pointed double-ended hull (white) with a dark gunwale."""
    c = Vector(c); X = Vector((math.cos(yaw), math.sin(yaw), 0)); Y = Vector((-X.y, X.x, 0)); Z = Vector((0, 0, 1)); pid = mb.pid
    ring = []
    for t in (-1.0, -0.6, 0.0, 0.6, 1.0):
        f = 1 - t * t * 0.95; ring.append([c + X * (t * l / 2) + Y * (s * w / 2 * f) + Z * zz for s, zz in ((-1, 0.6), (-0.5, 0.0), (0.5, 0.0), (1, 0.6))])
    for i in range(4):
        for j in range(3): mb.oface([ring[i][j], ring[i + 1][j], ring[i + 1][j + 1], ring[i][j + 1]], M['boat'], [(0, 0)] * 4, (Y * (j - 1)) - Z * 0.5 if j != 1 else -Z)
    mb.oface([r[0] for r in ring] + [r[3] for r in ring[::-1]], M['wood_d'], [(0, 0)] * 10, Z)
    mb.pid = pid + 50

def _gun(mb, x, z, M, paint, yaw=0.0, s=1.0):
    """A gun turret: a barbette ring, a sloped elliptic turret in the ship's paint with a roof, twin barrels with muzzle rings."""
    F = Frame((x, 0, z), yaw); c = math.cos(math.radians(yaw))
    rod(mb, F.p(0, 0, 0), F.p(0, 0, 0.55 * s), 1.35 * s, M['ship_dgrey'], seg=14)
    _ellip_prism(mb, F.p(0, 0, 0.55 * s), 1.75 * s, 1.35 * s, 1.25 * s, paint, top=M['ship_dgrey'], taper=0.76, lean=-0.25 * s * c)
    for dy in (-0.38, 0.38):
        a = F.p(1.0 * s, dy * s, 1.15 * s); b = F.p(4.8 * s, dy * s, 1.4 * s); rod(mb, a, b, 0.14 * s, M['ship_dgrey'], seg=6)
        rod(mb, b - (b - a).normalized() * 0.25 * s, b, 0.19 * s, M['ship_dgrey'], seg=6)

def _ship(name, kind, L, paint, M, root_loc, yaw=0.0, mats_override=None, detail=2, coll=None, foam=False, smoke=0, flag=True):
    """One ship: an empty root at the waterline (heading +x after yaw) with the ship mesh (hull + superstructure + funnels + masts +
    rigging) as child 'hull_<name>', optional foam (bow waves, side wash, stern wake) and funnel-smoke billows. paint: the paint
    material (dazzle hook). mats_override: every face gets that material (the ghost). Returns the ship dict."""
    coll = coll or STATE['SET']; sp = SHIP[kind]; B, Dk, sheer = sp['B'] * L / 64.0 if kind != 'merchant' else sp['B'], sp['Dk'], sp['sheer']
    O = mats_override
    def mm(k): return O if O is not None else M[k]
    pt = O if O is not None else paint; s = L / 64.0
    mb = MB(); S = _hull(mb, L, B, Dk, sheer, pt, mm('deck'))
    funnels = []
    if kind == 'warship':
        dz = Dk
        mb.box((0.12 * L, -0.3 * B, dz), (0.25 * L, 0.3 * B, dz + 3.2), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        mb.box((0.13 * L, -0.5 * B - 0.9, dz + 3.2), (0.24 * L, 0.5 * B + 0.9, dz + 3.45), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        mb.box((0.17 * L, -0.22 * B, dz + 3.45), (0.235 * L, 0.22 * B, dz + 5.8), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        _windows(mb, 0.17 * L, 0.235 * L, -0.22 * B, 0.22 * B, dz + 4.4, dz + 5.2, mm('window'), mm('white'))
        mb.box((0.238 * L, -0.3 * B, dz + 3.45), (0.245 * L, 0.3 * B, dz + 4.4), mm('canvas'))
        rod(mb, (0.15 * L, 0, dz + 3.45), (0.15 * L, 0, dz + 4.6), 0.25, mm('brass'), seg=8)
        for k in range(3): rod(mb, (0.21 * L, -0.15 * B + k * 0.5, dz + 3.45), (0.21 * L, -0.15 * B + k * 0.5, dz + 4.5), 0.07, mm('brass'), seg=6)
        for sg in (-1, 1):
            rod(mb, (0.135 * L, sg * (0.5 * B + 0.5), dz + 3.45), (0.135 * L, sg * (0.5 * B + 0.5), dz + 4.3), 0.06, mm('ship_dgrey'), seg=4)
            mb.frustum((0.135 * L - 0.25, sg * (0.5 * B + 0.5), dz + 4.55), (0.135 * L + 0.35, sg * (0.5 * B + 0.5), dz + 4.55), 0.32, 0.32, mm('ship_dgrey'), seg=10)
        for sg in (-1, 1):                                                                       # bridge-wing rails
            chain_rod(mb, [Vector((0.13 * L, sg * (0.5 * B + 0.85), dz + 4.45)), Vector((0.24 * L, sg * (0.5 * B + 0.85), dz + 4.45))], 0.05, mm('dark'), seg=4)
            for x in (0.13 * L, 0.185 * L, 0.24 * L): rod(mb, (x, sg * (0.5 * B + 0.85), dz + 3.45), (x, sg * (0.5 * B + 0.85), dz + 4.45), 0.05, mm('dark'), seg=4)
            chain_rod(mb, [Vector((0.13 * L, sg * (0.5 * B + 0.85), dz + 4.45)), Vector((0.13 * L, sg * 0.3 * B, dz + 4.45))], 0.05, mm('dark'), seg=4)
        mb.box((-0.25 * L, -0.28 * B, dz), (-0.12 * L, 0.28 * B, dz + 2.4), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        rod(mb, (-0.17 * L, 0, dz + 2.4), (-0.17 * L, 0, dz + 3.4), 0.5, mm('ship_dgrey'), seg=8)
        lumpy(mb, (-0.17 * L, 0.0, dz + 3.7), 0.55, mm('ship_dgrey'), 5, seg=8, rings=5, rough=0.0)
        for fx in (0.04 * L, -0.09 * L):
            p0 = Vector((fx, 0, dz - 0.3)); p1 = Vector((fx - 0.8 * s, 0, dz + 12.0 * s)); r0, r1 = 1.55 * s, 1.45 * s
            mb.box((fx - 2.0 * s, -1.9 * s, dz), (fx + 2.0 * s, 1.9 * s, dz + 1.4), pt, mats=dict(top=mm('deck')), tile=(4, 4))
            mb.frustum(p0, p1, r0, r1, pt, seg=12, cap1=False); mb.frustum(p1, p1 + Vector((-0.07 * s, 0, 1.0)), r1, r1, mm('funnel_top'), seg=12, cap1=False)
            mb.frustum(p1 + Vector((-0.07 * s, 0, 0.98)), p1 + Vector((-0.07 * s, 0, 0.99)), r1 * 0.94, r1 * 0.94, mm('dark'), seg=12, cap0=False)
            funnels.append(p1 + Vector((-0.1 * s, 0, 1.0)))
        for sg in (-1, 1):
            for bx in (-0.02 * L, -0.15 * L) if detail > 1 else ():
                _boat(mb, (bx, sg * (0.5 * B - 0.4), dz + 2.0), 5.0 * s, 1.5 * s, M if O is None else {k: O for k in ('boat', 'wood_d')})
                for dx in (-2.0 * s, 2.0 * s):
                    chain_rod(mb, [Vector((bx + dx, sg * (0.5 * B - 0.8), dz)), Vector((bx + dx, sg * (0.5 * B - 0.4), dz + 3.4)), Vector((bx + dx, sg * (0.5 * B + 0.05), dz + 3.2))], 0.07, mm('ship_dgrey'), seg=4)
            for vx in (0.08 * L, -0.03 * L):
                rod(mb, (vx, sg * 2.6 * s, dz), (vx, sg * 2.6 * s, dz + 2.0), 0.28 * s, pt, seg=8)
                _cowl(mb, (vx, sg * 2.6 * s, dz), 2.0, s, pt, mm('red'))
        fz = _deck_z(S, 0.36 * L); _gun(mb, 0.36 * L, fz, M if O is None else {k: O for k in ('ship_dgrey',)}, pt, 0.0, s)
        _gun(mb, -0.33 * L, Dk, M if O is None else {k: O for k in ('ship_dgrey',)}, pt, 180.0, s)
        fm0 = Vector((0.27 * L, 0, _deck_z(S, 0.27 * L))); fm1 = fm0 + Vector((-0.6, 0, 20.0 * s)); rod(mb, fm0, fm1, 0.24 * s, mm('ship_dgrey'), seg=6, r1=0.12)
        if O is None:                                        # a long red pennant streaming aft from the masthead
            mb.oface([fm1, fm1 + Vector((-5.5 * s, 0.3, -0.25)), fm1 + Vector((0, 0, -0.75))], M['red'], [(0, 0)] * 3, (0, 1, 0)); mb.oface([fm1, fm1 + Vector((-5.5 * s, 0.3, -0.25)), fm1 + Vector((0, 0, -0.75))], M['red'], [(0, 0)] * 3, (0, -1, 0))
        rod(mb, fm0 + Vector((-0.45, -3.2 * s, 15.0 * s)), fm0 + Vector((-0.45, 3.2 * s, 15.0 * s)), 0.09, mm('ship_dgrey'), seg=4)
        mb.frustum(fm0 + Vector((-0.38, 0, 11.6 * s)), fm0 + Vector((-0.4, 0, 12.8 * s)), 0.9 * s, 0.95 * s, mm('ship_dgrey'), seg=10)
        mm0 = Vector((-0.29 * L, 0, Dk)); mm1 = mm0 + Vector((-0.5, 0, 15.0 * s)); rod(mb, mm0, mm1, 0.2 * s, mm('ship_dgrey'), seg=6, r1=0.1)
        stem = Vector((S[-1][-1][0], 0, S[-1][-1][2])); stern = Vector((S[0][-1][0] + 1.0, 0, S[0][-1][2]))
        for a, b in ((fm1, stem), (fm1, mm1), (mm1, stern), (fm1 - Vector((0, 0, 4)), Vector((0.2 * L, 0.5 * B, Dk))), (fm1 - Vector((0, 0, 4)), Vector((0.2 * L, -0.5 * B, Dk))),
                     (mm1 - Vector((0, 0, 3)), Vector((-0.36 * L, 0.45 * B, Dk))), (mm1 - Vector((0, 0, 3)), Vector((-0.36 * L, -0.45 * B, Dk)))):
            rod(mb, a, b, 0.035, mm('dark'), seg=3)
        if detail > 1:
            for k in range(6): rod(mb, (-0.47 * L + 0.9 * (k % 3), (k // 3 - 0.5) * 2.0, Dk + 0.6), (-0.47 * L + 0.9 * (k % 3), (k // 3 - 0.5) * 2.0, Dk + 1.4), 0.38, mm('ship_dgrey'), seg=8)
        bridge = Vector((0.2 * L, 0, dz + 3.45)); STATE['marks_local_%s' % name] = dict(bridge=bridge, wing_s=Vector((0.17 * L, -(0.5 * B + 0.2), dz + 3.45)),
                                                                                          wing_p=Vector((0.17 * L, 0.5 * B + 0.2, dz + 3.45)), deck_aft=Vector((-0.4 * L, -1.5, Dk)),
                                                                                          deck_fwd=Vector((0.3 * L, -2.0, _deck_z(S, 0.3 * L))))
    elif kind == 'merchant':
        dz = Dk
        mb.box((0.38 * L, -0.5 * B + 0.2, _deck_z(S, 0.38 * L)), (0.5 * L - 2.0, 0.5 * B - 0.2, _deck_z(S, 0.38 * L) + 2.0), pt, mats=dict(top=mm('deck')), tile=(4, 4))   # forecastle
        mb.box((-0.5 * L + 1.5, -0.5 * B * 0.55, Dk), (-0.36 * L, 0.5 * B * 0.55, Dk + 2.3), pt, mats=dict(top=mm('deck')), tile=(4, 4))                                  # poop house
        mb.box((-0.06 * L, -0.38 * B, dz), (0.1 * L, 0.38 * B, dz + 2.6), mm('cream') if O is None else O, mats=dict(top=mm('deck')), tile=(4, 4))
        mb.box((-0.02 * L, -0.48 * B, dz + 2.6), (0.08 * L, 0.48 * B, dz + 2.85), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        mb.box((0.0, -0.25 * B, dz + 2.85), (0.07 * L, 0.25 * B, dz + 5.0), mm('cream') if O is None else O, mats=dict(top=mm('deck')), tile=(4, 4))
        _windows(mb, 0.0, 0.07 * L, -0.25 * B, 0.25 * B, dz + 3.7, dz + 4.5, mm('window'), mm('white'))
        fx = -0.12 * L; p0 = Vector((fx, 0, dz)); p1 = Vector((fx - 1.0, 0, dz + 13.0)); mb.frustum(p0, p1, 1.9, 1.8, pt, seg=12, cap1=False)
        mb.frustum(p1, p1 + Vector((-0.08, 0, 1.2)), 1.8, 1.8, mm('funnel_top'), seg=12, cap1=False); funnels.append(p1 + Vector((-0.1, 0, 1.2)))
        for hx in (0.28 * L, 0.18 * L, -0.22 * L, -0.31 * L):
            mb.box((hx - 2.2, -2.6, _deck_z(S, hx)), (hx + 2.2, 2.6, _deck_z(S, hx) + 1.0), mm('tarp') if O is None else O)
        for mx in (0.23 * L, -0.27 * L):
            m0 = Vector((mx, 0, _deck_z(S, mx))); m1 = m0 + Vector((0, 0, 16.0)); rod(mb, m0, m1, 0.28, mm('ship_dgrey'), seg=6, r1=0.14)
            rod(mb, m0 + Vector((0, -2.6, 7.0)), m0 + Vector((0, 2.6, 7.0)), 0.12, mm('ship_dgrey'), seg=4)
            for sg in (-1, 1): rod(mb, m0 + Vector((0, 0, 1.2)), m0 + Vector((sg * 6.5, 0, 6.0)), 0.13, mm('wood_d'), seg=4)
            for a in (Vector((mx, 0.5 * B, Dk)), Vector((mx, -0.5 * B, Dk)), Vector((mx + 6, 0, Dk)), Vector((mx - 6, 0, Dk))): rod(mb, m1, a, 0.03, mm('dark'), seg=3)
        bridge = Vector((0.035 * L, 0, dz + 2.85)); STATE['marks_local_%s' % name] = dict(bridge=bridge)
    else:                                                                               # far: hull + one block + funnel + mast
        mb.box((-0.1 * L, -0.3 * B, Dk), (0.15 * L, 0.3 * B, Dk + 4.0), pt, mats=dict(top=mm('deck')), tile=(4, 4))
        p0 = Vector((-0.02 * L, 0, Dk)); p1 = p0 + Vector((-0.6, 0, 9.5)); mb.frustum(p0, p1, 1.4, 1.35, pt, seg=8, cap1=False); funnels.append(p1)
        mb.frustum(p1, p1 + Vector((0, 0, 0.8)), 1.35, 1.35, mm('funnel_top'), seg=8, cap1=False)
        rod(mb, (0.25 * L, 0, Dk), (0.25 * L, 0, Dk + 15), 0.2, mm('ship_dgrey'), seg=4)
    if detail > 1 and kind != 'far':
        _rails(mb, S, M if O is None else {'dark': O})
        for sg in (-1, 1): _anchor(mb, S, L, sg, mm('dark'))
        if kind == 'merchant':
            for sg in (-1, 1):
                _boat(mb, (-0.2 * L, sg * (0.5 * B - 0.5), Dk + 1.8), 4.6, 1.4, M if O is None else {k: O for k in ('boat', 'wood_d')})
                for dx in (-1.8, 1.8): chain_rod(mb, [Vector((-0.2 * L + dx, sg * (0.5 * B - 0.9), Dk)), Vector((-0.2 * L + dx, sg * (0.5 * B - 0.5), Dk + 3.1)), Vector((-0.2 * L + dx, sg * (0.5 * B + 0.05), Dk + 2.9))], 0.07, mm('ship_dgrey'), seg=4)
                for vx in (0.13 * L, -0.06 * L): _cowl(mb, (vx, sg * 1.8, Dk), 1.8, 1.0, pt, mm('red'))
            f0 = funnels[0]; mb.frustum(f0 - Vector((0.0, 0, 2.2)), f0 - Vector((0.0, 0, 1.4)), 1.82, 1.82, mm('red'), seg=12, cap0=False, cap1=False)
    root = bpy.data.objects.new('ship_' + name, None); coll.objects.link(root); root.location = root_loc; root.rotation_euler = (0, 0, math.radians(yaw)); root.empty_display_size = 4
    hob = _obj(mb, 'hull_' + name, coll); hob.parent = root
    if O is not None: hob.visible_shadow = False
    if flag and O is None:
        fb = MB(); sx = S[0][-1][0] + 0.6; sz = S[0][-1][2]
        rod(fb, (sx, 0, sz), (sx, 0, sz + 4.5 * s), 0.06, M['dark'], seg=4)
        fb.face([Vector((sx, 0, sz + 4.4 * s)), Vector((sx - 3.0 * s, 0.3, sz + 4.2 * s)), Vector((sx - 3.0 * s, 0.3, sz + 2.6 * s)), Vector((sx, 0, sz + 2.8 * s))], M['ensign'], [(0, 1), (1, 1), (1, 0), (0, 0)])
        fo = _obj(fb, 'flag_' + name, coll); fo.parent = hob
    sh = dict(name=name, kind=kind, L=L, B=B, Dk=Dk, root=root, hull=hob, S=S, funnels=funnels, paint=paint, yaw=yaw, base=Vector(root_loc))
    if foam: _ship_foam(sh, M, coll)
    for fi, f in enumerate(funnels[:max(0, smoke)]): _funnel_smoke(sh, f, M, coll, seed=sum(ord(ch) * (i + 1) for i, ch in enumerate(name)) % 1000 + fi)
    STATE['ships'][name] = sh
    return sh

def _ship_foam(sh, M, coll, mats=None):
    """Big bow waves (two broad curling crests flaring out), side wash along the waterline and a long stern wake, flat on the water,
    children of the root. mats = (bow, wake) materials (the ghost has its own pale-cyan foam)."""
    L, B = sh['L'], sh['B']; fb = MB(); z = 0.32; mb_, mw_ = mats or (M['foam_bow'], M['foam'])
    for sg in (-1, 1):
        a = Vector((L / 2 - 1.0, 0, z)); b = Vector((L / 2 - 0.45 * L, sg * (B / 2 + 9.0), z)); n = Vector((0, 0, 1)); side = (b - a).normalized().cross(n) * (3.6 * sg)
        fb.oface([a - side * 0.25, b - side, b + side, a + side * 0.5], mb_, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
        a2 = Vector((L / 2 - 6.0, sg * (B / 2 - 0.6), z - 0.02)); b2 = Vector((-L / 2, sg * (B / 2 + 0.3), z - 0.02))
        fb.oface([a2, b2, b2 + Vector((0, sg * 2.2, 0)), a2 + Vector((0, sg * 1.6, 0))], mb_, [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.85)], n)
    s0 = Vector((-L / 2 + 1.0, 0, z)); s1 = Vector((-L / 2 - 2.6 * L, 0, z))
    fb.oface([s0 + Vector((0, -B * 0.42, 0)), s1 + Vector((0, -B * 1.6, 0)), s1 + Vector((0, B * 1.6, 0)), s0 + Vector((0, B * 0.42, 0))], mw_, [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
    if not mats:                                       # curling bow-wave crest (white spray lumps) + propeller wash churn at the stern
        for sg in (-1, 1):
            for k in range(8):
                t = k / 7.0; p = Vector((L / 2 - 1.5 - t * 0.33 * L, sg * (B * 0.18 + t * (B / 2 + 4.0)), 0.45 - 0.1 * t))
                lumpy(fb, p, 0.95 - 0.6 * t, M['spray'], 11 + k + (3 if sg > 0 else 0), seg=7, rings=4, rough=0.35, squash=0.55)
        for k in range(9):
            p = Vector((-L / 2 - 1.5 - k * 1.6, ((k * 37) % 7 - 3) * 0.55, 0.38)); lumpy(fb, p, 1.1 - 0.07 * k, M['spray'], 40 + k, seg=7, rings=4, rough=0.4, squash=0.4)
        fb.oface([Vector((-L / 2 - 1, -B * 0.5, z + 0.03)), Vector((-L / 2 - 16, -B * 0.75, z + 0.03)), Vector((-L / 2 - 16, B * 0.75, z + 0.03)), Vector((-L / 2 - 1, B * 0.5, z + 0.03))], mb_, [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
    o = _obj(fb, 'foam_' + sh['name'], coll, shadow=False); o.parent = sh['root']; sh['foam'] = o

def _funnel_smoke(sh, top, M, coll, seed=0, n=8):
    """Funnel smoke: cartoon billows (film-9 _mat_dust) rising from the funnel top and streaming aft, children of the ship root;
    set_smoke(level, frame) cycles them (call every frame)."""
    r = _rnd(seed)
    for k in range(n):
        mb = MB(); lumpy(mb, (0, 0, 0), 1.0, M['smoke'], seed + k, seg=10, rings=6, rough=0.18)
        o = _obj(mb, 'smoke_%s_%d' % (sh['name'], len(STATE['smoke'])), coll, shadow=False); o.parent = sh['root']
        STATE['smoke'].append(dict(ob=o, base=Vector(top) + Vector((0, 0, 0.6)), H=7.0 + r.uniform(0, 3), drift=Vector((-26.0 - r.uniform(0, 8), r.uniform(-3, 3), 0)),
                                   size=1.5 + r.uniform(0, 0.8), ph=k / n + r.uniform(0, 0.05)))

def _bob(sh, amp=1.0, seed=0):
    """Drivers on the ship mesh: a gentle heave / roll / pitch from the frame number (animated with no keys)."""
    ob = sh['hull']; r = _rnd(seed); ph = [r.uniform(0, 6.28) for _ in range(3)]
    for (path, idx, a, w, p) in (('location', 2, 0.16 * amp, 0.13, ph[0]), ('rotation_euler', 0, 0.018 * amp, 0.11, ph[1]), ('rotation_euler', 1, 0.008 * amp, 0.09, ph[2])):
        fc = ob.driver_add(path, idx); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '%.4f*sin(frame*%.4f+%.3f)' % (a, w, p)

# ============================================================================= harbour
QX = (-140.0, 160.0); QY = -70.0
BERTH = (0.0, 6.9)                    # the berth ship's root (x, y); its port side faces the quay
MOORED = [('m1', 'v1', (-46.0, 50.0), 0.0), ('m2', 'v2', (40.0, 54.0), 180.0), ('m3', 'v3', (-20.0, 88.0), 0.0), ('m4', 'v4', (62.0, 88.0), 0.0),
          ('m5', 'v5', (-110.0, 70.0), 0.0), ('m6', 'v6', (118.0, 52.0), 180.0)]
ROADS = [(-150.0, 150.0, 0.0), (-95.0, 176.0, 180.0), (-40.0, 158.0, 20.0), (15.0, 186.0, 0.0), (70.0, 164.0, 200.0), (125.0, 182.0, 0.0), (182.0, 158.0, 180.0),
         (-120.0, 232.0, 10.0), (-58.0, 252.0, 0.0), (2.0, 236.0, 190.0), (62.0, 248.0, 0.0), (122.0, 240.0, 170.0)]   # ships in the roads outside the breakwater

def _harbour(SET, P, M, dress):
    _sky(SET, P, M, 1100.0)
    mb = MB()
    mb.box((QX[0], QY, -4.0), (QX[1], 0.0, 0.0), M['setts'], mats=dict(front=M['kerb'], back=M['quaywall']), tile=(4, 4))
    mb.box((QX[0], -0.9, 0.0), (QX[1], 0.0, 0.18), M['kerb'], tile=(4, 4))
    for x in range(int(QX[0]) + 4, int(QX[1]), 6): mb.box((x - 0.15, -0.05, WZ - 0.3), (x + 0.15, 0.25, -0.1), M['wood_d'])            # fender piles
    for y in (-5.2, -7.2):                                                                                                                # crane rails
        for dy in (-0.7, 0.7): mb.box((QX[0], y + dy - 0.07, 0.0), (QX[1], y + dy + 0.07, 0.07), M['iron'])
    mb.box((-40.0, 104.0, -4.0), (150.0, 114.0, 1.6), M['stone'], mats=dict(top=M['kerb']), tile=(4, 4))                                 # breakwater
    for x in range(-38, 150, 7): lumpy(mb, (x + 0.5, 102.5, -1.2), 2.2, M['stone_d'], x + 300, seg=7, rings=4, rough=0.3)
    _obj(mb, 'quay', SET)
    wm = MB(); R = 1000.0; wm.face([Vector((-R, -R, WZ)), Vector((R, -R, WZ)), Vector((R, R, WZ)), Vector((-R, R, WZ))], M['water'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(wm, 'water', SET)
    sh = _ship('berth', 'warship', HX.HERO_L, _mat_paint(STATE['pre'] + 'paint_berth', P, STATE['tx'], 'dz_hero_base', [('dz_hero_l1', 1), ('dz_hero_l2', 2), ('dz_hero_l3', 3)], HX.HERO_L),
               M, (BERTH[0], BERTH[1], WZ), 0.0, smoke=0)
    STATE['berth'] = sh
    STATE['moored'] = []
    for i, (nm, var, pos, yaw) in enumerate(MOORED):
        L = HX.SHIP_LS[var]; pm = _mat_paint(STATE['pre'] + 'paint_' + nm, P, STATE['tx'], 'dz_%s_base' % var, [('dz_' + var, 1)], L)
        s2 = _ship(nm, 'warship', L, pm, M, (pos[0], pos[1], WZ), yaw, detail=1 if i >= 4 else 2, smoke=1 if nm in ('m2', 'm5') else 0); STATE['moored'].append(s2)
    for i, (x, y, yaw) in enumerate(ROADS):
        var = 'v%d' % (1 + i % 6); L = HX.SHIP_LS[var] * 0.9; pm = _mat_paint(STATE['pre'] + 'paint_r%d' % i, P, STATE['tx'], 'dz_%s_base' % var, [('dz_' + var, 1)], L)
        s2 = _ship('r%d' % i, 'far', L, pm, M, (x, y, WZ), yaw, detail=0, flag=False); STATE['moored'].append(s2)
    _lighthouse(SET, M, (150.0, 109.0, 1.6))
    _warehouses(SET, M)
    _cranes(SET, M)
    _scaffold(SET, M, sh)
    if dress: _quay_dress(SET, M, sh)
    _gulls(SET, M)
    _tug(SET, M)
    _harbour_extras(SET, M, sh)
    for i, s2 in enumerate(STATE['moored'][:6]): _bob(s2, 0.25, i)
    STATE['marks'].update(_harbour_marks(sh))

def _lighthouse(SET, M, base):
    b = Vector(base); mb = MB(); fl = MB()
    for k in range(6):
        z0, z1 = k * 3.2, (k + 1) * 3.2; mb.frustum(b + Vector((0, 0, z0)), b + Vector((0, 0, z1)), 3.0 - 0.18 * k, 3.0 - 0.18 * (k + 1), M['lh_red'] if k % 2 else M['lh_white'], seg=16, cap0=False, cap1=False)
    top = b + Vector((0, 0, 19.2))
    mb.frustum(top, top + Vector((0, 0, 0.5)), 2.6, 2.6, M['dark'], seg=16); fl.frustum(top + Vector((0, 0, 0.5)), top + Vector((0, 0, 2.9)), 1.4, 1.4, M['lh_lamp'], seg=12)
    for k in range(8): a = 2 * math.pi * k / 8; rod(mb, top + Vector((1.45 * math.cos(a), 1.45 * math.sin(a), 0.5)), top + Vector((1.45 * math.cos(a), 1.45 * math.sin(a), 2.9)), 0.06, M['dark'], seg=4)
    mb.frustum(top + Vector((0, 0, 2.9)), top + Vector((0, 0, 4.6)), 1.9, 0.2, M['lh_red'], seg=12)
    chain_rod(mb, [top + Vector((2.6 * math.cos(2 * math.pi * k / 24), 2.6 * math.sin(2 * math.pi * k / 24), 1.4)) for k in range(25)], 0.05, M['dark'], seg=3)
    mb.box((b.x - 4.5, b.y - 4.5, b.z - 0.2), (b.x + 4.5, b.y + 4.5, b.z + 0.4), M['stone'])
    mb.box((b.x - 7, b.y - 2.5, b.z), (b.x - 3, b.y + 2.5, b.z + 3.5), M['lh_white'], mats=dict(top=M['red_d']))
    _halo(fl, top + Vector((0, 0, 1.7)), 6.0, M)
    _obj(mb, 'lighthouse', SET); _obj(fl, 'lighthouse_lamp', SET, shadow=False)
    if STATE['P'].get('lamps', 0) > 0.2: D._flame_light('lighthouse', tuple(top + Vector((0, 0, 1.7))), LAMP, 9000, radius=0.6)

def _warehouses(SET, M):
    """Red-brick warehouses along the back of the quay (facades at y -26 facing the water): 2-3 storeys of arched-window bays,
    slate roofs, chimneys, loading doors with hoist beams, a small dock office."""
    mb = MB(); r = _rnd(7)
    for (x0, x1, st, mat) in ((-128.0, -74.0, 3, 'brick'), (-68.0, -14.0, 2, 'brick_b'), (-8.0, 46.0, 3, 'brick'), (52.0, 98.0, 2, 'brick_b'), (104.0, 152.0, 3, 'brick')):
        h = 5.0 * st; y0, y1 = -54.0, -36.0
        mb.box((x0, y0, 0.0), (x1, y1, h), M[mat], mats=dict(left=M['brick_side'], right=M['brick_side']), tile=(6, 5))
        mb.box((x0 - 0.3, y1 - 0.0, h - 0.1), (x1 + 0.3, y1 + 0.5, h + 0.4), M['stone'])
        rz = h + 6.0
        for sg, (ya, yb) in ((1, (y1 + 0.8, (y0 + y1) / 2)), (-1, (y0 - 0.8, (y0 + y1) / 2))):
            mb.oface([Vector((x0 - 0.6, ya, h)), Vector((x1 + 0.6, ya, h)), Vector((x1 + 0.6, yb, rz)), Vector((x0 - 0.6, yb, rz))], M['slate'],
                     [(x0 / 4, 0), (x1 / 4, 0), (x1 / 4, 3.0), (x0 / 4, 3.0)], (0, sg, 1))
        for xe in (x0, x1):
            mb.oface([Vector((xe, y1, h)), Vector((xe, y0, h)), Vector((xe, (y0 + y1) / 2, rz))], M['brick_side'], [(0, 0), (3, 0), (1.5, 1.2)], (1 if xe == x1 else -1, 0, 0))
        for cx in (x0 + 6, x1 - 6):
            mb.box((cx - 0.9, -46.0, rz - 3.0), (cx + 0.9, -44.2, rz + 2.6), M['brick_side'], tile=(6, 5)); mb.box((cx - 1.1, -46.2, rz + 2.6), (cx + 1.1, -44.0, rz + 3.0), M['stone_d'])
        for dx in range(int(x0) + 9, int(x1) - 6, 18):                         # loading doors on every floor + hoist beam
            mb.box((dx - 1.6, y1 - 0.05, 0.0), (dx + 1.6, y1 + 0.25, 4.2), M['wood_d'])
            for k in range(st - 1):
                mb.box((dx - 1.2, y1 - 0.05, 5.6 + 5 * k), (dx + 1.2, y1 + 0.22, 8.6 + 5 * k), M['wood'])
            mb.box((dx - 0.2, y1, h - 1.0), (dx + 0.2, y1 + 2.4, h - 0.6), M['wood_d']); chain_rod(mb, [Vector((dx, y1 + 2.2, h - 1.0)), Vector((dx, y1 + 2.2, h - 4.5))], 0.04, M['rope'])
    mb.box((60.0, -18.0, 0.0), (68.0, -12.0, 4.0), M['cream'], mats=dict(top=M['slate']))           # dock office
    mb.box((63.0, -12.05, 0.0), (64.6, -11.9, 3.0), M['green']); mb.box((65.5, -12.05, 1.5), (67.2, -11.9, 3.0), M['window'])
    rod(mb, (61.0, -15.0, 4.0), (61.0, -15.0, 6.4), 0.18, M['iron'], seg=6)
    _obj(mb, 'warehouses', SET)

def _crane(mb, M, base, yaw, jib_ang=38.0, jib_len=22.0, hook_drop=10.0, s=1.0):
    """Dockside portal jib crane on the rails: four lattice legs, a slewing cab, an A-frame and a lattice jib; returns the hook."""
    b = Vector(base); F = Frame(b, yaw)
    for (x, y) in ((-2.5, -0.7 - 1.4), (2.5, -0.7 - 1.4), (-2.5, 0.7), (2.5, 0.7)):
        rod(mb, F.p(x, y + 0.7, 0), F.p(x * 0.5, (y + 0.7) * 0.4, 9.0), 0.22, M['rust'], seg=4)
    F.box(mb, (-2.0, -1.2, 9.0), (2.0, 1.2, 9.6), M['rust'])
    for (x, y) in ((-2.5, -1.4), (2.5, -1.4), (-2.5, 1.4), (2.5, 1.4)): F.box(mb, (x - 0.3, y - 0.3, 0.0), (x + 0.3, y + 0.3, 0.5), M['iron'])
    F.box(mb, (-2.2, -1.6, 9.6), (2.4, 1.6, 13.0), M['ship_dgrey']); F.box(mb, (-2.0, -1.7, 11.2), (1.0, 1.7, 12.2), M['window'])
    F.box(mb, (-3.6, -1.2, 9.6), (-2.2, 1.2, 11.8), M['dark'])
    rod(mb, F.p(-1.0, 0, 13.0), F.p(0.5, 0, 17.0), 0.18, M['rust'], seg=4)
    a = math.radians(jib_ang); tip = F.p(1.5 + jib_len * math.cos(a), 0, 10.5 + jib_len * math.sin(a))
    for dy in (-0.7, 0.7):
        p0 = F.p(1.5, dy, 10.5); rod(mb, p0, tip, 0.14, M['rust'], seg=4)
        n = 9
        for k in range(n):
            q0 = p0.lerp(tip, k / n); q1 = p0.lerp(tip, (k + 1) / n); rod(mb, q0, q1 + Vector((0, 0, 0.0)) - (F.Y * dy * 2 if False else Vector()), 0.05, M['rust'], seg=3)
            rod(mb, q0 + Vector((0, 0, 0)), F.p(1.5, -dy, 10.5).lerp(tip, (k + 1) / n), 0.05, M['rust'], seg=3)
    rod(mb, F.p(0.5, 0, 17.0), tip, 0.05, M['dark'], seg=3)
    hook = tip - Vector((0, 0, hook_drop)); rod(mb, tip, hook, 0.04, M['dark'], seg=3)
    lumpy(mb, hook, 0.35, M['iron'], 3, seg=6, rings=4, rough=0.0)
    return hook

def _cranes(SET, M):
    mb = MB()
    h1 = _crane(mb, M, (-56.0, -6.2, 0.0), 80.0, 40, 24, 14)
    mb.frustum(h1 - Vector((0, 0, 2.6)), h1 - Vector((0, 0, 0.6)), 0.9, 0.9, M['grey_p'], seg=12)                                  # a paint drum on the hook
    for k in (-0.6, 0.6): rod(mb, h1 - Vector((0, 0, 0.3)), h1 + Vector((k, 0, -0.65)), 0.03, M['dark'], seg=3)
    _crane(mb, M, (38.0, -6.2, 0.0), 75.0, 30, 22, 9)
    _crane(mb, M, (96.0, -6.2, 0.0), 120.0, 52, 20, 6)
    _crane(mb, M, (-96.0, -6.2, 0.0), 60.0, 44, 22, 8)
    _obj(mb, 'cranes', SET)

def _ladder(mb, p0, p1, M, w=0.55):
    p0, p1 = Vector(p0), Vector(p1); d = (p1 - p0); side = d.cross(Vector((0, 0, 1))).normalized() * (w / 2)
    if side.length < 1e-4: side = Vector((w / 2, 0, 0))
    rod(mb, p0 - side, p1 - side, 0.05, M['wood_l'], seg=4); rod(mb, p0 + side, p1 + side, 0.05, M['wood_l'], seg=4)
    n = int(d.length / 0.42)
    for k in range(1, n): q = p0.lerp(p1, k / n); rod(mb, q - side, q + side, 0.035, M['wood_l'], seg=3)

def _bucket(mb, c, M, paint, r=0.38, h=0.6, drips=True):
    c = Vector(c); mb.frustum(c, c + Vector((0, 0, h)), r * 0.88, r, M['bucket'], seg=12, cap1=False)
    mb.frustum(c + Vector((0, 0, h - 0.06)), c + Vector((0, 0, h - 0.05)), r * 0.96, r * 0.96, M[paint], seg=12, cap0=False)
    chain_rod(mb, [c + Vector((-r, 0, h)), c + Vector((-r * 0.5, 0, h + r * 0.8)), c + Vector((r * 0.5, 0, h + r * 0.8)), c + Vector((r, 0, h))], 0.02, M['dark'], seg=3)
    if drips:
        for k in range(3):
            a = 2 * math.pi * (k * 0.37 + 0.1); p = c + Vector((math.cos(a) * r * 1.01, math.sin(a) * r * 1.01, h))
            rod(mb, p, p - Vector((0, 0, 0.15 + 0.12 * k)), 0.045, M[paint], seg=4, r1=0.03)
    if drips: mb.frustum(c + Vector((0.3, 0.2, 0.005)), c + Vector((0.3, 0.2, 0.012)), r * 1.3, r * 1.3, M[paint], seg=10, cap0=False)

def _brush(mb, p, d, M, paint, Lh=1.4):
    p = Vector(p); d = Vector(d).normalized(); rod(mb, p, p + d * Lh, 0.035, M['wood_l'], seg=4)
    q = p + d * Lh; mb.box((q.x - 0.14, q.y - 0.05, q.z - 0.05), (q.x + 0.14, q.y + 0.05, q.z + 0.12), M['wood']); mb.box((q.x - 0.14, q.y - 0.06, q.z + 0.12), (q.x + 0.14, q.y + 0.06, q.z + 0.32), M[paint])

def _hang_plank(mb, M, sh, x0, x1, z, off=0.55):
    """Painter's hanging stage: a plank on two short cross bearers, hung by ropes from the deck rail of the berth ship."""
    yh = sh['base'].y - _hb_at(sh, (x0 + x1) / 2, z - WZ) - off; ya, yb = yh - 0.45, yh + 0.3
    mb.box((x0, ya, z), (x1, yb, z + 0.14), M['planks'], tile=(4, 4))
    for x in (x0 + 0.4, x1 - 0.4):
        mb.box((x - 0.12, ya - 0.15, z - 0.12), (x + 0.12, yb + 0.15, z), M['wood_d'])
        top = Vector((x, sh['base'].y - _deck_hb(sh['S'], x) - 0.05, WZ + _deck_z(sh['S'], x) + 1.0))
        for yy in (ya - 0.1, yb + 0.1): rod(mb, (x, yy, z), top, 0.03, M['rope'], seg=3)
    return yh, z + 0.14

def _hb_at(sh, x, zl):
    """Half breadth of the berth hull at ship x, local z (interpolated between sections)."""
    S = sh['S']; xs = [s[-1][0] for s in S]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i]); best = 0.0
            for sec in (S[i], S[i + 1]):
                for a, b in zip(sec, sec[1:]):
                    if a[2] <= zl <= b[2]: k = (zl - a[2]) / max(1e-6, b[2] - a[2]); best += (a[1] * (1 - k) + b[1] * k) * (1 - t if sec is S[i] else t)
            return best
    return 0.0

def _scaffold(SET, M, sh):
    """Plank scaffolding on the quay along the hull (two lifts, braces, ladders), hanging painter's stages, buckets and brushes."""
    mb = MB(); STATE['planks'] = {}
    for (x0, x1) in ((-27.0, -9.0), (7.0, 19.0)):
        xs = [x0 + k * (x1 - x0) / 4 for k in range(5)]
        for x in xs:
            for y in (-0.35, -2.35): rod(mb, (x, y, 0.0), (x, y, 7.6), 0.09, M['wood_l'], seg=5); mb.box((x - 0.25, y - 0.25, 0.0), (x + 0.25, y + 0.25, 0.08), M['wood_d'])
            for z in (2.4, 4.8): rod(mb, (x, -2.5, z), (x, 0.2, z), 0.07, M['wood_l'], seg=4)
        for z in (2.4, 4.8):
            for y in (-0.35, -2.35): rod(mb, (x0, y, z + 0.9), (x1, y, z + 0.9), 0.05, M['wood_l'], seg=4)
            for k in range(4): mb.box((x0 - 0.3, -2.6 + k * 0.72, z + 0.07), (x1 + 0.3, -2.6 + k * 0.72 + 0.62, z + 0.19), M['planks'], tile=(4, 4))
        for i in range(4): rod(mb, (xs[i], -2.35, 0.2), (xs[i + 1], -2.35, 4.7), 0.05, M['wood_l'], seg=4)
        _ladder(mb, (x0 + 1.0, -3.3, 0.0), (x0 + 1.0, -2.6, 5.2), M)
    for name, (x0, x1, z) in dict(plank=(-6.0, -0.2, 2.6), plank_b=(21.0, 26.0, 4.2), plank_c=(-24.0, -19.0, -0.6)).items():
        yh, zt = _hang_plank(mb, M, sh, x0, x1, z); STATE['planks'][name] = dict(x=(x0, x1), y=yh, z=zt)
        for i, pc in enumerate(('paint_b', 'paint_w') if name == 'plank' else ('paint_g',)):
            _bucket(mb, (x0 + 0.7 + i * 0.9, yh - 0.1, zt), M, pc, r=0.28, h=0.45)
    pl = STATE['planks']['plank']; _brush(mb, (pl['x'][0] + 2.2, pl['y'] - 0.1, pl['z'] + 0.45), (0.2, 0.0, -1.0), M, 'paint_b', 0.4)
    _obj(mb, 'scaffold', SET)

def _bollard(mb, c, M):
    c = Vector(c); mb.frustum(c, c + Vector((0, 0, 0.9)), 0.42, 0.36, M['iron'], seg=10); mb.frustum(c + Vector((0, 0, 0.9)), c + Vector((0, 0, 1.1)), 0.55, 0.5, M['iron'], seg=10)

def _crate_stack(mb, c, M, seed, n=6):
    r = _rnd(seed); c = Vector(c)
    for k in range(n):
        s = r.uniform(1.0, 1.6); x = c.x + (k % 3) * 1.7 + r.uniform(-0.1, 0.1); y = c.y + (k // 3 % 2) * 1.7; z = 0.0 if k < 6 else 1.6
        if k >= 6: x = c.x + (k - 6) * 1.7 + 0.8
        mb.box((x - s / 2, y - s / 2, z), (x + s / 2, y + s / 2, z + s), M['crate'], tile=(4, 4))
        for e in (-1, 1): mb.box((x - s / 2 - 0.02, y + e * s / 2 - 0.02 * e - 0.02, z + 0.1), (x + s / 2 + 0.02, y + e * s / 2 + 0.02, z + 0.25), M['wood_d'])

def _barrel(mb, c, M, mat='wood', r=0.55, h=1.3, lying=False):
    c = Vector(c)
    if lying: mb.frustum(c - Vector((h / 2, 0, -r)), c + Vector((h / 2, 0, r)), r, r, M[mat], seg=12); return
    mb.frustum(c, c + Vector((0, 0, h / 2)), r * 0.85, r, M[mat], seg=12, cap1=False); mb.frustum(c + Vector((0, 0, h / 2)), c + Vector((0, 0, h)), r, r * 0.85, M[mat], seg=12, cap0=False)
    mb.frustum(c + Vector((0, 0, h - 0.01)), c + Vector((0, 0, h)), r * 0.85, r * 0.85, M['wood_d'], seg=12, cap0=False)
    for zz in (0.18, h - 0.18): mb.frustum(c + Vector((0, 0, zz - 0.05)), c + Vector((0, 0, zz + 0.05)), r * 0.93, r * 0.93, M['iron'], seg=12, cap0=False, cap1=False)

def _gas_lamp(mb, fl, c, M):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, 4.4)), 0.1, M['dark'], seg=6, r1=0.07); mb.frustum(c, c + Vector((0, 0, 0.6)), 0.24, 0.14, M['dark'], seg=8)
    rod(mb, c + Vector((-0.4, 0, 4.0)), c + Vector((0.4, 0, 4.0)), 0.035, M['dark'], seg=3)
    fl.frustum(c + Vector((0, 0, 4.4)), c + Vector((0, 0, 5.1)), 0.18, 0.28, M['lamp_glass'], seg=6)
    mb.frustum(c + Vector((0, 0, 5.1)), c + Vector((0, 0, 5.5)), 0.36, 0.05, M['dark'], seg=6)
    f = c + Vector((0, 0, 4.75)); _halo(fl, f, 1.3, M)
    if STATE['P'].get('lamps', 0) > 0.2: D._flame_light('gas_%d' % len(STATE['flames']), tuple(f), LAMP, 260, radius=0.15)

def _quay_dress(SET, M, sh):
    """The quay: bollards + mooring lines, gas lamps, crate stacks, barrels, sacks, a coal heap, paint drums and buckets (black,
    white, grey), ladders, a hand cart, coiled ropes, a capstan, chains, a brazier-free tea hut, life rings."""
    mb = MB(); fl = MB(); r = _rnd(31)
    for x in range(-126, 156, 14): _bollard(mb, (x, -1.4, 0.0), M)
    B = sh['base']
    for (xb, xs) in ((-42.0, -26.0), (-28.0, -14.0), (28.0, 16.0), (42.0, 30.0)):          # mooring lines to the berth ship's deck edge
        a = Vector((xb, -1.4, 1.0)); b = Vector((xs, B.y - _deck_hb(sh['S'], xs), WZ + _deck_z(sh['S'], xs) + 0.4))
        chain_rod(mb, catenary(a, b, 0.6, 10), 0.08, M['rope'], seg=4)
    for x in (-60.0, -18.0, 24.0, 70.0, 110.0, -100.0): _gas_lamp(mb, fl, (x, -3.6, 0.0), M)
    for (c, sd, n) in (((-60, -14), 3, 9), ((-48, -18), 5, 6), ((20, -16), 7, 9), ((76, -9), 9, 6), ((-86, -12), 11, 9), ((118, -14), 13, 6)): _crate_stack(mb, Vector((c[0], c[1], 0)), M, sd, n)
    for k in range(10):                                                                      # barrels by the warehouses
        x = -20 + (k % 5) * 1.3; y = -20.5 - (k // 5) * 1.3; _barrel(mb, (x, y, 0.0), M)
    for k in range(4): _barrel(mb, (88 + k * 1.6, -19.0, 0.0), M, lying=True)
    for (x, y, pc) in ((-4.0, -3.2, 'paint_b'), (-3.2, -3.9, 'paint_w'), (-2.2, -3.1, 'paint_g'), (-5.0, -4.2, 'paint_b'), (2.6, -3.0, 'paint_w'), (3.4, -3.8, 'paint_b'),
                       (-12.0, -3.6, 'paint_g'), (-11.2, -4.3, 'paint_w'), (12.5, -3.2, 'paint_b'), (13.3, -3.9, 'paint_g')):
        _bucket(mb, (x, y, 0.0), M, pc)
    for (x, y, pc) in ((-7.5, -5.4, 'black_p'), (-8.8, -5.6, 'white_p'), (-8.1, -6.8, 'grey_p'), (5.5, -5.6, 'black_p'), (6.8, -5.4, 'white_p')):   # big paint drums
        mb.frustum((x, y, 0), (x, y, 1.25), 0.55, 0.55, M[pc], seg=14)
    for (x, y) in ((-6.0, -2.4), (4.6, -2.6), (-14.0, -2.5)): _brush(mb, (x, y, 0.06), (0.9, 0.35, 0.02), M, 'paint_b', 1.6)
    _ladder(mb, (-1.0, -1.2, 0.0), (-1.0, 0.45, 5.6), M)
    _ladder(mb, (16.0, -10.0, 0.0), (16.0, -10.6, 3.6), M)
    for (x, y) in ((24.0, -2.6), (-50.0, -2.6), (60.0, -2.6)):                               # coiled ropes
        for k in range(4): mb.frustum((x, y, k * 0.12), (x, y, k * 0.12 + 0.12), 0.7 - k * 0.06, 0.7 - k * 0.06, M['rope'], seg=12, cap0=k == 0)
    mb.frustum((10.0, -3.0, 0.0), (10.0, -3.0, 1.0), 0.6, 0.45, M['iron'], seg=10); mb.frustum((10.0, -3.0, 1.0), (10.0, -3.0, 1.2), 0.8, 0.8, M['iron'], seg=10)   # capstan
    hc = Frame((-30.0, -10.0, 0.0), 20.0); hc.box(mb, (-1.0, -0.6, 0.6), (1.0, 0.6, 0.75), M['wood']); rod(mb, hc.p(1.0, -0.4, 0.7), hc.p(2.6, -0.4, 0.9), 0.05, M['wood_d'], seg=4)
    rod(mb, hc.p(1.0, 0.4, 0.7), hc.p(2.6, 0.4, 0.9), 0.05, M['wood_d'], seg=4)
    for sy in (-0.7, 0.7): mb.frustum(hc.p(0, sy, 0.45), hc.p(0, sy + (0.12 if sy > 0 else -0.12), 0.45), 0.45, 0.45, M['wood_d'], seg=10)
    for k in range(3): mb.frustum(hc.p(-0.4 + k * 0.45, 0, 0.75), hc.p(-0.4 + k * 0.45, 0, 1.35), 0.2, 0.2, M[('black_p', 'white_p', 'grey_p')[k]], seg=10)
    for k in range(8): lumpy(mb, (44 + (k % 4) * 1.1, -14.5 - (k // 4) * 0.9, 0.35), 0.6, M['canvas'], 70 + k, seg=8, rings=4, rough=0.15, squash=0.6)   # sacks
    for k in range(5): lumpy(mb, (-70 + k * 1.6, -21.5, 0.2), 1.6 - 0.15 * k, M['coal'], 90 + k, seg=8, rings=5, rough=0.35, squash=0.7)        # coal heap
    for x in (-36.0, 54.0): mb.box((x - 4, -22.0, 0.0), (x + 4, -18.0, 2.2), M['tarp'])                                                     # tarpaulin stacks
    th = Frame((-80.0, -8.5, 0.0), 0.0); th.box(mb, (-2.0, -1.6, 0.0), (2.0, 1.6, 3.0), M['green']); th.box(mb, (-2.3, -1.9, 3.0), (2.3, 1.9, 3.3), M['dark'])
    th.box(mb, (-0.6, -1.65, 0.0), (0.6, -1.55, 2.3), M['wood_d']); th.box(mb, (0.9, -1.65, 1.2), (1.7, -1.55, 2.2), M['window'])
    rod(mb, th.p(1.2, 0.8, 3.3), th.p(1.2, 0.8, 4.6), 0.12, M['iron'], seg=6)
    for x in (-62.0, 34.0):                                                                   # life rings on posts
        rod(mb, (x, -1.0, 0.0), (x, -1.0, 2.2), 0.06, M['wood_d'], seg=4)
        for k in range(12):
            a0, a1 = 2 * math.pi * k / 12, 2 * math.pi * (k + 1) / 12
            rod(mb, (x + 0.45 * math.cos(a0), -0.9, 1.6 + 0.45 * math.sin(a0)), (x + 0.45 * math.cos(a1), -0.9, 1.6 + 0.45 * math.sin(a1)), 0.11, M['red'] if k % 3 else M['white'], seg=5)
    for k in range(6):                                                                        # chain along the edge
        a = Vector((-118 + k * 4, -0.6, 0.18)); chain_rod(mb, catenary(a, a + Vector((4, 0, 0)), 0.25, 6), 0.06, M['iron'], seg=4)
    for (c, sd, n) in (((4.2, -12.0), 15, 3), ((-15.5, -10.5), 17, 4)): _crate_stack(mb, Vector((c[0], c[1], 0)), M, sd, n)
    for k in range(4): mb.frustum((-11.0, -9.2, k * 0.12), (-11.0, -9.2, k * 0.12 + 0.12), 0.75 - k * 0.06, 0.75 - k * 0.06, M['rope'], seg=12, cap0=k == 0)
    for (x, y, pc) in ((17.6, -3.1, 'paint_b'), (18.4, -3.8, 'paint_w'), (14.0, -2.9, 'paint_g')): _bucket(mb, (x, y, 0.0), M, pc)
    _brush(mb, (16.8, -2.6, 0.06), (0.9, 0.3, 0.02), M, 'paint_w', 1.6)
    for k in range(4): mb.frustum((12.4, -12.8, k * 0.12), (12.4, -12.8, k * 0.12 + 0.12), 0.7 - k * 0.06, 0.7 - k * 0.06, M['rope'], seg=12, cap0=k == 0)
    _bucket(mb, (15.2, -14.4, 0.0), M, 'paint_b'); _bucket(mb, (15.9, -13.6, 0.0), M, 'paint_w')
    _barrel(mb, (-12.6, -13.6, 0.0), M); _barrel(mb, (-13.4, -12.4, 0.0), M, mat='rust'); _bucket(mb, (-7.2, -10.6, 0.0), M, 'paint_w'); _bucket(mb, (2.0, -8.4, 0.0), M, 'paint_g')
    for y in (-15.3, -16.7): mb.box((QX[0], y - 0.08, 0.0), (QX[1], y + 0.08, 0.1), M['iron'])        # goods siding
    for k, (x, col) in enumerate(((-40.0, 'red_d'), (-31.0, 'wood'), (-22.0, 'ship_dgrey'), (40.0, 'red_d'), (49.0, 'wood'))):
        mb.box((x - 3.8, -17.4, 0.9), (x + 3.8, -14.6, 1.2), M['iron']); mb.box((x - 3.6, -17.3, 1.2), (x + 3.6, -14.7, 4.0), M[col], mats=dict(top=M['tarp' if k % 2 else 'dark']))
        mb.box((x - 0.9, -17.36, 1.6), (x + 0.9, -17.3, 3.6), M['wood_d'])
        for dx in (-2.4, 2.4):
            for yy in (-17.45, -14.55): mb.frustum((x + dx, yy, 0.55), (x + dx, yy + (0.12 if yy > -16 else -0.12), 0.55), 0.5, 0.5, M['iron'], seg=10)
    for k in range(3):                                                                         # timber stacks
        for j in range(4): mb.box((-8.0 + k * 7, -22.5 + j * 0.02, j * 0.35), (-2.0 + k * 7, -20.5, j * 0.35 + 0.33), M['wood_l'] if j % 2 else M['wood'])
    if STATE['P'].get('lamps', 0) > 0.2:                       # DUSK: warm brazier pools near the quay_low / harbour_wide cameras
        for c in ((12.4, -10.6), (-31.0, -11.5), (-3.5, -7.5)):
            c = Vector((c[0], c[1], 0.0)); rod(mb, c, c + Vector((0, 0, 1.1)), 0.06, M['iron'], seg=4)
            for k in range(3): a = 2 * math.pi * k / 3; rod(mb, c + Vector((0.5 * math.cos(a), 0.5 * math.sin(a), 0)), c + Vector((0.3 * math.cos(a), 0.3 * math.sin(a), 1.1)), 0.05, M['iron'], seg=4)
            mb.frustum(c + Vector((0, 0, 1.1)), c + Vector((0, 0, 1.6)), 0.35, 0.55, M['iron'], seg=10, cap1=False)
            lumpy(fl, c + Vector((0, 0, 1.72)), 0.34, M['fire'], 7, seg=8, rings=5, rough=0.3, squash=1.2); _halo(fl, c + Vector((0, 0, 1.85)), 1.5, M)
            D._flame_light('brazier_%d' % len(STATE['flames']), tuple(c + Vector((0, 0, 2.0))), FIRE, 520, radius=0.4)
    _obj(mb, 'quay_dress', SET); _obj(fl, 'quay_lamps', SET, shadow=False)

def _gulls(SET, M):
    """Gulls: 9 circling over the basin (wings flap, the flock circles: drivers from the frame number, no keys) + 3 perched."""
    r = _rnd(5)
    for k in range(18):
        mb = MB(); perched = k >= 15; s = 0.55
        body = [Vector((0.6 * s, 0, 0)), Vector((-0.6 * s, 0, 0))]; rod(mb, body[0], body[1], 0.14 * s, M['gull'], seg=6, r1=0.06 * s)
        lumpy(mb, (0.62 * s, 0, 0.08 * s), 0.13 * s, M['gull'], 9, seg=6, rings=4, rough=0.0); rod(mb, (0.74 * s, 0, 0.08 * s), (0.92 * s, 0, 0.05 * s), 0.03 * s, M['gull_y'], seg=3, r1=0.01)
        if perched:
            for sg in (-1, 1): mb.oface([Vector((0.25 * s, sg * 0.14 * s, 0.05)), Vector((-0.8 * s, sg * 0.16 * s, 0.02)), Vector((-0.2 * s, sg * 0.16 * s, 0.12))], M['gull_g'], [(0, 0)] * 3, (0, sg, 0))
        else:
            for sg in (-1, 1):
                mb.oface([Vector((0.25 * s, sg * 0.1 * s, 0)), Vector((-0.15 * s, sg * 0.1 * s, 0)), Vector((-0.05 * s, sg * 0.85 * s, 0.25 * s)), Vector((0.2 * s, sg * 0.85 * s, 0.25 * s))], M['gull'], [(0, 0)] * 4, (0, 0, 1))
                mb.oface([Vector((0.2 * s, sg * 0.85 * s, 0.25 * s)), Vector((-0.05 * s, sg * 0.85 * s, 0.25 * s)), Vector((-0.3 * s, sg * 1.6 * s, -0.05 * s))], M['gull_g'], [(0, 0)] * 3, (0, 0, 1))
        o = _obj(mb, 'gull_%d' % k, SET); o.visible_shadow = not perched and False
        if perched:
            o.location = [(-12.0, -1.4, 1.15), (38.0, -1.4, 1.15), (-35.6, -6.0, 13.2)][k - 15]; o.rotation_euler = (0, 0, r.uniform(0, 6.28))
        else:
            cx, cy, cz, rad, w, ph = r.uniform(-30, 40), r.uniform(-4, 40), r.uniform(12, 26), r.uniform(8, 20), r.uniform(0.012, 0.022) * (1 if k % 2 else -1), r.uniform(0, 6.28)
            for idx, ex in enumerate(('%.2f+%.2f*cos(frame*%.4f+%.3f)' % (cx, rad, w, ph), '%.2f+%.2f*sin(frame*%.4f+%.3f)' % (cy, rad, w, ph), '%.2f+0.8*sin(frame*0.05+%.3f)' % (cz, ph))):
                fc = o.driver_add('location', idx); fc.driver.type = 'SCRIPTED'; fc.driver.expression = ex
            fc = o.driver_add('rotation_euler', 2); fc.driver.type = 'SCRIPTED'; fc.driver.expression = 'frame*%.4f+%.3f+%.3f' % (w, ph, math.pi / 2 if w > 0 else -math.pi / 2)
            fc = o.driver_add('rotation_euler', 0); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '0.25*sin(frame*0.06+%.3f)' % ph
            fc = o.driver_add('scale', 2); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '0.9+0.9*sin(frame*0.55+%.3f)' % (ph * 3)
        STATE['gulls'].append(o)

def _tug(SET, M):
    """A small steam tug crossing the basin (grey, red-banded funnel, smoke)."""
    mb = MB(); F = Frame((70.0, 30.0, WZ), 160.0)
    S = _hull(mb, 18.0, 5.0, 2.4, 1.0, M['ship_dgrey'], M['deck'])
    F2 = Frame((0, 0, 0), 0); F2.box(mb, (-3.0, -1.5, 2.4), (2.5, 1.5, 4.6), M['cream']); F2.box(mb, (-3.0, -1.55, 3.6), (2.5, 1.55, 4.1), M['window'])
    mb.frustum((-1.0, 0, 4.6), (-1.4, 0, 8.6), 0.7, 0.7, M['dark'], seg=10, cap1=False); mb.frustum((-1.2, 0, 7.0), (-1.25, 0, 7.6), 0.72, 0.72, M['red'], seg=10, cap0=False, cap1=False)
    o = _obj(mb, 'tug', SET); o.location = F.o; o.rotation_euler = (0, 0, math.radians(160.0))
    root = bpy.data.objects.new('ship_tug', None); SET.objects.link(root); root.location = F.o; root.rotation_euler = o.rotation_euler; o.location = (0, 0, 0); o.rotation_euler = (0, 0, 0); o.parent = root
    sh = dict(name='tug', root=root, hull=o, L=18.0, B=5.0); _funnel_smoke(sh, Vector((-1.45, 0, 8.6)), M, SET, seed=77, n=6); _bob(sh, 0.6, 9)
    _ship_foam(dict(sh, B=5.0), M, SET)

CARD_ROLES = ('sailor', 'extra_a', 'extra_c', 'boy', 'extra_b')
def _card(role, loc, parent=None, i=0):
    """A small background figure (placeholder cast card) that turns to face the scene camera every frame (_cards_face)."""
    ob = T.placeholder_actor(role, tuple(loc), name='bgcard_%d' % len(STATE.setdefault('cards', [])))
    for c in list(ob.users_collection): c.objects.unlink(ob)
    STATE['SET'].objects.link(ob)
    if parent is not None: ob.parent = parent; ob.location = Vector(loc)
    ob.visible_shadow = True; STATE['cards'].append(ob); return ob

def _cards_face(scene, *args):
    """Handler: every background card yaws to face the scene camera (cards read from any preset)."""
    cam = scene.camera if scene else None
    if cam is None: return
    cp = cam.matrix_world.translation
    for ob in STATE.get('cards', []):
        try:
            p = ob.matrix_world.translation; d = cp - p; yaw = math.atan2(d.x, -d.y)
            if ob.parent is not None: yaw -= ob.parent.matrix_world.to_euler().z
            ob.rotation_euler = (0, 0, yaw)
        except ReferenceError: pass

def _horse_wagon(mb, base, yaw, M):
    """A dray: a brown horse in shafts pulling a flat wagon of barrels."""
    F = Frame(base, yaw)
    lumpy(mb, F.p(2.2, 0, 2.0), 1.0, M['horse'], 3, seg=10, rings=6, rough=0.05, squash=0.55); mb.obj if False else None
    for (x, y) in ((1.6, -0.35), (1.6, 0.35), (2.9, -0.35), (2.9, 0.35)): rod(mb, F.p(x, y, 1.6), F.p(x, y, 0.0), 0.13, M['horse'], seg=5, r1=0.1)
    rod(mb, F.p(3.0, 0, 2.2), F.p(3.6, 0, 3.0), 0.32, M['horse'], seg=6, r1=0.25); F.box(mb, (3.4, -0.22, 2.75), (4.3, 0.22, 3.2), M['horse'])
    rod(mb, F.p(1.25, 0, 2.1), F.p(0.9, 0, 1.2), 0.1, M['horse_d'], seg=4); F.box(mb, (3.3, -0.06, 3.0), (3.8, 0.06, 3.45), M['horse_d'])
    F.box(mb, (-3.6, -1.1, 1.1), (0.4, 1.1, 1.35), M['wood'])
    for x in (-3.0, -0.4):
        for y in (-1.2, 1.2): mb.frustum(F.p(x, y, 0.65), F.p(x, y + (0.15 if y > 0 else -0.15), 0.65), 0.65, 0.65, M['wood_d'], seg=12)
    for y in (-0.55, 0.55): rod(mb, F.p(0.4, y, 1.25), F.p(2.8, y * 0.8, 1.9), 0.06, M['wood_d'], seg=4)
    for k in range(4): _barrel(mb, F.p(-3.0 + (k % 2) * 1.5, -0.5 + (k // 2) * 1.0, 1.35), M, r=0.42, h=1.0)

def _harbour_extras(SET, M, sh):
    """Round-2 detail: water details (shallow tint and a foam slick along the quay wall and the berth hull, floating crates and a
    rope ring), a gangway, dressing-ship bunting, scaffold lanterns, warehouse awnings, roof vents and chimney smoke, a horse dray,
    a net-drying rack, a washing line, extra handcarts and channel buoys, and background workers / deck crew cards."""
    mb = MB(); fl = MB(); r = _rnd(77); B = sh['base']
    w = MB()                                                    # shallow turquoise + foam slick along the wall and the berth hull
    for x0 in range(int(QX[0]), int(QX[1]), 20):
        w.face([Vector((x0, 0.0, WZ + 0.02)), Vector((x0 + 20, 0.0, WZ + 0.02)), Vector((x0 + 20, 7.0, WZ + 0.02)), Vector((x0, 7.0, WZ + 0.02))], M['shallow'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        w.face([Vector((x0, 0.0, WZ + 0.04)), Vector((x0 + 20, 0.0, WZ + 0.04)), Vector((x0 + 20, 0.9, WZ + 0.04)), Vector((x0, 0.9, WZ + 0.04))], M['foam_bow'], [(0, 0.5), (1, 0.5), (1, 0.75), (0, 0.75)])
    yo = B.y + _deck_hb(sh['S'], 0) * 0.92
    w.face([Vector((-30, yo, WZ + 0.02)), Vector((30, yo, WZ + 0.02)), Vector((30, yo + 6, WZ + 0.02)), Vector((-30, yo + 6, WZ + 0.02))], M['shallow'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    w.face([Vector((-30, yo, WZ + 0.04)), Vector((28, yo, WZ + 0.04)), Vector((28, yo + 0.8, WZ + 0.04)), Vector((-30, yo + 0.8, WZ + 0.04))], M['foam_bow'], [(0, 0.5), (1, 0.5), (1, 0.75), (0, 0.75)])
    _obj(w, 'water_detail', SET, shadow=False)
    for (x, y, a) in ((14.0, 22.0, 0.4), (16.2, 24.5, 1.1), (-38.0, 30.0, 0.2), (52.0, 34.0, 0.8)):      # floating crates, half sunk
        obox(mb, (x, y, WZ + 0.1), (math.cos(a), math.sin(a), 0), (-math.sin(a), math.cos(a), 0), (0, 0, 1), 0.65, 0.65, 0.65, M['crate'], 0.25)
    for k in range(16):
        a0, a1 = 2 * math.pi * k / 16, 2 * math.pi * (k + 1) / 16; c = Vector((28.0, 14.0, WZ + 0.08))
        rod(mb, c + Vector((0.9 * math.cos(a0), 0.9 * math.sin(a0), 0)), c + Vector((0.9 * math.cos(a1), 0.9 * math.sin(a1), 0)), 0.12, M['rope'], seg=5)
    for (x, y, g) in ((20.0, 40.0, 0), (-60.0, 38.0, 1), (95.0, 80.0, 0), (-95.0, 92.0, 1)):            # channel buoys
        c = Vector((x, y, WZ)); mb.frustum(c - Vector((0, 0, 0.3)), c + Vector((0, 0, 1.4)), 0.9, 0.6 if g else 0.85, M['buoy_g'] if g else M['red'], seg=10)
        if g: mb.frustum(c + Vector((0, 0, 1.4)), c + Vector((0, 0, 2.4)), 0.6, 0.05, M['buoy_g'], seg=10)
    xa, xb = -21.0, -12.0; ya, yb = -1.6, B.y - _deck_hb(sh['S'], xb) - 0.1; za, zb = 0.0, WZ + _deck_z(sh['S'], xb)   # gangway
    for k in range(10):
        t0, t1 = k / 10, (k + 1) / 10; p0 = Vector((xa + (xb - xa) * t0, ya + (yb - ya) * t0, za + (zb - za) * t0)); p1 = Vector((xa + (xb - xa) * t1, ya + (yb - ya) * t1, za + (zb - za) * t1))
        mb.face([p0 + Vector((0, -0.55, 0.1)), p1 + Vector((0, -0.55, 0.1)), p1 + Vector((0, 0.55, 0.1)), p0 + Vector((0, 0.55, 0.1))], M['planks'], [(0, 0), (1, 0), (1, 0.3), (0, 0.3)])
    for dy in (-0.55, 0.55):
        rod(mb, (xa, ya + dy, za + 1.0), (xb, yb + dy, zb + 1.0), 0.04, M['rope'], seg=3)
        for t in (0.0, 0.5, 1.0): p = Vector((xa + (xb - xa) * t, ya + dy + (yb - ya) * t, za + (zb - za) * t)); rod(mb, p, p + Vector((0, 0, 1.0)), 0.05, M['wood_d'], seg=4)
    fm = Vector((0.27 * 64 - 0.6, B.y, WZ + _deck_z(sh['S'], 0.27 * 64) + 20.0)); stem = Vector((32.0, B.y, WZ + _deck_z(sh['S'], 31.5))); mm_ = Vector((-0.29 * 64 - 0.5, B.y, WZ + 8.6 + 15.0)); stern = Vector((-31.0, B.y, WZ + 9.2))
    cols = ['red', 'flag_y', 'flag_b', 'white']
    for (a, b) in ((fm, stem), (fm, mm_), (mm_, stern)):                                                  # dressing-ship bunting
        pts = catenary(a, b, 1.6, 22)
        for k, p in enumerate(pts[1:-1]):
            q = pts[k + 2]; d = (q - p).normalized(); mb.oface([p, p + d * 0.9, p + d * 0.45 - Vector((0, 0, 1.0))], M[cols[k % 4]], [(0, 0)] * 3, (0, 1, 0)); mb.oface([p, p + d * 0.9, p + d * 0.45 - Vector((0, 0, 1.0))], M[cols[k % 4]], [(0, 0)] * 3, (0, -1, 0))
        chain_rod(mb, pts, 0.02, M['dark'], seg=3)
    for (x, y, z) in ((-25.0, -0.2, 7.4), (-15.0, -0.2, 7.4), (9.0, -0.2, 7.4), (17.0, -0.2, 7.4)):      # scaffold lanterns
        rod(mb, (x, y, z), (x, y, z - 0.6), 0.02, M['dark'], seg=3); fl.frustum((x, y, z - 1.15), (x, y, z - 0.6), 0.16, 0.13, M['lamp_glass'], seg=6); mb.frustum((x, y, z - 0.6), (x, y, z - 0.45), 0.2, 0.05, M['dark'], seg=6)
        if STATE['P'].get('lamps', 0) > 0.2: D._flame_light('lantern_%d' % len(STATE['flames']), (x, y, z - 0.9), LAMP, 90, radius=0.1)
    for (x0, x1) in ((-128.0, -74.0), (-68.0, -14.0), (-8.0, 46.0), (52.0, 98.0), (104.0, 152.0)):        # awnings over the doors, roof vents
        for dx in range(int(x0) + 9, int(x1) - 6, 18):
            am = M['awning'] if (dx // 18) % 2 else M['awning2']
            mb.oface([Vector((dx - 2.2, -36.0, 5.0)), Vector((dx + 2.2, -36.0, 5.0)), Vector((dx + 2.2, -33.6, 4.2)), Vector((dx - 2.2, -33.6, 4.2))], am, [(0, 0)] * 4, (0, 0.3, 1))
            for xx in (dx - 2.1, dx + 2.1): rod(mb, (xx, -33.7, 4.2), (xx, -36.0, 3.0), 0.04, M['dark'], seg=3)
        for xv in np.arange(x0 + 10, x1 - 6, 14.0): mb.box((xv - 1.0, -46.0, 0.0), (xv + 1.0, -44.0, 0.0), M['slate']) if False else None
    for (c, sd) in (((-74.0, -16.0), 3), ((8.0, -12.5), 5), ((70.0, -15.0), 9)):                          # more handcarts with sacks
        hc = Frame((c[0], c[1], 0.0), sd * 30.0); hc.box(mb, (-1.0, -0.6, 0.6), (1.0, 0.6, 0.75), M['wood'])
        for y in (-0.7, 0.7): mb.frustum(hc.p(0, y, 0.45), hc.p(0, y + (0.12 if y > 0 else -0.12), 0.45), 0.45, 0.45, M['wood_d'], seg=10)
        for k in range(3): lumpy(mb, hc.p(-0.5 + k * 0.5, 0, 1.0), 0.35, M['canvas'], 90 + sd + k, seg=7, rings=4, rough=0.15, squash=0.6)
        rod(mb, hc.p(1.0, -0.4, 0.7), hc.p(2.4, -0.4, 0.9), 0.05, M['wood_d'], seg=4); rod(mb, hc.p(1.0, 0.4, 0.7), hc.p(2.4, 0.4, 0.9), 0.05, M['wood_d'], seg=4)
    _horse_wagon(mb, (-46.0, -22.5, 0.0), 0.0, M)
    for x in (-90.0, -84.0): rod(mb, (x, -10.5, 0.0), (x, -10.5, 3.2), 0.07, M['wood_d'], seg=4)                # net-drying rack
    rod(mb, (-90.0, -10.5, 3.2), (-84.0, -10.5, 3.2), 0.05, M['wood_d'], seg=4)
    mb.oface([Vector((-90, -10.5, 3.2)), Vector((-84, -10.5, 3.2)), Vector((-84.3, -9.3, 0.4)), Vector((-89.7, -9.3, 0.4))], M['net'], [(0, 0), (3, 0), (3, 1.4), (0, 1.4)], (0, 1, 0.2))
    mb.oface([Vector((-90, -10.5, 3.2)), Vector((-84, -10.5, 3.2)), Vector((-84.3, -11.7, 0.4)), Vector((-89.7, -11.7, 0.4))], M['net'], [(0, 0), (3, 0), (3, 1.4), (0, 1.4)], (0, -1, 0.2))
    a = Vector((-78.0, -7.0, 2.9)); b = Vector((-70.0, -7.0, 2.9)); pts = catenary(a, b, 0.35, 8); chain_rod(mb, pts, 0.02, M['rope'], seg=3)   # washing line
    rod(mb, (a.x, a.y, 0), a, 0.06, M['wood_d'], seg=4); rod(mb, (b.x, b.y, 0), b, 0.06, M['wood_d'], seg=4)
    for k, p in enumerate(pts[1:-1]):
        cm = M[('cloth_w', 'cloth_b', 'cloth_r', 'cloth_w', 'cloth_b', 'cloth_w', 'cloth_r')[k % 7]]; ww = 0.35 + 0.15 * (k % 2); hh = 0.9 + 0.3 * (k % 3) * 0.5
        for nn in ((0, 1, 0), (0, -1, 0)): mb.oface([p + Vector((-ww, 0, 0)), p + Vector((ww, 0, 0)), p + Vector((ww, 0, -hh)), p + Vector((-ww, 0, -hh))], cm, [(0, 0)] * 4, nn)
    _obj(mb, 'harbour_extras', SET); _obj(fl, 'harbour_extra_lamps', SET, shadow=False)
    croot = bpy.data.objects.new('chimneys_root', None); SET.objects.link(croot)                          # warehouse chimney smoke
    csh = dict(name='chim', root=croot)
    for i, cx in enumerate((-122.0, -2.0, 110.0)): _funnel_smoke(csh, Vector((cx, -45.1, 23.6)), M, SET, seed=300 + i, n=6)
    for i, (role, loc) in enumerate((('sailor', (-58.0, -11.0, 0.0)), ('extra_a', (-55.5, -12.5, 0.0)), ('extra_c', (41.0, -9.0, 0.0)), ('boy', (-44.0, -19.5, 0.0)),
                                     ('sailor', (-22.0, -1.3, 2.59)), ('extra_a', (64.5, -10.6, 0.0)), ('extra_c', (60.0, 106.0, 1.6)), ('sailor', (-8.0, -9.5, 0.0)),
                                     ('extra_b', (-74.0, -8.0, 0.0)), ('extra_c', (-88.0, -8.5, 0.0)), ('sailor', (-17.0, -1.2, 3.0)))):
        _card(role, loc)
    for nm, lx in (('m1', -8.0), ('m2', 6.0)):
        m_ = STATE['ships'][nm]; _card('sailor', (lx, -2.0, 8.6), parent=m_['root']); _card('extra_c', (lx - 9.0, 1.5, 8.6), parent=m_['root'])

def _sea_extras(SET, M):
    """Round-2 detail at sea: gulls riding the swell, channel buoys, distant sailing boats, deck crew cards on the convoy."""
    mb = MB(); r = _rnd(88)
    for k in range(10):                                                                   # gulls sitting on the water
        c = Vector((r.uniform(-90, 60), r.uniform(-110, -20), 0.3)); a = r.uniform(0, 6.28); s = 0.55
        lumpy(mb, c, 0.24, M['gull'], 70 + k, seg=6, rings=4, rough=0.0, squash=0.55); lumpy(mb, c + Vector((0.28 * math.cos(a), 0.28 * math.sin(a), 0.14)), 0.11, M['gull'], 80 + k, seg=6, rings=3, rough=0.0)
        rod(mb, c + Vector((-0.25 * math.cos(a), -0.25 * math.sin(a), 0.05)), c + Vector((-0.55 * math.cos(a), -0.55 * math.sin(a), 0.12)), 0.08, M['gull_g'], seg=4, r1=0.02)
    for (x, y, g) in ((-115.0, -40.0, 1), (70.0, -40.0, 0), (-120.0, 40.0, 0)):
        c = Vector((x, y, 0.0)); mb.frustum(c - Vector((0, 0, 0.6)), c + Vector((0, 0, 1.6)), 1.0, 0.7 if g else 0.95, M['buoy_g'] if g else M['red'], seg=10)
        if g: mb.frustum(c + Vector((0, 0, 1.6)), c + Vector((0, 0, 2.8)), 0.7, 0.05, M['buoy_g'], seg=10)
    for k, (x, y, a) in enumerate(((-260.0, 330.0, 0.3), (210.0, 380.0, 2.8), (40.0, 520.0, 1.2))):       # distant sailing boats
        F = Frame((x, y, 0.0), math.degrees(a)); F.box(mb, (-4.5, -1.2, -0.4), (4.5, 1.2, 1.2), M['wood_d']); rod(mb, F.p(0.5, 0, 1.2), F.p(0.5, 0, 11.0), 0.12, M['wood_d'], seg=4)
        F.quad(mb, [(0.6, 0, 1.6), (0.6, 0, 10.6), (-4.0, 0, 1.6)], M['sail'], [(0, 0)] * 3, (0, 1, 0)); F.quad(mb, [(0.6, 0, 1.6), (0.6, 0, 10.6), (-4.0, 0, 1.6)], M['sail'], [(0, 0)] * 3, (0, -1, 0))
        F.quad(mb, [(0.9, 0, 2.0), (0.9, 0, 9.0), (4.6, 0, 1.4)], M['sail'], [(0, 0)] * 3, (0, 1, 0)); F.quad(mb, [(0.9, 0, 2.0), (0.9, 0, 9.0), (4.6, 0, 1.4)], M['sail'], [(0, 0)] * 3, (0, -1, 0))
    _obj(mb, 'sea_extras', SET)
    for nm, pts in (('dazzle', ((-22.0, 2.0, 8.6), (-14.0, -2.5, 8.6))), ('flag', ((-20.0, 2.5, 8.6),)), ('c1', ((15.0, -1.5, 6.8),)), ('c3', ((-10.0, 2.0, 6.8), (20.0, -1.0, 8.6)))):
        for k, p in enumerate(pts): _card(('sailor', 'extra_c', 'extra_a')[k % 3], p, parent=STATE['ships'][nm]['root'])

def _harbour_marks(sh):
    pl = STATE['planks']['plank']; pb = STATE['planks']['plank_b']; B = sh['base']
    wl = STATE.get('marks_local_berth', {})
    def W(v): return tuple(round(c, 2) for c in (B + v))
    return dict(painter_plank=((pl['x'][0] + pl['x'][1]) / 2 + 0.6, pl['y'] - 0.12, pl['z']), admiral_plank=((pl['x'][0] + pl['x'][1]) / 2 - 0.9, pl['y'] - 0.12, pl['z']),
                painter_plank_b=((pb['x'][0] + pb['x'][1]) / 2, pb['y'] - 0.12, pb['z']),
                painter_quay=(15.6, -4.2, 0.0), admiral_quay=(20.4, -7.0, 0.0), admiral_stride_from=(40.0, -10.0, 0.0), painter_paint=(-1.6, -3.4, 0.0),
                sailor_quay_a=(-9.5, -7.5, 0.0), sailor_quay_b=(-7.6, -9.0, 0.0), sailor_quay_c=(9.5, -8.2, 0.0),
                sailor_deck_a=W(Vector((-14.0, -3.5, _deck_z(sh['S'], -14.0)))), sailor_deck_b=W(Vector((-20.0, -3.2, _deck_z(sh['S'], -20.0)))),
                sailor_scaffold=(-18.0, -1.4, 4.99), painter_scaffold=(12.0, -1.4, 4.99))

# ============================================================================= sea
CONVOY = [('dazzle', 'warship', 64.0, (0.0, 0.0)), ('c1', 'merchant', 60.0, (-150.0, 4.0)), ('c2', 'merchant', 58.0, (115.0, -3.0)),
          ('flag', 'warship', 62.0, (-60.0, 62.0)), ('c3', 'merchant', 62.0, (50.0, 66.0)), ('c4', 'merchant', 56.0, (160.0, 70.0))]
UBOAT = dict(pos=(-55.0, -96.0), yaw=86.0)
LEAD_AHEAD = 16.0                                 # the aim point leads the ship's centre by its travel + 16 D (ahead of the bow)
GHOST_AIM = (-(SEA_V * T_RUN + LEAD_AHEAD), 0.0)   # where the captain aims: ahead of the ghost's bow (the wrong heading, -x)
LEAD = (SEA_V * T_RUN + LEAD_AHEAD, 0.0)          # the right lead point: ahead of the real bow (the gold buoy)

def _swell_group():
    """Geometry nodes: z += three long crossing swells + two short chop waves (faded out beyond the fine-mesh zone so the coarse outer
    cells do not alias) of the world xy and the scene time; smooth shading. Animated by the frame, no keys."""
    ng = bpy.data.node_groups.new('HB_swell', 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes.new; L = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput')
    pos = N('GeometryNodeInputPosition'); sp = N('ShaderNodeSeparateXYZ'); L(pos.outputs[0], sp.inputs[0])
    tm = N('GeometryNodeInputSceneTime')
    def wave(A, lam, ang, spd):
        k = 2 * math.pi / lam; ca, sa = math.cos(math.radians(ang)) * k, math.sin(math.radians(ang)) * k
        m1 = N('ShaderNodeMath'); m1.operation = 'MULTIPLY'; m1.inputs[1].default_value = ca; L(sp.outputs['X'], m1.inputs[0])
        m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY_ADD'; m2.inputs[1].default_value = sa; L(sp.outputs['Y'], m2.inputs[0]); L(m1.outputs[0], m2.inputs[2])
        m3 = N('ShaderNodeMath'); m3.operation = 'MULTIPLY_ADD'; m3.inputs[1].default_value = -spd; L(tm.outputs['Seconds'], m3.inputs[0]); L(m2.outputs[0], m3.inputs[2])
        s_ = N('ShaderNodeMath'); s_.operation = 'SINE'; L(m3.outputs[0], s_.inputs[0])
        a_ = N('ShaderNodeMath'); a_.operation = 'MULTIPLY'; a_.inputs[1].default_value = A; L(s_.outputs[0], a_.inputs[0]); return a_
    def add(a, b): ad = N('ShaderNodeMath'); ad.operation = 'ADD'; L(a.outputs[0], ad.inputs[0]); L(b.outputs[0], ad.inputs[1]); return ad
    sw = add(add(wave(0.30, 34.0, 20.0, 0.9), wave(0.18, 21.0, 75.0, 1.2)), wave(0.11, 13.0, -35.0, 1.6))
    ch = add(add(add(wave(0.05, 7.3, 52.0, 2.2), wave(0.035, 4.9, -67.0, 2.8)), wave(0.025, 3.7, 13.0, 3.3)), wave(0.02, 2.9, 121.0, 3.7))
    ax = N('ShaderNodeMath'); ax.operation = 'ABSOLUTE'; L(sp.outputs['X'], ax.inputs[0])
    ay0 = N('ShaderNodeMath'); ay0.operation = 'ADD'; ay0.inputs[1].default_value = 30.0; L(sp.outputs['Y'], ay0.inputs[0])
    ay = N('ShaderNodeMath'); ay.operation = 'ABSOLUTE'; L(ay0.outputs[0], ay.inputs[0])
    mx = N('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L(ax.outputs[0], mx.inputs[0]); L(ay.outputs[0], mx.inputs[1])
    fz = N('ShaderNodeMapRange'); fz.inputs['From Min'].default_value = 120.0; fz.inputs['From Max'].default_value = 150.0; fz.inputs['To Min'].default_value = 1.0; fz.inputs['To Max'].default_value = 0.0; L(mx.outputs[0], fz.inputs['Value'])
    chf = N('ShaderNodeMath'); chf.operation = 'MULTIPLY'; L(ch.outputs[0], chf.inputs[0]); L(fz.outputs['Result'], chf.inputs[1])
    tot = add(sw, chf)
    cb = N('ShaderNodeCombineXYZ'); L(tot.outputs[0], cb.inputs['Z'])
    setp = N('GeometryNodeSetPosition'); L(gi.outputs[0], setp.inputs['Geometry']); L(cb.outputs[0], setp.inputs['Offset'])
    sm = N('GeometryNodeSetShadeSmooth'); L(setp.outputs[0], sm.inputs['Geometry']); L(sm.outputs[0], go.inputs[0])
    return ng

def _graded(a, b, c0, c1, h, grow=1.09):
    """Coordinates a..b: spacing h inside c0..c1, growing geometrically outside (fine near the action, coarse far off)."""
    xs = list(np.arange(c0, c1 + 1e-6, h)); d = h
    while xs[0] > a: d *= grow; xs.insert(0, max(a, xs[0] - d))
    d = h
    while xs[-1] < b: d *= grow; xs.append(min(b, xs[-1] + d))
    return np.array(xs, 'float64')

def _ocean(SET, M):
    """The animated ocean: a graded triangle grid (1.25 D cells over x -150..150, y -180..120, growing to x -420..460, y -340..440;
    about 250 x 270 verts) with the swell geometry nodes (smooth shaded), and a flat far disc (z -0.6) out to the sky dome."""
    X = _graded(-420.0, 460.0, -150.0, 150.0, 1.6); Y = _graded(-340.0, 440.0, -180.0, 120.0, 1.6); nx, ny = len(X), len(Y)
    gx, gy = np.meshgrid(X, Y); vs = np.stack([gx.ravel(), gy.ravel(), np.zeros(nx * ny)], 1)
    j, i = np.mgrid[0:ny - 1, 0:nx - 1]; a = (j * nx + i).ravel(); b = a + 1; c = a + nx + 1; d = a + nx
    alt = ((i + j) % 2).ravel().astype(bool)
    t1 = np.where(alt[:, None], np.stack([a, b, c], 1), np.stack([a, b, d], 1)); t2 = np.where(alt[:, None], np.stack([a, c, d], 1), np.stack([b, c, d], 1))
    tris = np.concatenate([t1, t2])
    me = bpy.data.meshes.new('ocean'); me.vertices.add(len(vs)); me.vertices.foreach_set('co', vs.astype('float32').ravel())
    me.loops.add(len(tris) * 3); me.loops.foreach_set('vertex_index', tris.astype('int32').ravel())
    me.polygons.add(len(tris)); me.polygons.foreach_set('loop_start', np.arange(0, len(tris) * 3, 3, dtype='int32')); me.polygons.foreach_set('loop_total', np.full(len(tris), 3, 'int32'))
    me.update(); me.validate(); me.materials.append(M['water'])
    ob = bpy.data.objects.new('ocean', me); SET.objects.link(ob)
    md = ob.modifiers.new('swell', 'NODES'); md.node_group = _swell_group()
    mb = MB(); R0, R1 = 330.0, 5000.0; seg = 64
    for k in range(seg):
        a0, a1 = 2 * math.pi * k / seg, 2 * math.pi * (k + 1) / seg
        mb.face([Vector((R0 * math.cos(a0) + 20, R0 * math.sin(a0) + 50, -0.55)), Vector((R1 * math.cos(a0), R1 * math.sin(a0), -0.55)), Vector((R1 * math.cos(a1), R1 * math.sin(a1), -0.55)),
                 Vector((R0 * math.cos(a1) + 20, R0 * math.sin(a1) + 50, -0.55))][::-1], M['water'], [(0, 0)] * 4)
    mb.face([Vector((R0 * math.cos(2 * math.pi * k / seg) + 20, R0 * math.sin(2 * math.pi * k / seg) + 50, -0.6)) for k in range(seg)], M['water'], [(0, 0)] * seg)
    _obj(mb, 'ocean_far', SET, shadow=False)

def _ellip_prism(mb, c, rx, ry, h, mat, top=None, taper=1.0, lean=0.0, seg=16):
    """Streamlined (elliptic, tapering, leaning) prism: conning towers, casings."""
    c = Vector(c); B_ = [c + Vector((rx * math.cos(2 * math.pi * k / seg), ry * math.sin(2 * math.pi * k / seg), 0)) for k in range(seg)]
    T_ = [c + Vector((lean + rx * taper * math.cos(2 * math.pi * k / seg), ry * taper * math.sin(2 * math.pi * k / seg), h)) for k in range(seg)]
    for k in range(seg):
        j = (k + 1) % seg; mb.oface([B_[k], B_[j], T_[j], T_[k]], mat, [(0, 0)] * 4, (B_[k] + B_[j]) / 2 - c)
    mb.oface(T_, top or mat, [(0, 0)] * seg, (0, 0, 1))

def _uboat(SET, M):
    """The U-boat: hull awash (cigar hull, deck casing, saw-tooth net cutter), conning tower with an open bridge, deck gun, the
    periscope (raised with set_uboat), foam washing over the casing and a feather at the periscope."""
    U = UBOAT; mb = MB(); Lh = 34.0
    rings = []
    for t in [-1.0, -0.9, -0.7, -0.4, 0.0, 0.4, 0.7, 0.9, 1.0]:
        r = 1.9 * math.sqrt(max(0.02, 1 - t ** 4)) if t < 1 else 0.08; rings.append((t * Lh / 2, r))
    for (xa, ra), (xb, rb) in zip(rings, rings[1:]): mb.frustum((xa, 0, -0.9), (xb, 0, -0.9), ra, rb, M['sub'], seg=12, cap0=False, cap1=False)
    mb.box((-13.0, -0.9, 0.55), (14.5, 0.9, 0.85), M['sub_d'])
    for k in range(5): mb.oface([Vector((14.5 + k * 0.6, 0, 0.85)), Vector((15.1 + k * 0.6, 0, 0.85)), Vector((15.1 + k * 0.6, 0, 2.4 - k * 0.3))], M['sub_d'], [(0, 0)] * 3, (0, 1, 0))
    rod(mb, (14.5, 0, 2.3), (-12.0, 0, 3.4), 0.03, M['dark'], seg=3)
    _ellip_prism(mb, (0.3, 0, 0.6), 3.4, 1.3, 2.7, M['sub'], top=M['sub_d'], taper=0.82, lean=-0.4)
    _ellip_prism(mb, (-0.9, 0, 3.3), 1.0, 0.75, 0.25, M['sub_d'], top=M['dark'])
    chain_rod(mb, [Vector((-0.1 + 2.6 * math.cos(2 * math.pi * k / 16), 1.0 * math.sin(2 * math.pi * k / 16), 3.75)) for k in range(17)], 0.05, M['dark'], seg=4)
    for k in range(0, 16, 2): rod(mb, (-0.1 + 2.6 * math.cos(2 * math.pi * k / 16), 1.0 * math.sin(2 * math.pi * k / 16), 3.3), (-0.1 + 2.6 * math.cos(2 * math.pi * k / 16), 1.0 * math.sin(2 * math.pi * k / 16), 3.75), 0.04, M['dark'], seg=3)
    rod(mb, (6.0, 0, 0.85), (6.0, 0, 1.5), 0.3, M['sub_d'], seg=8); rod(mb, (6.0, 0, 1.4), (9.0, 0, 1.6), 0.12, M['sub_d'], seg=6)
    root = bpy.data.objects.new('uboat', None); SET.objects.link(root); root.location = (U['pos'][0], U['pos'][1], 0.0); root.rotation_euler = (0, 0, math.radians(U['yaw']))
    o = _obj(mb, 'uboat_hull', SET); o.parent = root
    pm = MB(); rod(pm, (0, 0, 0), (0, 0, 1.0), PERI_R, M['sub_d'], seg=8)
    po = _obj(pm, 'periscope_tube', SET); po.parent = root; po.location = (0.6, 0, 2.6)
    pm2 = MB(); rod(pm2, (0.2, 0, 3.3), (0.2, 0, 5.4), 0.08, M['sub_d'], seg=6); _obj(pm2, 'uboat_mast', SET).parent = root
    hm = MB(); hm.box((-0.22, -0.18, 0.0), (0.3, 0.18, 0.55), M['sub_d']); hm.box((0.29, -0.13, 0.15), (0.33, 0.13, 0.42), M['window'])
    ho = _obj(hm, 'periscope_head', SET); ho.parent = root
    fb = MB(); n = Vector((0, 0, 1))
    for sg in (-1, 1): fb.oface([Vector((0, 0, 0)), Vector((-5.0, sg * 1.8, 0)), Vector((-5.0, sg * 3.0, 0)), Vector((0.3, sg * 0.4, 0))], M['foam_bow'], [(0, 0.3), (1, 0.3), (1, 0.8), (0, 0.6)], n)
    fo = _obj(fb, 'periscope_feather', SET, shadow=False)
    wb = MB()
    for sg in (-1, 1): wb.oface([Vector((Lh / 2 - 1, 0, 0.32)), Vector((-Lh / 2, sg * 2.6, 0.32)), Vector((-Lh / 2, sg * 4.2, 0.32)), Vector((Lh / 2 - 1, sg * 0.6, 0.32))], M['foam_bow'], [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.6)], n)
    wo = _obj(wb, 'uboat_wash', SET, shadow=False); wo.parent = root
    STATE['uboat'] = dict(root=root, hull=o, tube=po, head=ho, feather=fo, wash=wo)

def _torpedo(SET, M):
    """The torpedo (cigar, contra-props) and its bubble wake: a ribbon on the water along the path (A['torpedo_path']), revealed up
    to the torpedo and fading behind it (set_torpedo)."""
    mb = MB(); mb.frustum((-2.6, 0, 0), (2.0, 0, 0), 0.32, 0.32, M['torp'], seg=10, cap0=False, cap1=False); lumpy(mb, (2.0, 0, 0), 0.32, M['torp'], 3, seg=10, rings=5, rough=0.0, squash=1.0)
    mb.frustum((-2.6, 0, 0), (-3.1, 0, 0), 0.32, 0.1, M['torp'], seg=10, cap0=False)
    for k in range(4): a = k * math.pi / 2; mb.oface([Vector((-3.2, 0, 0)), Vector((-3.2, 0.5 * math.cos(a), 0.5 * math.sin(a))), Vector((-3.35, 0.5 * math.cos(a + 0.6), 0.5 * math.sin(a + 0.6)))], M['brass'], [(0, 0)] * 3, (1, 0, 0))
    lumpy(mb, (2.25, 0.0, 0.2), 0.17, M['torp_nose'], 5, seg=8, rings=4, rough=0.0)                              # warm glint on the nose
    for sg in (-1, 1): mb.oface([Vector((3.0, 0, 0.3)), Vector((-6.5, sg * 2.8, 0.3)), Vector((-6.5, sg * 4.4, 0.3)), Vector((3.3, sg * 0.6, 0.3))], M['foam_bow'], [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.6)], (0, 0, 1))
    o = _obj(mb, 'torpedo', SET)
    U = Vector((UBOAT['pos'][0], UBOAT['pos'][1], 0)); yaw = math.radians(UBOAT['yaw']); start = U + Vector((math.cos(yaw), math.sin(yaw), 0)) * 18.0
    G_ = Vector((GHOST_AIM[0], GHOST_AIM[1], 0)); d = (G_ - start).normalized(); end = G_ + d * 70.0
    STATE['torp'] = dict(ob=o, start=start, aim=G_, end=end, u_cross=(G_ - start).length / (end - start).length)
    _torpedo_wake(SET, M)

def _torpedo_wake(SET, M):
    tp = STATE['torp']; a, b = tp['start'], tp['end']; d = (b - a); n = 40; side = d.normalized().cross(Vector((0, 0, 1))); mb = MB(); w0, w1 = 0.7, 2.6
    for k in range(n):
        p0 = a + d * (k / n); p1 = a + d * ((k + 1) / n); ww0 = 4.0; ww1 = ww0
        mb.face([p0 - side * ww0 + Vector((0, 0, 0.42)), p1 - side * ww1 + Vector((0, 0, 0.42)), p1 + side * ww1 + Vector((0, 0, 0.42)), p0 + side * ww0 + Vector((0, 0, 0.42))],
                M['wake_mat'], [(k / n, 0), ((k + 1) / n, 0), ((k + 1) / n, 1), (k / n, 1)])
    old = bpy.data.objects.get('torpedo_wake')
    if old: bpy.data.objects.remove(old, do_unlink=True)
    o = _obj(mb, 'torpedo_wake', SET, shadow=False); tp['wake'] = o

def _buoy(name, c, M, glow, halo, light_rgb, SET):
    """A floating spar buoy (red / white body, a cage, a glowing lamp on top + camera-only halo + a real lamp)."""
    c = Vector(c); mb = MB(); fl = MB()
    mb.frustum(c + Vector((0, 0, -0.4)), c + Vector((0, 0, 1.4)), 1.5, 0.8, M['red'], seg=12); mb.frustum(c + Vector((0, 0, 1.4)), c + Vector((0, 0, 3.4)), 0.8, 0.45, M['white'], seg=12)
    for k in range(4): a = k * math.pi / 2; rod(mb, c + Vector((0.45 * math.cos(a), 0.45 * math.sin(a), 3.4)), c + Vector((0.2 * math.cos(a), 0.2 * math.sin(a), 4.6)), 0.06, M['dark'], seg=4)
    lumpy(fl, c + Vector((0, 0, 5.1)), 0.65, glow, 3, seg=10, rings=6, rough=0.0)
    _halo(fl, c + Vector((0, 0, 5.1)), 6.5, dict(M, halo=halo))
    for sg in (-1, 1): fl.oface([c + Vector((1.2, sg * 0.4, 0.34)), c + Vector((-3.5, sg * 2.4, 0.34)), c + Vector((-3.5, sg * 3.4, 0.34)), c + Vector((1.6, sg * 1.2, 0.34))], M['foam_bow'], [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.6)], (0, 0, 1))
    bo = _obj(mb, name, SET); fo = _obj(fl, name + '_glow', SET, shadow=False)
    L_ = BK._light(name + '_lamp', tuple(c + Vector((0, 0, 5.1))), light_rgb, 2200, radius=0.5, shadow=False)   # not a flame: set_flames must not relight it
    return [bo, fo], L_

def _markers(SET, M):
    """In-world markers only (no lines, arrows or rings): the gold lead buoy ahead of the real bow (where to aim) and the pale-cyan
    buoy ahead of the ghost's bow (where the captain aims)."""
    gb, gl = _buoy('lead_buoy', (LEAD[0], LEAD[1], 0.0), M, M['buoy_glow'], M['halo_gold'], (1.0, 0.75, 0.3), SET)
    cb, cl = _buoy('ghost_buoy', (GHOST_AIM[0], GHOST_AIM[1], 0.0), M, M['buoy_cyan'], M['halo_cyan'], (0.55, 0.9, 1.0), SET)
    STATE['markers'] = dict(buoy=gb, lamp=gl, ghost_buoy=cb, ghost_lamp=cl)

def _sea(SET, P, M, dress):
    _sky(SET, P, M, 5200.0)
    _ocean(SET, M)
    M['wake_mat'] = _mat_wake(STATE['pre'] + 'torp_wake', P, 'foam_bubbles')
    tx = STATE['tx']
    for i, (nm, kind, L, pos) in enumerate(CONVOY):
        if nm == 'dazzle': pm = _mat_paint(STATE['pre'] + 'paint_dazzle', P, tx, 'dz_hero_base', [('dz_hero_l1', 1), ('dz_hero_l2', 2), ('dz_hero_l3', 3)], HX.HERO_L, stage=3.0)
        else:
            var = ('v1', 'v2', 'v3', 'v4', 'v5', 'v6')[i % 6]; pm = _mat_paint(STATE['pre'] + 'paint_' + nm, P, tx, 'dz_%s_base' % var, [], HX.SHIP_LS[var] if kind != 'merchant' else L)
        sh = _ship(nm, kind, L, pm, M, (pos[0], pos[1], 0.0), 0.0, foam=True, smoke=2 if kind == 'warship' else 1)
        _bob(sh, 1.0, i)
    gh = _ship('ghost', 'warship', HX.HERO_L, None, M, (0.0, 0.0, 0.0), 180.0, mats_override=M['ghost'], flag=False)
    STATE['ghost'] = gh; gh['root'].scale = (1.035, 1.06, 1.03)
    gh['hull'].data.materials.append(M['ghost_rim']); md = gh['hull'].modifiers.new('rim', 'SOLIDIFY'); md.thickness = 0.32; md.offset = 1.0
    md.use_flip_normals = True; md.use_rim = False; md.material_offset = len(gh['hull'].data.materials) - 1; md.use_even_offset = True
    _ship_foam(gh, M, SET, mats=(M['ghost_foam_bow'], M['ghost_foam'])); gh['foam'].name = 'foam_ghost'
    STATE['ghost_smoke'] = []
    for fi, f in enumerate(gh['funnels']):
        r = _rnd(500 + fi)
        for k in range(6):
            mb = MB(); lumpy(mb, (0, 0, 0), 1.0, M['ghost'], 600 + 10 * fi + k, seg=10, rings=6, rough=0.18)
            o = _obj(mb, 'ghost_smoke_%d_%d' % (fi, k), SET, shadow=False); o.parent = gh['root']; ss = o.modifiers.new('billow_ss', 'SUBSURF'); ss.levels = ss.render_levels = 2
            for pg in o.data.polygons: pg.use_smooth = True
            STATE['ghost_smoke'].append(dict(ob=o, base=Vector(f) + Vector((0, 0, 0.6)), H=7.0 + r.uniform(0, 3), drift=Vector((-24.0 - r.uniform(0, 6), r.uniform(-2, 2), 0)), size=1.4 + r.uniform(0, 0.6), ph=k / 6))
    _uboat(SET, M); _torpedo(SET, M); _markers(SET, M); _plume(SET, M); _sea_extras(SET, M)
    flag = STATE['ships']['flag']; ml = STATE['marks_local_flag']; dz = STATE['ships']['dazzle']; mld = STATE['marks_local_dazzle']
    def W(sh, v): return tuple(round(c, 2) for c in (sh['base'] + v))
    STATE['marks'].update(admiral_bridge=W(flag, ml['wing_s'] + Vector((0.6, 0.6, 0.0))), painter_bridge=W(flag, ml['wing_s'] + Vector((-2.4, 1.2, 0.0))),
                          admiral_bridge_c=W(flag, ml['bridge'] + Vector((-1.5, -1.6, 0))), painter_deck_dazzle=W(dz, mld['deck_aft']),
                          uboat_captain=tuple(round(c, 2) for c in _uboat_world((-0.9, 0.0, 2.75))))
    for p in ('wing_s', 'bridge'): pass

def _plume(SET, M):
    """The hit on a far grey ship (shot 4): a tall white water column and dark smoke billows at c3 (set_hit)."""
    sh = STATE['ships']['c3']; c = Vector((6.0, -sh['B'] / 2 - 1.5, 0.0)); balls = []
    r = _rnd(17)
    for k in range(14):
        mb = MB(); lumpy(mb, (0, 0, 0), 1.0, M['plume'] if k < 8 else M['smoke'], 40 + k, seg=10, rings=6, rough=0.2)
        o = _obj(mb, 'plume_%d' % k, SET, shadow=False); o.parent = sh['root']; o.hide_render = True
        balls.append(dict(ob=o, c=c + Vector((r.uniform(-2, 2), r.uniform(-1.5, 1.5), 0)), k=k, h=(k / 8.0) if k < 8 else (k - 8) / 6.0, s=r.uniform(3.2, 4.6)))
    STATE['plume'] = balls

# ============================================================================= periscope overlay
def periscope_overlay(on=True, frame=None):
    """The periscope lens view (periscope_pov): a circular black vignette and a thin crosshair with small range ticks, real geometry
    placed just in front of the scene camera (it follows the camera in every frame through a handler). No text."""
    ob = bpy.data.objects.get('periscope_overlay')
    if ob is None:
        if not on: return
        M = STATE['M']; mb = MB(); seg = 96; R0, R1, Rb = 1.0, 6.0, 0.965
        for k in range(seg):
            a0, a1 = 2 * math.pi * k / seg, 2 * math.pi * (k + 1) / seg
            mb.face([Vector((R0 * math.cos(a0), R0 * math.sin(a0), 0)), Vector((R1 * math.cos(a0), R1 * math.sin(a0), 0)), Vector((R1 * math.cos(a1), R1 * math.sin(a1), 0)), Vector((R0 * math.cos(a1), R0 * math.sin(a1), 0))], M['vignette'])
            mb.face([Vector((Rb * math.cos(a0), Rb * math.sin(a0), 0.0005)), Vector((R0 * math.cos(a0), R0 * math.sin(a0), 0.0005)), Vector((R0 * math.cos(a1), R0 * math.sin(a1), 0.0005)), Vector((Rb * math.cos(a1), Rb * math.sin(a1), 0.0005))], M['bezel'])
        w = 0.0042; gap = 0.06
        for (ax, ay) in ((1, 0), (0, 1)):
            for sg in (-1, 1):
                p0 = Vector((ax * sg * gap, ay * sg * gap, 0.001)); p1 = Vector((ax * sg * 0.98, ay * sg * 0.98, 0.001)); s_ = Vector((-ay, ax, 0)) * w
                mb.face([p0 - s_, p1 - s_, p1 + s_, p0 + s_], M['reticle'])
                for t in (0.2, 0.4, 0.6, 0.8):                                               # range ticks (lines, no numbers)
                    q = Vector((ax * sg * t, ay * sg * t, 0.001)); tl = (0.035 if t in (0.4, 0.8) else 0.02)
                    s2 = Vector((ax, ay, 0)) * w; n_ = Vector((-ay, ax, 0)) * tl
                    mb.face([q - s2 - n_, q + s2 - n_, q + s2 + n_, q - s2 + n_], M['reticle'])
        ob = mb.obj('periscope_overlay', STATE['SET'])
        for a in ('visible_shadow', 'visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter'): setattr(ob, a, False)
    ob.hide_render = not on
    if frame is not None: T._key(ob, 'hide_render', frame)
    STATE['pov'] = on
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        if _pov_follow not in h: h.append(_pov_follow)
    _pov_follow(bpy.context.scene)

def _pov_follow(scene, *args):
    """Handler: keep the periscope overlay 0.2 D in front of the scene camera, scaled so the clear circle spans 96 % of the frame width."""
    ob = bpy.data.objects.get('periscope_overlay'); cam = scene.camera if scene else None
    if ob is None or cam is None: return
    d = 0.2; rx, ry = scene.render.resolution_x, scene.render.resolution_y
    half_big = d * (cam.data.sensor_width / 2) / cam.data.lens; half_w = half_big * min(rx, ry) / max(rx, ry) if ry > rx else half_big
    s = half_w * 0.96
    ob.matrix_world = cam.matrix_world @ Matrix.Translation((0, 0, -d)) @ Matrix.Diagonal((s, s, s, 1.0))

# ============================================================================= hooks
def _stage_val(m, v, frame, interp='CONSTANT'): _keyval(m, 'stage', v, frame, interp)

def set_stripes(stage, frame=None, ship=None, interp='LINEAR'):
    """Dazzle stage of the berth ship (harbour) / the dazzle ship (sea): 0 plain grey, 1 zigzag, 2 + staircase, 3 full dazzle.
    Fractions paint the next layer from the stern toward the bow (stage 0.47 = the first zigzag reaches midships, where the hanging
    stage `plank` is). Also accepts set_stripes(ship, stage). ship: 'berth' (harbour) | 'dazzle' (sea) | any ship name. Keys linear
    by default (a stripe being painted), interp='CONSTANT' for a cut."""
    if isinstance(stage, str): stage, ship = (frame if frame is not None else 0.0), stage; frame = None
    ship = ship or ('berth' if STATE['loc'] == 'harbour' else 'dazzle')
    sh = STATE['ships'].get(ship)
    if sh is None or sh.get('paint') is None: return
    _stage_val(sh['paint'], max(0.0, min(3.0, float(stage))), frame, interp); STATE['stripes'] = stage

def set_harbour_dazzle(k, frame=None):
    """The 'thousands' shot: the moored ships (6) and the ships in the roads (12) turn from grey to full dazzle one after another
    (ship i flips once k > (i + 0.5) / 18, basin first); 1 = all dazzle. The berth ship is set by set_stripes only (shot 22: leave
    it at 0, it is the admiral's, the last grey ship). Keys constant."""
    ms = STATE.get('moored', []); n = len(ms); k = float(k)
    for i, sh in enumerate(ms): _stage_val(sh['paint'], 1.0 if k > (i + 0.5) / n else 0.0, frame)
    STATE['harbour_dazzle'] = k

def set_smoke(level, frame=None, speed=1.0):
    """Funnel smoke of every steaming ship (convoy, harbour: m2, m5, the tug): billows rising and streaming aft, 0 none .. 1 .. 1.5.
    Call every frame (keys linear)."""
    if not STATE.get('smoke'): return
    W9._billows(STATE['smoke'], STATE['M']['smoke'], 0.85 * max(0.0, float(level)), level > 0.001, frame, 0.011 * speed)
    if STATE.get('ghost_smoke'):
        W9._billows(STATE['ghost_smoke'], STATE['M']['ghost'], 1.0, level > 0.001, frame, 0.011 * speed)

def set_convoy(s, frame=None):
    """Sea: s seconds of sailing since the torpedo was fired (0 = the moment of the shot, may be negative): every convoy ship at its
    start + (SEA_V x s, 0); the ghost (the captain's wrong guess) sails the other way from the dazzle ship's start: (-SEA_V x s, 0).
    Keys linear."""
    s = float(s)
    for nm, sh in STATE['ships'].items():
        if STATE['loc'] != 'sea' or nm == 'ghost': continue
        sh['root'].location = sh['base'] + Vector((SEA_V * s, 0, 0)); _keyp(sh['root'], 'location', frame)
    g = STATE.get('ghost')
    if g: g['root'].location = g['base'] + Vector((-SEA_V * s + STATE.get('ghost_off', 0.0), 0, 0)); _keyp(g['root'], 'location', frame)
    STATE['s'] = s

def torpedo_u(s):
    """Torpedo path parameter at sea time s (fired at s 0, crosses the course line at the ghost's aim point at s = T_RUN)."""
    return max(0.0, min(1.0, s / T_RUN * STATE['torp']['u_cross']))

def torpedo_pos(u):
    tp = STATE['torp']; return tp['start'].lerp(tp['end'], u)

def set_torpedo(u, frame=None, tail=0.55):
    """The torpedo at u (0 launch at the U-boat's bow .. u_cross at the ghost's aim point, behind the real ship's stern when s = T_RUN
    .. 1 the end of the run): the torpedo just under the surface, its white bubble wake from the launch point up to it, fading over
    `tail` (fraction of the path) behind it. u < 0 hides torpedo and wake. Keys linear."""
    tp = STATE.get('torp')
    if not tp: return
    u = float(u); vis = u >= 0.0; uu = max(0.0, min(1.0, u)); p = torpedo_pos(uu); d = (tp['end'] - tp['start']).normalized()
    o = tp['ob']; o.location = p + Vector((0, 0, 0.32)); o.rotation_euler = (0, 0, math.atan2(d.y, d.x)); _keyp(o, 'location', frame); _keyp(o, 'rotation_euler', frame)
    T._show([o, tp['wake']], vis, frame)
    m = STATE['M']['wake_mat']; _keyval(m, 'head', uu, frame); _keyval(m, 'tail', tail, frame)
    STATE['torp_u'] = uu

def set_ghost(k, frame=None, offset=None):
    """The ghost ship (the captain's wrong reading): a translucent (body alpha ~0.4) pale-cyan copy of the dazzle ship heading -x,
    with an emissive silhouette rim, its own pale-cyan bow wave / wake and smoke streaming the other way. k = opacity 0..1 (keys
    linear). Its position follows set_convoy (-SEA_V x s); offset (D along x, kept until changed) slides it, e.g. -18 for
    periscope_pov so its bow sticks out ~28 % past the real stern."""
    g = STATE.get('ghost')
    if not g: return
    if offset is not None: STATE['ghost_off'] = float(offset); set_convoy(STATE.get('s', 0.0), frame)
    k = max(0.0, min(1.0, float(k)))
    for mn in ('ghost', 'ghost_rim', 'ghost_foam', 'ghost_foam_bow'): _keyval(STATE['M'][mn], 'gk', k, frame)
    objs = [o for o in bpy.data.objects if o.parent in (g['root'], g['hull'])] + [g['hull']]
    T._show(objs, k > 0.001, frame)

def set_ghost_marker(k, frame=None):
    """The pale-cyan buoy ahead of the ghost's bow: where the captain aims (the torpedo runs at it and reaches it at s = T_RUN).
    0 hidden .. 1."""
    mk = STATE.get('markers')
    if not mk: return
    k = max(0.0, float(k)); T._show(mk['ghost_buoy'], k > 0.001, frame)
    mk['ghost_lamp'].data.energy = 2200 * k; _keyp(mk['ghost_lamp'].data, 'energy', frame); _keyval(STATE['M']['halo_cyan'], 'cyan_k', 1.2 * k, frame)

def set_lead_marker(k, frame=None):
    """The right lead point: the glowing gold buoy (+ halo, gold ring on the water, lamp) ahead of the dazzle ship's bow, where the
    ship will be when a torpedo fired at s 0 arrives. 0 hidden .. 1 (keys: constant visibility, linear glow)."""
    mk = STATE.get('markers')
    if not mk: return
    k = max(0.0, float(k)); T._show(mk['buoy'], k > 0.001, frame)
    mk['lamp'].data.energy = 2200 * k; _keyp(mk['lamp'].data, 'energy', frame)
    _keyval(STATE['M']['halo_gold'], 'gold_k', 1.4 * k, frame)

def set_aim_lines(true_k=1.0, ghost_k=0.0, frame=None):
    """REMOVED in round 3 (QA-art: no 2D infographic lines / arrows / rings). Kept as a no-op so old calls do not break; use the
    buoys (set_lead_marker, set_ghost_marker) and the torpedo + wake."""
    return None

def set_uboat(dive=0.0, frame=None, periscope=1.0):
    """The U-boat: dive 0 = hull awash with the conning tower up .. 1 = under (only the periscope cuts the water, with its foam
    feather). periscope 0..1 = how far the periscope is raised (its head stays ~2.2 D above the water when up). Keys linear."""
    u = STATE.get('uboat')
    if not u: return
    dive = max(0.0, min(1.0, float(dive))); pk = max(0.0, min(1.0, float(periscope)))
    r = u['root']; r.location.z = -5.2 * dive; _keyp(r, 'location', frame)
    top = 2.6 + (5.2 * dive + 2.2) * pk - 0.0                                               # head height in root space
    tube_len = max(0.05, top - 2.6); u['tube'].scale = (1, 1, tube_len); _keyp(u['tube'], 'scale', frame)
    u['head'].location = (0.6, 0, top); _keyp(u['head'], 'location', frame)
    f = u['feather']; w = Vector((r.location.x, r.location.y, 0)) + Vector((math.cos(r.rotation_euler.z), math.sin(r.rotation_euler.z), 0)) * 0.6
    f.location = (w.x, w.y, 0.34); f.rotation_euler = (0, 0, r.rotation_euler.z); _keyp(f, 'location', frame)
    T._show([f], pk > 0.05 and dive > 0.15, frame); T._show([u['wash']], dive < 0.6, frame)
    STATE['uboat_state'] = (dive, pk)

def periscope_eye():
    """World point of the periscope eye (head) and the U-boat's heading, for the periscope_pov camera."""
    u = STATE['uboat']; bpy.context.view_layer.update(); return u['head'].matrix_world @ Vector((0.25, 0, 0.3))

def set_hit(t, frame=None):
    """The torpedo hit on a far grey ship (shot 4): t 0..0.1 a white water column shoots up beside the ship, 0.1..0.6 it hangs and
    collapses; dark smoke billows from 0.15 rise and swell (hold at 1). t < 0 hidden. No fire, no wreck. Keys linear."""
    t = float(t)
    for b in STATE.get('plume', []):
        o = b['ob']
        if b['k'] < 8:
            up = min(1.0, t / 0.12) if t >= 0 else 0; fall = max(0.0, (t - 0.25) / 0.45); h = 30.0 * b['h'] * up * (1 - 0.7 * fall)
            o.location = b['c'] + Vector((0, 0, h + 1.0)); s = b['s'] * (0.5 + 0.7 * up) * (1 - 0.5 * fall); vis = 0 <= t < 0.75
        else:
            tt = max(0.0, t - 0.15 - 0.05 * b['h'] * 6) ; h = 4 + 16 * min(1.0, tt / 0.7) * (0.5 + b['h']); o.location = b['c'] + Vector((-6 * tt, 0, h))
            s = b['s'] * (0.6 + 1.4 * min(1.0, tt / 0.6)); vis = t > 0.15 + 0.05 * b['h'] * 6
        o.scale = (max(0.01, s),) * 3; _keyp(o, 'location', frame); _keyp(o, 'scale', frame); T._show([o], vis, frame)

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials, compositor), so plain set_* calls hold again. Unlike the film-8/9
    version it keeps the DRIVERS (ship bob, gull flight): only the keyed actions are removed."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights):
        ad = idb.animation_data
        if ad and ad.action: ad.action = None
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()
    ng = bpy.context.scene.compositing_node_group
    if ng is not None and ng.animation_data: ng.animation_data_clear()

def ship_root(name):
    """The root empty of a ship (parent actor cards to it so they sail and keep their deck spot)."""
    return STATE['ships'][name]['root']

def apply_preset_state(preset):
    PR = PRESETS[preset]
    set_smoke(1.0)
    if PR['loc'] == 'harbour':
        set_stripes(PR.get('stripes', 1.0)); set_harbour_dazzle(0.0)
        if PR.get('state'): apply_spec_state(PR['state'])
    else:
        STATE['ghost_off'] = 0.0; set_convoy(0.0); set_torpedo(-1); set_ghost(0.0); set_lead_marker(0.0); set_ghost_marker(0.0); set_uboat(0.0); set_hit(-1); set_stripes(3.0)
        periscope_overlay(False)
        apply_spec_state(PR.get('state', ''))
    set_flames(1.0)

# ============================================================================= cameras, anchors, staging
def _uboat_world(v):
    U = UBOAT; a = math.radians(U['yaw']); return Vector((U['pos'][0] + v[0] * math.cos(a) - v[1] * math.sin(a), U['pos'][1] + v[0] * math.sin(a) + v[1] * math.cos(a), v[2]))

def torpedo_cam(u, back=15.0, up=4.6, ahead=45.0, lens=22):
    """Camera setup low behind the torpedo at u (torpedo_chase follows it: call per frame)."""
    tp = STATE['torp']; p = torpedo_pos(u); d = (tp['end'] - tp['start']).normalized()
    return dict(loc=tuple(p - d * back + Vector((0, 0, up))), look_at=tuple(p + d * ahead + Vector((0, 0, 1.4))), lens=lens)

def _sea_cams():
    eye = _uboat_world((1.45, 0, 2.6 + 2.2 + 0.32))
    fb = Vector(CONVOY[3][3] + (0,)); A_ = fb + Vector((0.17 * 62 + 0.6, -(0.5 * 11 * 62 / 64 + 0.2) + 0.6, 8.6 + 3.45))   # admiral_bridge (feet)
    tgt = Vector((4.0, 0.0, 5.0)); d = (tgt - A_); d.z = 0; d.normalize(); perp = Vector((-d.y, d.x, 0))
    cam_b = A_ - d * 5.2 - perp * 1.5 + Vector((0, 0, 3.0))
    return dict(convoy_wide=dict(loc=(-65.0, -117.0, 15.0), look_at=(-11.0, 49.0, 1.0), lens=22),
                periscope_close=dict(loc=tuple(_uboat_world((-8.0, -8.5, 1.4))), look_at=tuple(_uboat_world((3.0, 1.5, 3.6))), lens=22),
                periscope_pov=dict(loc=tuple(eye), look_at=(-8.0, 0.0, 5.0), lens=30),
                topdown_sea=dict(loc=(-3.0, -86.0, 100.0), look_at=(-2.0, 12.0, 0.0), lens=22),
                torpedo_chase=dict(loc=(0, 0, 0), look_at=(0, 1, 0), lens=22),
                beauty_sea=dict(loc=(64.0, -56.0, 6.0), look_at=(4.0, 2.0, 7.0), lens=22),
                bridge_deck=dict(loc=tuple(cam_b), look_at=tuple(tgt + Vector((14.0, 0, -3.0))), lens=24))
CAMS = dict(
    harbour=dict(harbour_wide=dict(loc=(-46.0, -33.0, 30.0), look_at=(10.0, 24.0, 0.0), lens=20),
                 hull_side=dict(loc=(-30.0, -10.0, 9.0), look_at=(14.0, 7.0, 4.0), lens=22),
                 quay_low=dict(loc=(10.5, -17.5, 1.7), look_at=(22.5, -3.0, 3.8), lens=24),
                 hull_plank=dict(loc=(-1.5, -10.0, 3.6), look_at=(-2.4, 1.2, 4.6), lens=24),
                 beauty_harbour=dict(loc=(-44.0, -22.0, 13.0), look_at=(12.0, 22.0, 1.0), lens=20)),
)
CAM_NOTES = dict(
    harbour_wide='high crane over the warehouses: the quay with cranes, scaffold and paint, the berth ship along it, the basin with the moored ships, the breakwater and lighthouse, the town ring',
    hull_side='medium along the berth hull from the quay: scaffold lifts, ladders, hanging stages, the stripes receding toward the bow',
    quay_low='low two-shot on the quay (eye ~1.5 D): the admiral and the painter, the striped hull right, the basin with the grey ships behind',
    hull_plank='the painter (or the admiral) on the hanging stage against the hull: buckets, brush, the stripe being painted',
    beauty_harbour='beauty: the dockyard at golden DUSK light from a lower crane: dazzle ship at the quay, half the harbour dazzled, lamps, braziers, the church on the headland',
    convoy_wide='high wide from behind the U-boat: the periscope cuts the water in the foreground, the convoy in two columns with bow waves and smoke',
    periscope_close='low at the water by the U-boat: the conning tower and the raised periscope, the convoy beyond (the captain stands on the conning tower)',
    periscope_pov='through the periscope: circular black vignette + crosshair, the dazzle ship (pan the camera to sweep the convoy)',
    topdown_sea='high oblique over the encounter: U-boat, torpedo path, the real ship, the ghost, the lead buoy, the wake crossing behind the stern',
    torpedo_chase='low behind the running torpedo (use torpedo_cam(u) per frame), its bubble wake racing toward the dazzle ship',
    bridge_deck='on the flagship bridge wing: the admiral with binoculars, the convoy and the dazzle ship out to starboard',
    beauty_sea='beauty: a low 3/4 view of the hero dazzle ship from ahead to starboard in full sun, bow wave, smoke, the convoy beyond',
)
HEIGHT = dict(painter=3.0, admiral=3.3, sailor=2.9, captain=3.0)
T.PH.update(
    painter=('beach_man', dict(yaw=0.25, expr='happy', arm_l='down', arm_r='down', legs='stand'), HEIGHT['painter']),
    admiral=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), HEIGHT['admiral']),
    sailor=('senior_a', dict(yaw=0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), HEIGHT['sailor']),
    captain=('senior_b', dict(yaw=-0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), HEIGHT['captain']))
placeholder_actor = T.placeholder_actor

STAGING = dict(
    harbour_wide=[('painter', 'painter_quay'), ('admiral', 'admiral_quay'), ('sailor', 'sailor_quay_a'), ('sailor', 'sailor_deck_a')],
    hull_side=[('painter', 'painter_scaffold'), ('sailor', 'sailor_quay_a')],
    quay_low=[('admiral', 'admiral_quay'), ('painter', 'painter_quay')],
    hull_plank=[('painter', 'painter_plank')], beauty_harbour=[('painter', 'painter_quay'), ('admiral', 'admiral_quay')],
    convoy_wide=[], periscope_close=[('captain', 'uboat_captain')], periscope_pov=[], topdown_sea=[], torpedo_chase=[],
    bridge_deck=[('admiral', 'admiral_bridge')], beauty_sea=[],
)

def _staging(cam_name):
    return [(role, tuple(STATE['marks'][mk]) if isinstance(mk, str) else tuple(mk)) for role, mk in STAGING.get(cam_name, [])]

def anchors():
    P = STATE['P']; loc = STATE['loc']; cams = {k: dict(v) for k, v in (CAMS['harbour'] if loc == 'harbour' else _sea_cams()).items()}
    PR = PRESETS[STATE['preset']]
    if loc == 'sea': cams['torpedo_chase'] = torpedo_cam(0.35)
    A = dict(location=loc, preset=STATE['preset'], light=STATE['light'], cams=cams, cam=dict(cams[PR['cam']]), cam_name=PR['cam'], cam_notes={k: CAM_NOTES.get(k, '') for k in cams},
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()),
             sun_elevation_deg=P['sun_elev'], heights=dict(HEIGHT), marks=dict(STATE.get('marks', {})), lights=[o.name for o in STATE['LIGHTS'].objects],
             staging={k: _staging(k) for k in cams}, ships={k: dict(root=v['root'].name, L=v['L'], base=tuple(round(c, 2) for c in v['base'])) for k, v in STATE['ships'].items()})
    if loc == 'harbour':
        A.update(water_z=WZ, floor_z=0.0, planks={k: dict(v) for k, v in STATE['planks'].items()}, berth=dict(root='ship_berth', centre=BERTH, L=HX.HERO_L),
                 keep_out='water y > 0 (quay edge y 0); berth hull y 1.0..12.8, x -32..32; scaffolds x -27.3..-8.7 and 6.7..19.3, y -2.6..0.2; cranes x +-3 round -56 / 38 / 96 / -96, y -8.6..-3.8; warehouses y < -36')
    else:
        tp = STATE['torp']
        A.update(water_z=0.0, sea_speed=SEA_V, t_run=T_RUN, torpedo_path=[tuple(round(c, 2) for c in tp['start']), tuple(round(c, 2) for c in tp['aim']), tuple(round(c, 2) for c in tp['end'])],
                 torpedo_u_cross=round(tp['u_cross'], 4), lead_point=LEAD, ghost_aim=GHOST_AIM, uboat=dict(UBOAT), periscope_eye=tuple(round(c, 2) for c in periscope_eye()))
    return A

def stage_placeholders(A, cam_name, cam_loc):
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(cam_name):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px)] at 720x1280 (caption rule: chin < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        h = HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(round(v, 2) for v in mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def apply_spec_state(state):
    """CLI state strings (comma separated): st<k> stripes, hd<k> harbour dazzle, s<sec> convoy time (+ torpedo at torpedo_u(s) when
    s > 0), tu<u> torpedo, gh<k> ghost, lead<k> buoy, aim<t>/<g> aim lines, dive<k> U-boat, peri<k> periscope, hit<t>, smoke<k>,
    pov1 periscope overlay."""
    for tok in [s for s in (state or '').split(',') if s]:
        if tok.startswith('st'): set_stripes(float(tok[2:]))
        elif tok.startswith('hd'): set_harbour_dazzle(float(tok[2:]))
        elif tok.startswith('smoke'): set_smoke(float(tok[5:]))
        elif tok.startswith('s'): s = float(tok[1:]); set_convoy(s); set_torpedo(torpedo_u(s) if s > 0 else -1)
        elif tok.startswith('tu'): set_torpedo(float(tok[2:]))
        elif tok.startswith('go'): set_ghost(STATE.get('ghost_k', 0.0), offset=float(tok[2:]))
        elif tok.startswith('gh'): set_ghost(float(tok[2:])); STATE['ghost_k'] = float(tok[2:])
        elif tok.startswith('gb'): set_ghost_marker(float(tok[2:]))
        elif tok.startswith('lead'): set_lead_marker(float(tok[4:]))
        elif tok.startswith('aim'): pass                                     # removed (round 3)
        elif tok.startswith('dive'): set_uboat(float(tok[4:]), periscope=STATE.get('uboat_state', (0, 1))[1])
        elif tok.startswith('peri'): set_uboat(STATE.get('uboat_state', (0, 1))[0], periscope=float(tok[4:]))
        elif tok.startswith('hit'): set_hit(float(tok[3:]))
        elif tok.startswith('pov'): periscope_overlay(tok[3:] == '1')

def cli_render(specs=None, quality='final', outdir=None, actors=True):
    """specs: ['preset' | 'preset:LIGHT' | 'preset:LIGHT:state' | 'preset:LIGHT:state:cam']"""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        parts = spec.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None; st = parts[2] if len(parts) > 2 else ''
        A = build(None, pr, light=lt); sc = bpy.context.scene; setup_render(sc, quality)
        apply_spec_state(st)
        nm = parts[3] if len(parts) > 3 and parts[3] else A['cam_name']
        cs = torpedo_cam(STATE.get('torp_u', 0.35)) if nm == 'torpedo_chase' else A['cams'][nm]
        make_camera(cs)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm)
        tag = '%s_%s' % (pr if nm == A['cam_name'] else nm, A['light']) + ('_' + st.replace(',', '_').replace('/', '-') if st else '')
        w, c = T.render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(c, 1), hp)
        print('%s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'):
        cli_render(arg or None, 'final' if cmd == 'final' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
    elif cmd == 'digest':
        A = build(None, arg[0] if arg else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)
