"""c18.py -- film-18 take helper (render team 1): per-frame animated cast18 cards on the set3d18 jimo set. Copy of this file lives in every take folder.
Usage in shot.py:  import c18 as C ; C.run(shot, actors_fn, g0, g1, hb, ha, ...)   (actors_fn(f, cam, ctx) puts cards for film frame f)"""
import os, sys, math, json, time, random, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.dirname(os.path.dirname(HERE)); SET = os.path.join(V3, 'set3d18')
if SET not in sys.path: sys.path.insert(0, SET)
import jimo as J, jimo_shots as S, jimo_r2 as R2, jimo_cards as CD
import bpy
from mathutils import Vector as V
T = J.T; MN = J.MN; STATE = J.STATE
HEIGHT = J.HEIGHT
_SIDE = {}

def ox_card(shot_key, i, pos, travel_deg, scale, camloc, state='dragon', view='three_quarter', gait='stand', phase=0, flame=-1, blades=True, theta=36,
            bob=0.0, roll=0.0, tint=None, k=None, reed=0, coat=1.0, shadow=True, pitch_bb=0.0):
    """An ox card at pos; yaw ~theta deg off the camera axis, mirrored so the head points along travel_deg. (sgn, mirror) chosen once per ox so it never pops."""
    p = V(pos); sc = scale * 1.08
    dvec = V((math.cos(math.radians(travel_deg)), math.sin(math.radians(travel_deg)), 0.0)); c = camloc - p; c.z = 0.0; c.normalize()
    def nu(sgn):
        a = math.radians(sgn * theta); n = V((c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a), 0.0)); return n, V((-n.y, n.x, 0.0))
    key = (shot_key, i)
    if key not in _SIDE:
        best = None
        for sgn in (1, -1):
            n, u = nu(sgn)
            for fac in (1, -1):
                s = (u * fac).dot(dvec)
                if best is None or s > best[0]: best = (s, sgn, fac)
        _SIDE[key] = best[1:]
    sgn, fac = _SIDE[key]; n, u = nu(sgn)
    yaw = math.degrees(math.atan2(n.x, -n.y))
    meta = card_ox(state, view, gait, phase, flame, blades, reed, coat)
    ob = R2.put_card(meta, (p.x, p.y, p.z + bob), yaw, sc, mirror=(fac < 0), name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc, shadow=shadow)
    pitch = 0.0
    if pitch_bb:
        hd = math.hypot(camloc.x - p.x, camloc.y - p.y); pitch = -math.atan2(max(0.0, camloc.z - (p.z + 1.3)), max(0.5, hd)) * pitch_bb
    if roll or pitch: ob.rotation_euler = (pitch, math.radians(roll), math.radians(yaw))
    return ob

def card_ox(state, view, gait, phase, flame, blades, reed=0, coat=1.0):
    coat = round(coat * 10) / 10.0
    key = 'oxv_%s_%s_%s_%d_%d_%d_%d_%.1f' % (state, view, gait, phase if gait != 'stand' else 0, flame, int(blades), reed, coat); name = hashlib.md5(key.encode()).hexdigest()[:10] + '_oxv'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')): return json.load(open(mp))
    cast, P = CD._cast()
    f = cast.ox_figure(state=state, view=view, gait=gait, phase=(phase if gait != 'stand' else 0) / 8.0, flame=flame, blades=blades, reed=(True if reed else None), coat=coat, uid='c%s' % name[:6])
    m = CD._write(f['svg'], f['bbox'], 0.0, CD.PXD_O, name); m['kind'] = 'ox'; json.dump(m, open(mp, 'w')); return m

def card_person_mod(pose, **mods):
    key = 'pmod_%s_%s' % (pose, sorted(mods.items())); name = hashlib.md5(key.encode()).hexdigest()[:10] + '_pmod'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')): return json.load(open(mp))
    cast, P = CD._cast(); c, ps = cast.STORY18[pose]; ps = dict(ps); ps.update(mods); f = P.figure(c, ps, 'p%s' % name[:6]); a = f['anchors']
    m = CD._write(f['svg'], f['bbox'], f['feet_y'], CD.PXD_P, name); m['kind'] = 'person'; m['height'] = f['feet_y'] - a['head_top'][1]; m['x0'] = f['bbox'][0] - 4.0 / CD.PXD_P
    json.dump(m, open(mp, 'w')); return m

def person_card(role, pose, pos, camloc, i=0, h=None, bob=0.0, roll=0.0, sx=1.0, sz=1.0, mirror=False, tint=None, k=None, yaw_off=0.0, mods=None):
    p = V(pos); meta = card_person_mod(pose, **mods) if mods else CD.card('person', pose=pose); h = h or HEIGHT.get(role, 3.0); sc = h / meta['height']
    d = camloc - p; yaw = math.degrees(math.atan2(d.x, -d.y)) + yaw_off
    ob = R2.put_card(meta, (p.x, p.y, p.z + bob), yaw, sc, mirror=mirror, name='%s%d' % (role, i), tint=tint, k=k, sw=0.9 * h / 3.0)
    ob.rotation_euler = (0, math.radians(roll), math.radians(yaw)); ob.scale = ((-1.0 if mirror else 1.0) * sx, 1.0, sz)
    return ob

def sway(f, i, amp=1.5, hz=0.7): return amp * math.sin(2 * math.pi * hz * f / 30.0 + i * 1.7)
def hop(f, i, amp=0.06, hz=3.0): return amp * abs(math.sin(math.pi * hz * f / 30.0 + i))

def shake(cam, amp, f0, f1):
    """Hand-held feel: small deterministic rotation noise (rad) on the keyed camera, 2.3 + 4.1 Hz sinusoids per axis."""
    for fc in T._fcurves(cam):
        if fc.data_path != 'rotation_euler': continue
        for kp in fc.keyframe_points:
            f = kp.co[0]; a = fc.array_index
            kp.co[1] += amp * (0.6 * math.sin(2 * math.pi * 2.3 * f / 30.0 + 1.9 * a) + 0.4 * math.sin(2 * math.pi * 4.1 * f / 30.0 + 0.7 + 2.3 * a)) * (1.0 if a != 1 else 0.5)
            kp.handle_left[1] = kp.handle_right[1] = kp.co[1]

def run(shot, actors_fn, g0, g1, hb=0, ha=0, quality=None, outdir=None, tweak=None, state=None, ctx=None, only=None, shk=0.0, cam_fn=None, dress=None):
    quality = quality or os.environ.get('Q', 'final'); outdir = outdir or os.path.join(HERE, 'raw' if quality == 'final' else ('fast' if quality == 'fast' else 'draft')); os.makedirs(outdir, exist_ok=True)
    if tweak: tweak('pre')
    A = J.build(None, shot); sc = bpy.context.scene; MN.setup_render(sc, 'preview' if quality == 'fast' else quality); sc.render.threads = 2
    if quality == 'fast': sc.render.resolution_percentage = 50; sc.cycles.samples = 3
    J.apply_state(S.SHOTS[shot]['state'] if state is None else state)
    if tweak: tweak('post', A)
    cam0 = key_cam(shot, cam_fn, g0, g1 - 1) if cam_fn else J.key_camera(shot)
    if tweak: tweak('cam', cam0)
    if shk: shake(cam0, shk, g0, g1)
    if dress is not None:
        cam_ = sc.camera; R2.LIT.clear(); R2.clear_placeholders()
        for f_ in range(g0, g1, 15):
            sc.frame_set(f_); bpy.context.view_layer.update(); actors_fn(f_, cam_.matrix_world.translation.copy(), ctx)
        cards = [o for o in bpy.data.objects if o.name.startswith('ph_') and not o.name.startswith('ph_sh_')]
        info = J.dress_ground(frames=range(g0, g1), seed=dress, actors=cards, keep_clear=[], density=2.2); print('dress_ground', info.get('n'), info.get('stat'), flush=True)
        R2.clear_placeholders(); R2.LIT.clear()
    first, last = g0 - hb, g1 - 1 + ha
    for f in range(first, last + 1): J.flicker(f)
    frames = list(range(first, last + 1))
    if os.environ.get('FRAMES'): only = [int(x) for x in os.environ['FRAMES'].split(',')]
    if only: frames = [f for f in frames if f in only]
    cam = sc.camera; log = []
    if os.environ.get('GCHECK') == '1':                                   # GCHECK1: v3/tools/ground_check.py on the real per-frame scene
        import importlib.util
        sp_ = importlib.util.spec_from_file_location('ground_check', os.path.join(HERE, '..', '..', 'tools', 'ground_check.py')); GC = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(GC)
        res, airs, fl = [], {}, []
        for f in frames[::int(os.environ.get('GSTEP', '10'))]:
            sc.frame_set(f); bpy.context.view_layer.update(); R2.clear_placeholders(); R2.LIT.clear(); actors_fn(f, cam.matrix_world.translation.copy(), ctx); bpy.context.view_layer.update()
            rs, air = GC.run_check(sc, frame_list=[f], gap=0.05, include=os.environ.get('GCINC', r'(ph_|prop|pot|jar|bowl|reed|bundle|basket|rope|hay)'), skip=os.environ.get('GCSKIP', r'(spk|flame|puff|pf\d|glow|pool|shadow|tfl|spark|hole|ph_sh_|_sh_)'))
            for r in rs: r['frame'] = f
            res.extend(rs); fl.append(f)
            for k_, v_ in air.items(): airs.setdefault(k_, []).append(f)
        GC.write_report(os.path.join(HERE, 'GROUND.md'), res, airs, 'GCHECK=1 python3 shot.py draft (frames %d-%d step %s)' % (frames[0], frames[-1], os.environ.get('GSTEP', '10')), sc, 0.05, fl)
        nf = len([r for r in res if r['status'] == 'FAIL']); print('GROUND: rows %d FAIL %d' % (len(res), nf)); sys.exit(1 if nf else 0)
    for f in frames:
        path = os.path.join(outdir, 'g_%04d.png' % f)
        if os.path.exists(path): continue
        sc.frame_set(f); bpy.context.view_layer.update()
        R2.clear_placeholders(); R2.LIT.clear()
        cl = cam.matrix_world.translation.copy()
        actors_fn(f, cl, ctx)
        bpy.context.view_layer.update()
        w, c = T.render(path); log.append(w); print('g%d %.1fs' % (f, w), flush=True)
    return log


def warm_lantern(cam, off=(0.45, -0.45, 1.6), size=0.07, energy=900.0):
    """Warm paper lantern parented to the lens (1-2 D, bottom-right): soft emissive body, dark cap/base, a small flame card on top and a warm point light (pool on the near ground)."""
    import bpy as _b
    from mathutils import Vector
    m = T.mat_emit('c18_lantern2', '#ffb055', strength=0.4) if 'c18_lantern2' not in _b.data.materials else _b.data.materials['c18_lantern2']
    kd = T.mat_emit('c18_lantern_dark2', '#4a3426', strength=0.25) if 'c18_lantern_dark2' not in _b.data.materials else _b.data.materials['c18_lantern_dark2']
    root = Vector((off[0], off[1], -off[2])); parts = []
    for (name, loc, sc, mat) in (('body', 0.0, (1.0, 1.0, 1.35), m), ('cap', 1.45, (1.12, 1.12, 0.16), kd), ('base', -1.45, (1.12, 1.12, 0.16), kd), ('ring', 1.9, (0.1, 0.1, 0.35), kd)):
        _b.ops.mesh.primitive_cylinder_add(vertices=14, radius=1.0, depth=2.0, location=(0, 0, 0)); ob = _b.context.active_object; ob.name = 'c18_lan_' + name
        ob.scale = tuple(c * size for c in sc); ob.data.materials.append(mat); ob.visible_shadow = False
        ob.parent = cam; ob.location = (root.x, root.y + loc * size, root.z); ob.rotation_euler = (math.pi / 2, 0, 0); parts.append(ob)
    d = _b.data.lights.new('c18_lan_light', 'POINT'); d.color = (1.0, 0.62, 0.28); d.energy = energy; d.shadow_soft_size = 0.3; d.use_shadow = False
    lo = _b.data.objects.new('c18_lan_light', d); _b.context.scene.collection.objects.link(lo); lo.parent = cam; lo.location = (root.x - 0.1, root.y + 0.1, root.z + 0.25); lo.visible_camera = False
    return parts

def _sm(u): u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)

def cam_path(a, b, punches=(), shk=0.0, slide=0.0):
    """Camera function for key_cam: a = (loc, look, lens) at t 0, b = (loc, look, lens) at t 1, eased (0.35 sine + 0.65 linear: no dead ends); punches = [(t0, dur_t, amount)] are HELD
    zoom steps (distance /= 1 + amount, then hold; never returns); slide = lateral D shift at t 1 (+ = camera moves right)."""
    def fn(t):
        e = 0.35 * (0.5 - 0.5 * math.cos(math.pi * t)) + 0.65 * t
        loc = V(a[0]) * (1 - e) + V(b[0]) * e; look = V(a[1]) * (1 - e) + V(b[1]) * e; lens = a[2] * (1 - e) + b[2] * e
        z = 1.0
        for p in punches:
            t0, dt, amt = p[:3]; k = _sm((t - t0) / dt); z *= 1.0 + amt * k
            if len(p) > 3: lens *= 1.0 + (p[3] - 1.0) * k
        loc = look + (loc - look) / z
        fw = (look - loc); fw.z = 0; fw.normalize(); right = V((fw.y, -fw.x, 0.0)); loc = loc + right * (slide * e); look = look + right * (slide * e)
        return loc, look, lens
    return fn

def key_cam(shot, fn, f0, f1):
    """Key the camera every frame f0..f1 from fn(t) (replaces J.key_camera); builds the shot's fg prop as shot_camera does."""
    cam = J.shot_camera(shot, 0.0); prev = None; n = f1 - f0
    for i in range(n + 1):
        loc, look, lens = fn(i / max(1, n))
        prev = cam.rotation_euler = J._look_rot(tuple(loc), tuple(look), prev); cam.location = tuple(loc); cam.data.lens = lens
        cam.keyframe_insert('location', frame=f0 + i); cam.keyframe_insert('rotation_euler', frame=f0 + i); cam.data.keyframe_insert('lens', frame=f0 + i)
    for fc in T._fcurves(cam):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    return cam

def clear_sky():
    """Cloudless sky: the sky dome texture replaced by its per-row median (a smooth gradient), so no cloud / sun sticker shows."""
    import bpy as _b, numpy as _np
    from PIL import Image as _I
    m = STATE['M']['sky']
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image is not None:
            src = _b.path.abspath(n.image.filepath); a = _np.asarray(_I.open(src).convert('RGB'), 'float32')
            med = _np.median(a, axis=1)[:, None, :]; out = _np.repeat(med, a.shape[1], axis=1)
            p = os.path.join(HERE, 'sky_clear.png'); _I.fromarray(out.astype('uint8'), 'RGB').save(p)
            n.image = _b.data.images.load(p)
            return True
    return False

def hide(*names):
    for n in names:
        ob = STATE['objects'].get(n) if 'objects' in STATE else None
        if ob is not None: ob.hide_render = True


def world_lantern(P, height=0.52, r=0.18, energy=700.0, sc=1.0):
    """A real hanging paper lantern on a stake, WORLD-fixed at ground point P: warm paper body (emission x3.5), 6 dark ribs, wooden caps, a cord loop, a stake, a warm point light (orange pool on the ground)."""
    import bpy as _b
    P = V(P)
    body = T.mat_emit('c18_paper', '#ff8a2e', strength=3.5) if 'c18_paper' not in _b.data.materials else _b.data.materials['c18_paper']
    wood = T.mat_emit('c18_wood', '#3a2418', strength=0.35) if 'c18_wood' not in _b.data.materials else _b.data.materials['c18_wood']
    height *= sc; r *= sc; zc = 1.2 * sc; out = []
    def cyl(name, loc, rad, h, mat, v=16):
        _b.ops.mesh.primitive_cylinder_add(vertices=v, radius=rad, depth=h, location=(P.x + loc[0], P.y + loc[1], P.z + loc[2])); ob = _b.context.active_object; ob.name = name; ob.data.materials.append(mat); ob.visible_shadow = False; out.append(ob); return ob
    cyl('c18_lan_stake', (0, 0, 0.5 * sc), 0.04 * sc, 1.0 * sc, wood, 8)
    cyl('c18_lan_arm', (0.0, 0.0, 0.98 * sc), 0.03 * sc, 0.1 * sc, wood, 8)
    b = cyl('c18_lan_body', (0, 0, zc), r, height, body, 20)
    cyl('c18_lan_cap_t', (0, 0, zc + height / 2 + 0.04), r * 1.08, 0.08, wood, 20)
    cyl('c18_lan_cap_b', (0, 0, zc - height / 2 - 0.04), r * 1.08, 0.08, wood, 20)
    for k in range(5): cyl('c18_lan_rib%d' % k, (0, 0, zc - height / 2 + (k + 0.5) * height / 5), r * 1.03, 0.025, wood, 20)
    cyl('c18_lan_cord', (0, 0, zc + height / 2 + 0.2), 0.02, 0.3, wood, 6)
    d = _b.data.lights.new('c18_lan_light', 'POINT'); d.color = (1.0, 0.6, 0.25); d.energy = energy; d.shadow_soft_size = 0.35; d.use_shadow = False
    lo = _b.data.objects.new('c18_lan_light', d); _b.context.scene.collection.objects.link(lo); lo.location = (P.x, P.y, P.z + zc - 0.1); lo.visible_camera = False; d.energy = energy * sc * sc
    for ob in out:
        for c in ob.users_collection: pass
    return out


def fg_rail(cam, y=-1.62, z=-1.6, w=3.4):
    """Dark wooden fence rail with two posts and a small paper lantern across the bottom edge, parented to the camera (shows up when the lens goes wide)."""
    import bpy as _b
    wood = T.mat_emit('c18_rail', '#2c1c12', strength=0.5) if 'c18_rail' not in _b.data.materials else _b.data.materials['c18_rail']
    paper = T.mat_emit('c18_paper2', '#ff8a2e', strength=3.5) if 'c18_paper2' not in _b.data.materials else _b.data.materials['c18_paper2']
    def box(name, loc, sc, mat):
        _b.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0)); ob = _b.context.active_object; ob.name = name; ob.scale = sc; ob.data.materials.append(mat); ob.visible_shadow = False
        ob.parent = cam; ob.location = loc; ob.rotation_euler = (0, 0, 0); return ob
    box('c18_rail_bar', (0, y, z), (w, 0.14, 0.1), wood); box('c18_rail_bar2', (0, y - 0.28, z), (w, 0.12, 0.1), wood)
    for x in (-1.3, 0.2, 1.3): box('c18_rail_post%d' % int(x * 10), (x, y - 0.1, z), (0.11, 0.62, 0.11), wood)
    box('c18_rail_lan', (1.3, y + 0.42, z), (0.2, 0.34, 0.2), paper); box('c18_rail_lan_cap', (1.3, y + 0.62, z), (0.24, 0.05, 0.24), wood)
    d = _b.data.lights.new('c18_rail_light', 'POINT'); d.color = (1.0, 0.6, 0.25); d.energy = 160.0; d.shadow_soft_size = 0.3; d.use_shadow = False
    lo = _b.data.objects.new('c18_rail_light', d); _b.context.scene.collection.objects.link(lo); lo.parent = cam; lo.location = (1.2, y + 0.5, z + 0.3); lo.visible_camera = False

# GCHECK1 patched
