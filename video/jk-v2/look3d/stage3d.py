"""Our 2D characters as sprite cards in the 3D town: unlit to the camera, a sun-facing shadow proxy, per-frame sprite swap; camera keys with easing."""
import os, sys, math, json
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import town3d as T
S = T.S
K = 1.8 / 620.0            # world units per rig px (a standing character ~1.8 tall)

def card_mat(name):
    m = bpy.data.materials.new(name); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.extension = 'CLIP'; tex.interpolation = 'Cubic'; tex.name = 'spr'
    lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    L(tex.outputs['Color'], emi.inputs['Color']); L(lp.outputs['Is Camera Ray'], emi.inputs['Strength'])
    L(tex.outputs['Alpha'], mix.inputs['Fac']); L(tr.outputs['BSDF'], mix.inputs[1]); L(emi.outputs['Emission'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
    return m, tex

class Card:
    def __init__(s, name, canvas, coll):
        """canvas = (x0, y0, x1, y1) in rig px relative to the feet (y down)."""
        s.name = name; x0, y0, x1, y1 = canvas; s.canvas = canvas
        s.mat, s.tex = card_mat(name + '_m'); s.img = None
        def mk(nm):
            me = bpy.data.meshes.new(nm); me.from_pydata([(x0 * K, 0, -y1 * K), (x1 * K, 0, -y1 * K), (x1 * K, 0, -y0 * K), (x0 * K, 0, -y0 * K)], [], [(0, 1, 2, 3)]); me.update()
            uv = me.uv_layers.new(name='UVMap')
            for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
            me.materials.append(s.mat); ob = bpy.data.objects.new(nm, me); coll.objects.link(ob); S.no_bounce(ob); return ob
        s.card = mk(name); s.card.visible_shadow = False
        s.proxy = mk(name + '_shadow'); s.proxy.visible_camera = False; s.proxy.visible_glossy = False
        kd = Vector(T.DUSK['key_dir']); dh = Vector((kd.x, kd.y)).normalized(); s.sun_yaw = math.atan2(-dh.x, dh.y)
    def set(s, pos, cam_loc, png, scale=1.0, hidden=False):
        for ob in (s.card, s.proxy): ob.hide_render = hidden
        if hidden: return
        s.card.location = pos; s.proxy.location = pos; s.card.scale = (scale,) * 3; s.proxy.scale = (scale,) * 3
        d = Vector(cam_loc) - Vector(pos); s.card.rotation_euler = (0, 0, math.atan2(-d.x, d.y) + math.pi) if False else (0, 0, math.atan2(d.x, -d.y))
        s.proxy.rotation_euler = (0, 0, s.sun_yaw)
        if s.img is None or s.img.filepath != png:
            old = s.img; s.img = bpy.data.images.load(png); s.tex.image = s.img
            if old is not None and old.users == 0: bpy.data.images.remove(old)

def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ease5(u): u = max(0.0, min(1.0, u)); return u * u * u * (u * (6 * u - 15) + 10)

def cam_at(keys, t):
    """keys: [(t, loc, look_at, lens, ease_fn_name)]. Eased between keys, with a slow constant creep so it is never static."""
    if t <= keys[0][0]: k0 = k1 = keys[0]; u = 0
    else:
        i = 0
        while i + 1 < len(keys) and keys[i + 1][0] < t: i += 1
        k0 = keys[i]; k1 = keys[min(i + 1, len(keys) - 1)]
        u = 0 if k1[0] == k0[0] else (t - k0[0]) / (k1[0] - k0[0])
    f = {'s': ease, 'q': ease5, 'l': lambda x: max(0, min(1, x)), 'o': lambda x: 1 - (1 - max(0, min(1, x))) ** 3}[k1[4] if len(k1) > 4 else 's'](u)
    L = lambda a, b: tuple(a[j] + (b[j] - a[j]) * f for j in range(3))
    return L(k0[1], k1[1]), L(k0[2], k1[2]), k0[3] + (k1[3] - k0[3]) * f

def place_cam(cam, loc, look, lens, roll=0.0):
    cam.location = loc; fwd = (Vector(look) - Vector(loc)).normalized(); cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if roll: cam.rotation_euler.rotate_axis('Z', math.radians(roll))
    cam.data.lens = lens
