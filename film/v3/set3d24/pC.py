
# ============================================================================= materials
def make_materials():
    tx = S['tx']; M_ = {}
    M_['hull'] = wood('hull', '#976c4d', '#6a4630', 1.1, 'Z', 0.7, waterline=True)
    M_['hull_dk'] = wood('hull_dk', '#7c563c', '#553726', 1.1, 'Z', 0.7, waterline=True)
    M_['hexroof'] = imgmat('hex', 'hex', 1.0, rough=0.62, bumpk=0.9, uv=True)
    M_['walk'] = wood('walk', '#c8a46c', '#8d6a40', 1.8, 'Y', 0.65)
    M_['wood_d'] = wood('wood_d', '#5e3f2a', '#3c271b', 1.5, 'Y', 0.75); M_['wood_l'] = wood('wood_l', '#b88f5c', '#8a6a42', 1.6, 'Y', 0.7)
    M_['plank'] = wood('plank', '#a87c4e', '#6e4c30', 1.4, 'Z', 0.75); M_['deck'] = wood('deck', '#b98d58', '#7a5634', 1.6, 'Y', 0.7)
    M_['iron'] = flat('iron', '#3d4047', 0.34, 0.85); M_['cannon'] = flat('cannon', '#26282c', 0.4, 0.75)
    M_['port_dark'] = flat('port_dark', '#120d0c', 0.95); M_['red'] = flat('red', '#b3262a', 0.38); M_['red_d'] = flat('red_d', '#7e1c1e', 0.42)
    M_['gold'] = flat('gold', '#cb9f48', 0.3, 0.9); M_['teal'] = flat('teal', '#2c8a7a', 0.38); M_['dragon_red'] = flat('dragon_red', '#b8282c', 0.32)
    M_['mouth'] = flat('mouth', '#4d1018', 0.8); M_['tongue'] = flat('tongue', '#c85060', 0.5); M_['tooth'] = flat('tooth', '#f4eddc', 0.3)
    M_['eye_w'] = flat('eye_w', '#f6f2e6', 0.2); M_['eye_k'] = flat('eye_k', '#101010', 0.15); M_['rope'] = flat('rope', '#b79a62', 0.95)
    M_['sail_k'] = imgmat('matting', 'matting', 0.18, rough=0.9, bumpk=0.4); M_['sail_d'] = imgmat('matting_d', 'matting_d', 0.18, rough=0.9, bumpk=0.4)
    M_['cloth_w'] = flat('cloth_w', '#eee6d2', 0.95); M_['cloth_s'] = imgmat('cloth_s', 'flag_white_k', 1.0, uv=True, rough=0.95, bumpk=0.0)
    M_['black_l'] = flat('black_l', '#151316', 0.22); M_['red_l'] = flat('red_l', '#a8201f', 0.28); M_['white_p'] = flat('white_p', '#e9e2d0', 0.8)
    M_['tile'] = imgmat('tile', 'tile', 0.09, rough=0.6, bumpk=0.6); M_['tile_d'] = imgmat('tile_d', 'tile_d', 0.09, rough=0.6, bumpk=0.6)
    M_['stone'] = imgmat('stone', 'stone', 0.12, rough=0.92, bumpk=0.7); M_['stone_d'] = imgmat('stone_d', 'stone_d', 0.12, rough=0.92, bumpk=0.7)
    M_['dancheong'] = imgmat('dancheong', 'dancheong', 0.45, rough=0.55, bumpk=0.1)
    M_['plaster'] = flat('plaster', '#d9ceb4', 0.9); M_['basket'] = imgmat('basket', 'matting_d', 0.5, rough=0.95, bumpk=0.5)
    M_['earth'] = flat('earth', '#8a7456', 0.95); M_['spray'] = flat('spray', '#f3f7f6', 0.9)
    M_['smoke_g'] = smoke_mat('g', '#bdb9ae'); M_['smoke_d'] = smoke_mat('d', '#7e7b78'); M_['smoke_y'] = smoke_mat('y', '#cdc49a')
    M_['flash'] = emit('flash', '#ffcf6a', 40.0); M_['green_p'] = flat('green_p', '#2f6a4a', 0.5); M_['blue_p'] = flat('blue_p', '#2a56a8', 0.5)
    for nm, k in (('wake', 'foam_wake'), ('bow', 'foam_bow'), ('ring', 'foam_ring'), ('surf', 'foam_surf')):
        def f(b, k=k):
            t = b.img(k, 1.0, 'FLAT', vec=b.n('ShaderNodeUVMap').outputs[0], ext='EXTEND'); d = b.n('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.9, 0.95, 0.95, 1)
            em = b.n('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.85, 0.92, 0.92, 1); em.inputs['Strength'].default_value = 0.35; ad = b.n('ShaderNodeAddShader'); b.l(d.outputs[0], ad.inputs[0]); b.l(em.outputs[0], ad.inputs[1])
            tr = b.n('ShaderNodeBsdfTransparent'); mx = b.n('ShaderNodeMixShader'); b.l(t.outputs['Alpha'], mx.inputs[0]); b.l(tr.outputs[0], mx.inputs[1]); b.l(ad.outputs[0], mx.inputs[2]); b.l(mx.outputs[0], b.out.inputs['Surface'])
        M_['foam_' + nm if nm in ('wake', 'bow') else nm + '_f'] = mat('J_foam_' + nm, f)
    M_['foam_wake'] = M_['foam_wake']; M_['foam_bow'] = M_['foam_bow']
    for k in ('red', 'black', 'white_r', 'white_k', 'tri_red', 'tri_black', 'tri_blue', 'tri_yellow'): flagmat('flag_' + k)
    S['M'] = M_; return M_

def water_mat(name, calm=False):
    def f(b):
        c = b.coord(); gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0])
        patch = b.noise(0.035 if not calm else 0.06, 2.0, 0.5, c, None)
        deep, mid, shl = ('#0c5a7a', '#13808a', '#2fae9e') if not calm else ('#0f5058', '#1b6f70', '#2c8c82')
        col = b.mix(b.rng(patch, 0.35, 0.65), hexl(deep), hexl(mid))
        crest = b.rng(z.outputs['Z'], 0.05 if not calm else 9, 0.30, 0, 1); col = b.mix(b.math('MULTIPLY', crest, b.rng(b.noise(0.5, 1.0, 0.5, c), 0.4, 0.7), clamp=True), col, hexl(shl))
        if not calm:
            sp = b.rng(b.noise(0.8, 0.0, 0.5, c), 0.62, 0.72); wc = b.math('MULTIPLY', b.rng(z.outputs['Z'], 0.17, 0.30), sp, clamp=True); col = b.mix(wc, col, (0.93, 0.97, 0.96, 1))
        n1 = b.noise(1.3 if not calm else 0.9, 2.0, 0.5, c); n2 = b.noise(5.0, 1.0, 0.5, c); h = b.math('ADD', n1, b.math('MULTIPLY', n2, 0.35))
        nrm = b.bump(h, 0.32 if not calm else 0.06, 0.08)
        b.princ(col, 0.05 if not calm else 0.03, 0.0, nrm, IOR=1.333)
    return mat('J_' + name, f)

def land_mat(name, sand=False, rock=True, grass='#4f7d3c', rockc='#85796a', sandc='#dcc690'):
    def f(b):
        c = b.coord(); gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0])
        nz = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['True Normal'], nz.inputs[0]); n1 = b.noise(0.4, 4.0, 0.6, c); n2 = b.noise(3.0, 3.0, 0.5, c)
        gcol = b.mix(b.rng(n1, 0.35, 0.65), hexl(grass), hexl('#3a6a30'))
        rcol = b.mix(b.rng(n2, 0.3, 0.7), hexl(rockc), tint(rockc, 0.62) + (1.0,))
        slope = b.rng(nz.outputs['Z'], 0.55, 0.78, 0.0, 1.0) if rock else 1.0
        col = b.mix(slope, rcol, gcol)
        if sand:
            sd = b.rng(z.outputs['Z'], 0.9, 1.5, 1.0, 0.0); col = b.mix(sd, col, hexl(sandc))
        nrm = b.bump(b.math('ADD', n1, n2), 0.5, 0.2); b.princ(col, 0.92, 0.0, nrm)
    return mat('J_' + name, f)

def foliage_mat(name='pine'):
    def f(b):
        oi = b.n('ShaderNodeObjectInfo'); c = b.coord(); n = b.noise(2.0, 2.0, 0.5, c)
        col = b.mix(b.math('ADD', b.math('MULTIPLY', oi.outputs['Random'], 0.6), b.math('MULTIPLY', n, 0.4), clamp=True), hexl('#2a5532'), hexl('#47773e'))
        b.princ(col, 0.85, 0.0, b.bump(n, 0.35, 0.1))
    return mat('J_' + name, f)

# ============================================================================= terrain, pines, islands, mountains
def hfield(x, y, seed=0):
    return (math.sin(0.21 * x + seed) * math.cos(0.17 * y - seed) + 0.6 * math.sin(0.53 * x + 1.3 * seed + 0.7 * y) + 0.35 * math.sin(1.1 * x - 0.9 * y + seed)) / 1.95

def pine_kit(n=5):
    """n distinct pine meshes (shared mesh data, instanced as linked objects): trunk + 4-6 drooping tiers."""
    kit = []; fm = foliage_mat(); tm = flat('bark', '#5a3e2a', 0.95)
    for v in range(n):
        r = rnd(100 + v); mb = MB(); h = r.uniform(9.5, 13.0); nt_ = r.randint(4, 6)
        rod(mb, (0, 0, -0.4), (0, 0, h * 0.8), 0.28, tm, seg=5, r1=0.1)
        for t in range(nt_):
            f = t / nt_; zb = h * (0.16 + 0.62 * f); rr = (2.9 - 2.1 * f) * r.uniform(0.9, 1.1); hh = h * 0.30 * (1.0 - 0.3 * f)
            mb.frustum((0, 0, zb), (r.uniform(-0.1, 0.1), r.uniform(-0.1, 0.1), zb + hh), rr, 0.0, fm, seg=7, cap1=False)
        mb.frustum((0, 0, h * 0.78), (0, 0, h), 0.8, 0.0, fm, seg=6, cap1=False)
        me = bpy.data.meshes.new('pine%d' % v); me.from_pydata([Vector(a) for a in mb.v], [], mb.f); me.update()
        for m in mb.mats: me.materials.append(m)
        for fi, p in enumerate(me.polygons): p.material_index = mb.mi[fi]
        kit.append(me)
    S['pines'] = kit

def plant(x, y, z, h=None, seed=0, coll=None, rot=None):
    r = rnd(seed); me = S['pines'][r.randrange(len(S['pines']))]; o = bpy.data.objects.new('pine', me); (coll or S['coll']).objects.link(o)
    k = (h or r.uniform(0.8, 1.15)); o.location = (x, y, z); o.scale = (k * r.uniform(0.85, 1.1), k * r.uniform(0.85, 1.1), k); o.rotation_euler = (0, 0, r.uniform(0, 6.28)); return o

def polar_mesh(name, cx, cy, hfun, rmax, nr=28, nt=72, growth=1.06):
    """Radial height-field mesh around (cx, cy): rings spacing grows outward (fine near the shore). hfun(x, y) -> z."""
    rs = [0.0]; d = rmax / nr * 0.55
    while rs[-1] < rmax: d *= growth; rs.append(min(rmax, rs[-1] + d))
    rs = [r * rmax / rs[-1] for r in rs]; vs = []; fs = []
    for ri, r in enumerate(rs):
        for ti in range(nt):
            a = 2 * math.pi * ti / nt; x, y = cx + r * math.cos(a), cy + r * math.sin(a); vs.append((x, y, hfun(x, y)))
    for ri in range(len(rs) - 1):
        for ti in range(nt):
            t2 = (ti + 1) % nt; fs.append((ri * nt + ti, ri * nt + t2, (ri + 1) * nt + t2, (ri + 1) * nt + ti))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update(); [setattr(p, 'use_smooth', True) for p in me.polygons]
    ob = bpy.data.objects.new(name, me); S['coll'].objects.link(ob); return ob, me

def make_island(name, cx, cy, R, H, seed, kind='rock', npine=60, sand=False, dirn=None):
    """Green rocky island (or the beach island): height field cut by the sea level; pines and boulders placed ON the surface."""
    r = rnd(seed)
    def h(x, y):
        dx, dy = x - cx, y - cy; rr = math.hypot(dx, dy); a = math.atan2(dy, dx)
        Rn = R * (1 + 0.28 * math.sin(3 * a + seed) + 0.14 * math.sin(5 * a + 2 * seed) + 0.08 * math.sin(9 * a))
        u = rr / Rn
        if u >= 1: return -(u - 1) * (6 if kind == 'rock' else 3.0) - 0.05
        f = (1 - u * u) ** (1.15 if kind == 'rock' else 1.0)
        z = H * f * (1 + 0.28 * hfield(x * 0.6, y * 0.6, seed)) + (0.9 * H * 0.12 * math.sin(2.1 * a + 5 * u) * (1 - u) if kind == 'rock' else 0)
        if dirn is not None: z *= 0.55 + 0.45 * (0.5 + 0.5 * math.cos(a - dirn)) ** 0.7 if kind == 'beach' else 1.0
        return z - 0.15
    ob, me = polar_mesh(name, cx, cy, h, R * 1.5, 30, 80); me.materials.append(land_mat(name + '_m', sand=sand, rock=(kind == 'rock'), grass='#5a8240' if kind == 'beach' else '#4f7d3c'))
    S['islands'][name] = dict(c=(cx, cy), R=R, h=h)
    placed = 0; tries = 0
    while placed < npine and tries < npine * 12:
        tries += 1; a = r.uniform(0, 6.283); u = math.sqrt(r.uniform(0.0, 0.8)); x, y = cx + R * u * math.cos(a), cy + R * u * math.sin(a); z = h(x, y)
        if z < (1.8 if sand else 0.9): continue
        e = 0.5; sl = max(abs(h(x + e, y) - z), abs(h(x, y + e) - z)) / e
        if sl > 1.5: continue
        plant(x, y, z, r.uniform(0.7, 1.15) * (1.0 if kind == 'rock' else 0.8), seed * 100 + placed); placed += 1
    bm = MB(); mrock = flat('boulder', '#7e7466', 0.95)
    for k in range(int(R * 0.35)):
        a = r.uniform(0, 6.283); u = r.uniform(0.62, 1.0); x, y = cx + R * u * math.cos(a), cy + R * u * math.sin(a); z = h(x, y)
        if -0.4 < z < 2.2: lump(bm, (x, y, z + 0.1), r.uniform(0.5, 1.6), mrock, seed + k, seg=8, rings=5, rough=0.28, squash=0.7)
    if bm.f: mk(bm, name + '_rocks', smooth=True)
    return ob

def make_mountains(cx, cy, R0, R1, hmax, seed, az0=0, az1=360, col='#5b8a62', col2='#7c8f78', nt=180):
    """Backdrop mountain ring (green-blue, faded by the haze) between radii R0..R1 over azimuths az0..az1."""
    r = rnd(seed); vs = []; fs = []; nr = 7; ph = [r.uniform(0, 6.28) for _ in range(5)]
    def hz(a): return hmax * (0.35 + 0.65 * abs(math.sin(2.3 * a + ph[0]) * 0.6 + math.sin(5.1 * a + ph[1]) * 0.3 + math.sin(11.0 * a + ph[2]) * 0.18)) 
    n_az = int((az1 - az0) / 360 * nt) + 1
    for ri in range(nr):
        u = ri / (nr - 1); rr = R0 + (R1 - R0) * u
        for ti in range(n_az):
            a = math.radians(az0 + (az1 - az0) * ti / (n_az - 1)); z = hz(a) * (1 - u) ** 1.4 * (1 + 0.18 * math.sin(a * 37 + ri) ) - 4 + (2 if ri == 0 else 0)
            vs.append((cx + rr * math.cos(a), cy + rr * math.sin(a), z))
    for ri in range(nr - 1):
        for ti in range(n_az - 1): fs.append((ri * n_az + ti, ri * n_az + ti + 1, (ri + 1) * n_az + ti + 1, (ri + 1) * n_az + ti))
    me = bpy.data.meshes.new('mountains'); me.from_pydata(vs, [], fs); me.update(); [setattr(p, 'use_smooth', True) for p in me.polygons]
    def f(b):
        gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0]); n = b.noise(0.05, 3.0, 0.6, b.coord())
        c1 = b.mix(b.rng(z.outputs['Z'], 5, hmax * 0.8), hexl(col), hexl(col2)); c1 = b.mix(b.rng(n, 0.3, 0.7), c1, tint(col, 0.75) + (1.0,)); b.princ(c1, 0.95)
    me.materials.append(mat('J_mount_%d' % seed, f)); ob = bpy.data.objects.new('mountains', me); S['coll'].objects.link(ob); return ob

# ============================================================================= the ocean (film-10 swell geometry, physically shaded)
def swell_group():
    ng = bpy.data.node_groups.new('JO_swell', 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes.new; L = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput'); pos = N('GeometryNodeInputPosition'); sp = N('ShaderNodeSeparateXYZ'); L(pos.outputs[0], sp.inputs[0]); tm = N('GeometryNodeInputSceneTime')
    def wave(A, lam, ang, spd):
        k = 2 * math.pi / lam; ca, sa = math.cos(math.radians(ang)) * k, math.sin(math.radians(ang)) * k
        m1 = N('ShaderNodeMath'); m1.operation = 'MULTIPLY'; m1.inputs[1].default_value = ca; L(sp.outputs['X'], m1.inputs[0])
        m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY_ADD'; m2.inputs[1].default_value = sa; L(sp.outputs['Y'], m2.inputs[0]); L(m1.outputs[0], m2.inputs[2])
        m3 = N('ShaderNodeMath'); m3.operation = 'MULTIPLY_ADD'; m3.inputs[1].default_value = -spd; L(tm.outputs['Seconds'], m3.inputs[0]); L(m2.outputs[0], m3.inputs[2])
        s_ = N('ShaderNodeMath'); s_.operation = 'SINE'; L(m3.outputs[0], s_.inputs[0]); a_ = N('ShaderNodeMath'); a_.operation = 'MULTIPLY'; a_.inputs[1].default_value = A; L(s_.outputs[0], a_.inputs[0]); return a_
    def add(a, b): ad = N('ShaderNodeMath'); ad.operation = 'ADD'; L(a.outputs[0], ad.inputs[0]); L(b.outputs[0], ad.inputs[1]); return ad
    tot = None
    for w in SWELL + CHOP: tot = wave(*w) if tot is None else add(tot, wave(*w))
    cb = N('ShaderNodeCombineXYZ'); L(tot.outputs[0], cb.inputs['Z']); setp = N('GeometryNodeSetPosition'); L(gi.outputs[0], setp.inputs['Geometry']); L(cb.outputs[0], setp.inputs['Offset'])
    sm = N('GeometryNodeSetShadeSmooth'); L(setp.outputs[0], sm.inputs['Geometry']); L(sm.outputs[0], go.inputs[0]); return ng

def graded(a, b, c0, c1, h, grow=1.1):
    xs = list(np.arange(c0, c1 + 1e-6, h)); d = h
    while xs[0] > a: d *= grow; xs.insert(0, max(a, xs[0] - d))
    d = h
    while xs[-1] < b: d *= grow; xs.append(min(b, xs[-1] + d))
    return np.array(xs, 'float64')

def make_ocean(fine=(-260.0, 360.0, -200.0, 220.0), h=2.0, extent=(-1500.0, 1500.0, -1500.0, 1500.0)):
    X = graded(extent[0], extent[1], fine[0], fine[1], h); Y = graded(extent[2], extent[3], fine[2], fine[3], h); nx, ny = len(X), len(Y)
    gx, gy = np.meshgrid(X, Y); vs = np.stack([gx.ravel(), gy.ravel(), np.zeros(nx * ny)], 1); j, i = np.mgrid[0:ny - 1, 0:nx - 1]; a = (j * nx + i).ravel(); b = a + 1; c = a + nx + 1; d = a + nx
    alt = ((i + j) % 2).ravel().astype(bool); t1 = np.where(alt[:, None], np.stack([a, b, c], 1), np.stack([a, b, d], 1)); t2 = np.where(alt[:, None], np.stack([a, c, d], 1), np.stack([b, c, d], 1)); tris = np.concatenate([t1, t2])
    me = bpy.data.meshes.new('ocean'); me.vertices.add(len(vs)); me.vertices.foreach_set('co', vs.astype('float32').ravel()); me.loops.add(len(tris) * 3); me.loops.foreach_set('vertex_index', tris.astype('int32').ravel())
    me.polygons.add(len(tris)); me.polygons.foreach_set('loop_start', np.arange(0, len(tris) * 3, 3, dtype='int32')); me.polygons.foreach_set('loop_total', np.full(len(tris), 3, 'int32')); me.update(); me.validate()
    me.materials.append(water_mat('sea')); ob = bpy.data.objects.new('ocean', me); S['coll'].objects.link(ob); md = ob.modifiers.new('swell', 'NODES'); md.node_group = swell_group(); S['ocean'] = ob
    mb = MB(); R0, R1 = 1800.0, 6000.0; seg = 48                       # flat far disc under the horizon
    for k in range(seg):
        a0, a1 = 2 * math.pi * k / seg, 2 * math.pi * (k + 1) / seg
        mb.face([Vector((R0 * math.cos(a0), R0 * math.sin(a0), -0.3)), Vector((R1 * math.cos(a0), R1 * math.sin(a0), -0.3)), Vector((R1 * math.cos(a1), R1 * math.sin(a1), -0.3)), Vector((R0 * math.cos(a1), R0 * math.sin(a1), -0.3))][::-1], water_mat('sea'), [(0, 0)] * 4)
    mk(mb, 'ocean_far', shadow=False)
