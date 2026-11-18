#!/usr/bin/env python3
"""chicago.py : set of film 13 ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) as a real 3D Blender set (bpy 5.3, Cycles CPU).
STYLE-BOARD build: three locations, built by preset.

    import chicago as C
    A = C.build('street_wide')            # street_wide | hotel_front | front_stair | mud_low   (location 'street', light DAY)
    A = C.build('under_wide')             # under_wide | jack_close                             (location 'under', light CELLAR)
    A = C.build('suite_window')           # suite_window | tea_close                            (location 'suite', light SUITE)
    cam = C.make_camera(A['cam']); C.set_lift(0.5)   # hotel up 0..1 -> 0..LIFT_MAX D (street only)

World: 1 unit = 1 D (head), Z up. NO depth of field, NO text. See API.md.  CLI: python3 chicago.py stills|final [preset ...]"""
import os, sys, math, json, time, random
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d10'), os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'),
          os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import desert as D                                         # noqa: E402
import wall as W9                                          # noqa: E402
import chicago_tex as CX                                   # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, chain_rod, catenary, _obj, _untoon, _glossy   # noqa: E402,F401
STATE = T.STATE
Frame = BK.Frame; _halo = BK._halo; set_flames = D.set_flames
WORK = os.path.join(HERE, 'work')
def _rnd(seed): return random.Random(seed)
LAMP = (1.0, 0.66, 0.36)
LIFT_MAX = 6.0          # D: set_lift(1.0)
FILL_MAX = 3.0          # D: set_fill(1.0)
GF = 2.6                # hotel plinth top (main floor level) above the foundation bottom (z 0 at lift 0)
STOREYS = [6.2, 5.5, 5.5, 5.2, 5.0, 4.6]
ZS = [GF + sum(STOREYS[:i]) for i in range(7)]     # floor levels; ZS[6] = top of the wall
HX0, HX1, HY1 = -20.0, 20.0, 30.0                  # hotel footprint x, depth
NB = 7                                             # bays

# ----------------------------------------------------------------------------- light presets
_kdaz = W9._kdaz
_B = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.6, lamps=0.0, refl_k=0.75)
LIGHTS = dict(
    DAY=dict(_B, lamps=0.6, key=(1.95, 1.42, 0.82), key_dir=_kdaz(325, 33), sun_elev=33, shade=(0.10, 0.105, 0.31), shade_tint=(0.095, 0.10, 0.33), shade_mix=0.55,
             grade_offset=(-0.006, -0.01, -0.014), lift=(0.008, 0.008, 0.02), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.2,
             bounce=(1.0, 0.62, 0.34, 0.26), beams=0.04, air=('#f2c88c', 0.30, 50.0, 520.0)),
    CELLAR=dict(_B, key=(1.95, 1.34, 0.72), key_dir=_kdaz(342, 27), sun_elev=27, shade=(0.092, 0.108, 0.30), shade_tint=(0.088, 0.104, 0.34), shade_mix=0.6,
                grade_offset=(-0.006, -0.01, -0.012), lift=(0.008, 0.012, 0.028), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.2,
                bounce=None, beams=0.0, air=('#d8b090', 0.12, 20.0, 160.0), lamps=1.0),
    SUITE=dict(_B, key=(1.95, 1.42, 0.82), key_dir=_kdaz(305, 36), sun_elev=36, shade=(0.20, 0.19, 0.55), shade_tint=(0.19, 0.18, 0.55), shade_mix=0.6,
               grade_offset=(-0.006, -0.01, -0.012), lift=(0.012, 0.01, 0.026), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.2,
               bounce=None, beams=0.03, air=('#f2c88c', 0.20, 60.0, 520.0), lamps=1.0),
)
PRESETS = dict(
    street_wide=dict(loc='street', light='DAY', cam='street_wide', state='lift0.5'),
    hotel_front=dict(loc='street', light='DAY', cam='hotel_front', state='lift0.5'),
    front_stair=dict(loc='street', light='DAY', cam='front_stair', state='lift1'),
    mud_low=dict(loc='street', light='DAY', cam='mud_low', state='lift0.3'),
    under_wide=dict(loc='under', light='CELLAR', cam='under_wide', state=''),
    jack_close=dict(loc='under', light='CELLAR', cam='jack_close', state=''),
    suite_window=dict(loc='suite', light='SUITE', cam='suite_window', state=''),
    tea_close=dict(loc='suite', light='SUITE', cam='tea_close', state=''),
)
CAMS = dict(
    street_wide=dict(loc=(-16.0, -58.0, 2.4), look_at=(2.0, 0.0, 15.0), lens=22),
    hotel_front=dict(loc=(-8.0, -30.0, 2.4), look_at=(0.0, 0.0, 15.0), lens=22),
    front_stair=dict(loc=(2.0, -16.0, 3.0), look_at=(0.0, 0.0, 6.0), lens=24),
    mud_low=dict(loc=(-12.0, -40.0, 1.1), look_at=(4.0, -6.0, 7.0), lens=22),
    under_wide=dict(loc=(5.0, -2.0, 2.5), look_at=(9.0, 30.0, 2.9), lens=22),
    jack_close=dict(loc=(4.0, 8.0, 2.0), look_at=(8.0, 20.0, 2.4), lens=24),
    suite_window=dict(loc=(4.6, 10.2, 32.2), look_at=(-0.4, 0.0, 30.9), lens=22),
    tea_close=dict(loc=(-1.5, 9.5, 30.9), look_at=(-2.2, 5.0, 30.3), lens=26),
)
CAM_NOTES = dict(street_wide='eye-to-low 22 mm, hotel up 0.5: cribbing and jacks under the ground floor, cart in the mud, spire far right',
                 under_wide='inside the crawlspace looking down the jack rows, sun comes in from the open right side',
                 suite_window='top-floor suite, armchair and tea table, tall window down to the street')

# ----------------------------------------------------------------------------- mesh helpers
def grid_mesh(name, xs, ys, Z, mat, uvs=(0.1, 0.1), smooth=True, coll=None):
    """Shared-vertex smooth height-field mesh from numpy arrays xs (nx), ys (ny), Z (ny, nx); UV = (x, y) * uvs."""
    ny, nx = Z.shape; X, Y = np.meshgrid(xs, ys); V = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    idx = np.arange(ny * nx).reshape(ny, nx); F = np.stack([idx[:-1, :-1].ravel(), idx[:-1, 1:].ravel(), idx[1:, 1:].ravel(), idx[1:, :-1].ravel()], 1)
    me = bpy.data.meshes.new(name); me.from_pydata(V.tolist(), [], F.tolist()); me.update()
    uvl = me.uv_layers.new(name='UVMap'); uv = np.stack([X.ravel() * uvs[0], Y.ravel() * uvs[1]], 1)[F.ravel()]; uvl.data.foreach_set('uv', uv.ravel())
    me.materials.append(mat); me.polygons.foreach_set('use_smooth', [smooth] * len(me.polygons))
    ob = bpy.data.objects.new(name, me); (coll or STATE['SET']).objects.link(ob); no_bounce(ob); ob.visible_glossy = True
    return ob

def ell(mb, c, rx, ry, rz, mat, seg=10, rings=6, yaw=0.0, pitch=0.0):
    """Faceted ellipsoid centred c with radii (rx, ry, rz), rotated by yaw about z and pitch about x."""
    c = Vector(c); R = []; mb.pid += 1; rot = Matrix.Rotation(yaw, 3, 'Z') @ Matrix.Rotation(pitch, 3, 'X')
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; row.append(c + rot @ Vector((rx * math.sin(th) * math.cos(ph), ry * math.sin(th) * math.sin(ph), -rz * math.cos(th))))
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat, [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)])

def sbox(mb, lo, hi, mat, uvk=0.17):
    """axis box with world-ish UV (0..size*uvk) on every face (uniform tiling in D)."""
    c = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
    obox(mb, c, (1, 0, 0), (0, 1, 0), (0, 0, 1), (hi[0] - lo[0]) / 2, (hi[1] - lo[1]) / 2, (hi[2] - lo[2]) / 2, mat, uvk)

def prism_roof(mb, x0, x1, y0, y1, z, h, mat, uvk=0.17):
    """gabled roof ridge along x."""
    ym = (y0 + y1) / 2
    mb.oface([(x0, y0, z), (x1, y0, z), (x1, ym, z + h), (x0, ym, z + h)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -h, (y1 - y0) / 2))
    mb.oface([(x0, y1, z), (x1, y1, z), (x1, ym, z + h), (x0, ym, z + h)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, h, (y1 - y0) / 2))

def _tex_node(m): return [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]

# ----------------------------------------------------------------------------- build
def build(preset='street_wide', clear=True, light=None):
    assert preset in PRESETS, 'preset %s not in %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; loc = PR['loc']; lkey = light or PR['light']; scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    STATE.clear(); STATE.update(P=P, preset=preset, loc=loc, area=loc, light=lkey)
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_sun_screen', '_cards_face'): h.remove(f)
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('CH_', 'ink')): bpy.data.materials.remove(m)
    tx = CX.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_chicago') or bpy.data.worlds.new('W_chicago'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'CH_%s_%s_' % (loc, lkey); FORM = tuple(P['form'])
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
    STATE.update(flames=[], flame_mats=list(M['_flame_mats']), marks={}, cards=[], lift_movers=[], lift_stretch=[], lift_mid=[], fill_objs=[], crib_layers=[], steps=[])
    if loc == 'street': _street(SET, P, M)
    elif loc == 'under': _under(SET, P, M)
    else: _suite(SET, P, M)
    scene.cycles.use_light_tree = False
    MN._denoise(scene); setup_grade(scene); W9._air_comp(scene, P)
    for ob in SET.objects:
        no_bounce(ob)
        if loc == 'street' or ob.name in ('sky', 'floor', 'rug'): ob.visible_glossy = True
    if 'sky_obj' in STATE: STATE['sky_obj'].visible_glossy = True
    set_flames(1.0)
    apply_state(PR.get('state', ''))
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    MN.setup_render(scene, quality); scene.cycles.transparent_max_bounces = 24
    if STATE.get('loc') in ('street',): scene.cycles.glossy_bounces = 1

def make_camera(setup, name='cam', scene=None):
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 6000.0; ob.data.dof.use_dof = False; return ob

# ============================================================================= materials
def _materials(P, C, TX, tx, pre):
    lk = max(P.get('lamps', 0.0), 0.0)
    M = dict(brick=TX('brick_a'), brick_b=TX('brick_b'), brick_c=TX('brick_c'), brick_d=TX('brick_d'), brick_e=TX('brick_e'), ash=TX('ash'), rustic=TX('rustic'), stone_grey=TX('stone_grey'),
             walk=TX('plank_walk'), plank_d=TX('plank_dark'), plank_f=TX('plank_floor'), crate=TX('crate'), timber=TX('timber'), timber_d=TX('timber_d'), timber_w=TX('timber_w'),
             clap_ochre=TX('clap_ochre'), clap_teal=TX('clap_teal'), clap_cream=TX('clap_cream'), clap_green=TX('clap_green'), clay=TX('clay', form=False), gravel=TX('gravel', form=False),
             win_dark=TX('win_dark'), win_lit=TX('win_lit', glow='win_lit', glow_k=1.0), win_curt=TX('win_curt'), win_lit2=TX('win_lit2', glow='win_lit2', glow_k=1.0),
             win_dark_short=TX('win_dark_short'), win_lit_short=TX('win_lit_short', glow='win_lit_short', glow_k=1.0), win_dark_big=TX('win_dark_big'), win_lit_big=TX('win_lit_big', glow='win_lit_big', glow_k=1.1),
             win_base=TX('win_dark_base'), fac_a=TX('fac_a'), fac_b=TX('fac_b'), fac_c=TX('fac_c'), fac_d=TX('fac_d'), fac_e=TX('fac_e'), fac_f=TX('fac_f'),
             awn_rc=TX('awn_rc', sm=(1.2, 0.9, 0.8), smix=0.3), awn_tc=TX('awn_tc', smix=0.3), awn_oc=TX('awn_oc', smix=0.3),
             wallpaper=TX('wallpaper'), parquet=TX('parquet', form=False), rug=TX('rug', form=False), velvet_red=TX('velvet_red', smix=0.25), velvet_teal=TX('velvet_teal', smix=0.25),
             p_lake=TX('paint_lake'), p_land=TX('paint_land'), p_still=TX('paint_still'), p_portrait=TX('paint_portrait'), frame=_glossy(TX('frame_gold', sm=(2.0, 1.4, 0.6), smix=0.15), (1.0, 0.8, 0.5), 0.5, 0.25),
             iron=_glossy(C('#5a5e6c', 1.0, 1.6), (1.0, 0.85, 0.7), 0.35, 0.3), iron_d=C('#34363f', 1.0, 1.8), jack_red=_glossy(C('#c04a2c', 1.0, (1.5, 0.9, 0.8), smix=0.25), (1.0, 0.8, 0.6), 0.4, 0.3), steel=_glossy(C('#8a8f9e', 1.0, 1.5), (1.0, 0.9, 0.8), 0.3, 0.3), brass=_glossy(C('#b8923e', 1.0, (2.0, 1.5, 0.6), smix=0.2), (1.0, 0.8, 0.5), 0.5, 0.22),
             dirt=TX('mud_wet', form=False), stair_body=C('#d8c9a4', 1.0, 1.0), wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b8925e'), rope=C('#c8a868'), cream=C('#ecdcb6'), white=C('#efe8d8'), dark=C('#2a2a32', 1.0, 1.6, form=False),
             red=C('#b02a22', 1.0, (1.4, 0.8, 0.7), smix=0.25), teal=C('#2f8a82', 1.0, 1.0, smix=0.3), green=C('#3e6a46'), slate=C('#59607a'), stone=C('#b0a898'), canvas=C('#d8c89a'),
             door=C('#2e5a4c'), door_r=C('#7a2a24', 1.0, (1.4, 0.8, 0.7), smix=0.25), horse=C('#8a5230'), horse_d=C('#4a2c1a'), horse_w=C('#dcd2bc'), skin=C('#d8a880'), coal=C('#26262a', 1.0, 0.9),
             lamp_glass=mat_emit(pre + 'e_lampglass', '#ffd890', strength=3.4 * max(0.2, lk)), glass_cand=mat_emit(pre + 'e_cand', '#fff0b8', strength=6.0),
             win_dark_flat=C('#2a3050', 1.0, 1.0, form=False), under_dark=C('#1e1c26', 1.0, 1.0, form=False), flag_r=TX('awn_rc'), flag_b=C('#2c3f86'),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.6, 0.3), 0.8 if lk > 0 else 0.5), pool=MN._mat_pool(pre + 'poolmat', (1.0, 0.6, 0.28), 0.55))
    M['_flame_mats'] = [M['lamp_glass']]
    M['sky'] = D._mat_sky(pre + 'sky', dict(P, star_k=0.0), tx['sky_' + P['sky']], P['sky_k'])
    M['mud'] = _mud_mat(pre, P, tx); M['puddle'] = _puddle_mat(pre, P, tx)
    return M

def _mud_mat(pre, P, tx):
    """Street mud: painted ochre-brown (mud) blended to a wet dark brown (mud_wet) by height (the troughs and puddle rims are darker),
    plus a sharp-ish GGX lobe: wet glints from the key and mirrored sky / hotel through the glossy bounce."""
    m = _untoon(mat_lit(pre + 'mud', image=tx['mud'], form=tuple(P['form']), shade_mix=0.35, gain=0.78)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); links0 = list(tex.outputs['Color'].links); tex.extension = 'REPEAT'
    t2 = N('ShaderNodeTexImage'); t2.image = T._img(tx['mud_wet']); t2.extension = 'REPEAT'
    uv = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeUVMap']
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sp.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'; mr.inputs['From Min'].default_value = -0.45; mr.inputs['From Max'].default_value = 0.12; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    L(sp.outputs['Z'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(mr.outputs['Result'], mx.inputs[0]); L(tex.outputs['Color'], mx.inputs[6]); L(t2.outputs['Color'], mx.inputs[7])
    for l in links0: to = l.to_socket; nt.links.remove(l); L(mx.outputs[2], to)
    _glossy(m, (1.0, 0.82, 0.6), 0.3, 0.22)
    return m

def _puddle_mat(pre, P, tx):
    """Puddle water: dark brown-violet base (the shade stays painted) + a mirror (sharp GGX, glossy bounce) for hotel, sky, lamps."""
    m = _untoon(mat_lit(pre + 'puddle', '#4a3a40', form=tuple(P['form']), shade_mix=0.5, gain=0.7))
    def make(nt):
        N = nt.nodes.new; L = nt.links.new
        gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.02; gl.inputs['Color'].default_value = (0.95, 0.9, 0.85, 1)
        return gl.outputs['BSDF']
    MN._append_shader(m, make)
    return m

# ============================================================================= sky + far ground
def _sky(SET, P, M, R):
    mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o
    if P.get('pano'):
        mb = MB(); Rp = CX.PANO_R; seg = 192; pm = mat_emit(STATE['pre'] + 'e_pano', image=STATE['tx']['pano_' + P['pano']], strength=P['pano_k'], alpha=True)
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
            mb.face([Vector((Rp * math.cos(a0), Rp * math.sin(a0), CX.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), CX.PANO_Z0)),
                     Vector((Rp * math.cos(a1), Rp * math.sin(a1), CX.PANO_Z1)), Vector((Rp * math.cos(a0), Rp * math.sin(a0), CX.PANO_Z1))], pm, [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
        _obj(mb, 'backdrop', SET, shadow=False)

def _far_ground(SET, M, z=-2.5):
    mb = MB(); R = 430.0; fm = STATE['TX']('far_ground', form=False) if 'TX' in STATE else STATE['C']('#8c8a5a')
    mb.face([Vector((-R, -R, z)), Vector((R, -R, z)), Vector((R, R, z)), Vector((-R, R, z))], fm, [(0, 0), (R / 8, 0), (R / 8, R / 8), (0, R / 8)]); _obj(mb, 'far_ground', SET)

# ============================================================================= hotel
def _win_state(i, f):
    """deterministic window state per bay i, floor f: dark | lit | curt | lit2"""
    r = _rnd(i * 31 + f * 7 + 3).random()
    if f == 5 and i in (2, 3, 4): return 'lit2' if i == 3 else 'curt'
    return 'lit' if r < 0.22 else ('curt' if r < 0.45 else 'dark')

def _openings(mb, fr, M, xs, z0, z1, depth, wins, brick, uvk=1.0 / 6, sill=True, hood=True, thick=0.7):
    """A wall band (local frame fr: x along, y out-of-wall = -y) of height z0..z1 with openings. wins = list of (cx, w, zb, zt, kind, mat_name, state);
    the wall slab is `thick` deep (y 0..thick) with real reveals, the glass quad at y = thick - 0.1; cream sills, lintels and hoods are proud."""
    ps = sorted(wins, key=lambda w: w[0]); x_cur = xs[0]
    for (cx, w, zb, zt, kind, mat, state) in ps:
        x0, x1 = cx - w / 2, cx + w / 2
        fr.box(mb, (x_cur, 0, z0), (x0, thick, z1), brick, uvk); x_cur = x1
        fr.box(mb, (x0, 0, z0), (x1, thick, zb), brick, uvk); fr.box(mb, (x0, 0, zt), (x1, thick, z1), brick, uvk)
        fr.quad(mb, [(x0, thick - 0.12, zb), (x1, thick - 0.12, zb), (x1, thick - 0.12, zt), (x0, thick - 0.12, zt)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        if sill:
            fr.box(mb, (x0 - 0.3, -0.4, zb - 0.22), (x1 + 0.3, thick * 0.9, zb), M['ash'], 0.3)
        if hood:
            fr.box(mb, (x0 - 0.25, -0.3, zt), (x1 + 0.25, thick, zt + 0.45), M['ash'], 0.3)
            if kind == 'main':                                                     # pediment hood with a cap
                fr.box(mb, (x0 - 0.5, -0.65, zt + 0.45), (x1 + 0.5, thick, zt + 0.75), M['ash'], 0.3)
                for sgn in (-1, 1): fr.box(mb, ((cx + sgn * (w / 2 + 0.05)) - 0.18, -0.4, zb + 0.4), ((cx + sgn * (w / 2 + 0.05)) + 0.18, 0.1, zt), M['ash'], 0.3)
    fr.box(mb, (x_cur, 0, z0), (xs[1], thick, z1), brick, uvk)

def _hotel(SET, M, P):
    """The Tremont House: six storeys of warm brick with cream stone trim, seven bays, real window reveals, portico + grand stair,
    cornice and parapet. Everything in `hotel` moves with set_lift (the foundation bottom is z 0 at lift 0)."""
    mb = MB(); fr = Frame((HX0, 0, 0), 0); bw = (HX1 - HX0) / NB; W_ = HX1 - HX0
    # plinth: rusticated stone with small barred basement windows
    plw = [(HX1 - HX0) * 0 + (i + 0.5) * bw for i in range(NB) if i != 3]
    fr.box(mb, (0, 0, -0.4), (W_, 0.8, GF), M['rustic'], 1 / 8)
    fr.box(mb, (-0.25, -0.25, 0.0), (W_ + 0.25, 0.8, GF - 0.1), M['rustic'], 1 / 8)
    for cx in plw:
        fr.quad(mb, [(cx - 0.8, -0.27, 0.6), (cx + 0.8, -0.27, 0.6), (cx + 0.8, -0.27, 2.0), (cx - 0.8, -0.27, 2.0)], M['win_base'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        for k in range(5): rod(mb, fr.p(cx - 0.64 + k * 0.32, -0.3, 0.6), fr.p(cx - 0.64 + k * 0.32, -0.3, 2.0), 0.035, M['iron_d'], seg=4)
    fr.box(mb, (-0.35, -0.35, GF - 0.1), (W_ + 0.35, 0.85, GF + 0.18), M['ash'], 0.3)              # plinth cap
    # storeys: brick wall bands with openings
    for f in range(6):
        z0, z1 = ZS[f], ZS[f + 1]; sh = STOREYS[f]; wins = []
        for i in range(NB):
            cx = (i + 0.5) * bw
            if f == 0 and i == 3: continue
            st = _win_state(i, f)
            if f == 0: zb, zt, kind, nm, ww = z0 + 0.5, z1 - 0.9, 'main', {'dark': 'win_dark_big', 'curt': 'win_dark_big', 'lit': 'win_lit_big', 'lit2': 'win_lit_big'}[st], 2.6
            elif f == 5: zb, zt, kind, nm, ww = z0 + 0.7, z1 - 0.65, 'top', {'dark': 'win_dark_short', 'curt': 'win_dark_short', 'lit': 'win_lit_short', 'lit2': 'win_lit_short'}[st], 2.2
            else: zb, zt, kind, nm, ww = z0 + 0.75, z1 - 0.8, 'std', 'win_' + st, 2.2
            if f in (5,) and st in ('curt', 'lit2'): nm = 'win_curt' if st == 'curt' else 'win_lit2'
            wins.append((cx, ww, zb, zt, kind, M[nm], st))
        if f == 0: wins = [(cx, w, zb, zt, k, m, s) for (cx, w, zb, zt, k, m, s) in wins]
        if f == 0:                                                              # centre bay: the doorway bay is plain brick above a portico opening
            fr.box(mb, (3 * bw, 0, z0), (4 * bw, 0.8, z1), M['brick'], 1 / 6)
            _openings(mb, fr, M, (0, 3 * bw), z0, z1, 0.8, [w for w in wins if w[0] < 3 * bw], M['brick'])
            _openings(mb, fr, M, (4 * bw, W_), z0, z1, 0.8, [w for w in wins if w[0] > 4 * bw], M['brick'])
            cx = 3.5 * bw                                                         # double doors + fanlight in the centre bay
            fr.box(mb, (cx - 1.7, -0.5, z0), (cx + 1.7, 0.9, z0 + 0.3), M['ash'], 0.3)
            fr.box(mb, (cx - 1.5, 0.5, z0), (cx + 1.5, 0.8, z0 + 4.6), M['door'], 0.3)
            for sgn in (-1, 1): fr.box(mb, (cx + sgn * 0.75 - 0.6, 0.3, z0 + 0.6), (cx + sgn * 0.75 + 0.6, 0.55, z0 + 3.7), M['door_r'], 0.4); sbox(mb, fr.p(cx + sgn * 0.2 - 0.07, 0.1, z0 + 2.0), fr.p(cx + sgn * 0.2 + 0.07, 0.3, z0 + 2.3), M['brass'])
            fr.quad(mb, [(cx - 1.5, 0.45, z0 + 4.6), (cx + 1.5, 0.45, z0 + 4.6), (cx + 1.5, 0.45, z1 - 0.9), (cx - 1.5, 0.45, z1 - 0.9)], M['win_lit'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        else:
            _openings(mb, fr, M, (0, W_), z0, z1, 0.8, wins, M['brick'])
        fr.box(mb, (-0.1, -0.35, z1 - 0.32), (W_ + 0.1, 0.8, z1), M['ash'], 0.3)       # string course
    # quoins at the front corners and along the left side corner
    zq = GF + 0.2
    while zq < ZS[6] - 1.0:
        long_ = 1.5 if int(zq / 0.9) % 2 == 0 else 0.9
        for xq in (0.0, W_):
            sgn = 1 if xq == 0 else -1; fr.box(mb, (min(xq, xq + sgn * long_) - 0.0, -0.2, zq), (max(xq, xq + sgn * long_), 0.8, zq + 0.8), M['ash'], 0.3)
        zq += 0.9
    # cornice + parapet + pediment
    zt = ZS[6]
    fr.box(mb, (-0.5, -0.5, zt), (W_ + 0.5, 1.0, zt + 0.9), M['ash'], 0.3)                      # frieze
    for k in range(int(W_ / 1.3) + 1):                                                           # brackets
        xk = -0.2 + k * 1.3; fr.box(mb, (xk, -1.1, zt + 0.6), (xk + 0.5, -0.5, zt + 1.5), M['ash'], 0.3)
    fr.box(mb, (-1.5, -1.8, zt + 1.5), (W_ + 1.5, 1.6, zt + 2.1), M['ash'], 0.3)                  # corona
    fr.box(mb, (-1.7, -2.0, zt + 2.1), (W_ + 1.7, 1.7, zt + 2.55), M['cream'], 0.3)
    fr.box(mb, (-1.2, 0.3, zt + 2.55), (W_ + 1.2, 1.5, zt + 4.2), M['brick'], 1 / 6)              # parapet
    fr.box(mb, (-1.4, 0.2, zt + 4.2), (W_ + 1.4, 1.7, zt + 4.55), M['ash'], 0.3)
    for k in range(int((W_ - 2) / 1.4) + 1):                                                    # balusters in front of the parapet
        xk = 1.0 + k * 1.4; rod(mb, fr.p(xk, -0.1, zt + 2.6), fr.p(xk, -0.1, zt + 4.1), 0.14, M['cream'], seg=6, r1=0.2)
    xm0, xm1 = 2 * bw + 0.2, 5 * bw - 0.2                                                         # central pediment
    fr.box(mb, (xm0, 0.3, zt + 4.55), (xm1, 1.5, zt + 6.0), M['ash'], 0.3)
    for sgn in (0, 1):
        ptsx = [(xm0 - 0.3, zt + 6.0), ((xm0 + xm1) / 2, zt + 8.6), (xm1 + 0.3, zt + 6.0)]
        fr.quad(mb, [(ptsx[0][0], -0.3, ptsx[0][1]), (ptsx[1][0], -0.3, ptsx[1][1]), (ptsx[2][0], -0.3, ptsx[2][1])], M['ash'], [(0, 0), (0.5, 1), (1, 0)], (0, -1, 0)) if sgn == 0 else None
    fr.box(mb, (xm0 - 0.3, -0.5, zt + 6.0), (xm1 + 0.3, 1.0, zt + 6.4), M['ash'], 0.3)
    cx = (xm0 + xm1) / 2; fr.quad(mb, [(cx - 1.6, -0.34, zt + 6.7), (cx + 1.6, -0.34, zt + 6.7), (cx, -0.34, zt + 8.1)], M['brick_d'], [(0, 0), (1, 0), (0.5, 1)], (0, -1, 0))
    for xu in (-0.6, W_ + 0.6, xm0 - 0.2, xm1 + 0.2):                                              # urns
        lumpy(mb, fr.p(xu, 0.9, zt + 4.9), 0.55, M['cream'], int(xu * 7 + 5), seg=8, rings=5, rough=0.05, squash=1.3)
    for xc in (3.0, 9.0, 31.0, 36.0):                                                             # chimneys
        fr.box(mb, (xc, 12, zt + 2.5), (xc + 1.6, 13.6, zt + 6.5), M['brick_d'], 1 / 6); fr.box(mb, (xc - 0.15, 11.85, zt + 6.5), (xc + 1.75, 13.75, zt + 6.9), M['ash'], 0.3)
    # side walls (left: facing -x, right: facing +x), windows on 5 bays; back wall
    for side in (0, 1):
        fs = Frame((HX0, HY1, 0), -90) if side == 0 else Frame((HX1, 0, 0), 90); sbw = HY1 / 5
        for f in range(6):
            z0, z1 = ZS[f], ZS[f + 1]; wins = []
            for i in range(5):
                st = _win_state(i + 9 * (side + 1), f); zb, zt2 = z0 + (0.6 if f == 0 else 0.75), z1 - (0.9 if f == 0 else 0.8)
                nm = 'win_dark' if f else 'win_dark_big'; nm = 'win_lit' if st == 'lit' and f else nm
                wins.append(((i + 0.5) * sbw, 2.2, zb, zt2, 'std', M[nm], st))
            _openings(mb, fs, M, (0, HY1), z0, z1, 0.8, wins, M['brick_b'], hood=False, sill=True)
        fs.box(mb, (-0.1, -0.3, ZS[6]), (HY1 + 0.1, 1.0, ZS[6] + 0.9), M['ash'], 0.3); fs.box(mb, (-0.5, -1.3, ZS[6] + 0.9), (HY1 + 0.5, 1.4, ZS[6] + 1.6), M['ash'], 0.3)
        fs.box(mb, (-0.2, 0.1, ZS[6] + 1.6), (HY1 + 0.2, 1.2, ZS[6] + 3.0), M['brick_b'], 1 / 6)
        fs.box(mb, (0, 0, -0.4), (HY1, 0.8, GF), M['rustic'], 1 / 8)
    sbox(mb, (HX0, HY1 - 0.5, -0.4), (HX1, HY1, ZS[6] + 3.0), M['brick_b'], 1 / 6)
    sbox(mb, (HX0 + 0.8, 0.7, -0.4), (HX1 - 0.8, HY1 - 0.5, ZS[6] + 0.5), M['brick_d'], 1 / 6)      # solid core
    ho = _obj(mb, 'hotel', SET); STATE['lift_movers'].append((ho, 0.0)); STATE['hotel'] = ho
    # awnings over the main-floor windows (striped canvas) + the portico
    am = MB(); k = 0
    for i in range(NB):
        if i == 3: continue
        cx = HX0 + (i + 0.5) * bw; mat = [M['awn_rc'], M['awn_tc'], M['awn_oc']][k % 3]; k += 1; zb = ZS[0] + 0.5 + 4.35
        _awning(am, cx, 0.0, zb - 0.2, 3.5, 2.2, 1.7, mat, M)
    _obj(am, 'hotel_awn', SET); STATE['lift_movers'].append((bpy.data.objects['hotel_awn'], 0.0))
    # portico
    pm = MB(); zc = ZS[0]; xc = HX0 + 3.5 * bw
    for xs_ in (-4.3, -1.8, 1.8, 4.3):
        xx = xc + xs_; rod(pm, (xx, -3.3, zc), (xx, -3.3, zc + 5.4), 0.6, M['cream'], seg=12, r1=0.5); rod(pm, (xx, -3.3, zc), (xx, -3.3, zc + 0.35), 0.8, M['ash'], seg=8)
        rod(pm, (xx, -3.3, zc + 5.4), (xx, -3.3, zc + 5.75), 0.78, M['ash'], seg=8)
    sbox(pm, (xc - 5.6, -4.3, zc + 5.75), (xc + 5.6, 0.3, zc + 6.8), M['ash'], 0.3); sbox(pm, (xc - 5.9, -4.6, zc + 6.8), (xc + 5.9, 0.35, zc + 7.2), M['cream'], 0.3)
    sbox(pm, (xc - 5.8, -4.5, zc + 7.2), (xc + 5.8, 0.3, zc + 7.35), M['ash'], 0.3)
    for k2 in range(17):
        xx = xc - 5.6 + k2 * 0.7; rod(pm, (xx, -4.3, zc + 7.35), (xx, -4.3, zc + 8.3), 0.1, M['cream'], seg=6, r1=0.14)
    sbox(pm, (xc - 5.8, -4.45, zc + 8.3), (xc + 5.8, -4.15, zc + 8.5), M['ash'], 0.3)
    sbox(pm, (xc - 5.4, -4.0, zc - 0.4), (xc + 5.4, 0.3, zc + 0.05), M['ash'], 0.3)                  # landing slab
    _obj(pm, 'hotel_portico', SET); STATE['lift_movers'].append((bpy.data.objects['hotel_portico'], 0.0))
    _stair(SET, M, xc)

def _awning(mb, cx, y, z, w, depth, drop, mat, M):
    """sloped striped canvas awning: top edge on the wall at z, front edge `depth` out and `drop` lower; side triangles + valance."""
    x0, x1 = cx - w / 2, cx + w / 2
    mb.oface([(x0, y, z), (x1, y, z), (x1, y - depth, z - drop), (x0, y - depth, z - drop)], mat, [(0, 1), (1, 1), (1, 0.15), (0, 0.15)], (0, -1, 0.6))
    mb.oface([(x0, y - depth, z - drop), (x1, y - depth, z - drop), (x1, y - depth - 0.05, z - drop - 0.55), (x0, y - depth - 0.05, z - drop - 0.55)], mat, [(0, 0.15), (1, 0.15), (1, 0), (0, 0)], (0, -1, -0.1))
    for xs_ in (x0, x1):
        mb.oface([(xs_, y, z), (xs_, y - depth, z - drop), (xs_, y - depth, z - drop - 0.5)], M['canvas'], [(0, 0), (1, 0), (1, 1)], (xs_ - cx, 0, 0))
    for xs_ in (x0, x1): rod(mb, (xs_, y, z - 0.1), (xs_, y - depth, z - drop - 0.45), 0.05, M['iron_d'], seg=4)

def _stair(SET, M, xc):
    """grand front stair: 10 stone treads on timber carriages; treads and carriages follow set_lift (rise = (GF + lift) / 10)."""
    N = 10; xw0, xw1 = xc - 5.4, xc + 5.4; y_top, y_bot = -4.0, -9.0; dy = (y_top - y_bot) / N
    for i in range(N):
        ya, yb = y_bot + i * dy, y_bot + (i + 1) * dy
        mb = MB(); sbox(mb, (xw0 + 0.1, ya + 0.15, -0.0), (xw1 - 0.1, yb, 1.0), M['stair_body'], 0.2)                    # carriage block: unit height, scaled in z
        ob = _obj(mb, 'stair_body_%d' % i, SET); STATE['steps'].append(('body', i, ob))
        tm = MB(); sbox(tm, (xw0 - 0.25, ya - 0.18, -0.34), (xw1 + 0.25, yb, 0.0), M['ash'], 0.3)
        to = _obj(tm, 'stair_tread_%d' % i, SET); STATE['steps'].append(('tread', i, to))
    cm = MB()                                                                                   # side stringers: wooden cheek rails
    for xs_ in (xw0 - 0.3, xw1 + 0.3):
        for k in range(6):
            yy = y_bot + 0.4 + k * 0.9; rod(cm, (xs_, yy, 0.0), (xs_, yy, 1.0), 0.09, M['iron_d'], seg=5)
    STATE['stair_x'] = (xw0, xw1, y_bot, y_top, N)

# ============================================================================= jacks and cribs (street gap + cellar)
def _jack(mb_static, mb_stretch, mb_head, x, y, L, M, seed=0, bar_dir=0):
    """one iron jackscrew standing on a timber block: static foot + housing (z up to 1.35), a stretching screw, a head with pad and a lever bar.
    mb_head parts are in a frame whose origin is the hotel underside (z 0 = the underside, so the head sits at -0.4..0)."""
    r = _rnd(seed); foot = 0.55
    sbox(mb_static, (x - 0.75, y - 0.75, 0.0), (x + 0.75, y + 0.75, 0.5), M['timber_d'], 0.3)                # timber block
    rod(mb_static, (x, y, 0.5), (x, y, 0.62), 0.6, M['iron_d'], seg=8)
    rod(mb_static, (x, y, 0.62), (x, y, 1.3), 0.42, M['jack_red'], seg=8, r1=0.34)                              # housing
    rod(mb_static, (x, y, 1.0), (x, y, 1.12), 0.5, M['brass'], seg=8)                                      # gear collar
    for k in range(4):                                                                                       # collar bar holes
        a = k * math.pi / 2 + 0.4; mb_static.frustum((x + 0.5 * math.cos(a), y + 0.5 * math.sin(a), 1.06), (x + 0.6 * math.cos(a), y + 0.6 * math.sin(a), 1.06), 0.06, 0.06, M['dark'], seg=4)
    rod(mb_stretch, (x, y, 0.0), (x, y, 1.0), 0.22, M['steel'], seg=6)                                         # screw (unit height: scaled)
    rod(mb_head, (x, y, -0.4), (x, y, -0.34), 0.46, M['jack_red'], seg=8)                                      # head
    sbox(mb_head, (x - 0.85, y - 0.85, -0.12), (x + 0.85, y + 0.85, 0.0), M['timber'], 0.3)                  # pad against the beam
    rod(mb_head, (x, y, -0.34), (x, y, -0.12), 0.3, M['iron'], seg=8)
    a = bar_dir; rod(mb_static, (x - 1.0 * math.cos(a) - 0.0, y - 1.0 * math.sin(a), 1.06), (x + 1.9 * math.cos(a), y + 1.9 * math.sin(a), 1.2), 0.1, M['wood_l'], seg=5)   # the lever bar in the collar

def _jackfield(SET, M, L, xs, ys, name, static_only=False, crib_x=()):
    """rows of jacks on a grid; static foot objects, stretch screw objects (scale z via set_lift), mover heads. returns the three objects."""
    sm, st, hd = MB(), MB(), MB(); n = 0
    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            if any(abs(x - cx) < 1.7 for cx in crib_x): continue
            _jack(sm, st, hd, x, y, L, M, seed=n, bar_dir=0.5 + 0.7 * ((ix + iy) % 3)); n += 1
    so = _obj(sm, name + '_static', SET); sto = _obj(st, name + '_screw', SET); ho = _obj(hd, name + '_head', SET)
    return so, sto, ho, n

def _cribs(SET, M, xs, ys, L, name):
    """timber cribbing piers: stacks of crossed beams (layer i exists once lift > its z); layers are separate objects shown by set_lift."""
    layers = []; nl = int(LIFT_MAX / 0.5) + 1
    for li in range(nl):
        mb = MB(); z0 = li * 0.5
        for y in ys:
            for x in xs:
                a = (li % 2 == 0)
                for off in (-0.6, 0.6):
                    if a: sbox(mb, (x - 1.2, y + off - 0.28, z0), (x + 1.2, y + off + 0.28, z0 + 0.5), M['timber'], 0.28)
                    else: sbox(mb, (x + off - 0.28, y - 1.2, z0), (x + off + 0.28, y + 1.2, z0 + 0.5), M['timber_w'], 0.28)
        ob = _obj(mb, '%s_layer%d' % (name, li), SET); layers.append((li, z0 + 0.5, ob))
    return layers

# ============================================================================= street
PUDDLES = [(-14, -31, 4.8, 0.85), (6, -37, 3.6, 0.7), (-33, -24, 3.2, 0.7), (18, -23, 4.2, 0.8), (-3, -16.5, 2.4, 0.65), (30, -34, 3.0, 0.7), (-22, -42, 3.4, 0.7),
           (11, -12.5, 2.0, 0.6), (-40, -35, 3.4, 0.7), (40, -21, 2.8, 0.65), (-9, -24, 1.7, 0.6), (24, -41, 2.2, 0.6), (-8, -46, 3.0, 0.7), (12, -47, 2.6, 0.7), (-36, -46, 2.2, 0.6)]
def _terrain(SET, M):
    """Smooth mud height field (shared vertices, smooth shading): rolling noise, wheel ruts, a crown, and puddle basins; flat puddle water discs
    sit at the lowest rim height of each basin so the terrain cuts their outline (organic, layered with the wet-dark mud shader)."""
    xs = np.unique(np.round(np.concatenate([np.arange(-150, -76, 4.0), np.arange(-76, 76, 0.5), np.arange(76, 151, 4.0)]), 3))
    ys = np.unique(np.round(np.concatenate([np.arange(-130, -58, 4.0), np.arange(-58, -2, 0.45), np.arange(-2, 60, 4.0)]), 3))
    def sm(a, b, v):
        t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
    def mud_z(x, y):
        win = sm(-58, -48, y) * (1 - sm(-11, -7.5, y))
        flat = np.ones_like(x * 1.0)
        for (cx, cy, rr, dp) in PUDDLES: flat = flat * (1 - 0.85 * np.exp(-(((x - cx) / (rr * 1.9)) ** 2 + ((y - cy) / (rr * 1.5)) ** 2)))
        z = 0.2 * np.sin(0.21 * x + 0.7) * np.cos(0.17 * y + 1.1) + 0.12 * np.sin(0.43 * x + 0.2 * y) + 0.07 * np.sin(0.93 * x - 0.6 * y + 2.0)
        for yr in (-26.0, -29.4, -35.0, -38.2): z = z - 0.3 * np.exp(-((y - yr + 0.4 * np.sin(0.06 * x)) / 0.55) ** 2) * (0.7 + 0.3 * np.sin(0.11 * x + yr))
        z = (z + 0.18 * np.exp(-((y + 27.7) / 1.1) ** 2)) * flat * win
        for (cx, cy, rr, dp) in PUDDLES: z = z - dp * np.exp(-(((x - cx) / (rr * 1.25)) ** 2 + ((y - cy) / rr) ** 2) * 1.0)
        return z
    X, Y = np.meshgrid(xs, ys); Z = mud_z(X, Y)
    terr = grid_mesh('mud', xs, ys, Z, M['mud'], uvs=(0.1, 0.1)); STATE['terrain'] = terr; STATE['fill_objs'].append(terr); STATE['mud_z'] = mud_z
    pm = MB(); n = 32
    for (cx, cy, rr, dp) in PUDDLES:
        ang = np.linspace(0, 2 * math.pi, 48, endpoint=False); rim = mud_z(cx + rr * 2.3 * 1.25 * np.cos(ang), cy + rr * 2.3 * np.sin(ang)); zw = float(rim.min()) - 0.02
        zw = min(zw, -0.12)
        pts = [Vector((cx + rr * 2.3 * 1.25 * math.cos(2 * math.pi * k / n), cy + rr * 2.3 * math.sin(2 * math.pi * k / n), zw)) for k in range(n)]
        for k in range(n): pm.face([Vector((cx, cy, zw)), pts[(k + 1) % n], pts[k]], M['puddle'])
    po = _obj(pm, 'puddles', SET); STATE['fill_objs'].append(po)
    return mud_z

def _street(SET, P, M):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M)
    r = _rnd(5)
    mud_z = _terrain(SET, M)
    # --- plank sidewalks (two levels) and posts ---
    sb = MB()
    for (x0, x1, zt, y0, y1) in ((-110, -28, 1.3, -8.5, -3.2), (20, 110, 0.5, -8.0, -3.0)):
        sbox(sb, (x0, y0, zt - 0.3), (x1, y1, zt), M['walk'], 0.2)
        sbox(sb, (x0, y0 - 0.25, zt - 0.5), (x1, y0, zt + 0.12), M['plank_d'], 0.3)
        for xp in np.arange(x0 + 2, x1, 5.5): sbox(sb, (xp, y0, -0.4), (xp + 0.4, y0 + 0.4, zt - 0.3), M['timber_d'], 0.3)
    for xx in (-27.6, 19.6):                                                              # plank steps down to the street
        for k in range(3): sbox(sb, (xx - 0.0, -8.0 - k * 0.7 - 0.7, 0.0), (xx + 4.0, -8.0 - k * 0.7, 1.0 - 0.3 * k), M['walk'], 0.2)
    _obj(sb, 'sidewalk', SET)
    _hotel(SET, M, P)
    # jacks + cribs under the hotel (gap)
    xj = [-18.0 + 3.0 * k for k in range(13)]; yj = [1.6, 6.2, 11.0, 16.0, 21.5, 27.0]; xc = [-19.2, -9.6, 0.0, 9.6, 19.2]
    so, sto, ho, nj = _jackfield(SET, M, LIFT_MAX, xj, yj, 'jf', crib_x=xc)
    STATE['jack_static'] = so; STATE['lift_stretch'].append((sto, 0.5 + 0.8)); STATE['lift_movers'].append((ho, 0.0)); STATE['njacks'] = nj
    STATE['crib_layers'] = _cribs(SET, M, xc, [1.6, 11.0, 21.5, 27.0], LIFT_MAX, 'crib')
    # dark under-floor beams + lamps hung under the floor
    ub = MB(); sbox(ub, (HX0 + 0.2, 0.8, -0.35), (HX1 - 0.2, HY1 - 0.5, 0.0), M['timber_d'], 0.2)
    for yy in np.arange(1.5, HY1 - 1, 3.0): sbox(ub, (HX0 + 0.2, yy - 0.35, -0.9), (HX1 - 0.2, yy + 0.35, -0.35), M['timber'], 0.25)
    uo = _obj(ub, 'under_beams', SET); STATE['lift_movers'].append((uo, 0.0))
    fl = MB()
    for (xl, yl) in ((-12.0, 3.9), (3.0, 3.9), (12.0, 3.9)):
        c = Vector((xl, yl, 0.0)); rod(fl, c + Vector((0, 0, -0.9)), c + Vector((0, 0, -0.55)), 0.03, M['iron_d'], seg=4)
        fl.frustum(c + Vector((0, 0, -1.25)), c + Vector((0, 0, -0.65)), 0.2, 0.26, M['lamp_glass'], seg=7); _halo(fl, c + Vector((0, 0, -0.95)), 2.4, M)
    lo = _obj(fl, 'under_lamps', SET, shadow=False); STATE['lift_movers'].append((lo, 0.0))
    for k, xl in enumerate((-12.0, 3.0, 12.0)): D._flame_light('gap_%d' % k, (xl, 3.0, 1.6), LAMP, 900, radius=0.3, shadow=False)
    # ground below the hotel: dark earth slab (so the gap is not see-through to the sky)
    gb = MB(); gb.face([Vector((HX0, 0.8, 0.02)), Vector((HX1, 0.8, 0.02)), Vector((HX1, HY1, 0.02)), Vector((HX0, HY1, 0.02))], M['mud'], [(0, 0), (4, 0), (4, 3), (0, 3)]); _obj(gb, 'under_floor', SET)
    # --- neighbours ---
    _neighbours(SET, M)
    # --- street dressing ---
    _street_dress(SET, M, mud_z)
    _church(SET, M)

def _shop(mb, M, x0, x1, h, facname, y0=0.0, depth=22.0, zb=0.0, side_mat=None, roof_k=0, cornice_mat=None, awn=(None,)):
    """A shop: box with a painted facade, plain brick (or clapboard) sides, flat roof with cornice; optional gable."""
    fac = M[facname]; sidem = side_mat or M['brick_b']; w = x1 - x0
    mb.box((x0, y0, zb - 1.0), (x1, y0 + depth, zb + h), sidem, mats=dict(front=fac, right=sidem, left=sidem), tile=(6, 6))
    cm = cornice_mat or M['cream']
    sbox(mb, (x0 - 0.3, y0 - 0.9, zb + h - 0.9), (x1 + 0.3, y0 + 0.3, zb + h), cm, 0.3); sbox(mb, (x0 - 0.5, y0 - 1.5, zb + h), (x1 + 0.5, y0 + 0.4, zb + h + 0.5), cm, 0.3)
    for k in range(int(w / 1.5)):
        xk = x0 + 0.4 + k * 1.5; sbox(mb, (xk, y0 - 1.0, zb + h - 0.9), (xk + 0.45, y0 - 0.2, zb + h - 0.3), cm, 0.3)
    sbox(mb, (x0, y0 + depth - 0.4, zb + h), (x1, y0 + depth, zb + h + 1.3), sidem, 1 / 6)
    return mb

def _neighbours(SET, M):
    mb = MB(); am = MB()
    spec = [  # (x0, x1, h, fac, zb)
        ('L1', -52.0, -28.0, 21.0, 'fac_c', 1.3), ('L2', -72.0, -52.0, 14.0, 'fac_b', 0.0), ('L3', -90.0, -72.0, 12.5, 'fac_f', 0.0), ('L4', -110.0, -90.0, 17.0, 'fac_a', 0.0),
        ('R1', 20.0, 46.0, 17.0, 'fac_a', 0.5), ('R2', 46.0, 64.0, 15.0, 'fac_d', 0.5), ('R3', 64.0, 86.0, 18.0, 'fac_e', 0.5), ('R4', 86.0, 102.0, 12.5, 'fac_f', 0.5)]
    for (nm, x0, x1, h, fac, zb) in spec:
        side = M['clap_ochre'] if fac in ('fac_b',) else (M['clap_teal'] if fac == 'fac_d' else (M['clap_green'] if fac == 'fac_f' else M['brick_b']))
        _shop(mb, M, x0, x1, h, fac, zb=zb, side_mat=side)
        nb = max(1, int((x1 - x0) // 8)); aw = [M['awn_rc'], M['awn_tc'], M['awn_oc']]
        for k in range(nb):
            cx = x0 + (k + 0.5) * (x1 - x0) / nb; _awning(am, cx, 0.0, zb + 4.3, (x1 - x0) / nb * 0.8, 2.0, 1.3, aw[(k + int(abs(x0))) % 3], M)
    # raised left neighbour: cribbing under the front corner (already raised and bedded on timber)
    for xx in np.arange(-51.0, -29.0, 3.4):
        sbox(mb, (xx, -0.2, -0.3), (xx + 1.1, 0.9, 0.0), M['timber_d'], 0.3)
    _obj(mb, 'shops', SET); _obj(am, 'shop_awnings', SET)
    # shop-side clutter: barrels, crates, hand carts in front of the sidewalk shops
    cb = MB(); r = _rnd(77)
    for (xx, zz) in ((-58, 0.0), (-66, 0.0), (-80, 0.0), (26, 0.5), (36, 0.5), (50, 0.5), (70, 0.5), (92, 0.5), (-42, 1.3), (-34, 1.3)):
        _crate_stack(cb, (xx, -6.2, zz + 0.0), M, int(xx) + 11, 3 + int(abs(xx)) % 3); _barrel(cb, (xx + 4.5, -5.2, zz), M, 'wood'); _barrel(cb, (xx + 5.8, -5.6, zz), M, 'wood_d')
    _obj(cb, 'shop_clutter', SET)

def _crate_stack(mb, c, M, seed, n=4):
    r = _rnd(seed); c = Vector(c)
    for k in range(n):
        s = r.uniform(1.0, 1.7); x = c.x + (k % 3) * 1.8 + r.uniform(-0.1, 0.1); y = c.y + r.uniform(-0.2, 0.2); z = c.z if k < 3 else c.z + 1.4
        if k >= 3: x = c.x + (k - 3) * 1.8 + 0.9
        sbox(mb, (x - s / 2, y - s / 2, z), (x + s / 2, y + s / 2, z + s), M['crate'], 0.3)
        for e in (-1, 1): sbox(mb, (x - s / 2 - 0.02, y + e * (s / 2 - 0.05) - 0.06, z + 0.1), (x + s / 2 + 0.02, y + e * (s / 2 - 0.05) + 0.06, z + 0.3), M['wood_d'], 0.3)

def _barrel(mb, c, M, mat='wood', r=0.55, h=1.4):
    c = Vector(c)
    mb.frustum(c, c + Vector((0, 0, h / 2)), r * 0.85, r, M[mat], seg=12, cap1=False); mb.frustum(c + Vector((0, 0, h / 2)), c + Vector((0, 0, h)), r, r * 0.85, M[mat], seg=12, cap0=False)
    mb.frustum(c + Vector((0, 0, h - 0.01)), c + Vector((0, 0, h)), r * 0.85, r * 0.85, M['wood_d'], seg=12, cap0=False)
    for zz in (0.2, h - 0.2): mb.frustum(c + Vector((0, 0, zz - 0.05)), c + Vector((0, 0, zz + 0.05)), r * 0.93, r * 0.93, M['iron'], seg=12, cap0=False, cap1=False)
    mb.frustum(c + Vector((0, 0, h / 2 - 0.05)), c + Vector((0, 0, h / 2 + 0.05)), r * 1.01, r * 1.01, M['iron'], seg=12, cap0=False, cap1=False)

def _gas_lamp(mb, fl, c, M, k):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, 5.2)), 0.16, M['iron_d'], seg=6, r1=0.09); mb.frustum(c, c + Vector((0, 0, 0.9)), 0.34, 0.2, M['iron_d'], seg=8)
    rod(mb, c + Vector((0, 0, 3.2)), c + Vector((0.0, 0, 3.4)), 0.3, M['iron_d'], seg=6)
    fl.frustum(c + Vector((0, 0, 5.2)), c + Vector((0, 0, 6.0)), 0.26, 0.36, M['lamp_glass'], seg=6)
    mb.frustum(c + Vector((0, 0, 6.0)), c + Vector((0, 0, 6.5)), 0.5, 0.06, M['iron_d'], seg=6)
    f = c + Vector((0, 0, 5.6)); _halo(fl, f, 1.2, M)

def _pole(mb, x, y, M, h=15.0):
    rod(mb, (x, y, -0.2), (x, y, h), 0.32, M['wood_d'], seg=7, r1=0.2)
    sbox(mb, (x - 2.4, y - 0.18, h - 1.2), (x + 2.4, y + 0.18, h - 0.9), M['timber_d'], 0.3); sbox(mb, (x - 2.0, y - 0.18, h - 3.0), (x + 2.0, y + 0.18, h - 2.7), M['timber_d'], 0.3)
    for xo in (-2.2, -0.9, 0.9, 2.2):
        for hh in (h - 0.9, h - 2.7): rod(mb, (x + xo, y, hh), (x + xo, y, hh + 0.45), 0.09, M['teal'], seg=5)
    rod(mb, (x - 1.2, y - 0.4, 3.0), (x - 0.4, y - 0.4, 3.0), 0.05, M['iron_d'], seg=3)

def _wheel(mb, c, r, axis_x, M, yaw=0.0):
    """spoked cartwheel in the plane perpendicular to local x (after yaw): rim of 14 chunks, 12 spokes, hub."""
    c = Vector(c); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    n = 14
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; p0 = c + ey * math.cos(a0) * r + Z * math.sin(a0) * r; p1 = c + ey * math.cos(a1) * r + Z * math.sin(a1) * r
        beam(mb, p0, p1, 0.28, 0.45, M['wood'], up=tuple(ex)); beam(mb, p0 + ex * 0.0, p1, 0.06, 0.5, M['iron_d'], up=tuple(ex))
    for i in range(12):
        a = 2 * math.pi * i / 12; rod(mb, c, c + ey * math.cos(a) * r + Z * math.sin(a) * r, 0.07, M['wood_l'], seg=4)
    rod(mb, c - ex * 0.35, c + ex * 0.35, 0.22, M['wood_d'], seg=8)

def _horse(mb, base, yaw, M, mat='horse', z0=0.0, seed=1):
    """boxy-faceted draught horse (3 D at the shoulder); faces +x local. returns nothing."""
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    P = lambda x, y, z: b + ex * x + ey * y + Z * z
    mt = M[mat]; md = M['horse_d']
    ell(mb, P(0, 0, 3.4), 1.9, 0.95, 1.05, mt, seg=10, rings=6, yaw=yaw)
    ell(mb, P(-1.2, 0, 3.6), 1.1, 0.9, 1.0, mt, seg=8, rings=5, yaw=yaw)
    ell(mb, P(1.6, 0, 4.0), 0.9, 0.6, 0.9, mt, seg=8, rings=5, yaw=yaw, pitch=0.0)
    mb.frustum(P(1.5, 0, 3.8), P(2.7, 0, 5.2), 0.55, 0.38, mt, seg=8)                            # neck
    ell(mb, P(3.3, 0, 5.3), 0.75, 0.35, 0.42, mt, seg=8, rings=5, yaw=yaw)                            # head
    mb.frustum(P(3.9, 0, 5.15), P(4.2, 0, 4.9), 0.22, 0.2, md, seg=6)                                # muzzle
    for sg in (-1, 1): mb.frustum(P(2.9, sg * 0.2, 5.7), P(2.8, sg * 0.25, 6.2), 0.12, 0.02, md, seg=4)  # ears
    rod(mb, P(2.3, 0, 5.7), P(1.2, 0, 4.3), 0.3, md, seg=6)                                          # mane
    for (lx, ly) in ((1.5, 0.45), (1.5, -0.45), (-1.4, 0.45), (-1.4, -0.45)):
        mb.frustum(P(lx, ly, 3.0), P(lx + 0.1, ly, 1.1), 0.3, 0.2, mt, seg=6); mb.frustum(P(lx + 0.1, ly, 1.1), P(lx + 0.1, ly, 0.15), 0.18, 0.2, mt, seg=6)
        mb.frustum(P(lx + 0.1, ly, 0.25), P(lx + 0.1, ly, 0.0), 0.26, 0.3, md, seg=6)
    mb.frustum(P(-2.2, 0, 4.0), P(-2.6, 0, 1.9), 0.25, 0.08, md, seg=5)                              # tail
    mb.frustum(P(1.6, 0, 3.3), P(1.6, 0, 3.9), 0.98, 0.98, M['wood_d'], seg=10, cap0=False, cap1=False)    # collar

def _cart(mb, wm, fl, base, yaw, M, sink=0.6, load='barrels', horse=True, seed=3):
    """a horse cart bogged in the mud: bed, 4 wheels sunk by `sink`, load, shafts and horse (+x along yaw)."""
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    P = lambda x, y, z: b + ex * x + ey * y + Z * z
    zb = 2.4 - sink
    obox(mb, P(0, 0, zb), ex, ey, Z, 3.6, 1.7, 0.18, M['wood'], 0.3)
    for sg in (-1, 1):
        obox(mb, P(0, sg * 1.7, zb + 0.55), ex, ey, Z, 3.6, 0.1, 0.5, M['wood_l'], 0.3)
    obox(mb, P(-3.6, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3); obox(mb, P(3.5, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3)
    for sx in (-2.3, 2.3):
        for sg in (-1, 1): _wheel(wm, P(sx, sg * 2.0, 1.5 - sink), 1.9, True, M, yaw=yaw)
        rod(mb, P(sx, -2.0, 1.5 - sink), P(sx, 2.0, 1.5 - sink), 0.16, M['iron_d'], seg=6)
    if load == 'barrels':
        for (lx, ly, lz) in ((-2.4, -0.7, 0), (-1.0, -0.7, 0), (0.4, -0.7, 0), (1.8, -0.7, 0), (-2.4, 0.8, 0), (-1.0, 0.8, 0), (0.4, 0.8, 0), (1.8, 0.8, 0), (-1.7, 0.0, 1.4), (0.1, 0.0, 1.4), (1.2, 0.1, 1.4)):
            _barrel(mb, P(lx, ly, zb + 0.18 + lz), M, 'wood' if (lx + ly) % 2 < 1 else 'wood_l', r=0.62, h=1.5)
    else:
        for (lx, ly, lz, s) in ((-2.2, -0.6, 0, 1.5), (-0.4, 0.5, 0, 1.6), (1.4, -0.5, 0, 1.4), (-1.2, 0.0, 1.5, 1.3), (0.6, -0.2, 1.6, 1.2)):
            obox(mb, P(lx, ly, zb + 0.18 + lz + s / 2), ex, ey, Z, s / 2, s / 2, s / 2, M['crate'], 0.3)
    for sg in (-1, 1): beam(mb, P(3.5, sg * 0.9, zb - 0.1), P(8.2, sg * 0.9, zb + 0.9), 0.16, 0.22, M['wood_d'])                    # shafts
    if horse: _horse(mb, P(8.2, 0, 0.0 - 0.45 * 0), yaw, M, 'horse' if seed % 2 else 'horse_d', seed=seed)

def _mound(SET, M, name, cx, cy, rx, ry, h, seed, mat, mud_z):
    xs = np.linspace(cx - rx, cx + rx, 30); ys = np.linspace(cy - ry, cy + ry, 30); X, Y = np.meshgrid(xs, ys); rs = np.random.RandomState(seed)
    d = np.sqrt(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2); n = 0.07 * np.sin(2.3 * X + seed) * np.cos(1.9 * Y) + 0.05 * np.sin(5.0 * X - 3.1 * Y + seed)
    Z = h * np.clip(1 - d ** 1.7, 0, 1) ** 0.9 * (1 + n) - 0.35 + n * 0.3
    ob = grid_mesh(name, xs, ys, Z, mat, uvs=(0.2, 0.2)); STATE['fill_objs'].append(ob)
    return ob

def _street_dress(SET, M, mud_z):
    # gas lamps along the sidewalks, telegraph poles + wires
    mb = MB(); fl = MB()
    for k, xx in enumerate((-96, -66, -40, 28, 56, 84)): _gas_lamp(mb, fl, (xx, -8.2 if xx < 0 else -7.7, 1.3 if xx < 0 else 0.5), M, k)
    for xx in (-9.0, 9.0): _gas_lamp(mb, fl, (xx + (-7.0 if xx < 0 else 7.0), -9.6, 0.0), M, 9)
    poles = [(x, -13.0) for x in (-112, -74, -36, 2, 40, 78, 116)]
    for (x, y) in poles: _pole(mb, x, y, M)
    for (a, b) in zip(poles, poles[1:]):
        for dx, dz in ((-2.2, 14.1), (-0.9, 14.1), (0.9, 14.1), (2.2, 14.1), (-2.0, 12.3), (2.0, 12.3)):
            chain_rod(mb, catenary((a[0] + dx, a[1], dz), (b[0] + dx, b[1], dz), 0.9, 8), 0.05, M['iron_d'], seg=3)
    # hitching posts
    for xx in (-60, -30, 30, 60): rod(mb, (xx, -9.4, 0.0), (xx, -9.4, 2.4), 0.16, M['wood_d'], seg=5); sbox(mb, (xx - 0.7, -9.5, 2.0), (xx + 0.7, -9.3, 2.2), M['wood_d'], 0.3)
    _obj(mb, 'street_furniture', SET); _obj(fl, 'lamps_glass', SET, shadow=False)
    # carts in the mud
    cm = MB(); wm = MB(); cf = MB()
    _cart(cm, wm, cf, (-24.0, -34.0, 0.0), math.radians(8), M, sink=0.55, load='barrels', seed=3)
    _cart(cm, wm, cf, (17.0, -26.0, 0.0), math.radians(190), M, sink=0.4, load='crates', seed=4)
    _obj(cm, 'carts', SET); _obj(wm, 'cart_wheels', SET); STATE['fill_objs'] += [bpy.data.objects['carts'], bpy.data.objects['cart_wheels']]
    # fill earth piles, gravel heaps, planks, timber stack, barrels, crates in the street
    _mound(SET, M, 'pile_a', -34.0, -17.0, 8.0, 4.4, 3.4, 4, M['clay'], mud_z); _mound(SET, M, 'pile_b', 40.0, -14.0, 7.0, 3.8, 2.6, 5, M['clay'], mud_z)
    _mound(SET, M, 'pile_c', 12.0, -38.0, 5.0, 3.2, 1.9, 6, M['gravel'], mud_z); _mound(SET, M, 'pile_e', -7.0, -46.0, 5.0, 3.0, 2.2, 8, M['clay'], mud_z); _mound(SET, M, 'pile_d', -48.0, -22.0, 6.0, 3.4, 2.2, 7, M['clay'], mud_z)
    pm = MB()
    for k in range(6): sbox(pm, (-3.0 + k * 0.0, -14.0 - k * 0.0, 0.0), (-3.0, -14.0, 0.0), M['plank_d'], 0.3) if False else None
    for k in range(5): sbox(pm, (-12.0, -15.4 + k * 0.45, 0.0 + k * 0.0), (-4.0, -15.0 + k * 0.45, 0.35), M['walk'], 0.3)            # plank walk over the mud
    for k in range(5): sbox(pm, (24.0, -17.4 + k * 0.45, 0.1), (31.0, -17.0 + k * 0.45, 0.45), M['walk'], 0.3)
    for k in range(7):                                                                                                                  # timber stack
        for j in range(3 - k // 3): sbox(pm, (-60.0 + j * 0.8, -17.0 + k * 0.0 - 0.0, 0.6 * (k // 1) * 0.0), (-60.0, -17.0, 0.0), M['timber'], 0.3) if False else None
    for lvl in range(4):
        for j in range(5 - lvl): sbox(pm, (-62.0 + lvl * 0.5, -22.0 + j * 0.6 + lvl * 0.3, 0.45 * lvl - 0.1), (-54.0 - lvl * 0.5, -21.5 + j * 0.6 + lvl * 0.3, 0.45 * lvl + 0.35), M['timber_w'], 0.3)
    p0, p1 = Vector((-15.0, -52.0)), Vector((-3.0, -33.0)); dirv = (p1 - p0).normalized(); perp = Vector((-dirv.y, dirv.x)); n_ = int((p1 - p0).length / 0.7)
    for k in range(n_):
        c2 = p0 + dirv * (k * 0.7); zz = float(mud_z(np.array([c2.x]), np.array([c2.y]))[0]) + 0.1
        beam(pm, (c2.x - perp.x * 1.5, c2.y - perp.y * 1.5, zz), (c2.x + perp.x * 1.5, c2.y + perp.y * 1.5, zz), 0.58, 0.16, M['walk'], uvk=0.3)
    for sg in (-1, 1): beam(pm, (p0.x + perp.x * 1.3 * sg, p0.y + perp.y * 1.3 * sg, -0.0), (p1.x + perp.x * 1.3 * sg, p1.y + perp.y * 1.3 * sg, 0.0), 0.2, 0.2, M['timber_d'], uvk=0.3)
    _obj(pm, 'street_planks', SET); STATE['fill_objs'].append(bpy.data.objects['street_planks'])
    bm = MB()
    for (xx, yy) in ((-26, -11.5), (-24.6, -11.0), (-25.4, -12.7), (16, -11.0), (17.4, -11.8), (-2, -44), (-0.6, -44.8), (48, -28), (49.4, -27.4), (-56, -30), (-57.2, -29.4), (-5.0, -20.0)):
        _barrel(bm, (xx, yy, float(mud_z(np.array([xx]), np.array([yy]))[0]) - 0.2), M, 'wood' if int(xx) % 2 else 'wood_d')
    for (xx, yy) in ((-22.0, -40.0), (-20.6, -40.8), (-21.6, -41.9), (-12.0, -44.0), (-10.8, -44.5), (-30.0, -45.0), (4.0, -43.0), (5.3, -43.6)):
        _barrel(bm, (xx, yy, float(mud_z(np.array([xx]), np.array([yy]))[0]) - 0.15), M, 'wood' if int(xx) % 2 else 'wood_l')
    _crate_stack(bm, (-5.0, -42.0, -0.1), M, 12, 6)
    _crate_stack(bm, (22.0, -11.0, -0.1), M, 8, 5); _crate_stack(bm, (-31.0, -12.0, -0.1), M, 9, 5); _crate_stack(bm, (52.0, -36.0, -0.1), M, 10, 4)
    # wheelbarrow, ladder, stakes with rope around the fill, shovels
    for (xx, yy, a) in ((-28.0, -19.5, 0.5), (36.0, -17.0, 2.5)):
        sbox(bm, (xx - 0.8, yy - 0.5, 0.7), (xx + 0.8, yy + 0.5, 1.1), M['wood'], 0.3); rod(bm, (xx - 1.6, yy, 0.8), (xx - 0.4, yy, 1.1), 0.08, M['wood_d'], seg=4); rod(bm, (xx + 0.9, yy, 0.55), (xx + 0.9, yy, 0.55), 0.01, M['iron'], seg=3)
        rod(bm, (xx + 0.9, yy - 0.55, 0.5), (xx + 0.9, yy + 0.55, 0.5), 0.5, M['wood_d'], seg=8, r1=0.5)
    _obj(bm, 'street_crates', SET); STATE['fill_objs'].append(bpy.data.objects['street_crates'])

def _church(SET, M):
    mb = MB(); x, y = 105.0, 210.0
    sbox(mb, (x - 7, y - 7, -0.5), (x + 7, y + 7, 34.0), M['stone_grey'], 0.15)
    for k in range(4): sbox(mb, (x - 4.5 + (k % 2) * 6.0, y - 7.1, 22.0), (x - 3.0 + (k % 2) * 6.0, y - 6.9, 30.0), M['dark'], 0.3) if False else None
    for sx in (-1, 1): sbox(mb, (x + sx * 2.8 - 1.0, y - 7.1, 24.0), (x + sx * 2.8 + 1.0, y - 6.8, 31.0), M['dark'], 0.3)
    sbox(mb, (x - 7.6, y - 7.6, 33.5), (x + 7.6, y + 7.6, 34.6), M['cream'], 0.3)
    mb.frustum((x, y, 34.6), (x, y, 66.0), 5.8, 0.25, M['slate'], seg=8); rod(mb, (x, y, 66.0), (x, y, 72.0), 0.12, M['brass'], seg=4); sbox(mb, (x - 1.0, y - 0.06, 69.5), (x + 1.0, y + 0.06, 70.2), M['brass'], 0.3)
    sbox(mb, (x - 17, y - 7, -0.5), (x - 7, y + 20, 20.0), M['brick_d'], 0.15)                                  # nave
    prism_roof(mb, x - 17.2, x - 6.8, y - 7.3, y + 20.3, 20.0, 7.0, M['slate'])
    _obj(mb, 'church', SET)

# ============================================================================= cellar (crawlspace under the hotel)
CX0, CX1, CY0, CY1 = -9.0, 19.0, -4.0, 56.0
CZ_B = 5.0      # underside of the cross beams = top of the jack pads
def _under(SET, P, M):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M); r = _rnd(11)
    xs_g = np.linspace(-60, 60, 120); ys_g = np.linspace(-20, 90, 110); X, Y = np.meshgrid(xs_g, ys_g)
    Z = 0.1 * np.sin(0.7 * X) * np.cos(0.5 * Y) + 0.05 * np.sin(2.1 * X + 1.0 * Y)
    # outside the cellar on the right: the sunlit mud street (the open side)
    tmud = grid_mesh('floor', xs_g, ys_g, Z, M['dirt'], uvs=(0.1, 0.1))
    fb = MB()                                                                                       # plank walkway down the middle, and boards
    for k in range(5): sbox(fb, (1.0 + k * 1.7, CY0, 0.0), (2.6 + k * 1.7, CY1 - 3, 0.12), M['plank_f'], 0.2)
    for yy in np.arange(0.0, CY1 - 3, 3.6): sbox(fb, (0.8, yy, 0.0), (9.0, yy + 0.35, 0.18), M['timber_d'], 0.3)
    _obj(fb, 'walkway', SET)
    # left wall (brick foundation) with shafts of light slots and the far wall
    wb = MB(); sbox(wb, (CX0 - 1.0, CY0, -0.5), (CX0, CY1, CZ_B + 2.6), M['brick_d'], 1 / 6); sbox(wb, (CX0, CY1, -0.5), (CX1 + 8, CY1 + 1.0, CZ_B + 2.6), M['brick_d'], 1 / 6)
    sbox(wb, (CX0, CY0 - 1.0, -0.5), (CX1 + 8, CY0, CZ_B + 2.6), M['rustic'], 1 / 8)
    for yy in np.arange(4.0, CY1, 8.0): sbox(wb, (CX0, yy, 3.4), (CX0 + 1.2, yy + 1.3, 3.9), M['ash'], 0.3) if False else None
    _obj(wb, 'cellar_walls', SET)
    # right side: open, timber posts and cribbing at the edge
    pb = MB()
    for yy in np.arange(0.0, CY1, 6.8): sbox(pb, (CX1 + 0.2, yy - 0.5, -0.1), (CX1 + 1.2, yy + 0.5, CZ_B), M['timber_d'], 0.3)
    _obj(pb, 'edge_posts', SET)
    # beams and joists above
    bm = MB(); rows = [6.0 + 3.4 * k for k in range(13)]
    for y in rows:
        sbox(bm, (CX0, y - 0.55, CZ_B), (CX1 + 1.5, y + 0.55, CZ_B + 1.5), M['timber_w'], 0.25)                                  # cross beams
        pass
    for xj in np.arange(CX0, CX1 + 2.0, 2.0): sbox(bm, (xj - 0.28, CY0, CZ_B + 1.5), (xj + 0.28, CY1, CZ_B + 2.4), M['timber'], 0.25)
    sbox(bm, (CX0, CY0, CZ_B + 2.4), (CX1 + 2.0, CY1, CZ_B + 2.6), M['plank_d'], 0.2)
    _obj(bm, 'floor_beams', SET)
    # jackfield: rows under each cross beam, columns every 3.2
    xs = [-6.0 + 3.2 * k for k in range(8)]
    so, sto, ho, nj = _jackfield(SET, M, CZ_B, xs, rows, 'jf')
    STATE['njacks'] = nj
    # fixed-height jacks for the cellar: stretch screw to the beam, head at the beam
    sto.location = (0, 0, 1.3); sto.scale = (1, 1, CZ_B - 0.4 - 1.3); ho.location = (0, 0, CZ_B)
    # crib stacks under the jack feet: timber blocks (2 layers) lift each jack a little
    # props: crates, barrels, buckets, rolled tarp, tool bars leaning, a workbench
    pr = MB()
    for (xx, yy) in ((-18.0, 2.0), (-18.5, 20.0), (16.0, 12.0), (15.0, 35.0), (-17.5, 41.0)): _crate_stack(pr, (xx, yy, 0.0), M, int(yy), 4)
    for (xx, yy) in ((-12.5, 3.0), (9.0, 6.0), (13.0, 25.0), (-15.0, 30.0), (10.0, 44.0)): _barrel(pr, (xx, yy, 0.0), M, 'wood')
    for (xx, yy) in ((-7.5, 14.0), (16.0, 30.0)):
        rod(pr, (xx, yy, 0.0), (xx, yy, 0.8), 0.4, M['iron'], seg=8, r1=0.5)
    for yy in (7.4, 18.0, 28.0, 38.0):                                                                              # tool bars leaning on beams
        rod(pr, (6.5, yy, 0.0), (7.4, yy + 0.3, 4.2), 0.07, M['iron'], seg=4)
    _obj(pr, 'cellar_props', SET)
    # oil lamps: hung from beams + a few on crates; real point lights + halo + pools
    lamps = [(-2.5, 6.0, 3.9), (5.0, 16.0, 3.9), (-2.0, 26.0, 3.9), (6.0, 38.0, 3.9), (1.0, 50.0, 3.9), (12.0, 10.0, 3.7)]
    fl = MB(); hb = MB()
    for k, (xl, yl, zl) in enumerate(lamps):
        c = Vector((xl, yl, zl)); rod(fl, c + Vector((0, 0, 0.5)), c + Vector((0, 0, CZ_B - zl)), 0.03, M['iron_d'], seg=4)
        fl.frustum(c - Vector((0, 0, 0.5)), c + Vector((0, 0, 0.5)), 0.26, 0.34, M['lamp_glass'], seg=7); fl.frustum(c + Vector((0, 0, 0.5)), c + Vector((0, 0, 0.8)), 0.38, 0.05, M['iron_d'], seg=7)
        _halo(fl, c, 2.4, M)
        D._flame_light('oil_%d' % k, tuple(c), LAMP, 1500 if k < 5 else 900, radius=0.15, shadow=(k % 2 == 0))
        pool = MB(); pool.face([Vector((xl - 5.5, yl - 5.5, 0.04)), Vector((xl + 5.5, yl - 5.5, 0.04)), Vector((xl + 5.5, yl + 5.5, 0.04)), Vector((xl - 5.5, yl + 5.5, 0.04))], M['pool'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        _obj(pool, 'pool_%d' % k, SET, shadow=False)
    _obj(fl, 'cellar_lamps', SET, shadow=False)
    STATE['marks'].update(worker_a=(-1.2, 12.0, 0.0), worker_b=(7.2, 17.5, 0.0), worker_c=(-5.3, 24.0, 0.0), worker_d=(3.0, 31.0, 0.0), foreman=(1.5, 7.5, 0.0))

# ============================================================================= suite (rich guest's top-floor room)
RX0, RX1, RY1 = -11.0, 11.0, 18.0
ZF = 30.0; RH = 6.2
def _suite(SET, P, M):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M)
    # the street seen from the window: terrain + opposite shops + street dressing (reuses the street builders, no hotel)
    mud_z = _street_ground(SET, M); _opposite(SET, M); _street_dress_lite(SET, M, mud_z); _church(SET, M)
    mb = MB(); WX0, WX1, WZ0, WZ1 = -3.6, 3.6, ZF + 0.35, ZF + 5.4
    # floor, rug, ceiling
    fm = MB(); fm.face([Vector((RX0, 0, ZF)), Vector((RX1, 0, ZF)), Vector((RX1, RY1, ZF)), Vector((RX0, RY1, ZF))], M['parquet'], [(0, 0), (RX1 - RX0, 0), (RX1 - RX0, RY1), (0, RY1)]) if False else None
    sbox(fm, (RX0, 0, ZF - 0.6), (RX1, RY1, ZF), M['parquet'], 1 / 8)
    _obj(fm, 'floor', SET)
    rg = MB(); rg.face([Vector((-5.5, 1.6, ZF + 0.03)), Vector((6.5, 1.6, ZF + 0.03)), Vector((6.5, 8.6, ZF + 0.03)), Vector((-5.5, 8.6, ZF + 0.03))], M['rug'], [(0, 0), (1, 0), (1, 1), (0, 1)]); _obj(rg, 'rug', SET)
    sbox(mb, (RX0, 0, ZF + RH), (RX1, RY1, ZF + RH + 0.6), M['cream'], 0.2)
    # walls with wallpaper: front wall (window), left, right, back; dado + skirting + picture rail + cornice
    wp = M['wallpaper']; t = 0.8
    sbox(mb, (RX0 - t, 0, ZF - 0.6), (RX0, RY1 + t, ZF + RH + 0.6), wp, 0.25); sbox(mb, (RX1, 0, ZF - 0.6), (RX1 + t, RY1 + t, ZF + RH + 0.6), wp, 0.25)
    sbox(mb, (RX0, RY1, ZF - 0.6), (RX1, RY1 + t, ZF + RH + 0.6), wp, 0.25)
    sbox(mb, (RX0 - t, -t, ZF - 0.6), (WX0, 0, ZF + RH + 0.6), M['brick'], 1 / 6); sbox(mb, (WX1, -t, ZF - 0.6), (RX1 + t, 0, ZF + RH + 0.6), M['brick'], 1 / 6)
    sbox(mb, (WX0, -t, ZF - 0.6), (WX1, 0, WZ0), M['brick'], 1 / 6); sbox(mb, (WX0, -t, WZ1), (WX1, 0, ZF + RH + 0.6), M['brick'], 1 / 6)
    # inner wall faces (wallpaper) on the front wall, around the window
    for (a, b, z0, z1) in ((RX0, WX0, ZF, ZF + RH), (WX1, RX1, ZF, ZF + RH), (WX0, WX1, ZF, WZ0), (WX0, WX1, WZ1, ZF + RH)):
        sbox(mb, (a, 0.0, z0), (b, 0.5, z1), wp, 0.25)
    # window reveal (stone sill, jambs) and the sash: mullions + transom bars (open: the street is seen through)
    sbox(mb, (WX0 - 0.3, -0.5, WZ0 - 0.3), (WX1 + 0.3, 0.6, WZ0), M['ash'], 0.3)
    sbox(mb, (WX0 - 0.3, -0.4, WZ1), (WX1 + 0.3, 0.6, WZ1 + 0.4), M['ash'], 0.3)
    for xx in (WX0, WX1): sbox(mb, (xx - 0.18, -0.1, WZ0), (xx + 0.18, 0.5, WZ1), M['white'], 0.3)
    for xx in (-1.2, 1.2): sbox(mb, (xx - 0.09, 0.1, WZ0), (xx + 0.09, 0.25, WZ1), M['white'], 0.3)
    for zz in (WZ0 + 0.0, (WZ0 + WZ1) / 2 + 0.3, WZ1 - 0.2): sbox(mb, (WX0, 0.1, zz - 0.09), (WX1, 0.25, zz + 0.09), M['white'], 0.3)
    for zz in (WZ0 + 1.2, WZ0 + 2.2, WZ1 - 1.0):
        for xx in (-2.4, -0.0, 2.4): pass
    for xx in (-2.4, 0.0, 2.4):
        for zz in (WZ0 + (WZ1 - WZ0) * 0.25, WZ0 + (WZ1 - WZ0) * 0.75): sbox(mb, (xx - 0.05, 0.1, zz - 0.05), (xx + 0.05, 0.25, zz + 0.05), M['white'], 0.3) if False else None
    # dado (wainscot), skirting, picture rail, cornice
    for (x0, x1, y0, y1, ax) in ((RX0, RX1, RY1 - 0.0, RY1 - 0.35, 'back'), (RX0, RX0 + 0.35, 0.5, RY1, 'left'), (RX1 - 0.35, RX1, 0.5, RY1, 'right')):
        sbox(mb, (x0, y0, ZF), (x1, y1, ZF + 2.0), M['plank_f'], 0.2) if ax == 'back' else sbox(mb, (x0, y0, ZF), (x1, y1, ZF + 2.0), M['plank_f'], 0.2)
        sbox(mb, (x0 - (0.1 if ax != 'back' else 0), y0 + (0.0 if ax != 'back' else -0.15), ZF + 2.0), (x1 + (0.1 if ax != 'back' else 0), y1 + (0.0 if ax != 'back' else 0.0), ZF + 2.2), M['cream'], 0.3)
    sbox(mb, (RX0, 0, ZF + RH - 0.9), (RX1, 0.5, ZF + RH), M['cream'], 0.3)
    sbox(mb, (RX0, 0, ZF + RH - 0.6), (RX0 + 0.6, RY1, ZF + RH), M['cream'], 0.3); sbox(mb, (RX1 - 0.6, 0, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3); sbox(mb, (RX0, RY1 - 0.6, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3)
    # curtains: velvet drapes either side of the window with tie-backs
    cm = MB()
    for sg in (-1, 1):
        for k in range(5):
            x0 = sg * (WX1 + 0.1) + sg * k * 0.35; ob = (x0, 0.6 - 0.04 * k, ZF + 0.3); sbox(cm, (min(x0, x0 + sg * 0.4), 0.45, ZF + 0.3 + 0.12 * (k % 2)), (max(x0, x0 + sg * 0.4), 0.95 + 0.1 * (k % 2), ZF + 5.9), M['velvet_red'], 0.4)
    rod(cm, (WX0 - 1.8, 0.7, ZF + 6.0), (WX1 + 1.8, 0.7, ZF + 6.0), 0.1, M['brass'], seg=6)
    for sg in (-1, 1): ell(cm, (sg * 4.0, 0.4, ZF + 6.0), 0.2, 0.2, 0.2, M['brass'], seg=6, rings=4)
    sbox(cm, (WX0 - 1.0, 0.45, ZF + 5.5), (WX1 + 1.0, 1.2, ZF + 6.15), M['velvet_red'], 0.4)                  # pelmet
    _obj(cm, 'curtains', SET); _obj(mb, 'room', SET)
    # framed paintings (no text) on the left wall and back wall + a gilt mirror
    pf = MB()
    def picture(mat, x, y, z, w, h, face):
        """face 'x+' hangs on the left wall (normal +x), 'y-' on the back wall (normal -y)."""
        if face == 'x+':
            sbox(pf, (x, y - w / 2 - 0.2, z - h / 2 - 0.2), (x + 0.22, y + w / 2 + 0.2, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x + 0.23, y - w / 2, z - h / 2), (x + 0.23, y + w / 2, z - h / 2), (x + 0.23, y + w / 2, z + h / 2), (x + 0.23, y - w / 2, z + h / 2)], mat, [(1, 0), (0, 0), (0, 1), (1, 1)], (1, 0, 0))
        elif face == 'y+':
            sbox(pf, (x - w / 2 - 0.2, y, z - h / 2 - 0.2), (x + w / 2 + 0.2, y + 0.22, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x + w / 2, y + 0.23, z - h / 2), (x - w / 2, y + 0.23, z - h / 2), (x - w / 2, y + 0.23, z + h / 2), (x + w / 2, y + 0.23, z + h / 2)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 0))
        else:
            sbox(pf, (x - w / 2 - 0.2, y - 0.22, z - h / 2 - 0.2), (x + w / 2 + 0.2, y, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x - w / 2, y - 0.23, z - h / 2), (x + w / 2, y - 0.23, z - h / 2), (x + w / 2, y - 0.23, z + h / 2), (x - w / 2, y - 0.23, z + h / 2)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    picture(M['p_lake'], RX0 + 0.35, 9.0, ZF + 3.9, 3.0, 2.2, 'x+'); picture(M['p_land'], RX0 + 0.35, 4.6, ZF + 3.8, 2.2, 3.0, 'x+'); picture(M['p_portrait'], RX0 + 0.35, 13.5, ZF + 3.9, 1.8, 2.4, 'x+')
    picture(M['p_still'], -5.5, RY1 - 0.35, ZF + 3.8, 2.6, 2.0, 'y-'); picture(M['p_land'], 0.0, RY1 - 0.35, ZF + 3.7, 2.2, 3.0, 'y-'); picture(M['p_portrait'], 5.5, RY1 - 0.35, ZF + 3.8, 1.8, 2.4, 'y-')
    picture(M['p_portrait'], 7.4, 0.5, ZF + 3.6, 1.8, 2.4, 'y+'); picture(M['p_lake'], -7.6, 0.5, ZF + 3.6, 3.0, 2.2, 'y+')
    _obj(pf, 'paintings', SET)
    fb = MB(); _furniture(fb, M); _obj(fb, 'furniture', SET)
    # chandelier
    ch = MB(); fl = MB(); c = Vector((-0.8, 4.6, ZF + 4.4)); rod(ch, (c.x, c.y, ZF + RH), c + Vector((0, 0, 0.3)), 0.06, M['brass'], seg=6)
    ell(ch, c, 0.5, 0.5, 0.5, M['brass'], seg=8, rings=5); rod(ch, c + Vector((0, 0, -0.5)), c + Vector((0, 0, -1.0)), 0.04, M['brass'], seg=5); ell(ch, c + Vector((0, 0, -1.05)), 0.2, 0.2, 0.2, M['brass'], seg=6, rings=4)
    for k in range(6):
        a = 2 * math.pi * k / 6; e = c + Vector((1.5 * math.cos(a), 1.5 * math.sin(a), -0.1))
        ch.frustum(c + Vector((0, 0, -0.05)), e, 0.05, 0.05, M['brass'], seg=4); rod(ch, e, e + Vector((0, 0, 0.5)), 0.08, M['brass'], seg=6); rod(ch, e + Vector((0, 0, 0.5)), e + Vector((0, 0, 0.9)), 0.07, M['white'], seg=6)
        fl.frustum(e + Vector((0, 0, 0.9)), e + Vector((0, 0, 1.05)), 0.07, 0.01, M['glass_cand'], seg=5); _halo(fl, e + Vector((0, 0, 1.0)), 0.5, M)
        for j in range(3): rod(ch, e + Vector((0, 0, 0.0)) + Vector((0.08 * j, 0, 0)), e + Vector((0.08 * j, 0, -0.55 - 0.1 * j)), 0.02, M['white'], seg=3)
    D._flame_light('chandelier', tuple(c + Vector((0, 0, 0.5))), LAMP, 700, radius=0.3, shadow=True)
    _obj(ch, 'chandelier', SET); _obj(fl, 'candles', SET, shadow=False)
    STATE['marks'].update(guest=(-6.2, 10.0, ZF), maid=(3.5, 6.0, ZF))

def _furniture(mb, M):
    """armchair (velvet, wood feet, gilt trim), tea table with cup / saucer / pot / plate, a side table with a vase."""
    def chair(cx, cy, yaw, mat):
        ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); P = lambda x, y, z: Vector((cx, cy, ZF)) + ex * x + ey * y + Z * z
        obox(mb, P(0, 0, 1.0), ex, ey, Z, 1.4, 1.35, 0.45, mat, 0.4)                                # seat cushion
        obox(mb, P(0, 1.2, 2.5), ex, ey, Z, 1.4, 0.28, 1.45, mat, 0.4)                                # back
        for sg in (-1, 1): obox(mb, P(sg * 1.5, 0, 1.55), ex, ey, Z, 0.28, 1.35, 0.55, mat, 0.4)    # arms
        for sg in (-1, 1): ell(mb, P(sg * 1.5, -1.3, 2.15), 0.34, 0.34, 0.34, mat, seg=8, rings=5)
        ell(mb, P(0, 1.2, 4.05), 1.4, 0.3, 0.2, mat, seg=10, rings=4, yaw=yaw)
        for sx in (-1, 1):
            for sy in (-1, 1): rod(mb, P(sx * 1.25, sy * 1.2, 0.0), P(sx * 1.25, sy * 1.2, 0.6), 0.16, M['wood_d'], seg=6, r1=0.1)
        obox(mb, P(0, -1.38, 1.1), ex, ey, Z, 1.42, 0.05, 0.12, M['brass'], 0.4)
    chair(-4.4, 4.4, math.radians(-30), M['velvet_red']); chair(6.3, 3.4, math.radians(30), M['velvet_teal'])
    # tea table (round top, pedestal), with service
    tx, ty = 0.8, 4.6; zt = ZF + 1.5
    mb.frustum((tx, ty, ZF), (tx, ty, zt - 0.1), 0.25, 0.2, M['wood_d'], seg=8); mb.frustum((tx, ty, zt - 0.1), (tx, ty, zt), 1.5, 1.5, M['wood'], seg=16)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.4; mb.frustum((tx, ty, ZF + 0.15), (tx + 1.2 * math.cos(a), ty + 1.2 * math.sin(a), ZF), 0.14, 0.1, M['wood_d'], seg=5)
    mb.frustum((tx, ty, zt), (tx, ty, zt + 0.03), 1.1, 1.1, M['white'], seg=16)                                        # cloth
    def cup(cx, cy, s=1.0):
        mb.frustum((cx, cy, zt + 0.03), (cx, cy, zt + 0.1 * s), 0.38 * s, 0.38 * s, M['white'], seg=12)                    # saucer
        mb.frustum((cx, cy, zt + 0.1 * s), (cx, cy, zt + 0.1 * s + 0.1 * s), 0.12 * s, 0.14 * s, M['white'], seg=10)
        mb.frustum((cx, cy, zt + 0.2 * s), (cx, cy, zt + 0.46 * s), 0.17 * s, 0.26 * s, M['white'], seg=12, cap1=False)
        mb.frustum((cx, cy, zt + 0.44 * s), (cx, cy, zt + 0.44 * s + 0.01), 0.23 * s, 0.23 * s, M['wood'], seg=12)       # tea surface
        mb.frustum((cx + 0.24 * s, cy, zt + 0.35 * s), (cx + 0.36 * s, cy, zt + 0.28 * s), 0.025 * s, 0.025 * s, M['white'], seg=4)
    cup(tx - 0.2, ty - 0.55, 1.5); cup(tx + 0.6, ty + 0.3, 1.5)
    mb.frustum((tx - 0.5, ty + 0.5, zt + 0.03), (tx - 0.5, ty + 0.5, zt + 0.7), 0.26, 0.36, M['white'], seg=10); ell(mb, (tx - 0.5, ty + 0.5, zt + 0.74), 0.3, 0.3, 0.14, M['white'], seg=8, rings=4)   # teapot
    mb.frustum((tx - 0.3, ty + 0.5, zt + 0.5), (tx + 0.1, ty + 0.55, zt + 0.72), 0.05, 0.03, M['white'], seg=4)
    mb.frustum((tx + 0.5, ty - 0.4, zt + 0.03), (tx + 0.5, ty - 0.4, zt + 0.08), 0.42, 0.42, M['brass'], seg=12)       # plate of cakes
    for k in range(3): ell(mb, (tx + 0.4 + 0.2 * k, ty - 0.4 + 0.1 * (k % 2), zt + 0.18), 0.13, 0.13, 0.1, M['clay'], seg=6, rings=4)
    # side table + vase + sideboard against the right wall
    mb.frustum((7.5, 12.0, ZF), (7.5, 12.0, ZF + 1.6), 0.18, 0.2, M['wood_d'], seg=6); mb.frustum((7.5, 12.0, ZF + 1.6), (7.5, 12.0, ZF + 1.72), 0.8, 0.8, M['wood'], seg=12)
    ell(mb, (7.5, 12.0, ZF + 2.3), 0.35, 0.35, 0.55, M['teal'], seg=8, rings=5); mb.frustum((7.5, 12.0, ZF + 2.7), (7.5, 12.0, ZF + 3.2), 0.12, 0.2, M['teal'], seg=7)
    sbox(mb, (RX1 - 2.2, 2.0, ZF), (RX1 - 0.4, 7.5, ZF + 2.5), M['plank_f'], 0.2); sbox(mb, (RX1 - 2.35, 1.9, ZF + 2.5), (RX1 - 0.3, 7.6, ZF + 2.7), M['ash'], 0.3)
    ell(mb, (RX1 - 1.2, 3.5, ZF + 3.1), 0.35, 0.35, 0.4, M['brass'], seg=8, rings=5); ell(mb, (RX1 - 1.2, 6.0, ZF + 3.0), 0.3, 0.3, 0.3, M['red'], seg=8, rings=5)

def _street_ground(SET, M):
    mud_z = _terrain(SET, M)
    sb = MB(); sbox(sb, (-110, -8.0, 0.2), (110, -3.0, 0.5), M['walk'], 0.2); _obj(sb, 'sidewalk', SET); return mud_z

def _opposite(SET, M):
    """the row of shops across the street (y -62..-50, facing +y), seen from the suite window."""
    mb = MB(); am = MB(); Fr = lambda x0: Frame((x0, -50.0, 0), 180)
    spec = [(-70, -46, 24.0, 'fac_a'), (-46, -26, 20.0, 'fac_b'), (-26, -2, 28.0, 'fac_c'), (-2, 18, 22.0, 'fac_d'), (18, 44, 25.0, 'fac_e'), (44, 66, 19.0, 'fac_f'), (66, 90, 26.0, 'fac_a')]
    for (x0, x1, h, fac) in spec:
        side = M['brick_b']
        mb.box((x0, -52.0, -1.0), (x1, -36.0, h), side, mats=dict(back=M[fac]), tile=(6, 6))
        sbox(mb, (x0 - 0.3, -36.3, h - 0.9), (x1 + 0.3, -34.9, h), M['cream'], 0.3); sbox(mb, (x0, -52.0, h), (x1, -35.8, h + 0.5), M['cream'], 0.3)
        sbox(mb, (x0 + 3.0, -48.0, h + 0.5), (x0 + 4.6, -46.4, h + 4.0), M['brick_d'], 1 / 6)
    _obj(mb, 'opp_shops', SET)

def _street_dress_lite(SET, M, mud_z):
    mb = MB(); fl = MB(); cm = MB(); wm = MB(); cf = MB()
    poles = [(x, -13.0) for x in (-112, -74, -36, 2, 40, 78, 116)]
    for (x, y) in poles: _pole(mb, x, y, M)
    for (a, b) in zip(poles, poles[1:]):
        for dx, dz in ((-2.2, 14.1), (-0.9, 14.1), (0.9, 14.1), (2.2, 14.1)): chain_rod(mb, catenary((a[0] + dx, a[1], dz), (b[0] + dx, b[1], dz), 0.9, 8), 0.06, M['iron_d'], seg=3)
    for xx in (-40, 28, -66, 56): _gas_lamp(mb, fl, (xx, -8.0, 0.5), M, 0)
    _obj(mb, 'street_furniture', SET); _obj(fl, 'lamps_glass', SET, shadow=False)
    _cart(cm, wm, cf, (-14.0, -29.5, 0.0), math.radians(18), M, sink=0.55, load='barrels', seed=3); _cart(cm, wm, cf, (33.0, -22.0, 0.0), math.radians(-155), M, sink=0.4, load='crates', seed=4)
    _cart(cm, wm, cf, (-44.0, -40.0, 0.0), math.radians(95), M, sink=0.5, load='crates', seed=5)
    _obj(cm, 'carts', SET); _obj(wm, 'cart_wheels', SET)
    _mound(SET, M, 'pile_a', -34.0, -17.0, 8.0, 4.4, 3.4, 4, M['clay'], mud_z); _mound(SET, M, 'pile_b', 40.0, -14.0, 7.0, 3.8, 2.6, 5, M['clay'], mud_z)
    bm = MB()
    for (xx, yy) in ((-26, -11.5), (-24.6, -11.0), (16, -11.0), (-2, -44), (48, -28), (-56, -30)): _barrel(bm, (xx, yy, float(mud_z(np.array([xx]), np.array([yy]))[0]) - 0.2), M, 'wood')
    _obj(bm, 'street_crates', SET)

# ============================================================================= hooks
def _fcs(idb):
    return T._fcurves(idb)

def set_lift(h, frame=None):
    """Lift the hotel: h 0..1 -> 0..LIFT_MAX D. Moves the hotel, awnings, portico, stair treads, jack heads and the under-floor beams; the screws
    and stair carriages stretch; cribbing layers appear as the building clears them. Keys are linear if frame is given."""
    L_ = float(h) * LIFT_MAX; STATE['lift'] = L_
    def _setloc(ob, z):
        ob.location.z = z
        if frame is not None: ob.keyframe_insert('location', index=2, frame=frame)
    for ob, dz in STATE.get('lift_movers', []): _setloc(ob, L_ + dz)
    for ob, z0 in STATE.get('lift_stretch', []):
        ob.location.z = z0; ob.scale.z = max(0.001, L_ - 0.4 - z0)
        if frame is not None: ob.keyframe_insert('scale', index=2, frame=frame); ob.keyframe_insert('location', index=2, frame=frame)
    N = 10; tot = GF + L_
    for kind, i, ob in STATE.get('steps', []):
        ztop = tot * (N - i) / N
        if kind == 'body': ob.scale.z = max(0.001, ztop - 0.34); ob.location.z = 0.0
        else: ob.location.z = ztop
        if frame is not None:
            ob.keyframe_insert('scale', index=2, frame=frame); ob.keyframe_insert('location', index=2, frame=frame)
    for li, ztop, ob in STATE.get('crib_layers', []):
        vis = ztop <= L_ - 0.35
        ob.hide_render = not vis; ob.hide_viewport = not vis
        if frame is not None: ob.keyframe_insert('hide_render', frame=frame)
    if frame is not None:
        for kind, i, ob in STATE.get('steps', []):
            for fc in _fcs(ob):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    return L_

def set_fill(k, frame=None):
    """Street fill level k 0..1 -> raises the mud, puddles, piles, carts, barrels by k * FILL_MAX D (sidewalks and buildings stay)."""
    for ob in STATE.get('fill_objs', []):
        ob.location.z = float(k) * FILL_MAX
        if frame is not None: ob.keyframe_insert('location', index=2, frame=frame)

def clear_keys():
    for ob in bpy.data.objects:
        if ob.animation_data: ob.animation_data_clear()

def apply_state(state):
    for tok in [t for t in (state or '').replace(' ', '').split(',') if t]:
        if tok.startswith('lift'): set_lift(float(tok[4:]))
        elif tok.startswith('fill'): set_fill(float(tok[4:]))

# ----------------------------------------------------------------------------- placeholders
T.PH.update(
    worker=('beach_man', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    foreman=('senior_b', dict(yaw=-0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    rich=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), 3.3),
    maid=('beach_woman', dict(yaw=-0.2, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.9),
    clerk=('senior_a', dict(yaw=0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor
STAGING = dict(
    street_wide=[('rich', (-6.5, -14.0, 0.0)), ('worker', (9.0, -13.0, 0.0)), ('foreman', (-9.0, -41.0, 0.0)), ('clerk', (22.0, -9.2, 0.5))],
    hotel_front=[('rich', (-3.0, -11.0, 0.0)), ('worker', (6.0, -12.0, 0.0))],
    front_stair=[('rich', (0.0, -7.0, 2.2))],
    mud_low=[('worker', (-4.0, -22.0, 0.0))],
    under_wide=[('worker', (3.8, 12.0, 0.0)), ('worker', (10.5, 21.0, 0.0)), ('foreman', (-3.0, 9.0, 0.0)), ('worker', (1.3, 29.0, 0.0))],
    jack_close=[('worker', (9.0, 14.5, 0.0))],
    suite_window=[('rich', (3.4, 1.6, ZF))],
    tea_close=[('rich', (-3.8, 9.6, ZF))])

def stage_placeholders(A, cam_name, cam_loc):
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(STAGING.get(cam_name, [])):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, tuple(mk), face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def anchors():
    P = STATE['P']; return dict(location=STATE['loc'], preset=STATE['preset'], light=STATE['light'], cams={k: dict(v) for k, v in CAMS.items()}, cam=dict(CAMS[PRESETS[STATE['preset']]['cam']]),
                                cam_name=PRESETS[STATE['preset']]['cam'], key_dir=tuple(Vector(P['key_dir']).normalized()), marks=dict(STATE.get('marks', {})), lights=[o.name for o in STATE['LIGHTS'].objects])

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def render_preset(preset, out, quality='final', actors=True, state=None, light=None):
    scene = bpy.context.scene; A = build(preset, light=light)
    if state: apply_state(state)
    setup_render(scene, quality); cam = make_camera(A['cam'])
    if actors: stage_placeholders(A, A['cam_name'], tuple(cam.location))
    t = T.render(out); return t

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'; names = sys.argv[2:] or list(PRESETS)
    q = 'final' if mode == 'final' else 'preview'; od = os.path.join(WORK, 'final' if mode == 'final' else 'stills'); os.makedirs(od, exist_ok=True)
    for n in names:
        t = render_preset(n, os.path.join(od, n + '.png'), q); print(n, 'wall %.1f cpu %.1f' % t, flush=True)
