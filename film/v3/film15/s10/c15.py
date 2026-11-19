"""c15.py: per-frame cast15 cards in the set3d15 scene (adapted from set3d15/cast_test put()). One Card per actor track:
a quad + emission material whose image / geometry / transform are refreshed every frame before the render."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image
import cast15, sprites                 # cast15 BEFORE sprites
import bpy
from mathutils import Vector
import set15 as F
SPR = os.path.join(HERE, 'work', 'sprites'); os.makedirs(SPR, exist_ok=True)
CACHE = os.path.join(SPR, '_cache')

def _mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m, ti

def _shadow_obj(name):
    N = 64; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'shadow_disc_%d.png' % os.getpid()); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new(name); me.from_pydata([(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('m_' + name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.8
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_sh_' + name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    return ob

class Card:
    def __init__(self, tag):
        self.tag = tag; self.me = bpy.data.meshes.new('card_' + tag); self.me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], [], [(0, 1, 2, 3)]); self.me.update()
        uvl = self.me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        self.mat, self.ti = _mat('cm_' + tag); self.me.materials.append(self.mat)
        self.ob = bpy.data.objects.new('actor_' + tag, self.me); bpy.context.scene.collection.objects.link(self.ob); self.ob.visible_shadow = False
        self.sh = _shadow_obj(tag); self.img = None; self.n = 0

    def hide(self):
        self.ob.hide_render = True; self.sh.hide_render = True; self.ob.hide_viewport = True; self.sh.hide_viewport = True

    def show(self, cast, pose, cam_loc, mark=None, anchor=None, ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, .45), shadow_at=None,
             shadow_a=0.8, dz=0.0, yaw_fixed=None):
        """mark = world feet point (D); anchor = (name, world) puts that sprite anchor on a world point. returns dict(world, anchors, mk, yaw)"""
        pose = dict(pose); pose['mirror'] = bool(mirror); cv = canvas or cast15.CANVAS15[cast]
        self.n += 1; out = os.path.join(SPR, '%s_%d.png' % (self.tag, os.getpid()))
        r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)], cache_dir=CACHE)[0]
        assert not r['clipped'], 'sprite clipped: ' + self.tag
        # the output is a hardlink/copy of a cached file: load by cache hash path to avoid stale reloads
        path = os.path.join(CACHE, r['hash'][:24] + '.png')
        img = bpy.data.images.load(path, check_existing=True); img.alpha_mode = 'STRAIGHT'; self.ti.image = img
        x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
        X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
        for v, p in zip(self.me.vertices, ((X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1))): v.co = p
        self.me.update()
        cam = Vector(cam_loc)
        def yaw_of(p):
            if yaw_fixed is not None: return yaw_fixed
            d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
        mk = Vector(mark if mark is not None else (0, 0, 0)) + Vector((0, 0, dz))
        if anchor is not None:
            an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
            for _ in range(6):
                yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
                mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
        yaw = yaw_of(mk); self.ob.location = mk; self.ob.rotation_euler = (0, 0, yaw); self.ob.hide_render = False; self.ob.hide_viewport = False
        ax = Vector((math.cos(yaw), math.sin(yaw), 0))
        def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
        gz = (mark[2] if (mark is not None and anchor is None) else mk.z)
        if shadow_at is not None: c, L, Wd = Vector(shadow_at[:3]), shadow_at[3], shadow_at[4]
        elif shadow: c, L, Wd = Vector((mk.x, mk.y, gz + dz)), shadow[0] * k, shadow[1] * k
        else: c = None
        if c is not None:
            self.sh.hide_render = False; self.sh.hide_viewport = False; self.sh.location = (c.x, c.y, c.z + 0.03); self.sh.rotation_euler = (0, 0, yaw); self.sh.scale = (L, Wd, 1)
            self.sh.data.materials[0].node_tree.nodes['Math'].inputs[1].default_value = shadow_a
        else: self.sh.hide_render = True
        return dict(world=w, anchors=r['anchors'], mk=mk, yaw=yaw)


class ImgCard:
    """an upright card with an arbitrary RGBA png (emission only), width x height in D, centred on a world point, yawed about Z"""
    def __init__(self, tag, png):
        self.me = bpy.data.meshes.new('img_' + tag); self.me.from_pydata([(-.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-.5, 0, .5)], [], [(0, 1, 2, 3)]); self.me.update()
        uvl = self.me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        self.mat, ti = _mat('imc_' + tag); img = bpy.data.images.load(png, check_existing=True); img.alpha_mode = 'STRAIGHT'; ti.image = img; self.me.materials.append(self.mat)
        self.ob = bpy.data.objects.new('actor_img_' + tag, self.me); bpy.context.scene.collection.objects.link(self.ob); self.ob.visible_shadow = False
    def hide(self): self.ob.hide_render = True; self.ob.hide_viewport = True
    def show(self, centre, yaw, w, h):
        self.ob.location = centre; self.ob.rotation_euler = (0, 0, yaw); self.ob.scale = (w, 1, h); self.ob.hide_render = False; self.ob.hide_viewport = False

def make_paper_png(path, ppd=400):
    """the newspaper of shot 14: 1.56 x 1.14 D page, grey bars for the text, a BIG photo of the arched Dick (flop, head and legs hanging below a tan bar)"""
    from PIL import ImageDraw, ImageFilter
    pose = cast15.pose_for('flop', 'dick'); tmp = os.path.join(SPR, 'paper_flop_%d.png' % os.getpid())
    r = sprites.render_sprites([dict(cast='dick', pose=pose, px_per_D=256, out=tmp, canvas=cast15.CANVAS15_WIDE)], cache_dir=CACHE)[0]
    sp = Image.open(os.path.join(CACHE, r['hash'][:24] + '.png')).convert('RGBA'); k = 256.0
    ox, oy = r['origin_px']; fx, fy = r['feet']; by = oy + (r['anchors']['bar'][1] - fy) * k
    W_, H_ = int(1.56 * ppd), int(1.14 * ppd); im = Image.new('RGBA', (W_, H_), (239, 233, 218, 255)); d = ImageDraw.Draw(im)
    ink = (40, 36, 44, 255); d.rectangle([2, 2, W_ - 3, H_ - 3], outline=ink, width=6)
    d.line([(W_ // 2 + 40, 20), (W_ // 2 + 40, H_ - 20)], fill=(184, 178, 162, 255), width=3)
    # headline bars across the top
    d.rectangle([40, 34, 40 + int(W_ * 0.62), 34 + 26], fill=(74, 72, 80, 255)); d.rectangle([40, 74, 40 + int(W_ * 0.40), 74 + 16], fill=(74, 72, 80, 255))
    # the photo: left page, big
    px0, py0, px1, py1 = 40, 110, int(W_ * 0.60), H_ - 40
    ph = Image.new('RGBA', (px1 - px0, py1 - py0), (214, 208, 190, 255)); pd = ImageDraw.Draw(ph); pw, phh = ph.size
    for yy in range(phh):                                              # soft sky-to-pit tone
        t = yy / float(phh); c = (int(226 - 40 * t), int(220 - 40 * t), int(200 - 36 * t), 255); pd.line([(0, yy), (pw, yy)], fill=c)
    pd.rectangle([0, int(phh * 0.80), pw, phh], fill=(176, 160, 130, 255))   # pit
    # the figure, scaled so the arch spans ~66 % of the photo width
    bb = sp.getbbox(); crop = sp.crop(bb); s = (pw * 0.84) / crop.size[0]; crop = crop.resize((max(1, int(crop.size[0] * s)), max(1, int(crop.size[1] * s))), Image.LANCZOS)
    barY = int(phh * 0.46); figY = barY - int((by - bb[1]) * s); figX = int(pw * 0.5 - crop.size[0] / 2)
    pd.line([(int(pw * 0.04), barY), (int(pw * 0.96), barY)], fill=(208, 170, 96, 255), width=11); pd.line([(int(pw * 0.04), barY - 6), (int(pw * 0.96), barY - 6)], fill=(150, 112, 56, 255), width=3)
    for sx in (int(pw * 0.04), int(pw * 0.96)): pd.line([(sx, barY - 70), (sx, int(phh * 0.80))], fill=(110, 108, 116, 255), width=7)
    ph.alpha_composite(crop, (figX, figY)) if True else None
    im.paste(ph.convert('RGB'), (px0, py0)); d.rectangle([px0, py0, px1, py1], outline=ink, width=6)
    # grey column bars under the headline on the right page, and a small caption block under the photo
    for i in range(12):
        wd = int(W_ * 0.30) if i % 5 != 4 else int(W_ * 0.19); y = 40 + 36 * i; d.rectangle([W_ // 2 + 70 + int(W_ * 0.05), y + 20, W_ // 2 + 70 + int(W_ * 0.05) + wd, y + 32], fill=(138, 136, 144, 255)) if y + 40 < H_ - 40 else None
    # fingers / thumbs at both edges
    for xe in (10, W_ - 10):
        d.ellipse([xe - 34, int(H_ * 0.50) - 44, xe + 34, int(H_ * 0.50) + 44], fill=(243, 217, 192, 255), outline=ink, width=5)
    im.save(path)
    return path
