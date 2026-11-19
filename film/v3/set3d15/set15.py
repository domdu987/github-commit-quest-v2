#!/usr/bin/env python3
"""set15.py : set of film 15 ("ไอ้ปลาดิ้น", the Fosbury Flop) as a real 3D Blender set (bpy 5.x, Cycles CPU). See API.md.
    import set15 as F
    A = F.build('A', 'GOLDEN')            # A: GOLDEN | DAY   (high-school track 1963, SAWDUST pit)
    A = F.build('B', 'EVE')               # B: EVE | TENSE | DAY (Olympic stadium 1968, foam pit)
    A = F.build(shot=7)                   # location + light + camera of a shot of film15/shot_plan.md
    cam = F.make_camera(A['cam'])         # 22 mm, no DOF
World: 1 unit = 1 D = 0.6 m (adult 3.0 D), Z up. Inside the builders everything is metres; the set hangs under SETROOT scaled 1/0.6."""
import os, sys, math, json, time
import numpy as np
import bpy
from mathutils import Vector, Matrix
import set15_lib as L
from set15_lib import S, U, DM, STATE, T, kdir, mat, rnd
import set15_a as LA

HERE = L.HERE
WORK = os.path.join(HERE, 'work')

# ----------------------------------------------------------------------------- light presets
_B = dict(toon=1.0, form=(0.0, -0.05, 0.22), sun_angle=0.6, exposure=0.0, lift=(0.008, 0.008, 0.02), grade_offset=(-0.006, -0.01, -0.014), grade_saturation=1.16, bloom_size=0.05,
          shade_mix=0.55, crowd_k=1.0, season=0.0, floods=0.0, cx=0.0, cy=0.0)
_SKY_EVE = [(0.0, '#2a3494'), (0.4, '#5a68c4'), (0.5, '#f2a068'), (0.53, '#e6c0a0'), (0.58, '#a4b8e4'), (0.68, '#4a62c0'), (0.82, '#2a3a9c'), (1.0, '#212a82')]
LIGHTS = dict(
    A_GOLDEN=dict(_B, name='A_GOLDEN', loc='A', key=(1.62, 1.16, 0.68), key_dir=kdir(-60, 24), sun_elev=24, sun_angle=0.9, shade=(0.105, 0.10, 0.31), shade_tint=(0.10, 0.095, 0.33), season=1.0,
                  sky=[(0.0, '#7a70e0'), (0.40, '#f2b47a'), (0.5, '#f8cf96'), (0.56, '#d8d0c8'), (0.64, '#8aa0ec'), (0.8, '#5c6ee6'), (1.0, '#4a58d8')], sky_k=1.25, glow=('#ffa860', 0.35, 0.45),
                  hills=[(300, 6, 14, '#a08ac8'), (340, 20, 28, '#8f90d0')], hill_k=0.95),
    A_DAY=dict(_B, name='A_DAY', loc='A', key=(1.72, 1.56, 1.26), key_dir=kdir(-38, 44), sun_elev=44, shade=(0.115, 0.115, 0.34), shade_tint=(0.105, 0.105, 0.35), season=0.0,
               sky=[(0.0, '#8a90e8'), (0.4, '#bcd0f4'), (0.5, '#eaf0f8'), (0.56, '#dce8f6'), (0.64, '#86b0f0'), (0.8, '#5a8ae6'), (1.0, '#4474de')], sky_k=1.2, glow=('#fff0d0', 0.5, 0.3),
               hills=[(300, 6, 14, '#9aaedc'), (340, 20, 28, '#8aa0d8')], hill_k=0.95),
    B_EVE=dict(_B, name='B_EVE', loc='B', key=(1.42, 0.92, 0.5), key_dir=kdir(-48, 19), sun_elev=19, sun_angle=1.0, shade=(0.10, 0.10, 0.32), shade_tint=(0.095, 0.095, 0.34), cy=8.0, floods=1.0,
               sky=_SKY_EVE, sky_k=1.15, glow=('#ffb050', 0.6, 0.7), hills=[(420, 20, 30, '#6a60b8'), (480, 40, 40, '#5a58b0')], hill_k=0.9, towers=[20, 62, 118, 160], cauldron_t=104),
    B_TENSE=dict(_B, name='B_TENSE', loc='B', key=(0.92, 0.60, 0.42), key_dir=kdir(-48, 15), sun_elev=15, sun_angle=1.0, shade=(0.07, 0.07, 0.25), shade_tint=(0.07, 0.07, 0.27), lift=(0.006, 0.006, 0.02), cy=8.0, floods=2.2, crowd_k=0.62,
                 sky=[(0.0, '#141a60'), (0.4, '#26307c'), (0.5, '#8a5a7c'), (0.53, '#a8829e'), (0.58, '#5a68b0'), (0.68, '#2a3a94'), (0.82, '#1c2a84'), (1.0, '#141c6c')], sky_k=1.05, glow=('#ff9050', 0.7, 0.35),
                 hills=[(420, 20, 30, '#3c3c8c'), (480, 40, 40, '#34357e')], hill_k=0.8, towers=[20, 62, 118, 160], cauldron_t=104, grade_saturation=1.12),
    B_DAY=dict(_B, name='B_DAY', loc='B', key=(1.66, 1.52, 1.28), key_dir=kdir(-36, 42), sun_elev=42, shade=(0.115, 0.115, 0.35), shade_tint=(0.105, 0.105, 0.36), cy=8.0, floods=0.0,
               sky=[(0.0, '#3a50c8'), (0.4, '#6a94e8'), (0.5, '#d6e6f6'), (0.54, '#c8dcf2'), (0.6, '#8ab4f0'), (0.7, '#5584e2'), (0.84, '#3c66d6'), (1.0, '#2e52c8')], sky_k=1.15, glow=('#fff0d0', 0.5, 0.3),
               hills=[(420, 20, 30, '#7e96d6'), (480, 40, 40, '#6e88cc')], hill_k=0.9, towers=[20, 62, 118, 160], cauldron_t=104),
)
LOC_LIGHTS = dict(A=['GOLDEN', 'DAY'], B=['EVE', 'TENSE', 'DAY'])
HEIGHT = dict(dick=3.2, coach=2.85, boy=2.9, rival=3.1, official=2.9, photographer=2.7, spectator=2.8, reader=2.8)   # D

# ----------------------------------------------------------------------------- build
def build(location=None, light=None, preset=None, clear=True, dress=True, shot=None, **kw):
    """Build a location with a light preset into the current scene: world, sun, all set geometry, render settings, grade.
    build('A','GOLDEN') | build('B','TENSE') | build(shot=24). Returns the anchors dict (API.md)."""
    if shot is not None:
        sd = SHOTS[int(shot)]; location, light = sd['loc'], sd['light']
    location = location or 'A'; light = light or LOC_LIGHTS[location][0]
    assert light in LOC_LIGHTS[location], 'light %s: %s has %s' % (light, location, LOC_LIGHTS[location])
    key = '%s_%s' % (location, light); scene = bpy.context.scene; P = dict(LIGHTS[key])
    STATE.clear(); STATE['P'] = P; STATE['loc'] = location; STATE['light'] = light; STATE['key'] = key; S.MATS.clear(); LA.MARKS_A.clear()
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_cards_face',): h.remove(f)
    if clear:
        for ob in list(bpy.data.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras, bpy.data.materials):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('S15_'): bpy.data.node_groups.remove(ng)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    scene.frame_start = 1; scene.frame_current = 1; scene.render.fps = 30
    L.add_sun(P)
    M = S.pal(); STATE['M'] = M
    if location == 'A': LA.build_a(P, M, dress)
    else:
        import set15_b as LB
        LB.build_b(P, M, dress)
    set_bar_height(STATE['J']['h0'])
    setup_render(scene, 'final'); T.setup_grade(scene)
    A = anchors(shot); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """tower.setup_render (final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light only) + OIDN; no DOF."""
    T.setup_render(scene, quality); c = scene.cycles; c.use_light_tree = False; c.transparent_max_bounces = 24
    c.use_denoising = True; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'FAST'
    try: c.denoising_use_gpu = False
    except Exception: pass

def make_camera(setup, name='cam', scene=None):
    """tower.make_camera (loc / look_at / lens / up / roll, D units) with DOF off and far clip 2000."""
    ob = T.make_camera(setup, name, scene); ob.data.clip_start = 0.05; ob.data.clip_end = 2000.0; ob.data.dof.use_dof = False
    return ob

def cam_from(loc, look_at, lens=22.0, roll=0.0):
    """Helper: the 22 mm camera setup from (position, look-at), D units."""
    d = dict(loc=tuple(loc), look_at=tuple(look_at), lens=lens)
    if roll: d['roll'] = roll
    return d

def D3(p): return tuple(round(c * U, 3) for c in p)

# ----------------------------------------------------------------------------- shots table + anchors (filled further down)
SHOTS = {}
def anchors(shot=None):
    loc = STATE['loc']; P = STATE['P']
    mm = STATE.get('marks_m', {})
    marks = {}
    for k, v in mm.items():
        marks[k] = [D3(p) for p in v] if (isinstance(v, list) and v and isinstance(v[0], (tuple, list))) else D3(v)
    A = dict(location=loc, light=STATE['light'], marks=marks, key_dir=tuple(Vector(P['key_dir']).normalized()), sun_elevation_deg=P['sun_elev'], heights=dict(HEIGHT),
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), unit_m=DM)
    A['cam'] = dict(CAMS.get(STATE.get('cam_name', 'a_wide'), dict(loc=(0, 0, 3), look_at=(0, 10, 1), lens=22)))
    return A
CAMS = {}

# ============================================================================= hooks (frames are scene frames at 30 fps; positions in D unless a name says metres)
def _key(idb, path, frame, interp='CONSTANT'): T._key(idb, path, frame, interp)
def _J(): return STATE['J']
BAR_R = LA.BAR_R

def bar_height_m(): return _J().get('h', (None,))[0] if isinstance(_J().get('h'), tuple) else _J().get('h')

def set_bar_height(h_m, frame=None, peg='both', interp='LINEAR'):
    """Crossbar height setter. h_m = top of the bar above the floor, in METRES (1.72 = A default, 2.24 = B default). peg = 'both' | 'L' | 'R' (one peg only: the bar tilts,
    shot 18: raise L, then R). frame=None sets it now; frame=N keys it (interp of the segment that starts at N: LINEAR, BEZIER or CONSTANT). A bar that was knocked off
    (bar_fall) is re-seated by this call: call bar_reset(frame) first for a clean jump cut."""
    J = _J(); hl, hr = J.get('hL', J['h0']), J.get('hR', J['h0'])
    if peg in ('both', 'L'): hl = float(h_m)
    if peg in ('both', 'R'): hr = float(h_m)
    J['hL'], J['hR'] = hl, hr; J['h'] = (hl + hr) / 2
    half = J['half']; Lb = J['bar_len']
    for e in J['peg']:
        z = (hl if e['sx'] < 0 else hr) - 2 * BAR_R - 0.0175; e.location = (J['xc'] + e['sx'] * (1 - 0.06 / half), J['y'], z)
        if frame is not None: _key(e, 'location', frame, interp)
    bar = J['bar']; bar.location = (J['xc'], J['y'], (hl + hr) / 2 - BAR_R); bar.rotation_euler = (0.0, -math.atan2(hr - hl, Lb), 0.0)
    if frame is not None: _key(bar, 'location', frame, interp); _key(bar, 'rotation_euler', frame, interp)

def bar_reset(frame=None):
    """Put a knocked-off bar back on its pegs at `frame` (a hard jump cut: the fallen state is held up to frame-1)."""
    J = _J(); bar = J['bar']
    if frame is not None:
        for p in ('location', 'rotation_euler'): bar.keyframe_insert(p, frame=frame - 1)
        for p in ('location', 'rotation_euler'): _key(bar, p, frame - 1, 'CONSTANT')
    set_bar_height(J['h'], frame, 'both', 'CONSTANT')

def bar_fall(start_frame, side='back', bounce=True, seed=0):
    """Animated knock-off. At start_frame the bar leaves its pegs and falls (gravity, 0.45 restitution, up to 3 bounces, a roll and a small yaw wobble) onto the landing
    surface (sawdust A 0.44 m / foam B 1.0 m) and settles. side = 'back' (knocked toward +y, into the pit), 'front' (-y, towards the run-up), 'left' | 'right' (that end drops first).
    Returns the frame where the bar is at rest. Keys are per frame (linear)."""
    J = _J(); bar = J['bar']; rrr = rnd(1000 + seed + int(start_frame)); hl, hr = J.get('hL', J['h0']), J.get('hR', J['h0'])
    z = (hl + hr) / 2 - BAR_R; x, y = J['xc'], J['y']; th = -math.atan2(hr - hl, J['bar_len']); yaw = 0.0; roll = 0.0
    vz = 0.5; vy = {'back': 0.9, 'front': -0.9}.get(side, 0.35); vx = rrr.uniform(-0.15, 0.15)
    w = {'left': -2.4, 'right': 2.4}.get(side, rrr.choice((-1, 1)) * 1.0); wyaw = rrr.uniform(-0.6, 0.6); wroll = vy * 2.0
    g = 9.81; Lb = J['bar_len']; ground = J['ground']; e = 0.45 if bounce else 0.0; fr0 = int(start_frame)
    for p in ('location', 'rotation_euler'): bar.keyframe_insert(p, frame=fr0)
    nb = 0; f = fr0; sub = 6; rest = False; maxf = fr0 + 70
    while f < maxf:
        f += 1
        for _ in range(sub):
            dt = 1.0 / (30 * sub)
            if rest: break
            vz -= g * dt; z += vz * dt; y += vy * dt; x += vx * dt; th += w * dt; yaw += wyaw * dt; roll += wroll * dt
            low = z - abs(math.sin(th)) * Lb / 2 - BAR_R
            if low <= ground and vz < 0:
                z += ground - low; vz = -vz * e; w *= 0.55; vy *= 0.6; vx *= 0.6; wroll *= 0.6; wyaw *= 0.5; nb += 1
                if abs(vz) < 0.45 or nb >= 3:
                    vz = 0.0; vy = vx = 0.0; w = -th * 8 if abs(th) > 0.02 else 0.0
                    th *= 0.5; z = ground + BAR_R + abs(math.sin(th)) * Lb / 2
                    if abs(th) < 0.03: th = 0.0; z = ground + BAR_R; rest = True
        bar.location = (x, y, z); bar.rotation_euler = (roll, th, yaw)
        for p in ('location', 'rotation_euler'): bar.keyframe_insert(p, frame=f)
        if rest: break
    for p in ('location', 'rotation_euler'): _key(bar, p, f, 'CONSTANT')
    return f

def _pulse(idb, path, frame, vals, interp='CONSTANT'):
    for k, v in enumerate(vals):
        setattr(idb, path, v) if False else None

def flash_bulb(frame, where=None, energy=2.0e4):
    """Camera flash bulb pulse at `frame` (a white-yellow point light + a glowing bulb, 3 frames: full at frame, 40 % at frame+1, off at frame+3). where = (x, y, z) in D
    (default: the press photographer mark, 1.6 D up). The light also pops the nearby set up in the house look."""
    st = STATE; M = st['M']
    if 'flash' not in st:
        ld = bpy.data.lights.new('flashbulb', 'POINT'); ld.color = (1.0, 0.95, 0.8); ld.energy = 0.0; ld.use_shadow = False; ld.shadow_soft_size = 0.2
        lo = bpy.data.objects.new('flashbulb', ld); st['LIGHTS'].objects.link(lo)
        bm = mat_emit_local('flashbulb_m', '#fffbe8', 0.0); mb = S.MB('flashbulb'); mb.ell(bm, (0, 0, 0), (0.07, 0.07, 0.07), (8, 6)); bo = L.adopt(mb.finish(), cast=False)[0]
        st['flash'] = (lo, bo, bm)
    lo, bo, bm = st['flash']; where = where or tuple(st['A']['marks']['photographer']) if st.get('A') else (0, 0, 2)
    if where is None: where = (0, 0, 2)
    wm = Vector(where) * DM
    lo.parent = L.root(); lo.location = wm + Vector((0, 0, 0.2)); bo.location = wm + Vector((0, 0, 0.2)); lo.keyframe_insert('location', frame=frame - 1); bo.keyframe_insert('location', frame=frame - 1)
    sock = bm.node_tree.nodes[[n for n in bm.node_tree.nodes if n.bl_idname == 'ShaderNodeEmission'][0].name].inputs['Strength']
    for fr, k in ((frame - 1, 0.0), (frame, 1.0), (frame + 1, 0.4), (frame + 3, 0.0)):
        lo.data.energy = energy * k; lo.data.keyframe_insert('energy', frame=fr); sock.default_value = 120.0 * k; sock.keyframe_insert('default_value', frame=fr)
    for idb in (lo.data, bm.node_tree):
        for fc in T._fcurves(idb):
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    for ob in (lo, bo): _key(ob, 'location', frame - 1, 'CONSTANT')

def mat_emit_local(name, hexcol, k):
    key = 'E|' + name
    if key in S.MATS: return S.MATS[key]
    return L.mat_emit(name, hexcol, k)

# ---- sawdust spray -----------------------------------------------------------
def _spray_group():
    ng = bpy.data.node_groups.get('S15_spray')
    if ng: return ng
    ng = bpy.data.node_groups.new('S15_spray', 'GeometryNodeTree'); I = ng.interface
    I.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); I.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes.new; Lk = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput')
    def A(nm, typ):
        a = N('GeometryNodeInputNamedAttribute'); a.data_type = typ; a.inputs['Name'].default_value = nm; return a.outputs['Attribute']
    def M_(op, a=None, b=None, c=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]
    def V_(op, a, b=None):
        n = N('ShaderNodeVectorMath'); n.operation = op; Lk(a, n.inputs[0])
        if b is not None:
            if op == 'SCALE':
                if isinstance(b, (int, float)): n.inputs['Scale'].default_value = b
                else: Lk(b, n.inputs['Scale'])
            else: Lk(b, n.inputs[1])
        return n.outputs[0] if op != 'SCALE' else n.outputs['Vector']
    tm = N('GeometryNodeInputSceneTime'); stv = N('ShaderNodeValue'); stv.name = 'start'; t = M_('DIVIDE', M_('SUBTRACT', tm.outputs['Frame'], stv.outputs[0]), 30.0)
    te = M_('MINIMUM', M_('MAXIMUM', t, 0.0), A('tl', 'FLOAT')); live = M_('GREATER_THAN', t, 0.0)
    pos = N('GeometryNodeInputPosition'); c = A('c', 'FLOAT_VECTOR'); v = A('v', 'FLOAT_VECTOR'); sp = A('sp', 'FLOAT_VECTOR')
    rot = N('ShaderNodeVectorRotate'); rot.rotation_type = 'EULER_XYZ'; Lk(pos.outputs[0], rot.inputs['Vector']); Lk(c, rot.inputs['Center']); Lk(V_('SCALE', sp, te), rot.inputs['Rotation'])
    rel = V_('SUBTRACT', rot.outputs['Vector'], c); relS = V_('SCALE', rel, live)
    mv = V_('SCALE', v, te); grav = N('ShaderNodeCombineXYZ'); Lk(M_('MULTIPLY', M_('MULTIPLY', te, te), -4.905), grav.inputs['Z'])
    newp = V_('ADD', V_('ADD', c, mv), V_('ADD', grav.outputs[0], relS))
    setp = N('GeometryNodeSetPosition'); Lk(gi.outputs[0], setp.inputs['Geometry']); Lk(newp, setp.inputs['Position']); Lk(setp.outputs[0], go.inputs[0])
    return ng

def sawdust_spray(frame, position, strength=1.0, seed=0, floor=None):
    """Sawdust / wood-chip spray burst at `frame` from `position` (x, y, z in D: z = the surface the chips come off; the landing floor defaults to that z). A ring-shaped CROWN
    of tan chips thrown outward and up, a central plume of faster flakes and fine specks, all falling back under gravity and tumbling; the bits that land stay as chips.
    No round blobs: every bit is a thin chip / splinter (box). strength scales speed and count (1 = a body landing; 0.5 = a bar bounce). One object per burst."""
    M = STATE['M']; rr = rnd(77 + seed * 13 + int(frame)); p = Vector(position) * DM; fz = 0.06 if floor is None else (floor * DM - p.z) + 0.06
    n_crown, n_plume, n_spec = int(46 * strength) + 6, int(26 * strength) + 4, int(46 * strength) + 6
    items = []
    for i in range(n_crown):
        az = 2 * math.pi * (i + rr.random() * 0.6) / n_crown; el = math.radians(rr.uniform(50, 76)); sp_ = rr.uniform(2.2, 3.9) * (0.5 + 0.5 * strength); ln = rr.uniform(0.07, 0.15)
        items.append((0.26 * math.cos(az), 0.26 * math.sin(az), 0.05, sp_ * math.cos(el) * math.cos(az), sp_ * math.cos(el) * math.sin(az), sp_ * math.sin(el), ln, 0))
    for i in range(n_plume):
        az = rr.random() * 6.28; el = math.radians(rr.uniform(72, 88)); sp_ = rr.uniform(3.4, 5.6) * (0.5 + 0.5 * strength); ln = rr.uniform(0.05, 0.11)
        items.append((0.1 * math.cos(az), 0.1 * math.sin(az), 0.08, sp_ * math.cos(el) * math.cos(az), sp_ * math.cos(el) * math.sin(az), sp_ * math.sin(el), ln, 1))
    for i in range(n_spec):
        az = rr.random() * 6.28; el = math.radians(rr.uniform(20, 85)); sp_ = rr.uniform(1.5, 5.0) * (0.5 + 0.5 * strength); ln = rr.uniform(0.025, 0.05); rd = rr.uniform(0, 0.4)
        items.append((rd * math.cos(az), rd * math.sin(az), 0.05, sp_ * math.cos(el) * math.cos(az), sp_ * math.cos(el) * math.sin(az), sp_ * math.sin(el), ln, 1))
    V = []; F = []; mi = []; C = []; Vv = []; Sp = []; Tl = []
    for (cx, cy, cz, vx, vy, vz, ln, kind) in items:
        a = rr.random() * 6.28; b = rr.random() * 6.28
        B, Fs = boxes_np([(cx, cy, cz)], [(ln, ln * rr.uniform(0.28, 0.45), ln * 0.12)], [a])
        # tilt the chip a little so it is not axis-aligned
        t_land = (vz + math.sqrt(max(vz * vz + 19.62 * (cz - fz), 0.0))) / 9.81
        o = len(V); V += B.tolist(); F += [[o + i for i in f] for f in Fs.tolist()]; mi += [rr.choice((0, 0, 1)) if kind == 0 else rr.choice((0, 1, 1))] * 6
        C += [(cx, cy, cz)] * 8; Vv += [(vx, vy, vz)] * 8; Sp += [(rr.uniform(-14, 14), rr.uniform(-14, 14), rr.uniform(-14, 14))] * 8; Tl += [t_land] * 8
    me = bpy.data.meshes.new('spray'); me.from_pydata(V, [], F); me.update()
    for nm, typ, arr in (('c', 'FLOAT_VECTOR', C), ('v', 'FLOAT_VECTOR', Vv), ('sp', 'FLOAT_VECTOR', Sp), ('tl', 'FLOAT', Tl)):
        at = me.attributes.new(nm, typ, 'POINT')
        if typ == 'FLOAT': at.data.foreach_set('value', np.array(arr, dtype=np.float32))
        else: at.data.foreach_set('vector', np.array(arr, dtype=np.float32).reshape(-1))
    me.materials.append(M['saw']); me.materials.append(M['chip'])
    me.polygons.foreach_set('material_index', np.array(mi, dtype=np.int32))
    ob = bpy.data.objects.new('spray_%d' % frame, me); STATE['SET'].objects.link(ob); ob.parent = L.root(); ob.location = p; L.T.no_bounce(ob); ob.visible_shadow = True
    ng = _spray_group().copy(); ng.nodes['start'].outputs[0].default_value = float(frame); md = ob.modifiers.new('spray', 'NODES'); md.node_group = ng
    return ob

def boxes_np(centres, sizes, yaws):
    import set15_b as LB
    V, F = LB.boxes(np.array(centres, dtype=float), np.array(sizes, dtype=float), np.array(yaws, dtype=float)); return V, F

# ---- crowd, torch, flags -----------------------------------------------------
def crowd(amp=0.03, hz=1.2, cheer=0.0, frame=None, interp='BEZIER'):
    """Crowd bob control (B): amp = hop height in METRES (0.006 hush .. 0.03 chatter .. 0.10 cheer), hz = bob frequency, cheer 0..1 = everybody stands up and throws the arms up.
    frame=N keys it (interp = the segment after N)."""
    c = STATE['crowd_ctl']; c.location = (amp, hz, cheer)
    if frame is not None: _key(c, 'location', frame, interp)
def crowd_mode(mode, frame=None, interp='BEZIER'):
    """'hush' (shots 24-30: breathing, 0.4 Hz), 'normal' (stands bobbing), 'tense' (tiny shivers), 'cheer' (shot 31: arms up, 3 Hz)."""
    a = dict(hush=(0.006, 0.4, 0.0), normal=(0.03, 1.2, 0.0), tense=(0.012, 0.7, 0.0), cheer=(0.11, 3.0, 1.0), groan=(0.02, 0.8, 0.0))[mode]; crowd(*a, frame=frame, interp=interp)
def torch_flicker(level=1.0, frame=None, interp='LINEAR'):
    """Cauldron flame size / flicker amplitude (1 = normal, 0 = nearly out, 1.4 = roaring). The flame flickers by itself through the frame number (drivers)."""
    c = STATE['flame_ctl']; c.location = (level, 0, 0)
    if frame is not None: _key(c, 'location', frame, interp)
def flag_wave(amp=0.32, hz=0.55, frame=None, interp='LINEAR'):
    """Rim flags: wave amplitude in metres (0 = limp, 0.32 default, 0.6 strong wind) and frequency."""
    c = STATE['flag_ctl']; c.location = (amp, hz, 0)
    if frame is not None: _key(c, 'location', frame, interp)
def stand_flashes(f0, f1, density=0.35, seed=0):
    """Flash bulbs popping in the stands between frames f0..f1 (each of the 60 bulbs flashes 2 frames at a random time, about density x 60 of them per second)."""
    rr = rnd(5 + seed); bl = STATE['stand_bulbs']
    for o in bl:
        o.hide_render = True; _key(o, 'hide_render', f0 - 1, 'CONSTANT')
        n = int(density * (f1 - f0) / 30.0 * 2.0 + 0.5)
        for _ in range(n):
            f = rr.randint(f0, f1 - 2); o.hide_render = False; _key(o, 'hide_render', f, 'CONSTANT'); o.hide_render = True; _key(o, 'hide_render', f + 2, 'CONSTANT')

# ---- light preset switch with a smooth blend ----------------------------------
def switch_light(to, start_frame, n_frames=12):
    """Blend the CURRENT light preset of this location to `to` (e.g. 'EVE' while built with 'TENSE', shot 30) over n_frames starting at start_frame: the sun (colour, energy,
    direction), the painted shade of every material, the crowd dimming, the sky ramp, hills and floodlight pools are all driven by the frame number (drivers, no keys).
    Call once per frame range. The toon term of the materials keeps the start preset's sun direction (a few degrees: invisible)."""
    P0 = STATE['P']; P1 = LIGHTS['%s_%s' % (STATE['loc'], to)]; f0 = start_frame; n = max(1, n_frames)
    def ex(a, b): return '%g+(%g-(%g))*(max(0,min(1,(frame-%g)/%g))**2*(3-2*max(0,min(1,(frame-%g)/%g))))' % (a, b, a, f0, n, f0, n)
    def drv(idb, path, idx, a, b):
        if abs(a - b) < 1e-9: return
        d = idb.driver_add(path, idx) if idx is not None else idb.driver_add(path); d.driver.type = 'SCRIPTED'; d.driver.expression = ex(a, b)
    for m in bpy.data.materials:
        if not m.get('lit') or m.node_tree is None: continue
        nt = m.node_tree; sm = m['sm']; sm0 = sm / (P0['crowd_k'] if m['crowd'] else 1.0); g0 = m['gain'] / (P0['crowd_k'] if m['crowd'] else 1.0)
        k0 = P0['crowd_k'] if m['crowd'] else 1.0; k1 = P1['crowd_k'] if m['crowd'] else 1.0
        n1 = nt.nodes.get('sh_mul'); n2 = nt.nodes.get('sh_tint'); n3 = nt.nodes.get('sh_lift'); n4 = nt.nodes.get('gain_num')
        if not (n1 and n2 and n3 and n4): continue
        for c in range(3):
            drv(nt, 'nodes["sh_mul"].inputs[7].default_value', c, P0['shade'][c] * sm0 * k0, P1['shade'][c] * sm0 * k1)
            drv(nt, 'nodes["sh_tint"].inputs[0].default_value', c, P0['shade_tint'][c] * P0['shade_mix'], P1['shade_tint'][c] * P1['shade_mix'])
            drv(nt, 'nodes["sh_lift"].inputs[1].default_value', c, P0['lift'][c], P1['lift'][c])
        drv(nt, 'nodes["gain_num"].inputs[2].default_value', None, g0 * k0, g0 * k1)
    sun = STATE['sun']; k0m = max(P0['key']); k1m = max(P1['key']); sd = sun.data
    for c in range(3): drv(sd, 'color', c, P0['key'][c] / k0m, P1['key'][c] / k1m)
    drv(sd, 'energy', None, math.pi * k0m, math.pi * k1m)
    e0 = (-Vector(P0['key_dir']).normalized()).to_track_quat('Z', 'Y').to_euler(); e1 = (-Vector(P1['key_dir']).normalized()).to_track_quat('Z', 'Y').to_euler()
    for c in range(3): drv(sun, 'rotation_euler', c, e0[c], ((e1[c] - e0[c] + math.pi) % (2 * math.pi)) - math.pi + e0[c])
    w = bpy.context.scene.world; wn = w.node_tree
    for nd in wn.nodes:
        if nd.bl_idname == 'ShaderNodeValToRGB' and len(P0['sky']) == len(P1['sky']):
            for i, ((p0, c0), (p1, c1)) in enumerate(zip(P0['sky'], P1['sky'])):
                a = L.hexl(c0); b = L.hexl(c1)
                for c in range(3): drv(wn, 'nodes["%s"].color_ramp.elements[%d].color' % (nd.name, i), c, a[c], b[c])
    for fl in STATE.get('flood_lights', []): drv(fl.data, 'energy', None, 3.2e6 * P0['floods'] / 4.0, 3.2e6 * P1['floods'] / 4.0)
    for m in bpy.data.materials:
        if m.name.startswith('E|hill') and m.node_tree:
            em = [x for x in m.node_tree.nodes if x.bl_idname == 'ShaderNodeEmission'][0]; li = int(m.name.split('hill')[1][0]); a = L.hexl(P0['hills'][li][3]); b = L.hexl(P1['hills'][li][3])
            for c in range(3): drv(m.node_tree, 'nodes["%s"].inputs[0].default_value' % em.name, c, a[c], b[c])
    STATE['P_to'] = to

def set_season(k, frame=None, interp='LINEAR'):
    """A: leaves 0 = fresh green .. 1 = autumn orange (shot 16 season change). frame=N keys it."""
    for m in bpy.data.materials:
        if m.node_tree and 'season' in m.node_tree.nodes:
            s = m.node_tree.nodes['season'].outputs[0]; s.default_value = float(k)
            if frame is not None:
                s.keyframe_insert('default_value', frame=frame)
                for fc in T._fcurves(m.node_tree):
                    for kp in fc.keyframe_points:
                        if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def clear_keys():
    """Drop every hook key (bar, pegs, crowd / flag / torch control, flash, bulbs, seasons); the drivers (torch flame, light blend) and the geometry-node waves stay."""
    for ob in list(bpy.data.objects):
        if ob.animation_data and ob.animation_data.action: ob.animation_data.action = None
    for ld in bpy.data.lights:
        if ld.animation_data and ld.animation_data.action: ld.animation_data.action = None
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data and m.node_tree.animation_data.action: m.node_tree.animation_data.action = None
    for o in STATE.get('stand_bulbs', []): o.hide_render = True
