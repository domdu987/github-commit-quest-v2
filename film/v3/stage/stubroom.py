"""stubroom.py -- a small test room that follows the v3 world convention (NOT the real office; that is v3/set3d).

    import stubroom
    room = stubroom.build(scene)       # floor (planks), back wall at y = 0 (grid), one box, one hard sun, black world
    room["sun"], room["materials"], room["mark"](point, ...)      # see build()

1 unit = 1 D.  Floor z = 0, map wall = plane y = 0, room toward negative y, x = 0 = centre of the wall.
Lighting model of spec LOOK_SPEC 4.2 with the verify corrections: lit = Diffuse (roughness 0) + Emission(albedo x A),
emission sampling NONE, one sun with energy pi x max(K), colour K / max(K), angle 1.5 deg, no bounce.
"""
import math, os
import bpy
from mathutils import Vector

A_DAY = (0.42, 0.40, 0.56)          # INTERIOR_DAY ambient (linear)
K_DAY = (0.70, 0.54, 0.15)          # INTERIOR_DAY key (linear), on a surface facing the sun
A_TEST = (0.26, 0.25, 0.44)         # the stub's default: a harder sun so that cast shadows read clearly in the tests
K_TEST = (1.00, 0.80, 0.42)         # (floor in shadow = 0.33 of its sunlit value; clip A exteriors measure 0.11 to 0.33)


def hex_lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def _clean(mat):
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    return nt


def lit_material(name, albedo_hex="#808080", A=A_TEST, image=None):
    """Diffuse(albedo, roughness 0) + Emission(albedo x A); image = bpy image (sRGB) used as albedo (box-projected)."""
    m = bpy.data.materials.new(name)
    nt = _clean(m)
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    dif.inputs["Roughness"].default_value = 0.0
    emi = nt.nodes.new("ShaderNodeEmission")
    add = nt.nodes.new("ShaderNodeAddShader")
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    mul.inputs[7].default_value = (*A, 1.0)
    if image is not None:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image
        tex.interpolation = "Cubic"
        L(tex.outputs["Color"], dif.inputs["Color"])
        L(tex.outputs["Color"], mul.inputs[6])
    else:
        col = (*hex_lin(albedo_hex), 1.0)
        dif.inputs["Color"].default_value = col
        mul.inputs[6].default_value = col
    L(mul.outputs[2], emi.inputs["Color"])
    L(dif.outputs["BSDF"], add.inputs[0])
    L(emi.outputs["Emission"], add.inputs[1])
    L(add.outputs["Shader"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def emission_material(name, hex_color, strength=1.0):
    m = bpy.data.materials.new(name)
    nt = _clean(m)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emi = nt.nodes.new("ShaderNodeEmission")
    emi.inputs["Color"].default_value = (*hex_lin(hex_color), 1.0)
    emi.inputs["Strength"].default_value = strength
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def _textures(tex_dir):
    """plank floor (boards run along y, toward the wall) and wall grid (0.5 D squares, heavier lines every 1 D), PIL."""
    import numpy as np
    from PIL import Image, ImageDraw
    os.makedirs(tex_dir, exist_ok=True)
    fp, wp = os.path.join(tex_dir, "stub_floor.png"), os.path.join(tex_dir, "stub_wall.png")
    if not os.path.exists(fp):
        rng = np.random.RandomState(7)
        W = H = 1024                                   # 8 x 8 D tile: boards 0.5 D wide, butt joints every few D
        im = np.zeros((H, W, 3), np.float32)
        base = np.array([150, 96, 58], np.float32)
        for b in range(16):
            tone = base * (0.86 + 0.28 * rng.rand()) + rng.randn(3) * 3
            x0 = b * 64
            grain = (rng.randn(H, 1) * 2.0 + np.cumsum(rng.randn(1, 64), axis=1) * 1.2)
            im[:, x0:x0 + 64] = tone + grain[..., None]
            im[:, x0:x0 + 3] *= 0.45                   # gap between boards
            for _ in range(2):
                y = rng.randint(0, H)
                im[y:y + 3, x0:x0 + 64] *= 0.5
        Image.fromarray(np.clip(im, 0, 255).astype("uint8")).save(fp)
    if not os.path.exists(wp):
        W, H = 1024, 1024                              # 4 x 4 D tile
        im = Image.new("RGB", (W, H), (214, 190, 150))
        d = ImageDraw.Draw(im)
        for i in range(0, 9):
            p = i * 128
            wdt = 6 if i % 2 == 0 else 2
            col = (120, 84, 60) if i % 2 == 0 else (168, 138, 104)
            d.rectangle([p - wdt // 2, 0, p + wdt // 2, H], fill=col)
            d.rectangle([0, p - wdt // 2, W, p + wdt // 2], fill=col)
        im.save(wp)
    return fp, wp


def _box(name, lo, hi, mat, scene, uv_scale=None, uv_axes="xy"):
    """axis-aligned box with real thickness; UVs = world coordinates / uv_scale on the two axes that span each face."""
    import bmesh
    lo, hi = Vector(lo), Vector(hi)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((lo.x + (v.co.x + 0.5) * (hi.x - lo.x), lo.y + (v.co.y + 0.5) * (hi.y - lo.y), lo.z + (v.co.z + 0.5) * (hi.z - lo.z)))
    uvl = bm.loops.layers.uv.active
    s = float(uv_scale or 1.0)
    bm.normal_update()
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for lp in f.loops:
            c = lp.vert.co
            if ax == 2:
                lp[uvl].uv = (c.x / s, c.y / s)
            elif ax == 1:
                lp[uvl].uv = (c.x / s, c.z / s)
            else:
                lp[uvl].uv = (c.y / s, c.z / s)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    scene.collection.objects.link(ob)
    return ob


def build(scene=None, tex_dir=None, elev=38.0, az=-55.0, sun_angle=1.5, A=A_TEST, K=K_TEST):
    """build the stub room into `scene`.  Returns dict(sun, floor, wall, box, materials, mark).
    az: azimuth of the light's TRAVEL direction, 0 = travelling +Y (toward the wall), -90 = travelling +X.  The default
    (-55) is the spec's key: from camera-left, above and behind the camera, shadows fall to screen right and up the wall.
    mark(point, name, color="#18c8d8", size=0.05) adds a small emissive cross on the wall plane at a world point."""
    scene = scene or bpy.context.scene
    tex_dir = tex_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")
    fp, wp = _textures(tex_dir)
    fimg = bpy.data.images.load(fp, check_existing=True)
    wimg = bpy.data.images.load(wp, check_existing=True)
    m_floor = lit_material("stub_floor", image=fimg, A=A)
    m_wall = lit_material("stub_wall", image=wimg, A=A)
    m_box = lit_material("stub_box", "#3f6f9f", A=A)
    m_side = lit_material("stub_sidewall", "#8f5a44", A=A)
    floor = _box("stub_floor", (-8.0, -16.0, -0.3), (8.0, 0.0, 0.0), m_floor, scene, uv_scale=8.0)
    wall = _box("stub_wall", (-8.0, 0.0, -0.3), (8.0, 0.4, 7.0), m_wall, scene, uv_scale=4.0)
    side = _box("stub_sidewall", (8.0, -16.0, -0.3), (8.4, 0.4, 7.0), m_side, scene)
    box = _box("stub_box", (2.1, -1.5, 0.0), (3.3, -0.5, 1.3), m_box, scene)
    k = max(K)
    sd = bpy.data.lights.new("key_sun", "SUN")
    sd.color = tuple(x / k for x in K)
    sd.energy = math.pi * k
    sd.angle = math.radians(sun_angle)
    sun = bpy.data.objects.new("key_sun", sd)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(90.0 - elev), 0.0, math.radians(az))
    if scene.world is None:
        w = bpy.data.worlds.new("StubWorld")
        scene.world = w
    nt = scene.world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    bg = nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg.inputs["Color"].default_value = (*hex_lin("#2a2440"), 1.0)
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    marks = {}

    def mark(point, name="mark", color="#18c8d8", size=0.05, thick=0.012):
        """emissive cross lying on the wall plane (y = point.y - 0.002) centred on `point`."""
        p = Vector(point)
        mat = marks.get(color) or emission_material("stub_mark_" + color.lstrip("#"), color, 1.0)
        marks[color] = mat
        obs = []
        for i, (sx, sz) in enumerate(((size, thick), (thick, size))):
            me = bpy.data.meshes.new("%s_%d" % (name, i))
            y = p.y - 0.002
            me.from_pydata([(p.x - sx, y, p.z - sz), (p.x + sx, y, p.z - sz), (p.x + sx, y, p.z + sz), (p.x - sx, y, p.z + sz)], [], [(0, 1, 2, 3)])
            ob = bpy.data.objects.new("%s_%d" % (name, i), me)
            ob.data.materials.append(mat)
            ob.visible_shadow = False
            scene.collection.objects.link(ob)
            obs.append(ob)
        return obs

    return dict(sun=sun, floor=floor, wall=wall, box=box, side=side, mark=mark,
                materials=dict(floor=m_floor, wall=m_wall, box=m_box, side=m_side))
