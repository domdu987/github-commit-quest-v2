"""c14.py -- helper for film 14 takes (team 1). Placement code from set3d14/cast_test/cast_test.py (put(), contact shadow), per-frame
camera / hooks / cards. One location (preset) per process. Hooks are immediate: every frame calls every hook."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast14'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d14')]
import numpy as np
from PIL import Image
import cast14, sprites
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import farm as F
import farm_geo as G
MPD = cast14.M_PER_D
FPS = 30

def lerp(a, b, t): return a + (b - a) * t
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ez(x, k='sine'):
    x = clamp(x)
    return 0.5 - 0.5 * math.cos(math.pi * x) if k == 'sine' else x * x * (3 - 2 * x)
def u_of(g, a, b): return ez((g - a) / float(b - a)) if b > a else (1.0 if g >= a else 0.0)
def lerp3(a, b, t): return tuple(lerp(a[i], b[i], t) for i in range(3))
def g_of(t): return int(round((t + 0.10) * FPS))
def g_bound(t): return int(round(t * FPS))

def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p

class Take:
    def __init__(self, work, preset, light=None, quality='preview', samples=None, threads=2):
        self.work = work; self.spr = os.path.join(work, 'sprites'); os.makedirs(self.spr, exist_ok=True)
        self.q = quality; self.preset = preset
        self.A = F.build(preset, light, dress=True)
        self.sc = bpy.context.scene; F.setup_render(self.sc, quality)
        self.sc.render.threads = threads
        self.sc.cycles.samples = samples or (24 if quality == 'final' else 6)
        c = F.CAMS[preset]; self.cam = F.make_camera(c); self.cd = self.cam.data
        self.n = 0; self.heads = []

    # ---- camera
    def set_cam(self, loc, look, lens):
        self.cam.location = loc; self.cd.lens = lens
        self.cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        bpy.context.view_layer.update()

    # ---- cards
    def clear(self):
        for o in list(bpy.data.objects):
            if o.name.startswith('actor_'):
                me = o.data; bpy.data.objects.remove(o)
                if me and me.users == 0: bpy.data.meshes.remove(me)
        for m in list(bpy.data.materials):
            if m.name.startswith(('f14_', 'cm_')) and m.users == 0: bpy.data.materials.remove(m)
        for i in list(bpy.data.images):
            if i.users == 0 and i.name.startswith(('f14', 'contact_')): bpy.data.images.remove(i)
        for k in [k for k in G.MATS if k.startswith('f14_')]: G.MATS.pop(k)

    def put(self, tag, cast, pose, mark, ppd=128, mirror=False, canvas=None, shadow=True, yaw_off=0.0, yaw_fixed=None, contact=(0.22, 0.12)):
        """real puppet sprite -> card standing at `mark` (feet), turned to the camera (yaw only). Returns anchors in world + screen."""
        pose = dict(pose); pose['mirror'] = bool(mirror)
        cv = canvas or cast14.CANVAS14[cast]
        self.n += 1; ntag = 'f14_%s_%d' % (tag, self.n)
        out = os.path.join(self.spr, ntag + '.png')
        r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
        assert not r['clipped'], 'sprite clipped by canvas: %s %s' % (tag, cast)
        x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']
        X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
        me = bpy.data.meshes.new(ntag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
        uvl = me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        P = F.STATE['P']; m = G.mat_card(ntag + '_mat', out, P.get('card_k', 1.0)); me.materials.append(m)
        mk = Vector(mark); cl = self.cam.location
        d = cl - mk; yaw = (math.atan2(d.x, -d.y) + math.radians(yaw_off)) if yaw_fixed is None else yaw_fixed
        ob = bpy.data.objects.new('actor_' + ntag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
        ax = Vector((math.cos(yaw), math.sin(yaw), 0))
        def w(a): return mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
        if shadow and contact:
            self._contact(ntag, mk, yaw, contact[0] * 8 * MPD, contact[1] * 8 * MPD, cast)
        return dict(world=w, anchors=r['anchors'], res=r)

    def _contact(self, tag, mk, yaw, L, Wd, cast):
        N = 64; yy, xx = np.mgrid[0:N, 0:N]; rr = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
        im = np.zeros((N, N, 4), np.float32); im[..., 3] = np.clip(1 - rr, 0, 1) ** 0.8
        p = os.path.join(self.spr, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
        me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
        uvl = me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'; img.name = 'contact_' + tag
        m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
        out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission')
        em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1); em.inputs['Strength'].default_value = 1
        tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.7
        Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
        me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (mk.x, mk.y, mk.z + 0.02); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

    def screen(self, p):
        v = world_to_camera_view(self.sc, self.cam, Vector(p)); return [round(v.x * F.W), round((1 - v.y) * F.H)]

    def head_screen(self, a):
        """[(head_top_y, chin_y)] of one put() result at the render resolution scaled to 720x1280."""
        an = a['anchors']; w = a['world']
        top = self.screen(w(an['head_top'])) if 'head_top' in an else self.screen(w(an['head']))
        ch = self.screen(w(an['head'])); return top, ch

    def render(self, path):
        bpy.context.view_layer.update()
        wall, cpu = F.render(path)
        return wall, cpu
