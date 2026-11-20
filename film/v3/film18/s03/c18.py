#!/usr/bin/env python3
"""c18.py -- helper for the film-18 take scripts of render team 2 (copied per take folder; no shared film18/common.py).

Every take script does:
    import c18
    T = c18.Take('s03', first_g, last_g)      # builds the set (one location per process), the shot camera + fg prop
    T.run(frame_fn)                           # frame_fn(T, g) sets the state / cards for film frame g; the helper renders g_%04d.png (resumable)

What this adds on top of set3d18/jimo.py:
  * cam pose for ANY film frame g (handles outside the shot are extrapolated at the mean speed of the move, so dissolve handles keep moving)
  * per-frame cards (person puppets with arbitrary pose dicts, dragon / plain ox cards with optional tail smoke) baked through the cast18 rasteriser
    into THIS take folder (cards/), never into the set folder
  * head / chin pixel rows for QA, one JSON line per frame
"""
import os, sys, math, json, time, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))                  # film/v3
PROJ = os.path.dirname(V3)                                   # film
SETD = os.path.join(V3, 'set3d18')
CASTD = os.path.join(V3, 'cast18')
os.environ.setdefault('NODE_PATH', '/opt/node22/lib/node_modules')
for p in (SETD, CASTD):
    if p not in sys.path:
        sys.path.insert(0, p)
import numpy as np                                           # noqa: E402
import bpy                                                   # noqa: E402
from mathutils import Vector as V                            # noqa: E402
import jimo as J                                             # noqa: E402
import jimo_shots as S                                       # noqa: E402
import jimo_r2 as R2                                         # noqa: E402
import jimo_cards as CD                                      # noqa: E402

CD.CARDS = os.path.join(HERE, 'cards')                       # bake into the take folder
os.makedirs(CD.CARDS, exist_ok=True)
STATE = J.STATE
FRAMES = os.path.join(HERE, 'frames')


# ----------------------------------------------------------------------------- clock
def g_of(t):
    """narration time -> film frame of an event (narration at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def lerp(a, b, u): return a + (b - a) * u


def ramp(g, g0, g1):
    return ease((g - g0) / float(g1 - g0))


# ----------------------------------------------------------------------------- cards
def _cast():
    return CD._cast()


def pcard(cast, pose, key):
    """a person puppet card for an arbitrary pose dict (cached by key in cards/)."""
    name = hashlib.md5(('P|%s|%s' % (cast, key)).encode()).hexdigest()[:10] + '_person'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')):
        return json.load(open(mp))
    c18, P = _cast()
    f = P.figure(cast, dict(pose), 'p%s' % name[:6]); a = f['anchors']
    m = CD._write(f['svg'], f['bbox'], f['feet_y'], CD.PXD_P, name)
    m['kind'] = 'person'; m['height'] = f['feet_y'] - a['head_top'][1]; m['x0'] = f['bbox'][0] - 4.0 / CD.PXD_P
    json.dump(m, open(mp, 'w')); return m


def smoke_svg(ax, ay, k, n=4, grey='#a39ea4'):
    """tail smoke wisps rising from (ax, ay) (D units, y down); k = drawing index (drift / size vary)."""
    s = ['<defs><filter id="sb%d" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="0.07"/></filter></defs>' % k]
    for i in range(n):
        u = (i + 0.35 * (k % 3)) / n
        cx = ax - 0.15 - 0.55 * u + 0.16 * math.sin(k * 1.3 + i * 2.1); cy = ay - 0.25 - 2.0 * u
        r = 0.22 + 0.34 * u; op = 0.80 * (1.0 - 0.75 * u)
        s.append('<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="%s" opacity="%.2f" filter="url(#sb%d)"/>' % (cx, cy, r * 1.15, r, grey, op, k))
    return ''.join(s)


def oxcard(state='dragon', view='three_quarter', gait='gallop', phase=0, flame=-1, smoke=None, reed=False, face=None):
    """an ox card (8 gallop drawings, phase = 0..7); smoke = None or a drawing index for grey tail wisps (no flame)."""
    key = 'OX3|%s|%s|%s|%d|%d|%s|%s|%s' % (state, view, gait, phase, flame, smoke, reed, face)
    name = hashlib.md5(key.encode()).hexdigest()[:10] + '_ox'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')):
        return json.load(open(mp))
    c18, P = _cast()
    f = c18.ox_figure(state=state, view=view, gait=gait, phase=phase / 8.0, flame=flame, blades=True, reed=(True if reed else None), uid='c%s' % name[:6], face=face)
    svg = f['svg']; bb = list(f['bbox'])
    if smoke is not None:
        ax, ay = f['anchors']['tail_tip']
        svg += smoke_svg(ax, ay, smoke); bb[1] = min(bb[1], ay - 2.2); bb[0] = min(bb[0], ax - 1.2)
    m = CD._write(svg, bb, 0.0, CD.PXD_O, name); m['kind'] = 'ox'
    json.dump(m, open(mp, 'w')); return m


def put(meta, pos, cam_loc, height=None, scale=None, mirror=False, name='c', tint=None, k=None, sw=1.6, yaw_off=0.0, yaw=None):
    """card at pos, billboarded (yaw about z only) toward the camera position, optional yaw offset / absolute yaw (deg)."""
    p = V(pos)
    if height is not None:
        scale = height / meta['height']
    d = V(cam_loc) - p
    y = math.degrees(math.atan2(d.x, -d.y)) + yaw_off if yaw is None else yaw
    return R2.put_card(meta, tuple(p), y, scale or 1.0, mirror=mirror, name=name, tint=tint, k=k, sw=sw)


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, shot, first_g, last_g, draft=False, moves=None, cam_fn=None, setup=None):
        self.shot = shot; self.first_g = first_g; self.last_g = last_g; self.draft = draft
        self.sh = S.SHOTS[shot]; self.f0 = self.sh['f0']; self.frames = self.sh['frames']
        if moves is not None:
            self.sh['move'] = dict(self.sh['move'], moves=moves)
        self.A = J.build(None, shot)
        if setup:
            setup(self)
        sc = bpy.context.scene
        J.MN.setup_render(sc, 'preview' if draft else 'final'); sc.render.threads = int(os.environ.get('THREADS', '2'))
        self.cam = J.shot_camera(shot, 0.0)            # builds the shot's fg prop (parented to the camera) + the scene camera
        self.cam_fn = cam_fn
        self.log = []

    # -- camera
    def pose(self, g):
        t = (g - self.f0) / float(self.frames)
        if self.cam_fn is not None:
            return self.cam_fn(self, g, t)
        return self.base_pose(t)

    def base_pose(self, t):
        sh = self.sh
        if 0.0 <= t <= 1.0:
            return S.pose_at(sh, t)
        e = 0.12                                                          # handles: keep moving at the mean speed of the first / last 12 % of the move
        if t < 0:
            p0 = S.pose_at(sh, 0.0); p1 = S.pose_at(sh, e); dt = t / e
        else:
            p0 = S.pose_at(sh, 1.0); p1 = S.pose_at(sh, 1.0 - e); dt = (1.0 - t) / e
            p0, p1 = p0, p1
        sgn = 1.0 if t < 0 else -1.0
        loc = tuple(p0['loc'][i] + (p1['loc'][i] - p0['loc'][i]) * (dt if t < 0 else dt) for i in range(3))
        look = tuple(p0['look_at'][i] + (p1['look_at'][i] - p0['look_at'][i]) * (dt if t < 0 else dt) for i in range(3))
        return dict(loc=loc, look_at=look, lens=p0['lens'])

    def set_camera(self, g):
        pose = self.pose(g); cam = self.cam
        cam.location = pose['loc']; cam.rotation_euler = J._look_rot(pose['loc'], pose['look_at']); cam.data.lens = pose['lens']
        J._sky_follow(bpy.context.scene); bpy.context.view_layer.update()
        self.cur = pose
        return pose

    # -- heads
    def project(self, p):
        from bpy_extras.object_utils import world_to_camera_view
        a = world_to_camera_view(bpy.context.scene, self.cam, V(p))
        return (a.x * (720 if not self.draft else 360) * (1 if not self.draft else 2), (1 - a.y) * 1280)

    def head_row(self, pos, h, role):
        top = self.project((pos[0], pos[1], pos[2] + h)); chin = self.project((pos[0], pos[1], pos[2] + h - 1.0)); feet = self.project(pos)
        return dict(role=role, x=round(top[0]), top=round(top[1]), chin=round(chin[1]), feet=round(feet[1]))

    # -- run
    def frame_path(self, g):
        return os.path.join(FRAMES, 'g_%04d.png' % (g if not self.draft else g)) if not self.draft else os.path.join(HERE, 'draft', 'g_%04d.png' % g)

    def run(self, frame_fn, gs=None, force=False, only=None):
        os.makedirs(os.path.dirname(self.frame_path(0)), exist_ok=True)
        sc = bpy.context.scene
        glist = gs if gs is not None else list(range(self.first_g, self.last_g + 1))
        tl = os.path.join(HERE, 'frames_log.jsonl' if not self.draft else 'draft_log.jsonl')
        for g in glist:
            out = self.frame_path(g)
            if os.path.exists(out) and not force:
                continue
            R2.clear_placeholders(); R2.LIT.clear()
            sc.frame_set(self.f0 + (g - self.f0) + 1)
            pose = self.set_camera(g)
            info = frame_fn(self, g) or {}
            bpy.context.view_layer.update()
            t0 = time.time()
            w, c = J.T.render(out)
            row = dict(g=g, wall=round(w, 1), cpu=round(c, 1), cam=[round(x, 2) for x in pose['loc']], heads=info.get('heads', []))
            open(tl, 'a').write(json.dumps(row) + '\n')
            print('g%d %.1fs wall %.1fs cpu %s' % (g, w, c, info.get('heads', '')), flush=True)


def parse_args(default_first, default_last):
    """CLI: python3 shot.py draft|final [a:b[:step]] ..."""
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'
    rng = None
    if len(sys.argv) > 2:
        parts = sys.argv[2].split(':'); a, b = int(parts[0]), int(parts[1]); st = int(parts[2]) if len(parts) > 2 else 1
        rng = list(range(a, b + 1, st))
    return mode, rng


# ----------------------------------------------------------------------------- vista fixes (s03 / s04 / s25): all done at runtime, the set stays untouched
def fix_sky(T, tex_name='sky_DUSK'):
    """repaint the dusk sky clouds with SHORT base bars (QA_ART_SET_R2 13): the cloud base is a rounded band no wider than the puffs, same random sequence as the set's painter."""
    import random
    from PIL import Image as I, ImageDraw
    set_png = os.path.join(SETD, 'tex_jimo', tex_name + '.png')
    out = os.path.join(HERE, 'sky_fix.png')
    if not os.path.exists(out):
        a = I.open(set_png).convert('RGB')                       # the set's cached dusk sky incl. its (long-bar) clouds
        # repaint: re-run the set's painter body with a different cloud() into a temp file
        import jimo_tex as JX
        src = open(JX.__file__).read()
        i0 = src.rindex('def dusk_sky(path'); i1 = src.index('def patchwork', i0)
        body = src[i0:i1]
        c0 = body.index("    def cloud(cx, cy, cw, ch):"); c1 = body.index("    for k in range(34):")
        cloud_new = """    def cloud(cx, cy, cw, ch):
        n = r.randint(3, 5); top = (255, 214, 168, 255); base = (176, 112, 136, 255); pf = []
        for k in range(n):
            bx = cx - cw / 2 + cw * (k + 0.5) / n; rr = ch * r.uniform(0.45, 0.8); pf.append((bx, rr))
        for (bx, rr) in pf:                                       # mauve underside: the same puffs pushed down, no flat bar
            d.ellipse([bx - rr * 1.2, cy - rr * 0.8 + ch * 0.22, bx + rr * 1.2, cy + rr * 1.1 + ch * 0.12], fill=base)
        for (bx, rr) in pf:
            d.ellipse([bx - rr * 1.2, cy - rr * 1.0, bx + rr * 1.2, cy + rr * 0.9], fill=top)
"""
        body = body[:c0] + cloud_new + body[c1:]
        ns = dict(JX.__dict__); exec(compile(body, 'dusk_sky_fix', 'exec'), ns)
        ns['dusk_sky'](out)
    img = None
    for m in bpy.data.materials:
        if m.name.startswith(STATE['pre']) and m.node_tree and m.name.endswith('sky'):
            for n in m.node_tree.nodes:
                if n.bl_idname == 'ShaderNodeTexImage' and n.image is not None:
                    img = n.image
    if img is None:
        for im in bpy.data.images:
            if tex_name in os.path.basename(im.filepath):
                img = im
    if img is not None:
        img.filepath = out; img.reload()
    return img is not None


def qi_cloth_material():
    m = bpy.data.materials.get('t18_qicloth')
    if m is None:
        m = bpy.data.materials.new('t18_qicloth'); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfDiffuse'); bs.inputs['Color'].default_value = (0.42, 0.045, 0.04, 1.0)
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.5, 0.06, 0.05, 1.0); em.inputs['Strength'].default_value = 0.35
        ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(bs.outputs['BSDF'], ad.inputs[0]); nt.links.new(em.outputs['Emission'], ad.inputs[1]); nt.links.new(ad.outputs['Shader'], out.inputs['Surface'])
    return m


def solid_material(name, rgb, k=0.3):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfDiffuse'); bs.inputs['Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0); em.inputs['Strength'].default_value = k
        ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(bs.outputs['BSDF'], ad.inputs[0]); nt.links.new(em.outputs['Emission'], ad.inputs[1]); nt.links.new(ad.outputs['Shader'], out.inputs['Surface'])
    return m


def fix_vista(T, hold_scale=0.5, **kw):
    """vista round 3 does the farmland / Ju / shadows itself; here only: opaque Qi cloth flags (no bloom), Jimo's flag at half size."""
    red = solid_material('t18_qi_red', (0.46, 0.06, 0.05), 0.32); teal = solid_material('t18_qi_teal', (0.42, 0.26, 0.05), 0.2)
    for p in STATE['pennants']:
        o = p.get('ob')
        if o is None or p['kind'] != 'qi':
            continue
        for i, m in enumerate(o.data.materials):
            if m.name.endswith('b82c20_1.15_1_1_None'): o.data.materials[i] = red
            if m.name.endswith('2a6a7a_1.1_1_1_None'): o.data.materials[i] = teal
    STATE['hold_scale'] = hold_scale


def hold_apply(T):
    """after set_pennants / set_qi_return (which reset the holdout flag scale): scale the two holdout flags about their pole feet."""
    for p in STATE['pennants']:
        if p.get('hold') and p.get('ob') is not None:
            pass


def tilt_cam(dz_look, dz_loc=0.0):
    """camera function: the shot's move with the look-at dropped by dz_look (a tilt down: less empty sky)."""
    def fn(T, g, t):
        p = T.base_pose(t)
        return dict(loc=(p['loc'][0], p['loc'][1], p['loc'][2] + dz_loc), look_at=(p['look_at'][0], p['look_at'][1], p['look_at'][2] + dz_look), lens=p['lens'])
    return fn


def clear_sightline(T, key='ju', gs=(), radius=95, extra=()):
    """hide (for the whole take) the Yan pennants that cover the holdout town `key` in the frames gs (a near flag hides far Ju completely from the s04 camera)."""
    from mathutils import Vector as V_
    tx, ty, tz = STATE['marks'][key]; hide = set()
    for g in gs:
        T.set_camera(g); jx, jy = T.project((tx, ty, tz + 20.0)); r = radius
        for p in STATE['pennants']:
            if p['kind'] != 'yan' or p.get('hold'):
                continue
            t = STATE['towns'][p['town']]; s = t['s']; hgt = (10.0 + s * 0.6) * 1.35; fw, fh = s * 0.5 * 1.5, s * 0.3 * 1.5
            bx, by, bz = p['base']
            pts = [(bx + dx, by, bz + dz) for dx in (0, fw) for dz in (hgt - fh, hgt)]
            ps = [T.project(q) for q in pts]
            x0, x1 = min(q[0] for q in ps), max(q[0] for q in ps); y0, y1 = min(q[1] for q in ps), max(q[1] for q in ps)
            if x1 > jx - r and x0 < jx + r and y1 > jy - r and y0 < jy + r:
                hide.add(p['town'])
    STATE['hidden_pennants'] = hide | set(extra)
    return hide


def hide_pennants(T):
    for p in STATE['pennants']:
        if p['kind'] == 'yan' and p['town'] in STATE.get('hidden_pennants', ()) and p.get('ob') is not None:
            p['ob'].hide_render = True; p['ob'].scale = (0.01, 0.01, 0.01)


def rhythm_cam(push=0.12, slide=120.0, pulses=(), width=12, amp=0.05, sway=0.0, pan=0.0, axis='push', orbit=0.0):
    """camera function for the client's camera rhythm (in-shot frame diff median >= 4, p90 >= 12): the shot's own eased move, PLUS a steady extra push (fraction of the
    camera-to-target distance per second), a steady lateral slide (px/s of the frame width), and push 'punches': at each g in `pulses` the camera lunges in by amp x distance
    over `width` frames and settles back (a sin^2 bump).  Handles keep the same motion (the formula is defined for any g)."""
    import numpy as np

    def fn(T, g, t):
        p = T.base_pose(t); s = (g - T.f0) / 30.0
        loc = np.array(p['loc'], dtype=float); look = np.array(p['look_at'], dtype=float); d = look - loc; d0 = float(np.linalg.norm(d)); u = d / d0
        h = math.hypot(d[0], d[1]) or 1.0; right = np.array([d[1] / h, -d[0] / h, 0.0])
        loc = loc + u * d0 * push * s
        sh = slide * s / 720.0 * 2 * d0 * math.tan(math.atan(10.125 / p['lens']))
        if orbit:                                                     # orbit about the look-at point (the subject stays framed), deg/s
            a = math.radians(orbit * s); r = loc - look; ca, sa = math.cos(a), math.sin(a)
            loc = look + np.array([r[0] * ca - r[1] * sa, r[0] * sa + r[1] * ca, r[2]])
        else:
            loc = loc + right * sh; look = look + right * sh
        for g0 in pulses:
            k = (g - g0) / float(width)
            if 0.0 < k < 1.0:
                b = math.sin(math.pi * k) ** 2
                if axis == 'push':
                    loc = loc + u * d0 * amp * b
                elif axis == 'pan':                           # whip-pan wiggle: pure rotation (look point swings sideways, the lens stays where it is)
                    sgn = 1.0 if int(round(g0)) % 2 == 0 else -1.0
                    look = look + right * d0 * amp * b * sgn
                else:                                         # lateral punch (a sideways truck with a partial counter-pan): never drives the lens through the set
                    sgn = 1.0 if int(round(g0)) % 2 == 0 else -1.0
                    loc = loc + right * d0 * amp * b * sgn; look = look + right * d0 * amp * b * sgn * 0.45
        if sway:
            loc = loc + right * sway * d0 * math.sin(s * 4.2)
        return dict(loc=tuple(loc), look_at=tuple(look), lens=p['lens'])
    return fn


def compose(f1, f2):
    """camera functions: f1's pose, then f2 applied to it as the base (f2 sees f1's pose through T.base_pose)."""
    def fn(T, g, t):
        orig = T.base_pose
        p1 = f1(T, g, t)
        T.base_pose = lambda tt: p1
        try:
            return f2(T, g, t)
        finally:
            T.base_pose = orig
    return fn


def fix_sky_clean(T, tex_name='sky_DAWN'):
    """cloud stickers out (TAKE gate): the sky texture is replaced by its row-median gradient (every cloud / sun disc column averaged away)."""
    from PIL import Image as I
    out = os.path.join(HERE, 'sky_clean.png')
    if not os.path.exists(out):
        a = np.asarray(I.open(os.path.join(SETD, 'tex_jimo', tex_name + '.png')).convert('RGB'), dtype='float32')
        med = np.median(a, axis=1); k = np.ones(41, dtype='float32') / 41.0; pad = np.pad(med, ((20, 20), (0, 0)), mode='edge')
        ref = np.stack([np.convolve(pad[:, c], k, mode='valid') for c in range(3)], axis=1)[:, None, :]
        I.fromarray(np.clip(np.repeat(ref, a.shape[1], axis=1), 0, 255).astype('uint8'), 'RGB').save(out)
    for im in bpy.data.images:
        if tex_name in os.path.basename(im.filepath):
            im.filepath = out; im.reload(); return True
    return False


def dress(T, gs, seed=0, keep_clear=None, actors=None, density=1.0):
    """the director's J.dress_ground over the whole move: key the camera at the sampled film frames (the helper evaluates the camera per film frame), dress, drop the keys again
    (the per-frame driver sets the camera itself)."""
    cam = T.cam; sc = bpy.context.scene
    gl = list(gs)
    for g in gl[::max(1, len(gl) // 40)] + [gl[-1]]:
        pose = T.pose(g); cam.location = pose['loc']; cam.rotation_euler = J._look_rot(pose['loc'], pose['look_at']); cam.data.lens = pose['lens']
        cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g); cam.data.keyframe_insert('lens', frame=g)
    info = J.dress_ground(cam=cam, frames=gl, seed=seed, keep_clear=keep_clear, actors=actors, density=density)
    cam.animation_data_clear()
    try:
        cam.data.animation_data_clear()
    except Exception:
        pass
    return info


def vista_quiet(T, ju_y=100.0):
    """caption-band / bloom control for the round-3 vista: glints off, the halo cards of the Jimo side removed (Ju's stay), the siege-camp fire flames off, the grey Jimo ring road stays."""
    import bmesh
    ob = STATE['objects']
    if 'r3glints' in ob:
        ob['r3glints'].hide_render = True
    for k in list(ob):
        if k.startswith('flame_siegefire'):
            ob[k].hide_render = True
    h = ob.get('halos')
    if h is not None:
        bm = bmesh.new(); bm.from_mesh(h.data); mw = h.matrix_world
        dl = [f for f in bm.faces if (mw @ f.calc_center_median()).y < ju_y]
        bmesh.ops.delete(bm, geom=dl, context='FACES'); bm.to_mesh(h.data); bm.free()


def jimo_flag(k=0.45):
    """Vista round 4: the near Qi flag of Jimo (a holdout) at scale k (cloth grows from the pole top)."""
    import jimo_vista as VS_
    for i, t in enumerate(STATE['towns']):
        if t.get('name') == 'jimo':
            VS_.set_pennant_scale(i, k, kind='qi')
