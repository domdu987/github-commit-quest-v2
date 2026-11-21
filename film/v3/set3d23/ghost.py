#!/usr/bin/env python3
"""ghost.py : set builder of film 23 ("ไอ้กองทัพลูกโป่ง", the Ghost Army, Normandy 1944 / the Rhine 1945): a lit 3D world (bpy 5.3, Cycles CPU)
for the flat 2D puppet cards.  World: 1 unit = 1 D = one head, Z up.  Built on the v3 helpers (tower / mine / bakery) like set3d10 harbour.py.

    import ghost as GH
    A = GH.build('dawn')            # 'dawn' (dawn_fields_high) | 'morning' (inflate_lane_morning) | 'night' (night_sound_truck)
    cam = GH.make_camera(A['cam'])
CLI:  python3 ghost.py still <dawn|morning|night> [preview|final] [out.png]
      python3 ghost.py board          # the 3 style-board finals + style_board.jpg + numbers.json (see board/NOTES.md)
Textures: ghost_tex.py (painted, cached in tex_ghost/).  Props: ghost_props.py (rubber M4 tank, trucks, nets, crates, farm ...)."""
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
    DAWN=dict(_B, key=(1.30, 0.95, 0.52), sun_az=165.0, sun_el=19.0, sun_vis_el=6.0, sky='sky_dawn', sky_k=0.82, exposure=-0.5, shade=(0.27, 0.17, 0.48), shade_tint=(0.27, 0.17, 0.50), shade_mix=1.0, lift=(0.030, 0.024, 0.060),
              grade_offset=(-0.004, -0.006, -0.002), grade_saturation=1.4, bounce=(1.0, 0.7, 0.45, 0.12)),
    MORNING=dict(_B, key=(1.45, 1.05, 0.62), sun_az=200.0, sun_el=21.0, sky='sky_morning', sky_k=0.8, exposure=-0.7, shade=(0.23, 0.19, 0.47), shade_tint=(0.23, 0.19, 0.49), shade_mix=0.85,
                 grade_offset=(-0.004, -0.006, -0.002), grade_saturation=1.18, bounce=(1.0, 0.7, 0.45, 0.14)),
    NIGHT=dict(_B, key=(0.30, 0.42, 1.25), sun_az=64.0, sun_el=24.0, sun_vis_el=17.0, sky='sky_night', sky_k=1.0, night=True, lambert=True, key_desat=0.2, ink='#10143a', lamps=1.0, bloom_size=0.07,
               shade=(0.23, 0.15, 0.42), shade_tint=(0.23, 0.15, 0.44), shade_mix=0.8, lift=(0.026, 0.020, 0.052), grade_offset=(0.002, 0.003, 0.010), grade_saturation=1.16),
)
for _k, _v in LIGHTS.items(): _v['key_dir'] = kd_of(_v['sun_az'], _v['sun_el'])
SCENE_LIGHT = dict(dawn='DAWN', morning='MORNING', night='NIGHT')

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
    L(amb, emi.inputs['Color']); L(md.outputs['Vector'], dif.inputs['Color']); L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1])
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

# ----------------------------------------------------------------------------- mesh banks
class Banks:
    def __init__(s): s.b = {}; s.hull = {}; s.shadow = {}; s.smooth = {}
    def __call__(s, name, hull=0.0, shadow=True, smooth_=False):
        if name not in s.b: s.b[name] = MB(); s.hull[name] = hull; s.shadow[name] = shadow; s.smooth[name] = smooth_
        return s.b[name]
    def flush(s, SET):
        for n, mb in s.b.items():
            if mb.f:
                ob = _obj(mb, n, SET, hull=s.hull[n], shadow=s.shadow[n])
                if s.smooth[n]:
                    for p in ob.data.polygons: p.use_smooth = True

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
def make_terrain(scene):
    cfg = GX.SCENES[scene]; x0, x1, y0, y1 = cfg['rect']; st = STATE.get('terrain_step', 4.0)
    gz = STATE['gz']; nx = int((x1 - x0) / st); ny = int((y1 - y0) / st); M = STATE['M']; mb = MB(); mb.pid += 1
    xs = [x0 + (x1 - x0) * i / nx for i in range(nx + 1)]; ys = [y0 + (y1 - y0) * j / ny for j in range(ny + 1)]
    Z = [[gz(x, y) for y in ys] for x in xs]
    for i in range(nx):
        for j in range(ny):
            p = [(xs[i], ys[j]), (xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])]; z = [Z[i][j], Z[i + 1][j], Z[i + 1][j + 1], Z[i][j + 1]]
            mb.face([V((p[k][0], p[k][1], z[k])) for k in range(4)], M['ground'], [((p[k][0] - x0) / (x1 - x0), (p[k][1] - y0) / (y1 - y0)) for k in range(4)])
    ob = _obj(mb, 'terrain', STATE['SET'], shadow=True); return ob

def tex_path(name): return STATE['tx'][name]

# ----------------------------------------------------------------------------- build
def build(scene_name):
    sc = bpy.context.scene; lk = SCENE_LIGHT[scene_name]; P = dict(LIGHTS[lk])
    STATE.clear(); STATE.update(P=P, scene=scene_name, light=lk)
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_pre):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_sky_follow',): h.remove(f)
    for ob in list(sc.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', sc); LIG = T._coll('LIGHTS', sc); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('GH_', 'ink')): bpy.data.materials.remove(m)
    names = ['glow', 'pool', 'mist', 'hedge', 'leaf', 'poplar', 'apple', 'roof_red', 'roof_red_d', 'roof_slate', 'stone_farm', 'stone_wall', 'stone_church', 'barn_wood', 'wood', 'canvas_khaki', 'canvas_olive',
             'camonet', 'rubber', 'rubber_d', 'rubber_l', 'star', 'water', 'cow', 'cow_b', 'puff', 'grass_detail', 'sign', 'tankmark', 'crate_a', 'crate_b', 'crate_c', 'crate_plain', 'fields_' + scene_name, 'sky_' + scene_name]
    names += [n for n in GX.JOBS if n.startswith('sol_')]
    STATE['tx'] = GX.ensure(names, verbose=False)
    w = bpy.data.worlds.get('W_ghost') or bpy.data.worlds.new('W_ghost'); sc.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(sc, 'final'); sc.render.threads = 4; sc.frame_start = 1; sc.frame_current = 1
    pre = 'GH_%s_' % scene_name; STATE['pre'] = pre
    import ghost_props as PR; STATE['PR'] = PR
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    if P.get('bounce'):
        br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
        d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
        o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    STATE.update(marks={}, lamps=[], objects=STATE.get('objects', {}))
    PR.setup_materials(P, STATE['tx'], pre)
    cams = CAMS[scene_name]; STATE['cam'] = cams; cam = make_camera(cams); STATE['cam_ob'] = cam
    Bk = Banks(); STATE['B'] = Bk
    sky_dome(SET, P)
    import ghost_scenes as SCN
    SCN.build_scene(scene_name, Bk, STATE['M'])
    Bk.flush(SET)
    sc.cycles.use_light_tree = (scene_name == 'night')
    MN._denoise(sc); setup_grade(sc)
    for ob in SET.objects: no_bounce(ob)
    for ob in STATE.get('cards', ()): no_bounce(ob)
    A = dict(scene=scene_name, light=lk, cam=cams, marks=dict(STATE['marks']), key_dir=tuple(kd))
    STATE['A'] = A; return A

def sky_dome(SET, P):
    R = 900.0; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]; M = STATE['M']
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [V((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    so = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = so
    install_handlers()

def _sky_follow(scene, *a):
    cam = scene.camera; so = STATE.get('sky_obj')
    if cam is not None and so is not None: so.location = cam.matrix_world.translation

def install_handlers():
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_pre):
        for f in list(h):
            if getattr(f, '__name__', '') == '_sky_follow': h.remove(f)
        h.append(_sky_follow)

# ----------------------------------------------------------------------------- cameras (lens 22 mm, no DOF, far clip 2500)
CAMS = dict(
    dawn=dict(loc=(-16.0, -72.0, 66.0), look_at=(4.0, 62.0, 0.0), lens=24),
    morning=dict(loc=(-0.5, -8.2, 1.3), look_at=(0.4, 2.0, 2.3), lens=19),
    night=dict(loc=(-2.0, -31.0, 9.5), look_at=(3.0, 12.0, 6.4), lens=22),
)
def make_camera(setup, name='cam'):
    ob = T.make_camera(setup, name); ob.data.clip_end = 2500.0; ob.data.clip_start = 0.1; ob.data.dof.use_dof = False
    bpy.context.view_layer.update(); _sky_follow(bpy.context.scene); return ob

# ----------------------------------------------------------------------------- render + CLI
def render_still(scene_name, quality='final', out=None):
    A = build(scene_name); sc = bpy.context.scene; MN.setup_render(sc, quality); sc.render.threads = 4
    MN._denoise(sc); sc.view_settings.exposure = float(STATE['P'].get('exposure', 0.0))
    out = out or os.path.join(WORK, '%s_%s.png' % (scene_name, quality)); os.makedirs(os.path.dirname(out), exist_ok=True)
    wall, cpu = T.render(out)
    print('RENDER %s %.1f wall s, %.1f cpu s' % (scene_name, wall, cpu), flush=True); return out, wall, cpu

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'still':
        render_still(a[1], a[2] if len(a) > 2 else 'final', a[3] if len(a) > 3 else None)
    elif a and a[0] == 'board':
        import board; board.run()
    else: print(__doc__)
