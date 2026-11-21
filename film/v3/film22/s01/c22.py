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

def main(shot, g_first, g_last, actors_fn, quality='final', outdir=None, only=None, samples=None, scale=None):
    """build the lodgings once and render frames g_first..g_last (film frames) -> outdir/g_%04d.png (skips existing)."""
    sh = B.ALL_SHOTS[shot]
    outdir = outdir or os.path.join(HERE, 'frames')
    os.makedirs(outdir, exist_ok=True)
    frames = only if only else list(range(g_first, g_last + 1))
    todo = [g for g in frames if not os.path.exists(os.path.join(outdir, 'g_%04d.png' % g))]
    if not todo: print('nothing to do'); return
    scene = B.build(sh['location'], sh.get('light'), shot, quality, todo[0])
    scene.render.threads = 2
    if samples: scene.cycles.samples = samples
    if scale: scene.render.resolution_percentage = scale
    t0 = time.time()
    for i, g in enumerate(todo):
        clear_actors()
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
    ob.location = V((P.x - off.x + dx, P.y - off.y, 0.0))
    if shadow: B.card_shadow(ob)
    return ob


def fade_card(ob, a):
    """multiply a cast card's alpha by a (0..1): the card dissolves (used for Beck leaving the frame during the s01 swing)"""
    m = ob.data.materials[0]; nt = m.node_tree
    mix = [n for n in nt.nodes if n.type == 'MIX_SHADER'][0]; tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = float(a)
    nt.links.new(tex.outputs['Alpha'], mul.inputs[0]); nt.links.new(mul.outputs[0], mix.inputs['Fac'])
