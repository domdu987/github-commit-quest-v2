"""Props + per-frame FX for EP.2-4 of ช่างเชื่อมสายฟ้า remake, built into whichever set is loaded (soi3d / nurs3d / room3d).
Static props (call once after SET.build): fuse_box, charge_table, cable, poster, recolor.
Per-frame FX (into an office3d.MB): blast, rain, glow_body, current_along.
All materials are office3d toon materials (mat_lit / mat_emit) so props sit in the set's light model."""
import os, math, random
import bpy
from mathutils import Vector, Matrix, Euler
import office3d as S
HERE = os.path.dirname(os.path.abspath(__file__)); TXD = os.path.join(HERE, 'props_tex')
def TX(k): return os.path.join(TXD, k + '.png')
def G(): return S.STATE.get('P', {}).get('gain', 0.6)

def lit(name, img=None, color='#808080', gain=1.4, alpha=False, shade=1.0):
    return S.mat_lit('PR_' + name, color=color, image=img and TX(img), gain=gain * G(), shade_mul=shade, alpha=alpha, form=(0.0, 0.0, 0.2))
def emit(name, color='#ffffff', strength=1.0, img=None): return S.mat_emit('PR_E_' + name, color, image=img and TX(img), strength=strength)
def glow_mat(name, color, strength, opacity):
    """Transparent emissive (camera rays only): halos, fire and the welder's glow."""
    m = bpy.data.materials.get('PR_G_' + name)
    if m: return m
    m = bpy.data.materials.new('PR_G_' + name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    emi.inputs['Color'].default_value = (*S.hex_lin(color), 1); emi.inputs['Strength'].default_value = strength
    add = nt.nodes.new('ShaderNodeMixShader'); add.inputs['Fac'].default_value = opacity
    L(tr.outputs['BSDF'], add.inputs[1]); L(emi.outputs['Emission'], add.inputs[2]); L(add.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; return m

def _place(ob, loc, yaw):
    ob.location = Vector(loc); ob.rotation_euler = (0, 0, yaw); S.no_bounce(ob); return ob

def coll():
    return S._coll('PROPS', bpy.context.scene)

# ----------------------------------------------------------------------------- Kim's old fuse box (pole / wall mounted)
def fuse_box(loc, yaw, door_deg=0.0, plate_deg=0.0, w=0.56, h=0.76, dep=0.2, name='fusebox'):
    """loc = centre of the back face at the bottom edge (on the wall), yaw = rotation about z (front faces local -y).
    door_deg: 0 shut .. 115 wide open (swings toward the viewer, hinge on the left). plate_deg: inner steel plate, 0 shut .. 100 open (hinge at its bottom)."""
    c = coll(); body = lit('fb_body', 'fb_body'); mb = S.MB()
    mb.box((-w / 2, -dep, 0), (w / 2, 0, h), body, mats=dict(front=lit('fb_breakers', 'fb_breakers', gain=1.3)))
    mb.box((-w / 2 - 0.03, -dep - 0.01, h), (w / 2 + 0.03, 0.02, h + 0.04), lit('fb_rim', color='#5f7a6c'))           # little rain roof
    mb.frustum((-w / 2 + 0.08, -dep / 2, 0), (-w / 2 + 0.08, -dep / 2, -0.9), 0.03, 0.03, lit('conduit', color='#4b5a54'), seg=8)   # conduit to the ground
    mb.frustum((w / 2 - 0.1, -dep / 2, h + 0.04), (w / 2 - 0.1, -dep / 2, h + 0.6), 0.02, 0.02, lit('wire_k', color='#222226'), seg=6)
    # the engraved brass plate, then the steel plate that hides it (upper middle of the panel)
    pw, ph, pz = 0.34, 0.44, 0.27
    mb.quad((-pw / 2, -dep - 0.004, pz), (pw, 0, 0), (0, 0, ph), lit('fb_engraved', 'fb_engraved', gain=1.5))
    ob = _place(mb.obj(name, c), loc, yaw)
    dm = S.MB(); dm.box((0, -0.018, 0), (w, 0, h), body, mats=dict(front=lit('fb_door_out', 'fb_door_out'), back=lit('fb_door_in', 'fb_door_in', gain=1.5)))
    door = dm.obj(name + '_door', c); door.parent = ob; door.location = (-w / 2, -dep, 0); door.rotation_euler = (0, 0, -math.radians(door_deg)); S.no_bounce(door)
    pm = S.MB(); pm.box((-pw / 2 - 0.01, -0.012, 0), (pw / 2 + 0.01, 0, ph + 0.01), lit('fb_plate', 'fb_plate', gain=1.3))
    plate = pm.obj(name + '_plate', c); plate.parent = ob; plate.location = (0, -dep - 0.006, pz - 0.005); plate.rotation_euler = (-math.radians(plate_deg), 0, 0); S.no_bounce(plate)
    return dict(box=ob, door=door, plate=plate, front=tuple(ob.matrix_world @ Vector((0, -dep - 0.02, h * 0.6))))

def set_fuse(fb, door_deg=None, plate_deg=None):
    if door_deg is not None: fb['door'].rotation_euler = (0, 0, -math.radians(door_deg))
    if plate_deg is not None: fb['plate'].rotation_euler = (-math.radians(plate_deg), 0, 0)

# ----------------------------------------------------------------------------- Hong's charging table
def charge_table(loc, yaw, price=20, name='ctable'):
    c = coll(); mb = S.MB(); top = lit('ct_top', color='#e8e2d4'); leg = lit('ct_leg', color='#9aa0a8')
    mb.box((-0.6, -0.3, 0.70), (0.6, 0.3, 0.74), top)
    for x in (-0.55, 0.55):
        for y in (-0.25, 0.25): mb.frustum((x, y, 0), (x, y, 0.7), 0.018, 0.018, leg, seg=6)
    mb.box((-0.5, -0.18, 0.74), (-0.22, 0.08, 0.86), lit('ct_tin', color='#d23a34'), mats=dict(top=lit('ct_tin_top', color='#8a1e1a')))     # cash tin
    for k in range(5):                                                                                                # notes in the tin
        mb.box((-0.47 + k * 0.05, -0.15, 0.86), (-0.42 + k * 0.05, 0.05, 0.875), lit('ct_note%d' % (k % 2), color=['#6aa86a', '#c86ab0'][k % 2]))
    for k in range(4):                                                                                                # phones waiting
        x = 0.05 + k * 0.13; mb.box((x, -0.2, 0.74), (x + 0.08, -0.04, 0.752), lit('ct_ph', color='#1e1e24'), mats=dict(top=emit('ct_scr%d' % (k % 2), ['#9dffb0', '#7fd8ff'][k % 2], 1.2)))
    ob = _place(mb.obj(name, c), loc, yaw)
    sm = S.MB(); tex = lit('sign%d' % price, 'sign%d' % price, gain=1.5)
    sm.quad((-0.42, 0.0, 0.0), (0.84, 0, 0), (0, 0.18, 0.62), tex)
    sm.quad((0.42, 0.006, 0.0), (-0.84, 0, 0), (0, 0.18, 0.62), lit('ct_card', color='#b8885a'))
    sign = sm.obj(name + '_sign', c); sign.parent = ob; sign.location = (0.0, 0.32, 0.74); S.no_bounce(sign)
    return dict(table=ob, sign=sign, cash=tuple(ob.matrix_world @ Vector((-0.36, -0.05, 0.9))))

def cable(p0, p1, sag=0.25, r=0.028, name='cable', n=28, clamp=True):
    """Thick black cable along a sagging curve (Hong's jumper lead)."""
    mb = S.MB(); m = lit('cable', color='#18181c'); p0, p1 = Vector(p0), Vector(p1); pts = []
    for i in range(n + 1):
        u = i / n; q = p0.lerp(p1, u) + Vector((0, 0, -sag * 4 * u * (1 - u))); pts.append(q)
    for a, b in zip(pts[:-1], pts[1:]): mb.frustum(tuple(a), tuple(b), r, r, m, seg=6)
    if clamp:
        cm = lit('clamp', color='#d23a34')
        for p in (p0, p1): mb.box(tuple(p - Vector((0.05, 0.03, 0.04))), tuple(p + Vector((0.05, 0.03, 0.04))), cm)
    ob = mb.obj(name, coll()); S.no_bounce(ob); return pts

def poster(corner, u, v, img, name='poster', gain=1.4):
    mb = S.MB(); mb.quad(corner, u, v, lit(img, img, gain=gain)); ob = mb.obj(name, coll()); S.no_bounce(ob); return ob

def recolor(hex_sub, new_hex):
    """Change the base colour of every set material whose name contains hex_sub (e.g. the banana bunch)."""
    col = S.hex_lin(new_hex); n = 0
    for m in bpy.data.materials:
        if hex_sub in m.name and m.node_tree:
            for nd in m.node_tree.nodes:
                if nd.bl_idname == 'ShaderNodeMix' and nd.blend_type == 'MULTIPLY': nd.inputs[6].default_value = (*col, 1)
                if nd.bl_idname == 'ShaderNodeVectorMath' and nd.operation == 'SCALE' and not nd.inputs[0].is_linked: nd.inputs[0].default_value = col
            n += 1
    return n

def lerp_hex(a, b, u):
    a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(x + (y - x) * max(0, min(1, u))) for x, y in zip(a, b))

# ----------------------------------------------------------------------------- per-frame FX
def blast(mb, c, u, g):
    """Transformer explosion, u = seconds since the bang: white core -> fireball -> rolling dark smoke, plus burning drips and sparks."""
    c = Vector(c); r = random.Random(g * 13 + 5)
    core = glow_mat('blast_core', '#fff8e0', 30.0, 1.0); fire = glow_mat('blast_fire', '#ffa040', 12.0, 0.9); fire2 = glow_mat('blast_fire2', '#ff5a20', 6.0, 0.75)
    smoke = S.mat_lit('PR_smoke', color='#3a3640', gain=0.35 * G())
    if u < 0: return
    if u < 0.25: mb.sphere(tuple(c), 0.4 + 2.4 * u, core, seg=16, rings=10)
    rr = random.Random(41)
    for k in range(16):                                                    # fire puffs expanding and rising
        d = Vector((rr.uniform(-1, 1), rr.uniform(-1, 1), rr.uniform(-0.3, 1.0))).normalized(); life = rr.uniform(0.9, 2.0)
        if u > life: continue
        k_ = u / life; p = c + d * (0.3 + 1.6 * math.sqrt(k_)) + Vector((0, 0, 0.8 * k_))
        mb.sphere(tuple(p), 0.25 + 0.55 * math.sin(math.pi * min(1, k_ * 1.3)), fire if k % 3 else fire2, seg=12, rings=7)
    for k in range(14):                                                    # smoke takes over
        d = Vector((rr.uniform(-1, 1), rr.uniform(-1, 1), rr.uniform(0.2, 1.0))).normalized(); t0 = rr.uniform(0.3, 1.2)
        if u < t0: continue
        q = u - t0; p = c + d * (0.6 + 0.9 * q) + Vector((0, 0, 1.1 * q)); mb.sphere(tuple(p), 0.3 + 0.35 * q, smoke, seg=10, rings=6)
    em = S.mat_emit('PR_E_spark', '#fff2b0', strength=14.0); emo = S.mat_emit('PR_E_spark_o', '#ffb050', strength=10.0)
    for k in range(70):                                                    # ballistic sparks
        rs = random.Random(700 + k); v = Vector((rs.uniform(-1, 1), rs.uniform(-1, 1), rs.uniform(-0.1, 1.3))).normalized() * rs.uniform(4, 11); life = rs.uniform(0.5, 1.8)
        if u > life: continue
        p = c + v * u + Vector((0, 0, -4.9 * u * u)); vel = v + Vector((0, 0, -9.8 * u)); tail = p - vel.normalized() * min(0.6, 0.05 + vel.length * 0.035)
        mb.frustum(tuple(tail), tuple(p), 0.004, 0.02 * (1 - u / life) + 0.006, em if k % 3 else emo, seg=4)
    if u > 0.5:                                                            # burning oil dripping from the can
        for k in range(5):
            q = (u * 1.3 + k * 0.21) % 1.0; p = c + Vector((0.2 * math.sin(k * 2.0), 0.15 * math.cos(k), -0.5 - 6.5 * q * q)); mb.sphere(tuple(p), 0.05, fire2, seg=6, rings=4)

def rain(mb, cam_loc, fwd, t, n=700, spread=7.0, near=0.8, far=12.0, speed=14.0, seed=3):
    """Falling streaks in front of the camera (camera-only glow material)."""
    m = glow_mat('rain', '#cfe0ff', 1.6, 0.55); r = random.Random(seed); cam = Vector(cam_loc); f = Vector(fwd).normalized()
    side = f.cross(Vector((0, 0, 1))).normalized(); up = Vector((0, 0, 1))
    for k in range(n):
        d = r.uniform(near, far); x = r.uniform(-1, 1) * spread * d / far + r.uniform(-0.4, 0.4); z0 = r.uniform(-3, 4)
        z = ((z0 - t * speed) % 7.0) - 3.0; p = cam + f * d + side * x + up * z; L = 0.35 + 0.02 * d
        mb.frustum(tuple(p), tuple(p + Vector((0.04, 0.0, -L))), 0.004 + 0.0008 * d, 0.004 + 0.0008 * d, m, seg=3, cap0=False, cap1=False)

def glow_body(mb, feet, t, level=1.0, height=1.9, g=0):
    """The welder at 100%: a blue aura around his card + crackling arcs; level 0..1."""
    if level <= 0: return
    p = Vector(feet); halo = glow_mat('halo%d' % int(level * 20), '#7fd0ff', 1.4 * level, 0.07 * level); halo2 = glow_mat('halo2_%d' % int(level * 20), '#bfefff', 2.0 * level, 0.035 * level)
    mb.sphere(tuple(p + Vector((0, 0, height * 0.55))), 0.75 + 0.05 * math.sin(t * 9), halo, seg=18, rings=12)
    mb.sphere(tuple(p + Vector((0, 0, height * 0.55))), 1.0 + 0.08 * math.sin(t * 6), halo2, seg=18, rings=12)
    boltc = S.mat_emit('PR_E_arc', '#ffffff', strength=30.0 * level); bolth = S.mat_emit('PR_E_arch', '#8fd8ff', strength=3.0 * level)
    for k in range(int(4 + 6 * level)):
        ra = random.Random(g * 17 + k); a = p + Vector((ra.uniform(-0.5, 0.5), ra.uniform(-0.5, 0.5), ra.uniform(0.2, height + 0.3)))
        b = a + Vector((ra.uniform(-0.8, 0.8), ra.uniform(-0.8, 0.8), ra.uniform(-0.6, 0.6))); pts = [a]
        for q in range(1, 6): pts.append(a.lerp(b, q / 6) + Vector((ra.uniform(-0.1, 0.1), ra.uniform(-0.1, 0.1), ra.uniform(-0.1, 0.1))))
        pts.append(b)
        for p0, p1 in zip(pts[:-1], pts[1:]): mb.frustum(tuple(p0), tuple(p1), 0.008, 0.008, boltc, seg=4); mb.frustum(tuple(p0), tuple(p1), 0.025, 0.025, bolth, seg=5)

def current_along(mb, pts, u, g, n=3, length=0.18):
    """Bright pulses running along a cable (list of Vectors), u = 0..1 position of the lead pulse."""
    boltc = S.mat_emit('PR_E_cur', '#ffffff', strength=30.0); bolth = S.mat_emit('PR_E_curh', '#8fd8ff', strength=4.0)
    L = len(pts) - 1
    for k in range(n):
        uu = u - k * 0.08
        if not 0 <= uu <= 1: continue
        i = min(L - 1, int(uu * L)); f = uu * L - i; c = pts[i].lerp(pts[i + 1], f)
        mb.sphere(tuple(c), 0.06 - 0.012 * k, boltc, seg=8, rings=5); mb.sphere(tuple(c), 0.16 - 0.03 * k, glow_mat('curh', '#8fd8ff', 4.0, 0.4), seg=10, rings=6)
        ra = random.Random(g * 7 + k)
        for q in range(4):
            a = c; b = c + Vector((ra.uniform(-0.3, 0.3), ra.uniform(-0.3, 0.3), ra.uniform(-0.2, 0.3))); mb.frustum(tuple(a), tuple(b), 0.006, 0.002, boltc, seg=4)
