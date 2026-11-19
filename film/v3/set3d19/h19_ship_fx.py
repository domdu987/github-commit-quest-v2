"""h19_ship_fx.py : bow wave sheet (curling roll, lacy foam), spray, cumulus clouds, gulls, headland, far sail, rocks, rain, fog (metres, ship frame).
Grown from styleboard part_ship6.py (approved v6)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h19_kit as K
from h19_kit import mat, mat_emit, MB, hexc, rnd
import h19_ship_hull as HU
from h19_ship_hull import ss, vnoise2, fbm2, w_wl, YS, YB
import h19_ship_sea as SE
MATS = K.MATS
def loc2w(p): return Vector(p)
def swell_h(x, y): return float(SE.swell_h(x, y))
def catmull(Pc, n):
    Pc = np.asarray(Pc, dtype=np.float64); Pp = np.vstack([Pc[0] * 2 - Pc[1], Pc, Pc[-1] * 2 - Pc[-2]]); m = len(Pp) - 3; out = []
    for k in range(n):
        u = k / (n - 1) * m; i = min(int(u), m - 1); f = u - i; p0, p1, p2, p3 = Pp[i:i + 4]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f ** 3))
    return np.array(out)

def foam_sheet_mat(name, lacy=1.0, alpha_k=0.97):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeAttribute'); sp.attribute_type = 'GEOMETRY'; sp.attribute_name = 'sp'
    hz = N('ShaderNodeAttribute'); hz.attribute_type = 'GEOMETRY'; hz.attribute_name = 'hz'
    ln = N('ShaderNodeAttribute'); ln.attribute_type = 'GEOMETRY'; ln.attribute_name = 'lp'
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 7.0; nz.inputs['Roughness'].default_value = 0.62; L(tc.outputs['Object'], nz.inputs['Vector'])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 7.0; nz2.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz2.inputs['Vector'])
    # lacy outer edge: s + (noise-.5)*k - c  -> 0..1
    a1 = N('ShaderNodeMath'); a1.operation = 'SUBTRACT'; a1.inputs[1].default_value = 0.5; L(nz.outputs['Fac'], a1.inputs[0])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; a2.inputs[1].default_value = 1.15 * lacy; L(a1.outputs[0], a2.inputs[0])
    a3 = N('ShaderNodeMath'); a3.operation = 'ADD'; L(sp.outputs['Fac'], a3.inputs[0]); L(a2.outputs[0], a3.inputs[1])
    a4 = N('ShaderNodeMath'); a4.operation = 'SUBTRACT'; a4.inputs[1].default_value = -0.5; L(a3.outputs[0], a4.inputs[0])
    am = N('ShaderNodeMapRange'); am.inputs['From Min'].default_value = 0.0; am.inputs['From Max'].default_value = 0.16; L(a4.outputs[0], am.inputs['Value'])
    # fine speckle holes in the thin parts
    sk = N('ShaderNodeMapRange'); sk.inputs['From Min'].default_value = 0.30; sk.inputs['From Max'].default_value = 0.46; L(nz2.outputs['Fac'], sk.inputs['Value'])
    sk2 = N('ShaderNodeMath'); sk2.operation = 'MAXIMUM'; sk2.inputs[0].default_value = 1.0; sk2.inputs[1].default_value = 1.0
    # lip end / tail fade
    le = N('ShaderNodeMath'); le.operation = 'SUBTRACT'; le.inputs[0].default_value = 1.0; L(sp.outputs['Fac'], le.inputs[1])
    le1 = N('ShaderNodeMath'); le1.operation = 'ADD'; L(le.outputs[0], le1.inputs[0]); L(a2.outputs[0], le1.inputs[1])
    f1 = N('ShaderNodeMath'); f1.operation = 'SUBTRACT'; f1.inputs[1].default_value = 0.5; L(nz2.outputs['Fac'], f1.inputs[0]); f2 = N('ShaderNodeMath'); f2.operation = 'MULTIPLY'; f2.inputs[1].default_value = 0.9; L(f1.outputs[0], f2.inputs[0]); le1b = N('ShaderNodeMath'); le1b.operation = 'ADD'; L(le1.outputs[0], le1b.inputs[0]); L(f2.outputs[0], le1b.inputs[1]); le1 = le1b
    le2 = N('ShaderNodeMapRange'); le2.inputs['From Min'].default_value = 0.0; le2.inputs['From Max'].default_value = 0.30; L(le1.outputs[0], le2.inputs['Value'])
    tf = N('ShaderNodeMapRange'); tf.inputs['From Min'].default_value = 1.0; tf.inputs['From Max'].default_value = 0.82; L(ln.outputs['Fac'], tf.inputs['Value'])
    al = N('ShaderNodeMath'); al.operation = 'MULTIPLY'; L(am.outputs['Result'], al.inputs[0]); L(le2.outputs['Result'], al.inputs[1])
    al2 = N('ShaderNodeMath'); al2.operation = 'MULTIPLY'; L(al.outputs[0], al2.inputs[0]); L(tf.outputs['Result'], al2.inputs[1])
    al3 = N('ShaderNodeMath'); al3.operation = 'MULTIPLY'; L(al2.outputs[0], al3.inputs[0]); L(sk2.outputs[0], al3.inputs[1])
    hb = N('ShaderNodeMath'); hb.operation = 'ADD'; L(hz.outputs['Fac'], hb.inputs[0]); L(a2.outputs[0], hb.inputs[1])
    hm = N('ShaderNodeMapRange'); hm.inputs['From Min'].default_value = -0.6; hm.inputs['From Max'].default_value = -0.3; L(hb.outputs[0], hm.inputs['Value'])
    al3b = N('ShaderNodeMath'); al3b.operation = 'MULTIPLY'; L(al3.outputs[0], al3b.inputs[0]); L(hm.outputs['Result'], al3b.inputs[1])
    hq = N('ShaderNodeMapRange'); hq.inputs['From Min'].default_value = 0.25; hq.inputs['From Max'].default_value = 0.75; hq.inputs['To Min'].default_value = 0.62; hq.inputs['To Max'].default_value = 1.0; L(hz.outputs['Fac'], hq.inputs['Value'])
    al3c = N('ShaderNodeMath'); al3c.operation = 'MULTIPLY'; L(al3b.outputs[0], al3c.inputs[0]); L(hq.outputs['Result'], al3c.inputs[1])
    al4 = N('ShaderNodeMath'); al4.operation = 'MULTIPLY'; al4.inputs[1].default_value = alpha_k; al4.use_clamp = True; L(al3c.outputs[0], al4.inputs[0])
    # colour: white top, aqua toward the water; underside turquoise
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.inputs[6].default_value = hexc('#86c4be'); cm.inputs[7].default_value = hexc('#d6e0de'); cmr = N('ShaderNodeMapRange'); cmr.inputs['From Min'].default_value = 0.10; cmr.inputs['From Max'].default_value = 0.52; L(hz.outputs['Fac'], cmr.inputs['Value']); L(cmr.outputs['Result'], cm.inputs[0])
    b1 = N('ShaderNodeMath'); b1.operation = 'MULTIPLY'; b1.inputs[1].default_value = 11.0; L(hz.outputs['Fac'], b1.inputs[0])
    b2 = N('ShaderNodeMath'); b2.operation = 'MULTIPLY'; b2.inputs[1].default_value = 3.2; L(nz.outputs['Fac'], b2.inputs[0])
    b3 = N('ShaderNodeMath'); b3.operation = 'ADD'; L(b1.outputs[0], b3.inputs[0]); L(b2.outputs[0], b3.inputs[1])
    b4 = N('ShaderNodeMath'); b4.operation = 'SINE'; b4.inputs[1].default_value = 0.0; b3m = N('ShaderNodeMath'); b3m.operation = 'MULTIPLY'; b3m.inputs[1].default_value = 3.14159; L(b3.outputs[0], b3m.inputs[0]); L(b3m.outputs[0], b4.inputs[0])
    b5 = N('ShaderNodeMapRange'); b5.inputs['From Min'].default_value = 0.1; b5.inputs['From Max'].default_value = 1.0; b5.inputs['To Max'].default_value = 0.7; L(b4.outputs[0], b5.inputs['Value'])
    bt = N('ShaderNodeMix'); bt.data_type = 'RGBA'; bt.inputs[7].default_value = hexc('#8cccc6'); L(cm.outputs[2], bt.inputs[6]); L(b5.outputs['Result'], bt.inputs[0])
    cb = N('ShaderNodeMix'); cb.data_type = 'RGBA'; cb.inputs[7].default_value = hexc('#6fd8cc'); L(bt.outputs[2], cb.inputs[6]); L(geo.outputs['Backfacing'], cb.inputs[0])
    es = N('ShaderNodeMath'); es.operation = 'MULTIPLY_ADD'; es.inputs[1].default_value = 0.9; es.inputs[2].default_value = 0.03; L(geo.outputs['Backfacing'], es.inputs[0])
    bs.inputs['Roughness'].default_value = 0.55; bs.inputs['Specular IOR Level'].default_value = 0.2
    L(cb.outputs[2], bs.inputs['Base Color']); L(cb.outputs[2], bs.inputs['Emission Color']); L(es.outputs[0], bs.inputs['Emission Strength'])
    L(al4.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(bs.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); return m

SHEET_H = 1.2
def bow_wave6(P, parent=None):
    rr = np.random.RandomState(11)
    ts = np.linspace(0.58, 1.0, 100); xs = w_wl(ts); ys = YS + ts * (YB - YS)
    port = np.stack([-xs, ys], 1); d = np.diff(port, axis=0); d = np.vstack([d, d[-1]]); d /= np.linalg.norm(d, axis=1, keepdims=True); npt = np.stack([-d[:, 1], d[:, 0]], 1)
    stb = np.stack([xs[::-1], ys[::-1]], 1); d2 = np.diff(stb, axis=0); d2 = np.vstack([d2, d2[-1]]); d2 /= np.linalg.norm(d2, axis=1, keepdims=True); nst = np.stack([-d2[:, 1], d2[:, 0]], 1)
    seg = np.linalg.norm(np.diff(port, axis=0), axis=1); lp = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])      # arclength from the tip, negative on the port side
    a0 = math.atan2(npt[-1, 1], npt[-1, 0]); a1 = math.atan2(nst[0, 1], nst[0, 0])
    fan = [(YB * 0 + 0.0, YB) for _ in range(14)]; fan_n = [(math.cos(a0 + (a1 - a0) * k / 13.0), math.sin(a0 + (a1 - a0) * k / 13.0)) for k in range(14)]
    Pp = np.vstack([port, np.array(fan), stb]); Nn = np.vstack([npt, np.array(fan_n), nst]); Ll = np.concatenate([lp, np.linspace(-0.2, 0.2, 14), -lp[::-1]])
    prof = [(-1.0, 0.25), (-0.7, 0.8), (-0.35, 1.4), (0.05, 1.9), (0.5, 2.2), (0.95, 2.2), (1.35, 1.95), (1.62, 1.55), (1.74, 1.1), (1.8, 0.72), (1.98, 0.36), (2.4, 0.08), (2.95, -0.1)]
    nK = 26; pr = catmull(prof, nK); sp_ = np.linspace(0, 1, nK)
    verts = []; sp = []; hz = []; lp_ = []
    al = np.abs(Ll)
    E = np.exp(-(np.maximum(al - 3.0, 0) / 6.4) ** 2) * (0.72 + 0.28 * ss(0.0, 2.5, al))
    nzh = 1 + 0.24 * (vnoise2(Ll * 0.4 + 40, np.zeros_like(Ll) + 3.0, 5) - 0.5) * 2; nzd = 0.22 * (vnoise2(Ll * 1.3 + 90, np.zeros_like(Ll) + 8.0, 6) - 0.5) * 2
    for j in range(len(Pp)):
        D = 1.9 + 0.10 * al[j] + nzd[j]; Hs = SHEET_H * E[j] * nzh[j]; Wsc = 0.65 + 0.35 * E[j] + 0.25 * ss(6, 14, al[j])
        for k in range(nK):
            dn, zz = pr[k]; pxl = Pp[j, 0] + Nn[j, 0] * (D + dn * Wsc); pyl = Pp[j, 1] + Nn[j, 1] * (D + dn * Wsc)
            wp = loc2w((pxl, pyl, 0)); zb = float(swell_h(wp.x, wp.y)) * 0.92
            verts.append((pxl, pyl, zb + zz * Hs + (0.03 if E[j] < 0.05 else 0.0)))
            sp.append(sp_[k]); hz.append(float(np.clip(zz / 2.25, 0, 1))); lp_.append(float(al[j] / 16.0))
    faces = []; nJ = len(Pp)
    for j in range(nJ - 1):
        for k in range(nK - 1):
            a = j * nK + k; b = (j + 1) * nK + k; c = (j + 1) * nK + k + 1; dd = j * nK + k + 1; faces.append((a, b, c, dd))
    # orientation: the middle of the rising slope must face outward+up
    jm = 20; k = 8; a, b, c, dd = faces[jm * (nK - 1) + k]
    va = Vector(verts[a]); n = (Vector(verts[b]) - va).cross(Vector(verts[dd]) - va); want = Vector((Nn[jm, 0], Nn[jm, 1], 1.0))
    if n.dot(want) < 0: faces = [(f[3], f[2], f[1], f[0]) for f in faces]
    me = bpy.data.meshes.new('wave6'); me.from_pydata(verts, [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    for nm, arr in (('sp', sp), ('hz', hz), ('lp', lp_)):
        at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', np.array(arr, dtype=np.float32))
    ob = bpy.data.objects.new('foam_wave', me); bpy.context.scene.collection.objects.link(ob); me.materials.append(foam_sheet_mat('wave6')); ob.visible_shadow = False; ob.parent = parent
    return Pp, Nn, E, Ll

def spray6(P, M, Pp, Nn, E, Ll):
    rr = random.Random(21); sp = MB('ship6_fleck'); tq = mat_emit('fleck', '#f6fbf8', 1.0)
    for _ in range(130):
        j = rr.randrange(len(Pp)); al = abs(Ll[j]); 
        if E[j] < 0.15: continue
        D = 1.0 + 0.11 * al; r = rr.uniform(0.2, 3.6); hgt = rr.uniform(0.0, 1.0) ** 1.5 * 4.4 * E[j] + 1.4 * E[j]
        px_ = Pp[j, 0] + Nn[j, 0] * (D + r); py_ = Pp[j, 1] + Nn[j, 1] * (D + r)
        wp = loc2w((px_, py_, 0)); zb = float(swell_h(wp.x, wp.y))
        rad = rr.uniform(0.04, 0.11) * (1.0 if hgt < 2.4 else 0.75); sp.ell(tq, (px_, py_, zb + 1.2 + hgt), (rad, rad, rad * 0.9), (6, 4))
    sp.finish(shadow=False)
    # soft mist billboards above the crest, facing the camera
    cam = Vector(P['cam']['loc']); mm = bpy.data.materials.new('mist'); mm.use_nodes = True; nt = mm.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (2, 2, 2); mp.inputs['Location'].default_value = (-1, -1, 0); L(tc.outputs['Generated'], mp.inputs['Vector'])
    gr = N('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'; L(mp.outputs[0], gr.inputs['Vector'])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6; L(gr.outputs['Fac'], pw.inputs[0])
    sc_ = N('ShaderNodeMath'); sc_.operation = 'MULTIPLY'; sc_.inputs[1].default_value = P.get('mist_a', 0.30); L(pw.outputs[0], sc_.inputs[0])
    em.inputs['Color'].default_value = hexc('#f4fafa'); em.inputs['Strength'].default_value = 1.1
    L(sc_.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    rr = random.Random(33)
    for _ in range(26):
        j = rr.randrange(8, len(Pp) - 8)
        if E[j] < 0.25: continue
        D = 1.0 + 0.11 * abs(Ll[j]); p = loc2w((Pp[j, 0] + Nn[j, 0] * (D + rr.uniform(-0.2, 1.4)), Pp[j, 1] + Nn[j, 1] * (D + 0.5), 0)); p.z = float(swell_h(p.x, p.y)) + rr.uniform(1.8, 4.2) * E[j] + 0.6
        tcam = (cam - p).normalized(); rgt = Vector((0, 0, 1)).cross(tcam).normalized(); up = tcam.cross(rgt).normalized(); sz = rr.uniform(1.2, 2.6)
        vs = [p + rgt * (-sz) + up * (-sz * 0.7), p + rgt * sz + up * (-sz * 0.7), p + rgt * sz + up * (sz * 0.7), p + rgt * (-sz) + up * (sz * 0.7)]
        me = bpy.data.meshes.new('mist'); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update(); me.materials.append(mm)
        ob = bpy.data.objects.new('skyobj_mist', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False

# ---- smooth cumulus: metaball union (one smooth surface), flat soft bottom, emission gradient material
def cumulus6(P, name, c, size, seed, nballs=70, squash=0.9):
    rr = random.Random(seed); mbd = bpy.data.metaballs.new(name); mbd.resolution = 0.07; mbd.render_resolution = 0.07; mbd.threshold = 0.55
    balls = []
    nb = int(nballs * 0.35)
    for i in range(nb):                       # wide base row
        x = rr.uniform(-2.6, 2.6); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.0, 0.5), rr.uniform(0.75, 1.1)))
    for i in range(int(nballs * 0.4)):        # body
        x = rr.uniform(-2.0, 2.0); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.6, 1.5), rr.uniform(0.7, 1.05) * (1.1 - abs(x) * 0.12)))
    for i in range(int(nballs * 0.3)):        # towers
        x = rr.uniform(-1.3, 1.5); balls.append((x, rr.uniform(-0.4, 0.4), rr.uniform(1.4, 2.5) * (1.1 - abs(x) * 0.18), rr.uniform(0.5, 0.85)))
    for (x, y, z, r) in balls:
        e = mbd.elements.new(type='BALL'); e.co = (x, y, z); e.radius = r; e.stiffness = 2.2
    ob = bpy.data.objects.new(name, mbd); bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); bpy.data.objects.remove(ob)
    co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    zmin = 0.35; co[:, 2] = np.where(co[:, 2] < zmin, zmin + (co[:, 2] - zmin) * 0.18, co[:, 2]); co[:, 1] *= squash
    me.vertices.foreach_set('co', co.ravel()); me.update()
    for p in me.polygons: p.use_smooth = True
    ob2 = bpy.data.objects.new('clouds_' + name, me); bpy.context.scene.collection.objects.link(ob2); ob2.data.materials.append(cloud_mat(P) if 'cloudG' not in MATS else MATS['cloudG'])
    ob2.location = c; ob2.scale = (size, size, size * 0.85); ob2.visible_shadow = False
    return ob2

def cloud_mat6(P):
    m = bpy.data.materials.new('cloudG'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); gm = N('ShaderNodeNewGeometry')
    kd = Vector(P['key_dir']).normalized(); d1 = N('ShaderNodeVectorMath'); d1.operation = 'DOT_PRODUCT'; d1.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(gm.outputs['Normal'], d1.inputs[0])
    sz = N('ShaderNodeSeparateXYZ'); L(gm.outputs['Normal'], sz.inputs[0])
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY'; a.inputs[1].default_value = 0.55; L(d1.outputs['Value'], a.inputs[0])
    b = N('ShaderNodeMath'); b.operation = 'MULTIPLY_ADD'; b.inputs[1].default_value = 0.45; L(sz.outputs['Z'], b.inputs[0]); L(a.outputs[0], b.inputs[2])
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = hexc(P['cloud'][1]); cr.color_ramp.elements[1].position = 1.0; cr.color_ramp.elements[1].color = hexc(P['cloud'][0])
    e = cr.color_ramp.elements.new(0.42); e.color = hexc('#d4dcf8')
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -0.55; mr.inputs['From Max'].default_value = 0.42; L(b.outputs[0], mr.inputs['Value']); L(mr.outputs['Result'], cr.inputs['Fac'])
    em.inputs['Strength'].default_value = P.get('cloud_k', 1.0); L(cr.outputs[0], em.inputs['Color']); L(em.outputs[0], out.inputs['Surface']); MATS['cloudG'] = m; return m

def clouds6(P):
    cm = cloud_mat6(P)
    for (nm, c, sz, sd) in P['clouds6']: cumulus6(P, nm, c, sz, sd)

def gull6(mb, m, mt, c, yaw, s, flap):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(m, (0, 0, 0), (0.12, 0.42, 0.11), (10, 6)); mb.ell(m, (0, 0.40, 0.03), (0.075, 0.12, 0.07), (8, 5)); mb.ell(m, (0, -0.42, 0.0), (0.06, 0.2, 0.03), (8, 4))
    for sd in (-1, 1):
        pts = [(0.08, 0.15, 0.02), (0.75, 0.22 - 0.12 * flap, 0.12 + 0.34 * flap), (1.45, 0.02 - 0.2 * flap, 0.14 + 0.62 * flap), (1.95, -0.30 - 0.3 * flap, 0.0 + 0.6 * flap)]
        pb = [(0.08, -0.22, 0.0), (0.72, -0.12 - 0.1 * flap, 0.10 + 0.3 * flap), (1.35, -0.38 - 0.2 * flap, 0.1 + 0.55 * flap), (1.95, -0.58 - 0.3 * flap, 0.0 + 0.55 * flap)]
        for i in range(3):
            q = [(sd * pb[i][0], pb[i][1], pb[i][2]), (sd * pb[i + 1][0], pb[i + 1][1], pb[i + 1][2]), (sd * pts[i + 1][0], pts[i + 1][1], pts[i + 1][2]), (sd * pts[i][0], pts[i][1], pts[i][2])]
            mb.quad(mt if i == 2 else m, q); mb.quad(mt if i == 2 else m, q[::-1])
    mb.pop()

