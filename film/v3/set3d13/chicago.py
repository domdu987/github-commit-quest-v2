#!/usr/bin/env python3
"""chicago.py : set of film 13 ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) as a real 3D Blender set (bpy 5.3, Cycles CPU).
Three locations, built by preset (the preset picks the location, default light, camera and set state):

    import chicago as C
    A = C.build('street_wide')      # street: street_wide | hotel_front | front_stair | mud_low | rain_street | crowd_street      (DAY | RAIN | MORNING)
    A = C.build('under_rows')       # under : under_wide | under_rows | jack_close                                             (CELLAR)
    A = C.build('suite_two')        # suite : suite_window | tea_close | suite_two                                             (SUITE)
    cam = C.make_camera(A['cam']); C.stage_placeholders(A, A['cam_name'], tuple(cam.location))
    C.set_lift(0.5)  C.set_jack_turn(40)  C.set_fill(0.3)  C.set_tea_ripple(0)  C.crowd(20, region)  C.set_rain(1)

World: 1 unit = 1 D (head), Z up. NO depth of field, NO text. See API.md.  CLI: python3 chicago.py stills|final [spec ...]  spec = preset[:LIGHT[:state]]"""
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
LIFT_MAX = 3.6          # D: set_lift(1.0) = 3.6 D = about 1.2 character heights (~2 m)
CELL_LIFT = 1.0         # D: the cellar beams rise this much at set_lift(1.0)
FILL_MAX = 2.5          # D: set_fill(1.0)
GF = 2.6                # hotel plinth top (main floor level) above the foundation bottom (hotel base z 0 + lift)
STOREYS = [6.2, 5.5, 5.5, 5.2, 5.0, 4.6]
ZS = [GF + sum(STOREYS[:i]) for i in range(7)]     # floor levels; ZS[6] = top of the wall
HX0, HX1, HY1 = -20.0, 20.0, 30.0                  # hotel footprint x, depth
NB = 7                                             # bays
HEIGHT = dict(worker=3.0, foreman=3.0, rich=3.3, maid=2.9, clerk=3.0, kid=2.4, towns_m=3.1, towns_f=2.9, towns_o=3.0)

# ----------------------------------------------------------------------------- light presets
_kdaz = W9._kdaz
_B = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.6, lamps=0.0, refl_k=0.75, wet=0.0, beams=0.0)
LIGHTS = dict(
    DAY=dict(_B, lamps=0.6, key=(1.95, 1.42, 0.82), key_dir=_kdaz(325, 33), sun_elev=33, shade=(0.10, 0.105, 0.31), shade_tint=(0.095, 0.10, 0.33), shade_mix=0.55,
             grade_offset=(-0.006, -0.01, -0.014), lift=(0.008, 0.008, 0.02), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.18,
             bounce=(1.0, 0.62, 0.34, 0.26), beams=0.04, air=('#f2c88c', 0.30, 50.0, 520.0), wet=0.3),
    MORNING=dict(_B, lamps=0.35, key=(1.75, 1.28, 0.84), key_dir=_kdaz(338, 17), sun_elev=17, sun_angle=2.2, shade=(0.105, 0.11, 0.32), shade_tint=(0.10, 0.105, 0.34), shade_mix=0.6,
                 grade_offset=(-0.004, -0.008, -0.012), lift=(0.012, 0.011, 0.026), sky='CH_MORN', sky_k=0.95, pano='CHI', pano_k=0.85, grade_saturation=1.15,
                 bounce=(1.0, 0.7, 0.45, 0.2), beams=0.05, air=('#ffe0b0', 0.36, 40.0, 480.0), wet=0.2),
    RAIN=dict(_B, lamps=1.0, key=(0.62, 0.66, 0.82), key_dir=_kdaz(325, 52), sun_elev=52, sun_angle=9.0, shade=(0.12, 0.125, 0.335), shade_tint=(0.11, 0.115, 0.36), shade_mix=0.7,
              grade_offset=(-0.004, -0.006, -0.004), lift=(0.016, 0.016, 0.034), sky='CH_RAIN', sky_k=0.95, pano='CHI', pano_k=0.5, grade_saturation=1.12,
              bounce=(0.7, 0.75, 0.95, 0.10), beams=0.0, air=('#8c94b4', 0.5, 20.0, 300.0), wet=1.0),
    CELLAR=dict(_B, key=(1.95, 1.34, 0.72), key_dir=_kdaz(300, 30), sun_elev=30, sun_angle=0.5, shade=(0.092, 0.108, 0.30), shade_tint=(0.088, 0.104, 0.34), shade_mix=0.6,
                grade_offset=(-0.006, -0.01, -0.012), lift=(0.008, 0.012, 0.028), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.2,
                bounce=None, beams=0.05, air=('#d8b090', 0.12, 20.0, 160.0), lamps=1.0),
    SUITE=dict(_B, key=(1.95, 1.42, 0.82), key_dir=_kdaz(305, 36), sun_elev=36, shade=(0.20, 0.19, 0.55), shade_tint=(0.19, 0.18, 0.55), shade_mix=0.6,
               grade_offset=(-0.006, -0.01, -0.012), lift=(0.012, 0.01, 0.026), sky='CH_DAY', sky_k=0.95, pano='CHI', pano_k=0.95, grade_saturation=1.2,
               bounce=None, beams=0.03, air=('#f2c88c', 0.14, 80.0, 560.0), lamps=1.0, wet=0.3),
)
LOC_LIGHTS = dict(street=['DAY', 'RAIN', 'MORNING'], under=['CELLAR'], suite=['SUITE'])
PRESETS = dict(
    street_wide=dict(loc='street', light='DAY', cam='street_wide', state='lift0.7'),
    hotel_front=dict(loc='street', light='DAY', cam='hotel_front', state='lift0.7'),
    front_stair=dict(loc='street', light='DAY', cam='front_stair', state='lift1'),
    mud_low=dict(loc='street', light='DAY', cam='mud_low', state='lift0.5'),
    rain_street=dict(loc='street', light='RAIN', cam='rain_street', state='lift0'),
    crowd_street=dict(loc='street', light='DAY', cam='crowd_street', state='lift0.8'),
    under_wide=dict(loc='under', light='CELLAR', cam='under_wide', state='lift0.2'),
    under_rows=dict(loc='under', light='CELLAR', cam='under_rows', state='lift0.2,cut1'),
    jack_close=dict(loc='under', light='CELLAR', cam='jack_close', state='lift0.2,jack30'),
    suite_window=dict(loc='suite', light='SUITE', cam='suite_window', state=''),
    tea_close=dict(loc='suite', light='SUITE', cam='tea_close', state='tea0'),
    suite_two=dict(loc='suite', light='SUITE', cam='suite_two', state=''),
)
CAMS = dict(
    street_wide=dict(loc=(-30.0, -58.0, 2.8), look_at=(-4.0, 0.0, 15.5), lens=22),
    hotel_front=dict(loc=(-6.0, -26.0, 1.3), look_at=(0.0, 0.0, 17.0), lens=20),
    front_stair=dict(loc=(5.0, -15.0, 2.8), look_at=(0.0, -2.0, 6.8), lens=24),
    mud_low=dict(loc=(-14.0, -38.0, 0.9), look_at=(0.0, -12.0, 3.2), lens=20),
    rain_street=dict(loc=(-22.0, -52.0, 3.4), look_at=(0.0, 0.0, 13.0), lens=22),
    crowd_street=dict(loc=(-6.0, -34.0, 2.6), look_at=(0.0, -8.0, 7.5), lens=24),
    under_wide=dict(loc=(3.0, -3.0, 2.3), look_at=(8.0, 30.0, 2.3), lens=22),
    under_rows=dict(loc=(4.0, -6.0, 17.0), look_at=(5.0, 30.0, 1.5), lens=24),
    jack_close=dict(loc=(2.0, 5.0, 2.0), look_at=(7.0, 14.0, 2.2), lens=26),
    suite_window=dict(loc=(-2.6, 2.2, 32.5), look_at=(2.0, -12.0, 22.0), lens=22),
    tea_close=dict(loc=(0.4, 4.6, 33.2), look_at=(-1.6, 2.0, 31.6), lens=32),
    suite_two=dict(loc=(-3.4, 2.8, 32.6), look_at=(0.8, -8.0, 27.4), lens=22),
)
CAM_NOTES = {}

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

def ell(mb, c, rx, ry, rz, mat, seg=10, rings=6, yaw=0.0, pitch=0.0, rot=None):
    """Faceted ellipsoid centred c with radii (rx, ry, rz); rotated by `rot` (3x3) or by yaw about z and pitch about x."""
    c = Vector(c); R = []; mb.pid += 1; rot = rot if rot is not None else Matrix.Rotation(yaw, 3, 'Z') @ Matrix.Rotation(pitch, 3, 'X')
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; row.append(c + rot @ Vector((rx * math.sin(th) * math.cos(ph), ry * math.sin(th) * math.sin(ph), -rz * math.cos(th))))
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat, [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)])

def sbox(mb, lo, hi, mat, uvk=0.17):
    c = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
    obox(mb, c, (1, 0, 0), (0, 1, 0), (0, 0, 1), (hi[0] - lo[0]) / 2, (hi[1] - lo[1]) / 2, (hi[2] - lo[2]) / 2, mat, uvk)

def prism_roof(mb, x0, x1, y0, y1, z, h, mat, uvk=0.17):
    ym = (y0 + y1) / 2
    mb.oface([(x0, y0, z), (x1, y0, z), (x1, ym, z + h), (x0, ym, z + h)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -h, (y1 - y0) / 2))
    mb.oface([(x0, y1, z), (x1, y1, z), (x1, ym, z + h), (x0, ym, z + h)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, h, (y1 - y0) / 2))

def _tex_node(m): return [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]

def _new_obj(mb, name, SET, shadow=True, lst=None):
    ob = _obj(mb, name, SET, shadow=shadow)
    if lst is not None: lst.append(ob)
    return ob

# ----------------------------------------------------------------------------- build
def build(preset='street_wide', clear=True, light=None, state=None):
    assert preset in PRESETS, 'preset %s not in %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; loc = PR['loc']; lkey = light or PR['light']; scene = bpy.context.scene
    assert lkey in LOC_LIGHTS[loc], 'light %s: %s has %s' % (lkey, loc, LOC_LIGHTS[loc])
    P = dict(LIGHTS[lkey])
    STATE.clear(); STATE.update(P=P, preset=preset, loc=loc, area=loc, light=lkey)
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_sun_screen', '_cards_face', '_tea_phase'): h.remove(f)
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
    STATE.update(flames=[], flame_mats=list(M['_flame_mats']), marks={}, cards=[], movers=[], bars=[], mid=[], fill_objs=[], crib_layers=[], cut_objs=[], lift_k=0.0, protos={})
    if loc == 'street': _street(SET, P, M)
    elif loc == 'under': _under(SET, P, M)
    else: _suite(SET, P, M)
    scene.cycles.use_light_tree = False
    MN._denoise(scene); setup_grade(scene); W9._air_comp(scene, P)
    if lkey == 'RAIN': W9._rain_comp(scene)
    for ob in SET.objects:
        no_bounce(ob)
        if loc in ('street', 'suite') or ob.name in ('sky',): ob.visible_glossy = True
    if 'sky_obj' in STATE: STATE['sky_obj'].visible_glossy = True
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        if _cards_face not in h: h.append(_cards_face)
    set_flames(1.0)
    apply_state(PR.get('state', '') if state is None else state)
    if lkey == 'RAIN': set_rain(1.0)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    MN.setup_render(scene, quality); scene.cycles.transparent_max_bounces = 24
    if STATE.get('loc') in ('street', 'suite'): scene.cycles.glossy_bounces = 1

def make_camera(setup, name='cam', scene=None):
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 6000.0; ob.data.dof.use_dof = False
    _cards_face(bpy.context.scene); return ob

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
             iron=_glossy(C('#5a5e6c', 1.0, 1.6), (1.0, 0.85, 0.7), 0.35, 0.3), iron_d=C('#34363f', 1.0, 1.8),
             iron_k=_glossy(C('#2c2e38', 1.0, 1.9), (1.0, 0.85, 0.7), 0.45, 0.28), iron_bar=_glossy(C('#4c505e', 1.0, 1.7), (1.0, 0.85, 0.7), 0.5, 0.25), thread=TX('thread', gain=0.75, sm=1.5),
             jack_red=_glossy(C('#c04a2c', 1.0, (1.5, 0.9, 0.8), smix=0.25), (1.0, 0.8, 0.6), 0.4, 0.3), brass=_glossy(C('#b8923e', 1.0, (2.0, 1.5, 0.6), smix=0.2), (1.0, 0.8, 0.5), 0.5, 0.22),
             dirt=TX('mud_wet', form=False), stair_stone=TX('ash'), wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b8925e'), rope=C('#c8a868'), cream=C('#ecdcb6'), white=C('#efe8d8'),
             dark=C('#2a2a32', 1.0, 1.6, form=False), red=C('#b02a22', 1.0, (1.4, 0.8, 0.7), smix=0.25), teal=C('#2f8a82', 1.0, 1.0, smix=0.3), green=C('#3e6a46'), slate=C('#59607a'), stone=C('#b0a898'),
             canvas=C('#d8c89a'), sack=C('#c9b78c'), hay=C('#d4b45c'), door=C('#2e5a4c'), door_r=C('#7a2a24', 1.0, (1.4, 0.8, 0.7), smix=0.25), horse=C('#8a5230'), horse_d=C('#4a2c1a'), horse_g=C('#8a8680'),
             horse_w=C('#dcd2bc'), skin=C('#d8a880'), coal=C('#26262a', 1.0, 0.9),
             lamp_glass=mat_emit(pre + 'e_lampglass', '#ffd890', strength=3.4 * max(0.2, lk)), glass_cand=mat_emit(pre + 'e_cand', '#fff0b8', strength=6.0),
             flag_r=TX('awn_rc'), flag_b=C('#2c3f86'),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.6, 0.3), 0.8 if lk > 0 else 0.5), pool=MN._mat_pool(pre + 'poolmat', (1.0, 0.6, 0.28), 0.55),
             shaft=BK._mat_add(pre + 'shaft', tx['shaft'], (1.0, 0.82, 0.55), 0.5))
    M['_flame_mats'] = [M['lamp_glass']]
    M['sky'] = D._mat_sky(pre + 'sky', dict(P, star_k=0.0), tx['sky_' + P['sky']], P['sky_k'])
    M['mud'] = _mud_mat(pre, P, tx); M['puddle'] = _puddle_mat(pre, P, tx); M['scum'] = _scum_mat(pre, P, tx); M['tea'] = _tea_mat(pre, P)
    return M

def _mud_mat(pre, P, tx):
    """Street mud: painted grey-brown ochre blended to a wet dark grey-brown by height (troughs, ruts and puddle rims), a soft broad GGX sheen
    (wetter in RAIN), not polished."""
    m = _untoon(mat_lit(pre + 'mud', image=tx['mud'], form=tuple(P['form']), shade_mix=0.35, gain=0.85)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); links0 = list(tex.outputs['Color'].links); tex.extension = 'REPEAT'
    t2 = N('ShaderNodeTexImage'); t2.image = T._img(tx['mud_wet']); t2.extension = 'REPEAT'
    geo = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Object'], sp.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'; mr.inputs['From Min'].default_value = -0.42; mr.inputs['From Max'].default_value = 0.10; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    L(sp.outputs['Z'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(mr.outputs['Result'], mx.inputs[0]); L(tex.outputs['Color'], mx.inputs[6]); L(t2.outputs['Color'], mx.inputs[7])
    for l in links0: to = l.to_socket; nt.links.remove(l); L(mx.outputs[2], to)
    w = float(P.get('wet', 0.3))
    _glossy(m, (1.0, 0.86, 0.68), 0.10 + 0.34 * w, 0.5 - 0.3 * w)
    return m

def _puddle_mat(pre, P, tx):
    """Puddle water: dark grey-brown base (shade stays painted) + a mirror (sharp GGX + glossy bounce): hotel, sky, lamps."""
    m = _untoon(mat_lit(pre + 'puddle', '#4a4038', form=tuple(P['form']), shade_mix=0.5, gain=0.7))
    def make(nt):
        gl = nt.nodes.new('ShaderNodeBsdfGlossy' if False else 'ShaderNodeBsdfAnisotropic'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.02; gl.inputs['Color'].default_value = (0.9, 0.88, 0.86, 1)
        return gl.outputs['BSDF']
    MN._append_shader(m, make)
    return m

def _scum_mat(pre, P, tx):
    """soft foam / scum on the puddles: pale tan blotches (image alpha) over the water."""
    return _untoon(mat_lit(pre + 'scum', image=tx['scum'], form=tuple(P['form']), alpha=True, shade_mix=0.4, gain=0.95))

def _tea_mat(pre, P):
    """Tea surface: dark amber diffuse + sharp mirror; Value 'ripple_k' (0 = perfectly flat mirror) scales a noise bump on the normal, 'ripple_p' is its phase."""
    m = _untoon(mat_lit(pre + 'tea', '#7a3e1a', form=None, shade_mix=0.3, gain=0.75)); nt = m.node_tree
    rk = D._value(nt, 'ripple_k', 0.0); rp = D._value(nt, 'ripple_p', 0.0); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.inputs['Scale'].default_value = 9.0; nz.inputs['Detail'].default_value = 1.0
    L(tc.outputs['Object'], nz.inputs['Vector']); L(rp.outputs[0], nz.inputs['W'])
    bp = N('ShaderNodeBump'); bp.inputs['Distance'].default_value = 0.02; L(rk.outputs[0], bp.inputs['Strength']); L(nz.outputs['Fac'], bp.inputs['Height'])
    def make(nt2):
        gl = nt2.nodes.new('ShaderNodeBsdfAnisotropic'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.0; gl.inputs['Color'].default_value = (1.0, 0.98, 0.95, 1)
        nt2.links.new(bp.outputs['Normal'], gl.inputs['Normal']); return gl.outputs['BSDF']
    MN._append_shader(m, make)
    dif = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfDiffuse'][0]; L(bp.outputs['Normal'], dif.inputs['Normal'])
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
    mb = MB(); R = 430.0; fm = STATE['TX']('far_ground', form=False)
    mb.face([Vector((-R, -R, z)), Vector((R, -R, z)), Vector((R, R, z)), Vector((-R, R, z))], fm, [(0, 0), (R / 8, 0), (R / 8, R / 8), (0, R / 8)]); _obj(mb, 'far_ground', SET)

# ============================================================================= terrain: mud with ruts and layered puddles
# (cx, cy, rx, ry, depth): ellipse basins; the long thin ones sit in the wheel ruts
PUDDLES = [(-14, -31, 6.0, 4.8, 0.85), (6, -37, 4.5, 3.6, 0.7), (-33, -24, 4.0, 3.2, 0.7), (18, -23, 5.2, 4.2, 0.8), (-3, -16.5, 3.0, 2.4, 0.65), (30, -34, 3.8, 3.0, 0.7),
           (-22, -42, 4.2, 3.4, 0.7), (11, -12.5, 2.6, 2.0, 0.6), (-40, -35, 4.2, 3.4, 0.7), (40, -21, 3.5, 2.8, 0.65), (-9, -24, 2.1, 1.7, 0.6), (24, -41, 2.7, 2.2, 0.6),
           (-8, -46, 3.8, 3.0, 0.7), (12, -47, 3.2, 2.6, 0.7), (-36, -46, 2.7, 2.2, 0.6), (-2, -29.4, 9.0, 0.75, 0.5), (22, -35.0, 8.0, 0.7, 0.5), (-26, -26.0, 7.0, 0.65, 0.5),
           (14, -38.2, 7.0, 0.7, 0.45), (-18, -35.0, 6.0, 0.7, 0.5), (-50, -30, 4.0, 3.2, 0.6), (52, -30, 4.0, 3.2, 0.6),
           (-27, -50, 6.0, 4.6, 0.85), (-12, -46, 6.5, 4.6, 0.8), (6, -52, 5.5, 4.0, 0.8), (-20, -56, 4.5, 3.0, 0.7), (-36, -42, 4.5, 3.4, 0.7), (-44, -48, 4.5, 3.5, 0.7), (22, -52, 5.0, 3.6, 0.7), (-4, -9.4, 2.4, 1.4, 0.5)]
def _terrain(SET, M):
    """Smooth mud height field (shared vertices): rolling noise, wheel ruts, a crown, elliptical puddle basins; flat water discs sit at each basin's lowest rim
    height so the terrain cuts the outline; a second scum disc 0.1 higher floats pale blotches near the rim (soft foam edge)."""
    xs = np.unique(np.round(np.concatenate([np.arange(-150, -76, 4.0), np.arange(-76, 76, 0.5), np.arange(76, 151, 4.0)]), 3))
    ys = np.unique(np.round(np.concatenate([np.arange(-130, -70, 4.0), np.arange(-70, -2, 0.45), np.arange(-2, 60, 4.0)]), 3))
    def sm(a, b, v):
        t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
    def mud_z(x, y):
        win = sm(-70, -60, y) * (1 - sm(-11, -7.5, y)); flat = np.ones_like(x * 1.0)
        for (cx, cy, rx, ry, dp) in PUDDLES: flat = flat * (1 - 0.85 * np.exp(-(((x - cx) / (rx * 1.5)) ** 2 + ((y - cy) / (ry * 1.5)) ** 2)))
        z = 0.2 * np.sin(0.21 * x + 0.7) * np.cos(0.17 * y + 1.1) + 0.12 * np.sin(0.43 * x + 0.2 * y) + 0.07 * np.sin(0.93 * x - 0.6 * y + 2.0)
        for yr in (-26.0, -29.4, -35.0, -38.2): z = z - 0.34 * np.exp(-((y - yr + 0.4 * np.sin(0.06 * x)) / 0.6) ** 2) * (0.75 + 0.25 * np.sin(0.11 * x + yr))
        z = (z + 0.2 * np.exp(-((y + 27.7) / 1.1) ** 2) + 0.15 * np.exp(-((y + 36.6) / 0.9) ** 2)) * flat * win
        for (cx, cy, rx, ry, dp) in PUDDLES: z = z - dp * np.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
        return z
    X, Y = np.meshgrid(xs, ys); Z = mud_z(X, Y)
    terr = grid_mesh('mud', xs, ys, Z, M['mud'], uvs=(0.1, 0.1)); STATE['terrain'] = terr; STATE['fill_objs'].append(terr); STATE['mud_z'] = mud_z
    pm = MB(); sc = MB(); n = 32
    for (cx, cy, rx, ry, dp) in PUDDLES:
        ang = np.linspace(0, 2 * math.pi, 48, endpoint=False); rim = mud_z(cx + rx * 2.2 * np.cos(ang), cy + ry * 2.2 * np.sin(ang)); zw = min(float(rim.min()) - 0.02, -0.12)
        for (mbx, k, dz, mat) in ((pm, 2.3, 0.0, M['puddle']), (sc, 2.0, 0.09, M['scum'])):
            pts = [Vector((cx + rx * k * math.cos(2 * math.pi * j / n), cy + ry * k * math.sin(2 * math.pi * j / n), zw + dz)) for j in range(n)]
            for j in range(n):
                a, b = pts[(j + 1) % n], pts[j]; c = Vector((cx, cy, zw + dz))
                mbx.face([c, a, b], mat, [(cx * 0.08, cy * 0.08), (a.x * 0.08, a.y * 0.08), (b.x * 0.08, b.y * 0.08)])
    po = _obj(pm, 'puddles', SET); so = _obj(sc, 'scum', SET, shadow=False); STATE['fill_objs'] += [po, so]
    return mud_z

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
    fr.box(mb, (0, 0, 0.0), (W_, 0.8, GF), M['rustic'], 1 / 8)
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
        fs.box(mb, (0, 0, 0.0), (HY1, 0.8, GF), M['rustic'], 1 / 8)
    sbox(mb, (HX0, HY1 - 0.5, 0.0), (HX1, HY1, ZS[6] + 3.0), M['brick_b'], 1 / 6)
    sbox(mb, (HX0 + 0.8, 0.7, 0.0), (HX1 - 0.8, HY1 - 0.5, ZS[6] + 0.5), M['brick_d'], 1 / 6)      # solid core
    ho = _obj(mb, 'hotel', SET); STATE['movers'].append((ho, 0.0)); STATE['hotel'] = ho
    # awnings over the main-floor windows (striped canvas) + the portico
    am = MB(); k = 0
    for i in range(NB):
        if i == 3: continue
        cx = HX0 + (i + 0.5) * bw; mat = [M['awn_rc'], M['awn_tc'], M['awn_oc']][k % 3]; k += 1; zb = ZS[0] + 0.5 + 4.35
        _awning(am, cx, 0.0, zb - 0.2, 3.5, 2.2, 1.7, mat, M)
    _obj(am, 'hotel_awn', SET); STATE['movers'].append((bpy.data.objects['hotel_awn'], 0.0))
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
    _obj(pm, 'hotel_portico', SET); STATE['movers'].append((bpy.data.objects['hotel_portico'], 0.0))
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
    """grand front stair: 10 stone steps that STAY at the old street level (top z = GF) plus a static stone landing; the hotel's portico landing and door rise
    away from it (set_lift): at lift 1 the door threshold is LIFT_MAX above the stair top."""
    N = 10; xw0, xw1 = xc - 5.4, xc + 5.4; y_top, y_bot = -4.0, -9.0; dy = (y_top - y_bot) / N; mb = MB()
    for i in range(N):
        ya, yb = y_bot + i * dy, y_bot + (i + 1) * dy; zt = GF * (i + 1) / N
        sbox(mb, (xw0, ya, -0.3), (xw1, yb, zt - 0.14), M['rustic'], 0.15); sbox(mb, (xw0 - 0.2, ya - 0.1, zt - 0.14), (xw1 + 0.2, yb, zt), M['ash'], 0.3)
    sbox(mb, (xw0 - 0.2, y_top - 0.1, -0.3), (xw1 + 0.2, -1.4, GF - 0.1), M['ash'], 0.3)                                   # static landing (top z GF - 0.1)
    for sx in (xw0 - 0.45, xw1 + 0.45):                                                                                      # iron rail on posts
        for k in range(6):
            yy = y_bot + 0.3 + k * 1.0; zz = GF * (yy - y_bot) / (y_top - y_bot); rod(mb, (sx, yy, zz), (sx, yy, zz + 2.2), 0.09, M['iron_d'], seg=5)
        beam(mb, (sx, y_bot + 0.3, 2.2 + 0.0), (sx, y_top, GF + 2.2), 0.14, 0.14, M['iron_d'])
    _obj(mb, 'stair', SET); STATE['stair_x'] = (xw0, xw1, y_bot, y_top, N)

# ============================================================================= jackscrews and cribbing (street gap + cellar)
def _jack(sm, mv, x, y, zb, S, M, crib=0, hd=0.55):
    """one dark-iron screw jack. static: timber block / crib stack, base flange, housing (zb .. zb + 0.75) with a collar. mover (relative to the underside it pushes,
    z 0 = the underside): the threaded screw of length S hanging inside the housing, a head cap and a timber pad. The turning bar is a separate rotating object."""
    z = zb
    for li in range(crib):                                                       # crib layers under the jack (alternating directions)
        for off in (-0.45, 0.45):
            if li % 2 == 0: sbox(sm, (x - 0.95, y + off - 0.22, z), (x + 0.95, y + off + 0.22, z + 0.42), M['timber'], 0.28)
            else: sbox(sm, (x + off - 0.22, y - 0.95, z), (x + off + 0.22, y + 0.95, z + 0.42), M['timber_w'], 0.28)
        z += 0.42
    zb = z
    sbox(sm, (x - 0.75, y - 0.75, zb), (x + 0.75, y + 0.75, zb + 0.3), M['timber_d'], 0.3)                    # base plank under the flange
    zb += 0.3
    rod(sm, (x, y, zb), (x, y, zb + 0.12), 0.62, M['iron_k'], seg=8); rod(sm, (x, y, zb + 0.12), (x, y, zb + 0.78), 0.46, M['iron_k'], seg=8, r1=0.36)
    rod(sm, (x, y, zb + 0.55), (x, y, zb + 0.72), 0.55, M['iron_k'], seg=8)
    for k in range(4):                                                            # lugs on the housing
        a = k * math.pi / 2 + 0.4; sm.frustum((x + 0.4 * math.cos(a), y + 0.4 * math.sin(a), zb + 0.3), (x + 0.58 * math.cos(a), y + 0.58 * math.sin(a), zb + 0.3), 0.07, 0.07, M['iron_d'], seg=4)
    rod(mv, (x, y, -0.3 - S), (x, y, -0.3), 0.23, M['thread'], seg=8, uv=(1.0, S * 2.5))                          # threaded screw
    rod(mv, (x, y, -0.3 - hd), (x, y, -0.3), 0.46, M['iron_k'], seg=8, r1=0.4); rod(mv, (x, y, -0.3 - hd * 0.5 - 0.12), (x, y, -0.3 - hd * 0.5 + 0.12), 0.56, M['iron_d'], seg=8)                                         # head cap (bar passes through it)
    sbox(mv, (x - 0.7, y - 0.7, -0.1), (x + 0.7, y + 0.7, 0.0), M['timber'], 0.3); rod(mv, (x, y, -0.3), (x, y, -0.1), 0.3, M['iron_d'], seg=8)
    return zb + 0.78

def _bar_obj(SET, M, x, y, z, name, phase):
    """turning bar: an iron lever through the jack head, a separate object so set_jack_turn can rotate it about the jack axis."""
    mb = MB(); rod(mb, (-1.45, 0, 0), (1.75, 0, 0), 0.085, M['iron_bar'], seg=5)
    for sx in (-1.45, 1.75): rod(mb, (sx, 0, 0), (sx + (-0.12 if sx < 0 else 0.12), 0, 0), 0.13, M['iron_d'], seg=5)
    ob = _obj(mb, name, SET); ob.location = (x, y, z); ob.rotation_euler = (0, 0, phase); return ob

def _jackfield(SET, M, xs, ys, name, zb, crib, S, head_base, skip=(), bars=True, hd=0.55):
    """a grid of jacks: one static mesh (blocks + housings), one mover mesh (screws + heads + pads, location z = head_base + lift) and one bar object per jack
    (location z = head_base - 0.45 + lift, rotation about z = the turn). Returns (static, mover, n)."""
    sm, mv = MB(), MB(); n = 0
    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            if any(abs(x - px) < sx and abs(y - py) < sy for (px, py, sx, sy) in skip): continue
            _jack(sm, mv, x, y, zb, S, M, crib, hd)
            if bars:
                ph = ((n * 37) % 11) * 0.03 - 0.15; bz = head_base - 0.3 - hd * 0.5; bo = _bar_obj(SET, M, x, y, bz, '%s_bar%d' % (name, n), ph); STATE['bars'].append((bo, bz, ph, x, y))
            n += 1
    so = _obj(sm, name + '_static', SET); mo = _obj(mv, name + '_head', SET); STATE['movers'].append((mo, head_base)); return so, mo, n

def _cribs(SET, M, piers, name, lmax):
    """timber cribbing piers (crossed layers of squared timbers, one object per layer index); layer li exists once the building has cleared its top (set_lift)."""
    nl = int(lmax / 0.5) + 1; out = []
    for li in range(nl):
        mb = MB(); z0 = li * 0.5
        for (x, y) in piers:
            for off in (-0.65, 0.65):
                if li % 2 == 0: sbox(mb, (x - 1.3, y + off - 0.3, z0), (x + 1.3, y + off + 0.3, z0 + 0.5), M['timber'], 0.28)
                else: sbox(mb, (x + off - 0.3, y - 1.3, z0), (x + off + 0.3, y + 1.3, z0 + 0.5), M['timber_w'], 0.28)
        ob = _obj(mb, '%s_layer%d' % (name, li), SET); out.append((li, z0 + 0.5, ob))
    return out

# ============================================================================= street
def _street(SET, P, M, hotel=True, opp=False):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M)
    mud_z = _terrain(SET, M)
    sb = MB()
    for (x0, x1, zt, y0, y1) in ((-110, -28, 1.3, -8.5, -3.2), (20, 110, 0.5, -8.0, -3.0)):
        sbox(sb, (x0, y0, zt - 0.3), (x1, y1, zt), M['walk'], 0.2); sbox(sb, (x0, y0 - 0.25, zt - 0.5), (x1, y0, zt + 0.12), M['plank_d'], 0.3)
        for xp in np.arange(x0 + 2, x1, 5.5): sbox(sb, (xp, y0, -0.4), (xp + 0.4, y0 + 0.4, zt - 0.3), M['timber_d'], 0.3)
    for xx in (-27.6, 19.6):
        for k in range(3): sbox(sb, (xx, -8.0 - k * 0.7 - 0.7, 0.0), (xx + 4.0, -8.0 - k * 0.7, 1.0 - 0.3 * k), M['walk'], 0.2)
    _obj(sb, 'sidewalk', SET)
    if hotel:
        _hotel(SET, M, P)
        xj = [-18.0 + 3.0 * k for k in range(13)]; yj = [1.3, 6.0, 11.0, 16.0, 21.5, 27.0]; piers = [(x, y) for x in (-19.0, -9.5, 0.0, 9.5, 19.0) for y in (1.3, 11.0, 21.5)] + [(-5.0, -2.6), (5.0, -2.6)]
        skip = [(px, py, 2.0, 1.6) for (px, py) in piers]
        so, mo, nj = _jackfield(SET, M, xj, yj, 'jf', 0.0, 0, 3.0, 0.0, skip=skip); STATE['njacks'] = nj
        STATE['crib_layers'] = _cribs(SET, M, piers, 'crib', LIFT_MAX)
        fl = MB()
        for (xl, yl) in ((-12.0, 3.6), (3.0, 3.6), (12.0, 3.6)):
            c = Vector((xl, yl, 0.0)); rod(fl, c + Vector((0, 0, -0.9)), c + Vector((0, 0, -0.55)), 0.03, M['iron_d'], seg=4)
            fl.frustum(c + Vector((0, 0, -1.2)), c + Vector((0, 0, -0.62)), 0.2, 0.26, M['lamp_glass'], seg=7); _halo(fl, c + Vector((0, 0, -0.95)), 2.2, M)
        lo = _obj(fl, 'under_lamps', SET, shadow=False); STATE['movers'].append((lo, 0.0))
        for k, xl in enumerate((-12.0, 3.0, 12.0)): D._flame_light('gap_%d' % k, (xl, 3.0, 1.4), LAMP, 700, radius=0.3, shadow=False)
        gb = MB(); gb.face([Vector((HX0, 0.8, 0.02)), Vector((HX1, 0.8, 0.02)), Vector((HX1, HY1, 0.02)), Vector((HX0, HY1, 0.02))], M['dirt'], [(0, 0), (4, 0), (4, 3), (0, 3)]); _obj(gb, 'under_floor', SET)
    _neighbours(SET, M, hotel=hotel)
    if opp: _opposite(SET, M)
    _street_dress(SET, M, mud_z, hotel=hotel); _church(SET, M)
    return mud_z

def _shop(mb, M, x0, x1, h, facname, y0=0.0, depth=22.0, zb=0.0, side_mat=None, cornice_mat=None):
    fac = M[facname]; sidem = side_mat or M['brick_b']; w = x1 - x0
    mb.box((x0, y0, zb - 1.0), (x1, y0 + depth, zb + h), sidem, mats=dict(front=fac, right=sidem, left=sidem), tile=(6, 6))
    cm = cornice_mat or M['cream']
    sbox(mb, (x0 - 0.3, y0 - 0.9, zb + h - 0.9), (x1 + 0.3, y0 + 0.3, zb + h), cm, 0.3); sbox(mb, (x0 - 0.5, y0 - 1.5, zb + h), (x1 + 0.5, y0 + 0.4, zb + h + 0.5), cm, 0.3)
    for k in range(int(w / 1.5)):
        xk = x0 + 0.4 + k * 1.5; sbox(mb, (xk, y0 - 1.0, zb + h - 0.9), (xk + 0.45, y0 - 0.2, zb + h - 0.3), cm, 0.3)
    sbox(mb, (x0, y0 + depth - 0.4, zb + h), (x1, y0 + depth, zb + h + 1.3), sidem, 1 / 6)

def _neighbours(SET, M, hotel=True):
    mb = MB(); am = MB()
    spec = [('L1', -52.0, -28.0, 21.0, 'fac_c', 1.3), ('L2', -72.0, -52.0, 14.0, 'fac_b', 0.0), ('L3', -90.0, -72.0, 12.5, 'fac_f', 0.0), ('L4', -110.0, -90.0, 17.0, 'fac_a', 0.0),
            ('R1', 20.0, 46.0, 17.0, 'fac_a', 0.5), ('R2', 46.0, 64.0, 15.0, 'fac_d', 0.5), ('R3', 64.0, 86.0, 18.0, 'fac_e', 0.5), ('R4', 86.0, 102.0, 12.5, 'fac_f', 0.5)]
    for (nm, x0, x1, h, fac, zb) in spec:
        side = M['clap_ochre'] if fac == 'fac_b' else (M['clap_teal'] if fac == 'fac_d' else (M['clap_green'] if fac == 'fac_f' else M['brick_b']))
        _shop(mb, M, x0, x1, h, fac, zb=zb, side_mat=side)
        nb = max(1, int((x1 - x0) // 8)); aw = [M['awn_rc'], M['awn_tc'], M['awn_oc']]
        for k in range(nb):
            cx = x0 + (k + 0.5) * (x1 - x0) / nb; _awning(am, cx, 0.0, zb + 4.3, (x1 - x0) / nb * 0.8, 2.0, 1.3, aw[(k + int(abs(x0))) % 3], M)
    for xx in np.arange(-51.0, -29.0, 3.4): sbox(mb, (xx, -0.2, -0.3), (xx + 1.1, 0.9, 0.0), M['timber_d'], 0.3)       # L1 already raised: timber blocks under it
    _obj(mb, 'shops', SET); _obj(am, 'shop_awnings', SET)
    cb = MB()
    for (xx, zz) in ((-58, 0.0), (-66, 0.0), (-80, 0.0), (26, 0.5), (36, 0.5), (50, 0.5), (70, 0.5), (92, 0.5), (-42, 1.3), (-34, 1.3)):
        _crate_stack(cb, (xx, -6.2, zz), M, int(xx) + 11, 3 + int(abs(xx)) % 3); _barrel(cb, (xx + 4.5, -5.2, zz), M, 'wood'); _barrel(cb, (xx + 5.8, -5.6, zz), M, 'wood_d')
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

def _sack(mb, c, M, seed=1, s=1.0):
    c = Vector(c); r = _rnd(seed); ell(mb, c + Vector((0, 0, 0.55 * s)), 0.5 * s, 0.38 * s, 0.6 * s, M['sack'], seg=8, rings=5, yaw=r.uniform(0, 3)); mb.frustum(c + Vector((0, 0, 1.05 * s)), c + Vector((0, 0, 1.25 * s)), 0.17 * s, 0.1 * s, M['sack'], seg=6)

def _gas_lamp(mb, fl, c, M, k):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, 5.2)), 0.16, M['iron_d'], seg=6, r1=0.09); mb.frustum(c, c + Vector((0, 0, 0.9)), 0.34, 0.2, M['iron_d'], seg=8)
    rod(mb, c + Vector((0, 0, 3.2)), c + Vector((0.0, 0, 3.4)), 0.3, M['iron_d'], seg=6)
    fl.frustum(c + Vector((0, 0, 5.2)), c + Vector((0, 0, 6.0)), 0.26, 0.36, M['lamp_glass'], seg=6); mb.frustum(c + Vector((0, 0, 6.0)), c + Vector((0, 0, 6.5)), 0.5, 0.06, M['iron_d'], seg=6)
    f = c + Vector((0, 0, 5.6)); _halo(fl, f, 1.2, M)
    if STATE['P'].get('lamps', 0) >= 0.9: D._flame_light('gas_%d_%d' % (int(c.x), int(c.y)), tuple(f), LAMP, 260, radius=0.15)

def _pole(mb, x, y, M, h=15.0):
    rod(mb, (x, y, -0.2), (x, y, h), 0.32, M['wood_d'], seg=7, r1=0.2)
    sbox(mb, (x - 2.4, y - 0.18, h - 1.2), (x + 2.4, y + 0.18, h - 0.9), M['timber_d'], 0.3); sbox(mb, (x - 2.0, y - 0.18, h - 3.0), (x + 2.0, y + 0.18, h - 2.7), M['timber_d'], 0.3)
    for xo in (-2.2, -0.9, 0.9, 2.2):
        for hh in (h - 0.9, h - 2.7): rod(mb, (x + xo, y, hh), (x + xo, y, hh + 0.45), 0.09, M['teal'], seg=5)

def _wheel(mb, c, r, M, yaw=0.0):
    c = Vector(c); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); n = 16
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; p0 = c + ey * math.cos(a0) * r + Z * math.sin(a0) * r; p1 = c + ey * math.cos(a1) * r + Z * math.sin(a1) * r
        beam(mb, p0, p1, 0.26, 0.45, M['wood'], up=tuple(ex)); beam(mb, p0, p1, 0.06, 0.5, M['iron_d'], up=tuple(ex))
    for i in range(12):
        a = 2 * math.pi * i / 12; rod(mb, c, c + ey * math.cos(a) * r + Z * math.sin(a) * r, 0.07, M['wood_l'], seg=4)
    rod(mb, c - ex * 0.35, c + ex * 0.35, 0.22, M['wood_d'], seg=8)

def _horse(mb, base, yaw, M, mat='horse', seed=1):
    """draught horse, smoother: overlapping ellipsoids (10 x 7 faces) for chest, barrel, rump, neck, head; jointed legs; mane, tail, collar and straps. +x forward."""
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    R = Matrix((ex, ey, Z)).transposed(); P = lambda x, y, z: b + ex * x + ey * y + Z * z
    mt = M[mat]; md = M['horse_d'] if mat != 'horse_d' else M['wood_d']; Ry = lambda a: R @ Matrix.Rotation(a, 3, 'Y')
    ell(mb, P(0.0, 0, 3.35), 1.75, 0.86, 0.96, mt, seg=14, rings=9, rot=R); ell(mb, P(1.05, 0, 3.4), 0.95, 0.8, 0.98, mt, seg=12, rings=8, rot=R); ell(mb, P(-1.15, 0, 3.5), 1.0, 0.82, 0.94, mt, seg=12, rings=8, rot=R)
    ell(mb, P(1.95, 0, 4.2), 1.05, 0.4, 0.46, mt, seg=12, rings=7, rot=Ry(-0.8)); ell(mb, P(2.5, 0, 4.85), 0.55, 0.36, 0.5, mt, seg=10, rings=6, rot=Ry(-0.6))
    ell(mb, P(3.05, 0, 5.3), 0.72, 0.3, 0.3, mt, seg=12, rings=7, rot=Ry(0.7)); ell(mb, P(3.55, 0, 4.98), 0.32, 0.23, 0.22, md, seg=8, rings=5, rot=Ry(0.7))
    for sg in (-1, 1):
        mb.frustum(P(2.75, sg * 0.2, 5.5), P(2.68, sg * 0.24, 6.0), 0.1, 0.02, md, seg=4); ell(mb, P(3.1, sg * 0.22, 5.42), 0.06, 0.04, 0.05, M['dark'], seg=5, rings=3)
    for k in range(6): ell(mb, P(1.5 + 0.22 * k, 0, 4.0 + 0.2 * k + (0.2 if k > 3 else 0)), 0.2, 0.1, 0.22, md, seg=6, rings=4, rot=Ry(-0.8))
    for (lx, ly, hind) in ((1.45, 0.45, 0), (1.45, -0.45, 0), (-1.45, 0.45, 1), (-1.45, -0.45, 1)):
        top = P(lx, ly, 3.05); knee = P(lx + (0.15 if not hind else -0.25), ly, 1.7); fet = P(lx + (0.05 if not hind else 0.1), ly, 0.5)
        mb.frustum(top, knee, 0.34, 0.2, mt, seg=8); ell(mb, knee, 0.2, 0.19, 0.2, mt, seg=6, rings=4); mb.frustum(knee, fet, 0.17, 0.15, mt, seg=8)
        mb.frustum(fet, fet - Z * 0.5, 0.2, 0.25, md, seg=8)
    mb.frustum(P(-2.0, 0, 4.1), P(-2.5, 0, 2.2), 0.22, 0.06, md, seg=6)
    ring = P(1.6, 0, 3.55); mb.frustum(ring - ex * 0.1, ring + ex * 0.1, 1.0, 1.0, M['wood_d'], seg=12, cap0=False, cap1=False)            # collar
    mb.frustum(P(0.0, 0, 3.35) - Z * 0.0, P(0.1, 0, 3.35), 0.99, 0.99, M['wood_d'], seg=12, cap0=False, cap1=False) if False else None
    for sg in (-1, 1): beam(mb, P(1.5, sg * 0.9, 3.5), P(-0.9, sg * 0.88, 3.0), 0.09, 0.05, M['wood_d'])                                   # traces

def _cart(mb, wm, base, yaw, M, sink=0.6, load='barrels', horse=True, seed=3, hmat='horse'):
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    P = lambda x, y, z: b + ex * x + ey * y + Z * z; zb = 2.4 - sink
    obox(mb, P(0, 0, zb), ex, ey, Z, 3.6, 1.7, 0.18, M['wood'], 0.3)
    for sg in (-1, 1): obox(mb, P(0, sg * 1.7, zb + 0.55), ex, ey, Z, 3.6, 0.1, 0.5, M['wood_l'], 0.3)
    obox(mb, P(-3.6, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3); obox(mb, P(3.5, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3)
    for sx in (-2.3, 2.3):
        for sg in (-1, 1): _wheel(wm, P(sx, sg * 2.0, 1.5 - sink), 1.9, M, yaw=yaw)
        rod(mb, P(sx, -2.0, 1.5 - sink), P(sx, 2.0, 1.5 - sink), 0.16, M['iron_d'], seg=6)
    if load == 'barrels':
        for (lx, ly, lz) in ((-2.4, -0.7, 0), (-1.0, -0.7, 0), (0.4, -0.7, 0), (1.8, -0.7, 0), (-2.4, 0.8, 0), (-1.0, 0.8, 0), (0.4, 0.8, 0), (1.8, 0.8, 0), (-1.7, 0.0, 1.4), (0.1, 0.0, 1.4), (1.2, 0.1, 1.4)):
            _barrel(mb, P(lx, ly, zb + 0.18 + lz), M, 'wood' if (lx + ly) % 2 < 1 else 'wood_l', r=0.62, h=1.5)
    else:
        for (lx, ly, lz, s) in ((-2.2, -0.6, 0, 1.5), (-0.4, 0.5, 0, 1.6), (1.4, -0.5, 0, 1.4), (-1.2, 0.0, 1.5, 1.3), (0.6, -0.2, 1.6, 1.2)): obox(mb, P(lx, ly, zb + 0.18 + lz + s / 2), ex, ey, Z, s / 2, s / 2, s / 2, M['crate'], 0.3)
    for sg in (-1, 1): beam(mb, P(3.5, sg * 0.9, zb - 0.1), P(8.2, sg * 0.9, zb + 0.9), 0.16, 0.22, M['wood_d'])
    if horse: _horse(mb, P(8.2, 0, 0.0), yaw, M, hmat, seed=seed)

def _mound(SET, M, name, cx, cy, rx, ry, h, seed, mat, mud_z):
    xs = np.linspace(cx - rx, cx + rx, 30); ys = np.linspace(cy - ry, cy + ry, 30); X, Y = np.meshgrid(xs, ys)
    d = np.sqrt(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2); n = 0.07 * np.sin(2.3 * X + seed) * np.cos(1.9 * Y) + 0.05 * np.sin(5.0 * X - 3.1 * Y + seed)
    Z = h * np.clip(1 - d ** 1.7, 0, 1) ** 0.9 * (1 + n) - 0.35 + n * 0.3
    ob = grid_mesh(name, xs, ys, Z, mat, uvs=(0.2, 0.2)); STATE['fill_objs'].append(ob); return ob

def _wheelbarrow(mb, x, y, z, yaw, M):
    ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); P = lambda a, b, c: Vector((x, y, z)) + ex * a + ey * b + Z * c
    obox(mb, P(0.0, 0, 1.0), ex, ey, Z, 0.9, 0.55, 0.28, M['wood'], 0.3)
    for sg in (-1, 1): beam(mb, P(0.8, sg * 0.45, 0.9), P(2.4, sg * 0.4, 0.9), 0.1, 0.12, M['wood_d']); beam(mb, P(-0.8, sg * 0.45, 0.9), P(-0.8, sg * 0.5, 0.0), 0.08, 0.1, M['wood_d'])
    rod(mb, P(1.5, -0.55, 0.55), P(1.5, 0.55, 0.55), 0.4, M['wood_d'], seg=10, r1=0.4)

def _ladder(mb, p0, p1, M, w=0.7):
    p0, p1 = Vector(p0), Vector(p1); d = (p1 - p0); side = Vector((0, 1, 0)) if abs(d.y) < abs(d.x) else Vector((1, 0, 0))
    for sg in (-1, 1): beam(mb, p0 + side * sg * w / 2, p1 + side * sg * w / 2, 0.1, 0.14, M['wood_d'])
    for k in range(1, 9): a = p0.lerp(p1, k / 9); beam(mb, a - side * w / 2, a + side * w / 2, 0.08, 0.1, M['wood_l'])

def _street_dress(SET, M, mud_z, hotel=True):
    mb = MB(); fl = MB(); zq = lambda x, y: float(mud_z(np.array([x]), np.array([y]))[0])
    for k, xx in enumerate((-96, -66, -40, 28, 56, 84)): _gas_lamp(mb, fl, (xx, -8.2 if xx < 0 else -7.7, 1.3 if xx < 0 else 0.5), M, k)
    for xx in (-9.0, 9.0): _gas_lamp(mb, fl, (xx + (-7.0 if xx < 0 else 7.0), -9.6, 0.0), M, 9)
    poles = [(x, -13.0) for x in (-112, -74, -36, 2, 40, 78, 116)]
    for (x, y) in poles: _pole(mb, x, y, M)
    for (a, b) in zip(poles, poles[1:]):
        for dx, dz in ((-2.2, 14.1), (-0.9, 14.1), (0.9, 14.1), (2.2, 14.1), (-2.0, 12.3), (2.0, 12.3)):
            chain_rod(mb, catenary((a[0] + dx, a[1], dz), (b[0] + dx, b[1], dz), 0.9, 8), 0.05, M['iron_d'], seg=3)
    for xx in (-60, -30, 30, 60): rod(mb, (xx, -9.4, 0.0), (xx, -9.4, 2.4), 0.16, M['wood_d'], seg=5); sbox(mb, (xx - 0.7, -9.5, 2.0), (xx + 0.7, -9.3, 2.2), M['wood_d'], 0.3)
    _obj(mb, 'street_furniture', SET); _obj(fl, 'lamps_glass', SET, shadow=False)
    cm = MB(); wm = MB()
    _cart(cm, wm, (-24.0, -35.0, 0.0), math.radians(8), M, sink=0.6, load='barrels', seed=3)                          # the stuck cart (mud_low, street_wide)
    _cart(cm, wm, (17.0, -26.0, 0.0), math.radians(190), M, sink=0.45, load='crates', seed=4, hmat='horse_g')
    _cart(cm, wm, (-46.0, -42.0, 0.0), math.radians(60), M, sink=0.4, load='crates', seed=5, hmat='horse_d')
    _obj(cm, 'carts', SET); _obj(wm, 'cart_wheels', SET); STATE['fill_objs'] += [bpy.data.objects['carts'], bpy.data.objects['cart_wheels']]
    _mound(SET, M, 'pile_a', -34.0, -17.0, 8.0, 4.4, 3.2, 4, M['clay'], mud_z); _mound(SET, M, 'pile_b', 40.0, -14.0, 7.0, 3.8, 2.6, 5, M['clay'], mud_z)
    _mound(SET, M, 'pile_c', 12.0, -38.0, 5.0, 3.2, 1.9, 6, M['gravel'], mud_z); _mound(SET, M, 'pile_e', -8.0, -46.0, 5.0, 3.0, 2.2, 8, M['clay'], mud_z)
    _mound(SET, M, 'pile_d', -50.0, -22.0, 6.0, 3.4, 2.2, 7, M['clay'], mud_z)
    pm = MB()
    for k in range(5): sbox(pm, (-12.0, -15.4 + k * 0.45, 0.0), (-4.0, -15.0 + k * 0.45, 0.35), M['walk'], 0.3)
    for k in range(5): sbox(pm, (24.0, -17.4 + k * 0.45, 0.1), (31.0, -17.0 + k * 0.45, 0.45), M['walk'], 0.3)
    for lvl in range(4):
        for j in range(5 - lvl): sbox(pm, (-62.0 + lvl * 0.5, -22.0 + j * 0.6 + lvl * 0.3, 0.45 * lvl - 0.1), (-54.0 - lvl * 0.5, -21.5 + j * 0.6 + lvl * 0.3, 0.45 * lvl + 0.35), M['timber_w'], 0.3)
    def walk(p0, p1, wdt=3.0):                                                                           # plank walkway across the mud with two stringers
        p0, p1 = Vector(p0), Vector(p1); dv = (p1 - p0).normalized(); pr = Vector((-dv.y, dv.x)); n_ = int((p1 - p0).length / 0.7)
        for k in range(n_):
            c2 = p0 + dv * (k * 0.7); zz = zq(c2.x, c2.y) + 0.12; beam(pm, (c2.x - pr.x * wdt / 2, c2.y - pr.y * wdt / 2, zz), (c2.x + pr.x * wdt / 2, c2.y + pr.y * wdt / 2, zz), 0.58, 0.16, M['walk'], uvk=0.3)
        for sg in (-1, 1): beam(pm, (p0.x + pr.x * (wdt / 2 - 0.2) * sg, p0.y + pr.y * (wdt / 2 - 0.2) * sg, 0.0), (p1.x + pr.x * (wdt / 2 - 0.2) * sg, p1.y + pr.y * (wdt / 2 - 0.2) * sg, 0.0), 0.2, 0.2, M['timber_d'], uvk=0.3)
    walk((-28.0, -57.0), (-12.0, -28.0)); walk((-12.0, -22.0), (0.0, -11.0), 2.6); walk((8.0, -12.0), (8.0, -45.0), 2.4)
    _obj(pm, 'street_planks', SET); STATE['fill_objs'].append(bpy.data.objects['street_planks'])
    bm = MB()
    for (xx, yy) in ((-33, -47.0), (-31.8, -47.6), (-26, -11.5), (-24.6, -11.0), (-25.4, -12.7), (16, -11.0), (17.4, -11.8), (-2, -44), (-0.6, -44.8), (-3.0, -48.0), (-1.8, -48.6), (48, -28), (49.4, -27.4), (-56, -30), (-57.2, -29.4), (-5.0, -20.0),
                     (-22.0, -40.0), (-20.6, -40.8), (-21.6, -41.9), (-13.0, -44.0), (-11.8, -44.5), (-30.0, -45.0), (4.0, -43.0), (5.3, -43.6), (-34.0, -29.0), (36.0, -30.0), (14.0, -18.0)):
        _barrel(bm, (xx, yy, zq(xx, yy) - 0.15), M, 'wood' if int(xx) % 2 else 'wood_l')
    for (xx, yy, s_) in ((-17.0, -45.0, 21), (6.0, -44.0, 22), (-5.0, -42.0, 12), (22.0, -11.0, 8), (-31.0, -12.0, 9), (52.0, -36.0, 10), (-40.0, -41.0, 13), (28.0, -43.0, 14)): _crate_stack(bm, (xx, yy, zq(xx, yy) - 0.1), M, s_, 5)
    for k, (xx, yy) in enumerate(((-31.0, -43.0), (-30.0, -43.7), (-31.2, -44.4), (-18.0, -22.0), (-16.5, -22.6), (-17.4, -21.0), (-3.0, -26.0), (-1.8, -26.6), (22.0, -30.0), (-44.0, -27.0), (30.0, -18.5))): _sack(bm, (xx, yy, zq(xx, yy) - 0.1), M, k, 1.1)
    for (xx, yy) in ((-28.0, -19.5), (36.0, -17.0), (2.0, -31.0), (-20.0, -49.0), (-6.0, -40.0)): _wheelbarrow(bm, xx, yy, zq(xx, yy) - 0.1, 0.7 * xx, M)
    _ladder(bm, (-33.0, -4.0, 0.5), (-33.5, -8.5, 6.0), M); _ladder(bm, (9.0, -12.0, 0.0), (11.0, -14.0, 5.5), M) if False else None
    for xx in (-44.0, -30.0, 28.0, 44.0):                                                                  # stakes with a rope round the fill piles
        for k in range(4): rod(bm, (xx + k * 2.2, -23.0, zq(xx + k * 2.2, -23.0) - 0.2), (xx + k * 2.2, -23.0, zq(xx + k * 2.2, -23.0) + 1.4), 0.1, M['wood_d'], seg=5)
    for k in range(5): bm_h = _rnd(k); _bale = (-16.0 + 2.2 * k, -20.5 + 0.3 * (k % 2)); sbox(bm, (_bale[0] - 0.9, _bale[1] - 0.5, zq(*_bale) - 0.1), (_bale[0] + 0.9, _bale[1] + 0.5, zq(*_bale) + 0.8), M['hay'], 0.4) if k < 3 else None
    _obj(bm, 'street_props', SET); STATE['fill_objs'].append(bpy.data.objects['street_props'])
    STATE['marks'].update(
        door=(0.0, -0.9, GF, 1), stair_top=(0.0, -3.0, GF - 0.1, 0), stair_mid=(0.0, -6.5, GF * 0.5, 0), stair_foot=(0.0, -9.6, 0.0, 0), mud_fall=(2.0, -6.4, 0.0, 0), door_b=(-3.5, -0.9, GF, 1),
        walk_a=(-14.0, -41.0, 0.0, 0), walk_b=(-8.0, -35.0, 0.0, 0), walk_c=(8.0, -20.0, 0.0, 0), cart_a=(-21.0, -29.5, 0.0, 0), cart_b=(-27.5, -31.5, 0.0, 0), cart_c=(-14.5, -31.0, 0.0, 0),
        front_a=(-9.0, -13.0, 0.0, 0), front_b=(9.0, -13.5, 0.0, 0), front_c=(-1.5, -17.0, 0.0, 0), pile_a=(-30.0, -20.5, 0.0, 0), pile_b=(5.0, -40.0, 0.0, 0), sidewalk_r=(24.0, -5.6, 0.5, 0), sidewalk_l=(-36.0, -5.6, 1.3, 0))

def _church(SET, M):
    mb = MB(); x, y = 105.0, 210.0
    sbox(mb, (x - 7, y - 7, -0.5), (x + 7, y + 7, 34.0), M['stone_grey'], 0.15)
    for sx in (-1, 1): sbox(mb, (x + sx * 2.8 - 1.0, y - 7.1, 24.0), (x + sx * 2.8 + 1.0, y - 6.8, 31.0), M['dark'], 0.3)
    sbox(mb, (x - 7.6, y - 7.6, 33.5), (x + 7.6, y + 7.6, 34.6), M['cream'], 0.3)
    mb.frustum((x, y, 34.6), (x, y, 66.0), 5.8, 0.25, M['slate'], seg=8); rod(mb, (x, y, 66.0), (x, y, 72.0), 0.12, M['brass'], seg=4); sbox(mb, (x - 1.0, y - 0.06, 69.5), (x + 1.0, y + 0.06, 70.2), M['brass'], 0.3)
    sbox(mb, (x - 17, y - 7, -0.5), (x - 7, y + 20, 20.0), M['brick_d'], 0.15); prism_roof(mb, x - 17.2, x - 6.8, y - 7.3, y + 20.3, 20.0, 7.0, M['slate'])
    _obj(mb, 'church', SET)

def _opposite(SET, M):
    """the row of shops across the street (y -68..-52, facing +y), seen from the suite window."""
    mb = MB()
    spec = [(-70, -46, 24.0, 'fac_a'), (-46, -26, 20.0, 'fac_b'), (-26, -2, 28.0, 'fac_c'), (-2, 18, 22.0, 'fac_d'), (18, 44, 25.0, 'fac_e'), (44, 66, 19.0, 'fac_f'), (66, 90, 26.0, 'fac_a')]
    for (x0, x1, h, fac) in spec:
        mb.box((x0, -68.0, -1.0), (x1, -52.0, h), M['brick_b'], mats=dict(back=M[fac]), tile=(6, 6))
        sbox(mb, (x0 - 0.3, -52.3, h - 0.9), (x1 + 0.3, -50.9, h), M['cream'], 0.3); sbox(mb, (x0, -68.0, h), (x1, -51.8, h + 0.5), M['cream'], 0.3); sbox(mb, (x0 + 3.0, -64.0, h + 0.5), (x0 + 4.6, -62.4, h + 4.0), M['brick_d'], 1 / 6)
    sb = MB(); sbox(sb, (-110, -52.0, 0.0), (110, -47.0, 0.45), M['walk'], 0.2); _obj(sb, 'opp_walk', SET); _obj(mb, 'opp_shops', SET)

# ============================================================================= cellar (crawlspace under the hotel)
CX0, CX1, CY0, CY1 = -9.0, 19.0, -4.0, 68.0
CZ_B = 3.5      # underside of the cross beams = top of the jack pads (at lift 0)
UX = [-6.0 + 2.6 * k for k in range(10)]; UY = [6.0 + 2.7 * k for k in range(23)]       # jack grid: 230 jacks
VENTS = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
def _under(SET, P, M):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M); r = _rnd(11)
    xs_g = np.unique(np.round(np.concatenate([np.arange(-70, -12, 4.0), np.arange(-12, 24, 0.6), np.arange(24, 71, 4.0)]), 3)); ys_g = np.unique(np.round(np.concatenate([np.arange(-30, -8, 4.0), np.arange(-8, 72, 0.6), np.arange(72, 101, 4.0)]), 3))
    X, Y = np.meshgrid(xs_g, ys_g); Z = 0.12 * np.sin(0.7 * X + 0.3 * Y) * np.cos(0.5 * Y) + 0.07 * np.sin(2.1 * X + 1.0 * Y) + 0.05 * np.sin(4.3 * X - 2.0 * Y)
    inside = (X > CX0) & (X < CX1) & (Y > CY0 + 1) & (Y < CY1)
    for (cx, cy, rr, h) in ((-6.0, 12.0, 1.8, 0.5), (14.0, 26.0, 2.0, 0.45), (2.0, 45.0, 2.5, 0.55), (15.5, 55.0, 1.6, 0.4)): Z = Z + h * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / rr ** 2)    # earth lumps
    grid_mesh('floor', xs_g, ys_g, Z, M['dirt'], uvs=(0.1, 0.1))
    fb = MB()                                                                                       # a worn plank walkway down the middle aisle
    for k in range(3): sbox(fb, (0.6 + k * 1.2, CY0, 0.02), (1.6 + k * 1.2, CY1 - 3, 0.1), M['plank_f'], 0.2)
    for yy in np.arange(0.0, CY1 - 3, 4.1): sbox(fb, (0.4, yy, 0.02), (4.4, yy + 0.3, 0.18), M['timber_d'], 0.3)
    _obj(fb, 'walkway', SET)
    wb = MB(); zt = CZ_B + 2.6
    sbox(wb, (CX0 - 1.0, CY0, -0.6), (CX0, CY1 + 1.0, zt), M['brick_d'], 1 / 6); sbox(wb, (CX0, CY1, -0.6), (CX1 + 1.2, CY1 + 1.0, zt), M['brick_d'], 1 / 6)
    ys_v = [CY0] + [v for yv in VENTS for v in (yv - 0.9, yv + 0.9)] + [CY1]                              # right wall with 6 ventilation slots (z 0.9..4.0)
    for i in range(0, len(ys_v), 2):
        sbox(wb, (CX1, ys_v[i], -0.6), (CX1 + 1.2, ys_v[i + 1], zt), M['brick_d'], 1 / 6)
    for yv in VENTS: sbox(wb, (CX1, yv - 0.9, -0.6), (CX1 + 1.2, yv + 0.9, 0.7), M['brick_d'], 1 / 6); sbox(wb, (CX1, yv - 0.9, 3.0), (CX1 + 1.2, yv + 0.9, zt), M['brick_d'], 1 / 6)
    for yy in np.arange(CY0 + 2.0, CY1, 8.0): sbox(wb, (CX0, yy, 0.0), (CX0 + 0.3, yy + 0.5, 4.8), M['timber_d'], 0.3)           # pilasters on the left wall
    _obj(wb, 'cellar_walls', SET)
    pb = MB()                                                                                       # front: timber posts + cribs at the open front (y -4)
    for xx in (CX0 + 0.5, 1.0, 6.5, 12.0, CX1 - 0.5): sbox(pb, (xx - 0.5, CY0 - 0.5, -0.1), (xx + 0.5, CY0 + 0.5, CZ_B + 0.2), M['timber_d'], 0.3)
    _obj(pb, 'front_posts', SET)
    bm = MB(); kd = Vector(P['key_dir'])
    for y in UY:
        sbox(bm, (CX0, y - 0.5, 0.0), (CX1 + 1.0, y + 0.5, 1.2), M['timber_w'], 0.25)                      # heavy cross beams (rel z 0 = underside)
        sbox(bm, (CX0, y - 0.58, 0.8), (CX0 + 0.8, y + 0.58, 1.4), M['iron_k'], 0.3)
    for xj in np.arange(CX0, CX1 + 1.5, 2.0): sbox(bm, (xj - 0.28, CY0, 1.2), (xj + 0.28, CY1, 2.1), M['timber'], 0.25)
    sbox(bm, (CX0, CY0, 2.1), (CX1 + 1.0, CY1, 2.3), M['plank_d'], 0.2)
    bo = _obj(bm, 'floor_beams', SET); STATE['movers'].append((bo, CZ_B)); STATE['cut_objs'].append(bo)
    so, mo, nj = _jackfield(SET, M, UX, UY, 'jf', 0.0, 1, 3.3, CZ_B, hd=1.0); STATE['njacks'] = nj
    pr = MB()
    for (xx, yy) in ((-7.0, 3.0), (-7.5, 20.0), (17.0, 14.0), (16.0, 36.0), (-7.0, 52.0), (16.5, 62.0)): _crate_stack(pr, (xx, yy, 0.0), M, int(yy), 4)
    for (xx, yy) in ((-7.0, 8.0), (3.0, 4.5), (15.5, 25.0), (-7.2, 33.0), (17.0, 46.0), (-7.0, 60.0)): _barrel(pr, (xx, yy, 0.0), M, 'wood')
    for (xx, yy) in ((-7.4, 14.0), (17.5, 30.0), (3.0, 3.0)): rod(pr, (xx, yy, 0.0), (xx, yy, 0.8), 0.4, M['iron'], seg=8, r1=0.5)
    for yy in (9.4, 20.2, 31.0, 42.0):                                                                 # long turning bars leaning on the beams
        rod(pr, (3.2, yy, 0.0), (4.0, yy + 0.3, 3.3), 0.08, M['iron_bar'], seg=4)
    for k, (xx, yy) in enumerate(((2.2, 6.0), (3.0, 16.0), (4.5, 27.0), (2.6, 38.0))): _sack(pr, (xx, yy, 0.0), M, k, 1.0)
    _obj(pr, 'cellar_props', SET)
    lamps = [(1.5, 9.0, 2.6), (9.0, 17.0, 2.6), (3.0, 26.0, 2.6), (10.0, 34.0, 2.6), (2.0, 44.0, 2.6), (9.0, 54.0, 2.6), (4.0, 63.0, 2.6)]
    fl = MB()
    for k, (xl, yl, zl) in enumerate(lamps):
        c = Vector((xl, yl, zl)); rod(fl, c + Vector((0, 0, 0.5)), c + Vector((0, 0, CZ_B + 0.0 - zl)), 0.03, M['iron_d'], seg=4)
        fl.frustum(c - Vector((0, 0, 0.5)), c + Vector((0, 0, 0.5)), 0.26, 0.34, M['lamp_glass'], seg=7); fl.frustum(c + Vector((0, 0, 0.5)), c + Vector((0, 0, 0.8)), 0.38, 0.05, M['iron_d'], seg=7)
        _halo(fl, c, 2.4, M); D._flame_light('oil_%d' % k, tuple(c), LAMP, 650 if k < 5 else 420, radius=0.15, shadow=(k % 2 == 0))
        pool = MB(); pool.face([Vector((xl - 5.5, yl - 5.5, 0.12)), Vector((xl + 5.5, yl - 5.5, 0.12)), Vector((xl + 5.5, yl + 5.5, 0.12)), Vector((xl - 5.5, yl + 5.5, 0.12))], M['pool'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        _obj(pool, 'pool_%d' % k, SET, shadow=False)
    _obj(fl, 'cellar_lamps', SET, shadow=False)
    sh = MB(); kn = kd.normalized()                                                                 # dusty shafts of light through the vents (additive cards along the key direction)
    for yv in VENTS:
        for sg in (-1, 1):
            a = Vector((CX1, yv + sg * 0.9, 3.0)); b = Vector((CX1, yv + sg * 0.9, 0.7)); ta = a.z / max(0.05, -kn.z); tb = b.z / max(0.05, -kn.z)
            sh.face([a, b, b + kn * tb, a + kn * ta], M['shaft'], [(0, 1), (0, 0), (1, 0), (1, 1)])
    _obj(sh, 'shafts', SET, shadow=False)
    # stand points: aisles between the jack columns (x = column + 1.3), between beam rows
    for k in range(4):
        for j, yy in enumerate((9.35, 17.45, 28.25, 41.75)): STATE['marks']['aisle_%d_%d' % (k, j)] = (UX[2 * k + 1] + 1.3 if 2 * k + 1 < len(UX) else UX[-1] + 1.3, yy, 0.0, 0)
    STATE['marks'].update(foreman=(0.0, 7.4, 0.0, 0), worker_a=(3.6, 12.0, 0.0, 0), worker_b=(9.4, 19.0, 0.0, 0), worker_c=(1.0, 24.4, 0.0, 0), worker_d=(6.2, 30.0, 0.0, 0), jack_hands=(8.6, 12.4, 0.0, 0))

# ============================================================================= suite (rich guest's top-floor room, window looks down on the muddy street)
RX0, RX1, RY1 = -11.0, 11.0, 18.0
ZF = 30.0; RH = 6.2
TEA = dict(x=-1.4, y=2.5, top=ZF + 1.5)
def _cup(mb, tea_mb, cx, cy, z0, s):
    """a proper teacup on a saucer (lathe profiles, 20 segments): saucer dish, foot, bowl with an inner wall, rim, a looped handle; the tea disc is a separate flat mesh just under the rim."""
    seg = 20
    prof = [(0.0, 0.0), (0.2, 0.0), (0.36, 0.035), (0.58, 0.13), (0.62, 0.15)]                              # saucer outer (r, z) * s
    def lathe(pts, mat, flip=False):
        for (r0, h0), (r1, h1) in zip(pts, pts[1:]):
            for i in range(seg):
                a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
                q = [Vector((cx + r0 * s * math.cos(a0), cy + r0 * s * math.sin(a0), z0 + h0 * s)), Vector((cx + r0 * s * math.cos(a1), cy + r0 * s * math.sin(a1), z0 + h0 * s)),
                     Vector((cx + r1 * s * math.cos(a1), cy + r1 * s * math.sin(a1), z0 + h1 * s)), Vector((cx + r1 * s * math.cos(a0), cy + r1 * s * math.sin(a0), z0 + h1 * s))]
                mb.face(q[::-1] if flip else q, mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.pid += 1
    lathe(prof, STATE['M']['white']); lathe([(0.62, 0.15), (0.6, 0.165), (0.5, 0.11), (0.3, 0.07), (0.0, 0.07)], STATE['M']['white'])    # saucer rim and dish
    cp = [(0.2, 0.07), (0.22, 0.12), (0.3, 0.26), (0.4, 0.5), (0.45, 0.62)]                                    # cup outer wall
    lathe(cp, STATE['M']['white']); lathe([(0.45, 0.62), (0.44, 0.63), (0.39, 0.5)], STATE['M']['white']); lathe([(0.39, 0.5), (0.3, 0.26), (0.23, 0.15), (0.0, 0.13)], STATE['M']['wood_l'])     # rim + inner glaze
    for k in range(7):                                                                                       # handle: a loop of small segments on the +x side
        t0, t1 = math.pi * 0.15 + k * math.pi * 0.7 / 7, math.pi * 0.15 + (k + 1) * math.pi * 0.7 / 7
        p0 = Vector((cx + (0.45 + 0.2 * math.sin(t0)) * s, cy, z0 + (0.4 + 0.2 * math.cos(t0) * 1.0) * s)); p1 = Vector((cx + (0.45 + 0.2 * math.sin(t1)) * s, cy, z0 + (0.4 + 0.2 * math.cos(t1)) * s))
        mb.frustum(p0, p1, 0.035 * s, 0.035 * s, STATE['M']['white'], seg=6, cap0=False, cap1=False)
    tea_mb.pid += 1; zt = z0 + 0.5 * s; R_ = 0.4 * s                                                          # flat tea surface (fan of 28 triangles)
    pts = [Vector((cx + R_ * math.cos(2 * math.pi * j / 28), cy + R_ * math.sin(2 * math.pi * j / 28), zt)) for j in range(28)]
    for j in range(28): tea_mb.face([Vector((cx, cy, zt)), pts[j], pts[(j + 1) % 28]], STATE['M']['tea'], [(0.5, 0.5), (0.5 + 0.5 * math.cos(2 * math.pi * j / 28), 0.5 + 0.5 * math.sin(2 * math.pi * j / 28)), (0.5, 0.5)])

def _suite(SET, P, M):
    mud_z = _street(SET, P, M, hotel=False, opp=True)
    mb = MB(); WX0, WX1, WZ0, WZ1 = -5.0, 5.0, ZF + 0.08, ZF + 5.6; t = 0.8; wp = M['wallpaper']
    fm = MB(); sbox(fm, (RX0, 0, ZF - 0.6), (RX1, RY1, ZF), M['parquet'], 1 / 8); _obj(fm, 'floor_room', SET)
    rg = MB(); rg.face([Vector((-8.0, 1.0, ZF + 0.03)), Vector((6.0, 1.0, ZF + 0.03)), Vector((6.0, 11.0, ZF + 0.03)), Vector((-8.0, 11.0, ZF + 0.03))], M['rug'], [(0, 0), (1, 0), (1, 1), (0, 1)]); _obj(rg, 'rug', SET)
    sbox(mb, (RX0 - t, -t, ZF + RH), (RX1 + t, RY1 + t, ZF + RH + 0.6), M['cream'], 0.2)                                      # ceiling slab
    sbox(mb, (RX0 - t, 0, ZF - 0.6), (RX0, RY1 + t, ZF + RH + 0.6), wp, 0.25); sbox(mb, (RX1, 0, ZF - 0.6), (RX1 + t, RY1 + t, ZF + RH + 0.6), wp, 0.25); sbox(mb, (RX0, RY1, ZF - 0.6), (RX1, RY1 + t, ZF + RH + 0.6), wp, 0.25)
    sbox(mb, (RX0 - t, -t, ZF - 0.6), (WX0, 0, ZF + RH + 0.6), M['brick'], 1 / 6); sbox(mb, (WX1, -t, ZF - 0.6), (RX1 + t, 0, ZF + RH + 0.6), M['brick'], 1 / 6)
    sbox(mb, (WX0, -t, ZF + RH - 0.6), (WX1, 0, ZF + RH + 0.6), M['brick'], 1 / 6); sbox(mb, (WX0, -t, WZ1), (WX1, 0, ZF + RH - 0.6), M['brick'], 1 / 6); sbox(mb, (WX0, -t, ZF - 0.6), (WX1, 0, WZ0), M['brick'], 1 / 6)
    for (a, b, z0, z1) in ((RX0, WX0, ZF, ZF + RH), (WX1, RX1, ZF, ZF + RH), (WX0, WX1, WZ1, ZF + RH)): sbox(mb, (a, 0.0, z0), (b, 0.5, z1), wp, 0.25)
    sbox(mb, (WX0 - 0.3, -0.7, WZ0 - 0.4), (WX1 + 0.3, 0.6, WZ0), M['ash'], 0.3); sbox(mb, (WX0 - 0.3, -0.4, WZ1), (WX1 + 0.3, 0.6, WZ1 + 0.4), M['ash'], 0.3)           # threshold + head
    for xx in (WX0, WX1): sbox(mb, (xx - 0.18, -0.1, WZ0), (xx + 0.18, 0.5, WZ1), M['white'], 0.3)
    for xx in (-2.5, 0.0, 2.5): sbox(mb, (xx - 0.07, 0.1, WZ0), (xx + 0.07, 0.25, WZ1), M['white'], 0.3)
    for zz in (ZF + 4.1, WZ1 - 0.1): sbox(mb, (WX0, 0.1, zz - 0.08), (WX1, 0.25, zz + 0.08), M['white'], 0.3)
    sbox(mb, (WX0 - 0.6, -1.0, ZF - 0.4), (WX1 + 0.6, 0.0, ZF + 0.05), M['ash'], 0.3)                                              # Juliet balcony ledge + see-through iron rail
    for k in range(int((WX1 - WX0 + 1.2) / 0.55) + 1):
        xx = WX0 - 0.6 + k * 0.55; rod(mb, (xx, -0.9, ZF + 0.05), (xx, -0.9, ZF + 2.3), 0.05, M['iron_d'], seg=4)
    beam(mb, (WX0 - 0.6, -0.9, ZF + 2.3), (WX1 + 0.6, -0.9, ZF + 2.3), 0.12, 0.12, M['iron_d']); beam(mb, (WX0 - 0.6, -0.9, ZF + 0.3), (WX1 + 0.6, -0.9, ZF + 0.3), 0.08, 0.08, M['iron_d'])
    for (x0, x1, y0, y1) in ((RX0, RX0 + 0.35, 0.5, RY1), (RX1 - 0.35, RX1, 0.5, RY1)): sbox(mb, (x0, y0, ZF), (x1, y1, ZF + 2.0), M['plank_f'], 0.2); sbox(mb, (x0 - 0.1, y0, ZF + 2.0), (x1 + 0.1, y1, ZF + 2.2), M['cream'], 0.3)
    sbox(mb, (RX0, RY1 - 0.35, ZF), (RX1, RY1, ZF + 2.0), M['plank_f'], 0.2); sbox(mb, (RX0, RY1 - 0.5, ZF + 2.0), (RX1, RY1, ZF + 2.2), M['cream'], 0.3)
    sbox(mb, (RX0, 0, ZF + RH - 0.9), (RX1, 0.5, ZF + RH), M['cream'], 0.3); sbox(mb, (RX0, 0, ZF + RH - 0.6), (RX0 + 0.6, RY1, ZF + RH), M['cream'], 0.3)
    sbox(mb, (RX1 - 0.6, 0, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3); sbox(mb, (RX0, RY1 - 0.6, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3)
    cm = MB()
    for sg in (-1, 1):                                                                                                        # velvet drapes either side, tied back
        for k in range(5):
            x0 = sg * (WX1 + 0.15) + sg * k * 0.38; sbox(cm, (min(x0, x0 + sg * 0.42), 0.45, ZF + 0.3 + 0.12 * (k % 2)), (max(x0, x0 + sg * 0.42), 1.0 + 0.1 * (k % 2), ZF + 5.9), M['velvet_red'], 0.4)
        ell(cm, (sg * (WX1 + 0.5), 0.4, ZF + 2.4), 0.25, 0.3, 0.25, M['brass'], seg=6, rings=4)
    rod(cm, (WX0 - 2.2, 0.75, ZF + 6.0), (WX1 + 2.2, 0.75, ZF + 6.0), 0.1, M['brass'], seg=6); sbox(cm, (WX0 - 1.0, 0.45, ZF + 5.7), (WX1 + 1.0, 1.2, ZF + 6.15), M['velvet_red'], 0.4)
    _obj(cm, 'curtains', SET); _obj(mb, 'room', SET)
    pf = MB()
    def picture(mat, x, y, z, w, h, face):
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
    picture(M['p_portrait'], 8.0, 0.5, ZF + 3.6, 1.8, 2.4, 'y+'); picture(M['p_lake'], -8.2, 0.5, ZF + 3.6, 3.0, 2.2, 'y+')
    _obj(pf, 'paintings', SET)
    fb = MB(); tmb = MB(); _furniture(fb, tmb, M); _obj(fb, 'furniture', SET); to = _obj(tmb, 'tea', SET, shadow=False); STATE['tea_obj'] = to
    ch = MB(); fl = MB(); c = Vector((-1.2, 5.0, ZF + 4.4)); rod(ch, (c.x, c.y, ZF + RH), c + Vector((0, 0, 0.3)), 0.06, M['brass'], seg=6)
    ell(ch, c, 0.5, 0.5, 0.5, M['brass'], seg=8, rings=5); rod(ch, c + Vector((0, 0, -0.5)), c + Vector((0, 0, -1.0)), 0.04, M['brass'], seg=5); ell(ch, c + Vector((0, 0, -1.05)), 0.2, 0.2, 0.2, M['brass'], seg=6, rings=4)
    for k in range(6):
        a = 2 * math.pi * k / 6; e = c + Vector((1.5 * math.cos(a), 1.5 * math.sin(a), -0.1))
        ch.frustum(c + Vector((0, 0, -0.05)), e, 0.05, 0.05, M['brass'], seg=4); rod(ch, e, e + Vector((0, 0, 0.5)), 0.08, M['brass'], seg=6); rod(ch, e + Vector((0, 0, 0.5)), e + Vector((0, 0, 0.9)), 0.07, M['white'], seg=6)
        fl.frustum(e + Vector((0, 0, 0.9)), e + Vector((0, 0, 1.05)), 0.07, 0.01, M['glass_cand'], seg=5); _halo(fl, e + Vector((0, 0, 1.0)), 0.5, M)
        for j in range(3): rod(ch, e + Vector((0.08 * j, 0, 0.0)), e + Vector((0.08 * j, 0, -0.55 - 0.1 * j)), 0.02, M['white'], seg=3)
    D._flame_light('chandelier', tuple(c + Vector((0, 0, 0.5))), LAMP, 700, radius=0.3, shadow=True)
    _obj(ch, 'chandelier', SET); _obj(fl, 'candles', SET, shadow=False)
    STATE['marks'].update(window=(0.4, 1.4, ZF, 0), window_l=(-3.2, 1.6, ZF, 0), window_r=(3.4, 1.6, ZF, 0), tea_side=(-3.6, 3.8, ZF, 0), chair_side=(3.2, 5.8, ZF, 0), room_c=(-1.0, 8.0, ZF, 0))
    STATE['tea_xyz'] = (TEA['x'] - 0.2, TEA['y'] - 0.5, TEA['top'] + 0.03)
    # a busy street below: carts (street dress) + a crowd of workers and townsfolk standing in the mud and on the plank walks
    crowd(30, [(-34, 34, -46, -20)], seed=21, ground=lambda x, y: float(mud_z(np.array([x]), np.array([y]))[0]))
    crowd(8, [(-30, 30, -8.2, -3.5)], seed=33, ground=lambda x, y: 0.4)

def _furniture(mb, tmb, M):
    """red velvet armchair (visible), teal armchair, round tea table with cup / saucer / pot / plate, side table with vase, sideboard."""
    def chair(cx, cy, yaw, mat):
        ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); P = lambda x, y, z: Vector((cx, cy, ZF)) + ex * x + ey * y + Z * z
        obox(mb, P(0, 0, 1.0), ex, ey, Z, 1.4, 1.35, 0.45, mat, 0.4); obox(mb, P(0, 1.2, 2.5), ex, ey, Z, 1.4, 0.28, 1.45, mat, 0.4)
        for sg in (-1, 1): obox(mb, P(sg * 1.5, 0, 1.55), ex, ey, Z, 0.28, 1.35, 0.55, mat, 0.4); ell(mb, P(sg * 1.5, -1.3, 2.15), 0.34, 0.34, 0.34, mat, seg=10, rings=6)
        ell(mb, P(0, 1.2, 4.05), 1.4, 0.3, 0.2, mat, seg=12, rings=5, yaw=yaw)
        for sx in (-1, 1):
            for sy in (-1, 1): rod(mb, P(sx * 1.25, sy * 1.2, 0.0), P(sx * 1.25, sy * 1.2, 0.6), 0.16, M['wood_d'], seg=6, r1=0.1)
        obox(mb, P(0, -1.38, 1.1), ex, ey, Z, 1.42, 0.05, 0.12, M['brass'], 0.4)
        for k in range(5): ell(mb, P(-1.0 + 0.5 * k, -1.45, 1.1), 0.08, 0.08, 0.08, M['brass'], seg=5, rings=3)       # brass studs along the seat front
    chair(4.2, 4.2, math.radians(-150), M['velvet_red']); chair(-7.4, 6.4, math.radians(-40), M['velvet_teal'])
    tx, ty = TEA['x'], TEA['y']; zt = TEA['top']
    mb.frustum((tx, ty, ZF), (tx, ty, zt - 0.1), 0.25, 0.2, M['wood_d'], seg=8); mb.frustum((tx, ty, zt - 0.1), (tx, ty, zt), 1.5, 1.5, M['wood'], seg=20)
    for k in range(3): a = k * 2 * math.pi / 3 + 0.4; mb.frustum((tx, ty, ZF + 0.15), (tx + 1.2 * math.cos(a), ty + 1.2 * math.sin(a), ZF), 0.14, 0.1, M['wood_d'], seg=5)
    mb.frustum((tx, ty, zt), (tx, ty, zt + 0.03), 1.1, 1.1, M['white'], seg=20)
    _cup(mb, tmb, tx - 0.2, ty - 0.5, zt + 0.03, 1.5); _cup(mb, tmb, tx + 0.7, ty + 0.35, zt + 0.03, 1.5)
    mb.frustum((tx - 0.6, ty + 0.5, zt + 0.03), (tx - 0.6, ty + 0.5, zt + 0.7), 0.26, 0.36, M['white'], seg=12); ell(mb, (tx - 0.6, ty + 0.5, zt + 0.74), 0.3, 0.3, 0.14, M['white'], seg=10, rings=5)
    mb.frustum((tx - 0.4, ty + 0.5, zt + 0.5), (tx, ty + 0.55, zt + 0.72), 0.05, 0.03, M['white'], seg=4)
    mb.frustum((tx + 0.35, ty - 0.55, zt + 0.03), (tx + 0.35, ty - 0.55, zt + 0.08), 0.42, 0.42, M['brass'], seg=12)
    for k in range(3): ell(mb, (tx + 0.25 + 0.2 * k, ty - 0.55 + 0.1 * (k % 2), zt + 0.18), 0.13, 0.13, 0.1, M['clay'], seg=6, rings=4)
    mb.frustum((7.5, 12.0, ZF), (7.5, 12.0, ZF + 1.6), 0.18, 0.2, M['wood_d'], seg=6); mb.frustum((7.5, 12.0, ZF + 1.6), (7.5, 12.0, ZF + 1.72), 0.8, 0.8, M['wood'], seg=12)
    ell(mb, (7.5, 12.0, ZF + 2.3), 0.35, 0.35, 0.55, M['teal'], seg=8, rings=5); mb.frustum((7.5, 12.0, ZF + 2.7), (7.5, 12.0, ZF + 3.2), 0.12, 0.2, M['teal'], seg=7)
    sbox(mb, (RX1 - 2.2, 2.0, ZF), (RX1 - 0.4, 7.5, ZF + 2.5), M['plank_f'], 0.2); sbox(mb, (RX1 - 2.35, 1.9, ZF + 2.5), (RX1 - 0.3, 7.6, ZF + 2.7), M['ash'], 0.3)
    ell(mb, (RX1 - 1.2, 3.5, ZF + 3.1), 0.35, 0.35, 0.4, M['brass'], seg=8, rings=5); ell(mb, (RX1 - 1.2, 6.0, ZF + 3.0), 0.3, 0.3, 0.3, M['red'], seg=8, rings=5)

# ============================================================================= hooks
def _lift_world(h): return float(h) * (LIFT_MAX if STATE.get('loc') == 'street' else CELL_LIFT)

def set_lift(h, frame=None):
    """Lift the building. street: h 0..1 -> 0..LIFT_MAX (3.6 D): the hotel, awnings, portico (door threshold z = GF + lift), jack screws / heads / bars, lamps rise;
    the front stair stays at the old street level (its top is LIFT_MAX below the door at h 1); timber crib layers show once the building clears them.
    under: h 0..1 -> beams, screws and bars rise CELL_LIFT (1 D). Keys linear when frame is given."""
    Lw = _lift_world(h); STATE['lift_k'] = float(h); STATE['lift'] = Lw
    def _k(ob, path, idx): 
        if frame is not None: ob.keyframe_insert(path, index=idx, frame=frame)
    for ob, base in STATE.get('movers', []): ob.location.z = base + Lw; _k(ob, 'location', 2)
    for (bo, bz, ph, x, y) in STATE.get('bars', []): bo.location.z = bz + Lw; _k(bo, 'location', 2)
    for li, ztop, ob in STATE.get('crib_layers', []):
        vis = ztop <= Lw - 0.05 and Lw > 0.4; ob.hide_render = not vis; ob.hide_viewport = not vis
        if frame is not None: ob.keyframe_insert('hide_render', frame=frame)
    if frame is not None:
        for ob in bpy.data.objects:
            if ob.animation_data and ob.animation_data.action:
                for fc in T._fcurves(ob):
                    for kp in fc.keyframe_points: kp.interpolation = 'LINEAR' if fc.data_path != 'hide_render' else 'CONSTANT'
    return Lw

def set_jack_turn(angle, frame=None):
    """Turn every jack lever by `angle` degrees about its screw axis (a half turn = 180). Keys linear when frame is given."""
    for (bo, bz, ph, x, y) in STATE.get('bars', []):
        bo.rotation_euler.z = ph + math.radians(angle)
        if frame is not None:
            bo.keyframe_insert('rotation_euler', index=2, frame=frame)
            for fc in T._fcurves(bo):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    STATE['jack_angle'] = float(angle)

def set_fill(k, frame=None):
    """Street fill level k 0..1 raises mud, puddles, scum, piles, carts, barrels, planks by k * FILL_MAX (2.5 D); buildings, stair and sidewalks stay."""
    for ob in STATE.get('fill_objs', []):
        ob.location.z = float(k) * FILL_MAX
        if frame is not None: ob.keyframe_insert('location', index=2, frame=frame)
    STATE['fill'] = float(k)

def set_tea_ripple(k, frame=None):
    """Tea surface: k 0 = perfectly still flat mirror (no normal perturbation at all), 1 = visible ripples. The phase follows the frame number."""
    m = STATE['M']['tea']; f = frame if frame is not None else bpy.context.scene.frame_current
    D._keyval(m, 'ripple_k', float(k), frame, 'LINEAR'); D._keyval(m, 'ripple_p', f * 0.35, frame, 'LINEAR'); STATE['tea_k'] = float(k)

def set_rain(level, frame=None, speed=1.0):
    """Rain streaks (compositor overlay, RAIN light only; level 0..1.5). See wall.set_rain."""
    if STATE.get('rain'): W9.set_rain(level, frame=frame, speed=speed)

def set_cutaway(on):
    """Hide the cellar ceiling (beams, joists, floor slab) from the camera only: it keeps casting shadows, so the lighting does not change (under_rows)."""
    for ob in STATE.get('cut_objs', []): ob.visible_camera = not bool(on); ob.visible_shadow = not bool(on)
    STATE['cut'] = bool(on)

def clear_keys():
    for ob in bpy.data.objects:
        if ob.animation_data: ob.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()

def apply_state(state):
    for tok in [t for t in (state or '').replace(' ', '').split(',') if t]:
        if tok.startswith('lift'): set_lift(float(tok[4:]))
        elif tok.startswith('fill'): set_fill(float(tok[4:]))
        elif tok.startswith('jack'): set_jack_turn(float(tok[4:]))
        elif tok.startswith('tea'): set_tea_ripple(float(tok[3:]))
        elif tok.startswith('cut'): set_cutaway(float(tok[3:]) > 0)
        elif tok.startswith('rain'): set_rain(float(tok[4:]))

def stand(name):
    """world position of a named stand point at the current lift (marks flagged 'moves with the lift' add the lift)."""
    x, y, z, lk = STATE['marks'][name]; return (x, y, z + (STATE.get('lift', 0.0) if lk else 0.0))

# ----------------------------------------------------------------------------- placeholder cast + crowd
T.PH.update(
    worker=('beach_man', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    foreman=('senior_b', dict(yaw=-0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    rich=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), 3.3),
    maid=('beach_woman', dict(yaw=-0.2, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.9),
    clerk=('senior_a', dict(yaw=0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 3.0),
    kid=('beach_kid', dict(yaw=-0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.4),
    towns_m=('senior_a', dict(yaw=-0.2, expr='smug', arm_l='hip', arm_r='down', legs='stand'), 3.1),
    towns_f=('beach_woman', dict(yaw=0.2, expr='happy', arm_l='down', arm_r='hip', legs='stand'), 2.9),
    towns_o=('beach_man', dict(yaw=-0.25, expr='happy', arm_l='hip', arm_r='hip', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor
KINDS_STREET = ['worker', 'clerk', 'foreman', 'towns_m', 'towns_f', 'towns_o', 'maid', 'kid']
KINDS_WORK = ['worker', 'foreman', 'worker', 'clerk', 'worker']

def _cards_face(scene, *args):
    """Handler: every background / crowd card yaws to face the scene camera (cards read from any preset)."""
    cam = scene.camera if scene else None
    if cam is None: return
    cp = cam.matrix_world.translation
    for ob in STATE.get('cards', []):
        try:
            p = ob.matrix_world.translation; d = cp - p; ob.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
        except ReferenceError: pass

def _proto(role):
    pr = STATE.setdefault('protos', {})
    if role not in pr:
        ob = T.placeholder_actor(role, (0, 0, -500), name='bgproto_' + role)
        for c in list(ob.users_collection): c.objects.unlink(ob)
        STATE['SET'].objects.link(ob); ob.hide_render = True; ob.hide_viewport = True; pr[role] = ob
    return pr[role]

def crowd(n, regions, seed=1, kinds=None, ground=0.0, min_dist=1.5, scale=(0.93, 1.07), points=None):
    """Place n placeholder cards (cast cards copied from prototypes, sharing mesh + material, turned to the camera every frame by _cards_face).
    regions: [(x0, x1, y0, y1), ...] random rejection sampling with min_dist; or points=[(x, y), ...] exact positions. ground: z or f(x, y) -> z.
    kinds: list of roles (default KINDS_STREET). Returns the objects (names 'bgcard_*'; they are not removed by stage_placeholders)."""
    r = _rnd(seed); kinds = kinds or KINDS_STREET; out = []; pts = []
    if points is None:
        tries = 0
        while len(pts) < n and tries < n * 80:
            tries += 1; (x0, x1, y0, y1) = regions[r.randrange(len(regions))]; x, y = r.uniform(x0, x1), r.uniform(y0, y1)
            if all((x - a) ** 2 + (y - b) ** 2 >= min_dist ** 2 for a, b in pts): pts.append((x, y))
    else: pts = list(points)[:n]
    for i, (x, y) in enumerate(pts):
        role = kinds[r.randrange(len(kinds))]; pro = _proto(role); ob = pro.copy(); ob.name = 'bgcard_%d_%s' % (len(STATE['cards']), role)
        STATE['SET'].objects.link(ob); ob.hide_render = False; ob.hide_viewport = False; s = r.uniform(*scale); ob.scale = (s, s, s)
        z = ground(x, y) if callable(ground) else float(ground); ob.location = (x, y, z); ob.visible_shadow = True; STATE['cards'].append(ob); out.append(ob)
    return out

def crowd_aisles(n, seed=1, kinds=None, rows=None):
    """workers standing in the cellar aisles beside the jacks (one per aisle slot: x = jack column + 1.3, y = beam row - 1.35)."""
    r = _rnd(seed); slots = [(UX[k] + 1.3, UY[j] - 1.35) for k in range(len(UX) - 1) for j in range(len(UY)) if rows is None or j in rows]; r.shuffle(slots)
    return crowd(n, None, seed=seed, kinds=kinds or KINDS_WORK, ground=0.0, points=slots[:n], scale=(0.95, 1.05))

# ----------------------------------------------------------------------------- staging
STAGING = dict(
    street_wide=[('rich', 'front_a'), ('worker', 'front_b'), ('foreman', 'walk_a'), ('clerk', 'sidewalk_r')],
    hotel_front=[('rich', 'front_c'), ('worker', 'front_b'), ('foreman', 'front_a')],
    front_stair=[('rich', 'door'), ('clerk', 'stair_foot'), ('worker', 'mud_fall')],
    mud_low=[('worker', 'cart_c'), ('foreman', 'walk_b')],
    rain_street=[('worker', 'front_a'), ('clerk', 'sidewalk_r'), ('foreman', 'walk_a')],
    crowd_street=[('rich', 'front_c')],
    under_wide=[('worker', 'worker_a'), ('worker', 'worker_b'), ('foreman', 'foreman'), ('worker', 'worker_c'), ('worker', 'worker_d')],
    under_rows=[('foreman', 'foreman')],
    jack_close=[('worker', 'jack_hands')],
    suite_window=[('rich', 'window_r')],
    tea_close=[],
    suite_two=[('rich', 'window')])
PRESET_CROWD = dict(
    crowd_street=lambda: crowd(24, [(-16, 16, -26, -14)], seed=5, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=1.7) + crowd(8, [(-28, -10, -7.5, -4)], seed=8, ground=1.3, min_dist=1.7),
    street_wide=lambda: crowd(10, [(-30, 30, -30, -14)], seed=6, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=3.0),
    rain_street=lambda: crowd(6, [(-20, 20, -30, -14)], seed=7, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=4.0),
    under_wide=lambda: crowd_aisles(16, seed=3, rows=range(0, 9)),
    under_rows=lambda: crowd_aisles(70, seed=4),
    jack_close=lambda: crowd_aisles(6, seed=9, rows=range(5, 9)),
)

def stage_placeholders(A, name, cam_loc, with_crowd=True):
    """actor cards at the named stand points of the preset (STAGING) + the preset's crowd (PRESET_CROWD)."""
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(STAGING.get(name, [])):
        pos = stand(mk) if isinstance(mk, str) else tuple(mk); d = Vector(cam_loc) - Vector(pos); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, tuple(pos), face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    if with_crowd and name in PRESET_CROWD and not STATE.get('crowd_done'): PRESET_CROWD[name](); STATE['crowd_done'] = True
    return out

def head_pixels(name):
    """[(role, mark, chin_y_px, feet_y_px)] at 720x1280 for the preset's staged actors (rule: chin y < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for (role, mk) in STAGING.get(name, []):
        pos = Vector(stand(mk) if isinstance(mk, str) else mk); h = T.PH[role][2]
        b = world_to_camera_view(sc, cam, pos + Vector((0, 0, h - 1.0))); f = world_to_camera_view(sc, cam, pos)
        out.append((role, mk, round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

def anchors():
    P = STATE['P']; PR = PRESETS[STATE['preset']]
    return dict(location=STATE['loc'], preset=STATE['preset'], light=STATE['light'], cams={k: dict(v) for k, v in CAMS.items()}, cam=dict(CAMS[PR['cam']]), cam_name=PR['cam'],
                key_dir=tuple(Vector(P['key_dir']).normalized()), marks={k: tuple(v[:3]) for k, v in STATE.get('marks', {}).items()}, lights=[o.name for o in STATE['LIGHTS'].objects],
                lift_max=LIFT_MAX, cell_lift=CELL_LIFT, fill_max=FILL_MAX, staging={k: list(v) for k, v in STAGING.items()})

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def render_preset(preset, out, quality='final', actors=True, state=None, light=None, crowds=True):
    scene = bpy.context.scene; A = build(preset, light=light, state=state)
    setup_render(scene, quality); cam = make_camera(A['cam'])
    if actors: stage_placeholders(A, A['cam_name'], tuple(cam.location), with_crowd=crowds)
    return T.render(out)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'; names = sys.argv[2:] or list(PRESETS)
    q = 'final' if mode == 'final' else 'preview'; od = os.path.join(WORK, 'final' if mode == 'final' else 'stills'); os.makedirs(od, exist_ok=True)
    for n in names:
        parts = n.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None; stt = parts[2] if len(parts) > 2 else None
        t = render_preset(pr, os.path.join(od, n.replace(':', '_').replace(',', '-') + '.png'), q, light=lt, state=stt); print(n, 'wall %.1f cpu %.1f' % t, flush=True)
