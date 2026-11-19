#!/usr/bin/env python3
"""film 14 take s11 (RE-DO v2): shots 11-14 (the count): day 1 one hive / day 2 ten hives / day 3 ONE wire through every hive / the whole ring on one wire.
g 759..1000 (+6 handle frames each side: 753..1006).  One shot per process (one location per process):
    python3 shot.py <shot 11|12|13|14> <a:b[:step]> <out_dir> [draft|final]
v2 (QA_TECH s11 FAIL): 12/14 are MEDIUM-height 3/4 dollies along the fence (no high ring view), 11 is an orbit round a hive that reads as a box and a farmer who
ties it on, 13 threads the wire through an eyelet ring on the hive bar (coil shrinks), mouth held, eye-line on the wire, stool contact shadow, no sapling.
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, put, story, lerp, clamp, sm, blink_at, cast14, Vector, bpy
import numpy as np

BOUND = {11: (759, 820), 12: (821, 869), 13: (864, 929), 14: (930, 1000)}
GR = {11: (753, 820), 12: (821, 863), 13: (864, 929), 14: (930, 1006)}      # with handles (6 each side of the take)

# -------------------------------------------------------------------- cameras (centre of each move is the preset camera used for the set's grass scatter)
def L3(a, b, x): return tuple(lerp(p, q, x) for p, q in zip(a, b))
def ease(x, k=0.45): x = clamp(x); return k * sm(x) + (1 - k) * x
# shot 11: ORBIT round the one hive, left-front -> front (hive 1 at x -6.5, y 5): the trapezoid box + end slot read in 3/4
C11 = ((-8.5, 1.7, 1.75), (-6.9, 1.0, 1.7)); L11 = ((-6.1, 5.0, 1.65), (-6.0, 5.0, 1.65)); LENS11 = (24, 24)
# shot 12: dolly along the front of the fence from its left end at hive height (boxes visible under the roofs); stays 5+ m clear of every roof
C12 = ((-23.0, 1.9, 2.0), (-17.5, 2.1, 2.1)); L12 = ((-4.0, 6.5, 1.3), (-2.0, 6.6, 1.3)); LENS12 = (40, 38)
# shot 13: close on the bar, farmer on the left of the hive, the camera drifts right and in
C13 = ((-9.0, 1.2, 1.75), (-8.3, 1.5, 1.75)); L13 = ((-7.2, 5.0, 1.6), (-6.6, 5.0, 1.6)); LENS13 = (24, 24)
# shot 14: dolly + pan round the front-left corner at hive height: the thin wire runs through every hive bar, round the corner and up the left side
C14 = ((-19.5, 2.4, 2.0), (-17.0, 4.0, 2.0)); L14 = ((-8.0, 7.5, 1.2), (-12.0, 11.0, 1.2)); LENS14 = (32, 30)

def cam_at(shot, g):
    a, b = BOUND[shot]; xr = (g - a) / float(b - a); x = clamp(xr)
    Cs, Ls, Ln = {11: (C11, L11, LENS11), 12: (C12, L12, LENS12), 13: (C13, L13, LENS13), 14: (C14, L14, LENS14)}[shot]
    e = ease(x) + (xr - x) * 0.55          # handle frames keep moving (extrapolated), never frozen
    return L3(Cs[0], Cs[1], e), L3(Ls[0], Ls[1], e), lerp(Ln[0], Ln[1], e)

F.CAMS['fence_ring'] = dict(loc=C12[0], look=L12[0], lens=22)
F.PRESETS['fence_ring'] = dict(light='DAY', state='fs2', wire_r=0.03, staging=[])
F.CAMS['hive_close'] = dict(loc=C13[0], look=L13[0], lens=24)
F.PRESETS['hive_close'] = dict(light='DUSK', state='fs3', staging=[])
F.CAMS['fence_line'] = dict(loc=C11[0], look=L11[0], lens=24)
F.PRESETS['fence_line'] = dict(light='DAY', state='fs1', staging=[])
PRESET = {11: ('fence_line', 'DAY'), 12: ('fence_ring', 'DAY'), 13: ('hive_close', 'DUSK'), 14: ('fence_ring', 'DUSK')}

# -------------------------------------------------------------------- helpers
def rod(a, b, r, mat, name='actor_stub'):
    a = Vector(a); b = Vector(b); d = b - a; L = d.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=r, depth=max(L, 1e-3), location=(a + b) / 2)
    o = bpy.context.active_object; o.name = name; o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); o.data.materials.append(mat); o.visible_shadow = False
    return o

def tube(pts, r, mat, name='actor_wire', ns=6, shadow=False):
    """smooth tube along the polyline pts (list of xyz); returns the object."""
    P = np.asarray(pts, float); n = len(P)
    tg = np.gradient(P, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1, keepdims=True), 1e-9)
    up = np.array([0, 0, 1.0]); sd = np.cross(tg, up); bad = np.linalg.norm(sd, axis=1) < 1e-6; sd[bad] = (1, 0, 0)
    sd /= np.maximum(np.linalg.norm(sd, axis=1, keepdims=True), 1e-9); uu = np.cross(sd, tg)
    V = np.zeros((n, ns, 3))
    for q in range(ns):
        a = 2 * math.pi * q / ns; V[:, q] = P + r * (math.cos(a) * sd + math.sin(a) * uu)
    faces = [(k * ns + q, k * ns + (q + 1) % ns, (k + 1) * ns + (q + 1) % ns, (k + 1) * ns + q) for k in range(n - 1) for q in range(ns)]
    me = bpy.data.meshes.new(name); me.from_pydata(V.reshape(-1, 3).tolist(), [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(mat); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = shadow
    return ob

def ring_obj(center, r_major, r_minor, mat, axis='X', name='actor_eyelet'):
    pts = []; n = 20
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        pts.append((center[0], center[1] + r_major * math.cos(a), center[2] + r_major * math.sin(a)) if axis == 'X' else (center[0] + r_major * math.cos(a), center[1], center[2] + r_major * math.sin(a)))
    return tube(pts, r_minor, mat, name, ns=6)

def solid_mat(name, col, k=1.0):
    return F.G.mat_emit(name, col, k) if False else None

def hive_pivot(i=1):
    u = F.UNITS[i]; return Vector((u['pos'][0], u['pos'][1] - F.WIRE_OFF, F.WIRE_Z))

def wire_pts():
    W = F.STATE['wire']; return W['S'], W['base']
def wire_at_s(s):
    S, base = wire_pts(); s = s % F.S_TOT; i = int(np.searchsorted(S, s, side='right') - 1); i = max(0, min(i, len(S) - 2)); u = (s - S[i]) / max(S[i + 1] - S[i], 1e-9)
    return Vector(base[i]) * (1 - u) + Vector(base[i + 1]) * u

def sharp_ground():
    """remove the soft green grass-patch mask from the ground material (it reads as a blurry blotch): the mask's Green channel no longer drives the mix."""
    m = bpy.data.materials.get('ground'); nt = m.node_tree
    for n in nt.nodes:
        if n.type == 'MIX' and n.inputs[0].links and n.inputs[0].links[0].from_node.type == 'SEPARATE_COLOR' and n.inputs[0].links[0].from_socket.name == 'Green':
            nt.links.remove(n.inputs[0].links[0]); n.inputs[0].default_value = 1.0
def matte_wire():
    """thin taut grey-silver, non-emissive wire (cut every link into the material's colour / emission sockets)."""
    m = F.STATE['M']['wire']; nt = m.node_tree
    for n in nt.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            for nm in ('Base Color', 'Emission Color', 'Emission Strength'):
                for l in list(n.inputs[nm].links): nt.links.remove(l)
            n.inputs['Base Color'].default_value = (0.50, 0.52, 0.55, 1); n.inputs['Emission Strength'].default_value = 0.0
            n.inputs['Emission Color'].default_value = (0, 0, 0, 1); n.inputs['Roughness'].default_value = 0.45; n.inputs['Metallic'].default_value = 0.35
def glow_wire(k):
    """raise the emission of the set's wire material (the wire must read as ONE bright line at phone size)."""
    m = F.STATE['M']['wire']
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            for nm in ('Emission Strength',):
                if nm in n.inputs: n.inputs[nm].default_value = k
            if 'Emission Color' in n.inputs: n.inputs['Emission Color'].default_value = (1.0, 0.8, 0.45, 1)

def hide_set_wire(on=True):
    F.STATE['wire_ob'].hide_render = on; F.STATE['wire_ob'].hide_viewport = on

# -------------------------------------------------------------------- the farmer on his stool
STOOL11 = (-5.55, 4.25, 0.26)       # shot 11: right of hive 1 (mirror: faces the hive on his left)
STOOL13 = (-7.95, 4.25, 0.26)       # shot 13: left of hive 1 (faces right: the bar, the wire and the row of hives)
def stool_at(pos, scale=0.3):
    mb = C.G.MB('s_stool'); C.G.stool(mb, F.STATE['M'], (pos[0], pos[1], 0.0), scale); mb.finish()

def farmer11(g):
    """TIE-ON loop (24 frames, 3 poses): A reach to the hive's hanging rope / B pull the cord down and back / C lift and loop it over the hook."""
    c, p = story('farmer_tie_wire'); p = dict(p)
    ph = ((g - 759) % 24) / 24.0
    keysA = [(0.86, 0.22), (0.58, -0.10), (0.92, 0.42)]           # hand (x, y) in D from the shoulder
    k = ph * 3; i = int(k) % 3; u = sm(k - int(k)); h0 = keysA[i]; h1 = keysA[(i + 1) % 3]
    hand = (lerp(h0[0], h1[0], u), lerp(h0[1], h1[1], u))
    p['arm_r'] = dict(p['arm_r'], hand=hand, bend=-0.3 + 0.25 * math.sin(2 * math.pi * ph), stretch=1.2)
    p['arm_l'] = dict(hand=(-0.30 + 0.10 * math.sin(2 * math.pi * ph + 1.0), 0.80 - 0.08 * math.cos(2 * math.pi * ph)), bend=0.4); p['prop_l'] = dict(type='wirecoil', scale=1.0)
    p['lean'] = 3.0 + 3.0 * math.sin(2 * math.pi * ph); p['head_roll'] = -3 + 2 * math.sin(2 * math.pi * ph + 0.5); p['blink'] = blink_at(g, 80, 11); p['t'] = g / 30.0
    p['expr'] = 'determined'; p['mouth'] = 'flat'; p['gaze'] = (0.95, 0.35)
    return c, p, hand

def farmer13(g, x):
    """threading: right hand holds the wire at the eyelet and feeds it through; left forearm carries the coil that gets smaller; mouth held; eyes on the wire."""
    c, p = story('farmer_tie_wire'); p = dict(p)
    w = g * 0.5
    hand = (0.80 + 0.06 * math.sin(w) + 0.10 * x, 0.24 + 0.05 * math.cos(w * 1.3))
    p['arm_r'] = dict(p['arm_r'], hand=hand, bend=-0.2, stretch=1.2, shape='open')
    p['arm_l'] = dict(hand=(-0.40, 0.90), bend=0.4); p['prop_l'] = dict(type='wirecoil', scale=lerp(1.15, 0.55, x))
    p['lean'] = 4.0 + 1.5 * math.sin(g * 0.1); p['head_roll'] = -3 + 1.0 * math.sin(g * 0.07); p['blink'] = blink_at(g, 80, 11); p['t'] = g / 30.0
    p['expr'] = 'determined'; p['mouth'] = 'flat'; p['gaze'] = (0.95, 0.30)
    return c, p, hand

# -------------------------------------------------------------------- builds
def build_for(shot):
    def b():
        pr, light = PRESET[shot]
        F.build(pr, light, dress=False); cam = F.make_camera(F.CAMS[pr]); sharp_ground()
        a, b = BOUND[shot]; path = []
        for g in range(a, b + 1, 6):
            lo, lk, _ = cam_at(shot, g)
            for t in (0.0, 0.25, 0.5, 0.75): path.append((lo[0] + (lk[0] - lo[0]) * t, lo[1] + (lk[1] - lo[1]) * t))
        print('cut near', C.cut_near(('props', 'grass', 'flowers', 'pebbles', 'edge'), path, {11: 2.6, 12: 3.2, 13: 2.6, 14: 3.2}[shot]))
        if shot in (11, 13):
            print('ladder cut', C.cut_region('props', [(-8.4, -5.0, 3.0, 4.95, 2.7)]))
            stool_at(STOOL11 if shot == 11 else STOOL13)
        return dict(cam=cam)
    return b

def hide_near_stool(pos):
    pass

def frame11(st, g):
    loc, look, lens = cam_at(11, g); C.set_cam(st['cam'], loc, look, lens)
    F.set_fence_stage(1); F.set_wire_push(-1); bpy.context.view_layer.update(); F.set_bees(-1)
    c, p, hand = farmer11(g)
    r = put(c, p, STOOL11, loc, ppd=128, mirror=True, contact=True, shadow_k=1.6)
    h = r['world']('hand_r'); piv = hive_pivot(1)
    top = Vector((piv.x + 0.45, piv.y, 1.98))
    rod(h, top, 0.014, F.STATE['M']['rope'], 'actor_cord')                                   # the cord from his hand to the hive's hanging rope
    return dict(cam=[round(v, 2) for v in loc], head=C.screen(r['world']('head')), top=C.screen(r['world']('head_top')), hand=[round(v, 2) for v in h], hand_scr=C.screen(h))

EY_R = 0.12
def frame13(st, g):
    loc, look, lens = cam_at(13, g); C.set_cam(st['cam'], loc, look, lens)
    F.set_fence_stage(3); F.set_wire_push(-1); bpy.context.view_layer.update(); F.set_bees(-1); hide_set_wire(True); matte_wire()
    x = clamp((g - 864) / 65.0); M = F.STATE['M']
    c, p, hand = farmer13(g, x)
    r = put(c, p, STOOL13, loc, ppd=128, mirror=False, contact=True, shadow_k=1.7)
    h = r['world']('hand_r'); piv = hive_pivot(1); zE = 2.0
    EL = Vector((piv.x - 0.45, piv.y, zE)); ER = Vector((piv.x + 0.45, piv.y, zE))
    for e in (EL, ER): ring_obj(e, EY_R, 0.02, M['metal'], 'X', 'actor_eyelet')
    cend = r['world']('wire_end_l') if 'wire_end_l' in r['anchors'] else r['world']('hand_l')
    # master path: coil end (sagging) -> hand -> eyelet L -> eyelet R -> along the wire to the next hives (the set's own wire line), truncated at the tip
    se = F.UNITS[1]['s']; S, base = wire_pts()
    master = [h, Vector((EL.x - 0.15, EL.y, zE)), EL, ER]
    for i in range(len(S)):
        if S[i] > se + 0.5 and S[i] < se + 30: master.append(Vector(base[i]))
    cum = [0.0]
    for a_, b_ in zip(master, master[1:]): cum.append(cum[-1] + (b_ - a_).length)
    d_el = cum[2]; d_er = cum[3]
    # tip travel: stub in the hand -> through eyelet L (~g 876) -> through eyelet R (~g 892) -> runs on along the row (the wire grows toward the next hive)
    kf = [(0.0, 0.28), (0.15, d_el + 0.10), (0.30, d_er + 0.10), (1.0, d_er + 9.5)]
    for (xa, la), (xb, lb) in zip(kf, kf[1:]):
        if xa <= x <= xb: Ltip = lerp(la, lb, (x - xa) / (xb - xa)); break
    pts = []
    for k, q in enumerate(master):
        if cum[k] >= Ltip:
            u = (Ltip - cum[k - 1]) / max(cum[k] - cum[k - 1], 1e-9); pts.append(master[k - 1] * (1 - u) + q * u); break
        pts.append(q)
    else: pts.append(master[-1])
    tube(pts, 0.03, M['wire'], 'actor_wire')
    # the slack from the coil to the hand: sagging, thin, gets shorter as the coil shrinks
    mid = (cend + h) / 2 + Vector((-0.45, 0.0, 0.25 + 0.2 * (1.0 - x)))
    sl = [cend * (1 - t) ** 2 + mid * 2 * t * (1 - t) + h * t * t for t in np.linspace(0, 1, 12)]
    tube(sl, 0.016, M['wire'], 'actor_wire2', ns=5)
    return dict(cam=[round(v, 2) for v in loc], head=C.screen(r['world']('head')), top=C.screen(r['world']('head_top')), hand=[round(v, 2) for v in h], hand_scr=C.screen(h),
                eyelet_scr=[C.screen(EL), C.screen(ER)], tip=round(Ltip, 2), dEL=round(d_el, 2), dER=round(d_er, 2))

def frame12(st, g):
    loc, look, lens = cam_at(12, g); C.set_cam(st['cam'], loc, look, lens)
    F.set_fence_stage(2); F.set_wire_push(-1); bpy.context.view_layer.update(); F.set_bees(-1); hide_set_wire(True)
    return dict(cam=[round(v, 2) for v in loc])

def frame14(st, g):
    loc, look, lens = cam_at(14, g); C.set_cam(st['cam'], loc, look, lens)
    F.set_fence_stage(3); F.set_wire_push(-1); bpy.context.view_layer.update(); F.set_bees(-1); matte_wire()
    return dict(cam=[round(v, 2) for v in loc])

FR = {11: frame11, 12: frame12, 13: frame13, 14: frame14}
if __name__ == '__main__':
    shot = int(sys.argv[1]); gs = [g for g in C.parse(sys.argv[2]) if GR[shot][0] <= g <= GR[shot][1]]; out = sys.argv[3]; q = sys.argv[4] if len(sys.argv) > 4 else 'draft'
    C.run(build_for(shot), FR[shot], out, gs, quality=q, samples=int(os.environ['SAMPLES']) if 'SAMPLES' in os.environ else None)
