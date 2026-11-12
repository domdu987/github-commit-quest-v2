#!/usr/bin/env python3
"""shot.py -- film 2 take s20: shots 20 + 21, the disaster (g 1660..1843, out-handle g 1844..1852 for the 15f dissolve into s22).
Hard cut in from s19, hard cuts inside. Timed on the narration words (captions.json), see QA.md for the plan differences.

    20a g 1660..1707  tower NIGHT_STORM spire_insert (no rod). g 1660 white flash + bolt hits the empty finial (cut lands 3 f
                      before "ฟ้าผ่าลงยอด" g 1663, re-strike on it), camera jolts; the finial glows hot, a glowing crack starts down
                      the spire; second flicker + snap punch-in on "หอระฆังพอดี" (g 1686).
    20b g 1708..1743  hard cut on "ไฟวิ่งลงตามกำแพง": tower NIGHT_STORM tower_side_mid, the glow runs down the west wall of the
                      tower (a crack of fire, with a moving orange light at its head), the camera tilts down after it to the ground.
    20c g 1744..1777  hard cut on "ลงไปถึงห้องใต้ดิน": vault BURN crack_follow, the glow runs along the vault crack from the stair
                      opening to the barrels (arrives g 1771), flicker, then the barrels flare (orange-white) into the cut.
    21  g 1778..1852  hard cut on "แล้วหอระฆังทั้งหอ": tower NIGHT_STORM town_wide. White flash; the whole bell tower lifts into the
                      sky on a column of fire and smoke (built here at runtime: fire puffs, smoke puffs, ground ring, debris,
                      two fire lights); the camera tilts up after it. No people. Out-handle g 1844..1852 (3D, continues).

    python3 shot.py stills <sub a|b|c|d> <a:b:step> <out_dir> [scale] [samples]
    python3 shot.py final <sub> <a:b>
    python3 shot.py deliver
"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s19"))
import fx
from fx import g_of, g_cut

G20 = g_cut(55.35)               # 1660
G_SIDE = g_cut(56.943)           # 1708  "ไฟวิ่งลงตาม"
G_VAULT = g_cut(58.132)          # 1744  "ลงไปถึง"
G21 = g_cut(59.26)               # 1778
G_END = g_cut(61.45)             # 1844 (exclusive)
DISS_OUT = 15
H_OUT = DISS_OUT // 2 + 2        # 9
LAST = G_END + H_OUT - 1         # 1852
G_STRIKE = g_of(55.343)          # 1663
G_STRIKE2 = g_of(56.081)         # 1686
G_LIFT = g_of(59.799)            # 1797 "ทั้งหอ"
G_FLY = g_of(60.379)             # 1814 "ก็ลอยขึ้นไป"
G_SKY = g_of(60.822)             # 1827 "บนฟ้า"
SUBS = {"a": (G20, G_SIDE - 1), "b": (G_SIDE, G_VAULT - 1), "c": (G_VAULT, G21 - 1), "d": (G21, LAST)}
FINIAL = (0.0, 0.0, 28.45)


def keys(g, ks, lin=0.15):
    from anim import keys as K, lerp
    return lerp(K(g, ks), K(g, [(f, v, "lin") for f, v, e in ks]), lin)


def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = (math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr))
    return tuple(look[i] - d[i] * dist for i in range(3))


def jolt(g, starts, amp, decay=0.45):
    dx = dz = 0.0
    for i, s in enumerate(starts):
        d = g - s
        if 0 <= d <= 10:
            a = amp * math.exp(-decay * d)
            dz += a * math.cos(d * 2.3 + i); dx += 0.7 * a * math.sin(d * 3.1 + 2 * i)
    return dx, dz


# ----------------------------------------------------------------------------- the strike (20a)
def strike(g):
    """(flash strength of the set, white card strength, bolt visible)"""
    tab = {G20: (3.0, 0.92, True), G20 + 1: (1.6, 0.45, True), G20 + 2: (0.4, 0.0, False), G_STRIKE: (2.6, 0.6, True),
           G_STRIKE + 1: (1.2, 0.2, True), G_STRIKE + 2: (1.8, 0.1, True), G_STRIKE + 3: (0.6, 0.0, True), G_STRIKE + 4: (0.3, 0.0, False),
           G_STRIKE2 - 1: (0.9, 0.0, True), G_STRIKE2: (2.0, 0.35, True), G_STRIKE2 + 1: (0.7, 0.0, True), G_STRIKE2 + 2: (1.2, 0.0, False)}
    if g in tab:
        return tab[g]
    return (0.08 if G_STRIKE + 5 <= g <= G_STRIKE + 7 else 0.0, 0.0, False)


def heat(g):
    """glow of the struck finial 0..1"""
    if g < G20:
        return 0.0
    return min(1.0, 0.55 + 0.45 * math.exp(-0.05 * (g - G20))) * (1.0 + 0.12 * math.sin(g * 1.7))


def cam_a(g):
    ks = [(G20, (3.6, 34.0, 13.0, 27.9), "sine"),
          (G_STRIKE2 - 2, (3.25, 37.0, 12.0, 27.8), "quint"),
          (G_STRIKE2 + 5, (2.35, 40.0, 7.0, 27.45), "sine"),
          (G_SIDE, (2.15, 42.5, 4.0, 27.2), "hold")]
    dist, yaw, pitch, lz = keys(g, ks)
    dx, dz = jolt(g, [G20, G_STRIKE, G_STRIKE2], 0.10)
    look = (dx * 0.7, -dx * 0.7, lz + dz)
    return sph(look, dist, yaw, pitch), look, 2.5 * dz / 0.1


def crack_u_a(g):              # reveal of the tower crack (arc fraction), 20a: finial -> base of the spire cone
    return keys(g, [(G_STRIKE + 2, 0.0, "sine"), (G_SIDE, 0.17, "hold")], 0.4) if g >= G_STRIKE + 2 else 0.0


def crack_u_b(g):              # 20b: from the cornice to the ground (arrives g 1737)
    return keys(g, [(G_SIDE, 0.12, "cubic_in"), (G_SIDE + 6, 0.24, "lin"), (G_VAULT - 7, 1.0, "hold")], 0.3)


def cam_b(g):
    ks = [(G_SIDE, ((-8.2, -7.5, 12.5), (-2.3, -0.9, 20.0)), "sine"),
          (G_SIDE + 14, ((-8.4, -7.7, 10.5), (-2.3, -0.9, 13.5)), "sine"),
          (G_VAULT, ((-8.6, -7.9, 6.8), (-2.3, -0.9, 3.6)), "hold")]
    v = keys(g, [(f, tuple(a) + tuple(b), e) for f, (a, b), e in ks])
    dx, dz = jolt(g, [G_SIDE], 0.12)
    return v[:3], (v[3] + dx, v[4], v[5] + dz), 0.0


# ----------------------------------------------------------------------------- the vault (20c)
G_ARRIVE = G21 - 7               # 1771: glow reaches the barrels


def crack_u_c(g):
    return keys(g, [(G_VAULT, 0.02, "sine"), (G_ARRIVE, 1.0, "hold")], 0.35)


def vault_flash(g):
    """(set flash, orange card)"""
    if g >= G_ARRIVE:
        d = g - G_ARRIVE
        return (1.0 + 0.5 * d, min(0.75, 0.05 * d * d))
    return (0.35 * math.sin(g * 1.9) * math.sin(g * 0.7 + 1), 0.0)


# ----------------------------------------------------------------------------- the lift (21)
def lift(g):
    """(z offset, tilt deg about y, tilt deg about x) of the tower"""
    t = g - G21
    if t < 0:
        return 0.0, 0.0, 0.0
    burst = 1.6 * (1 - math.exp(-0.35 * t))
    rise = 0.006 * max(0, t - 2) ** 1.9
    z = burst + rise
    return z, -4.5 * min(1.0, t / 60.0) ** 1.3, 1.8 * math.sin(t * 0.06)


def lift_flash(g):
    t = g - G21
    tab = {0: (2.6, 0.9), 1: (1.8, 0.5), 2: (1.2, 0.2), 3: (0.8, 0.05), 4: (0.5, 0.0)}
    if t in tab:
        return tab[t]
    if G_LIFT <= g <= G_LIFT + 2:
        return (0.6, 0.0)
    return (0.25 + 0.08 * math.sin(g * 1.3), 0.0)


def cam_d(g):
    zl = lift(g)[0]
    ks = [(G21, ((-12.6, -33.0, 7.6), (0.4, 0.0, 13.5)), "sine"),
          (G_FLY, ((-12.3, -32.6, 7.0), (0.4, 0.0, 15.5)), "sine"),
          (LAST + 1, ((-12.0, -32.2, 6.6), (0.4, 0.0, 21.0)), "hold")]
    v = keys(g, [(f, tuple(a) + tuple(b), e) for f, (a, b), e in ks], 0.25)
    dx, dz = jolt(g, [G21, G21 + 4, G_LIFT], 0.35, decay=0.3)
    return v[:3], (v[3] + dx, v[4], v[5] + dz), 1.5 * dx


# ----------------------------------------------------------------------------- runtime builders
def crack_path_tower(scene):
    """Points of the glowing crack: finial -> down the spire cone (south-west rib) -> over the parapet -> down the west face
    to the ground. Each point by a horizontal ray cast onto the set, 0.035 D proud."""
    from mathutils import Vector
    import bpy
    hidden = [o for o in bpy.data.objects if o.name.startswith(("bolt", "rod", "wire", "pigeons"))]
    for o in hidden:
        o.hide_viewport = True
    bpy.context.view_layer.update()
    dg = bpy_ctx().evaluated_depsgraph_get()
    r = random.Random(21); pts = []
    d = Vector((-0.72, -0.70, 0.0)).normalized()
    z = 28.35
    while z > 22.0:
        j = r.uniform(-0.12, 0.12); dd = Vector((d.x + j * 0.3, d.y - j * 0.3, 0)).normalized()
        o = Vector((0, 0, z)) + dd * 8.0
        hit, loc, nor, *_ = scene.ray_cast(dg, o, -dd, distance=8.0)
        if hit:
            pts.append(tuple(loc + dd * 0.035))
        z -= 0.14
    y = -0.85; z = 22.75
    while z > 0.05:
        y += r.uniform(-0.06, 0.06); y = max(-1.5, min(-0.3, y))
        o = Vector((-4.0, y, z))
        hit, loc, nor, *_ = scene.ray_cast(dg, o, Vector((1, 0, 0)), distance=2.2)
        if hit:
            pts.append(tuple(loc + Vector((-0.035, 0, 0))))
        z -= 0.18
    for o in hidden:
        o.hide_viewport = False
    return pts


def bpy_ctx():
    import bpy
    return bpy.context


def arc_point(pts, Ls, u):
    s = max(0.0, min(1.0, u)) * Ls[-1]
    for i in range(len(pts) - 1):
        if Ls[i + 1] >= s:
            t = (s - Ls[i]) / max(Ls[i + 1] - Ls[i], 1e-9)
            return tuple(pts[i][k] + (pts[i + 1][k] - pts[i][k]) * t for k in range(3))
    return pts[-1]


def curve(name, pts, radius, mat, coll=None):
    import bpy
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (*p, 1.0)
    cu.bevel_depth = radius; cu.bevel_resolution = 2; cu.use_fill_caps = True
    ob = bpy.data.objects.new(name, cu); (coll or bpy.context.scene.collection).objects.link(ob)
    ob.data.materials.append(mat); fx.no_bounce(ob)
    return ob


def puff_mat(name):
    """Smoke: painted two-tone, emission only. Object colour r = heat (fire light from below), g = shade variation.
    moon side cool grey-blue, shade blue-violet, underside warm cream/orange by heat."""
    import bpy
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); emi = N('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0
    geo = N('ShaderNodeNewGeometry'); oi = N('ShaderNodeObjectInfo'); sep = N('ShaderNodeSeparateColor'); L(oi.outputs['Color'], sep.inputs[0])
    moon = N('ShaderNodeVectorMath'); moon.operation = 'DOT_PRODUCT'; moon.inputs[1].default_value = (-0.50, -0.62, 0.60); L(geo.outputs['Normal'], moon.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'; mr.inputs[1].default_value = 0.05; mr.inputs[2].default_value = 0.45
    L(moon.outputs['Value'], mr.inputs[0])
    lo = N('ShaderNodeVectorMath'); lo.operation = 'DOT_PRODUCT'; lo.inputs[1].default_value = (0.25, 0.35, -0.90); L(geo.outputs['Normal'], lo.inputs[0])
    lr = N('ShaderNodeMapRange'); lr.interpolation_type = 'SMOOTHSTEP'; lr.inputs[1].default_value = -0.35; lr.inputs[2].default_value = 0.35
    L(lo.outputs['Value'], lr.inputs[0])
    hm = N('ShaderNodeMath'); hm.operation = 'MULTIPLY'; L(lr.outputs[0], hm.inputs[0]); L(sep.outputs[0], hm.inputs[1])
    # also a heat base on all sides (smoke near the fire is glowing through)
    hb = N('ShaderNodeMath'); hb.operation = 'MULTIPLY'; hb.inputs[1].default_value = 0.35; L(sep.outputs[0], hb.inputs[0])
    hs = N('ShaderNodeMath'); hs.operation = 'ADD'; hs.use_clamp = True; L(hm.outputs[0], hs.inputs[0]); L(hb.outputs[0], hs.inputs[1])
    c1 = N('ShaderNodeMix'); c1.data_type = 'RGBA'; L(mr.outputs[0], c1.inputs[0])
    c1.inputs[6].default_value = (0.030, 0.026, 0.085, 1); c1.inputs[7].default_value = (0.14, 0.135, 0.27, 1)
    c2 = N('ShaderNodeMix'); c2.data_type = 'RGBA'; L(hs.outputs[0], c2.inputs[0]); L(c1.outputs[2], c2.inputs[6])
    c2.inputs[7].default_value = (1.35, 0.62, 0.22, 1)
    # shade variation per puff
    vm = N('ShaderNodeMath'); vm.operation = 'MULTIPLY_ADD'; vm.inputs[1].default_value = 0.5; vm.inputs[2].default_value = 0.75; L(sep.outputs[1], vm.inputs[0])
    sc = N('ShaderNodeVectorMath'); sc.operation = 'SCALE'; L(c2.outputs[2], sc.inputs[0]); L(vm.outputs[0], sc.inputs['Scale'])
    L(sc.outputs['Vector'], emi.inputs['Color']); L(emi.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


def fire_mat(name):
    """Fire: emission, object colour r = temperature (1 white-yellow .. 0 deep orange-red), g = strength / 6."""
    import bpy
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); emi = N('ShaderNodeEmission')
    geo = N('ShaderNodeLayerWeight'); geo.inputs['Blend'].default_value = 0.35
    oi = N('ShaderNodeObjectInfo'); sep = N('ShaderNodeSeparateColor'); L(oi.outputs['Color'], sep.inputs[0])
    # hotter in the middle of each puff (facing), cooler at the rim
    rim = N('ShaderNodeMath'); rim.operation = 'MULTIPLY_ADD'; rim.inputs[1].default_value = -0.6; L(geo.outputs['Facing'], rim.inputs[0]); L(sep.outputs[0], rim.inputs[2])
    ramp = N('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (0.75, 0.10, 0.02, 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (1.0, 0.92, 0.55, 1)
    e = cr.elements.new(0.45); e.color = (1.0, 0.38, 0.05, 1)
    L(rim.outputs[0], ramp.inputs[0])
    st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = 6.0; L(sep.outputs[1], st.inputs[0])
    L(ramp.outputs['Color'], emi.inputs['Color']); L(st.outputs[0], emi.inputs['Strength'])
    L(emi.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


class Column(object):
    """The column of fire and smoke under the rising tower + a ground ring + flying debris. Deterministic in g."""

    def __init__(self, T):
        import bpy
        self.coll = bpy.data.collections.new("S20_COLUMN"); bpy.context.scene.collection.children.link(self.coll)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0)
        ico = bpy.context.active_object; me = ico.data
        for p in me.polygons:
            p.use_smooth = True
        bpy.data.objects.remove(ico)
        self.me = me
        self.smoke_m = puff_mat("S20_smoke"); self.fire_m = fire_mat("S20_fire")
        r = random.Random(1769)
        self.fire, self.smoke, self.ring, self.debris = [], [], [], []

        def mk(nm, lst, n):
            for i in range(n):
                ob = bpy.data.objects.new("%s_%03d" % (nm, i), me)
                self.coll.objects.link(ob); lst.append(ob)
        mk("fire", self.fire, 70); mk("smoke", self.smoke, 150); mk("ring", self.ring, 36)
        self.me.materials.append(self.smoke_m)
        for ob in self.fire:                         # object-level material link
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = self.fire_m
            fx.no_bounce(ob)
        for ob in self.smoke + self.ring:
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = self.smoke_m
            fx.no_bounce(ob); ob.visible_shadow = True
        self.pf = [(r.random(), r.uniform(0, 2 * math.pi), r.uniform(0.0, 1.0), r.uniform(0.8, 1.25), r.random()) for _ in self.fire]
        self.ps = [(r.random(), math.radians(69 + r.uniform(-125, 125)), r.uniform(0.6, 1.0), r.uniform(0.8, 1.3), r.random(), r.uniform(0, 14)) for _ in self.smoke]
        self.pr = [(i / len(self.ring) * 2 * math.pi + r.uniform(-0.1, 0.1), r.uniform(0.8, 1.2), r.random()) for i in range(len(self.ring))]
        brick = T.mat_lit("S20_debris", color="#8a4a30", gain=1.0)
        dark = T.mat_lit("S20_debris_d", color="#4a3040", gain=1.0)
        bpy.ops.mesh.primitive_cube_add(size=1.0); cube = bpy.context.active_object; cme = cube.data; bpy.data.objects.remove(cube)
        cme.materials.append(brick)
        self.pd = []
        for i in range(44):
            ob = bpy.data.objects.new("debris_%02d" % i, cme); self.coll.objects.link(ob)
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = brick if i % 3 else dark
            fx.no_bounce(ob); ob.visible_shadow = True
            a = r.uniform(0, 2 * math.pi); self.debris.append(ob)
            self.pd.append(dict(a=a, z0=r.uniform(0.3, 9.0), vr=r.uniform(0.22, 0.55), vz=r.uniform(0.25, 0.85), s=r.uniform(0.18, 0.5),
                                spin=(r.uniform(-0.4, 0.4), r.uniform(-0.4, 0.4), r.uniform(-0.4, 0.4)), b=G21 + r.randint(0, 3)))
        # fire lights: one at the foot of the column, one under the tower
        self.l1 = bpy.data.lights.new("S20_fire_l1", 'POINT'); self.l1.color = (1.0, 0.45, 0.12); self.l1.shadow_soft_size = 1.5
        o1 = bpy.data.objects.new("S20_fire_l1", self.l1); self.coll.objects.link(o1); o1.location = (0.0, -1.0, 2.5)
        self.l2 = bpy.data.lights.new("S20_fire_l2", 'POINT'); self.l2.color = (1.0, 0.55, 0.18); self.l2.shadow_soft_size = 1.0
        self.o2 = bpy.data.objects.new("S20_fire_l2", self.l2); self.coll.objects.link(self.o2)
        for l in (self.l1, self.l2):
            l.use_soft_falloff = False

    def update(self, g):
        t = g - G21
        zb = lift(g)[0]                          # tower bottom
        top = zb + 1.0
        on = t >= 0
        for ob, (ph, a, rr, k, v) in zip(self.fire, self.pf):
            h = ((ph + 0.035 * t * k) % 1.0)
            z = h * max(top, 1.2) + 0.2
            rad = (0.5 + 1.6 * rr) * (1.0 - 0.25 * h)
            aa = a + 0.05 * t
            ob.location = (rad * math.cos(aa) - 0.3, rad * math.sin(aa) - 0.8, z)
            s = (1.4 + 1.0 * v) * k * (0.8 + 0.4 * min(1.0, t / 6.0)) * (1.0 if zb > 2.5 or h < 0.8 else 0.8)
            ob.scale = (s, s, s * 1.25)
            ob.color = (max(0.0, 1.0 - 0.9 * h) * 0.8 + 0.2 * v, (0.55 + 0.35 * (1 - h)) * (1.0 + 0.6 * math.exp(-0.25 * max(t, 0))), 0, 1)
            ob.hide_render = not on
        for i, (ob, (ph, a, rr, k, v, d0)) in enumerate(zip(self.smoke, self.ps)):
            born = G21 + i * 0.22
            age = g - born
            if age < 0:
                ob.hide_render = True; continue
            ob.hide_render = False
            span = top + 9.0
            h = (ph + 0.022 * age * k) % 1.0
            z = 0.5 + h * span
            near = abs(z - zb)
            rad = 2.0 + 1.4 * rr + 0.02 * age * rr
            if z > zb + 1.0:                        # beside and above the tower: hug it tighter, lag behind (it is a trail)
                rad = 2.3 + 0.8 * rr
            aa = a + 0.02 * t * (1 if i % 2 else -1)
            ob.location = (rad * math.cos(aa), rad * math.sin(aa) - 0.4, z)
            s = (0.85 + 0.85 * v + 0.012 * age) * k * min(1.0, 0.3 + age / 6.0)
            ob.scale = (s * 1.1, s * 1.1, s)
            heat_v = (0.55 + 0.4 * v) * (1.0 - 0.5 * z / max(zb, 1.0)) if z < zb + 1 else max(0.0, 0.5 - 0.12 * (z - zb)) * v
            ob.color = (heat_v, v, 0, 1)
        for ob, (a, k, v) in zip(self.ring, self.pr):
            if t < 0:
                ob.hide_render = True; continue
            ob.hide_render = False
            R = 2.5 + 9.0 * (1 - math.exp(-0.06 * t)) * k
            ob.location = (R * math.cos(a), R * math.sin(a) - 0.5, 0.6 + 0.6 * v + 0.02 * t)
            s = (0.6 + 0.8 * (1 - math.exp(-0.08 * t))) * (0.8 + 0.5 * v)
            ob.scale = (s * 1.3, s * 1.3, s * 0.8)
            ob.color = (0.55 * math.exp(-0.03 * t) + 0.2, v, 0, 1)
        for ob, p in zip(self.debris, self.pd):
            a = g - p["b"]
            if a < 0:
                ob.hide_render = True; continue
            ob.hide_render = False
            R = 2.4 + p["vr"] * a
            z = p["z0"] + p["vz"] * a - 0.012 * a * a
            ob.location = (R * math.cos(p["a"]), R * math.sin(p["a"]), max(z, 0.1))
            ob.rotation_euler = tuple(w * a for w in p["spin"])
            ob.scale = (p["s"], p["s"] * 0.7, p["s"] * 0.55)
        f = 1.0 + 0.15 * math.sin(g * 2.1) + 0.1 * math.sin(g * 3.7)
        self.l1.energy = (0 if not on else 8000.0 * f * (1.0 + 1.5 * math.exp(-0.2 * max(t, 0))))
        self.o2.location = (0.0, -0.5, max(zb - 0.5, 1.0))
        self.l2.energy = (0 if not on else 4500.0 * f)


def tower_objects():
    import bpy
    names = ["balusters", "bell_frame", "bell_pivot", "chamber_ceiling", "chamber_floor", "chamber_props", "chamber_walls", "finial",
             "ladder", "lantern", "lantern_glass", "parapet", "pigeons", "rod", "rope_b", "spire_cone", "spire_drum", "spire_eave",
             "terrace", "tower_archetti", "tower_clock", "tower_clock_rim", "tower_courses", "tower_dentils", "tower_lesene",
             "tower_shaft", "tower_slits", "trapdoor", "wire", "wire_brackets"]
    return [bpy.data.objects[n] for n in names if n in bpy.data.objects]


# ----------------------------------------------------------------------------- build / apply per sub-shot
def build_tower(sub):
    import bpy
    import tower as T
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    A = T.build("NIGHT_STORM")
    T.setup_render(scene, "final")
    scene.cycles.transparent_max_bounces = 16
    mk = bpy.data.objects.get("market")
    if mk is not None:
        mk.hide_render = True
    T.set_rod(0)
    cam = T.make_camera(A["cams"]["spire_insert"], name="cam_s20"); cam.data.clip_start = 0.02; cam.data.clip_end = 400
    ctx = dict(scene=scene, T=T, cam=cam, sub=sub)
    if sub in ("a", "b"):
        bpy.context.view_layer.update()
        pts = crack_path_tower(scene)
        Ls = [0.0]
        for p, q in zip(pts, pts[1:]):
            Ls.append(Ls[-1] + math.dist(p, q))
        ctx["pts"], ctx["Ls"] = pts, Ls
        core = fx.emit_mat("S20_crack_core", (1.0, 0.72, 0.30), 7.0, additive=False, camera_only=True)
        halo = fx.emit_mat("S20_crack_halo", (1.0, 0.32, 0.05), 0.9, additive=True, camera_only=True)
        dark = T.mat_emit("S20_crack_dark", "#1a0d10", strength=1.0)
        ctx["crack"] = curve("S20_crack", pts, 0.022, core)
        ctx["halo"] = curve("S20_crack_halo", pts, 0.07, halo)
        ctx["scar"] = curve("S20_crack_scar", pts, 0.05, dark)          # burnt line left behind the head
        ctx["scar"].hide_render = True
        for o in (ctx["crack"], ctx["halo"]):
            o.data.bevel_factor_mapping_end = 'SPLINE'
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1.0); hd = bpy.context.active_object
        hd.name = "S20_head"; hd.data.materials.append(fx.emit_mat("S20_head_m", (1.0, 0.85, 0.55), 6.0, additive=False)); fx.no_bounce(hd)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1.0); hh = bpy.context.active_object
        hh.name = "S20_head_halo"; hh.data.materials.append(fx.emit_mat("S20_head_h", (1.0, 0.35, 0.06), 1.4, additive=True)); fx.no_bounce(hh)
        ctx["head"], ctx["hhalo"] = hd, hh
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1.0); ht = bpy.context.active_object
        ht.name = "S20_hot"; ht.location = (0.0, 0.0, 28.08); ht.data.materials.append(fx.emit_mat("S20_hot_m", (1.0, 0.45, 0.08), 1.3, additive=True)); fx.no_bounce(ht)
        ctx["hot"] = ht
        ld = bpy.data.lights.new("S20_head_l", 'POINT'); ld.color = (1.0, 0.45, 0.12); ld.shadow_soft_size = 0.3
        lo = bpy.data.objects.new("S20_head_l", ld); scene.collection.objects.link(lo); ctx["hl"] = (lo, ld)
        ctx["rain"] = fx.Rain(n=700 if sub == "a" else 1100, size=(8.0, 8.0, 10.0) if sub == "a" else (12.0, 12.0, 16.0),
                              ahead=3.5 if sub == "a" else 6.0, speed=1.2, length=0.7 if sub == "a" else 1.0,
                              width=0.006 if sub == "a" else 0.01, strength=0.32, near=0.8)
    ctx["card"] = fx.FlashCard(cam)              # after the ray casts (the card sits in front of the lens)
    if sub == "d":
        empty = bpy.data.objects.new("S20_lift", None); scene.collection.objects.link(empty)
        for o in tower_objects():
            if o.parent is None:
                mw = o.matrix_world.copy(); o.parent = empty; o.matrix_world = mw
        ctx["lift"] = empty
        ctx["col"] = Column(T)
        ctx["rain"] = fx.Rain(n=700, size=(20.0, 20.0, 24.0), ahead=12.0, speed=1.3, length=1.1, width=0.014, strength=0.16, near=4.0, seed=11)
    return ctx


def apply_tower(ctx, g):
    T = ctx["T"]; sub = ctx["sub"]
    if sub == "a":
        loc, look, roll = cam_a(g)
        fl, card, bolt = strike(g)
        T.flash(fl); T.set_bolt(bolt, target="tower"); ctx["card"].set(card)
        u = crack_u_a(g)
    elif sub == "b":
        loc, look, roll = cam_b(g)
        fl = 0.25 if g in (G_SIDE, G_SIDE + 1) else (0.1 if g == G_SIDE + 2 else 0.0)
        T.flash(fl); T.set_bolt(False); ctx["card"].set(0.0)
        u = crack_u_b(g)
    else:
        loc, look, roll = cam_d(g)
        fl, card = lift_flash(g)
        T.flash(fl); T.set_bolt(g - G21 in (0, 1), target="sky"); ctx["card"].set(card)
        z, ty, tx = lift(g)
        ctx["lift"].location = (0.0, 0.0, z)
        ctx["lift"].rotation_euler = (math.radians(tx), math.radians(ty), 0.0)
        ctx["col"].update(g)
    fx.set_cam(ctx["cam"], loc, look, roll)
    if sub in ("a", "b"):
        pts, Ls = ctx["pts"], ctx["Ls"]
        h = heat(g)
        for o in (ctx["crack"], ctx["halo"]):
            o.data.bevel_factor_end = max(u, 0.001); o.hide_render = u <= 0.001
        if sub == "a" and g >= G20:
            p = arc_point(pts, Ls, u) if u > 0.001 else (0.0, 0.0, 28.32)
            fin = True
        else:
            p = arc_point(pts, Ls, u); fin = True
        flick = 1.0 + 0.18 * math.sin(g * 2.3) + 0.1 * math.sin(g * 5.1)
        rs = (0.09 if sub == "a" else 0.16) * flick
        ctx["head"].location = p; ctx["head"].scale = (rs,) * 3
        ctx["hhalo"].location = p; ctx["hhalo"].scale = (rs * 2.4,) * 3
        hide = (sub == "b" and u >= 0.999) or (sub == "a" and g < G20)
        ctx["head"].hide_render = hide; ctx["hhalo"].hide_render = hide
        lo, ld = ctx["hl"]
        from mathutils import Vector
        lo.location = Vector(p) + Vector((-0.35, -0.3, 0.0))
        ld.energy = 0.0 if hide else (60.0 if sub == "a" else 500.0) * flick * h
        ctx["hot"].hide_render = g < G20 + 2
        ctx["hot"].scale = (0.16 * h * flick,) * 3
        ctx["rain"].update(g, loc, look)
    else:
        ctx["rain"].update(g, loc, look)
    ctx["scene"].frame_set(1)


def build_vault():
    import bpy
    import vault as V
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    A = V.build("BURN")
    V.setup_render(scene, "final")
    cam = V.make_camera(A["cams"]["crack_follow"]); cam.data.clip_start = 0.02
    ctx = dict(scene=scene, V=V, cam=cam, sub="c", A=A)
    ctx["card"] = fx.FlashCard(cam, rgb=(1.0, 0.72, 0.4))
    return ctx


def cam_c(g):
    V = None
    import vault as V
    u = crack_u_c(g)
    p = V.crack_point(max(0.0, u - 0.08))
    end = V.crack_point(1.0)
    lookp = tuple(p[i] * 0.55 + end[i] * 0.45 for i in range(3))
    ks = [(G_VAULT, (0.95, -3.4, 1.95), "sine"), (G21, (0.55, -4.9, 1.75), "hold")]
    loc = keys(g, ks, 0.3)
    dx, dz = jolt(g, [G_VAULT, G_ARRIVE], 0.06)
    return loc, (lookp[0] + dx, lookp[1], lookp[2] + dz), 0.0


def apply_vault(ctx, g):
    V = ctx["V"]
    loc, look, roll = cam_c(g)
    fx.set_cam(ctx["cam"], loc, look, roll)
    V.set_crack_glow(crack_u_c(g))
    fl, card = vault_flash(g)
    V.flash(fl)
    ctx["card"].set(card)
    ctx["scene"].frame_set(1)


def build(sub):
    return (lambda: build_vault()) if sub == "c" else (lambda: build_tower(sub))


def apply(sub):
    return apply_vault if sub == "c" else apply_tower


def report(ctx, g):
    return dict(sub=ctx["sub"])


# ----------------------------------------------------------------------------- delivery
def src_of(g):
    for s, (a, b) in SUBS.items():
        if a <= g <= b:
            return s


def deliver():
    import shutil
    fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
    files, js = {}, []
    for g in range(G20, LAST + 1):
        s = src_of(g)
        src = os.path.join(HERE, "raw", s, "g_%04d.png" % g); dst = os.path.join(fr, "g_%04d.png" % g)
        shutil.copyfile(src, dst); files[g] = dst
        js.append(json.load(open(src[:-4] + ".json")))
    wall = sum(j["wall"] for j in js) / len(js); cpu = sum(j["cpu"] for j in js) / len(js)
    names = {"a": "20 strike", "b": "20 wall", "c": "20 vault", "d": "21 lift"}
    fx.contact(files, os.path.join(HERE, "contact.jpg"), n=24, cols=8, label=lambda g: names[src_of(g)])
    fx.encode(HERE, G20)
    per = {}
    for s in SUBS:
        sj = [j for j in js if j["sub"] == s]
        per[s] = dict(wall=round(sum(j["wall"] for j in sj) / len(sj), 2), cpu=round(sum(j["cpu"] for j in sj) / len(sj), 2))
    meta = {"take": "s20", "shots": [20, 21], "g0": G20, "g1": G_END, "handle_in": 0, "handle_out": H_OUT,
            "first_g": G20, "n_frames": LAST - G20 + 1,
            "transition_in": {"type": "cut", "frames": 0},
            "transition_out": {"type": "dissolve", "frames": DISS_OUT, "note": "out-handle g %d..%d rendered in 3D (the lift continues)" % (G_END, LAST)},
            "internal": [{"at": G_SIDE, "type": "cut", "from": "20 spire_insert", "to": "20 tower_side_mid"},
                         {"at": G_VAULT, "type": "cut", "from": "20 tower_side_mid", "to": "20 vault crack_follow"},
                         {"at": G21, "type": "cut", "from_shot": 20, "to_shot": 21}],
            "shot_ranges": {"20": [G20, G21 - 1], "21": [G21, G_END - 1]},
            "sub_ranges": {k: list(v) for k, v in SUBS.items()},
            "set": "v3/set3d2/tower.py (NIGHT_STORM: spire_insert, tower_side_mid, town_wide) + v3/set3d2/vault.py (BURN: crack_follow)",
            "light": "NIGHT_STORM / BURN", "rod": "set_rod(0) throughout", "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(wall, 2), "s_per_frame_cpu_mean": round(cpu, 2), "s_per_frame_by_sub": per,
            "events": {"white_flash_strike": G20, "restrike_on_word": G_STRIKE, "second_flicker_punch": G_STRIKE2,
                       "glow_reaches_ground": G_VAULT - 7, "glow_reaches_barrels": G_ARRIVE, "tower_lift_flash": G21,
                       "lift_jolt": G_LIFT, "fly": G_FLY, "sky": G_SKY},
            "frame_source": {str(g): src_of(g) for g in range(G20, LAST + 1)}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    t = lambda g: round(g / 30.0, 3)
    ev = []

    def add(a, b, label, kind, **kw):
        e = dict(time=t(a), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label); e.update(kw); ev.append(e)
    add(G20, G_VAULT, "heavy rain (bed, continues from s19) under the strike and the wall", "ambience")
    add(G20, G20 + 2, "LIGHTNING STRIKE on the bare finial: white flash, huge crack of thunder right on top (hard cut)", "strike", impact_frame=G20)
    add(G_STRIKE, G_STRIKE + 4, "re-strike flicker on 'fa pha long yot' (electric crackle, sizzle on copper)", "strike", impact_frame=G_STRIKE)
    add(G20 + 3, G_SIDE, "hot copper hiss / sizzle of the glowing finial, crackle as the glow starts down the spire", "crackle")
    add(G_STRIKE2, G_STRIKE2 + 3, "second flicker + snap punch-in (short whoosh, crackle)", "camera_snap", peak_frame=G_STRIKE2)
    add(G_SIDE, G_VAULT - 7, "glow runs down the tower wall: fizzing electric crackle travelling downward, stone cracking ticks", "crackle")
    add(G_SIDE, G_SIDE + 2, "hard cut (thunder tail)", "cut")
    add(G_VAULT - 7, G_VAULT - 5, "glow hits the ground (low thump)", "impact")
    add(G_VAULT, G_VAULT, "hard cut into the vault: rain gone, muffled; low rumble", "cut")
    add(G_VAULT, G_ARRIVE, "glow fizzes along the vault crack overhead toward the barrels (crackle, trickling grit)", "crackle")
    add(G_ARRIVE, G21, "barrels flare: rising roar / suck-in before the blast", "riser")
    add(G21, G21, "EXPLOSION: hard cut, white flash, huge deep boom", "explosion", impact_frame=G21)
    add(G21, LAST + 1, "fire roar of the column, rumble, falling debris patter, bell clangs once as the tower lifts", "ambience")
    add(G_LIFT, G_LIFT + 3, "second jolt as the tower tears free ('thang ho'): stone crack, bell clang", "impact", impact_frame=G_LIFT)
    add(G21 + 6, G21 + 50, "debris pieces whistling out, bricks landing on the square", "debris")
    json.dump(dict(take="s20", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    rows = [("s20 %s (g %d-%d)" % (names[s], a, b), [files[g] for g in range(a, b + 1)]) for s, (a, b) in SUBS.items()]
    rows.append(("s20 all (g %d-%d)" % (G20, LAST), [files[g] for g in sorted(files)]))
    print(fx.hue_rows(rows))
    print("s/frame wall %.2f cpu %.2f" % (wall, cpu), per)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "deliver":
        deliver(); sys.exit()
    sub = sys.argv[2]
    a, b = SUBS[sub]
    gs = [g for g in fx.parse(sys.argv[3]) if a <= g <= b]
    if cmd == "stills":
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        ctx = build(sub)()
        for g in gs:
            apply(sub)(ctx, g)
            w, c = fx.render_frame(ctx["scene"], os.path.join(out, "s20%s_g_%04d.png" % (sub, g)), samples, scale)
            print("g %d %.1f s" % (g, w), flush=True)
    elif cmd == "final":
        fx.run_final(HERE, sub, gs, build(sub), apply(sub), report=report)
