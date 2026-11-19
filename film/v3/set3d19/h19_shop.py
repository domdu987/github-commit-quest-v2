"""h19_shop.py : WORKSHOP of film 19 (Harrison's village workshop, Lincolnshire), grown from styleboard/part_shop.py.
Authored in METRES under the scaled root (D = 1.85 x m). Room x -2.3..2.3 (+x right), y -2.9 (front wall + door) .. 3.4 (back wall + window), height 2.9.
build_shop(SET, preset, light) fills SET: cams, marks, staging, cam_name, light; hooks: set_clock, set_balance, set_candles, set_door."""
import os, sys, math
import bpy
from mathutils import Vector, Matrix, Euler
import h19_kit as K
from h19_kit import MB, mat, mat_emit, metal_mat, rnd, W, hexc, gear, curl, sphere_brass, hang_saw, ring_xy, ring_xz, sun, area_light, point_light

X0, X1, Y0, Y1, ZH = -2.3, 2.3, -2.9, 3.4, 2.9
BZ = 0.9                       # bench top height
DOORX = (-0.75, 0.15)          # door opening in the front wall
WIN = (-1.55, -0.3, 0.9, 2.3)  # window x0 x1 z0 z1 (back wall)

CAMS_M = dict(
    shop_wide=((0.05, -2.3, 1.32), (0.0, 3.4, 0.95)),
    shop_bench=((1.25, -0.6, 1.2), (1.35, 2.5, 1.2)),
    shop_clock=((1.15, 0.45, 1.3), (1.25, 1.9, 1.1)),
    shop_door=((0.75, 0.2, 1.3), (-0.15, -2.9, 1.15)),
)
CAM_NOTES = dict(
    shop_wide='sb1 framing: the room with the bench, the hero clock, the window shaft, the lathe; tool chest + offcut basket + half-built case + stump low in the frame',
    shop_bench='medium on the bench and the hero clock, low-ish; plane, mallet, shavings in FG; Harrison behind the bench at the right',
    shop_clock='closer 3/4 on the clock on the bench, Harrison behind it (set_clock([1,4]) = H1 + H4 side by side)',
    shop_door='from the middle of the room toward the front door (mocker visiting): door ajar, daylight spill, shelves and tools on the front wall',
)
STAGING = dict(
    shop_wide=[('harrison', 'harrison_lathe'), ('william', 'william_bench')],
    shop_bench=[('harrison', 'harrison_bench')],
    shop_clock=[('harrison', 'harrison_bench')],
    shop_door=[('mocker', 'visitor_a'), ('astro', 'visitor_b')],
)
MARKS_M = dict(harrison_bench=(1.8, 2.75, 0.0), harrison_lathe=(-1.1, 1.5, 0.0), harrison_window=(-0.9, 2.75, 0.0), door=(-0.3, -2.7, 0.0),
               visitor_a=(-0.35, -1.7, 0.0), visitor_b=(0.55, -1.55, 0.0), william_bench=(0.55, 2.75, 0.0))

LIGHTS = dict(
    DAY=dict(key=(1.0, 0.86, 0.66, 36.0), az=-46, el=19, sun_angle=1.0, exposure=0.75, sat=1.08, fill=1.35, win=1.0, warm=0.4, candle=0.5, door=0.3,
             pane=('#a8c8f4', 0.95), hedge=('#4e7a58', 0.45), roof=('#b86a4a', 0.55), out=('#fff0d0', 0.85), outg=('#6e9a58', 0.8), moon=0.0),
    NIGHT=dict(key=(0.42, 0.52, 1.0, 40.0), az=-30, el=34, sun_angle=1.5, exposure=0.3, sat=1.04, fill=0.08, win=0.6, warm=0.0, candle=0.7, door=0.05,
               pane=('#3a4a9a', 0.55), hedge=('#1e2c4a', 0.25), roof=('#2a3050', 0.3), out=('#26306a', 0.5), outg=('#1a2444', 0.4), moon=1.0),
)

def shop_mats():
    M = {}
    M['plaster'] = mat('plaster', '#9a7a66', '#aa8a72', scale=1.6, contrast=1.2, zgrad=(0.0, 0.6, '#5c4650'))        # dusty lime plaster (ochre-grey, never orange): the warm practicals make it warm, the violet fill keeps it from going monochrome
    M['floor'] = mat('floor', '#7a5a3c', '#6a4c32', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('floor2', '#624632', '#725238', scale=2.2, aniso=(0.5, 0.12, 1))
    M['walnut'] = mat('walnut', '#6b4a2e', '#7a5636', scale=5, aniso=(0.15, 1, 1), contrast=1.2)
    M['gap'] = mat('gap', '#2a1a22')
    M['beam'] = mat('beam', '#46301f', '#5a3a26', scale=2.0, aniso=(0.1, 1, 1))
    M['honey'] = mat('honey', '#c28b3e', '#aa7430', scale=5, aniso=(0.15, 1, 1), contrast=1.3)
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['oakd'] = mat('oakd', '#5d3a20', '#72482a', scale=5, aniso=(0.2, 1, 1))
    M['bark'] = mat('bark', '#4a3220', '#6a4a30', scale=14, aniso=(1, 1, 0.12), contrast=1.6)
    M['ring'] = mat('ring', '#c79a58', '#d8ae6c', scale=9, contrast=1.3)
    M['gearw'] = mat('gearw', '#b98240', '#a06c30', scale=8, contrast=1.3)
    M['iron'] = metal_mat('iron', '#3a3430', '#4a4038', rough=0.6, spec=0.15)       # warm iron-grey (never blue)
    M['steel'] = mat('steel', '#3e3028', '#4c3c30', scale=8)               # warm iron (#3a3430 family): no blue-grey bars
    M['brass'] = metal_mat('brass', '#b8923a', '#d6b050', rough=0.4, spec=0.6, metallic=0.78)
    M['brassd'] = metal_mat('brassd', '#8a6424', '#a8802e', rough=0.45, spec=0.5, metallic=0.55)        # rims never go black: part diffuse brass
    M['silver'] = metal_mat('silver', '#b8bcc4', '#d4d8de', rough=0.26, spec=0.8, metallic=1.0)
    M['terra'] = mat('terra', '#b5532c', '#c9683a', scale=4)
    M['cloth'] = mat('cloth', '#a98354', '#bd9560', scale=7)
    M['sack'] = mat('sack', '#c4a66a', '#a88a52', scale=9)
    M['cream'] = mat('cream', '#e8d6aa', '#f0e0b8', scale=5)
    M['face'] = mat('face', '#efe2bc', '#e6d6a8', scale=5, emit='#efe2bc', emit_k=0.25)
    M['tick'] = mat('tick', '#2a1c20')
    M['red'] = mat('red', '#8a2630', '#a23238', scale=6)
    M['redcloth'] = mat('redcloth', '#a02a34', '#bb3a3e', scale=14, contrast=1.4)
    M['green'] = mat('green', '#5e7a3a', '#748c44', scale=6)
    M['dark'] = mat('dark', '#2a1a14', '#3a2a1e', scale=4); M['coat'] = mat('coat', '#5a4a3a', '#6a5646', scale=6); M['leather'] = mat('leather', '#6a4228', '#7a5030', scale=8)
    M['shav'] = mat('shav', '#d9a85a', '#c8924a', scale=8)
    M['stone'] = mat('stone', '#8a6e56', '#9c8066', scale=6)
    M['grey'] = mat('grey', '#9aa0b0')
    M['wick'] = mat('wick', '#2a2020')
    M['rug1'] = mat('rug1', '#7a4232', '#86503a', scale=14); M['rug2'] = mat('rug2', '#9a7c4c', '#a68858', scale=14); M['rug3'] = mat('rug3', '#4a5a38', '#566a40', scale=14); M['rug4'] = mat('rug4', '#b8a47c', '#a89468', scale=14)
    M['rugg'] = mat('rugg', '#7c6c58', '#8a7a64', scale=14); M['rugd'] = mat('rugd', '#5c4a3a', '#6a5646', scale=14)
    M['brassm'] = metal_mat('brassm', '#cb9f48', '#dcb25a', rough=0.24, spec=0.8, metallic=0.88); M['ceilp'] = mat('ceilp', '#6a5244', '#7a6050', scale=1.4, contrast=1.2)
    M['flame'] = mat_emit('flame', '#ffc860', 28.0)
    M['lampg'] = mat_emit('lampg', '#e89a48', 0.6)
    return M

def box_wall(mb, m, x0, x1, y0, y1, z0, z1): mb.box(m, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0))

def pivot(name, parent, loc, rot=(0, 0, 0), scale=1.0):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.parent = parent; e.location = loc; e.rotation_euler = rot; e.scale = (scale,) * 3; return e

def gear_obj(name, parent, m, c, r, **kw):
    """one gear as its own object under a pivot empty (turns about local y)"""
    pv = pivot(name, parent, c); mb = MB(name); gear(mb, m, (0, 0, 0), r, **kw); mb.finish(parent=pv); return pv

# ----------------------------------------------------------------------------- the four clocks
def clock_h1(M, par, big=1.0, tall=0.0, gold2=False):
    """H1: big brass frame (4 corner posts, rails), exposed brass gear wheels, two crossed dumbbell bars with 4 balls on top. Local origin = base centre on the bench."""
    hw, hd, hh = 0.86, 0.5, 0.42 + tall; mb = MB('h1'); G = []
    B, BD = M['brass'], M['brassd']
    for dx in (-hw / 2, hw / 2):
        for dy in (-hd / 2, hd / 2): mb.box(B, (dx, dy, hh / 2 + 0.05), (0.05, 0.05, hh))
    for z in (0.05, hh + .05):
        for dy in (-hd / 2, hd / 2): mb.box(B, (0, dy, z), (hw + 0.05, 0.045, 0.045))
        for dx in (-hw / 2, hw / 2): mb.box(B, (dx, 0, z), (0.045, hd, 0.045))
    mb.box(M['honey'], (0, 0, 0.02), (hw + 0.12, hd + 0.12, 0.04))
    for dx in (-hw / 2 - 0.02, hw / 2 + 0.02): mb.cyl(M['brassd'], (dx, -hd / 2 - 0.02, 0.07), 0.035, 0.04, seg=10)
    mb.box(BD, (0, 0, hh + .08), (hw, hd, 0.02))
    mb.box(BD, (0, -0.12, 0.28 + tall / 2), (hw - .08, 0.02, hh - .1)); mb.box(BD, (0, 0.12, 0.28 + tall / 2), (hw - .08, 0.02, hh - .1))
    mb.rod(BD, (-0.3, -0.2, 0.3), (0.3, -0.2, 0.3), 0.008, 0.008, 6); mb.rod(B, (0, -0.19, 0.12), (0, -0.19, hh), 0.006, 0.006, 6)
    mb.finish(parent=par)
    specs = [(-0.22, 0.30, 0.15, 20, 0.5), (0.05, 0.25, 0.11, 16, -0.9), (0.26, 0.31, 0.12, 16, 0.8), (-0.02, 0.38 + tall * 0.6, 0.065, 10, -1.6), (0.33, 0.18, 0.06, 10, 1.7), (-0.33, 0.15, 0.07, 10, -1.5)]
    for i, (dx, dz, r, nt, sp) in enumerate(specs):
        pv = gear_obj('h1gear%d' % i, par, B if i % 3 else BD, (dx, -0.19 - 0.045 * (0, 1, 0, 2, 1, 1)[i], dz), r, nt=nt, th=0.035, rim=0.024, tooth=0.026, hub=0.027, n=14); G.append((pv, sp))
    zt = hh + 0.22; bars = []
    pc = pivot('h1balance', par, (0, 0, zt)); bars.append(pc)
    for sgn, zz in ((1, 0.0), (-1, 0.07)):
        pv = pivot('h1bar%d' % sgn, pc, (0, 0, zz), rot=(0, 0, sgn * math.radians(33))); mb = MB('h1b'); L = 0.42
        mb.rod(BD, (-L, 0, 0), (L, 0, 0), 0.017, 0.017, 8, True, True)
        for e in (-1, 1): sphere_brass(mb, B, (e * L, 0, 0), 0.095)
        mb.finish(parent=pv); bars.append(pv)
    mb = MB('h1p'); mb.rod(B, (0, 0, hh + .09 - zt), (0, 0, 0.1), 0.02, 0.02, 8); mb.ell(B, (0, 0, 0.1), (0.04, 0.04, 0.04), (10, 8)); mb.finish(parent=pc)
    for dx in (-0.3, 0.3):
        mb = MB('h1s'); mb.rod(B, (dx, -0.1, hh + .09), (dx * .3, 0, zt - 0.02), 0.008, 0.008, 6); mb.finish(parent=par)
    return dict(gears=G, bars=bars)

def clock_h3(M, par):
    """H3: compact brass box with a window onto gears and two big round balance wheels (rings with spokes) on top"""
    B, BD = M['brassm'], M['brassd']; mb = MB('h3'); w, d, h = 0.5, 0.36, 0.34
    mb.box(M['honey'], (0, 0, 0.02), (w + 0.1, d + 0.1, 0.04)); mb.box(B, (0, 0, 0.04 + h / 2), (w, d, h)); mb.box(BD, (0, -d / 2 - 0.004, 0.04 + h / 2), (w - 0.1, 0.01, h - 0.1))
    for dx in (-w / 2, w / 2):
        for dy in (-d / 2, d / 2): mb.box(BD, (dx, dy, 0.04 + h / 2), (0.03, 0.03, h + 0.02))
    mb.box(BD, (0, 0, 0.04 + h + 0.01), (w + 0.04, d + 0.04, 0.02)); mb.box(M['brassd'], (0, -d / 2 - 0.012, 0.04 + h / 2), (w - 0.18, 0.006, h - 0.18))
    for dx in (-w / 2 + 0.03, w / 2 - 0.03): mb.cyl(M['brassd'], (dx, -d / 2 - 0.03, 0.06), 0.03, 0.04, seg=10)
    mb.finish(parent=par); G = []
    for i, (dx, dz, r, nt, sp) in enumerate([(-0.1, 0.2, 0.07, 12, 0.9), (0.06, 0.22, 0.09, 14, -0.7), (0.16, 0.14, 0.05, 8, 1.4)]):
        G.append((gear_obj('h3gear%d' % i, par, B, (dx, -d / 2 - 0.02 - 0.025 * (0, 1, 0)[i], dz), r, nt=nt, th=0.02, rim=0.014, tooth=0.016, hub=0.016, n=12), sp))
    bars = []
    for sgn, x in ((1, -0.13), (-1, 0.13)):
        mount = pivot('h3mount%d' % sgn, par, (x * 1.45, 0.03 * sgn,  0.04 + h + 0.02 + 0.16), rot=(math.pi / 2, 0, 0)); pv = pivot('h3bal%d' % sgn, mount, (0, 0, 0)); mb = MB('h3b'); r = 0.155      # rings stand upright facing the camera; the balance turns in its own plane
        for k in range(20):
            a = 2 * math.pi * (k + .5) / 20; mb.box(B, (r * math.cos(a), r * math.sin(a), 0), (2 * math.pi * r / 20 * 1.12, 0.034, 0.038), rz=a + math.pi / 2)
        for k in range(3): mb.box(B, (0, 0, 0), (2 * r, 0.018, 0.022), rz=math.pi * k / 3)
        mb.cyl(B, (0, 0, 0), 0.02, 0.05, seg=10); mb.cyl(B, (0, 0, -0.04), 0.008, 0.08, seg=6)
        for k in range(4):
            a = math.pi / 2 * k; sphere_brass(mb, B, (r * math.cos(a), r * math.sin(a), 0.0), 0.03)
        mb.finish(parent=pv); bars.append((pv, sgn))
    return dict(gears=G, bars=[b for b, _ in bars], balsgn=[s for _, s in bars])

def watch_h4(M, par):
    """H4: silver watch ~13 cm across lying on a red cloth, open face with tick marks and two hands, NO numerals"""
    mb = MB('h4'); r = 0.065
    mb.box(M['oakd'], (0, 0.05, -0.03), (0.2, 0.15, 0.05), rx=-H4_TILT)           # a closed ledger wedges the cloth up toward the lens
    mb.box(M['redcloth'], (0, 0, 0.007), (0.26, 0.21, 0.014), rz=0.12); mb.box(M['redcloth'], (-0.05, 0.02, 0.016), (0.14, 0.12, 0.012), rz=-0.5); mb.box(M['redcloth'], (0.07, -0.03, 0.017), (0.10, 0.08, 0.01), rz=0.9)
    z0 = 0.028
    mb.cyl(M['silver'], (0, 0, z0), r, 0.02, seg=40, smooth=True); mb.cyl(M['face'], (0, 0, z0 + 0.0115), r - 0.007, 0.003, seg=40)
    ring_xy(mb, M['silver'], (0, 0, z0 + 0.012), r - 0.002, 0.006, 0.012, 36)
    for k in range(60):
        a = 2 * math.pi * k / 60; big = k % 5 == 0; rr_ = r - 0.014 if big else r - 0.011; ln = 0.012 if big else 0.005; wd = 0.003 if big else 0.0015
        mb.box(M['tick'], (rr_ * math.sin(a), rr_ * math.cos(a), z0 + 0.0135), (wd, ln, 0.002), rz=-a)
    ha = math.radians(-60); hb = math.radians(40)       # hour hand ~10, minute hand ~ 8: about ten past ten
    for a, ln, wd in ((math.radians(305), 0.032, 0.0055), (math.radians(60), 0.046, 0.0035)):
        mb.box(M['tick'], (0.5 * ln * math.sin(a), 0.5 * ln * math.cos(a), z0 + 0.0145), (wd, ln, 0.002), rz=-a)
    mb.cyl(M['brass'], (0, 0, z0 + 0.0155), 0.005, 0.004, seg=10)
    mb.cyl(M['silver'], (0, r + 0.012, z0), 0.007, 0.016, axis='y', seg=10)                  # crown
    ring_xz(mb, M['silver'], (0, r + 0.02, z0 + 0.0), 0.016, 0.004, 0.006, 12)               # bow
    mb.finish(parent=par)
    return dict(gears=[], bars=[])

CLOCK_BUILD = {1: ('h1', lambda M, p: clock_h1(M, p)), 2: ('h2', lambda M, p: clock_h1(M, p, tall=0.13)), 3: ('h3', clock_h3), 4: ('h4', watch_h4)}
CLOCK_SCALE = {1: 1.22, 2: 1.18, 3: 1.35, 4: 2.3}           # H4 is a hero prop: 2.3 x (about 30 cm) so it reads at 150+ px in shop_clock; tilted toward the lens on a folded cloth
H4_TILT = 0.75
CLOCK_SLOTS = {1: [(1.2, 1.88)], 2: [(0.9, 1.84), (1.78, 1.88)], 3: [(0.8, 1.84), (1.3, 1.88), (1.8, 1.88)]}


# ----------------------------------------------------------------------------- the world outside the front door: yard, path, fence, trees in depth, hills, sky (self-lit, day / night switch = apply_light)
def ext_mat(SET, name, day, night, scale=1.0, aniso=(1, 1, 1), contrast=1.0, grad=None):
    """self-lit two-tone noise material; day / night colour pair + strength switched by the Value node 'dn' (apply_light). grad=(z0, z1) makes it a vertical gradient (sky): A at z0 -> B at z1"""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tc = N('ShaderNodeTexCoord'); dn = N('ShaderNodeValue'); dn.name = 'dn'; dn.outputs[0].default_value = 0.0
    if grad:
        sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0]); mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = grad[0]; mr.inputs['From Max'].default_value = grad[1]; mr.clamp = True; L(sp.outputs['Z'], mr.inputs['Value']); fac = mr.outputs[0]
    else:
        mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale * aniso[0], scale * aniso[1], scale * aniso[2]); L(tc.outputs['Object'], mp.inputs['Vector'])
        nz = N('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 4; nz.inputs['Roughness'].default_value = 0.6; L(mp.outputs[0], nz.inputs['Vector'])
        cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.5 - 0.2 / contrast; cr.color_ramp.elements[1].position = 0.5 + 0.2 / contrast; L(nz.outputs['Fac'], cr.inputs['Fac']); fac = cr.outputs[0]
    cols = []
    for (A_, B_, k_) in (day, night):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(A_); mx.inputs[7].default_value = hexc(B_); L(fac, mx.inputs[0]); cols.append(mx.outputs[2])
    mf = N('ShaderNodeMix'); mf.data_type = 'RGBA'; L(dn.outputs[0], mf.inputs[0]); L(cols[0], mf.inputs[6]); L(cols[1], mf.inputs[7])
    ks = N('ShaderNodeMix'); ks.data_type = 'FLOAT'; L(dn.outputs[0], ks.inputs[0]); ks.inputs[2].default_value = day[2]; ks.inputs[3].default_value = night[2]
    L(mf.outputs[2], em.inputs['Color']); L(ks.outputs[0], em.inputs['Strength']); L(em.outputs[0], out.inputs['Surface'])
    SET.setdefault('ext_mats', []).append(m); return m

def build_exterior(SET, light):
    """what the door (and the front-wall window) look onto: a dirt path, a rail fence with an open gate, hedge + bushes, trees in three depth layers, a hazy far hill, a gradient sky. Self-lit (the room walls shade the real sun)."""
    X = MB('outside'); E = lambda n, d, nn, **kw: ext_mat(SET, n, d, nn, **kw); rr = rnd(77)
    grass = E('x_grass', ('#6e9a4c', '#84ac5a', 0.62), ('#1c2a3c', '#26364a', 0.42), scale=0.8, contrast=1.4)
    path = E('x_path', ('#c2ab80', '#b09870', 0.7), ('#3a4258', '#48526c', 0.7), scale=3.0, contrast=1.6)
    wood = E('x_wood', ('#86705a', '#745e48', 0.62), ('#2a3048', '#363e5a', 0.6), scale=6.0, aniso=(1, 1, 0.15))
    bush = E('x_bush', ('#3f6e3c', '#52844a', 0.55), ('#12202e', '#1a2c3c', 0.34), scale=3.0, contrast=1.3)
    tree1 = E('x_tree1', ('#3a6838', '#4c7c44', 0.55), ('#101e2c', '#182a3a', 0.34), scale=1.6, contrast=1.5)
    tree2 = E('x_tree2', ('#4e7e48', '#62925a', 0.6), ('#16263a', '#1e3246', 0.36), scale=1.4, contrast=1.5)
    tree3 = E('x_tree3', ('#7aa078', '#8cb088', 0.75), ('#20304c', '#283a58', 0.4), scale=1.0, contrast=1.3)
    bark = E('x_bark', ('#5e4a38', '#4a382a', 0.5), ('#1c2434', '#262e42', 0.32), scale=8.0, aniso=(1, 1, 0.2))
    hill = E('x_hill', ('#97b496', '#a8c4a4', 0.82), ('#26345a', '#303e66', 0.42), scale=0.12, contrast=1.2)
    sky = E('x_sky', ('#dce8e6', '#74a6e0', 1.05), ('#34427a', '#121a42', 0.6), grad=(8.0, 55.0))
    Yf = Y0 - 3.7                                                                                      # fence line, 3.7 m outside the front wall
    X.quad(sky, [(-90, -72, -4), (90, -72, -4), (90, -72, 70), (-90, -72, 70)][::-1])
    for (hx, hy, rx_, rz_) in [(-30, -58, 26, 7.5), (6, -61, 30, 10), (40, -57, 20, 6.5), (-62, -60, 18, 8)]: X.ell(hill, (hx, hy, -0.5), (rx_, 1.0, rz_), (24, 10))
    X.quad(grass, [(-90, Y0 - 0.02, -0.07), (90, Y0 - 0.02, -0.07), (90, -70, -0.07), (-90, -70, -0.07)][::-1])
    X.quad(path, [(DOORX[0] - 0.25, Y0 - 0.02, -0.055), (DOORX[1] + 0.2, Y0 - 0.02, -0.055), (DOORX[1] + 0.5, -26, -0.055), (DOORX[0] - 0.7, -26, -0.055)][::-1])
    # hedge row + far field edge, then fence
    X.box(bush, (0, -26, 0.9), (90, 1.6, 1.8)); X.box(tree3, (0, -34, 2.2), (90, 2.0, 4.4))
    gate0, gate1 = DOORX[0] - 0.55, DOORX[1] + 0.35
    xs = [x for x in [-9 + 0.85 * i for i in range(0, 18)] if not (gate0 - 0.3 < x < gate1 + 0.3)]
    for x in xs: X.box(wood, (x, Yf, 0.58), (0.09, 0.09, 1.16))
    for (a_, b_) in ((-9.0, gate0), (gate1, 5.5)):
        for z in (0.38, 0.86): X.box(wood, ((a_ + b_) / 2, Yf + 0.05, z), (b_ - a_, 0.04, 0.09))
    for x in (gate0, gate1): X.box(wood, (x, Yf, 0.7), (0.14, 0.14, 1.4))
    gl_ = gate1 - gate0 - 0.2                                                             # the gate stands open, swung out on its hinge post
    for z in (0.3, 0.62, 0.94): X.box(wood, (gate0 + 0.12, Yf - gl_ / 2, z), (0.05, gl_, 0.07))
    X.box(wood, (gate0 + 0.12, Yf - gl_ / 2, 0.62), (0.05, 0.06, 0.74)); X.box(wood, (gate0 + 0.12, Yf - gl_ + 0.06, 0.62), (0.05, 0.06, 0.74))
    for (bx_, bw_, bh_) in [(-3.4, 1.6, 0.8), (-1.9, 1.2, 0.6), (1.8, 1.7, 0.85), (3.5, 1.3, 0.7), (-6.5, 1.8, 0.9)]: X.ell(bush, (bx_, Yf - 0.6, bh_ * 0.45), (bw_, 0.7, bh_), (14, 8))
    # trees: (x, y, trunk height, canopy radius, canopy material, trunk radius)
    for (tx, ty, th, tr, tm, rad) in [(-3.4, -12.5, 3.2, 2.5, tree1, 0.3), (-1.3, -10.2, 2.4, 1.8, tree2, 0.22), (1.9, -13.5, 3.8, 2.8, tree1, 0.34), (-6.8, -14.0, 3.4, 2.6, tree2, 0.3), (4.8, -10.5, 2.8, 2.0, tree2, 0.26),
                                      (-9.5, -11.0, 3.0, 2.2, tree1, 0.28), (-4.6, -19.0, 4.2, 3.2, tree3, 0.36), (0.4, -21.0, 4.6, 3.6, tree3, 0.4), (6.5, -18.5, 4.0, 3.0, tree3, 0.34), (-1.4, -9.0, 1.9, 1.3, tree1, 0.18)]:
        X.rod(bark, (tx, ty, 0.0), (tx, ty, th), rad * 1.25, rad * 0.8, 8, True, True)
        for k in range(5):
            a_ = k * 1.26 + tx; X.ell(tm, (tx + 0.55 * tr * math.cos(a_) * (k > 0), ty + 0.4 * tr * math.sin(a_) * (k > 0), th + tr * (0.55 if k == 0 else 0.4 + 0.18 * (k % 2))), (tr * (0.8 if k else 1.0), tr * (0.8 if k else 1.0), tr * (0.7 if k else 0.85)), (12, 8))
    X.finish(shadow=False)
    moon = MB('outside_moon'); moon.ell(mat_emit('x_moon', '#e8eeff', 3.0), (-9, -70.5, 36), (3.2, 0.3, 3.2), (16, 10)); mo = moon.finish(shadow=False)[0]; SET['ext_moon'] = mo
    # a hay cart and a milk churn by the gate: something to read in the yard
    cm = MB('outside_props')
    cm.box(wood, (3.2, Yf + 1.6, 0.55), (1.8, 1.0, 0.12)); cm.box(wood, (3.2, Yf + 1.1, 0.8), (1.8, 0.06, 0.5)); cm.box(wood, (3.2, Yf + 2.1, 0.8), (1.8, 0.06, 0.5)); cm.cyl(wood, (2.6, Yf + 1.6, 0.4), 0.4, 0.08, axis='y', seg=14); cm.cyl(wood, (3.8, Yf + 1.6, 0.4), 0.4, 0.08, axis='y', seg=14)
    cm.ell(path, (3.2, Yf + 1.6, 1.0), (0.85, 0.45, 0.4), (10, 6)); cm.cyl(bush, (-1.9, Yf + 0.9, 0.3), 0.18, 0.6, seg=10)
    cm.finish(shadow=False)

# ----------------------------------------------------------------------------- build
def build_shop(SET, preset, light):
    root = K.new_root(); M = shop_mats(); SET['M'] = M; rr = rnd(19); PL = LIGHTS[light]; SET['caption_shade'] = None  # director: no bottom darkening card (new effect, not approved)
    K.flat_world('#7a82ff', 0.0, env=('#ffd6a0', 0.9)); SET['samples'] = 8; SET['dbounce'] = 0
    mb = MB('shop'); fl = []
    # ---- shell
    for i in range(23):
        x = X0 + 0.21 * i + 0.105
        mb.box(M['floor'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.2, Y1 - Y0, 0.06))
    mb.box(M['gap'], (0, (Y0 + Y1) / 2, -0.07), (X1 - X0 + .3, Y1 - Y0 + .3, 0.05))
    wx0, wx1, wz0, wz1 = WIN
    box_wall(mb, M['plaster'], X0 - .2, wx0, Y1, Y1 + .32, 0, ZH); box_wall(mb, M['plaster'], wx1, X1 + .2, Y1, Y1 + .32, 0, ZH)
    box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, 0, wz0); box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, wz1, ZH)
    box_wall(mb, M['plaster'], X0 - .3, X0, Y0, Y1 + .3, 0, ZH); box_wall(mb, M['plaster'], X1, X1 + .3, Y0, Y1 + .3, 0, ZH)
    box_wall(mb, M['plaster'], X0 - .3, DOORX[0], Y0 - .3, Y0, 0, ZH); FW = (1.3, 2.1, 0.95, 1.95)                                       # small window in the front wall (x0 x1 z0 z1), looks onto the yard
    box_wall(mb, M['plaster'], DOORX[1], FW[0], Y0 - .3, Y0, 0, ZH); box_wall(mb, M['plaster'], FW[1], X1 + .3, Y0 - .3, Y0, 0, ZH); box_wall(mb, M['plaster'], FW[0], FW[1], Y0 - .3, Y0, 0, FW[2]); box_wall(mb, M['plaster'], FW[0], FW[1], Y0 - .3, Y0, FW[3], ZH)
    box_wall(mb, M['plaster'], DOORX[0], DOORX[1], Y0 - .3, Y0, 2.1, ZH); box_wall(mb, M['ceilp'], X0 - .3, X1 + .3, Y0, Y1 + .3, ZH, ZH + .3)
    # timber frame
    for x in (-2.2, 2.2): mb.box(M['beam'], (x, Y1 - 0.06, ZH / 2), (0.2, 0.14, ZH))
    mb.box(M['beam'], (0, Y1 - 0.06, 0.12), (4.6, 0.14, 0.24)); mb.box(M['beam'], (0, Y1 - 0.06, ZH - 0.12), (4.6, 0.14, 0.24))
    mb.box(M['beam'], (0.85, Y1 - 0.06, 1.62), (2.8, 0.1, 0.13))
    for y in (-1.8, -0.3, 1.2, 2.7): mb.box(M['beam'], (0, y, ZH - 0.14), (4.6, 0.24, 0.28))
    for x in (-1.2, 1.2): mb.box(M['beam'], (x, 0.5, ZH - 0.05), (0.14, 6.2, 0.14))
    for x in (X0 + 0.06, X1 - 0.06): mb.box(M['beam'], (x, 0.25, ZH - 0.2), (0.14, 6.0, 0.3)); mb.box(M['beam'], (x, 0.25, 0.1), (0.14, 6.0, 0.2))
    # front wall timbers + door frame
    mb.box(M['beam'], (0, Y0 + 0.06, 0.12), (4.6, 0.14, 0.24)); mb.box(M['beam'], (0, Y0 + 0.06, ZH - 0.12), (4.6, 0.14, 0.24))
    for x in (-2.2, 2.2): mb.box(M['beam'], (x, Y0 + 0.06, ZH / 2), (0.2, 0.14, ZH))
    for x in (DOORX[0] - 0.05, DOORX[1] + 0.05): mb.box(M['oakd'], (x, Y0 + 0.05, 1.07), (0.12, 0.2, 2.2))
    mb.box(M['oakd'], ((DOORX[0] + DOORX[1]) / 2, Y0 + 0.05, 2.16), (DOORX[1] - DOORX[0] + 0.3, 0.2, 0.14)); mb.box(M['stone'], ((DOORX[0] + DOORX[1]) / 2, Y0 - 0.02, 0.025), (DOORX[1] - DOORX[0] + 0.1, 0.5, 0.05))
    mb.box(M['beam'], (1.4, Y0 + 0.06, 1.62), (1.8, 0.1, 0.13)); mb.box(M['beam'], (-1.5, Y0 + 0.06, 1.62), (1.4, 0.1, 0.13))
    # ---- window: reveal, mullions, sill, shutter
    gl = MB('glass'); sky_m = mat_emit('sky_pane', PL['pane'][0], PL['pane'][1]); hedge_m = mat_emit('hedge_pane', PL['hedge'][0], PL['hedge'][1]); roof_m = mat_emit('roof_pane', PL['roof'][0], PL['roof'][1])
    gl.quad(sky_m, [(wx0, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz1), (wx0, Y1 + 0.5, wz1)][::-1])
    gl.quad(hedge_m, [(wx0, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0 + 0.5), (wx0, Y1 + 0.49, wz0 + 0.5)][::-1])
    gl.quad(roof_m, [(wx0 + .55, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.7), (wx0 + .55, Y1 + 0.48, wz0 + 0.7)][::-1])
    if light == 'NIGHT':                                              # a few stars + a pale moon in the night pane
        mm = mat_emit('moon_pane', '#d8e0ff', 3.0); gl.ell(mm, (wx0 + 0.3, Y1 + 0.47, wz1 - 0.3), (0.09, 0.01, 0.09), (14, 10))
        for k in range(14): gl.ell(mat_emit('star_pane', '#c8d0ff', 2.2), (rr.uniform(wx0 + .1, wx1 - .1), Y1 + 0.47, rr.uniform(wz0 + 0.6, wz1 - .1)), (0.008, 0.005, 0.008), (5, 4))
    gl.finish(shadow=False)
    ym = Y1 + 0.12
    for k in range(5): mb.box(M['oakd'], (wx0 + k * (wx1 - wx0) / 4, ym, (wz0 + wz1) / 2), (0.03, 0.05, wz1 - wz0))
    for k in range(6): mb.box(M['oakd'], ((wx0 + wx1) / 2, ym, wz0 + k * (wz1 - wz0) / 5), (wx1 - wx0, 0.05, 0.03))
    for x in (wx0 - 0.04, wx1 + 0.04): mb.box(M['oakd'], (x, ym, (wz0 + wz1) / 2), (0.08, 0.14, wz1 - wz0 + .1))
    mb.box(M['oak'], ((wx0 + wx1) / 2, Y1 - 0.12, wz0 - 0.03), (wx1 - wx0 + .3, 0.34, 0.07))
    mb.box(M['oakd'], (wx0 - 0.28, Y1 - 0.14, (wz0 + wz1) / 2), (0.34, 0.04, wz1 - wz0 - .02), rz=0.5)
    # sill clutter: a candle stub in a brass stick, two small jars, a pot of herbs
    for (x, r_, h_, cm) in [(wx0 + 0.25, 0.04, 0.1, 'terra'), (wx0 + 0.4, 0.03, 0.07, 'cream')]: mb.cyl(M[cm], (x, Y1 - 0.14, wz0 + 0.035 + h_ / 2), r_, h_, seg=10)
    mb.cyl(M['terra'], (wx1 - 0.2, Y1 - 0.14, wz0 + 0.08), 0.06, 0.1, seg=12, r2=0.075)
    for k in range(6): mb.rod(M['green'], (wx1 - 0.2, Y1 - 0.14, wz0 + 0.13), (wx1 - 0.2 + 0.05 * math.cos(k * 1.05), Y1 - 0.14 + 0.05 * math.sin(k * 1.05), wz0 + 0.28), 0.004, 0.012, 4)
    # ---- front door: leaf swung inward, hinge at DOORX[0]; strap hinges, latch; daylight beyond
    dl = MB('doorleaf'); hx_ = DOORX[0] + 0.04; hy_ = Y0 + 0.08; lw = DOORX[1] - DOORX[0] - 0.08
    ang = math.radians(78)
    dl.push(Matrix.Translation((hx_, hy_, 0)) @ Euler((0, 0, ang)).to_matrix().to_4x4())
    for k in range(6): dl.box(M['oak'] if k % 2 else M['oakd'], (0.0 + lw * (k + .5) / 6 * 0 + 0, 0, 0), (0, 0, 0)) if False else None
    for k in range(6): dl.box(M['oak'] if k % 2 else M['oakd'], (lw * (k + .5) / 6, 0, 1.04), (lw / 6 - 0.004, 0.05, 2.08))
    for z in (0.3, 1.0, 1.75): dl.box(M['iron'], (lw / 2, -0.03, z), (lw, 0.012, 0.09)); dl.cyl(M['iron'], (lw - 0.05, -0.036, z), 0.016, 0.01, axis='y', seg=8)
    dl.box(M['iron'], (lw - 0.08, -0.04, 1.0), (0.14, 0.015, 0.025)); dl.finish(shadow=True); dl.pop()
    build_exterior(SET, light)
    # ---- longcase clock (back-left corner), visible wooden movement
    cx, cy = -1.95, 3.0
    mb.box(M['oakd'], (cx, cy, 0.07), (0.56, 0.34, 0.14)); mb.box(M['oak'], (cx - 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['oak'], (cx + 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['dark'], (cx, cy + 0.1, 0.8), (0.4, 0.06, 1.5))
    mb.box(M['oakd'], (cx, cy - 0.12, 1.55), (0.5, 0.05, 0.1)); mb.box(M['oak'], (cx - 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['oak'], (cx + 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['dark'], (cx, cy + 0.12, 2.05), (0.5, 0.06, 0.9))
    mb.box(M['oak'], (cx, cy, 2.55), (0.74, 0.38, 0.1)); mb.box(M['oakd'], (cx, cy, 2.66), (0.62, 0.32, 0.12)); mb.box(M['oak'], (cx, cy - 0.02, 1.58), (0.62, 0.34, 0.05)); mb.box(M['oak'], (cx, cy + 0.04, 2.05), (0.44, 0.03, 0.82))
    for gi, (dx, dz, r, nt) in enumerate([(-0.08, 2.3, 0.11, 14), (0.07, 2.12, 0.085, 12), (-0.07, 1.95, 0.065, 10), (0.08, 1.84, 0.045, 8)]): gear(mb, M['gearw'], (cx + dx, cy - 0.04 - 0.045 * gi, dz), r, nt=nt, th=0.035, rim=0.02, tooth=0.02, hub=0.02, n=12)   # each gear offset along its normal (y) so teeth never intersect
    mb.rod(M['iron'], (cx, cy - 0.02, 2.4), (cx, cy - 0.02, 1.1), 0.007, 0.007, 6); mb.cyl(M['brass'], (cx, cy - 0.02, 1.0), 0.1, 0.03, axis='y', seg=16)
    for dx in (-0.1, 0.1):
        mb.rod(M['iron'], (cx + dx, cy - 0.04, 1.8), (cx + dx, cy - 0.04, 0.45 if dx < 0 else 0.7), 0.004, 0.004, 4); mb.cyl(M['brass'], (cx + dx, cy - 0.04, 0.38 if dx < 0 else 0.62), 0.045, 0.2, seg=10)
    for dx in (-0.3, 0, 0.3): mb.ell(M['brass'], (cx + dx, cy, 2.78), (0.03, 0.03, 0.05), (8, 6))
    # ---- back wall: wooden gear wheels on pegs, saws, chisel rack
    for gi, (x, z, r, nt, col) in enumerate([(0.55, 2.0, 0.31, 18, 'gearw'), (1.0, 2.3, 0.2, 14, 'honey'), (0.87, 1.74, 0.14, 10, 'gearw'), (0.3, 1.7, 0.1, 8, 'oak')]):
        gy = Y1 - 0.08 - 0.05 * gi                    # each gear offset along its normal (y) by > its thickness: no intersecting teeth
        gear(mb, M[col], (x, gy, z), r, nt=nt, th=0.045, rim=0.045 * (r / 0.3 + 0.5), tooth=0.05 * (r / 0.3 + 0.4), hub=0.04)
        mb.rod(M['iron'], (x, gy, z + r + 0.04), (x, Y1, z + r + 0.04), 0.012, 0.012, 6)
    hang_saw(mb, M, (1.6, Y1 - 0.12, 2.45), 0.7, 0.0); hang_saw(mb, M, (2.05, Y1 - 0.12, 2.0), 0.55, 1.2); hang_saw(mb, M, (1.75, Y1 - 0.12, 1.85), 0.5, -0.06)
    mb.box(M['oakd'], (1.2, Y1 - 0.1, 1.5), (1.4, 0.06, 0.06))
    for k in range(7):
        x = 0.6 + k * 0.2; mb.box(M['steel'], (x, Y1 - 0.13, 1.58), (0.018, 0.012, 0.16)); mb.box(M['honey'], (x, Y1 - 0.14, 1.42), (0.04, 0.045, 0.1))
    # ---- workbench (against the back wall, right)
    bx0, bx1, by0, by1 = 0.3, 2.2, 1.5, 2.3
    mb.box(M['walnut'], ((bx0 + bx1) / 2, (by0 + by1) / 2, BZ - 0.05), (bx1 - bx0, by1 - by0, 0.1)); mb.box(M['walnut'], ((bx0 + bx1) / 2, by0 + 0.02, BZ - 0.17), (bx1 - bx0, 0.05, 0.14))
    for x in (bx0 + 0.1, bx1 - 0.1):
        for y in (by0 + 0.08, by1 - 0.1): mb.box(M['walnut'], (x, y, BZ / 2 - 0.05), (0.12, 0.12, BZ - 0.1))
    mb.box(M['oakd'], ((bx0 + bx1) / 2, (by0 + by1) / 2, 0.3), (bx1 - bx0 - .1, by1 - by0 - .1, 0.05))
    mb.box(M['oak'], (bx0 + 0.15, by0 - 0.06, BZ), (0.14, 0.1, 0.1)); mb.cyl(M['iron'], (bx0 + 0.15, by0 - 0.16, BZ - 0.02), 0.025, 0.18, axis='y', seg=8)
    mb.rod(M['oakd'], (bx0 + 0.04, by0 - 0.22, BZ - 0.02), (bx0 + 0.26, by0 - 0.22, BZ - 0.02), 0.015, 0.015, 6)
    for k in range(4): mb.cyl(M['honey'], (bx0 + 0.35 + 0.12 * k, 1.9, 0.37 + 0.035 * k), 0.16, 0.04, seg=14)
    mb.box(M['oak'], (1.5, 1.9, 0.36), (0.5, 0.3, 0.05)); mb.box(M['oakd'], (1.7, 1.95, 0.42), (0.6, 0.12, 0.05))
    # bench tools + clutter (kept off the clock slots x 0.7..2.0, y 1.7..2.05)
    mb.box(M['honey'], (0.45, 1.65, BZ + 0.035), (0.34, 0.1, 0.07)); mb.box(M['steel'], (0.45, 1.65, BZ + 0.075), (0.18, 0.05, 0.012)); mb.box(M['oakd'], (0.52, 1.65, BZ + 0.1), (0.05, 0.05, 0.07))        # plane
    mb.cyl(M['oakd'], (0.7, 1.62, BZ + 0.07), 0.04, 0.16, axis='x', seg=8); mb.rod(M['oak'], (0.7, 1.62, BZ + 0.07), (0.7, 1.9, BZ + 0.07), 0.014, 0.014, 6)                                         # mallet
    mb.box(M['steel'], (2.0, 1.62, BZ + 0.012), (0.5, 0.075, 0.008)); mb.box(M['oakd'], (2.15, 1.62, BZ + 0.04), (0.1, 0.04, 0.08))
    for k in range(4): mb.box(M['steel'], (1.75 + 0.05 * k, 1.58, BZ + 0.012), (0.015, 0.2, 0.01)); mb.box(M['honey'], (1.75 + 0.05 * k, 1.44, BZ + 0.02), (0.03, 0.08, 0.03))
    mb.rod(M['iron'], (0.55, 2.2, BZ + 0.2), (0.55, 2.2, BZ + 0.02), 0.012, 0.012, 6); mb.rod(M['iron'], (0.55, 2.2, BZ + 0.2), (0.7, 2.2, BZ + 0.2), 0.012, 0.012, 6); mb.ell(M['oakd'], (0.7, 2.2, BZ + 0.2), (0.04, 0.04, 0.04), (8, 6))
    mb.box(M['steel'], (0.4, 2.0, BZ + 0.01), (0.3, 0.012, 0.01)); mb.box(M['steel'], (0.26, 2.1, BZ + 0.01), (0.012, 0.2, 0.01))
    mb.cyl(M['terra'], (2.05, 2.2, BZ + 0.07), 0.06, 0.14, seg=10)
    for k in range(6): curl(mb, M['shav'], (0.4 + 0.3 * k, 1.62 + 0.1 * (k % 2), BZ), rr, 0.9)
    # brass candlestick + oil lamp on the bench (flames are separate objects)
    mb.cyl(M['brass'], (0.38, 2.28, BZ + 0.015), 0.05, 0.03, seg=10); mb.cyl(M['brass'], (0.38, 2.28, BZ + 0.07), 0.015, 0.1, seg=8)
    mb.ell(M['terra'], (2.0, 2.3, BZ + 0.07), (0.085, 0.06, 0.07), (10, 8)); mb.box(M['terra'], (2.0, 2.3, BZ + 0.15), (0.03, 0.03, 0.05))
    # ---- treadle lathe
    lx, ly = -1.1, 2.15
    for x in (lx - 0.55, lx + 0.55):
        for y in (ly - 0.15, ly + 0.15): mb.box(M['oak'], (x, y, 0.45), (0.09, 0.09, 0.9))
    for y in (ly - 0.07, ly + 0.07): mb.box(M['honey'], (lx, y, 0.92), (1.3, 0.07, 0.07))
    mb.box(M['oakd'], (lx - 0.45, ly, 1.07), (0.16, 0.26, 0.24)); mb.box(M['oakd'], (lx + 0.42, ly, 1.04), (0.12, 0.22, 0.18)); mb.box(M['iron'], (lx + 0.3, ly, 1.0), (0.06, 0.03, 0.03))
    mb.cyl(M['honey'], (lx - 0.02, ly, 1.04), 0.05, 0.6, axis='x', seg=12, r2=0.035); mb.box(M['oakd'], (lx + 0.05, ly - 0.14, 0.99), (0.2, 0.04, 0.025))
    gear(mb, M['oak'], (lx - 0.78, ly - 0.35, 0.62), 0.3, nt=0, th=0.06, rim=0.05, spokes=3, tooth=0.0, rot=(0, 0, math.pi / 2), hub=0.06, n=18)
    mb.box(M['oakd'], (lx + 0.1, ly - 0.55, 0.12), (0.7, 0.16, 0.04), ry=0.12); mb.rod(M['iron'], (lx - 0.78, ly - 0.35, 0.62), (lx - 0.35, ly - 0.52, 0.16), 0.01, 0.01, 6)
    curl(mb, M['shav'], (lx, ly - 0.2, 0.92), rr, 0.9)
    # ---- right wall: leaning boards, chest + lantern, barrel
    for k in range(5): mb.box(M['honey'] if k % 2 else M['oak'], (2.12 - 0.01 * k, 3.15 - 0.2 * k, 1.1), (0.05, 0.2, 2.1), ry=0.09)
    mb.box(M['oakd'], (2.0, 0.95, 0.26), (0.7, 0.5, 0.52)); mb.box(M['oak'], (2.0, 0.95, 0.55), (0.74, 0.54, 0.08))
    for dx in (-0.25, 0.25): mb.box(M['brassd'], (2.0 + dx, 0.95, 0.3), (0.05, 0.56, 0.54))
    mb.cyl(M['oak'], (-1.85, 1.2, 0.3), 0.26, 0.6, seg=14)
    for z in (0.12, 0.3, 0.48): mb.cyl(M['iron'], (-1.85, 1.2, z), 0.275, 0.03, seg=14)
    mb.box(M['iron'], (2.0, 0.95, 0.6), (0.2, 0.2, 0.04)); mb.box(M['iron'], (2.0, 0.95, 0.95), (0.2, 0.2, 0.04))
    for dx, dy in ((-0.08, -0.08), (0.08, -0.08), (-0.08, 0.08), (0.08, 0.08)): mb.box(M['iron'], (2.0 + dx, 0.95 + dy, 0.78), (0.02, 0.02, 0.32))
    # ---- ceiling: hanging oil lamp + herbs
    mb.rod(M['iron'], (-0.1, 1.6, ZH - 0.28), (-0.1, 1.6, 2.35), 0.008, 0.008, 4); mb.ell(M['brassd'], (-0.1, 1.6, 2.25), (0.09, 0.09, 0.07), (10, 8))
    for k in range(6): mb.rod(M['green'] if k % 2 else M['cloth'], (1.0 + 0.1 * k, -0.3, ZH - 0.28), (1.0 + 0.1 * k + 0.02 * (k - 2), -0.3, 2.25), 0.02, 0.05, 5)
    for k in range(4): mb.rod(M['cloth'], (-1.6 + 0.12 * k, 0.4, ZH - 0.28), (-1.6 + 0.12 * k, 0.4, 2.3 - 0.05 * k), 0.015, 0.045, 5)
    # ---- wall shelf of jars, tins and clock parts above the lathe, hung from the beam
    for dx in (-0.62, 0.62): mb.rod(M['cloth'], (-1.1 + dx, 2.3, ZH - 0.26), (-1.1 + dx, 2.3, 2.06), 0.012, 0.012, 5)
    mb.box(M['oak'], (-1.1, 2.3, 2.04), (1.4, 0.3, 0.05))
    for (dx, r, h, col) in [(-0.55, 0.06, 0.2, 'terra'), (-0.4, 0.05, 0.14, 'cream'), (-0.22, 0.07, 0.24, 'terra'), (-0.05, 0.05, 0.1, 'green')]: mb.cyl(M[col], (-1.1 + dx, 2.3, 2.065 + h / 2), r, h, seg=10)
    mb.box(M['iron'], (-1.1 + 0.18, 2.3, 2.12), (0.14, 0.1, 0.1)); mb.box(M['brass'], (-1.1 + 0.36, 2.3, 2.09), (0.12, 0.12, 0.04)); gear(mb, M['brass'], (-1.1 + 0.52, 2.18, 2.13), 0.07, nt=10, th=0.02, rim=0.015, tooth=0.015, hub=0.015, n=10, rot=(math.pi / 2, 0, 0))
    mb.cyl(M['cream'], (-1.1 + 0.6, 2.3, 2.2), 0.018, 0.14, seg=8)
    # second shelf on the left wall: tins, clock movements, a brass bell
    mb.box(M['oak'], (X0 + 0.2, 0.2, 1.7), (0.3, 1.3, 0.05)); mb.box(M['oak'], (X0 + 0.2, 0.2, 2.2), (0.3, 1.3, 0.05))
    for (yy, cm, r, h) in [(-0.25, 'terra', 0.06, 0.16), (-0.05, 'cream', 0.05, 0.12), (0.12, 'green', 0.06, 0.2), (0.35, 'terra', 0.05, 0.1), (0.55, 'cloth', 0.05, 0.14)]: mb.cyl(M[cm], (X0 + 0.2, yy, 1.725 + h / 2), r, h, seg=10)
    for (yy, a) in [(-0.2, 0.3), (0.15, -0.2), (0.45, 0.5)]:
        gear(mb, M['brass'], (X0 + 0.2, yy, 2.32), 0.09, nt=10, th=0.02, rim=0.015, tooth=0.016, hub=0.015, n=10, rot=(math.pi / 2, 0, a))
    mb.cyl(M['brass'], (X0 + 0.2, 0.55, 2.3), 0.07, 0.1, seg=14, r2=0.03)
    # ---- front wall dressing (visible from shop_door): pegs with tools, shelf of jars, ladder, boards, sacks, barrel
    yw = Y0 + 0.12
    # right of the door: a coat-peg rail with a coat, a leather apron and a hat; the small window onto the yard; a shelf of jars above
    mb.box(M['oakd'], (0.78, yw, 1.66), (0.95, 0.05, 0.1))
    for k in range(4): mb.box(M['iron'], (0.45 + 0.22 * k, yw - 0.03, 1.66), (0.03, 0.08, 0.03))
    mb.box(M['coat'], (0.45, yw - 0.06, 1.2), (0.34, 0.07, 0.8)); mb.box(M['coat'], (0.45, yw - 0.1, 1.5), (0.38, 0.06, 0.3)); mb.box(M['coat'], (0.27, yw - 0.08, 1.15), (0.1, 0.07, 0.62), rz=0.0); mb.box(M['coat'], (0.63, yw - 0.08, 1.15), (0.1, 0.07, 0.62))
    mb.box(M['leather'], (0.67, yw - 0.06, 1.28), (0.24, 0.05, 0.62)); mb.box(M['leather'], (0.67, yw - 0.08, 1.52), (0.06, 0.04, 0.2)); mb.cyl(M['dark'], (0.89, yw - 0.1, 1.74), 0.13, 0.02, axis='y', seg=14); mb.cyl(M['dark'], (0.89, yw - 0.12, 1.76), 0.07, 0.1, axis='y', seg=12)
    wx0_, wx1_, wz0_, wz1_ = FW; ym_ = Y0 - 0.02
    for k in range(4): mb.box(M['oakd'], (wx0_ + k * (wx1_ - wx0_) / 3, ym_, (wz0_ + wz1_) / 2), (0.035, 0.05, wz1_ - wz0_))
    for k in range(4): mb.box(M['oakd'], ((wx0_ + wx1_) / 2, ym_, wz0_ + k * (wz1_ - wz0_) / 3), (wx1_ - wx0_, 0.05, 0.035))
    for x in (wx0_, wx1_): mb.box(M['oakd'], (x, Y0 - 0.1, (wz0_ + wz1_) / 2), (0.1, 0.28, wz1_ - wz0_ + 0.1))
    for z in (wz0_, wz1_): mb.box(M['oakd'], ((wx0_ + wx1_) / 2, Y0 - 0.1, z), (wx1_ - wx0_ + 0.1, 0.28, 0.1))
    mb.box(M['oak'], ((wx0_ + wx1_) / 2, Y0 + 0.08, wz0_ - 0.04), (wx1_ - wx0_ + 0.3, 0.3, 0.06))
    mb.cyl(M['terra'], (1.55, Y0 + 0.12, wz0_ + 0.06), 0.06, 0.1, seg=10, r2=0.075); mb.cyl(M['cream'], (1.9, Y0 + 0.12, wz0_ + 0.05), 0.04, 0.07, seg=10)
    # left of the door: two saws hung upright and a spoke-shave rack
    hang_saw(mb, M, (-1.42, yw, 1.35), 0.8, math.pi / 2); hang_saw(mb, M, (-1.2, yw, 1.3), 0.65, math.pi / 2 + 0.03)
    for k in range(4): mb.box(M['iron'], (-1.45 + 0.12 * k, yw - 0.03, 1.95), (0.02, 0.05, 0.02)); mb.box(M['oak'], (-1.45 + 0.12 * k, yw - 0.05, 1.82), (0.04, 0.03, 0.2))
    mb.box(M['oak'], (1.55, yw - 0.1, 2.05), (1.5, 0.28, 0.05))
    for k, (cm, r, h) in enumerate([('terra', 0.07, 0.22), ('cream', 0.05, 0.16), ('terra', 0.06, 0.26), ('green', 0.05, 0.12), ('cloth', 0.06, 0.18), ('terra', 0.05, 0.14)]): mb.cyl(M[cm], (0.95 + 0.2 * k, yw - 0.1, 2.075 + h / 2), r, h, seg=10)
    mb.box(M['oak'], (-1.55, yw - 0.1, 1.9), (1.1, 0.28, 0.05))
    for k, (cm, w_, h) in enumerate([('red', 0.18, 0.26), ('cloth', 0.14, 0.2), ('cream', 0.12, 0.3), ('terra', 0.16, 0.18)]): mb.box(M[cm], (-1.95 + 0.27 * k, yw - 0.1, 1.925 + h / 2), (w_, 0.14, h))
    mb.box(M['oakd'], (-1.95, yw - 0.06, 1.0), (0.06, 0.04, 1.8)); mb.box(M['oakd'], (-1.65, yw - 0.06, 1.0), (0.06, 0.04, 1.8))          # ladder
    for k in range(9): mb.box(M['oak'], (-1.8, yw - 0.06, 0.2 + 0.2 * k), (0.3, 0.035, 0.035))
    for k in range(5): mb.box(M['honey'] if k % 2 else M['oak'], (X0 + 0.45, Y0 + 0.3 + 0.0, 0.5 + 0.0), (0, 0, 0)) if False else None
    for k in range(6): mb.box(M['honey'] if k % 2 else M['oak'], (1.95, -2.35, 0.04 + 0.075 * k), (0.9 + 0.04 * (k % 2), 0.28, 0.07), rz=0.04 * k)             # stacked boards
    mb.ell(M['sack'], (-2.0, -2.35, 0.28), (0.32, 0.26, 0.3), (12, 8)); mb.ell(M['sack'], (-1.6, -2.45, 0.22), (0.28, 0.24, 0.24), (12, 8)); mb.box(M['sack'], (-2.0, -2.35, 0.55), (0.1, 0.08, 0.06))
    mb.cyl(M['oak'], (1.2, -2.35, 0.32), 0.28, 0.64, seg=14)
    for z in (0.12, 0.32, 0.52): mb.cyl(M['iron'], (1.2, -2.35, z), 0.29, 0.03, seg=14)
    mb.rod(M['oak'], (0.75, -2.7, 1.5), (0.6, -2.3, 0.0), 0.014, 0.014, 5)
    for a in range(10): mb.rod(M['honey'], (0.6, -2.3, 0.2), (0.6 + 0.02 * (a - 5), -2.3 + 0.01 * a, 0.0), 0.012, 0.008, 4)    # broom
    # ---- overhead dressing: cart-wheel candle chandelier, herb bunches, hanging tools on the beams, planks stored on the joists, coil of rope, pulley
    wcx, wcy, wcz = 0.15, 0.7, 2.28
    for k in range(3): mb.rod(M['iron'], (wcx + 0.35 * math.cos(k * 2.094 + 0.4), wcy + 0.35 * math.sin(k * 2.094 + 0.4), wcz + 0.05), (wcx, wcy, ZH - 0.28), 0.006, 0.006, 4)
    mb.cyl(M['oak'], (wcx, wcy, wcz), 0.5, 0.05, seg=24); mb.cyl(M['dark'], (wcx, wcy, wcz), 0.44, 0.06, seg=24); mb.cyl(M['oak'], (wcx, wcy, wcz), 0.36, 0.07, seg=24)
    for k in range(6): mb.box(M['oakd'], (wcx, wcy, wcz), (1.0, 0.05, 0.05), rz=k * math.pi / 6)
    mb.cyl(M['iron'], (wcx, wcy, wcz + 0.04), 0.06, 0.08, seg=10)
    SET['wheelcandles'] = [(wcx + 0.46 * math.cos(k * math.pi / 2 + 0.3), wcy + 0.46 * math.sin(k * math.pi / 2 + 0.3), wcz + 0.03) for k in range(4)]
    for (px_, py_, pz_) in SET['wheelcandles']: mb.cyl(M['brass'], (px_, py_, pz_ + 0.012), 0.035, 0.02, seg=8); mb.cyl(M['cream'], (px_, py_, pz_ + 0.1), 0.02, 0.16, seg=8)
    for k in range(7): mb.rod(M['green'] if k % 2 else M['cloth'], (-0.5 + 0.12 * k, 2.7, ZH - 0.28), (-0.5 + 0.12 * k + 0.02 * (k - 3), 2.7, 2.2 - 0.06 * (k % 3)), 0.015, 0.05, 5)
    for k in range(5): mb.rod(M['green'], (-1.9 + 0.1 * k, -1.8, ZH - 0.28), (-1.9 + 0.1 * k, -1.8, 2.3 - 0.04 * k), 0.012, 0.04, 5)
    for (x_, y_, ln) in [(1.9, -0.3, 0.8), (-1.7, 1.2, 0.7), (1.5, 1.5, 0.9)]:
        mb.rod(M['iron'], (x_, y_, ZH - 0.28), (x_, y_, ZH - 0.5), 0.006, 0.006, 4); hang_saw(mb, M, (x_, y_, ZH - 0.55), ln, 0.0)
    for k in range(5): mb.box(M['honey'] if k % 2 else M['oak'], (X1 - 0.5, -1.0 + 0.5 * k, ZH - 0.33), (0.2, 0.9, 0.04), rz=0.05 * k)
    for k in range(4): mb.box(M['oak'], (-1.9, -1.4 + 0.55 * k, ZH - 0.33), (0.18, 0.9, 0.04))
    for k in range(6): mb.cyl(M['cloth'], (-0.6, -1.6, ZH - 0.6 + 0.0), 0.12 - 0.012 * k, 0.03, seg=12) if False else None
    mb.cyl(M['iron'], (-0.6, -0.9, ZH - 0.45), 0.09, 0.04, axis='y', seg=16); mb.rod(M['iron'], (-0.6, -0.9, ZH - 0.28), (-0.6, -0.9, ZH - 0.4), 0.006, 0.006, 4)
    # woven rag rug (muted ochre / rust / grey stripes, fringed ends) on the floor between the figures: no bullseye
    cols = ('rug2', 'rug1', 'rugg', 'rug2', 'rugd', 'rug1', 'rugg', 'rug2', 'rug1'); n_ = len(cols); rw = 0.2; rl = 1.25
    mb.push(Matrix.Translation((0.05, 0.35, 0)) @ Euler((0, 0, 0.12)).to_matrix().to_4x4())
    for k, cc in enumerate(cols): mb.box(M[cc], (-(n_ - 1) * rw / 2 + k * rw, 0, 0.007), (rw - 0.004, rl, 0.014))
    for e in (-1, 1):
        for k in range(18): mb.box(M['rug4'], (-n_ * rw / 2 + 0.05 + k * (n_ * rw - 0.1) / 17, e * (rl / 2 + 0.04), 0.004), (0.012, 0.09, 0.006), rz=0.08 * ((k % 3) - 1))
    mb.pop()
    # ---- floor-level dense dressing (lower third of shop_wide / bench): tool chest with open drawers, offcut basket, half-built clock case, stump + axe, plank, sawhorse
    def chest(cx_, cy_, s=0.8, yaw=0.0):
        mb.push(Matrix.Translation((cx_, cy_, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
        mb.box(M['oakd'], (0, 0, 0.3), (0.9, 0.5, 0.6)); mb.box(M['oak'], (0, 0, 0.62), (0.94, 0.54, 0.05))
        for k in range(3):
            dz = 0.14 + 0.17 * k; ext = 0.0 if k == 1 else 0.22
            mb.box(M['honey'], (0, -0.27 - ext, dz), (0.78, 0.04, 0.13)); mb.box(M['brass'], (0, -0.29 - ext, dz), (0.12, 0.02, 0.03))
            if ext:
                mb.box(M['dark'], (0, -0.15 - ext / 2, dz - 0.02), (0.72, ext, 0.05)); mb.box(M['steel'], (-0.1, -0.15 - ext / 2, dz + 0.03), (0.3, 0.04, 0.01), rz=0.4); mb.box(M['honey'], (0.15, -0.2 - ext / 2, dz + 0.05), (0.1, 0.1, 0.1))
                mb.box(M['iron'], (0.28, -0.2 - ext / 2, dz + 0.03), (0.05, 0.12, 0.03)); mb.cyl(M['brass'], (-0.28, -0.22 - ext / 2, dz + 0.03), 0.03, 0.04, seg=8)
        mb.pop()
    def basket(cx_, cy_):
        mb.cyl(M['oakd'], (cx_, cy_, 0.15), 0.21, 0.3, seg=16, r2=0.25)
        for k in range(4): mb.cyl(M['cloth'], (cx_, cy_, 0.05 + 0.08 * k), 0.215 + 0.012 * k, 0.02, seg=16)
        for a in range(11): mb.rod(M['honey'] if a % 2 else M['oak'], (cx_ + 0.1 * math.cos(a * 0.6), cy_ + 0.1 * math.sin(a * 0.6), 0.28), (cx_ + 0.22 * math.cos(a * 0.6 + 0.4), cy_ + 0.22 * math.sin(a * 0.6 + 0.4), 0.55 + 0.04 * (a % 3)), 0.03, 0.03, 6)
        for a in range(3): mb.box(M['oak'], (cx_ + 0.18 * math.cos(a * 2.1), cy_ + 0.18 * math.sin(a * 2.1), 0.33), (0.22, 0.06, 0.04), rz=a * 2.1)
    def case(cx_, cy_):
        for dx in (-0.2, 0.2): mb.box(M['honey'], (cx_ + dx, cy_, 0.95), (0.07, 0.07, 1.9), ry=0.05)
        for z in (0.15, 0.7, 1.25, 1.8): mb.box(M['honey'], (cx_, cy_, z), (0.46, 0.06, 0.07))
        mb.box(M['oak'], (cx_, cy_ + 0.05, 0.95), (0.4, 0.02, 0.5)); mb.box(M['oakd'], (cx_, cy_ - 0.02, 1.95), (0.5, 0.1, 0.1), ry=0.05)
    def stump(cx_, cy_, r=0.34, h=0.46):
        n = 28
        mb.cyl(M['bark'], (cx_, cy_, h / 2), r, h, seg=n, r2=r * 0.93)
        for a in range(18):
            aa = a * 2 * math.pi / 18 + rr.random() * 0.2; mb.box(M['dark'], (cx_ + (r * 0.96) * math.cos(aa), cy_ + (r * 0.96) * math.sin(aa), h / 2), (0.025, 0.03, h * (0.6 + 0.4 * rr.random())), rz=aa)
        for k in range(7): mb.cyl(M['ring'] if k % 2 == 0 else M['honey'], (cx_, cy_, h + 0.003 * (k + 1)), r * (0.93 - 0.13 * k), 0.003, seg=n)
        for a in range(3): mb.box(M['bark'], (cx_ + (r + 0.06) * math.cos(a * 2.1 + 0.4), cy_ + (r + 0.06) * math.sin(a * 2.1 + 0.4), 0.05), (0.2, 0.1, 0.1), rz=a * 2.1 + 0.4)
        mb.box(M['dark'], (cx_ + 0.1, cy_ - 0.05, h + 0.12), (0.04, 0.05, 0.24), rx=0.3); mb.box(M['steel'], (cx_ + 0.1, cy_ - 0.18, h + 0.2), (0.05, 0.16, 0.12), rx=0.3)   # axe in the stump
    def horse(cx_, cy_):
        mb.box(M['oak'], (cx_, cy_, 0.62), (0.9, 0.08, 0.08))
        for sx in (-0.4, 0.4):
            mb.rod(M['oakd'], (cx_ + sx, cy_ - 0.2, 0.0), (cx_ + sx, cy_, 0.62), 0.03, 0.03, 6); mb.rod(M['oakd'], (cx_ + sx, cy_ + 0.2, 0.0), (cx_ + sx, cy_, 0.62), 0.03, 0.03, 6)
        mb.box(M['honey'], (cx_ + 0.05, cy_, 0.69), (1.0, 0.24, 0.05), rz=0.1)
    PRESET_FG = SET['preset']
    if preset == 'shop_door': chest(-1.6, -0.6, 0.6, 0.4); basket(-0.15, -0.35); case(-2.05, 0.9); stump(1.45, -0.9, r=0.24, h=0.32)
    else: chest(-0.55, -0.6, 0.62, 0.2); basket(0.5, -0.85); case(-2.05, 0.9); stump(0.75, -1.5, r=0.24, h=0.32)
    mb.box(M['oak'], (-0.2, -1.5, 0.022), (0.9, 0.12, 0.044), rz=0.5); mb.box(M['oakd'], (0.25, -0.6, 0.022), (0.7, 0.1, 0.044), rz=-0.35)
    mb.box(M['oakd'], (-0.2, -1.5, 0.006), (0.7, 0.08, 0.012), rz=0.5); mb.box(M['oakd'], (0.25, -0.6, 0.006), (0.5, 0.07, 0.012), rz=-0.35)           # dark contact strip under each offcut: they lie on the boards
    horse(1.45, 0.0)
    # a smoothing plane + a curl of honey shavings on the sawhorse plank, 1-2 D from the lens in shop_bench (bottom-left foreground)
    mb.box(M['honey'], (1.16, 0.0, 0.745), (0.3, 0.075, 0.04)); mb.box(M['steel'], (1.16, 0.0, 0.768), (0.17, 0.05, 0.008)); mb.box(M['oakd'], (1.1, 0.0, 0.79), (0.045, 0.045, 0.06)); mb.box(M['oakd'], (1.27, 0.0, 0.775), (0.05, 0.03, 0.035))
    for k in range(5): curl(mb, M['shav'], (0.97 + 0.045 * k, 0.07 - 0.03 * (k % 2), 0.72), rr, 0.7)
    # a second case + half a gear in progress on the floor near the bench, bucket of water, stool
    mb.cyl(M['oakd'], (1.15, 0.45, 0.4), 0.2, 0.06, seg=14)
    for a in (0.3, 2.4, 4.5): mb.rod(M['oak'], (1.15 + 0.16 * math.cos(a), 0.45 + 0.16 * math.sin(a), 0.38), (1.15 + 0.24 * math.cos(a), 0.45 + 0.24 * math.sin(a), 0.0), 0.025, 0.02, 6)
    mb.cyl(M['cloth'], (-1.65, 0.9, 0.13), 0.14, 0.26, seg=12, r2=0.17)
    gear(mb, M['honey'], (0.56, 2.08, BZ + 0.025), 0.12, nt=12, th=0.03, rim=0.025, tooth=0.025, hub=0.025, n=14, rot=(math.pi / 2, 0, 0.5))       # half-made gear lies on the bench, not on the rug
    # shavings: ~240 thin honey ribbons clustered round the bench, lathe, chest and stump
    for k in range(240):
        c = rr.random()
        if c < 0.35: x, y = rr.gauss(1.1, 0.5), rr.gauss(1.1, 0.4)
        elif c < 0.6: x, y = rr.gauss(-1.1, 0.4), rr.gauss(1.6, 0.3)
        elif c < 0.8: x, y = rr.gauss(-0.4, 0.5), rr.gauss(-0.7, 0.5)
        else: x, y = rr.gauss(0.3, 0.9), rr.gauss(0.2, 0.8)
        curl(mb, M['shav'], (x, y, 0.0), rr, rr.uniform(0.32, 0.5))
    mb.finish()
    # ---- flames (emissive, no shadow) and the burn-down candle
    SET['flames'] = []
    fm = M['flame']; lamps = SET.setdefault('lampset', [])
    def flame(name, p, r=0.02, h=0.05, lamp=None, group='candle'):
        f = MB(name); f.ell(fm, (0, 0, 0), (r, r, h), (8, 6)); o = f.finish(shadow=False)[0]; o.location = p; SET['flames'].append((o, p)); return o
    def candle_obj(name, p, h):
        pv = pivot(name, root, p); b = MB(name); b.cyl(M['cream'], (0, 0, 0.5), 0.022, 1.0, seg=10); b.cyl(M['wick'], (0, 0, 1.0), 0.003, 0.025, seg=4); o = b.finish(shadow=True, parent=pv)[0]
        pv.scale = (1, 1, h); return pv
    st = candle_obj('stub_bench', (0.38, 2.28, BZ + 0.03), 0.17); fl0 = flame('flame_bench', (0.38, 2.28, BZ + 0.03 + 0.17 + 0.03)); SET['stub'] = dict(pv=st, h=0.17, flame=fl0, base=(0.38, 2.28, BZ + 0.03))
    flame('flame_lamp', (2.0, 2.3, BZ + 0.2), 0.02, 0.045); flame('flame_hang', (-0.1, 1.6, 2.3), 0.025, 0.05)
    flame('flame_shelf', (-1.1 + 0.6, 2.3, 2.3), 0.02, 0.045); candle_obj('stub_shelf', (-1.1 + 0.6, 2.3, 2.065), 0.14)
    candle_obj('stub_sill', (wx0 + 0.55, Y1 - 0.14, wz0 + 0.035), 0.12); flame('flame_sill', (wx0 + 0.55, Y1 - 0.14, wz0 + 0.035 + 0.12 + 0.03))
    for i, p_ in enumerate(SET['wheelcandles']): flame('flame_wheel%d' % i, (p_[0], p_[1], p_[2] + 0.22), 0.02, 0.05)
    lanm = MB('lantern'); lanm.box(M['lampg'], (0, 0, 0), (0.13, 0.13, 0.28)); lo = lanm.finish(shadow=False)[0]; lo.location = (2.0, 0.95, 0.78); SET['flames'].append((lo, (2.0, 0.95, 0.78)))
    lan2 = MB('lantern2'); lan2.box(M['lampg'], (0, 0, 0), (0.11, 0.11, 0.24)); l2 = lan2.finish(shadow=False)[0]; l2.location = (-0.9, Y0 + 0.35, 1.95); SET['flames'].append((l2, (-0.9, Y0 + 0.35, 1.95)))
    mb2 = MB('lantern2f'); mb2.rod(M['iron'], (-0.9, Y0 + 0.35, 2.07), (-0.9, Y0 + 0.2, 2.35), 0.008, 0.008, 4); mb2.box(M['iron'], (-0.9, Y0 + 0.35, 2.09), (0.15, 0.15, 0.03)); mb2.box(M['iron'], (-0.9, Y0 + 0.35, 1.81), (0.15, 0.15, 0.03)); mb2.finish()
    for dx, dy in ((-0.06, -0.06), (0.06, -0.06), (-0.06, 0.06), (0.06, 0.06)):
        mb2 = MB('lantern2g'); mb2.box(M['iron'], (-0.9 + dx, Y0 + 0.35 + dy, 1.95), (0.015, 0.015, 0.28)); mb2.finish()
    # ---- clocks (hooks): clock roots hidden until set_clock
    SET['clocks'] = {}
    for n in (1, 2, 3, 4):
        nm, fn = CLOCK_BUILD[n]; pv = pivot('clock%d' % n, root, (1.2, 1.88, BZ), scale=CLOCK_SCALE[n]); d = fn(M, pv); d['root'] = pv; SET['clocks'][n] = d
    SET['PL'] = PL; SET['light'] = light; SET['mats'] = M
    # ---- lights
    build_lights(SET, light)
    SET['marks'] = {k: W(v) for k, v in MARKS_M.items()}
    SET['cams'] = {k: dict(loc=W(c[0]), look_at=W(c[1]), lens=22.0) for k, c in CAMS_M.items()}
    SET['cam_name'] = preset; SET['cam_notes'] = CAM_NOTES
    SET['staging'] = {k: [(r, SET['marks'][m]) for r, m in v] for k, v in STAGING.items()}
    SET['floor_z'] = 0.0
    for o, p in SET['flames']: o.location = p
    set_door(78.0)
    set_clock(DEFAULT_CLOCK.get(preset, 1)); set_candles(1.0)

DEFAULT_CLOCK = dict(shop_wide=1, shop_bench=1, shop_clock=[1, 4], shop_door=1)

def build_lights(SET, light):
    PL = LIGHTS[light]; S = SET; S['lampgroups'] = {'candle': [], 'fill': [], 'warm': [], 'win': [], 'door': []}
    d = Vector(K.kdir(PL['az'], PL['el'])); sun('key', PL['key'], PL['key'][3], d, PL['sun_angle']); S['sundir'] = d
    G = S['lampgroups']
    def A(grp, *a, **k):
        o = area_light(*a, **k); G[grp].append((o, K.STATE['lights'][a[0]][1])); return o
    def Pt(grp, *a, **k):
        o = point_light(*a, **k); G[grp].append((o, K.STATE['lights'][a[0]][1])); return o
    K.shafts(d, (WIN[0], WIN[1], WIN[2], WIN[3], Y1 - 0.02), k=4.0, a=0.004 if light == 'DAY' else 0.0004, col='#ffd890' if light == 'DAY' else '#8fa4ff')
    A('fill', 'fill', (0, 0.3, 2.85), (0, 0, 0), (4.4, 5.5), (0.34, 0.4, 1.0), 220)
    A('fill', 'fillc', (0.0, -2.8, 1.5), (math.pi / 2, 0, 0), (4.4, 2.8), (0.4, 0.45, 1.0), 60)
    A('win', 'winfill', (-0.85, 3.3, 1.6), (-math.pi / 2, 0, 0), (1.1, 1.3), (0.3, 0.42, 1.0), 220)
    A('warm', 'roomwarm', (0.3, 1.0, 2.8), (0, 0, 0), (3.5, 4.5), (1.0, 0.72, 0.42), 110)
    A('warm', 'warmfront', (0.0, -2.6, 2.0), (math.pi / 2, 0, 0), (3.5, 2.0), (1.0, 0.7, 0.4), 50)
    A('door', 'doorlight', (-0.3, -2.55, 1.0), (-math.pi / 2, 0, 0), (0.9, 1.5), (1.0, 0.92, 0.7), 260)
    for (nm, loc, en) in [('p_bench', (0.38, 2.15, 1.25), 30), ('p_lamp', (2.0, 2.15, 1.2), 16), ('p_hang', (-0.1, 1.5, 2.3), 20), ('p_chest', (2.0, 0.72, 0.95), 18), ('p_shelf', (-0.5, 2.2, 2.35), 12),
                          ('p_clock', (0.3, 1.3, 1.75), 30), ('p_wheel', (0.15, 0.7, 2.45), 40), ('p_door', (-0.9, -2.5, 1.95), 20), ('p_sill', (-0.75, 3.1, 1.25), 10)]:
        Pt('candle', nm, loc, (1.0, 0.62, 0.26), en, 0.05)
    # per-light scaling by the light preset
    S['PLK'] = PL
    apply_light(light)

def apply_light(name, frame=None):
    S = K.STATE; PL = LIGHTS[name]; S['light'] = name; sc = bpy.context.scene
    k = sc.objects.get('key'); d = k.data; d.color = PL['key'][:3]; d.energy = PL['key'][3]; d.angle = math.radians(PL['sun_angle']); v = Vector(K.kdir(PL['az'], PL['el'])); k.rotation_euler = (-v).to_track_quat('Z', 'Y').to_euler()
    for grp, lst in S['lampgroups'].items():
        for o, base in lst: o.data.energy = base * PL.get(grp, 1.0) * K.E2
    sc.view_settings.exposure = PL['exposure']; S['sat'] = PL['sat']
    for m_ in S.get('ext_mats', []): m_.node_tree.nodes['dn'].outputs[0].default_value = 1.0 if name == 'NIGHT' else 0.0
    if S.get('ext_moon') is not None: S['ext_moon'].hide_render = name != 'NIGHT'
    S['candle_k'] = PL['candle']
    return PL

# ----------------------------------------------------------------------------- hooks
def _noise(frame, i=0):
    f = (frame if frame is not None else 0)
    return 0.5 * math.sin(f * 0.9 + i * 1.7) + 0.3 * math.sin(f * 2.3 + i * 0.6) + 0.2 * math.sin(f * 5.1 + i * 2.9)

def set_door(deg=78.0, frame=None):
    """front door leaf swing (deg from closed, 0..110)"""
    S = K.STATE
    for o in bpy.data.objects:
        if o.name.startswith('doorleaf'):
            pass
    S['door_deg'] = deg

def set_clock(n=1, frame=None):
    """n: 0 none | 1 H1 big brass (dumbbell bars) | 2 H2 | 3 H3 compact box with two round balances | 4 H4 silver watch on red cloth; or a list, e.g. [1, 4] side by side (the 'shrink' reveal)"""
    S = K.STATE; ns = [] if not n else (list(n) if isinstance(n, (list, tuple)) else [n]); S['clock_set'] = ns
    big = [x for x in ns if x != 4]; slots = {}
    if len(big) + (1 if 4 in ns else 0) == 1 and big: slots[big[0]] = (1.0, 1.88)
    elif big:
        if 4 in ns and len(big) == 1: slots[big[0]] = (0.5, 1.92)
        else:
            tab = CLOCK_SLOTS[min(3, len(big))]
            for x, s in zip(big, tab): slots[x] = s
    if 4 in ns: slots[4] = (1.15, 1.62) if not big else (1.12, 1.62)
    for c, d in S['clocks'].items():
        on = c in ns; root = d['root']; K._show([root] + list(root.children_recursive), on, frame)
        if on:
            root.location = (slots[c][0], slots[c][1], BZ + (0.0 if c != 4 else 0.105 * math.sin(H4_TILT) * CLOCK_SCALE[4] + 0.02)); K._keyxf(root, frame)
            if c == 4: root.rotation_euler = (H4_TILT, 0, 0); K._keyxf(root, frame, loc=False, rot=True)

def set_balance(t=0.0, frame=None):
    """balance and gears at time t (seconds): the crossed bars of H1 / H2 rock +-24 deg (H3: the two round balances counter-rotate +-70 deg), every gear turns at its own rate"""
    S = K.STATE; w = 2 * math.pi / 1.3
    for c, d in S['clocks'].items():
        for pv, sp in d.get('gears', []):
            pv.rotation_euler = (0, t * sp * 1.3, 0); K._keyxf(pv, frame, loc=False, rot=True)
        if c in (1, 2):
            th = math.radians(24) * math.sin(w * t); bars = d['bars']
            for pv, s_ in zip(bars[1:], (1, -1)): pv.rotation_euler = (0, 0, s_ * math.radians(33) + th * s_); K._keyxf(pv, frame, loc=False, rot=True)
        elif c == 3:
            th = math.radians(70) * math.sin(w * t)
            for pv, s_ in zip(d['bars'], d['balsgn']): pv.rotation_euler = (0, 0, th * s_); K._keyxf(pv, frame, loc=False, rot=True)

def set_candles(level=1.0, frame=None):
    """flame flicker (call per frame with frame=); level 0..1 also burns the NIGHT bench candle stub down (stub height = 0.17 m x level, 0 hides the flame and its light)"""
    S = K.STATE; lv = max(0.0, min(1.0, float(level))); fk = 1.0 + 0.16 * _noise(frame, 0)
    m = S['M']['flame']; em = m.node_tree.nodes['Emission'].inputs['Strength']; K._keysock(em, 28.0 * (0.9 + 0.2 * (fk - 0.84) / 0.32 * 1.0) * (1.0 if lv > 0 else 0.0), frame)
    st = S['stub']; pv = st['pv']; pv.scale = (1, 1, max(0.04, st['h'] * lv)); K._keyxf(pv, frame, loc=False, scl=True)
    fo = st['flame']; fo.location = (st['base'][0], st['base'][1], st['base'][2] + max(0.04, st['h'] * lv) + 0.03); K._keyxf(fo, frame); K._show(fo, lv > 0.02, frame)
    for i, (o, base) in enumerate(S['lampgroups']['candle']):
        f = 1.0 + 0.14 * _noise(frame, i + 1); on = 1.0 if (lv > 0.02 or o.name != 'p_bench') else 0.0
        o.data.energy = base * S['candle_k'] * f * on * K.E2
        if frame is not None: K._key(o.data, 'energy', frame, 'LINEAR')

# ----------------------------------------------------------------------------- foreground dressing is part of the room; per-preset extras
def finish_preset(SET, preset): pass
