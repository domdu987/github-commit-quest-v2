"""Rooftop of a 7-storey building in Thonburi during a violent afternoon thunderstorm, as a real 3D set (bpy 5.3, Cycles CPU).
For 'ช่างเชื่อมสายฟ้า' (the welder struck by lightning). Same method as town3d.py: SVG artwork -> textures (tex_roof.py), office3d.MB meshes,
office3d.mat_lit toon materials (blue-violet ambient as emission + one hard cold key), emissive bulbs / windows, camera-only sky.

World: 1 unit ~ 1 m, Z up, roof floor z = 0, street level z = GROUND (-24.5). The billboard faces -y; its catwalk runs along the front
at z 7.05; the welder works at the right-hand front post (x 5.4). +y (behind the billboard) looks east across the Chao Phraya to Bangkok.
    import roof3d; A = roof3d.build('storm', flash=0.0)     # -> anchors (A['weld_mark'], A['weld_point'], A['cams'], A['bolt_obj'], ...)
    roof3d.set_bolt(True)                                     # show / hide the lightning bolt object
CLI: python3 roof3d.py stills [preview]  -> out_roof/<cam>.png (+ est_aerial_169.png) and out_roof/timing.json"""
import os, sys, math, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import office3d as S
import tex_roof
MB = S.MB

GROUND = -24.5
PRESETS = {
    'storm': dict(shade=(0.205, 0.185, 0.44), key=(1.10, 1.24, 1.62), lift=(0.010, 0.009, 0.026), key_dir=(-0.80, 0.30, -0.52), sun_angle=0.9,
                  form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.05, grade_offset=(0.003, 0.003, 0.013), grade_saturation=1.10,
                  sky=1.0, haze='#38386a', haze_d=330.0, haze_max=0.95),
}
FLASH = dict(shade=(0.30, 0.31, 0.58), key=(3.2, 3.45, 4.2), key_dir=(-0.30, 0.42, -0.86), sky=1.75, haze='#6a70b0')
GAIN = 0.5
A = {}
PX = (-5.4, -1.8, 1.8, 5.4)          # billboard frames (front posts)
YF = 2.45                            # front post centre line
PZ0, PZ1 = 9.3, 15.3                 # billboard panel bottom / top
CW_Z = 7.05                          # catwalk deck top
WELD = Vector((5.4, YF - 0.15, 8.45))
LAMPS = tex_roof.LAMP_U

def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))
def _lin(h): return S.hex_lin(h)

# ----------------------------------------------------------------------------- materials
def lit(name, img=None, color='#808080', gain=0.9, shade=1.0, alpha=False):
    return S.mat_lit('R_' + name, color=color, image=img, gain=gain * GAIN, shade_mul=shade, alpha=alpha, form=S.STATE['P']['form'])

def add_glow(m, glow_img, strength, tint=(1, 1, 1)):
    """Add an emission term (glow mask texture x strength) to a lit material: lit windows, lamp pools on the billboard."""
    nt = m.node_tree; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; L = nt.links.new
    src = out.inputs['Surface'].links[0].from_socket
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = S._img(glow_img)
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    if tint != (1, 1, 1):
        mx = nt.nodes.new('ShaderNodeVectorMath'); mx.operation = 'MULTIPLY'; mx.inputs[1].default_value = tint; L(tex.outputs['Color'], mx.inputs[0]); L(mx.outputs[0], em.inputs['Color'])
    else: L(tex.outputs['Color'], em.inputs['Color'])
    ad = nt.nodes.new('ShaderNodeAddShader'); L(src, ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs['Surface'])
    return m

def lit_glow(name, img, glow_img, gain=0.9, shade=1.0, strength=1.4, tint=(1, 1, 1)):
    nm = 'R_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    return add_glow(lit(name, img, gain=gain, shade=shade), glow_img, strength, tint)

def emit(name, color, strength):
    return S.mat_emit('R_e_' + name, color, strength=strength)

def additive(name, color, strength, img=None):
    """Transparent + emission (adds light on top of what is behind): bulb pools, light beams, bolt halo. Camera rays only."""
    nm = 'R_add_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    m = bpy.data.materials.new(nm); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*_lin(color), 1); lp = nt.nodes.new('ShaderNodeLightPath'); mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    L(lp.outputs['Is Camera Ray'], mul.inputs[0]); mul.inputs[1].default_value = strength
    if img:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = S._img(img); m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
        L(tex.outputs['Alpha'], m2.inputs[0]); L(mul.outputs[0], m2.inputs[1]); L(m2.outputs[0], em.inputs['Strength'])
    else: L(mul.outputs[0], em.inputs['Strength'])
    ad = nt.nodes.new('ShaderNodeAddShader'); L(tr.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_city(name, img=None, color='#808080', glow=None, gstr=1.4, gain=0.9, shade=1.0):
    """Distant city surface: the same toon light model computed in the shader (no shadow rays: cheap and noise free),
    plus a glow mask (lit windows, street lights), faded into the storm haze by view distance."""
    nm = 'R_city_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    P = S.STATE['P']; m = bpy.data.materials.new(nm); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); geo = nt.nodes.new('ShaderNodeNewGeometry')
    kd = Vector(P['key_dir']).normalized()
    nd = nt.nodes.new('ShaderNodeVectorMath'); nd.operation = 'DOT_PRODUCT'; nd.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(geo.outputs['True Normal'], nd.inputs[0])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'GREATER_THAN'; st.inputs[1].default_value = 0.12; L(nd.outputs['Value'], st.inputs[0])
    fd = nt.nodes.new('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(P['form']); L(geo.outputs['True Normal'], fd.inputs[0])
    fa = nt.nodes.new('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
    sm = shade if isinstance(shade, (tuple, list)) else (shade,) * 3
    shv = nt.nodes.new('ShaderNodeVectorMath'); shv.operation = 'SCALE'; shv.inputs[0].default_value = tuple(s * k for s, k in zip(P['shade'], sm)); L(fa.outputs[0], shv.inputs['Scale'])
    kv = nt.nodes.new('ShaderNodeVectorMath'); kv.operation = 'SCALE'; kv.inputs[0].default_value = tuple(k * gain * GAIN for k in P['key']); L(st.outputs[0], kv.inputs['Scale'])
    li = nt.nodes.new('ShaderNodeVectorMath'); li.operation = 'ADD'; L(shv.outputs[0], li.inputs[0]); L(kv.outputs[0], li.inputs[1])
    col = nt.nodes.new('ShaderNodeVectorMath'); col.operation = 'MULTIPLY'; L(li.outputs[0], col.inputs[1])
    if img:
        tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = S._img(img); L(tx.outputs['Color'], col.inputs[0])
    else: col.inputs[0].default_value = _lin(color)
    lf = nt.nodes.new('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P['lift']); L(col.outputs[0], lf.inputs[0])
    cam = nt.nodes.new('ShaderNodeCameraData')
    dd = nt.nodes.new('ShaderNodeMath'); dd.operation = 'MULTIPLY'; dd.inputs[1].default_value = -1.0 / P['haze_d']; L(cam.outputs['View Distance'], dd.inputs[0])
    ex = nt.nodes.new('ShaderNodeMath'); ex.operation = 'EXPONENT'; L(dd.outputs[0], ex.inputs[0])
    hz = nt.nodes.new('ShaderNodeMath'); hz.operation = 'MULTIPLY_ADD'; hz.inputs[1].default_value = -P['haze_max']; hz.inputs[2].default_value = P['haze_max']; L(ex.outputs[0], hz.inputs[0])
    last = lf.outputs[0]
    if glow:
        gt = nt.nodes.new('ShaderNodeTexImage'); gt.image = S._img(glow)
        gf = nt.nodes.new('ShaderNodeMath'); gf.operation = 'POWER'; L(ex.outputs[0], gf.inputs[0]); gf.inputs[1].default_value = 0.9     # lights pierce the haze
        gs = nt.nodes.new('ShaderNodeMath'); gs.operation = 'MULTIPLY'; gs.inputs[1].default_value = gstr; L(gf.outputs[0], gs.inputs[0])
        gv = nt.nodes.new('ShaderNodeVectorMath'); gv.operation = 'SCALE'; L(gt.outputs['Color'], gv.inputs[0]); L(gs.outputs[0], gv.inputs['Scale'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; L(hz.outputs[0], mix.inputs[0]); L(last, mix.inputs[6]); mix.inputs[7].default_value = (*_lin(P['haze']), 1)
    res = mix.outputs[2]
    if glow:
        ad = nt.nodes.new('ShaderNodeVectorMath'); ad.operation = 'ADD'; L(res, ad.inputs[0]); L(gv.outputs[0], ad.inputs[1]); res = ad.outputs[0]
    L(res, em.inputs['Color']); L(em.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- geometry helpers
def obox(mb, p0, p1, a, b, mat, side=(0, 0, 1), tile=1.0):
    """Box of half-sections a (along `side`) and b around the segment p0 -> p1; UVs in metres / tile."""
    p0, p1 = Vector(p0), Vector(p1); d = p1 - p0; Ln = d.length
    if Ln < 1e-6: return
    d /= Ln; sv = Vector(side); u = sv - d * sv.dot(d)
    if u.length < 1e-4:
        sv = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0)); u = sv - d * sv.dot(d)
    u.normalize(); v = d.cross(u); mb.pid += 1
    offs = [(-a, -b), (a, -b), (a, b), (-a, b)]; P = [u * x + v * y for x, y in offs]
    per = 0.0
    for i in range(4):
        j = (i + 1) % 4; w = (P[j] - P[i]).length
        mb.face([p0 + P[i], p0 + P[j], p1 + P[j], p1 + P[i]], mat, [(per / tile, 0), ((per + w) / tile, 0), ((per + w) / tile, Ln / tile), (per / tile, Ln / tile)]); per += w
    mb.face([p0 + P[3], p0 + P[2], p0 + P[1], p0 + P[0]], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.face([p1 + P[0], p1 + P[1], p1 + P[2], p1 + P[3]], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])

def cyl(mb, p0, p1, r0, mat, seg=16, r1=None, cap0=True, cap1=True, vt=None, cap_mat=None, u_rep=1.0):
    """Cylinder / cone with wrapped UVs (u around, v along: 0..1 or metres / vt)."""
    r1 = r0 if r1 is None else r1; p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0); Ln = a.length; a.normalize(); mb.pid += 1
    u = a.cross(Vector((0, 0, 1)))
    if u.length < 1e-4: u = Vector((1, 0, 0))
    u.normalize(); v = a.cross(u); V1 = Ln / vt if vt else 1.0
    ring = lambda p, r: [p + r * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg + 1)]
    A_, B_ = ring(p0, r0), ring(p1, r1)
    for i in range(seg):
        mb.face([A_[i], A_[i + 1], B_[i + 1], B_[i]], mat, [(u_rep * i / seg, 0), (u_rep * (i + 1) / seg, 0), (u_rep * (i + 1) / seg, V1), (u_rep * i / seg, V1)])
    if cap0 and r0 > 0: mb.face(A_[:seg][::-1], cap_mat or mat, [(0.5 + 0.5 * math.cos(-2 * math.pi * i / seg), 0.5 + 0.5 * math.sin(-2 * math.pi * i / seg)) for i in range(seg)])
    if cap1 and r1 > 0: mb.face(B_[:seg], cap_mat or mat, [(0.5 + 0.5 * math.cos(2 * math.pi * i / seg), 0.5 + 0.5 * math.sin(2 * math.pi * i / seg)) for i in range(seg)])

def tube(mb, pts, r, mat, seg=6):
    for a, b in zip(pts[:-1], pts[1:]): cyl(mb, a, b, r, mat, seg, cap0=False, cap1=False)

def sag(p0, p1, s, n=12):
    p0, p1 = Vector(p0), Vector(p1); return [p0.lerp(p1, i / n) + Vector((0, 0, -s * 4 * (i / n) * (1 - i / n))) for i in range(n + 1)]

def bez(pts, n=24):
    """Smooth path through control points (quadratic B-spline-ish via Chaikin)."""
    P = [Vector(p) for p in pts]
    for _ in range(3):
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]): Q += [a.lerp(b, 0.25), a.lerp(b, 0.75)]
        Q.append(P[-1]); P = Q
    return P

def quad(mb, corners, mat, uv=((0, 0), (1, 0), (1, 1), (0, 1))):
    mb.pid += 1; mb.face([Vector(c) for c in corners], mat, list(uv))

def grid(mb, fn, nu, nv, mat, uvs=(1, 1)):
    mb.pid += 1; P = [[fn(i / nu, j / nv) for i in range(nu + 1)] for j in range(nv + 1)]
    for j in range(nv):
        for i in range(nu):
            mb.face([P[j][i], P[j][i + 1], P[j + 1][i + 1], P[j + 1][i]], mat, [(uvs[0] * i / nu, uvs[1] * j / nv), (uvs[0] * (i + 1) / nu, uvs[1] * j / nv), (uvs[0] * (i + 1) / nu, uvs[1] * (j + 1) / nv), (uvs[0] * i / nu, uvs[1] * (j + 1) / nv)])

def fin(ob, cast=True):
    S.no_bounce(ob)
    if not cast: ob.visible_shadow = False
    return ob

# ----------------------------------------------------------------------------- the building and the roof slab
def building(coll, M, T):
    mb = MB(); X0, X1, Y0, Y1 = -13.0, 13.0, -10.0, 10.0; H = -GROUND
    quad(mb, [(X0, Y0, GROUND), (X1, Y0, GROUND), (X1, Y0, 0), (X0, Y0, 0)], M['facade'])
    quad(mb, [(X1, Y1, GROUND), (X0, Y1, GROUND), (X0, Y1, 0), (X1, Y1, 0)], M['facade_s'])
    quad(mb, [(X1, Y0, GROUND), (X1, Y1, GROUND), (X1, Y1, 0), (X1, Y0, 0)], M['facade_s'], ((0, 0), (20 / 26, 0), (20 / 26, 1), (0, 1)))
    quad(mb, [(X0, Y1, GROUND), (X0, Y0, GROUND), (X0, Y0, 0), (X0, Y1, 0)], M['facade_s'], ((0.2, 0), (0.2 + 20 / 26, 0), (0.2 + 20 / 26, 1), (0.2, 1)))
    zs = [GROUND + 3.8 + 3.45 * i for i in range(7)]
    for z in zs:   # floor slab ledges (real relief for the high and aerial shots)
        mb.box((X0 - 0.22, Y0 - 0.22, z - 0.12), (X1 + 0.22, Y0, z + 0.06), M['ledge'], tile=(4, 2)); mb.box((X0 - 0.22, Y1, z - 0.12), (X1 + 0.22, Y1 + 0.22, z + 0.06), M['ledge'], tile=(4, 2))
        mb.box((X0 - 0.22, Y0, z - 0.12), (X0, Y1, z + 0.06), M['ledge'], tile=(4, 2)); mb.box((X1, Y0, z - 0.12), (X1 + 0.22, Y1, z + 0.06), M['ledge'], tile=(4, 2))
    r = random.Random(4)
    for f in range(1, 7):   # AC compressors and balconies hanging on the facade
        z = GROUND + 3.8 + 3.45 * (f - 1) + 0.25
        for bay in range(8):
            x = X0 + (bay + 0.5) * 26 / 8
            if r.random() < 0.4: mb.box((x - 0.4, Y0 - 0.42, z), (x + 0.4, Y0 - 0.02, z + 0.6), M['acbox'], mats={'front': M['ac']})
            if r.random() < 0.25: mb.box((x - 1.2, Y0 - 1.0, z - 0.1), (x + 1.2, Y0, z + 0.02), M['ledge'], tile=(4, 2)); obox(mb, (x - 1.2, Y0 - 0.98, z + 1.0), (x + 1.2, Y0 - 0.98, z + 1.0), 0.03, 0.03, M['rail'])
    # vertical corner sign "เจ๊หงส์"
    mb.box((X1 + 0.1, Y0 - 1.3, GROUND + 6), (X1 + 0.35, Y0 - 0.1, GROUND + 16), M['steel'])
    quad(mb, [(X1 + 0.36, Y0 - 1.25, GROUND + 6.3), (X1 + 0.36, Y0 - 0.15, GROUND + 6.3), (X1 + 0.36, Y0 - 0.15, GROUND + 15.7), (X1 + 0.36, Y0 - 1.25, GROUND + 15.7)], M['vsign'], ((0, 1), (0, 0), (1, 0), (1, 1)))
    ob = fin(mb.obj('building', coll, hull=0.03))
    # roof slab + parapet + railing
    mb = MB(); I = 0.22; PH = 1.0
    quad(mb, [(X0 + I, Y0 + I, 0), (X1 - I, Y0 + I, 0), (X1 - I, Y1 - I, 0), (X0 + I, Y1 - I, 0)], M['floor'], ((X0 / 9, Y0 / 9), (X1 / 9, Y0 / 9), (X1 / 9, Y1 / 9), (X0 / 9, Y1 / 9)))
    mb.box((X0, Y0, 0), (X1, Y0 + I, PH), M['parapet'], tile=(4, 2)); mb.box((X0, Y1 - I, 0), (X1, Y1, PH), M['parapet'], tile=(4, 2))
    mb.box((X0, Y0 + I, 0), (X0 + I, Y1 - I, PH), M['parapet'], tile=(4, 2)); mb.box((X1 - I, Y0 + I, 0), (X1, Y1 - I, PH), M['parapet'], tile=(4, 2))
    c = 0.06
    for (a, b) in (((X0 - c, Y0 - c), (X1 + c, Y0 + I + c)), ((X0 - c, Y1 - I - c), (X1 + c, Y1 + c)), ((X0 - c, Y0), (X0 + I + c, Y1)), ((X1 - I - c, Y0), (X1 + c, Y1))):
        mb.box((a[0], a[1], PH), (b[0], b[1], PH + 0.08), M['cap'], tile=(4, 2))
    ob2 = fin(mb.obj('roof_slab', coll, hull=0.02))
    mb = MB(); zr = PH + 0.08
    def rail_run(p0, p1):
        p0, p1 = Vector(p0), Vector(p1); n = max(1, int((p1 - p0).length / 2.0))
        for i in range(n + 1): q = p0.lerp(p1, i / n); cyl(mb, q, q + Vector((0, 0, 0.62)), 0.024, M['rail'], 6)
        for h in (0.32, 0.62): cyl(mb, p0 + Vector((0, 0, h)), p1 + Vector((0, 0, h)), 0.022, M['rail'], 6)
    m = I / 2
    rail_run((X0 + m, Y0 + m, zr), (X1 - m, Y0 + m, zr)); rail_run((X1 - m, Y0 + m, zr), (X1 - m, Y1 - m, zr)); rail_run((X1 - m, Y1 - m, zr), (X0 + m, Y1 - m, zr)); rail_run((X0 + m, Y1 - m, zr), (X0 + m, Y0 + m, zr))
    # drains: floor grate + scupper + downpipe
    cyl(mb, (0.6, -9.25, 0.0), (0.6, -9.25, 0.02), 0.22, M['dark'], 16);
    for k in range(-3, 4): obox(mb, (0.6 + k * 0.05, -9.45, 0.022), (0.6 + k * 0.05, -9.05, 0.022), 0.008, 0.006, M['steel'])
    mb.box((0.3, Y0 - 0.25, -0.05), (0.9, Y0 + I, 0.12), M['dark']); cyl(mb, (0.6, Y0 - 0.25, -0.1), (0.6, Y0 - 0.25, GROUND), 0.08, M['pvc'], 10)
    cyl(mb, (-9.0, 9.25, 0.0), (-9.0, 9.25, 0.02), 0.2, M['dark'], 16)
    ob3 = fin(mb.obj('roof_rail', coll, hull=0.008))
    return ob

# ----------------------------------------------------------------------------- the billboard: lattice tower, panel, catwalk, ladder, lamps
def billboard(coll, M, T):
    mb = MB(); st = M['steel']
    yb = lambda z: 6.6 - 3.2 * z / PZ1        # raked back leg
    LV = [0.6, 2.4, 4.2, 5.9, 7.0, 8.45, 10.2, 12.0, 13.7, PZ1]
    for x in PX:
        # front post: H section, front flange faces -y
        mb.box((x - 0.13, YF - 0.13, 0.35), (x + 0.13, YF - 0.105, PZ1), st, tile=(1, 1)); mb.box((x - 0.13, YF + 0.105, 0.35), (x + 0.13, YF + 0.13, PZ1), st, tile=(1, 1))
        mb.box((x - 0.012, YF - 0.105, 0.35), (x + 0.012, YF + 0.105, PZ1), st, tile=(1, 1))
        obox(mb, (x, yb(0.35), 0.35), (x, yb(PZ1), PZ1), 0.09, 0.09, st, side=(1, 0, 0))      # back leg
        for z in (0.0,):
            mb.box((x - 0.4, YF - 0.4, 0), (x + 0.4, YF + 0.4, 0.33), M['plinth'], tile=(1, 1)); mb.box((x - 0.4, yb(0) - 0.4, 0), (x + 0.4, yb(0) + 0.4, 0.33), M['plinth'], tile=(1, 1))
            for (py) in (YF, yb(0)):
                mb.box((x - 0.28, py - 0.28, 0.33), (x + 0.28, py + 0.28, 0.36), st)
                for sx in (-0.2, 0.2):
                    for sy in (-0.2, 0.2): cyl(mb, (x + sx, py + sy, 0.36), (x + sx, py + sy, 0.42), 0.025, M['dark'], 6)
        for i, z in enumerate(LV):   # ties front -> back and zig-zag diagonals
            obox(mb, (x, YF + 0.13, z), (x, yb(z) - 0.08, z), 0.05, 0.05, st, side=(1, 0, 0))
            if i + 1 < len(LV):
                z2 = LV[i + 1]
                if i % 2 == 0: obox(mb, (x, YF + 0.13, z), (x, yb(z2) - 0.08, z2), 0.04, 0.04, st, side=(1, 0, 0))
                else: obox(mb, (x, yb(z) - 0.08, z), (x, YF + 0.13, z2), 0.04, 0.04, st, side=(1, 0, 0))
    for xa, xb in zip(PX[:-1], PX[1:]):
        for z in (0.6, 4.2, 7.0, 8.45):   # front-plane girts
            obox(mb, (xa + 0.13, YF - 0.06, z), (xb - 0.13, YF - 0.06, z), 0.06, 0.05, st, side=(0, 0, 1))
        for (z0, z1) in ((0.6, 4.2), (4.2, 7.0)):   # X bracing in the front plane
            obox(mb, (xa + 0.13, YF, z0), (xb - 0.13, YF, z1), 0.035, 0.035, st, side=(0, 1, 0)); obox(mb, (xa + 0.13, YF + 0.02, z1), (xb - 0.13, YF + 0.02, z0), 0.035, 0.035, st, side=(0, 1, 0))
        for i, z in enumerate(LV[:-1]):   # back-plane girts and X braces
            obox(mb, (xa + 0.09, yb(z), z), (xb - 0.09, yb(z), z), 0.045, 0.045, st)
            z1 = LV[i + 1]
            if i % 2 == 0: obox(mb, (xa + 0.09, yb(z), z), (xb - 0.09, yb(z1), z1), 0.03, 0.03, st)
            else: obox(mb, (xa + 0.09, yb(z1), z1), (xb - 0.09, yb(z), z), 0.03, 0.03, st)
    for z in (PZ0 + 0.3, 11.0, 12.4, 13.8, PZ1 - 0.1):   # panel purlins (C channels behind the face)
        obox(mb, (-6.0, YF - 0.17, z), (6.0, YF - 0.17, z), 0.04, 0.08, st, side=(0, 1, 0))
    # the weld joint: gusset plate between post, girt and a short knee brace
    gp = [Vector((5.27, YF - 0.135, 8.15)), Vector((5.27, YF - 0.135, 8.75)), Vector((4.85, YF - 0.135, 8.45))]
    mb.pid += 1; mb.face(gp, M['gusset'], [(0, 0), (0, 1), (1, 0.5)]); mb.face(gp[::-1], M['gusset'], [(0, 0), (1, 0.5), (0, 1)])
    obox(mb, (4.5, YF - 0.08, 7.12), (5.25, YF - 0.08, 8.40), 0.03, 0.03, st, side=(0, 1, 0))
    for k in range(6): cyl(mb, (5.27 - 0.02 * k, YF - 0.14, 8.17 + 0.1 * k), (5.27 - 0.02 * k, YF - 0.15, 8.2 + 0.1 * k), 0.018, M['weldbead'], 6)
    # junction box + conduit up the post at x 1.8, warning signs
    mb.box((1.55, YF - 0.33, 1.1), (2.05, YF - 0.13, 1.7), M['jbox']); cyl(mb, (1.68, YF - 0.2, 1.7), (1.68, YF - 0.2, CW_Z + 0.9), 0.022, M['pvc_g'], 8)
    cyl(mb, (1.68, YF - 0.2, 1.1), (1.68, YF - 0.2, 0.05), 0.022, M['pvc_g'], 8)
    quad(mb, [(5.15, YF - 0.14, 1.25), (5.65, YF - 0.14, 1.25), (5.65, YF - 0.14, 1.63), (5.15, YF - 0.14, 1.63)], M['sign_rain'])
    quad(mb, [(-2.05, YF - 0.14, 1.9), (-1.55, YF - 0.14, 1.9), (-1.55, YF - 0.14, 2.28), (-2.05, YF - 0.14, 2.28)], M['sign_hv'])
    truss = fin(mb.obj('bb_truss', coll, hull=0.012))
    # the panel
    mb = MB(); YP = 2.0
    quad(mb, [(-6, YP, PZ0), (6, YP, PZ0), (6, YP, PZ1), (-6, YP, PZ1)], M['board'])
    quad(mb, [(6, YP + 0.25, PZ0), (-6, YP + 0.25, PZ0), (-6, YP + 0.25, PZ1), (6, YP + 0.25, PZ1)], M['pback'], ((0, 0), (12 / 4, 0), (12 / 4, 6 / 2), (0, 6 / 2)))
    for (a, b) in (((-6.12, YP - 0.08, PZ0 - 0.14), (6.12, YP + 0.27, PZ0)), ((-6.12, YP - 0.08, PZ1), (6.12, YP + 0.27, PZ1 + 0.14)),
                   ((-6.12, YP - 0.08, PZ0), (-6.0, YP + 0.27, PZ1)), ((6.0, YP - 0.08, PZ0), (6.12, YP + 0.27, PZ1))):
        mb.box(a, b, st, tile=(1, 1))
    cyl(mb, (-5.8, YP + 0.1, PZ1 + 0.14), (-5.8, YP + 0.1, PZ1 + 1.6), 0.02, M['rail'], 6); mb.sphere((-5.8, YP + 0.1, PZ1 + 1.62), 0.05, M['rail'], 8, 5)   # lightning rod (disconnected)
    tube(mb, bez([(-5.8, YP + 0.12, PZ1 + 0.2), (-6.3, YP + 0.3, PZ1 - 0.5), (-6.2, YP + 0.4, PZ1 - 2.2)]), 0.012, M['cable'], 5)
    panel = fin(mb.obj('bb_panel', coll, hull=0.02))
    # catwalk
    mb = MB(); X0c, X1c, Y0c, Y1c = -6.6, 7.35, 0.85, 2.32
    quad(mb, [(X0c, Y0c, CW_Z), (X1c, Y0c, CW_Z), (X1c, Y1c, CW_Z), (X0c, Y1c, CW_Z)], M['grating'], ((X0c, Y0c), (X1c, Y0c), (X1c, Y1c), (X0c, Y1c)))
    ys = M['steel_y']
    mb.box((X0c, Y0c - 0.06, CW_Z - 0.2), (X1c, Y0c, CW_Z + 0.02), st, tile=(1, 1)); mb.box((X0c, Y1c - 0.02, CW_Z - 0.2), (X1c, Y1c + 0.04, CW_Z), st, tile=(1, 1))
    x = X0c
    while x <= X1c + 1e-3:
        mb.box((x - 0.03, Y0c, CW_Z - 0.12), (x + 0.03, Y1c, CW_Z - 0.01), st); x += 1.15
    for xp in PX:
        obox(mb, (xp, YF - 0.13, CW_Z - 0.9), (xp, Y0c + 0.02, CW_Z - 0.12), 0.035, 0.035, st, side=(1, 0, 0))
    for xp in (X1c - 0.03,): obox(mb, (xp, Y0c, CW_Z - 0.15), (6.0, YF - 0.12, CW_Z - 1.2), 0.035, 0.035, st)
    # handrail along the front + ends (gap at the ladder)
    xs = [X0c + i * (X1c - X0c) / 10 for i in range(11)]
    for xp in xs: obox(mb, (xp, Y0c + 0.03, CW_Z), (xp, Y0c + 0.03, CW_Z + 1.1), 0.025, 0.025, ys, side=(1, 0, 0))
    for h, t in ((1.1, 0.03), (0.55, 0.022)): obox(mb, (X0c, Y0c + 0.03, CW_Z + h), (X1c, Y0c + 0.03, CW_Z + h), t, t, ys)
    mb.box((X0c, Y0c - 0.005, CW_Z), (X1c, Y0c + 0.015, CW_Z + 0.12), ys, tile=(1, 1))
    for (yy) in (Y0c + 0.03, Y1c - 0.05): obox(mb, (X0c, yy, CW_Z), (X0c, yy, CW_Z + 1.1), 0.025, 0.025, ys)
    for h in (1.1, 0.55): obox(mb, (X0c, Y0c + 0.03, CW_Z + h), (X0c, Y1c - 0.05, CW_Z + h), 0.025, 0.025, ys)
    obox(mb, (X1c, Y1c - 0.05, CW_Z), (X1c, Y1c - 0.05, CW_Z + 1.1), 0.025, 0.025, ys); obox(mb, (X1c, Y1c - 0.05, CW_Z + 1.1), (X1c, 1.92, CW_Z + 1.1), 0.025, 0.025, ys)
    obox(mb, (X1c, Y0c + 0.03, CW_Z + 1.1), (X1c, 1.18, CW_Z + 1.1), 0.025, 0.025, ys)
    # lamps: arms off the handrail, heads aimed up at the face; half broken
    lamp_heads = []
    for (lx, ok) in LAMPS:
        obox(mb, (lx, Y0c + 0.03, CW_Z + 1.1), (lx, 0.15, CW_Z + 1.65), 0.025, 0.025, st)
        c = Vector((lx, 0.12, CW_Z + 1.75))
        if ok or lx < 0:
            mb.box((lx - 0.28, 0.0, CW_Z + 1.62), (lx + 0.28, 0.32, CW_Z + 1.8), M['lamp_body'])
        else:   # broken head hanging off its bracket
            obox(mb, (lx, 0.15, CW_Z + 1.65), (lx + 0.35, 0.05, CW_Z + 1.25), 0.2, 0.08, M['lamp_body'], side=(0, 1, 0))
        lamp_heads.append((tuple(c), ok))
    tube(mb, sag((X0c + 0.2, Y0c + 0.06, CW_Z + 1.02), (X1c - 0.3, Y0c + 0.06, CW_Z + 1.02), 0.12, 30), 0.012, M['cable'], 5)
    catwalk = fin(mb.obj('bb_catwalk', coll, hull=0.01))
    gm = MB()
    for (lx, ok), (c, _) in zip(LAMPS, lamp_heads):
        if ok: quad(gm, [(lx - 0.25, 0.03, CW_Z + 1.81), (lx + 0.25, 0.03, CW_Z + 1.81), (lx + 0.25, 0.3, CW_Z + 1.81), (lx - 0.25, 0.3, CW_Z + 1.81)], M['lamp_on'])
        elif lx < 0: quad(gm, [(lx - 0.25, 0.03, CW_Z + 1.81), (lx + 0.25, 0.03, CW_Z + 1.81), (lx + 0.25, 0.3, CW_Z + 1.81), (lx - 0.25, 0.3, CW_Z + 1.81)], M['lamp_off'])
    lg = fin(gm.obj('bb_lamp_glass', coll), cast=False)
    bm = MB()   # light beams in the rain, from the working lamps up the face
    for (lx, ok) in LAMPS:
        if ok: cyl(bm, (lx, 0.25, CW_Z + 1.85), (lx, 1.75, PZ0 + 3.2), 0.22, M['beam'], 14, r1=1.9, cap0=False, cap1=False)
    beams = fin(bm.obj('bb_beams', coll), cast=False)
    # ladder with safety cage (right end)
    mb = MB(); LX = 7.48; LY0, LY1 = 1.28, 1.82; top = CW_Z + 1.15
    for yy in (LY0, LY1): obox(mb, (LX, yy, 0.0), (LX, yy, top), 0.03, 0.008, ys, side=(1, 0, 0))
    z = 0.3
    while z < top - 0.2: cyl(mb, (LX, LY0, z), (LX, LY1, z), 0.017, M['rail'], 6); z += 0.3
    for zz in [2.4 + i * 0.85 for i in range(7)]:
        pts = [Vector((LX + 0.38 - 0.42 * math.cos(a), (LY0 + LY1) / 2 - 0.42 * math.sin(a), zz)) for a in [math.pi * (-0.5 + i / 8) for i in range(9)]]
        pts = [Vector((LX + 0.42 * math.sin(math.pi * i / 8), (LY0 + LY1) / 2 - 0.42 * math.cos(math.pi * i / 8), zz)) for i in range(9)]
        for a, b in zip(pts[:-1], pts[1:]): obox(mb, a, b, 0.006, 0.025, ys, side=(0, 0, 1))
    for i in (1, 3, 4, 5, 7):
        a = math.pi * i / 8; p = Vector((LX + 0.42 * math.sin(a), (LY0 + LY1) / 2 - 0.42 * math.cos(a), 2.4)); obox(mb, p, p + Vector((0, 0, top - 2.4)), 0.02, 0.006, ys)
    for yy in (LY0, LY1): obox(mb, (LX, yy, top), (X1c - 0.25, yy, top - 0.05), 0.022, 0.022, ys)
    for yy in (LY0, LY1): obox(mb, (LX, yy, 1.0), (LX - 0.55, yy, 1.0), 0.02, 0.02, st)   # wall ties to the frame
    ladder = fin(mb.obj('bb_ladder', coll, hull=0.008))
    A.update(lamp_heads=lamp_heads, billboard_face=dict(x0=-6, x1=6, z0=PZ0, z1=PZ1, y=YP, normal=(0, -1, 0)),
             catwalk=dict(x0=X0c, x1=X1c, y0=Y0c, y1=Y1c, z=CW_Z, rail_y=Y0c + 0.03, rail_h=1.1),
             ladder=dict(x=LX, y=(LY0 + LY1) / 2, base=(LX + 0.35, (LY0 + LY1) / 2, 0.0), top=(X1c - 0.4, (LY0 + LY1) / 2, CW_Z)))

# ----------------------------------------------------------------------------- stair hut
def stair_hut(coll, M):
    mb = MB(); X0, X1, Y0, Y1, H = -12.78, -8.4, -9.78, -6.0, 2.9
    mb.box((X0, Y0, 0), (X1, Y1, H), M['hut'], tile=(4, 3))
    mb.box((X0 - 0.05, Y0 - 0.05, H), (X1 + 0.35, Y1 + 0.3, H + 0.18), M['cap'], tile=(4, 2))
    dy0, dy1 = -7.75, -6.75
    mb.box((X1, dy0 - 0.12, 0), (X1 + 0.08, dy0, 2.22), M['steel']); mb.box((X1, dy1, 0), (X1 + 0.08, dy1 + 0.12, 2.22), M['steel']); mb.box((X1, dy0 - 0.12, 2.1), (X1 + 0.08, dy1 + 0.12, 2.22), M['steel'])
    quad(mb, [(X1 + 0.01, dy0, 0.04), (X1 + 0.01, dy1, 0.04), (X1 + 0.01, dy1, 2.1), (X1 + 0.01, dy0, 2.1)], M['door'])
    mb.sphere((X1 + 0.08, dy1 - 0.12, 1.02), 0.04, M['rail'], 8, 5); mb.box((X1 + 0.01, dy1 - 0.16, 0.98), (X1 + 0.06, dy1 - 0.08, 1.06), M['rail'])
    mb.box((X1, dy0 - 0.3, 0), (X1 + 0.45, dy1 + 0.3, 0.12), M['plinth'], tile=(1, 1))
    mb.box((X1 + 0.0, -9.2, 1.3), (X1 + 0.18, -8.7, 1.95), M['jbox'])       # electric meter box
    cyl(mb, (X1 + 0.09, -8.95, 1.95), (X1 + 0.09, -8.95, H), 0.02, M['pvc_g'], 6)
    # bulb with a little hood over the door
    mb.box((X1, -7.45, 2.36), (X1 + 0.22, -7.05, 2.42), M['steel']); cyl(mb, (X1 + 0.15, -7.25, 2.36), (X1 + 0.15, -7.25, 2.3), 0.03, M['dark'], 8)
    for k in range(4): a = k * math.pi / 2; obox(mb, (X1 + 0.15 + 0.07 * math.cos(a), -7.25 + 0.07 * math.sin(a), 2.3), (X1 + 0.15 + 0.07 * math.cos(a), -7.25 + 0.07 * math.sin(a), 2.15), 0.005, 0.005, M['dark'])
    # louvre vent on the +y face, a lightning rod and a vent stack on the roof
    mb.box((-11.4, Y1, 1.6), (-10.4, Y1 + 0.06, 2.3), M['steel'])
    for k in range(6): obox(mb, (-11.35, Y1 + 0.07, 1.68 + k * 0.1), (-10.45, Y1 + 0.07, 1.68 + k * 0.1), 0.012, 0.03, M['dark'], side=(0, 1, 1))
    cyl(mb, (-12.3, -9.3, H + 0.18), (-12.3, -9.3, H + 1.6), 0.015, M['rail'], 6)
    cyl(mb, (-9.2, -6.5, H + 0.18), (-9.2, -6.5, H + 0.9), 0.06, M['pvc'], 10); cyl(mb, (-9.2, -6.5, H + 0.9), (-9.2, -6.5, H + 1.0), 0.12, M['pvc'], 10)
    hut = fin(mb.obj('stair_hut', coll, hull=0.02))
    gm = MB(); gm.sphere((X1 + 0.15, -7.25, 2.22), 0.065, M['bulb'], 10, 6); b = fin(gm.obj('hut_bulb', coll), cast=False)
    dm = MB()
    quad(dm, [(X1 + 0.02, -8.65, 0.9), (X1 + 0.02, -5.85, 0.9), (X1 + 0.02, -5.85, 3.3), (X1 + 0.02, -8.65, 3.3)], M['pool_warm'])
    quad(dm, [(X1 + 0.05, -8.9, 0.012), (X1 + 2.9, -8.9, 0.012), (X1 + 2.9, -5.6, 0.012), (X1 + 0.05, -5.6, 0.012)], M['pool_warm_f'])
    fin(dm.obj('hut_bulb_pool', coll), cast=False)
    A.update(hut_door=(X1 + 0.6, (dy0 + dy1) / 2, 0.0), hut_bulb=(X1 + 0.15, -7.25, 2.22))

# ----------------------------------------------------------------------------- rooftop clutter
def clutter(coll, M):
    mb = MB(); r = random.Random(11)
    # water tanks on stilts + blue PVC pipes into the hut
    for (tx, ty) in ((-10.6, 4.4), (-10.6, 7.5)):
        for sx in (-0.85, 0.85):
            for sy in (-0.85, 0.85): obox(mb, (tx + sx, ty + sy, 0), (tx + sx * 0.8, ty + sy * 0.8, 1.6), 0.045, 0.045, M['steel'])
        for z in (0.5, 1.6):
            for (a, b) in (((-0.85, -0.85), (0.85, -0.85)), ((0.85, -0.85), (0.85, 0.85)), ((0.85, 0.85), (-0.85, 0.85)), ((-0.85, 0.85), (-0.85, -0.85))):
                k = 0.8 if z > 1 else 0.93; obox(mb, (tx + a[0] * k, ty + a[1] * k, z), (tx + b[0] * k, ty + b[1] * k, z), 0.04, 0.04, M['steel'])
        mb.box((tx - 0.95, ty - 0.95, 1.6), (tx + 0.95, ty + 0.95, 1.66), M['tread'], tile=(1, 1))
        cyl(mb, (tx, ty, 1.66), (tx, ty, 4.0), 1.1, M['tank'], 28, cap0=False, cap1=False)
        cyl(mb, (tx, ty, 4.0), (tx, ty, 4.4), 1.1, M['tank_top'], 28, r1=0.3, cap0=False, cap1=False); cyl(mb, (tx, ty, 4.4), (tx, ty, 4.5), 0.3, M['pvc'], 16)
        for z in (2.1, 3.0, 3.8): cyl(mb, (tx, ty, z), (tx, ty, z + 0.05), 1.12, M['tank_band'], 28, cap0=False, cap1=False)
        tube(mb, [Vector((tx + 0.5, ty - 0.6, 1.7)), Vector((tx + 0.5, ty - 0.6, 0.15)), Vector((tx + 0.5, -5.6, 0.15)), Vector((tx + 0.5, -5.95, 0.9)), Vector((tx + 0.5, -5.95, 2.6))], 0.05, M['pvc'], 10)
    # AC condensers along the right parapet, fan guards, copper pipes into a cable tray
    for i, y in enumerate((-8.2, -6.8, -5.4, -4.0, -2.6, -1.2)):
        x0 = 12.2; mb.box((x0 - 0.05, y - 0.5, 0), (x0 + 0.4, y + 0.5, 0.14), M['plinth'], tile=(1, 1))
        mb.box((x0, y - 0.46, 0.14), (x0 + 0.36, y + 0.46, 0.84), M['acbox'], mats={'left': M['ac' if i % 2 else 'ac2']})
        cyl(mb, (x0 - 0.002, y - 0.08, 0.49), (x0 - 0.06, y - 0.08, 0.49), 0.29, M['rail'], 20, r1=0.27, cap0=False, cap1=False)
        tube(mb, [Vector((x0 + 0.1, y + 0.46, 0.3)), Vector((x0 + 0.1, y + 0.62, 0.3)), Vector((x0 - 0.3, y + 0.62, 0.28)), Vector((x0 - 0.3, -9.0, 0.28))], 0.02, M['copper'], 6)
    # cable trays: along the front parapet from the hut to the AC bank, and a branch to the billboard
    def tray(p0, p1):
        p0, p1 = Vector(p0), Vector(p1); d = (p1 - p0); Ln = d.length; d.normalize(); s = Vector((-d.y, d.x, 0))
        obox(mb, p0, p1, 0.16, 0.01, M['steel'], side=s); obox(mb, p0 + s * 0.16 + Vector((0, 0, 0.06)), p1 + s * 0.16 + Vector((0, 0, 0.06)), 0.01, 0.06, M['steel'], side=s)
        obox(mb, p0 - s * 0.16 + Vector((0, 0, 0.06)), p1 - s * 0.16 + Vector((0, 0, 0.06)), 0.01, 0.06, M['steel'], side=s)
        for k in range(int(Ln / 1.4) + 1):
            q = p0 + d * min(k * 1.4, Ln); obox(mb, q - s * 0.2 + Vector((0, 0, -0.01)), q + s * 0.2 + Vector((0, 0, -0.01)), 0.03, 0.03, M['steel'], side=Vector((0, 0, 1)))
            for e in (-0.18, 0.18): obox(mb, q + s * e + Vector((0, 0, -0.01)), q + s * e - Vector((0, 0, p0.z)), 0.02, 0.02, M['steel'])
        for j, (o, rr, mm) in enumerate(((-0.08, 0.03, 'cable'), (0.0, 0.025, 'cable_g'), (0.07, 0.035, 'cable'))):
            cyl(mb, p0 + s * o + Vector((0, 0, rr + 0.012)), p1 + s * o + Vector((0, 0, rr + 0.012)), rr, M[mm], 6, cap0=False, cap1=False)
    tray((-8.3, -9.05, 0.28), (11.9, -9.05, 0.28)); tray((-3.2, -8.85, 0.28), (-3.2, 1.6, 0.28))
    # satellite dishes
    for (dx, dy, R, col) in ((9.4, 6.9, 0.55, 'dish'), (11.2, 8.8, 0.38, 'dish_o')):
        cyl(mb, (dx, dy, 0), (dx, dy, 1.5), 0.04, M['rail'], 8); mb.box((dx - 0.25, dy - 0.25, 0), (dx + 0.25, dy + 0.25, 0.12), M['plinth'], tile=(1, 1))
        ax = Vector((-0.25, -0.55, 0.8)).normalized(); c0 = Vector((dx, dy, 1.6))
        cyl(mb, c0, c0 + ax * 0.16, 0.06, M[col], 20, r1=R, cap0=True, cap1=False)
        tip = c0 + ax * 0.75; obox(mb, c0 + ax * 0.02 - Vector((0, 0, R * 0.8)), tip, 0.012, 0.012, M['rail']); mb.box(tuple(tip - Vector((0.05, 0.05, 0.05))), tuple(tip + Vector((0.05, 0.05, 0.05))), M['dark'])
        obox(mb, c0, (dx, dy, 1.45), 0.03, 0.03, M['rail'])
    # TV antennas with guy wires
    for (ax_, ay, h, rot) in ((12.0, 9.0, 4.6, 0.4), (-6.6, -9.3, 3.8, -0.3), (12.1, -9.4, 5.2, 1.1)):
        cyl(mb, (ax_, ay, 0), (ax_, ay, h), 0.03, M['rail'], 8)
        for lvl, L in ((h - 0.1, 1.5), (h - 0.9, 1.1)):
            d = Vector((math.cos(rot), math.sin(rot), 0)); p = Vector((ax_, ay, lvl)); cyl(mb, p - d * L / 2, p + d * L / 2, 0.012, M['rail'], 5)
            n = Vector((-d.y, d.x, 0))
            for k in range(8):
                q = p - d * L / 2 + d * L * k / 7; w = 0.55 - 0.035 * k; cyl(mb, q - n * w / 2, q + n * w / 2, 0.006, M['rail'], 4, cap0=False, cap1=False)
        for k in range(3):
            a = rot + k * 2.1; g = Vector((ax_ + 1.6 * math.cos(a), ay + 1.6 * math.sin(a), 0.6))
            cyl(mb, (ax_, ay, h * 0.7), g, 0.004, M['cable'], 4, cap0=False, cap1=False)
    # plastic chairs (red upright, blue tipped over), buckets, a tyre with rainwater
    def chair(cx, cy, mat, rot=0.0, tip=False):
        R_ = lambda x, y, z: Vector((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot), z))
        if tip:
            R_ = (lambda f: (lambda x, y, z: f(x, -z + 0.25, y + 0.25)))(R_)
        for sx in (-0.21, 0.21):
            for sy in (-0.2, 0.2): obox(mb, R_(sx * 1.12, sy * 1.12, 0), R_(sx, sy, 0.43), 0.022, 0.022, mat)
        mb.pid += 1
        sq = [R_(-0.23, -0.23, 0.45), R_(0.23, -0.23, 0.45), R_(0.23, 0.21, 0.45), R_(-0.23, 0.21, 0.45)]
        obox(mb, (sq[0] + sq[3]) / 2, (sq[1] + sq[2]) / 2, 0.22, 0.02, mat, side=(R_(0, 1, 0) - R_(0, 0, 0)))
        obox(mb, R_(-0.22, 0.22, 0.45), R_(-0.24, 0.3, 0.9), 0.02, 0.02, mat); obox(mb, R_(0.22, 0.22, 0.45), R_(0.24, 0.3, 0.9), 0.02, 0.02, mat)
        obox(mb, R_(0, 0.24, 0.62), R_(0, 0.31, 0.88), 0.24, 0.015, mat, side=(R_(1, 0, 0) - R_(0, 0, 0)))
        for sx in (-0.24, 0.24): obox(mb, R_(sx, -0.18, 0.62), R_(sx, 0.26, 0.64), 0.02, 0.025, mat)
    chair(3.4, -4.3, M['red'], 0.5); chair(-1.2, -6.9, M['blue'], -0.3, tip=True)
    for (bx, by, col, h) in ((2.6, -3.3, 'blue', 0.32), (2.95, -3.85, 'orange', 0.3), (-4.2, 5.0, 'green', 0.36)):
        cyl(mb, (bx, by, 0), (bx, by, h), 0.13, M[col], 14, r1=0.16, cap1=False)
        cyl(mb, (bx, by, h * 0.93), (bx, by, h * 0.94), 0.158, M['water'], 14, cap0=False)
        tube(mb, [Vector((bx - 0.16, by, h)), Vector((bx - 0.08, by - 0.06, h + 0.14)), Vector((bx + 0.08, by - 0.06, h + 0.14)), Vector((bx + 0.16, by, h))], 0.006, M['rail'], 4)
    cyl(mb, (0.2, -8.4, 0.16), (0.55, -8.2, 0.16), 0.13, M['grey'], 14, r1=0.16, cap1=False)
    cyl(mb, (-6.5, 3.2, 0.0), (-6.5, 3.2, 0.2), 0.32, M['tyre'], 18); cyl(mb, (-6.5, 3.2, 0.2), (-6.5, 3.2, 0.205), 0.2, M['water'], 14, cap0=False)
    # styrofoam planter boxes with dead and live plants along the left parapet; brick stacks
    for i, y in enumerate((-4.2, -3.4, -2.6, -1.4, -0.6)):
        x = -12.25; mb.box((x - 0.3, y - 0.2, 0), (x + 0.3, y + 0.2, 0.3), M['foam'])
        for k in range(4):
            px, py = x + r.uniform(-0.2, 0.2), y + r.uniform(-0.12, 0.12)
            if i % 2: mb.sphere((px, py, 0.38 + r.uniform(0, 0.1)), r.uniform(0.09, 0.15), M['leaf'], 8, 5)
            else: obox(mb, (px, py, 0.3), (px + r.uniform(-0.1, 0.1), py + r.uniform(-0.1, 0.1), 0.62), 0.008, 0.008, M['twig'])
    for (bx, by, n) in ((-7.4, -3.2, 3), (8.8, 1.2, 4)):
        for k in range(n):
            for j in range(3): mb.box((bx + j * 0.24, by, k * 0.075), (bx + j * 0.24 + 0.22, by + 0.11, k * 0.075 + 0.07), M['brick'])
    # welder's gear near the ladder: gas cylinders on a trolley, welding machine, toolbox, steel stock
    for (gx, mat) in ((6.25, 'o2'), (6.55, 'c2h2')):
        gy = 0.15; cyl(mb, (gx, gy, 0.12), (gx, gy, 1.35), 0.115, M[mat], 16, cap0=False, cap1=False)
        cyl(mb, (gx, gy, 1.35), (gx, gy, 1.5), 0.115, M[mat + '_t'], 16, r1=0.05, cap0=False); cyl(mb, (gx, gy, 1.5), (gx, gy, 1.6), 0.025, M['brass'], 8)
        mb.box((gx - 0.05, gy - 0.12, 1.58), (gx + 0.05, gy - 0.03, 1.66), M['brass']); cyl(mb, (gx, gy - 0.12, 1.62), (gx, gy - 0.15, 1.62), 0.04, M['gauge'], 12)
    mb.box((6.0, -0.05, 0.08), (6.8, 0.35, 0.12), M['steel']); obox(mb, (6.05, 0.33, 0.12), (6.1, 0.3, 1.25), 0.02, 0.02, M['steel']); obox(mb, (6.75, 0.33, 0.12), (6.7, 0.3, 1.25), 0.02, 0.02, M['steel'])
    obox(mb, (6.1, 0.3, 1.25), (6.7, 0.3, 1.25), 0.02, 0.02, M['steel']); obox(mb, (6.05, 0.0, 0.85), (6.75, 0.0, 0.85), 0.01, 0.025, M['chain'])
    for wx in (5.98, 6.82): cyl(mb, (wx, 0.32, 0.12), (wx + (0.04 if wx > 6.4 else -0.04), 0.32, 0.12), 0.12, M['tyre'], 14)
    for (hx, hm, dx) in ((6.25, 'hose_g', 0.0), (6.55, 'hose_r', 0.04)):   # hoses: cylinder -> along the floor -> up the ladder -> onto the catwalk
        tube(mb, bez([(hx, 0.03, 1.62), (hx + 0.3, -0.25, 1.0), (hx + 0.6, -0.1, 0.05), (7.2, 0.9 + dx, 0.05), (7.42, 1.22 + dx, 0.6), (7.42, 1.22 + dx, 4.0), (7.42, 1.22 + dx, 7.6),
                       (7.0, 1.3 + dx, CW_Z + 0.04), (6.0, 1.9 + dx, CW_Z + 0.04), (5.3, 1.75 + dx, CW_Z + 0.04)]), 0.013, M[hm], 6)
    mb.box((6.05, -1.45, 0.0), (6.65, -1.05, 0.48), M['machine_b'], mats={'front': M['machine']})
    tube(mb, bez([(6.35, -1.05, 0.3), (6.9, -0.6, 0.05), (7.3, 0.6, 0.05), (7.5, 1.2, 0.5), (7.52, 1.3, 7.4), (6.8, 1.4, CW_Z + 0.04), (5.6, 1.5, CW_Z + 0.05)]), 0.018, M['cable'], 6)
    mb.box((4.35, -1.15, 0.0), (4.9, -0.9, 0.24), M['toolbox_b'], mats={'front': M['toolbox']}); obox(mb, (4.35, -0.9, 0.24), (4.9, -0.9, 0.24), 0.002, 0.002, M['red'])
    mb.pid += 1; mb.face([Vector((4.35, -0.9, 0.24)), Vector((4.9, -0.9, 0.24)), Vector((4.9, -0.72, 0.43)), Vector((4.35, -0.72, 0.43))], M['red'])
    obox(mb, (4.5, -1.32, 0.02), (4.8, -1.45, 0.02), 0.012, 0.012, M['wood']); mb.box((4.78, -1.5, 0.0), (4.86, -1.4, 0.06), M['dark'])
    for k in range(5): obox(mb, (1.2, -1.6 + k * 0.09, 0.14 + (k % 2) * 0.06), (4.0, -1.6 + k * 0.09, 0.14 + (k % 2) * 0.06), 0.035, 0.035, M['steel'])
    for xw in (1.5, 3.6): mb.box((xw, -1.75, 0), (xw + 0.12, -1.1, 0.1), M['wood'])
    mb.sphere((5.2, -0.6, 0.12), 0.13, M['dark'], 10, 6)   # spare welding helmet
    # vent stacks, old leaning lightbox sign
    for (vx, vy) in ((-2.0, 8.6), (4.5, 8.9)):
        cyl(mb, (vx, vy, 0), (vx, vy, 1.2), 0.07, M['pvc'], 10); cyl(mb, (vx, vy, 1.2), (vx, vy, 1.32), 0.16, M['pvc'], 10, r1=0.05)
    ob = fin(mb.obj('clutter', coll, hull=0.01))
    # old lightbox sign leaning on the right parapet (unlit)
    mb = MB(); quad(mb, [(12.55, 3.2, 0.05), (12.55, 5.6, 0.05), (12.75, 5.6, 0.95), (12.75, 3.2, 0.95)], M['oldsign'])
    obox(mb, (12.5, 3.15, 0.0), (12.72, 3.15, 1.0), 0.03, 0.03, M['steel']); obox(mb, (12.5, 5.65, 0.0), (12.72, 5.65, 1.0), 0.03, 0.03, M['steel'])
    fin(mb.obj('oldsign', coll, hull=0.01))
    # blue tarp over a pile of junk, one corner lifted by the wind, roped to bricks
    mb = MB(); cx, cy, W2, D2 = -5.6, -5.0, 1.6, 1.15
    def tarp_pt(u, v):
        x = cx + (u - 0.5) * 2 * W2 * 1.15; y = cy + (v - 0.5) * 2 * D2 * 1.2
        nx = abs(x - cx) / W2; ny = abs(y - cy) / D2; inside = max(nx, ny)
        z = 0.95 * max(0.0, 1 - max(0.0, inside - 0.75) * 4) + 0.04 * math.sin(u * 23 + v * 7)
        z = max(z, 0.02); lift = max(0.0, (u - 0.62)) * max(0.0, (0.45 - v)) * 9.0
        return Vector((x - lift * 0.2, y - lift * 0.15, z + lift * 0.55 + 0.05 * math.sin(u * 40) * lift))
    grid(mb, tarp_pt, 26, 20, M['tarp'], (2.6, 2.0))
    for (u, v) in ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0)):
        p = tarp_pt(u, v); mb.box(tuple(p + Vector((-0.12, -0.06, -p.z))), tuple(p + Vector((0.12, 0.06, 0.08 - p.z))), M['brick'])
    fin(mb.obj('tarp', coll, hull=0.01))
    # clothesline with wet laundry
    mb = MB(); p0, p1 = Vector((-7.6, -7.1, 1.95)), Vector((-2.4, -7.6, 1.95))
    for p in (p0, p1): cyl(mb, (p.x, p.y, 0), p, 0.03, M['rail'], 6); mb.box((p.x - 0.15, p.y - 0.15, 0), (p.x + 0.15, p.y + 0.15, 0.1), M['plinth'])
    wire = sag(p0, p1, 0.22, 20); tube(mb, wire, 0.005, M['cable'], 4)
    items = [(0.12, 0.55, 0.75, 'cl1'), (0.27, 0.5, 0.6, 'cl2'), (0.42, 0.7, 0.4, 'cl3'), (0.58, 0.45, 0.85, 'cl4'), (0.73, 0.55, 0.65, 'cl2'), (0.88, 0.4, 0.5, 'cl1')]
    for (u, w, h, m) in items:
        def at(t): i = t * 20; k = min(int(i), 19); return wire[k].lerp(wire[k + 1], i - k)
        a = at(u - w / 2 / 5.2); b = at(u + w / 2 / 5.2); sw = Vector((0.12, 0.18, 0))
        grid(mb, lambda s, t, a=a, b=b, h=h, sw=sw: a.lerp(b, s) + Vector((0, 0, -h * (1 - t))) + sw * (1 - t) ** 1.5 + Vector((0, 0.04 * math.sin(s * 9 + t * 3), 0)), 4, 3, M[m])
    fin(mb.obj('laundry', coll, hull=0.006))
    A.update(chair=(3.4, -4.3, 0.0), gas=(6.4, 0.15, 0.0), toolbox=(4.62, -1.02, 0.24), tarp=(cx, cy, 0.0), tanks=[(-10.6, 4.4, 0.0), (-10.6, 7.5, 0.0)],
             machine=(6.35, -1.25, 0.48), clothesline=(tuple(p0), tuple(p1)))

# ----------------------------------------------------------------------------- the city: blocks to the horizon, river, expressway, temples
def river_y(x): return 340.0 + 55.0 * math.sin(x / 420.0 + 0.6)
RIV_W = 150.0

def city(coll, M):
    rnd = random.Random(2026)
    TILE = dict(shop=(16, 14), flat=(12, 12), office=(12, 12), condo=(12, 12), old=(12, 12))
    mats = dict(shop1=M['c_shop1'], shop2=M['c_shop2'], flat=M['c_flat'], office=M['c_office'], condo=M['c_condo'], old=M['c_old'])
    near = MB(); far = MB(); roofs = []
    WAT = Vector((-110.0, river_y(-110) - RIV_W - 42)); UBO = Vector((95.0, 38.0))
    def bldg(mb, x0, y0, x1, y1, h, kind):
        tex = kind if kind != 'shop' else rnd.choice(['shop1', 'shop2']); tw, th = TILE[kind]; m = mats[tex]; z0, z1 = GROUND, GROUND + h
        off = rnd.randrange(8) * 0.25; mb.pid += 1
        walls = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
        u = off
        for (a, b) in walls:
            L = math.hypot(b[0] - a[0], b[1] - a[1]); mb.pid += 1
            mb.face([Vector((a[0], a[1], z0)), Vector((b[0], b[1], z0)), Vector((b[0], b[1], z1)), Vector((a[0], a[1], z1))], m,
                    [(u, 0), (u + L / tw, 0), (u + L / tw, h / th), (u, h / th)]); u += L / tw
        mb.pid += 1; ru = rnd.random()
        mb.face([Vector((x0, y0, z1)), Vector((x1, y0, z1)), Vector((x1, y1, z1)), Vector((x0, y1, z1))], M['c_roof'], [(ru + x0 / 16, y0 / 16), (ru + x1 / 16, y0 / 16), (ru + x1 / 16, y1 / 16), (ru + x0 / 16, y1 / 16)])
        return z1
    def blocked(x0, y0, x1, y1):
        if x1 > -16 and x0 < 16 and y1 > -13 and y0 < 13: return True
        for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2)):
            if abs(y - river_y(x)) < RIV_W + 6: return True
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if (Vector((cx, cy)) - WAT).length < 75 or (Vector((cx, cy)) - UBO).length < 34: return True
        return False
    def split(x0, y0, x1, y1, depth, out):
        w, d = x1 - x0, y1 - y0
        if depth > 3 or (max(w, d) < 26 and rnd.random() < 0.6) or max(w, d) < 14: out.append((x0, y0, x1, y1)); return
        if w > d:
            s = x0 + w * rnd.uniform(0.35, 0.65); split(x0, y0, s - 1.0, y1, depth + 1, out); split(s + 1.0, y0, x1, y1, depth + 1, out)
        else:
            s = y0 + d * rnd.uniform(0.35, 0.65); split(x0, y0, x1, s - 1.0, depth + 1, out); split(x0, s + 1.0, x1, y1, depth + 1, out)
    nb = 0; trees = MB()
    for j in range(-16, 41):
        for i in range(-28, 29):
            bx0, by0, bx1, by1 = 60 * i - 18, 60 * j - 30, 60 * i + 30, 60 * j + 18
            cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2; dist = math.hypot(cx, cy)
            if dist > 2300: continue
            east = cy > river_y(cx) + RIV_W
            lots = []; split(bx0, by0, bx1, by1, 0, lots)
            for (x0, y0, x1, y1) in lots:
                if blocked(x0, y0, x1, y1): continue
                lx, ly = (x0 + x1) / 2, (y0 + y1) / 2; dd = math.hypot(lx, ly); area = (x1 - x0) * (y1 - y0)
                if dd < 600 and rnd.random() < 0.08:   # trees
                    for k in range(3): trees.sphere((rnd.uniform(x0, x1), rnd.uniform(y0, y1), GROUND + rnd.uniform(4, 7)), rnd.uniform(3, 6), M['c_tree'], 8, 5)
                    continue
                if east:
                    dr = ly - river_y(lx) - RIV_W; tall = rnd.random() < (0.06 if dr < 700 else 0.03)
                    kind = rnd.choice(['office', 'condo', 'office']) if tall else rnd.choice(['flat', 'old', 'shop', 'condo'])
                    h = rnd.choice([rnd.uniform(40, 80), rnd.uniform(55, 110), rnd.uniform(90, 170)]) if tall else rnd.uniform(9, 34)
                    if tall and area > 500: hw_ = rnd.uniform(9, 15); x0, x1 = lx - hw_, lx + hw_; y0, y1 = ly - hw_ * rnd.uniform(0.7, 1.2), ly + hw_ * rnd.uniform(0.7, 1.2)
                else:
                    r_ = rnd.random()
                    if dd < 110: kind, h = rnd.choice(['shop', 'shop', 'old', 'flat']), rnd.uniform(7, 17)
                    elif r_ < 0.05 and dd > 150: kind, h = rnd.choice(['condo', 'office']), rnd.uniform(40, 95)
                    elif r_ < 0.5: kind, h = 'shop', rnd.choice([10.5, 14.0, 14.0, 7.0])
                    else: kind, h = rnd.choice(['flat', 'old', 'condo']), rnd.uniform(9, 30)
                if 70 < ly < 100: h = min(h, 9.0)    # under the expressway
                mb = near if dd < 400 else far
                z1 = bldg(mb, x0, y0, x1, y1, h, kind); nb += 1
                if dd < 260 and h < 40:   # rooftop junk on the near blocks
                    for k in range(rnd.randint(1, 3)):
                        px, py = rnd.uniform(x0 + 1.5, x1 - 1.5), rnd.uniform(y0 + 1.5, y1 - 1.5)
                        if rnd.random() < 0.5: cyl(near, (px, py, z1), (px, py, z1 + 1.8), 0.7, M['c_tank'], 10)
                        else: near.box((px - 0.6, py - 0.4, z1), (px + 0.6, py + 0.4, z1 + 0.8), M['c_ac'])
                    near.box((x0, y0, z1), (x1, y0 + 0.2, z1 + 0.9), M['c_roof']); near.box((x0, y1 - 0.2, z1), (x1, y1, z1 + 0.9), M['c_roof'])
    # landmark neighbours (taller, close: parallax for the hero shots) with signs on top
    specials = [(-78, 38, 16, 14, 52, 'condo', 'neon1'), (128, -78, 14, 14, 74, 'office', 'neon3'), (-40, -88, 18, 12, 30, 'flat', 'neon2'), (60, -40, 12, 10, 22, 'old', 'neon4')]
    sm = MB()
    for (sx, sy, w, d, h, kind, sg) in specials:
        z1 = bldg(near, sx - w, sy - d, sx + w, sy + d, h, kind)
        quad(sm, [(sx - w * 0.85, sy - d - 0.6, z1 + 0.4), (sx + w * 0.85, sy - d - 0.6, z1 + 0.4), (sx + w * 0.85, sy - d - 0.6, z1 + 0.4 + w * 0.42), (sx - w * 0.85, sy - d - 0.6, z1 + 0.4 + w * 0.42)], M[sg])
        obox(near, (sx - w * 0.7, sy - d - 0.4, z1), (sx - w * 0.7, sy - d - 0.4, z1 + 0.5), 0.15, 0.15, M['c_ac']); obox(near, (sx + w * 0.7, sy - d - 0.4, z1), (sx + w * 0.7, sy - d - 0.4, z1 + 0.5), 0.15, 0.15, M['c_ac'])
    fin(near.obj('city_near', coll), cast=False); fin(far.obj('city_far', coll), cast=False); fin(trees.obj('city_trees', coll), cast=False); fin(sm.obj('city_signs', coll), cast=False)
    # aircraft warning lights on the tall towers are drawn as tiny red emitters
    # ground, river, embankments
    g = MB(); E = 6000
    quad(g, [(-E, -E, GROUND), (E, -E, GROUND), (E, E, GROUND), (-E, E, GROUND)], M['c_ground'], ((-E / 60 + 0.5, -E / 60 + 0.5), (E / 60 + 0.5, -E / 60 + 0.5), (E / 60 + 0.5, E / 60 + 0.5), (-E / 60 + 0.5, E / 60 + 0.5)))
    xs = [-3000 + 50 * i for i in range(121)]
    for a, b in zip(xs[:-1], xs[1:]):
        ya0, ya1 = river_y(a), river_y(b); g.pid += 1
        g.face([Vector((a, ya0 - RIV_W, GROUND + 0.08)), Vector((b, ya1 - RIV_W, GROUND + 0.08)), Vector((b, ya1 + RIV_W, GROUND + 0.08)), Vector((a, ya0 + RIV_W, GROUND + 0.08))], M['c_river'],
               [(a / 200, (ya0 - RIV_W) / 100), (b / 200, (ya1 - RIV_W) / 100), (b / 200, (ya1 + RIV_W) / 100), (a / 200, (ya0 + RIV_W) / 100)])
        for sgn in (-1, 1):
            g.pid += 1; o = sgn * (RIV_W + 0.5)
            g.face([Vector((a, ya0 + o, GROUND)), Vector((b, ya1 + o, GROUND)), Vector((b, ya1 + o, GROUND + 1.6)), Vector((a, ya0 + o, GROUND + 1.6))], M['c_bank'], [(0, 0), (8, 0), (8, 1), (0, 1)])
    fin(g.obj('ground_river', coll), cast=False)
    # boats on the river (lit cabins)
    bm = MB()
    for k in range(9):
        bx = rnd.uniform(-900, 900); byy = river_y(bx) + rnd.uniform(-RIV_W * 0.7, RIV_W * 0.7); L = rnd.uniform(14, 30)
        bm.box((bx - L / 2, byy - 2.5, GROUND), (bx + L / 2, byy + 2.5, GROUND + 1.4), M['c_boat']); bm.box((bx - L / 4, byy - 1.8, GROUND + 1.4), (bx + L / 4, byy + 1.8, GROUND + 3.0), M['c_cabin'])
    fin(bm.obj('boats', coll), cast=False)
    # elevated expressway along y = 85 with piers, lamp heads and car lights
    xm = MB(); zt = GROUND + 14.0; YA, YB = 76.0, 94.0
    for a, b in zip(range(-2400, 2400, 40), range(-2360, 2440, 40)):
        xm.pid += 1; xm.face([Vector((a, YA, zt)), Vector((b, YA, zt)), Vector((b, YB, zt)), Vector((a, YB, zt))], M['c_deck'], [(0, 0), (1, 0), (1, 0.45), (0, 0.45)])
        for (yy, sgn) in ((YA, -1), (YB, 1)):
            p = [Vector((a, yy, zt - 1.6)), Vector((b, yy, zt - 1.6)), Vector((b, yy, zt + 1.1)), Vector((a, yy, zt + 1.1))]
            xm.pid += 1; xm.face(p if sgn < 0 else p[::-1], M['c_xway'], [(0, 0.48), (1, 0.48), (1, 1), (0, 1)] if sgn < 0 else [(0, 1), (1, 1), (1, 0.48), (0, 0.48)])
        xm.pid += 1; xm.face([Vector((a, YA, zt - 1.6)), Vector((b, YA, zt - 1.6)), Vector((b, YB, zt - 1.6)), Vector((a, YB, zt - 1.6))], M['c_deck'])
        cyl(xm, (a, 85, GROUND), (a, 85, zt - 2.4), 1.4, M['c_pier'], 10); xm.box((a - 1.5, YA + 1, zt - 2.4), (a + 1.5, YB - 1, zt - 1.6), M['c_pier'])
    lm = MB()
    for k in range(260):
        x = rnd.uniform(-2000, 2000); lane = rnd.choice([79.5, 82.5, 87.5, 90.5]); red = lane < 85
        lm.box((x - 2.0, lane - 0.8, zt), (x + 2.0, lane + 0.8, zt + 1.3), M['c_car' + str(k % 3)])
        lm.box((x + (2.0 if not red else -2.05), lane - 0.7, zt + 0.5), (x + (2.05 if not red else -2.0), lane + 0.7, zt + 0.8), M['tail' if red else 'head'])
    for x in range(-2400, 2400, 30):
        for yy in (YA + 0.5, YB - 0.5): lm.box((x - 0.4, yy - 0.4, zt + 7.8), (x + 0.4, yy + 0.4, zt + 8.0), M['streetlamp'])
    fin(xm.obj('expressway', coll), cast=False); fin(lm.obj('xway_lights', coll), cast=False)
    # cars on the streets around our block
    cm = MB()
    for k in range(70):
        if k % 2: x = rnd.uniform(-300, 300); yy = 60 * rnd.randint(-4, 4) + 20 + rnd.choice([2.7, 7.3]); along = 'x'
        else: yy = rnd.uniform(-300, 300); x = 60 * rnd.randint(-4, 4) - 30 + rnd.choice([2.7, 7.3]); along = 'y'
        if 70 < yy < 100: continue
        hl, hw = (2.1, 0.9) if along == 'x' else (0.9, 2.1)
        cm.box((x - hl, yy - hw, GROUND), (x + hl, yy + hw, GROUND + 1.4), M['c_car' + str(k % 3)])
        if along == 'x': cm.box((x + hl, yy - 0.7, GROUND + 0.5), (x + hl + 0.05, yy + 0.7, GROUND + 0.8), M['head']); cm.box((x - hl - 0.05, yy - 0.7, GROUND + 0.5), (x - hl, yy + 0.7, GROUND + 0.8), M['tail'])
        else: cm.box((x - 0.7, yy + hw, GROUND + 0.5), (x + 0.7, yy + hw + 0.05, GROUND + 0.8), M['head']); cm.box((x - 0.7, yy - hw - 0.05, GROUND + 0.5), (x + 0.7, yy - hw, GROUND + 0.8), M['tail'])
    fin(cm.obj('cars', coll), cast=False)
    temples(coll, M, WAT, UBO)
    A.update(river=dict(center_y_at_x0=river_y(0), half_width=RIV_W), expressway=dict(y=(YA, YB), deck_z=zt), wat=(WAT.x, WAT.y, GROUND), ubosot=(UBO.x, UBO.y, GROUND), city_buildings=nb)

def thai_roof(mb, cx, cy, L, W, z0, M, tiers=3, rise=0.75):
    """Ubosot roof: stacked gable tiers along x with chofa finials and naga barge boards."""
    for t in range(tiers):
        l = L * (1 - 0.14 * t); w = W * (1 - 0.18 * t); zb = z0 + t * W * 0.22; zt = zb + w * rise * 0.5; x0, x1 = cx - l / 2, cx + l / 2
        for sgn in (-1, 1):
            mb.pid += 1; mb.face([Vector((x0, cy + sgn * w / 2, zb)), Vector((x1, cy + sgn * w / 2, zb)), Vector((x1, cy, zt)), Vector((x0, cy, zt))][::(1 if sgn < 0 else -1)], M['c_troof'], [(0, 0), (3, 0), (3, 1), (0, 1)] if sgn < 0 else [(0, 1), (3, 1), (3, 0), (0, 0)])
        for xe in (x0, x1):
            mb.pid += 1; mb.face([Vector((xe, cy - w / 2 + 0.6, zb)), Vector((xe, cy + w / 2 - 0.6, zb)), Vector((xe, cy, zt - 0.2))], M['c_gable'])
            for sgn in (-1, 1):   # barge boards curling up into the chofa / bai raka
                obox(mb, (xe, cy + sgn * w / 2, zb), (xe, cy, zt + 0.3), 0.25, 0.18, M['c_gold'], side=(1, 0, 0))
                p = Vector((xe, cy + sgn * w / 2, zb)); obox(mb, p, p + Vector((0, sgn * 0.6, 1.2)), 0.12, 0.12, M['c_gold'])
            tip = Vector((xe, cy, zt + 0.3)); d = 1 if xe > cx else -1
            obox(mb, tip, tip + Vector((d * 0.6, 0, 1.4)), 0.14, 0.14, M['c_gold']); obox(mb, tip + Vector((d * 0.6, 0, 1.4)), tip + Vector((d * 1.3, 0, 1.9)), 0.1, 0.1, M['c_gold'])
            obox(mb, tip + Vector((d * 1.3, 0, 1.9)), tip + Vector((d * 1.2, 0, 2.5)), 0.07, 0.07, M['c_gold'])

def temples(coll, M, WAT, UBO):
    mb = MB()
    # ubosot near our building: hall, three-tier roof with chofa, compound wall, a small chedi, bodhi trees
    cx, cy = UBO.x, UBO.y; L, W = 26, 13
    mb.box((cx - L / 2 - 1, cy - W / 2 - 1, GROUND), (cx + L / 2 + 1, cy + W / 2 + 1, GROUND + 1.2), M['c_twall'])
    mb.box((cx - L / 2, cy - W / 2, GROUND + 1.2), (cx + L / 2, cy + W / 2, GROUND + 7.5), M['c_twall'])
    thai_roof(mb, cx, cy, L + 4, W + 3, GROUND + 7.3, M)
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box((cx + sx * 17 - 0.4, cy + sy * 12 - 0.4, GROUND), (cx + sx * 17 + 0.4, cy + sy * 12 + 0.4, GROUND + 2.2), M['c_twall'])
    for (a, b) in (((-17, -12), (17, -12.4)), ((-17, 12), (17, 12.4)), ((-17.4, -12), (-17, 12)), ((17, -12), (17.4, 12))):
        mb.box((cx + a[0], cy + a[1], GROUND), (cx + b[0], cy + b[1], GROUND + 1.6), M['c_twall'])
    ch = Vector((cx - 12, cy + 7, GROUND))
    cyl(mb, ch, ch + Vector((0, 0, 3)), 3.2, M['c_twall'], 16); cyl(mb, ch + Vector((0, 0, 3)), ch + Vector((0, 0, 7)), 2.6, M['c_twall'], 16, r1=1.0); cyl(mb, ch + Vector((0, 0, 7)), ch + Vector((0, 0, 13)), 1.0, M['c_gold'], 12, r1=0.05)
    # Wat Arun-like prang by the river: terraces, the corn-cob tower, four satellite prangs
    def prang(c, s):
        z = GROUND
        for k, (w, h) in enumerate(((22, 4), (18, 5), (14, 5), (10, 4))):
            mb.box((c.x - w * s, c.y - w * s, z), (c.x + w * s, c.y + w * s, z + h * s), M['c_prang']); z += h * s
        rr = 7.5 * s
        for k in range(9):
            h = 4.2 * s; cyl(mb, (c.x, c.y, z), (c.x, c.y, z + h), rr, M['c_prang'], 16, r1=rr * 0.86); cyl(mb, (c.x, c.y, z + h), (c.x, c.y, z + h + 0.8 * s), rr * 0.92, M['c_prang'], 16, r1=rr * 0.8); z += h + 0.8 * s; rr *= 0.86
        cyl(mb, (c.x, c.y, z), (c.x, c.y, z + 12 * s), rr, M['c_gold'], 10, r1=0.15)
        return z
    top = prang(WAT, 1.0)
    for sx in (-1, 1):
        for sy in (-1, 1): prang(WAT + Vector((sx * 27, sy * 27)), 0.45)
    fin(mb.obj('temples', coll), cast=False)
    tm = MB()
    for k in range(10):
        a = k * 0.63; p = Vector((cx + 22 * math.cos(a), cy + 16 * math.sin(a), GROUND + 6)); tm.sphere(tuple(p), 4.5, M['c_tree'], 10, 6)
    fin(tm.obj('temple_trees', coll), cast=False)
    A.update(prang_top=(WAT.x, WAT.y, top))

# ----------------------------------------------------------------------------- sky and the bolt
def world_sky(scene, T, P):
    """Camera-only storm sky: equirect cloud bank near the horizon + an undistorted cloud base overhead (gnomonic x/z, y/z) above ~35 deg."""
    w = bpy.data.worlds.new('storm'); scene.world = w; w.use_nodes = True; nt = w.node_tree; L = nt.links.new
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground'); env = nt.nodes.new('ShaderNodeTexEnvironment')
    env.image = S._img(T['sky']); lp = nt.nodes.new('ShaderNodeLightPath'); mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    tc = nt.nodes.new('ShaderNodeTexCoord'); nrm = nt.nodes.new('ShaderNodeVectorMath'); nrm.operation = 'NORMALIZE'; L(tc.outputs['Generated'], nrm.inputs[0])
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); L(nrm.outputs[0], sep.inputs[0])
    def math_(op, a, b=None, c=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L(v, n.inputs[i])
        return n.outputs[0]
    zc = math_('MAXIMUM', sep.outputs['Z'], 0.05)
    u = math_('MULTIPLY_ADD', math_('DIVIDE', sep.outputs['X'], zc), 0.2, 0.5); v = math_('MULTIPLY_ADD', math_('DIVIDE', sep.outputs['Y'], zc), 0.2, 0.5)
    cmb = nt.nodes.new('ShaderNodeCombineXYZ'); L(u, cmb.inputs[0]); L(v, cmb.inputs[1])
    top = nt.nodes.new('ShaderNodeTexImage'); top.image = S._img(T['sky_top']); top.extension = 'EXTEND'; L(cmb.outputs[0], top.inputs[0])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.52; mr.inputs['From Max'].default_value = 0.80; L(sep.outputs['Z'], mr.inputs['Value'])
    sm = nt.nodes.new('ShaderNodeMix'); sm.data_type = 'RGBA'; L(mr.outputs[0], sm.inputs[0]); L(env.outputs['Color'], sm.inputs[6]); L(top.outputs['Color'], sm.inputs[7])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[0].default_value = min(0.12, 0.12 * (P['sky'] - 1.0)); L(sm.outputs[2], mix.inputs[6]); mix.inputs[7].default_value = (*_lin('#c8d0ff'), 1)
    L(mix.outputs[2], bg.inputs['Color']); L(lp.outputs['Is Camera Ray'], mul.inputs[0]); mul.inputs[1].default_value = P['sky']
    L(mul.outputs[0], bg.inputs['Strength']); L(bg.outputs[0], out.inputs[0])
    w.light_settings.distance = 0.001

def bolt(coll, M, start, end, seed=5):
    r = random.Random(seed); mb = MB(); hm = MB()
    def path(a, b, n, jag):
        pts = [a]; d = b - a; Ln = d.length; side = d.cross(Vector((0, 0, 1))).normalized(); up = side.cross(d).normalized()
        for i in range(1, n):
            t = i / n; q = a.lerp(b, t) + (side * r.uniform(-1, 1) + up * r.uniform(-1, 1)) * jag * Ln / n * (1 - t * 0.6)
            pts.append(q)
        pts.append(b); return pts
    main = path(Vector(start), Vector(end), 44, 1.25)
    for i, (a, b) in enumerate(zip(main[:-1], main[1:])):
        t = i / len(main); rr = 0.32 * (1 - t) ** 1.5 + 0.045
        cyl(mb, a, b, rr, M['bolt'], 6); cyl(hm, a, b, rr * 4.0 + 0.1, M['bolt_halo'], 8, cap0=False, cap1=False)
    for k in range(5):   # branches
        i = r.randint(4, 30); a = main[i]; d = (main[i + 1] - main[i]).normalized()
        b = a + (d + Vector((r.uniform(-0.8, 0.8), r.uniform(-0.8, 0.8), -0.2))).normalized() * r.uniform(8, 22)
        br = path(a, b, 8, 1.2)
        for j, (p, q) in enumerate(zip(br[:-1], br[1:])): cyl(mb, p, q, 0.12 * (1 - j / 9) + 0.02, M['bolt'], 5); cyl(hm, p, q, 0.4, M['bolt_halo'], 6, cap0=False, cap1=False)
    hm.sphere(tuple(Vector(end)), 0.45, M['bolt_halo'], 12, 8); mb.sphere(tuple(Vector(end)), 0.12, M['bolt'], 8, 6)
    o1 = fin(mb.obj('lightning_bolt', coll), cast=False); o2 = fin(hm.obj('lightning_bolt_halo', coll), cast=False); o2.parent = o1
    return o1

LOW_TRUSS = dict(loc=(4.9, -3.4, 0.45), look_at=(3.6, 2.4, 9.6), lens=17)

def _bolt_start(cam, sx, sy, dist, aspect=(720, 1280)):
    """World point on the camera ray through normalised screen (sx, sy) in [-1, 1] (portrait, sensor fit on height), `dist` away."""
    loc = Vector(cam['loc']); f = (Vector(cam['look_at']) - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    tv = 18.0 / cam['lens']; th = tv * aspect[0] / aspect[1]
    return loc + (f + r * sx * th + u * sy * tv).normalized() * dist

RAIN_PERIOD = 8.0     # the rain volume tiles in z every RAIN_PERIOD m: move 'rain' down by v*dt and wrap modulo RAIN_PERIOD to animate

def rain(coll, M, n=6500, seed=21, keep_clear=()):
    """Static rain streaks (camera-only, additive) in a box around the roof; one object, hide it or animate its z (see RAIN_PERIOD)."""
    r = random.Random(seed); mb = MB(); wind = Vector((-0.2, 0.06, -1.0)).normalized(); L = 1.1; w = 0.008
    for i in range(n):
        near = i < n * 0.6
        if near: c = Vector((r.uniform(-22, 22), r.uniform(-18, 18), r.uniform(-4, 30)))
        else: c = Vector((r.uniform(-70, 70), r.uniform(-70, 70), r.uniform(-24, 45)))
        if any((c - Vector(k)).length < 4.5 for k in keep_clear): continue
        a = c - wind * L / 2; b = c + wind * L / 2; yaw = r.uniform(0, math.pi)
        sv = Vector((math.cos(yaw), math.sin(yaw), 0)) * w * 1.4
        mb.pid += 1; mb.face([a - sv, a + sv, b + sv, b - sv], M['rain'])
    ob = fin(mb.obj('rain', coll), cast=False); return ob

def set_bolt(show=True):
    for nm in ('lightning_bolt', 'lightning_bolt_halo'):
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = not show; ob.hide_viewport = not show

# ----------------------------------------------------------------------------- build
def build(preset='storm', flash=0.0, clear=True, city_on=True, rain_on=True):
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    P = dict(PRESETS[preset]); f = max(0.0, min(1.0, float(flash)))
    if f > 0:
        for k in ('shade', 'key'): P[k] = _lerp(P[k], FLASH[k], f)
        P['key_dir'] = tuple(Vector(_lerp(Vector(P['key_dir']).normalized(), Vector(FLASH['key_dir']).normalized(), f)).normalized())
        P['sky'] = P['sky'] + (FLASH['sky'] - P['sky']) * f
        P['haze'] = '#%02x%02x%02x' % tuple(int(round(a + (b - a) * f)) for a, b in zip(bytes.fromhex(P['haze'][1:]), bytes.fromhex(FLASH['haze'][1:])))
    S.STATE.clear(); S.STATE['P'] = P; A.clear()
    T = tex_roof.build_all()
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    warm = (1.0, 0.85, 0.65)
    M = dict(
        floor=lit('floor', T['floor'], gain=0.95, shade=(1.0, 1.05, 1.1)), parapet=lit('parapet', T['parapet'], gain=0.9), cap=lit('cap', T['plinth'], gain=0.95, shade=1.1),
        ledge=lit('ledge', T['plinth'], gain=0.85), plinth=lit('plinth', T['plinth'], gain=0.9),
        facade=lit_glow('facade', T['main'], T['main_g'], gain=0.85, shade=(1.1, 1.05, 1.0), strength=1.5), facade_s=lit_glow('facade_s', T['side'], T['side_g'], gain=0.85, strength=1.5),
        steel=lit('steel', T['steel'], gain=0.95, shade=1.05), steel_y=lit('steel_y', T['steel_y'], gain=0.9), grating=lit('grating', T['grating'], gain=0.95, alpha=True), tread=lit('tread', T['tread'], gain=0.9),
        gusset=lit('gusset', T['steel'], gain=1.0), weldbead=lit('weldbead', color='#3a3436', gain=0.8),
        board=lit_glow('board', T['board'], T['pool'], gain=0.82, shade=(1.25, 1.1, 1.0), strength=0.55, tint=(1.0, 0.92, 0.78)), pback=lit('pback', T['pback'], gain=0.9),
        hut=lit('hut', T['hut'], gain=0.85, shade=(1.15, 1.05, 1.0)), door=lit('door', T['door'], gain=0.85), jbox=lit('jbox', color='#9a9c9e', gain=0.85),
        sign_rain=lit('sign_rain', T['sign_rain'], gain=0.75), sign_hv=lit('sign_hv', T['sign_hv'], gain=0.75),
        tank=lit('tank', T['tank'], gain=0.85), tank_top=lit('tank_top', color='#b8bcc4', gain=0.85), tank_band=lit('tank_band', color='#8a8e98', gain=0.85),
        ac=lit('ac', T['ac'], gain=0.85), ac2=lit('ac2', T['ac2'], gain=0.85), acbox=lit('acbox', color='#cfcdc4', gain=0.85), tarp=lit('tarp', T['tarp'], gain=0.85, shade=(1.0, 1.0, 1.15)),
        o2=lit('o2', T['o2'], gain=0.9), c2h2=lit('c2h2', T['c2h2'], gain=0.9), o2_t=lit('o2_t', color='#e8e4dc', gain=0.85), c2h2_t=lit('c2h2_t', color='#d8d0c0', gain=0.85),
        machine=lit('machine', T['machine'], gain=0.85), machine_b=lit('machine_b', color='#e0b020', gain=0.85), toolbox=lit('toolbox', T['toolbox'], gain=0.85), toolbox_b=lit('toolbox_b', color='#c8241e', gain=0.85),
        cl1=lit('cl1', T['cl1'], gain=0.85), cl2=lit('cl2', T['cl2'], gain=0.85), cl3=lit('cl3', T['cl3'], gain=0.85), cl4=lit('cl4', T['cl4'], gain=0.85),
        oldsign=lit('oldsign', T['neon2'], gain=0.6), vsign=lit_glow('vsign', T['neon1'], T['neon1_g'], gain=0.6, strength=0.8),
        rail=lit('rail', color='#a8acb4', gain=0.9), dark=lit('dark', color='#2a2a30', gain=0.7), pvc=lit('pvc', color='#2a5ab8', gain=0.85), pvc_g=lit('pvc_g', color='#8a8c90', gain=0.85),
        cable=lit('cable', color='#1e1e24', gain=0.7), cable_g=lit('cable_g', color='#5a5a60', gain=0.8), copper=lit('copper', color='#c87a40', gain=0.85),
        hose_r=lit('hose_r', color='#c8241e', gain=0.85), hose_g=lit('hose_g', color='#2a8a3a', gain=0.85), brass=lit('brass', color='#c8a040', gain=0.9), gauge=lit('gauge', color='#e8e8e0', gain=0.9),
        chain=lit('chain', color='#6a6a70', gain=0.8), lamp_body=lit('lamp_body', color='#5a5e66', gain=0.85), lamp_off=lit('lamp_off', color='#3a3e4a', gain=0.9),
        red=lit('red', color='#d42a1e', gain=0.9), blue=lit('blue', color='#2a6ad0', gain=0.9), orange=lit('orange', color='#f07a1e', gain=0.9), green=lit('green', color='#3aa050', gain=0.9),
        grey=lit('grey', color='#8a8a8a', gain=0.9), water=lit('water_b', color='#3a3e58', gain=0.6), tyre=lit('tyre', color='#222226', gain=0.7), foam=lit('foam', color='#e8e8e0', gain=0.85),
        leaf=lit('leaf', color='#4a8a3a', gain=0.85), twig=lit('twig', color='#6a4a2a', gain=0.8), brick=lit('brick', color='#b05a3a', gain=0.85), wood=lit('wood', color='#8a5a34', gain=0.8),
        dish=lit('dish', color='#d8d8d0', gain=0.9), dish_o=lit('dish_o', color='#e87a1e', gain=0.9),
        lamp_on=emit('lamp_on', '#fff0c8', 5.0), bulb=emit('bulb', '#ffcf80', 7.0), beam=additive('beam', '#fff0d0', 0.028),
        pool_warm=additive('pool_w', '#ffb868', 0.45, T['glow']), pool_warm_f=additive('pool_wf', '#ffb868', 0.32, T['glow']),
        bolt=emit('bolt', '#f2f4ff', 40.0), rain=additive('rain', '#aab2ee', 0.32), bolt_halo=additive('bolt_halo', '#8a9cff', 0.55),
        head=emit('head', '#fff4d8', 4.0), tail=emit('tail', '#ff3a2a', 3.0), streetlamp=emit('streetlamp', '#ffc070', 4.0),
    )
    M.update(
        c_shop1=mat_city('shop1', T['shop1'], glow=T['shop1_g'], gstr=1.3), c_shop2=mat_city('shop2', T['shop2'], glow=T['shop2_g'], gstr=1.3), c_flat=mat_city('flat', T['flat'], glow=T['flat_g'], gstr=1.3),
        c_office=mat_city('office', T['office'], glow=T['office_g'], gstr=0.6, gain=0.55), c_condo=mat_city('condo', T['condo'], glow=T['condo_g'], gstr=0.8, gain=0.65), c_old=mat_city('old', T['old'], glow=T['old_g'], gstr=1.3),
        c_roof=mat_city('roof', T['croof'], gain=0.9), c_tree=mat_city('tree', color='#3a6a3a', gain=0.8), c_tank=mat_city('tank', color='#b8bcc4'), c_ac=mat_city('ac', color='#c8c6be'),
        c_ground=mat_city('ground', T['ground'], glow=T['ground_g'], gstr=1.6), c_river=mat_city('river', T['river'], glow=T['river_g'], gstr=1.4, gain=0.5), c_bank=mat_city('bank', color='#8a867e'),
        c_boat=mat_city('boat', color='#5a3a2a'), c_cabin=mat_city('cabin', color='#e8d8a0'),
        c_deck=mat_city('deck', color='#7e7a74'), c_xway=mat_city('xway', T['xway'], glow=T['xway_g'], gstr=1.6), c_pier=mat_city('pier', color='#9a968e'),
        c_car0=mat_city('car0', color='#d8d8d0'), c_car1=mat_city('car1', color='#c8241e'), c_car2=mat_city('car2', color='#2a3a5a'),
        c_twall=mat_city('twall', T['twall'], gain=1.0), c_troof=mat_city('troof', T['troof'], gain=1.0), c_gable=mat_city('gable', color='#d8a830', gain=1.0), c_gold=mat_city('gold', color='#e8b830', gain=1.1),
        c_prang=mat_city('prang', T['prang'], gain=1.0, shade=1.3),
        neon1=emit('neon1', '#ffffff', 1.0), neon2=emit('neon2', '#ffffff', 1.0), neon3=emit('neon3', '#ffffff', 1.0), neon4=emit('neon4', '#ffffff', 1.0),
    )
    for k in ('neon1', 'neon2', 'neon3', 'neon4'):
        m = bpy.data.materials.new('R_neon_' + k); nt = S._tree(m); L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
        tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = S._img(T[k]); gt = nt.nodes.new('ShaderNodeTexImage'); gt.image = S._img(T[k + '_g'])
        ad = nt.nodes.new('ShaderNodeVectorMath'); ad.operation = 'MULTIPLY_ADD'; L(gt.outputs['Color'], ad.inputs[0]); ad.inputs[1].default_value = (2.5, 2.5, 2.5); L(tx.outputs['Color'], ad.inputs[2])
        sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'SCALE'; sc.inputs['Scale'].default_value = 0.35; L(tx.outputs['Color'], sc.inputs[0])
        ad2 = nt.nodes.new('ShaderNodeVectorMath'); ad2.operation = 'MULTIPLY_ADD'; L(gt.outputs['Color'], ad2.inputs[0]); ad2.inputs[1].default_value = (2.5, 2.5, 2.5); L(sc.outputs[0], ad2.inputs[2])
        L(ad2.outputs[0], em.inputs['Color']); L(em.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; M[k] = m
    building(coll, M, T); billboard(coll, M, T); stair_hut(coll, M); clutter(coll, M)
    if city_on: city(coll, M)
    if rain_on: rain(coll, M, keep_clear=[LOW_TRUSS['loc'], (9.6, -0.5, 8.75), (6.3, 0.9, 16.4)])
    bstart = _bolt_start(LOW_TRUSS, sx=0.98, sy=1.08, dist=120.0); bo = bolt(coll, M, bstart, WELD); set_bolt(f > 0)
    # key light: the one hard sun (cold cloud light from screen-right / +x)
    sd = bpy.data.lights.new('key_sun', 'SUN'); mk = max(P['key']); sd.energy = math.pi * mk; sd.color = tuple(c / mk for c in P['key']); sd.angle = math.radians(P['sun_angle'])
    sd.use_shadow = True; so = bpy.data.objects.new('key_sun', sd); lc.objects.link(so)
    so.rotation_euler = Vector(P['key_dir']).normalized().to_track_quat('-Z', 'Y').to_euler()
    world_sky(scene, T, P); S.setup_render(scene, 'fast'); scene.render.use_persistent_data = False; scene.cycles.transparent_max_bounces = 6; S.setup_grade(scene, bloom=True)
    cams = dict(
        est_aerial=dict(loc=(-24.0, -47.0, 31.0), look_at=(3.0, 30.0, 7.0), lens=22),
        low_truss=dict(LOW_TRUSS),
        eye_weld=dict(loc=(9.6, -0.5, 8.75), look_at=(5.0, 2.0, 8.5), lens=24),
        high_down=dict(loc=(6.3, 0.9, 16.4), look_at=(4.2, -1.5, 5.0), lens=18),
    )
    cams['flash_low'] = dict(cams['low_truss'])
    cams['est_aerial_169'] = dict(loc=(-24.0, -47.0, 31.0), look_at=(3.0, 30.0, 15.0), lens=20)
    A.update(preset=preset, flash=f, ground_z=GROUND, roof=dict(x0=-12.78, x1=12.78, y0=-9.78, y1=9.78, z=0.0, parapet_h=1.0, rail_top=1.7),
             weld_mark=(5.0, 1.65, CW_Z), weld_point=tuple(WELD), weld_face_dir=(0.0, 1.0, 0.0), bolt_obj='lightning_bolt', bolt_halo_obj='lightning_bolt_halo', rain_obj='rain', rain_period=RAIN_PERIOD, bolt_start=tuple(bstart),
             key_dir=tuple(Vector(P['key_dir']).normalized()), key_screen_note='key from +x (screen-right in low_truss / est_aerial), shadows fall to -x and slightly +y',
             cams=cams, render=dict(samples=scene.cycles.samples, resolution=(720, 1280), shade=P['shade'], key=P['key'], sun_angle=P['sun_angle']))
    S.STATE['A'] = A
    return json.loads(json.dumps(A, default=list))

def make_cam(c, w=720, h=1280):
    scene = bpy.context.scene; ob = S.make_camera(c, name='cam'); ob.data.clip_end = 9000.0; ob.data.clip_start = 0.05
    scene.render.resolution_x = w; scene.render.resolution_y = h
    return ob

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'; q = sys.argv[2] if len(sys.argv) > 2 else 'final'
    only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    out = os.path.join(HERE, 'out_roof'); os.makedirs(out, exist_ok=True); timing = {}
    tp = os.path.join(out, 'timing.json')
    if os.path.exists(tp): timing = json.load(open(tp))
    def go(name, cam, w=720, h=1280):
        scene = bpy.context.scene; make_cam(cam, w, h)
        if q == 'preview': scene.render.resolution_percentage = 50; scene.cycles.samples = 8
        t, c = S.render(os.path.join(out, name + '.png')); timing[name] = dict(wall_s=round(t, 2), cpu_s=round(c, 2), load=os.getloadavg()[0], samples=scene.cycles.samples, res=(w, h))
        print(name, round(t, 2), 's', flush=True)
    t0 = time.time(); A_ = build('storm', 0.0); print('build', round(time.time() - t0, 1), 's', flush=True)
    for nm in ('est_aerial', 'low_truss', 'eye_weld', 'high_down'):
        if only is None or nm in only: go(nm, A_['cams'][nm])
    if only is None or 'est_aerial_169' in only: go('est_aerial_169', A_['cams']['est_aerial_169'], 1920, 1080)
    if only is None or 'flash_low' in only:
        A2 = build('storm', 1.0); go('flash_low', A2['cams']['flash_low'])
    json.dump(timing, open(tp, 'w'), indent=1)
    anc = {k: v for k, v in A_.items()}
    json.dump(anc, open(os.path.join(out, 'anchors.json'), 'w'), indent=1, default=str)
