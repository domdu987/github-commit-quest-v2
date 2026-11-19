"""set15_lib.py : shared pieces of the film-15 set (materials in the film house look, builder helpers, root, world, lights).
Metres inside the builders; the whole SET hangs under ROOT (scale U = 1/0.6): world units are D (1 D = 0.6 m, adult 3.0 D)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(HERE, 'styleboard'), os.path.join(PROJ, 'v3', 'set3d2')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import sb as S                                             # noqa: E402   (approved style board: props, MB, sky)

DM = 0.6                     # metres per D
U = 1.0 / DM                 # D per metre
STATE = T.STATE
def hexl(h): return S.hexc(h)[:3]
def rnd(s): return random.Random(s)
def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

# ----------------------------------------------------------------------------- lit material (house look, noise tones from the board)
def _lit_tail(nt, art, gain=1.0, shade_mul=1.0, shade_mix=None, form=True, add_emit=None):
    P = STATE['P']; L = nt.links.new; N = nt.nodes.new
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    kd = Vector(P['key_dir']).normalized(); geo = N('ShaderNodeNewGeometry')
    dot = N('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(geo.outputs['True Normal'], dot.inputs[0])
    cpos = N('ShaderNodeMath'); cpos.operation = 'MAXIMUM'; cpos.inputs[1].default_value = 0.0; L(dot.outputs['Value'], cpos.inputs[0])
    k0 = float(P.get('toon', 1.0))
    num = N('ShaderNodeMath'); num.name = 'gain_num'; num.operation = 'MULTIPLY_ADD'; num.inputs[1].default_value = (1.0 - k0) * gain; num.inputs[2].default_value = k0 * gain; L(cpos.outputs[0], num.inputs[0])
    mxn = N('ShaderNodeMath'); mxn.operation = 'MAXIMUM'; mxn.inputs[1].default_value = 0.12; L(dot.outputs['Value'], mxn.inputs[0])
    div = N('ShaderNodeMath'); div.operation = 'DIVIDE'; L(num.outputs[0], div.inputs[0]); L(mxn.outputs[0], div.inputs[1])
    emi = N('ShaderNodeEmission'); add = N('ShaderNodeAddShader')
    ms = N('ShaderNodeMix'); ms.name = 'sh_mul'; ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0
    sm = shade_mul if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3
    ms.inputs[7].default_value = (*[s * k for s, k in zip(P['shade'], sm)], 1.0)
    md = N('ShaderNodeVectorMath'); md.operation = 'SCALE'; L(div.outputs[0], md.inputs['Scale'])
    L(art, ms.inputs[6]); L(art, md.inputs[0])
    bw = N('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
    mmix = float(P.get('shade_mix', 0.0) if shade_mix is None else shade_mix)
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 1.0 - mmix; L(ms.outputs[2], sa.inputs[0])
    tb = N('ShaderNodeVectorMath'); tb.name = 'sh_tint'; tb.operation = 'SCALE'; L(bw.outputs[0], tb.inputs['Scale']); tb.inputs[0].default_value = tuple(x * mmix for x in P['shade_tint'])
    sab = N('ShaderNodeVectorMath'); sab.operation = 'ADD'; L(sa.outputs['Vector'], sab.inputs[0]); L(tb.outputs['Vector'], sab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.name = 'sh_lift'; lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P['lift']); L(sab.outputs['Vector'], lf.inputs[0]); amb = lf.outputs['Vector']
    if form and any(abs(x) > 1e-6 for x in P['form']):
        fd = N('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(P['form']); L(geo.outputs['True Normal'], fd.inputs[0])
        fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
        fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(amb, fs.inputs[0]); L(fa.outputs[0], fs.inputs['Scale']); amb = fs.outputs['Vector']
    if add_emit is not None:
        ea = N('ShaderNodeVectorMath'); ea.operation = 'ADD'; L(amb, ea.inputs[0]); ea.inputs[1].default_value = add_emit; amb = ea.outputs['Vector']
    L(amb, emi.inputs['Color']); emi.inputs['Strength'].default_value = 1.0
    L(md.outputs['Vector'], dif.inputs['Color']); L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1]); L(add.outputs['Shader'], out.inputs['Surface'])
    return out

def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0, gain=1.0, shade_mul=1.0, season=None, sval=0.0, crowd=False):
    """Board-style two-tone object-space noise (colour from the hex pair) shaded in the house look (key + painted blue-violet shade)."""
    key = '%s|%s' % (STATE['P']['name'], name)
    if key in S.MATS: return S.MATS[key]
    if crowd: gain = gain * STATE['P']['crowd_k']; shade_mul = shade_mul * STATE['P']['crowd_k']
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale * aniso[0], scale * aniso[1], scale * aniso[2]); L(tc.outputs['Object'], mp.inputs['Vector'])
    if B is not None:
        nz = N('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 4; nz.inputs['Roughness'].default_value = 0.6; L(mp.outputs[0], nz.inputs['Vector'])
        cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.5 - 0.2 / contrast; cr.color_ramp.elements[1].position = 0.5 + 0.2 / contrast; L(nz.outputs['Fac'], cr.inputs['Fac'])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = S.hexc(A); mx.inputs[7].default_value = S.hexc(B); L(cr.outputs[0], mx.inputs[0]); col = mx.outputs[2]
    else:
        rg = N('ShaderNodeRGB'); rg.outputs[0].default_value = S.hexc(A); col = rg.outputs[0]
    if season:      # (hexA2, hexB2): the colour pair of the other season, blended by the keyable Value node 'season'
        mxs = N('ShaderNodeMix'); mxs.data_type = 'RGBA'; mxs.inputs[6].default_value = S.hexc(season[0]); mxs.inputs[7].default_value = S.hexc(season[1])
        if B is not None: L(cr.outputs[0], mxs.inputs[0])
        sv = N('ShaderNodeValue'); sv.name = 'season'; sv.outputs[0].default_value = sval
        m2 = N('ShaderNodeMix'); m2.data_type = 'RGBA'; L(col, m2.inputs[6]); L(mxs.outputs[2], m2.inputs[7]); L(sv.outputs[0], m2.inputs[0]); col = m2.outputs[2]
    if wave:
        wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = wave[0]; wv.inputs['Distortion'].default_value = 1.5; wv.inputs['Detail'].default_value = 1; L(tc.outputs['Object'], wv.inputs['Vector'])
        cr2 = N('ShaderNodeValToRGB'); L(wv.outputs['Fac'], cr2.inputs['Fac']); cr2.color_ramp.elements[0].position = 0.35; cr2.color_ramp.elements[1].position = 0.65
        mx2 = N('ShaderNodeMix'); mx2.data_type = 'RGBA'; L(col, mx2.inputs[6]); mx2.inputs[7].default_value = S.hexc(wave[1]); L(cr2.outputs[0], mx2.inputs[0]); col = mx2.outputs[2]
    if zgrad:
        sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
        mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = zgrad[0]; mr.inputs['From Max'].default_value = zgrad[1]; L(sp.outputs['Z'], mr.inputs['Value'])
        mx3 = N('ShaderNodeMix'); mx3.data_type = 'RGBA'; mx3.inputs[6].default_value = S.hexc(zgrad[2]); L(col, mx3.inputs[7]); L(mr.outputs['Result'], mx3.inputs[0]); col = mx3.outputs[2]
    ae = None
    if emit and emit_k > 0: e = hexl(emit); ae = (e[0] * emit_k, e[1] * emit_k, e[2] * emit_k)
    _lit_tail(nt, col, gain, shade_mul, None, True, ae); m.cycles.emission_sampling = 'NONE'
    m['lit'] = 1; m['gain'] = float(gain); m['sm'] = float(shade_mul if not isinstance(shade_mul, (tuple, list)) else shade_mul[0]); m['crowd'] = int(bool(crowd))
    S.MATS[key] = m; return m

def mat_emit(name, hexcol, k):
    key = 'E|%s' % name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = S.hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

# the board's pal() calls its own module-level mat / mat_emit: swap them
S.mat = mat; S.mat_emit = mat_emit

# ----------------------------------------------------------------------------- scene plumbing
def root():
    r = bpy.data.objects.get('SETROOT')
    if r is None:
        r = bpy.data.objects.new('SETROOT', None); bpy.context.scene.collection.objects.link(r); r.scale = (U, U, U)
    return r

def adopt(objs, shadow=True, cast=True):
    """Move objects into SET, parent them to ROOT (scale U), hide from bounce rays."""
    SET = STATE['SET']; r = root()
    for o in objs:
        for c in list(o.users_collection): c.objects.unlink(o)
        SET.objects.link(o); o.parent = r; T.no_bounce(o)
        if not cast: o.visible_shadow = False
    return objs

def fin(mb, cast=True):
    return adopt(mb.finish(), cast=cast)

def new_obj(name, me, mat_=None, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, me); ob.location = loc
    if mat_ is not None: me.materials.append(mat_)
    adopt([ob]); return ob

def plane_at(m, size, z=0.0, c=(0, 0), name='ground'):
    me = bpy.data.meshes.new(name); me.from_pydata([(-size / 2, -size / 2, 0), (size / 2, -size / 2, 0), (size / 2, size / 2, 0), (-size / 2, size / 2, 0)], [], [(0, 1, 2, 3)])
    return new_obj(name, me, m, (c[0], c[1], z))

def sky_world(P):
    """The board's sky ramp + sun glow, seen by camera rays only (the lighting is the house key + painted shade)."""
    S.sky2(P); w = bpy.context.scene.world; nt = w.node_tree; bg = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBackground'][0]
    lp = nt.nodes.new('ShaderNodeLightPath'); mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = P['sky_k']
    nt.links.new(lp.outputs['Is Camera Ray'], mu.inputs[0]); nt.links.new(mu.outputs[0], bg.inputs['Strength'])
    w.light_settings.distance = 0.001

def ridges(P):
    mb = S.MB('hills'); rr = rnd(9)
    for li, (rad, bh, amp, col) in enumerate(P['hills']):
        m = mat_emit('hill%d_%s' % (li, P['name']), col, P['hill_k']); n = 240; ph = [rr.uniform(0, 6) for _ in range(4)]; pts = []
        for i in range(n + 1):
            t = i / n * 2 * math.pi; h = bh + amp * (0.5 * math.sin(t * 7 + ph[0]) + 0.3 * math.sin(t * 17 + ph[1]) + 0.2 * math.sin(t * 41 + ph[2]))
            pts.append((P['cx'] + rad * math.cos(t), P['cy'] + rad * math.sin(t), h))
        for i in range(n):
            a, b = pts[i], pts[i + 1]; mb.quad(m, [(a[0], a[1], -5), (b[0], b[1], -5), (b[0], b[1], b[2]), (a[0], a[1], a[2])])
    for o in adopt(mb.finish()): o.visible_shadow = False

def add_sun(P):
    k = max(P['key']); kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key_sun', d); STATE['LIGHTS'].objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); o.location = (-20, -40, 40); STATE['sun'] = o
    return o
