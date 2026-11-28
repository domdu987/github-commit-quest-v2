#!/usr/bin/env python3
"""beach_ext.py : what the shot plan asks of the beach set for shots 8, 16, 23, 24, as an extension of v3/set3d_beach/beach3d.py
(imported, never edited).  See API.md next to this file.

    import beach_ext as BX
    A = BX.build("grey_drizzle")              # beach_sunny | grey_drizzle | storm_approach | storm  (plan light names)
    cam = BX.B.make_camera(BX.cam_pose("beach_shore_eye"))
    BX.set_sign_swing(0.05, frame=1); BX.set_windows(1.0); BX.set_shutters(1.0, frame=10)

Adds: the light preset STORM_APPROACH, the cameras beach_high / beach_shore_eye / beach_low_wave, the LONG ISLAND sign (paper registry
'beach_sign') as a hanging sign that can swing, a landing with a step through the fence gap, weather vane and brick chimney on the porch
cottage, a towel line with a towel on the nearest porch, lit windows and banging shutters on every cottage front, a cobweb with a spider
that lowers itself, and a flying-boater card."""
import os, sys, math, json, hashlib, subprocess
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d_beach'))
import beach3d as B                                         # noqa: E402
S = B.S
TEX = os.path.join(HERE, 'tex')
PAPER_REG = os.path.join(PROJ, 'v3', 'paper', 'tex', 'registry.json')

# ----------------------------------------------------------------------------- light presets (plan names -> beach3d presets)
LIGHTS = dict(beach_sunny='SUMMER_SUN', grey_drizzle='GREY_DRIZZLE', storm_approach='STORM_APPROACH', storm='STORM')

def _scale_hex(h, k):
    c = [int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]; return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v * k)))) for v in c)

def _storm_approach():
    """GREY_DRIZZLE at 0.75 (key, ambient, sand), a bruise-violet sky with one sick yellow band above the horizon, a sea like glass
    (no streaks, darker, a pale horizon band), the pale fog band #c9bfbd (plan), and calm."""
    P = dict(B.PRESETS['GREY_DRIZZLE'])
    P.update(
        A=tuple(a * 0.75 for a in P['A']), A_pale=tuple(a * 0.75 for a in P['A_pale']), K=tuple(k * 0.75 for k in P['K']),
        shade_tint=(0.36, 0.36, 0.56), grade_sat=1.22, obj_sat=0.95,
        sky=[(0.0, '#8d8496'), (0.05, '#a39a8a'), (0.11, '#c2b27c'), (0.17, '#b3a07e'), (0.24, '#8e7f98'), (0.45, '#6a5f8e'), (1.0, '#3a3466')],
        sky_span=0.7,
        cloud=dict(lo='#4d4672', hi='#7d7398', cover=0.70, soft=0.22, opacity=0.70, scale=0.30), glow=None,
        haze='#8f889f', haze_max=0.75, haze_d=(16.0, 240.0),
        sand=tuple(_scale_hex(c, 0.80) for c in P['sand']), wet=_scale_hex(P['wet'], 0.8), sand_far=('#7d6f78', '#857c8a'),
        sea_near='#2e3658', sea_far='#4c5076', sea_band='#a69fae', streak='#8d90aa', streak_amt=0.04, foam='#b9bccb',
        fog='#d4cac6', fog_foot='#b2a8ad', fog_alpha=0.98, ink='#251a30', headland=('#6e6688', '#787294'),
        rain_col='#b9bed6')
    return P

B.PRESETS.setdefault('STORM_APPROACH', _storm_approach())

# ----------------------------------------------------------------------------- cameras (22 mm), one axis along the shore at three heights
CAMS = dict(
    # THE BEACH FRAMING (shots 16, 23): 2.6 D high, -3 deg, looking along the shore toward +x; sea and horizon at left, fence and sign
    # mid-right, porch cottages and poles at right, horizon about 0.46 H
    beach_shore_eye=dict(loc=(-7.4, 7.0, 2.6), look_at=(22.0, 5.0, 2.6 - 29.5 * math.tan(math.radians(3.0))), lens=22),
    # shot 8: the vista_high axis, lower: 5 D above the sand, -17 deg, 12 D from the deck chair, horizon about 0.31 H
    beach_high=dict(loc=(-2.4, 10.0, 5.0), look_at=(9.6, 8.6, 5.0 - 12.1 * math.tan(math.radians(17.0))), lens=22),
    # shot 24: on the beach framing's axis, 0.7 D above the sand, turned 15 deg toward the sea, pitched up 8 deg (start pose)
    beach_low_wave=dict(loc=(-6.0, 7.0, 0.7), look_at=(-6.0 + 20 * math.cos(math.radians(11.0)), 7.0 + 20 * math.sin(math.radians(11.0)), 0.7 + 20 * math.tan(math.radians(8.0))), lens=22),
)

def cam_pose(name): return dict(CAMS[name])

# ----------------------------------------------------------------------------- dressing positions
EXT = dict(
    sign=(2.0, 4.9), sign_yaw=65.0,               # LONG ISLAND sign: between boardwalk and fence, its face turned 65 deg toward -x (reads along the shore axis)
    landing=(-3.2, -1.4),                         # landing + step through the fence gap (x range), boardwalk edge to the sand
    vane_cottage='cottage_07', chimney_too=('cottage_06',),   # weather vane + brick chimney on the porch cottage; chimneys only on these
    towel_cottage='cottage_06',                   # towel line on the nearest porch
    cobweb=((7.2, 9.4), (9.6, 8.6)),              # between the umbrella pole and the deck-chair arm
)

def _ctl(): return B.STATE['ctl']

def _addprop(name, v):
    c = _ctl()
    if name not in c.keys(): c[name] = float(v)

def _key(name, v, frame):
    c = _ctl(); c[name] = float(v)
    if frame is not None: c.keyframe_insert('["%s"]' % name, frame=frame); B._linear(c)

def set_sign_swing(amp, frame=None): _key('sign_sw', amp, frame)        # radians of swing amplitude of the LONG ISLAND board
def set_windows(a, frame=None): _key('windows', a, frame)              # 0 dark panes, 1 lit (#ffd995)
def set_shutters(a, frame=None): _key('shutters', a, frame)            # 0 shut and still, 1 banging (open up to 75 deg)
def set_towel(on, frame=None): _key('towel_on', on, frame)             # 0 = no towel on the line (before the woman pegs it), 1 = hung
def set_spider(a, frame=None): _key('spider', a, frame)                # 0 spider at the web, 1 lowered 0.35 D on its thread
def set_fog_near(k, frame=None):
    """bring the fog ring in: radius = 300 x k about the origin (k 1 = the set's ring; 0.5 = 150 D). Height and opacity stay set_fog_bank's."""
    ob = bpy.data.objects['fog_bank']; ob.scale[0] = k; ob.scale[1] = k
    if frame is not None:
        for i in (0, 1): ob.keyframe_insert('scale', index=i, frame=frame)
        B._linear(ob)
def set_vane(deg, frame=None): _key('vane', math.radians(deg), frame)  # weather-vane heading (it swings in the wind)

# ----------------------------------------------------------------------------- small helpers
def _empty(name, coll, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); coll.objects.link(e); e.location = loc; e.rotation_euler = rot
    if parent is not None: e.parent = parent
    return e

def _raster(svg, out, w, h):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out): return out
    sp = out[:-4] + '.svg'; open(sp, 'w').write(svg); jp = out[:-4] + '_job.json'
    json.dump([dict(src=sp, out=out, w=w, h=h, transparent=True)], open(jp, 'w'))
    r = subprocess.run(['node', os.path.join(PROJ, 'v3', 'set3d', 'raster.js'), jp], capture_output=True, text=True,
                       env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
    if r.returncode != 0: raise RuntimeError(r.stderr[-1500:])
    return out

def _card_mat(name, png, haze=0.0, strength=1.0, lit=True):
    """alpha card: lit like the set (mat_lit with alpha) or self-coloured."""
    if lit: return B.mat_lit(name, image=png, pale=False, alpha=True, haze=haze)
    def af(nb):
        t = nb.n('ShaderNodeTexImage'); t.image = B._img(png); t.extension = 'CLIP'; return t.outputs['Alpha']
    def cf(nb):
        t = nb.n('ShaderNodeTexImage'); t.image = B._img(png); t.extension = 'CLIP'; return t.outputs['Color']
    return B.mat_unlit(name, None, strength=strength, alpha_fn=af, color_fn=cf, haze=haze, camera_only=True)

# ----------------------------------------------------------------------------- LONG ISLAND sign (hanging, swings)
def build_sign(coll):
    for nm in ('sign', 'sign_face'):                         # the set's BATHING BEACH sign is replaced
        ob = bpy.data.objects.get(nm)
        if ob is not None: ob.hide_render = True; ob.hide_viewport = True
    if not os.path.exists(PAPER_REG):
        raise FileNotFoundError(PAPER_REG + ': the paper artwork is not built. Run `python3 v3/paper/paper.py build` first (examples/setup_kit.sh does it).')
    png = json.load(open(PAPER_REG))['beach_sign']['png']
    x, y = EXT['sign']; yaw = math.radians(EXT['sign_yaw'])
    root = _empty('li_sign_root', coll, (x, y, 0.0), (0, 0, yaw))
    post = B.mat_lit('signpost', '#6d3a1f'); mb = S.MB()
    for sx in (-1.25, 1.25): mb.box((sx - 0.06, -0.06, 0), (sx + 0.06, 0.06, 2.95), post)
    mb.box((-1.4, -0.05, 2.85), (1.4, 0.05, 2.97), post)
    mb.frustum((-1.25, 0, 2.97), (-1.25, 0, 3.05), 0.09, 0.02, post, seg=6); mb.frustum((1.25, 0, 2.97), (1.25, 0, 3.05), 0.09, 0.02, post, seg=6)
    po = mb.obj('li_sign_posts', coll); B.add_hull(po, 0.02); S.no_bounce(po); po.parent = root
    piv = _empty('li_sign_pivot', coll, (0, 0, 2.85), parent=root)
    mb = S.MB(); board = B.mat_lit('signboard', '#f6efe2'); chain = B.mat_unlit('li_chain', '#2a1d26', camera_only=False)
    mb.box((-1.15, -0.035, -1.18), (1.15, 0.035, -0.20), board)
    for sx in (-0.95, 0.95): B._tube(mb, [(sx, 0, 0.0), (sx, 0, -0.2)], 0.012, chain)
    bo = mb.obj('li_sign_board', coll); B.add_hull(bo, 0.018); S.no_bounce(bo); bo.parent = piv
    mb = S.MB(); mb.quad((1.1, 0.04, -1.165), (-2.2, 0, 0), (0, 0, 0.95), B.mat_lit('li_sign_face', image=png), (0, 0, 1, 1))
    fo = mb.obj('li_sign_face', coll); S.no_bounce(fo); fo.parent = piv
    _addprop('sign_sw', 0.0)
    B._drive(piv, 'rotation_euler', 'sign_sw*sin(frame*0.42)+0.10*min(wind,1.2)', ['sign_sw', 'wind'], 0)
    return dict(root=root, pivot=piv, face_center=(x, y, 2.18), yaw=EXT['sign_yaw'])

# ----------------------------------------------------------------------------- landing through the fence gap
def build_landing(coll):
    x0, x1 = EXT['landing']; deck = B.mat_lit('deck', '#a8774f'); wood = B.mat_lit('stilt', '#6d3a1f'); mb = S.MB()
    mb.box((x0, 4.6, 0.0), (x1, 5.95, 0.36), deck, mats=dict(back=wood, left=wood, right=wood, front=wood))
    mb.box((x0 + 0.1, 5.95, 0.0), (x1 - 0.1, 6.25, 0.18), deck, mats=dict(back=wood, left=wood, right=wood))
    ob = mb.obj('landing', coll); B.add_hull(ob, 0.02); S.no_bounce(ob)
    return dict(top=(0.5 * (x0 + x1), 5.6, 0.36), step=(0.5 * (x0 + x1), 6.1, 0.18), sand=(0.5 * (x0 + x1), 6.7, 0.0))

# ----------------------------------------------------------------------------- weather vane and chimney
def _cot(name): return next(c for c in B.STATE['A']['cottages'] if c['name'] == name)

def build_vane_chimney(coll, name=None, vane=True):
    c = _cot(name or EXT['vane_cottage']); cx = 0.5 * (c['x'][0] + c['x'][1]); yb, yf = c['y_back'], c['y_front']
    sc = (c['x'][1] - c['x'][0]) / B.BT.W_C; zr = c['ridge']; ze = c['eave']
    brick = B.mat_lit('li_brick', '#9a4a3a'); cap = B.mat_lit('li_brick_cap', '#5a3a36'); iron = B.mat_lit('iron', '#3b3442', shade_mul=1.2)
    mb = S.MB(); chx = cx + 0.75 * sc; chy = yb + 0.9 * sc                       # chimney on the right roof slope near the back
    zroof = zr - (zr - ze) * (0.75 * sc) / (B.BT.W_C * sc / 2) + 0.05
    mb.box((chx - 0.24, chy - 0.24, zroof - 0.6), (chx + 0.24, chy + 0.24, zr + 0.85), brick)
    mb.box((chx - 0.30, chy - 0.30, zr + 0.85), (chx + 0.30, chy + 0.30, zr + 0.97), cap)
    ob = mb.obj('li_chimney_' + c['name'], coll); B.add_hull(ob, B.hull_for((chx, chy, zr))); S.no_bounce(ob)
    if not vane: return dict(cottage=c['name'], chimney_top=(chx, chy, zr + 0.97))
    vx, vy = cx, yf - 0.35 * sc; vz = zr + 0.08                                  # vane on the ridge over the porch end
    mb = S.MB(); mb.frustum((vx, vy, vz), (vx, vy, vz + 1.15), 0.025, 0.02, iron, seg=6)
    for a in (0, 90):                                                             # compass arms
        d = Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0)) * 0.32
        mb.frustum(Vector((vx, vy, vz + 0.55)) - d, Vector((vx, vy, vz + 0.55)) + d, 0.012, 0.012, iron, seg=4)
    mb.sphere((vx, vy, vz + 1.17), 0.05, iron, seg=8, rings=4)
    po = mb.obj('li_vane_post', coll); B.add_hull(po, 0.012); S.no_bounce(po)
    piv = _empty('li_vane_pivot', coll, (vx, vy, vz + 0.95))
    mb = S.MB()                                                                    # arrow + rooster silhouette (flat, both faces)
    pts = [(-0.55, 0.0), (0.38, 0.0), (0.38, 0.05), (0.55, 0.0), (0.38, -0.05), (0.38, 0.0)]
    mb.box((-0.55, -0.012, -0.012), (0.42, 0.012, 0.012), iron)
    mb.pid += 1; mb.face([(0.42, 0, -0.07), (0.6, 0, 0), (0.42, 0, 0.07)], iron); mb.pid += 1; mb.face([(0.42, 0, 0.07), (0.6, 0, 0), (0.42, 0, -0.07)], iron)
    mb.pid += 1; mb.face([(-0.55, 0, -0.10), (-0.38, 0, 0), (-0.55, 0, 0.12), (-0.62, 0, 0.0)], iron); mb.pid += 1; mb.face([(-0.62, 0, 0.0), (-0.55, 0, 0.12), (-0.38, 0, 0), (-0.55, 0, -0.10)], iron)
    roo = [(-0.22, 0.02), (0.18, 0.02), (0.22, 0.12), (0.30, 0.22), (0.24, 0.30), (0.17, 0.26), (0.12, 0.17), (-0.05, 0.15), (-0.18, 0.30), (-0.30, 0.24), (-0.24, 0.10)]
    mb.pid += 1; mb.face([(x, 0.0, z) for x, z in roo], iron); mb.pid += 1; mb.face([(x, 0.0, z) for x, z in roo[::-1]], iron)
    vo = mb.obj('li_vane', coll); S.no_bounce(vo); vo.parent = piv
    _addprop('vane', math.radians(35.0))
    B._drive(piv, 'rotation_euler', 'vane+0.12*wind*sin(frame*0.31)', ['vane', 'wind'], 2)
    return dict(cottage=c['name'], chimney_top=(chx, chy, zr + 0.97), vane_top=(vx, vy, vz + 1.22))

# ----------------------------------------------------------------------------- towel line on the nearest porch
def build_towel_line(coll, name=None):
    c = _cot(name or EXT['towel_cottage']); x0, x1 = c['x']; yl = c['porch_front'] - 0.06; zl = c['eave'] - 0.42
    line = B.mat_unlit('li_line', '#e8e0d0', camera_only=False); mb = S.MB()
    B._tube(mb, B._sag((x0 + 0.08, yl, zl), (x1 - 0.14, yl, zl), 0.06, 8), 0.012, line)
    lo = mb.obj('li_towel_line', coll); S.no_bounce(lo)
    tx = x0 + 0.38 * (x1 - x0); piv = _empty('li_towel_pivot', coll, (tx, yl, zl - 0.045))
    mb = S.MB(); stripes = (B.mat_lit('li_towel_a', '#c2311e'), B.mat_lit('li_towel_b', '#f6efe2'))
    for k in range(5): mb.quad((-0.35 + 0.14 * k, 0.0, -0.78), (0.14, 0, 0), (0, 0, 0.78), stripes[k % 2])
    for k in range(5): mb.quad((-0.35 + 0.14 * (k + 1), 0.0, -0.78), (-0.14, 0, 0), (0, 0, 0.78), stripes[k % 2])
    to = mb.obj('li_towel', coll); S.no_bounce(to); to.parent = piv
    pg = S.MB(); pm = B.mat_lit('li_peg', '#8a5a35')
    for sx in (-0.28, 0.28): pg.box((sx - 0.02, -0.02, -0.04), (sx + 0.02, 0.02, 0.07), pm)
    po = pg.obj('li_pegs', coll); S.no_bounce(po); po.parent = piv
    _addprop('towel_on', 1.0)
    B._drive(piv, 'rotation_euler', '(0.10*min(wind,1.5)+0.09*wind*sin(frame*0.83)+0.04*wind*sin(frame*2.1))', ['wind'], 0)
    for o in (to, po): B._drive(o, 'hide_render', 'towel_on<0.5', ['towel_on'])
    return dict(line=((x0 + 0.08, yl, zl), (x1 - 0.14, yl, zl)), towel=(tx, yl, zl), cottage=c['name'])

# ----------------------------------------------------------------------------- lit windows and banging shutters (cottage fronts)
def _glow_mat():
    full = 'BEACH_li_window'
    if full in bpy.data.materials: return bpy.data.materials[full]
    m = B._newmat(full); nt = B._tree(m); nb = B.NB(nt); out = nb.n('ShaderNodeOutputMaterial')
    w = nb.ctl('windows'); c = nb.mix(w, '#2b3150', '#ffd995')
    em = nb.n('ShaderNodeEmission'); nb.L(c, em.inputs['Color']); nb.L(nb.math('ADD', 1.0, nb.math('MULTIPLY', w, 0.9)), em.inputs['Strength'])
    last = B._haze(nb, em.outputs[0], 0.6)
    lp = nb.n('ShaderNodeLightPath'); tr = nb.n('ShaderNodeBsdfTransparent'); mx = nb.n('ShaderNodeMixShader')
    nb.L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); nb.L(tr.outputs[0], mx.inputs[1]); nb.L(last, mx.inputs[2]); nb.L(mx.outputs[0], out.inputs['Surface'])
    return m

def build_windows_shutters(coll):
    _addprop('windows', 0.0); _addprop('shutters', 0.0)
    gm = _glow_mat(); mb = S.MB(); shut = []; i = 0
    for c in B.STATE['A']['cottages']:
        x0, x1 = c['x']; sc = (x1 - x0) / B.BT.W_C; yf = c['y_front'] + 0.012; zf = B.BT.Z_FLOOR * sc
        for wx in (x0 + 0.62 * sc, x1 - 0.62 * sc):
            w, h = 0.40 * sc, 0.60 * sc; zb = zf + (1.6 - 0.72 + 0.06) * sc
            mb.quad((wx - w / 2, yf, zb), (w, 0, 0), (0, 0, h), gm)
            shut.append((c, wx, 0.52 * sc, 0.72 * sc, zf + (1.6 - 0.72) * sc, yf + 0.01, i)); i += 1
    ob = mb.obj('li_windows', coll); S.no_bounce(ob); ob.visible_shadow = False
    sm = B.mat_lit('li_shutter', '#3d5a6e'); out = []
    for (c, wx, w, h, zb, yf, k) in shut:
        for side in (-1, 1):
            hx = wx + side * w / 2; piv = _empty('li_shut_%d_%d' % (k, side), coll, (hx, yf, zb))
            mb = S.MB(); sw = 0.5 * w
            mb.box((min(0, side * sw), 0.0, 0.0), (max(0, side * sw), 0.04, h), sm)
            so = mb.obj('li_shutter_%d_%d' % (k, side), coll); B.add_hull(so, 0.012); S.no_bounce(so); so.parent = piv
            ph = (k * 1.7 + side * 0.6) % 6.28
            # banging: open up to 75 deg, slamming shut on a fast rhythm (abs of a sine), each shutter its own phase
            B._drive(piv, 'rotation_euler', '%d*shutters*1.31*sqrt(abs(sin(frame*0.37+%.2f)))' % (side, ph), ['shutters'], 2)
            out.append(piv.name)
    return dict(count=len(shut), shutters=len(out))

# ----------------------------------------------------------------------------- cobweb with a spider
def _cobweb_svg(W, H):
    cx, cy = W * 0.55, H * 0.42; s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H)]
    st = 'stroke="#f4f2fa" stroke-opacity="0.85" fill="none" stroke-linecap="round"'
    ends = [(0, 0), (W * 0.5, 0), (W, H * 0.1), (W, H * 0.6), (W * 0.7, H), (W * 0.2, H), (0, H * 0.55)]
    for (x, y) in ends: s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke-width="2.4" %s/>' % (cx, cy, x, y, st))
    for r in (0.12, 0.22, 0.33, 0.45, 0.58):
        pts = []
        for (x, y) in ends + [ends[0]]: pts.append('%.1f,%.1f' % (cx + (x - cx) * r, cy + (y - cy) * r + 6 * r * H * 0.05))
        s.append('<polyline points="%s" stroke-width="1.8" %s/>' % (' '.join(pts), st))
    s.append('</svg>'); return ''.join(s)

def _spider_svg(W, H):
    c = W / 2; s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H)]
    s.append('<line x1="%d" y1="0" x2="%d" y2="%d" stroke="#f4f2fa" stroke-width="3"/>' % (c, c, H * 0.62))
    for k in range(4):
        for sg in (-1, 1):
            s.append('<polyline points="%d,%d %d,%d %d,%d" stroke="#2a1d2c" stroke-width="7" fill="none" stroke-linejoin="round"/>' %
                     (c, H * 0.75, c + sg * W * 0.22, H * (0.62 + 0.06 * k), c + sg * W * 0.32, H * (0.70 + 0.07 * k)))
    s.append('<circle cx="%d" cy="%d" r="%d" fill="#2a1d2c"/><circle cx="%d" cy="%d" r="%d" fill="#2a1d2c"/>' % (c, H * 0.78, W * 0.09, c, H * 0.68, W * 0.06))
    s.append('<circle cx="%d" cy="%d" r="4" fill="#fff"/><circle cx="%d" cy="%d" r="4" fill="#fff"/></svg>' % (c - 7, H * 0.66, c + 7, H * 0.66))
    return ''.join(s)

def build_cobweb(coll):
    (ux, uy), (dx, dy) = EXT['cobweb']
    a = Vector((ux + 0.04, uy - 0.12, 0.85)); b = Vector((dx - 0.45, dy + 0.05, 0.75))      # pole side, chair-arm side
    web = _raster(_cobweb_svg(512, 512), os.path.join(TEX, 'cobweb.png'), 512, 512)
    spi = _raster(_spider_svg(160, 320), os.path.join(TEX, 'spider.png'), 160, 320)
    mid = (a + b) * 0.5; u = (b - a); L = u.length; u.normalize(); size = min(0.9, L * 0.8)
    mb = S.MB(); mb.quad(mid - u * size / 2 - Vector((0, 0, size / 2)), u * size, Vector((0, 0, size)), _card_mat('li_cobweb', web, lit=False, strength=1.1))
    wo = mb.obj('li_cobweb', coll); S.no_bounce(wo); wo.visible_shadow = False
    piv = _empty('li_spider', coll, mid + Vector((0, 0, size * 0.10)))
    mb = S.MB(); mb.quad(Vector((-0.06, 0.0, -0.24)), Vector((0.12, 0, 0)), Vector((0, 0, 0.24)), _card_mat('li_spider', spi, lit=False))
    so = mb.obj('li_spider_card', coll); S.no_bounce(so); so.visible_shadow = False; so.parent = piv
    _addprop('spider', 0.0); B._drive(piv, 'location', '%.4f-0.35*spider' % piv.location.z, ['spider'], 2)
    yaw = math.atan2(u.y, u.x); wo.rotation_mode = 'XYZ'
    piv.rotation_euler = (0, 0, yaw)
    return dict(center=tuple(mid), size=size)

# ----------------------------------------------------------------------------- flying boater (shot 24)
def build_boater(coll, px=512):
    sys.path.insert(0, os.path.join(PROJ, 'v3', 'acting')); import acting
    frag = acting.flying_hat_svg('beach_man', 0.5)
    W, H = px * 2, px
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="-1.0 -0.9 2.0 1.0">%s</svg>' % (W, H, frag)
    png = _raster(svg, os.path.join(TEX, 'boater_%s.png' % hashlib.sha1(svg.encode()).hexdigest()[:10]), W, H)
    piv = _empty('li_boater', coll)
    mb = S.MB(); mb.quad((-1.0, 0.0, -0.1), (2.0, 0, 0), (0, 0, 1.0), _card_mat('li_boater', png, lit=False))
    bo = mb.obj('li_boater_card', coll); S.no_bounce(bo); bo.parent = piv; piv.scale = (1, 1, 1); piv.hide_render = True; bo.hide_render = True
    return piv

def set_boater(frame, loc=None, spin_deg=0.0, scale=1.0, visible=True, cam=None):
    """key the flying boater card: world position, spin in the image plane (deg), scale; the card faces the camera (yaw)."""
    piv = bpy.data.objects['li_boater']; card = bpy.data.objects['li_boater_card']
    for o in (piv, card): o.hide_render = not visible; o.keyframe_insert('hide_render', frame=frame)
    if loc is not None:
        piv.location = loc; piv.keyframe_insert('location', frame=frame)
    yaw = 0.0
    if cam is not None:
        d = Vector(cam.matrix_world.to_translation()) - Vector(piv.location); yaw = math.atan2(d.y, d.x) - math.pi / 2
    piv.rotation_euler = (0, math.radians(spin_deg), yaw); piv.keyframe_insert('rotation_euler', frame=frame)
    piv.scale = (scale, scale, scale); piv.keyframe_insert('scale', frame=frame)

# ----------------------------------------------------------------------------- build
def build(light='grey_drizzle', clear=True, dressing=True, boater=False):
    """beach3d.build with the plan's light name, plus every dressing item. Returns beach3d's anchors with A['ext'] and A['cams'] extended."""
    pre = LIGHTS.get(light, light)
    A = B.build(pre, clear=clear)
    A['cams'].update({k: dict(v) for k, v in CAMS.items()})
    ext = {}
    if dressing:
        coll = S._coll('BEACH_EXT', bpy.context.scene); S._wipe(coll)
        ext['sign'] = build_sign(coll); ext['landing'] = build_landing(coll); ext['vane'] = build_vane_chimney(coll); ext['chimneys'] = [build_vane_chimney(coll, n, vane=False) for n in EXT['chimney_too']]
        ext['towel'] = build_towel_line(coll); ext['windows'] = build_windows_shutters(coll); ext['cobweb'] = build_cobweb(coll)
        if boater: ext['boater'] = build_boater(coll)
    A['ext'] = ext; A['light'] = light
    return A

if __name__ == '__main__':
    print(__doc__)
