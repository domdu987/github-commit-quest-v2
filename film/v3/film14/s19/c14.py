"""c14.py -- helper for film 14 take s20 (reveal): scene setup, real cast14 cards, swarm cards, camera, lamps.
Placement code adapted from v3/set3d14/cast_test/cast_test.py (put(), _contact()). One location (the farm) per process."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast14'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d14')]
import numpy as np
from PIL import Image
import cast14, sprites
import bpy, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import farm as F
import farm_geo as G
MPD = cast14.M_PER_D
SPR = os.path.join(HERE, 'sprites'); os.makedirs(SPR, exist_ok=True)
PS0 = 14.0 + 10.25            # push point arc length (x 10.25 on the front row)

def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def lerp(a, b, u): return a + (b - a) * u
def sm(u): u = clamp(u); return u * u * (3 - 2 * u)
def mv(u): return 0.35 * (0.5 - 0.5 * math.cos(math.pi * clamp(u))) + 0.65 * clamp(u)     # never dead at the ends
def pw(g, kn):
    """piecewise-linear value at g from knots [(g, v), ...]"""
    if g <= kn[0][0]: return kn[0][1] + (g - kn[0][0]) * (kn[1][1] - kn[0][1]) / (kn[1][0] - kn[0][0])
    for (g0, v0), (g1, v1) in zip(kn, kn[1:]):
        if g <= g1: return lerp(v0, v1, (g - g0) / (g1 - g0))
    (g0, v0), (g1, v1) = kn[-2], kn[-1]; return v1 + (g - g1) * (v1 - v0) / (g1 - g0)

# ----------------------------------------------------------------------------- scene
def register_preset(name, loc, look, lens, wire_r=0.03):
    F.CAMS[name] = dict(loc=tuple(loc), look=tuple(look), lens=lens)
    F.PRESETS[name] = dict(light='NIGHT', state='fs3', wire_r=wire_r, staging=[])

def patch_bees(near=0.10, per_m=0.010, far=0.30):
    """bigger bees so they read at phone size: patch the size clip of farm._bees_apply at runtime (the set module on disk is untouched)"""
    import inspect
    src = inspect.getsource(F._bees_apply); old = "np.clip(0.07 + 0.006 * dist, 0.07, 0.17)"
    assert old in src; src = src.replace(old, "np.clip(%g + %g * dist, %g, %g)" % (near, per_m, near, far)); exec(src, F.__dict__)

def build(name, quality, threads=2, samples=None, dense_bees=240):
    F.BEE_PER_HIVE = dense_bees; patch_bees()
    A = F.build(name, 'NIGHT'); sc = bpy.context.scene; F.setup_render(sc, quality)
    sc.render.threads = threads
    if samples: sc.cycles.samples = samples
    sc.cycles.transparent_max_bounces = 24
    wm = F.STATE['M']['beewing']; em = [n for n in wm.node_tree.nodes if n.type == 'EMISSION'][0]; mx = [n for n in wm.node_tree.nodes if n.type == 'MIX_SHADER'][0]
    em.inputs['Color'].default_value = (1.0, 0.82, 0.42, 1); em.inputs['Strength'].default_value = 0.9; mx.inputs[0].default_value = 0.30      # warm, thin wing blur: gold dots at distance, not blue snow
    bm = F.STATE['M']['beegold']
    wmat = F.STATE['M']['wire']                      # matte grey-silver wire (director continuity note), reads as wire not a pipe
    for n in wmat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Base Color'].default_value = (0.52, 0.53, 0.56, 1); n.inputs['Roughness'].default_value = 0.55
            if 'Emission Strength' in n.inputs: n.inputs['Emission Strength'].default_value = 0.0
        if n.type == 'EMISSION': n.inputs['Strength'].default_value = 0.0
    F._clear_actors(); F.apply_state('fs3'); F.STATE['wire_r'] = F.PRESETS[name]['wire_r']; F._update_fence()
    return A

def cut_boxes(boxes, names=('props',)):
    """review-still trick of cast_test: delete set-dressing vertices inside (x0,x1,y0,y1,zmax) boxes"""
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(tuple(names)): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and (mw @ v.co).z < b[4] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data)
        bm.free()

def cut_path(pts, radius, names=('props', 'grass', 'flowers', 'edge', 'pebbles'), zmax=2.2, keep=None):
    """delete dressing within `radius` m (xy) of the camera path points (keeps the camera clear of blades / props)."""
    P = np.array([(p[0], p[1]) for p in pts])
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(tuple(names)): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world; dl = []
        for v in bm.verts:
            w = mw @ v.co
            if w.z > zmax: continue
            if keep and keep(w): continue
            if np.min(np.hypot(P[:, 0] - w.x, P[:, 1] - w.y)) < radius: dl.append(v)
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data)
        bm.free()

def dim_lamps(center, radius, k):
    n = 0
    for ob in bpy.data.objects:
        if ob.type == 'LIGHT' and ob.data.type == 'POINT' and (Vector(ob.location) - Vector(center)).length < radius:
            ob.data.energy *= k; n += 1
    return n

class Cam:
    def __init__(self):
        c = F.CAMS[F.STATE['preset']]; self.ob = F.make_camera(c)
    def set(self, loc, look, lens):
        ob = self.ob; ob.location = loc; ob.data.lens = lens
        ob.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        self.loc = Vector(loc)

# ----------------------------------------------------------------------------- cards
def _contact(tag, L, Wd):
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1); em.inputs['Strength'].default_value = 1
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 1.0
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    return ob

class Card:
    """one 2D puppet / sprite card in the 3D set. The canvas is fixed per card; the sprite (image) changes per frame."""
    def __init__(self, tag, cast, canvas, ppd, contact=None, card_k=None):
        self.tag, self.cast, self.canvas, self.ppd = tag, cast, canvas, ppd
        x0, y0, x1, y1 = canvas; self.me = None; self.ob = None; self.node = None; self.contact = None; self.card_k = card_k
        self.contact_size = contact; self.grade = False
    def _make(self, r):
        x0, y0, x1, y1 = r['canvas']; X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
        me = bpy.data.meshes.new(self.tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
        uvl = me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        P = F.STATE['P']; m = G.mat_card(self.tag + '_mat', r['out'], self.card_k or P.get('card_k', 1.0)); me.materials.append(m)
        self.node = [n for n in m.node_tree.nodes if n.type == 'TEX_IMAGE'][0]
        self.ob = bpy.data.objects.new('actor_' + self.tag, me); bpy.context.scene.collection.objects.link(self.ob)
        if self.contact_size: self.contact = _contact(self.tag, *self.contact_size)
    def sprite(self, pose, key):
        pose = dict(pose); out = os.path.join(SPR, '%s_%s.png' % (self.tag, key))
        r = sprites.render_sprites([dict(cast=self.cast, pose=pose, px_per_D=self.ppd, out=out, canvas=self.canvas)])[0]
        if r['clipped']: print('WARNING clipped', self.tag, key, flush=True)
        r['out'] = out
        if self.cast == 'swarm': out = self._warm_wings(out); r['out'] = out
        if self.grade: out = self._night(out); r['out'] = out
        if self.ob is None: self._make(r)
        else:
            old = self.node.image; img = bpy.data.images.load(out); img.alpha_mode = 'STRAIGHT'; self.node.image = img
            if old is not None and old.users == 0: bpy.data.images.remove(old)
        self.r = r; return r
    @staticmethod
    def _night(path):
        """elephant card for NIGHT (director note): x0.70, tint (0.78,0.82,1.0), cool moon rim on the top edge, warm hut tint on the right side. Writes <name>_n.png (cache hard link untouched)."""
        o2 = path[:-4] + '_n.png'
        im = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32) / 255.0; a = im[..., 3]; rgb = im[..., :3] * np.array([0.70 * 0.78, 0.70 * 0.82, 0.70], np.float32)
        ys, xs = np.nonzero(a > 0.1)
        if len(xs):
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); fx = np.clip((np.arange(im.shape[1]) - x0) / max(1, x1 - x0), 0, 1)[None, :]
            warm = np.clip((fx - 0.5) / 0.5, 0, 1) ** 1.3 * 0.42; rgb = rgb * (1 + warm[..., None] * np.array([0.55, 0.12, -0.35], np.float32))
            fy = np.clip(1 - (np.arange(im.shape[0]) - y0) / max(1, 0.18 * (y1 - y0)), 0, 1)[:, None] ** 2 * 0.22; rgb = rgb + fy[..., None] * np.array([0.04, 0.07, 0.14], np.float32) * (a[..., None] > 0.5)
        a = np.clip(a * 1.8, 0, 1)                      # opaque card (ears were semi-transparent: roofs showed through)
        out = np.concatenate([np.clip(rgb, 0, 1), a[..., None]], -1); Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(o2); return o2
    @staticmethod
    def _warm_wings(path):
        """swarm sprites: pale-blue wing ghosts glow like snow at night; make them thin and warm so the gold-black bodies read. Writes <name>_w.png (the cache hard link is untouched)."""
        o2 = path[:-4] + '_w.png'
        im = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32) / 255.0; r_, g_, b_, a_ = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
        wing = ((b_ - r_) > 0.06) & ((r_ + g_ + b_) / 3 > 0.55)
        a2 = np.where(wing, a_ * 0.42, a_); k = wing[..., None]; warm = np.stack([r_ * 0.95 + 0.04, g_ * 0.8 + 0.02, b_ * 0.55], -1)
        rgb = np.where(k, warm, im[..., :3]); out = np.concatenate([rgb, a2[..., None]], -1)
        Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(o2); return o2
    def put(self, origin, yaw):
        """card origin = feet point at world `origin`, rotated yaw about z"""
        self.ob.location = origin; self.ob.rotation_euler = (0, 0, yaw); self.ob.hide_render = False; self.mk = Vector(origin); self.yaw = yaw
        if self.contact is not None: self.contact.location = (origin[0], origin[1], origin[2] + 0.03); self.contact.rotation_euler = (0, 0, yaw)
    def put_anchor(self, an, gxy, yaw, z=0.0):
        """place the card so that anchor `an` is above the ground point gxy (xy), yaw about z"""
        a = self.r['anchors'][an]; fx, fy = self.r['feet']; ax = Vector((math.cos(yaw), math.sin(yaw), 0))
        mk = Vector((gxy[0], gxy[1], 0)) - ax * ((a[0] - fx) * MPD) + Vector((0, 0, z)); self.put(mk, yaw)
    def world(self, an):
        a = self.r['anchors'][an] if isinstance(an, str) else an; fx, fy = self.r['feet']; ax = Vector((math.cos(self.yaw), math.sin(self.yaw), 0))
        return self.mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
    def hide(self):
        if self.ob is not None: self.ob.hide_render = True
        if self.contact is not None: self.contact.hide_render = True

def yaw_to(cam_loc, p): d = Vector(cam_loc) - Vector(p); return math.atan2(d.x, -d.y)

def matriarch_card(ppd, tag='mat'):
    s = 1.0; return Card(tag, 'matriarch', cast14.CANVAS14['matriarch'], ppd, contact=(1.0 * MPD * 11, 0.30 * MPD * 11))

def swarm_card(tag, canvas, ppd=96):
    return Card(tag, 'swarm', canvas, ppd, contact=None, card_k=1.0)

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return round(v.x * F.W), round((1 - v.y) * F.H)

def trunk_mix(a, b, u, **extra):
    """numeric trunk keys between two TRUNKS presets (lerp_pose drops strings)"""
    A, B = cast14.TRUNKS[a], cast14.TRUNKS[b]
    return dict(trunk=a if u < 0.5 else b, trunk_a0=lerp(A[0], B[0], u), trunk_a1=lerp(A[1], B[1], u), trunk_curl=lerp(A[2], B[2], u), **extra)

def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p


# ----------------------------------------------------------------------------- swarm cards + ground dressing
class Swarm:
    """a billboard swarm card (cast14 'swarm' sprite: wing-blur bees); canvas is a +-R D square centred on the card origin"""
    def __init__(self, tag, R=4.0, ppd=160):
        self.card = Card(tag, 'swarm', (-R, -R, R, R), ppd, contact=None, card_k=1.0); self.R = R
    def show(self, key, pose, centre, cam_loc, yaw_off=0.0):
        self.card.sprite(pose, key); self.card.put(Vector(centre) - Vector((0, 0, 0)), yaw_to(cam_loc, centre) + yaw_off)
        self.card.world = None
    def hide(self): self.card.hide()

def dress(xr, yr, n, seed, avoid=(), mats=('grass', 'grassgreen')):
    """extra low grass clumps in a rectangle (foreground depth for the low cameras); no flowers"""
    rr = np.random.RandomState(seed); mb = G.MB('xdress'); M = F.STATE['M']; k = 0
    for i in range(n * 4):
        if k >= n: break
        x = rr.uniform(*xr); y = rr.uniform(*yr)
        if any((x - ax) ** 2 + (y - ay) ** 2 < ar * ar for ax, ay, ar in avoid): continue
        G.grass_clump(mb, M, (x, y, 0.0), rr, rr.uniform(0.3, 0.6), mats[0] if rr.rand() < 0.65 else mats[1], 5); k += 1
    mb.finish()

def hide_maize_rows(ymax=7.0):
    """the wave pushes the wire and its hives up to ~1.2 m into the field: clear the first maize rows (hero field only) so the hives stay visible"""
    n = 0
    for o in bpy.data.objects:
        if o.name.startswith('mz') and o.location.y < ymax: o.hide_render = True; n += 1
    return n


def cut_roofs(x0, x1, y0, y1, zmin=1.9, prefix='roof'):
    """delete roof-mesh vertices inside the box (the near roof must not cut through the elephant card)"""
    n = 0
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(prefix): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if x0 < (mw @ v.co).x < x1 and y0 < (mw @ v.co).y < y1 and (mw @ v.co).z > zmin]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data); n += len(dl)
        bm.free()
    return n

def hide_grass_box(x0, x1, y0, y1, zmax=1.0):
    return cut_boxes([(x0, x1, y0, y1, zmax)], names=('grass', 'flowers', 'edge', 'pebbles', 'xdress'))


def darken_mat(name, k):
    m = F.STATE['M'][name]
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            col = n.inputs['Base Color'].default_value; n.inputs['Base Color'].default_value = (col[0] * k, col[1] * k, col[2] * k, 1)
            if 'Emission Strength' in n.inputs: n.inputs['Emission Strength'].default_value *= k
        if n.type == 'EMISSION': n.inputs['Strength'].default_value *= k
        if n.type == 'RGB': col = n.outputs[0].default_value; n.outputs[0].default_value = (col[0] * k, col[1] * k, col[2] * k, 1)
