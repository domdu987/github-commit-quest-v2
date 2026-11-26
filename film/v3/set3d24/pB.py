
# ============================================================================= scene: world, sun, haze, render settings
SKY = [(0.0, '#f3d3b0'), (0.09, '#d2c3d2'), (0.28, '#93b3e4'), (0.62, '#4a78cd')]       # peach horizon -> blue zenith (COLOUR_SPEC daytime sky)

def setup_world(sc, sky_k=1.0):
    w = bpy.data.worlds.new('joseon_sky'); sc.world = w; b = NB.__new__(NB); w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD': nt.nodes.remove(n)
    N = nt.nodes.new; L = nt.links.new; o = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0]); ramp = N('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = SKY[0][0]; cr.elements[0].color = (*hexl(SKY[0][1]), 1); cr.elements[1].position = SKY[-1][0]; cr.elements[1].color = (*hexl(SKY[-1][1]), 1)
    for pos, col in SKY[1:-1]: e = cr.elements.new(pos); e.color = (*hexl(col), 1)
    L(sep.outputs['Z'], ramp.inputs[0])
    glow = N('ShaderNodeVectorMath', operation='DOT_PRODUCT'); L(tc.outputs['Generated'], glow.inputs[0]); S['sun_glow'] = glow
    pw = N('ShaderNodeMath', operation='POWER'); pw.inputs[1].default_value = 18.0; mx = N('ShaderNodeMath', operation='MAXIMUM'); mx.inputs[1].default_value = 0.0
    L(glow.outputs['Value'], mx.inputs[0]); L(mx.outputs[0], pw.inputs[0]); sc_ = N('ShaderNodeMath', operation='MULTIPLY'); sc_.inputs[1].default_value = 1.4; L(pw.outputs[0], sc_.inputs[0])
    col = N('ShaderNodeMix', data_type='RGBA'); col.inputs[6].default_value = (0, 0, 0, 1); col.inputs[7].default_value = (3.0, 1.7, 0.8, 1); L(sc_.outputs[0], col.inputs[0])
    ad = N('ShaderNodeMix', data_type='RGBA', blend_type='ADD'); ad.inputs[0].default_value = 1.0; L(ramp.outputs[0], ad.inputs[6]); L(col.outputs[2], ad.inputs[7])
    bg = N('ShaderNodeBackground'); bg.inputs['Strength'].default_value = sky_k; L(ad.outputs[2], bg.inputs['Color']); L(bg.outputs[0], o.inputs['Surface'])

def set_sun(az_deg, elev, energy=None):
    """Sun by azimuth (direction TO the sun, degrees from +x CCW) and elevation. Warm key (1.0, 0.66, 0.40), 1.5 deg disc."""
    sun = S['sun']; e = math.radians(elev); a = math.radians(az_deg); to_sun = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))
    sun.rotation_euler = (-to_sun).to_track_quat('-Z', 'Y').to_euler(); S['to_sun'] = to_sun; S['sun_glow'].inputs[1].default_value = to_sun
    if energy: sun.data.energy = energy

def sun_for_camera(setup, elev=16.0, left=1.0, behind=0.38):
    """The key comes from the camera's left (and a little behind it)."""
    f = Vector(setup['look_at']) - Vector(setup['loc']); f.z = 0; f.normalize(); lf = Vector((-f.y, f.x, 0)); h = (lf * left - f * behind).normalized()
    return math.degrees(math.atan2(h.y, h.x)), elev

def make_haze(density, center, size):
    m = mat('J_haze', lambda b: None); b = NB(m); v = b.n('ShaderNodeVolumePrincipled'); v.inputs['Density'].default_value = density; v.inputs['Anisotropy'].default_value = 0.5
    v.inputs['Color'].default_value = (*hexl('#f1e6e0'), 1); b.l(v.outputs[0], b.out.inputs['Volume']); S['haze_mat'] = m; S['haze_node'] = v
    vs = [(center[0] + sx * size[0], center[1] + sy * size[1], center[2] + sz * size[2]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new('haze'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(m); ob = bpy.data.objects.new('haze', me); S['coll'].objects.link(ob)
    ob.visible_shadow = False; ob.visible_glossy = True; return ob

def setup_render(sc, quality='final'):
    """Cycles CPU, path tracing with GI, 24 samples adaptive + OIDN, 75 % resolution (540x960) upscaled to 720x1280 by post(); preview 40 %."""
    r = sc.render; r.engine = 'CYCLES'; r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 75 if quality == 'final' else 40
    r.image_settings.file_format = 'PNG'; r.use_motion_blur = False; r.fps = FPS
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = 24 if quality == 'final' else 10; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05; cy.adaptive_min_samples = 6
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 1
    cy.volume_bounces = 0; cy.transparent_max_bounces = 6; cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0; cy.volume_step_rate = 3.0
    cy.use_light_tree = True; r.threads_mode = 'FIXED'; r.threads = 2; r.use_persistent_data = True
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except TypeError: pass
    sc.view_settings.exposure = float(S.get('exposure', 0.0))

def make_camera(setup, name='cam', scene=None):
    """Camera from {loc, look_at, lens[, fstop, focus (distance or point), up, roll]}. Lens on a 36 mm sensor (film-10 convention). DOF only when fstop is given
    (macro presets); wide shots are sharp. Nothing is ever parented to the camera."""
    scene = scene or bpy.context.scene; ob = bpy.data.objects.get(name)
    if ob is None: cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 9000
    ob.location = setup['loc']; fwd = (Vector(setup['look_at']) - Vector(setup['loc'])).normalized()
    if 'up' in setup:
        right = fwd.cross(Vector(setup['up'])).normalized(); up = right.cross(fwd); ob.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
    else: ob.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    if setup.get('fstop'):
        cd.dof.use_dof = True; cd.dof.aperture_fstop = setup['fstop']; fp = setup.get('focus', setup['look_at'])
        cd.dof.focus_distance = float(fp) if isinstance(fp, (int, float)) else (Vector(fp) - Vector(setup['loc'])).length; cd.dof.aperture_blades = 7
    else: cd.dof.use_dof = False
    scene.camera = ob; return ob

# ============================================================================= swell (shared by the ocean mesh and the ship / plank drivers)
SWELL = [(0.20, 34.0, 20.0, 0.9), (0.12, 21.0, 75.0, 1.2), (0.07, 13.0, -35.0, 1.6)]       # A, wavelength, direction deg, angular speed
CHOP = [(0.03, 7.3, 52.0, 2.2), (0.02, 4.9, -67.0, 2.8)]
def swell_z(x, y, t):
    z = 0.0
    for A, lam, ang, spd in SWELL: k = 2 * math.pi / lam; z += A * math.sin(k * (x * math.cos(math.radians(ang)) + y * math.sin(math.radians(ang))) - spd * t)
    return z
def swell_expr(xs='x', ys='y', amp=1.0):
    parts = []
    for A, lam, ang, spd in SWELL:
        k = 2 * math.pi / lam; parts.append('%.4f*sin(%.5f*%s+%.5f*%s-%.4f*frame/%d)' % (A * amp, k * math.cos(math.radians(ang)), xs, k * math.sin(math.radians(ang)), ys, spd, FPS))
    return '+'.join(parts)

def drive(ob, path, idx, expr, vars_):
    fc = ob.driver_add(path, idx); d = fc.driver; d.type = 'SCRIPTED'; d.expression = expr
    for nm, (idb, dp) in vars_.items():
        v = d.variables.new(); v.name = nm; v.type = 'SINGLE_PROP'; v.targets[0].id = idb; v.targets[0].data_path = dp

def ride_swell(ob, root, base_z=0.0, amp=1.0, roll=0.0, pitch=0.0, seed=0, extra=''):
    """Heave of `ob` (child of root) from the SAME swell as the ocean mesh at the root's x, y (ships sit in the water at every frame)."""
    drive(ob, 'location', 2, '%.3f+%s%s' % (base_z, swell_expr('x', 'y', amp), extra), dict(x=(root, 'location[0]'), y=(root, 'location[1]')))
    r = rnd(seed); a, b = r.uniform(0, 6.28), r.uniform(0, 6.28)
    if roll: drive(ob, 'rotation_euler', 0, '%.4f*sin(frame*0.11+%.3f)' % (roll, a), {})
    if pitch: drive(ob, 'rotation_euler', 1, '%.4f*sin(frame*0.09+%.3f)' % (pitch, b), {})

# ============================================================================= ships: common
def new_ship(name, kind, L, B, loc, yaw_deg, scale=1.0, sea=True, hscale=1.0):
    root = empty('ship_' + name, None, tuple(loc), (0, 0, math.radians(yaw_deg))); root.rotation_mode = 'XYZ'; root.scale = (scale,) * 3
    ride = empty('ride_' + name, root); sh = dict(name=name, kind=kind, L=L, B=B, root=root, ride=ride, base=Vector(loc), yaw=yaw_deg, scale=scale, guns=[], oars=[], masts=[], parts=[], sea=sea)
    if sea: ride_swell(ride, root, 0.0, 1.0, roll=0.014, pitch=0.007, seed=hash(name) % 97)
    S['ships'][name] = sh; return sh

def wake_foam(sh, big=True, bowspray=True):
    """Flat foam on the water, children of the root: bow-wave crests, side wash, stern wake (swell-driven so it sits on the surface)."""
    L, B = sh['L'], sh['B']; fb = MB(); mb_, mw_ = S['M']['foam_bow'], S['M']['foam_wake']; z = 0.0; n = Vector((0, 0, 1))
    for sg in (-1, 1):
        a = Vector((L / 2 - 0.8, 0, z)); b = Vector((L / 2 - 0.42 * L, sg * (B / 2 + 0.28 * B + 3.0), z)); side = (b - a).normalized().cross(n) * (0.13 * B + 1.3 * (1 if big else 0.6) * sg)
        fb.oface([a - side * 0.25, b - side, b + side, a + side * 0.5], mb_, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
        a2 = Vector((L / 2 - 4.0, sg * (B / 2 - 0.3), z)); b2 = Vector((-L / 2, sg * (B / 2 + 0.2), z))
        fb.oface([a2, b2, b2 + Vector((0, sg * 1.4, 0)), a2 + Vector((0, sg * 1.0, 0))], mb_, [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.85)], n)
    s0 = Vector((-L / 2 + 0.8, 0, z)); s1 = Vector((-L / 2 - 2.4 * L, 0, z))
    fb.oface([s0 + Vector((0, -B * 0.42, 0)), s1 + Vector((0, -B * 1.4, 0)), s1 + Vector((0, B * 1.4, 0)), s0 + Vector((0, B * 0.42, 0))], mw_, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
    o = mk(fb, 'foam_' + sh['name'], sh['root'], shadow=False); o.visible_glossy = False
    drive(o, 'location', 2, '0.17+' + swell_expr('x', 'y', 1.0), dict(x=(sh['root'], 'location[0]'), y=(sh['root'], 'location[1]')))
    sh['foam'] = o
    if bowspray:
        mb = MB()
        for sg in (-1, 1):
            for k in range(6):
                t = k / 5.0; lump(mb, Vector((L / 2 - 1.0 - t * 0.3 * L, sg * (B * 0.22 + t * (B / 2 + 2.2)), 0.25 - 0.1 * t)), (0.75 - 0.45 * t) * min(1.4, B / 8), S['M']['spray'], 11 + k + (3 if sg > 0 else 0), seg=7, rings=4, rough=0.3, squash=0.55)
        for k in range(6): lump(mb, Vector((-L / 2 - 1.2 - k * 1.3, ((k * 37) % 7 - 3) * 0.4, 0.2)), 0.9 - 0.08 * k, S['M']['spray'], 40 + k, seg=7, rings=4, rough=0.3, squash=0.45)
        o2 = mk(mb, 'spray_' + sh['name'], sh['root'], shadow=False); smooth_round(o2, 1)
        drive(o2, 'location', 2, '0.1+' + swell_expr('x', 'y', 1.0), dict(x=(sh['root'], 'location[0]'), y=(sh['root'], 'location[1]'))); sh['spray'] = o2

def flag_obj(sh, key, base, h, w, wave=0.0, pole=True, parent=None, name='flag', pole_r=0.07, pole_mat=None, vertical=False, ph=0.0):
    """A flag on a pole: pole rod from base up h; cloth (plain colour or white banner) hung from the top, streaming aft (-x local), slight S wave."""
    mb = MB(); base = Vector(base); M_ = S['M']
    if pole: rod(mb, base, base + Vector((0, 0, h)), pole_r, pole_mat or M_['wood_d'], seg=6)
    top = base + Vector((0, 0, h)); fm = flagmat(key); mb2 = MB(); nu, nv = 6, 1
    if vertical:                                           # nobori: tall narrow banner on a cross-bar, hanging
        bar = w * 1.15; beam(mb, top - Vector((0, bar / 2, 0.08)), top + Vector((0, bar / 2, -0.08)), 0.07, 0.07, M_['wood_d'])
        quad_grid(mb2, lambda i, j: top + Vector((0.03 * math.sin(i * 0.9 + ph), -w / 2 + w * j, -0.15 - (w * 3.3) * i / nu)), nu, nv, fm, uvs=lambda i, j: (j, 1 - i / nu))
    else:
        quad_grid(mb2, lambda i, j: top + Vector((-w * i / nu, wave * math.sin(i * 1.1 + ph) * (i / nu), -(w * 0.62) * j - 0.1)), nu, nv, fm, uvs=lambda i, j: (i / nu, 1 - j))
    o = mk(mb, name + '_pole', parent or sh['ride']); o2 = mk(mb2, name + '_cloth', parent or sh['ride'], shadow=True); o2.data.materials[0] = fm
    for pg in o2.data.polygons: pg.use_smooth = True
    return o

def oar_set(sh, xs, ys, zp, length_out=6.4, length_in=1.4, dip=True, tilt_deg=None, stroke=True, blade=True):
    """Oars through the hull side: pivot (x, +-y, zp); tilted so the blade dips into the water (dip) or raised (rest). Stroke = driver on the yaw."""
    M_ = S['M']; r = rnd(len(sh['name']) * 7)
    for i, (x, yh) in enumerate(zip(xs, ys)):
        for sg in (1, -1):
            mb = MB(); rod(mb, (0, -length_in, 0), (0, length_out - 1.0, 0), 0.085, M_['wood_l'], seg=6, r1=0.07)
            beam(mb, (0, length_out - 1.3, 0), (0, length_out + 0.1, 0), 0.5, 0.05, M_['wood_l'])
            o = mk(mb, 'oar_%s_%d_%s' % (sh['name'], i, 'p' if sg > 0 else 's'), sh['ride']); o.location = (x, sg * yh, zp)
            a = math.asin(max(-0.9, min(0.9, (zp + 0.12) / (length_out - 0.5)))) if dip else math.radians(tilt_deg if tilt_deg is not None else 35)
            o.rotation_mode = 'XYZ'; o.rotation_euler = (-a if dip else a, 0, 0 if sg > 0 else math.pi)
            if stroke: drive(o, 'rotation_euler', 2, '%.4f+0.2*sin(frame*0.33+%.3f)' % (0 if sg > 0 else math.pi, i * 0.5 + (0 if sg > 0 else 0.7) + r.uniform(0, 0.4)), {})
            sh['oars'].append(o)

# ============================================================================= THE TURTLE SHIP (hero prop)
TLEN = 34.0; THALF = 17.0; TBM = 4.6; Z_EAVE = 2.7
def t_b(x):
    p = 3.2 if x > 0 else 2.6
    return TBM * math.sqrt(max(0.0, 1.0 - (abs(x) / THALF) ** p))
def t_ye(x): return t_b(x) + 0.42
def t_H(x): return 2.7 * math.sqrt(max(0.0, 1.0 - (abs(x) / THALF) ** 2.4))
def roof_z(x, y):
    ye = max(0.05, t_ye(x)); v = min(1.0, abs(y) / ye); return Z_EAVE + t_H(x) * (1.0 - v ** 2.2)
def roof_n(x, y):
    e = 0.05; dx = (roof_z(x + e, y) - roof_z(x - e, y)) / (2 * e); dy = (roof_z(x, y + e) - roof_z(x, y - e)) / (2 * e); return Vector((-dx, -dy, 1.0)).normalized()

SPIKE_V = [(0.17, 0.29, 0.41), (0.53, 0.65, 0.77), (0.86, 0.92, 0.975)]     # spike lines (fraction of the half-width), ridge -> eave: stage 1, 2, 3

def build_turtle(name='turtle', loc=(0, 0, 0), yaw=0.0, sea=False, sail=False, oars_dip=None, scale=1.0, pitch=0.0):
    M_ = S['M']; sh = new_ship(name, 'turtle', TLEN, 2 * TBM, loc, yaw, scale, sea=sea); ride = sh['ride']
    if pitch: ride.rotation_mode = 'XYZ'; ride.rotation_euler = (0, math.radians(pitch), 0)
    N = 36; xs = [-THALF + TLEN * (1 - math.cos(math.pi * i / N)) / 2 for i in range(N + 1)]
    prof = [(0.0, -1.55), (0.42, -1.5), (0.8, -1.05), (0.965, -0.4), (1.0, 0.0), (1.012, 1.0), (1.005, 2.0), (0.99, 2.52)]
    def hp(i, j):                                      # j runs over the full section: starboard keel->eave then port eave->keel
        x = xs[i]; b = t_b(x); k = j if j < len(prof) else 2 * len(prof) - 1 - j; f, z = prof[k]; return Vector((x, (f * b) * (1 if j < len(prof) else -1), z))
    mb = MB(); quad_grid(mb, hp, N, 2 * len(prof) - 1, M_['hull'], orient=lambda c: Vector((0, c.y, c.z * 0.2 + 0.001)).normalized() if abs(c.y) > 0.05 else Vector((0, 0, -1)))
    sh['hull'] = mk(mb, name + '_hull', ride, smooth=True)
    # --- roof (hexagonal plates) : the dome
    nv = 28; mb = MB()
    def rp(i, j):
        x = xs[i]; v = -1 + 2 * j / nv; y = v * t_ye(x); return Vector((x, y, roof_z(x, y)))
    quad_grid(mb, rp, N, nv, M_['hexroof'], uvs=lambda i, j: (xs[i] / 11.2, (-1 + 2 * j / nv) * t_ye(xs[i]) / 9.7), orient=lambda c: Vector((0, 0, 1)))
    sh['roof'] = mk(mb, name + '_roof', ride, smooth=True)
    # --- eave trim (dark wood lip) + soffit
    mb = MB()
    for sg in (-1, 1):
        for i in range(N):
            x0, x1 = xs[i], xs[i + 1]; a, b = Vector((x0, sg * t_ye(x0), Z_EAVE)), Vector((x1, sg * t_ye(x1), Z_EAVE)); a2, b2 = a - Vector((0, 0, 0.34)), b - Vector((0, 0, 0.34))
            mb.oface([a, b, b2, a2], M_['wood_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
            c0, c1 = Vector((x0, sg * t_b(x0), 2.52)), Vector((x1, sg * t_b(x1), 2.52)); mb.oface([a2, b2, c1, c0], M_['wood_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, -1)))
    mk(mb, name + '_eave', ride)
    # --- cross-shaped walkway on the ridge
    mb = MB(); wy = 0.62
    def strip(f, n_, hw, lo, hi, along_x):
        for sgn in (-1, 1):
            quad_grid(mb, lambda i, j: f(lo + (hi - lo) * i / n_, sgn * hw * j) + Vector((0, 0, 0.1)) if True else None, n_, 1, M_['walk'], orient=lambda c: Vector((0, 0, 1)))
    P_ = lambda t, d: Vector((t, d, roof_z(t, d)))                            # along the ridge
    strip(lambda t, d: P_(t, d), 30, wy, -10.5, 10.5, True)
    strip(lambda t, d: Vector((d, t, roof_z(d, t))), 14, wy, -3.3, 3.3, False)
    for sgn in (-1, 1):                                                         # low side rails of the walkway (cross + long)
        for t0 in range(-10, 10):
            a = P_(t0 + 0.0, sgn * wy) + Vector((0, 0, 0.1)); b = P_(t0 + 1.0, sgn * wy) + Vector((0, 0, 0.1))
            if abs(t0) >= 1 and abs(t0 + 1) >= 1 or True: beam(mb, a + Vector((0, 0, 0.14)), b + Vector((0, 0, 0.14)), 0.07, 0.2, M_['wood_d'])
    mk(mb, name + '_walk', ride, smooth=False)
    # --- iron spikes in 3 stages (ridge -> eave); each stage is one object popped in by set_spikes
    sh['spikes'] = []
    for st, vs in enumerate(SPIKE_V):
        mb = MB()
        for li, vv in enumerate(vs):
            for sg in (-1, 1):
                x = -14.0 + (0.6 if (li + (sg > 0)) % 2 else 0.0)
                while x < 14.2:
                    ye = t_ye(x); y = sg * vv * ye
                    if abs(x) > 0.95 and ye * 0.12 > 0.30:
                        n = roof_n(x, y); base = Vector((x, y, roof_z(x, y))) - n * 0.04; tilt = Vector((0, sg * 0.16, 0)); tip = base + (n + tilt).normalized() * 0.82
                        mb.frustum(base, tip, 0.2, 0.0, M_['iron'], seg=5, cap1=False)
                    x += 1.22
        sh['spikes'].append(mk(mb, '%s_spikes_%d' % (name, st + 1), ride, smooth=False))
    # --- gun ports (6 per side), lids on hinges, cannon muzzles
    sh['lids'] = []; sh['muzzles'] = []; mbs = MB(); gx = [-10.0 + 4.0 * i for i in range(6)]
    for i, x in enumerate(gx):
        b = t_b(x) * 1.004
        for sg in (-1, 1):
            cy_ = sg * b; mbs.oface([Vector((x - 0.55, cy_ + sg * 0.015, 1.3)), Vector((x + 0.55, cy_ + sg * 0.015, 1.3)), Vector((x + 0.55, cy_ + sg * 0.015, 2.2)), Vector((x - 0.55, cy_ + sg * 0.015, 2.2))], M_['port_dark'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
            for (dx, dz, w_, h_) in ((-0.62, 1.75, 0.08, 1.0), (0.62, 1.75, 0.08, 1.0), (0, 2.27, 1.3, 0.09), (0, 1.27, 1.3, 0.09)):
                cbox(mbs, (x + dx, cy_ + sg * 0.03, dz), w_ / 2 + 0.02, 0.07, h_ / 2, M_['red_d'])
            mbl = MB(); mbl.box((-0.56, 0.0, -0.9), (0.56, 0.07, 0.0), M_['red']); cbox(mbl, (0, 0.075, -0.45), 0.13, 0.02, 0.13, M_['gold'])
            lid = mk(mbl, '%s_lid_%d_%s' % (name, i, 'p' if sg > 0 else 's'), ride); lid.location = (x, cy_ + sg * 0.05, 2.2); lid.rotation_mode = 'XYZ'
            if sg < 0: lid.rotation_euler = (0, 0, math.pi); lid.location = (x, cy_ - sg * 0.0 + sg * 0.05, 2.2)
            sh['lids'].append((lid, sg))
            mbm = MB(); rod(mbm, (0, -1.1, 0), (0, 0.55, 0), 0.3, M_['cannon'], seg=10); rod(mbm, (0, 0.5, 0), (0, 0.75, 0), 0.37, M_['cannon'], seg=10); rod(mbm, (0, -0.2, 0), (0, 0.2, 0), 0.36, M_['cannon'], seg=10)
            mz = mk(mbm, '%s_muzzle_%d_%s' % (name, i, 'p' if sg > 0 else 's'), ride); mz.location = (x, cy_, 1.75)
            if sg < 0: mz.rotation_mode = 'XYZ'; mz.rotation_euler = (0, 0, math.pi)
            mz.hide_render = True; sh['muzzles'].append(mz); sh['guns'].append(dict(local=Vector((x, cy_ + sg * 0.9, 1.75)), dir=Vector((0, sg, 0.15)).normalized(), name='%s_g%d%s' % (name, i, 'p' if sg > 0 else 's')))
    mk(mbs, name + '_ports', ride)
    # --- carved dragon head at the bow
    dragon(sh)
    # --- turtle tail, rudder, stem post
    mb = MB(); rod(mb, (-16.2, 0, 0.3), (-19.4, 0, 2.2), 0.62, M_['wood_d'], seg=8, r1=0.3); beam(mb, (-17.3, 0, -1.4), (-17.3, 0, 2.0), 0.18, 0.9, M_['wood_d'], up=(1, 0, 0)); rod(mb, (16.3, 0, -0.8), (17.4, 0, 2.3), 0.55, M_['wood_d'], seg=8, r1=0.4)
    cbox(mb, (-18.9, 0, 2.5), 0.5, 0.2, 0.12, M_['gold']); mk(mb, name + '_tail', ride)
    # --- oars
    ox = [-11.5 + 2.55 * i for i in range(10)]; oy = [t_b(x) + 0.04 for x in ox]
    oar_set(sh, ox, oy, 1.0, dip=(sea if oars_dip is None else oars_dip), stroke=sea)
    # --- two masts (kept up), stays, flags; matting sails at sea
    for mi, mx in enumerate((5.0, -6.0)):
        zb = roof_z(mx, 0) + 0.1; H_ = 8.2 if mi == 0 else 6.6; mb = MB(); rod(mb, (mx, 0, zb), (mx, 0, zb + H_), 0.17, M_['wood_l'], seg=8, r1=0.11)
        beam(mb, (mx - 0.1, -2.6, zb + H_ * 0.82), (mx - 0.1, 2.6, zb + H_ * 0.82), 0.1, 0.1, M_['wood_l'])
        for (yy, ex) in ((3.2, 0), (-3.2, 0)): rod(mb, (mx, 0, zb + H_ * 0.9), (mx + 0.3 * (1 if mi else -1), yy * 1.45, roof_z(mx, yy * 1.45) + 0.05), 0.025, M_['rope'], seg=4)
        mk(mb, '%s_mast%d' % (name, mi), ride); sh['masts'].append((mx, zb, H_))
        flag_obj(sh, 'flag_tri_red' if mi == 0 else 'flag_tri_blue', (mx, 0, zb + H_), 0.5, 1.9, 0.12, pole=False, name='%s_pen%d' % (name, mi), ph=mi)
        if sail and mi == 0:
            mb = MB(); sw, shh = 5.6, 4.6
            quad_grid(mb, lambda i, j: Vector((mx - 0.25 - 0.9 * math.sin(math.pi * j / 6) * math.sin(math.pi * i / 8) , -sw / 2 + sw * j / 6, zb + H_ * 0.82 - shh * i / 8)), 8, 6, M_['sail_k'], uvs=lambda i, j: (j / 6 * 1.4, i / 8 * 1.2), orient=lambda c: Vector((-1, 0, 0)))
            s_ = mk(mb, name + '_sail', ride, smooth=True)
    flag_obj(sh, 'flag_red', (-17.0, 0, 2.6), 4.2, 2.6, 0.25, name=name + '_stern', ph=1.5)
    return sh

def dragon(sh):
    """Carved dragon head: red + gold + teal, open mouth with teeth, horns, eyes, mane. Mouth centre = sh['mouth'] (ride-local)."""
    M_ = S['M']; ride = sh['ride']; mb = MB(); X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    rod(mb, (15.6, 0, 2.4), (17.5, 0, 3.7), 1.18, M_['teal'], seg=12, r1=0.95)
    ell(mb, (18.5, 0, 3.75), 1.3, 1.02, 0.98, M_['dragon_red'], 14, 9)
    a = math.radians(7); ax = (Vector((math.cos(a), 0, -math.sin(a))), Y, Vector((math.sin(a), 0, math.cos(a))))
    obox(mb, Vector((20.2, 0, 3.52)), *ax, 1.1, 0.64, 0.42, M_['dragon_red']); ell(mb, (21.25, 0, 3.4), 0.72, 0.64, 0.44, M_['dragon_red'], 12, 8)
    a2 = math.radians(24); ax2 = (Vector((math.cos(a2), 0, -math.sin(a2))), Y, Vector((math.sin(a2), 0, math.cos(a2)))); H = Vector((19.0, 0, 2.95))
    obox(mb, H + ax2[0] * 1.15 + ax2[2] * -0.15, *ax2, 1.15, 0.52, 0.2, M_['gold']); ell(mb, H + ax2[0] * 2.3 + ax2[2] * -0.15, 0.35, 0.5, 0.2, M_['gold'], 10, 6)
    obox(mb, Vector((19.9, 0, 3.12)), X, Y, Z, 0.95, 0.5, 0.3, M_['mouth']); ell(mb, (19.9, 0, 2.95), 0.75, 0.3, 0.14, M_['tongue'], 10, 6)
    for i in range(6):
        xx = 19.3 + 0.38 * i
        for sg in (-1, 1):
            cone(mb, (xx, sg * 0.5, 3.18), (xx + 0.03, sg * 0.5, 2.78), 0.085, M_['tooth'], 5)
            cone(mb, H + ax2[0] * (0.4 + 0.42 * i) + Vector((0, sg * 0.46, 0.0)) + ax2[2] * 0.0, H + ax2[0] * (0.4 + 0.42 * i) + Vector((0, sg * 0.46, 0.0)) + ax2[2] * 0.4, 0.07, M_['tooth'], 5)
    for sg in (-1, 1):
        ell(mb, (18.9, sg * 0.84, 4.12), 0.34, 0.2, 0.34, M_['eye_w'], 10, 6); ell(mb, (19.05, sg * 0.97, 4.13), 0.18, 0.1, 0.18, M_['eye_k'], 8, 5)
        beam(mb, (18.4, sg * 0.8, 4.55), (19.5, sg * 0.82, 4.4), 0.2, 0.12, M_['teal']); ell(mb, (21.45, sg * 0.25, 3.78), 0.1, 0.1, 0.08, M_['eye_k'], 6, 4)
        pts = [(18.1, sg * 0.5, 4.5), (17.3, sg * 0.75, 5.2), (16.4, sg * 1.0, 5.6), (15.6, sg * 1.2, 5.45)]
        for k in range(3): rod(mb, pts[k], pts[k + 1], 0.27 - 0.08 * k, M_['gold'], seg=6, r1=0.27 - 0.08 * (k + 1))
        ell(mb, (17.4, sg * 1.2, 3.5), 0.15, 0.55, 0.45, M_['teal'], 8, 5)
    for k in range(6):
        xx = 18.0 - 0.45 * k; cone(mb, (xx, 0, 4.55 - 0.05 * k), (xx - 0.9, 0, 5.2 + 0.08 * k - 0.1 * k), 0.3 - 0.02 * k, M_['dragon_red'] if k % 2 == 0 else M_['gold'], 5)
    sh['dragon'] = mk(mb, sh['name'] + '_dragon', ride); sh['mouth'] = Vector((20.4, 0, 3.15))
