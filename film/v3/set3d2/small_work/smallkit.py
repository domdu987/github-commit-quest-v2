"""smallkit.py : shared helpers for the two small sets (vault.py, room.py).

Light model (scene-linear), same idea as v3/set3d/office3d.py, generalised to a point key and to painted pools:
    displayed = art * gain * KEY * fall(d) * visibility                 (the one hard key: Sun or Point light)
              + art * shade_mul * AMB(P, N) + LIFT                       (ambient, injected as emission: noise-free)
    AMB = SHADE * (1 + N.form) * (1 - kc * clamp(|P - c| / rc)) * (1 - kz * clamp((z - z0) / (z1 - z0)))
        + sum over pools: col * (0.35 + 0.65 max(N.l, 0)) / (1 + (d / r)^2)      (unshadowed painted glow: candle, embers)
        + flash * flash_col                                                    (keyable Value node 'flash' in the AMB group)
The diffuse colour is divided by the true cosine to the key (and, for a point key, multiplied by d^2), so every face the key
reaches gets art * gain * KEY * fall(d): two-tone like the reference, with a falloff we choose, and ray-traced hard shadows.
Both terms live in two node groups per preset (AMB_<tag>, KEYF_<tag>), shared by every material.
Imports office3d (read-only) for the mesh builder, camera and card helpers."""
import os, sys, math, json, time, hashlib, subprocess
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SET2 = os.path.dirname(HERE)
PROJ = os.path.dirname(os.path.dirname(SET2))
SET3D = os.path.join(PROJ, 'v3', 'set3d')
sys.path.insert(0, SET3D)
import office3d as S                                                     # noqa: E402  read-only: MB, make_camera, no_bounce, mat_card
TEX = os.path.join(SET2, 'tex_small'); WORK = HERE
MB = S.MB; make_camera = S.make_camera; no_bounce = S.no_bounce
COS_MIN = 0.12
ST = {}                                                                  # current preset dict 'P', tag

def hex_lin(h): return S.hex_lin(h)

# ----------------------------------------------------------------------------- textures (SVG -> PNG by headless Chromium, cached by hash)
def raster(jobs, verbose=False):
    """jobs: {name: (svg_text, w, h, transparent)} -> {name: png path} in tex_small/ (only changed SVGs are rasterised)."""
    os.makedirs(TEX, exist_ok=True); mp = os.path.join(TEX, 'manifest.json')
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    todo = []; out = {}
    for name in sorted(jobs):
        svg, w, h, tr = jobs[name]; hh = hashlib.sha1((svg + str(tr) + '%dx%d' % (w, h)).encode()).hexdigest()
        png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != hh or not os.path.exists(png):
            sp = os.path.join(TEX, name + '.svg'); open(sp, 'w').write(svg)
            todo.append(dict(src=sp, out=png, w=w, h=h, transparent=tr)); man[name] = hh
    if todo:
        jp = os.path.join(TEX, '_jobs.json'); json.dump(todo, open(jp, 'w'))
        for attempt in range(3):
            r = subprocess.run(['node', os.path.join(SET3D, 'raster.js'), jp], capture_output=True, text=True,
                               env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
            if r.returncode == 0: break
            time.sleep(1.0)
        else: raise RuntimeError('raster failed: ' + r.stderr[-1500:])
        json.dump(man, open(mp, 'w'), indent=0, sort_keys=True)
        if verbose: print('rasterised', [os.path.basename(t['out']) for t in todo])
    return out

def svg_doc(w_px, h_px, vb_w, vb_h, body, bg=None):
    b = f'<rect x="-1" y="-1" width="{vb_w + 2}" height="{vb_h + 2}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_px}" height="{h_px}" viewBox="0 0 {vb_w:g} {vb_h:g}" '
            f'preserveAspectRatio="none" style="display:block">{b}{body}</svg>')

def mulc(h, k):
    h = h.lstrip('#'); c = [min(255, max(0, int(round(int(h[i:i + 2], 16) * k)))) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(c)

def mixc(a, b, t):
    a = a.lstrip('#'); b = b.lstrip('#')
    return '#%02x%02x%02x' % tuple(int(round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t)) for i in (0, 2, 4))

# ----------------------------------------------------------------------------- node groups: ambient and key factor
def _grp(name, out_type='NodeSocketVector', out_name='Out'):
    ng = bpy.data.node_groups.get(name)
    if ng is not None: bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new(name, 'ShaderNodeTree')
    ng.interface.new_socket(out_name, in_out='OUTPUT', socket_type=out_type)
    return ng

def _vm(nt, op, a=None, b=None):
    n = nt.nodes.new('ShaderNodeVectorMath'); n.operation = op
    for i, v in ((0, a), (1, b)):
        if v is None: continue
        if isinstance(v, (tuple, list)): n.inputs[i].default_value = tuple(v)
        else: nt.links.new(v, n.inputs[i])
    return n

def _m(nt, op, a=None, b=None, c=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    for i, v in ((0, a), (1, b), (2, c)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[i].default_value = float(v)
        else: nt.links.new(v, n.inputs[i])
    return n.outputs[0]

def _vout(n, kind='Vector'):
    return n.outputs['Value'] if kind == 'Value' else n.outputs['Vector']

def build_groups(P, tag):
    """AMB_<tag> (vector) and KEYF_<tag> (value) from the preset dict P."""
    ST['P'] = P; ST['tag'] = tag
    # ---- ambient
    ng = _grp('AMB_' + tag); nt = ng.nodes; L = ng.links.new
    out = nt.new('NodeGroupOutput'); geo = nt.new('ShaderNodeNewGeometry'); N = geo.outputs['True Normal']; Pp = geo.outputs['Position']
    fac = None
    form = P.get('form')
    if form:
        d = _vm(ng, 'DOT_PRODUCT', N, tuple(form)); fac = _m(ng, 'ADD', _vout(d, 'Value'), 1.0)
    if P.get('amb_center'):
        c, rc, kc = P['amb_center']
        dist = _vm(ng, 'DISTANCE', Pp, tuple(c)); q = _m(ng, 'DIVIDE', _vout(dist, 'Value'), float(rc), clamp=True)
        f2 = _m(ng, 'MULTIPLY_ADD', q, -float(kc), 1.0); fac = f2 if fac is None else _m(ng, 'MULTIPLY', fac, f2)
    if P.get('amb_z'):
        z0, z1, kz = P['amb_z']
        sep = nt.new('ShaderNodeSeparateXYZ'); L(Pp, sep.inputs[0])
        q = _m(ng, 'MULTIPLY_ADD', sep.outputs['Z'], 1.0 / (z1 - z0), -z0 / (z1 - z0)); q = _m(ng, 'MINIMUM', _m(ng, 'MAXIMUM', q, 0.0), 1.0)
        f3 = _m(ng, 'MULTIPLY_ADD', q, -float(kz), 1.0); fac = f3 if fac is None else _m(ng, 'MULTIPLY', fac, f3)
    amb = _vm(ng, 'SCALE', tuple(P['shade']))
    if fac is not None: L(fac, amb.inputs['Scale'])
    else: amb.inputs['Scale'].default_value = 1.0
    acc = amb.outputs['Vector']
    for (pos, col, r) in P.get('pools', []):
        lv = _vm(ng, 'SUBTRACT', tuple(pos), Pp); ln = _vm(ng, 'LENGTH', lv.outputs['Vector']); nv = _vm(ng, 'NORMALIZE', lv.outputs['Vector'])
        cs = _vm(ng, 'DOT_PRODUCT', N, nv.outputs['Vector']); lam = _m(ng, 'MULTIPLY_ADD', _m(ng, 'MAXIMUM', _vout(cs, 'Value'), 0.0), 0.65, 0.35)
        q = _m(ng, 'DIVIDE', _vout(ln, 'Value'), float(r)); att = _m(ng, 'DIVIDE', 1.0, _m(ng, 'MULTIPLY_ADD', q, q, 1.0))
        k = _m(ng, 'MULTIPLY', lam, att); sc = _vm(ng, 'SCALE', tuple(col)); L(k, sc.inputs['Scale'])
        acc = _vm(ng, 'ADD', acc, sc.outputs['Vector']).outputs['Vector']
    fl = nt.new('ShaderNodeValue'); fl.name = 'flash'; fl.label = 'flash'; fl.outputs[0].default_value = 0.0
    fs = _vm(ng, 'SCALE', tuple(P.get('flash_col', (1.0, 0.45, 0.12)))); L(fl.outputs[0], fs.inputs['Scale'])
    acc = _vm(ng, 'ADD', acc, fs.outputs['Vector']).outputs['Vector']
    L(acc, out.inputs[0])
    # ---- key factor
    kg = _grp('KEYF_' + tag, 'NodeSocketFloat'); nt = kg.nodes; L = kg.links.new
    out = nt.new('NodeGroupOutput'); geo = nt.new('ShaderNodeNewGeometry'); N = geo.outputs['True Normal']; Pp = geo.outputs['Position']
    if P['key_type'] == 'SUN':
        kd = Vector(P['key_dir']).normalized()
        cs = _vm(kg, 'DOT_PRODUCT', N, tuple(-kd)); res = _m(kg, 'DIVIDE', 1.0, _m(kg, 'MAXIMUM', _vout(cs, 'Value'), COS_MIN))
    else:
        lv = _vm(kg, 'SUBTRACT', tuple(P['key_pos']), Pp); ln = _vm(kg, 'LENGTH', lv.outputs['Vector']); nv = _vm(kg, 'NORMALIZE', lv.outputs['Vector'])
        cs = _vm(kg, 'DOT_PRODUCT', N, nv.outputs['Vector']); d = _vout(ln, 'Value')
        R = float(P['key_falloff'])                     # fall(d) = 1 / (1 + (d / R)^2)  -> d^2 fall = d^2 R^2 / (R^2 + d^2)
        d2 = _m(kg, 'MULTIPLY', d, d); num = _m(kg, 'MULTIPLY', d2, R * R); den = _m(kg, 'ADD', d2, R * R)
        res = _m(kg, 'DIVIDE', _m(kg, 'DIVIDE', num, den), _m(kg, 'MAXIMUM', _vout(cs, 'Value'), COS_MIN))
    L(res, out.inputs[0])
    return ng, kg

def amb_group(): return bpy.data.node_groups['AMB_' + ST['tag']]

def set_flash(value, frame=None):
    """Ambient flash term (multiplies flash_col of the preset), keyable."""
    n = amb_group().nodes['flash']; n.outputs[0].default_value = float(value)
    if frame is not None:
        n.outputs[0].keyframe_insert('default_value', frame=frame)

# ----------------------------------------------------------------------------- materials
def _tree(m):
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt

def mat_lit(name, color='#808080', image=None, gain=1.0, shade_mul=1.0, alpha=False, interp='Linear', desat=None):
    """desat (default P['shade_desat']): the ambient sees the artwork mixed this far toward its own grey, so a red brick in the
    blue-violet shade turns blue-violet (like the reference) instead of dark maroon."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    P = ST['P']; m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    ga = nt.nodes.new('ShaderNodeGroup'); ga.node_tree = bpy.data.node_groups['AMB_' + ST['tag']]
    gk = nt.nodes.new('ShaderNodeGroup'); gk.node_tree = bpy.data.node_groups['KEYF_' + ST['tag']]
    sm = tuple(shade_mul) if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(image, check_existing=True); tex.interpolation = interp
        art = tex.outputs['Color']
    else:
        tex = None; cn = nt.nodes.new('ShaderNodeRGB'); cn.outputs[0].default_value = (*hex_lin(color), 1.0); art = cn.outputs[0]
    ds = P.get('shade_desat', 0.0) if desat is None else desat; art_s = art
    if ds > 0:
        bw = nt.nodes.new('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[0].default_value = ds; L(art, mx.inputs[6]); L(bw.outputs[0], mx.inputs[7]); art_s = mx.outputs[2]
    a1 = nt.nodes.new('ShaderNodeVectorMath'); a1.operation = 'MULTIPLY'; L(art_s, a1.inputs[0]); L(ga.outputs[0], a1.inputs[1])
    a2 = nt.nodes.new('ShaderNodeVectorMath'); a2.operation = 'MULTIPLY_ADD'; L(a1.outputs['Vector'], a2.inputs[0]); a2.inputs[1].default_value = sm
    a2.inputs[2].default_value = tuple(P.get('lift', (0, 0, 0)))
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0; L(a2.outputs['Vector'], emi.inputs['Color'])
    k1 = nt.nodes.new('ShaderNodeMath'); k1.operation = 'MULTIPLY'; k1.inputs[1].default_value = gain; L(gk.outputs[0], k1.inputs[0])
    kds = P.get('key_desat', 0.0); art_k = art
    if kds > 0:                                              # moonlight: the key sees the artwork pulled toward grey (pale blue patches, not red ones)
        bw2 = nt.nodes.new('ShaderNodeRGBToBW'); L(art, bw2.inputs[0])
        mk = nt.nodes.new('ShaderNodeMix'); mk.data_type = 'RGBA'; mk.inputs[0].default_value = kds; L(art, mk.inputs[6]); L(bw2.outputs[0], mk.inputs[7]); art_k = mk.outputs[2]
    k2 = nt.nodes.new('ShaderNodeVectorMath'); k2.operation = 'SCALE'; L(art_k, k2.inputs[0]); L(k1.outputs[0], k2.inputs['Scale'])
    L(k2.outputs['Vector'], dif.inputs['Color'])
    add = nt.nodes.new('ShaderNodeAddShader'); L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1]); last = add.outputs['Shader']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_emit(name, color='#ffffff', image=None, strength=1.0, alpha=False):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = strength
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(image, check_existing=True); L(tex.outputs['Color'], emi.inputs['Color'])
    else: emi.inputs['Color'].default_value = (*hex_lin(color), 1.0)
    last = emi.outputs['Emission']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def mat_ink(ink_hex):
    name = 'SM_ink_' + ink_hex.lstrip('#')
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); geo = nt.nodes.new('ShaderNodeNewGeometry'); lp = nt.nodes.new('ShaderNodeLightPath')
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(ink_hex), 1.0)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    notcam = nt.nodes.new('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MAXIMUM'
    L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def add_hull(ob, thickness, ink_hex):
    ob.data.materials.append(mat_ink(ink_hex))
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY')
    mod.thickness = thickness; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(ob.data.materials) - 1; mod.use_even_offset = True
    return mod

def obj(mb, name, coll, hull=0.0, ink='#2a1712', shadow=True):
    ob = mb.obj(name, coll)
    if hull > 0: add_hull(ob, hull, ink)
    ob.visible_shadow = shadow
    return ob

def hull_t(dist): return 0.00384 * dist                  # 3 px ink at camera distance dist (720 px wide frame)

# ----------------------------------------------------------------------------- scene, render, grade
def coll(name, scene):
    c = bpy.data.collections.get(name)
    if c is None: c = bpy.data.collections.new(name)
    if name not in [k.name for k in scene.collection.children]: scene.collection.children.link(c)
    return c

def reset_scene(scene, prefix):
    for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for m in list(bpy.data.materials):
        if m.name.startswith((prefix, 'SM_ink_')): bpy.data.materials.remove(m)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for cu in list(bpy.data.curves):
        if cu.users == 0: bpy.data.curves.remove(cu)
    for li in list(bpy.data.lights):
        if li.users == 0: bpy.data.lights.remove(li)
    w = bpy.data.worlds.get('W_small') or bpy.data.worlds.new('W_small'); scene.world = w
    nt = _tree(w); bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld')
    bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0; nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])

def setup_render(scene, quality='final'):
    """final: 720x1280, 12 samples, 2 threads. preview: 360x640, 8 samples, 2 threads. (brief: max 2 render threads per process)"""
    S.setup_render(scene, 'final' if quality == 'final' else 'preview')
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 2
    scene.cycles.samples = 12 if quality == 'final' else 8
    scene.cycles.seed = 0; scene.cycles.use_animated_seed = False

def setup_grade(scene, P):
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    gp = dict(vignette_strength=0.0, bloom_strength=P.get('bloom_strength', 0.5), bloom_size=P.get('bloom_size', 0.05))
    if 'grade_offset' in P: gp['offset'] = tuple(P['grade_offset'])
    if 'grade_saturation' in P: gp['saturation'] = float(P['grade_saturation'])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore'); ng = G.build(scene, preset=gp)
    scene.render.use_compositing = True
    return ng

def add_key(P, coll_):
    """The one hard key: SUN (energy pi * max K) or POINT (energy 4 pi^2 * max K: with the KEYF normalisation a lit face shows art*gain*K*fall(d))."""
    K = P['key']; k = max(K)
    if k <= 0: return None
    if P['key_type'] == 'SUN':
        d = bpy.data.lights.new('key', 'SUN'); d.energy = math.pi * k; d.angle = math.radians(P.get('sun_angle', 0.45))
        ob = bpy.data.objects.new('key', d); coll_.objects.link(ob)
        ob.rotation_euler = (-Vector(P['key_dir']).normalized()).to_track_quat('Z', 'Y').to_euler(); ob.location = P.get('key_loc', (0, 0, 10))
    else:
        d = bpy.data.lights.new('key', 'POINT'); d.energy = 4 * math.pi ** 2 * k; d.shadow_soft_size = P.get('key_radius', 0.03)
        try: d.use_soft_falloff = False
        except AttributeError: pass
        ob = bpy.data.objects.new('key', d); coll_.objects.link(ob); ob.location = P['key_pos']
    d.color = tuple(x / k for x in K)
    ST['key'] = ob; ST['key_energy'] = d.energy
    return ob

def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = time.process_time(); bpy.ops.render.render(write_still=True)
    return time.time() - t0, time.process_time() - c0

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
def placeholder_actor(cast, pose, mark, face_to=None, name=None, scale=1.0, ppd=300, z=None):
    """Rasterise a v2 puppet pose to a PNG (cached in small_work/actors) and stand it on an emission card at `mark`.
    scale 0.8 = the boy (about 2.4 D). z overrides the feet height (sitting on a bed)."""
    sys.path.insert(0, os.path.join(PROJ, 'v2', 'puppet'))
    import puppet
    name = name or ('actor_' + cast); f = puppet.figure(cast, dict(pose), name)
    bx0, by0, bx1, by1 = f['bbox']; pad = 0.08; bx0 -= pad; by0 -= pad; bx1 += pad; by1 = max(by1, f['feet_y']) + pad
    w, h = bx1 - bx0, by1 - by0; Wp, Hp = int(round(w * ppd)), int(round(h * ppd))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wp}" height="{Hp}" viewBox="{bx0:.4f} {by0:.4f} {w:.4f} {h:.4f}" style="display:block">{f["svg"]}</svg>')
    d = os.path.join(WORK, 'actors'); os.makedirs(d, exist_ok=True)
    tag = name + '_' + hashlib.sha1(svg.encode()).hexdigest()[:10]; sp = os.path.join(d, tag + '.svg'); pp = os.path.join(d, tag + '.png')
    if not os.path.exists(pp):
        open(sp, 'w').write(svg); jp = os.path.join(d, tag + '_job.json'); json.dump([dict(src=sp, out=pp, w=Wp, h=Hp, transparent=True)], open(jp, 'w'))
        r = subprocess.run(['node', os.path.join(SET3D, 'raster.js'), jp], capture_output=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
        if r.returncode != 0: raise RuntimeError(r.stderr.decode()[-500:])
    fx = f['anchors']['feet'][0]; fy = f['feet_y']
    me = bpy.data.meshes.new(name); xs = ((bx0 - fx) * scale, (bx1 - fx) * scale); zs = ((fy - by1) * scale, (fy - by0) * scale)
    me.from_pydata([(xs[0], 0, zs[0]), (xs[1], 0, zs[0]), (xs[1], 0, zs[1]), (xs[0], 0, zs[1])], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(S.mat_card(name + '_mat', pp))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    loc = list(mark); loc[2] = mark[2] if z is None else z; ob.location = loc; no_bounce(ob)
    if face_to is not None:
        dv = Vector(face_to) - Vector(mark); ob.rotation_euler = (0, 0, math.atan2(dv.x, -dv.y))
    return ob

def clear_actors(scene=None):
    scene = scene or bpy.context.scene
    for o in list(scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def digest(colls=('SET', 'LIGHTS')):
    """sha1 over object names, transforms, vertex coordinates and materials (determinism check)."""
    h = hashlib.sha1()
    for cn in colls:
        c = bpy.data.collections.get(cn)
        if not c: continue
        for ob in sorted(c.objects, key=lambda o: o.name):
            h.update(ob.name.encode()); h.update(str([round(x, 5) for x in ob.matrix_world.col[3]]).encode())
            if ob.type == 'MESH':
                h.update(str(len(ob.data.vertices)).encode())
                for v in ob.data.vertices: h.update(('%.5f,%.5f,%.5f' % tuple(v.co)).encode())
                h.update(str([m.name for m in ob.data.materials if m]).encode())
    return h.hexdigest()
