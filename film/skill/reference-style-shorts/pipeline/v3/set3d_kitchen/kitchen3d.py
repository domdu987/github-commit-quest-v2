#!/usr/bin/env python3
"""kitchen3d.py : a table corner by a four-pane window in a Long Island cottage, 1938 (shots 15 and 26). bpy 5.3, Cycles CPU.

Built the way the office is built: office3d's light model and helpers (mat_lit, mat_emit, mat_card, mat_ink, MB, add_hull,
no_bounce, setup_render, setup_grade, make_camera) are imported, not copied; only what the one planned camera sees exists.

    import kitchen3d as K
    A = K.build('kitchen_grey')          # or 'kitchen_storm'  -> anchors (cams, wb_centre, cup_rest, ...)
    K.set_state(g=..., cup=(x, y, z_lift, tilt), ripple=(phase, amp), steam=k, window=('drizzle', k), flutter=(t, amp),
                bleed=None | k, lightning=0..1, crack=None | k, chair=0..1)
World: 1 unit = 1 D, Z up, window wall = plane y = 0, room toward -y, table top z = 1.30. See API.md."""
import os, sys, math, json, time
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'paper')); sys.path.insert(0, HERE)
import office3d as S                                    # noqa: E402  light model, materials, mesh builder, render helpers
import kitchen_tex as KT                                # noqa: E402
OTEX = os.path.join(PROJ, 'v3', 'set3d', 'tex')
_PREG_PATH = os.path.join(PROJ, 'v3', 'paper', 'tex', 'registry.json')
if not os.path.exists(_PREG_PATH):
    raise FileNotFoundError(_PREG_PATH + ': the paper artwork is not built. Run `python3 v3/paper/paper.py build` first (examples/setup_kit.sh does it).')
PREG = json.load(open(_PREG_PATH))

TOP = 1.30                                              # table top
WIN = dict(x0=KT.WIN['x0'], x1=KT.WIN['x1'], z0=KT.WIN['z0'], z1=KT.WIN['z1'], mull=0.5 * (KT.WIN['x0'] + KT.WIN['x1']), tran=0.5 * (KT.WIN['z0'] + KT.WIN['z1']))
PS = 0.9                                                # newspaper scale: the page is 1.5 x 1.95 D in the registry -> 1.35 x 1.755 D
PAPER = dict(cx=0.0, foot_y=-1.15, lip=0.075, alpha=62.0, nu=24, nv=30)   # folded front page: lower half, leaning back on the coffee pot
CUP_REST = (0.38, -1.40)                                # saucer centre on the table (it pins the paper's bottom-right corner)

PRESETS = {
    # dull drizzle morning: soft cool key from the unseen room side (front-left, high), blue-violet ambient, bright grey window
    'kitchen_grey': dict(shade=(0.25, 0.27, 0.52), key=(0.56, 0.53, 0.54), lift=(0.002, 0.003, 0.014), key_dir=(0.42, 0.62, -0.66), sun_angle=2.0,
                         form=(0.10, -0.05, 0.22), falloff_y=1.3, bloom_size=0.05, grade_offset=(0.002, 0.003, 0.004), grade_saturation=1.22,
                         window=1.0, flash=0.0, wall_shade=(1.9, 1.5, 0.9), wood_shade=(0.9, 0.95, 1.1)),
    # storm: the room almost dark, deep blue-violet ambient, a weak key; lightning = a second sun through the window pulsed per frame
    'kitchen_storm': dict(shade=(0.050, 0.072, 0.20), key=(0.28, 0.20, 0.125), lift=(0.001, 0.002, 0.008), key_dir=(0.42, 0.62, -0.66), sun_angle=4.0,
                          form=(0.10, -0.05, 0.22), falloff_y=1.2, bloom_size=0.05, grade_offset=(0.0, 0.002, 0.007), grade_saturation=1.15,
                          window=0.85, flash=3.2, cloth_shade=(2.2, 1.3, 0.55), flash_dir=(-0.15, -0.75, -0.62), wall_shade=(2.6, 1.5, 0.55), wood_shade=(1.8, 1.15, 0.55)),
}
ST = {}

# ----------------------------------------------------------------------------- materials
def _coffee_mat(name):
    """Black coffee: unlit (camera only) dark brown with a ring pattern whose phase and amplitude are set per frame."""
    m = bpy.data.materials.new(name); nt = m.node_tree; [nt.nodes.remove(n) for n in list(nt.nodes)]; L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission')
    tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.rings_direction = 'SPHERICAL'
    wv.wave_profile = 'SIN'; wv.inputs['Scale'].default_value = 22.0; wv.inputs['Distortion'].default_value = 0.0
    L(tc.outputs['Object'], wv.inputs['Vector'])
    mp = nt.nodes.new('ShaderNodeMapRange'); mp.inputs['From Min'].default_value = 0.55; mp.inputs['From Max'].default_value = 1.0
    L(wv.outputs['Fac'], mp.inputs['Value'])
    amp = nt.nodes.new('ShaderNodeMath'); amp.operation = 'MULTIPLY'; amp.inputs[1].default_value = 0.0; amp.name = 'amp'; L(mp.outputs['Result'], amp.inputs[0])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = (*S.hex_lin('#22130a'), 1); mx.inputs[7].default_value = (*S.hex_lin('#8a5c3a'), 1)
    L(amp.outputs[0], mx.inputs[0]); L(mx.outputs[2], emi.inputs['Color'])
    lp = nt.nodes.new('ShaderNodeLightPath'); L(lp.outputs['Is Camera Ray'], emi.inputs['Strength'])
    L(emi.outputs['Emission'], out.inputs['Surface']); wv.name = 'wave'
    return m

def _seq_mat(name, png, strength=1.0, alpha=False, camera_only=True):
    """Unlit image card whose image is swapped per frame (window views, steam, crack, the bleed frames)."""
    m = S.mat_emit(name, image=png, strength=strength, alpha=alpha)
    if camera_only:
        nt = m.node_tree; emi = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeEmission'][0]
        lp = nt.nodes.new('ShaderNodeLightPath'); mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = strength; mu.name = 'str'
        nt.links.new(lp.outputs['Is Camera Ray'], mu.inputs[0]); nt.links.new(mu.outputs[0], emi.inputs['Strength'])
    return m

def _set_image(mat, png):
    for n in mat.node_tree.nodes:
        if n.bl_idname == 'ShaderNodeTexImage':
            if n.image is None or bpy.path.abspath(n.image.filepath) != png:
                n.image = bpy.data.images.load(png, check_existing=True)
            return

# ----------------------------------------------------------------------------- geometry helpers
def _ring_handle(mb, c, r, tube, mat, seg=10, ring=8):
    """Half ring (cup handle) in the xz plane on the +x side of point c: one continuous swept tube (clean ink hull)."""
    mb.pid += 1; R = []
    for i in range(seg + 1):
        th = math.pi * i / seg; ctr = Vector((c[0] + r * math.sin(th), c[1], c[2] + r * math.cos(th)))
        rad = Vector((math.sin(th), 0, math.cos(th))); ax = Vector((0, 1, 0))
        R.append([ctr + tube * (math.cos(2 * math.pi * k / ring) * rad + math.sin(2 * math.pi * k / ring) * ax) for k in range(ring)])
    for i in range(seg):
        for k in range(ring):
            k2 = (k + 1) % ring; mb.face([R[i][k], R[i][k2], R[i + 1][k2], R[i + 1][k]], mat)

def paper_points(t_flutter=0.0, amp=0.0):
    """Vertices (nu+1)x(nv+1) of the folded front page, row j along the page from its bottom edge (j = 0) to the fold, and the UV
    of each. The bottom margin lies flat on the table (lip), then the page leans back at alpha onto the coffee pot. Flutter lifts
    the free top-left corner and runs a small wave across the sheet (amp in D)."""
    W = 1.5 * PS; Hh = 0.975 * PS; nu, nv = PAPER['nu'], PAPER['nv']; a = math.radians(PAPER['alpha']); lip = PAPER['lip']
    V = []; UV = []
    for j in range(nv + 1):
        s = Hh * j / nv
        if s <= lip: y, z, nrm = PAPER['foot_y'] - (lip - s), TOP + 0.0025, Vector((0, 0, 1))
        else:
            q = s - lip; bend = 0.05
            ang = a * min(1.0, q / bend) if q < bend else a
            # short rounded bend from flat to the lean angle
            if q < bend:
                y = PAPER['foot_y'] + sum(math.cos(a * min(1, (i + 0.5) / 8)) for i in range(int(8 * q / bend))) * bend / 8
                z = TOP + 0.0025 + sum(math.sin(a * min(1, (i + 0.5) / 8)) for i in range(int(8 * q / bend))) * bend / 8
            else:
                y0 = PAPER['foot_y'] + sum(math.cos(a * (i + 0.5) / 8) for i in range(8)) * bend / 8
                z0 = TOP + 0.0025 + sum(math.sin(a * (i + 0.5) / 8) for i in range(8)) * bend / 8
                y = y0 + (q - bend) * math.cos(a); z = z0 + (q - bend) * math.sin(a)
            nrm = Vector((0, -math.sin(ang), math.cos(ang)))
        for i in range(nu + 1):
            u = i / nu; x = PAPER['cx'] - W / 2 + W * u
            p = Vector((x, y, z))
            if amp > 0 and s > lip:
                f = (s - lip) / (Hh - lip)
                w = amp * (0.35 * math.sin(2 * math.pi * (1.7 * t_flutter - 1.3 * u) ) * f ** 1.5 + 0.9 * max(0.0, 1 - u * 2.2) ** 2 * f ** 2 * (0.6 + 0.4 * math.sin(2 * math.pi * 2.3 * t_flutter)))
                p = p + nrm * w
            V.append(p); UV.append((u, 0.5 * j / nv))
    return V, UV

def wb_point(u_page, y_page):
    """World point of the front page at page coordinates (D, page 1.5 x 1.95, y down from the masthead), on the visible half."""
    V, UV = paper_points(); nu, nv = PAPER['nu'], PAPER['nv']
    fu = u_page / 1.5 * nu; fv = (1.95 - y_page) / 0.975 * nv
    i0, j0 = min(nu - 1, int(fu)), min(nv - 1, int(fv)); du, dv = fu - i0, fv - j0
    P = lambda i, j: V[j * (nu + 1) + i]
    return tuple((P(i0, j0) * (1 - du) + P(i0 + 1, j0) * du) * (1 - dv) + (P(i0, j0 + 1) * (1 - du) + P(i0 + 1, j0 + 1) * du) * dv)

# ----------------------------------------------------------------------------- build
def build(light='kitchen_grey'):
    scene = bpy.context.scene
    for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    P = dict(PRESETS[light]); S.STATE.clear(); S.STATE['P'] = P; S.STATE['preset'] = light; ST.clear(); ST['light'] = light; ST['P'] = P
    SET = S._coll('SET', scene); LIGHTS = S._coll('LIGHTS', scene)
    tx = KT.ensure()
    w = bpy.data.worlds.get('W_kitchen') or bpy.data.worlds.new('W_kitchen'); scene.world = w; nt = S._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    S.setup_render(scene, 'final')
    FORM = tuple(P['form']); pre = light + '_'
    def C(hexcol, gain=0.9, sm=1.0, form=True): return S.mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol, gain, str(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None)
    def TXM(name, png, gain=0.9, sm=1.0, alpha=False, form=True): return S.mat_lit('%st_%s' % (pre, name), image=png, gain=gain, shade_mul=sm, alpha=alpha, form=FORM if form else None)
    ws, wd = P['wall_shade'], P['wood_shade']
    M = dict(wall=TXM('kwall', tx['kwall'], 0.85, ws), wains=TXM('wainscot', os.path.join(OTEX, 'wainscot.png'), 0.85, wd),
             wood=C('#7b3b26', 0.9, wd), frame=C('#8a4a2a', 0.9, wd), dark=C('#3d1c12', 0.9, 1.25), cloth=TXM('oilcloth', tx['oilcloth'], 0.72, P.get('cloth_shade', (1.4, 1.2, 0.7)), form=False),
             curtain=TXM('curtain', tx['curtain'], 0.85, (1.2, 1.1, 1.0), form=False), cream=C('#f1e4cb', 0.85, (1.25, 1.15, 1.0)), navy=C('#2e4686', 0.9, 1.2),
             pot=C('#b8322a', 0.85, (1.4, 1.1, 1.0)), potrim=C('#f1e4cb', 0.85), steel=C('#9aa0ae', 0.85), floor=TXM('planks', os.path.join(OTEX, 'planks.png'), 0.9, (1.06, 1.2, 1.3), form=False),
             paperback=C('#efe2c8', 0.8, (1.2, 1.1, 1.0)), brass=C('#c89a3c', 0.8))
    hull = lambda d: 0.00384 * d                           # 3 px ink at distance d (office rule)
    MB = S.MB

    # ---- window wall with the opening, wainscot under the sill, reveal, sill, frame, glazing bars
    XL, XR, ZT = -2.6, 2.8, 4.4; Z_RAIL = 1.62
    mb = MB(); wx0, wx1, wz0, wz1 = WIN['x0'] - 0.10, WIN['x1'] + 0.10, WIN['z0'] - 0.08, WIN['z1'] + 0.10   # opening with its frame
    def wq(x0, x1, z0, z1, mat, tu, tv):
        mb.quad((x0, 0.0, z0), (x1 - x0, 0, 0), (0, 0, z1 - z0), mat, (x0 / tu, z0 / tv, x1 / tu, z1 / tv))
    wq(XL, XR, 0.0, Z_RAIL, M['wains'], 0.76, 1.02)
    wq(XL, wx0, Z_RAIL, ZT, M['wall'], 0.4, 0.6); wq(wx1, XR, Z_RAIL, ZT, M['wall'], 0.4, 0.6)
    wq(wx0, wx1, Z_RAIL, wz0, M['wall'], 0.4, 0.6); wq(wx0, wx1, wz1, ZT, M['wall'], 0.4, 0.6)
    t = 0.2                                                 # reveal (thick wall) around the opening
    mb.quad((wx0, 0, wz0), (0, t, 0), (0, 0, wz1 - wz0), M['wall']); mb.quad((wx1, t, wz0), (0, -t, 0), (0, 0, wz1 - wz0), M['wall'])
    mb.quad((wx0, t, wz1), (wx1 - wx0, 0, 0), (0, -t, 0), M['wall']); mb.quad((wx0, 0, wz0), (wx1 - wx0, 0, 0), (0, t, 0), M['wall'])
    wall = mb.obj('wall', SET)
    mb = MB(); mb.box((XL, -0.05, Z_RAIL - 0.02), (XR, 0.0, Z_RAIL + 0.05), M['wood']); mb.obj('chair_rail', SET, hull=hull(2.6))
    mb = MB(); f = 0.07; fy0, fy1 = 0.06, 0.13
    x0, x1, z0, z1 = WIN['x0'], WIN['x1'], WIN['z0'], WIN['z1']
    mb.box((x0 - f, fy0, z0 - f), (x0, fy1, z1 + f), M['frame']); mb.box((x1, fy0, z0 - f), (x1 + f, fy1, z1 + f), M['frame'])
    mb.box((x0, fy0, z1), (x1, fy1, z1 + f), M['frame']); mb.box((x0, fy0, z0 - f), (x1, fy1, z0), M['frame'])
    mb.box((WIN['mull'] - 0.03, fy0 + 0.01, z0), (WIN['mull'] + 0.03, fy1 - 0.01, z1), M['frame'])
    mb.box((x0, fy0 + 0.01, WIN['tran'] - 0.03), (x1, fy1 - 0.01, WIN['tran'] + 0.03), M['frame'])
    mb.box((wx0 - 0.06, -0.17, wz0 - 0.06), (wx1 + 0.06, 0.06, wz0 + 0.0), M['frame'])          # sill board
    mb.box((wx0 - 0.02, -0.04, wz0 - 0.20), (wx1 + 0.02, 0.0, wz0 - 0.06), M['wood'])          # apron
    mb.obj('window', SET, hull=hull(2.4))
    ex = KT.EXT; mb = MB(); emat = _seq_mat(pre + 'ext', tx['drizzle'][0], strength=P['window'])
    mb.quad((ex['x0'], ex['y'], ex['z0']), (ex['x1'] - ex['x0'], 0, 0), (0, 0, ex['z1'] - ex['z0']), emat, (0, 0, 1, 1)); o = mb.obj('exterior', SET); o.visible_shadow = False
    ST['ext_mat'] = emat
    # crack card on the lower-right pane, just inside the glass plane
    cw = 0.42; mb = MB(); cmat = _seq_mat(pre + 'crack', tx['crack'][0], strength=1.0, alpha=True)
    mb.quad((WIN['mull'] + 0.06, 0.095, WIN['z0'] + 0.04), (cw, 0, 0), (0, 0, cw), cmat, (0, 0, 1, 1)); o = mb.obj('crack', SET); o.visible_shadow = False; o.hide_render = True
    ST['crack_mat'] = cmat
    # curtains: folded panels hanging from a rod, tied back
    def curtain(name, xa, xb, flip):
        mb = MB(); n = 10; za, zb = WIN['z0'] - 0.18, WIN['z1'] + 0.22
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n
            for (ua, ub) in ((u0, u1),):
                xa_, xb_ = xa + (xb - xa) * ua, xa + (xb - xa) * ub
                ya, yb_ = -0.10 - 0.05 * math.sin(math.pi * 2 * ua * n / 2) ** 2, -0.10 - 0.05 * math.sin(math.pi * 2 * ub * n / 2) ** 2
                # waist: the panel is pinched at 0.35 of its height (tie-back)
                pts = [];
                mb.face([(xa_, ya, za), (xb_, yb_, za), (xb_, yb_, zb), (xa_, ya, zb)], M['curtain'], [(ua, 0), (ub, 0), (ub, 1), (ua, 1)])
        ob = mb.obj(name, SET, hull=hull(2.4)); return ob
    curtain('curtain_l', WIN['x0'] - 0.20, WIN['x0'] - 0.02, False); curtain('curtain_r', WIN['x1'] + 0.02, WIN['x1'] + 0.34, True)
    mb = MB(); mb.frustum((WIN['x0'] - 0.26, -0.12, WIN['z1'] + 0.24), (WIN['x1'] + 0.42, -0.12, WIN['z1'] + 0.24), 0.018, 0.018, M['brass'], seg=8)
    for xx in (WIN['x0'] - 0.26, WIN['x1'] + 0.42): mb.sphere((xx, -0.12, WIN['z1'] + 0.24), 0.035, M['brass'], seg=10, rings=6)
    mb.obj('rod', SET, hull=hull(2.4))
    # calendar pad 21 on the wall right of the window (the paper registry's art)
    cal = PREG['calendar_pad_21']; cws, chs = cal['size_D'][0] * 0.42, cal['size_D'][1] * 0.42
    mb = MB(); cx0 = WIN['x0'] - 0.62; cz0 = 2.10
    mb.box((cx0 - 0.01, -0.02, cz0 - 0.01), (cx0 + cws + 0.01, 0.0, cz0 + chs + 0.01), M['dark']); mb.obj('calendar_block', SET, hull=hull(2.6))
    mb = MB(); mb.quad((cx0, -0.022, cz0), (cws, 0, 0), (0, 0, chs), TXM('calendar', cal['png'], 0.8, (1.2, 1.1, 1.0), alpha=True), (0, 0, 1, 1)); mb.obj('calendar_face', SET)
    # floor (only seen at the very bottom in the wide steps)
    mb = MB(); mb.quad((-3, -4.5, 0), (6, 0, 0), (0, 4.5, 0), M['floor'], (-3 / 1.0, -4.5 / 6.0, 3 / 1.0, 0)); mb.obj('floor', SET)

    # ---- table with the red-check oilcloth (top + hanging drop), legs
    tx0, tx1, ty0, ty1 = -1.6, 0.98, -1.95, -0.02
    mb = MB(); mb.quad((tx0, ty0, TOP), (tx1 - tx0, 0, 0), (0, ty1 - ty0, 0), M['cloth'], (tx0 / 0.6, ty0 / 0.6, tx1 / 0.6, ty1 / 0.6))
    mb.quad((tx0, ty0 - 0.012, TOP - 0.24), (tx1 - tx0, 0, 0), (0, 0, 0.24), M['cloth'], (tx0 / 0.6, 0, tx1 / 0.6, 0.4))
    mb.quad((tx1 + 0.012, ty0, TOP - 0.24), (0, ty1 - ty0, 0), (0, 0, 0.24), M['cloth'], (ty0 / 0.6, 0, ty1 / 0.6, 0.4))
    mb.quad((tx0, ty0 - 0.012, TOP), (tx1 - tx0, 0, 0), (0, 0.012, 0), M['cloth']); mb.quad((tx1, ty0, TOP), (0.012, 0, 0), (0, ty1 - ty0, 0), M['cloth'])
    mb.obj('table_top', SET, hull=hull(1.6))
    mb = MB()
    for (lx, ly) in ((tx0 + 0.1, ty0 + 0.1), (tx1 - 0.1, ty0 + 0.1), (tx1 - 0.1, ty1 - 0.1)): mb.box((lx - 0.05, ly - 0.05, 0), (lx + 0.05, ly + 0.05, TOP - 0.24), M['wood'])
    mb.obj('table_legs', SET, hull=hull(2.0))

    # ---- bread box (stained wood, rounded lid) that the folded paper leans on
    mb = MB(); bx0, bx1, by0, by1 = -0.55, 0.45, -0.66, -0.12; bz = TOP + 0.70
    mb.box((bx0, by0, TOP), (bx1, by1, bz), C('#8a4a2a', 0.9, wd), mats=dict(top=C('#a85e34', 0.9, wd)))
    mb.box((bx0 - 0.02, by0 - 0.02, bz), (bx1 + 0.02, by1 + 0.02, bz + 0.06), C('#6e3520', 0.9, wd))
    mb.box((-0.12, by0 - 0.04, bz - 0.16), (0.02, by0, bz - 0.11), M['brass'])
    mb.obj('bread_box', SET, hull=hull(2.0))
    # ---- the folded newspaper (front page, lower half shows: the weather box) and its folded-back upper half
    V, UV = paper_points(); nu, nv = PAPER['nu'], PAPER['nv']
    news = PREG['newspaper']['png']; pm = S.mat_lit(pre + 'news', image=news, gain=0.62, shade_mul=(1.3, 1.15, 0.85), form=None)
    me = bpy.data.meshes.new('newspaper'); faces = [(j * (nu + 1) + i, j * (nu + 1) + i + 1, (j + 1) * (nu + 1) + i + 1, (j + 1) * (nu + 1) + i) for j in range(nv) for i in range(nu)]
    me.from_pydata([tuple(v) for v in V], [], faces); me.update(); uvl = me.uv_layers.new(name='UVMap'); k = 0
    for fc in faces:
        for vi in fc: uvl.data[k].uv = UV[vi]; k += 1
    me.materials.append(pm); np_ = bpy.data.objects.new('newspaper', me); SET.objects.link(np_); S.add_hull(np_, 0.004)
    ST['paper'] = np_; ST['paper_mat'] = pm; ST['paper_png'] = news
    fold = V[nv * (nu + 1)]; W = 1.5 * PS
    mb = MB(); mb.quad((PAPER['cx'] - W / 2, fold.y + 0.012, fold.z - 0.01), (W, 0, 0), (0, 0.30, -0.62), M['paperback']); mb.obj('newspaper_back', SET, hull=0.004)

    # ---- cup, saucer, spoon (their own object: it moves), coffee disc, steam card
    mb = MB(); cr = M['cream']
    mb.frustum((0, 0, 0.0), (0, 0, 0.022), 0.15, 0.205, cr, seg=28); mb.frustum((0, 0, 0.022), (0, 0, 0.030), 0.205, 0.205, cr, seg=28, cap0=False)
    mb.obj('saucer', SET, hull=hull(1.6))
    mb = MB(); h = 0.17
    mb.frustum((0, 0, 0.026), (0, 0, 0.026 + h), 0.085, 0.125, cr, seg=28, cap1=False)
    mb.frustum((0, 0, 0.026 + h - 0.028), (0, 0, 0.026 + h), 0.120, 0.126, M['navy'], seg=28, cap0=False, cap1=False)
    mb.frustum((0, 0, 0.026 + h), (0, 0, 0.026 + h - 0.12), 0.118, 0.090, M['cream'], seg=28, cap0=False, cap1=True)   # inner wall
    _ring_handle(mb, (0.105, 0, 0.026 + h * 0.52), 0.06, 0.02, cr, seg=10); cup = mb.obj('cup', SET, hull=hull(1.6))
    mb = MB(); mb.frustum((0, 0, 0.026 + h - 0.03), (0, 0, 0.026 + h - 0.0295), 0.112, 0.112, M['dark'], seg=40, cap0=False)
    cmat = _coffee_mat(pre + 'coffee'); mb.face([Vector((0.112 * math.cos(2 * math.pi * i / 40), 0.112 * math.sin(2 * math.pi * i / 40), 0.026 + h - 0.03)) for i in range(40)], cmat)
    coffee = mb.obj('coffee', SET); coffee.visible_shadow = False
    mb = MB(); mb.box((-0.17, -0.012, 0.03), (-0.02, 0.012, 0.038), M['steel']); mb.box((-0.24, -0.03, 0.03), (-0.165, 0.03, 0.042), M['steel']); mb.obj('spoon', SET, hull=0.003)
    smat = _seq_mat(pre + 'steam', tx['steam'][0], strength=0.9, alpha=True)
    mb = MB(); mb.quad((-0.12, 0, 0.16), (0.24, 0, 0), (0, 0, 0.48), smat, (0, 0, 1, 1)); steam = mb.obj('steam', SET); steam.visible_shadow = False
    ST['steam_mat'] = smat; ST['coffee_mat'] = cmat
    rig = bpy.data.objects.new('cup_rig', None); SET.objects.link(rig)
    for ob in (cup, coffee, steam): ob.parent = rig
    sau = bpy.data.objects.new('saucer_rig', None); SET.objects.link(sau)
    for ob in (bpy.data.objects['saucer'], bpy.data.objects['spoon'], rig): ob.parent = sau
    ST['cup_rig'] = rig; ST['saucer_rig'] = sau; ST['steam'] = steam
    # ---- toast plate (left front)
    mb = MB(); plx, ply = -0.50, -1.50
    mb.frustum((plx, ply, TOP), (plx, ply, TOP + 0.022), 0.17, 0.25, cr, seg=28); mb.frustum((plx, ply, TOP + 0.022), (plx, ply, TOP + 0.03), 0.25, 0.25, C('#e9dcc0', 0.85), seg=28, cap0=False)
    mb.obj('plate', SET, hull=hull(1.4))
    mb = MB(); mb.quad((plx - 0.16, ply - 0.14, TOP + 0.034), (0.30, 0.06, 0), (-0.05, 0.28, 0.0), TXM('toast', tx['toast'], 0.85, alpha=True), (0, 0, 1, 1)); mb.obj('toast', SET)
    # ---- chair at the right end of the table (it is shoved back in the storm)
    mb = MB(); cc = M['wood']; cl = C('#9a5432', 0.9, wd)
    mb.box((-0.32, -0.32, 0.86), (0.32, 0.32, 0.94), cl)
    for (ax, ay) in ((-0.30, -0.30), (0.24, -0.30), (-0.30, 0.24), (0.24, 0.24)): mb.box((ax, ay, 0), (ax + 0.06, ay + 0.06, 0.86), cc)
    for ay in (-0.32, 0.26): mb.box((0.26, ay, 0.94), (0.32, ay + 0.06, 2.05), cc)
    mb.box((0.25, -0.34, 1.80), (0.33, 0.34, 2.05), cl); mb.box((0.27, -0.34, 1.42), (0.31, 0.34, 1.52), cl)
    chair = mb.obj('chair', SET, hull=hull(2.4)); ST['chair'] = chair

    # ---- the falling drop (shot 26)
    mb = MB(); mb.sphere((0, 0, 0), 0.022, S.mat_emit(pre + 'drop', '#cfe0ff', strength=1.4), seg=12, rings=8); d = mb.obj('drop', SET); d.scale = (1, 1, 1.8); d.hide_render = True; d.visible_shadow = False
    ST['drop'] = d

    # ---- an unseen cupboard edge behind the lens shades the near part of the table: the light pools on the paper and the cup
    mb = MB(); mb.box((-3.0, -4.2, 2.62), (3.0, -2.87, 2.70), M['dark']); bl = mb.obj('fg_blocker', SET)
    bl.visible_camera = False
    # ---- lights: the key, and (storm) the lightning sun through the window
    def sun(name, col, energy, kd, ang):
        L_ = bpy.data.lights.new(name, 'SUN'); L_.color = col; L_.energy = energy; L_.angle = math.radians(ang)
        o = bpy.data.objects.new(name, L_); LIGHTS.objects.link(o); o.rotation_euler = (-Vector(kd).normalized()).to_track_quat('Z', 'Y').to_euler(); return o
    k = max(P['key']); ST['key'] = sun('key_sun', tuple(x / k for x in P['key']), math.pi * k, P['key_dir'], P['sun_angle'])
    if P['flash'] > 0: ST['flash'] = sun('flash_sun', (0.86, 0.88, 1.0), 0.0, P['flash_dir'], 1.5)
    S.setup_grade(scene)
    for ob in SET.objects: S.no_bounce(ob)
    A = anchors(); ST['A'] = A
    set_state()
    return A

def anchors():
    wbc = wb_point(1.0, 1.42); w1 = wb_point(1.0, 1.47)
    hdr = wb_point(1.0, 1.06); w2 = wb_point(1.0, 1.70)
    cams = dict(
        table=dict(loc=(0.225, -2.42, 1.80), look_at=(0.225, -0.30, 1.07), lens=22),
        steep=dict(loc=(0.225, -1.62, 2.30), look_at=(wbc[0], wbc[1], wbc[2] - 0.02), lens=22),
        window_tight=dict(loc=(WIN['mull'], -1.05, 2.48), look_at=(WIN['mull'], 0.0, 2.50), lens=22))
    return dict(cams=cams, wb_centre=wbc, word1=w1, header=hdr, word2=w2, cup_rest=CUP_REST, top=TOP, win=WIN, paper=PAPER, paper_scale=PS,
                exterior=KT.EXT, lightning=KT.LIGHTNING, crack_g=KT.CRACK_G)

# ----------------------------------------------------------------------------- per-frame state
def set_state(cup=None, saucer=None, ripple=(0.0, 0.0), steam=None, window=None, flutter=(0.0, 0.0), bleed=None, lightning=0.0, crack=None, chair=0.0, drop=None):
    """cup/saucer: (x, y, z_lift, rot_deg) of the cup rig relative to the saucer / of the saucer on the table (default: at rest).
    ripple = (phase, amplitude 0..1); steam = frame index of the loop or None (hidden); window = ('drizzle'|'wave', k);
    flutter = (t, amp D); bleed = None or bleed frame 0..11; lightning 0..1; crack = None or 0..5; chair 0 (in place) .. 1 (shoved back);
    drop = None or world (x, y, z) of the falling drop."""
    tx = KT.ensure(); P = ST['P']
    sx, sy, sz, sr = saucer or (CUP_REST[0], CUP_REST[1], 0.0, 0.0)
    ST['saucer_rig'].location = (sx, sy, TOP + 0.003 + sz); ST['saucer_rig'].rotation_euler = (0, 0, math.radians(sr))
    cx, cy, cz, cr = cup or (0.0, 0.0, 0.0, 0.0)
    ST['cup_rig'].location = (cx, cy, cz); ST['cup_rig'].rotation_euler = (0, 0, math.radians(cr))
    nt = ST['coffee_mat'].node_tree; nt.nodes['wave'].inputs['Phase Offset'].default_value = ripple[0]; nt.nodes['amp'].inputs[1].default_value = ripple[1]
    if steam is None: ST['steam'].hide_render = True
    else: ST['steam'].hide_render = False; _set_image(ST['steam_mat'], tx['steam'][steam % 24])
    kind, k = window or ('drizzle', 0)
    _set_image(ST['ext_mat'], tx[kind][k % len(tx[kind])])
    em = ST['ext_mat'].node_tree.nodes['str']; em.inputs[1].default_value = P['window'] * (1.0 + 0.6 * lightning)
    V, _ = paper_points(*flutter); me = ST['paper'].data
    for v, p in zip(me.vertices, V): v.co = p
    me.update()
    png = ST['paper_png'] if bleed is None else PREG['newspaper_bleed']['png'][min(11, bleed)]
    _set_image(ST['paper_mat'], png)
    if 'flash' in ST: ST['flash'].data.energy = math.pi * P['flash'] * lightning; ST['flash'].hide_render = lightning <= 0.0
    cobj = bpy.data.objects['crack']
    if crack is None: cobj.hide_render = True
    else: cobj.hide_render = False; _set_image(ST['crack_mat'], tx['crack'][min(5, crack)])
    c = ST['chair']; c.location = (1.30 + 0.30 * chair, -1.10 - 0.30 * chair, 0.0); c.rotation_euler = (0, 0, math.radians(180 + 24 * chair))
    d = ST['drop']
    if drop is None: d.hide_render = True
    else: d.hide_render = False; d.location = drop

# ----------------------------------------------------------------------------- CLI: stills of the named cameras
def stills(light='kitchen_grey', quality='preview', outdir=None, samples=None):
    A = build(light); scene = bpy.context.scene; S.setup_render(scene, quality)
    if samples: scene.cycles.samples = samples
    outdir = outdir or os.path.join(HERE, 'work'); os.makedirs(outdir, exist_ok=True)
    win = ('wave', 40) if light == 'kitchen_storm' else ('drizzle', 0)
    set_state(steam=3 if light == 'kitchen_grey' else None, window=win, ripple=(1.0, 0.6 if light == 'kitchen_storm' else 0.0), chair=1.0 if light == 'kitchen_storm' else 0.0)
    for nm, cs in A['cams'].items():
        S.make_camera(cs); w, c = S.render(os.path.join(outdir, 'still_%s_%s.png' % (light, nm))); print(nm, '%.1f s wall' % w)

if __name__ == '__main__':
    a = sys.argv[1:]
    stills(a[0] if a else 'kitchen_grey', a[1] if len(a) > 1 else 'preview', samples=int(a[2]) if len(a) > 2 else None)
