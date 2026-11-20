"""shot 24: BIGZOOM 2. ONE build (camp_bank end preset + the valley extras), ONE eased camera path from the valley_loop pose to the camp_bank pose."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21
from c21 import K, bpy, np, cast21, actors, sprites, Vector, lerp, smooth, sstep
from shot import Cast, render_frame, g_of, G_HALF, G_WATCH, PPD, sway

A0, S0, S1 = 1345, 1420, 1490          # drift start, swoop start (acceleration begins just before "อีกครึ่ง" 1428), arrival
P0, L0, LENS0 = Vector((-72.0, -133.0, 229.0)), Vector((12.0, 36.0, 0.0)), 21.0                               # valley_loop camera
VIV0 = tuple(float(v) for v in os.environ.get('VIV0', '1.9,1.05').split(','))                                # valley_loop VIVID (entry)
VIV1, LENS1 = (1.52, 1.30), 26.0                                                                           # camp_bank
S_A = 0.035
WAY = Vector((-85.0, -50.0, 0.0))          # a waypoint over the camp lane: keeps 3 m clear of every pavilion, pole and banner (BVH scan)
G_SHOCK_C, G_SHOCK_S = 1494, 1500
CAMP = {}

def sparam(g):
    if g <= S0: return S_A * (g - A0) / float(S0 - A0)
    if g >= S1: return 1.0
    T = S1 - S0; t = (g - S0) / float(T); v0 = S_A / float(S0 - A0)
    return (2 * t**3 - 3 * t**2 + 1) * S_A + (t**3 - 2 * t**2 + t) * T * v0 + (-2 * t**3 + 3 * t**2)

def lat_off(g):
    """metres to the camera's right: a slide of about 40 px/s over the drift, eased out by the arrival (C1 at S0)"""
    v = 13.0 / 30.0
    if g <= S0: return v * (g - A0)
    if g >= S1: return 0.0
    T = S1 - S0; t = (g - S0) / float(T); L0_ = v * (S0 - A0)
    return (2 * t**3 - 3 * t**2 + 1) * L0_ + (t**3 - 2 * t**2 + t) * T * v

def camera(g):
    P1, L1 = CAMP['P1'], CAMP['L1']
    s = sparam(g)
    xy = P0.to_2d() * (1 - s) ** 2 + 2 * (1 - s) * s * WAY.to_2d() + P1.to_2d() * s * s
    z = math.exp(lerp(math.log(P0.z), math.log(P1.z), s))
    loc = Vector((xy.x, xy.y, z)); look = L0 * (1 - s) + L1 * s
    lens = lerp(LENS0, LENS1, sstep(s))
    fwd = (look - loc); fwd.z = 0; fwd.normalize(); right = Vector((fwd.y, -fwd.x, 0.0))
    lo = lat_off(g)
    loc = loc + right * lo; look = look + right * lo * 0.6
    if g > S1:                                              # settle: push 6 %/s and slide 40 px/s, eased in
        k = g - S1; e = k * k / 24.0 if k < 12 else (k - 6.0)
        d = (look - loc); dist = d.length
        loc = loc + d.normalized() * 0.055 * 3.3 / 30.0 * e + right * (3.3 * 40.0 / 924.0 / 30.0) * e
        look = look + d.normalized() * 0.055 * 3.3 / 30.0 * e + right * (3.3 * 40.0 / 924.0 / 30.0) * e
    vg = lerp(VIV0[0], VIV1[0], s); vs = lerp(VIV0[1], VIV1[1], s)
    return loc, look, lens, (vg, vs)

def big_wall(rs, n=24, ranks=3, y0=26.0, half=13.0, sc=2.1):
    """the cork: the Scots' spear wall across the north end of the bridge, scaled up (x2.1) so it reads as a tan block from 230 m; spears level."""
    B = K.Batch(83); cnt = 0
    for rank in range(ranks):
        for k in range(n):
            x = -half + 2 * half * k / (n - 1) + (0.6 if rank % 2 else 0.0); y = y0 + 1.3 * sc * rank; z = float(K.ground(x, y))
            B.box(['hay', 'thatch', 't_brown', 'hay'][(k + rank) % 4], (x, y, z + 0.85 * sc), (0.8 * sc, 0.6 * sc, 1.6 * sc)); B.sphere('iron', (x, y, z + 1.78 * sc), 0.21 * sc, seg=6, rings=4)
            K.spear(B, (x, y - 0.4 * sc, z), tilt=(0.0, -0.9), h=2.4 * sc); cnt += 1
    B.finalize('spear_wall', ink=False); return cnt

def run24(mode, gs, samples):
    P = dict(K.PRESETS['camp_bank']); P.update(farms=True, heather_n=900, gorse_n=200, crag_n=140, pine_n=60, bridge_pairs=None)
    K.PRESETS['reveal'] = P
    A = K.build('reveal'); P['fg'](A, P); P['camp_fg'](A, P)
    items = []; orig_stage, orig_wall = K.stage_crowd, K.spear_wall
    K.stage_crowd = lambda it, cam=None, seg=10, shadow=True: items.extend(it)
    K.spear_wall = lambda n, ranks, rs, y0=27.0, half=9.0: big_wall(rs)
    K.crowd_loop(A, P); K.stage_crowd, K.spear_wall = orig_stage, orig_wall
    scene = bpy.context.scene; cam = scene.camera
    CAMP['P1'] = Vector(P['cam']); CAMP['L1'] = Vector(P['look'])
    ln = P['lens']
    marks = dict(
        cress=K.mark_px(P['cam'], P['look'], ln, 3.1, 205, 'cressingham'), surrey=K.mark_px(P['cam'], P['look'], ln, 3.0, 580, 'surrey'),
        e0=K.mark_px(P['cam'], P['look'], ln, 8.0, 60, 'foot'), e1=K.mark_px(P['cam'], P['look'], ln, 11.0, 335, 'foot'), e2=K.mark_px(P['cam'], P['look'], ln, 13.0, 440, 'foot'),
        e3=K.mark_px(P['cam'], P['look'], ln, 10.0, 520, 'foot'), e4=K.mark_px(P['cam'], P['look'], ln, 14.0, 640, 'foot'))
    C = Cast()
    spec = [('cress', 'cressingham'), ('surrey', 'surrey'), ('e0', 'footman_a'), ('e1', 'knight_a'), ('e2', 'footman_b'), ('e3', 'knight_b'), ('e4', 'footman_a_v1')]
    for nm, cast in spec: C.add(nm, cast, marks[nm][:3])
    near = [marks[n][:2] for n, _ in spec]
    def restage(camloc):
        for o in [o for o in bpy.data.objects if o.name.startswith('crowdx_')]:
            me = o.data; bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
        its = []
        for (x, y, z, kind, sc) in items:
            if any(math.hypot(x - a, y - b) < 3.5 for a, b in near): continue
            d = math.sqrt((x - camloc.x) ** 2 + (y - camloc.y) ** 2 + (z - camloc.z) ** 2)
            its.append((x, y, z, kind, sc * min(3.2, max(1.0, d / 75.0))))
        for o in orig_stage(its, cam=cam): o.name = 'crowdx_' + o.name
    for g in gs:
        if mode == 'final' and os.path.exists(os.path.join(HERE, 'raw_final', 'g_%04d.json' % g)): continue
        t0 = time.time(); f = g
        loc, look, lens, viv = camera(g); c21.set_cam(cam, loc, look, lens); K.STATE['vivid'] = viv
        t = g / 30.0; K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        restage(loc); scene.frame_set(f)
        # --- cast
        for nm in ('cress', 'surrey'):
            sw = sway(g, 0.7 if nm == 'cress' else 2.0, 1.5)
            if nm == 'cress':
                a, b = G_SHOCK_C, G_SHOCK_C + 3
                pose = dict(cast21.STORY21['cressingham_shocked' if g >= a + 1 else 'cressingham_neutral'][1])
                if g < a: pose['expr'] = 'worried'; pose['mouth'] = 'flat'
                pose['blink'] = {a - 1: 1, a: 2, a + 1: 1}.get(g, 0) if abs(g - a) <= 1 else cast21.blink_at(g, 84, 11) if g < a - 4 else 0
            else:
                a = G_SHOCK_S
                pose = dict(cast21.STORY21['surrey_shocked' if g >= a + 1 else 'surrey_worried'][1])
                pose['blink'] = {a - 1: 1, a: 2, a + 1: 1}.get(g, 0) if abs(g - a) <= 1 else cast21.blink_at(g, 96, 40) if g < a - 4 else 0
            pose['head_roll'] = pose.get('head_roll', 0) + sw
            if g > (G_SHOCK_C if nm == 'cress' else G_SHOCK_S): pose['head_roll'] += 2.5 * math.sin(g * 0.9)      # trembling
            C.put(nm, f, pose)
        casts = dict(e0='footman_a', e1='knight_a', e2='footman_b', e3='knight_b', e4='footman_a')
        for i, nm in enumerate(('e0', 'e1', 'e2', 'e3', 'e4')):
            base = casts[nm]
            if g < G_WATCH + i * 2:
                pose = dict(cast21.STORY21[base + '_stand'][1]); lift = 0.0
            else:
                pose = dict(cast21.STORY21[base + '_tiptoe'][1]); lift = 0.10 + 0.07 * math.sin(g * 0.45 + i)
            pose['blink'] = cast21.blink_at(g, 80 + 9 * i, 17 * i); pose['head_roll'] = pose.get('head_roll', 0) + sway(g, i, 2.5, 0.5)
            C.put(nm, f, pose, lift=lift)
        C.sprites(f); bpy.context.view_layer.update(); actors.sync_all(scene, cam)
        out = os.path.join(HERE, 'raw_' + mode, 'g_%04d.png' % g); os.makedirs(os.path.dirname(out), exist_ok=True)
        render_frame(out, mode, samples)
        hd = {}
        for nm, it in C.items.items():
            x, y, z = it['xyz']; hh = {'cress': 3.23, 'surrey': 3.2}.get(nm, 3.2) * it['scale']
            hd[nm] = [round(v) for v in K.project(cam, (x, y, z + hh - 0.5 * it['scale']))[:2]]
        json.dump(dict(g=g, heads=hd, cam=[round(v, 2) for v in loc], lens=round(lens, 2), vivid=[round(v, 3) for v in viv]), open(out[:-4] + '.json', 'w'))
        print('s24 g', g, round(time.time() - t0, 1), flush=True)
