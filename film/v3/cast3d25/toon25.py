#!/usr/bin/env python3
"""toon25.py -- film-25 cast as 3D TOON characters (bpy only, procedural, no external assets).  Our designs and colours
(cast25): general25 (stout, big belly, khaki service dress, scarlet sash / gorget tabs / cap band, white walrus moustache)
and tommy_a25 (slim Tommy, khaki, buff webbing, drab-green Brodie).  See API.md.

    import toon25 as T
    gen = T.build_general(name='gen')            # -> Char: .root (empty at the feet, faces -Y), .joints, .set_pose(), .set_mouth()
    tom = T.build_tommy(name='tom')
    gen.root.location = (x, y, z); gen.root.rotation_euler.z = yaw
    gen.set_pose('point_stick'); gen.set_mouth('talk_b')

Units: 1 D = one head diameter (the set's units).  Faces: swappable alpha DECALS rasterised from the cast25 puppet's own
face (eyes, brows, moustache, cheeks, mouth) through v3/set3d/raster.js, projected on the front of the head.
Outline: an inverted hull (solidify, flipped normals) whose material is dark #3a2832 on front faces and transparent on
back faces (the Cycles equivalent of backface culling).
"""
import os, sys, math, json, hashlib, subprocess, copy
import bpy
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(HERE, "decals")
INK = "#3a2832"
FACE = "#fef7f6"


def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


# ----------------------------------------------------------------------------- materials
def _nt(m):
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    return nt, nt.links.new


def mat_toon(name, col, rough=0.5, sheen=0.25, img=None):
    """Principled, roughness 0.5, light sheen; colour from `col` or an image (UV)."""
    m = bpy.data.materials.new(name); nt, L = _nt(m)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bs.inputs["Roughness"].default_value = rough
    for k in ("Sheen Weight", "Sheen"):
        if k in bs.inputs:
            bs.inputs[k].default_value = sheen; break
    if "Specular IOR Level" in bs.inputs:
        bs.inputs["Specular IOR Level"].default_value = 0.25
    if img:
        ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = bpy.data.images.load(img); ti.interpolation = "Cubic"
        L(ti.outputs["Color"], bs.inputs["Base Color"])
    else:
        bs.inputs["Base Color"].default_value = (*lin(col), 1)
    L(bs.outputs[0], out.inputs["Surface"])
    return m


def mat_outline(name="toon_outline"):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); nt, L = _nt(m)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*lin(INK), 1); em.inputs["Strength"].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); geo = nt.nodes.new("ShaderNodeNewGeometry"); lp = nt.nodes.new("ShaderNodeLightPath")
    mx = nt.nodes.new("ShaderNodeMixShader"); mx2 = nt.nodes.new("ShaderNodeMixShader")
    L(geo.outputs["Backfacing"], mx.inputs[0]); L(em.outputs[0], mx.inputs[1]); L(tr.outputs[0], mx.inputs[2])
    L(lp.outputs["Is Camera Ray"], mx2.inputs[0]); L(tr.outputs[0], mx2.inputs[1]); L(mx.outputs[0], mx2.inputs[2])   # only camera rays see the outline
    L(mx2.outputs[0], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def mat_head(name, decal_img):
    """head: Principled #fef7f6 + a front-projected alpha decal (object coords x, z -> uv on the -Y half)."""
    m = bpy.data.materials.new(name); nt, L = _nt(m)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bs = nt.nodes.new("ShaderNodeBsdfPrincipled"); bs.inputs["Roughness"].default_value = 0.55
    for k in ("Sheen Weight", "Sheen"):
        if k in bs.inputs:
            bs.inputs[k].default_value = 0.15; break
    if "Specular IOR Level" in bs.inputs:
        bs.inputs["Specular IOR Level"].default_value = 0.2
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sep.inputs[0])
    cu = nt.nodes.new("ShaderNodeMath"); cu.operation = "MULTIPLY_ADD"; cu.inputs[1].default_value = 1.0; cu.inputs[2].default_value = 0.5; L(sep.outputs["X"], cu.inputs[0])
    cv = nt.nodes.new("ShaderNodeMath"); cv.operation = "MULTIPLY_ADD"; cv.inputs[1].default_value = 1.0; cv.inputs[2].default_value = 0.5; L(sep.outputs["Z"], cv.inputs[0])
    cm = nt.nodes.new("ShaderNodeCombineXYZ"); L(cu.outputs[0], cm.inputs["X"]); L(cv.outputs[0], cm.inputs["Y"])
    ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = bpy.data.images.load(decal_img); ti.extension = "CLIP"; ti.interpolation = "Cubic"; L(cm.outputs[0], ti.inputs[0])
    front = nt.nodes.new("ShaderNodeMath"); front.operation = "LESS_THAN"; front.inputs[1].default_value = -0.05; L(sep.outputs["Y"], front.inputs[0])
    a = nt.nodes.new("ShaderNodeMath"); a.operation = "MULTIPLY"; L(ti.outputs["Alpha"], a.inputs[0]); L(front.outputs[0], a.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.inputs[6].default_value = (*lin(FACE), 1)
    L(a.outputs[0], mix.inputs[0]); L(ti.outputs["Color"], mix.inputs[7]); L(mix.outputs[2], bs.inputs["Base Color"])
    L(bs.outputs[0], out.inputs["Surface"])
    m["decal_node"] = ti.name
    return m


# ----------------------------------------------------------------------------- meshes
def _obj(name, me, parent=None, mats=(), outline=0.03, smooth=True):
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for m in mats:
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    if parent is not None:
        ob.parent = parent
    if outline:
        me.materials.append(mat_outline())
        sd = ob.modifiers.new("outline", "SOLIDIFY"); sd.thickness = outline; sd.offset = 1.0; sd.use_flip_normals = True
        sd.material_offset = len(me.materials) - 1; sd.use_rim = False
    return ob


def lathe(name, prof, seg=40, bulge=None, uv=True):
    """surface of revolution about Z: prof = [(z, r)] bottom -> top; bulge(z, c) -> radial factor (c = cos to the FRONT, -Y).
    UV: u = angle / 2pi (u 0.5 = front, -Y), v = (z - z0) / (z1 - z0)."""
    vs, fs, uvs = [], [], []
    z0, z1 = prof[0][0], prof[-1][0]
    for i, (z, r) in enumerate(prof):
        for j in range(seg + 1):
            a = 2 * math.pi * j / seg; x, y = math.sin(a), -math.cos(a) * -1
            # angle 0 -> +Y (back), pi -> -Y (front)
            x, y = math.sin(a), math.cos(a)
            c = -y
            k = bulge(z, c) if bulge else 1.0
            vs.append((x * r * k, y * r * k * (0.92 if bulge else 1.0), z))
    n = seg + 1
    for i in range(len(prof) - 1):
        for j in range(seg):
            fs.append((i * n + j, i * n + j + 1, (i + 1) * n + j + 1, (i + 1) * n + j))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    if uv:
        ul = me.uv_layers.new(name="UVMap")
        for p in me.polygons:
            for li, vi in zip(p.loop_indices, p.vertices):
                i, j = divmod(vi, n); ul.data[li].uv = (j / seg, (prof[i][0] - z0) / (z1 - z0))
    return me


def sphere(name, r, scale=(1, 1, 1), seg=32, rings=16):
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    for v in bm.verts:
        v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me


def capsule(name, length, r0, r1=None, seg=16):
    """limb segment along -Z from the joint (0,0,0) to (0,0,-length), rounded ends"""
    r1 = r0 if r1 is None else r1
    prof = []
    for k in range(5):
        a = math.pi / 2 * k / 4; prof.append((-length - r1 * math.cos(a) + 0 * k, r1 * math.sin(a) + 1e-4))
    prof.append((-length, r1)); prof.append((0.0, r0))
    for k in range(1, 5):
        a = math.pi / 2 * k / 4; prof.append((r0 * math.sin(a), r0 * math.cos(a) + 1e-4))
    prof.sort(key=lambda t: t[0])
    return lathe(name, prof, seg, uv=False)


def frustum(name, z0, z1, r0, r1, seg=40, cap=True, yscale=1.0):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=cap, segments=seg, radius1=r0, radius2=r1, depth=z1 - z0)
    for v in bm.verts:
        v.co.z += (z0 + z1) / 2; v.co.y *= yscale
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me


def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.empty_display_size = 0.1
    if parent is not None:
        e.parent = parent
    e.location = loc; e.rotation_mode = "XYZ"; return e


# ----------------------------------------------------------------------------- textures (uniform painted on the body UV)
def paint_uniform(path, kind):
    """cylindrical UV image 1024x512 of the torso (u 0.5 = front centre, v 0 = hip line, v 1 = collar)"""
    from PIL import Image, ImageDraw
    W, H = 1024, 512
    if kind == "general":
        base, dark = "#8f813f", "#645a24"
    else:
        base, dark = "#8a7d3c", "#5e5529"
    im = Image.new("RGB", (W, H), base); d = ImageDraw.Draw(im)
    fx = W // 2
    Y = lambda v: int((1 - v) * H)
    d.rectangle([0, Y(1.0), W, Y(0.93)], fill=dark if kind == "general" else "#7a6e34")          # collar
    if kind == "general":
        d.rectangle([0, Y(0.20), W, Y(0.12)], fill="#6a4222")                                     # Sam Browne belt
        d.rectangle([fx - 22, Y(0.215), fx + 22, Y(0.105)], outline="#f6c21c", width=6)           # buckle
        for v in (0.80, 0.64, 0.48, 0.33):
            d.ellipse([fx - 9, Y(v) - 9, fx + 9, Y(v) + 9], fill="#f6c21c", outline="#8a6a10", width=2)   # brass buttons
        # scarlet sash: from the figure's right shoulder (screen-left in front view = u > 0.5? front view: +X is screen-right)
        sw = 46
        p0, p1 = (fx - 150, Y(0.99)), (fx + 170, Y(0.17))          # u > 0.5 is screen-LEFT in a front view
        d.line([p0, p1], fill="#e8231a", width=sw)
        d.line([(fx + 150 - 260, Y(0.99)), (fx + 150 - 260, Y(0.99))], fill="#e8231a", width=1)
        d.rectangle([fx - 70, Y(0.99), fx - 34, Y(0.90)], fill="#e8231a"); d.rectangle([fx + 34, Y(0.99), fx + 70, Y(0.90)], fill="#e8231a")   # gorget tabs
        d.ellipse([fx - 58, Y(0.955) - 6, fx - 46, Y(0.955) + 6], fill="#f6c21c"); d.ellipse([fx + 46, Y(0.955) - 6, fx + 58, Y(0.955) + 6], fill="#f6c21c")
        cols = ["#2050c0", "#e0b020", "#c02020", "#208040", "#f0f0f0", "#8030a0"]                # one block of plain ribbons (left chest = screen-right)
        x0, y0 = fx - 40 - 96, Y(0.80)
        for r in range(2):
            for c in range(6):
                d.rectangle([x0 + c * 16, y0 + r * 14, x0 + c * 16 + 15, y0 + r * 14 + 12], fill=cols[(c + r * 2) % 6])
    else:
        d.rectangle([0, Y(0.20), W, Y(0.11)], fill="#b8a870")                                     # webbing belt
        d.line([(fx - 90, Y(1.0)), (fx - 60, Y(0.2))], fill="#b8a870", width=26)                 # braces
        d.line([(fx + 90, Y(1.0)), (fx + 60, Y(0.2))], fill="#b8a870", width=26)
        d.rectangle([fx - 150, Y(0.20), fx - 92, Y(0.06)], fill="#8c8055"); d.rectangle([fx + 92, Y(0.20), fx + 150, Y(0.06)], fill="#8c8055")   # pouches
        for v in (0.82, 0.62, 0.42):
            d.ellipse([fx - 8, Y(v) - 8, fx + 8, Y(v) + 8], fill="#d0a830")
        d.rectangle([fx - 120, Y(1.0), fx + 120, Y(0.94)], fill="#f01818")                       # red muffler at the neck
    im.save(path); return path


# ----------------------------------------------------------------------------- face decals from the cast25 puppet
def face_decal(member, expr, mouth, px=512):
    """rasterise the puppet's own face (no hat) and keep only the features: alpha = distance from the skin colour,
    clipped to the head disc.  Returns the PNG path (cached)."""
    sys.path.insert(0, os.path.join(PROJ, "v3", "cast25"))
    import cast25, puppet                                                     # noqa: F401
    from PIL import Image
    import numpy as np
    os.makedirs(CACHE, exist_ok=True)
    p = dict(yaw=0.0, pitch=0.0, expr=expr, arm_r="down", arm_l="down", legs="stand", hat_off25=1, finish25=0, rim25=0)
    if mouth:
        p["mouth"] = mouth
    f = puppet.figure(member, p, "d")
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="-0.5 -0.5 1 1" style="display:block">%s</svg>' % (px, px, f["svg"])
    tag = "%s_%s_%s_%s" % (member, expr, mouth or "x", hashlib.sha1(svg.encode()).hexdigest()[:8])
    out = os.path.join(CACHE, tag + ".png")
    if os.path.exists(out):
        return out
    raw = os.path.join(CACHE, tag + "_raw.png"); sp = os.path.join(CACHE, tag + ".svg"); open(sp, "w").write(svg)
    jp = os.path.join(CACHE, tag + "_job.json"); json.dump([dict(src=sp, out=raw, w=px, h=px, transparent=True)], open(jp, "w"))
    r = subprocess.run(["node", os.path.join(PROJ, "v3", "set3d", "raster.js"), jp], capture_output=True,
                       env=dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")))
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-400:])
    a = np.asarray(Image.open(raw).convert("RGBA")).astype(np.float32) / 255
    skin = np.array([0xfe, 0xf7, 0xf6], np.float32) / 255
    dist = np.abs(a[..., :3] - skin).sum(-1)
    al = np.clip((dist - 0.06) / 0.18, 0, 1) * a[..., 3]
    yy, xx = np.mgrid[0:px, 0:px]; rr = np.hypot(xx - px / 2 + 0.5, yy - px / 2 + 0.5) / (px / 2)
    al *= np.clip((0.80 - rr) / 0.05, 0, 1)                                    # drop the head outline ring (the 3D outline draws it)
    o = np.dstack([a[..., :3], al]); Image.fromarray((o * 255 + 0.5).astype(np.uint8)).save(out)
    for t in (raw, sp, jp):
        os.remove(t)
    return out


MOUTHS = ("talk_a", "talk_b", "talk_o", "flat", "laugh")


# ----------------------------------------------------------------------------- character
class Char(object):
    def __init__(self, name):
        self.name = name; self.root = None; self.joints = {}; self.head = None; self.decals = {}; self.mats = {}

    def set_mouth(self, mouth):
        """swap the face decal: mouth in MOUTHS ('laugh' = the laughing expression)"""
        img = self.decals[mouth]
        m = self.head.data.materials[0]; ti = m.node_tree.nodes[m["decal_node"]]
        ti.image = bpy.data.images.load(img, check_existing=True)

    def set_pose(self, pose, **over):
        """pose: a preset name (POSES) or a dict {joint: (rx, ry, rz) degrees}; walk / march: set_pose('walk', phase=0..1)"""
        if isinstance(pose, str):
            d = POSES[pose](over.pop("phase", 0.0)) if callable(POSES[pose]) else dict(POSES[pose])
        else:
            d = dict(pose)
        d.update(over)
        for j, e in self.joints.items():
            fwd, out, tw = d.get(j, (0, 0, 0))                                 # degrees: forward swing, out to the side, twist
            sd = 1.0 if j.endswith("_r") else -1.0                              # the right side is -X: +Y rotation swings a hanging limb out to -X
            e.rotation_euler = Euler((math.radians(-fwd), math.radians(out * sd), math.radians(tw)), "XYZ")
        bpy.context.view_layer.update()


def _build(name, kind):
    C = Char(name)
    gen = kind == "general"
    root = empty(name + "_root"); C.root = root
    col_base = "#8f813f" if gen else "#8a7d3c"
    tex = paint_uniform(os.path.join(CACHE if os.makedirs(CACHE, exist_ok=True) is None else CACHE, "uniform_%s.png" % kind), kind)
    m_body = mat_toon(name + "_body", None, 0.55, 0.3, img=tex)
    m_cloth = mat_toon(name + "_cloth", col_base, 0.6, 0.3)
    m_hand = mat_toon(name + "_hand", INK, 0.5, 0.1)
    m_boot = mat_toon(name + "_boot", "#7a4524" if gen else "#4a3020", 0.35, 0.1)
    m_putt = mat_toon(name + "_puttee", "#7d7038", 0.7, 0.2)
    # --- proportions (D)
    if gen:
        hip_z, sh_z, head_z = 1.05, 2.30, 2.80
        prof = [(0.85, 0.62), (1.0, 0.86), (1.3, 0.98), (1.6, 0.98), (1.9, 0.90), (2.15, 0.76), (2.32, 0.55), (2.40, 0.30)]
        belly = lambda z, c: 1.0 + 0.22 * max(0.0, c) ** 1.5 * math.exp(-((z - 1.45) / 0.38) ** 2)
        arm = (0.62, 0.55, 0.15, 0.14); leg = (0.50, 0.50, 0.19, 0.16); hip_x, sh_x = 0.38, 0.78
    else:
        hip_z, sh_z, head_z = 1.25, 2.38, 2.86
        prof = [(1.10, 0.42), (1.25, 0.52), (1.6, 0.56), (1.95, 0.58), (2.2, 0.55), (2.38, 0.40), (2.45, 0.22)]
        belly = lambda z, c: 1.0 + 0.04 * max(0.0, c) * math.exp(-((z - 1.7) / 0.4) ** 2)
        arm = (0.62, 0.58, 0.12, 0.11); leg = (0.62, 0.62, 0.14, 0.12); hip_x, sh_x = 0.25, 0.56
    ol = 0.018                                                                # outline thickness ~1.8 % of the head
    body = _obj(name + "_torso", lathe(name + "_torso", prof, 48, belly), root, [m_body], ol)
    # head + face decal
    for mo in MOUTHS:
        expr = "laughing" if mo == "laugh" else ("smug" if gen else "determined")
        C.decals[mo] = face_decal("general25" if gen else "tommy_a25", expr, None if mo == "laugh" else mo)
    hm = mat_head(name + "_head", C.decals["flat"])
    C.head = _obj(name + "_head", sphere(name + "_head", 0.5, (1.0, 0.92, 0.96)), root, [hm], ol)
    C.head.location = (0, 0, head_z)
    # hat
    if gen:
        olive, band, blk = mat_toon(name + "_cap", "#8a7c3a", 0.6, 0.3), mat_toon(name + "_band", "#ee2418", 0.5, 0.2), mat_toon(name + "_peak", "#1e1a22", 0.25, 0.1)
        cz = head_z + 0.18
        _obj(name + "_crown", frustum(name + "_crown", cz + 0.14, cz + 0.30, 0.50, 0.68, yscale=0.92), root, [olive], ol)     # flat-topped crown, wider at the top
        _obj(name + "_band", frustum(name + "_band", cz - 0.06, cz + 0.15, 0.50, 0.51), root, [band], ol)                       # broad scarlet band
        pk = _obj(name + "_peak", sphere(name + "_peak", 0.5, (0.60, 0.62, 0.05), 32, 8), root, [blk], ol)
        pk.location = (0, -0.36, cz - 0.08); pk.rotation_euler = (math.radians(-18), 0, 0)
        bt = _obj(name + "_button", sphere(name + "_button", 0.055), root, [mat_toon(name + "_brass", "#f6c21c", 0.3, 0.1)], 0.0)
        bt.location = (0, -0.50, cz + 0.05)
    else:
        green = mat_toon(name + "_brodie", "#5f8c2a", 0.55, 0.2)
        dome = _obj(name + "_dome", sphere(name + "_dome", 0.5, (0.98, 0.98, 0.55)), root, [green], ol); dome.location = (0, 0, head_z + 0.20)
        brim = _obj(name + "_brim", frustum(name + "_brim", head_z + 0.12, head_z + 0.17, 0.80, 0.70), root, [green], ol)
    # limbs on joint empties (shoulder -> elbow -> hand ; hip -> knee -> foot); rest pose hangs along -Z
    def limb(side, base, up, lo, r0, r1, m_up, m_lo, end):
        s = 1 if side == "r" else -1                                          # 'r' = the character's right = screen-left in a front view (-X)
        j0 = empty("%s_%s_%s" % (name, base[0], side), root, (-s * base[1], 0.0, base[2]))
        _obj(j0.name + "_m", capsule(j0.name + "_m", up, r0, r0 * 0.95), j0, [m_up], ol)
        j1 = empty("%s_%s_%s" % (name, base[3], side), j0, (0, 0, -up))
        _obj(j1.name + "_m", capsule(j1.name + "_m", lo, r0 * 0.95, r1), j1, [m_lo], ol)
        C.joints[j0.name.split(name + "_")[1]] = j0; C.joints[j1.name.split(name + "_")[1]] = j1
        return j1, s
    for side in ("r", "l"):
        el, s = limb(side, ("shoulder", sh_x, sh_z, "elbow"), arm[0], arm[1], arm[2], arm[3], m_cloth, m_cloth, None)
        hd = _obj("%s_hand_%s" % (name, side), sphere("%s_hand_%s" % (name, side), 0.15, (1, 0.9, 1.1)), el, [m_hand], ol); hd.location = (0, 0, -arm[1] - 0.08)
        kn, s = limb(side, ("hip", hip_x, hip_z, "knee"), leg[0], leg[1], leg[2], leg[3], m_cloth, m_boot if gen else m_putt, None)
        bt = _obj("%s_boot_%s" % (name, side), sphere("%s_boot_%s" % (name, side), 0.2, (0.95, 1.5, 0.75)), kn, [m_boot], ol)
        bt.location = (0, -0.10, -leg[1] - 0.06)
    if gen:                                                                   # swagger stick in the right hand
        hr = bpy.data.objects[name + "_hand_r"]
        st = _obj(name + "_stick", frustum(name + "_stick", -1.10, 0.10, 0.03, 0.04, 12), hr, [mat_toon(name + "_wood", "#6a3a1c", 0.3, 0.1)], 0.012)
        st.location = (0, 0, 0)                                                # continues the forearm line (-Z of the hand)
        kb = _obj(name + "_knob", sphere(name + "_knob", 0.07), st, [mat_toon(name + "_brass2", "#f6c21c", 0.3, 0.1)], 0.0); kb.location = (0, 0, -1.10)
    # contact: everything stands with the boot soles on z = 0 of the root
    C.kind = kind; C.feet_z = 0.0
    C.set_pose("stand")
    return C


def build_general(name="gen"):
    return _build(name, "general")


def build_tommy(name="tom"):
    return _build(name, "tommy")


# ----------------------------------------------------------------------------- poses: {joint: (forward, out, twist)} degrees; forward + = limb swings to the front (knees: negative bends back)
def _walk(ph, amp=28.0, knee=35.0, arm=26.0, march=False):
    s = math.sin(2 * math.pi * ph); c = math.sin(2 * math.pi * ph + math.pi)
    hipr, hipl = (-amp * s, -amp * c) if not march else (-60 * max(s, 0) + 10 * min(s, 0), -60 * max(c, 0) + 10 * min(c, 0))
    return {"shoulder_r": (arm * c, 6, 0), "shoulder_l": (arm * s, 6, 0), "elbow_r": (25, 0, 0), "elbow_l": (25, 0, 0),
            "hip_r": (-hipr, 0, 0), "hip_l": (-hipl, 0, 0), "knee_r": (-(knee * max(0, s) + (50 if march and s > 0 else 0)), 0, 0),
            "knee_l": (-(knee * max(0, c) + (50 if march and c > 0 else 0)), 0, 0)}


POSES = {
    "stand": {"shoulder_r": (0, 10, 0), "shoulder_l": (0, 10, 0), "elbow_r": (10, 0, 0), "elbow_l": (10, 0, 0)},
    "point_stick": {"shoulder_r": (35, 80, 0), "elbow_r": (10, 0, 0),                   # stick arm out to his right side, a little forward
                    "shoulder_l": (-5, 40, 0), "elbow_l": (100, -60, 0),               # other fist on the hip
                    "hip_r": (0, 6, 0), "hip_l": (0, 6, 0)},
    "laugh": {"shoulder_r": (25, 25, 0), "elbow_r": (80, -40, 0), "shoulder_l": (25, 25, 0), "elbow_l": (80, -40, 0), "hip_r": (0, 6, 0), "hip_l": (0, 6, 0)},
    "walk": lambda ph: _walk(ph),
    "march": lambda ph: _walk(ph, march=True, arm=40),
}
