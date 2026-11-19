
# ============================================================================= materials
def _materials(P, C, TX, tx, pre):
    lk = max(P.get('lamps', 0.0), 0.0)
    M = dict(brick=TX('brick_a'), brick_b=TX('brick_b'), brick_c=TX('brick_c'), brick_d=TX('brick_d'), brick_e=TX('brick_e'), ash=TX('ash'), rustic=TX('rustic'), stone_grey=TX('stone_grey'),
             walk=TX('plank_walk'), plank_d=TX('plank_dark'), plank_f=TX('plank_floor'), crate=TX('crate'), timber=TX('timber'), timber_d=TX('timber_d'), timber_w=TX('timber_w'),
             clap_ochre=TX('clap_ochre'), clap_teal=TX('clap_teal'), clap_cream=TX('clap_cream'), clap_green=TX('clap_green'), clay=TX('clay', form=False), gravel=TX('gravel', form=False),
             win_dark=TX('win_dark'), win_lit=TX('win_lit', glow='win_lit', glow_k=1.0), win_curt=TX('win_curt'), win_lit2=TX('win_lit2', glow='win_lit2', glow_k=1.0),
             win_dark_short=TX('win_dark_short'), win_lit_short=TX('win_lit_short', glow='win_lit_short', glow_k=1.0), win_dark_big=TX('win_dark_big'), win_lit_big=TX('win_lit_big', glow='win_lit_big', glow_k=1.1),
             win_base=TX('win_dark_base'), fac_a=TX('fac_a'), fac_b=TX('fac_b'), fac_c=TX('fac_c'), fac_d=TX('fac_d'), fac_e=TX('fac_e'), fac_f=TX('fac_f'),
             awn_rc=TX('awn_rc', sm=(1.2, 0.9, 0.8), smix=0.3), awn_tc=TX('awn_tc', smix=0.3), awn_oc=TX('awn_oc', smix=0.3),
             wallpaper=TX('wallpaper'), parquet=TX('parquet', form=False), rug=TX('rug', form=False), velvet_red=TX('velvet_red', smix=0.25), velvet_teal=TX('velvet_teal', smix=0.25),
             p_lake=TX('paint_lake'), p_land=TX('paint_land'), p_still=TX('paint_still'), p_portrait=TX('paint_portrait'), frame=_glossy(TX('frame_gold', sm=(2.0, 1.4, 0.6), smix=0.15), (1.0, 0.8, 0.5), 0.5, 0.25),
             iron=_glossy(C('#5a5e6c', 1.0, 1.6), (1.0, 0.85, 0.7), 0.35, 0.3), iron_d=C('#34363f', 1.0, 1.8),
             iron_k=_glossy(C('#3a3d48', 1.1, 1.9), (1.0, 0.85, 0.7), 0.45, 0.28), iron_bar=_glossy(C('#4c505e', 1.0, 1.7), (1.0, 0.85, 0.7), 0.5, 0.25), thread=TX('thread', gain=1.1, sm=1.5),
             jack_red=_glossy(C('#c04a2c', 1.0, (1.5, 0.9, 0.8), smix=0.25), (1.0, 0.8, 0.6), 0.4, 0.3), brass=_glossy(C('#b8923e', 1.0, (2.0, 1.5, 0.6), smix=0.2), (1.0, 0.8, 0.5), 0.5, 0.22),
             dirt=TX('mud_wet', form=False), stair_stone=TX('ash'), wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b8925e'), rope=C('#c8a868'), cream=C('#ecdcb6'), white=C('#efe8d8'),
             dark=C('#2a2a32', 1.0, 1.6, form=False), red=C('#b02a22', 1.0, (1.4, 0.8, 0.7), smix=0.25), teal=C('#2f8a82', 1.0, 1.0, smix=0.3), green=C('#3e6a46'), slate=C('#59607a'), stone=C('#b0a898'),
             canvas=C('#d8c89a'), sack=C('#c9b78c'), hay=C('#d4b45c'), door=C('#2e5a4c'), door_r=C('#7a2a24', 1.0, (1.4, 0.8, 0.7), smix=0.25), horse=C('#8a5230'), horse_d=C('#4a2c1a'), horse_g=C('#8a8680'),
             horse_w=C('#dcd2bc'), skin=C('#d8a880'), coal=C('#26262a', 1.0, 0.9),
             lamp_glass=mat_emit(pre + 'e_lampglass', '#ffd890', strength=3.4 * max(0.2, lk)), glass_cand=mat_emit(pre + 'e_cand', '#fff0b8', strength=6.0),
             flag_r=TX('awn_rc'), flag_b=C('#2c3f86'),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.6, 0.3), 0.8 if lk > 0 else 0.5), pool=MN._mat_pool(pre + 'poolmat', (1.0, 0.6, 0.28), 0.55),
             shaft=BK._mat_add(pre + 'shaft', tx['shaft'], (1.0, 0.82, 0.55), 0.5))
    M['_flame_mats'] = [M['lamp_glass']]
    M['sky'] = D._mat_sky(pre + 'sky', dict(P, star_k=0.0), tx['sky_' + P['sky']], P['sky_k'])
    M['mud'] = _mud_mat(pre, P, tx); M['puddle'] = _puddle_mat(pre, P, tx); M['scum'] = _scum_mat(pre, P, tx); M['tea'] = _tea_mat(pre, P)
    return M

def _mud_mat(pre, P, tx):
    """Street mud: painted grey-brown ochre blended to a wet dark grey-brown by height (troughs, ruts and puddle rims), a soft broad GGX sheen
    (wetter in RAIN), not polished."""
    m = _untoon(mat_lit(pre + 'mud', image=tx['mud'], form=tuple(P['form']), shade_mix=0.35, gain=0.85)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); links0 = list(tex.outputs['Color'].links); tex.extension = 'REPEAT'
    t2 = N('ShaderNodeTexImage'); t2.image = T._img(tx['mud_wet']); t2.extension = 'REPEAT'
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sp.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'; mr.inputs['From Min'].default_value = -0.42; mr.inputs['From Max'].default_value = 0.10; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    L(sp.outputs['Z'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(mr.outputs['Result'], mx.inputs[0]); L(tex.outputs['Color'], mx.inputs[6]); L(t2.outputs['Color'], mx.inputs[7])
    for l in links0: to = l.to_socket; nt.links.remove(l); L(mx.outputs[2], to)
    w = float(P.get('wet', 0.3))
    _glossy(m, (1.0, 0.86, 0.68), 0.10 + 0.34 * w, 0.5 - 0.3 * w)
    return m

def _puddle_mat(pre, P, tx):
    """Puddle water: dark grey-brown base (shade stays painted) + a mirror (sharp GGX + glossy bounce): hotel, sky, lamps."""
    m = _untoon(mat_lit(pre + 'puddle', '#4a4038', form=tuple(P['form']), shade_mix=0.5, gain=0.7))
    def make(nt):
        gl = nt.nodes.new('ShaderNodeBsdfGlossy' if False else 'ShaderNodeBsdfAnisotropic'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.02; gl.inputs['Color'].default_value = (0.9, 0.88, 0.86, 1)
        return gl.outputs['BSDF']
    MN._append_shader(m, make)
    return m

def _scum_mat(pre, P, tx):
    """soft foam / scum on the puddles: pale tan blotches (image alpha) over the water."""
    return _untoon(mat_lit(pre + 'scum', image=tx['scum'], form=tuple(P['form']), alpha=True, shade_mix=0.4, gain=0.95))

def _tea_mat(pre, P):
    """Tea surface: dark amber diffuse + sharp mirror; Value 'ripple_k' (0 = perfectly flat mirror) scales a noise bump on the normal, 'ripple_p' is its phase."""
    m = _untoon(mat_lit(pre + 'tea', '#7a3e1a', form=None, shade_mix=0.3, gain=0.75)); nt = m.node_tree
    rk = D._value(nt, 'ripple_k', 0.0); rp = D._value(nt, 'ripple_p', 0.0); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.inputs['Scale'].default_value = 9.0; nz.inputs['Detail'].default_value = 1.0
    L(tc.outputs['Object'], nz.inputs['Vector']); L(rp.outputs[0], nz.inputs['W'])
    bp = N('ShaderNodeBump'); bp.inputs['Distance'].default_value = 0.02; L(rk.outputs[0], bp.inputs['Strength']); L(nz.outputs['Fac'], bp.inputs['Height'])
    def make(nt2):
        gl = nt2.nodes.new('ShaderNodeBsdfAnisotropic'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.0; gl.inputs['Color'].default_value = (1.0, 0.98, 0.95, 1)
        nt2.links.new(bp.outputs['Normal'], gl.inputs['Normal']); return gl.outputs['BSDF']
    MN._append_shader(m, make)
    dif = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfDiffuse'][0]; L(bp.outputs['Normal'], dif.inputs['Normal'])
    return m

# ============================================================================= sky + far ground
def _sky(SET, P, M, R):
    mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o
    if P.get('pano'):
        mb = MB(); Rp = CX.PANO_R; seg = 192; pm = mat_emit(STATE['pre'] + 'e_pano', image=STATE['tx']['pano_' + P['pano']], strength=P['pano_k'], alpha=True)
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
            mb.face([Vector((Rp * math.cos(a0), Rp * math.sin(a0), CX.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), CX.PANO_Z0)),
                     Vector((Rp * math.cos(a1), Rp * math.sin(a1), CX.PANO_Z1)), Vector((Rp * math.cos(a0), Rp * math.sin(a0), CX.PANO_Z1))], pm, [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
        _obj(mb, 'backdrop', SET, shadow=False)

def _far_ground(SET, M, z=-2.5):
    mb = MB(); R = 430.0; fm = STATE['TX']('far_ground', form=False)
    mb.face([Vector((-R, -R, z)), Vector((R, -R, z)), Vector((R, R, z)), Vector((-R, R, z))], fm, [(0, 0), (R / 8, 0), (R / 8, R / 8), (0, R / 8)]); _obj(mb, 'far_ground', SET)

# ============================================================================= terrain: mud with ruts and layered puddles
# (cx, cy, rx, ry, depth): ellipse basins; the long thin ones sit in the wheel ruts
PUDDLES = [(-14, -31, 6.0, 4.8, 0.85), (6, -37, 4.5, 3.6, 0.7), (-33, -24, 4.0, 3.2, 0.7), (18, -23, 5.2, 4.2, 0.8), (-3, -16.5, 3.0, 2.4, 0.65), (30, -34, 3.8, 3.0, 0.7),
           (-22, -42, 4.2, 3.4, 0.7), (11, -12.5, 2.6, 2.0, 0.6), (-40, -35, 4.2, 3.4, 0.7), (40, -21, 3.5, 2.8, 0.65), (-9, -24, 2.1, 1.7, 0.6), (24, -41, 2.7, 2.2, 0.6),
           (-8, -46, 3.8, 3.0, 0.7), (12, -47, 3.2, 2.6, 0.7), (-36, -46, 2.7, 2.2, 0.6), (-2, -29.4, 9.0, 0.75, 0.5), (22, -35.0, 8.0, 0.7, 0.5), (-26, -26.0, 7.0, 0.65, 0.5),
           (14, -38.2, 7.0, 0.7, 0.45), (-18, -35.0, 6.0, 0.7, 0.5), (-50, -30, 4.0, 3.2, 0.6), (52, -30, 4.0, 3.2, 0.6)]
def _terrain(SET, M):
    """Smooth mud height field (shared vertices): rolling noise, wheel ruts, a crown, elliptical puddle basins; flat water discs sit at each basin's lowest rim
    height so the terrain cuts the outline; a second scum disc 0.1 higher floats pale blotches near the rim (soft foam edge)."""
    xs = np.unique(np.round(np.concatenate([np.arange(-150, -76, 4.0), np.arange(-76, 76, 0.5), np.arange(76, 151, 4.0)]), 3))
    ys = np.unique(np.round(np.concatenate([np.arange(-130, -58, 4.0), np.arange(-58, -2, 0.45), np.arange(-2, 60, 4.0)]), 3))
    def sm(a, b, v):
        t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
    def mud_z(x, y):
        win = sm(-58, -48, y) * (1 - sm(-11, -7.5, y)); flat = np.ones_like(x * 1.0)
        for (cx, cy, rx, ry, dp) in PUDDLES: flat = flat * (1 - 0.85 * np.exp(-(((x - cx) / (rx * 1.5)) ** 2 + ((y - cy) / (ry * 1.5)) ** 2)))
        z = 0.2 * np.sin(0.21 * x + 0.7) * np.cos(0.17 * y + 1.1) + 0.12 * np.sin(0.43 * x + 0.2 * y) + 0.07 * np.sin(0.93 * x - 0.6 * y + 2.0)
        for yr in (-26.0, -29.4, -35.0, -38.2): z = z - 0.34 * np.exp(-((y - yr + 0.4 * np.sin(0.06 * x)) / 0.6) ** 2) * (0.75 + 0.25 * np.sin(0.11 * x + yr))
        z = (z + 0.2 * np.exp(-((y + 27.7) / 1.1) ** 2) + 0.15 * np.exp(-((y + 36.6) / 0.9) ** 2)) * flat * win
        for (cx, cy, rx, ry, dp) in PUDDLES: z = z - dp * np.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2))
        return z
    X, Y = np.meshgrid(xs, ys); Z = mud_z(X, Y)
    terr = grid_mesh('mud', xs, ys, Z, M['mud'], uvs=(0.1, 0.1)); STATE['terrain'] = terr; STATE['fill_objs'].append(terr); STATE['mud_z'] = mud_z
    pm = MB(); sc = MB(); n = 32
    for (cx, cy, rx, ry, dp) in PUDDLES:
        ang = np.linspace(0, 2 * math.pi, 48, endpoint=False); rim = mud_z(cx + rx * 2.2 * np.cos(ang), cy + ry * 2.2 * np.sin(ang)); zw = min(float(rim.min()) - 0.02, -0.12)
        for (mbx, k, dz, mat) in ((pm, 2.3, 0.0, M['puddle']), (sc, 2.0, 0.09, M['scum'])):
            pts = [Vector((cx + rx * k * math.cos(2 * math.pi * j / n), cy + ry * k * math.sin(2 * math.pi * j / n), zw + dz)) for j in range(n)]
            for j in range(n):
                a, b = pts[(j + 1) % n], pts[j]; c = Vector((cx, cy, zw + dz))
                mbx.face([c, a, b], mat, [(cx * 0.08, cy * 0.08), (a.x * 0.08, a.y * 0.08), (b.x * 0.08, b.y * 0.08)])
    po = _obj(pm, 'puddles', SET); so = _obj(sc, 'scum', SET, shadow=False); STATE['fill_objs'] += [po, so]
    return mud_z
