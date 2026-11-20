#!/usr/bin/env python3
"""shot.py -- film 18 take s26 (render team 2, KEY SHOT, ending): jimo_out road at DAWN.  Low tracking pull in front of the running general (he runs -y toward the lens
down the road), front-3/4 dragon oxen directly behind him gaining on him, grey tail smoke (no flame); a held +19 % push-in from "วิ่งหนีวัว" (g 2068) through the hard cut.
Panic run: forward lean 21, round stunned eyes + sweat, cup held out at arm's length, one head turn to profile g 2070-2080.  NO pulses.
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S, R2, STATE
import cast18
import os
from mathutils import Vector as V

G0, G1 = 1958, 2112
H_IN, H_OUT = 8, 0                   # dissolve 11 in; the film ends here (hard cut on "ตลอดทาง")
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
SPEED = 6.0                          # D/s the group (and the camera with it) travels down the road, toward -y
mode, rng = c18.parse_args(FIRST, LAST)


def _dress(p):
    """own road dressing along the whole tracked stretch (no 'hay' / 'plume' / rocks / rings / baskets / wheels): furrows, red silk strips, torch stakes."""
    avoid = lambda x, y: -3.4 < x < 4.6                                  # keep the lane itself clear (the group runs there); warm period props on both verges
    R2.dress(-10.5, 10.5, -126, -34, 140, 26, kinds=('stone', 'hay', 'basket', 'pot', 'hay', 'stone'), avoid=avoid)
    R2.dress(-70.0, 70.0, -128, -36, 420, 27, kinds=('hay', 'hay', 'basket', 'stone', 'pot', 'hay'), avoid=lambda x, y: -4.5 < x < 5.5)       # field dressing for the crane over the plain (ground share <= 0.30)
    for i, yy in enumerate(range(-40, -125, -13)):
        R2.stake(-9.0 if i % 2 == 0 else 9.0, float(yy), 3.0)
R2.POST['s26'] = _dress

DIST0, DIST1 = 4.3, 4.9              # camera-to-general distance (D): a slow pull, the general is ~45-50 % of the frame height


def rel(g):
    d = c18.lerp(DIST0, DIST1, c18.ease((g - G0) / 110.0)) if g < 2068 else DIST1
    return d * (1.0 - 0.19 * c18.ramp(g, 2068, 2078))          # the held push-in


def cam_track(T, g, t):
    dy = SPEED * (g - G0) / 30.0
    sw = 1.2 * math.sin(2 * math.pi * 0.4 * (g - G0) / 30.0)   # smooth lateral weave of the tracking camera (the subject stays framed)
    gen_y = -50.0 - dy
    return dict(loc=(2.0 + sw, gen_y - rel(g), 0.95), look_at=(0.8 + 0.4 * sw, gen_y + 4.0, 2.5), lens=24)


def _gen_pos(g):
    return (1.35 + 0.3 * math.sin(g * 0.11) + 7.5 * max(0.0, 1.0 - (g - G0) / 80.0) ** 2, -50.0 - SPEED * (g - G0) / 30.0)


G_ZOOM = 2066                                       # end of the BIGZOOM: low medium on the general
WIDE_LOC = (30.0, 60.0, 62.0); WIDE_LOOK = (0.0, -75.0, -10.0)


def cam_bigzoom(T, g, t):
    """one continuous eased crane-down + swing round in FRONT of him: cylindrical interpolation about the general (azimuth 51 -> -83 deg through screen-right,
    radius 38 -> 4.9 D, height 60 -> 0.95 D), look-at from the wall/road overview to his chest; from g 2066 the old tracking pull + push-in, identical at the join."""
    end = cam_track(T, g, t)
    if g >= G_ZOOM:
        return end
    gx, gy = _gen_pos(g)
    u = c18.ease((g - G0) / float(G_ZOOM - G0)) if g > G0 else 0.0
    u = 0.9 * u + 0.1 * u * u * (3 - 2 * u) if False else u
    g0x, g0y = _gen_pos(G0)
    s_off = (WIDE_LOC[0] - g0x, WIDE_LOC[1] - g0y)
    r0 = math.hypot(*s_off); a0 = math.atan2(s_off[1], s_off[0])
    e_off = (end['loc'][0] - gx, end['loc'][1] - gy)
    r1 = math.hypot(*e_off); a1 = math.atan2(e_off[1], e_off[0])
    r = r0 * (r1 / r0) ** u                          # geometric: equal zoom steps per second
    ang = c18.lerp(a0, a1, u)
    z = end['loc'][2] + (WIDE_LOC[2] - end['loc'][2]) * max(0.0, (r - r1) / (r0 - r1))      # height follows the radius: no top-down view in the middle
    w = (1.0 - u) ** 6.0                                                       # the look-at lets go of the overview quickly and stays on him
    look = tuple((end['look_at'][i] - (gx, gy, 0.0)[i]) * (1 - w) + (WIDE_LOOK[i] - (g0x, g0y, 0.0)[i]) * w + (gx, gy, 0.0)[i] for i in range(3))
    return dict(loc=(gx + r * math.cos(ang), gy + r * math.sin(ang), z), look_at=look, lens=c18.lerp(34.0, 24.0, u))


T = c18.Take('s26', FIRST, LAST, draft=(mode == 'draft'), cam_fn=cam_bigzoom)
c18.fix_sky_clean(T, 'sky_DAWN', flat_above=0.6)
for _n in ('wallpools', 'cityglow', 'tw_glow', 'posts'):        # translucent glow quads on the city wall rendered as pale rectangles (TAKE gate 16)
    if _n in STATE['objects']:
        STATE['objects'][_n].hide_render = True
import bpy
for ob in bpy.data.objects:                       # no grey rocks / wheels / ring props / hay anywhere (TAKE gate rule 2)
    if ob.name.startswith(('fgwood', 'fgstone', 'dr_hay', 'dr_plume', 'dr_pot', 'dr_rope', 'dr_stone', 'dr_wheel', 'dr_basket')) or ob.name == 'hay':
        ob.hide_render = True
OX_LAT = [-1.5, 1.7, -3.0, 3.1]
OX_START = [9.0, 11.5, 14.0, 16.5]; OX_END = [5.0, 4.3, 6.0, 7.8]       # distance behind the general: gaining on him


import bpy
_sm = R2._shadow_quad('cpool', 1.0, 1.0)
if not _sm.materials:
    _sm.materials.append(STATE['M']['pool_w'])
POOL = bpy.data.objects.new('t18_genpool', _sm); STATE['SET'].objects.link(POOL); POOL.visible_shadow = False; J.no_bounce(POOL)
POOL2 = bpy.data.objects.new('t18_genpool2', _sm); STATE['SET'].objects.link(POOL2); POOL2.visible_shadow = False; J.no_bounce(POOL2)


import numpy as _np
PLAQUE = None


def make_plaque():
    global PLAQUE
    me = bpy.data.meshes.new('t18_plaque'); w, h = 12.0, 4.5
    me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    m = R2._card_mat(os.path.join(HERE_, 'plaque.png'), (1.0, 1.0, 1.0), 1.15, 'plaque')
    me.materials.append(m)
    ob = bpy.data.objects.new('t18_plaque', me); STATE['SET'].objects.link(ob)
    ob.location = (0.0, 3.35, 9.6); ob.rotation_euler = (0, 0, math.pi); ob.visible_shadow = False; J.no_bounce(ob)
    PLAQUE = ob


HERE_ = os.path.dirname(os.path.abspath(__file__))
make_plaque()


def rim_mat(path):
    m = bpy.data.materials.get('t18_rim_' + os.path.basename(path))
    if m is None:
        m = bpy.data.materials.new('t18_rim_' + os.path.basename(path)); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
        out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); t = N('ShaderNodeTexImage')
        t.image = bpy.data.images.load(path, check_existing=True); t.image.alpha_mode = 'STRAIGHT'; t.extension = 'CLIP'
        em.inputs['Color'].default_value = (0.55, 0.78, 1.0, 1.0); em.inputs['Strength'].default_value = 1.7          # a flat pale sky-blue (170, 210, 255): the silhouette, not the dark ink
        L(t.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
        m.cycles.emission_sampling = 'NONE'
    return m


def rim(meta, pos, cam_loc, mirror=False, height=None, scale=None, name='rim', yaw_off=0.0, tint=(0.35, 0.62, 1.0), k=1.3, back=0.05):
    """cool sky-blue rim from behind: a blue-tinted copy of the card, 4 % larger, pushed 0.07 D away from the lens (it shows as an outline round the silhouette)."""
    p = V(pos); d = V(cam_loc) - p; d.z = 0; d.normalize()
    q = p - d * back + V((0, 0, -0.0))
    sc = (height / meta['height'] if height is not None else (scale or 1.0)) * 1.028
    ob = c18.put(meta, tuple(q), cam_loc, scale=sc, mirror=mirror, name=name, yaw_off=yaw_off, tint=tint, k=k, sw=0.01)
    ob.data.materials[0] = rim_mat(meta['path'])
    return ob


def _smoke_mat():
    m = bpy.data.materials.get('t18_smoke')
    if m is None:
        m = bpy.data.materials.new('t18_smoke'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
        out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
        em.inputs['Color'].default_value = (0.78, 0.74, 0.76, 1.0); em.inputs['Strength'].default_value = 0.9; mx.inputs['Fac'].default_value = 0.45
        L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    return m


SMOKE = []
for _i in range(4 * 4):
    _bpy_me = bpy.data.meshes.new('t18_smk_%d' % _i)
    import bmesh as _bm
    _b_ = _bm.new(); _bm.ops.create_uvsphere(_b_, u_segments=12, v_segments=8, radius=1.0); _b_.to_mesh(_bpy_me); _b_.free()
    for _p in _bpy_me.polygons: _p.use_smooth = True
    _bpy_me.materials.append(_smoke_mat())
    _o = bpy.data.objects.new('t18_smk_%d' % _i, _bpy_me); STATE['SET'].objects.link(_o); _o.visible_shadow = False; J.no_bounce(_o); SMOKE.append(_o)


def tail_smoke(i, pos, cam_loc, mirror, yaw_off, g, sc=1.08):
    d = V(cam_loc) - V(pos); yaw = math.atan2(d.x, -d.y) + math.radians(yaw_off)
    ux, uy = math.cos(yaw), math.sin(yaw); sgn = -1.0 if mirror else 1.0
    tx = pos[0] + ux * (-2.19 * sc) * sgn; ty = pos[1] + uy * (-2.19 * sc) * sgn; tz = 2.38 * sc
    for j in range(4):
        o = SMOKE[i * 4 + j]; u = ((g * 0.045 + j * 0.25 + i * 0.13) % 1.0)
        o.location = (tx + ux * (-0.35 * sgn) * u * 3 + 0.15 * math.sin(g * 0.3 + j), ty + uy * (-0.35 * sgn) * u * 3 - 0.45 * u * 2, tz + 0.2 + 1.6 * u)
        r = 0.22 + 0.55 * u; o.scale = (r, r, r * 0.9); o.hide_render = u > 0.97


def _near_hide(cam, r=9.0):
    """the dark octagonal torch-stake posts of the road dressing slid past the lens as the crane came down (gate 17): hide any post within r D of the camera, every frame."""
    for o in bpy.data.objects:
        if o.type == 'MESH' and (o.name.startswith('stk') or o.name.startswith('flame_stk')):
            c = o.matrix_world @ (sum((V(b) for b in o.bound_box), V((0, 0, 0))) / 8.0)
            o.hide_render = (c - cam).length < r


def frame(T, g):
    _near_hide(V(T.cur['loc']))
    gx, gy = _gen_pos(g); u_ = c18.ease((g - G0) / float(G_ZOOM - G0)) if G0 < g < G_ZOOM else (0.0 if g <= G0 else 1.0)
    POOL.location = (gx, gy + 1.5, 0.08); k = 2.4 + 15.0 * (1.0 - u_) ** 2; POOL.scale = (k, k, 1.0); POOL2.location = (gx, gy + 1.5, 0.1); POOL2.scale = (0.55 * k, 0.55 * k, 1.0)       # a warm dawn pool of light under him: findable in the wide
    cam = V(T.cur['loc']); dy = SPEED * (g - G0) / 30.0
    gen = V((_gen_pos(g)[0], -50.0 - dy, 0.0))
    heads = []
    ph = (g * 0.0625) % 1.0; i16 = int(ph * 16)
    lb = 2070 <= g <= 2080                                                            # head turned back over the shoulder g 2070-2080
    pose = dict(cast18.general_run_scream_frame(ph, facing=-1, lookback=lb)); pose['t'] = g / 30.0
    wob = int(round(math.sin(g * 0.55) * 4))                                   # helmet wobble + cup slosh every few frames (quantised so cards are reused)
    pose['hat_askew'] = 24 + 5 * wob; pose['cup_tilt'] = 22 * wob
    pose['prop_r'] = dict(pose['prop_r'], scale=pose['prop_r'].get('scale', 1.0) * 0.62)    # the cup was head-sized: 62 %
    m = c18.pcard('general', pose, 'gs%02d_%d_%d' % (i16, int(lb), wob))
    rim(m, tuple(gen), cam, height=3.4, name='grim')
    c18.put(m, tuple(gen), cam, height=3.4, name='general', sw=1.0)
    heads.append(T.head_row(tuple(gen), 3.4, 'general'))
    u = c18.ramp(g, G0, 2085)
    for i in range(4):
        back = OX_START[i] + (OX_END[i] - OX_START[i]) * u
        lat = OX_LAT[i] * (1.0 - 0.35 * u)
        if i == 0:
            lat = c18.lerp(-1.5, 2.0, c18.ramp(g, 2040, 2100))       # the nearest ox ends at screen-right of him: its face shows at his shoulder at the cut
        pos = gen + V((lat, back, 0.0))
        phase = (int(g / 2.5) + i * 3) % 8
        mo = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=None, face='rage')
        mo_ns = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=None, face='rage')      # the rim copy has NO smoke (its faint alpha showed as pale rectangles)
        mo_ns = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=None, face='rage')
        rim(mo_ns, tuple(pos), cam, scale=1.08, mirror=bool(i % 2), name='orim%d' % i, yaw_off=(10 if i % 2 else -10))
        tail_smoke(i, tuple(pos), cam, bool(i % 2), (10 if i % 2 else -10), g)
        c18.put(mo, tuple(pos), cam, scale=1.08, mirror=bool(i % 2), name='ox%d' % i, sw=2.7, yaw_off=(10 if i % 2 else -10))
        heads.append(T.head_row(tuple(pos), 2.6, 'ox'))
        if i == 0:
            heads.append(dict(role='oxmouth', chin=round(T.project((pos.x, pos.y, 0.80))[1])))
    return dict(heads=heads)


# one dark, lit foreground prop low in the bottom-left corner: a dropped bronze helmet (J.prop_helmet), parented to nothing, keyed per frame in frame()
HELM = J.prop_helmet((0.0, 0.0, 0.0), rot=0.0, scale=0.5)


def corner_helmet(g):
    dy = SPEED * (g - G0) / 30.0
    cam = T.cur['loc']
    J._xf(HELM, loc=(cam[0] - 1.5, cam[1] + 2.6, 0.0), rot=(0.0, 0.0, 0.7))


_f0 = frame
def frame(T, g):
    HELM.hide_render = g < 2046
    corner_helmet(g)
    return _f0(T, g)


T.run(frame, gs=rng, force=(mode == 'draft'))
