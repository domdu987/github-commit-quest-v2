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
    street_wide=dict(loc=(-34.0, -62.0, 2.8), look_at=(-5.0, 0.0, 15.5), lens=22),
    hotel_front=dict(loc=(-6.0, -26.0, 1.3), look_at=(0.0, 0.0, 17.0), lens=20),
    front_stair=dict(loc=(5.0, -15.0, 2.8), look_at=(0.0, -2.0, 6.8), lens=24),
    mud_low=dict(loc=(-14.0, -38.0, 0.9), look_at=(0.0, -12.0, 3.2), lens=20),
    rain_street=dict(loc=(-22.0, -52.0, 3.4), look_at=(0.0, 0.0, 13.0), lens=22),
    crowd_street=dict(loc=(-6.0, -34.0, 2.6), look_at=(0.0, -8.0, 7.5), lens=24),
    under_wide=dict(loc=(5.0, -2.0, 2.5), look_at=(9.0, 30.0, 2.9), lens=22),
    under_rows=dict(loc=(4.0, -6.0, 17.0), look_at=(5.0, 30.0, 1.5), lens=24),
    jack_close=dict(loc=(4.0, 10.0, 2.2), look_at=(7.0, 18.0, 2.6), lens=26),
    suite_window=dict(loc=(-3.0, 2.0, 32.6), look_at=(2.5, -10.0, 27.5), lens=22),
    tea_close=dict(loc=(-1.0, 6.2, 31.9), look_at=(-2.4, 3.6, 31.0), lens=30),
    suite_two=dict(loc=(-5.0, 4.4, 32.5), look_at=(1.5, -6.0, 28.5), lens=22),
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
