#!/usr/bin/env python3
"""ghost.py : the film-23 set ("ไอ้กองทัพลูกโป่ง", the Ghost Army, Normandy 1944 / the Rhine 1945): one lit 3D world (bpy 5.3, Cycles CPU)
for the flat 2D puppet cards.  1 unit = 1 D = one head, Z up.  Four locations in one world frame (LOCATIONS: origin of each), 19 shot cameras,
marks, setters.  See API.md.

    import ghost as GH
    A = GH.build('S07')                  # or GH.build('LANE', 'S07') / GH.build('RHINE') (default camera, no shot dressing)
    GH.key_camera('S07', f0=1)           # the eased move, one key per frame, planned length x 1.25
    GH.set_inflate('tank_hero', 0.4, frame=12) ...
CLI:  python3 ghost.py still <SHOT|LOCATION>[@t] [preview|final] [out.png]
      python3 ghost.py sheet | finals | ground | board (old style board)
Textures: ghost_tex.py + ghost_tex2.py (painted, cached in tex_ghost/).  Props: ghost_props.py.  Locations: ghost_fields.py, ghost_lane.py,
ghost_camp.py, ghost_rhine.py (+ the shared scenery in ghost_scenes.py).  Shots: ghost_shots.py.  Sheet / numbers: ghost_sheet.py."""
import os, sys, math, json, time, random, subprocess, re
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, ) + tuple(os.path.join(PROJ, 'v3', d) for d in ('set3d6', 'set3d5', 'set3d4', 'set3d2')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import ghost_tex as GX                                     # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_emit     # noqa: E402,F401
from mine import obox, rod, lumpy, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
STATE = T.STATE
OUT = os.path.join(HERE, 'board')
WORK = os.path.join(HERE, 'ghost_work')
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)
def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)

# ----------------------------------------------------------------------------- light presets
def kd_of(az, el):
    """key_dir (the direction the light TRAVELS) for a sun/moon at azimuth az (deg from +x CCW) and elevation el."""
    e = math.radians(el); a = math.radians(az)
    return (-math.cos(e) * math.cos(a), -math.cos(e) * math.sin(a), -math.sin(e))

_B = dict(toon=1.0, key_desat=0.0, ink='#1c1a2e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.06, sun_angle=0.6, lambert=False, lift=(0.030, 0.024, 0.060), lamps=0.0, ground_k=1.0)
LIGHTS = dict(
    # r3 shade model: shade = art x `shade` (cooled local colour) mixed with luminance x `shade_tint` at `shade_mix` (foliage: `fol_mix`); measured shade
    # hue ~245, sat ~0.40, value ~0.35 (about 0.5 of lit).  The shade is a REPLACEMENT colour: shade_cut() removes `amb_cut` of it where the key lands,
    # so lit colours stay clean and saturated.  sun_angle 2-2.5 deg gives soft penumbrae.  Saturation comes from the materials: grade_saturation ~1.05.
    DAWN=dict(_B, key=(1.50, 1.13, 0.69), sun_az=165.0, sun_el=19.0, sun_vis_el=6.0, sun_angle=2.5, sky='sky_dawn', sky_k=0.82, exposure=-0.5,
              shade=(0.30, 0.17, 0.66), shade_tint=(0.23, 0.14, 0.52), shade_mix=0.8, fol_mix=0.85, lift=(0.016, 0.018, 0.040), amb_cut=0.85,
              grade_offset=(-0.004, -0.006, -0.002), grade_saturation=1.06, bounce=(1.0, 0.7, 0.45, 0.12)),
    MORNING=dict(_B, key=(1.62, 1.20, 0.74), sun_az=172.0, sun_el=22.0, sun_angle=2.0, sky='sky_morning', sky_k=0.8, exposure=-0.65,
                 shade=(0.30, 0.17, 0.66), shade_tint=(0.23, 0.14, 0.52), shade_mix=0.8, fol_mix=0.85, lift=(0.016, 0.018, 0.040), amb_cut=0.85,
                 grade_offset=(-0.004, -0.006, -0.002), grade_saturation=1.04, bounce=(1.0, 0.7, 0.45, 0.14)),
    NIGHT=dict(_B, key=(0.30, 0.42, 1.25), sun_az=64.0, sun_el=24.0, sun_vis_el=17.0, sky='sky_night', sky_k=1.0, night=True, lambert=True, key_desat=0.2, ink='#10143a', lamps=1.0, bloom_size=0.07,
               shade=(0.22, 0.26, 0.52), shade_tint=(0.20, 0.18, 0.50), shade_mix=0.5, lift=(0.016, 0.018, 0.044), grade_offset=(0.002, 0.003, 0.010), grade_saturation=1.04),
)
# set r1: the Rhine night (moon south-east, over the German bank: it rims the decoys toward the enemy and lights the river) and the pre-dawn blue
LIGHTS['NIGHT'].update(sky='sky_night2', exposure=-0.2, shade=(0.31, 0.22, 0.58), shade_tint=(0.27, 0.17, 0.54), shade_mix=0.8, key=(0.44, 0.40, 1.25), grade_saturation=1.12)
LIGHTS['MORNING'].update(sky_k=0.95)
LIGHTS['NIGHT_R'] = dict(LIGHTS['NIGHT'], sun_az=-35.0, sun_el=26.0, sun_vis_el=21.0, sky='sky_night2r', exposure=0.3)
LIGHTS['DAY'] = dict(LIGHTS['MORNING'], sun_az=200.0, sun_el=34.0, exposure=-0.7, sky_k=1.0)
LIGHTS['PREDAWN'] = dict(LIGHTS['NIGHT'], key=(0.42, 0.56, 1.15), sun_az=8.0, sun_el=12.0, sun_vis_el=-8.0, sky='sky_predawn', lamps=0.4, exposure=0.05,
                         shade=(0.24, 0.30, 0.58), shade_tint=(0.22, 0.22, 0.54))
for _k, _v in LIGHTS.items(): _v['key_dir'] = kd_of(_v['sun_az'], _v['sun_el'])
SCENE_LIGHT = dict(dawn='DAWN', morning='MORNING', night='NIGHT', rhine='NIGHT_R')

# ----------------------------------------------------------------------------- the shared material: painted shade + one hard key (tower.mat_lit) with options
def mat_g(name, art='#808080', gain=1.0, shade_mul=1.0, form=True, smooth_n=False, shade_mix=None, glow=None, glow_k=0.0, alpha=False, spec=None, rim=None, interp='Linear', clip=False, lam=None):
    """art: '#hex' | png path | callable(nt) -> color socket or (color, alpha) sockets.  spec=(rgb,k,rough): GGX lobe from the key; rim=(rgb,k,power): warm
    rim glow on edges that face the sun; smooth_n: use the shading normal for the toon terminator (pillows); lam: force Lambert (default P['lambert'])."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    P = STATE['P']; m = bpy.data.materials.new(name); nt = T._tree(m); L = nt.links.new; N = nt.nodes.new
    lam = P.get('lambert', False) if lam is None else lam
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    kd = Vector(P['key_dir']).normalized(); geo = N('ShaderNodeNewGeometry'); nsock = geo.outputs['Normal' if smooth_n else 'True Normal']
    alpha_s = None
    if callable(art):
        r = art(nt); art_s, alpha_s = r if isinstance(r, tuple) else (r, None)
    elif isinstance(art, str) and art.startswith('#'):
        rgb = N('ShaderNodeRGB'); rgb.outputs[0].default_value = (*T.hex_lin(art), 1.0); art_s = rgb.outputs[0]
    else:
        tex = N('ShaderNodeTexImage'); tex.image = T._img(art); tex.interpolation = interp
        if clip: tex.extension = 'CLIP'
        art_s = tex.outputs['Color']; alpha_s = tex.outputs['Alpha']
    emi = N('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0; add = N('ShaderNodeAddShader')
    md = N('ShaderNodeVectorMath'); md.operation = 'SCALE'
    if lam:
        md.inputs['Scale'].default_value = gain
    else:
        dot = N('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(nsock, dot.inputs[0])
        cpos = N('ShaderNodeMath'); cpos.operation = 'MAXIMUM'; cpos.inputs[1].default_value = 0.0; L(dot.outputs['Value'], cpos.inputs[0])
        k0 = float(P.get('toon', 1.0)); num = N('ShaderNodeMath'); num.operation = 'MULTIPLY_ADD'; num.inputs[1].default_value = (1.0 - k0) * gain; num.inputs[2].default_value = k0 * gain; L(cpos.outputs[0], num.inputs[0])
        mxn = N('ShaderNodeMath'); mxn.operation = 'MAXIMUM'; mxn.inputs[1].default_value = T.COS_MIN; L(dot.outputs['Value'], mxn.inputs[0])
        div = N('ShaderNodeMath'); div.operation = 'DIVIDE'; L(num.outputs[0], div.inputs[0]); L(mxn.outputs[0], div.inputs[1]); L(div.outputs[0], md.inputs['Scale'])
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0
    sm = tuple(shade_mul) if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3
    ms.inputs[7].default_value = (*[s * k for s, k in zip(P['shade'], sm)], 1.0); L(art_s, ms.inputs[6])
    bw = N('ShaderNodeRGBToBW'); L(art_s, bw.inputs[0])
    kdm = N('ShaderNodeMix'); kdm.data_type = 'RGBA'; kdm.blend_type = 'MIX'; kdm.inputs[0].default_value = float(P.get('key_desat', 0.0)); L(art_s, kdm.inputs[6]); L(bw.outputs[0], kdm.inputs[7]); L(kdm.outputs[2], md.inputs[0])
    mmix = float(P.get('shade_mix', 0.0) if shade_mix is None else shade_mix); smm = sum(sm) / 3.0
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 1.0 - mmix; L(ms.outputs[2], sa.inputs[0])
    tb = N('ShaderNodeVectorMath'); tb.operation = 'SCALE'; L(bw.outputs[0], tb.inputs['Scale']); tb.inputs[0].default_value = tuple(x * mmix * smm for x in P.get('shade_tint', (0, 0, 0)))
    sab = N('ShaderNodeVectorMath'); sab.operation = 'ADD'; L(sa.outputs['Vector'], sab.inputs[0]); L(tb.outputs['Vector'], sab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P.get('lift', (0, 0, 0))); L(sab.outputs['Vector'], lf.inputs[0]); amb = lf.outputs['Vector']
    if form and any(abs(x) > 1e-6 for x in P['form']):
        fd = N('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(P['form']); L(nsock, fd.inputs[0])
        fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
        fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(amb, fs.inputs[0]); L(fa.outputs[0], fs.inputs['Scale']); amb = fs.outputs['Vector']
    if glow is not None and glow_k > 0:
        gt = N('ShaderNodeTexImage'); gt.image = T._img(glow); gs = N('ShaderNodeVectorMath'); gs.operation = 'SCALE'; gs.inputs['Scale'].default_value = glow_k
        L(gt.outputs['Color'], gs.inputs[0]); ga = N('ShaderNodeVectorMath'); ga.operation = 'ADD'; L(amb, ga.inputs[0]); L(gs.outputs['Vector'], ga.inputs[1]); amb = ga.outputs['Vector']
    L(amb, emi.inputs['Color']); L(md.outputs['Vector'], dif.inputs['Color'])
    L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1])
    aov = N('ShaderNodeOutputAOV'); aov.aov_name = 'amb'; L(amb, aov.inputs['Color'])          # r3: the ambient (shade) term, cut in sun by shade_cut()
    last = add.outputs['Shader']
    if rim:
        rc, rk, rp = rim; inc = N('ShaderNodeNewGeometry')
        dt = N('ShaderNodeVectorMath'); dt.operation = 'DOT_PRODUCT'; L(nsock, dt.inputs[0]); L(inc.outputs['Incoming'], dt.inputs[1])
        ab = N('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L(dt.outputs['Value'], ab.inputs[0]); sb = N('ShaderNodeMath'); sb.operation = 'SUBTRACT'; sb.inputs[0].default_value = 1.0; L(ab.outputs[0], sb.inputs[1])
        pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = rp; L(sb.outputs[0], pw.inputs[0])
        sd = N('ShaderNodeVectorMath'); sd.operation = 'DOT_PRODUCT'; sd.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(nsock, sd.inputs[0])
        sf = N('ShaderNodeMath'); sf.operation = 'ADD'; sf.use_clamp = True; sf.inputs[1].default_value = 0.35; L(sd.outputs['Value'], sf.inputs[0])
        mm = N('ShaderNodeMath'); mm.operation = 'MULTIPLY'; L(pw.outputs[0], mm.inputs[0]); L(sf.outputs[0], mm.inputs[1])
        re = N('ShaderNodeEmission'); re.inputs['Color'].default_value = (*rc, 1.0); re.inputs['Strength'].default_value = 1.0
        ms2 = N('ShaderNodeMath'); ms2.operation = 'MULTIPLY'; ms2.inputs[1].default_value = rk; L(mm.outputs[0], ms2.inputs[0]); L(ms2.outputs[0], re.inputs['Strength'])
        ad2 = N('ShaderNodeAddShader'); L(last, ad2.inputs[0]); L(re.outputs['Emission'], ad2.inputs[1]); last = ad2.outputs['Shader']
    if alpha and alpha_s is not None:
        tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(alpha_s, mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    if spec: MN._glossy(m, *spec)
    return m

def art_detail(base, detail, scale, k=0.6, extent='REPEAT'):
    """Ground art: painted patchwork x a tiled grass micro detail (UV scaled by `scale`)."""
    def f(nt):
        N = nt.nodes.new; L = nt.links.new; t1 = N('ShaderNodeTexImage'); t1.image = T._img(base)
        uv = N('ShaderNodeUVMap'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, 1.0); L(uv.outputs['UV'], mp.inputs['Vector'])
        t2 = N('ShaderNodeTexImage'); t2.image = T._img(detail); L(mp.outputs['Vector'], t2.inputs['Vector'])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = k; L(t1.outputs['Color'], mx.inputs[6]); L(t2.outputs['Color'], mx.inputs[7])
        return mx.outputs[2]
    return f

def art_star(base, star, c, size, side_min=0.45, tint=None):
    """Rubber art with a white star projected along object Y at object-space (x, z) = c (stars on both sides, only where |y| > side_min)."""
    def f(nt):
        N = nt.nodes.new; L = nt.links.new; tb = N('ShaderNodeTexImage'); tb.image = T._img(base)
        tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
        ux = N('ShaderNodeMath'); ux.operation = 'MULTIPLY_ADD'; ux.inputs[1].default_value = 1.0 / size; ux.inputs[2].default_value = 0.5 - c[0] / size; L(sp.outputs['X'], ux.inputs[0])
        uz = N('ShaderNodeMath'); uz.operation = 'MULTIPLY_ADD'; uz.inputs[1].default_value = 1.0 / size; uz.inputs[2].default_value = 0.5 - c[1] / size; L(sp.outputs['Z'], uz.inputs[0])
        cm = N('ShaderNodeCombineXYZ'); L(ux.outputs[0], cm.inputs['X']); L(uz.outputs[0], cm.inputs['Y'])
        ts = N('ShaderNodeTexImage'); ts.image = T._img(star); ts.extension = 'CLIP'; L(cm.outputs['Vector'], ts.inputs['Vector'])
        ay = N('ShaderNodeMath'); ay.operation = 'ABSOLUTE'; L(sp.outputs['Y'], ay.inputs[0]); gt = N('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = side_min; L(ay.outputs[0], gt.inputs[0])
        am = N('ShaderNodeMath'); am.operation = 'MULTIPLY'; L(ts.outputs['Alpha'], am.inputs[0]); L(gt.outputs[0], am.inputs[1])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MIX'; L(am.outputs[0], mx.inputs[0]); L(tb.outputs['Color'], mx.inputs[6]); L(ts.outputs['Color'], mx.inputs[7])
        return mx.outputs[2]
    return f

# ----------------------------------------------------------------------------- mesh banks (+ set r1 prop groups)
class Banks:
    """Named mesh banks (one object each).  set r1: `with Bk.prop('crate'):` puts every bank a builder opens into one PROP GROUP: after flush the
    group's first shadow-casting part becomes the prop object (named after the group, gc_role 'prop'), the other parts are parented to it
    (gc_role 'skip'), and build() snaps the prop onto the ground (ground_snap) and gives it a contact shadow (contact_shadow)."""
    def __init__(s): s.b = {}; s.hull = {}; s.shadow = {}; s.smooth = {}; s.grp = None; s.groups = {}; s.order = []; s.n = 0
    def __call__(s, name, hull=0.0, shadow=True, smooth_=False):
        if s.grp is not None:
            name = s.grp + '~' + name
            if name not in s.groups[s.grp]['banks']: s.groups[s.grp]['banks'].append(name)
        if name not in s.b: s.b[name] = MB(); s.hull[name] = hull; s.shadow[name] = shadow; s.smooth[name] = smooth_
        return s.b[name]
    def prop(s, gname, shadow_r=None, snap=True, role='prop', airborne=False, main=None):
        s.n += 1; g = gname[1:] if gname.startswith('=') else '%s.%03d' % (gname, s.n); s.groups[g] = dict(banks=[], shadow_r=shadow_r, snap=snap, role=role, airborne=airborne, main=main); s.order.append(g)
        bk = s
        class _Ctx:
            def __enter__(self_): bk.grp = g; return g
            def __exit__(self_, *a): bk.grp = None; return False
        return _Ctx()
    def flush(s, SET):
        made = {}
        for n, mb in s.b.items():
            if mb.f:
                ob = _obj(mb, n, SET, hull=s.hull[n], shadow=s.shadow[n]); made[n] = ob
                if s.smooth[n]:
                    for p in ob.data.polygons: p.use_smooth = True
        for g in s.order:
            G = s.groups[g]; parts = [made[b] for b in G['banks'] if b in made]
            if not parts: continue
            main = next((o for o in parts if G['main'] and o.name.endswith('~' + G['main'])), None) or next((o for o in parts if o.visible_shadow), parts[0])
            main.name = g; main['gc_role'] = G['role']
            if G['airborne']: main['airborne'] = True
            for o in parts:
                if o is main: continue
                o['gc_role'] = 'skip'; o.parent = main; o.matrix_parent_inverse = main.matrix_world.inverted()
            STATE.setdefault('props', []).append((main, G['shadow_r'], G['snap']))
            STATE.setdefault('objects', {})[g] = main
        s.b = {}; s.order = []; s.groups = {}

def view_ok(p, margin=0.15, cam=None):
    """True if world point p projects inside the frame (with a margin of the frame) - used to skip hidden geometry."""
    cam = cam or STATE.get('cam_ob')
    if cam is None: return True
    q = cam.matrix_world.inverted() @ Vector(p)
    if q.z > -0.3: return False
    t = (cam.data.sensor_width / 2.0) / cam.data.lens                      # AUTO fit: the sensor width spans the long (vertical) side
    ny = (q.y / -q.z) / t; nx = (q.x / -q.z) / (t * 720.0 / 1280.0)
    return abs(nx) <= 1 + margin and abs(ny) <= 1 + margin

# ----------------------------------------------------------------------------- terrain
def make_terrain(scene, rect=None, step=None, mat='ground', name='terrain', hole=None, uvrect=None):
    """Height-field grid from STATE['gz'] over rect (default the scene's painted rect); hole=(x0,x1,y0,y1) leaves the inner cells out (far ring)."""
    cfg = GX.SCENES[scene]; x0, x1, y0, y1 = rect or cfg['rect']; ux0, ux1, uy0, uy1 = uvrect or cfg['rect']; st = step or STATE.get('terrain_step', 4.0)
    gz = STATE['gz']; nx = int(round((x1 - x0) / st)); ny = int(round((y1 - y0) / st)); M = STATE['M']; mb = MB(); mb.pid += 1
    xs = [x0 + (x1 - x0) * i / nx for i in range(nx + 1)]; ys = [y0 + (y1 - y0) * j / ny for j in range(ny + 1)]
    Z = [[gz(x, y) for y in ys] for x in xs]
    for i in range(nx):
        for j in range(ny):
            if hole and hole[0] <= xs[i] and xs[i + 1] <= hole[1] and hole[2] <= ys[j] and ys[j + 1] <= hole[3]: continue
            p = [(xs[i], ys[j]), (xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])]; z = [Z[i][j], Z[i + 1][j], Z[i + 1][j + 1], Z[i][j + 1]]
            mb.face([V((p[k][0], p[k][1], z[k])) for k in range(4)], M[mat], [((p[k][0] - ux0) / (ux1 - ux0), (p[k][1] - uy0) / (uy1 - uy0)) for k in range(4)])
    ob = _obj(mb, name, STATE['SET'], shadow=True); ob['gc_role'] = 'ground'; return ob

def tex_path(name): return STATE['tx'][name]

# ----------------------------------------------------------------------------- locations (one world frame: each location's local frame sits at `origin`)
LOCATIONS = dict(
    FIELDS=dict(scene='dawn', light='DAWN', origin=(0.0, 0.0, 0.0), cam=dict(loc=(-16.0, -72.0, 66.0), look_at=(4.0, 62.0, 0.0), lens=24),
                note='Normandy bocage at dawn: the patchwork valley, the tank column on the winding lane, farm, village, river'),
    LANE=dict(scene='morning', light='MORNING', origin=(-700.0, -260.0, 0.0), cam=dict(loc=(0.8, -12.5, 2.0), look_at=(-0.3, 17.0, 2.45), lens=30),
              note='the farm lane 700 D west of the column (in the FIELDS far patchwork): inflation site, decoy field, jeep, bikes, the ending'),
    CAMP=dict(scene='night', light='NIGHT', origin=(760.0, -180.0, 0.0), cam=dict(loc=(-2.0, -31.0, 9.5), look_at=(3.0, 12.0, 6.4), lens=22),
              note='the moonlit decoy camp 760 D east of the column: tank rows, sound truck, radio tent, lanterns'),
    RHINE=dict(scene='rhine', light='NIGHT_R', origin=(0.0, 9000.0, 0.0), cam=dict(loc=(-150.0, -230.0, 70.0), look_at=(-20.0, 40.0, 0.0), lens=22),
               note='the Rhine, March 1945 (9000 D north = the next spring, Germany): river along local +y, US bank west, decoy field south-west, crossing north, German OP east'),
)
ALIAS = dict(dawn='FIELDS', morning='LANE', night='CAMP', rhine='RHINE')
def loc_origin(location=None): return Vector(LOCATIONS[location or STATE['location']]['origin'])
def to_world(p, location=None):
    o = loc_origin(location); return (p[0] + o.x, p[1] + o.y, (p[2] if len(p) > 2 else 0.0) + o.z)
def to_local(p, location=None):
    o = loc_origin(location); return (p[0] - o.x, p[1] - o.y, (p[2] if len(p) > 2 else 0.0) - o.z)

# ----------------------------------------------------------------------------- build
def _shots():
    import ghost_shots as SH; return SH

def build(location, shot=None, light=None, cards=True, dress=True):
    """Build one location into the current scene.  build('S07') = build('LANE', 'S07').  With a shot: its light, its foreground prop, its state at
    the middle of the move (un-keyed), placeholder cards at its marks (cards=False leaves them out) and the camera at t = 0.  Returns the anchors dict."""
    SH = _shots()
    if shot is None and location in SH.SHOTS: shot = location; location = None
    sh = SH.SHOTS[shot] if shot else None
    location = ALIAS.get(location, location) or sh['loc']
    if sh: assert sh['loc'] == location, (shot, location)
    L_ = LOCATIONS[location]; scene_name = L_['scene']; lk = light or (sh['light'] if sh else L_['light'])
    sc = bpy.context.scene; P = dict(LIGHTS[lk])
    if os.environ.get('GH_P'): P.update(json.loads(os.environ['GH_P'])); P['key_dir'] = kd_of(P['sun_az'], P['sun_el'])     # tuning override (JSON)
    STATE.clear(); STATE.update(P=P, scene=scene_name, light=lk, location=location, shot=shot)
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_pre):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_sky_follow', '_follow'): h.remove(f)
    for ob in list(sc.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    import ghost_props as PR; PR._TANK_CACHE.clear()
    SET = T._coll('SET', sc); LIG = T._coll('LIGHTS', sc); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    CARDS = T._coll('CARDS', sc); T._wipe(CARDS); STATE['CARDS'] = CARDS
    for m in list(bpy.data.materials):
        if m.name.startswith(('GH_', 'ink')): bpy.data.materials.remove(m)
    import ghost_tex2 as GX2                                                                 # noqa: F401 (registers the r1 textures)
    names = ['glow', 'pool', 'mist', 'hedge', 'leaf', 'poplar', 'apple', 'roof_red', 'roof_red_d', 'roof_slate', 'stone_farm', 'stone_wall', 'stone_church', 'barn_wood', 'wood', 'canvas_khaki', 'canvas_olive',
             'camonet', 'rubber', 'rubber_d', 'rubber_l', 'star', 'water', 'cow', 'cow_b', 'puff', 'grass_detail', 'sign', 'tankmark', 'crate_a', 'crate_b', 'crate_c', 'crate_plain', 'dirt', 'rut',
             'fields_' + scene_name, P['sky'], 'crate_30', 'crate_79', 'crate_chalk', 'sign_rhine', 'sandbag', 'record', 'water_night', 'glints']
    names.append('fields_far')
    names += [n for n in GX.JOBS if n.startswith('sol_')]
    STATE['tx'] = GX.ensure(names, verbose=False)
    w = bpy.data.worlds.get('W_ghost') or bpy.data.worlds.new('W_ghost'); sc.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(sc, 'final'); sc.render.threads = 4; sc.frame_start = 1; sc.frame_current = 1
    pre = 'GH_%s_' % scene_name; STATE['pre'] = pre; STATE['PR'] = PR
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    if P.get('bounce'):
        br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
        d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
        o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    STATE.update(marks={}, lamps=[], objects={}, props=[], cards=[], tank_objs={})
    PR.setup_materials(P, STATE['tx'], pre)
    ref = SH.pose(shot, 0.5, local=True) if sh else dict(L_['cam'])                         # the layout camera (local frame): billboards / tufts face it
    STATE['cam'] = ref; cam = make_camera(ref); STATE['cam_ob'] = cam
    Bk = Banks(); STATE['B'] = Bk
    sky_dome(SET, P)
    import ghost_scenes as SCN
    mod = dict(FIELDS='ghost_fields', LANE='ghost_lane', CAMP='ghost_camp', RHINE='ghost_rhine')[location]
    LM = __import__(mod); LM.build(Bk, STATE['M'], shot)
    if sh and dress: SH.dress(shot, Bk, STATE['M'])
    Bk.flush(SET)
    finish_location(location)
    sc.cycles.use_light_tree = (lk in ('NIGHT', 'NIGHT_R', 'PREDAWN'))
    MN._denoise(sc); setup_grade(sc); shade_cut(sc, P)
    for ob in SET.objects: no_bounce(ob)
    if STATE.get('glossy_ok'): _glossy_setup()
    sc.view_settings.exposure = float(P.get('exposure', 0.0))
    if sh:
        if sh.get('state'): apply_state(sh['state'])
        if cards: place_cards(shot)
        shot_camera(shot, 0.0)
    else:
        make_camera(dict(loc=to_world(L_['cam']['loc']), look_at=to_world(L_['cam']['look_at']), lens=L_['cam']['lens']))
    A = dict(location=location, shot=shot, light=lk, key_dir=tuple(kd), origin=tuple(loc_origin()), marks=marks(shot) if sh else {},
             anchors={k_: tuple(to_world(v)) for k_, v in STATE['marks'].items()}, tanks=sorted(STATE['tank_objs']))
    STATE['A'] = A; return A

def _glossy_setup():
    """RHINE: the river reflects (one glossy bounce): lanterns, halos, the tent glow, the decoys, trucks, trees, sky and moon are seen by glossy rays."""
    for ob in STATE['SET'].objects:
        n = ob.name
        if ob.get('tank') or n.startswith(('lantern', 'tent', 'sound_truck', 'truck', 'sky', 'sun_disc', 'poplar', 'trees', 'boat', 'pontoons', 'sign', 'crate', 'farm', 'sandbags', 'hut', 'tripod')) or '~halos' in n or '~lanterns' in n or '~tent_in' in n:
            ob.visible_glossy = True
    for ob in STATE['CARDS'].objects: ob.visible_glossy = True

def quality(sc=None, q='final', scale=None, samples=None):
    """Render settings of the set (tower.setup_render + OIDN + 4 threads + this location's extras: RHINE gets one glossy bounce for the river)."""
    sc = sc or bpy.context.scene; MN.setup_render(sc, q); sc.render.threads = 4
    if scale: sc.render.resolution_percentage = int(round(scale * 100))
    if samples: sc.cycles.samples = samples
    if STATE.get('glossy_ok'): sc.cycles.glossy_bounces = 1; sc.cycles.max_bounces = 2
    sc.cycles.use_light_tree = STATE.get('light') in ('NIGHT', 'NIGHT_R', 'PREDAWN')
    MN._denoise(sc); sc.view_settings.exposure = float(STATE['P'].get('exposure', 0.0)); return sc

def finish_location(location):
    """Parent the location to its root (origin in the world), then ground-snap every prop and give it a contact shadow."""
    SET = STATE['SET']; root = bpy.data.objects.new('LOC_ROOT_' + location, None); SET.objects.link(root); STATE['root'] = root
    skip = {root, STATE.get('sky_obj'), STATE.get('cam_ob')}
    for ob in list(SET.objects) + list(STATE['LIGHTS'].objects):
        if ob in skip or ob.parent is not None: continue
        ob.parent = root
    for ob in SET.objects:
        if ob.type == 'MESH' and 'gc_role' not in ob.keys(): ob['gc_role'] = 'ground'       # merged scenery banks (terrain, hedges, buildings, tufts)
    for fn in STATE.get('post_flush', []): fn()
    root.location = loc_origin(location); bpy.context.view_layer.update()
    for (ob, r, snap) in STATE['props']:
        if snap and not ob.get('airborne'): ground_snap(ob)
    bpy.context.view_layer.update()
    for nm in STATE.get('movers', []):                                                     # movers keep their height over the ground
        ob = STATE['objects'].get(nm)
        if ob is not None:
            w = ob.matrix_world.translation; g = ground_z(w.x, w.y, w.z + 30.0); ob['zoff'] = (w.z - g) if g is not None else 0.0
    for (ob, r, snap) in STATE['props']:
        if r is not None and r > 0: contact_shadow(ob, r)

# ----------------------------------------------------------------------------- nothing floats: ground_snap / contact_shadow
def _gc():
    p = os.path.join(PROJ, 'v3', 'tools')
    if p not in sys.path: sys.path.insert(0, p)
    import ground_check as GC; return GC

DRESS = ('tufts', 'tufts2', 'flowers', 'litter', 'glints', 'mist', 'smoke', 'pools', 'blobs', 'halos', 'puddle', 'fg_reeds', 'stars', 'hills', 'treeline', 'sun_disc')
class dress_hidden:
    """Hide the fine dressing (grass tufts, flowers, pebbles, glints, decals, mist) from ray casts: props are snapped to (and checked against) the
    real surface, never to a grass blade."""
    def __enter__(s):
        s.obs = [o for o in STATE['SET'].objects if o.name.split('~')[-1] in DRESS and not o.hide_viewport]
        for o in s.obs: o.hide_viewport = True
        bpy.context.view_layer.update(); return s
    def __exit__(s, *a):
        for o in s.obs: o.hide_viewport = False
        bpy.context.view_layer.update(); return False

def ground_snap(ob, sink=0.012, max_move=6.0):
    with dress_hidden(): return _ground_snap(ob, sink, max_move)

def _ground_snap(ob, sink=0.012, max_move=6.0):
    """Drop (or lift) `ob` so its lowest contact point sits `sink` D into the first surface below it (scene.ray_cast through everything but the
    object itself, its children, cards and shadows).  Returns the move (D).  Works on props (lowest vertices) and cards (lowest visible alpha row)."""
    GC = _gc(); sc = bpy.context.scene; bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    kind = 'card' if (ob.get('gc_role') == 'card' or ob.name.endswith('_card')) else 'prop'
    pts, zmin = (GC.card_contacts(ob, dg, sc.frame_current)[:2] if kind == 'card' else GC.bbox_contacts(ob, dg))
    best = None
    with GC._Hidden(ob) as dgh:
        for p in pts:
            hz, hob = GC.cast_down(sc, dgh, ob, p, lift=1.2)
            if hz is None: continue
            g = p.z - hz
            if best is None or g < best: best = g
    if best is None or abs(best) > max_move: return 0.0
    dz = -(best + sink); k = ob.parent.matrix_world.to_scale().z if ob.parent is not None else 1.0
    ob.location.z += dz / k; bpy.context.view_layer.update(); return dz

def ground_z(x, y, z0=500.0):
    """World height of the set surface under (x, y) (ray cast from z0 down through ground-like objects only)."""
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); o = Vector((x, y, z0))
    for _ in range(40):
        ok, loc, n, i, hit, m = sc.ray_cast(dg, o, Vector((0, 0, -1)))
        if not ok: return None
        if hit.get('gc_role') == 'ground' and hit.name not in ('sky',) and hit.name.split('~')[-1] not in DRESS: return loc.z
        o = Vector((loc.x, loc.y, loc.z - 1e-3))
    return None

def contact_shadow(ob, radius, depth=None, k=0.55, follow=True):
    """Soft dark contact blob (camera-only, no shadow casting) on the ground under `ob`: an ellipse radius x depth (default 0.6 x radius, turned
    with the object's yaw).  follow=True: it follows the object's XY and yaw (COPY_LOCATION x/y + COPY_ROTATION z), its height stays on the ground
    (so a lifted tank leaves its shadow on the grass).  Named <ob>_contact, gc_role 'shadow'."""
    nm = ob.name + '_contact'
    if nm in bpy.data.objects: return bpy.data.objects[nm]
    bpy.context.view_layer.update(); c = ob.matrix_world.translation; dep = depth or radius * 0.6
    gz_ = ground_z(c.x, c.y, c.z + 40.0); gz_ = c.z if gz_ is None else gz_
    me = bpy.data.meshes.new(nm); me.from_pydata([(-radius, -dep, 0), (radius, -dep, 0), (radius, dep, 0), (-radius, dep, 0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name='UVMap')
    for i, q in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = q
    me.materials.append(STATE['M']['blob']); sh = bpy.data.objects.new(nm, me); STATE['SET'].objects.link(sh)
    sh.location = (c.x, c.y, gz_ + 0.05); sh.rotation_euler = (0, 0, ob.matrix_world.to_euler().z); sh['gc_role'] = 'shadow'; sh.visible_shadow = False; no_bounce(sh)
    if follow:
        cl = sh.constraints.new('COPY_LOCATION'); cl.target = ob; cl.use_z = False
        cr = sh.constraints.new('COPY_ROTATION'); cr.target = ob; cr.use_x = False; cr.use_y = False
    return sh

# ----------------------------------------------------------------------------- shade cut, sky
def shade_cut(sc, P):
    """r3: make the painted shade a REPLACEMENT colour, not an additive one.  mat_g adds its ambient (blue shade) term as emission everywhere,
    so in sunlight it greys the key colour.  Here, before the grade: Image - amb x q x vis, where vis = smoothstep(lo, hi, lum(diffuse) / lum(amb))
    is 1 where the key light lands and 0 in shade (the AOV 'amb' is written by mat_g; cards, sky and emitters have none and are untouched)."""
    q = float(P.get('amb_cut', 0.0))
    if q <= 0: return
    vl = sc.view_layers[0]; vl.use_pass_diffuse_direct = True; vl.use_pass_diffuse_color = True
    if 'amb' not in [a.name for a in vl.aovs]: a = vl.aovs.add(); a.name = 'amb'; a.type = 'COLOR'
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore'); ng = sc.compositing_node_group
    src = next(n for n in ng.nodes if n.bl_idname == 'CompositorNodeRLayers')
    lk = next(l for l in ng.links if l.from_node == src and l.from_socket.name == 'Image'); dst = lk.to_socket; ng.links.remove(lk)
    N = ng.nodes.new; L = ng.links.new
    def mix(bt, a_, b_, fac=1.0):
        m = N('ShaderNodeMix'); m.data_type = 'RGBA'; m.blend_type = bt; m.inputs[0].default_value = fac; L(a_, m.inputs[6]); L(b_, m.inputs[7]); return m.outputs[2]
    dif = mix('MULTIPLY', src.outputs['Diffuse Direct'], src.outputs['Diffuse Color'])
    bd = N('CompositorNodeRGBToBW'); L(dif, bd.inputs[0]); ba = N('CompositorNodeRGBToBW'); L(src.outputs['amb'], ba.inputs[0])
    ad = N('ShaderNodeMath'); ad.operation = 'ADD'; ad.inputs[1].default_value = 0.003; L(ba.outputs[0], ad.inputs[0])
    dv = N('ShaderNodeMath'); dv.operation = 'DIVIDE'; L(bd.outputs[0], dv.inputs[0]); L(ad.outputs[0], dv.inputs[1])
    mr = N('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'; mr.inputs['From Min'].default_value = float(P.get('amb_lo', 0.6)); mr.inputs['From Max'].default_value = float(P.get('amb_hi', 1.6)); L(dv.outputs[0], mr.inputs['Value'])
    k = N('ShaderNodeMath'); k.operation = 'MULTIPLY'; k.inputs[1].default_value = q; L(mr.outputs['Result'], k.inputs[0])
    sub = mix('SUBTRACT', src.outputs['Image'], src.outputs['amb']); ng.nodes[-1].inputs[0].default_value = 0.0; L(k.outputs[0], ng.nodes[-1].inputs[0])
    if os.environ.get('GH_VIS'): L(mr.outputs['Result'], dst)
    else: L(sub, dst)

def sky_dome(SET, P):
    R = 2700.0 if STATE.get('location') == 'FIELDS' else 900.0; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]; M = STATE['M']
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [V((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    so = _obj(mb, 'sky', SET, shadow=False); so['gc_role'] = 'skip'; STATE['sky_obj'] = so
    install_handlers()

def _sky_follow(scene, *a):
    cam = scene.camera; so = STATE.get('sky_obj')
    if cam is not None and so is not None:
        try: so.location = cam.matrix_world.translation
        except ReferenceError: pass

def install_handlers():
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_pre):
        for f in list(h):
            if getattr(f, '__name__', '') == '_sky_follow': h.remove(f)
        h.append(_sky_follow)

# ----------------------------------------------------------------------------- cameras (no DOF, far clip 2500)
CAMS = dict(dawn=LOCATIONS['FIELDS']['cam'], morning=LOCATIONS['LANE']['cam'], night=LOCATIONS['CAMP']['cam'])
def make_camera(setup, name='cam'):
    ob = T.make_camera(setup, name); ob.data.clip_end = 3000.0; ob.data.clip_start = 0.1; ob.data.dof.use_dof = False
    bpy.context.view_layer.update(); _sky_follow(bpy.context.scene); return ob

def shot_camera(shot, t=0.0):
    """Pose the scene camera at t of the shot's move (t = 0 start, 1 = the planned end, 1.25 = the end of the x1.25 tail).  World frame."""
    c = _shots().pose(shot, t); cam = make_camera(c); STATE['cam_ob'] = cam; return cam

def key_camera(shot, f0=1, step=1):
    """Key the shot's whole move on the scene camera: one LINEAR key per frame from f0 over round(planned length x 1.25 x 30) frames.  The
    easing is in the sampled poses (ghost_shots.ease), so the keys are linear in between.  Sets scene.frame_start / frame_end.  -> (f0, f1)."""
    SH = _shots(); sh = SH.SHOTS[shot]; n = SH.frames(shot); cam = shot_camera(shot, 0.0); cam.animation_data_clear()
    cd = cam.data
    for i in range(0, n + 1, step):
        t = i / float(n) * 1.25; c = SH.pose(shot, t); f = f0 + i
        cam.location = c['loc']; fwd = (Vector(c['look_at']) - Vector(c['loc'])).normalized(); cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler(); cd.lens = c['lens']
        if i > 0:                                                        # keep euler continuity
            prev = STATE.get('_prev_rot')
            if prev is not None: cam.rotation_euler.make_compatible(prev)
        STATE['_prev_rot'] = cam.rotation_euler.copy()
        cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f); cd.keyframe_insert('lens', frame=f)
    PR_ = STATE['PR']; PR_._lin(cam); PR_._lin(cd)
    sc = bpy.context.scene; sc.frame_start = f0; sc.frame_end = f0 + n; sc.camera = cam; return f0, f0 + n

def marks(shot):
    """{role: [(x, y, z, yaw_deg, extra), ...]} WORLD marks of a shot at the current set state.  z = the surface under the mark (ray cast; marks with
    a fixed z keep it).  yaw turns a card that faces -y at yaw 0 toward the shot's start camera.  extra: ph / pose (placeholder silhouette),
    parent (a mover name: the mark is in the PARENT's local frame - parent the card to it: jeep seats, the lift, boats, the lead tank's deck),
    airborne.  Requires the location to be built."""
    SH = _shots(); out = {}
    for role, lst in SH.marks_local(shot).items():
        out[role] = []
        for m in lst:
            extra = m[5]
            if extra.get('parent'):
                par = _ob(extra['parent']); bpy.context.view_layer.update(); w = par.matrix_world @ Vector(m[:3]); x, y, gz_ = w.x, w.y, w.z
                c0 = SH.pose(shot, 0.0)['loc']; yaw = round(math.degrees(math.atan2(c0[0] - x, -(c0[1] - y))), 1)
                out[role].append((round(x, 3), round(y, 3), round(gz_, 3), yaw, extra)); continue
            else:
                x, y, z = to_world(m[:3]); gz_ = ground_z(x, y, z + 6.0) if m[3] is None else z
                if gz_ is None: gz_ = z
            out[role].append((round(x, 3), round(y, 3), round(gz_, 3), m[4], extra))
    return out

# ----------------------------------------------------------------------------- placeholder cards
def ph_card(name, role, pose, pos, yaw=None, face_to=None, night=None, parent=None):
    """A flat placeholder silhouette card (ghost_tex2.PH_ROLES / POSES_PH) with its feet at pos (world), turned by yaw (deg, card faces -y at 0)
    or toward face_to (yaw only).  Named <name>_card, gc_role 'card', in collection CARDS.  The real cast cards replace these (API.md)."""
    import ghost_tex2 as GX2
    night = (STATE['light'] in ('NIGHT', 'NIGHT_R', 'PREDAWN')) if night is None else night
    tn = 'ph_%s_%s_%s' % (role, pose, 'n' if night else 'd'); tx = GX.ensure([tn], verbose=False)[tn]
    R = GX2.PH_ROLES[role]; Wd, Hd = GX2.PH_CANVAS['bike' if R.get('bike') else ('dog' if R.get('dog') else 'man')]
    me = bpy.data.meshes.new(name + '_card'); me.from_pydata([(-Wd / 2, 0, 0), (Wd / 2, 0, 0), (Wd / 2, 0, Hd), (-Wd / 2, 0, Hd)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    mn = 'GHcard_' + tn; mat = bpy.data.materials.get(mn) or T.mat_card(mn, tx); me.materials.append(mat)
    ob = bpy.data.objects.new(name + '_card', me); STATE['CARDS'].objects.link(ob); no_bounce(ob); ob['gc_role'] = 'card'; ob['role'] = role; ob['pose'] = pose
    if face_to is not None: d_ = Vector(face_to) - Vector(pos); yaw = math.degrees(math.atan2(d_.x, -d_.y))
    if parent is not None:
        ob.parent = parent; ob.matrix_parent_inverse.identity(); bpy.context.view_layer.update()
        ob.location = parent.matrix_world.inverted() @ Vector(pos); ob.rotation_euler = (0, 0, math.radians(yaw or 0.0) - parent.matrix_world.to_euler().z)
        ps = parent.matrix_world.to_scale(); ob.scale = (1.0 / ps.x, 1.0 / ps.y, 1.0 / ps.z)
    else:
        ob.location = pos; ob.rotation_euler = (0, 0, math.radians(yaw or 0.0))
    STATE['cards'].append(ob); return ob

def place_cards(shot):
    """Placeholder cards at every mark of the shot (role -> silhouette); marks with a parent (jeep, boat, lift tank) are parented to it."""
    SH = _shots(); M_ = marks(shot); out = []
    for role, lst in M_.items():
        for i, m in enumerate(lst):
            x, y, z, yaw, extra = m; ph = extra.get('ph', 'soldier'); pose = extra.get('pose', 'stand'); par = bpy.data.objects.get(extra['parent']) if extra.get('parent') else None
            ob = ph_card('%s_%d' % (role, i), ph, pose, (x, y, z), yaw=yaw, parent=par); out.append(ob)
            if extra.get('airborne'): ob['airborne'] = True
    bpy.context.view_layer.update()
    for ob in out:
        if not ob.get('airborne'): ground_snap(ob, sink=0.005, max_move=1.5)
        if not ob.get('airborne') and ob.parent is None: contact_shadow(ob, 0.9, 0.42, follow=True)
    return out

def remove_placeholders():
    """Delete the placeholder cards (and their contact blobs) before the real cast cards go in."""
    for ob in list(STATE['CARDS'].objects):
        n = ob.name; bpy.data.objects.remove(ob, do_unlink=True)
        sh = bpy.data.objects.get(n + '_contact')
        if sh: bpy.data.objects.remove(sh, do_unlink=True)
    STATE['cards'] = []

# ----------------------------------------------------------------------------- setters (frame=None: set; frame=n: set and key)
def _ob(name):
    ob = STATE['objects'].get(name) or bpy.data.objects.get(name)
    if ob is None: raise KeyError('no object %r in %s (have: %s)' % (name, STATE.get('location'), ', '.join(sorted(STATE.get('tank_objs', {}))[:40])))
    return ob

def _key(ob, path, frame, interp='LINEAR', index=-1):
    if frame is None: return
    ob.keyframe_insert(path, index=index, frame=frame)
    ad = ob.animation_data
    if ad and ad.action:
        for fc in STATE['PR']._fcs(ad.action):
            if fc.data_path == path:
                for kp in fc.keyframe_points:
                    if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def tanks(location_filter=None):
    """Names of the rubber tanks of the built location (each takes set_inflate / set_sag / set_barrel)."""
    return sorted(STATE.get('tank_objs', {}))

def _own(ob):
    """Give a tank its own mesh (shape keys are per mesh; instances share one) before keying it."""
    if ob.data.users > 1:
        ob.data = ob.data.copy()
    return ob

def _place(ob, p_local, yaw, frame=None, ground=True):
    """Move a mover (parented to the location root) to local (x, y) / yaw; its height follows the ground (+ its 'zoff') unless ground=False."""
    z = ob.location.z
    if ground and 'zoff' in ob.keys():
        w = to_world((p_local[0], p_local[1], 0.0)); g = ground_z(w[0], w[1], w[2] + ob.matrix_world.translation.z + 30.0)
        if g is not None: z = g - loc_origin().z + ob['zoff']
    ob.location = (p_local[0], p_local[1], z); ob.rotation_euler = (0, 0, math.radians(yaw))
    if ground and 'zoff' in ob.keys() and not ob.hide_render: ground_snap(ob, max_move=2.0)
    _key(ob, 'location', frame); _key(ob, 'rotation_euler', frame)

def set_inflate(name, v, frame=None):
    """Tank `name`: inflate 0 (flat rubber sheet) .. 1 (full).  Also sinks a flat tank's contact blob."""
    ob = _own(_ob(name)); STATE['PR'].set_tank_shape(ob, inflate=v, frame=frame)

def set_sag(name, v, frame=None):
    """Tank `name`: barrel sag 0 (straight) .. 1 (limp)."""
    ob = _own(_ob(name)); STATE['PR'].set_tank_shape(ob, sag=v, frame=frame)

def set_barrel(name, deg, frame=None):
    """Tank `name`: barrel elevation in degrees (0 level .. 40 'pointing at the sky')."""
    ob = _own(_ob(name)); STATE['PR'].set_tank_shape(ob, elev=deg, frame=frame)

def set_deflate(v, frame=None, name='tank_hero'):
    """S03: the pricked hero tank goes 'ฟู่ แฟบ': v 0 (full, barrel straight) .. 1 (flat, barrel draped on the pricked soldier's helmet)."""
    ob = _own(_ob(name)); v = max(0.0, min(1.0, v)); STATE['PR'].set_tank_shape(ob, inflate=1.0 - 0.82 * v, sag=min(1.0, v * 1.6), frame=frame)

def set_lift(h, frame=None, name='tank_lift'):
    """S12 / S13: the 4-man lift.  h 0 = the tank on the grass, 1 = overhead (its belly 3.55 D up, on the four lifters' hands); flagged
    airborne (the ONLY airborne tank).  The contact blob stays on the ground and shrinks."""
    ob = _ob(name); z0 = ob.get('z0', ob.location.z); ob['z0'] = z0; ob.location.z = z0 + 3.55 * max(0.0, min(1.0, h)); _key(ob, 'location', frame, index=2)
    ob['airborne'] = bool(h > 0.01) if frame is None else True
    sh = bpy.data.objects.get(ob.name + '_contact')
    if sh: s_ = 1.0 - 0.45 * h; sh.scale = (s_, s_, 1.0); _key(sh, 'scale', frame)

def set_jeep(s, frame=None, name='jeep'):
    """The Major's jeep along its path (ghost_lane.JEEP_PATH): s 0 = far down the lane (out of the S06 frame) .. 1 = parked at its mark."""
    import ghost_lane as GL; ob = _ob(name); p, yaw = GL.jeep_at(max(0.0, min(1.0, s)))
    hid = s <= 0.001
    for o in [ob] + list(ob.children_recursive):
        o.hide_render = hid
        if frame is not None: o.keyframe_insert('hide_render', frame=frame)
    _place(ob, p, yaw, frame)

def set_column(d, frame=None):
    """S01: the column rolls: every column tank moves d D along the FIELDS lane (towed / pushed slowly; about 1.2 D/s looks right)."""
    import ghost_fields as GF
    for name, s0 in STATE.get('column', []):
        ob = _ob(name); p, yaw = GF.lane_pose(s0 - d, ob.get('lat', 0.0)); _place(ob, p, yaw, frame)

def set_record(angle_deg, frame=None, name='record'):
    """CAMP / RHINE sound truck turntable: the record's rotation (78 rpm = 936 deg/s: key angle = 936 * t, or use spin_record)."""
    ob = _ob(name); ob.rotation_euler.z = math.radians(angle_deg); _key(ob, 'rotation_euler', frame, index=2)

def spin_record(f0, f1, rpm=78.0, name='record'):
    for f in range(f0, f1 + 1): set_record(rpm * 6.0 * (f - f0) / 30.0, frame=f, name=name)

def flicker(frame, k=1.0):
    """Lantern flicker: every lamp's energy and halo varies per frame (deterministic hash, per-lamp phase); keyed at `frame`."""
    for i, lp in enumerate(STATE.get('lamps', [])):
        e0 = lp.get('e0', lp.data.energy); lp['e0'] = e0
        h = (math.sin(frame * 1.7 + i * 2.3) * 0.5 + math.sin(frame * 3.1 + i * 0.7) * 0.3 + math.sin(frame * 0.53 + i) * 0.2)
        lp.data.energy = e0 * k * (0.86 + 0.14 * h); lp.data.keyframe_insert('energy', frame=frame)
    for i, hb in enumerate(STATE.get('halo_obs', [])):
        h = 1.0 + 0.06 * math.sin(frame * 2.3 + i * 1.9); hb.scale = (h, h, h); hb.keyframe_insert('scale', frame=frame)

def set_boats(t, frame=None):
    """RHINE S18: the assault boats cross: t 0 (at the west bank) .. 1 (at the east bank).  Passenger cards parented to a boat ride with it."""
    import ghost_rhine as GR
    for name, path in STATE.get('boats', []):
        ob = _ob(name); p, yaw = GR.boat_at(path, t); _place(ob, p, yaw, frame, ground=False)

def set_pile(k, frame=None):
    """LANE S19: the balloon pile, k 0 (none) .. 1 (the 'huge pile', 120 balloons); balloons appear bottom-up, the heap core grows."""
    import ghost_lane as GL; GL.set_pile(k, frame)

def set_chalk(k, frame=None):
    """LANE S08: 'BALLOON ARMY' chalked on the crate: k 0 (plain crate) .. 1 (written)."""
    m = bpy.data.materials.get(STATE['pre'] + 'chalk_mix')
    if m is None: return
    n = m.node_tree.nodes['chalk_k']; n.outputs[0].default_value = k
    if frame is not None: n.outputs[0].keyframe_insert('default_value', frame=frame)

def set_loose_balloon(t, frame=None, name='balloon_loose'):
    """S19 last word: the last balloon escapes and loops away (t 0 in the Major's hands .. 1 gone up-left); flagged airborne."""
    import ghost_lane as GL; ob = _ob(name); p = GL.loose_path(t); ob.location = p; ob.hide_render = t > 0.999
    _key(ob, 'location', frame)
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame)

STATE_KEYS = dict(inflate=set_inflate, deflate=set_deflate, lift=set_lift, jeep=set_jeep, column=set_column, boats=set_boats, pile=set_pile, chalk=set_chalk)
def apply_state(spec):
    """'deflate=0.9,jeep=1,lift=0.6,pile=0.8,chalk=1,boats=0.5,column=3' or inflate:<tank>=v ; un-keyed (the build uses the shot's mid state)."""
    for part in [p.strip() for p in spec.split(',') if p.strip()]:
        k, v = part.split('=')
        if ':' in k:
            fn, nm = k.split(':'); STATE_KEYS[fn](nm, float(v))
        else: STATE_KEYS[k](float(v))

def animate(setter, f0, f1, v0, v1, step=1, ease=True, **kw):
    """Key any value setter from v0 at f0 to v1 at f1 (eased smoothstep), one key every `step` frames."""
    for f in range(f0, f1 + 1, step):
        x = (f - f0) / max(1, f1 - f0); u = x * x * (3 - 2 * x) if ease else x; setter(v0 + (v1 - v0) * u, frame=f, **kw)

# ----------------------------------------------------------------------------- render + CLI
def render_still(spec, quality='final', out=None, samples=None):
    """spec: 'S07' | 'S07@0.5' (t of the move, 0..1.25) | 'LANE' (default camera).  Builds, poses, renders; prints RENDER ... wall s."""
    name, _, t = spec.partition('@'); t = float(t) if t else 0.0
    A = build(name); sc = globals()['quality'](None, quality, samples=samples)
    if A['shot']: shot_camera(A['shot'], t)
    out = out or os.path.join(WORK, '%s_%s.png' % (spec.replace('@', '_'), quality)); os.makedirs(os.path.dirname(out), exist_ok=True)
    wall, cpu = T.render(out)
    print('RENDER %s %.1f wall s, %.1f cpu s' % (spec, wall, cpu), flush=True); return out, wall, cpu

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'still':
        render_still(a[1], a[2] if len(a) > 2 else 'final', a[3] if len(a) > 3 else None)
    elif a and a[0] in ('sheet', 'finals', 'ground', 'frames'):
        import ghost_sheet as GS; GS.main(a)
    elif a and a[0] == 'board':
        import board; board.run()
    else: print(__doc__)
