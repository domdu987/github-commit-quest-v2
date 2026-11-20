"""c17.py -- helpers for film 17 take s11 (copied in spirit from film8/common.py: cast17 + set3d17/bertillon.py)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                            # before sprites
import bpy
from mathutils import Vector
import actors, sprites, puppet
import bertillon as K

def g_of(t): return int(round((t + 0.10) * 30))

def blink_list(g, ks): return cast17.blink_at(g, 90) if False else 0

def smooth(u):  # smootherstep
    u = max(0.0, min(1.0, u)); return u * u * u * (u * (u * 6 - 15) + 10)

def lerp3(a, b, u): return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))

class CamPath:
    """waypoints [(g, loc, look, kind)]; kind = how to travel from this waypoint to the next: 'drift' (35% sine + 65% linear) or 'snap' (smootherstep)."""
    def __init__(self, pts, shake=0.0): self.pts, self.shake = pts, shake
    def at(self, g):
        pts = self.pts
        if g <= pts[0][0]: seg = 0; u = 0.0
        elif g >= pts[-1][0]: seg = len(pts) - 2; u = 1.0
        else:
            seg = max(i for i in range(len(pts) - 1) if pts[i][0] <= g); u = (g - pts[seg][0]) / float(pts[seg + 1][0] - pts[seg][0])
        a, b = pts[seg], pts[seg + 1]
        e = smooth(u) if a[3] == 'snap' else 0.35 * (0.5 - 0.5 * math.cos(math.pi * u)) + 0.65 * u
        loc, look = lerp3(a[1], b[1], e), lerp3(a[2], b[2], e)
        if self.shake:     # light handheld sway so no frame is static
            s = self.shake; loc = (loc[0] + s * math.sin(g * 0.71), loc[1] + s * 0.6 * math.sin(g * 0.53 + 1), loc[2] + s * 0.8 * math.sin(g * 0.97 + 2))
        return loc, look

def key_cam(cam, f, loc, look):
    cam.location = loc
    cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)

def hand_world(a, anch, f, cam, key='hand_r', d=(0, 0)):
    lx, ly = anch[key]
    return actors.local_to_world(a, (lx + d[0], ly + d[1]), f, camera=cam)

def render_frame(path, mode, samples, threads):
    sc = bpy.context.scene; K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.render.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t; K.grade(path); return dt

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def emissive_bar(name, parent, w, h, centre, color=(1.0, 0.82, 0.35), strength=2.5, alpha=0.5):
    """a camera-only glowing translucent bar in card-local coordinates (card faces local +y; centre = (x, z))."""
    me = bpy.data.meshes.new(name); me.from_pydata([(-w/2, 0, -h/2), (-w/2, 0, h/2), (w/2, 0, h/2), (w/2, 0, -h/2)], [], [(0, 1, 2, 3)]); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.parent = parent; ob.location = (centre[0], 0.0045, centre[1])
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = color + (1.0,); em.inputs['Strength'].default_value = strength
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes.new('ShaderNodeOutputMaterial'); mx.inputs[0].default_value = alpha
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    me.materials.append(m); ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False; ob.hide_render = True
    return ob, mx

def image_quad(name, parent, w, h, centre, png, strength=1.3, off_y=0.006):
    """camera-only emissive image plane (straight alpha) in card-local coordinates; returns (obj, emission node)."""
    me = bpy.data.meshes.new(name); me.from_pydata([(-w/2, 0, -h/2), (-w/2, 0, h/2), (w/2, 0, h/2), (w/2, 0, -h/2)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, (u, v) in enumerate(((0, 0), (0, 1), (1, 1), (1, 0))): uv.data[i].uv = (u, v)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.parent = parent; ob.location = (centre[0], off_y, centre[1])
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(png); tx.image.alpha_mode = 'STRAIGHT'; tx.interpolation = 'Cubic'
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(tx.outputs['Color'], em.inputs['Color']); nt.links.new(tx.outputs['Alpha'], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    me.materials.append(m); ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False; ob.hide_render = True
    return ob, em

def bottle_png(path, W=640, H=224):
    from PIL import Image, ImageDraw
    if os.path.exists(path): return path
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, W - 5, H - 5], 22, fill=(255, 205, 105, 255), outline=(120, 52, 40, 255), width=10)
    d.rounded_rectangle([26, 24, W - 27, H - 25], 14, fill=(255, 226, 150, 255))
    cx = W // 2; top = 26; bot = H - 30
    # empty glass bottle: dark outline, pale glass inside, a bright highlight, no liquid
    body = [cx - 50, top + 78, cx + 50, bot]
    d.rounded_rectangle(body, 26, fill=(205, 238, 224, 255), outline=(60, 36, 34, 255), width=9)
    d.rectangle([cx - 17, top + 16, cx + 17, top + 86], fill=(205, 238, 224, 255), outline=(60, 36, 34, 255), width=9)
    d.rectangle([cx - 24, top + 4, cx + 24, top + 22], fill=(130, 70, 46, 255), outline=(60, 36, 34, 255), width=8)
    d.rounded_rectangle([cx - 36, top + 100, cx - 26, bot - 24], 5, fill=(255, 255, 255, 255))
    for k in range(3): d.line([(cx + 120 + 50 * k, H // 2 - 30), (cx + 150 + 50 * k, H // 2 + 30)], fill=(150, 70, 56, 255), width=8) if False else None
    im.save(path); return path

def tick_bars(name, parent, centre, size=0.012):
    """a green tick (two thin glowing bars) in card-local coordinates, returns [(obj, mix)...]."""
    out = []
    for k, (dx, dz, rot, ln) in enumerate(((-0.3, -0.15, -45, 0.55), (0.25, 0.1, 40, 1.0))):
        ob, mx = emissive_bar('%s_%d' % (name, k), parent, size * ln, size * 0.28, (centre[0] + dx * size, centre[1] + dz * size), color=(0.45, 1.0, 0.5), strength=3.0, alpha=0.95)
        ob.rotation_euler = (0, math.radians(rot), 0); ob.location.y = 0.0065; out.append((ob, mx))
    return out
