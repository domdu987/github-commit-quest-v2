"""set_build.py -- blockout night expressway for the DEAD ZONE 09 EP.1 animatic (bpy 5.3, Cycles CPU).
Units: metres. Road runs along +Y, deck top z = 0. Thai traffic: right-hand drive, driver door on the car's right (+x).
"""
import math, os, random
import bpy
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
FPS = 24
TOTAL_FRAMES = 1280

# ---- layout constants (shared with shots.py) ----------------------------------------------------------------------
SEDAN = (-2.0, 8.0)          # hero sedan centre, heading +Y
DRIVER_SEAT = (-1.55, 8.35)
DOOR_HINGE = (-1.1, 9.0)
KONG = (0.25, 6.4)
CREW = (-0.55, 8.35)
TRUCK = (3.2, 1.0)


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (c[0], c[1], c[2], a)


def red_pulse(f):
    """2 Hz double flash (L-L . R-R): 1.0 on flash frames, low glow otherwise."""
    ph = (f / FPS) % 1.0
    for a in (0.0, 0.17, 0.5, 0.67):
        if a <= ph < a + 0.085:
            return 1.0
    return 0.06


# ---- materials ------------------------------------------------------------------------------------------------------
def _mat(name):
    m = bpy.data.materials.get(name)
    if m:
        return m, False
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m, True


def principled(name, col, rough=0.5, metal=0.0, emit=None, estr=0.0):
    m, new = _mat(name)
    if not new:
        return m
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = estr
    return m


def emission(name, col, strength=1.0, pulse=False):
    m, new = _mat(name)
    if not new:
        return m
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = col
    e.inputs["Strength"].default_value = strength
    if pulse:
        g = nt.nodes.new("ShaderNodeGroup")
        g.node_tree = pulse_group()
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = strength
        nt.links.new(g.outputs[0], mul.inputs[0])
        nt.links.new(mul.outputs[0], e.inputs["Strength"])
    nt.links.new(e.outputs[0], out.inputs[0])
    return m


_PG = []


def pulse_group():
    if _PG:
        return _PG[0]
    g = bpy.data.node_groups.new("RedPulse", "ShaderNodeTree")
    g.interface.new_socket("Value", in_out="OUTPUT", socket_type="NodeSocketFloat")
    o = g.nodes.new("NodeGroupOutput")
    v = g.nodes.new("ShaderNodeValue")
    v.name = "pulse"
    g.links.new(v.outputs[0], o.inputs[0])
    sock = v.outputs[0]
    for f in range(0, TOTAL_FRAMES + 30):
        sock.default_value = red_pulse(f)
        sock.keyframe_insert("default_value", frame=f + 1)
    for fc in _fcurves(g):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT"
    _PG.append(g)
    return g


def _fcurves(idblock):
    ad = idblock.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        return list(act.fcurves)
    except AttributeError:
        pass
    out = []
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                out.extend(cb.fcurves)
    return out


def set_constant(idblock):
    for fc in _fcurves(idblock):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT"


def glass(name, col=(0.02, 0.03, 0.05, 1), transp=0.72):
    m, new = _mat(name)
    if not new:
        return m
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    gl = nt.nodes.new("ShaderNodeBsdfGlossy")
    gl.inputs["Color"].default_value = (0.6, 0.65, 0.75, 1)
    gl.inputs["Roughness"].default_value = 0.08
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    tr.inputs["Color"].default_value = (0.75, 0.8, 0.9, 1)
    mx = nt.nodes.new("ShaderNodeMixShader")
    mx.inputs[0].default_value = 1.0 - transp
    nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(gl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0])
    return m


def road_material():
    m, new = _mat("road")
    if not new:
        return m
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    b = N["Principled BSDF"]
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Object"], sep.inputs[0])
    # puddles: noise -> roughness 0.04 (mirror-ish water) .. 0.45
    nz = N.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.35
    nz.inputs["Detail"].default_value = 3.0
    L.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = N.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0.04, 0.04, 0.04, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.42, 0.42, 0.42, 1)
    L.new(nz.outputs["Fac"], ramp.inputs[0])
    L.new(ramp.outputs[0], b.inputs["Roughness"])

    # lane lines: dashed at |x| = 2 and 6? lanes centred -6,-2,2,6 -> lines at x = -4, 0, 4 (dashed), +-8 (solid)
    def absn(inp):
        n = N.new("ShaderNodeMath"); n.operation = "ABSOLUTE"; L.new(inp, n.inputs[0]); return n.outputs[0]

    def op(o, a, bv):
        n = N.new("ShaderNodeMath"); n.operation = o
        if isinstance(a, float):
            n.inputs[0].default_value = a
        else:
            L.new(a, n.inputs[0])
        if isinstance(bv, float):
            n.inputs[1].default_value = bv
        else:
            L.new(bv, n.inputs[1])
        return n.outputs[0]
    x = sep.outputs[0]
    y = sep.outputs[1]
    ax = absn(x)
    # dashed: distance to nearest multiple of 4 (for |x| < 5)
    m4 = op("PINGPONG", ax, 2.0)                       # 0 at multiples of 4
    dash_x = op("LESS_THAN", m4, 0.07)
    inner = op("LESS_THAN", ax, 5.0)
    ydash = op("LESS_THAN", op("FRACT", op("DIVIDE", y, 9.0), 0.0), 0.42)
    dashed = op("MULTIPLY", op("MULTIPLY", dash_x, inner), ydash)
    solid = op("LESS_THAN", absn(op("SUBTRACT", ax, 8.1)), 0.08)
    line = op("MAXIMUM", dashed, solid)
    mix = N.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = (0.018, 0.02, 0.027, 1)
    mix.inputs["B"].default_value = (0.5, 0.5, 0.48, 1)
    L.new(line, mix.inputs["Factor"])
    L.new(mix.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Specular IOR Level"].default_value = 0.6
    return m


def image_emission_material(name, path, strength=1.0, alpha=True, repeat=False, mapping_anim=None):
    m, new = _mat(name)
    if not new:
        return m
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    N.clear()
    out = N.new("ShaderNodeOutputMaterial")
    tex = N.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path, check_existing=True)
    tex.image.alpha_mode = "STRAIGHT"
    tex.extension = "REPEAT" if repeat else "CLIP"
    e = N.new("ShaderNodeEmission")
    e.inputs["Strength"].default_value = strength
    L.new(tex.outputs["Color"], e.inputs["Color"])
    if mapping_anim is not None:
        tc = N.new("ShaderNodeTexCoord")
        mp = N.new("ShaderNodeMapping")
        mp.name = "map"
        mp.inputs["Scale"].default_value = mapping_anim.get("scale", (1, 1, 1))
        L.new(tc.outputs["UV"], mp.inputs["Vector"])
        L.new(mp.outputs[0], tex.inputs["Vector"])
    if alpha:
        tr = N.new("ShaderNodeBsdfTransparent")
        mx = N.new("ShaderNodeMixShader")
        L.new(tex.outputs["Alpha"], mx.inputs[0])
        L.new(tr.outputs[0], mx.inputs[1])
        L.new(e.outputs[0], mx.inputs[2])
        L.new(mx.outputs[0], out.inputs[0])
    else:
        L.new(e.outputs[0], out.inputs[0])
    return m


def card_material(name, path, tint=(0.80, 0.84, 1.0), red=0.55):
    """puppet card: image * (night tint + red pulse), emission only, never lit."""
    m, new = _mat(name)
    if not new:
        return m
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    N.clear()
    out = N.new("ShaderNodeOutputMaterial")
    tex = N.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path, check_existing=True)
    tex.image.alpha_mode = "STRAIGHT"
    tex.extension = "CLIP"
    tex.interpolation = "Linear"
    g = N.new("ShaderNodeGroup")
    g.node_tree = pulse_group()
    # tint colour = base + pulse * red
    redc = N.new("ShaderNodeMix"); redc.data_type = "RGBA"; redc.blend_type = "ADD"
    redc.inputs["A"].default_value = (tint[0], tint[1], tint[2], 1)
    redc.inputs["B"].default_value = (red, red * 0.18, red * 0.14, 1)
    L.new(g.outputs[0], redc.inputs["Factor"])
    mul = N.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    L.new(tex.outputs["Color"], mul.inputs["A"])
    L.new(redc.outputs["Result"], mul.inputs["B"])
    e = N.new("ShaderNodeEmission")
    L.new(mul.outputs["Result"], e.inputs["Color"])
    tr = N.new("ShaderNodeBsdfTransparent")
    mx = N.new("ShaderNodeMixShader")
    L.new(tex.outputs["Alpha"], mx.inputs[0])
    L.new(tr.outputs[0], mx.inputs[1])
    L.new(e.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], out.inputs[0])
    return m


# ---- geometry helpers -----------------------------------------------------------------------------------------------
def box(name, size, loc, mat, bevel=0.0, rot=(0, 0, 0), parent=None, segs=2):
    me = bpy.data.meshes.new(name)
    sx, sy, sz = [s / 2.0 for s in size]
    v = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
         (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    me.materials.append(mat)
    if bevel > 0:
        md = ob.modifiers.new("bev", "BEVEL")
        md.width = bevel
        md.segments = segs
        md.limit_method = "NONE"
    if parent:
        ob.parent = parent
    return ob


def cyl(name, r, depth, loc, mat, rot=(0, 0, 0), parent=None, n=12):
    me = bpy.data.meshes.new(name)
    v, f = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        v.append((r * math.cos(a), r * math.sin(a), -depth / 2))
        v.append((r * math.cos(a), r * math.sin(a), depth / 2))
    for i in range(n):
        j = (i + 1) % n
        f.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    f.append(tuple(2 * i for i in reversed(range(n))))
    f.append(tuple(2 * i + 1 for i in range(n)))
    me.from_pydata(v, [], f)
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    me.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


def plane(name, w, h, loc, mat, rot=(0, 0, 0), parent=None, uv=True, origin_bottom=False):
    """plane in the XZ plane (normal -Y), w along X, h along Z."""
    me = bpy.data.meshes.new(name)
    z0, z1 = (0.0, h) if origin_bottom else (-h / 2, h / 2)
    v = [(-w / 2, 0, z0), (w / 2, 0, z0), (w / 2, 0, z1), (-w / 2, 0, z1)]
    me.from_pydata(v, [], [(0, 1, 2, 3)])
    if uv:
        uvl = me.uv_layers.new()
        for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
            uvl.data[i].uv = c
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    me.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    e.rotation_euler = rot
    return e


# ---- cars -----------------------------------------------------------------------------------------------------------
PAINTS = ["#2b3445", "#3a4152", "#59606c", "#1c2230", "#6d7480", "#23293a", "#4a3036", "#7a7f88", "#30353f"]


def car(name, loc, heading=0.0, paint="#3a4152", crumple=0.0, hero=False, lights=True, seed=0):
    """bevelled blockout car; front toward +Y (heading rotates about Z, degrees)."""
    root = empty(name, (loc[0], loc[1], 0.0), (0, 0, math.radians(heading)))
    pm = principled("paint_" + paint, hexcol(paint), rough=0.22, metal=0.4)
    dark = principled("tyre", hexcol("#0d0d10"), rough=0.7)
    trim = principled("trim", hexcol("#15161b"), rough=0.4)
    L, W = 4.5, 1.8
    if hero:
        # hollow lower body so the driver card shows through the glass: sides, nose, tail
        box(name + "_sideL", (0.08, L, 0.62), (-W / 2 + 0.04, 0, 0.62), pm, 0.03, parent=root)
        box(name + "_nose", (W, 1.35, 0.62), (0, L / 2 - 0.675, 0.62), pm, 0.08, parent=root)
        box(name + "_tail", (W, 1.0, 0.62), (0, -L / 2 + 0.5, 0.62), pm, 0.08, parent=root)
        box(name + "_floor", (W, L, 0.12), (0, 0, 0.36), trim, 0.0, parent=root)
        box(name + "_sideRrear", (0.08, 1.15, 0.62), (W / 2 - 0.04, -0.45, 0.62), pm, 0.03, parent=root)
        # driver door (right side, front), hinge at its front edge
        hinge = empty(name + "_hinge", (0, 0, 0))
        hinge.parent = root
        hinge.location = (W / 2, 1.0, 0)
        box(name + "_door", (0.08, 1.12, 0.62), (-0.04, -0.56, 0.62), pm, 0.03, parent=hinge)
        box(name + "_doorglass", (0.03, 1.0, 0.4), (-0.04, -0.56, 1.13), glass("glass_side", transp=0.8), 0.0, parent=hinge)
        # seat + wheel
        seat = principled("seat", hexcol("#1b1c22"), rough=0.8)
        box(name + "_seat", (0.55, 0.55, 0.12), (0.45, 0.25, 0.5), seat, 0.03, parent=root)
        box(name + "_seatback", (0.55, 0.12, 0.7), (0.45, -0.05, 0.85), seat, 0.03, rot=(math.radians(-12), 0, 0), parent=root)
        cyl(name + "_wheel", 0.19, 0.04, (0.45, 0.95, 0.95), trim, rot=(math.radians(65), 0, 0), parent=root)
        box(name + "_dash", (W - 0.1, 0.35, 0.2), (0, 1.2, 0.85), trim, 0.03, parent=root)
        # glass cabin: pillars + panes
        gl = glass("glass_hero", transp=0.88)
        box(name + "_ws", (W - 0.12, 0.04, 0.62), (0, 1.05, 1.18), gl, 0.0, rot=(math.radians(-35), 0, 0), parent=root)
        box(name + "_rw", (W - 0.12, 0.04, 0.55), (0, -1.3, 1.17), gl, 0.0, rot=(math.radians(30), 0, 0), parent=root)
        box(name + "_roof", (W - 0.1, 2.0, 0.07), (0, -0.1, 1.45), pm, 0.03, rot=(math.radians(-3 * crumple), math.radians(4 * crumple), 0), parent=root)
        for sx in (-1, 1):
            box(name + "_pA%d" % sx, (0.07, 0.07, 0.6), (sx * (W / 2 - 0.08), 1.02, 1.18), pm, 0.0, rot=(math.radians(-35), 0, 0), parent=root)
            box(name + "_pC%d" % sx, (0.07, 0.07, 0.55), (sx * (W / 2 - 0.08), -1.28, 1.17), pm, 0.0, rot=(math.radians(30), 0, 0), parent=root)
        box(name + "_sideglassL", (0.03, 2.0, 0.42), (-W / 2 + 0.06, -0.1, 1.15), gl, 0.0, parent=root)
        box(name + "_sideglassRr", (0.03, 1.0, 0.42), (W / 2 - 0.06, -0.6, 1.15), gl, 0.0, parent=root)
        # crumpled nose
        box(name + "_crush", (W * 0.9, 0.5, 0.35), (0.2, L / 2 + 0.05, 0.75), pm, 0.05,
            rot=(math.radians(18), math.radians(-12), math.radians(8)), parent=root)
    else:
        body = box(name + "_body", (W, L, 0.62), (0, 0, 0.62), pm, 0.12, parent=root)
        cab = box(name + "_cab", (W - 0.14, 2.3, 0.55), (0, -0.25, 1.17), glass("glass_dark", transp=0.15), 0.14, parent=root)
        if crumple:
            body.rotation_euler = (math.radians(3 * crumple), math.radians(-2 * crumple), math.radians(2 * crumple))
            cab.rotation_euler = (0, math.radians(5 * crumple), math.radians(-4 * crumple))
            box(name + "_crush", (W * 0.95, 0.6, 0.4), (0, L / 2 + 0.1, 0.65), pm, 0.06,
                rot=(math.radians(20), math.radians(15), math.radians(-10)), parent=root)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(name + "_w%d%d" % (sx, sy), 0.33, 0.24, (sx * (W / 2 - 0.08), sy * 1.45, 0.33), dark,
                rot=(0, math.radians(90), 0), parent=root)
    if lights:
        tl = emission("taillight", hexcol("#ff2a1e"), 6.0)
        hl = emission("headlight", hexcol("#fff2d8"), 5.0)
        for sx in (-1, 1):
            box(name + "_tl%d" % sx, (0.4, 0.05, 0.14), (sx * 0.62, -L / 2 - 0.01, 0.82), tl, 0.0, parent=root)
            box(name + "_hl%d" % sx, (0.36, 0.05, 0.12), (sx * 0.6, L / 2 + 0.01, 0.75), hl, 0.0, parent=root)
    return root


def rescue_truck(loc):
    root = empty("truck", (loc[0], loc[1], 0))
    white = principled("truck_white", hexcol("#d9dde4"), rough=0.35, metal=0.1)
    orange = principled("truck_orange", hexcol("#d8641e"), rough=0.4)
    dark = principled("tyre", hexcol("#0d0d10"), rough=0.7)
    box("truck_cab", (2.0, 2.4, 1.2), (0, 1.3, 1.3), white, 0.15, parent=root)
    box("truck_low", (2.0, 5.4, 0.7), (0, 0, 0.7), white, 0.1, parent=root)
    box("truck_bed", (2.0, 2.8, 0.9), (0, -1.25, 1.45), white, 0.06, parent=root)
    box("truck_stripe", (2.04, 5.0, 0.12), (0, 0, 0.95), orange, 0.0, parent=root)
    box("truck_ws", (1.8, 0.05, 0.7), (0, 2.45, 1.55), glass("glass_dark", transp=0.15), 0.0,
        rot=(math.radians(-25), 0, 0), parent=root)
    bar = emission("lightbar", hexcol("#ff1a10"), 30.0, pulse=True)
    box("truck_bar", (1.6, 0.3, 0.16), (0, 1.3, 2.0), bar, 0.04, parent=root)
    box("truck_bar2", (0.3, 0.3, 0.16), (0.7, -2.6, 2.0), bar, 0.04, parent=root)
    box("truck_bar3", (0.3, 0.3, 0.16), (-0.7, -2.6, 2.0), bar, 0.04, parent=root)
    tl = emission("taillight", hexcol("#ff2a1e"), 6.0)
    hl = emission("headlight", hexcol("#fff2d8"), 5.0)
    for sx in (-1, 1):
        cyl("truck_w%d" % sx, 0.38, 0.28, (sx * 0.95, 1.6, 0.38), dark, rot=(0, math.radians(90), 0), parent=root)
        cyl("truck_wr%d" % sx, 0.38, 0.28, (sx * 0.95, -1.7, 0.38), dark, rot=(0, math.radians(90), 0), parent=root)
        box("truck_tl%d" % sx, (0.3, 0.05, 0.2), (sx * 0.75, -2.71, 0.95), tl, 0.0, parent=root)
        box("truck_hl%d" % sx, (0.32, 0.05, 0.14), (sx * 0.7, 2.71, 0.9), hl, 0.0, parent=root)
    # pulsing red point light (no shadows) above the bar
    ld = bpy.data.lights.new("redlight", "POINT")
    ld.color = (1.0, 0.08, 0.05)
    ld.shadow_soft_size = 0.3
    ld.use_shadow = False
    lo = bpy.data.objects.new("redlight", ld)
    bpy.context.scene.collection.objects.link(lo)
    lo.location = (loc[0], loc[1] + 1.3, 2.4)
    for f in range(0, TOTAL_FRAMES + 30):
        ld.energy = 600.0 * red_pulse(f)
        ld.keyframe_insert("energy", frame=f + 1)
    set_constant(ld)
    return root


def lamp_post(y, side, real_light=True):
    x = side * 8.75
    pole = principled("pole", hexcol("#5a606a"), rough=0.5, metal=0.6)
    cyl("pole_%d_%d" % (y, side), 0.09, 10.0, (x, y, 5.9), pole)
    box("arm_%d_%d" % (y, side), (2.2, 0.12, 0.12), (x - side * 1.05, y, 10.8), pole, 0.0)
    head = emission("lamp_head", hexcol("#ffb35a"), 25.0)
    box("lamphead_%d_%d" % (y, side), (0.6, 0.3, 0.12), (x - side * 2.0, y, 10.72), head, 0.03)
    if real_light:
        ld = bpy.data.lights.new("lamp_%d_%d" % (y, side), "SPOT")
        ld.color = hexcol("#ffb46a")[:3]
        ld.energy = 4000.0
        ld.spot_size = math.radians(110)
        ld.spot_blend = 0.6
        ld.shadow_soft_size = 0.4
        lo = bpy.data.objects.new("lamp_%d_%d" % (y, side), ld)
        bpy.context.scene.collection.objects.link(lo)
        lo.location = (x - side * 2.0, y, 10.5)


def make_textures():
    """rain streaks, distant city, phone screens are made by make_tex.py; here only verify they exist."""
    for f in ("rain.png", "city.png"):
        assert os.path.exists(os.path.join(TEX, f)), f


def build(scene):
    random.seed(9)
    make_textures()
    # world
    w = bpy.data.worlds.new("night")
    scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexcol("#0b1022")
    bg.inputs["Strength"].default_value = 0.9
    # deck
    road = road_material()
    deck = box("deck", (18.4, 700, 0.6), (0, 300, -0.3), road)
    deck.data.materials.clear(); deck.data.materials.append(road)
    under = principled("concrete", hexcol("#3b4150"), rough=0.8)
    box("deck_side_l", (0.4, 700, 1.4), (-9.4, 300, -0.9), under)
    box("deck_side_r", (0.4, 700, 1.4), (9.4, 300, -0.9), under)
    # jersey barriers (both edges + median-less)
    bar = principled("barrier", hexcol("#8a909b"), rough=0.65)
    for side in (-1, 1):
        box("barrier_%d" % side, (0.5, 700, 0.95), (side * 8.95, 300, 0.47), bar, 0.12)
    # lamp posts
    for i, y in enumerate(range(-56, 400, 32)):
        for side in (-1, 1):
            lamp_post(y, side, real_light=(-56 <= y <= 72))
    # hero pile-up
    car("sedan", SEDAN, heading=4.0, paint="#59606c", crumple=1.0, hero=True)
    car("rammer", (-1.6, 3.15), heading=14.0, paint="#2b3445", crumple=1.0)
    car("front1", (-2.4, 13.7), heading=-9.0, paint="#7a7f88", crumple=0.6)
    rescue_truck(TRUCK)
    # gridlock lanes (bevelled cars near, tail-light pairs far)
    lanes = [-6.0, -2.0, 2.0, 6.0]
    spots = [(-6.0, 9.0), (-6.0, 18.5), (2.2, 15.0), (6.0, 6.0), (6.0, 16.0), (-2.0, 21.5), (2.0, 26.0), (-6.0, 29.0),
             (6.0, 27.0), (-2.0, 33.5), (2.0, 37.5)]
    for i, (x, y) in enumerate(spots):
        car("car%02d" % i, (x + random.uniform(-0.3, 0.3), y), heading=random.uniform(-6, 6),
            paint=PAINTS[i % len(PAINTS)], crumple=(0.5 if i in (2, 5) else 0.0), seed=i)
    tl = emission("taillight_far", hexcol("#ff2a1e"), 9.0)
    hl = emission("roof_far", hexcol("#1a1e28"), 0.0)
    farbody = principled("farbody", hexcol("#141821"), rough=0.4)
    for lane in lanes:
        y = 42.0 + random.uniform(0, 6)
        while y < 560:
            x = lane + random.uniform(-0.4, 0.4)
            if y < 160:
                box("fb_%d_%d" % (lane, y), (1.8, 4.3, 1.1), (x, y, 0.75), farbody, 0.15)
            for sx in (-1, 1):
                box("ft_%d_%d_%d" % (lane, y, sx), (0.4, 0.05, 0.15), (x + sx * 0.62, y - 2.17, 0.82), tl, 0.0)
            y += random.uniform(6.0, 9.5)
    # distant city: back plane + side planes
    city = image_emission_material("city", os.path.join(TEX, "city.png"), 1.4, alpha=True)
    plane("city_back", 1600, 420, (0, 900, -60), city, origin_bottom=True)
    for side in (-1, 1):
        plane("city_side_%d" % side, 1400, 380, (side * 420, 300, -80), city,
              rot=(0, 0, math.radians(90 * side)), origin_bottom=True)
    # moon key (cool, weak)
    sd = bpy.data.lights.new("key", "SUN")
    sd.energy = 0.9
    sd.color = hexcol("#cfd8ff")[:3]
    sd.angle = math.radians(1.0)
    so = bpy.data.objects.new("key", sd)
    scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(48), 0, math.radians(-60))


def rain_rig(scene, cam):
    """three rain streak cards parented to the camera, texture scrolling down."""
    rain = os.path.join(TEX, "rain.png")
    lens_h = 36.0
    for i, (d, spd, strg) in enumerate([(1.2, 2.6, 0.22), (3.5, 1.4, 0.16), (9.0, 0.8, 0.12)]):
        m = image_emission_material("rain%d" % i, rain, strg, alpha=True, repeat=True,
                                    mapping_anim={"scale": (1.0 + i * 0.7, 1.0 + i * 0.5, 1)})
        h = 2 * d * (lens_h / 2) / 22.0 * 1.6          # generous: covers 22-50 mm lenses with shake
        p = plane("raincard%d" % i, h * 0.62, h, (0, 0, -d), m, rot=(math.radians(90), 0, 0), parent=cam)
        p.visible_shadow = False
        p.visible_diffuse = False
        p.visible_glossy = False
        mp = m.node_tree.nodes["map"]
        for f in (1, TOTAL_FRAMES + 30):
            mp.inputs["Location"].default_value = (0.13 * i, (f / FPS) * spd + 0.37 * i, 0)
            mp.inputs["Location"].keyframe_insert("default_value", frame=f)
        for fc in _fcurves(m.node_tree):
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR"


def merge_static(scene, keep_prefixes=("sedan_hinge", "sedan_door")):
    """bake every static mesh (modifiers applied, world transform) into one mesh object: far fewer objects to sync."""
    import bmesh
    dg = bpy.context.evaluated_depsgraph_get()
    copies = []
    for ob in list(scene.collection.objects):
        if ob.type != "MESH" or ob.name.startswith(keep_prefixes):
            continue
        if ob.parent and ob.parent.name.startswith(keep_prefixes):
            continue
        copies.append((ob, bpy.data.meshes.new_from_object(ob.evaluated_get(dg)), ob.matrix_world.copy()))
    dg = None
    mats, idx = [], {}
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    victims = []
    for ob, me, mw in copies:
        tmp = bmesh.new()
        tmp.from_mesh(me)
        tmp.transform(mw)
        src_uv = tmp.loops.layers.uv.active
        remap = []
        for m in me.materials:
            if m.name not in idx:
                idx[m.name] = len(mats)
                mats.append(m)
            remap.append(idx[m.name])
        vmap = {}
        for v in tmp.verts:
            vmap[v.index] = bm.verts.new(v.co)
        for f in tmp.faces:
            try:
                nf = bm.faces.new([vmap[v.index] for v in f.verts])
            except ValueError:
                continue
            nf.material_index = remap[f.material_index] if remap else 0
            nf.smooth = f.smooth
            if src_uv is not None:
                for l_new, l_old in zip(nf.loops, f.loops):
                    l_new[uv].uv = l_old[src_uv].uv
        tmp.free()
        victims.append((ob, me))
    me = bpy.data.meshes.new("static")
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new("static", me)
    scene.collection.objects.link(ob)
    for v, mcopy in victims:
        bpy.data.objects.remove(v, do_unlink=True)
        bpy.data.meshes.remove(mcopy)
    # empties that no longer parent anything
    for e in list(scene.collection.objects):
        if e.type == "EMPTY" and not e.children and not e.name.startswith(keep_prefixes):
            bpy.data.objects.remove(e, do_unlink=True)
    return ob
