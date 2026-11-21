#!/usr/bin/env python3
"""c22.py -- helpers for the film-22 take scripts (team 4): driver around beck.py (set3d22) + cast22 animated cards.
Copied per take folder (no shared film22/common.py).  Import FIRST in a shot.py:  import c22 as C
  C.beck, C.U (beck_util), C.BU (beck_under), C.V
  C.g_of(t) / C.g_bound(t)      narration time -> film frame
  C.Idle(name, story, mark, deltas, rim, period)   a named card with N breathing variants (lean / head_roll sway); C.Idle.update(f)
  C.Variants(name, story, mark, variants:{key: pose-dict}, rim)  explicit pose variants (mouth / hands) switched per frame via C.U.set_pose
  C.Walker(...)                a cast22 crowd walker: nph walk-cycle cards, moved per frame with a contact shadow
  C.hide_near(pred)            hide crowd cards by predicate on the card position
  C.run(shot, cfg, argv)       CLI: probe/stills/final
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, 'set3d22'), os.path.join(V3, 'cast22'), os.path.join(V3, 'cast')):
    if p not in sys.path: sys.path.insert(0, p)
import beck                                   # noqa: E402
import beck_util as U                         # noqa: E402
import beck_under as BU                       # noqa: E402
import bpy                                    # noqa: E402
from beck import V                            # noqa: E402
import cast22                                 # noqa: E402

def g_of(t): return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ez(u): u = clamp(u); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u

STORY = cast22.STORY22

# ---------------------------------------------------------------- animated named cards
class Idle:
    """A named cast22 pose that never freezes: N variants (lean / head_roll / pitch sway), one shown per frame (smooth sine through the variants)."""
    def __init__(s, name, story, mark, rim, period=40, n=8, lean=2.0, roll=2.5, pitch=0.0, base_over=None, cast=None, extra_poses=None, phase=0.0, alt=None, alt_over=None, mirror=False):
        c, p = STORY[story] if isinstance(story, str) else story
        p = dict(p); p.update(base_over or {})
        s.has_alt = alt is not None
        s.name, s.n, s.period, s.phase = name, n, period, phase
        s.base_lean = p.get('lean', 0.0); s.base_roll = p.get('head_roll', 0.0); s.base_pitch = p.get('pitch', 0.0)
        poses = {}
        for k in range(n):
            a = math.sin(2 * math.pi * k / n)
            q = dict(p); q['lean'] = s.base_lean + lean * a; q['head_roll'] = s.base_roll + roll * a; q['pitch'] = s.base_pitch + pitch * a
            poses['v%d' % k] = (cast or c, q)
        if alt is not None:
            c2, p2 = STORY[alt] if isinstance(alt, str) else alt; p2 = dict(p2); p2.update(alt_over or {})
            for k in range(n):
                a = math.sin(2 * math.pi * k / n); q = dict(p2); q['lean'] = p2.get('lean', 0.0) + lean * a; q['head_roll'] = p2.get('head_roll', 0.0) + roll * a
                poses['b%d' % k] = (cast or c2, q)
        for k, v in (extra_poses or {}).items(): poses[k] = v
        main = poses.pop('v0')
        s.d = U.actor(name, main, mark, poses=poses, rim=rim, cast=None, mirror=mirror)
        s.override = None
    def update(s, f, alt=False):
        if s.override: U.set_pose(s.name, s.override); return
        k = int(((f / float(s.period) + s.phase) % 1.0) * s.n) % s.n
        if alt and s.has_alt: U.set_pose(s.name, 'b%d' % k)
        else: U.set_pose(s.name, 'main' if k == 0 else 'v%d' % k)

# ---------------------------------------------------------------- walkers (crowd, walk cycle)
class Walker:
    def __init__(s, name, i, rim, nph=8, mirror=False, scale=1.0):
        s.name, s.nph = name, nph
        s.cards = []
        for k in range(nph):
            cn, pn = cast22.crowd_member(i, 'pass_walk', phase=k / float(nph), mirror=mirror)
            ob = beck.cast_card((cn, pn), (0, 0, 0), face_to=None, yaw_deg=0.0, tilt=0.0, rim=rim, name='wk_%s_%d' % (name, k), scale=scale, shadow=(k == 0))
            ob.hide_render = True; ob.hide_viewport = True
            U.BILL.append((ob, 0.0)); s.cards.append(ob)
        s.shadow = bpy.data.objects.get('shadow_' + s.cards[0].name)
        s.cur = -1
    def at(s, x, y, z, ph):
        k = int(ph * s.nph) % s.nph
        for j, ob in enumerate(s.cards):
            vis = (j == k); ob.hide_render = not vis; ob.hide_viewport = not vis; ob.location = (x, y, z)
        s.place_shadow(x, y, z)
    def hide(s):
        for ob in s.cards: ob.hide_render = True
        if s.shadow is not None: s.shadow.hide_render = True
    def place_shadow(s, x, y, z):
        if s.shadow is None: return
        # the shadow part was built at the origin mark (0,0,0): move the object itself
        s.shadow.hide_render = False; s.shadow.location = (x, y, z)

def hide_actor(name):
    d = U.ACTORS[name]
    for ob in d['poses'].values(): ob.hide_render = True; ob.hide_viewport = True
    sh = bpy.data.objects.get('shadow_act_%s_main' % name)
    if sh: sh.hide_render = True
    d['hidden'] = True

def move_actor(name, world):
    """move a placed actor (all its pose cards + contact shadow) to world (x, y, z)."""
    d = U.ACTORS[name]; old = V(d['mark']); new = V(world); dv = new - old
    for ob in d['poses'].values(): ob.location = V(ob.location) + dv
    sh = bpy.data.objects.get('shadow_act_%s_main' % name)
    if sh: sh.location = V(sh.location) + dv
    d['mark'] = tuple(new)

def hide_cards(pred):
    """hide every cast card (crowd or named) whose mark satisfies pred(x, y, z).  Returns the number hidden."""
    n = 0
    for name, d in U.ACTORS.items():
        x, y, z = d['mark']
        if pred(x, y, z):
            for ob in d['poses'].values(): ob.hide_render = True; ob.hide_viewport = True
            sh = bpy.data.objects.get('shadow_act_%s_main' % name)
            if sh: sh.hide_render = True
            d['hidden'] = True; n += 1
    return n

_orig_set_pose = U.set_pose
def _set_pose(name, key):
    d = U.ACTORS[name]
    if d.get('hidden'): return
    _orig_set_pose(name, key)
U.set_pose = _set_pose

# ---------------------------------------------------------------- driver
def build(shot, cfg, quality='final', frame=None, samples=None, threads=2):
    sh = beck.ALL_SHOTS[shot]; sh.update(cfg)
    sc = beck.build(sh['location'], sh.get('light'), shot, quality, frame)
    sc.render.threads = threads
    if samples: sc.cycles.samples = samples
    return sc

def render_range(shot, g0, g1, outdir, quality='final', samples=None, step=1, tag='g'):
    os.makedirs(outdir, exist_ok=True); t0 = time.time(); n = 0
    for g in range(g0, g1 + 1, step):
        out = os.path.join(outdir, '%s_%04d.png' % (tag, g))
        if os.path.exists(out) and os.path.getsize(out) > 1000: continue
        beck.render_frame(shot, g, out, quality, samples); n += 1
        print('frame', g, '%.1fs' % (time.time() - t0), flush=True)
    return n

def run(shot, cfg, argv, hook_after_build=None):
    """argv: stills a,b,c outdir [q] | final a:b [samples] | draft a:b[:step]"""
    mode = argv[0]
    if mode == 'stills':
        frames = [int(x) for x in argv[1].split(',')]; out = argv[2]; q = argv[3] if len(argv) > 3 else 'preview'
        sc = build(shot, cfg, q, frames[0], threads=4)
        if hook_after_build: hook_after_build()
        os.makedirs(out, exist_ok=True)
        for g in frames: beck.render_frame(shot, g, os.path.join(out, '%s_%04d.png' % (shot, g)), q)
    else:
        a = argv[1].split(':'); g0, g1 = int(a[0]), int(a[1]); step = int(a[2]) if len(a) > 2 else 1
        q = 'preview' if mode == 'draft' else 'final'
        samples = int(argv[2]) if (mode == 'final' and len(argv) > 2) else None
        sc = build(shot, cfg, q, g0, samples=samples, threads=2)
        if hook_after_build: hook_after_build()
        out = os.path.join(HERE, 'work', 'draft' if mode == 'draft' else 'frames')
        render_range(shot, g0, g1, out, q, samples, step)

def proj(pt):
    """(u, v) of a world point in the current camera, u 0..1 left->right, v 0..1 top->bottom (frame 720x1280); None if behind the camera."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; bpy.context.view_layer.update()
    r = world_to_camera_view(sc, sc.camera, V(pt))
    if r.z <= 0: return None
    return (round(r.x, 3), round(1.0 - r.y, 3))

def bench_new(mb, x, y0, y1, back, C_):
    """slatted wooden bench (seat + back slats, cast-iron end frames), brown wood."""
    wood = C_('#b06a2a', 1.0, 1.5); iron = C_('#1d1a45', 1.0, 1.2)
    for k in range(4):
        a = x - 0.9 + k * 0.46; mb.box((a, y0, 1.42), (a + 0.40, y1, 1.58), wood)
    for k in range(3):
        mb.box((x + back * 0.72 - 0.06, y0, 1.85 + k * 0.30), (x + back * 0.72 + 0.06, y1, 2.05 + k * 0.30), wood)
    for yy in (y0 + 0.25, y1 - 0.35):
        mb.box((x - 0.85, yy, 0.0), (x - 0.7, yy + 0.12, 1.42), iron); mb.box((x + 0.7, yy, 0.0), (x + 0.85, yy + 0.12, 1.42), iron)
        mb.box((x + back * 0.72 - 0.07, yy, 1.42), (x + back * 0.72 + 0.07, yy + 0.12, 2.65), iron)
