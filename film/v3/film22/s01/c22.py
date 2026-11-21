"""c22.py -- helpers for film-22 team-1 takes (lodgings NIGHT). Copy of the film8/common.py idea for cast22 + set3d22.
Per take: shot.py imports this, defines CAMS/actors, calls C.main(SHOT, first_g, last_g, actors_fn, setup_fn)."""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SET = os.path.join(PROJ, 'v3', 'set3d22')
for p in (SET, os.path.join(PROJ, 'v3', 'cast22'), os.path.join(PROJ, 'v3', 'cast')):
    if p not in sys.path: sys.path.insert(0, p)
import bpy
from mathutils import Vector as V
import beck as B
import beck_hq as H

def g_of(t): return int(round((t + 0.10) * 30))
def ez(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def fl(g, a, b): return max(0.0, min(1.0, (g - a) / float(b - a)))

_live = []
CUR = [0]
TRACK = dict(mode='off', raw={}, sm={})

def clear_actors():
    for n in _live:
        o = bpy.data.objects.get(n)
        if o:
            me = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0 and isinstance(me, bpy.types.Mesh): bpy.data.meshes.remove(me)
    _live.clear()

def track(fn, *a, **k):
    """run fn(*a, **k) and remember every object it creates (removed by clear_actors)"""
    before = set(o.name for o in bpy.data.objects)
    r = fn(*a, **k)
    for o in bpy.data.objects:
        if o.name not in before: _live.append(o.name)
    return r

def configure(shot, cams, marks=None, state=None, animate=None, light=None):
    sh = B.ALL_SHOTS[shot]
    d = dict(sh, cam=cams, animate=animate or {}); d.pop('actors', None)
    if state is not None: d['state'] = state
    if light: d['light'] = light
    dict.__setitem__(B.ALL_SHOTS, shot, d)
    return B.ALL_SHOTS[shot]

def precompute_track(actors_fn, g_first, g_last, sigma=2.0):
    """pass 1: record where place_ray puts the card each frame, low-pass it (gaussian, sigma frames) so pose swaps glide instead of jumping (QA section L, no jitter); pass 2 uses it."""
    import numpy as np
    TRACK.update(mode='record', raw={}, sm={})
    for g in range(g_first, g_last + 1):
        CUR[0] = g; clear_actors(); track(actors_fn, g)
    clear_actors()
    gs = sorted(TRACK['raw'])
    if gs:
        a = np.array([[TRACK['raw'][g].x, TRACK['raw'][g].y, TRACK['raw'][g].z] for g in gs]); r = int(sigma * 3)
        w = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); w /= w.sum()
        pad = np.concatenate([np.repeat(a[:1], r, 0), a, np.repeat(a[-1:], r, 0)])
        sm = np.stack([np.convolve(pad[:, i], w, mode='valid') for i in range(3)], 1)
        TRACK['sm'] = {g: V(tuple(v)) for g, v in zip(gs, sm)}
    TRACK['mode'] = 'use'


def main(shot, g_first, g_last, actors_fn, quality='final', outdir=None, only=None, samples=None, scale=None, pre=None, track_smooth=True):
    """build the lodgings once and render frames g_first..g_last (film frames) -> outdir/g_%04d.png (skips existing)."""
    sh = B.ALL_SHOTS[shot]
    outdir = outdir or os.path.join(HERE, 'frames')
    os.makedirs(outdir, exist_ok=True)
    frames = only if only else list(range(g_first, g_last + 1))
    todo = [g for g in frames if not os.path.exists(os.path.join(outdir, 'g_%04d.png' % g))]
    if not todo: print('nothing to do'); return
    scene = B.build(sh['location'], sh.get('light'), shot, quality, todo[0])
    scene.render.threads = 2
    mark_mounted()
    if pre: pre()
    if samples: scene.cycles.samples = samples
    if scale: scene.render.resolution_percentage = scale
    t0 = time.time()
    for i, g in enumerate(todo):
        clear_actors(); CUR[0] = g
        B.set_frame_cam(shot, g)
        for k, fn in sh.get('animate', {}).items(): fn(g - sh['f0'], sh['f1'] - sh['f0'])
        track(actors_fn, g)
        out = os.path.join(outdir, 'g_%04d.png' % g)
        B.T.render(out + '.tmp.png', scene); os.replace(out + '.tmp.png', out)
        print(g, '%.1fs' % ((time.time() - t0) / (i + 1)), flush=True)


def place_ray(story, anchor, tip, cam, ycard, pose=None, rim='#8fb0ff', kmin=0.85, kmax=1.25, shadow=True, tilt=0.0, roll=0.0, mirror=False, dx=0.0):
    """Cast card standing on the floor at depth y=ycard whose `anchor` projects exactly onto the world point `tip` from the camera
    (the card sits on the camera->tip ray, scaled to fit the height); keeps him in FRONT of the board with his feet visible."""
    cam = V(cam); tip = V(tip)
    t = (ycard - cam.y) / (tip.y - cam.y); t = max(0.05, min(0.98, t)); P = cam + (tip - cam) * t
    yaw = math.degrees(math.atan2(cam.x - P.x, -(cam.y - P.y)))
    kw = dict(yaw_deg=yaw, shadow=False, pose=pose, rim=rim, tilt=tilt, roll=roll, mirror=mirror)
    ob = B.cast_card(story, (P.x, P.y, 0), **kw)
    az = ob['anc'][anchor][1]; k = max(kmin, min(kmax, P.z / az)) if az > 0.2 else 1.0
    if abs(k - 1.0) > 0.01:
        bpy.data.objects.remove(ob, do_unlink=True); ob = B.cast_card(story, (P.x, P.y, 0), scale=k, **kw)
    off = B._anc_off(ob, anchor)
    loc = V((P.x - off.x + dx, P.y - off.y, 0.0))
    g_ = CUR[0]
    if TRACK['mode'] == 'record': TRACK['raw'][g_] = loc.copy()
    elif TRACK['mode'] == 'use' and g_ in TRACK['sm']: loc = TRACK['sm'][g_].copy()
    ob.location = loc
    if shadow: B.card_shadow(ob)
    return ob


def fade_card(ob, a):
    """multiply a cast card's alpha by a (0..1): the card dissolves (used for Beck leaving the frame during the s01 swing)"""
    m = ob.data.materials[0]; nt = m.node_tree
    mix = [n for n in nt.nodes if n.type == 'MIX_SHADER'][0]; tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = float(a)
    nt.links.new(tex.outputs['Alpha'], mul.inputs[0]); nt.links.new(mul.outputs[0], mix.inputs['Fac'])


def ground(shot, g_first, g_last, actors_fn, md, pre=None, step=10):
    """QA_TEAM §K: build the scene once, place the actors of every `step`-th frame and run set3d-independent ground_check22 on it -> md (GROUND.md)."""
    sys.path.insert(0, os.path.join(PROJ, 'v3', 'tools')); import ground_check22 as GC
    sh = B.ALL_SHOTS[shot]
    scene = B.build(sh['location'], sh.get('light'), shot, 'preview', g_first)
    mark_mounted()
    if pre: pre()
    frames = list(range(g_first, g_last + 1, step)) + ([g_last] if (g_last - g_first) % step else [])
    allf = []
    for g in frames:
        clear_actors(); CUR[0] = g; B.set_frame_cam(shot, g)
        for k, fn in sh.get('animate', {}).items(): fn(g - sh['f0'], sh['f1'] - sh['f0'])
        track(actors_fn, g)
        allf += [(g, b, c) for (_a, b, c) in GC.check_frame(scene, scene.frame_current)]
    ok = not allf
    L = ['# GROUND.md (QA_TEAM section K ground_check, film22 fallback tool)', 'take %s, frames %d-%d step %d, tolerance 0.02' % (shot, g_first, g_last, step),
         'RESULT: %s (%d failures)' % ('PASS' if ok else 'FAIL', len(allf)), '', '| frame | object | problem |', '|---|---|---|']
    seen = {}
    for a, b, c in allf: seen.setdefault((b, c), []).append(a)
    L += ['| %s | %s | %s |' % (','.join(map(str, v[:6])), k[0], k[1]) for k, v in seen.items()]
    open(md, 'w').write('\n'.join(L) + '\n'); print('ground', 'PASS' if ok else 'FAIL', len(allf)); return ok, allf


MOUNTED = ('window_frame', 'old_map', 'old_map_img', 'cork', 'cork_img', 'shelf', 'wall_posters', 'pendant', 'coat_hook', 'pin_new', 'window_back', 'window_view')
def mark_mounted():
    """wall / cord mounted set items that were SEEN touching their wall or cord in the stills (frames, map, cork, shelf, posters, coat hook, pendant on its cord)"""
    for n in MOUNTED:
        o = bpy.data.objects.get(n)
        if o: o['mounted'] = True


def smooth_keys(cams, n, sigma=3.0, pad=24):
    """one key per frame 0..n (and 6+ handles) from the spline `cams`, gaussian-smoothed (sigma frames) so velocity/acceleration are continuous: no jitter, no kinks (QA §L)."""
    import numpy as np
    fr = list(range(-pad - 12, n + pad + 13))
    raw = []
    for f in fr:
        l, la, ln, ro = B.cam_eval(cams, f); raw.append([*l, *la, ln, ro])
    a = np.array(raw); r = int(sigma * 3); w = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); w /= w.sum()
    pad_a = np.concatenate([np.repeat(a[:1], r, 0), a, np.repeat(a[-1:], r, 0)])
    sm = np.stack([np.convolve(pad_a[:, i], w, mode='valid') for i in range(a.shape[1])], 1)
    out = []
    for f, v in zip(fr, sm):
        if -10 <= f <= n + 12: out.append((f, tuple(v[0:3]), tuple(v[3:6]), float(v[6]), float(v[7])))
    return out
