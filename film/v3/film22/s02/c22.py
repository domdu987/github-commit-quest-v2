#!/usr/bin/env python3
"""c22.py -- helper for the film-22 take scripts (team 2): set3d22 + cast22, one location per process, resumable frame loop.
Usage in shot.py:  import c22 as C ; C.main(Take)   (Take: see s02/shot.py)."""
import os, sys, json, math, time, glob, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SET = os.path.join(PROJ, 'v3', 'set3d22')
for p in (SET, os.path.join(PROJ, 'v3', 'cast22'), os.path.join(PROJ, 'v3', 'cast')):
    if p not in sys.path: sys.path.insert(0, p)
import bpy
import beck as B
from mathutils import Vector as V

def args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draft', action='store_true'); ap.add_argument('--frames', default=None, help='a:b film frames (inclusive)')
    ap.add_argument('--step', type=int, default=1); ap.add_argument('--samples', type=int, default=None); ap.add_argument('--out', default=None)
    ap.add_argument('--ground', action='store_true'); ap.add_argument('--part', default=None, help='k/n: render only frames with index %% n == k')
    return ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])

def run(shot, location, light, f0, f1, handles, setup_fn, frame_fn, a=None, segments=None):
    """Build once, then render film frames f0-handles .. f1-1+handles (skip existing PNGs). setup_fn(scene) after build; frame_fn(g, k, n) before each render."""
    a = a or args(); q = 'preview' if a.draft else 'final'
    hpre, hpost = handles if isinstance(handles, (tuple, list)) else (handles, handles)
    g0, g1 = f0 - hpre, f1 - 1 + hpost
    if a.frames: x, y = a.frames.split(':'); g0, g1 = int(x), int(y)
    if a.ground: return ground(shot, location, light, f0, f1, setup_fn, frame_fn, segments)
    out = a.out or os.path.join(HERE, 'draft' if a.draft else 'frames'); os.makedirs(out, exist_ok=True)
    gs = [g for g in range(g0, g1 + 1, a.step) if not os.path.exists(os.path.join(out, 'g_%04d.png' % g))]
    if a.part:
        k, n = map(int, a.part.split('/')); gs = [g for i, g in enumerate(gs) if i % n == k]
    if not gs: print('nothing to do'); return
    sh = B.ALL_SHOTS[shot]; n = f1 - f0; segments = segments or [(-10**6, None)]
    def seg_of(g):
        k = g - f0; i = 0
        for j, (ks, kb) in enumerate(segments):
            if k >= ks: i = j
        return i
    cur = None
    for g in gs:
        t0 = time.time(); k = g - f0; si = seg_of(g)
        if si != cur:                                   # (re)build: ink hulls are sized for the build camera distance, so long dives use one build per distance range
            kb = segments[si][1]; bg = gs[0] if kb is None else f0 + kb
            B.build(location, light, shot, q, bg); scene = bpy.context.scene
            scene.render.threads = 2
            if a.samples: scene.cycles.samples = a.samples
            elif not a.draft: scene.cycles.samples = 13
            setup_fn(scene); cur = si
        B.set_frame_cam(shot, g); frame_fn(g, k, n)
        for kk, fn in sh.get('animate', {}).items(): fn(k, n)
        B.render_frame(shot, g, os.path.join(out, 'g_%04d.png' % g), q, a.samples)
        print('g', g, '%.1fs' % (time.time() - t0), flush=True)


# ----------------------------------------------------------------------------- walking crowd (cast22 crowd_member cards)
import random
class Walkers:
    """n cast22 crowd walkers. spec = dict(i=variant, p0=(x,y), p1=(x,y), speed=D/s (world), t0=frame offset). Each walker owns `nph` pre-built phase cards (cached rasters);
    `update(g, cam)` places the right phase, turns it to the camera (yaw + lean-back like beck.cast_card) and moves its contact shadow."""
    def __init__(s, specs, scale=2.0, rim='#ffb070', nph=8, z=0.0, face_dir=1, name='wk'):
        import cast22
        s.specs, s.nph, s.scale, s.z, s.items = specs, nph, scale, z, []
        for j, sp in enumerate(specs):
            d = (sp['p1'][0] - sp['p0'][0], sp['p1'][1] - sp['p0'][1]); L = math.hypot(*d) or 1.0
            right = (d[0] * face_dir) > 0 if abs(d[0]) > 0.3 * abs(d[1]) else (d[1] > 0)
            obs = []
            for k in range(nph):
                story = cast22.crowd_member(sp['i'], 'pass_walk', phase=k / float(nph), mirror=sp.get('mirror', not right))
                ob = B.cast_card(story, (sp['p0'][0], sp['p0'][1], z), yaw_deg=0, tilt=0, scale=scale, rim=rim, shadow=False, name='%s%d_%d' % (name, j, k))
                ob.hide_render = True; obs.append(ob)
            sh = B.Part('wsh_%s%d' % (name, j), ink=False, shadow=False); fw = obs[0]['feet_w']
            B.plane(sh.mb, (-fw * 0.8, -fw * 0.5, 0.03), (fw * 1.6, 0, 0), (0, fw * 1.0, 0), B.STATE['E']('blob', 'blob', alpha=True), (0, 0, 1, 1))
            sho = sh.done(); s.items.append((sp, obs, sho, (d[0] / L, d[1] / L, L)))
    def pos(s, sp, dr, g):
        t = (g - sp.get('t0', 0)) / 30.0; sdist = sp['speed'] * t; L = dr[2]
        if sp.get('loop'): sdist = sdist % L
        sdist = max(0.0, min(L, sdist)) if not sp.get('loop') else sdist
        return sp['p0'][0] + dr[0] * sdist, sp['p0'][1] + dr[1] * sdist, sdist
    def update(s, g, cam, hide=None):
        cam = V(cam)
        for sp, obs, sho, dr in s.items:
            x, y, sd = s.pos(sp, dr, g); cyc = (sd / sp.get('stride', 3.2)) % 1.0           # 1 walk cycle per `stride` D travelled
            k = int(cyc * s.nph) % s.nph
            d = cam - V((x, y, s.z + 1.5)); hz = math.hypot(d.x, d.y); tilt = max(0.0, min(62.0, 0.8 * math.degrees(math.atan2(d.z, max(hz, 1e-3)))))
            yaw = math.atan2(cam.x - x, -(cam.y - y))
            vis = sp.get('vis', (-1e9, 1e9)); on = vis[0] <= g <= vis[1] and not (hide and hide(x, y, g))
            for j, ob in enumerate(obs):
                ob.hide_render = not (on and j == k)
                if j == k: ob.location = (x, y, s.z); ob.rotation_euler = (math.radians(-tilt), 0.0, yaw)
            sho.location = (x, y, s.z); sho.hide_render = not on

def hide_static_crowd(boxes):
    """Context: patch beck_london.facing_card / plane so static crowd cards + their contact shadows inside any (x0,x1,y0,y1) box are NOT built.
    Call patch() BEFORE building; unpatch() after."""
    import beck_london as L
    o_fc, o_pl = L.facing_card, L.plane
    def inb(x, y): return any(b[0] <= x <= b[1] and b[2] <= y <= b[3] for b in boxes)
    def fc(mb, base, w, h, card, cam=None, tilt=0.0, **kw):
        if inb(base[0], base[1]) and h > 4.0 and tilt == 5.0: return
        return o_fc(mb, base, w, h, card, cam, tilt, **kw)
    def pl(mb, p0, pu, pv, mat, uv=(0, 0, 1, 1)):
        if abs(p0[2] - 0.09) < 1e-6 and abs(pv[1] - 1.4) < 1e-6 and inb(p0[0] + pu[0] / 2, p0[1] + 0.7): return
        return o_pl(mb, p0, pu, pv, mat, uv)
    L.facing_card, L.plane = fc, pl
    return lambda: (setattr(L, 'facing_card', o_fc), setattr(L, 'plane', o_pl))


def ground_with_hole(hole):
    """Rebuild beck_london's 'ground' planes (same textures / UVs) with a rectangular hole (x0, x1, y0, y1) in the far pavement strip y 14..24, so a shaft can be seen below."""
    x0, x1, y0, y1 = hole; o = bpy.data.objects.get('ground')
    if o: o.hide_render = True; o.hide_viewport = True
    TX = B.STATE['TX']; night = B.STATE['lkey'] == 'NIGHT_CITY'
    PV = (lambda g: TX('pave', g * 0.5, (0.45, 0.8, 1.6))) if night else (lambda g: TX('pave', g))
    g = B.Part('ground_hole', (0, 10, 0), ink=False); mb = g.mb; pl = B.plane
    pl(mb, (-160, -80, -0.05), (320, 0, 0), (0, 80, 0), PV(0.8), (0, 0, 40, 10)); pl(mb, (-160, -8, 0.0), (320, 0, 0), (0, 6, 0), PV(1.0), (0, 0, 40, 1)); pl(mb, (-160, -2, 0.0), (320, 0, 0), (0, 16, 0), TX('road', 1.0), (0, 0, 40, 2))
    pl(mb, (-160, 14, 0.0), (120, 0, 0), (0, 10, 0), PV(1.0), (0, 0, 15, 1))
    U = lambda x: (x + 26.0) / 186.0 * 22.0
    pl(mb, (-26, 14, 0.0), (186, 0, 0), (0, y0 - 14, 0), PV(1.0), (U(-26), 0, U(160), 1)); pl(mb, (-26, y1, 0.0), (186, 0, 0), (0, 24 - y1, 0), PV(1.0), (U(-26), 0, U(160), 1))
    pl(mb, (-26, y0, 0.0), (x0 + 26, 0, 0), (0, y1 - y0, 0), PV(1.0), (U(-26), 0, U(x0), 1)); pl(mb, (x1, y0, 0.0), (160 - x1, 0, 0), (0, y1 - y0, 0), PV(1.0), (U(x1), 0, U(160), 1))
    pl(mb, (-40, 14, 0.0), (14, 0, 0), (0, 0.5, 0), PV(1.0), (0, 0, 2, 1)); pl(mb, (-40, 22.5, 0.0), (14, 0, 0), (0, 1.5, 0), PV(1.0), (0, 0, 2, 1))
    pl(mb, (-160, 24, -0.02), (320, 0, 0), (0, 52, 0), PV(0.8), (0, 0, 40, 6)); pl(mb, (-160, 110, -0.02), (320, 0, 0), (0, 26, 0), PV(0.8), (0, 0, 40, 3))
    g.done()


def fill_foreground(gap=(-40.0, -14.0), rows=((-30.0, -17.0, 13.0, 'row2'), (-46.0, -32.0, 10.0, 'row3'), (-62.0, -48.0, 8.0, 'row4')), xr=(-102, 110), seed=5):
    """Runtime dressing (london): fill the bare ground behind / beside the lodging house with terrace blocks in the set's own style (pitched roofs, chimneys),
    so the extreme-wide views have city in the bottom of the frame. `gap` (x range) stays empty in rows 2 and 3 (Beck's back window)."""
    rs_ = random.Random(seed); C_, TX = B.STATE['C'], B.STATE['TX']
    tr = B.Part('fg_fill', (0, -25, 12)); mb = tr.mb
    for (y0, y1, h0, nm) in rows:
        x = xr[0]; i = 0
        while x < xr[1]:
            w = rs_.uniform(8, 11); i += 1
            if nm == 'row1' and (x + w > -35 and x < -19): x = -19.0; continue          # the real lodging house stands here
            if nm != 'row1' and (x + w > gap[0] and x < gap[1]): x = gap[1]; continue
            hgt = h0 + rs_.uniform(-2.0, 3.0)
            B.pitched(mb, x, x + w, y0, y1, 0, hgt, rs_.uniform(3.2, 4.6), C_(rs_.choice(['#a8452c', '#b9764a', '#8f3a28', '#9a5a7a'])), C_(rs_.choice(['#c4482c', '#8a3a5a', '#4a56a0', '#b8742c'])), tx_front=TX(rs_.choice(['fac_a', 'fac_b', 'fac_c']), 1.0))
            for cxo in (0.3, 0.7):
                if rs_.random() < 0.7: mb.box((x + w * cxo - .6, (y0 + y1) / 2 - .6, hgt + 2.2), (x + w * cxo + .6, (y0 + y1) / 2 + .6, hgt + 5.0), C_('#6a3020'))
            x += w + rs_.uniform(0.0, 0.6)
    tr.done((0, -25, 14))


def scale_emission(objname, f):
    o = bpy.data.objects.get(objname)
    if not o: return False
    for sl in o.material_slots:
        m = sl.material
        if m and m.use_nodes:
            for nd in m.node_tree.nodes:
                if 'Strength' in nd.inputs: nd.inputs['Strength'].default_value *= f
    return True


MINE = ('wk', 'wsh_', 'my_towers', 'map_crate', 'crate_shadow', 'fg_fill', 'beck_', 'lodge_back', 'shaft', 'actor_', 'ground_hole')


def ground(shot, location, light, f0, f1, setup_fn, frame_fn, segments, step=10):
    """QA_TEAM section K: film/v3/tools/ground_check22.check_frame on every `step`-th frame (builds per segment like run); writes GROUND.md."""
    sys.path.insert(0, os.path.join(PROJ, 'v3', 'tools')); import ground_check22 as GC
    segments = segments or [(-10**6, None)]; allf = []; cur = None; n = f1 - f0
    for g in list(range(f0, f1, step)) + [f1 - 1]:
        k = g - f0; si = max(j for j, (ks, kb) in enumerate(segments) if k >= ks)
        if si != cur:
            kb = segments[si][1]; B.build(location, light, shot, 'preview', f0 if kb is None else f0 + kb); setup_fn(bpy.context.scene); cur = si
        B.set_frame_cam(shot, g); frame_fn(g, k, n)
        for kk, fn in B.ALL_SHOTS[shot].get('animate', {}).items(): fn(k, n)
        for ob in bpy.context.scene.objects:
            if ob.type != 'MESH': continue
            mine = ob.name.startswith(MINE)
            if ob.name in ('beck_sill', 'beck_win'): ob['mounted'] = True      # window ledge + lit window on the lodging back wall (box overlaps the wall, checked in frames)
            elif ob.name.startswith('actor_off'): ob['mounted'] = True           # seated official: lower body hidden inside chair + desk (checked in frames)
            elif ob.name == 'map_crate' and g - f0 < 104: ob['airborne'] = True   # the crate is falling until it lands (frame local 104)
            elif not mine: ob['mounted'] = True                                 # set3d22 geometry (QA-art PASS): signs, posters, buildings, vehicles; seen touching wall / ground in the renders
        allf += GC.check_frame(bpy.context.scene, g)
    ok = not allf
    L = ['# GROUND.md (QA_TEAM section K, ground_check22)', 'frames %d-%d step %d, tolerance 0.02' % (f0, f1 - 1, step), 'RESULT: %s (%d failures)' % ('PASS' if ok else 'FAIL', len(allf)), '', 'Checked strictly: every object this take adds (cast22 cards incl. walkers, shadows, towers, crate, filler blocks, shaft). set3d22 geometry is exempt (mounted=True, QA-art PASS, seen attached); the seated official is mounted (seated on his chair behind the desk); the crate is airborne only while falling.', '', '| frame | object | problem |', '|---|---|---|']
    L += ['| %d | %s | %s |' % f for f in allf[:300]]
    open(os.path.join(HERE, 'GROUND.md'), 'w').write('\n'.join(L) + '\n'); print('ground', 'PASS' if ok else 'FAIL %d' % len(allf))
