#!/usr/bin/env python3
"""v2_a.py : location A, v2 (client rejected v1: washed out, floating, too close). Extension of set15: imports set15 and ADDS / OVERRIDES geometry, presets and lights.
Nothing in set15*.py is edited.  See API_v2_a.md.

    import v2_a as V
    A = V.build_a2()                 # = F.build('A', 'HERO') + saturated palette + town + hills + signs + people + god rays  (about 20 s)
    V.ground_card(...), V.newspaper(...), V.rim_on(...)   # helpers (see API_v2_a.md)

World: metres inside the builders (SETROOT scale 1/0.54 -> 1 D = 0.54 m); cameras / marks are D, like set15. Sun at +y (behind the pit), the camera mostly looks +y (backlit golden hour).
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..'))
for p in (os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), HERE):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import set15 as F
import set15_lib as L
import set15_a as LA
import set15_props as PR
from set15_lib import S, mat, mat_emit, rnd, adopt, root, STATE, DM, U, kdir, hexl

WORK = os.path.join(HERE, 'work_v2_a'); TEX = os.path.join(WORK, 'tex'); os.makedirs(TEX, exist_ok=True)
FONT_DIR = os.path.normpath(os.path.join(V3, '..', 'fonts'))
FONTS = dict(black=os.path.join(FONT_DIR, 'Kanit_900Black.ttf'), work=os.path.join(FONT_DIR, 'WorkSans-Black.ttf'),
             serif='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', serif2='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
             sans='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', reg='/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')

# ============================================================================= palette (saturated, school MAROON + GOLD, red cinder, green grass)
MAROON = '#a01830'; GOLD = '#ffc928'
PALETTE = {   # name -> (A, B) hex pair of the board two-tone noise (or a single colour); applied by recolor() on every material called A_<LIGHT>|name
    'grassA': ('#4a9a2a', '#68b032'), 'lawnA': ('#449028', '#60aa30'), 'gp1': ('#1f8a12', '#3ca81c'), 'gp2': ('#8ec81c', '#aedc30'), 'grass': ('#2f9d16', '#58bb24'),
    'cinderA': ('#c3301a', '#e4501e'), 'dirtA': ('#9c7a4c', '#b8925a'), 'cinder': ('#c3301a', '#e4501e'),
    'saw': ('#f0aa24', '#ffc844'), 'chip': ('#c47a22', '#e29a36'), 'sawdk': ('#d08c1e', '#e8a42c'),
    'brick': ('#a0182e', '#c42a3a'), 'trim': ('#ffd23c', '#ffc020'), 'roofd': ('#5c1030', '#7a1a40'), 'roofdb': ('#5c1030', '#7a1a40'),
    'glass': ('#1c3ca0', '#3a62d0'), 'glasslit': ('#ffb020', '#ffd048'),
    'pine': ('#087a36', '#14a040'), 'pine2': ('#0a8a3c', '#26a83a'), 'trunk': ('#6a3418', '#8a4a22'),
    'leaf': ('#2fa016', '#62c024'), 'leafg': ('#2fa016', '#62c024'), 'leafo': ('#ee5a12', '#ff8a1c'), 'leafy': ('#ffc414', '#ffe040'), 'leafr': ('#d82a14', '#f04a1c'),
    'woodgrey': ('#c8842a', '#e29c3a'), 'woodpale': ('#e8a030', '#ffbe48'), 'wood': ('#8e4416', '#b05a22'),
    'asphalt': ('#4a4a8c', '#5c5ca0'), 'curb': ('#f0dc9c', '#ffe9ae'), 'steel': ('#2c52b8', '#4a72d6'), 'metal': ('#9ab0e0', '#7e98d0'),
    'concrete': ('#e0b090', '#f0c4a0'), 'concrete2': ('#8a8ccc', '#a0a2dc'), 'concreteb': ('#e0b090', '#f0c4a0'), 'concrete2b': ('#8a8ccc', '#a0a2dc'),
    'red': ('#e82212', '#ff3c1e'), 'orange': ('#ff8a08', '#ffa424'), 'yellow': ('#ffcc10', '#ffe030'), 'blue': ('#1858e8', '#3a7af8'), 'teal': ('#08b0a0', '#20d0b8'),
    'green': ('#22a82c', '#44c83a'), 'navy': ('#16288c', '#2a40b0'), 'cream': ('#ffe08a', '#ffd070'),
    'car_t': ('#10b8a8', '#28d4c0'), 'car_c': ('#fff0b0', '#ffe48c'), 'car_r': ('#e0200e', '#ff3c1e'), 'car_m': ('#34d070', '#54e888'), 'car_b': ('#1c54e0', '#3c78f4'), 'car_y': ('#ffc010', '#ffd838'),
    'carglass': ('#1c3ca0', '#3860c8'), 'bikeb': ('#1858e8', '#3a7af8'), 'bikeg': ('#18b050', '#34d068'), 'towel_w': ('#e8c880', '#f0d890'), 'towel_b': ('#2a6af0', '#4a88ff'),
    'tuft': ('#c0d020', '#e8e048'), 'mark': ('#fff8e0', '#fff0c8'), 'chalk': ('#fffbe8', '#fff4d0'), 'paper': ('#f0dc9c', '#e8cc88'), 'leather': ('#9a4018', '#b85424'),
    'tartan': ('#d03a1a', '#ee5a24'), 'rust': ('#d4561c', '#f07428'), 'bone': ('#fff0c0', '#ffe4a0'), 'skin1': ('#f0a060', '#e08a48'), 'skin2': ('#a8602c', '#8a4a20'), 'dark': ('#2a1838', '#3c2250'),
    'barW': ('#fff6e0', '#fff6e0'), 'barR': ('#e82212', '#e82212'),
}

def recolor(light_name=None):
    """Re-tone the board materials of the CURRENT preset to PALETTE (first Mix node pair = noise tones, second pair = the season pair of leaf mats; single-colour mats: RGB node)."""
    pn = STATE['P']['name']; n = 0
    for nm, (a, b) in PALETTE.items():
        m = bpy.data.materials.get('%s|%s' % (pn, nm))
        if m is None or m.node_tree is None: continue
        nt = m.node_tree; mixes = [x for x in nt.nodes if x.bl_idname == 'ShaderNodeMix' and x.data_type == 'RGBA' and x.inputs[0].is_linked and not x.inputs[6].is_linked and not x.inputs[7].is_linked
                                   and x.inputs[0].links[0].from_node.bl_idname == 'ShaderNodeValToRGB']
        rgbs = [x for x in nt.nodes if x.bl_idname == 'ShaderNodeRGB']
        if mixes:
            mixes[0].inputs[6].default_value = S.hexc(a); mixes[0].inputs[7].default_value = S.hexc(b); n += 1
        elif rgbs: rgbs[0].outputs[0].default_value = S.hexc(a); n += 1
    # autumn pair of the leaf material (season node feeds a 2nd Mix)
    m = bpy.data.materials.get('%s|leaf' % pn)
    if m:
        mixes = [x for x in m.node_tree.nodes if x.bl_idname == 'ShaderNodeMix' and x.data_type == 'RGBA' and x.inputs[0].is_linked and not x.inputs[6].is_linked and not x.inputs[7].is_linked
                 and x.inputs[0].links[0].from_node.bl_idname == 'ShaderNodeValToRGB']
        if len(mixes) > 1: mixes[1].inputs[6].default_value = S.hexc('#f04a10'); mixes[1].inputs[7].default_value = S.hexc('#ffb018')
    return n

# ============================================================================= light preset  A_HERO
_SKY_HERO = [(0.0, '#a8d4ff'), (0.04, '#7cbcff'), (0.14, '#4a98fa'), (0.34, '#2a6ee8'), (0.62, '#1c4cd0'), (1.0, '#1638b4')]
F.LIGHTS['A_HERO'] = dict(F._B, name='A_HERO', loc='A', key=(1.8, 1.30, 0.80), key_dir=kdir(-105, 28), sun_elev=28, sun_angle=0.8, shade=(0.24, 0.20, 0.50), shade_tint=(0.25, 0.20, 0.55),
                          lift=(0.012, 0.018, 0.07), season=1.0, grade_saturation=1.22, grade_offset=(-0.008, -0.012, -0.012), exposure=-0.7, shade_mix=0.72,
                          sky=_SKY_HERO, sky_k=1.0, glow=('#ffd890', 0.90, 0.5), hills=[(560, 40, 70, '#4838b8'), (640, 70, 90, '#6a4ad0')], hill_k=1.0)
F.LIGHTS['A_HERODAY'] = dict(F.LIGHTS['A_HERO'], name='A_HERODAY', key=(2.0, 1.8, 1.4), key_dir=kdir(-38, 44), sun_elev=44, season=0.0, sky=[(0.0, '#d8ecff'), (0.05, '#8cc4ff'), (0.2, '#3a84f6'), (0.5, '#1c5ae8'), (1.0, '#1244d0')], glow=('#fff0c0', 0.5, 0.3), hills=[(560, 40, 70, '#4a6ad8'), (640, 70, 90, '#6a8aee')])
for _k in ('HERO', 'HERODAY'):
    if _k not in F.LOC_LIGHTS['A']: F.LOC_LIGHTS['A'].append(_k)

# ============================================================================= world: deep blue sky, sun glow, clouds (camera rays only; the lighting is the house key + painted shade)
def sky_clouds(P, cloud_cover=0.55, seed=3):
    w = bpy.data.worlds.new('sky2'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); Lk(sp.outputs['Z'], cr.inputs[0]); st = P['sky']
    cr.color_ramp.elements[0].position = st[0][0]; cr.color_ramp.elements[0].color = S.hexc(st[0][1])
    for pos, col in st[1:-1]: cr.color_ramp.elements.new(pos).color = S.hexc(col)
    cr.color_ramp.elements[-1].position = st[-1][0]; cr.color_ramp.elements[-1].color = S.hexc(st[-1][1])
    kd = Vector(P['key_dir']).normalized(); sd = -kd
    dt = N('ShaderNodeVectorMath'); dt.operation = 'DOT_PRODUCT'; Lk(tc.outputs['Generated'], dt.inputs[0]); dt.inputs[1].default_value = tuple(sd)
    ma = tc
    mr = N('ShaderNodeMapRange'); Lk(dt.outputs['Value'], mr.inputs['Value']); mr.inputs['From Min'].default_value = P['glow'][1]; mr.inputs['From Max'].default_value = 1.0; mr.interpolation_type = 'SMOOTHSTEP'
    zf = N('ShaderNodeMapRange'); Lk(sp.outputs['Z'], zf.inputs['Value']); zf.inputs['From Min'].default_value = 0.6; zf.inputs['From Max'].default_value = 0.0
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; Lk(mr.outputs['Result'], mu.inputs[0]); Lk(zf.outputs['Result'], mu.inputs[1])
    mu2 = N('ShaderNodeMath'); mu2.operation = 'MULTIPLY'; mu2.inputs[1].default_value = P['glow'][2]; Lk(mu.outputs[0], mu2.inputs[0])
    ad = N('ShaderNodeMix'); ad.data_type = 'RGBA'; Lk(cr.outputs[0], ad.inputs[6]); ad.inputs[7].default_value = S.hexc(P['glow'][0]); Lk(mu2.outputs[0], ad.inputs[0])
    col = ad.outputs[2]
    if cloud_cover > 0:
        # clouds: stretched noise on the dome direction (flattened in z so they form bands), band-limited to a belt above the horizon, lit warm on the sun side
        d3 = N('ShaderNodeVectorMath'); d3.operation = 'MULTIPLY'; Lk(tc.outputs['Generated'], d3.inputs[0]); d3.inputs[1].default_value = (3.2, 3.2, 8.0)
        nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0; nz.inputs['Detail'].default_value = 5; nz.inputs['Roughness'].default_value = 0.55; Lk(d3.outputs[0], nz.inputs['Vector'])
        cc = N('ShaderNodeMapRange'); Lk(nz.outputs['Fac'], cc.inputs['Value']); cc.inputs['From Min'].default_value = 0.62 - 0.2 * cloud_cover; cc.inputs['From Max'].default_value = 0.70 - 0.2 * cloud_cover
        cc.interpolation_type = 'SMOOTHSTEP'
        belt = N('ShaderNodeMapRange'); Lk(sp.outputs['Z'], belt.inputs['Value']); belt.inputs['From Min'].default_value = 0.04; belt.inputs['From Max'].default_value = 0.16
        bm_ = N('ShaderNodeMath'); bm_.operation = 'MULTIPLY'; Lk(cc.outputs['Result'], bm_.inputs[0]); Lk(belt.outputs['Result'], bm_.inputs[1])
        # cloud colour: shaded side lilac-blue, sun side hot gold-pink
        sun_k = N('ShaderNodeMapRange'); Lk(dt.outputs['Value'], sun_k.inputs['Value']); sun_k.inputs['From Min'].default_value = -1.0; sun_k.inputs['From Max'].default_value = 0.1
        cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.inputs[6].default_value = S.hexc('#ffe6c0'); cm.inputs[7].default_value = S.hexc('#ffffff'); Lk(sun_k.outputs['Result'], cm.inputs[0])
        cmix = N('ShaderNodeMix'); cmix.data_type = 'RGBA'; Lk(col, cmix.inputs[6]); Lk(cm.outputs[2], cmix.inputs[7]); Lk(bm_.outputs[0], cmix.inputs[0]); col = cmix.outputs[2]
    Lk(col, bg.inputs['Color']); Lk(bg.outputs[0], out.inputs['Surface'])
    lp = N('ShaderNodeLightPath'); m3 = N('ShaderNodeMath'); m3.operation = 'MULTIPLY'; m3.inputs[1].default_value = P['sky_k']; Lk(lp.outputs['Is Camera Ray'], m3.inputs[0]); Lk(m3.outputs[0], bg.inputs['Strength'])
    w.light_settings.distance = 0.001
    return w

# ============================================================================= numpy instanced meshes with per-vertex colour ('Col') -> one lit material
def _tpl_box():
    v = np.array([(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0), (-.5, -.5, 1), (.5, -.5, 1), (.5, .5, 1), (-.5, .5, 1)], float)
    f = [(0, 3, 2), (0, 2, 1), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return v, f
def _tpl_gable():
    v = np.array([(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0), (-.5, 0, 1), (.5, 0, 1)], float)
    f = [(0, 1, 5), (0, 5, 4), (2, 3, 4), (2, 4, 5), (0, 4, 3), (1, 2, 5), (0, 3, 2), (0, 2, 1)]
    return v, f
def _tpl_cone(n=7, cap=True):
    v = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), 0.0) for i in range(n)] + [(0, 0, 1.0), (0, 0, 0.0)]
    f = [(i, (i + 1) % n, n) for i in range(n)]
    if cap: f += [((i + 1) % n, i, n + 1) for i in range(n)]
    return np.array(v, float), f
def _tpl_cyl(n=8):
    v = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), 0.0) for i in range(n)] + [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n), 1.0) for i in range(n)] + [(0, 0, 0), (0, 0, 1)]
    f = []
    for i in range(n):
        j = (i + 1) % n; f += [(i, j, n + j), (i, n + j, n + i), (n + i, n + j, 2 * n + 1), (j, i, 2 * n)]
    return np.array(v, float), f
def _tpl_blob(us=8, vs=5):
    v = [(0, 0, 0.0)]
    for j in range(1, vs):
        th = math.pi * j / vs
        for i in range(us): ph = 2 * math.pi * i / us; v.append((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), 0.5 - math.cos(th) * 0.5))
    v.append((0, 0, 1.0)); f = []
    for i in range(us): f.append((0, 1 + (i + 1) % us, 1 + i))
    for j in range(vs - 2):
        for i in range(us):
            a = 1 + j * us + i; b = 1 + j * us + (i + 1) % us; c = 1 + (j + 1) * us + (i + 1) % us; d = 1 + (j + 1) * us + i; f += [(a, b, c), (a, c, d)]
    top = len(v) - 1; base = 1 + (vs - 2) * us
    for i in range(us): f.append((top, base + i, base + (i + 1) % us))
    return np.array(v, float), f
def _tpl_quad():                 # vertical quad in the xz plane facing -y, x -0.5..0.5, z 0..1 (two-sided cards use two of them)
    return np.array([(-.5, 0, 0), (.5, 0, 0), (.5, 0, 1), (-.5, 0, 1)], float), [(0, 1, 2), (0, 2, 3)]
def _tpl_flat():                 # horizontal quad x,y -0.5..0.5 at z 0
    return np.array([(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0)], float), [(0, 1, 2), (0, 2, 3)]
TPL = dict(box=_tpl_box(), gable=_tpl_gable(), cone=_tpl_cone(7), cone5=_tpl_cone(5), cyl=_tpl_cyl(8), cyl6=_tpl_cyl(6), blob=_tpl_blob(), blob6=_tpl_blob(6, 4), quad=_tpl_quad(), flat=_tpl_flat())

class NM:
    """Instanced numpy mesh with vertex colours. add(tpl, pos(N,3), scale(N,3), yaw(N), col(N,3 linear rgb)) vectorised; -> finish() one object, material vc_mat()."""
    def __init__(self, name): self.name = name; self.V = []; self.F = []; self.C = []; self.n = 0
    def add(self, tpl, pos, scale, yaw=0.0, col=(0.5, 0.5, 0.5), tilt=0.0):
        V, Fc = TPL[tpl]; pos = np.atleast_2d(np.asarray(pos, float)); N = len(pos)
        sc = np.broadcast_to(np.asarray(scale, float), (N, 3)); yw = np.broadcast_to(np.asarray(yaw, float), (N,)); cl = np.broadcast_to(np.asarray(col, float), (N, 3))
        c = np.cos(yw)[:, None]; s = np.sin(yw)[:, None]
        X = V[None, :, 0] * sc[:, None, 0]; Y = V[None, :, 1] * sc[:, None, 1]; Z = V[None, :, 2] * sc[:, None, 2]
        wx = X * c - Y * s + pos[:, None, 0]; wy = X * s + Y * c + pos[:, None, 1]; wz = Z + pos[:, None, 2]
        self.V.append(np.stack([wx, wy, wz], -1).reshape(-1, 3)); m = len(V)
        fa = np.array(Fc, int); self.F.append((np.arange(N)[:, None, None] * m + fa[None] + self.n).reshape(-1, fa.shape[1])); self.n += N * m
        self.C.append(np.repeat(cl, m, axis=0))
    def finish(self, shadow=True, recalc=True):
        if not self.V: return None
        V = np.concatenate(self.V); Fc = np.concatenate(self.F); C = np.concatenate(self.C)
        me = bpy.data.meshes.new(self.name); me.from_pydata(V.tolist(), [], Fc.tolist()); me.update()
        at = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT'); rgba = np.concatenate([C, np.ones((len(C), 1))], 1).astype(np.float32); at.data.foreach_set('color', rgba.reshape(-1))
        if recalc:
            bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
        me.materials.append(vc_mat())
        ob = bpy.data.objects.new(self.name, me); STATE['SET'].objects.link(ob); ob.parent = root(); L.T.no_bounce(ob); ob.visible_shadow = shadow
        return ob

def lin(h): return np.array(S.hexc(h)[:3], float)

def vc_mat(name='vc', gain=1.0, shade_mul=1.0):
    key = '%s|%s' % (STATE['P']['name'], name)
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_type = 'GEOMETRY'; at.attribute_name = 'Col'
    L._lit_tail(nt, at.outputs['Color'], gain, shade_mul, None, True, None); m.cycles.emission_sampling = 'NONE'
    m['lit'] = 1; m['gain'] = float(gain); m['sm'] = float(shade_mul); m['crowd'] = 0; m['mix'] = float(STATE['P']['shade_mix'])
    S.MATS[key] = m; return m

def mat_tex(name, png, k=0.9, tint=(1.0, 0.96, 0.86), lit=0.0):
    """Sign / poster / newspaper: image colour as EMISSION (readable in any light), k = brightness, tint = warm key. lit>0 mixes in the house-lit look."""
    key = 'E|tex_' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Cubic'; ti.extension = 'CLIP'
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0; Lk(ti.outputs['Color'], mx.inputs[6]); mx.inputs[7].default_value = (*tint, 1.0)
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; Lk(mx.outputs[2], em.inputs['Color'])
    tr = N('ShaderNodeBsdfTransparent'); mix = N('ShaderNodeMixShader'); Lk(ti.outputs['Alpha'], mix.inputs[0]); Lk(tr.outputs[0], mix.inputs[1]); Lk(em.outputs[0], mix.inputs[2])
    out = N('ShaderNodeOutputMaterial'); Lk(mix.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def quad_obj(name, corners, mat_, uv=((0, 0), (1, 0), (1, 1), (0, 1)), cast=False, parent=True):
    """a textured quad from 4 corners (metres, set-local; counter-clockwise seen from the front)."""
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(c) for c in corners], [], [(0, 1, 2, 3)]); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(uv): uvl.data[i].uv = c
    me.materials.append(mat_); ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob)
    if parent: ob.parent = root()
    L.T.no_bounce(ob); ob.visible_shadow = cast; return ob

# ============================================================================= terrain, hills, pines
def hfun(x, y):
    """ground height (m): flat town basin (r < 250), rolling pine hills beyond; x, y arrays."""
    r = np.hypot(x - 0.0, y - 20.0); k = np.clip((r - 235.0) / 150.0, 0, 1); k = k * k * (3 - 2 * k)
    ang = np.arctan2(y - 20.0, x)
    ridge = 0.55 + 0.25 * np.sin(ang * 5 + 1.0) + 0.2 * np.sin(ang * 11 + 2.0) + 0.12 * np.sin(x * 0.011 + y * 0.017)
    return -0.03 + k * 95.0 * ridge + k * 6.0 * np.sin(x * 0.045) * np.sin(y * 0.05)

def terrain(P, rr):
    n = 150; R = 700.0; xs = np.linspace(-R, R, n); X, Y = np.meshgrid(xs, xs); Z = hfun(X, Y)
    nm = NM('terrain'); V = np.stack([X, Y, Z], -1).reshape(-1, 3)
    faces = []
    for j in range(n - 1):
        for i in range(n - 1):
            a = j * n + i; b = a + 1; c = a + n + 1; d = a + n; faces += [(a, b, c), (a, c, d)]
    fa = np.array(faces, int)
    # colour: bright grass; olive/gold meadow patches; deep green on the hills
    h = Z.reshape(-1); xx = X.reshape(-1); yy = Y.reshape(-1)
    t = 0.5 + 0.5 * np.sin(xx * 0.021 + 1.3) * np.sin(yy * 0.017 + 0.4) + 0.25 * np.sin(xx * 0.09) * np.sin(yy * 0.07)
    g1 = lin('#4a9e22'); g2 = lin('#98c630'); gh = lin('#1c8a38'); gold = lin('#e0b428')
    c = g1[None] * (1 - t[:, None]) + g2[None] * t[:, None]
    hill = np.clip(h / 45.0, 0, 1)[:, None]; c = c * (1 - hill) + gh[None] * hill
    patch = (np.sin(xx * 0.013 + 2.0) * np.sin(yy * 0.011 + 5.0) > 0.55)[:, None]; c = np.where(patch & (h[:, None] < 8), gold[None] * 0.9 + c * 0.1, c)
    me = bpy.data.meshes.new('terrain'); me.from_pydata(V.tolist(), [], fa.tolist()); me.update()
    at = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT'); at.data.foreach_set('color', np.concatenate([c, np.ones((len(c), 1))], 1).astype(np.float32).reshape(-1))
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        if me.vertices[f.vertices[0]].co.z is None: pass
    me.materials.append(vc_mat()); ob = bpy.data.objects.new('terrain', me); STATE['SET'].objects.link(ob); ob.parent = root(); L.T.no_bounce(ob)
    return ob

def pines(rr, n_hill=1500, n_town=0):
    """instanced pine forests: dense on the hills (r > 240), groves at the school (see school_pines), colour variety deep green / blue-green / olive."""
    nm = NM('pines_hills'); cols = [lin('#087a36'), lin('#0c8a44'), lin('#18902c'), lin('#0a6a40'), lin('#2a9a2a')]
    pts = []
    while len(pts) < n_hill:
        a = rr.uniform(0, 2 * math.pi); r = 240 + 300 * rr.random() ** 0.8; x = r * math.cos(a); y = 20 + r * math.sin(a)
        if rr.random() < 0.35 and math.sin(x * 0.03 + y * 0.02) < 0.0: continue
        pts.append((x, y))
    P = np.array(pts); z = hfun(P[:, 0], P[:, 1]); N = len(P); h = np.array([rr.uniform(14, 30) for _ in range(N)])
    ci = np.array([rr.randrange(len(cols)) for _ in range(N)]); C = np.array([cols[i] for i in ci]) * (0.8 + 0.4 * np.array([rr.random() for _ in range(N)]))[:, None]
    tr = lin('#5a2c14')
    nm.add('cyl6', np.c_[P, z - 0.3], np.c_[h * 0.04, h * 0.04, h * 0.3], 0, np.broadcast_to(tr, (N, 3)))
    for k, (zf, rf, hf) in enumerate(((0.12, 0.30, 0.45), (0.38, 0.24, 0.40), (0.62, 0.17, 0.34))):
        nm.add('cone5', np.c_[P, z + h * zf], np.c_[h * rf, h * rf, h * hf], np.array([rr.random() * 6 for _ in range(N)]), C * (0.95 + 0.05 * k))
    return nm.finish()

# ============================================================================= art: signs, poster, newspaper (PIL)
def _font(key, size):
    from PIL import ImageFont
    return ImageFont.truetype(FONTS[key], size)

def _fit_text(d, text, box, key, fill, stroke=0, stroke_fill=(0, 0, 0), spacing=0.0, anchor='mm'):
    """largest font that fits `text` in box (x0,y0,x1,y1) and draw it centred."""
    from PIL import ImageFont
    x0, y0, x1, y1 = box; sz = int((y1 - y0) * 1.1)
    while sz > 8:
        f = _font(key, sz); bb = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
        if bb[2] - bb[0] <= (x1 - x0) and bb[3] - bb[1] <= (y1 - y0): break
        sz -= 4
    d.text(((x0 + x1) // 2, (y0 + y1) // 2), text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)
    return sz

def tex_medford_high():
    p = os.path.join(TEX, 'medford_high.png')
    from PIL import Image, ImageDraw
    W, H = 4096, 560; im = Image.new('RGB', (W, H), (150, 20, 44)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(255, 214, 60), width=22); d.rectangle([36, 36, W - 37, H - 37], outline=(255, 244, 214), width=6)
    _fit_text(d, 'MEDFORD HIGH', (130, 70, W - 130, H - 70), 'black', (255, 208, 48), stroke=10, stroke_fill=(70, 6, 24))
    im.save(p); return p

def tex_track_field():
    p = os.path.join(TEX, 'track_field.png')
    from PIL import Image, ImageDraw
    W, H = 2800, 640; im = Image.new('RGB', (W, H), (255, 246, 220)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(150, 20, 44), width=30); d.rectangle([40, 40, W - 41, H - 41], outline=(255, 190, 30), width=10)
    _fit_text(d, 'TRACK & FIELD', (120, 90, W - 120, H - 90), 'black', (150, 20, 44), stroke=0)
    im.save(p); return p

def tex_scoreboard():
    p = os.path.join(TEX, 'scoreboard.png')
    from PIL import Image, ImageDraw
    W, H = 2400, 1000; im = Image.new('RGB', (W, H), (12, 60, 34)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(255, 244, 214), width=26)
    _fit_text(d, 'HIGH JUMP', (120, 70, W - 120, 560), 'black', (255, 214, 60), stroke=6, stroke_fill=(30, 20, 0))
    d.rectangle([120, 610, W - 120, 640], fill=(255, 244, 214))
    f = _font('black', 190)
    d.text((W // 2 - 540, 810), 'BAR', font=f, fill=(255, 244, 214), anchor='mm'); d.text((W // 2 + 300, 810), "5' 8\"", font=f, fill=(255, 90, 60), anchor='mm')
    im.save(p); return p

def tex_mexico68():
    p = os.path.join(TEX, 'mexico68.png')
    from PIL import Image, ImageDraw
    import numpy as np
    W, H = 1200, 1600; yy, xx = np.mgrid[0:H, 0:W].astype(float); cx, cy = W / 2, H * 0.40
    r = np.hypot(xx - cx, yy - cy); ang = np.arctan2(yy - cy, xx - cx)
    # concentric op-art ripples (Mexico 68 look): bands whose frequency wobbles with the angle
    v = np.sin((r + 22 * np.sin(ang * 6)) / 14.0)
    img = np.zeros((H, W, 3), float); base = np.array([255, 206, 40], float); ink = np.array([20, 14, 40], float)
    m = (v > 0.1)[..., None]; img = np.where(m, ink[None, None], base[None, None])
    # fade the ripples at the edge to a colour field
    edge = np.clip((r - 470) / 140, 0, 1)[..., None]; fld = np.array([240, 50, 60], float); img = img * (1 - edge) + fld * edge
    im = Image.fromarray(img.astype(np.uint8)); d = ImageDraw.Draw(im)
    d.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], fill=(255, 250, 230)); d.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], outline=(20, 14, 40), width=18)
    _fit_text(d, 'MEXICO', (cx - 270, cy - 230, cx + 270, cy - 30), 'black', (20, 14, 40))
    _fit_text(d, '68', (cx - 270, cy - 20, cx + 270, cy + 250), 'black', (240, 50, 60))
    cols = [(30, 110, 230), (20, 14, 40), (240, 50, 60), (255, 190, 30), (40, 170, 70)]
    for i, c in enumerate(cols):                                    # five rings
        rx = 170 + i * 215; ry = 1210 + (i % 2) * 90; d.ellipse([rx - 85, ry - 85, rx + 85, ry + 85], outline=c, width=26)
    d.rectangle([0, 0, W - 1, H - 1], outline=(255, 250, 230), width=30)
    im.save(p); return p

def _halftone(gray, cell=7, angle=45.0):
    """gray 0..1 array -> halftone dots (1 = paper, 0 = ink) as float array."""
    H, W = gray.shape; yy, xx = np.mgrid[0:H, 0:W].astype(float); a = math.radians(angle); u = (xx * math.cos(a) + yy * math.sin(a)) / cell; v = (-xx * math.sin(a) + yy * math.cos(a)) / cell
    d = np.hypot((u % 1) - 0.5, (v % 1) - 0.5) * 2 / 1.0   # 0 at cell centre .. ~1.4 at corners
    rad = np.sqrt(np.clip(1 - gray, 0, 1)) * 1.0           # ink radius
    return (d > rad).astype(float)

def photo_flop(out_png, w=1400, h=1000, seed=0):
    """the cast15 `flop` sprite of Dick over a bar against the sky / pines / sawdust, as a 1963 newspaper halftone (sepia ink on newsprint)."""
    import cast15, sprites
    from PIL import Image, ImageFilter
    sp = os.path.join(TEX, 'flop_sprite.png'); pose = cast15.pose_for('flop', 'dick')
    r = sprites.render_sprites([dict(cast='dick', pose=pose, px_per_D=200, out=sp, canvas=cast15.CANVAS15_WIDE)])[0]
    spr = Image.open(sp).convert('RGBA'); a = np.asarray(spr).astype(float) / 255
    # scene (grayscale): bright sky gradient, dark pine silhouettes, a light bar, dark sawdust
    yy, xx = np.mgrid[0:h, 0:w].astype(float); g = 0.88 - 0.38 * (yy / h) ** 1.2
    rng = np.random.RandomState(4); tree = np.zeros(w)
    for k in range(40): c = rng.uniform(0, w); wd = rng.uniform(30, 90); ht = rng.uniform(120, 330); tree = np.maximum(tree, np.clip(ht * (1 - np.abs(np.arange(w) - c) / wd), 0, None))
    base = h * 0.64; g = np.where(yy > base - tree[None, :], 0.20, g)
    g = np.where(yy > h * 0.80, 0.42 + 0.1 * np.sin(xx * 0.05), g)                                        # sawdust
    bar_y = int(h * 0.60); g[bar_y - 7:bar_y + 7, int(w * 0.10):int(w * 0.90)] = 1.0; g[int(h * 0.26):int(h * 0.80), int(w * 0.10):int(w * 0.10) + 10] = 0.15; g[int(h * 0.26):int(h * 0.80), int(w * 0.90) - 10:int(w * 0.90)] = 0.15
    # paste the sprite (scaled so the arch is ~55 % of the width): bar anchor on the bar line
    sw = int(spr.width * 0.95 * (w * 0.62 / 1400)); k = w * 0.62 / 880.0
    sc = spr.resize((int(spr.width * k), int(spr.height * k)), Image.LANCZOS); fx, fy = r['feet']; ax, ay = r['anchors']['bar']
    x0, y0, x1, y1 = r['canvas']; px_ax = (ax - fx - x0) * 200 * k; px_ay = (ay - fy - y0) * 200 * k
    ox = int(w * 0.52 - px_ax); oy = int(bar_y + 4 - px_ay)
    sa = np.asarray(sc).astype(float) / 255; gl = (0.30 * sa[..., 0] + 0.59 * sa[..., 1] + 0.11 * sa[..., 2]); al = sa[..., 3]
    # sprite luminance, contrast stretched so it reads as a figure
    gl = np.clip((gl - 0.15) * 1.25, 0, 1); canvas = g.copy(); hh, ww = gl.shape
    ys0 = max(0, oy); xs0 = max(0, ox); ys1 = min(h, oy + hh); xs1 = min(w, ox + ww)
    sub = canvas[ys0:ys1, xs0:xs1]; sg = gl[ys0 - oy:ys1 - oy, xs0 - ox:xs1 - ox]; sal = al[ys0 - oy:ys1 - oy, xs0 - ox:xs1 - ox]
    # soft drop shadow on the sawdust under the arch
    canvas[ys0:ys1, xs0:xs1] = sub * (1 - sal) + sg * sal
    ht = _halftone(np.clip(canvas, 0, 1), cell=9, angle=45.0)
    ink = np.array([46, 30, 20], float); paper = np.array([238, 222, 178], float)
    img = paper[None, None] * ht[..., None] + ink[None, None] * (1 - ht[..., None]); Image.fromarray(img.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(out_png)
    return out_png

def tex_newspaper(headline=('FOSBURY FLOPS', 'OVER BAR')):
    p = os.path.join(TEX, 'newspaper.png')
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 2400, 3200; paper = (240, 224, 176); ink = (36, 26, 20); im = Image.new('RGB', (W, H), paper); d = ImageDraw.Draw(im)
    # newsprint tone: mottled
    rng = np.random.RandomState(7); nz = rng.rand(H // 8, W // 8); nzi = Image.fromarray((nz * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(10))
    arr = np.asarray(im).astype(float) * (0.93 + 0.1 * (np.asarray(nzi).astype(float) / 255)[..., None]); im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    M = 110
    d.text((M, 130), 'VOL. LXXXVI  *  FRIDAY EDITION', font=_font('serif', 54), fill=ink, anchor='lm'); d.text((W - M, 130), 'MEDFORD, OREGON  *  5c', font=_font('serif', 54), fill=ink, anchor='rm')
    d.rectangle([M, 175, W - M, 188], fill=ink)
    _fit_text(d, 'MEDFORD MAIL TRIBUNE', (M, 215, W - M, 520), 'serif', ink)
    d.rectangle([M, 545, W - M, 560], fill=ink); d.rectangle([M, 575, W - M, 583], fill=ink)
    _fit_text(d, headline[0], (M, 640, W - M, 1000), 'serif', ink); _fit_text(d, headline[1], (M, 1010, W - M, 1370), 'serif', ink)
    d.rectangle([M, 1400, W - M, 1410], fill=ink)
    ph = photo_flop(os.path.join(TEX, 'photo_flop.png'), 1500, 1050); pim = Image.open(ph).convert('RGB'); pw = W - 2 * M - 650; ph_h = int(pw * 1050 / 1500)
    im.paste(pim.resize((pw, ph_h), Image.LANCZOS), (M, 1450)); d.rectangle([M - 6, 1444, M + pw + 6, 1450 + ph_h + 6], outline=ink, width=8)
    d.text((M, 1450 + ph_h + 40), 'Dick Fosbury, Medford High junior, arches over the bar at 5 ft 8 in.', font=_font('reg', 44), fill=ink, anchor='lm')
    # right column: fake text lines + a small second headline
    cx0 = M + pw + 60; cx1 = W - M
    _fit_text(d, 'BACKWARD', (cx0, 1450, cx1, 1620), 'serif', ink); _fit_text(d, 'LEAP WINS', (cx0, 1630, cx1, 1800), 'serif', ink)
    for i in range(30):
        y = 1850 + i * 46
        if y > 1450 + ph_h - 30: break
        d.rectangle([cx0, y, cx1 - int(rng.rand() * 140), y + 20], fill=(70, 56, 44))
    y0 = 1450 + ph_h + 130
    for c in range(4):
        cx = M + c * ((W - 2 * M) // 4); cw = (W - 2 * M) // 4 - 36
        d.rectangle([cx, y0, cx + cw, y0 + 8], fill=ink)
        for i in range(34):
            y = y0 + 40 + i * 44
            if y > H - 140: break
            d.rectangle([cx, y, cx + cw - int(rng.rand() * 120), y + 19], fill=(76, 60, 48))
    im.save(p); return p

# ============================================================================= the school extras: oval, infield, signs, scoreboard, bunting, poster, gym
def oval_track(P, M, rr):
    """full 400 m oval: the set's top half-ring (r 47-53 about (0,-34)) + two straights + a lower half-ring about (0,-74); chalk lines; green infield with mowing stripes and goal posts."""
    mb = S.MB('ovalA'); CX, CY = 0.0, -34.0; CY2 = -50.0
    S.ring(mb, M['cinder'], CX, CY2, 47, 47, 53, 53, 180, 360, 0.012, 1.0)
    for sx in (-1, 1):
        x0 = sx * 47 if sx > 0 else -53; mb.box(M['cinder'], (sx * 50.0, (CY + CY2) / 2, 0.012), (6.0, CY - CY2, 0.02))
        for r in (47.0, 49.0, 50.9, 52.85): mb.box(M['chalk'], (sx * r, (CY + CY2) / 2, 0.02), (0.1, CY - CY2, 0.004))
    for r in (47.0, 49.0, 50.9, 52.85): S.ring(mb, M['chalk'], CX, CY2, r, r, r + 0.1, r + 0.1, 180, 360, 0.02, 1.0)
    # infield mowing stripes
    gA = mat('stripeA', '#3ab01a', '#4cc424'); gB = mat('stripeB', '#2a9414', '#38a81c')
    for i, x in enumerate(np.arange(-30, 30, 6.0)): mb.box(gA if i % 2 else gB, (x + 3, -50.0, 0.004), (6.0, 64.0, 0.004))
    # field markings
    for (x0, y0, x1, y1) in [(-30, -82, 30, -82), (-30, -18, 30, -18)]: mb.box(M['chalk'], ((x0 + x1) / 2, y0, 0.02), (x1 - x0, 0.15, 0.004))
    for x in (-30, 30): mb.box(M['chalk'], (x, -50.0, 0.02), (0.15, 64.0, 0.004))
    mb.box(M['chalk'], (0, -50, 0.02), (60, 0.15, 0.004))
    S.ring(mb, M['chalk'], 0, -50, 8.0, 8.0, 8.15, 8.15, 0, 360, 0.02, 3.0)
    for yy in (-82.0, -18.0):                                                      # goal posts
        for xx in (-3.6, 3.6): mb.rod(M['cream'], (xx, yy, 0), (xx, yy, 6.0), 0.07, 0.07, 6)
        mb.rod(M['cream'], (-3.6, yy, 3.0), (3.6, yy, 3.0), 0.07, 0.07, 6)
    # parking lot / paved forecourt before the gym with lines
    mb.box(M['asphalt'], (16.0, 56.0, 0.011), (60.0, 8.0, 0.02))
    for i in range(20): mb.box(M['chalk'], (-12.0 + i * 3.0, 56.0, 0.024), (0.12, 5.0, 0.004))
    L.fin(mb, cast=False)

def school_extras(P, M, rr):
    """gym: big MEDFORD HIGH sign + gold trim + MEXICO 68 poster, flagpole, TRACK & FIELD gate arch, HIGH JUMP scoreboard, bunting in school colours, bleacher banner."""
    gx, gy = 16.0, 45.0; wall_y = gy - 6.06 - 0.2
    # --- MEDFORD HIGH on the gym front, between the two window rows
    p = tex_medford_high(); m = mat_tex('medford_high', p, k=0.95)
    w, h = 22.0, 2.95; zc = 5.95; x0 = gx - 2.0 - w / 2
    quad_obj('sign_medford_high', [(x0, wall_y, zc - h / 2), (x0 + w, wall_y, zc - h / 2), (x0 + w, wall_y, zc + h / 2), (x0, wall_y, zc + h / 2)], m)
    # --- MEXICO 68 poster beside the doors
    p = tex_mexico68(); m = mat_tex('mexico68', p, k=0.9)
    pw_, ph_ = 2.7, 3.6; px = gx + 0.0 - 0.2; pz = 3.0
    quad_obj('poster_mexico68', [(px, wall_y, pz - ph_ / 2 + 0.6), (px + pw_, wall_y, pz - ph_ / 2 + 0.6), (px + pw_, wall_y, pz + ph_ / 2 + 0.6), (px, wall_y, pz + ph_ / 2 + 0.6)], m)
    STATE['marks_m']['poster'] = (px + pw_ / 2, wall_y, pz + 0.6); STATE['marks_m']['gym_sign'] = (x0 + w / 2, wall_y, zc)
    # --- TRACK & FIELD arch at the track gate (north-west), board facing the infield (-y) and the road (+y)
    p = tex_track_field(); m = mat_tex('track_field', p, k=0.95)
    gxx, gyy = -24.0, 16.0; bw_, bh_ = 11.0, 2.4; zt = 6.4
    for sx in (-1, 1):
        mb = S.MB('gate'); mb.rod(M['wood'], (gxx + sx * (bw_ / 2 - 0.3), gyy, 0), (gxx + sx * (bw_ / 2 - 0.3), gyy, zt + 0.5), 0.2, 0.18, 8); L.fin(mb)
    mb = S.MB('gate2'); mb.box(M['red'], (gxx, gyy, zt - bh_ - 0.12), (bw_ + 0.6, 0.3, 0.2)); mb.box(M['yellow'], (gxx, gyy, zt + 0.12), (bw_ + 0.6, 0.3, 0.2)); L.fin(mb)
    quad_obj('sign_track_a', [(gxx - bw_ / 2, gyy - 0.2, zt - bh_), (gxx + bw_ / 2, gyy - 0.2, zt - bh_), (gxx + bw_ / 2, gyy - 0.2, zt), (gxx - bw_ / 2, gyy - 0.2, zt)], m)
    quad_obj('sign_track_b', [(gxx + bw_ / 2, gyy + 0.2, zt - bh_), (gxx - bw_ / 2, gyy + 0.2, zt - bh_), (gxx - bw_ / 2, gyy + 0.2, zt), (gxx + bw_ / 2, gyy + 0.2, zt)], m)
    STATE['marks_m']['gate_sign'] = (gxx, gyy - 0.2, zt - bh_ / 2)
    # --- HIGH JUMP scoreboard on two posts behind the pit
    p = tex_scoreboard(); m = mat_tex('scoreboard', p, k=0.95)
    sx_, sy_ = -9.0, 15.0; sw_, sh_ = 6.6, 2.75; sz_ = 2.6
    mb = S.MB('sbposts')
    for dx in (-sw_ / 2 + 0.5, sw_ / 2 - 0.5): mb.rod(M['wood'], (sx_ + dx, sy_, 0), (sx_ + dx, sy_, sz_ + 0.3), 0.12, 0.1, 7)
    mb.box(M['wood'], (sx_, sy_ + 0.12, sz_ + sh_ / 2), (sw_ + 0.4, 0.14, sh_ + 0.4)); L.fin(mb)
    quad_obj('scoreboard', [(sx_ - sw_ / 2, sy_ - 0.01, sz_), (sx_ + sw_ / 2, sy_ - 0.01, sz_), (sx_ + sw_ / 2, sy_ - 0.01, sz_ + sh_), (sx_ - sw_ / 2, sy_ - 0.01, sz_ + sh_)], m)
    STATE['marks_m']['scoreboard'] = (sx_, sy_ - 0.01, sz_ + sh_ / 2)
    # --- bunting: maroon / gold / white pennants along the bleacher, over the gate and from the gym to the poles
    mb = S.MB('bunting'); mats = ['maroonp', 'goldp', 'cream']
    M['maroonp'] = mat('maroonp', '#a82040', '#bc3050'); M['goldp'] = mat('goldp', '#f0c040', '#f4d060')
    for (a, b, n) in [((11.0, -3.0, 4.3), (11.0, 9.5, 4.3), 22), ((4.0, 17.0, 6.4), (-24.0, 16.0, 6.3), 40), ((-24.0, 16.0, 6.3), (-48.0, 12.0, 6.0), 36), ((16.0, 38.0, 11.0), (-9.0, 38.0, 11.0), 36), ((-9.0, 15.0, 5.8), (18.0, 15.0, 5.8), 44),
                      ((32.0, -2.0, 6.0), (32.0, 22.0, 6.0), 30)]:
        S.pennant_line(mb, M, a, b, n, mats, 1.4, 0.7)
    for (x, y, hh) in [(11.0, -3.0, 4.3), (11.0, 9.5, 4.3), (18.0, 15.0, 5.8), (32.0, -2.0, 6.0), (32.0, 22.0, 6.0), (-48.0, 12.0, 6.0)]: mb.rod(M['wood'], (x, y, 0), (x, y, hh + 0.2), 0.08, 0.06, 6)
    L.fin(mb, cast=False)
    # --- bleacher banner (maroon with gold stripe) on the front rail
    mb = S.MB('banner'); mb.box(M['maroonp'], (11.15, 3.5, 0.75), (0.06, 10.6, 0.7)); mb.box(M['goldp'], (11.1, 3.5, 0.75), (0.04, 10.6, 0.14)); L.fin(mb)

# ============================================================================= town
STREET_Y_EW = [30.2, 75.0, 120.0, 165.0, 210.0, -150.0, -195.0]     # east-west streets (centre y)
STREET_X_NS = [-85.0, 85.0, -135.0, 135.0, -185.0, 185.0, -45.0 - 120.0 * 0, 0.0]

def _excluded(x, y, pad=0.0):
    """school grounds + gym + parking + the track block where no houses may stand"""
    if -75 - pad < x < 75 + pad and -135 - pad < y < 60 + pad: return True
    return False

def town(P, M, rr):
    """houses (varied walls + red / green / blue / terracotta roofs), roads with dashed lines, street trees, church, water tower, shops, a river, farmland patches, parked + driving cars."""
    walls = [lin(h) for h in ('#fff4e0', '#ffe27a', '#8ed0ff', '#ffb39a', '#c4f09a', '#ffffff', '#ffd2a0', '#b8c8ff')]
    roofs = [lin(h) for h in ('#e02a1c', '#d01818', '#1e8a3c', '#1a52d8', '#b0301c', '#2a9a50', '#1c3cb8', '#f0561c', '#8a1c3a')]
    trees_c = [lin(h) for h in ('#ee5a12', '#ffc414', '#d82a14', '#2fa016', '#62c024', '#ff8a1c', '#e8a010')]
    trunk = lin('#6a3418'); doorc = [lin('#c01830'), lin('#1850c8'), lin('#ffc010')]; win = lin('#2c60d8'); road = lin('#46467e'); dash = lin('#ffd830'); curb = lin('#f0dca0')
    nmH = NM('houses'); nmR = NM('roads'); nmT = NM('streettrees'); nmC = NM('cars_parked'); nmL = NM('lawns')
    houses = []
    def road_ew(y, x0, x1, w=7.0):
        nmR.add('box', [((x0 + x1) / 2, y, 0.0)], [(x1 - x0, w, 0.03)], 0, road); nmR.add('box', [((x0 + x1) / 2, y - w / 2 - 0.35, 0.0)], [(x1 - x0, 0.7, 0.05)], 0, curb); nmR.add('box', [((x0 + x1) / 2, y + w / 2 + 0.35, 0.0)], [(x1 - x0, 0.7, 0.05)], 0, curb)
        xs = np.arange(x0 + 4, x1 - 4, 9.0); nmR.add('box', np.c_[xs, np.full(len(xs), y), np.full(len(xs), 0.03)], [(4.0, 0.25, 0.01)], 0, dash)
    def road_ns(x, y0, y1, w=7.0):
        nmR.add('box', [(x, (y0 + y1) / 2, 0.0)], [(w, y1 - y0, 0.03)], 0, road); nmR.add('box', [(x - w / 2 - 0.35, (y0 + y1) / 2, 0.0)], [(0.7, y1 - y0, 0.05)], 0, curb); nmR.add('box', [(x + w / 2 + 0.35, (y0 + y1) / 2, 0.0)], [(0.7, y1 - y0, 0.05)], 0, curb)
        ys = np.arange(y0 + 4, y1 - 4, 9.0); nmR.add('box', np.c_[np.full(len(ys), x), ys, np.full(len(ys), 0.03)], [(0.25, 4.0, 0.01)], 0, dash)
    XM = 300.0; YM0, YM1 = -260.0, 290.0
    for y in STREET_Y_EW: road_ew(y, -XM, XM)
    for x in [-85.0, 85.0, -135.0, 135.0, -185.0, 185.0, -235.0, 235.0]: road_ns(x, YM0, YM1)
    for x in (-45.0, 45.0, 0.0): road_ns(x, 33.0, YM1)                        # side streets behind the gym line
    # --- houses along every street (both sides), skipping the school
    def place_row(y_or_x, ew, lo, hi, side, setback=10.0):
        t = lo + rr.uniform(0, 8)
        while t < hi:
            wd = rr.uniform(8.0, 11.5); dp = rr.uniform(6.5, 9.0)
            if ew: x, y = t, y_or_x + side * (3.5 + setback + dp / 2); yaw = 0.0 if side < 0 else math.pi
            else: x, y = y_or_x + side * (3.5 + setback + dp / 2), t; yaw = math.pi / 2 if side < 0 else -math.pi / 2
            if not _excluded(x, y, 6) and not (ew and abs(y_or_x - 30.2) < 1 and False):
                houses.append((x, y, wd, dp, yaw, rr.randrange(len(walls)), rr.randrange(len(roofs))))
            t += wd + rr.uniform(4.0, 9.0)
    for y in STREET_Y_EW:
        for side in (-1, 1): place_row(y, True, -XM + 8, XM - 8, side)
    for x in [-85.0, 85.0, -135.0, 135.0, -185.0, 185.0, -235.0, 235.0]:
        for side in (-1, 1): place_row(x, False, YM0 + 10, YM1 - 10, side)
    # drop houses that overlap a road they do not belong to (cheap test: distance to every street centre-line must exceed the half width + yard)
    keep = []
    for (x, y, wd, dp, yaw, wi, ri) in houses:
        hw = max(wd, dp) / 2 + 1.0; ok = True
        for yy_ in STREET_Y_EW:
            if abs(y - yy_) < hw + 4.5: ok = False; break
        if ok:
            for xx_ in [-85.0, 85.0, -135.0, 135.0, -185.0, 185.0, -235.0, 235.0]:
                if abs(x - xx_) < hw + 4.5: ok = False; break
        if ok and y > 33 and abs(x) < 70 and abs(y) < 300:
            for xx_ in (-45.0, 45.0, 0.0):
                if abs(x - xx_) < hw + 4.5: ok = False; break
        if ok and (hfun(np.array([x]), np.array([y]))[0] > 3.0): ok = False
        if ok: keep.append((x, y, wd, dp, yaw, wi, ri))
    houses = keep; STATE['n_houses'] = len(houses)
    for (x, y, wd, dp, yaw, wi, ri) in houses:
        hz = rr.uniform(2.8, 3.4); rh = rr.uniform(1.8, 2.8)
        nmH.add('box', [(x, y, 0.0)], [(wd, dp, hz)], yaw, walls[wi])
        nmH.add('gable', [(x, y, hz - 0.02)], [(wd + 1.2, dp + 1.0, rh)], yaw, roofs[ri])
        if rr.random() < 0.55:
            cx_ = x + math.cos(yaw) * wd * 0.28; cy_ = y + math.sin(yaw) * wd * 0.28; nmH.add('box', [(cx_, cy_, hz + 1.0)], [(0.8, 0.8, 1.6)], yaw, lin('#b0301c'))
        fx = math.sin(-yaw) * 0; fdx = -math.sin(yaw) * 0; ndir = (math.sin(yaw), -math.cos(yaw))       # front normal of the footprint: local -y rotated by yaw
        door = doorc[rr.randrange(3)]; px_ = x + ndir[0] * (dp / 2 + 0.02); py_ = y + ndir[1] * (dp / 2 + 0.02)
        nmH.add('box', [(px_, py_, 0.0)], [(1.1, 0.12, 2.1)], yaw, door)
        for sx in (-0.30, 0.30):
            wx = x + math.cos(yaw) * wd * sx + ndir[0] * (dp / 2 + 0.02); wy = y + math.sin(yaw) * wd * sx + ndir[1] * (dp / 2 + 0.02); nmH.add('box', [(wx, wy, 1.1)], [(1.3, 0.12, 1.2)], yaw, win)
        # street trees / yard trees in front
        if rr.random() < 0.9:
            tx = x + ndir[0] * (dp / 2 + 3.2 + rr.uniform(-0.5, 0.8)) + math.cos(yaw) * rr.choice((-1, 1)) * wd * 0.55; ty = y + ndir[1] * (dp / 2 + 3.2) + math.sin(yaw) * rr.choice((-1, 1)) * wd * 0.2
            th = rr.uniform(5.5, 8.5); tc = trees_c[rr.randrange(len(trees_c))]
            nmT.add('cyl6', [(tx, ty, -0.2)], [(0.22, 0.22, th * 0.55)], 0, trunk); nmT.add('blob', [(tx, ty, th * 0.38)], [(th * 0.36, th * 0.36, th * 0.62)], rr.random() * 6, tc)
        if rr.random() < 0.5:   # parked car at the kerb
            carc = [lin(h) for h in ('#e0200e', '#1c54e0', '#10b8a8', '#ffc010', '#fff0b0', '#34d070', '#e0200e', '#7a2a9a')][rr.randrange(8)]
            cx_ = x + ndir[0] * (dp / 2 + 6.3); cy_ = y + ndir[1] * (dp / 2 + 6.3)
            if abs(ndir[0]) > 0.5: cyaw = math.pi / 2 + 0.0
            else: cyaw = 0.0
            nmC.add('box', [(cx_, cy_, 0.3)], [(4.4, 1.8, 0.7) if cyaw == 0 else (1.8, 4.4, 0.7)], 0, carc)
            nmC.add('box', [(cx_, cy_, 1.0)], [(2.2, 1.6, 0.55) if cyaw == 0 else (1.6, 2.2, 0.55)], 0, lin('#fff0c0'))
    # --- street trees along main street + roads (autumn colours), every 11 m
    for y in (30.2,):
        for sgn in (-1, 1):
            for x in np.arange(-290, 290, 11.0):
                if -62 < x < 62 and sgn > 0: continue
                if abs(x % 85) < 8: continue
                ty = y + sgn * 5.2; th = rr.uniform(6.0, 8.5); tc = trees_c[rr.randrange(len(trees_c))]
                nmT.add('cyl6', [(x, ty, -0.2)], [(0.22, 0.22, th * 0.55)], 0, trunk); nmT.add('blob', [(x, ty, th * 0.38)], [(th * 0.34, th * 0.34, th * 0.6)], rr.random() * 6, tc)
    # --- main street: a row of 2-storey shops with awnings east and west of the school (ground-level colour)
    shopc = [lin(h) for h in ('#ffd23c', '#ff6a4a', '#46b8ff', '#ffffff', '#ffa030', '#9ae860')]; awn = [lin(h) for h in ('#d01c2c', '#1c50d0', '#14a050', '#ffb000')]
    for sgn_x in (-1, 1):
        for i in range(9):
            x = sgn_x * (82 + i * 13.0) + (0 if sgn_x > 0 else -0); y = 41.0 + rr.uniform(-0.5, 0.5); wd = 11.0; hz = rr.uniform(6.0, 8.0)
            if abs(x) < 80 and False: continue
            nmH.add('box', [(x, y, 0)], [(wd, 9.0, hz)], 0, shopc[rr.randrange(len(shopc))]); nmH.add('box', [(x, y, hz)], [(wd + 0.4, 9.4, 0.5)], 0, lin('#6a2a1c'))
            nmH.add('box', [(x, y - 4.9, 3.0)], [(wd - 0.6, 1.8, 0.2)], 0, awn[rr.randrange(len(awn))]); nmH.add('box', [(x, y - 4.52, 0.0)], [(wd - 2.5, 0.1, 2.6)], 0, lin('#2a3c98'))
            for k in range(3): nmH.add('box', [(x - 3.6 + k * 3.6, y - 4.52, hz - 2.4)], [(1.5, 0.1, 1.5)], 0, lin('#2c60d8'))
    # --- church with steeple + water tower + silo
    cx, cy = 60.0, 90.0
    nmH.add('box', [(cx, cy, 0)], [(10.0, 20.0, 6.0)], 0, lin('#fffaf0')); nmH.add('gable', [(cx, cy, 5.98)], [(11.0, 21.0, 4.5)], math.pi / 2, lin('#c01828'))
    nmH.add('box', [(cx, cy - 11.0, 0)], [(4.5, 4.5, 15.0)], 0, lin('#fffaf0')); nmH.add('cone', [(cx, cy - 11.0, 15.0)], [(3.4, 3.4, 8.0)], 0.4, lin('#c01828'))
    wx, wy = -70.0, 100.0
    for dx, dy in ((-3, -3), (3, -3), (3, 3), (-3, 3)): nmH.add('cyl6', [(wx + dx, wy + dy, 0)], [(0.35, 0.35, 22.0)], 0, lin('#3c4cb0'))
    nmH.add('cyl', [(wx, wy, 22.0)], [(6.5, 6.5, 9.0)], 0, lin('#e8e0f0')); nmH.add('cone', [(wx, wy, 31.0)], [(6.8, 6.8, 3.4)], 0, lin('#c01828')); nmH.add('cyl', [(wx, wy, 21.5)], [(5.0, 5.0, 0.7)], 0, lin('#3c4cb0'))
    STATE['marks_m']['water_tower'] = (wx, wy, 26.0)
    # --- rail line? no. River south of the school: blue ribbon + bridge
    nmW = NM('river'); xs = np.linspace(-320, 320, 60); ys = -232.0 + 18.0 * np.sin(xs * 0.021) + 9.0 * np.sin(xs * 0.057 + 1.0)
    for i in range(len(xs) - 1):
        a = (xs[i], ys[i]); b = (xs[i + 1], ys[i + 1]); mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; ln = math.hypot(b[0] - a[0], b[1] - a[1]); yw = math.atan2(b[1] - a[1], b[0] - a[0])
        nmW.add('box', [(mx, my, 0.02)], [(ln + 0.8, 24.0, 0.03)], yw, lin('#1a6af0'))
    # --- farmland patchwork south / far east and west
    nmF = NM('fields'); fc = [lin(h) for h in ('#d8b81c', '#58c020', '#8ad024', '#e8a020', '#2aa838', '#b8d030', '#c86a1c')]
    for i in range(70):
        x = rr.uniform(-330, 330); y = rr.uniform(-300, 320)
        if (abs(x) < 280 and -255 < y < 300) and not (abs(y + 232) < 30): continue
        if hfun(np.array([x]), np.array([y]))[0] > 4: continue
        nmF.add('box', [(x, y, 0.0)], [(rr.uniform(20, 45), rr.uniform(20, 40), 0.04)], rr.uniform(-0.3, 0.3), fc[rr.randrange(len(fc))])
    objs = [nmH.finish(), nmR.finish(shadow=False), nmT.finish(), nmC.finish(), nmW.finish(shadow=False), nmF.finish(shadow=False)]
    return objs

# ============================================================================= moving cars (individual animated objects, keyed linear over the shot)
def moving_cars(M, f0=0, f1=140):
    """six 1960s cars driving along Main St (y 30) and Second St: parented to empties keyed LINEAR over frames f0..f1 (~9 m/s)."""
    spec = [('car_r', 'car_c', 30.2 - 1.8, -140.0, 0.0, 9.0), ('car_b', 'car_c', 30.2 + 1.8, 150.0, math.pi, 8.0), ('car_y', 'car_c', 30.2 - 1.8, -20.0, 0.0, 10.0), ('car_t', 'car_c', 75.0 + 1.8, 110.0, math.pi, 8.5),
            ('car_m', 'car_c', 75.0 - 1.8, -60.0, 0.0, 9.5), ('car_r', 'car_c', 30.2 + 1.8, 40.0, math.pi, 9.0)]
    out = []
    for i, (c1, c2, y, x0, yaw, v) in enumerate(spec):
        mb = S.MB('mcar%d' % i); PR.car60(mb, M, (0, 0, 0), 0.0, c1, c2); parts = L.adopt(mb.finish())
        e = bpy.data.objects.new('mcar_%d' % i, None); STATE['SET'].objects.link(e); e.parent = root(); e.rotation_euler = (0, 0, yaw)
        for o in parts: o.parent = e
        dirx = math.cos(yaw)
        e.location = (x0, y, 0.0); e.keyframe_insert('location', frame=f0); e.location = (x0 + dirx * v * (f1 - f0) / 30.0, y, 0.0); e.keyframe_insert('location', frame=f1)
        for fc in L.T._fcurves(e):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
        out.append(e)
    return out

# ============================================================================= school pines + god rays
def school_pines(M, rr):
    """tall pine groves around the school: a screen of pines behind the gym, groves left (west) and right (east) of the field so the camera descends past them, and sun gaps for the rays."""
    nm = NM('pines_school'); cols = [lin('#087a36'), lin('#0c8a44'), lin('#18902c'), lin('#0a6a40'), lin('#2a9a2a')]; tr = lin('#5a2c14'); pts = []
    def grove(x0, x1, y0, y1, n, h0, h1):
        for _ in range(n): pts.append((rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(h0, h1)))
    grove(-68, -40, 12, 34, 12, 13, 19); grove(36, 54, -8, 22, 12, 13, 19); grove(-60, 70, 64, 90, 22, 16, 24); grove(56, 74, -48, -10, 8, 12, 17); grove(-74, -56, -48, -8, 8, 12, 17)
    grove(-34, -16, 22, 32, 4, 11, 15); grove(48, 74, 24, 29, 5, 11, 15); grove(-120, -76, 36, 100, 22, 15, 22); grove(76, 125, 38, 100, 22, 15, 22)
    P = np.array([(a, b) for a, b, c in pts]); h = np.array([c for a, b, c in pts]); N = len(P)
    ci = np.array([rr.randrange(len(cols)) for _ in range(N)]); C = np.array([cols[i] for i in ci]) * (0.85 + 0.3 * np.array([rr.random() for _ in range(N)]))[:, None]
    nm.add('cyl6', np.c_[P, np.full(N, -0.3)], np.c_[h * 0.04, h * 0.04, h * 0.3], 0, np.broadcast_to(tr, (N, 3)))
    for k, (zf, rf, hf) in enumerate(((0.10, 0.30, 0.38), (0.30, 0.25, 0.36), (0.50, 0.20, 0.32), (0.68, 0.14, 0.30))):
        nm.add('cone', np.c_[P, np.full(N, 0.0) + h * zf], np.c_[h * rf, h * rf, h * hf], np.array([rr.random() * 6 for _ in range(N)]), C * (0.92 + 0.06 * k))
    STATE['school_pine_pts'] = [(a, b, c) for a, b, c in pts]
    return nm.finish()

_SHAFT_MAT = {}
def shaft_mat(color=(1.0, 0.72, 0.30), k=1.0):
    key = 'shaft'
    if key in _SHAFT_MAT: return _SHAFT_MAT[key]
    m = bpy.data.materials.new('E|shaft'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['UV'], sp.inputs[0])
    # across the beam: 1 - |2u-1|^2 smooth; along it: fade in over 18 %, out over the last 55 %; streaks: wave noise across u
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY_ADD'; a.inputs[1].default_value = 2.0; a.inputs[2].default_value = -1.0; Lk(sp.outputs['X'], a.inputs[0])
    b = N('ShaderNodeMath'); b.operation = 'ABSOLUTE'; Lk(a.outputs[0], b.inputs[0]); c = N('ShaderNodeMath'); c.operation = 'POWER'; c.inputs[1].default_value = 2.4; Lk(b.outputs[0], c.inputs[0])
    d = N('ShaderNodeMath'); d.operation = 'SUBTRACT'; d.inputs[0].default_value = 1.0; Lk(c.outputs[0], d.inputs[0] if False else d.inputs[1]); across = d
    f1 = N('ShaderNodeMapRange'); Lk(sp.outputs['Y'], f1.inputs['Value']); f1.inputs['From Min'].default_value = 0.0; f1.inputs['From Max'].default_value = 0.16; f1.interpolation_type = 'SMOOTHSTEP'
    f2 = N('ShaderNodeMapRange'); Lk(sp.outputs['Y'], f2.inputs['Value']); f2.inputs['From Min'].default_value = 1.0; f2.inputs['From Max'].default_value = 0.35; f2.interpolation_type = 'SMOOTHSTEP'
    wv = N('ShaderNodeTexNoise'); wv.inputs['Scale'].default_value = 7.0; wv.inputs['Detail'].default_value = 2; Lk(tc.outputs['UV'], wv.inputs['Vector'])
    st = N('ShaderNodeMapRange'); Lk(wv.outputs['Fac'], st.inputs['Value']); st.inputs['From Min'].default_value = 0.0; st.inputs['From Max'].default_value = 1.0; st.inputs['To Min'].default_value = 0.9; st.inputs['To Max'].default_value = 1.0
    m1 = N('ShaderNodeMath'); m1.operation = 'MULTIPLY'; Lk(across.outputs[0], m1.inputs[0]); Lk(f1.outputs['Result'], m1.inputs[1])
    m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY'; Lk(m1.outputs[0], m2.inputs[0]); Lk(f2.outputs['Result'], m2.inputs[1])
    m3 = N('ShaderNodeMath'); m3.operation = 'MULTIPLY'; Lk(m2.outputs[0], m3.inputs[0]); Lk(st.outputs['Result'], m3.inputs[1])
    k_ = N('ShaderNodeMath'); k_.operation = 'MULTIPLY'; k_.name = 'shaft_k'; k_.inputs[1].default_value = k; Lk(m3.outputs[0], k_.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1.0); Lk(k_.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); Lk(tr.outputs[0], ad.inputs[0]); Lk(em.outputs[0], ad.inputs[1])
    out = N('ShaderNodeOutputMaterial'); Lk(ad.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; _SHAFT_MAT[key] = m; return m

def god_rays(P, n=16, seed=5, strength=0.9, width=(3.0, 7.0), length=(38.0, 55.0), where=None, cross=True, z_range=(12.0, 16.0)):
    """fake volumetric light shafts: long additive emissive cards (Transparent + Emission, no shadow, no bounce) lying along the sun direction, starting in the pine canopy and ending on the field.
    Each shaft is a CROSS of two quads (90 deg apart about the beam axis) so it reads from any direction. strength = emission multiplier (0.9 default); shaft_k node of the material scales all."""
    rr = rnd(seed); m = shaft_mat(k=strength * 1.0); kd = Vector(P['key_dir']).normalized(); sd = -kd
    pts = where or [(rr.uniform(-60, 40), rr.uniform(20, 70)) for _ in range(n)]
    objs = []
    for i, (x, y) in enumerate(pts):
        ln = rr.uniform(*length); wd = rr.uniform(*width); top = Vector((x, y, rr.uniform(*z_range))); end = top + kd * ln
        if end.z < 0: ln = top.z / -kd.z; end = top + kd * ln
        ax = (end - top).normalized(); up = Vector((0, 0, 1)); side = ax.cross(up).normalized(); nrm = side.cross(ax).normalized()
        for q in range(2 if cross else 1):
            s = side if q == 0 else nrm; w0 = wd * (0.55 if q else 1.0)
            c0 = top - s * w0 / 2; c1 = top + s * w0 / 2; c2 = end + s * w0 * 0.9; c3 = end - s * w0 * 0.9           # widens toward the ground
            o = quad_obj('shaft_%d_%d' % (i, q), [c0, c1, c2, c3], m, uv=((0, 0), (1, 0), (1, 1), (0, 1))); objs.append(o)
    return objs

def tune_rays(k):
    m = _SHAFT_MAT.get('shaft')
    if m: m.node_tree.nodes['shaft_k'].inputs[1].default_value = k

# ============================================================================= people: low-poly chibi stand-ins (same proportions as the cast15 cards: head 0.5 m, 1.6 m tall)
SKINS = ['skin1', 'skin1', 'skin2', 'skin1', 'skinp']; HAIRS = ['hair', 'hairb', 'hairg', 'hair', 'hairr']

def mk_people_mats(M):
    M['skinp'] = mat('skinp', '#ffc090', '#f4a878', 6); M['hairb'] = mat('hairb', '#7a4418', '#965a24', 6); M['hairg'] = mat('hairg', '#d8b84a', '#f0cc5a', 6); M['hairr'] = mat('hairr', '#c8501c', '#e46a28', 6)
    M['maroon'] = mat('maroon', '#a01830', '#c42a42', 4); M['gold'] = mat('gold', '#ffc820', '#ffdc40', 4); M['white'] = mat('white', '#fff4e4', '#ffe6c8', 4); M['ink'] = mat('ink', '#1a1224', '#2a1c38', 4)
    M['pantsb'] = mat('pantsb', '#26348a', '#364aa8', 4); M['pantsk'] = mat('pantsk', '#d8b888', '#e8c898', 4); M['pantsg'] = mat('pantsg', '#4a4a64', '#5a5a78', 4)
    return M

def face_yaw(frm, to): return math.atan2(to[0] - frm[0], -(to[1] - frm[1]))

def person(mb, M, x, y, z, yaw, shirt='maroon', pants='pantsb', skin='skin1', hair='hair', pose='stand', s=1.0, phase=0.0, hat=None):
    """chibi figure, feet (or seat plank for 'sit') at z. Faces local -y rotated by yaw. poses: stand | cheer | sit | sit_cheer | stretch | lunge | run | wave."""
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    sit = pose.startswith('sit'); hz = 0.10 if sit else 0.62
    # torso, head
    lean = 0.0 if pose not in ('stretch',) else 0.25
    tz = hz + 0.27
    mb.box(M[shirt], (0, 0, tz), (0.46, 0.27, 0.56), rx=lean * 0.3)
    mb.box(M['white'] if shirt in ('maroon', 'blue', 'navy') else M['cream'], (0, -0.14, tz + 0.1), (0.2, 0.01, 0.26)) if shirt == 'maroon' else None
    hzc = tz + 0.55
    mb.ell(M[skin], (0, 0, hzc), (0.25, 0.24, 0.26), (8, 6)); mb.ell(M[hair], (0, 0.035, hzc + 0.07), (0.265, 0.26, 0.22), (8, 5))
    if hat: mb.ell(M[hat], (0, -0.01, hzc + 0.12), (0.27, 0.27, 0.15), (8, 4))
    mb.ell(M['ink'], (-0.085, -0.225, hzc - 0.01), (0.035, 0.02, 0.05), (5, 4)); mb.ell(M['ink'], (0.085, -0.225, hzc - 0.01), (0.035, 0.02, 0.05), (5, 4))
    # legs
    if sit:
        for sx in (-0.11, 0.11):
            mb.rod(M[pants], (sx, 0, hz), (sx, -0.42, hz), 0.085, 0.08, 6); mb.rod(M[pants], (sx, -0.42, hz), (sx, -0.44, hz - 0.45), 0.08, 0.07, 6); mb.box(M['ink'], (sx, -0.5, hz - 0.46), (0.13, 0.26, 0.07))
    elif pose == 'lunge':
        mb.rod(M[pants], (-0.11, 0, hz), (-0.14, -0.4, 0.28), 0.09, 0.08, 6); mb.rod(M[pants], (-0.14, -0.4, 0.28), (-0.14, -0.42, 0.04), 0.08, 0.07, 6)
        mb.rod(M[pants], (0.11, 0, hz), (0.13, 0.42, 0.2), 0.09, 0.08, 6); mb.rod(M[pants], (0.13, 0.42, 0.2), (0.13, 0.5, 0.04), 0.08, 0.07, 6)
        mb.box(M['ink'], (-0.14, -0.5, 0.04), (0.13, 0.26, 0.07)); mb.box(M['ink'], (0.13, 0.4, 0.04), (0.13, 0.26, 0.07))
    elif pose == 'run':
        a = math.sin(phase) * 0.35
        for sx, sg in ((-0.11, 1), (0.11, -1)):
            mb.rod(M[pants], (sx, 0, hz), (sx, -0.34 * a * sg * 2, 0.32), 0.09, 0.08, 6); mb.rod(M[pants], (sx, -0.34 * a * sg * 2, 0.32), (sx, -0.5 * a * sg * 2 - 0.06 * (1 - sg), 0.05 + 0.1 * (1 - sg) / 2), 0.08, 0.07, 6)
    else:
        for sx in (-0.11, 0.11): mb.rod(M[pants], (sx, 0, hz), (sx, 0, 0.05), 0.09, 0.08, 6); mb.box(M['ink'], (sx, -0.06, 0.04), (0.13, 0.26, 0.08))
    # arms
    sh_z = tz + 0.2
    for sx in (-1, 1):
        x0 = sx * 0.27
        if pose in ('cheer', 'sit_cheer'): p1 = (sx * 0.38, -0.05, sh_z + 0.5)
        elif pose == 'wave' and sx > 0: p1 = (sx * 0.42, -0.1, sh_z + 0.45)
        elif pose == 'stretch': p1 = (sx * 0.28, 0.0, sh_z + 0.55) if sx > 0 else (sx * 0.7, -0.1, sh_z - 0.1)
        elif sit: p1 = (sx * 0.3, -0.3, tz - 0.1)
        elif pose == 'run': p1 = (sx * 0.3, -0.3 * math.sin(phase) * sx, tz - 0.05)
        else: p1 = (sx * 0.32, 0.0, tz - 0.35)
        mb.rod(M[shirt], (x0, 0, sh_z), p1, 0.07, 0.06, 6); mb.ell(M[skin], p1, (0.07, 0.07, 0.07), (5, 4))
    mb.pop()

def fill_bleacher(mb, M, c, yaw, L_, rows, rr, density=0.7, seat_step=0.62, face=None, cheer=0.25):
    """spectators SITTING on the planks of a set bleacher (S.bleacher(mb, M, c, yaw, L, rows)): seat world position = c + R(yaw) (lx, row*0.85 - 0.15), plank top z = c.z + 0.45 (row+1) + 0.06.
    Returns the list of (x, y, z) seat positions used (metres)."""
    x0, y0, z0 = c; cs, sn = math.cos(yaw), math.sin(yaw); used = []
    shirts = ['maroon', 'gold', 'red', 'blue', 'white', 'teal', 'orange', 'navy', 'green', 'yellow', 'maroon', 'cream']; pants = ['pantsb', 'pantsk', 'pantsg', 'pantsb']
    # front direction of a seated person: local -y rotated by yaw -> toward the pit; person yaw = bleacher yaw
    for row in range(rows):
        n = int(L_ / seat_step) - 1
        for i in range(n):
            if rr.random() > density: continue
            lx = -L_ / 2 + 0.4 + i * seat_step + rr.uniform(-0.06, 0.06); ly = row * 0.85 - 0.15; zz = z0 + 0.45 * (row + 1) + 0.06
            wx = x0 + cs * lx - sn * ly; wy = y0 + sn * lx + cs * ly
            pose = 'sit_cheer' if rr.random() < cheer else 'sit'
            person(mb, M, wx, wy, zz, yaw if face is None else face_yaw((wx, wy), face), shirts[rr.randrange(len(shirts))], pants[rr.randrange(4)], SKINS[rr.randrange(5)], HAIRS[rr.randrange(5)], pose, s=rr.uniform(0.9, 1.08),
                   hat=('maroon' if rr.random() < 0.12 else None))
            used.append((wx, wy, zz))
    return used

def populate(M, rr, density=0.72):
    """spectators on the three bleachers, boys warming up (stretching, lunging, jogging, sitting on the benches), a coach's bench crew, parents along the fence."""
    mk_people_mats(M); mb = S.MB('folk')
    fill_bleacher(mb, M, (11.6, 3.5, 0.0), -1.5708, 11.0, 5, rr, density, cheer=0.3)            # main bleacher (faces the pit): the coach card stands in front (coach_bleacher)
    fill_bleacher(mb, M, (-27.0, 14.0, 0.0), 1.0, 9.0, 4, rr, 0.55, face=(0, 6)); fill_bleacher(mb, M, (30.0, 10.0, 0.0), -1.7, 8.0, 3, rr, 0.55, face=(0, 6))
    # boys warming up on the grass / run-up area (not on the card marks)
    shirts = ['maroon', 'maroon', 'blue', 'maroon', 'green', 'maroon', 'navy', 'maroon']
    spots = [(-3.0, -5.0, 'stretch'), (-4.4, -5.6, 'lunge'), (-1.8, -6.6, 'stretch'), (-5.8, -3.6, 'lunge'), (9.8, -7.0, 'stretch'), (11.0, -5.5, 'wave'), (-7.0, -7.2, 'stretch'), (-9.0, -4.5, 'lunge'),
             (3.2, -8.6, 'lunge'), (-12.5, 2.0, 'stretch'), (-13.8, 0.4, 'stretch'), (14.0, -9.0, 'lunge')]
    for i, (x, y, p) in enumerate(spots): person(mb, M, x, y, 0.0, face_yaw((x, y), (0.5, 5.0)) + rr.uniform(-0.6, 0.6), shirts[i % 8], 'pantsb' if i % 2 else 'pantsk', SKINS[i % 5], HAIRS[i % 5], p)
    for i in range(7):                                                                                         # joggers on the cinder (static, mid-stride)
        a = math.radians(rr.uniform(50, 130)); r = rr.choice((48.0, 49.9, 51.8)); x = r * math.cos(a); y = -34 + r * math.sin(a)
        person(mb, M, x, y, 0.02, a + math.pi / 2 + 3.14, ['maroon', 'gold', 'white', 'blue'][i % 4], 'pantsb', SKINS[i % 5], HAIRS[i % 5], 'run', phase=i * 1.1)
    # sitting on the benches
    for (bx, by, yawb, n) in [(7.4, -1.0, 0.0, 3), (9.0, -4.0, 0.0, 2), (-6.2, 2.4, 0.0, 3), (-8.4, -2.0, 0.0, 2), (-4.0, -6.0, 0.0, 2)]:
        for k in range(n):
            xx = bx + (k - (n - 1) / 2) * 0.8 * (1 if (bx, by) in [(-6.2, 2.4), (-8.4, -2.0), (-4.0, -6.0)] else 1); face = (0.5, 4.5)
            if (bx, by) == (7.4, -1.0): continue            # the cooler bench next to Dick's mark stays free for card boys
            person(mb, M, xx, by + 0.05, 0.48, face_yaw((xx, by), face), shirts[(k + int(bx)) % 8], 'pantsb', SKINS[k % 5], HAIRS[(k + 1) % 5], 'sit')
    # parents along the fence on the road side, little groups of 2-3 with coats
    for i in range(14):
        x = rr.uniform(-40, 44); y = 24.0 + rr.uniform(-0.5, 1.0)
        person(mb, M, x, y, 0.0, face_yaw((x, y), (rr.uniform(-3, 8), 4)), ['red', 'blue', 'yellow', 'teal', 'orange', 'green', 'cream', 'navy'][i % 8], 'pantsg', SKINS[i % 5], HAIRS[(i + 2) % 5], 'cheer' if i % 3 == 0 else 'stand', hat='red' if i % 4 == 0 else None)
    L.fin(mb)


def infield_life(M, rr):
    """the south half of the field is not empty: team tents (maroon / gold), a long-jump runway + pit, a pole-vault mat, hurdle rows on the straights, cones, relay runners, benches + gear piles."""
    mk_people_mats(M); mb = S.MB('infield')
    M['maroonp'] = M.get('maroonp') or mat('maroonp', '#a82040', '#bc3050'); M['goldp'] = M.get('goldp') or mat('goldp', '#f0c040', '#f4d060')
    M['sand'] = mat('sandA', '#ffd070', '#ffe08c', 6)
    # tents: four posts, striped pyramid roof, bench + coolers under it
    for i, (tx, ty, yw, c1) in enumerate([(-18, -30, 0.1, 'maroonp'), (-10, -30, 0.0, 'goldp'), (14, -28, -0.1, 'maroonp'), (22, -30, 0.1, 'blue')]):
        for dx, dy in ((-2.2, -2.2), (2.2, -2.2), (2.2, 2.2), (-2.2, 2.2)): mb.rod(M['metal'], (tx + dx, ty + dy, 0), (tx + dx, ty + dy, 2.6), 0.05, 0.05, 6)
        for k in range(4):
            a = k * math.pi / 2; mb.tri(M[c1 if k % 2 == 0 else 'white'], [(tx + 2.5 * math.cos(a) - 2.5 * math.sin(a), ty + 2.5 * math.sin(a) + 2.5 * math.cos(a), 2.55), (tx + 2.5 * math.cos(a + math.pi / 2) - 2.5 * math.sin(a + math.pi / 2), ty + 2.5 * math.sin(a + math.pi / 2) + 2.5 * math.cos(a + math.pi / 2), 2.55), (tx, ty, 3.6)])
        S.bench(mb, M, (tx, ty + 1.2, 0.0), 0.0, 3.0); S.cooler(mb, M, (tx - 1.4, ty - 0.8, 0.0)); S.bag(mb, M, (tx + 0.9, ty - 1.0, 0.0), 0.5, ['red', 'blue', 'teal', 'orange'][i], 0.7)
        for k in range(3): person(mb, M, tx - 1.0 + k * 1.0, ty + 1.15, 0.48, math.pi, ['maroon', 'gold', 'white'][k], 'pantsb', SKINS[(i + k) % 5], HAIRS[(i * 2 + k) % 5], 'sit')
    # long jump: runway + sand pit + board
    mb.box(M['dirt'], (-24, -62, 0.012), (30.0, 2.4, 0.02)); mb.box(M['sand'], (-6.5, -62, 0.014), (5.0, 3.2, 0.02)); mb.box(M['chalk'], (-9.0, -62, 0.03), (0.3, 2.4, 0.01))
    person(mb, M, -17.0, -62.0, 0.02, -math.pi / 2, 'maroon', 'pantsb', 'skin1', 'hair', 'run', phase=0.6)
    # pole-vault / high-jump style mats (blue) with standards
    for (yy, rx, ry) in ((-62.0, 2.6, 2.0), (-55.5, 1.6, 1.2)):                       # 1963: SAWDUST pits in a wooden frame (no foam anywhere)
        mb.box(M['wood'], (18.0, yy, 0.2), (rx * 2 + 0.3, ry * 2 + 0.3, 0.4)); mb.ell(M['saw'], (18.0, yy, 0.38), (rx, ry, 0.22), (14, 8))
    mb.rod(M['woodpale'], (15.0, -58.5, 0), (15.0, -58.5, 4.5), 0.05, 0.05, 6); mb.rod(M['woodpale'], (21.0, -58.5, 0), (21.0, -58.5, 4.5), 0.05, 0.05, 6)
    mb.rod(M['yellow'], (15.0, -58.5, 4.2), (21.0, -58.5, 4.2), 0.03, 0.03, 6)
    # hurdles on the straights (lane 2 / 3), cones, start blocks
    for k in range(9): S.hurdle(mb, M, (-49.0, -36.0 - k * 1.7, 0.0), math.pi / 2, 0.0); S.hurdle(mb, M, (51.0, -36.0 - k * 1.7, 0.0), math.pi / 2, 0.0)
    for k in range(12): S.cone_t(mb, M, (-46.0, -36.0 - k * 1.3, 0.0)); S.cone_t(mb, M, (47.6, -36.0 - k * 1.3, 0.0))
    # relay: four runners in a row on the south curve, a baton exchange
    for i in range(6):
        a = math.radians(rr.uniform(200, 340)); r = rr.choice((48.0, 50.0, 51.8)); x = r * math.cos(a); y = -50 + r * math.sin(a)
        person(mb, M, x, y, 0.02, a - math.pi / 2, ['maroon', 'gold', 'white', 'blue', 'red', 'maroon'][i], 'pantsb', SKINS[i % 5], HAIRS[i % 5], 'run', phase=i * 1.3)
    for i in range(16):
        x = rr.uniform(-26, 26); y = rr.uniform(-80, -20)
        if abs(x) > 12 and abs(x) < 26 and -34 < y < -26: continue
        person(mb, M, x, y, 0.0, rr.uniform(0, 6.28), ['maroon', 'gold', 'white', 'blue', 'maroon', 'green'][i % 6], 'pantsb' if i % 2 else 'pantsk', SKINS[i % 5], HAIRS[i % 5], rr.choice(['stretch', 'lunge', 'stand', 'wave', 'stand']))
    L.fin(mb)

def ground_detail(M, rr):
    """breaks up the flat dirt discs: grass edges, chalk arcs / dashes, dark scuffs and sand specks around the run-up and the benches."""
    mb = S.MB('gdetail'); gm = [M['gp1'], M['gp2'], M['grass']]
    for (cx, cy, rad) in [(1.4, 2.4, 4.4), (6.0, -2.2, 2.2), (-6.0, 1.8, 2.4), (8.2, -1.0, 1.6)]:
        for i in range(34):
            a = rr.uniform(0, 6.28); r = rad * rr.uniform(0.8, 1.15); S.disc(mb, gm[i % 3], (cx + r * math.cos(a), cy + r * math.sin(a)), rr.uniform(0.25, 0.7), 0.012 + 0.0003 * i, 8, rr.uniform(0.3, 0.9))
        for i in range(40):
            a = rr.uniform(0, 6.28); r = rad * rr.uniform(0.0, 0.8); mb.box(M['chip'] if i % 2 else M['sawdk'], (cx + r * math.cos(a), cy + r * math.sin(a), 0.014), (rr.uniform(0.1, 0.35), rr.uniform(0.03, 0.08), 0.004), rz=rr.random() * 6)
        S.ring(mb, M['chalk'], cx, cy, rad * 0.9, rad * 0.9, rad * 0.9 + 0.07, rad * 0.9 + 0.07, 20, 300, 0.016, 4.0)
    L.fin(mb, cast=False)

# ============================================================================= build
KILL_PREFIX = ('treesA_', 'hills_', 'tuftsA_', 'grass')       # replaced by v2 versions
def _kill(prefixes):
    for o in list(bpy.data.objects):
        if o.name.startswith(prefixes) or o.name in ('grass',): bpy.data.objects.remove(o, do_unlink=True)

def build_a2(light='HERO', town_on=True, people=True, rays=True, clouds=0.55, seed=1963, hills=True):
    """Build location A v2. light: 'HERO' (golden hour, deep blue sky) or 'HERODAY' (day, for T3's season shift). Returns the anchors dict (marks in D) + extra marks: poster, gym_sign, gate_sign, scoreboard."""
    t0 = time.time(); rr = rnd(seed); _SHAFT_MAT.clear()
    A = F.build('A', light); P = STATE['P']; M = STATE['M']; sc = bpy.context.scene
    recolor()
    _kill(KILL_PREFIX)
    sky_clouds(P, clouds)
    # the far ridge ring of set15 (emissive) was built with my P['hills'] already: kept as the distant blue-violet mountains
    terrain(P, rr)
    if hills: pines(rr)
    oval_track(P, M, rr)
    school_pines(M, rr)
    ground_detail(M, rr)
    infield_life(M, rr)
    school_extras(P, M, rr)
    if town_on:
        town(P, M, rr); moving_cars(M)
    if people: populate(M, rr)
    if rays: god_rays(P)
    # sun: a stronger warm key lamp, soft rim sun shares the direction
    sc.frame_start = 0
    A['marks'].update({k: F.D3(v) for k, v in STATE['marks_m'].items() if k in ('poster', 'gym_sign', 'gate_sign', 'scoreboard', 'water_tower')})
    STATE['A'] = A; STATE['v2_build_s'] = time.time() - t0
    return A

# ============================================================================= grounding: surface probe, cards that touch the ground, cast shadows
import importlib
_CT = None
def CT():
    """cast_test (put() helper) with its sprite cache redirected to work_v2_a/sprites."""
    global _CT
    if _CT is None:
        d = os.path.join(HERE, 'cast_test')
        if d not in sys.path: sys.path.insert(0, d)
        import cast15, sprites                     # cast15 BEFORE sprites
        _CT = importlib.import_module('cast_test'); _CT.SPR = os.path.join(WORK, 'sprites'); os.makedirs(_CT.SPR, exist_ok=True)
    return _CT

_IGN = ('actor_', 'shaft_', 'sign_', 'poster', 'scoreboard', 'newspaper', 'mcar', 'rimglow')
def surface_z(x, y, z_top=80.0):
    """z (D) of the first set surface below (x, y, z_top) in D (cards, signs, shafts and shadow quads are skipped). Ground = terrain; seats, pit sawdust, benches are found too."""
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); o = Vector((x, y, z_top)); d = Vector((0, 0, -1))
    for _ in range(12):
        hit, loc, nrm, idx, ob, mw = bpy.context.scene.ray_cast(dg, o, d)
        if not hit: return 0.0
        if ob.name.startswith(_IGN) or abs(nrm.z) < 0.5: o = loc + d * 0.002; continue
        return float(loc.z)
    return 0.0

def _shadow_mat(png, alpha):
    m = bpy.data.materials.new('castshadow'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'; ti = N('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha; Lk(ti.outputs['Alpha'], mu.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.01, 0.006, 0.05, 1.0); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); out = N('ShaderNodeOutputMaterial'); Lk(mx.outputs[0], out.inputs['Surface']); return m

def cast_shadow(tag, r, png, zg, alpha=0.82, kd=None):
    """the sprite's own silhouette projected onto the ground along the sun direction (a true long golden-hour shadow, dark violet). r = dict returned by put(); zg = surface z (D)."""
    kd = Vector(kd if kd is not None else STATE['P']['key_dir']).normalized(); hxy = Vector((kd.x, kd.y)); ln = hxy.length
    if ln < 1e-4 or kd.z > -0.05: return None
    sx, sy = hxy.x / (-kd.z), hxy.y / (-kd.z)                    # ground displacement per unit of height
    x0, y0, x1, y1 = r['res']['canvas']; k = r['scale']; X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
    mk = r['mk']; yaw = r['yaw']; ax = Vector((math.cos(yaw), math.sin(yaw), 0)); cs = []
    for (X, Z) in ((X0, Z0), (X1, Z0), (X1, Z1), (X0, Z1)):
        w = mk + ax * X + Vector((0, 0, Z)); h = max(w.z - zg, 0.0); cs.append((w.x + sx * h, w.y + sy * h, zg + 0.07))
    me = bpy.data.meshes.new('actor_s_' + tag); me.from_pydata(cs, [], [(0, 1, 2, 3)]); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(_shadow_mat(png, alpha)); ob = bpy.data.objects.new('actor_s_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; L.T.no_bounce(ob)
    return ob

def ground_card(tag, cast, pose, xy, cam_loc, z=None, scale=1.0, shadow='cast', shadow_a=0.82, contact=(1.6, 0.6), **kw):
    """Place a cast15 card so its feet TOUCH the surface: z = surface_z under xy (D) unless given (e.g. seat plank). Adds a soft contact ellipse + the long cast shadow.
    xy = (x, y) in D; cam_loc = camera position (D, the card yaws to face it). kw -> cast_test.put (ppd, mirror, yaw_off, canvas, anchor, ...). Returns put()'s dict plus ['z']."""
    ct = CT(); zz = surface_z(xy[0], xy[1]) if z is None else z
    r = ct.put(tag, cast, pose, mark=(xy[0], xy[1], zz), cam_loc=cam_loc, scale=scale, shadow=contact, **kw)
    if shadow == 'cast': cast_shadow(tag, r, os.path.join(ct.SPR, tag + '.png'), zz, shadow_a)
    r['z'] = zz; return r

def ground_card_anchor(tag, cast, pose, anchor, cam_loc, zg, scale=1.0, shadow_a=0.55, **kw):
    """Airborne / lying cards (flop, straddle, buried): placed by sprite anchor (`('bar', world_xyz)`); the cast shadow lands on the surface zg (sawdust top, D) under the body."""
    ct = CT(); r = ct.put(tag, cast, pose, cam_loc=cam_loc, scale=scale, anchor=anchor, shadow=None, **kw)
    cast_shadow(tag, r, os.path.join(ct.SPR, tag + '.png'), zg, shadow_a); r['z'] = zg; return r

# ============================================================================= rim / back light for cards (document: API_v2_a.md)
RIM = dict(on=False, to_light=(-0.7, -0.7), color=(1.0, 0.74, 0.30), width=5, strength=1.0, glow=0.5)
def rim_on(to_light=(-0.7, -0.7), color='#ffb040', width=5, strength=1.0, glow=0.5):
    """Turn the rim light on for every card put() AFTER this call. to_light = direction ON THE SCREEN from the figure towards the light (x right, y down: (-0.7, -0.7) = light up-left behind),
    color = hot gold, width in sprite pixels (ppd 128), glow = outer halo opacity. rim_off() restores plain cards."""
    c = hexl(color); RIM.update(on=True, to_light=tuple(to_light), color=tuple(min(1.0, v ** (1 / 2.2) * 1.25) for v in c), width=int(width), strength=float(strength), glow=float(glow))
    ct = CT()
    if not hasattr(ct, '_card_mat_orig'): ct._card_mat_orig = ct.card_mat
    ct.card_mat = _rim_card_mat
def rim_off():
    RIM['on'] = False; ct = CT()
    if hasattr(ct, '_card_mat_orig'): ct.card_mat = ct._card_mat_orig

def rim_png(png, to_light, color, width, strength, glow, out):
    from PIL import Image, ImageFilter
    im = Image.open(png).convert('RGBA'); a = np.asarray(im).astype(np.float32) / 255; al = a[..., 3]; H, W = al.shape
    lx, ly = to_light; n = math.hypot(lx, ly) or 1.0; lx, ly = lx / n, ly / n
    def shift(arr, dx, dy):
        out_ = np.zeros_like(arr); sx, sy = int(round(dx)), int(round(dy))
        ys0, ys1 = max(0, -sy), min(H, H - sy); xs0, xs1 = max(0, -sx), min(W, W - sx)
        out_[ys0:ys1, xs0:xs1] = arr[ys0 + sy:ys1 + sy, xs0 + sx:xs1 + sx]; return out_
    inside = np.ones_like(al)
    for s_ in range(1, width + 1): inside = np.minimum(inside, shift(al, lx * s_, ly * s_))       # pixels whose neighbours toward the light are all inside
    edge = np.clip(al * (1 - inside), 0, 1); edge = np.asarray(Image.fromarray((edge * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255 * (al > 0.2)
    rimc = np.array(color, np.float32)[None, None]; rgb = a[..., :3] * (1 - np.clip(edge * 0.95 * strength, 0, 1)[..., None]) + rimc * np.clip(edge * 0.95 * strength, 0, 1)[..., None]
    # outer halo on the light side
    gl = shift(al, lx * width * 0.7, ly * width * 0.7); gl = np.asarray(Image.fromarray((gl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(width * 1.3))).astype(np.float32) / 255 * (1 - al) * glow * strength
    A2 = np.maximum(al, np.clip(gl, 0, 1)); RGB = np.where(al[..., None] > 0.5, rgb, np.broadcast_to(rimc, rgb.shape))
    o = np.concatenate([RGB, A2[..., None]], -1); Image.fromarray((np.clip(o, 0, 1) * 255).astype(np.uint8), 'RGBA').save(out); return out

def _rim_card_mat(name, png, k=1.0):
    ct = CT(); d = os.path.join(ct.SPR, 'rim'); os.makedirs(d, exist_ok=True); out = os.path.join(d, os.path.basename(png))
    rim_png(png, RIM['to_light'], RIM['color'], RIM['width'], RIM['strength'], RIM['glow'], out)
    return ct._card_mat_orig(name, out, k)

# ============================================================================= newspaper prop (front page, readable, fills the frame)
def newspaper(cam_loc, look, dist=0.85, fill=1.16, roll_deg=2.0, bend=0.05, name='newspaper', hands=True):
    """The front page of the MEDFORD MAIL TRIBUNE (masthead, headline FOSBURY FLOPS OVER BAR, halftone photo of the arched jumper) as a bent paper mesh facing the camera.
    cam_loc, look in D (as F.cam_from); dist = metres in front of the lens; fill = page WIDTH relative to the frame width at that distance (1.16 = page a bit wider than the frame, headline stays inside).
    Returns the object. For a push-through animate `dist` (or the camera) over the frames."""
    png = tex_newspaper(); m = mat_tex('newspaper', png, k=0.92, tint=(1.0, 0.95, 0.84))
    cam = Vector(cam_loc) * DM; fwd = (Vector(look) * DM - cam).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
    wfr = 2 * dist * math.tan(math.atan(18.0 / 22.0 * 720 / 1280)); w = wfr * fill; h = w * 3200 / 2400
    cr, sr = math.cos(math.radians(roll_deg)), math.sin(math.radians(roll_deg)); rt = right * cr + up * sr; upv = up * cr - right * sr
    nu, nv = 14, 18; V = []; Fc = []; UV = []
    for j in range(nv + 1):
        for i in range(nu + 1):
            u = i / nu; v = j / nv; xx = (u - 0.5) * w; yy = (v - 0.5) * h - h * 0.12
            z = bend * w * (1 - (2 * u - 1) ** 2) * 0.5 + 0.02 * h * math.sin(v * 3.1)         # page bows toward the camera
            V.append(cam + fwd * (dist - z) + rt * xx + upv * yy); UV.append((u, v))
    for j in range(nv):
        for i in range(nu): a = j * (nu + 1) + i; Fc.append((a, a + 1, a + nu + 2, a + nu + 1))
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in V], [], Fc); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for pi, poly in enumerate(me.polygons):
        for li, vi in zip(poly.loop_indices, poly.vertices): uvl.data[li].uv = UV[vi]
    me.materials.append(m); ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob); ob.parent = root(); L.T.no_bounce(ob); ob.visible_shadow = False
    if hands:        # a reader's hands gripping the lower corners
        mb = S.MB('hands'); M = STATE['M']; mk_people_mats(M)
        for sg in (-1, 1):
            base = cam + fwd * (dist - bend * w * 0.1 - 0.012) + rt * (sg * w * 0.43) + upv * (-h * 0.44 - h * 0.12 * 0 + 0.0)
            # relative to the camera frame (mb works in set-local metres; build with a transform)
            Mx = Matrix(((rt.x, upv.x, fwd.x, base.x), (rt.y, upv.y, fwd.y, base.y), (rt.z, upv.z, fwd.z, base.z), (0, 0, 0, 1)))
            mb.push(Mx)
            mb.ell(M['skin1'], (0, 0, 0), (0.07, 0.04, 0.09), (8, 6)); mb.ell(M['skin1'], (-sg * 0.05, 0.0, 0.07), (0.035, 0.03, 0.06), (6, 4))
            for fi in range(4): mb.ell(M['skin1'], (-sg * (0.03 + fi * 0.028), -0.02, 0.03 + fi * 0.004), (0.022, 0.02, 0.07), (6, 4))
            mb.pop()
        L.fin(mb, cast=False)
    return ob

def set_grade_sat(sc, v):
    """per-shot saturation of the compositor grade (HueSat node of the GradeCLP group)."""
    for ng in bpy.data.node_groups:
        for n in ng.nodes:
            if n.bl_idname == 'CompositorNodeHueSat': n.inputs['Saturation'].default_value = v
    cg = getattr(sc, 'compositing_node_group', None)
    if cg:
        for n in cg.nodes:
            if n.bl_idname == 'CompositorNodeHueSat': n.inputs['Saturation'].default_value = v

def spot(x, y, r=5.0, k=1.2, color=(1.0, 0.8, 0.35)):
    """a soft additive pool of sunlight on the ground at (x, y) m (makes a tiny character findable from 100 m)."""
    m = bpy.data.materials.new('E|spot'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Location'].default_value = (-1.0, -1.0, 0); mp.inputs['Scale'].default_value = (2.0, 2.0, 2.0); Lk(tc.outputs['UV'], mp.inputs['Vector'])
    gr = N('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'; Lk(mp.outputs[0], gr.inputs['Vector'])
    ma = N('ShaderNodeMath'); ma.operation = 'SUBTRACT'; ma.inputs[0].default_value = 1.0; Lk(gr.outputs['Fac'], ma.inputs[1]); mc = N('ShaderNodeMath'); mc.operation = 'MULTIPLY'; mc.inputs[1].default_value = 2.0 * k; Lk(ma.outputs[0], mc.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1.0); Lk(mc.outputs[0], em.inputs['Strength']); tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); Lk(tr.outputs[0], ad.inputs[0]); Lk(em.outputs[0], ad.inputs[1])
    out = N('ShaderNodeOutputMaterial'); Lk(ad.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    z = 0.06
    return quad_obj('spot', [(x - r, y - r, z), (x + r, y - r, z), (x + r, y + r, z), (x - r, y + r, z)], m)


def sawdust_flecks(frame, position, strength=1.0, seed=0, floor=None):
    """v2 sawdust burst: SMALL flecks (2-4 cm grains, a few 6 cm splinters), low arcs (about 0.3 m high, 1 m out) that fall back and stay on the surface within ~0.5 s: nothing hangs in the air.
    Same geometry-node group as F.sawdust_spray; position (x, y, z) in D (z = the surface), floor = landing z in D."""
    M = STATE['M']; rr = rnd(91 + seed * 7 + int(frame)); p = Vector(position) * DM; fz = 0.02 if floor is None else (floor * DM - p.z) + 0.02
    items = []
    for i in range(int(70 * strength) + 10):
        az = rr.random() * 6.28; el = math.radians(rr.uniform(35, 68)); sp_ = rr.uniform(0.9, 2.3) * (0.6 + 0.4 * strength); ln = rr.choice((0.025, 0.03, 0.04, 0.045, 0.06)); rd = rr.uniform(0.1, 0.7)
        items.append((rd * math.cos(az), rd * math.sin(az), 0.03, sp_ * math.cos(el) * math.cos(az), sp_ * math.cos(el) * math.sin(az), sp_ * math.sin(el), ln))
    V_ = []; F_ = []; mi = []; C = []; Vv = []; Sp = []; Tl = []
    for (cx, cy, cz, vx, vy, vz, ln) in items:
        a = rr.random() * 6.28; B, Fs = F.boxes_np([(cx, cy, cz)], [(ln, ln * rr.uniform(0.4, 0.8), ln * 0.35)], [a]); t_land = (vz + math.sqrt(max(vz * vz + 19.62 * (cz - fz), 0.0))) / 9.81
        o = len(V_); V_ += B.tolist(); F_ += [[o + i for i in f] for f in Fs.tolist()]; mi += [rr.choice((0, 0, 1))] * 6; C += [(cx, cy, cz)] * 8; Vv += [(vx, vy, vz)] * 8; Sp += [(rr.uniform(-8, 8), rr.uniform(-8, 8), rr.uniform(-8, 8))] * 8; Tl += [t_land] * 8
    me = bpy.data.meshes.new('flecks'); me.from_pydata(V_, [], F_); me.update()
    for nm, typ, arr in (('c', 'FLOAT_VECTOR', C), ('v', 'FLOAT_VECTOR', Vv), ('sp', 'FLOAT_VECTOR', Sp), ('tl', 'FLOAT', Tl)):
        at = me.attributes.new(nm, typ, 'POINT')
        if typ == 'FLOAT': at.data.foreach_set('value', np.array(arr, dtype=np.float32))
        else: at.data.foreach_set('vector', np.array(arr, dtype=np.float32).reshape(-1))
    me.materials.append(M['saw']); me.materials.append(M['chip']); me.polygons.foreach_set('material_index', np.array(mi, dtype=np.int32))
    ob = bpy.data.objects.new('flecks_%d' % frame, me); STATE['SET'].objects.link(ob); ob.parent = root(); ob.location = p; L.T.no_bounce(ob)
    ng = F._spray_group().copy(); ng.nodes['start'].outputs[0].default_value = float(frame); md = ob.modifiers.new('spray', 'NODES'); md.node_group = ng
    return ob

def burial_mound(x, y, base, top, rr=None, r=(1.15, 0.95), toward=(0.0, -0.3)):
    """a real 3D sawdust mound (smooth ellipsoids + grains, metres) from z `base` to `top`, centred (x, y) shifted by `toward`: the buried coach sits inside it (card chest at `top`)."""
    rr = rr or rnd(7); M = STATE['M']; mb = S.MB('burial'); cx, cy = x + toward[0], y + toward[1]; h = top - base
    mb.ell(M['saw'], (cx, cy, base), (r[0], r[1], h), (24, 12)); mb.ell(M['saw'], (cx - 0.55, cy + 0.15, base), (r[0] * 0.7, r[1] * 0.7, h * 0.8), (18, 10)); mb.ell(M['saw'], (cx + 0.55, cy - 0.1, base), (r[0] * 0.65, r[1] * 0.7, h * 0.75), (18, 10))
    for i in range(160):
        a = rr.random() * 6.28; rd = rr.random() ** 0.6; xx = cx + math.cos(a) * rd * r[0]; yy = cy + math.sin(a) * rd * r[1]; zz = base + h * math.sqrt(max(0.0, 1 - rd * rd)) * 0.97
        mb.box(M['chip'] if i % 3 else M['sawdk'], (xx, yy, zz), (rr.uniform(0.04, 0.09), rr.uniform(0.015, 0.03), 0.01), rz=rr.random() * 6, rx=rr.uniform(-0.4, 0.4))
    L.fin(mb)
