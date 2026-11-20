#!/usr/bin/env python3
"""shot.py -- film 17 take s11: shots 27-28 (reveal payoff), g 1515..1694 + 6 handle frames each side (first_g 1509, last 1700).
  id 27  g 1509..1578  reveal / card_hero room, Bertillon (foreground left) holds the Dupont card beside Dupont's face; his profile turns to the card;
                       the five number rows glow one by one.  Drift (slide + push) with a reframe snap at g 1544.
  id 28  g 1579..1700  measure room, two-shot: Dupont seated in the chair, Bertillon turns the card (bottle panel glows) toward him, Dupont goes wide-eyed,
                       the inspector (arms crossed, smirk) -> jaw drops (shocked, mouth CLOSED).  Push-in, snap (18 f) to the inspector on "ขวดเปล่า" (~55.1 s).
  python3 shot.py <27|28> stills a:b[:step] out_dir [mode draft|final] [samples]
  python3 shot.py <27|28> final a:b[:step] [mode] [samples]
"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import bpy, K, cast17, actors, sprites, puppet, Vector
SHOT = int(sys.argv[1]); CMD = sys.argv[2]
G_FIRST, G_CUT, G_LAST = 1509, 1579, 1700
RANGES = {27: (G_FIRST, G_CUT - 1), 28: (G_CUT, G_LAST)}
BF0 = 1499
def bf(g): return g - BF0
THREADS = int(os.environ.get("THREADS", "2"))
TMP = os.path.join(HERE, "work")
SHAKE = float(os.environ.get('SHAKE', '0.016'))
G_BOTTLE = C.g_of(55.10)     # 1656 "ขวดเปล่า"
def lerp(a, b, t): return a + (b - a) * t
def u_(g, a, b): return C.smooth((g - a) / float(b - a))

# ---------------------------------------------------------------- cameras
if SHOT == 27:
    CAM = C.CamPath([(1509, (1.15, 3.60, 1.58), (0.30, 1.72, 1.34), 'drift'), (1528, (0.85, 3.35, 1.55), (0.20, 1.72, 1.33), 'snap'),
                     (1542, (0.35, 3.35, 1.50), (0.05, 1.72, 1.35), 'drift'), (1556, (0.34, 3.20, 1.50), (0.10, 1.72, 1.35), 'snap'),
                     (1570, (0.70, 2.95, 1.52), (0.24, 1.72, 1.34), 'drift'), (1584, (0.55, 2.80, 1.50), (0.20, 1.72, 1.34), 'drift')], shake=SHAKE)
else:
    CAM = C.CamPath([(1579, (2.10, 0.50, 1.50), (1.30, 2.55, 1.28), 'drift'), (1600, (1.95, 0.70, 1.50), (1.20, 2.55, 1.30), 'snap'),
                     (1614, (1.75, 0.95, 1.48), (1.25, 2.50, 1.30), 'drift'), (1636, (1.90, 0.65, 1.50), (1.10, 2.50, 1.29), 'snap'),
                     (1650, (1.80, 0.80, 1.50), (1.05, 2.50, 1.29), 'snap'), (1668, (1.00, 0.85, 1.46), (0.10, 2.1, 1.30), 'drift'),
                     (1700, (0.75, 1.05, 1.45), (0.0, 2.1, 1.32), 'drift')], shake=SHAKE)

# ---------------------------------------------------------------- build
LOC = ('reveal', 'card_hero') if SHOT == 27 else ('measure', 'measure_chair')
A = K.build(preset=LOC[1]); STATE = K.STATE
bpy.context.scene.render.use_persistent_data = False
cam = bpy.context.scene.camera; cam.data.clip_start = 0.02
if SHOT == 27:
    for ob in STATE['anim']['hero']['objs'] + [STATE['anim']['hero']['root']]: ob.hide_render = True    # the in-box card is replaced by the held one
K.clear_keys()
if SHOT == 28:     # director R3: a loose pair of cream rods floats in the measure room at (1.54-1.79, 1.63-1.79, 0.97-1.14): delete that geometry from the merged mesh
    import bmesh
    _o = bpy.data.objects['measure_cream']; _bm = bmesh.new(); _bm.from_mesh(_o.data); _M = _o.matrix_world
    _bm.verts.ensure_lookup_table()
    _kill = [v for v in _bm.verts if 1.3 < (_M @ v.co).x < 2.1 and 1.3 < (_M @ v.co).y < 2.0 and 0.85 < (_M @ v.co).z < 1.3]
    bmesh.ops.delete(_bm, geom=_kill, context='VERTS'); _bm.to_mesh(_o.data); _bm.free()
for o in bpy.data.objects:      # director fix: the additive light shafts wash over the cast cards
    if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])): o.hide_render = True

def make_actor(name, cast):
    a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(TMP, "sprites"), contact=True); a.head_flip = True; return a

def scale_of(cast): return K.CAST_H[cast] / K.CAST_HD[cast]

ACT = {}
SEATLEGS = dict(preset='narrow', crouch=0.45, knee_r=0.0, knee_l=0.0)
def put(key, cast, xy, seated=None, mirror=False, pose0=None):
    a = make_actor(key, cast); ACT[key] = a
    sc = scale_of(cast)
    if seated:
        fx, fy = sprites.feet_of(cast, pose0 or {}); z = K.HEAD_Z[seated] - sc * fy
    else: z = 0.0
    a._place = (xy[0], xy[1], z); a._sc = sc; return a

# the held card (3D, Dupont art) + glow bars
held = K.card_plane('held', (0, 0, 0), (0.30, 0.20), key='card_bertillon', ink_t=0.0)
def px2c(px, py, W=768, H=512): return ((px / W - 0.5) * 0.30, (0.5 - py / H) * 0.20)
ROWS = []; TICKS = []
for i in range(5):
    cx, cz = px2c(384, 348 + 32 * i); ROWS.append(C.emissive_bar('row%d' % i, held, 0.281, 0.0078, (cx, cz), strength=2.2, alpha=0.50))
    tx_, tz_ = px2c(748, 348 + 32 * i); TICKS.append(C.tick_bars('tick%d' % i, held, (-0.112, cz), size=0.028))
cx, cz = px2c(335, 218); PROF = C.emissive_bar('prof', held, 0.0773, 0.078, (cx, cz), color=(1.0, 0.9, 0.5), strength=2.0, alpha=0.30)
BOTTLE = C.image_quad('bottle', held, 0.21, 0.0826, (-0.040, 0.0925), C.bottle_png(os.path.join(TMP, 'bottle.png')), strength=1.25)
def glow(bar, f, on, a=None):
    ob, mx = bar; ob.hide_render = not on; ob.keyframe_insert('hide_render', frame=f)
    if on and a is not None:
        mx.inputs[0].default_value = a; mx.inputs[0].keyframe_insert('default_value', frame=f)

# ---------------------------------------------------------------- poses
def idle(g, k=0.0): return dict(head_roll=1.8 * math.sin(g * 0.13 + k), lean=1.2 * math.sin(g * 0.09 + k))
def blink(g, k): return cast17.blink_at(g + k, 83)

def pose_bert(g):
    cast, p = cast17.STORY17['bertillon_holding_card']; p = dict(p); p.pop('prop_r', None)
    p['seat17'] = None
    r = u_(g, G_FIRST, G_FIRST + 8) if SHOT == 27 else 1.0
    p['arm_r'] = dict(p['arm_r'], hand=(0.66, lerp(0.30, 0.04, r)))
    if SHOT == 28:    # turns the card toward dupont: mirrored, hand out to the screen-left
        p['mirror'] = True; t = u_(g, 1579, 1596); p['arm_r'] = dict(p['arm_r'], hand=(lerp(0.40, 0.66, t), lerp(0.30, 0.10, t)))
        p['yaw'] = 0.35
    p.update(idle(g, 0.5)); p['blink'] = blink(g, 11); return p

def pose_dup(g):
    if SHOT == 27:
        cast, p = cast17.STORY17['dupont_innocent']; p = dict(p); p['yaw'] = lerp(0.0, -0.65, u_(g, 1520, 1534))
        p['expr'] = 'worried'; p.update(idle(g, 1.7)); p['blink'] = blink(g, 29); return p
    cast, p0 = cast17.STORY17['dupont_sweating']; cast, p1 = cast17.STORY17['dupont_caught']
    p0 = dict(p0, seat17=None); p1 = dict(p1, seat17=None)
    p1['arm_r'] = dict(p1['arm_r'], hand=(0.52, 0.80), bend=0.55); p1['arm_l'] = dict(p1['arm_l'], hand=(-0.52, 0.80), bend=0.55)   # hands up at the chest, not a T-pose
    t = u_(g, 1605, 1609)                                    # eyes go wide over ~4 frames
    p = dict(puppet.lerp_pose('dupont', p0, p1, t)) if 0 < t < 1 else dict(p0 if t <= 0 else p1)
    if t >= 1: p['head_dy'] = -0.03 * u_(g, 1609, 1615)
    p['legs'] = SEATLEGS; p['seat17'] = None; p['yaw'] = -0.1
    if g < 1614: p['fx'] = ['sweat']; p['sweat'] = 1.0 - 0.7 * u_(g, 1607, 1614)
    else: p.pop('fx', None)
    p['head_roll'] = 2.0 * math.sin(g * 0.15) if g < 1607 else 1.0 * math.sin(g * 0.3)
    p['blink'] = blink(g, 29) if g < 1604 else 0; return p

def pose_ins(g):
    if g < 1607:
        cast, p = cast17.STORY17['inspector_arms_crossed']; p = dict(p); p['expr'] = 'smirk'
    else:
        cast, p = cast17.STORY17['inspector_shocked']; p = dict(p); p['mouth'] = 'flat'; p['head_dy'] = 0.05 * u_(g, 1614, 1622)
        p['fx'] = ['sweat'] if g > 1650 else []
    p['seat17'] = None; p['yaw'] = 0.2; p.update(idle(g, 2.9)); p['blink'] = blink(g, 3) if g < 1604 else 0; return p

if SHOT == 27:
    bert = put('bert', 'bertillon', (0.68, 1.70)); dup = put('dup', 'dupont', (-0.30, 1.75))
    ACTORS = [bert, dup]
else:
    dup = put('dup', 'dupont', (0.68, 2.20), seated='chair', pose0=dict(cast17.STORY17['dupont_sweating'][1], legs=SEATLEGS))
    ins = put('ins', 'inspector17', (0.12, 2.10)); bert = put('bert', 'bertillon', (1.62, 2.68))
    ACTORS = [dup, ins, bert]
POSE = {'bert': pose_bert, 'dup': pose_dup, 'ins': pose_ins}

def card_rz(g, hand_world):
    d = Vector((cam.location.x - hand_world.x, cam.location.y - hand_world.y, 0)); d.normalize()
    if SHOT == 28:
        t = u_(g, 1579, 1596); th = math.radians(lerp(0, 38, t)); d = Vector((d.x * math.cos(th) - d.y * math.sin(th), d.x * math.sin(th) + d.y * math.cos(th), 0))
    return math.atan2(-d.x, d.y)

def key_cam_frame(g):
    loc, look = CAM.at(g); C.key_cam(cam, bf(g), loc, look)

def SILENT(p, name, g):
    p = cast17.silent(p)
    if name == 'ins' and g >= 1607: p['mouth'] = ('open', 0.09, 0.11)        # static small dark oval (director option 4), never animated
    return p

RIGHT28 = Vector((0.82, 0.57, 0.0))            # screen-right in the measure room (camera looks toward +y, -x)
def card_target(g, f):
    """world centre of the held card from Dupont's head."""
    dh = actors.local_to_world(dup, dup.anch[f]['head'], f, camera=cam)
    if SHOT == 27: return Vector((dh.x + 0.56, dh.y, dh.z - 0.03))
    return Vector((dh.x, dh.y, dh.z)) + RIGHT28 * 0.62 + Vector((0, 0, 0.14))

def pose_all(gs):
    for g in gs: key_cam_frame(g)
    for g in gs:
        f = bf(g); bpy.context.scene.frame_set(f)
        for a in ACTORS:
            x, y, z = a._place; a.place(f, (x, y, z), scale=a._sc)
    fr = [bf(g) for g in gs]
    def sprites_of(acts):
        for a in acts:
            a.anch = {}
            for f, r in zip(fr, a.render_sprites(320, frames=fr)):
                a.anch[f] = r['anchors']
                if r.get('clipped'): print("WARNING clipped", a.name, f, flush=True)
    others = [a for a in ACTORS if a is not bert]
    for g in gs:
        f = bf(g); bpy.context.scene.frame_set(f)
        for a in others: a.pose(f, SILENT(POSE[a.name](g), a.name, g), camera=cam)
    sprites_of(others)
    CT = {}
    for g in gs:
        f = bf(g); bpy.context.scene.frame_set(f)
        C_ = card_target(g, f); CT[g] = C_
        sc = 1.6 if SHOT == 27 else 2.7
        if SHOT == 27: hp = C_ + Vector((0.235, 0, -0.03))
        else: hp = C_ + RIGHT28 * 0.22 + Vector((0, 0, -0.27))
        lx, ly = actors.world_to_local(bert, cam, tuple(hp), f)
        p = SILENT(POSE['bert'](g), 'bert', g)
        bert.pose(f, p, hands={'r': {'hand': (lx, ly), 'bend': (0.5 if SHOT == 28 else p['arm_r'].get('bend', -0.6)), 'shape': 'fist'}}, camera=cam)
    sprites_of([bert])
    for g in gs:
        f = bf(g); bpy.context.scene.frame_set(f)
        C_ = CT[g]; scl = 1.6 if SHOT == 27 else 2.7
        if SHOT == 27:
            rz = math.atan2(-(cam.location.x - C_.x), (cam.location.y - C_.y)) * 1.0
        else:
            d = Vector((cam.location.x - C_.x, cam.location.y - C_.y, 0)); d.normalize(); t = u_(g, 1579, 1596)
            th = math.radians(lerp(0, 36, t)); d = Vector((d.x * math.cos(th) - d.y * math.sin(th), d.x * math.sin(th) + d.y * math.cos(th), 0)); rz = math.atan2(-d.x, d.y)
        kk = 1.0 + (0.32 / max(0.5, (C_ - cam.location).length) if SHOT == 28 else 0.0)
        scl *= kk; C_ = cam.location + (C_ - cam.location) * kk
        held.location = C_ + Vector((0, 0, 0.012 * math.sin(g * 0.3))); held.rotation_euler = (math.radians(2 * math.sin(g * 0.2)), 0, rz + math.radians(1.5 * math.sin(g * 0.17)))
        held.scale = (scl,) * 3
        held.keyframe_insert('location', frame=f); held.keyframe_insert('rotation_euler', frame=f); held.keyframe_insert('scale', frame=f)
        for i, bar in enumerate(ROWS):
            t0 = 1527 + 10 * i; on = SHOT == 27 and g >= t0
            glow(bar, f, on, 0.50 + (0.30 * max(0.0, 1 - (g - t0) / 6.0) if on else 0))
            for tb in TICKS[i]: glow(tb, f, SHOT == 27 and g >= t0 + 3, 0.95)
        glow(PROF, f, SHOT == 27 and 1534 <= g <= 1552, 0.35 + 0.2 * math.sin(g * 0.6))
        ob, em = BOTTLE; on = SHOT == 28 and g >= 1588
        ob.hide_render = not on; ob.keyframe_insert('hide_render', frame=f)
        if on: em.inputs['Strength'].default_value = 0.6 + 0.7 * u_(g, 1588, 1596) + 0.15 * math.sin(g * 0.5); em.inputs['Strength'].keyframe_insert('default_value', frame=f)
        K.set_flicker(1.0, frame=f); K.set_dust(0.5, frame=f)
        if SHOT == 28: K.set_pendulum(frame=f); K.set_smoke(1.0, frame=f)

def report(g):
    f = bf(g); bpy.context.scene.frame_set(f); out = {'g': g, 'cam': [round(v, 3) for v in cam.location]}
    for a in ACTORS:
        hx, hy = a.anch[f]['head']; c = actors.local_to_screen(a, cam, (hx, hy), f); l = actors.local_to_screen(a, cam, (hx - 0.5, hy), f)
        out[a.name] = dict(x=round(c[0]), y=round(c[1]), w=round(math.hypot(c[0] - l[0], c[1] - l[1])))
    return out

def render(g, path, mode, samples):
    f = bf(g); bpy.context.scene.frame_set(f); actors.sync_all(camera=cam)
    return C.render_frame(path, mode, samples, THREADS)

if __name__ == '__main__':
    gs = [g for g in C.parse(sys.argv[3]) if RANGES[SHOT][0] <= g <= RANGES[SHOT][1]]
    if CMD == 'stills':
        out = sys.argv[4]; mode = sys.argv[5] if len(sys.argv) > 5 else 'draft'; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        os.makedirs(out, exist_ok=True); pose_all(gs)
        for g in gs:
            print(json.dumps(report(g)), flush=True); dt = render(g, os.path.join(out, 's%d_g%04d.png' % (SHOT, g)), mode, samples); print('g', g, '%.1fs' % dt, flush=True)
    elif CMD == 'final':
        mode = sys.argv[4] if len(sys.argv) > 4 else 'final'; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 32
        out = os.path.join(HERE, 'raw_' + mode); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, 'g_%04d.png' % g))]
        pose_all(gs)
        for g in todo:
            p = os.path.join(out, 'g_%04d.png' % g); dt = render(g, p + '.tmp.png', mode, samples); os.replace(p + '.tmp.png', p)
            json.dump(report(g), open(p[:-4] + '.json', 'w')); print('g', g, '%.1fs' % dt, flush=True)
