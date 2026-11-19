"""c14.py -- helper module of take s25 (film 14, shots 25-30). Own helpers: puppet -> metre card (put), per-frame cleanup,
persistent camera, the dust spray card, contact shadows. Based on set3d14/cast_test/cast_test.py (put / _contact)."""
import sys, os, math, json, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast14'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d14')]
import numpy as np
from PIL import Image, ImageDraw
import cast14, sprites
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import farm as F
import farm_geo as G
MPD = cast14.M_PER_D
SPR = os.path.join(HERE, 'work', 'sprites'); os.makedirs(SPR, exist_ok=True)

def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p

def ez(u, kind='sine'):
    u = min(1.0, max(0.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u) if kind == 'sine' else u * u * (3 - 2 * u) if kind == 'smooth' else u
def mixu(u):                       # camera ease with no dead ends: 35 % sine + 65 % linear
    u = min(1.0, max(0.0, u)); return 0.35 * ez(u) + 0.65 * u
def lerp(a, b, t): return a + (b - a) * t
def lerp3(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))

# ----------------------------------------------------------------------------- per-frame object bookkeeping
_FRAME = {'objs': [], 'imgs': [], 'mats': [], 'meshes': []}
def begin_frame():
    for o in _FRAME['objs']:
        try: bpy.data.objects.remove(o)
        except Exception: pass
    for me in _FRAME['meshes']:
        try: bpy.data.meshes.remove(me)
        except Exception: pass
    for m in _FRAME['mats']:
        G.MATS.pop(m.name, None)
        try: bpy.data.materials.remove(m)
        except Exception: pass
    for im in _FRAME['imgs']:
        try: bpy.data.images.remove(im)
        except Exception: pass
    for k in _FRAME: _FRAME[k] = []

def _card_mesh(tag, x0, z0, x1, z1):
    me = bpy.data.meshes.new(tag); me.from_pydata([(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    _FRAME['meshes'].append(me); return me

def _mat(tag, png, k=None, tint=None, fade=1.0):
    P = F.STATE['P']; m = G.mat_card(tag, png, P.get('card_k', 1.0) if k is None else k); _FRAME['mats'].append(m)
    if tint is not None:                        # multiply the card colour (director QA: night elephants no brighter than the lit soil)
        nt = m.node_tree; ti = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]; em = nt.nodes[m['card_em']]
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
        nt.links.new(ti.outputs['Color'], mx.inputs[6]); nt.links.new(mx.outputs[2], em.inputs['Color'])
    if fade < 0.999:                            # alpha x fade (turn cross-fade between the frontal and the side card)
        nt = m.node_tree; ti = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]; mixn = [n for n in nt.nodes if n.type == 'MIX_SHADER'][0]
        mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = max(0.0, fade)
        nt.links.new(ti.outputs['Alpha'], mu.inputs[0]); nt.links.new(mu.outputs[0], mixn.inputs[0])
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE': _FRAME['imgs'].append(n.image)
    return m

def _link(ob): bpy.context.scene.collection.objects.link(ob); _FRAME['objs'].append(ob); return ob

def _contact(tag, mk, yaw, L, Wd, strength=0.8):
    N = 96; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8
    p = os.path.join(SPR, 'contact_blob.png')
    if not os.path.exists(p): Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = _card_mesh('c_' + tag, -L / 2, 0, L / 2, 0)    # placeholder; rebuild flat
    bpy.data.meshes.remove(me); _FRAME['meshes'].remove(me)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update(); _FRAME['meshes'].append(me)
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'; _FRAME['imgs'].append(img)
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; _FRAME['mats'].append(m); nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.004, 0.003, 0.02, 1); em.inputs['Strength'].default_value = 1
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = strength
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = _link(bpy.data.objects.new('actor_c_' + tag, me)); ob.location = (mk.x, mk.y, mk.z + 0.08); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

_SCALE = dict(matriarch=1.0, elephant_b=.86, elephant_c=.93, elephant_d=.77, calf=.36)
def put(tag, cast, pose, mark, cam_loc, ppd=128, mirror=False, canvas=None, shadow=True, contact=None, dz=0.0, yaw_fixed=None, anchor_ground=None, yaw_off=0.0, roll=0.0, yaw_extra=0.0, fade=1.0, shadow_k=1.0):
    """real puppet sprite -> metre card with its FEET at `mark` (x, y, z), turned to face the camera (yaw only) unless yaw_fixed.
    anchor_ground=(anchor, (x, y)): shift the card in its plane so that the anchor sits over the ground point.
    Returns dict(world=fn(local D point)->world Vector, anchors, res, mark, yaw)."""
    pose = dict(pose); pose['mirror'] = bool(mirror)
    cv = canvas or cast14.CANVAS14[cast]
    key = hashlib.sha1(json.dumps([cast, pose, ppd, cv], sort_keys=True, default=str).encode()).hexdigest()[:16]
    out = os.path.join(SPR, key + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
    assert not r['clipped'], 'sprite clipped by canvas: %s %s' % (tag, r.get('bbox'))
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']
    X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
    me = _card_mesh(tag, X0, Z0, X1, Z1); me.materials.append(_mat('%s_mat_%s' % (tag, key), out, tint=(0.62, 0.67, 0.86) if (cast in _SCALE and F.STATE['light'] == 'NIGHT') else None, fade=fade))
    mk = Vector(mark) + Vector((0, 0, dz))
    def yaw_of(m):
        if yaw_fixed is not None: return yaw_fixed
        d = Vector(cam_loc) - m; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    if anchor_ground is not None:
        an, gp = anchor_ground; a = r['anchors'][an]
        for _ in range(4):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0)); mk = Vector((gp[0], gp[1], mk.z)) - axx * ((a[0] - fx) * MPD)
    yaw = yaw_of(mk) + math.radians(yaw_extra)
    ob = _link(bpy.data.objects.new('actor_' + tag, me)); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
    if shadow:
        s = _SCALE.get(cast)
        if s is not None: L, Wd = 6.4 * s, 2.4 * s
        else: L, Wd = 1.5, 0.7
        if contact is not None: L, Wd = contact
        _contact(tag, mk, yaw - math.radians(yaw_extra), L, Wd, min(1.0, 0.85 * shadow_k) if fade > 0.5 else 0.0)
    return dict(world=w, anchors=r['anchors'], res=r, mark=mk, yaw=yaw)

def card(tag, png, x0, z0, x1, z1, loc, yaw=0.0, k=None, shadow=False):
    """a free transparent PNG card, rectangle x0..x1 (m, in the card plane) by z0..z1, at world loc."""
    me = _card_mesh(tag, x0, z0, x1, z1); me.materials.append(_mat('%s_mat' % tag, png, k))
    ob = _link(bpy.data.objects.new('actor_' + tag, me)); ob.location = loc; ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = bool(shadow); return ob

# ----------------------------------------------------------------------------- camera
_CAM = {}
def cam_make():
    sc = bpy.context.scene; cd = bpy.data.cameras.new('cam14'); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False; cd.clip_end = 3000; cd.clip_start = 0.05
    ob = bpy.data.objects.new('cam14', cd); sc.collection.objects.link(ob); sc.camera = ob; _CAM['ob'] = ob; return ob
def cam_set(loc, look, lens, roll=0.0):
    ob = _CAM['ob']; ob.location = loc; ob.data.lens = lens
    q = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y'); ob.rotation_euler = q.to_euler()
    if roll: ob.rotation_euler.rotate_axis('Z', math.radians(roll))
    bpy.context.view_layer.update()
def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return round(v.x * F.W), round((1 - v.y) * F.H)

# ----------------------------------------------------------------------------- dust: a spray crown of droplets + thin wisps (no round blobs)
class Dust(object):
    """Deterministic particle spray painted into ONE strip card (world x range, z 0..zh) per call. Sources emit droplets (ballistic, tiny
    streaked ellipses) and thin curved tapered wisps; a burst makes a crown (fan of droplets over the foot)."""
    PPM = 90
    def __init__(self, seed=1, col=(196, 168, 146), life=22):
        self.rs = np.random.RandomState(seed); self.col = col; self.life = life; self.parts = []   # emitted events: (g0, kind, x, y?, vx, vz, ...)
    def burst(self, g, x, n=46, dirx=-1.0, power=1.0, zspread=1.0):
        r = self.rs
        for i in range(n):
            a = r.uniform(0.15, 1.45) * math.pi / 2 * 1.0   # elevation 15..130 deg-ish fan
            ang = r.uniform(math.radians(18), math.radians(160)); sp = r.uniform(2.0, 6.0) * power
            vx = math.cos(ang) * sp * (-0.7 if dirx < 0 else 0.7) + dirx * r.uniform(0.2, 1.8); vz = math.sin(ang) * sp * zspread
            self.parts.append(dict(g=g, k='d', x=x + r.uniform(-0.5, 0.5), vx=vx, vz=vz, s=r.uniform(0.05, 0.12), life=r.uniform(18, 36)))
        for i in range(max(6, n // 6)):
            self.parts.append(dict(g=g, k='w', x=x + r.uniform(-0.7, 0.7), vx=dirx * r.uniform(0.6, 2.4) + r.uniform(-0.5, 0.5), vz=r.uniform(0.5, 2.1), s=r.uniform(1.8, 3.6), w=r.uniform(0.2, 0.42), life=r.uniform(34, 60), bend=r.uniform(-1, 1)))
    def trail(self, g, x, dirx=-1.0, power=1.0, n=4):
        r = self.rs
        for i in range(n):
            ang = r.uniform(math.radians(25), math.radians(110)); sp = r.uniform(1.0, 3.4) * power
            self.parts.append(dict(g=g, k='d', x=x + r.uniform(-0.6, 0.6), vx=-dirx * math.cos(ang) * sp * -1 * 0.5 + dirx * r.uniform(0.3, 1.4), vz=math.sin(ang) * sp, s=r.uniform(0.045, 0.10), life=r.uniform(14, 30)))
        if r.rand() < 0.45: self.parts.append(dict(g=g, k='w', x=x + r.uniform(-0.5, 0.5), vx=dirx * r.uniform(0.4, 1.6), vz=r.uniform(0.3, 1.3), s=r.uniform(1.4, 2.8), w=r.uniform(0.16, 0.34), life=r.uniform(30, 50), bend=r.uniform(-1, 1)))
    def paint(self, g, xa, xb, zh=3.4, tag='dust', light_k=1.0):
        ppm = self.PPM; SS = 2; Wp, Hp = int((xb - xa) * ppm), int(zh * ppm); im = Image.new('RGBA', (Wp * SS, Hp * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA'); n = 0
        def P(x, z): return ((x - xa) * ppm * SS, (zh - z) * ppm * SS)
        r0, g0, b0 = self.col
        for p in self.parts:
            age = (g - p['g']) / 30.0
            if age < 0 or age * 30 > p['life']: continue
            u = age * 30 / p['life']
            if p['k'] == 'd':
                x = p['x'] + p['vx'] * age * (1 - 0.35 * u); z = 0.04 + p['vz'] * age - 0.5 * 9.0 * age * age
                if z < 0.02: z = 0.02
                a = int(235 * (1 - u) ** 0.8); s = p['s'] * (1 - 0.35 * u)
                vx, vz = p['vx'] * (1 - 0.35 * u), p['vz'] - 9.0 * age
                L = min(0.12, 0.01 + 0.02 * math.hypot(vx, vz)); th = math.atan2(-vz, vx)
                cx, cy = P(x, z); lx, ly = math.cos(th) * L * ppm * SS, math.sin(th) * L * ppm * SS; rr = s * ppm * SS
                # droplet: a round head with a short tapered tail along the motion (teardrop), a darker underside crescent
                ux, uy = math.cos(th), math.sin(th); nx, ny = -uy, ux; tl = L * ppm * SS * 1.3
                d.polygon([(cx - ux * tl, cy - uy * tl), (cx + nx * rr * 0.8, cy + ny * rr * 0.8), (cx - nx * rr * 0.8, cy - ny * rr * 0.8)], fill=(r0, g0, b0, int(a * 0.55)))
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(int(r0 * 0.7), int(g0 * 0.66), int(b0 * 0.7), a))
                d.ellipse([cx - rr * 0.85, cy - rr * 0.95, cx + rr * 0.75, cy + rr * 0.55], fill=(min(255, r0 + 34), min(255, g0 + 28), min(255, b0 + 24), a)); n += 1
            else:
                # wisp: a curved tapered ribbon drifting up and back, fading
                x0 = p['x'] + p['vx'] * age * 0.9; z0 = 0.15 + p['vz'] * age * 0.7 - 0.25 * age * age; Ln = p['s'] * (0.5 + 0.9 * min(1, u * 2)); w = p['w'] * (0.5 + 0.7 * u)
                a = int(190 * (1 - u) ** 1.1 * min(1, u * 8 + 0.35)); pts = []; N = 14
                dirx = 1 if p['vx'] > 0 else -1
                for i in range(N + 1):
                    t = i / N; px = x0 - dirx * Ln * t * 0.9; pz = z0 + (0.25 + 0.5 * p['bend']) * Ln * t + 0.4 * p['bend'] * Ln * t * t
                    pts.append((px, pz))
                up, dn = [], []
                for i, (px, pz) in enumerate(pts):
                    t = i / N; wd = w * math.sin(math.pi * (0.12 + 0.88 * t)) * (1 - 0.3 * t)
                    up.append(P(px, pz + wd)); dn.append(P(px, pz - wd))
                d.polygon(up + dn[::-1], fill=(r0, g0, b0, a)); d.line([P(px, pz + 0.001) for px, pz in pts], fill=(min(255, r0 + 40), min(255, g0 + 32), min(255, b0 + 28), int(a * 0.8)), width=max(2, int(0.02 * ppm * SS))); n += 1
        im = im.resize((Wp, Hp), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32); a[..., :3] *= light_k; im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        p = os.path.join(SPR, 'dust_%s_%d_%d.png' % (tag, os.getpid(), g)); im.save(p); return p, n

import bmesh
def cut_region(boxes, pref='props'):
    """delete set-dressing vertices of the merged 'props' meshes inside the (x0,x1,y0,y1,zmax) boxes (runtime change, set module untouched)"""
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(pref): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and (mw @ v.co).z < b[4] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data); print('cut', ob.name, len(dl))
        bm.free()
def cut_stool(): cut_region([(-23.1, -21.7, 1.8, 3.0, 0.62)])

def cut_tree33(): cut_region([(-43.0, -24.0, 0.0, 13.0, 40.0)], "trees")
