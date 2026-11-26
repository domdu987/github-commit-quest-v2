"""core.py -- shared helpers of the EP.1 sets (scenes 02-04).  Imports v11/set (and through it v4) read-only.

Units as everywhere in the project: 1 BU = 1 D = 0.6 m, Z up, deck top z = 0, traffic runs +Y (= path length s) for
s < 420, lateral offset o = world X (our carriageway o -22.15 .. -0.75; the left barrier, the shoulder side, is -X).
Object index: 1 road, 2 cast, 3 car bodies, 4 everything else.
"""
import os, sys, math, random, json
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(PROJ, "v11", "set"), HERE):
    if p not in sys.path: sys.path.insert(0, p)
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, Euler
import beauty as B

X = B.X; kit = B.kit; V = B.V; tex = B.tex
from kit import MB, hexlin

TEX = os.path.join(HERE, "tex"); os.makedirs(TEX, exist_ok=True)
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
REG = {}            # everything a builder returns, by set key ("x1", "sedan", "x2", "cab", "gear", "stair", "under")


def coll(name="EP1_SETS"):
    return kit.coll(name)


def lights_coll():
    return bpy.data.collections.get("LIGHTS") or kit.coll("LIGHTS")


def P(s, o, z=0.0):
    return Vector(X.P(s, o, z))


def empty(name, loc=(0, 0, 0), parent=None, c=None, rot=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None); (c or coll()).objects.link(ob)
    ob.location = loc; ob.rotation_euler = rot
    if parent is not None: ob.parent = parent
    return ob


def box(name, size, loc, mat, parent=None, bevel=0.0, rot=(0, 0, 0), c=None, idx=4):
    ob = kit.box(name, size, loc, c or coll(), mat, bevel=bevel, rot=rot)
    if parent is not None: ob.parent = parent
    ob.pass_index = idx
    return ob


def cyl(name, r, h, loc, mat, parent=None, rot=(0, 0, 0), c=None, idx=4, segs=12):
    ob = kit.cyl(name, r, h, c or coll(), segs, mat, loc=loc, rot=rot)
    if parent is not None: ob.parent = parent
    ob.pass_index = idx
    return ob


def lathe(name, profile, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), c=None, idx=4, segs=16, axis="Z", cap=True):
    ob = kit.lathe(name, profile, c or coll(), segs, mat, axis=axis, cap=cap)
    ob.location = loc; ob.rotation_euler = rot
    if parent is not None: ob.parent = parent
    ob.pass_index = idx
    return ob


def quad(name, w, h, loc, facing, mat, parent=None, rot=None, c=None, idx=4):
    ob = kit.quad(name, w, h, loc, facing, c or coll(), mat)
    if rot is not None: ob.rotation_euler = rot
    if parent is not None: ob.parent = parent
    ob.pass_index = idx
    return ob


def tube(name, pts, r, mat, parent=None, c=None, idx=4, segs=8):
    """a bent tube through pts (local points): one mesh, ring per point."""
    pts = [Vector(p) for p in pts]
    rings = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
        a = d.cross(up).normalized(); b = d.cross(a).normalized()
        rings.append([tuple(p + (a * math.cos(2 * math.pi * k / segs) + b * math.sin(2 * math.pi * k / segs)) * r) for k in range(segs)])
    v, f, seg, st, uv = kit.loft(rings, True, True, True)
    ob = kit.mesh_obj(name, v, f, c or coll(), uvs=uv, mat=mat, smooth=True, sharp_angle=60)
    if parent is not None: ob.parent = parent
    ob.pass_index = idx
    return ob


def tree(ob):
    return [ob] + list(ob.children_recursive)


def show(root, on=True):
    for o in tree(root): o.hide_render = not on; o.hide_viewport = not on


def set_index(root, idx):
    for o in tree(root):
        if o.type in ("MESH", "CURVE"): o.pass_index = idx


def world_box(root):
    """world AABB of an object tree (meshes only)."""
    bpy.context.view_layer.update()
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for o in tree(root):
        if o.type != "MESH": continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z))); hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
    return tuple(round(x, 3) for x in lo), tuple(round(x, 3) for x in hi)


def wpt(root, local):
    bpy.context.view_layer.update()
    return tuple(root.matrix_world @ Vector(local))


# ------------------------------------------------------------------------------------------------------- materials
def simple(name, col, rough=0.5, metal=0.0, coat=0.0):
    return kit.m_simple("ep1_" + name, col, rough, metal, coat)


def emit(name, col, strength):
    """a unique emission material; .["node"] is not storable, use set_emit()."""
    name = "ep1_" + name
    m = bpy.data.materials.get(name)
    if m is None:
        mb = MB(name); c = hexlin(col) if isinstance(col, str) else (tuple(col) + (1,))[:4]
        e = mb.n("ShaderNodeEmission", Color=c, Strength=strength); e.name = "E"
        mb.out(e); m = mb.m
    return m


def set_emit(m, strength=None, col=None):
    if isinstance(m, str): m = bpy.data.materials.get(m if m.startswith("ep1_") else "ep1_" + m)
    if m is None: return
    e = m.node_tree.nodes.get("E")
    if e is None: return
    if strength is not None: e.inputs["Strength"].default_value = strength
    if col is not None: e.inputs["Color"].default_value = (tuple(col) + (1,))[:4]


def key_emit(m, frames_values, period=None):
    """key an emission material's strength; cycles forever."""
    e = m.node_tree.nodes["E"]
    kit.key_series(e.inputs["Strength"], "default_value", m.node_tree, frames_values, "CONSTANT")


def image_mat(name, path, rough=0.5, emit_strength=0.0, alpha=False, coat=0.0, ext="EXTEND"):
    return X.m_textured("ep1_" + name, path, rough=rough, emit=emit_strength, coat=coat, alpha=alpha, ext=ext)


def glass_clear(name="ep1_glass", tint=(0.80, 0.84, 0.88), wet=True, gloss=0.08, bump=0.5, scale=2.0):
    """see-through glass (transparent + Fresnel gloss, no refraction: cheap and noise free) with rain beads as bump
    and as slightly frosted dots, so a wet pane reads as wet from both sides."""
    m = bpy.data.materials.get(name)
    if m: return m
    mb = MB(name)
    tr = mb.n("ShaderNodeBsdfTransparent", Color=(*tint, 1))
    gl = mb.n("ShaderNodeBsdfGlossy", Roughness=0.04)
    fr = mb.n("ShaderNodeFresnel", IOR=1.45)
    fac = mb.math("ADD", fr.outputs[0], gloss)
    if wet:
        gen = mb.n("ShaderNodeTexCoord")
        mp = mb.n("ShaderNodeMapping", Scale=(scale, scale, scale)); mb.l(gen.outputs["UV"], mp.inputs[0])
        dr = mb.tex(tex.droplets(), mp.outputs[0], noncolor=True, ext="REPEAT")
        nrm = kit.bump_node(mb, dr.outputs["Color"], bump, 0.01)
        mb.l(nrm, gl.inputs["Normal"]); mb.l(nrm, fr.inputs["Normal"])
        fac = mb.math("ADD", fac, mb.math("MULTIPLY", dr.outputs["Color"], 0.22))
    mx = mb.n("ShaderNodeMixShader"); mb.l(fac, mx.inputs[0]); mb.l(tr.outputs[0], mx.inputs[1]); mb.l(gl.outputs[0], mx.inputs[2])
    return mb.out(mx)


def alpha_card(name, path, col=(1, 1, 1), strength=1.0, alpha_mul=1.0, lit=False, rough=0.6):
    """RGBA image on a card: emission (lit=False) or principled (lit=True) over transparent."""
    name = "ep1_" + name
    m = bpy.data.materials.get(name)
    if m: return m
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    mp = mb.n("ShaderNodeMapping"); mp.name = "MAP"; mb.l(uv.outputs[0], mp.inputs[0])
    t = mb.tex(path, mp.outputs[0], ext="REPEAT")
    c = mb.mix(1.0, t.outputs["Color"], (*col[:3], 1), "MULTIPLY")
    if lit:
        sh = mb.principled(c, rough)
    else:
        sh = mb.n("ShaderNodeEmission", Strength=strength); sh.name = "E"; mb.l(c, sh.inputs["Color"])
    tr = mb.n("ShaderNodeBsdfTransparent")
    mx = mb.n("ShaderNodeMixShader"); a = mb.math("MULTIPLY", t.outputs["Alpha"], alpha_mul, True); a.node.name = "AMUL"
    mb.l(a, mx.inputs[0]); mb.l(tr.outputs[0], mx.inputs[1]); mb.l(sh.outputs[0], mx.inputs[2])
    return mb.out(mx)


# ---------------------------------------------------------------------------------------------------------- lights
def spot(name, loc, aim, energy, col=(1, 1, 1), size_deg=60.0, blend=0.4, radius=0.08, parent=None, kind=None):
    ld = bpy.data.lights.new(name, "SPOT"); ld.energy = energy; ld.color = col
    ld.spot_size = math.radians(size_deg); ld.spot_blend = blend; ld.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, ld); lights_coll().objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if parent is not None: ob.parent = parent
    if kind: ob["kind"] = kind
    return ob


def point(name, loc, energy, col=(1, 1, 1), radius=0.1, parent=None, glossy=True):
    ld = bpy.data.lights.new(name, "POINT"); ld.energy = energy; ld.color = col; ld.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, ld); lights_coll().objects.link(ob)
    ob.location = loc
    if parent is not None: ob.parent = parent
    ob.visible_glossy = glossy
    return ob


def key_light(ob, frames_values, interp="CONSTANT"):
    kit.key_series(ob.data, "energy", ob.data, frames_values, interp)


def light(name, energy=None, on=None):
    """set a light by name: energy and / or on-off. Returns the object (None if it does not exist)."""
    ob = bpy.data.objects.get(name)
    if ob is None or ob.type != "LIGHT": return None
    if energy is not None:
        ad = ob.data.animation_data
        if ad and ad.action: ob.data.animation_data_clear()
        ob.data.energy = energy
    if on is not None: ob.hide_render = not on
    return ob


def retarget(cam):
    """point every camera-facing card (steam, smoke) at the stage camera. Call after building dressing on a Stage."""
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO": con.target = cam


def steam_card(name, pos, w, h, strength=0.42, alpha=0.6, c=None):
    m = X.m_card("ep1_steam", tex.smoke(2), (0.62, 0.62, 0.70), strength, alpha)
    q = kit.quad(name, w, h, (0, 0, 0), "+Y", c or coll(), m)
    q.data.transform(Matrix.Translation((0, 0, h / 2 - 0.2)))
    q.location = pos; q.visible_shadow = False; q["fx"] = "smoke"
    con = q.constraints.new("TRACK_TO"); con.track_axis = "TRACK_Y"; con.up_axis = "UP_Z"; con.use_target_z = False
    con.target = bpy.context.scene.camera
    q.pass_index = 4
    return q


# ----------------------------------------------------------------------------------------------------- small scatter
def shards(name, centres, mat=None, c=None, seed=1, zfn=None):
    """glass crumbs: centres = [((x, y), radius, count)], one mesh."""
    rng = random.Random(seed)
    gm = mat or bpy.data.materials.get("glass_shard") or simple("shard", "#9fb4c0", 0.05)
    verts, faces = [], []
    for cen, rad, cnt in centres:
        for _ in range(cnt):
            r = rad * math.sqrt(rng.random()); a = rng.uniform(0, 2 * math.pi)
            x, y = cen[0] + r * math.cos(a), cen[1] + r * math.sin(a)
            z0 = zfn(x, y) if zfn else (cen[2] if len(cen) > 2 else 0.0)
            e = rng.uniform(0.012, 0.035); rz = rng.uniform(0, math.pi)
            b = len(verts)
            for (dx, dy, dz) in ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)):
                px, py = dx * e, dy * e * rng.uniform(0.5, 1.5)
                verts.append((x + px * math.cos(rz) - py * math.sin(rz), y + px * math.sin(rz) + py * math.cos(rz), z0 + dz * e * 0.6 + 0.004))
            faces += [(b, b + 3, b + 2, b + 1), (b + 4, b + 5, b + 6, b + 7), (b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 6, b + 5), (b + 2, b + 3, b + 7, b + 6), (b + 3, b, b + 4, b + 7)]
    ob = kit.mesh_obj(name, verts, faces, c or coll(), mat=gm)
    ob.pass_index = 4
    return ob


def puddle(name, loc, w, l, rot=0.0, c=None, col="#05070c"):
    """a standing-water mirror decal (dark, coat 1, roughness 0.02) with an irregular outline."""
    m = bpy.data.materials.get("ep1_puddle")
    if m is None:
        mb = MB("ep1_puddle")
        m = mb.out(mb.principled(hexlin(col), 0.02, 0.0, 1.0, spec=1.0, ambient=(0.01, 0.014, 0.03)))
    import zlib
    rng = random.Random(zlib.crc32(name.encode()) & 0xffff)      # (checker) hash(str) is salted per process: every worker and every resume drew a different outline
    n = 18
    verts = [(0, 0, 0)] + [(math.cos(2 * math.pi * k / n) * w / 2 * rng.uniform(0.7, 1.1), math.sin(2 * math.pi * k / n) * l / 2 * rng.uniform(0.7, 1.1), 0) for k in range(n)]
    faces = [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)]
    ob = kit.mesh_obj(name, verts, faces, c or coll(), mat=m)
    ob.location = loc; ob.rotation_euler = (0, 0, rot); ob.pass_index = 1
    ob.visible_shadow = False
    return ob


def top(x, y, z0=6.4):
    """height of the first surface under (x, y)."""
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, n, i, ob, m = bpy.context.scene.ray_cast(dg, Vector((x, y, z0)), Vector((0, 0, -1)))
    return (loc.z, ob.name) if hit else (0.0, None)


def hide_rows(pred):
    """hide the instanced jam cars for which pred(x, y, name) is true. Returns their names."""
    out = []
    rows = bpy.data.collections.get("ROWS")
    if rows is None: return out
    for ob in rows.objects:
        p = ob.matrix_world.translation
        if pred(p.x, p.y, ob.name):
            ob.hide_render = True; ob.hide_viewport = True; out.append(ob.name)
    return out


def font(size):
    from PIL import ImageFont
    return ImageFont.truetype(FONT, size, layout_engine=ImageFont.Layout.RAQM)


def smash_glass(body, pred, rng, name=None, c=None, keep=0.7):
    """delete the glass faces for which pred(face centre, material name) is true and leave teeth round the hole.
    Returns (teeth object, hole centre in body space) or None."""
    me = body.data
    names = [m.name if m else "" for m in me.materials]
    bm = bmesh.new(); bm.from_mesh(me)
    fs = [f for f in bm.faces if names[f.material_index].startswith("glass") and pred(f.calc_center_median(), names[f.material_index])]
    if not fs:
        bm.free(); return None
    sel = set(fs)
    cen = sum((f.calc_center_median() for f in fs), Vector()) / len(fs)
    teeth = []
    for f in fs:
        for e in f.edges:
            if sum(1 for lf in e.link_faces if lf in sel) != 1: continue
            a, b = e.verts[0].co.copy(), e.verts[1].co.copy()
            n = max(1, int((a - b).length / 0.14))
            for k in range(n):
                if rng.random() > keep: continue
                p0 = a.lerp(b, k / n); p1 = a.lerp(b, (k + 1) / n); m = (p0 + p1) / 2
                tip = m + (cen - m).normalized() * rng.uniform(0.04, 0.16)
                teeth.append((tuple(p0), tuple(p1), tuple(tip)))
    bmesh.ops.delete(bm, geom=fs, context="FACES_ONLY")
    bm.to_mesh(me); bm.free()
    verts, faces = [], []
    for t in teeth:
        b = len(verts); verts += list(t); faces.append((b, b + 1, b + 2))
    gm = bpy.data.materials.get("ep1_glass_tooth")
    if gm is None:
        mb = MB("ep1_glass_tooth")
        gm = mb.out(mb.principled((0.10, 0.16, 0.18, 1), 0.06, spec=1.0, ambient=(0.03, 0.04, 0.06)))
    ob = kit.mesh_obj(name or body.name + "_teeth", verts, faces, c or coll(), mat=gm)
    ob.parent = body.parent; ob.pass_index = 4
    return ob, cen


def cut_gap(ob, y0, y1):
    """cut a mesh whose vertices are world points (the deck sweeps) between the planes y = y0 and y = y1."""
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me)
    for y in (y0, y1):
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-5, plane_co=(0, y, 0), plane_no=(0, 1, 0))
    dead = [f for f in bm.faces if y0 < f.calc_center_median().y < y1]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    bm.to_mesh(me); bm.free(); me.update()
    return len(dead)


def draw_tex(name, size, fn, force=False):
    """a code-drawn PNG in ep1/sets/tex (cached by name): fn(PIL.ImageDraw, image) draws it."""
    from PIL import Image, ImageDraw
    p = os.path.join(TEX, name + ".png")
    if force or not os.path.exists(p):
        im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        r = fn(d, im)
        tmp = p + ".%d.tmp.png" % os.getpid()                  # (checker) atomic: four workers start at once and may all find the cache empty
        (r or im).save(tmp); os.replace(tmp, p)
    return p
