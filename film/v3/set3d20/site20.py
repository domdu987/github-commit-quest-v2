"""site20.py : SITE of film 20: the Champ de Mars building site 1887-88 (the tower under construction). Authoring in metres under core20.root() (x SC = D).
build(preset, light) -> A; hooks set_stage(s, frame), crane_swing(k, frame), spark(frame), rivet_toss(k, frame), forge_glow(on, frame)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import core20 as C
import kit20 as K
from core20 import MB, mat, mat_emit, SC, STATE, W, rnd
from kit20 import tw, th, Z1, Z2

# ------------------------------------------------------------------ lights (DAY)
SKY_DAY = ['#f2c89a', '#eec4a4', '#cfc0cc', '#94aee8', '#6a8cdc', '#4c74d2', '#3a62c8']
LIGHTS = dict(
    DAY=dict(sky=SKY_DAY, sky_k=0.8, amb=('#6286FF', 2.4), key=(1.0, 0.82, 0.58, 8.0), key_dir=(0.50, 0.42, -0.42), sun_angle=1.0, exposure=-0.7, sat=1.08, lamp=1.0),
    LATE=dict(sky=['#f0a878', '#e8a090', '#c8a0b8', '#8a8cd8', '#6a76d0', '#5266c4', '#3a4cb8'], sky_k=0.8, amb=('#5a74F8', 2.0), key=(1.0, 0.66, 0.42, 7.0), key_dir=(0.62, 0.30, -0.30), sun_angle=1.2, exposure=-0.7, sat=1.1, lamp=1.0),
)

# ------------------------------------------------------------------ cameras (metres: loc, look, lens, shift) -> world D in A['cams']
CAMS_M = dict(
    site_wide=dict(loc=(-44.0, -178.0, 10.0), look=(4.0, -30.0, 8.0), lens=22, shift=-0.2),
    site_wide_end=dict(loc=(-43.5, -175.0, 8.0), look=(2.0, -30.0, 8.0), lens=22, shift=-0.28),
    site_table=dict(loc=(45.4, -76.6, 1.5), look=(50.0, -72.0, 1.9), lens=22),
    site_leg_low=dict(loc=(-60.0, -82.0, 1.4), look=(-52.0, -58.0, 14.0), lens=22, shift=-0.2),
    site_fence=dict(loc=(-20.0, -109.5, 1.5), look=(-2.0, -98.0, 2.5), lens=22),
    site_girders=dict(loc=(-66.0, -45.0, 1.3), look=(-66.0, -25.0, 2.4), lens=22, shift=0.1),
    site_rivet=dict(loc=(-39.0, -73.0, 17.7), look=(-47.0, -63.0, 17.6), lens=22),
    site_rise=dict(loc=(-30.0, -170.0, 30.0), look=(0.0, 0.0, 55.0), lens=22),
    site_rise_snap1=dict(loc=(-30.0, -170.0, 30.0), look=(0.0, 0.0, 55.0), lens=22),
    site_rise_snap2=dict(loc=(-34.0, -215.0, 50.0), look=(0.0, 0.0, 85.0), lens=22),
    site_rise_snap3=dict(loc=(-40.0, -290.0, 75.0), look=(0.0, 0.0, 150.0), lens=22),
)
PRESETS = dict(site_wide=dict(stage=0), site_table=dict(stage=0), site_leg_low=dict(stage=0), site_fence=dict(stage=0), site_girders=dict(stage=1), site_rivet=dict(stage=1),
               site_rise=dict(stage=1), site_rise_snap1=dict(stage=1), site_rise_snap2=dict(stage=2), site_rise_snap3=dict(stage=3))
EXTRA_CAMS = ['site_wide_end', 'site_rise_snap1', 'site_rise_snap2', 'site_rise_snap3']

def cam_D(c):
    d = dict(loc=W(c['loc']), look_at=W(c['look']), lens=c.get('lens', 22))
    if c.get('shift'): d['shift'] = c['shift']
    return d

SCATTER = dict(site_wide=(15.0, 60.0, 34), site_rise=(30.0, 150.0, 36), site_rise_snap1=(30.0, 150.0, 36), site_rise_snap2=(40.0, 190.0, 34), site_rise_snap3=(60.0, 260.0, 30), site_table=(7.0, 26.0, 14), site_leg_low=(7.0, 26.0, 10), site_fence=(7.0, 30.0, 12), site_girders=(7.0, 30.0, 10), site_rivet=(5.0, 12.0, 3))
APRON = dict(site_wide=(13.0, 12.0, 0.6), site_wide_end=(9.0, 9.0, 0.6), site_table=(3.5, 5.0, 0.6), site_leg_low=(3.5, 5.0, 0.6), site_fence=(3.5, 5.0, 0.6), site_girders=(3.5, 5.0, 0.6), site_rivet=(3.0, 5.0, 0.5),
             site_rise=(45.0, 30.0, 0.55), site_rise_snap1=(45.0, 30.0, 0.55), site_rise_snap2=(60.0, 45.0, 0.55), site_rise_snap3=(80.0, 60.0, 0.55))
PLAN_TABLE = (49.0, -73.4)
LEG_ZS = (5.5, 9.5, 13.5); LEG_DX = (-1.8, 1.6, -0.4)
GIRDER_CARRY = ((-68.2, -37.0), (-63.8, -37.0))
def leg_pt(z, dx=0.0):
    """platform centre on the outer -y face of the front-left leg at height z (m)"""
    return (-K.tw(z) + dx, -(K.tw(z) + K.th(z)) - 0.9, z)
PROP_SCALE = dict(site_wide=1.6, site_rise=2.0, site_rise_snap1=2.0, site_rise_snap2=2.2, site_rise_snap3=2.4)
# foreground dressing per preset: (kind, right_m, up_m, fwd_m, param): see kit20.fg_dress
FG_ITEMS = dict(
    site_wide=[('post', -0.45, 0.0, 1.0, 0.035), ('hook', 0.62, 0.45, 1.6, 0), ('girder', 0.56, -0.22, 1.2, 1.0)],
    site_table=[('girder', 0.50, -0.18, 1.1, 1.0), ('post', -0.47, 0.0, 1.1, 0.04)],
    site_leg_low=[('post', -0.47, 0.0, 1.1, 0.04)],
    site_fence=[('post', -0.47, 0.0, 1.1, 0.04), ('rail', 0.0, -0.26, 1.0, 1.4)],
    site_girders=[('post', -0.47, 0.0, 1.0, 0.04), ('girder', 0.52, -0.20, 1.1, 1.0)],
    site_rivet=[('post', 0.47, 0.0, 1.1, 0.04), ('rail', 0.0, -0.28, 1.1, 1.4)],
    site_rise=[('post', -0.45, 0.0, 1.0, 0.035), ('hook', 0.62, 0.45, 1.6, 0), ('girder', 0.56, -0.22, 1.2, 1.0)], site_rise_snap1=[('post', -0.45, 0.0, 1.0, 0.035), ('hook', 0.62, 0.45, 1.6, 0), ('girder', 0.56, -0.22, 1.2, 1.0)],
    site_rise_snap2=[('post', -0.45, 0.0, 1.0, 0.035), ('hook', 0.62, 0.45, 1.6, 0), ('girder', 0.56, -0.22, 1.2, 1.0)], site_rise_snap3=[('post', -0.45, 0.0, 1.0, 0.035), ('hook', 0.62, 0.45, 1.6, 0), ('girder', 0.56, -0.22, 1.2, 1.0)],
)

# ------------------------------------------------------------------ layout (metres)
# the site: yard between the four legs, fence line y -100, left / right sheds, derricks with the work gantry, Paris behind (Seine y 205-245)
SEINE = (205.0, 245.0, 40.0)
def _band(cam_m):
    c = Vector(cam_m['loc'])
    def f(p, bands):
        d = (Vector((p[0], p[1], 0.0)) - Vector((c.x, c.y, 0.0))).length
        for lim, mb in bands:
            if d < lim: return mb
        return bands[-1][1]
    return f

def gantry(mb, M, c, w=14.0, d=9.0, z=26.0, post=0.55):
    """timber work gantry: 4 braced legs + plank deck + handrail (the 'high crane' the site_wide camera sits on)"""
    x, y, _ = c
    for px in (-w / 2, w / 2):
        for py in (-d / 2, d / 2): mb.rod(M['timber'], (x + px, y + py, 0), (x + px, y + py, z + 1.2), post * 1.2, post, 6)
    for k in range(1, 4):
        zz = z * k / 3.0
        for px in (-w / 2, w / 2): mb.rod(M['timberdk'], (x + px, y - d / 2, zz), (x + px, y + d / 2, zz), post * 0.6, post * 0.6, 5)
        for py in (-d / 2, d / 2): mb.rod(M['timberdk'], (x - w / 2, y + py, zz), (x + w / 2, y + py, zz), post * 0.6, post * 0.6, 5)
        for py in (-d / 2, d / 2): mb.rod(M['timberdk'], (x - w / 2, y + py, zz - z / 3), (x + w / 2, y + py, zz), post * 0.5, post * 0.5, 5); mb.rod(M['timberdk'], (x + w / 2, y + py, zz - z / 3), (x - w / 2, y + py, zz), post * 0.5, post * 0.5, 5)
    mb.box(M['plank'], (x, y, z + 0.1), (w + 0.8, d + 0.8, 0.22))
    for px in (-w / 2 - 0.3, w / 2 + 0.3):
        for k in range(5): mb.rod(M['timberdk'], (x + px, y - d / 2 - 0.3 + k * (d + 0.6) / 4, z + 0.2), (x + px, y - d / 2 - 0.3 + k * (d + 0.6) / 4, z + 1.4), 0.07, 0.07, 4)
        mb.rod(M['timber'], (x + px, y - d / 2 - 0.3, z + 1.3), (x + px, y + d / 2 + 0.3, z + 1.3), 0.06, 0.06, 4)
    for py in (-d / 2 - 0.3, d / 2 + 0.3):
        for k in range(8): mb.rod(M['timberdk'], (x - w / 2 - 0.3 + k * (w + 0.6) / 7, y + py, z + 0.2), (x - w / 2 - 0.3 + k * (w + 0.6) / 7, y + py, z + 1.4), 0.07, 0.07, 4)
        mb.rod(M['timber'], (x - w / 2 - 0.3, y + py, z + 1.3), (x + w / 2 + 0.3, y + py, z + 1.3), 0.06, 0.06, 4)

def derrick2(mb, M, c, h=38.0, jib=22.0, yaw=0.0):
    """timber derrick: mast, boom, guy ropes; returns the boom tip (for the hanging girder)"""
    x, y, z = c
    mb.rod(M['timber'], (x, y, z), (x, y, z + h), 0.55, 0.35, 6); mb.box(M['timberdk'], (x, y, z + 0.5), (2.6, 2.6, 1.0))
    tip = Vector((x + math.cos(yaw) * jib * 0.8, y + math.sin(yaw) * jib * 0.8, z + h * 0.8 + 4.0)); base = Vector((x, y, z + h * 0.62))
    mb.rod(M['timber'], base, tip, 0.4, 0.28, 6)
    mb.rod(M['dark'], Vector((x, y, z + h)), tip, 0.1, 0.1, 4)
    for a in (0.6, 2.2, 3.8, 5.4): mb.rod(M['rope'], (x, y, z + h * 0.97), (x + math.cos(a) * h * 0.75, y + math.sin(a) * h * 0.75, z), 0.1, 0.1, 4)
    return tip

def scaffold_stack(mb, M, c, sx, sy, hgt, lvl=8.0, post=0.8):
    K.scaffold(mb, M, c, sx, sy, hgt, lvl, post)

def build(preset, light=None):
    """SITE builder. preset in PRESETS, light in LIGHTS (default DAY). Returns A."""
    assert preset in PRESETS, preset
    light = light or 'DAY'; P = dict(LIGHTS[light])
    M = C.reset('site', preset, light, spp=8, dbounce=1 if preset in ('site_table', 'site_leg_low', 'site_fence', 'site_girders', 'site_rivet') else 0); R = C.root(); rr = rnd(5)
    M['bluep'] = mat('bluep', '#4a6ea8', '#5a7eb8', 6, contrast=0.8)
    A = dict(preset=preset, light=light, loc='site', cams={}, marks=STATE['marks'], staging=STATE['staging'], hooks={}); STATE['A'] = A
    for n, c in CAMS_M.items(): A['cams'][n] = cam_D(c)
    _marks(A)
    cam0 = CAMS_M[preset]; band = _band(cam0)
    # ---- ground + sky stuff
    ap = APRON.get(preset)
    if ap:
        cl_, fl_, rl_, u_ = K.cam_basis(cam0); fh0 = Vector((fl_.x, fl_.y, 0)); fh0.normalize(); ac = Vector((cl_.x, cl_.y, 0)) + fh0 * ap[0]; ap = (ac.x, ac.y, ap[1], ap[2], (0.6, 0.47, 0.37))
    K.ground_plane(0.0, ('#c98a54', '#b07444', '#8a5a3a'), 3000, 1.0, (0, 600), apron=ap)
    K.clouds(dict(cloud=('#fff0dc', '#c8a8c8', '#e8c8d0'), cloud_k=1.0, ncloud=11, cloud_z=(70, 250), cloud_scale=0.9, cloud_seed=4))
    # ---- tower stages (groups) + creepers
    stages = K.build_tower_stages(M, thick=2.0, lamps=False, gal=M['galwall']); STATE['stage_objs'] = stages
    creep = []
    for s, z in enumerate((K.S_TOPS[0], K.S_TOPS[1], K.S_TOPS[2])):
        mb = MB('creep%d' % s, R)
        for i, (sx, sy) in enumerate(K.LEGS): K.creeper(mb, M, z, sx, sy, 1.0 if s < 2 else 0.8, carry=(i % 2 == 0))
        creep.append(mb.finish())
    STATE['creep'] = creep
    # ---- scaffolds under the legs (timber towers, 36 m, X-braced) + outer low scaffolds
    mb = MB('scaff', R)
    for (sx, sy) in K.LEGS:
        K.scaffold(mb, M, (sx * (tw(24) - 3.0), sy * (tw(24) - 3.0), 4.0), 9.0, 9.0, 36.0, 8.0, 0.8)
        K.scaffold(mb, M, (sx * (tw(24) + 12.0), sy * (tw(24) - 3.0), 0.0), 7.0, 7.0, 24.0, 8.0, 0.7)
        # leg-to-scaffold struts
        mb.rod(M['timber'], (sx * (tw(24) - 3.0), sy * (tw(24) - 3.0) + sy * 4.5, 30.0), (sx * (tw(34) - 0.5), sy * (tw(34) + th(34) * 0.9), 34.0), 0.4, 0.3, 5)
    STATE['scaff'] = mb.finish()
    # ---- derricks + work gantry (the camera platform) + hanging girders
    mb = MB('derricks', R)
    tips = []
    tips.append(derrick2(mb, M, (-84.0, -14.0, 0.0), 42.0, 24.0, 0.0)); tips.append(derrick2(mb, M, (62.0, -92.0, 0.0), 38.0, 22.0, math.pi - 0.5))
    tips.append(derrick2(mb, M, (-82.0, 30.0, 0.0), 44.0, 22.0, -0.2)); tips.append(derrick2(mb, M, (84.0, 26.0, 0.0), 40.0, 22.0, 3.3))
    gantry(mb, M, (70.0, -150.0, 0.0), 12.0, 9.0, 16.0)
    STATE['derricks'] = mb.finish()
    # swinging girder (hook hook): a girder hanging from the left derrick tip on a pivot empty at the mast head
    piv = bpy.data.objects.new('swing', None); bpy.context.scene.collection.objects.link(piv); piv.parent = R; piv.location = (-84.0, -14.0, 42.0 * 0.8 + 4.0); STATE['swing'] = piv
    mb = MB('swinggirder', piv)
    mb.rod(M['dark'], (24.0 * 0.8, 0, 0), (24.0 * 0.8, 0, -9.0), 0.12, 0.12, 4); mb.box(M['dark'], (24.0 * 0.8, 0, -9.3), (1.4, 1.4, 0.8))
    mb.rod(M['rope'], (24.0 * 0.8, 0, -9.0), (24.0 * 0.8 - 2.6, 0, -10.8), 0.1, 0.1, 4); mb.rod(M['rope'], (24.0 * 0.8, 0, -9.0), (24.0 * 0.8 + 2.6, 0, -10.8), 0.1, 0.1, 4)
    for dy in (0.0,): mb.box(M['redleadlt'], (24.0 * 0.8, 0, -11.2), (7.0, 0.9, 0.3)); mb.box(M['redleadlt'], (24.0 * 0.8, 0, -10.6), (7.0, 0.2, 1.2)); mb.box(M['redleadlt'], (24.0 * 0.8, 0, -10.0), (7.0, 0.9, 0.3))
    STATE['swing_objs'] = mb.finish()
    # ---- fence along the visitors' line
    mb = MB('fence', R); K.fence(mb, M, (-60, -100), (-8, -100), 1.15); K.fence(mb, M, (14, -100), (60, -100), 1.15)
    for k in range(5): mb.rod(M['timberdk'], (-8 + k * 4.4, -100, 0.0), (-8 + k * 4.4, -100, 1.15), 0.05, 0.05, 4) if False else None
    mb.finish()
    # (near-yard dressing is added below with the props)
    # ---- props in distance bands (ink hull on the hand-sized props), scaled for wide cameras (PS)
    PS = PROP_SCALE.get(preset, 1.0); FS = 1.0 + (PS - 1.0) * 0.4
    bands = [MB('pn', R), MB('pm', R), MB('pf', R)]; limits = [(14.0, bands[0]), (45.0, bands[1]), (1e9, bands[2])]
    mbn = MB('pnoink', R); lights = []
    def put(fn, p, *a, ink=True, s=None, **k):
        """draw fn(mb, M, *a) with the prop scaled by PS about the ground point p, into the hull band of p"""
        mbx = band(p, limits) if ink else mbn; sc_ = PS if s is None else s
        mbx.push(Matrix.Translation((p[0], p[1], 0)) @ Matrix.Scale(sc_, 4) @ Matrix.Translation((-p[0], -p[1], 0))); fn(mbx, M, *a, **k); mbx.pop()
    # girder stacks (red-lead I-girders: shot 12 slides along them)
    for (x, y, yaw, L_, nx, nz) in [(-66, -30, 0.02, 11.0, 7, 6), (-66, -22, 0.0, 11.0, 7, 6), (-66, -14, 0.03, 10.0, 6, 5), (-30, -24, 1.55, 9.0, 6, 4), (42, -30, 1.6, 9.0, 5, 4), (74, -48, 0.05, 11.0, 6, 5), (-20, -82, 0.1, 8.0, 5, 4)]:
        put(K.girder_pile, (x, y), (x, y, 0), yaw, L_, nx, nz, rr, ink=False, s=(1.7 if preset == 'site_girders' else (1.0 if abs(x) > 60 else PS)))
    forges = [(-20.0, -64.0, 0.1), (24.0, -62.0, 3.0), (-8.0, -30.0, 0.3), (34.0, -12.0, 2.8), (-44.0, -20.0, 0.2), (54.0, -58.0, 0.2), (-34.0, -176.0, 0.4), (-38.0, -148.0, 2.0), (28.0, -150.0, 1.0), (-70.0, -120.0, 0.2), (-12.0, -166.0, 3.0)]
    for (x, y, yaw) in forges:
        K.forge(band((x, y, 0), limits), M, (x, y, 0), yaw, lights, 1.7 * FS)
        mbn.push(Matrix.Translation((x, y, 0)) @ Matrix.Scale(FS, 4) @ Matrix.Translation((-x, -y, 0))); K.smoke_puffs(mbn, M, (x - 0.2, y + 1.0, 6.4), 6, 0.4); mbn.pop()
    for (x, y, h_) in [(-30, -78, 4), (30, -80, 5), (-50, -64, 4), (44, -44, 5), (8, -58, 6), (-6, -86, 3), (-60, -168, 5), (14, -170, 5), (-22, -128, 5), (36, -124, 4), (20, -190, 4)]:
        for i in range(h_): put(K.keg, (x, y), (x + (i % 3) * 0.85 - 0.4, y + (i // 3) * 0.85, 0), 0.95, 0.36, 'timberdk' if i % 2 else 'timber')
    for (x, y, yaw, w, d, h_) in [(-100, -66, 0.1, 9.0, 5.0, 5.2), (-104, 20, 0.0, 10.0, 5.0, 3.6), (100, -74, -0.1, 10.0, 5.0, 3.8), (106, 14, 0.2, 9.0, 5.0, 4.0), (-60, 70, 0.0, 12.0, 6.0, 4.5), (60, 70, 0.0, 12.0, 6.0, 4.5), (-8, -160, 0.1, 8.0, 5.0, 4.2), (36, -124, 0.2, 8.0, 5.0, 4.2), (-70, -120, 0.0, 9.0, 5.0, 4.4)]:
        put(K.shed, (x, y), (x, y, 0), w, d, h_, yaw, s=1.0)
    for (x, y, yaw) in [(30.0, -44.0, 3.0), (-52.0, -76.0, 0.15), (58.0, -76.0, 2.9), (-34.0, -136.0, 0.3), (24.0, -176.0, 2.8)]:
        cp = Vector((x, y, 0)); mbc = band((x, y, 0), limits); mbc.push(Matrix.Translation(cp) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(PS, 4))
        mbc.box(M['timber'], (0, 0, 1.0), (3.4, 1.5, 0.12))
        for s_ in (-1, 1): mbc.box(M['timber'], (0, s_ * 0.74, 1.3), (3.4, 0.08, 0.5))
        K.wheel(mbc, M, (0.2, 0.9, 0.7), 0.7); K.wheel(mbc, M, (0.2, -0.9, 0.7), 0.7); mbc.rod(M['timberdk'], (0.2, 0.9, 0.7), (0.2, -0.9, 0.7), 0.05, 0.05, 6)
        for k in range(3): mbc.box(M['redlead'], (0, (k - 1) * 0.3, 1.2), (3.2, 0.2, 0.06)); mbc.box(M['redlead'], (0, (k - 1) * 0.3, 1.33), (3.2, 0.04, 0.26))
        mbc.rod(M['timberdk'], (1.7, 0.4, 1.0), (4.4, 0.4, 0.9), 0.05, 0.04, 6); mbc.rod(M['timberdk'], (1.7, -0.4, 1.0), (4.4, -0.4, 0.9), 0.05, 0.04, 6)
        mbc.pop(); K.horse_card(mbc, M, (cp.x + math.cos(yaw) * 5.6 * PS, cp.y + math.sin(yaw) * 5.6 * PS, 0.0), yaw, PS)
    for (x, y, yaw) in [(-12, -72, 0.4), (16, -70, 2.0), (-34, -36, 0.9), (40, -66, 0.2), (-20, -140, 1.0), (10, -150, 2.4), (-50, -150, 0.6)]: put(K.wheelbarrow, (x, y), (x, y, 0), yaw, 'glow' if x < 0 else 'rivets')
    for (x, y) in [(-18, -63), (22, -61), (-6, -29), (36, -11), (-42, -19), (-22, -66), (26, -64), (-30, -170), (-10, -162), (-36, -144), (30, -148)]: put(K.bucket, (x, y), (x, y, 0), True, 1.3)
    for (x, y) in [(-26, -70), (6, -62), (-60, -66), (50, -62), (0, -40), (-46, -172), (-2, -140), (22, -128)]: put(K.coil, (x, y), (x, y, 0), 0.65, 0.08, 4)
    for (x, y, yaw) in [(-14, -78, 0.3), (-12, -77, 1.0), (20, -80, 2.0), (-40, -70, 0.0), (-38, -69, 0.9), (-39, -71, 1.9), (48, -70, 0.5), (50, -69, 1.2), (-26, -176, 0.2), (-24, -175, 1.1), (4, -156, 2.0), (6, -155, 0.4), (-44, -134, 0.7)]: put(K.sack, (x, y), (x, y, 0), yaw, 1.15)
    for i, (x, y) in enumerate([(-10, -92), (28, -88), (-48, -84), (56, -86), (-16, -120), (40, -140), (-62, -150)]): put(K.gravel_heap, (x, y), (x, y, 0), 1.7, 0.75, i)
    for (x, y, yaw) in [(-45, -28, 0.3), (-70, -70, 1.6), (58, -34, 3.2), (66, -60, 3.0)]: put(K.ladder, (x, y), (x, y, 0), 4.6, 1.0, yaw, ink=False)
    for (x, y, yaw) in [(24, -50, 0.0)]: put(K.trestle, (x, y), (x, y, 0), 2.6, 0.85, yaw)
    for (x, y, yaw) in [(-4, -104, 0.0), (22, -106, 0.0)]: put(K.bench, (x, y), (x, y, 0), yaw)
    for i in range(44):                                                                 # clutter: stones, offcuts
        x = rr.uniform(-85, 85); y = rr.uniform(-190, 60); k = rr.random()
        if abs(x) < 52 and abs(y) < 52 and rr.random() < 0.8: continue
        if k < 0.5: mbn.ell(M['stonedk'], (x, y, 0.14), (rr.uniform(.2, .55), rr.uniform(.2, .5), 0.2), (8, 6))
        else: mbn.box(M['timber'], (x, y, 0.07), (rr.uniform(1.0, 3.0), 0.16, 0.14), rz=rr.uniform(0, 3.1))
    # camera-frustum scatter: dense, readable yard dressing in front of the preset camera
    cam_ = CAMS_M[preset]; loc_, f_, r_, u_ = K.cam_basis(cam_); fh_ = Vector((f_.x, f_.y, 0)); fh_.normalize(); rh_ = Vector((fh_.y, -fh_.x, 0))
    F0, F1, N_ = SCATTER.get(preset, (4.0, 30.0, 16)); r3 = rnd(77); placed = []
    def clear(x, y):
        if any(abs(x - sx_ * 57.6) < 12 and abs(y - sy_ * 57.6) < 12 for sx_, sy_ in K.LEGS): return False
        if any((Vector((x, y, 0)) - Vector((mm[0] / SC, mm[1] / SC, 0))).length < 2.2 for mm in STATE['marks'].values() if mm): return False
        if (Vector((x, y, 0)) - Vector((loc_.x, loc_.y, 0))).length < 2.5: return False
        return all((x - px_) ** 2 + (y - py_) ** 2 > 6.0 for px_, py_ in placed)
    tries = 0; nforge = 0
    while len(placed) < N_ and tries < 600:
        tries += 1; fw = r3.uniform(F0, F1); rt = r3.uniform(-0.40, 0.40) * fw; p = Vector((loc_.x, loc_.y, 0)) + fh_ * fw + rh_ * rt
        if not clear(p.x, p.y): continue
        placed.append((p.x, p.y)); k = r3.random(); x, y = p.x, p.y
        if k < 0.10 and nforge < 3 and fw > 14: nforge += 1; K.forge(band((x, y, 0), limits), M, (x, y, 0), r3.uniform(0, 6.28), lights, 1.7 * FS)
        elif k < 0.34:
            for j in range(r3.randint(3, 6)): put(K.keg, (x, y), (x + (j % 3) * 0.85 - 0.4, y + (j // 3) * 0.85, 0), 0.95, 0.36, 'timberdk' if j % 2 else 'timber')
        elif k < 0.46: put(K.girder_pile, (x, y), (x, y, 0), r3.uniform(0, 3.1), 6.0, 5, 3, rr, ink=False)
        elif k < 0.60:
            for j in range(r3.randint(2, 4)): put(K.sack, (x, y), (x + j * 0.55, y + (j % 2) * 0.4, 0), r3.uniform(0, 3), 1.15)
        elif k < 0.68: put(K.coil, (x, y), (x, y, 0), 0.65, 0.08, 4)
        elif k < 0.76: put(K.wheelbarrow, (x, y), (x, y, 0), r3.uniform(0, 6.28), 'glow')
        elif k < 0.84: put(K.bucket, (x, y), (x, y, 0), True, 1.3)
        elif k < 0.90: put(K.gravel_heap, (x, y), (x, y, 0), 1.7, 0.75, len(placed))
        elif k < 0.95: put(K.trestle, (x, y), (x, y, 0), 2.6, 0.85, r3.uniform(0, 3))
        elif PS > 1.0: put(K.shed, (x, y), (x, y, 0), 7.0, 4.5, 3.6, r3.uniform(-0.4, 0.4), s=1.0)
    for i in range(0):
        fw = r3.uniform(F0, F1 * 1.3); rt = r3.uniform(-0.45, 0.45) * fw; p = Vector((loc_.x, loc_.y, 0)) + fh_ * fw + rh_ * rt
        mbn.box(M['earthpatch'], (p.x, p.y, 0.014), (r3.uniform(2, 7), r3.uniform(1.2, 3.5), 0.02), rz=r3.uniform(0, 3.1)) if False else None
    K.plank_walk(mbn, M, (0, -192), (-4, -60)); K.plank_walk(mbn, M, (30, -190), (22, -56), 1.0); K.plank_walk(mbn, M, (-30, -60), (30, -62), 1.4)
    for sd in (-0.9, 0.9):
        mbn.box(M['earthpatch'], (p.x, p.y, 0.014), (r3.uniform(2, 7), r3.uniform(1.2, 3.5), 0.02), rz=r3.uniform(0, 3.1)) if False else None
    for i in range(40):
        mbn.box(M['earthpatch'], (p.x, p.y, 0.014), (r3.uniform(2, 7), r3.uniform(1.2, 3.5), 0.02), rz=r3.uniform(0, 3.1)) if False else None
    # the rivet deck at z 16 on the front-left scaffold (shot 13): planks, rails, forge, kegs, bucket, anvil
    dk = Vector((-47.0, -64.0, 16.0))
    mbn.box(M['plank'], (dk.x, dk.y, dk.z), (9.0, 6.0, 0.3))
    for px in (-4.4, 4.4):
        for k in range(4): mbn.rod(M['timberdk'], (dk.x + px, dk.y - 2.8 + k * 1.9, dk.z), (dk.x + px, dk.y - 2.8 + k * 1.9, dk.z + 1.2), 0.07, 0.07, 4)
        mbn.rod(M['timber'], (dk.x + px, dk.y - 2.8, dk.z + 1.15), (dk.x + px, dk.y + 2.9, dk.z + 1.15), 0.06, 0.06, 4)
    for py in (-3.0, 3.0):
        for k in range(7): mbn.rod(M['timberdk'], (dk.x - 4.4 + k * 8.8 / 6, dk.y + py, dk.z), (dk.x - 4.4 + k * 8.8 / 6, dk.y + py, dk.z + 1.2), 0.07, 0.07, 4)
        mbn.rod(M['timber'], (dk.x - 4.4, dk.y + py, dk.z + 1.15), (dk.x + 4.4, dk.y + py, dk.z + 1.15), 0.06, 0.06, 4)
    for k in range(5): mbn.rod(M['timber'], (dk.x - 4.0 + k * 2.0, dk.y - 3.0, dk.z - 14), (dk.x - 4.0 + k * 2.0, dk.y - 3.0, dk.z), 0.2, 0.2, 5) if False else None
    for sx_ in (-4.0, 4.0):
        for sy_ in (-2.6, 2.6): mbn.rod(M['timber'], (dk.x + sx_, dk.y + sy_, 0.0), (dk.x + sx_, dk.y + sy_, dk.z), 0.3, 0.25, 5)
    K.forge(bands[0], M, (dk.x + 2.4, dk.y + 1.4, dk.z + 0.15), 0.35, lights, 1.5)
    for i in range(4): K.keg(bands[0], M, (dk.x - 3.4 + (i % 2) * 0.8, dk.y + 1.5 + (i // 2) * 0.8, dk.z + 0.15), 0.8, 0.3)
    K.bucket(bands[0], M, (dk.x - 0.6, dk.y - 0.4, dk.z + 0.15), True, 1.3)
    K.smoke_puffs(mbn, M, (dk.x + 2.0, dk.y + 2.4, dk.z + 6.2), 5, 0.4)
    STATE['spark_at'] = (dk.x + 1.2, dk.y - 0.8, dk.z + 0.9)
    # shot 4: Eiffel's plan table (plank top on trestles, unrolled blueprint with greeked drawing lines, rolled plans, inkwell, T-square, stool) in front of the front-right leg
    tx_, ty_ = PLAN_TABLE
    def plan_table(mb, M_, c):
        x, y, z0 = c
        mb.box(M_['plank'], (x, y, 0.88), (2.8, 1.2, 0.07))
        for sx_ in (-1.2, 1.2):
            for sy_ in (-0.45, 0.45): mb.rod(M_['timberdk'], (x + sx_, y + sy_, 0.0), (x + sx_ * 0.9, y + sy_ * 0.6, 0.86), 0.05, 0.045, 5)
        mb.box(M_['bluep'], (x + 0.1, y, 0.945), (1.7, 0.95, 0.07), rz=0.04)
        for i in range(9): mb.box(M_['canvasw'], (x + 0.1, y - 0.38 + i * 0.095, 0.99), (1.3 - 0.07 * (i % 3), 0.03, 0.05), rz=0.04)
        for i in range(4): mb.box(M_['canvasw'], (x - 0.4 + i * 0.35, y + 0.05, 0.99), (0.03, 0.5, 0.05), rz=0.04)
        mb.cyl(M_['canvasw'], (x - 1.0, y + 0.3, 0.97), 0.07, 0.9, 'y', 10); mb.cyl(M_['bluep'], (x - 1.0, y + 0.76, 0.97), 0.075, 0.03, 'y', 10); mb.cyl(M_['bluep'], (x - 1.0, y - 0.16, 0.97), 0.075, 0.03, 'y', 10)
        mb.box(M_['timber'], (x + 0.3, y - 0.5, 0.99), (1.4, 0.05, 0.05), rz=0.04); mb.cyl(M_['dark'], (x + 1.05, y + 0.35, 0.96), 0.045, 0.07, 'z', 8)
        mb.box(M_['plank'], (x + 0.4, y + 1.05, 0.5), (0.5, 0.5, 0.05)); [mb.rod(M_['timberdk'], (x + 0.4 + a_, y + 1.05 + b_, 0.0), (x + 0.4 + a_, y + 1.05 + b_, 0.5), 0.03, 0.03, 4) for a_ in (-0.2, 0.2) for b_ in (-0.2, 0.2)]
    mbp = bands[0]; plan_table(mbp, M, (tx_, ty_, 0.0))
    # shot 5: cantilever work platforms on the OUTER (sunlit) -y face of the front-left leg, with rails and braces: riveters stand on them
    for (zz_, dx_) in zip(LEG_ZS, LEG_DX):
        px_, py_, pz_ = leg_pt(zz_, dx_)
        mbn.box(M['plank'], (px_, py_, pz_), (3.4, 1.9, 0.14)); mbn.rod(M['timber'], (px_ - 1.5, py_ - 0.9, pz_ + 1.0), (px_ + 1.5, py_ - 0.9, pz_ + 1.0), 0.05, 0.05, 4)
        for k_ in (-1.6, 0.0, 1.6): mbn.rod(M['timberdk'], (px_ + k_, py_ - 0.9, pz_), (px_ + k_, py_ - 0.9, pz_ + 1.0), 0.05, 0.05, 4)
        for k_ in (-1.5, 1.5): mbn.rod(M['timberdk'], (px_ + k_, py_ + 0.9, pz_ - 0.1), (px_ + k_ * 0.9, py_ + 2.4, pz_ - 1.3), 0.09, 0.07, 4)
        mbn.rod(M['timberdk'], (px_ - 1.5, py_ - 0.9, pz_ + 1.0), (px_ - 1.5, py_ + 0.9, pz_ + 1.0), 0.05, 0.05, 4); mbn.rod(M['timberdk'], (px_ + 1.5, py_ - 0.9, pz_ + 1.0), (px_ + 1.5, py_ + 0.9, pz_ + 1.0), 0.05, 0.05, 4)
        K.bucket(bands[0], M, (px_ + 1.0, py_ - 0.2, pz_ + 0.07), True, 1.2)
    # shot 12: the girder carried on two riveters' shoulders (between the carrier marks)
    gx = (GIRDER_CARRY[0][0] + GIRDER_CARRY[1][0]) / 2.0; gy = GIRDER_CARRY[0][1]
    for (dz_, sz_, dy_) in ((0.0, 0.3, 0.0), (0.18, 0.05, 0.0), (0.36, 0.3, 0.0)): mbn.box(M['redleadlt'], (gx, gy, 1.55 + dz_), (7.0, sz_ if dz_ != 0.18 else 0.05, 0.04 if dz_ != 0.18 else 0.30))
    for (x, y, yaw) in ((-71.0, -40.5, 0.4), (-70.0, -39.8, 1.4), (-61.0, -41.0, 2.1), (-60.0, -39.5, 0.6)): put(K.sack, (x, y), (x, y, 0), yaw, 1.15, ink=True)
    for (x, y) in ((-69.5, -42.0), (-62.5, -43.0)): put(K.coil, (x, y), (x, y, 0), 0.7, 0.08, 4)
    put(K.wheelbarrow, (-59.5, -37.0), (-59.5, -37.0, 0), 2.6, 'glow'); put(K.bucket, (-72.0, -37.5), (-72.0, -37.5, 0), True, 1.3)
    for j in range(4): put(K.keg, (-72.5, -42.5), (-72.5 + (j % 2) * 0.85, -42.5 + (j // 2) * 0.85, 0), 0.95, 0.36, 'timberdk' if j % 2 else 'timber')
    # camera foreground dressing (1-2 D from the lens, in shade)
    fgmb = MB('fg', R); fg_pts = K.fg_dress(fgmb, C.ShadeMats(M), CAMS_M[preset], FG_ITEMS.get(preset, [])); fgmb.finish(hull=0.004)
    STATE['fg_pts'] = fg_pts
    for mbx in bands:
        t = 0.00384 * {id(bands[0]): 10.0, id(bands[1]): 28.0, id(bands[2]): 80.0}[id(mbx)]; mbx.finish(hull=t)
    mbn.finish()
    # ---- Paris: Seine, bridge, Trocadero, Haussmann ring, side blocks (static)
    mb = MB('city', R); Sy = SEINE
    K.seine(mb, M, 0.0, Sy[0], Sy[1], 22.0); K.bridge(mb, M, 0.0, Sy[2], Sy[0], Sy[1] + 10); K.trocadero(mb, M, (Sy[2] + 20, Sy[1] + 120, 0.0), 0.0, 1.4)
    mb.box(M['stone'], (0, Sy[0] - 12, 0.0), (3000, 3, 2.0))
    K.city_ring(mb, M, rnd(7), 0.0, 230.0, 900.0, [(-1000, 1000, Sy[0] - 30, Sy[1] + 400)], 36.0, 300.0)
    for i in range(-3, 4):
        for sgn in (-1, 1): K.haus(mb, M, sgn * (150.0 + 18 * (i % 2)), -60 + 33 * (i + 3) + 10, rr.uniform(22, 28), 26, rr.choice([18.0, 21.0, 24.0]), rr, True)
    mb.finish()
    # ---- trees along the Seine quay (plane trees) for scale/life
    mb = MB('trees', R)
    for i in range(14): K.plane_tree(mb, M, (-180 + i * 28, Sy[0] - 24, 0), 1.4, 20 + i)
    mb.finish()
    # ---- lights: forges (warm point lights)
    for i, (p, c_, e) in enumerate(lights): C.lamp('forge%d' % i, W(p), c_, e, 0.25, group='lamp')
    # ---- hidden shade casters + marks + staging
    _marks(A); _staging(A); _shade_casters(A, P)
    A['hooks'] = dict(set_stage=set_stage, crane_swing=crane_swing, spark=spark, rivet_toss=rivet_toss)
    set_stage(PRESETS[preset]['stage'])
    STATE['light_table'] = LIGHTS
    C.apply_P(P)
    A['cam_name'] = preset; A['cam'] = A['cams'][preset]
    STATE['A'] = A
    return A

# ------------------------------------------------------------------ hooks
def set_stage(s, frame=None):
    """site stage 0..3: 0 legs to 50 m + scaffolds + creeper cranes; 1 + first platform (57 m) and the second-stage stubs (to 90 m); 2 + second platform (115 m) and the upper stub (to 150 m); 3 finished spire.
    Visibility keys are CONSTANT (a snap)."""
    st = STATE['stage_objs']; cr = STATE['creep']
    for i, grp in enumerate(st): C.show(grp, i <= s, frame)
    for i, grp in enumerate(cr): C.show(grp, i == s, frame)
    C.show(STATE['scaff'], s <= 2, frame); STATE['stage'] = s

def crane_swing(k, frame=None):
    """the derrick (left, mast (-62,-88)) swings its hanging red-lead girder: k 0..1 -> yaw from the front-left to over the yard (rotation of the pivot at the mast head)"""
    p = STATE['swing']; p.rotation_euler = (0, 0, (k - 0.5) * 1.3)
    if frame is not None: C.key(p, 'rotation_euler', frame)

def _spark_objs():
    if STATE.get('spk'): return STATE['spk']
    import bmesh
    M = STATE['M']; R = C.root(); out = []; em = mat_emit('spark_h', '#ffcf60', 45.0); em2 = mat_emit('spark_c', '#fff0c0', 90.0)
    for i in range(14):                                         # short emissive streaks (thin stretched ellipsoids), oriented along their flight
        ob = bpy.data.objects.new('spk_%d' % i, bpy.data.meshes.new('spk_%d' % i)); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=4, radius=0.04, matrix=Matrix.Diagonal((1.0, 1.0, 3.6, 1.0))); bm.to_mesh(ob.data); bm.free()
        ob.data.materials.append(em2 if i % 3 == 0 else em); bpy.context.scene.collection.objects.link(ob); ob.parent = R; ob.visible_shadow = False; ob.hide_render = True; out.append(ob)
    STATE['spk'] = out; return out
def spark(frame=None, at=None, t0=None, period=9, strength=1.0):
    """hammer sparks at the rivet deck anvil (hook for site_rivet, world metres 'at' default = the deck anvil): fan of 14 short glowing streaks (6-12 px) that fly out and fall; the phase follows the frame
    (a hit every `period` frames, or one burst at frame t0). Key it on every rendered frame."""
    sp = _spark_objs(); at = Vector(at or STATE.get('spark_at', (-45.0, -62.0, 17.2))); rr = random.Random(3)
    f = 0 if frame is None else frame; ph = ((f - (t0 or 0)) % period) / float(period)
    t = ph * 0.9; on = strength > 0
    for i, ob in enumerate(sp):
        a = rr.uniform(0, 6.283); v = rr.uniform(1.6, 3.4); up = rr.uniform(0.8, 2.6)
        p = at + Vector((math.cos(a) * v * t, math.sin(a) * v * t * 0.5, up * t - 4.0 * t * t * 1.0)); vel = Vector((math.cos(a) * v, math.sin(a) * v * 0.5, up - 8.0 * t))
        ob.location = p; ob.rotation_euler = vel.to_track_quat('Z', 'Y').to_euler(); vis = on and (t < 0.8); ob.hide_render = not vis; ob.scale = (1 - t * 0.5,) * 3
        if frame is not None: C.key(ob, 'location', frame); C.key(ob, 'rotation_euler', frame); C.key(ob, 'hide_render', frame, 'CONSTANT'); C.key(ob, 'scale', frame)

def rivet_toss(k, frame=None):
    """glowing rivet (a small elongated cylinder, emission 60) in flight from the tongs mark (riveter_tongs) to the bucket mark (riveter_catch), k 0..1 (arc); None hides"""
    o = STATE.get('rivet')
    if o is None:
        import bmesh
        o = bpy.data.objects.new('toss_rivet', bpy.data.meshes.new('toss_rivet')); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.035, radius2=0.04, depth=0.15); bm.to_mesh(o.data); bm.free()
        o.data.materials.append(mat_emit('toss_hot', '#ff8a2a', 60.0)); bpy.context.scene.collection.objects.link(o); o.parent = C.root(); o.visible_shadow = False; STATE['rivet'] = o
    if k is None: C.setv(o, False, frame); return
    m = STATE['marks']; a = Vector(m['riveter_tongs']) / SC + Vector((0.5, 0, 2.3)); b = Vector(m['riveter_catch']) / SC + Vector((-0.4, 0, 1.7))
    p = a.lerp(b, k); p.z += 1.6 * 4 * k * (1 - k); o.location = p; C.setv(o, True, frame)
    d = (b - a); d.z += 1.6 * 4 * (1 - 2 * k); o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    if frame is not None: C.key(o, 'location', frame); C.key(o, 'rotation_euler', frame)

# ------------------------------------------------------------------ marks / staging / shade
def _m(x, y, z=0.0): return (x * SC, y * SC, z * SC)
def _marks(A):
    m = A['marks']
    lp = [leg_pt(z, dx) for z, dx in zip(LEG_ZS, LEG_DX)]
    m.update(eiffel_table=_m(50.7, -71.3), plan_table=_m(PLAN_TABLE[0], PLAN_TABLE[1]), eiffel_plan_a=_m(PLAN_TABLE[0], PLAN_TABLE[1], 0.95), eiffel_fence=_m(-1.5, -96.5), eiffel_leg=_m(-58.5, -70.5),
             lady_fence=_m(-8.0, -103.6), gent_fence=_m(-4.6, -103.2), child_fence=_m(-1.6, -103.0), gent2_fence=_m(1.8, -103.4),
             riveter_tongs=_m(-48.5, -63.6, 16.0), riveter_catch=_m(-45.3, -64.8, 16.0), riveter_hammer=_m(-46.8, -61.3, 16.0), forge_deck=_m(-44.6, -62.6, 16.0),
             worker_a=_m(-44.9, -161.4), worker_b=_m(-41.0, -160.6), worker_c=_m(-37.9, -164.2), worker_d=_m(-34.0, -161.8), worker_e=_m(-44.3, -157.9), worker_g=_m(-32.9, -166.4),
             worker_f=_m(-71.0, -33.0), worker_h=_m(-40.0, -150.0),
             leg_a=_m(lp[0][0], lp[0][1], lp[0][2] + 0.08), leg_b=_m(lp[1][0], lp[1][1], lp[1][2] + 0.08), leg_c=_m(lp[2][0], lp[2][1], lp[2][2] + 0.08),
             scaff_a=_m(-40.0, -57.0, 18.0), scaff_b=_m(-36.0, -60.0, 26.0), scaff_c=_m(-42.5, -54.0, 34.0), scaff_d=_m(-33.0, -52.0, 36.0),
             girder_carry_a=_m(GIRDER_CARRY[0][0], GIRDER_CARRY[0][1]), girder_carry_b=_m(GIRDER_CARRY[1][0], GIRDER_CARRY[1][1]), forge_a=_m(-20, -64), forge_b=_m(24, -62))
    A['marks_m'] = {k: tuple(v / SC for v in vv) for k, vv in m.items()}
def _staging(A):
    S = A['staging']
    S['site_wide'] = [('riveter_tongs', 'worker_a', dict(pose=dict(expr='working'))), ('riveter_hammer', 'worker_b'), ('riveter_forge', 'worker_c'), ('riveter_tongs', 'worker_d'), ('riveter_hammer', 'worker_e'), ('riveter_forge', 'worker_g')]
    S['site_wide_end'] = S['site_wide']
    S['site_table'] = [('eiffel', 'eiffel_table', dict(pose=dict(expr='proud', yaw=-0.5)))]
    S['site_leg_low'] = [('eiffel', 'eiffel_leg', dict(pose=dict(expr='proud', arm_r='up'))), ('riveter_hammer', 'leg_a'), ('riveter_tongs', 'leg_b'), ('riveter_forge', 'leg_c')]
    S['site_fence'] = [('eiffel', 'eiffel_fence', dict(pose=dict(expr='proud', yaw=-0.3))), ('lady20', 'lady_fence'), ('gent20', 'gent_fence'), ('child20', 'child_fence')]
    S['site_girders'] = [('riveter_tongs', 'girder_carry_a'), ('riveter_hammer', 'girder_carry_b'), ('riveter_forge', 'worker_g')]
    S['site_rivet'] = [('riveter_tongs', 'riveter_tongs'), ('riveter_hammer', 'riveter_catch'), ('riveter_forge', 'riveter_hammer')]
    for n in ('site_rise', 'site_rise_snap1', 'site_rise_snap2', 'site_rise_snap3'): S[n] = []
    STATE['staging'] = S
SHADE_ZONE = dict(site_wide=(13.5, 18.0, 9.0, 20.0), site_wide_end=(9.0, 16.0, 8.0, 18.0), site_table=(3.5, 9.0, 5.0, 14.0), site_leg_low=(3.0, 9.0, 5.0, 14.0), site_fence=(3.5, 9.0, 5.0, 14.0),
                  site_girders=(3.5, 9.0, 5.0, 14.0), site_rivet=(17.0, 16.0, 12.0, 22.0), site_rise=(50.0, 50.0, 30.0, 30.0), site_rise_snap1=(50.0, 50.0, 30.0, 30.0), site_rise_snap2=(70.0, 70.0, 40.0, 40.0), site_rise_snap3=(90.0, 90.0, 50.0, 50.0))
def _shade_casters(A, P):
    """invisible sun-blockers (shadow only, not seen by the camera) that put the foreground ground / props of the preset camera in cast shade (QA: the nearest 15 % of the frame in shade)."""
    sun = Vector(P['key_dir']).normalized(); M = STATE['M']; R = C.root(); mb = MB('shade_casters', R); cam = CAMS_M[A['preset']]
    def caster(c, w, d, hgt):
        off = Vector((-sun.x, -sun.y, 0)) * (hgt / -sun.z); mb.box(M['dark'], (c.x + off.x, c.y + off.y, c.z + hgt), (w, d, 0.2))
    loc, f, r, u = K.cam_basis(cam)
    z = SHADE_ZONE.get(A['preset'])
    if z:
        fh = Vector((f.x, f.y, 0)); fh.normalize(); caster(Vector((loc.x, loc.y, 0)) + fh * z[0], z[1], z[2], z[3])
    for o in mb.finish(): o.visible_camera = False

def build_shade_defaults():
    pass
