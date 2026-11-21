#!/usr/bin/env python3
"""c22.py -- film-22 take helper (copy of the film8 common.py idea, on cast22 + set3d22).  Import FIRST in a take's shot.py:

    import c22 as C          # puts set3d22 on sys.path, imports beck (bpy), beck_under, beck_map
Provides: build/render driver for one take (probe/stills/final), emission & light scalers, resumable frame loop.
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # .../film
SET = os.path.join(PROJ, 'v3', 'set3d22')
for p in (SET, os.path.join(PROJ, 'v3', 'cast22'), os.path.join(PROJ, 'v3', 'cast')):
    if p not in sys.path: sys.path.insert(0, p)
import beck as B                                   # noqa: E402
import bpy                                         # noqa: E402
from mathutils import Vector                       # noqa: E402
V = Vector
import beck_util as U                              # noqa: E402
ALL = B.ALL_SHOTS

def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ez(u):
    u = clamp(u); return u * u * (3 - 2 * u)

def scale_emission(matname_sub, k):
    """multiply every Emission-node strength of the materials whose name contains matname_sub (and node 'Strength' value)"""
    n = 0
    for m in bpy.data.materials:
        if matname_sub in m.name and m.node_tree:
            for nd in m.node_tree.nodes:
                if nd.type == 'EMISSION':
                    nd.inputs['Strength'].default_value *= k; n += 1
    return n

def scale_lights(prefix, k):
    for o in bpy.context.scene.objects:
        if o.type == 'LIGHT' and o.name.startswith(prefix): o.data.energy *= k

def hide(*names):
    for o in bpy.context.scene.objects:
        if o.name in names or any(o.name.startswith(n + '*') for n in names if False): o.hide_render = True

def hide_prefix(prefix):
    for o in bpy.context.scene.objects:
        if o.name.startswith(prefix): o.hide_render = True; o.hide_viewport = True

def obj(name): return bpy.data.objects.get(name)

def grade_stats(path):
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(path).convert('RGB'), 'float32') / 255
    mx = a.max(2); mn = a.min(2); sat = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0)
    luma = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) * 255
    return sat.mean(), luma.mean()

def drive(shot, cam, location, light, animate, post_build, args, f0, f1, state=None, extra_shot=None):
    """args: [mode, a:b[:step], out, scale?, samples?]   mode = stills | final | probe.
    cam = key list; animate(local_f, n); post_build(): runtime set changes after the location is built."""
    sh = ALL[shot]; sh['cam'] = cam; sh['f0'] = f0; sh['f1'] = f1
    if state is not None: sh['state'] = state
    sh['animate'] = {'take': animate}
    if extra_shot: sh.update(extra_shot)
    mode = args[0]; a, b = [int(x) for x in args[1].split(':')[:2]]
    step = int(args[1].split(':')[2]) if args[1].count(':') == 2 else 1
    out = args[2]; os.makedirs(out, exist_ok=True)
    q = 'final' if mode == 'final' else 'preview'
    B.build(location, light, shot, q, a)
    if post_build: post_build()
    sc = bpy.context.scene
    if mode == 'ground':
        sys.path.insert(0, os.path.join(PROJ, 'v3', 'tools')); import ground_check22 as G
        allf = []
        for g in range(a, b + 1, 10):
            B.set_frame_cam(shot, g); animate(g - f0, f1 - f0); allf += G.check_frame(sc, g)
        L = ['# GROUND.md (QA_TEAM section K, ground_check22, animate applied per frame)', 'frames %d-%d step 10' % (a, b), 'RESULT: %s (%d failures)' % ('PASS' if not allf else 'FAIL', len(allf)), '', '| frame | object | problem |', '|---|---|---|']
        L += ['| %d | %s | %s |' % x for x in allf[:400]]
        open(os.path.join(out, 'GROUND.md'), 'w').write('\n'.join(L) + '\n'); print('ground', 'PASS' if not allf else 'FAIL %d' % len(allf)); return
    if mode == 'stills':
        sc.render.resolution_percentage = int(args[3]) if len(args) > 3 else 50
        sc.cycles.samples = int(args[4]) if len(args) > 4 else 6
    else:
        if len(args) > 3: sc.cycles.samples = int(args[3])
        sc.cycles.use_denoising = True
    sc.render.threads = int(os.environ.get('THREADS', '2'))
    t0 = time.time(); n = 0
    for g in range(a, b + 1, step):
        p = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(p): continue
        B.render_frame(shot, g, p, q); n += 1
        print('frame', g, '%.1fs' % (time.time() - t0), flush=True)
    print('done', n, 'frames, %.1f s/frame' % ((time.time() - t0) / max(1, n)))

LAST_MIX = []
def tint_emission(matname_sub, rgb, fac=1.0):
    """multiply the Emission colour input of matching materials by rgb (inserts a MixRGB MULTIPLY node)."""
    n = 0; LAST_MIX.clear()
    for m in bpy.data.materials:
        if matname_sub in m.name and m.node_tree:
            nt = m.node_tree
            for nd in list(nt.nodes):
                if nd.type == 'EMISSION':
                    inp = nd.inputs['Color']
                    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = fac
                    mx.inputs[7].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
                    if inp.links:
                        src = inp.links[0].from_socket; nt.links.new(src, mx.inputs[6])
                    else:
                        mx.inputs[6].default_value = tuple(inp.default_value)
                    nt.links.new(mx.outputs[2], inp); n += 1; LAST_MIX.append((m, nd, mx))
    return n

def set_emission_color(matname_sub, rgb, strength=None):
    for m in bpy.data.materials:
        if matname_sub in m.name and m.node_tree:
            nt = m.node_tree
            for nd in nt.nodes:
                if nd.type == 'EMISSION':
                    for l in list(nd.inputs['Color'].links): nt.links.remove(l)
                    nd.inputs['Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
                    if strength is not None: nd.inputs['Strength'].default_value = strength

def mount(names=(), prefixes=('shadow_',)):
    """mark objects as touching their wall/floor (seen in the frames) for ground_check22"""
    for o in bpy.context.scene.objects:
        if o.name in names or any(o.name.startswith(p) for p in prefixes): o['mounted'] = True

def move_card(name, x, y, z):
    """move an actor card AND its contact shadow (the shadow quad is built at the mark, so it is offset by the delta)"""
    d = U.ACTORS[name]; m = d['mark']
    for ob in d['poses'].values(): ob.location = (x, y, z)
    for o in bpy.data.objects:
        if o.name.startswith('shadow_act_%s_main' % name): o.location = (x - m[0], y - m[1], z - m[2])
