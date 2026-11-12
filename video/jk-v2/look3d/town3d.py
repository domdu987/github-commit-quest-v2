"""The town plaza in front of the Guild of Heroes, as a real 3D set (bpy, Cycles CPU), dusk.
World: 1 unit ~ 1 m (characters ~1.8 tall). Z up, plaza floor z = 0, guild facade = plane y = 0 facing -y, x = 0 = guild door.
Light model from the skill's office set (office3d.mat_lit): ambient as emission (blue-violet shade) + one hard warm sun, toon key."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import office3d as S
import tex_town
MB = S.MB

DUSK = dict(shade=(0.21, 0.23, 0.50), key=(2.35, 1.42, 0.62), lift=(0.010, 0.006, 0.024), key_dir=(0.80, 0.52, -0.42), sun_angle=0.6,
            form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.05, grade_offset=(0.004, 0.003, 0.012), grade_saturation=1.12)
A = {}
GAIN = 0.52

def lit(name, img=None, color='#808080', gain=0.9, shade=1.0, alpha=False):
    return S.mat_lit('T_' + name, color=color, image=img, gain=gain * GAIN, shade_mul=shade, alpha=alpha, form=DUSK['form'])

def quad_obj(name, coll, corners, mat, uv=((0, 0), (1, 0), (1, 1), (0, 1)), hull=0.0):
    mb = MB(); mb.face([Vector(c) for c in corners], mat, list(uv)); return mb.obj(name, coll, hull=hull)

def world_sky(scene):
    w = bpy.data.worlds.new('dusk'); scene.world = w; w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground'); tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB'); lp = nt.nodes.new('ShaderNodeLightPath'); mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    e = ramp.color_ramp.elements; e[0].position = 0.0; e[0].color = (*S.hex_lin('#ffc58a'), 1); e[1].position = 0.75; e[1].color = (*S.hex_lin('#41397a'), 1)
    m = e.new(0.12); m.color = (*S.hex_lin('#f08a6e'), 1); m2 = e.new(0.3); m2.color = (*S.hex_lin('#9a5e9a'), 1)
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); nt.links.new(lp.outputs['Is Camera Ray'], mul.inputs[0]); mul.inputs[1].default_value = 1.0
    nt.links.new(mul.outputs[0], bg.inputs['Strength']); nt.links.new(bg.outputs[0], out.inputs[0])
    w.light_settings.distance = 0.001

def window(mb, x, z, y, w, h, M, lit_pane=True, normal='-y', shutters=True, box=False):
    """A window on a wall plane facing -y (normal '-y'), or facing +x / -x ('x+' / 'x-') at wall coordinate y = x position."""
    def P(a, zz, d):   # a along the wall, d out of the wall
        if normal == '-y': return Vector((a, y - d, zz))
        if normal == 'x+': return Vector((y + d, a, zz))
        return Vector((y - d, -a, zz))
    def boxw(a0, a1, z0, z1, d0, d1, mat):
        c = [P(a0, z0, d0), P(a1, z0, d0), P(a1, z1, d0), P(a0, z1, d0), P(a0, z0, d1), P(a1, z0, d1), P(a1, z1, d1), P(a0, z1, d1)]
        lo = Vector((min(v.x for v in c), min(v.y for v in c), min(v.z for v in c))); hi = Vector((max(v.x for v in c), max(v.y for v in c), max(v.z for v in c)))
        mb.box(tuple(lo), tuple(hi), mat)
    a0, a1 = x - w / 2, x + w / 2
    mb.face([P(a0, z, 0.02), P(a1, z, 0.02), P(a1, z + h, 0.02), P(a0, z + h, 0.02)] if normal != 'x-' else [P(a1, z, 0.02), P(a0, z, 0.02), P(a0, z + h, 0.02), P(a1, z + h, 0.02)],
            M['pane_lit' if lit_pane else 'pane_dark'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    t = 0.09
    boxw(a0 - t, a1 + t, z - t, z, 0, 0.14, M['wood']); boxw(a0 - t, a1 + t, z + h, z + h + t, 0, 0.12, M['wood'])
    boxw(a0 - t, a0, z, z + h, 0, 0.12, M['wood']); boxw(a1, a1 + t, z, z + h, 0, 0.12, M['wood'])
    boxw(a0 - 0.12, a1 + 0.12, z - 0.16, z - t, 0, 0.22, M['wood'])   # sill
    if shutters:
        boxw(a0 - t - w * 0.48, a0 - t - 0.02, z, z + h, 0.02, 0.07, M['shutter']); boxw(a1 + t + 0.02, a1 + t + w * 0.48, z, z + h, 0.02, 0.07, M['shutter'])
    if box:   # flower box with flowers
        boxw(a0 - 0.05, a1 + 0.05, z - 0.42, z - 0.16, 0.05, 0.36, M['wood'])
        for i in range(7):
            a = a0 + (i + 0.5) * (a1 - a0) / 7; c = P(a, z - 0.1, 0.2); mb.sphere(tuple(c), 0.09, M[['flower_r', 'flower_y', 'flower_p'][i % 3]], seg=8, rings=5)
            mb.sphere(tuple(P(a + 0.08, z - 0.16, 0.24)), 0.07, M['leaf'], seg=6, rings=4)

def house(coll, name, M, tex, x0, x1, y0, y1, h, facing='-y', roof='roof_r', ridge_h=2.4, wins=(), door=None, chimney=None):
    """Box house with a pitched roof. facing: which side shows the decorated facade ('-y', 'x+', 'x-')."""
    mb = MB(); w = M[tex]
    mb.box((x0, y0, 0), (x1, y1, h), w, tile=(6.0, 6.0))
    # gable roof, ridge parallel to the facade, overhang 0.35
    o = 0.35; rm = M[roof]
    if facing in ('-y', 'y+'):
        ym = (y0 + y1) / 2
        mb.face([Vector((x0 - o, y0 - o, h - 0.15)), Vector((x1 + o, y0 - o, h - 0.15)), Vector((x1 + o, ym, h + ridge_h)), Vector((x0 - o, ym, h + ridge_h))], rm, [(0, 0), (1.6, 0), (1.6, 1.0), (0, 1.0)])
        mb.face([Vector((x1 + o, y1 + o, h - 0.15)), Vector((x0 - o, y1 + o, h - 0.15)), Vector((x0 - o, ym, h + ridge_h)), Vector((x1 + o, ym, h + ridge_h))], rm, [(0, 0), (1.6, 0), (1.6, 1.0), (0, 1.0)])
        mb.face([Vector((x0, y0, h)), Vector((x0, ym, h + ridge_h - 0.1)), Vector((x0, y1, h))], w, [(0, 0), (0.5, 0.4), (1, 0)])
        mb.face([Vector((x1, y1, h)), Vector((x1, ym, h + ridge_h - 0.1)), Vector((x1, y0, h))], w, [(0, 0), (0.5, 0.4), (1, 0)])
    else:
        xm = (x0 + x1) / 2
        mb.face([Vector((x0 - o, y1 + o, h - 0.15)), Vector((x0 - o, y0 - o, h - 0.15)), Vector((xm, y0 - o, h + ridge_h)), Vector((xm, y1 + o, h + ridge_h))], rm, [(0, 0), (1.6, 0), (1.6, 1.0), (0, 1.0)])
        mb.face([Vector((x1 + o, y0 - o, h - 0.15)), Vector((x1 + o, y1 + o, h - 0.15)), Vector((xm, y1 + o, h + ridge_h)), Vector((xm, y0 - o, h + ridge_h))], rm, [(0, 0), (1.6, 0), (1.6, 1.0), (0, 1.0)])
        mb.face([Vector((x1, y0, h)), Vector((xm, y0, h + ridge_h - 0.1)), Vector((x0, y0, h))], w, [(0, 0), (0.5, 0.4), (1, 0)])
        mb.face([Vector((x0, y1, h)), Vector((xm, y1, h + ridge_h - 0.1)), Vector((x1, y1, h))], w, [(0, 0), (0.5, 0.4), (1, 0)])
    # beam ends under the eaves
    for (wx, wz, lit_, box) in wins:
        if facing == '-y': window(mb, wx, wz, y0, 1.0, 1.25, M, lit_, '-y', True, box)
        elif facing == 'x+': window(mb, wx, wz, x1, 1.0, 1.25, M, lit_, 'x+', True, box)
        else: window(mb, wx, wz, x0, 1.0, 1.25, M, lit_, 'x-', True, box)
    if door is not None:
        dx = door
        if facing == '-y': mb.box((dx - 0.6, y0 - 0.03, 0), (dx + 0.6, y0 + 0.02, 2.3), M['door']); mb.box((dx - 0.75, y0 - 0.12, 2.3), (dx + 0.75, y0, 2.45), M['wood'])
        elif facing == 'x+': mb.box((x1 - 0.02, dx - 0.6, 0), (x1 + 0.03, dx + 0.6, 2.3), M['door'])
        else: mb.box((x0 - 0.03, -dx - 0.6, 0), (x0 + 0.02, -dx + 0.6, 2.3), M['door'])
    if chimney:
        cx, cy = chimney; mb.box((cx - 0.35, cy - 0.35, h), (cx + 0.35, cy + 0.35, h + ridge_h + 1.2), M['stone'], tile=(1.5, 1.5)); mb.box((cx - 0.45, cy - 0.45, h + ridge_h + 1.2), (cx + 0.45, cy + 0.45, h + ridge_h + 1.4), M['stone'])
    return mb.obj(name, coll, hull=0.025)

def lantern_post(mb_m, coll, name, x, y, h=3.2, M=None):
    mb = MB(); mb.frustum((x, y, 0), (x, y, h), 0.07, 0.05, M['iron'], seg=8); mb.box((x - 0.18, y - 0.18, 0), (x + 0.18, y + 0.18, 0.25), M['iron'])
    mb.box((x - 0.04, y - 0.04, h - 0.05), (x + 0.42, y + 0.04, h + 0.02), M['iron'])
    lx = x + 0.42; mb.box((lx - 0.2, y - 0.2, h - 0.72), (lx + 0.2, y + 0.2, h - 0.62), M['iron']); mb.frustum((lx, y, h - 0.25), (lx, y, h), 0.24, 0.05, M['iron'], seg=8)
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box((lx + sx * 0.18 - 0.02, y + sy * 0.18 - 0.02, h - 0.62), (lx + sx * 0.18 + 0.02, y + sy * 0.18 + 0.02, h - 0.25), M['iron'])
    ob = mb.obj(name, coll, hull=0.012)
    gl = MB(); gl.box((lx - 0.15, y - 0.15, h - 0.6), (lx + 0.15, y + 0.15, h - 0.27), M['glow']); g = gl.obj(name + '_glass', coll); S.no_bounce(g); g.visible_shadow = False
    return (lx, y, h - 0.45)

def bunting(coll, name, p0, p1, n, M, sag=0.8):
    mb = MB(); p0, p1 = Vector(p0), Vector(p1); cols = ['flag_r', 'flag_y', 'flag_b', 'flag_g', 'flag_w']
    pt = lambda u: p0.lerp(p1, u) + Vector((0, 0, -sag * 4 * u * (1 - u)))
    for i in range(40):
        a, b = pt(i / 40), pt((i + 1) / 40); mb.frustum(tuple(a), tuple(b), 0.012, 0.012, M['iron'], seg=4, cap0=False, cap1=False)
    for i in range(n):
        u0 = (i + 0.15) / n; u1 = (i + 0.85) / n; a, b = pt(u0), pt(u1); m = (a + b) / 2 + Vector((0, 0, -0.45))
        mb.face([a, b, m], M[cols[i % 5]])
    ob = mb.obj(name, coll); return ob

def build(clear=True):
    scene = bpy.context.scene
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True); scene = bpy.context.scene
    S.STATE.clear(); S.STATE['P'] = DUSK
    T = tex_town.build_all()
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    M = dict(
        cob=lit('cob', T['cobbles'], gain=0.95, shade=(1.05, 1.15, 1.25)), guild=lit('guild', T['guild'], gain=0.9, shade=(1.6, 1.3, 1.0), alpha=True),
        house_a=lit('ha', T['house_a'], gain=0.9, shade=(1.5, 1.25, 1.0)), house_b=lit('hb', T['house_b'], gain=0.9, shade=(1.5, 1.25, 1.0)),
        house_c=lit('hc', T['house_c'], gain=0.9, shade=(1.5, 1.25, 1.0)), house_d=lit('hd', T['house_d'], gain=0.9, shade=(1.5, 1.25, 1.0)),
        roof_r=lit('rr', T['roof_r'], gain=0.85, shade=(1.3, 1.1, 1.1)), roof_o=lit('ro', T['roof_o'], gain=0.85, shade=(1.3, 1.1, 1.1)), roof_b=lit('rb', T['roof_b'], gain=0.85, shade=(1.2, 1.1, 1.2)),
        door=lit('door', T['door'], gain=0.75), wood=lit('wood', color='#6a4128', gain=0.75, shade=(1.0, 1.0, 1.1)), planks=lit('planks', T['planks'], gain=0.75),
        shutter=lit('shutter', color='#3f6a5a', gain=0.8), sign=lit('sign', T['sign'], gain=0.85), board=lit('board', T['board'], gain=0.85, shade=(1.5, 1.3, 1.1)),
        shield=lit('shield', T['shield'], gain=0.85, alpha=True), banner=lit('banner', T['banner'], gain=0.85, alpha=True), awning=lit('awning', T['awning'], gain=0.85),
        stone=lit('stone', T['stone'], gain=0.85), water=S.mat_emit('T_water', image=T['water'], strength=0.8), iron=lit('iron', color='#2e2a30', gain=0.6),
        glow=S.mat_emit('T_glow', '#ffcf7a', strength=7.0), pane_lit=S.mat_emit('T_pane_lit', image=T['pane_lit'], strength=1.6), pane_dark=lit('pane_dark', T['pane_dark'], gain=0.7),
        flower_r=lit('fr', color='#e0443a'), flower_y=lit('fy', color='#f2c040'), flower_p=lit('fp', color='#d070c0'), leaf=lit('leaf', color='#4a8a3a'),
        flag_r=lit('flr', color='#d8453a'), flag_y=lit('fly', color='#f0c040'), flag_b=lit('flb', color='#3a6ad0'), flag_g=lit('flg', color='#3aa060'), flag_w=lit('flw', color='#f4ecd8'),
        barrel=lit('barrel', color='#8a5a30', gain=0.8), crate=lit('crate', T['planks'], gain=0.8), bush=lit('bush', color='#5a9a48', gain=0.8, shade=(0.9, 1.1, 1.0)),
        trunk=lit('trunk', color='#5a3a24'), grass=lit('grass', color='#7a8a4a', gain=0.8, shade=(0.9, 1.0, 1.0)), cloth=lit('cloth', color='#e8d8b8'), fruit_r=lit('fruit_r', color='#e04a30'), fruit_o=lit('fruit_o', color='#f0a030'), fruit_g=lit('fruit_g', color='#8ac040'),
    )
    for m in ('glow', 'pane_lit', 'water'): pass
    # --- floor
    mb = MB(); mb.quad((-30, -34, 0), (60, 0, 0), (0, 44, 0), M['cob'], uv=(0, 0, 60 / 4.0, 44 / 4.0)); mb.quad((-90, 10, -0.01), (180, 0, 0), (0, 60, 0), M['grass'], uv=(0, 0, 30, 10)); mb.obj('plaza', coll)
    # --- guild hall
    mb = MB(); W2 = 4.5; G = M['guild']
    mb.face([Vector((-W2, 0, 0)), Vector((W2, 0, 0)), Vector((W2, 0, 6.8)), Vector((0, 0, 10.5)), Vector((-W2, 0, 6.8))], G,
            [(0, 0), (1, 0), (1, 6.8 / 10.5), (0.5, 1), (0, 6.8 / 10.5)])
    mb.box((-W2, 0.0, 0), (-W2 + 0.01, 9, 6.8), M['house_a'], tile=(6, 6)); mb.box((W2 - 0.01, 0.0, 0), (W2, 9, 6.8), M['house_a'], tile=(6, 6))
    o = 0.5
    mb.face([Vector((-W2 - o, -o, 6.8 - 0.4)), Vector((0, -o, 10.5 + 0.1)), Vector((0, 9.5, 10.5 + 0.1)), Vector((-W2 - o, 9.5, 6.8 - 0.4))], M['roof_r'], [(0, 0), (3, 0), (3, 4), (0, 4)])
    mb.face([Vector((0, -o, 10.6)), Vector((W2 + o, -o, 6.4)), Vector((W2 + o, 9.5, 6.4)), Vector((0, 9.5, 10.6))], M['roof_r'], [(0, 0), (3, 0), (3, 4), (0, 4)])
    # barge boards along the gable
    mb.frustum((-W2 - o, -o - 0.05, 6.4), (0, -o - 0.05, 10.6), 0.12, 0.12, M['wood'], seg=6); mb.frustum((0, -o - 0.05, 10.6), (W2 + o, -o - 0.05, 6.4), 0.12, 0.12, M['wood'], seg=6)
    # door: frame, recessed double door, steps
    mb.box((-1.25, -0.28, 0), (-0.95, 0.0, 3.0), M['wood']); mb.box((0.95, -0.28, 0), (1.25, 0.0, 3.0), M['wood']); mb.box((-1.35, -0.32, 3.0), (1.35, 0.0, 3.3), M['wood'])
    mb.box((-0.95, 0.05, 0), (0.0, 0.12, 3.0), M['door']); mb.box((0.0, 0.05, 0), (0.95, 0.12, 3.0), M['door'])
    mb.box((-1.6, -0.9, 0), (1.6, 0.0, 0.16), M['stone'], tile=(1.2, 1.2)); mb.box((-1.4, -0.55, 0.16), (1.4, 0.0, 0.3), M['stone'], tile=(1.2, 1.2))
    for sx in (-0.2, 0.2): mb.sphere((sx, 0.0, 1.55), 0.09, M['iron'], seg=8, rings=5)
    # sign over the door
    mb.box((-2.1, -0.2, 3.45), (2.1, -0.08, 4.3), M['wood']); mb.quad((-2.0, -0.205, 3.5), (4.0, 0, 0), (0, 0, 0.75), M['sign'])
    # ranking board, mounted right of the door
    mb.box((1.65, -0.22, 0.8), (5.0 - 0.6, -0.04, 3.25), M['wood']); mb.quad((1.75, -0.225, 0.9), (2.55, 0, 0), (0, 0, 1.81), M['board'])
    mb.box((1.55, -0.45, 3.25), (4.5, -0.04, 3.38), M['roof_r'])   # little roof over the board
    # windows
    for wx in (-3.6,): window(mb, wx, 1.35, 0.0, 1.0, 1.3, M, True, '-y', True, False)
    for wx in (-3.2, -1.1, 1.1, 3.2): window(mb, wx, 4.65, 0.0, 0.9, 1.25, M, wx in (-1.1, 3.2), '-y', False, True)
    window(mb, 0, 7.4, 0.0, 0.8, 0.9, M, True, '-y', False, False)
    guild = mb.obj('guild', coll, hull=0.03)
    shield = quad_obj('guild_shield', coll, [(-0.65, -0.06, 8.35), (0.65, -0.06, 8.35), (0.65, -0.06, 9.85), (-0.65, -0.06, 9.85)], M['shield'])
    # wall lanterns at the door
    L1 = lantern_post(None, coll, 'lamp_door_l', -1.95, -0.35, 2.9, M); L2 = lantern_post(None, coll, 'lamp_door_r', 1.35 - 0.42 + 0.0, -0.35, 2.9, M) if False else None
    # banners on poles
    for i, bx in enumerate((-5.4, 5.4)):
        mb = MB(); mb.frustum((bx, -0.9, 0), (bx, -0.9, 6.6), 0.08, 0.06, M['wood'], seg=8); mb.sphere((bx, -0.9, 6.7), 0.14, M['flag_y'], seg=8, rings=5)
        mb.box((bx - 0.65, -0.95, 6.15), (bx + 0.65, -0.87, 6.25), M['wood']); mb.obj(f'banner_pole{i}', coll, hull=0.015)
        quad_obj(f'banner{i}', coll, [(bx - 0.6, -0.95, 2.9), (bx + 0.6, -0.95, 2.9), (bx + 0.6, -0.95, 6.15), (bx - 0.6, -0.95, 6.15)], M['banner'])
    # --- houses: back row beside the guild, side rows facing the plaza, a front row behind the camera
    house(coll, 'house_bl', M, 'house_b', -12.5, -5.0, 0.6, 7.0, 5.6, '-y', 'roof_o', 2.6, wins=[(-11, 1.3, True, False), (-8.8, 1.3, False, False), (-11, 3.9, False, True), (-8.8, 3.9, True, True), (-6.6, 3.9, False, True)], door=-6.6, chimney=(-10.5, 4.0))
    house(coll, 'house_br', M, 'house_c', 5.0, 12.0, 0.8, 7.0, 6.2, '-y', 'roof_r', 2.4, wins=[(6.6, 1.3, False, False), (10.4, 1.3, True, False), (6.6, 4.2, True, True), (8.5, 4.2, False, True), (10.4, 4.2, True, True)], door=8.5, chimney=(10.8, 3.5))
    house(coll, 'house_l1', M, 'house_a', -20, -13.2, -9.5, -1.0, 6.0, 'x+', 'roof_r', 2.5, wins=[(-2.6, 1.3, True, False), (-7.5, 1.3, False, False), (-2.6, 4.0, False, True), (-5.0, 4.0, True, True), (-7.5, 4.0, False, True)], door=-5.0, chimney=(-17, -6))
    house(coll, 'house_l2', M, 'house_d', -19, -13.0, -19.5, -10.2, 5.2, 'x+', 'roof_o', 2.4, wins=[(-12, 1.3, False, False), (-17.5, 1.3, True, False), (-12, 3.6, True, True), (-15, 3.6, False, True), (-17.5, 3.6, True, True)], door=-15.0)
    house(coll, 'house_r1', M, 'house_d', 13.0, 20, -9.5, -1.0, 5.6, 'x-', 'roof_b', 2.6, wins=[(2.6, 1.3, False, False), (7.5, 1.3, True, False), (2.6, 3.9, True, True), (5.0, 3.9, False, True), (7.5, 3.9, True, True)], door=5.0, chimney=(17, -4))
    house(coll, 'house_r2', M, 'house_a', 13.4, 20, -19.5, -10.2, 6.4, 'x-', 'roof_r', 2.4, wins=[(12, 1.3, True, False), (17.5, 1.3, False, False), (12, 4.3, False, True), (15, 4.3, True, True), (17.5, 4.3, False, True)], door=15.0)
            # back skyline beyond the guild: a few taller roofs
    house(coll, 'house_far1', M, 'house_d', -9, -2.5, 11, 17, 8.0, '-y', 'roof_b', 3.0, wins=[(-7.5, 5.2, True, False), (-4.5, 5.2, True, False)])
    house(coll, 'house_far2', M, 'house_c', 3, 10, 12, 18, 7.4, '-y', 'roof_o', 3.0, wins=[(5, 4.8, True, False), (8, 4.8, False, False)])
    # --- fountain
    mb = MB(); fx, fy = -7.2, -7.5
    mb.frustum((fx, fy, 0), (fx, fy, 0.65), 2.0, 2.0, M['stone'], seg=28, cap1=False); mb.frustum((fx, fy, 0.65), (fx, fy, 0.78), 2.1, 2.1, M['stone'], seg=28)
    mb.frustum((fx, fy, 0.3), (fx, fy, 1.7), 0.32, 0.22, M['stone'], seg=12); mb.frustum((fx, fy, 1.7), (fx, fy, 1.85), 0.95, 0.75, M['stone'], seg=18); mb.frustum((fx, fy, 1.85), (fx, fy, 2.6), 0.16, 0.12, M['stone'], seg=10)
    mb.sphere((fx, fy, 2.7), 0.2, M['stone'], seg=10, rings=6); mb.obj('fountain', coll, hull=0.02)
    wt = MB(); wt.frustum((fx, fy, 0.55), (fx, fy, 0.6), 1.92, 1.92, M['water'], seg=28, cap0=False); w = wt.obj('fountain_water', coll); S.no_bounce(w)
    # --- market stall with an awning, fruit crates
    mb = MB(); sx, sy = 9.0, -8.5
    for dx in (-1.6, 1.6):
        for dy in (-0.9, 0.9): mb.box((sx + dx - 0.07, sy + dy - 0.07, 0), (sx + dx + 0.07, sy + dy + 0.07, 2.5), M['wood'])
    mb.box((sx - 1.7, sy - 1.0, 0.9), (sx + 1.7, sy + 1.0, 1.05), M['planks'])
    mb.face([Vector((sx - 1.9, sy - 1.5, 2.3)), Vector((sx + 1.9, sy - 1.5, 2.3)), Vector((sx + 1.9, sy + 1.0, 2.8)), Vector((sx - 1.9, sy + 1.0, 2.8))], M['awning'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    for i in range(9):
        cx = sx - 1.4 + i * 0.35
        for j in range(2): mb.sphere((cx, sy - 0.6 + j * 0.5, 1.15), 0.12, M[['fruit_r', 'fruit_o', 'fruit_g'][(i + j) % 3]], seg=8, rings=5)
    mb.obj('stall', coll, hull=0.015)
    # --- barrels, crates, bushes, a tree
    mb = MB()
    for (bx, by) in ((-3.6, -1.4), (-3.0, -1.6), (5.6, -1.6), (12.2, -11.5), (-12.3, -12.5)):
        mb.frustum((bx, by, 0), (bx, by, 0.45), 0.36, 0.42, M['barrel'], seg=14, cap0=False, cap1=False); mb.frustum((bx, by, 0.45), (bx, by, 0.9), 0.42, 0.36, M['barrel'], seg=14, cap0=False)
        for z in (0.12, 0.45, 0.78): mb.frustum((bx, by, z - 0.03), (bx, by, z + 0.03), 0.43, 0.43, M['iron'], seg=14, cap0=False, cap1=False)
    for (cx, cy, s) in ((6.2, -1.3, 0.7), (6.9, -1.4, 0.6), (6.5, -1.3, 0.55), (-12.5, -14, 0.8), (11.6, -7.0, 0.7)):
        z0 = 0.7 if (cx, cy) == (6.5, -1.3) else 0.0; mb.box((cx - s / 2, cy - s / 2, z0), (cx + s / 2, cy + s / 2, z0 + s), M['crate'])
    mb.obj('props', coll, hull=0.015)
    mb = MB()
    for (bx, by, r) in ((-4.6, -0.7, 0.6), (4.75, -0.8, 0.55), (-12.8, -3.5, 0.8), (12.8, -3.8, 0.75)):
        mb.sphere((bx, by, r * 0.8), r, M['bush'], seg=12, rings=8); mb.sphere((bx + r * 0.6, by - 0.1, r * 0.6), r * 0.7, M['bush'], seg=10, rings=6)
    tx, ty = -10.5, -17.0; mb.frustum((tx, ty, 0), (tx, ty, 3.0), 0.25, 0.18, M['trunk'], seg=10)
    for (dx, dy, dz, r) in ((0, 0, 4.0, 1.7), (1.0, 0.3, 3.4, 1.2), (-1.0, -0.2, 3.5, 1.3), (0.2, -0.6, 4.8, 1.1)): mb.sphere((tx + dx, ty + dy, dz), r, M['bush'], seg=14, rings=9)
    mb.obj('greens', coll, hull=0.02)
    # lantern posts on the plaza
    lamps = [lantern_post(None, coll, f'lamp{i}', x, y, 3.3, M) for i, (x, y) in enumerate(((-3.8, -4.2), (3.6, -4.4), (-11.5, -11.5), (11.0, -12.5)))]
    # bunting from the guild gable to the houses
    bunting(coll, 'bunt0', (-4.4, -0.3, 6.6), (-12.4, 0.0, 5.4), 14, M, 0.9)
    bunting(coll, 'bunt1', (4.4, -0.3, 6.6), (12.0, 0.2, 6.0), 14, M, 0.9)
    bunting(coll, 'bunt2', (-13.2, -4.0, 5.6), (13.0, -4.5, 5.4), 30, M, 1.6)
    # far backdrop: sky card behind the town (emission, camera rays only)
    sky = S.mat_emit('T_sky', image=T['sky'], strength=1.0, camera_only=True)
    mb = MB(); R = 70.0; nseg = 24
    for i in range(nseg):
        a0 = math.radians(-160 + 140 * i / nseg); a1 = math.radians(-160 + 140 * (i + 1) / nseg)
        p0 = Vector((R * math.cos(a0 + math.pi), R * -math.sin(a0 + math.pi), -2)); p1 = Vector((R * math.cos(a1 + math.pi), R * -math.sin(a1 + math.pi), -2))
    # simpler: one wide curved strip around the back (+y) half
    for i in range(nseg):
        a0 = math.radians(200 + 140 * i / nseg); a1 = math.radians(200 + 140 * (i + 1) / nseg)
        c0 = Vector((R * math.cos(a0), R * -math.sin(a0) , 0)); c1 = Vector((R * math.cos(a1), R * -math.sin(a1), 0))
        mb.face([c0 + Vector((0, 0, -3)), c1 + Vector((0, 0, -3)), c1 + Vector((0, 0, 75)), c0 + Vector((0, 0, 75))], sky, [(i / nseg, 0), ((i + 1) / nseg, 0), ((i + 1) / nseg, 1), (i / nseg, 1)])
    bd = mb.obj('backdrop', coll); bd.visible_shadow = False
    for ob in coll.objects: S.no_bounce(ob)
    # sun
    sd = bpy.data.lights.new('key_sun', 'SUN'); sd.energy = math.pi * max(DUSK['key']); sd.color = tuple(c / max(DUSK['key']) for c in DUSK['key']); sd.angle = math.radians(DUSK['sun_angle'])
    sd.use_shadow = True; so = bpy.data.objects.new('key_sun', sd); lc.objects.link(so)
    so.rotation_euler = Vector(DUSK['key_dir']).normalized().to_track_quat('-Z', 'Y').to_euler()
    world_sky(scene); S.setup_render(scene, 'final'); scene.render.use_persistent_data = False; S.setup_grade(scene, bloom=True)
    A.update(dict(door=(0, -0.6, 0), board=(3.0, -0.25, 2.1), fountain=(fx, fy, 0), lamps=lamps, stall=(sx, sy, 0)))
    return A

if __name__ == '__main__':
    import time
    build(); scene = bpy.context.scene
    q = sys.argv[1] if len(sys.argv) > 1 else 'preview'
    if q == 'preview': scene.render.resolution_percentage = 50; scene.cycles.samples = 8
    cams = dict(wide_high=dict(loc=(2, -30, 14), look_at=(0, -2, 2.5)), two_eye=dict(loc=(1.5, -9.5, 1.7), look_at=(0.6, 0, 2.6)), low=dict(loc=(-1.5, -6.5, 0.5), look_at=(0.5, 0, 3.8)),
                rev=dict(loc=(0, -2, 1.8), look_at=(0, -20, 2.5)))
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    for nm, c in cams.items():
        S.make_camera(dict(c, lens=22), name='cam'); t = time.time(); S.render(os.path.join(out, f'set_{nm}.png')); print(nm, round(time.time() - t, 1), 's')
