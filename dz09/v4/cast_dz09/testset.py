"""testset.py -- a small lit test stage for the 2.5D cast: a patch of wet Bangkok expressway at night.
NOT the EP.1 set (that belongs to the set agent): just enough world to prove the puppets: wet asphalt with
reflections, lane paint, a concrete barrier, two crashed cars, a rescue pickup with a red beacon, a sodium lamp,
cool moon key, rain streaks.  1 BU = 1 D ~ 0.52 m (Kong is 3.3 D = 1.72 m; a car is 2.8 D tall, 8.6 D long).

    import testset; L = testset.build(scene, rain=True)      # returns light names {"key", "beacon", "sodium"}
"""
import math, random
import bpy
from mathutils import Vector


def _mat(name, base, rough=0.5, metal=0.0, emit=None, estr=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base + (1,) if len(base) == 3 else base
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = emit + (1,)
        b.inputs["Emission Strength"].default_value = estr
    return m


def _box(name, size, loc, mat, bevel=0.0, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        md = ob.modifiers.new("bev", "BEVEL")
        md.width = bevel
        md.segments = 3
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


def _asphalt():
    m = bpy.data.materials.new("asphalt_wet")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.08
    nz.inputs["Detail"].default_value = 4
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    puddle = nt.nodes.new("ShaderNodeMapRange")
    puddle.inputs[1].default_value, puddle.inputs[2].default_value = 0.45, 0.58
    puddle.inputs[3].default_value, puddle.inputs[4].default_value = 0.38, 0.03
    nt.links.new(nz.outputs["Fac"], puddle.inputs[0])
    nt.links.new(puddle.outputs[0], b.inputs["Roughness"])
    grain = nt.nodes.new("ShaderNodeTexNoise")
    grain.inputs["Scale"].default_value = 9.0
    nt.links.new(tc.outputs["Object"], grain.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeMapRange")
    cr.inputs[3].default_value, cr.inputs[4].default_value = 0.018, 0.045
    nt.links.new(grain.outputs["Fac"], cr.inputs[0])
    comb = nt.nodes.new("ShaderNodeCombineColor")
    nt.links.new(cr.outputs[0], comb.inputs[0])
    nt.links.new(cr.outputs[0], comb.inputs[1])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 1.25
    nt.links.new(cr.outputs[0], mul.inputs[0])
    nt.links.new(mul.outputs[0], comb.inputs[2])
    nt.links.new(comb.outputs[0], b.inputs["Base Color"])
    bm = nt.nodes.new("ShaderNodeBump")
    bm.inputs["Strength"].default_value = 0.08
    nt.links.new(grain.outputs["Fac"], bm.inputs["Height"])
    nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
    return m


def car(name, loc, rot_deg, body_col, parent=None, lights=True):
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    root.location = loc
    root.rotation_euler = (0, 0, math.radians(rot_deg))
    body = _mat(name + "_paint", body_col, 0.22, 0.4)
    glass = _mat(name + "_glass", (0.02, 0.025, 0.035), 0.05)
    tyre = _mat(name + "_tyre", (0.02, 0.02, 0.022), 0.8)
    rim = _mat(name + "_rim", (0.55, 0.56, 0.58), 0.3, 1.0)
    _box(name + "_body", (8.4, 3.4, 1.35), (0, 0, 1.25), body, 0.3, parent=root)
    _box(name + "_cabin", (4.6, 3.1, 1.25), (-0.4, 0, 2.45), body, 0.35, parent=root)
    _box(name + "_ws", (4.2, 3.16, 0.95), (-0.4, 0, 2.5), glass, 0.3, parent=root)
    for x in (-2.8, 2.8):
        for y in (-1.6, 1.6):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.68, depth=0.5, location=(x, y, 0.68), rotation=(math.pi / 2, 0, 0))
            w = bpy.context.active_object
            w.data.materials.append(tyre)
            w.parent = root
            bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.52, location=(x, y, 0.68), rotation=(math.pi / 2, 0, 0))
            r = bpy.context.active_object
            r.data.materials.append(rim)
            r.parent = root
    if lights:
        hl = _mat(name + "_hl", (1, 0.95, 0.8), 0.2, emit=(1.0, 0.9, 0.7), estr=6)
        tl = _mat(name + "_tl", (0.6, 0.02, 0.02), 0.2, emit=(1.0, 0.03, 0.02), estr=5)
        for y in (-1.25, 1.25):
            _box(name + "_hl%d" % (y > 0), (0.1, 0.7, 0.3), (4.2, y, 1.45), hl, parent=root)
            _box(name + "_tl%d" % (y > 0), (0.1, 0.6, 0.28), (-4.2, y, 1.5), tl, parent=root)
    # plate panel lines
    line = _mat(name + "_seam", (0.01, 0.01, 0.01), 0.6)
    _box(name + "_seam", (0.04, 3.42, 1.0), (1.0, 0, 1.25), line, parent=root)
    return root


def build(scene, rain=True, seed=9):
    random.seed(seed)
    # world: dark night blue
    w = bpy.data.worlds.new("night")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.006, 0.009, 0.026, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    scene.world = w
    # road
    bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 20, 0))
    road = bpy.context.active_object
    road.name = "road"
    road.data.materials.append(_asphalt())
    paint = _mat("lane_paint", (0.75, 0.74, 0.70), 0.35)
    yel = _mat("lane_yellow", (0.80, 0.62, 0.10), 0.35)
    for i in range(-6, 14):
        _box("dash%d" % i, (0.22, 4.0, 0.02), (-6.8, i * 8.0, 0.01), paint)
        _box("dashb%d" % i, (0.22, 4.0, 0.02), (6.8, i * 8.0 + 2, 0.01), paint)
    _box("edge_y", (0.22, 150, 0.02), (-13.2, 20, 0.01), yel)
    # concrete barrier (jersey profile approximated by two boxes) on the left edge + its parapet
    conc = _mat("concrete", (0.32, 0.33, 0.35), 0.75)
    _box("barrier_lo", (1.6, 150, 0.7), (-14.6, 20, 0.35), conc, 0.1)
    _box("barrier_hi", (0.7, 150, 1.4), (-14.6, 20, 1.3), conc, 0.1)
    # cars: crashed gridlock
    car("car_red", (5.5, 9.5, 0), 72, (0.42, 0.03, 0.03))
    car("car_white", (-4.5, 14.0, 0), 98, (0.70, 0.70, 0.68))
    car("car_grey", (9.0, 22.0, 0), 85, (0.18, 0.19, 0.21))
    car("car_far1", (-6.0, 34.0, 0), 92, (0.08, 0.12, 0.30))
    car("car_far2", (4.0, 42.0, 0), 88, (0.45, 0.45, 0.47))
    # rescue pickup with the red beacon (behind Kong, screen-left)
    pk = car("rescue_truck", (-7.5, 3.5, 0), 95, (0.85, 0.82, 0.78))
    bar = _mat("beacon_red", (0.6, 0.0, 0.0), 0.2, emit=(1.0, 0.04, 0.02), estr=30)
    _box("beacon_bar", (0.6, 2.6, 0.35), (-0.5, 0, 3.3), bar, 0.1, parent=pk)
    # sodium lamp pole on the right, arm over the road
    steel = _mat("pole", (0.25, 0.26, 0.28), 0.4, 0.8)
    _box("pole", (0.35, 0.35, 19.0), (12.5, 4.0, 9.5), steel)
    _box("pole_arm", (6.0, 0.25, 0.25), (9.7, 4.0, 18.8), steel)
    lampm = _mat("sodium_head", (1, 0.6, 0.2), 0.3, emit=(1.0, 0.55, 0.15), estr=40)
    _box("lamp_head", (1.6, 0.7, 0.3), (7.0, 4.0, 18.55), lampm, 0.1)
    # lights
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 30))
    moon = bpy.context.active_object
    moon.name = "Moon"
    moon.data.energy = 0.25
    moon.data.color = (0.55, 0.65, 1.0)
    moon.data.angle = math.radians(1.0)
    moon.rotation_euler = (math.radians(50), 0, math.radians(-35))
    bpy.ops.object.light_add(type="POINT", location=(7.0, 4.0, 18.2))
    sod = bpy.context.active_object
    sod.name = "Sodium"
    sod.data.energy = 14000
    sod.data.color = (1.0, 0.55, 0.18)
    sod.data.shadow_soft_size = 0.6
    sod["rim_gain"] = 0.9
    sod["rim_radius"] = 16.0
    bpy.ops.object.light_add(type="POINT", location=(-7.9, 3.5, 3.9))
    bea = bpy.context.active_object
    bea.name = "Beacon"
    bea.data.energy = 9000
    bea.data.color = (1.0, 0.06, 0.04)
    bea.data.shadow_soft_size = 0.3
    bea["rim_gain"] = 1.6
    bea["rim_radius"] = 7.0
    if rain:
        rm = bpy.data.materials.new("rain")
        rm.use_nodes = True
        nt = rm.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (0.55, 0.62, 0.8, 1)
        em.inputs["Strength"].default_value = 0.45
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = 0.22
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], o.inputs["Surface"])
        rm.cycles.emission_sampling = "NONE"
        verts, faces = [], []
        for i in range(900):
            x, y, z = random.uniform(-14, 14), random.uniform(2.5, 30), random.uniform(0, 14)
            L = random.uniform(0.9, 1.6)
            wdt = 0.010
            k = len(verts)
            verts += [(x - wdt, y, z), (x + wdt, y, z), (x + wdt + 0.08, y, z + L), (x - wdt + 0.08, y, z + L)]
            faces.append((k, k + 1, k + 2, k + 3))
        me = bpy.data.meshes.new("rain")
        me.from_pydata(verts, [], faces)
        me.materials.append(rm)
        ob = bpy.data.objects.new("rain", me)
        scene.collection.objects.link(ob)
        ob.visible_shadow = False
    return {"key": "Moon", "beacon": "Beacon", "sodium": "Sodium"}
