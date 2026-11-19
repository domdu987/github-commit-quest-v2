
# ================================================================== common helpers (set3d19)
def metal_mat(name, A, B, rough=0.3, scale=6.0, spec=0.6, metallic=0.0):
    m = mat(name, A, B, scale=scale, rough=rough, sheen=spec)
    bs = m.node_tree.nodes.get('Principled BSDF')
    if bs: bs.inputs['Metallic'].default_value = metallic
    return m

def gear(mb, m, c, r, nt=12, th=0.04, rim=0.03, spokes=4, tooth=0.035, rot=(0, 0, 0), hub=0.05, n=16):
    """wooden/brass gear wheel built from boxes: rim ring, teeth, spokes, hub. Built in the XZ plane (axis y); rot orients it."""
    mb.push(Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4())
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.10
        mb.box(m, (r * math.cos(a), 0, r * math.sin(a)), (seg, th, rim), ry=-(a + math.pi / 2))
    for i in range(nt):
        a = 2 * math.pi * i / nt; rr = r + tooth * .45 + rim / 2
        mb.box(m, (rr * math.cos(a), 0, rr * math.sin(a)), (tooth, th, tooth * 1.1), ry=-a)
    for i in range(spokes):
        a = math.pi * i / spokes
        mb.box(m, (0, 0, 0), (2 * r, th * .8, rim * .8), ry=-a)
    mb.cyl(m, (0, 0, 0), hub, th * 1.7, axis='y', seg=12)
    mb.pop()

def ring_xy(mb, m, c, r, w, h, n=14):
    """flat ring (rope coil / hoop) in the XY plane, section w (radial) x h (z)"""
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]), (seg, w, h), rz=a + math.pi / 2)

def ring_xz(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), (seg, h, w), ry=-(a + math.pi / 2))

def curl_old(mb, m, p, rr, s=1.0):
    """wood shaving: a short curled ribbon (chain of thin boxes along an arc)"""
    a0 = rr.uniform(0, 6.28); r = rr.uniform(0.03, 0.055) * s; n = 7; turn = rr.uniform(4.0, 6.5); yaw = rr.uniform(0, 6.28)
    pts = []
    for i in range(n + 1):
        t = i / n * turn; pts.append((r * (1 + 0.25 * i / n) * math.cos(a0 + t), 0.012 * i * s * 3, r * (1 + 0.25 * i / n) * math.sin(a0 + t) + r * 1.1))
    mb.push(Matrix.Translation(p) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(n):
        a = Vector(pts[i]); b = Vector(pts[i + 1]); d = b - a
        mb.rod(m, a, b, 0.0075 * s, 0.0075 * s, seg=4, caps=False)
    mb.pop()

def pile(mb, m, c, s, rr):
    mb.ell(m, (c[0], c[1], c[2] + 0.02 * s), (0.16 * s, 0.12 * s, 0.045 * s), (10, 6))

def hang_saw(mb, M, c, ln=0.62, rz=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, rz, 0)).to_matrix().to_4x4())
    mb.box(M['steel'], (0, 0, 0), (ln, 0.012, 0.075))
    mb.box(M['iron'], (0, -0.008, -0.04), (ln, 0.01, 0.014))
    mb.box(M['oakd'], (ln / 2 + 0.06, -0.01, 0.0), (0.12, 0.035, 0.11))
    mb.pop()

def sphere_brass(mb, m, c, r): mb.ell(m, c, (r, r, r), (14, 10))

def area_light(name, loc, rot, size, col, en, cam=False):
    sc = bpy.context.scene
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = size[0]; l.size_y = size[1]; l.color = col; l.energy = en
    ob = bpy.data.objects.new(name, l); ob.location = loc; ob.rotation_euler = rot; sc.collection.objects.link(ob); ob.visible_camera = cam; return ob
def point_light(name, loc, col, en, r=0.1):
    sc = bpy.context.scene
    l = bpy.data.lights.new(name, 'POINT'); l.color = col; l.energy = en; l.shadow_soft_size = r
    ob = bpy.data.objects.new(name, l); ob.location = loc; sc.collection.objects.link(ob); return ob
def sun_light(P):
    sc = bpy.context.scene; k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()

def flat_world(col, k, env=('#ffd6a0', 2.2)):
    """interior world: camera/diffuse rays see a flat colour (strength k, 0 = none); glossy rays see a warm room-like environment so brass reads as metal"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); b1 = N('ShaderNodeBackground'); b1.inputs['Color'].default_value = hexc(col); b1.inputs['Strength'].default_value = k
    b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(env[0]); b2.inputs['Strength'].default_value = env[1]
    lp = N('ShaderNodeLightPath'); mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Glossy Ray'], mx.inputs[0]); L(b1.outputs[0], mx.inputs[1]); L(b2.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])

def card(mb, m, x, y, h=1.62, w=0.7, z0=0.0):
    """flat grey 2D-puppet placeholder card (3 D tall = 1.62 m)"""
    mb.box(m, (x, y, z0 + h / 2), (w, 0.02, h))
    mb.ell(m, (x, y, z0 + h * 0.9), (0.2, 0.012, 0.2), (14, 10))

def curl(mb, m, p, rr, s=1.0):
    """wood shaving: a curled flat ribbon (chain of thin flat boxes along a loose spiral)"""
    a0 = rr.uniform(0, 6.28); r0 = rr.uniform(0.05, 0.08) * s; n = 10; turn = rr.uniform(0.7, 1.3); yaw = rr.uniform(0, 6.28)
    pts = [Vector((r0 * (1 - 0.35 * i / n) * math.cos(a0 + i / n * turn * 2 * math.pi), 0.012 * i * s, r0 * (1 - 0.35 * i / n) * math.sin(a0 + i / n * turn * 2 * math.pi) + r0 * 1.15)) for i in range(n + 1)]
    mb.push(Matrix.Translation(p) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(n):
        a = pts[i]; b = pts[i + 1]; d = b - a
        mb.push(Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()); mb.box(m, (0, 0, 0), (0.034 * s, 0.006, d.length * 1.15)); mb.pop()
    mb.pop()

def shafts(P, rect, zfloor=0.0, n=1):
    """faint light-shaft volume: the window rectangle projected along the sun direction to the floor (emission/transparent mix, no shadows)"""
    kd = Vector(P['key_dir']).normalized(); (x0, x1, z0, z1, y) = rect
    corners = [Vector((x0, y, z0)), Vector((x1, y, z0)), Vector((x1, y, z1)), Vector((x0, y, z1))]
    proj = [c + kd * ((zfloor - c.z) / kd.z) for c in corners]
    m = bpy.data.materials.new('shaft'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc('#ffd890'); em.inputs['Strength'].default_value = P.get('shaft_k', 4.0); mx.inputs[0].default_value = P.get('shaft_a', 0.004)
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    mb = MB('shafts')
    for i in range(4):
        j = (i + 1) % 4; mb.quad(m, [corners[i], corners[j], proj[j], proj[i]]); mb.quad(m, [proj[i], proj[j], corners[j], corners[i]])
    mb.finish(shadow=False)
