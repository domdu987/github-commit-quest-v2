#!/usr/bin/env python3
"""c18.py -- film 18 take helper (team 4): per-frame cast18 cards (atlas textures) in the set3d18 yan_camp set.

Design: everything is set directly for the frame being rendered (no keyframes except none at all), then scene.frame_set(g) lets the set's
frame handler flicker every fire / flame card.  Cards are one quad per actor; the drawing is chosen by two object custom props (ou, ov = the
atlas cell offset) read by an Attribute node, so one material / mesh serves every actor of an atlas and a variant switch costs nothing.

    import c18 as C
    C.begin('s14')                                  # build the set (one location per process)
    at = C.Atlas('gen', {key: C.person_variant('general', pose, 'g')})   # rasterise (cached) + pack
    a = C.Actor(at, 'general', height=3.4)          # a card actor
    a.show(key, pos, cam_loc, ...)                  # per frame
"""
import os, sys, math, json, hashlib, subprocess, time, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))                      # .../film/v3
PROJ = os.path.dirname(V3)
SET = os.path.join(V3, 'set3d18')
for p in (SET, os.path.join(V3, 'cast18')):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault('NODE_PATH', '/opt/node22/lib/node_modules')
import bpy                                                       # noqa: E402
from mathutils import Vector as V                                # noqa: E402
import jimo as J                                                 # noqa: E402
import jimo_r2 as R2                                             # noqa: E402
import jimo_shots as S                                           # noqa: E402
import jimo_cards as CD                                          # noqa: E402
cast18, P = CD._cast()
T = J.T; STATE = J.STATE
WORK = os.path.join(HERE, 'work'); os.makedirs(WORK, exist_ok=True)
PNG = os.path.join(WORK, 'png'); os.makedirs(PNG, exist_ok=True)
ATL = os.path.join(WORK, 'atlas'); os.makedirs(ATL, exist_ok=True)
RASTER_MULTI = os.path.join(PROJ, 'v2', 'puppet', 'raster_multi.js')


# ----------------------------------------------------------------------------- clock
def g_of(t):
    return int(round((t + 0.10) * 30))


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


# ----------------------------------------------------------------------------- variants -> atlas
class Var(object):
    def __init__(self, svg, bbox, feet_y, height=None, anchors=None):
        self.svg, self.bbox, self.feet_y, self.height, self.anchors = svg, tuple(bbox), feet_y, height, anchors or {}
        self.h = hashlib.md5(('%s|%s|%s' % (svg, self.bbox, feet_y)).encode()).hexdigest()[:14]


def person_variant(cast, pose, uid='p'):
    f = P.figure(cast, dict(pose), uid)
    a = f['anchors']
    return Var(f['svg'], f['bbox'], f['feet_y'], height=f['feet_y'] - a['head_top'][1], anchors=a)


def ox_variant(state='dragon', view='front_three_quarter', gait='gallop', phase=0, flame=-1, reed=None, uid='o'):
    f = cast18.ox_figure(state=state, view=view, gait=gait, phase=phase / 8.0 if gait == 'gallop' else phase, flame=flame, blades=True, reed=(True if reed else None), uid=uid)
    return Var(f['svg'], (cast18.OX_CANVAS[0] - 1.4, cast18.OX_CANVAS[1] - 1.4, cast18.OX_CANVAS[2] + 1.0, cast18.OX_CANVAS[3]), 0.0, height=2.6, anchors=f['anchors'])           # the full ox canvas: the flame glow must not be clipped by a tight bbox


def _raster_all(vs, ppd):
    """rasterise every variant (cached by hash + ppd) with ONE Chromium launch; returns {h: (png, W, H, x0, feet_row)}"""
    meta, jobs = {}, []
    for v in vs:
        x0, y0, x1, y1 = v.bbox; y1 = max(y1, v.feet_y)
        W = int((x1 - x0) * ppd) + 8; H = int((y1 - y0) * ppd) + 8
        png = os.path.join(PNG, '%s_%d.png' % (v.h, ppd))
        meta[v.h] = (png, W, H, x0 - 4.0 / ppd, (v.feet_y - y0) + 4.0 / ppd)
        if not os.path.exists(png):
            svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><g transform="translate(%.2f %.2f) scale(%d)">%s</g></svg>'
                   % (W, H, 4 - x0 * ppd, 4 - y0 * ppd, ppd, v.svg))
            sp = png[:-4] + '.svg'; open(sp, 'w').write(svg)
            jobs.append(dict(svg=sp, out=png, w=W, h=H, dsf=1))
    if jobs:
        jp = os.path.join(PNG, 'jobs_%d.json' % os.getpid()); json.dump(jobs, open(jp, 'w'))
        r = subprocess.run(['node', RASTER_MULTI, jp], capture_output=True, text=True, env=os.environ)
        if r.returncode != 0:
            raise RuntimeError('raster failed: ' + r.stderr[-1500:])
        for j in jobs:
            try: os.remove(j['svg'])
            except OSError: pass
    return meta


class Atlas(object):
    """variants {key: Var} packed on a grid; every cell has the same size, drawings aligned on x = feet x (centre column 0) and the soles."""
    def __init__(self, name, variants, ppd=130, pad=3):
        from PIL import Image
        self.name, self.keys = name, list(variants.keys())
        vs = [variants[k] for k in self.keys]
        meta = _raster_all(vs, ppd)
        xmin = min(meta[v.h][3] for v in vs); xmax = max(meta[v.h][3] + meta[v.h][1] / ppd for v in vs)
        up = max(meta[v.h][4] for v in vs); down = max(meta[v.h][2] / ppd - meta[v.h][4] for v in vs)
        cw = int(math.ceil((xmax - xmin) * ppd)) + 2 * pad; ch = int(math.ceil((up + down) * ppd)) + 2 * pad
        n = len(vs); cols = max(1, int(math.ceil(math.sqrt(n * ch / float(cw))))); rows = int(math.ceil(n / float(cols)))
        while cols * cw > 8192 and cols > 1: cols -= 1; rows = int(math.ceil(n / float(cols)))
        sig = hashlib.md5(('%s|%d|%d|%d|%s' % (name, ppd, cols, pad, '|'.join(v.h for v in vs))).encode()).hexdigest()[:12]
        self.path = os.path.join(ATL, '%s_%s.png' % (name, sig))
        self.cols, self.rows, self.cw, self.ch, self.ppd = cols, rows, cw, ch, ppd
        # card rectangle in D (x relative to the feet x, z up from the soles)
        self.x0 = xmin - pad / float(ppd); self.x1 = xmin + (cw - pad) / float(ppd); self.z0 = -(down + pad / float(ppd)); self.z1 = up + pad / float(ppd)
        self.height = {k: variants[k].height for k in self.keys}; self.anchors = {k: variants[k].anchors for k in self.keys}
        self.cell = {}
        for i, k in enumerate(self.keys): self.cell[k] = (i % cols, i // cols)
        if not os.path.exists(self.path):
            im = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0))
            for k, v in zip(self.keys, vs):
                png, W, H, x0, fr = meta[v.h]; ci, cj = self.cell[k]
                src = Image.open(png).convert('RGBA')
                im.alpha_composite(src, (ci * cw + pad + int(round((x0 - xmin) * ppd)), cj * ch + pad + int(round((up - fr) * ppd))))
            im.save(self.path)
        self.meta = dict(path=self.path, x0=self.x0, x1=self.x1, z0=self.z0, z1=self.z1, cols=cols, rows=rows)

    def offsets(self, key):
        ci, cj = self.cell[key]
        return ci / float(self.cols), (self.rows - 1 - cj) / float(self.rows)


_MATS = {}


def _atlas_mat(atlas, tint, k, name):
    key = (atlas.path, tuple(round(x, 3) for x in tint), round(k, 3), STATE.get('pre'))
    if key in _MATS and bpy.data.materials.get(_MATS[key]) is not None:
        return bpy.data.materials[_MATS[key]]
    m = bpy.data.materials.new('JM_card_%s_%d' % (name, len(_MATS))); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); t = N('ShaderNodeTexImage')
    t.image = T._img(atlas.path); t.interpolation = 'Linear'; t.extension = 'CLIP'; t.image.alpha_mode = 'STRAIGHT'
    uv = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.vector_type = 'POINT'
    mp.inputs['Scale'].default_value = (1.0 / atlas.cols, 1.0 / atlas.rows, 1.0)
    a1 = N('ShaderNodeAttribute'); a1.attribute_type = 'OBJECT'; a1.attribute_name = '["ou"]'
    a2 = N('ShaderNodeAttribute'); a2.attribute_type = 'OBJECT'; a2.attribute_name = '["ov"]'
    cm = N('ShaderNodeCombineXYZ'); L(a1.outputs['Fac'], cm.inputs['X']); L(a2.outputs['Fac'], cm.inputs['Y'])
    L(uv.outputs['UV'], mp.inputs['Vector']); L(cm.outputs['Vector'], mp.inputs['Location']); L(mp.outputs['Vector'], t.inputs['Vector'])
    mm = N('ShaderNodeMix'); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs[0].default_value = 1.0; mm.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
    L(t.outputs['Color'], mm.inputs[6]); L(mm.outputs[2], em.inputs['Color']); em.inputs['Strength'].default_value = k
    L(t.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; _MATS[key] = m.name; return m


_QUADS = {}


def _atlas_quad(atlas, scale):
    key = (atlas.path, round(scale, 4))
    if key in _QUADS and bpy.data.meshes.get(_QUADS[key]) is not None:
        return bpy.data.meshes[_QUADS[key]]
    me = bpy.data.meshes.new('aq_%s_%.3f' % (atlas.name, scale))
    me.from_pydata([(atlas.x0 * scale, 0, atlas.z0 * scale), (atlas.x1 * scale, 0, atlas.z0 * scale), (atlas.x1 * scale, 0, atlas.z1 * scale), (atlas.x0 * scale, 0, atlas.z1 * scale)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    _QUADS[key] = me.name
    return me


LIGHT_TINT = R2.LIGHT_TINT


class Actor(object):
    """One card. `height` (D) scales the card so head-to-feet = height (people); for oxen pass scale=..."""
    _n = 0

    def __init__(self, atlas, role, height=None, scale=None, tint=None, k=None, shadow=True, sw=1.0, warm=0.0, ref=None, rim=None):
        Actor._n += 1
        self.rim = None; self.rim_cfg = rim
        self.atlas, self.role, self.n = atlas, role, Actor._n
        ref = ref or atlas.keys[0]
        self.sc = scale if scale is not None else height / atlas.height[ref]
        tn, kk = R2._tint(warm=warm); tn = tint or tn; kk = k if k is not None else kk
        self.me = _atlas_quad(atlas, self.sc)
        if not self.me.materials: self.me.materials.append(_atlas_mat(atlas, tn, kk, role))
        self.ob = bpy.data.objects.new('c18_%s_%d' % (role, self.n), self.me); STATE['SET'].objects.link(self.ob)
        self.ob.visible_shadow = False; J.no_bounce(self.ob); self.ob['ou'] = 0.0; self.ob['ov'] = 0.0
        self.so = None
        if shadow:
            sm = R2._shadow_quad('csh_%.2f' % sw, 1.0, 0.5)
            if not sm.materials: sm.materials.append(R2._card_mat(R2._shadow_png(), (1, 1, 1), 0.0, 'shadow'))
            self.so = bpy.data.objects.new('c18_sh_%d' % self.n, sm); STATE['SET'].objects.link(self.so); self.so.visible_shadow = False; J.no_bounce(self.so)
            self.sw = sw * self.sc
        self.height_D = height
        self.last = None
        if rim is not None:                                 # warm rim light: a second, warm-tinted, slightly bigger copy behind the card, shifted toward the fire side
            self.rim = Actor(atlas, role + '_rim', scale=self.sc, tint=rim[0], k=rim[3] if len(rim) > 3 else 1.0, shadow=False, ref=ref)

    def hide(self):
        self.ob.hide_render = True
        if self.so: self.so.hide_render = True

    def show(self, key, pos, cam, yaw=None, mirror=False, squash=(1.0, 1.0), lift=0.0, roll=0.0, scale=1.0, shadow=True, yaw_add=0.0):
        """key: atlas cell; pos: feet world point; cam: camera location (card faces it unless yaw is given, degrees)."""
        p = V(pos)
        if yaw is None:
            d = V(cam) - p; yaw = math.degrees(math.atan2(d.x, -d.y))
        ou, ov = self.atlas.offsets(key); ob = self.ob
        ob['ou'] = ou; ob['ov'] = ov
        ob.hide_render = False
        ob.location = (p.x, p.y, p.z + lift)
        ob.rotation_euler = (math.radians(roll), 0.0, math.radians(yaw + yaw_add))
        ob.scale = ((-1.0 if mirror else 1.0) * squash[0] * scale, scale, squash[1] * scale)
        if self.so:
            so = self.so; so.hide_render = (not shadow) or bool(os.environ.get('NOSH')); so.location = (p.x, p.y, p.z); so.rotation_euler = (0, 0, math.radians(yaw)); so.scale = (self.sw * scale, self.sw * scale, 1.0)
        self.last = (p, key, scale)
        if self.rim is not None:
            side, amt = self.rim_cfg[1], self.rim_cfg[2]; yr = math.radians(yaw)
            rt = V((math.cos(yr), math.sin(yr), 0.0)); nrm = V((math.sin(yr), -math.cos(yr), 0.0))
            sgn = -1.0 if mirror else 1.0
            self.rim.show(key, p + rt * (side * amt * self.sc) - nrm * 0.03, cam, yaw=yaw, mirror=mirror, squash=squash, lift=lift, roll=roll, scale=scale * 1.0, shadow=False)

    def head_chin_y(self, cam_obj, h=None):
        """px y (of 1280) of the chin line of the last shown pose (feet + height - 1 D)"""
        if self.last is None or self.ob.hide_render: return None
        from bpy_extras.object_utils import world_to_camera_view
        p, key, scale = self.last; hh = (h or self.height_D or 3.0) * scale
        c = world_to_camera_view(bpy.context.scene, cam_obj, V((p.x, p.y, p.z + hh - 1.0 * scale)))
        return round((1 - c.y) * 1280) if c.z > 0 else None


# ----------------------------------------------------------------------------- camera
def _smooth01(t):
    t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)


def cam_pose(name, g, move=None, cam=None, ease=0.35):
    """The shot's planned move evaluated at film frame g (extrapolated linearly outside the shot for handle frames).
    Same maths as jimo_shots.pose_at but the ease keeps 65 % linear speed so there are no dead ends (client rule: always moving)."""
    sh = S.SHOTS[name]; c = dict(sh['cam'], **(cam or {})); mv = dict(sh['move'], **(move or {})); dur = sh['dur']; fr = sh['frames']
    t = (g - sh['f0']) / float(fr); e = ease * _smooth01(t) + (1 - ease) * t
    loc, look = c['loc'], c['look_at']; d = S._sub(look, loc); d0 = math.sqrt(sum(x * x for x in d)); u = S._norm(d)
    push = mv.get('push', 0.0); delta = max(-0.9 * d0, min(0.6 * d0, push * dur * d0)) * e
    hx, hy = S._norm((d[0], d[1], 0.0))[:2]; right = (hy, -hx, 0.0)
    shift = mv.get('slide', 0.0) * dur / 720.0 * 2 * d0 * math.tan(S.hfov_half(c['lens'])) * e
    loc2 = S._add(S._add(loc, S._mul(u, delta)), S._mul(right, shift)); look2 = S._add(look, S._mul(right, shift))
    for m in mv.get('moves', ()):
        k = _smooth01((t - m['t']) / max(1e-6, m['dur'] / max(1, fr)))
        if k <= 0: continue
        if 'd' in m:
            dd = S._sub(look2, loc2); L = math.sqrt(sum(x * x for x in dd)); loc2 = S._sub(look2, S._mul(S._norm(dd), L * (1 + (m['d'] - 1) * k)))
    return dict(loc=tuple(loc2), look_at=tuple(look2), lens=c['lens'])


def pulse(g, gc, n_up=3, n_dn=14):
    """snap pulse 0..1: rises over n_up frames from gc, decays (smooth) over n_dn frames"""
    if g < gc: return 0.0
    if g < gc + n_up: return smooth((g - gc) / float(n_up))
    return 1.0 - smooth((g - gc - n_up) / float(n_dn))


def set_camera(name, g, shake=None, snaps=None, focus=None, **kw):
    """pose the scene camera for frame g.  shake = (yaw deg, pitch deg, roll deg, Hz): a smooth hand-held / rumble sway (client rule: always moving);
    snaps = [(g_centre, zoom factor, n_up, n_dn)]: quick push-in pulses on punch lines (lens zoom)."""
    from mathutils import Quaternion, Euler
    pose = cam_pose(name, g, **kw); cam = bpy.data.objects['cam']
    lens = pose['lens']; pk = 0.0
    for sn in (snaps or []):
        gc, fac = sn[0], sn[1]; nu = sn[2] if len(sn) > 2 else 3; nd = sn[3] if len(sn) > 3 else 14
        pp = pulse(g, gc, nu, nd); lens *= 1.0 + (fac - 1.0) * pp; pk = max(pk, pp)
    loc, look = V(pose['loc']), V(pose['look_at']); roll = 0.0
    if focus is not None and pk > 0: look = look + (V(focus) - look) * (0.45 * pk)               # the punch-in homes on the speaker, so the head does not slide down
    if shake:
        ay, ap, ar, hz = shake; t = g / 30.0; w = 2 * math.pi * hz
        yaw = ay * (0.7 * math.sin(w * t + 0.4) + 0.3 * math.sin(1.9 * w * t + 1.3)); pit = ap * (0.7 * math.sin(1.13 * w * t + 2.1) + 0.3 * math.sin(2.3 * w * t + 0.2)); roll = ar * math.sin(0.83 * w * t + 0.9)
        d = look - loc; L = d.length; d.normalize()
        up = V((0, 0, 1)); rt = d.cross(up); rt.normalize(); up2 = rt.cross(d)
        d2 = d + rt * math.tan(math.radians(yaw)) + up2 * math.tan(math.radians(pit)); d2.normalize(); look = loc + d2 * L
    q = (look - loc).normalized().to_track_quat('-Z', 'Y')
    if roll: q = q @ Quaternion((0, 0, 1), math.radians(roll))
    cam.location = loc; cam.rotation_euler = q.to_euler(); cam.data.lens = lens
    J._sky_follow(bpy.context.scene); pose = dict(pose, lens=lens); return pose


# ----------------------------------------------------------------------------- build / render
def begin(name, state=None, quality='final'):
    """Build the shot's location (once per process), the camera and the render settings."""
    A = J.build(None, name, None); sc = bpy.context.scene
    J.MN.setup_render(sc, quality); sc.render.threads = 2
    sc.cycles.transparent_max_bounces = 64          # dense herds stack 20+ alpha cards on one ray: the default 8 ended the rays as violet 'bands'
    J.apply_state(state if state is not None else S.SHOTS[name]['state'])
    J.shot_camera(name, 0.0)
    sc.camera = bpy.data.objects['cam']
    return A


def render_frame(path, g):
    sc = bpy.context.scene
    sc.frame_set(int(g))                                  # the frame handler flickers every fire / flame card for g
    bpy.context.view_layer.update()
    return T.render(path)


def head_report(cam_obj, actors):
    rep = {}
    for nm, a in actors.items():
        y = a.head_chin_y(cam_obj)
        if y is not None: rep[nm] = y
    return rep


def run_frames(name, gs, out_dir, drive, quality='final', actors=None, tag=''):
    """for g in gs: drive(g) sets the whole scene; render raw/g_%04d.png (+ json); resumable."""
    os.makedirs(out_dir, exist_ok=True); cam = bpy.data.objects['cam']
    for g in gs:
        png = os.path.join(out_dir, 'g_%04d.png' % g); js = png[:-4] + '.json'
        if os.path.exists(png) and os.path.exists(js) and json.load(open(js)).get('q') == quality: continue
        drive(g); bpy.context.view_layer.update()
        w, c = render_frame(png, g)
        rep = dict(g=g, q=quality, wall=round(w, 2), cpu=round(c, 2), heads=head_report(cam, actors or {}))
        json.dump(rep, open(js, 'w'))
        print('%s g %d: %.1f s wall %.1f cpu heads %s' % (name, g, w, c, rep['heads']), flush=True)


def warm_light(loc, energy=600.0, name='wl', radius=0.6, rgb=(1.0, 0.5, 0.18)):
    d = bpy.data.lights.new(name, 'POINT'); d.color = rgb; d.energy = energy; d.shadow_soft_size = radius; d.use_shadow = False
    o = bpy.data.objects.new(name, d); STATE['LIGHTS'].objects.link(o); o.location = loc; o.visible_camera = False; return o


def parse(spec):
    out = []
    for part in spec.split(','):
        if ':' in part:
            a = [int(v) for v in part.split(':')]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def cli(name, g0, g1, make_driver, handle_in=6, handle_out=6):
    """python3 shot.py stills|final|probe a:b[:step] [out_dir]  -- make_driver(quality) -> (drive, actors)"""
    cmd = sys.argv[1]; spec = sys.argv[2] if len(sys.argv) > 2 else '%d:%d' % (g0 - handle_in, g1 + handle_out - 1)
    if cmd == 'diff': spec = '%d:%d' % (g0, g1)
    gs = [g for g in parse(spec) if g0 - handle_in <= g <= g1 + handle_out - 1]
    quality = 'final' if cmd in ('final', 'diff') else 'preview'
    drive, actors = make_driver(quality)
    if cmd == 'diff':                                       # motion measurement: 288x512 (40 %), final 12 samples + denoise (a low-sample render is noisy and inflates the diff), mean abs diff of 90x160 grey frames
        from PIL import Image
        sc = bpy.context.scene; sc.render.resolution_percentage = 40; prev = None; ds = []
        out = os.path.join(WORK, 'diff'); os.makedirs(out, exist_ok=True)
        for g in gs:
            drive(g); bpy.context.view_layer.update(); p = os.path.join(out, 'g_%04d.png' % g); render_frame(p, g)
            im = np.asarray(Image.open(p).convert('L').resize((90, 160), Image.BILINEAR), np.float32)
            if prev is not None: ds.append(float(np.abs(im - prev).mean()))
            prev = im
        ds = np.array(ds); print('DIFF median %.2f p90 %.2f min %.2f max %.2f n %d  <1: %d' % (np.median(ds), np.percentile(ds, 90), ds.min(), ds.max(), len(ds), (ds < 1).sum()), flush=True)
        print('diffs', ' '.join('%.1f' % d for d in ds), flush=True)
        return
    if cmd == 'final':
        out = os.path.join(HERE, 'frames'); run_frames(name, gs, out, drive, quality, actors)
    else:
        out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'stills')
        for g in gs:
            drive(g); bpy.context.view_layer.update()
            p = os.path.join(out, 'g_%04d.png' % g); os.makedirs(out, exist_ok=True); w, c = render_frame(p, g)
            print('%s g %d: %.1f s heads %s' % (name, g, w, head_report(bpy.data.objects['cam'], actors)), flush=True)


def ground_at(cam_obj, u, v, z=0.0):
    """world point on the plane z = `z` seen at screen fraction (u from left, v from the TOP) through the current camera (None above the horizon)"""
    sc = bpy.context.scene; cd = cam_obj.data
    fr = list(cd.view_frame(scene=sc))                                     # 4 corners in camera space (-Z forward); identify by sign
    def corner(sx, sy): return [c for c in fr if (c.x > 0) == (sx > 0) and (c.y > 0) == (sy > 0)][0]
    bl, br, tl = corner(-1, -1), corner(1, -1), corner(-1, 1)
    pt = bl + (br - bl) * u + (tl - bl) * (1.0 - v)
    mw = cam_obj.matrix_world; o = mw.translation; d = ((mw @ pt) - o).normalized()
    if d.z > -1e-6: return None
    t = (z - o.z) / d.z
    return o + d * t



def flat_mat(rgb, name='flat'):
    """an unlit flat colour material (used to darken the moat water strip that reads as a purple band from the camp)."""
    m = bpy.data.materials.new('JM_' + name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0); em.inputs['Strength'].default_value = 1.0
    L(em.outputs['Emission'], out.inputs['Surface']); return m


def with_mouth(var, w, h, y=0.34, x=0.04, tongue=True):
    """overlay an open mouth below the moustache (the general's drawn mouth hides under it): dark ellipse w x h D at (x, y) in head coordinates"""
    el = ('<g><ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="#4a1414" stroke="#3a2832" stroke-width="0.03"/>' % (x, y, w / 2, max(h / 2, 0.012)))
    if tongue and h > 0.12: el += '<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="#d65a5a"/>' % (x, y + h * 0.22, w * 0.3, h * 0.22)
    el += '</g>'
    return Var(var.svg + el, var.bbox, var.feet_y, var.height, var.anchors)
