#!/usr/bin/env python3
"""beck.py : set of film 22 ("ไอ้ช่างวงจร", Harry Beck draws the Tube diagram, London 1931-33) as a real 3D Blender set (bpy 5.3, Cycles CPU).
STYLE BOARD stage: three locations built as stills (the module will grow into the full set).

    python3 beck.py board            # rebuild board/board_1..3.png + style_board.jpg (+ stats)
    python3 beck.py still london_dusk|beck_lodgings_night|platform_tunnel [preview]

World: 1 unit = 1 D (head), Z up. Helpers are imported from the older film sets (tower / mine) the way harbour.py does; every
location here is new. No depth of field, no haze. Painted art lives in beck_tex.py (cache tex_beck/)."""
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
import mine as MN                                          # noqa: E402
import beck_tex as BX                                      # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit, mat_card   # noqa: E402
from mine import obox, rod, lumpy, _untoon                 # noqa: E402
STATE = T.STATE
BOARD = os.path.join(HERE, 'board'); T.ACT = os.path.join(HERE, 'actors')
V = Vector

# ----------------------------------------------------------------------------- light presets
def kdir(az, el):
    """Direction the light travels (from the sun toward the scene); az = compass angle of the SUN (deg, 0 = +y, 90 = +x), el = elevation."""
    a, e = math.radians(az), math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))
_B = dict(toon=1.0, key_desat=0.0, ink='#1a1450', form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.8, night=False)
LIGHTS = dict(
    DUSK_CITY=dict(_B, key=(1.9, 1.0, 0.42), key_dir=kdir(60, 11), shade=(0.10, 0.10, 0.40), shade_tint=(0.085, 0.095, 0.44), shade_mix=0.8,
                   grade_offset=(-0.004, -0.006, 0.0), lift=(0.034, 0.030, 0.078), grade_saturation=1.18),
    LODGINGS=dict(_B, key=(0.0, 0.0, 0.0), key_dir=kdir(0, 60), shade=(0.09, 0.15, 0.46), shade_tint=(0.06, 0.14, 0.56), shade_mix=0.92,
                  grade_offset=(0.0, -0.006, 0.004), lift=(0.006, 0.014, 0.054), grade_saturation=1.32, toon=0.8),
    PLATFORM=dict(_B, key=(0.0, 0.0, 0.0), key_dir=kdir(0, 60), shade=(0.09, 0.14, 0.46), shade_tint=(0.06, 0.12, 0.55), shade_mix=0.8,
                  grade_offset=(0.0, -0.006, 0.004), lift=(0.012, 0.020, 0.070), grade_saturation=1.2, toon=0.8),
)

# ----------------------------------------------------------------------------- scene setup
def setup(lkey, cam_setup, quality='final', sky=False):
    scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    STATE.clear(); STATE['P'] = P; STATE['lkey'] = lkey
    for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('BK_', 'ink')): bpy.data.materials.remove(m)
    tx = BX.ensure(); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_beck') or bpy.data.worlds.new('W_beck'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0.02, 0.03, 0.12, 1); bg.inputs['Strength'].default_value = 1.0
    if sky:
        env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = T._img(tx['sky']); lp = nt.nodes.new('ShaderNodeLightPath')
        nt.links.new(env.outputs['Color'], bg.inputs['Color']); nt.links.new(lp.outputs['Is Camera Ray'], bg.inputs['Strength'])
    else:
        lp = nt.nodes.new('ShaderNodeLightPath'); nt.links.new(lp.outputs['Is Camera Ray'], bg.inputs['Strength'])
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(scene, 'final'); scene.render.threads = 4; scene.cycles.samples = 14 if quality == 'final' else 6
    if quality != 'final': scene.render.resolution_percentage = 50
    scene.frame_start = scene.frame_current = 1
    cam = T.make_camera(cam_setup); cam.data.clip_end = 3000.0; cam.data.dof.use_dof = False; cam.data.shift_y = cam_setup.get('shift_y', 0.0)
    STATE['cam'] = V(cam_setup['loc'])
    FORM = tuple(P['form']); untoon = lkey != 'DUSK_CITY'
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def U(m): return _untoon(m) if untoon else m
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return U(mat_lit('BK_c_%s_%g_%s_%d_%s' % (hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, glow=None, glow_k=0.0, smix=None):
        return U(mat_lit('BK_t_%s_%g_%s_%d_%d_%s_%g_%s' % (name, gain, _k(sm), form, alpha, glow, glow_k, smix), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                         alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    def E(name, image=None, color='#ffffff', k=1.0, alpha=False, additive=False, cam_only=False):
        return mat_emit('BK_e_%s' % name, color, image=tx[image] if image else None, strength=k, alpha=alpha, additive=additive, camera_only=cam_only)
    cards = {}
    def CARD(img):
        if img not in cards: cards[img] = mat_card('BK_card_' + img, tx[img])
        return cards[img]
    STATE.update(C=C, TX=TX, E=E, CARD=CARD, SET=SET)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    return scene, P

def hull_at(p, px=3.0):
    """Ink thickness for 3 px at the distance of point p from the camera (T.hull gives 3 px at 720x1280, lens 22)."""
    return T.hull((V(p) - STATE['cam']).length) * px / 3.0

class Part:
    """One mesh object (many materials). ink = True adds the 3 px inverted hull at the part's distance."""
    def __init__(s, name, at=None, ink=True, shadow=True, camera_only=False):
        s.mb = MB(); s.name = name; s.at = at; s.ink = ink; s.shadow = shadow
    def done(s, at=None, px=3.0):
        at = at or s.at or (0, 0, 0); h = hull_at(at, px) if s.ink else 0.0
        o = s.mb.obj(s.name, STATE['SET'], hull=h)
        no_bounce(o)
        if not s.shadow: o.visible_shadow = False
        return o

def plane(mb, p0, pu, pv, mat, uv=(0, 0, 1, 1)): mb.quad(V(p0), V(pu), V(pv), mat, uv)

def facing_card(mb, base, w, h, mat, cam=None, tilt=0.0, flip=False, v0=0.0):
    cam = cam or STATE['cam']; base = V(base); n = V((cam.x - base.x, cam.y - base.y, 0)); n.normalize()
    r = V((-n.y, n.x, 0)); u = V((0, 0, 1)) * math.cos(math.radians(tilt)) - n * math.sin(math.radians(tilt))
    pts = [base - r * w / 2, base + r * w / 2, base + r * w / 2 + u * h, base - r * w / 2 + u * h]
    mb.pid += 1; mb.face(pts, mat, [(0, v0), (1, v0), (1, 1), (0, 1)] if not flip else [(1, v0), (0, v0), (0, 1), (1, 1)])

def halo_card(mb, c, r, mat):
    cam = STATE['cam']; c = V(c); f = (c - cam).normalized(); rt = f.cross(V((0, 0, 1))).normalized(); up = rt.cross(f)
    mb.pid += 1; mb.face([c - rt * r - up * r, c + rt * r - up * r, c + rt * r + up * r, c - rt * r + up * r], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])

def point_light(name, loc, rgb, energy, radius=0.4):
    return MN._light(name, loc, rgb, energy, radius)

def spot_light(name, loc, target, rgb, energy, spot_deg=60, blend=0.4, radius=0.3):
    d = bpy.data.lights.new(name, 'SPOT'); d.color = rgb; d.energy = energy; d.spot_size = math.radians(spot_deg); d.spot_blend = blend; d.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, d); STATE['LIGHTS'].objects.link(ob); ob.location = loc
    ob.rotation_euler = (V(target) - V(loc)).to_track_quat('-Z', 'Y').to_euler(); ob.visible_camera = False
    return ob

def sun_light(P):
    kd = V(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    ob = bpy.data.objects.new('key_sun', d); STATE['LIGHTS'].objects.link(ob); ob.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); ob.location = (-20, -40, 40)
    return ob

def pitched(mb, x0, x1, y0, y1, z0, z1, rise, wall, roof, ridge_x=True, tx_front=None):
    """Box wall z0..z1 with a pitched roof (ridge along x when ridge_x)."""
    mats = {'front': tx_front or wall, 'back': wall, 'left': wall, 'right': wall}
    mb.box((x0, y0, z0), (x1, y1, z1), wall, mats=dict(mats, top=roof), skip='top')
    zr = z1 + rise
    if ridge_x:
        ym = (y0 + y1) / 2
        mb.pid += 1; mb.face([V((x0, y0, z1)), V((x1, y0, z1)), V((x1, ym, zr)), V((x0, ym, zr))], roof, [(0, 0), (1, 0), (1, 1), (0, 1)])
        mb.pid += 1; mb.face([V((x1, y1, z1)), V((x0, y1, z1)), V((x0, ym, zr)), V((x1, ym, zr))], roof, [(0, 0), (1, 0), (1, 1), (0, 1)])
        mb.pid += 1; mb.face([V((x0, y0, z1)), V((x0, ym, zr)), V((x0, y1, z1))], wall); mb.pid += 1; mb.face([V((x1, y1, z1)), V((x1, ym, zr)), V((x1, y0, z1))], wall)

# ============================================================================= STILL 1: london_dusk
CAM1 = dict(loc=(-13, -46, 70), look_at=(-3, 44, 0), lens=22, shift_y=0.19)

def build_london(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(22)
    sun_light(P)
    # ---- ground: road, pavements, kerbs
    g = Part('ground', (0, 10, 0), ink=False); mb = g.mb
    plane(mb, (-160, -80, -0.05), (320, 0, 0), (0, 80, 0), TX('pave', 0.8), (0, 0, 40, 10))                     # far foreground ground
    plane(mb, (-160, -8, 0.0), (320, 0, 0), (0, 6, 0), TX('pave', 1.0), (0, 0, 40, 1))                          # near pavement
    plane(mb, (-160, -2, 0.0), (320, 0, 0), (0, 16, 0), TX('road', 1.0), (0, 0, 40, 2))                         # road
    plane(mb, (-160, 14, 0.0), (120, 0, 0), (0, 10, 0), TX('pave', 1.0), (0, 0, 15, 1)); plane(mb, (-26, 14, 0.0), (186, 0, 0), (0, 10, 0), TX('pave', 1.0), (0, 0, 22, 1))
    plane(mb, (-40, 14, 0.0), (14, 0, 0), (0, 0.5, 0), TX('pave', 1.0), (0, 0, 2, 1)); plane(mb, (-40, 22.5, 0.0), (14, 0, 0), (0, 1.5, 0), TX('pave', 1.0), (0, 0, 2, 1))   # far pavement with the stair well
    plane(mb, (-160, 24, -0.02), (320, 0, 0), (0, 52, 0), TX('pave', 0.8), (0, 0, 40, 6)); plane(mb, (-160, 110, -0.02), (320, 0, 0), (0, 26, 0), TX('pave', 0.8), (0, 0, 40, 3))   # ground behind HQ (river gap y 76-98)
    g.done()
    k = Part('kerbs', (0, 6, 0)); mb = k.mb; kc = C('#b8a890')
    mb.box((-160, -2.4, 0), (160, -2.0, 0.5), kc); mb.box((-160, 13.6, 0), (160, 14.0, 0.5), kc); k.done()
    # ---- HQ (Underground headquarters): stone block, lit windows, PUBLICITY DEPT big window and sign
    h = Part('hq', (0, 24, 12)); mb = h.mb; fac = TX('hq', 1.0, glow='hq_glow', glow_k=1.5); stone = C('#e4d2a4', 1.0); roofm = C('#3a4690')
    mb.box((-22, 24, 0), (22, 34, 22), stone, mats={'front': fac}, skip='top')
    mb.box((-23, 23, 22), (23, 35, 23.4), stone); mb.box((-23.4, 22.6, 23.4), (23.4, 35.4, 24.2), C('#cdb888'))          # cornice
    mb.box((-22, 24, 24.2), (22, 34, 25.0), roofm)
    for i in range(9): mb.box((-21 + i * 5.2, 23.2, 23.4), (-20 + i * 5.2, 24.0, 24.6), stone)                           # parapet balusters
    mb.box((-6, 27, 25.0), (6, 32, 28), C('#c9b080'))                                                                  # roof lantern block
    mb.box((12, 27, 25.0), (18, 32, 30), C('#7a4a2a')); rod(mb, (15, 29.5, 30), (15, 29.5, 33), 0.4, C('#262050'))       # water tank + vent
    mb.box((-20, 23.4, 0), (20, 24.0, 1.4), C('#8f7d5e'))                                                              # plinth
    for i in range(7): mb.box((-20 + i * 6.6, 23.2, 1.4), (-19.2 + i * 6.6, 24.0, 8), C('#dccaa0'))                    # pilasters
    h.done((0, 24, 14))
    pl = Part('sign_publicity', (0, 24, 24), ink=False); plane(pl.mb, (-8.8, 23.7, 15.6), (17.6, 0, 0), (0, 0, 3.6), E('pub', 'sign_publicity', k=1.9), (0, 0, 1, 1)); pl.done()
    # ---- station entrance: stone block, big roundel, lit canopy, steps down
    e = Part('entrance', (-33, 24, 8)); mb = e.mb; stone2 = C('#d8c498')
    mb.box((-44, 24, 0), (-22, 34, 18), stone2, mats={'front': TX('fac_a', 1.0, glow='fac_a_glow', glow_k=1.2)}, skip='top'); mb.box((-44.6, 23.4, 18), (-21.4, 34.6, 19.2), C('#cdb888'))
    mb.box((-44, 24, 0), (-41, 24.6, 7), C('#9a8868')); mb.box((-25, 24, 0), (-22, 24.6, 7), C('#9a8868'))
    mb.box((-41, 23.7, 0), (-25, 24.1, 6.6), C('#ffb352', 1.6))                                                        # lit doorway
    mb.box((-41.6, 23.0, 6.4), (-24.4, 24.4, 7.2), C('#9a8868'))                                                       # lintel
    for x in (-41.4, -24.6): rod(mb, (x, 13.6, 0), (x, 13.6, 6.5), 0.35, C('#262050'))                                  # canopy posts
    e.done((-33, 24, 10))
    cp = Part('canopy', (-33, 19, 6.8)); mb = cp.mb
    mb.box((-42.4, 13.2, 6.5), (-23.6, 23.6, 7.2), C('#1c2a68')); mb.box((-42.4, 13.0, 7.2), (-23.6, 23.8, 7.7), C('#e3262b'))
    cp.done((-33, 18, 7))
    cg = Part('canopy_glow', ink=False, shadow=False); plane(cg.mb, (-42.0, 13.4, 6.48), (18, 0, 0), (0, 10, 0), E('canopy', color='#ffc46a', k=2.2), (0, 0, 1, 1)); cg.done()
    rg = Part('roundel', ink=False); plane(rg.mb, (-40.4, 23.6, 8.2), (14.8, 0, 0), (0, 0, 9.2), E('roundel', 'roundel', k=1.5, alpha=True), (0, 0, 1, 1)); rg.done()
    bar = Part('canopy_bar', ink=False); plane(bar.mb, (-41.5, 13.1, 6.7), (17, 0, 0), (0, 0, 0.75), E('ugbar', 'sign_underground_bar', k=1.6), (0, 0, 1, 1)); bar.done()
    # steps down into the pit: dark walls, warm lit risers (the pavement has a hole here)
    st = Part('stairs', (-33, 19, 0)); mb = st.mb; wmat = C('#3a2a58')
    mb.box((-40, 14.5, -9.0), (-26, 22.5, -8.6), C('#12102a'))
    for i in range(9):
        z = -0.4 - i * 0.95; y0 = 14.5 + i * 0.9
        mb.box((-39.4, y0, z - 0.5), (-26.6, y0 + 0.9, z), C('#ffb352', 1.5 if i % 2 == 0 else 1.0))
    mb.box((-40.6, 14.0, -9), (-39.4, 23, 0), wmat); mb.box((-26.6, 14.0, -9), (-25.4, 23, 0), wmat); mb.box((-40.6, 22.4, -9), (-25.4, 23.4, 0), wmat)
    st.done((-33, 19, 0))
    pg = Part('pit_glow', ink=False, shadow=False); halo_card(pg.mb, (-33, 18.5, 1.5), 7.0, E('hpit', 'halo_warm', k=1.4, additive=True)); pg.done()
    point_light('pit_up', (-33, 19, 1.0), (1.0, 0.62, 0.3), 1200, 0.8)
    # ---- grate (pavement, warm light from below) near the middle of the far pavement
    gr = Part('grate', (8, 19, 0.1), ink=False); plane(gr.mb, (4, 15.5, 0.06), (8, 0, 0), (0, 7, 0), TX('grate', 1.0, glow='grate_glow', glow_k=2.0), (0, 0, 1, 1)); gr.done()
    gh = Part('grate_glow', ink=False, shadow=False); halo_card(gh.mb, (8, 19, 3.0), 7.0, E('hgr', 'halo_warm', k=1.7, additive=True)); plane(gh.mb, (-1.0, 13.5, 0.09), (18, 0, 0), (0, 11, 0), E('hgr2', 'halo_warm', k=1.5, additive=True), (0, 0, 1, 1)); gh.done()
    point_light('grate_up', (8, 19, 0.6), (1.0, 0.6, 0.25), 900, 0.8)
    # ---- lodging house: end of the near-side terrace, side wall facing the street (+x), Beck's lit window
    lh = Part('lodging', (0, 0, 10)); mb = lh.mb; brick = TX('brick', 1.0, 1.0)
    mb.box((-6, -5, 0), (6, 5, 25), brick, mats={'right': TX('lodging', 1.0, 1.0, glow='lodging_glow', glow_k=2.2)}, skip='top'); mb.box((-6.6, -5.6, 25), (6.6, 5.6, 26.2), C('#e8d8ae'))
    pitched(mb, -6.4, 6.4, -5.4, 5.4, 26.2, 26.2, 5.0, brick, C('#7a3a6a'))
    for cx in (-3, 3): mb.box((cx - .8, -1, 30.5), (cx + .8, 1, 34.5), brick); mb.box((cx - 1.0, -1.2, 34.5), (cx + 1.0, 1.2, 35.2), C('#4a3a30'))
    ob = lh.done((-34, -9, 12)); ob.location = (-32, -9, 0); ob.rotation_euler = (0, 0, math.radians(-32))
    sg = Part('sign_rooms', ink=False); facing_card(sg.mb, (-19, 1.0, 0.0), 10.0, 3.4, E('rooms', 'sign_rooms', k=1.7), STATE['cam'], 0.0)  # stands on the pavement, faces the camera
    sg.done(); rm_ = Part('rooms_posts', (-19, 1, 2)); [rod(rm_.mb, (px, 1.0, 0), (px, 1.0, 3.4), 0.2, C('#26204e'), seg=6) for px in (-23.4, -14.6)]; rm_.done((-19, 1, 2))
    bw = Part('beck_window_glow', ink=False, shadow=False); halo_card(bw.mb, (-32 + 6.4 * math.cos(math.radians(-32)) - 2.0 * math.sin(math.radians(-32)), -9 + 6.4 * math.sin(math.radians(-32)) + 2.0 * math.cos(math.radians(-32)), 14.6), 4.6, E('hbw', 'halo_warm', k=1.4, additive=True)); bw.done()
    # near-side terrace (roofs seen from above: dark foreground) x -80..-38
    tr = Part('terrace', (-60, -9, 12)); mb = tr.mb
    for i, x0 in enumerate(range(-102, -30, 8)):
        hgt = 19 + (i % 3) * 2.5
        pitched(mb, x0, x0 + 8, -14, -4, 0, hgt, 4.2, C(['#a8452c', '#b9764a', '#8f3a28'][i % 3]), C('#c4482c' if i % 2 else '#8a3a5a'), tx_front=TX(['fac_b', 'fac_a', 'fac_b'][i % 3], 1.0, glow=['fac_b_glow', 'fac_a_glow', 'fac_b_glow'][i % 3], glow_k=1.3))
        for cxo in (2.2, 5.8): mb.box((x0 + cxo - .6, -10.6, hgt + 2.2), (x0 + cxo + .6, -9.4, hgt + 5), C('#6a3020')); mb.box((x0 + cxo - .8, -10.8, hgt + 5), (x0 + cxo + .8, -9.2, hgt + 5.6), C('#3a2a30'))
    tr.done((-60, -9, 14))
    # ---- far side buildings flanking the HQ
    fl = Part('flank', (0, 30, 12)); mb = fl.mb
    xs = [(-90, -66, 15, 'fac_b'), (-66, -44, 17, 'fac_c'), (22, 44, 17, 'fac_b'), (44, 68, 18, 'fac_a'), (68, 96, 15, 'fac_c')]
    for x0, x1, hgt, t in xs:
        pitched(mb, x0, x1, 24, 33, 0, hgt, 3.0, C('#a8452c'), C('#c4482c'), tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
        for cx in np.linspace(x0 + 3, x1 - 3, 3): mb.box((cx - .7, 31, hgt + 2), (cx + .7, 32.4, hgt + 5.2), C('#6a3020')); mb.box((cx - .9, 30.8, hgt + 5.2), (cx + .9, 32.6, hgt + 5.8), C('#3a2a30'))
    fl.done((30, 30, 14))
    # ---- rooftop city beyond: rows of gabled blocks with chimneys (smoke)
    ct = Part('city', (0, 70, 12)); mb = ct.mb; chim = []
    for row, (y0, y1) in enumerate(((40, 52),)):
        x = -130 + rs.uniform(0, 6)
        while x < 130:
            w = rs.uniform(9, 17); hg = rs.uniform(7, 12)
            if (-23 < x < 23 and row == 0) or (x < -22 and x + w > -46 and row == 0) or (x < 0 < x + w and row == 0): x += w + 0.6; continue
            t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
            pitched(mb, x, x + w, y0, y1, 0, hg, rs.uniform(3, 5), C(rs.choice(['#a8452c', '#c08050', '#d9c49a', '#8f5a9a'])), C(rs.choice(['#c4482c', '#8a3a5a', '#4a56a0', '#b8742c'])), ridge_x=rs.random() < .7, tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
            for cx in (x + w * .3, x + w * .7):
                if rs.random() < .55: mb.box((cx - .6, (y0 + y1) / 2 - .6, hg + 2.6), (cx + .6, (y0 + y1) / 2 + .6, hg + 5.2), C('#7a3a2a')); chim.append((cx, (y0 + y1) / 2, hg + 5.4))
            x += w + rs.uniform(0.2, 1.2)
    ct.done((0, 70, 14))
    sm = Part('smoke', ink=False, shadow=False); mb = sm.mb; smat = C('#efe4f6', 1.3, 2.6, smix=0.2)
    sel = [c for i, c in enumerate(chim) if i % 2 == 0][:20]
    for (cx, cy, cz) in sel:
        for k in range(4):
            lumpy(mb, (cx + 1.0 * k + rs.uniform(-.3, .3), cy, cz + 1.6 + k * 2.0), 1.0 + k * 0.55, smat, rs.randint(1, 99), seg=8, rings=5, rough=0.18)
    sm.done()
    # ---- river, embankments, bridges
    rv = Part('river', ink=False, shadow=False); plane(rv.mb, (-300, 64, -1.0), (600, 0, 0), (0, 30, 0), E('river', 'river', k=1.1), (0, 0, 9, 1)); rv.done()
    em = Part('embank', (0, 110, 0)); mb = em.mb; ec = C('#9a8ab8')
    mb.box((-300, 62, -1.4), (300, 64, 2.0), ec); mb.box((-300, 94, -1.4), (300, 96, 2.0), ec)
    em.done((0, 70, 0), px=4)
    br = Part('bridge', (30, 74, 3)); mb = br.mb; bc = C('#e8d8b0'); bd = C('#2a2a60')
    mb.box((24, 60, 1.4), (36, 98, 2.6), bc); mb.box((23.4, 60, 2.6), (24.4, 98, 4.0), bd); mb.box((35.6, 60, 2.6), (36.6, 98, 4.0), bd)
    for y in (68, 79, 90): mb.box((25, y - 1.4, -1.2), (35, y + 1.4, 1.4), bc); mb.box((24.4, y - 2.4, 0.4), (35.6, y + 2.4, 1.4), C('#c8b890'))
    for y in (62, 72, 82, 92):
        for x in (24.0, 36.0): rod(mb, (x, y, 4.0), (x, y, 9.5), 0.28, C('#262050'))
    br.done((30, 74, 3), px=3)
    # second bridge (far, simple lattice) at x -70
    b2 = Part('bridge2', (-70, 74, 3)); mb = b2.mb
    mb.box((-76, 60, 1.4), (-64, 98, 2.4), C('#c04a3a'));
    for y in (66, 79, 92): mb.box((-76, y - .6, 2.4), (-75.2, y + .6, 12), C('#c04a3a')); mb.box((-64.8, y - .6, 2.4), (-64, y + .6, 12), C('#c04a3a')); mb.box((-76, y - .6, 12), (-64, y + .6, 12.8), C('#c04a3a'))
    b2.done((-70, 74, 3))
    bg = Part('bridge_lamps', ink=False, shadow=False); mb = bg.mb
    for y in (62, 72, 82, 92):
        for x in (24.0, 36.0): halo_card(mb, (x, y, 9.8), 2.4, E('hb', 'halo_warm', k=1.9, additive=True))
    bg.done()
    bg2 = Part('bridge_lamps2', ink=False, shadow=False)
    for y in (66, 79, 92): halo_card(bg2.mb, (-70, y, 13.2), 2.6, E('hb', 'halo_warm', k=1.9, additive=True))
    bg2.done()
    # south bank buildings
    sb = Part('southbank', (0, 92, 10)); mb = sb.mb
    x = -150
    while x < 150:
        w = rs.uniform(10, 18); hg = rs.uniform(8, 13); t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
        pitched(mb, x, x + w, 86, 98, 0, hg, 3.6, C('#b8603a'), C('#3a3550'), tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.6))
        for cx in (x + w * .3, x + w * .7):
            mb.box((cx - .5, 91, hg + 2), (cx + .5, 92, hg + 4.8), C('#7a3a2a'))
            for j in (-.25, .25): rod(mb, (cx + j, 91.5, hg + 4.8), (cx + j, 91.5, hg + 5.7), 0.22, C('#c4562a'), seg=6)
        x += w + 0.4
    sb.done((0, 92, 10), px=4)
    # dome (St Paul's-ish) and clock tower with a lit clock
    dm = Part('dome', (-45, 108, 20)); mb = dm.mb; dc = C('#cfc4a8', 1.0, 1.6, smix=0.4); dg = C('#e8b24a', 1.3)
    mb.box((-61, 98, 0), (-29, 122, 12), C('#e4d2a4'), mats={'front': TX('fac_a', 1.0, glow='fac_a_glow', glow_k=1.5)})
    mb.frustum((-45, 111, 12), (-45, 111, 26), 11, 10.5, dc, seg=24);
    for i in range(12): a = 2 * math.pi * i / 12; rod(mb, (-45 + 10.7 * math.cos(a), 111 + 10.7 * math.sin(a), 12.4), (-45 + 10.7 * math.cos(a), 111 + 10.7 * math.sin(a), 25), 0.45, C('#f0e4c8'), seg=5)
    mb.sphere((-45, 111, 26), 10.5, dc, seg=24, rings=10); mb.frustum((-45, 111, 36.5), (-45, 111, 41), 2.6, 2.4, C('#e4d2a4'), seg=12); mb.sphere((-45, 111, 43), 2.6, dg, seg=12, rings=8); rod(mb, (-45, 111, 45), (-45, 111, 50), 0.35, dg)
    dm.done((-45, 108, 20), px=3)
    ck = Part('clocktower', (52, 104, 25)); mb = ck.mb; tw = TX('fac_c', 1.0, glow='fac_c_glow', glow_k=1.6)
    mb.box((44, 96, 0), (60, 112, 30), C('#e4d2a4'), mats={'front': tw}); mb.box((45, 97, 30), (59, 111, 44), C('#d8c498')); mb.box((44, 96, 44), (60, 112, 46), C('#c8b080'))
    mb.box((46.5, 98.5, 46), (57.5, 109.5, 54), C('#c8b080')); mb.frustum((52, 104, 54), (52, 104, 68), 6.2, 0.2, C('#3a6a98'), seg=4); rod(mb, (52, 104, 68), (52, 104, 73), 0.3, dg)
    for px_, py_ in ((44.6, 96.6), (59.4, 96.6), (44.6, 111.4), (59.4, 111.4)): mb.frustum((px_, py_, 44), (px_, py_, 52), 1.0, 0.1, C('#c8b080'), seg=4); rod(mb, (px_, py_, 52), (px_, py_, 54), 0.1, dg)
    mb.box((45.4, 95.6, 31.4), (58.6, 96.0, 44.6), dg)
    ck.done((52, 104, 25), px=3)
    cf = Part('clockface', ink=False); plane(cf.mb, (46.6, 95.5, 33), (10.8, 0, 0), (0, 0, 10.8), E('clk', 'clock', k=1.5, alpha=True), (0, 0, 1, 1)); cf.done()
    # far field: filler rows of blocks, a glowing far ground, two skyline cards, so there is city all the way to the horizon
    ff = Part('farfield', (0, 200, 12), ink=False); mb = ff.mb
    plane(mb, (-3000, 100, -0.6), (6000, 0, 0), (0, 2600, 0), E('farground', 'farground', k=1.0), (0, 0, 1, 1))
    for (y0, y1, hmin, hmax) in ((100, 114, 8, 12), (118, 134, 8, 13), (140, 160, 9, 14), (170, 196, 9, 14), (210, 244, 9, 14)):
        x = -260
        while x < 260:
            w = rs.uniform(12, 24); hg = rs.uniform(hmin, hmax); t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
            if not (y0 == 100 and -66 < x < -26 or y0 == 100 and 40 < x < 64):
                pitched(mb, x, x + w, y0, y1, 0, hg, rs.uniform(2.4, 4), C('#8a3a2a'), C(rs.choice(['#3a3550', '#4a3a58', '#5a3a3a'])), ridge_x=rs.random() < .75, tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
                for cx in (x + w * .25, x + w * .6, x + w * .85):
                    if rs.random() < .6:
                        mb.box((cx - .4, (y0 + y1) / 2 - .4, hg + 2), (cx + .4, (y0 + y1) / 2 + .4, hg + 4.5), C('#7a3a2a'))
                        for j in (-.18, .18): rod(mb, (cx + j, (y0 + y1) / 2, hg + 4.5), (cx + j, (y0 + y1) / 2, hg + 5.3), 0.2, C('#c4562a'), seg=6)
            x += w + rs.uniform(0.3, 1.5)
    ff.done()
    sk = Part('skyline', ink=False, shadow=False)
    plane(sk.mb, (-340, 330, 0), (680, 0, 0), (0, 0, 105), E('sky1', 'skyline', k=1.15, alpha=True), (0, 0, 1, 1))
    plane(sk.mb, (-700, 600, 0), (1400, 0, 0), (0, 0, 150), E('sky2', 'skyline2', k=1.0, alpha=True), (0, 0, 1, 1)); sk.done()
    for n in ('river', 'embank', 'bridge', 'bridge2', 'bridge_lamps', 'bridge_lamps2'):
        bpy.data.objects[n].location.y += 12
    for n in ('bridge', 'bridge_lamps'): bpy.data.objects[n].location.x -= 46
    for n in ('bridge2', 'bridge_lamps2'): bpy.data.objects[n].location.x += 124
    stars = Part('stars', ink=False, shadow=False)
    for i in range(46):
        az = math.radians(rs.uniform(-34, 30)); el = math.radians(rs.uniform(3.5, 16)); d = 1500
        halo_card(stars.mb, (-13 + d * math.sin(az) * math.cos(el) * 0.0 + d * math.sin(az), -46 + d * math.cos(az) * math.cos(el), 70 + d * math.sin(el)), rs.uniform(3.0, 6.0), E('star', 'halo_white', k=2.6, additive=True))
    stars.done()
    for n in ('southbank', 'dome', 'clocktower', 'clockface', 'farfield'):
        bpy.data.objects[n].location.y += 24
    # ---- vehicles: red double-decker bus, black cabs
    bus = Part('bus', (-4, 4, 4)); mb = bus.mb; bm = TX('bus', 1.0, 6.0, glow='bus_glow', glow_k=1.6, smix=0.15); bred = C('#c8201e', 1.0, 6.0, smix=0.15)
    mb.box((-16, 1.2, 0.8), (8, 6.2, 10.4), bred, mats={'front': bm, 'back': bm, 'top': C('#e03a30', 1.2, 7.0, smix=0.15)}, skip='')
    mb.box((-16.2, 1.0, 10.4), (8.2, 6.4, 10.8), C('#9a1614', 1.0, 4.0, smix=0.15)); mb.box((-16, 1.2, 0.2), (8, 6.2, 1.2), C('#3a0a10', 1.0, 3.0))
    mb.box((-16.1, 2.0, 4.6), (-15.9, 5.4, 5.2), C('#fff2c0', 1.8))                                                       # route board
    mb.box((7.0, 1.0, 0.8), (8.6, 1.5, 10.4), C('#2a0a14')); mb.box((7.0, 5.9, 0.8), (8.6, 6.4, 10.4), C('#2a0a14'))     # open rear platform posts
    for wx in (-12, -9.5, 3.0):
        for wy in (1.6, 5.8): mb.frustum((wx, wy - .35, 1.1), (wx, wy + .35, 1.1), 1.15, 1.15, C('#14143a'), seg=12)
    bus.done((-4, 4, 4))
    point_light('bus_warm', (-4, -3, 6), (1.0, 0.7, 0.4), 5200, 1.0)
    bl = Part('bus_lamps', ink=False, shadow=False); halo_card(bl.mb, (-16.4, 2.4, 2.2), 2.4, E('hl', 'halo_white', k=1.8, additive=True)); halo_card(bl.mb, (-16.4, 5.0, 2.2), 2.4, E('hl', 'halo_white', k=1.8, additive=True)); bl.done()
    cabs = [((14, 0.6), 1), ((26, 11.2), -1), ((-26, 11.4), -1), ((38, 0.8), 1)]
    cb = Part('cabs', (20, 6, 3)); mb = cb.mb; cm = TX('cab', 1.0, 2.0, glow='cab_glow', glow_k=1.6, smix=0.3); cbk = C('#1d2250', 1.0, 1.6)
    for (cx, cy), d in cabs:
        mb.box((cx - 3.6, cy, 0.7), (cx + 3.6, cy + 3.6, 3.2), cbk, mats={'front': cm, 'back': cm}); mb.box((cx - 2.2 * d - 1.4 + (0 if d > 0 else 0.0), cy + 0.25, 3.2), (cx - 2.2 * d + 1.4 + (0), cy + 3.35, 5.0), cbk, mats={'front': cm, 'back': cm})
        for wx in (cx - 2.2, cx + 2.2):
            for wy in (cy + 0.1, cy + 3.5): mb.frustum((wx, wy - .25, 0.7), (wx, wy + .25, 0.7), 0.7, 0.7, C('#0e0e28'), seg=10)
    cb.done((20, 6, 3))
    ch = Part('cab_lamps', ink=False, shadow=False)
    for (cx, cy), d in cabs: halo_card(ch.mb, (cx - 3.9 * d, cy + 0.8, 1.9), 1.5, E('hl', 'halo_white', k=1.7, additive=True)); halo_card(ch.mb, (cx - 3.9 * d, cy + 2.8, 1.9), 1.5, E('hl', 'halo_white', k=1.7, additive=True))
    ch.done()
    # ---- street furniture: lamp posts + halos, kiosk, flower stall, bollards, railings
    lp = Part('lamps', (0, 6, 7)); mb = lp.mb; lc = C('#26204e'); bulb = E('bulb', color='#ffd98a', k=2.2)
    lamps = [(-52, -3.3), (-20, -3.3), (14, -3.3), (44, -3.3), (-52, 24.5 - 9.6), (-12, 24.5 - 9.6), (30, 24.5 - 9.6), (56, 24.5 - 9.6)]
    lamps = [(-18, -3.3), (12, -3.3), (40, -3.3), (66, -3.3), (-24, 15.2), (-6, 15.2), (32, 15.2), (56, 15.2)]
    for (lx, ly) in lamps:
        rod(mb, (lx, ly, 0), (lx, ly, 12.5), 0.34, lc, r1=0.22, seg=8); mb.box((lx - .8, ly - .8, 0), (lx + .8, ly + .8, 1.5), lc); mb.box((lx - 1.0, ly - 1.0, 12.5), (lx + 1.0, ly + 1.0, 13.0), lc)
        mb.frustum((lx, ly, 13.0), (lx, ly, 13.8), 0.9, 0.6, lc, seg=8); mb.sphere((lx, ly, 15.0), 1.4, bulb, seg=12, rings=8)
    lp.done((0, 6, 7))
    lh_ = Part('lamp_halos', ink=False, shadow=False)
    for (lx, ly) in lamps:
        halo_card(lh_.mb, (lx, ly, 13.9), 4.4, E('hh', 'halo_warm', k=1.9, additive=True)); plane(lh_.mb, (lx - 5, ly - 5, 0.07), (10, 0, 0), (0, 10, 0), E('hp', 'halo_warm', k=0.9, additive=True), (0, 0, 1, 1))
    lh_.done()
    for i, (lx, ly) in enumerate(lamps[:4]): point_light('lamp%d' % i, (lx, ly, 13.2), (1.0, 0.68, 0.34), 2200, 0.6)
    ks = Part('kiosk', (-16, 20, 3)); mb = ks.mb
    mb.box((-19, 17.5, 0), (-13, 21.5, 4.6), C('#1f8a52'), mats={'front': C('#1f8a52')}); mb.box((-19.6, 17.0, 4.6), (-12.4, 22, 5.6), C('#e3262b')); mb.box((-18.4, 17.1, 1.6), (-13.6, 17.5, 3.4), C('#ffc65a', 1.5))
    ks.done((-16, 20, 3))
    ksg = Part('kiosk_sign', ink=False); plane(ksg.mb, (-21.0, 16.8, 5.6), (9.0, 0, 0), (0, 0, 2.7), E('news', 'sign_news', k=1.7), (0, 0, 1, 1)); ksg.done()
    fs = Part('flowers', (20, 21, 2)); mb = fs.mb
    mb.box((17, 19.5, 0), (23, 22, 1.8), C('#6a3a1a')); mb.box((16.6, 19.2, 1.8), (23.4, 22.4, 2.0), C('#f0e4c8'))
    for i in range(6): lumpy(mb, (17.6 + i * 1.0, 20.7, 2.5), 0.55, C(['#e3262b', '#ffc81e', '#d1409a', '#ffffff', '#ff7a1e', '#e3262b'][i]), i, seg=8, rings=5)
    mb.box((15.8, 18.8, 5.0), (24.2, 22.8, 5.3), C('#12724a')); rod(mb, (16, 19, 2), (16, 19, 5), 0.2, lc); rod(mb, (24, 19, 2), (24, 19, 5), 0.2, lc)
    fs.done((20, 21, 2))
    fgn = Part('flower_sign', ink=False); plane(fgn.mb, (15.4, 18.6, 5.5), (9.0, 0, 0), (0, 0, 2.5), E('flw', 'sign_flowers', k=1.4), (0, 0, 1, 1)); fgn.done()
    bol = Part('bollards', (0, -1, 1)); mb = bol.mb
    for bx in range(-30, 60, 7): rod(mb, (bx, -2.8, 0), (bx, -2.8, 1.4), 0.4, C('#e8e0c8'), seg=8)
    bol.done((0, -1, 1))
    # tall iron railings on the near embankment edge dark foreground + traffic signal
    rl = Part('railings', (6, -9, 2)); mb = rl.mb; rc = C('#1e1a46')
    for rx in np.arange(2, 70, 1.6): rod(mb, (rx, -8.2, 0), (rx, -8.2, 3.0), 0.12, rc, seg=4)
    mb.box((2, -8.4, 2.8), (70, -8.0, 3.2), rc); mb.box((2, -8.4, 0.6), (70, -8.0, 0.9), rc)
    rl.done((6, -9, 2))
    pb = Part('phoneboxes', (10, -5, 3)); mb = pb.mb; red = C('#e3262b', 1.0, 3.2, smix=0.22)
    for bx in (-8, 26):
        mb.box((bx - 1.4, -6.8, 0), (bx + 1.4, -4.2, 6.4), red); mb.box((bx - 1.6, -7.0, 6.4), (bx + 1.6, -4.0, 6.9), red)
        mb.box((bx - 1.0, -7.05, 1.2), (bx + 1.0, -6.75, 5.4), C('#ffd88a', 1.6)); 
    for bx in (4, 48): rod(mb, (bx, -5.2, 0), (bx, -5.2, 4.2), 1.1, red, seg=12); mb.frustum((bx, -5.2, 4.2), (bx, -5.2, 4.8), 1.2, 0.8, red, seg=12)
    pb.done((10, -5, 3))
    pg2 = Part('phone_glow', ink=False, shadow=False)
    for bx in (-8, 26): halo_card(pg2.mb, (bx, -7.4, 3.4), 3.6, E('hph', 'halo_warm', k=1.2, additive=True))
    pg2.done()
    # ---- crowds (painted placeholder cards with hats, rim light)
    cr = Part('crowd', ink=False); mb = cr.mb; cam = STATE['cam']
    PEOPLE = []
    def person(x, y, k, rimset='w', h=4.1, z=0.0):
        card = CARD('crowd_%s%d' % (rimset, k % 10)); w = h * 200 / 440; facing_card(mb, (x, y, z), w, h, card, cam, tilt=5.0); PEOPLE.append((x, y, w))
    n = 0
    for (x0, x1, y0, y1, num, rimset) in ((-30, -2, 15.5, 22.5, 18, 'w'), (-6, 40, 15.6, 22.5, 16, 'w'), (0, 66, 14.5, 23, 12, 'w'), (-30, 66, -7, -3, 14, 'c'), (-8, 22, 1.0, 12.5, 6, 'w'), (-20, 60, -8, -4.5, 12, 't')):
        for i in range(num): person(rs.uniform(x0, x1), rs.uniform(y0, y1), n, rimset, h=rs.uniform(5.6, 6.6)); n += 1
    for i in range(9): person(-39 + i * 1.6, 16.5 + (i % 3) * 1.6, n, 't', 6.0); n += 1        # queue at the entrance
    for (x0, x1, y0, y1, num, rimset) in ((24, 70, -7.5, -3.5, 16, 't'), (20, 66, 0.5, 12, 8, 'c'), (-70, -40, 15.5, 22.5, 10, 'w')):
        for i in range(num): person(rs.uniform(x0, x1), rs.uniform(y0, y1), n, rimset, h=rs.uniform(5.6, 6.6)); n += 1
    cr.done()
    bsh = Part('contact_shadows', ink=False, shadow=False)
    for (bx, by, bw_) in PEOPLE: plane(bsh.mb, (bx - bw_ * 0.7, by - 0.7, 0.09), (bw_ * 1.4, 0, 0), (0, 1.4, 0), E('blob', 'blob', alpha=True), (0, 0, 1, 1))
    bsh.done()
    bl2 = Part('blobs', ink=False, shadow=False); mb = bl2.mb
    # ---- foreground dark prop: big lamp post at the bottom right, in the nearest 15 %
    fg = Part('fg_post', (10, -26, 8)); mb = fg.mb; fc = C('#1c1850', 0.8)
    rod(mb, (12, -22, 0), (12, -22, 15), 0.55, fc, r1=0.3, seg=10); mb.box((11, -23, 0), (13, -21, 2.2), fc); mb.box((10.6, -22.6, 15), (13.4, -21.4, 16))  if False else None
    mb.frustum((12, -22, 15), (12, -22, 16.2), 1.8, 1.0, fc, seg=10); mb.sphere((12, -22, 18.0), 1.7, bulb, seg=14, rings=9)
    fg.done((12, -22, 10))
    fh = Part('fg_halo', ink=False, shadow=False); halo_card(fh.mb, (12, -22, 17.6), 5.0, E('hh', 'halo_warm', k=2.0, additive=True)); fh.done()

# ============================================================================= STILL 2: beck_lodgings_night
def rim_card(ob, left=None, right=None, px=6):
    """Re-paint a placeholder actor card with a painted rim light (left / right colour) and swap its image."""
    from PIL import Image
    nt = ob.data.materials[0].node_tree; node = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
    src = bpy.path.abspath(node.image.filepath); im = Image.open(src).convert('RGBA')
    if right: im = BX.add_rim(im, right, 'r', px)
    if left: im = BX.add_rim(im, left, 'l', px)
    out = os.path.join(BX.OUT, 'actor_' + os.path.basename(src)); im.save(out)
    node.image = bpy.data.images.load(out, check_existing=True); node.image.reload()

def actor(role, mark, face_to, tilt=0.0, left=None, right=None):
    ob = T.placeholder_actor(role, mark, face_to=face_to, tilt=tilt, name='actor_%s_%d' % (role, len(bpy.data.objects)))
    if left or right: rim_card(ob, left, right)
    return ob

CAM2 = dict(loc=(-1.8, -9.5, 5.0), look_at=(1.2, 9.0, 3.0), lens=30)

def build_lodgings(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(5); cam = S['cam']
    X, Y, Z = V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1))
    RW, BW, LW = 10.0, 14.0, -10.0; CE = 13.0
    wp = TX('wallpaper', 1.0, 1.0); wpb = TX('wallpaper_b', 1.0, 1.0); wd = C('#7a3a1a', 1.0, 1.0); wood = C('#8a4a22', 1.0, 1.0); dwood = C('#5a2c12', 1.0, 1.0)
    r = Part('room', (0, 7, 3), ink=False); mb = r.mb
    plane(mb, (LW, -12, 0), (20, 0, 0), (0, 26, 0), TX('wood', 1.0, 1.0), (0, 0, 7, 9))
    plane(mb, (-6.0, -5.0, 0.03), (13, 0, 0), (0, 15, 0), TX('wallpaper_b', 1.0, 0.9), (0, 0, 3.2, 3.6))                    # rug
    plane(mb, (LW, BW, 0), (20, 0, 0), (0, 0, CE), wp, (0, 0, 7, 3.6)); plane(mb, (RW, -12, 0), (0, 26, 0), (0, 0, CE), wpb, (0, 0, 8, 3.6))
    plane(mb, (LW, -12, 0), (0, 26, 0), (0, 0, CE), wp, (0, 0, 8, 3.6)); plane(mb, (LW, -12, CE), (20, 0, 0), (0, 26, 0), C('#f0a050', 0.9, 1.0), (0, 0, 1, 1))
    r.done()
    sk = Part('skirting', (0, 14, 0.4)); mb = sk.mb
    mb.box((LW, BW - 0.3, 0), (RW, BW, 0.8), wd); mb.box((RW - 0.3, -12, 0), (RW, BW, 0.8), wd); mb.box((LW, BW - 0.2, CE - 1.4), (RW, BW, CE - 1.1), wd); mb.box((LW, BW - 0.3, CE - 0.6), (RW, BW, CE), C('#e8d8ae'))
    sk.done((0, 14, 0.4), px=2)
    # ---- night window (right of the board) with the HQ and its roundel across the street, curtains
    wx0, wx1, wz0, wz1 = 4.5, 8.7, 2.8, 8.4
    wn = Part('window_view', ink=False, shadow=False); plane(wn.mb, (wx0, BW - 0.05, wz0), (wx1 - wx0, 0, 0), (0, 0, wz1 - wz0), E('nightcity', 'night_city', k=1.15), (0.0, 0.0, 0.56, 0.78)); wn.done()
    wf = Part('window_frame', (6.6, 14, 5)); mb = wf.mb; wfm = C('#e8dcc0', 1.0, 1.0)
    mb.box((wx0 - 0.4, BW - 0.5, wz0 - 0.4), (wx1 + 0.4, BW + 0.1, wz0), wfm); mb.box((wx0 - 0.4, BW - 0.5, wz1), (wx1 + 0.4, BW + 0.1, wz1 + 0.4), wfm)
    mb.box((wx0 - 0.4, BW - 0.5, wz0), (wx0, BW + 0.1, wz1), wfm); mb.box((wx1, BW - 0.5, wz0), (wx1 + 0.4, BW + 0.1, wz1), wfm)
    xm = (wx0 + wx1) / 2; mb.box((xm - 0.12, BW - 0.4, wz0), (xm + 0.12, BW, wz1), wfm); mb.box((wx0, BW - 0.4, (wz0 + wz1) / 2 - 0.12), (wx1, BW, (wz0 + wz1) / 2 + 0.12), wfm)
    mb.box((wx0 - 0.9, BW - 1.0, wz0 - 0.7), (wx1 + 0.9, BW - 0.2, wz0 - 0.4), wfm)
    for a, b in ((wx0 - 1.5, wx0 + 0.1), (wx1 - 0.1, wx1 + 1.5)): mb.box((a, BW - 1.1, wz0 - 0.5), (b, BW - 0.5, wz1 + 0.9), C('#c4272f', 1.0, 1.4))
    mb.box((wx0 - 1.9, BW - 1.3, wz1 + 0.8), (wx1 + 1.9, BW - 0.6, wz1 + 1.1), C('#6a3a1a'))
    wf.done((6.6, 14, 5), px=2.5)
    # ---- OLD tangled map (left of the board, facing the camera), cork board of circuits above the board
    om = Part('old_map', (-4, 14, 5)); mb = om.mb; mb.box((-6.15, BW - 0.3, 3.65), (-1.95, BW, 6.95), C('#6a3a1a', 1.0, 1.5)); om.done((-4, 14, 5), px=2.5)
    omp = Part('old_map_img', ink=False); plane(omp.mb, (-5.95, BW - 0.34, 3.85), (3.8, 0, 0), (0, 0, 2.76), TX('old_map', 1.15, 1.0, glow='old_map', glow_k=0.55), (0, 0, 1, 1)); omp.done()
    cb = Part('cork', (1.6, 14, 8.6)); mb = cb.mb; mb.box((-1.7, BW - 0.3, 7.2), (4.9, BW, 10.2), C('#5a2f14')); cb.done((1.6, 14, 8.6), px=2.5)
    cbp = Part('cork_img', ink=False); plane(cbp.mb, (-1.5, BW - 0.34, 7.4), (6.2, 0, 0), (0, 0, 2.6), TX('cork', 1.1, 1.0, glow='cork', glow_k=0.4), (0, 0, 1, 1)); cbp.done()
    sh = Part('shelf', (-4, 13.5, 7.6)); mb = sh.mb; mb.box((-6.2, BW - 1.0, 7.6), (-1.9, BW, 7.85), wd)
    for i in range(10): bh = 0.9 + rs.random() * .5; mb.box((-6.0 + i * 0.4, BW - 0.8, 7.85), (-6.0 + i * 0.4 + 0.34, BW - 0.2, 7.85 + bh), C(rs.choice(['#e3262b', '#1f49c8', '#12a15a', '#ffc81e', '#7a3a8a', '#d8d0b0']), 1.0, 1.5))
    sh.done((-4, 13.5, 8), px=2.5)
    # ---- the drafting board (tilted), diagram, legs, ledge, inks, T-square
    th = math.radians(56); u = V((0, math.cos(th), math.sin(th))); n = V((0, -math.sin(th), math.cos(th))); c0 = V((1.2, 8.3, 3.3)); HW, HS = 3.05, 2.3
    db = Part('drafting_board', (1.2, 8.3, 3.3)); mb = db.mb
    obox(mb, c0, X, u, n, HW + 0.1, HS + 0.1, 0.1, wood)
    for sx in (-1, 1):
        rod(mb, c0 + X * (2.7 * sx) - u * 1.6 - n * 0.2, V((3.1 * sx + 1.2, 6.2, 0.0)), 0.16, dwood, seg=6); rod(mb, c0 + X * (2.5 * sx) + u * 1.2 - n * 0.2, V((3.0 * sx + 1.2, 12.0, 0.0)), 0.16, dwood, seg=6)
    mb.box((-1.8, 6.1, 1.2), (4.2, 6.9, 1.34), wood)
    db.done((1.2, 8.3, 3.3), px=3)
    dg = Part('diagram', ink=False); p0 = c0 + n * 0.115 - X * 2.75 - u * 1.97
    dg.mb.quad(p0, X * 5.5, u * 3.94, TX('diagram', 0.9, 1.0, glow='diagram', glow_k=0.35), (0, 0, 1, 1)); dg.done()
    ts = Part('tools', (1.2, 8.3, 3.3)); mb = ts.mb
    obox(mb, c0 + n * 0.19 + u * 1.7, X, u, n, 2.9, 0.1, 0.04, C('#c8793a', 1.2, 1.3)); obox(mb, c0 + n * 0.19 + u * 1.7 - X * 2.85, X, u, n, 0.22, 0.9, 0.06, C('#4a2410'))
    for k_, (sx_, col) in enumerate(((2.6, '#38d68a'), (3.4, '#56e0ff'))):                                           # set squares lie flat on the ledge, clear of the diagram
        p = [V((sx_, 6.2, 1.36)), V((sx_ + 0.7, 6.2, 1.36)), V((sx_, 6.8, 1.36))]; mb.pid += 1; mb.face(p, C(col, 1.5, 1.5))
    for i, col in enumerate(('#e3262b', '#1f49c8', '#12a15a', '#ffc81e')):
        bx = -1.3 + i * 1.2; rod(mb, (bx, 6.5, 1.34), (bx, 6.5, 2.0), 0.34, C('#222244', 1.0, 1.3), seg=10); rod(mb, (bx, 6.5, 1.34), (bx, 6.5, 1.78), 0.30, C(col, 1.6, 2.0, smix=0.2), seg=10); rod(mb, (bx, 6.5, 2.0), (bx, 6.5, 2.25), 0.16, C(col, 1.2, 1.6, smix=0.2), seg=8)
    ts.done((1.2, 7, 2), px=2.5)
    # ---- key lamp (green shade) left of the board
    lamp = V((-3.3, 5.6, 0)); lm = Part('key_lamp', (-3.3, 5.6, 3.5)); mb = lm.mb; dk = C('#2a2250')
    rod(mb, lamp, lamp + Z * 3.6, 0.16, dk, seg=8); mb.frustum(lamp, lamp + Z * 0.2, 0.55, 0.5, dk, seg=10)
    mb.frustum(lamp + Z * 3.7, lamp + Z * 2.9, 0.2, 1.2, C('#12a15a', 1.0, 1.8, smix=0.2), seg=16, cap0=True, cap1=False); mb.sphere(lamp + Z * 3.3, 0.35, E('bulb2', color='#fff2c0', k=3.0), seg=10, rings=6)
    lm.done((-3.3, 5.6, 3.5), px=3)
    lg = Part('lamp_glow', ink=False, shadow=False); halo_card(lg.mb, lamp + Z * 3.0 + V((0, -0.3, 0)), 3.2, E('hlg', 'halo_warm', k=1.3, additive=True)); lg.done()
    point_light('key_lamp_L', lamp + Z * 3.3 + V((0.3, -0.5, 0)), (1.0, 0.72, 0.38), 1900, 0.35)
    # ---- stove + kettle under the window, coat stand
    st = Part('stove', (7.2, 12.8, 1.5)); mb = st.mb; kc = C('#d8d8e8', 1.3, 1.6)
    mb.box((6.2, 12.0, 0), (8.4, 13.8, 2.3), C('#2a2a50', 1.0, 1.4)); mb.box((6.4, 11.9, 0.6), (8.2, 12.05, 1.6), C('#ff8a3a', 1.6))
    rod(mb, (7.3, 12.9, 2.3), (7.3, 12.9, 3.2), 0.55, kc, r1=0.4, seg=12); rod(mb, (7.3, 12.9, 3.2), (7.3, 12.9, 3.45), 0.2, C('#222244')); rod(mb, (7.8, 12.7, 2.8), (8.6, 12.5, 3.2), 0.1, kc, seg=5); rod(mb, (6.9, 13.6, 2.3), (6.9, 13.6, 7.0), 0.22, C('#222244'), seg=6)
    st.done((7.2, 12.8, 1.5), px=3)
    cs = Part('coat_stand', (8.6, 10.0, 3.5)); mb = cs.mb
    rod(mb, (8.6, 10.0, 0), (8.6, 10.0, 6.0), 0.12, dwood, seg=6); mb.box((8.0, 9.4, 3.0), (9.2, 10.6, 5.6), C('#7a4a2a', 1.0, 1.8)); mb.box((7.7, 9.5, 3.4), (8.2, 10.5, 5.2), C('#7a4a2a', 1.0, 1.8))
    for a_ in range(4): ang = a_ * math.pi / 2; rod(mb, (8.6, 10.0, 5.9), (8.6 + 0.5 * math.cos(ang), 10.0 + 0.5 * math.sin(ang), 6.2), 0.08, dwood, seg=4)
    cs.done((8.6, 10, 3.5), px=3)
    # ---- letter table (right foreground): NOTICE letter lying propped toward the camera, tea cup
    tb = Part('table', (4.0, 0.0, 1.4)); mb = tb.mb
    mb.box((-0.8, -3.4, 1.55), (2.4, -0.6, 1.8), wood)
    for lx in (-0.6, 2.2):
        for ly in (-3.2, -0.8): mb.box((lx - 0.15, ly - 0.15, 0), (lx + 0.15, ly + 0.15, 1.55), dwood)
    rod(mb, (1.8, -1.2, 1.8), (1.8, -1.2, 1.95), 0.36, C('#fff0d0', 1.3, 3.0, smix=0.2), r1=0.28, seg=14); rod(mb, (1.8, -1.2, 1.95), (1.8, -1.2, 2.3), 0.26, C('#fff0d0', 1.3, 3.0, smix=0.2), r1=0.34, seg=14)
    tb.done((4.0, 0, 1.4), px=3)
    ln = Part('letter', ink=True); ln.mb.quad(V((-0.5, -3.0, 1.84)), V((2.0, 0, 0)), V((0, 1.2, 0.8)), TX('note', 1.0, 1.0, glow='note', glow_k=0.35), (0, 0, 1, 1)); ln.done((1.8, -2.4, 2.2), px=2)
    # ---- cot with a patchwork quilt (left foreground, dark foreground layer), pot of rolled drawings, waste basket
    bd = Part('cot', (-3.2, 0.0, 1.5)); mb = bd.mb
    mb.box((-7.4, -3.4, 0.9), (-2.6, 3.0, 1.6), C('#e8dcc0', 1.0, 1.6)); mb.box((-7.5, 3.0, 0), (-2.5, 3.3, 2.5), dwood); mb.box((-7.5, -3.5, 0), (-2.5, -3.2, 2.2), dwood)
    for lx in (-7.3, -2.7):
        for ly in (-3.3, 3.1): rod(mb, (lx, ly, 0), (lx, ly, 0.95), 0.12, dwood, seg=5)
    mb.box((-7.0, 1.4, 1.6), (-3.0, 2.9, 2.0), C('#fff6e0', 1.2, 2.0, smix=0.2))
    bd.done((-4.7, 0, 1.5), px=3)
    qt = Part('quilt', ink=False); plane(qt.mb, (-7.2, -3.2, 1.62), (4.4, 0, 0), (0, 4.5, 0), TX('quilt', 1.0, 1.3), (0, 0, 1, 1)); qt.done()
    rl = Part('rolls', (-5.4, 7.0, 2)); mb = rl.mb
    rod(mb, (-5.4, 7.0, 0), (-5.4, 7.0, 0.9), 0.8, C('#6a3a1a'), r1=0.65, seg=10)
    for i, (dx, dy, tl) in enumerate(((0.0, 0.0, 0.0), (0.35, 0.25, 0.12), (-0.3, 0.3, -0.1), (0.15, -0.3, 0.05))): rod(mb, (-5.4 + dx, 7.0 + dy, 0.9), (-5.4 + dx + tl * 3, 7.0 + dy, 3.2 + i * 0.1), 0.3, C('#f4eccf', 1.2, 1.7), seg=10)
    rl.done((-5.4, 7, 2), px=3)
    tk = Part('trunk', (5.4, 0.4, 0.7)); mb = tk.mb; mb.box((4.4, -0.6, 0), (6.6, 1.6, 1.3), C('#8a4a22', 1.0, 3.0, smix=0.3)); mb.box((4.3, -0.7, 0.5), (6.7, 1.7, 0.65), C('#2a1408')); mb.box((5.3, -0.75, 0.9), (5.7, -0.6, 1.2), C('#e8b84a', 1.4)); tk.done((5.4, 0.4, 0.7), px=3)
    wb = Part('basket', (0.6, 3.0, 0.8)); mb = wb.mb
    rod(mb, (0.2, 3.0, 0), (0.2, 3.0, 1.5), 0.7, C('#3a1a22', 1.0, 1.4), r1=0.9, seg=14)
    for i in range(7): lumpy(mb, (0.2 + rs.uniform(-.5, .5), 3.0 + rs.uniform(-.5, .5), 1.5 + rs.uniform(-.1, .35)), rs.uniform(.28, .42), C('#fff6e0', 1.0, 1.6, smix=0.2), i + 3, seg=8, rings=5, rough=0.35)
    wb.done((0.2, 3.0, 1), px=3)
    pd = Part('pendant', (-1.0, 2.5, 6.8), ink=False, shadow=False); mb = pd.mb; rod(mb, (-0.8, 6.0, CE), (-0.8, 6.0, 7.6), 0.03, C('#222244'), seg=4)
    mb.frustum((-0.8, 6.0, 7.6), (-0.8, 6.0, 7.0), 0.25, 0.85, C('#ffd2a0', 1.2, 2.0), seg=14); mb.sphere((-0.8, 6.0, 7.1), 0.3, E('bulb3', color='#fff2c0', k=3.0), seg=10, rings=6)
    pd.done((-0.8, 6.0, 7.3), px=3)
    point_light('pendant_L', (-0.8, 6.0, 6.8), (1.0, 0.72, 0.4), 750, 0.3)
    point_light('window_rim', (5.5, 15.0, 5.0), (0.28, 0.5, 1.0), 2600, 0.6); point_light('window_rim2', (8.2, 14.8, 4.0), (0.25, 0.45, 1.0), 1500, 0.5)
    # ---- Beck (placeholder card) fully in frame at the board's right side, in front of the window: blue rim from the window, warm from the lamp
    bk = actor('priest', (5.4, 7.2, 0.0), cam, tilt=0.0, left=(110, 170, 255), right=(255, 170, 90)); bk.scale = (1.3, 1.3, 1.3)
    cs_ = Part('contact_shadows', ink=False, shadow=False); plane(cs_.mb, (4.5, 6.4, 0.07), (1.8, 0, 0), (0, 1.6, 0), E('blob', 'blob', alpha=True), (0, 0, 1, 1)); cs_.done()

# ============================================================================= STILL 3: platform_tunnel
CAM3 = dict(loc=(-11.0, -3.0, 4.0), look_at=(0.4, 42.0, 2.8), lens=22)

def build_platform(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(33); cam = S['cam']
    X, Y, Z = V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1))
    RX, SPR, RZ, YA, YB = 13.0, 7.0, 9.0, -12.0, 42.0; TZ = -1.5; PE = 4.4; CX, CZ, CR = 0.0, 2.6, 4.6
    N = 30; outl = [(-RX, 0.0), (-RX, SPR)]
    for i in range(1, N): th = math.pi * (1 - i / N); outl.append((RX * math.cos(th), SPR + RZ * math.sin(th)))
    outl += [(RX, SPR), (RX, 0.0)]
    vt = Part('vault', ink=False); mb = vt.mb; tw = TX('tiles_cool', 1.0, 1.0); tp = TX('tiles_cool_plain', 0.62, 1.0); s_acc = 0.0
    for (x0, z0), (x1, z1) in zip(outl, outl[1:]):
        L = math.hypot(x1 - x0, z1 - z0); mat = tw if z1 <= SPR + 1e-6 and z0 <= SPR + 1e-6 else tp
        v0, v1 = (s_acc / 8.0, (s_acc + L) / 8.0) if mat is tw else ((s_acc - SPR) / 8.0, (s_acc + L - SPR) / 8.0)
        mb.pid += 1; mb.face([V((x0, YA, z0)), V((x1, YA, z1)), V((x1, YB, z1)), V((x0, YB, z0))], mat, [(YA / 4, v0), (YA / 4, v1), (YB / 4, v1), (YB / 4, v0)]); s_acc += L
    # end wall with a real round tunnel hole (annulus triangulated between the vault outline and the hole circle)
    outer = [(-RX, -2.4)] + outl + [(RX, -2.4)] + [(x, -2.4) for x in (8.0, 0.0, -8.0)]
    inner = [(CX + CR * math.cos(2 * math.pi * i / 40), CZ + CR * math.sin(2 * math.pi * i / 40)) for i in range(40)]
    ang = lambda p: math.atan2(p[1] - CZ, p[0] - CX)
    O = sorted(outer, key=ang); I = sorted(inner, key=ang); n_, m_ = len(O), len(I); i = j = 0
    def tri(a, b, c): mb.pid += 1; mb.face([V((p[0], YB, p[1])) for p in (a, b, c)], tw, [(p[0] / 4, p[1] / 8) for p in (a, b, c)])
    while i < n_ or j < m_:
        ai = ang(O[(i + 1) % n_]) + (2 * math.pi if i + 1 >= n_ else 0); aj = ang(I[(j + 1) % m_]) + (2 * math.pi if j + 1 >= m_ else 0)
        if i < n_ and (j >= m_ or ai <= aj): tri(O[i], O[(i + 1) % n_], I[j % m_]); i += 1
        else: tri(I[j], I[(j + 1) % m_], O[i % n_]); j += 1
    vt.done()
    # the tunnel: dark blue tube behind the hole
    tb = Part('tube', ink=False); mb = tb.mb; tube = E('tube', color='#050b30', k=1.0); TL = 60.0
    for k in range(24):
        a0, a1 = 2 * math.pi * k / 24, 2 * math.pi * (k + 1) / 24
        mb.pid += 1; mb.face([V((CX + (CR + 0.15) * math.cos(a0), YB, CZ + (CR + 0.15) * math.sin(a0))), V((CX + (CR + 0.15) * math.cos(a1), YB, CZ + (CR + 0.15) * math.sin(a1))), V((CX + (CR + 0.15) * math.cos(a1), YB + TL, CZ + (CR + 0.15) * math.sin(a1))), V((CX + (CR + 0.15) * math.cos(a0), YB + TL, CZ + (CR + 0.15) * math.sin(a0)))], tube, [(0, 0)] * 4)
    mb.pid += 1; mb.face([V((CX + 4.8 * math.cos(2 * math.pi * k / 24), YB + TL, CZ + 4.8 * math.sin(2 * math.pi * k / 24))) for k in range(24)], E('tube_end', color='#02061c', k=1.0), [(0, 0)] * 24)
    tb.done()
    tl = Part('tunnel_lamps', ink=False, shadow=False)
    for yy in (52.0, 62.0, 72.0): halo_card(tl.mb, (0, yy, 5.6), 2.6, E('htl', 'halo_cool', k=1.2, additive=True))
    tl.done()
    # ---- platforms, track trough, floor
    fl = Part('floor', ink=False); mb = fl.mb
    plane(mb, (-RX, YA, 0), (RX - PE, 0, 0), (0, YB - YA, 0), TX('floor_pf', 1.0, 1.0), (0, 0, 4, 12)); plane(mb, (PE, YA, 0), (RX - PE, 0, 0), (0, YB - YA, 0), TX('floor_pf', 1.0, 1.0), (0, 0, 4, 12))
    plane(mb, (-PE, YA, TZ), (2 * PE, 0, 0), (0, YB - YA + 60, 0), TX('ballast', 1.0, 1.0), (0, 0, 4, 20))
    plane(mb, (-PE, YA, TZ), (0, 0, -TZ), (0, YB - YA, 0), tw, (YA / 4, 0.0, YB / 4, 0.2)); plane(mb, (PE, YA, TZ), (0, 0, -TZ), (0, YB - YA, 0), tw, (YA / 4, 0.0, YB / 4, 0.2))
    fl.done()
    ed = Part('edges', (0, 15, 0.1)); mb = ed.mb; yl = C('#ffd22a', 1.3, 2.0, smix=0.2)
    mb.box((-PE - 0.9, YA, 0), (-PE, YB, 0.12), yl); mb.box((PE, YA, 0), (PE + 0.9, YB, 0.12), yl); mb.box((-PE - 0.25, YA, -0.05), (-PE, YB, 0.0), C('#2a2060'))
    ed.done((0, 15, 0.1), px=2.5)
    rl = Part('rails', (0, 15, TZ)); mb = rl.mb; steel = C('#c8d0ff', 2.0, 3.0, smix=0.1); slp = C('#4a2a1a', 1.0, 1.6)
    for rx in (-1.15, 1.15): mb.box((rx - 0.1, YA, TZ + 0.1), (rx + 0.1, YB + 60, TZ + 0.42), steel)
    mb.box((2.3, YA, TZ + 0.1), (2.55, YB + 60, TZ + 0.3), C('#ff8a3a', 1.6, 2.0))
    for yy in np.arange(YA, YB + 40, 1.4): mb.box((-1.7, yy, TZ), (1.7, yy + 0.4, TZ + 0.12), slp)
    rl.done((0, 15, TZ), px=2.5)
    # ---- vault ribs and globe lamps (warm practicals on a cool vault)
    rb = Part('ribs', (0, 15, 12)); mb = rb.mb; rm = C('#a82838', 1.0, 1.6, smix=0.3)
    for yy in (4.0, 16.0, 28.0, 40.0):
        for (x0, z0), (x1, z1) in zip(outl[1:-1], outl[2:-1]):
            c = V(((x0 + x1) / 2, yy, (z0 + z1) / 2)); tg = V((x1 - x0, 0, z1 - z0)); L = tg.length; tg.normalize(); nrm = V((-tg.z, 0, tg.x))
            obox(mb, c, tg, Y, nrm, L / 2 + 0.05, 0.4, 0.28, rm)
    rb.done((0, 15, 12), px=3)
    gl = Part('globes', (0, 15, 11)); mb = gl.mb; gm = E('globe', color='#fff0c0', k=2.6); lcol = C('#2a2250')
    gh = Part('globe_halos', ink=False, shadow=False); gpos = []
    for yy in (7.0, 20.0, 33.0):
        for gx in (-5.6, 5.6):
            gz = 11.4; gpos.append((gx, yy, gz)); rod(mb, (gx, yy, gz + 1.4), (gx, yy, gz + 0.6), 0.05, lcol, seg=5); mb.sphere((gx, yy, gz), 0.85, gm, seg=14, rings=9)
            halo_card(gh.mb, (gx, yy, gz), 3.0, E('hg', 'halo_warm', k=1.4, additive=True))
    gl.done((0, 15, 11), px=3); gh.done()
    for i, (gx, yy, gz) in enumerate(gpos): point_light('globe%d' % i, (gx, yy, gz - 0.6), (1.0, 0.7, 0.36), 2200 if i < 4 else 1800, 0.5)
    for yy in (10.0, 26.0):
        for wx_, sgn in ((-RX + 0.5, 1), (RX - 0.5, -1)): point_light('wall%d_%d' % (yy, sgn), (wx_ + sgn * 0.4, yy, 6.2), (1.0, 0.68, 0.34), 520, 0.4)
    # ---- end wall: liner ring, station roundel, WAY OUT, clock, old cramped map
    lr = Part('liner', (0, YB, 2.6)); mb = lr.mb; lc_ = C('#3a2a6a', 1.0, 1.6)
    for i in range(32):
        a0, a1 = 2 * math.pi * i / 32, 2 * math.pi * (i + 1) / 32; am = (a0 + a1) / 2; c = V((CX + (CR + 0.5) * math.cos(am), YB - 0.5, CZ + (CR + 0.5) * math.sin(am)))
        tg = V((-math.sin(am), 0, math.cos(am))); nr = V((math.cos(am), 0, math.sin(am))); obox(mb, c, tg, Y, nr, (CR + 0.5) * math.pi / 32 + 0.04, 0.5, 0.5, lc_)
    lr.done((0, YB, 2.6), px=3)
    rd = Part('roundel_name', ink=False); plane(rd.mb, (-6.3, YB - 0.1, 8.1), (12.6, 0, 0), (0, 0, 7.8), E('rndl', 'roundel_piccadilly', k=1.5, alpha=True), (0, 0, 1, 1)); rd.done()
    wo = Part('way_out', ink=True); plane(wo.mb, (6.9, YB - 0.12, 1.4), (5.4, 0, 0), (0, 0, 1.8), E('wayout', 'sign_way_out', k=1.6), (0, 0, 1, 1)); wo.done((9, YB, 2), px=3)
    ck = Part('clock', (8, YB - 3, 12)); mb = ck.mb; rod(mb, (9.2, YB - 3.0, 14.3), (9.2, YB - 3.0, 12.3), 0.06, C('#222244'), seg=5); mb.frustum((9.2, YB - 3.3, 10.8), (9.2, YB - 2.7, 10.8), 1.55, 1.55, C('#1a1840'), seg=20)
    ck.done((9.2, YB - 3, 12), px=3)
    cf = Part('clock_face', ink=False); plane(cf.mb, (7.75, YB - 3.35, 9.35), (2.9, 0, 0), (0, 0, 2.9), E('clk', 'clock', k=1.4, alpha=True), (0, 0, 1, 1)); cf.done()
    om = Part('old_map', ink=True); mb = om.mb
    mb.box((-12.3, YB - 0.4, 1.0), (-6.1, YB - 0.1, 6.0), C('#6a3a1a', 1.0, 1.6)); om.done((-9.2, YB, 3.5), px=2.5)
    omi = Part('old_map_img', ink=False); plane(omi.mb, (-12.0, YB - 0.44, 1.25), (5.6, 0, 0), (0, 0, 4.5), TX('old_map', 1.1, 1.0, glow='old_map', glow_k=0.5), (0, 0, 1, 1)); omi.done()
    # ---- train: deep inside the tunnel; only two hot headlamps and a warm spill show through the hole
    tr = Part('train', (0, 55, 2)); mb = tr.mb; tf = TX('train_front', 1.0, 1.4, glow='train_front_glow', glow_k=0.7, smix=0.15); ts_ = TX('train_side', 1.0, 2.6, glow='train_side_glow', glow_k=1.8, smix=0.15); red = C('#e3262b', 1.0, 2.8, smix=0.15)
    mb.box((-2.8, 54.0, -0.8), (2.8, 80, 5.0), red, mats={'front': tf, 'left': ts_, 'right': ts_}); mb.box((-3.0, 53.9, 5.0), (3.0, 80, 5.25), C('#8a1018', 1.0, 2.0))
    tr.done((0, 55, 2), px=3)
    hl = Part('headlights', ink=False, shadow=False); mb = hl.mb
    for hx_ in (-1.6, 1.6):
        mb.pid += 1; mb.face([V((hx_ + 0.55 * math.cos(2 * math.pi * i / 16), 53.8, 2.4 + 0.55 * math.sin(2 * math.pi * i / 16))) for i in range(16)], E('headl', color='#fffbe0', k=4.5), [(0, 0)] * 16)
        halo_card(mb, (hx_, 53.7, 2.4), 5.0, E('hh2', 'halo_warm', k=2.0, additive=True)); halo_card(mb, (hx_, 53.7, 2.4), 2.4, E('hh3', 'halo_white', k=2.2, additive=True))
    plane(mb, (-3.6, 33.0, TZ + 0.06), (7.2, 0, 0), (0, 12.5, 0), E('spill', 'halo_warm', k=0.9, additive=True), (0, 0, 1, 1))
    hl.done()
    spot_light('headlamp', (0, 52.5, 2.6), (-6.0, 0.0, 1.0), (1.0, 0.78, 0.45), 16000, 52, 0.5, 0.5)
    # ---- posters (un-mirrored), benches, the porter's trolley, a vending machine, newspapers
    ps = Part('posters', ink=True); mb = ps.mb; UV = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for (yy, im) in ((13.0, 'poster0'), (17.0, 'poster1'), (22.0, 'poster2'), (28.0, 'poster3')):                                   # left wall faces +x, u runs +y
        mb.pid += 1; mb.face([V((-RX + 0.06, yy, 2.2)), V((-RX + 0.06, yy + 3.2, 2.2)), V((-RX + 0.06, yy + 3.2, 6.2)), V((-RX + 0.06, yy, 6.2))], TX(im, 1.0, 1.0, glow=im, glow_k=0.35), UV)
    for (yy, im) in ((5.0, 'poster4'), (11.0, 'poster5'), (17.0, 'poster1'), (23.0, 'poster0')):                                     # right wall faces -x, u runs -y
        mb.pid += 1; mb.face([V((RX - 0.06, yy + 4.0, 2.0)), V((RX - 0.06, yy, 2.0)), V((RX - 0.06, yy, 6.4)), V((RX - 0.06, yy + 4.0, 6.4))], TX(im, 1.0, 1.0, glow=im, glow_k=0.35), UV)
    ps.done((0, 12, 4), px=2.5)
    bn = Part('benches', (0, 15, 1)); mb = bn.mb; wood = C('#a85a2a', 1.0, 2.0, smix=0.3); dw = C('#4a2410', 1.0, 1.8)
    for (y0_, y1_) in ((7.0, 13.0), (19.0, 25.0)):
        mb.box((-RX + 0.3, y0_, 1.5), (-RX + 2.0, y1_, 1.75), wood); mb.box((-RX + 0.1, y0_, 1.75), (-RX + 0.5, y1_, 3.4), wood)
        for yy in (y0_ + 0.3, y1_ - 0.5): mb.box((-RX + 0.4, yy, 0), (-RX + 1.9, yy + 0.2, 1.5), dw)
    for (y0_, y1_) in ((10.0, 15.0), (30.0, 35.0)):
        mb.box((RX - 2.0, y0_, 1.5), (RX - 0.3, y1_, 1.75), wood); mb.box((RX - 0.5, y0_, 1.75), (RX - 0.1, y1_, 3.2), wood)
        for yy in (y0_ + 0.3, y1_ - 0.5): mb.box((RX - 1.9, yy, 0), (RX - 0.4, yy + 0.2, 1.5), dw)
    bn.done((0, 15, 1), px=2.5)
    tm = Part('machine', (-RX + 1, 14.5, 2)); mb = tm.mb; mb.box((-RX + 0.1, 14.0, 0), (-RX + 1.6, 16.2, 4.4), C('#c8201e', 1.0, 3.0, smix=0.15)); mb.box((-RX + 1.55, 14.2, 2.0), (-RX + 1.7, 16.0, 3.8), C('#ffd88a', 1.8)); mb.box((-RX + 1.55, 14.3, 0.6), (-RX + 1.7, 15.9, 1.2), C('#3a0a10'))
    tm.done((-RX + 1, 15, 2), px=3)
    tl2 = Part('trolley', (-9.0, 10.5, 1.5)); mb = tl2.mb
    mb.box((-10.0, 9.2, 1.0), (-8.2, 12.0, 1.2), C('#3a2a1a', 1.0, 2.0)); rod(mb, (-8.2, 9.4, 1.2), (-8.2, 9.4, 3.2), 0.1, C('#222244'), seg=5); rod(mb, (-8.2, 11.8, 1.2), (-8.2, 11.8, 3.2), 0.1, C('#222244'), seg=5); mb.box((-8.3, 9.3, 3.1), (-8.1, 11.9, 3.3), C('#222244'))
    for wy in (9.4, 11.8): mb.frustum((-9.6, wy, 0.5), (-9.6, wy + 0.2, 0.5), 0.5, 0.5, C('#14143a'), seg=10)
    mb.box((-9.9, 9.4, 1.2), (-8.5, 10.6, 2.4), C('#8a4a22', 1.0, 3.0, smix=0.3)); mb.box((-9.8, 10.8, 1.2), (-8.6, 11.9, 2.0), C('#1f49c8', 1.0, 3.0, smix=0.3)); mb.box((-9.8, 9.5, 2.4), (-8.6, 10.5, 3.1), C('#12724a', 1.0, 3.0, smix=0.3))
    tl2.done((-9.0, 10.5, 1.5), px=3)
    np_ = Part('newspapers', ink=True); mb = np_.mb
    for (nx, ny, rot) in ((-8.0, 2.5, 0.5), (-6.4, 6.4, -0.4), (-9.8, 4.0, 1.0)):
        ax = V((math.cos(rot), math.sin(rot), 0)); ay = V((-math.sin(rot), math.cos(rot), 0)); obox(mb, V((nx, ny, 0.06)), ax, ay, Z, 0.45, 0.32, 0.03, C('#e8dcb8', 1.0, 1.6, smix=0.3))
    np_.done((-8, 6, 0.1), px=2)
    ab = Part('aframe', (-8.6, 15.5, 1.5)); mb = ab.mb
    for sgn in (-1, 1):
        mb.pid += 1; mb.face([V((-9.8, 17.5, 0)), V((-7.4, 17.5, 0)), V((-7.6, 17.5 + 0.55 * sgn, 3.2)), V((-9.6, 17.5 + 0.55 * sgn, 3.2))], TX('sign_gap', 1.0, 2.0, glow='sign_gap', glow_k=0.3) if sgn < 0 else C('#ffd22a', 1.0, 2.0), UV)
    ab.done((-8.6, 17.5, 1.5), px=3)
    sc3 = Part('suitcases', ink=True); mb = sc3.mb
    mb.box((-8.4, 0.8, 0), (-6.8, 1.8, 1.3), C('#8a4a22', 1.0, 3.0, smix=0.3)); mb.box((-8.5, 0.8, 0.55), (-6.7, 1.8, 0.68), C('#2a1408')); mb.box((-6.4, 2.6, 0), (-5.3, 3.4, 0.9), C('#1f49c8', 1.0, 3.0, smix=0.3))
    sc3.done((-7, 2, 1), px=3)
    # ---- crowd (hats, folded maps) along the platform edge and the far platform; seated reader on the near bench
    cr = Part('crowd', ink=False); mb = cr.mb; PEOPLE = []
    def person(x, y, k, kind='t', h=3.5, z=0.0, crop=0.0):
        card = CARD('crowd_%s%d' % (kind, k % 10)); w = h * 200 / 440; facing_card(mb, (x, y, z), w, h * (1 - crop), card, cam, tilt=0.0, v0=crop)
        if not crop: PEOPLE.append((x, y, w, z))
    n = 0
    for yy in np.arange(8.0, 26.0, 1.2): person(-4.9 - rs.uniform(0, 1.3), yy + rs.uniform(-.2, .2), n, 't', rs.uniform(3.3, 3.7)); n += 1
    for yy in (28.0, 31.0): person(-5.4 - rs.uniform(0, .8), yy, n, 'w', 3.4); n += 1
    person(-11.3, 10.0, 4, 't', 3.5, 1.75, crop=0.36); person(-11.3, 22.0, 7, 'w', 3.5, 1.75, crop=0.36)
    for yy in list(np.arange(5.0, 36.0, 1.2)): person(5.6 + rs.uniform(0, 4.2), yy + rs.uniform(-.4, .4), n, 'c', rs.uniform(3.2, 3.6)); n += 1
    cr.done()
    dk = Part('fg_dark', ink=False)
    for (x, y, k, h) in ((-9.8, 6.0, 0, 3.6), (-5.3, 4.6, 3, 3.6)):
        facing_card(dk.mb, (x, y, 0.0), h * 200 / 440, h, CARD('crowd_d%d' % k), cam, 0.0); PEOPLE.append((x, y, h * 200 / 440, 0.0))
    dk.done()
    actor('priest', (-6.2, 12.2, 0.0), cam, 0.0, left=(110, 170, 255), right=(255, 190, 110)); PEOPLE.append((-6.2, 12.2, 1.3, 0.0))
    actor('extra_b', (-4.9, 16.0, 0.0), cam, 0.0, left=(110, 170, 255), right=(255, 190, 110)); PEOPLE.append((-4.9, 16.0, 1.3, 0.0))
    sh_ = Part('contact_shadows', ink=False, shadow=False)
    for (bx, by, bw_, bz) in PEOPLE: plane(sh_.mb, (bx - bw_ * 0.75, by - 0.7, bz + 0.09), (bw_ * 1.5, 0, 0), (0, 1.4, 0), E('blob', 'blob', alpha=True), (0, 0, 1, 1))
    sh_.done()
    pools = Part('light_pools', ink=False, shadow=False)
    for (gx, yy, gz) in gpos: plane(pools.mb, (gx - 4.5, yy - 4.5, 0.07), (9, 0, 0), (0, 9, 0), E('pool', 'halo_warm', k=0.45, additive=True), (0, 0, 1, 1))
    pools.done()

def render_still(name, builder, lkey, cam, sky=False, quality='final'):
    scene, P = setup(lkey, cam, quality, sky=sky)
    builder(scene, P); setup_grade(scene)
    os.makedirs(BOARD, exist_ok=True); out = os.path.join(BOARD, name + ('.png' if quality == 'final' else '_prev.png'))
    t0 = time.time(); wall, cpu = T.render(out, scene)
    return out, wall, cpu

STILLS = {}
def reg(name, builder, lkey, cam, sky=False, out=None): STILLS[name] = (builder, lkey, cam, sky, out)

reg('london_dusk', build_london, 'DUSK_CITY', CAM1, True, 'board_1')
reg('beck_lodgings_night', build_lodgings, 'LODGINGS', CAM2, False, 'board_2')
reg('platform_tunnel', build_platform, 'PLATFORM', CAM3, False, 'board_3')

def board(only=None):
    """Rebuild board_1..3.png, style_board.jpg and board/stats.json (NOTES.md is written by hand from them)."""
    sys.path.insert(0, HERE); import stats as ST
    res = {}
    for name, (b, l, c, s_, o) in STILLS.items():
        if only and name not in only: continue
        out, wall, cpu = render_still(o, b, l, c, s_, 'final'); st = ST.stats(out); st.update(name=name, file=os.path.basename(out), wall_s=round(wall, 1), cpu_s=round(cpu, 1)); res[name] = st
        print(name, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items()}, flush=True)
    sj = os.path.join(BOARD, 'stats.json')
    old = json.load(open(sj)) if os.path.exists(sj) else {}
    old.update(res); json.dump(old, open(sj, 'w'), indent=1)
    sheet(old)

def sheet(res):
    from PIL import Image, ImageDraw, ImageFont
    names = list(STILLS); W, H = 720, 1280; LAB = 70; im = Image.new('RGB', (W * 3 + 40, H + LAB), '#10102a'); d = ImageDraw.Draw(im)
    ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    for i, n in enumerate(names):
        p = os.path.join(BOARD, STILLS[n][4] + '.png')
        if not os.path.exists(p): continue
        t = Image.open(p).convert('RGB'); x = 20 * i + W * i; im.paste(t, (x, 0)); d.line((x, 880, x + W, 880), fill=(0, 255, 255), width=3)
        d.text((x + 10, H + 6), '%d  %s' % (i + 1, n), font=ft, fill='white')
        r = res.get(n)
        if r: d.text((x + 10, H + 44), 'sat %.2f  luma %.0f  vivid %.0f%%  shade hue %.0f' % (r['sat'], r['luma'], r['vivid'], r['shade_hue']), font=fs, fill=(170, 200, 255))
    im.save(os.path.join(BOARD, 'style_board.jpg'), quality=90)

if __name__ == '__main__':
    a = sys.argv[1:] or ['board']
    if a[0] == 'board': board(a[1:] or None)
    elif a[0] == 'still':
        b, l, c, s_, o = STILLS[a[1]]
        out, wall, cpu = render_still(o, b, l, c, s_, 'preview' if (len(a) > 2 and a[2] == 'preview') else 'final')
        print(out, '%.1fs' % wall)
