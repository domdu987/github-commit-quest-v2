#!/usr/bin/env python3
"""office_mech.py : build-order steps 2 and 9 of the shot plan (the mechanism on the wall map, shots 19-22).
An EXTENSION of the office set: imports v3/set3d/office3d.py, v3/set3d_ext/props/office_props.py and v3/set3d_ext/light/office_light.py
and edits none of them.  See API.md next to this file.

    import office3d as S, office_props as X, office_light as OL, office_mech as M
    A = S.build('INTERIOR_DAY'); PA = X.build(A, hi_map=True)
    MA = M.build(A, PA, wall_height=0.55)      # collection MECH + control empty 'mech_ctl'
    OL.apply('office_grey')                    # AFTER M.build, so the new materials get the grey ambient
    M.set_wall('E', rise=4, slide=1, lock=1, frame=None)    # every setter: frame=None sets statically, frame=N inserts keys
    S.make_camera(M.cam('corridor', u_lens=-0.12))
"""
import os, sys, math, json
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
for p in (os.path.join(PROJ, 'v3', 'set3d'), os.path.join(PROJ, 'v3', 'set3d_ext', 'props'), os.path.join(PROJ, 'v3', 'set3d_ext', 'light')):
    if p not in sys.path: sys.path.insert(0, p)
import office3d as S                      # noqa: E402
import office_props as X                  # noqa: E402

TEXD = os.path.join(HERE, 'tex')
MAP_Y = S.MAP_Y                           # paper surface plane y = -0.05
STATE = {}

# ----------------------------------------------------------------------------- the track frame (HAND-DRAWN line, client decision)
# The red line is the set's 85-point freehand stroke (office3d TRACK_STYLE "hand"): it leaves the storm heading north-west, bows up
# to 0.155 D WEST of the straight chord near u 0.5 and comes back north-north-east into N.Y.  Everything that sits on or along
# the line is placed from S.track_point(u) through this frame, never from the chord:
#   chord frame  : T0 (storm symbol), TDIR (chord direction, north), NDIR (across the chord, east), YDIR (+y, into the wall);
#                  sc = position along the chord, lateral = across it.  The line is a graph over the chord: lateral = DEV(sc).
#   world(a, s, h, u): the point `a` D east of the LINE at u, i.e. lateral = line(sc) + a * KF(sc) (KF = 1/cos of the local slope,
#                  so `a` is the distance across the line), h D proud of the paper.  a = 0 is exactly on the red line; for |a| >=
#                  LANE_HALF the lightly smoothed line (DEVS) is used, so lane edges and wall faces are smooth curves 0.11 D off the line.
T0 = Vector(S.track_point(0.0)); T1 = Vector(S.track_point(1.0))
CHORD = (T1 - T0).length                                      # 1.016 D (chord)
TDIR = (T1 - T0).normalized()                                 # along the chord, north (map plane)
NDIR = Vector((TDIR.z, 0.0, -TDIR.x))                         # across the chord, toward the east (+x side)
YDIR = Vector((0.0, 1.0, 0.0))                                # into the wall; -YDIR = out of the paper, toward the room

def _track_table(n=541, sigma=0.035):
    us = [i / (n - 1) for i in range(n)]; P = [Vector(S.track_point(u)) for u in us]
    sc = [(p - T0).dot(TDIR) for p in P]; dv = [(p - T0).dot(NDIR) for p in P]
    arc = [0.0]
    for i in range(1, n): arc.append(arc[-1] + (P[i] - P[i - 1]).length)
    # smoothed line (gaussian in sc, ends pinned): the lane edges and the corridor faces follow it
    m = 200; g = [CHORD * i / (m - 1) for i in range(m)]
    def raw(x): return _interp1(sc, dv, x)
    e = 0.04; k0 = (raw(e) - raw(0.0)) / e; k1 = (raw(CHORD) - raw(CHORD - e)) / e     # end slopes: extend the line straight
    def ext(y): return raw(y) if 0 <= y <= CHORD else (k0 * y if y < 0 else k1 * (y - CHORD))
    ds = []
    for x in g:
        w = 0.0; acc = 0.0
        for j in range(-12, 13):
            y = x + j * sigma / 4.0; k = math.exp(-0.5 * (j / 4.0) ** 2)
            w += k; acc += k * ext(y)
        ds.append(acc / w)
    sl = [(ds[min(m - 1, i + 1)] - ds[max(0, i - 1)]) / (g[min(m - 1, i + 1)] - g[max(0, i - 1)]) for i in range(m)]
    return dict(u=us, sc=sc, dev=dv, arc=arc, g=g, devs=ds, slope=sl)

def _interp1(xs, ys, x):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x: lo = mid
        else: hi = mid
    t = (x - xs[lo]) / ((xs[hi] - xs[lo]) or 1); return ys[lo] + (ys[hi] - ys[lo]) * t

TT = _track_table()
TLEN = TT['arc'][-1]                                          # 1.076 D: length of the hand-drawn line (u is by arc length)

def sc_of_u(u):
    """Chord coordinate of track fraction u (u < 0 / > 1 extend along the chord beyond the ends)."""
    if u < 0: return u * TLEN
    if u > 1: return CHORD + (u - 1) * TLEN
    return _interp1(TT['u'], TT['sc'], u)

def u_of_sc(sc):
    if sc < 0: return sc / TLEN
    if sc > CHORD: return 1 + (sc - CHORD) / TLEN
    return _interp1(TT['sc'], TT['u'], sc)

def dev(sc):
    """Lateral offset (D, + = east) of the RED LINE from the chord at chord coordinate sc (0 outside the ends)."""
    return _interp1(TT['sc'], TT['dev'], sc) if 0 <= sc <= CHORD else 0.0

def dev_s(sc):
    """The same for the lightly smoothed line (sigma 0.035 D) that the lane edges and corridor faces follow."""
    return _interp1(TT['g'], TT['devs'], sc) if 0 <= sc <= CHORD else 0.0

def slope(sc):
    return _interp1(TT['g'], TT['slope'], sc) if 0 <= sc <= CHORD else 0.0

def kf(sc): return math.sqrt(1.0 + slope(sc) ** 2)

def lateral(a, sc):
    """Lateral (chord frame) of the point `a` D east of the line at chord coordinate sc."""
    w = max(0.0, 1.0 - abs(a) / LANE_HALF)
    return dev_s(sc) + a * kf(sc) + (dev(sc) - dev_s(sc)) * w

def world_sc(lat, sc, h=0.0):
    """World point from chord-frame coordinates (lateral, sc) and height h."""
    return tuple(Vector((T0.x, MAP_Y, T0.z)) + lat * NDIR + sc * TDIR - h * YDIR)

def world(a, s, h=0.0, u=None):
    """World point `a` D east of the hand-drawn line (negative = west), `s` D along it from the storm symbol (or u = fraction of the
    track by arc length, as S.track_point), `h` D proud of the paper.  a = 0, h = 0 is on the red line (within 0.1 mm)."""
    if u is None: u = s / TLEN
    sc = sc_of_u(u); return world_sc(lateral(a, sc), sc, h)

def tangent(u):
    """Unit direction of the (smoothed) line at u, north-going, in the map plane."""
    t = TDIR + slope(sc_of_u(u)) * NDIR; return t.normalized()

def east(u):
    """Unit direction across the line at u, toward the east (map plane)."""
    t = tangent(u); return Vector((t.z, 0.0, -t.x))

def frame(u):
    """(point on the line, tangent north, east) at u: what a prop that sits ON the line uses."""
    return Vector(world(0, 0, 0, u=u)), tangent(u), east(u)

def track_frame_matrix():
    """3x3 rotation of the CHORD frame: local X = east across the chord, local Y = into the wall (+y), local Z = north along it.
    (The wall meshes are built in it; their vertices follow the line through lateral().)"""
    return Matrix((NDIR, YDIR, TDIR)).transposed()

# ----------------------------------------------------------------------------- geometry constants (all D)
LANE_HALF = 0.11                       # lane 0.22 D wide: the corridor faces of the locked walls stand at a = +-0.11
U_WALL = (0.05, 0.92)                  # walls flank the track from u 0.05 to 0.92
SLIDE_OUT = 0.15                       # slide 0: each wall stands this much further out; slide 1: on its line
LOCK_STEP = 0.035                      # lock 0: step k stands k x this further out (stepped corridor face); lock 1: vertical face
LOCK_MIN = 0.006                       # even locked, step k stands k x 6 mm back: no coplanar faces, and the ink edges draw the terrace lines on the face
STEPS = 4
WALL_W = {'E': (0.72, 0.56, 0.42, 0.30), 'W': (0.50, 0.40, 0.31, 0.23)}   # width of step k (inner edge aligned on the corridor face)
END_INSET = 0.055                      # each step is shorter by this at both ends
CORNER = (0.16, 0.13, 0.10, 0.08)      # corner radius of each step (contour-like rounded ends)
WALL_COL = {'E': '#c4c6d4', 'W': '#cac6d2'}   # pale paper blue (Atlantic) / blue-lavender (land): violet-blue paper, kept out of the violet hue band
H_COL = '#2c3f74'                      # the big Latin H (printed-map navy)

# ----------------------------------------------------------------------------- textures (PIL, cached in tex/)
def _textures():
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    os.makedirs(TEXD, exist_ok=True); out = {}
    INK = (42, 23, 18, 255)
    def save(im, name): p = os.path.join(TEXD, name); im.save(p); out[name.split('.')[0]] = p
    # 1. the big Latin H (DejaVu Serif Bold), navy ink, transparent
    p = os.path.join(TEXD, 'H.png')
    if not os.path.exists(p):
        W = 512; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 430)
        bb = d.textbbox((0, 0), 'H', font=f); x = (W - (bb[2] - bb[0])) / 2 - bb[0]; y = (W - (bb[3] - bb[1])) / 2 - bb[1]
        c = tuple(int(H_COL[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
        d.text((x, y), 'H', font=f, fill=c, stroke_width=6, stroke_fill=c); im.save(p)
    out['H'] = p
    # 2. wind arrow: a pale cream chevron arrowhead with a soft tail streak and an ink edge (points to +v = up in the image)
    p = os.path.join(TEXD, 'wind_arrow.png')
    if not os.path.exists(p):
        W, Hh = 256, 512; im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for k in range(40):                                 # tail streak, fading toward the bottom
            a = int(150 * (1 - k / 40)); y0 = 230 + k * 7
            d.rectangle([W / 2 - 14 + k * 0.2, y0, W / 2 + 14 - k * 0.2, y0 + 7], fill=(246, 240, 226, a))
        chev = [(W / 2, 20), (W - 18, 250), (W / 2 + 40, 250), (W / 2, 150), (W / 2 - 40, 250), (18, 250)]
        d.polygon(chev, fill=(250, 246, 236, 255), outline=INK); d.line(chev + [chev[0]], fill=INK, width=9, joint='curve')
        im.save(p)
    out['wind_arrow'] = p
    # 3. isobar rings for the spinner (pulse card): three dark blue-grey circles
    p = os.path.join(TEXD, 'rings.png')
    if not os.path.exists(p):
        W = 1024; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for r, w in ((230, 12), (340, 10), (460, 9)):
            d.ellipse([W / 2 - r, W / 2 - r, W / 2 + r, W / 2 + r], outline=(52, 72, 110, 235), width=w)
        im.save(p)
    out['rings'] = p
    # 4. sweat drop: pale blue drop with an ink outline and a highlight (tip up)
    p = os.path.join(TEXD, 'drop.png')
    if not os.path.exists(p):
        W, Hh = 256, 360; im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        poly = []
        for i in range(60):
            t = 2 * math.pi * i / 60; r = 1.0
            x = math.sin(t) * 95 * (0.18 + 0.82 * ((1 - math.cos(t)) / 2) ** 0.6); y = -math.cos(t) * 150
            poly.append((W / 2 + x, Hh / 2 + 20 + y))
        d.polygon(poly, fill=(150, 205, 245, 255)); d.line(poly + [poly[0]], fill=INK, width=12, joint='curve')
        d.ellipse([W / 2 - 40, Hh / 2 + 30, W / 2 - 10, Hh / 2 + 80], fill=(255, 255, 255, 230))
        im.save(p)
    out['drop'] = p
    # 5. snail shell (for one ghost spinner): cream-brown spiral shell, ink outline
    p = os.path.join(TEXD, 'shell.png')
    if not os.path.exists(p):
        W = 512; im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([40, 40, W - 40, W - 40], fill=(214, 176, 120, 255), outline=INK, width=14)
        pts = []
        for i in range(260):
            t = i / 259 * 3.2 * 2 * math.pi; r = 200 * (1 - i / 259) + 6
            pts.append((W / 2 + r * math.cos(t), W / 2 + r * math.sin(t)))
        d.line(pts, fill=(110, 70, 40, 255), width=14, joint='curve'); im.save(p)
    out['shell'] = p
    return out

# ----------------------------------------------------------------------------- material and key helpers
def _lit(key, color='#808080', image=None, gain=0.35, shade_mul=1.0, alpha=False, form=True):
    P = S.STATE['P']; f = tuple(P.get('form', (0, 0, 0))) if form else None
    return S.mat_lit(S.STATE['preset'] + '_mx_' + key, color, image=image, gain=gain, shade_mul=shade_mul, alpha=alpha, form=f)

def _ctl(): return STATE['ctl']

def _drv(nt, prop, expr='v'):
    n = nt.nodes.new('ShaderNodeValue'); n.name = 'drv_' + prop
    fc = n.outputs[0].driver_add('default_value'); d = fc.driver; d.type = 'SCRIPTED'
    v = d.variables.new(); v.name = 'v'; v.type = 'SINGLE_PROP'; v.targets[0].id = _ctl(); v.targets[0].data_path = '["%s"]' % prop
    d.expression = expr; return n.outputs[0]

_math = X._math; _alpha_mask = X._alpha_mask; _uv_x = X._uv_x; _interp = X._interp

def _setp(prop, value, frame=None, interp='LINEAR'):
    c = _ctl(); c[prop] = float(value)
    if frame is not None: c.keyframe_insert('["%s"]' % prop, frame=frame); _interp(c, '["%s"]' % prop, frame, interp)
    c.update_tag()

def _key(ob, frame, loc=True, rot=True, scale=True):
    if frame is None: return
    for on, path in ((loc, 'location'), (rot, 'rotation_euler'), (scale, 'scale')):
        if on: ob.keyframe_insert(path, frame=frame); _interp(ob, path, frame, 'LINEAR')

def _vis(ob, visible, frame):
    for o in [ob] + list(ob.children_recursive):
        o.hide_render = not visible
        if frame is not None: o.keyframe_insert('hide_render', frame=frame); _interp(o, 'hide_render', frame, 'CONSTANT')

def _empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); STATE['coll'].objects.link(e); e.location = loc; e.empty_display_size = 0.04
    if parent: e.parent = parent
    STATE['objects'][name] = e; return e

def _mesh(name, V, F, mat, uvs=None, mats=None, mi=None):
    me = bpy.data.meshes.new(name); me.from_pydata([Vector(v) for v in V], [], F); me.update()
    if uvs is not None:
        uvl = me.uv_layers.new(name='UVMap'); i = 0
        for fi, f in enumerate(F):
            for c in uvs[fi]: uvl.data[i].uv = c; i += 1
    for m in (mats or [mat]): me.materials.append(m)
    if mi:
        for fi, p in enumerate(me.polygons): p.material_index = mi[fi]
    ob = bpy.data.objects.new(name, me); STATE['coll'].objects.link(ob); STATE['objects'][name] = ob; return ob

def _quad(name, w, h, mat, origin=(0.5, 0.5)):
    """Quad w x h in local XZ facing local -Y; `origin` = pivot as a fraction from the left and from the BOTTOM."""
    ox, oz = origin[0] * w, origin[1] * h
    V = [(-ox, 0, -oz), (w - ox, 0, -oz), (w - ox, 0, h - oz), (-ox, 0, h - oz)]
    return _mesh(name, V, [(0, 1, 2, 3)], mat, uvs=[[(0, 0), (1, 0), (1, 1), (0, 1)]])

def _ink_mat(key, fade_prop):
    """Ink outline material for an inverted hull, camera rays only, opacity follows fade_prop."""
    name = S.STATE['preset'] + '_mx_ink_' + key
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*S.hex_lin('#2a1712'), 1)
    lp = nt.nodes.new('ShaderNodeLightPath'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    geo = nt.nodes.new('ShaderNodeNewGeometry')            # Cycles has no material backface culling: the hull shows only its front faces
    fac = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', lp.outputs['Is Camera Ray'], _math(nt, 'SUBTRACT', 1.0, geo.outputs['Backfacing'])), _drv(nt, fade_prop))
    nt.links.new(fac, mx.inputs['Fac']); nt.links.new(tr.outputs['BSDF'], mx.inputs[1]); nt.links.new(em.outputs['Emission'], mx.inputs[2])
    nt.links.new(mx.outputs['Shader'], out.inputs['Surface']); m.use_backface_culling = True
    m.cycles.emission_sampling = 'NONE'; return m

def _hull(ob, mat, t):
    ob.data.materials.append(mat); mod = ob.modifiers.new('ink_hull', 'SOLIDIFY')
    mod.thickness = t; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(ob.data.materials) - 1; mod.use_even_offset = True

def _lit_color(m, sock):
    """Feed a colour socket into a mat_lit material (both the ambient and the key branch) instead of its flat colour."""
    nt = m.node_tree
    ms = next(n for n in nt.nodes if n.bl_idname == 'ShaderNodeMix' and n.blend_type == 'MULTIPLY')
    md = next(n for n in nt.nodes if n.bl_idname == 'ShaderNodeVectorMath' and n.operation == 'SCALE' and n.inputs['Scale'].links
              and n.inputs['Scale'].links[0].from_node.bl_idname == 'ShaderNodeMath')
    nt.links.new(sock, ms.inputs[6]); nt.links.new(sock, md.inputs[0])

def _rgb(nt, hexcol):
    n = nt.nodes.new('ShaderNodeRGB'); n.outputs[0].default_value = (*S.hex_lin(hexcol), 1.0); return n.outputs[0]

def _mixc(nt, fac, a, b):
    n = nt.nodes.new('ShaderNodeMix'); n.data_type = 'RGBA'; nt.links.new(fac, n.inputs[0]); nt.links.new(a, n.inputs[6]); nt.links.new(b, n.inputs[7]); return n.outputs[2]

def _add_glow(m, color_sock, strength_sock):
    """Add an emission (camera rays) on top of the material's surface: the 'neon' of the lane dashes, the ping of the compass."""
    nt = m.node_tree; out = next(n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial')
    src = out.inputs['Surface'].links[0].from_socket; em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(color_sock, em.inputs['Color'])
    nt.links.new(strength_sock, em.inputs['Strength']); ad = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(src, ad.inputs[0]); nt.links.new(em.outputs['Emission'], ad.inputs[1]); nt.links.new(ad.outputs['Shader'], out.inputs['Surface'])

# ----------------------------------------------------------------------------- build
DEFAULTS = dict(wallE_fade=1.0, wallW_fade=1.0, lane_grow=0.0, lane_red=0.0, lane_fuse=0.0, lane_alpha=1.0, lane_glow=0.0,
                compass_alpha=1.0, compass_glow=0.0, ring_alpha=0.0, drop_alpha=0.0, wind_alpha=1.0,
                wake_head=0.0, wake_len=0.0, wake_alpha=0.0, picto_alpha=1.0, sign_alpha=1.0)

def build(A=None, PA=None, wall_height=0.55):
    """Add the mechanism to the current scene after office3d.build() and office_props.build(). Call office_light.apply() after it.
    wall_height = height of the top terrace above the paper at rise 4 (the gate fixed it, see API.md). Returns MA (cams, anchors)."""
    scene = bpy.context.scene; A = A or S.STATE['A']; PA = PA or X.STATE['PA']
    coll = S._coll('MECH', scene); S._wipe(coll)
    for m in list(bpy.data.materials):
        if '_mx_' in m.name: bpy.data.materials.remove(m)
    STATE.clear(); STATE.update(coll=coll, objects={}, A=A, PA=PA, H=float(wall_height))
    ctl = bpy.data.objects.new('mech_ctl', None); coll.objects.link(ctl); ctl.hide_render = True; STATE['ctl'] = ctl; STATE['objects']['mech_ctl'] = ctl
    for k, v in DEFAULTS.items(): ctl[k] = float(v)
    STATE['tex'] = _textures()
    _build_walls(); _build_lane(); _build_compass(); _build_pictos(); _build_wind(); _build_sign(); _build_spinner_fx(); _build_wake(); _build_shell()
    for ob in coll.objects:
        if ob.type == 'MESH': S.no_bounce(ob)
    reset()
    MA = dict(cams=cams(), wall_height=STATE['H'], lane_half=LANE_HALF, u_wall=U_WALL, sign_u=0.62, compass_xz=COMPASS_XZ,
              track_dir=tuple(TDIR), east_dir=tuple(NDIR))
    STATE['MA'] = MA; return MA

def reset():
    """Everything of the mechanism hidden / at 0 (walls sunk, lane not grown, signs and arrows hidden)."""
    for k, v in DEFAULTS.items(): _ctl()[k] = float(v)
    for sd in 'EW': set_wall(sd, rise=0.0, slide=0.0, lock=0.0)
    set_lane(0.0); set_compass(show=0); set_picto('E', show=0); set_picto('W', show=0); set_wind(0.0, amount=0)
    set_speed_sign(show=0); set_spinner_fx(ring=0, drop=0); set_wake(0, 0, 0); set_shell(0)

# ---- pressure walls
def _stadium(a0, a1, s0, s1, r, seg=7, r_in=None, inner='a0'):
    """Rounded rectangle in (a, s) (list of (a, s)); the two corners on the `inner` edge ('a0' or 'a1', the corridor side) take
    radius r_in (small, so the corridor face runs straight almost to the wall ends), the outer ones r (contour-like round ends)."""
    lim = min((a1 - a0) / 2, (s1 - s0) / 2) - 1e-4; r = min(r, lim); ri = min(r if r_in is None else r_in, lim); pts = []
    for (ca_o, cs, t0, edge) in ((a1, s0, -90, 'a1'), (a1, s1, 0, 'a1'), (a0, s1, 90, 'a0'), (a0, s0, 180, 'a0')):
        rr = ri if edge == inner else r; ca = ca_o - rr if edge == 'a1' else ca_o + rr; cs_ = cs + rr if cs == s0 else cs - rr
        for i in range(seg + 1):
            t = math.radians(t0 + 90 * i / seg); pts.append((ca + rr * math.cos(t), cs_ + rr * math.sin(t)))
    return pts

def _densify(poly, step=0.012):
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]; L = math.hypot(q[0] - p[0], q[1] - p[1]); n = max(1, int(math.ceil(L / step)))
        for j in range(n): out.append((p[0] + (q[0] - p[0]) * j / n, p[1] + (q[1] - p[1]) * j / n))
    return out

def wall_shift(sd):
    """Outward shift (D) of the outer edge of wall sd so that no terrace is narrower than its nominal width where the hand-drawn
    line bows toward that wall (W: 0.155 D, the line bows west; E: about 0)."""
    sign = 1.0 if sd == 'E' else -1.0; s0w, s1w = sc_of_u(U_WALL[0]), sc_of_u(U_WALL[1])
    return max(0.0, max(sign * dev_s(s0w + (s1w - s0w) * i / 60.0) for i in range(61)))

def warp(sd, a, sc):
    """Chord-frame lateral of the virtual wall point (a, sc): a = +-LANE_HALF is the corridor face, exactly LANE_HALF off the
    (smoothed) hand-drawn line; the outer edge (|a| = LANE_HALF + width of the bottom terrace) is a straight contour parallel to the
    chord, shifted out by wall_shift(sd); in between the offset blends linearly (upper terraces half follow the line, like contours)."""
    sign = 1.0 if sd == 'E' else -1.0; W0 = WALL_W[sd][0]; D = STATE.get('shift_' + sd, wall_shift(sd))
    t = max(0.0, min(1.0, (abs(a) - LANE_HALF) / W0))
    return (dev_s(sc) + a * kf(sc)) * (1 - t) + (a + sign * D) * t

def _build_walls():
    H = STATE['H']; hs = H / STEPS; s0w, s1w = sc_of_u(U_WALL[0]), sc_of_u(U_WALL[1])
    rot = track_frame_matrix().to_euler()
    hmat = _lit('Hdecal', image=STATE['tex']['H'], gain=0.30, alpha=True)
    STATE['walls'] = {}
    for sd, sign in (('E', 1.0), ('W', -1.0)):
        STATE['shift_' + sd] = wall_shift(sd)
        fade = 'wall%s_fade' % sd
        body = _lit('wall_' + sd, WALL_COL[sd], gain=0.32, shade_mul=1.0)
        _alpha_mask(body, _drv(body.node_tree, fade))
        hm = hmat.copy(); hm.name = S.STATE['preset'] + '_mx_Hdecal_' + sd; _alpha_mask(hm, _drv(hm.node_tree, fade))
        ink = _ink_mat('wall_' + sd, fade)
        root = _empty('wall%s_root' % sd, world_sc(0, 0, -0.0005)); root.rotation_euler = rot
        steps = []
        for k in range(STEPS):
            w = WALL_W[sd][k]; a_in = sign * LANE_HALF; a_out = sign * (LANE_HALF + w)
            a0, a1 = min(a_in, a_out), max(a_in, a_out); s0, s1 = s0w + k * END_INSET, s1w - k * END_INSET
            poly = _stadium(a0, a1, s0, s1, CORNER[k], r_in=0.03, inner='a0' if sign > 0 else 'a1')
            poly = [(warp(sd, a, s), s) for a, s in _densify(poly)]; n = len(poly); top = (k + 1) * hs
            V = [(a, 0.0, s) for a, s in poly] + [(a, -top, s) for a, s in poly]
            F = []; UV = []
            F.append(tuple(range(n, 2 * n))); UV.append([(0, 0)] * n)
            for i in range(n):
                j = (i + 1) % n; F.append((i, j, n + j, n + i)); UV.append([(0, 0)] * 4)
            ob = _mesh('wall%s_step%d' % (sd, k), V, F, body, uvs=UV)
            me = ob.data; me.update()
            c = me.polygons[0]
            if c.normal.y > 0:
                for p in me.polygons: p.flip()
            me.update()
            ob.parent = root; ob.location = (0, 0, 0)
            _hull(ob, ink, 0.0035)
            steps.append(ob)
        # Latin H: on the top terrace (facing the room) and on the corridor face of the top two steps (a strip bent along the face)
        k = STEPS - 1; w = WALL_W[sd][k]; sc_m = (s0w + s1w) / 2; hsz = min(w * 0.8, 0.26)
        ht = _quad('wall%s_H_top' % sd, hsz, hsz, hm); ht.parent = steps[k]
        ht.location = (warp(sd, sign * (LANE_HALF + w / 2), sc_m), -(H + 0.002), sc_m); ht.rotation_euler = (0, 0, 0); ht.visible_shadow = False
        hw = H * 0.62; ncol = 12; V = []; F = []; UV = []
        for i in range(ncol + 1):
            f = i / ncol; s_ = sc_m + sign * (f - 0.5) * hw          # image left -> right as read from inside the lane
            lat = warp(sd, sign * LANE_HALF, s_) - sign * 0.004
            V += [(lat, -H * 0.5 + hw / 2, s_), (lat, -H * 0.5 - hw / 2, s_)]
        for i in range(ncol):
            a_, b_ = 2 * i, 2 * i + 2; F.append((a_, b_, b_ + 1, a_ + 1)); UV.append([(i / ncol, 0), ((i + 1) / ncol, 0), ((i + 1) / ncol, 1), (i / ncol, 1)])
        hf = _mesh('wall%s_H_face' % sd, V, F, hm, uvs=UV); hf.parent = root; hf.visible_shadow = False
        nrm_ok = hf.data.polygons[ncol // 2].normal.x * (-sign) > 0
        if not nrm_ok:
            for p in hf.data.polygons: p.flip()
        # scale pivot of the stamp: the centre of the strip
        cx = warp(sd, sign * LANE_HALF, sc_m) - sign * 0.004
        for v in hf.data.vertices: v.co.x -= cx; v.co.y += H * 0.5; v.co.z -= sc_m
        hf.location = (cx, -H * 0.5, sc_m)
        STATE['walls'][sd] = dict(root=root, steps=steps, sign=sign, H_top=ht, H_face=hf)
        STATE['wall_state_%s' % sd] = dict(rise=0.0, slide=0.0, lock=0.0, pulse=0.0)

def face_basis(nrm, up):
    """Rotation for a _quad: its visible side faces `nrm`, its image up is `up` (orthogonalised). Right-handed."""
    n = Vector(nrm).normalized(); Y = -n; Z = (Vector(up) - n * Vector(up).dot(n)).normalized(); Xv = Y.cross(Z)
    return Matrix((Xv, Y, Z)).transposed()

def _smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def set_wall(side, rise=None, slide=None, lock=None, fade=None, pulse=None, frame=None):
    """One pressure wall. side 'E' (Atlantic, east of the line) or 'W' (land).
    rise 0..4: the four terraces swell out of the paper one after another (step k grows during rise k..k+1; 4 = full height);
    slide 0..1: 0 = the wall stands SLIDE_OUT (0.15 D) further out, 1 = its corridor face on the lane edge (0.11 D from the line);
    lock 0..1: 0 = stepped corridor face (each terrace set back 0.035 D), 1 = the face vertical (locked);
    fade 0..1: opacity of the wall (body, ink edges and H);  pulse: height x (1 + 0.15 pulse) (the reveal pulse of shot 22).
    Arguments left None keep the last value. Every call with frame=N keys all of it."""
    W = STATE['walls'][side]; st = STATE['wall_state_%s' % side]
    for k_, v in (('rise', rise), ('slide', slide), ('lock', lock), ('pulse', pulse)):
        if v is not None: st[k_] = float(v)
    sign = W['sign']; root = W['root']; H = STATE['H']; hs = H / STEPS
    off = sign * SLIDE_OUT * (1 - st['slide'])
    root.location = Vector(world_sc(0, 0, -0.0005)) + off * NDIR
    root.scale = (1, 1 + 0.15 * st['pulse'], 1)
    for k, ob in enumerate(W['steps']):
        e = _smooth(st['rise'] - k); vis = st['rise'] - k > 1e-3
        top = hs * (k + e); sy = max(1e-4, top / ((k + 1) * hs))
        ob.scale = (1, sy, 1); ob.location = (sign * k * (LOCK_MIN + (LOCK_STEP - LOCK_MIN) * (1 - st['lock'])), 0, 0)
        _key(ob, frame, rot=False); _vis(ob, vis, frame)
    hf = W['H_face']; e = _smooth((st['lock'] - 0.3) / 0.7) * _smooth(st['rise'] - 3.0)       # the H is stamped on the face as it locks
    hf.scale = (max(1e-4, e),) * 3; _key(hf, frame, rot=False, loc=False); _vis(hf, e > 1e-3, frame)
    _key(root, frame, rot=False)
    if fade is not None or frame is not None: _setp('wall%s_fade' % side, fade if fade is not None else _ctl()['wall%s_fade' % side], frame)

# ---- lane (pale road with white dashes along both edges; the red line stays its centre line)
LANE_U = (0.04, 0.95)
def _build_lane():
    s0, s1 = LANE_U[0] * TLEN, LANE_U[1] * TLEN; L = s1 - s0; w = 2 * LANE_HALF; n = 180      # follows the hand-drawn line
    m = _lit('lane', '#efe7d2', gain=0.33, shade_mul=1.15); nt = m.node_tree
    ux, uy = _uv_x(nt); grow = _drv(nt, 'lane_grow'); red = _drv(nt, 'lane_red'); fuse = _drv(nt, 'lane_fuse')
    alpha = _drv(nt, 'lane_alpha'); glow = _drv(nt, 'lane_glow')
    dist = _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', uy, 0.5))                      # 0 centre .. 0.5 edge
    cen = _math(nt, 'MULTIPLY', _math(nt, 'SUBTRACT', 1.0, fuse), 0.36)               # dash lines at 0.36 of the half width -> 0 when fused
    band = _math(nt, 'LESS_THAN', _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', dist, cen)), 0.045)
    duty = _math(nt, 'ADD', 0.55, _math(nt, 'MULTIPLY', fuse, 0.46))
    dashp = _math(nt, 'LESS_THAN', _math(nt, 'FRACT', _math(nt, 'MULTIPLY', ux, L / 0.075)), duty)
    dash = _math(nt, 'MULTIPLY', band, dashp)
    # lane body fades out over the last 8 percent of the width (soft edge against the walls) and while fused
    body_a = _math(nt, 'MULTIPLY', _math(nt, 'LESS_THAN', dist, 0.47), _math(nt, 'SUBTRACT', 1.0, _math(nt, 'MULTIPLY', fuse, 0.85)))
    dcol = _mixc(nt, red, _rgb(nt, '#fbfaf4'), _rgb(nt, '#d0281c'))
    col = _mixc(nt, dash, _rgb(nt, '#efe7d2'), dcol)
    _lit_color(m, col)
    vis = _math(nt, 'LESS_THAN', ux, _math(nt, 'ADD', grow, 0.0005))
    a = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', vis, alpha), _math(nt, 'MAXIMUM', _math(nt, 'MULTIPLY', body_a, 0.82), dash))
    _alpha_mask(m, a)
    _add_glow(m, dcol, _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', dash, glow), vis))
    V = []; F = []; UV = []
    for i in range(n + 1):
        s = s0 + L * i / n
        V += [world(-LANE_HALF * 1.001, s, 0.0006), world(LANE_HALF * 1.001, s, 0.0006)]
    for i in range(n):
        a_, b_ = 2 * i, 2 * i + 2; F.append((a_, b_, b_ + 1, a_ + 1)); UV.append([(i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1)])
    ob = _mesh('lane', V, F, m, uvs=UV); ob.visible_shadow = False
    me = ob.data
    if me.polygons[0].normal.y > 0:
        for p in me.polygons: p.flip()

def set_lane(grow, red=None, fuse=None, alpha=None, glow=None, frame=None):
    """The pale lane with white dashes between the walls (u 0.04-0.95). grow 0..1 unrolls it from the south (the storm end) north;
    red 0..1 turns the dashes red; fuse 0..1 slides the two dash lines into the centre and closes their gaps (shot 22: they fuse into
    the pencil line, the pale body fades with it); alpha = opacity; glow = neon emission of the dashes (hum-on, about 0.6 then 0.15)."""
    _setp('lane_grow', grow, frame)
    for k, v in (('lane_red', red), ('lane_fuse', fuse), ('lane_alpha', alpha), ('lane_glow', glow)):
        if v is not None or frame is not None: _setp(k, v if v is not None else _ctl()[k], frame)

# ---- compass (Latin N), flat on the paper north-east of the lane end
COMPASS_XZ = (0.50, 2.86); COMPASS_D = 0.30
def _build_compass():
    m = _lit('compass', image=X.paper_png('compass', (0.3, 0.3), 700), gain=0.30, alpha=True); nt = m.node_tree
    _alpha_mask(m, _drv(nt, 'compass_alpha')); _add_glow(m, _rgb(nt, '#ff5a3c'), _math(nt, 'MULTIPLY', _drv(nt, 'compass_glow'), 0.0))
    root = _empty('compass_root', (COMPASS_XZ[0], MAP_Y - 0.0035, COMPASS_XZ[1]))
    q = _quad('compass', COMPASS_D, COMPASS_D, m); q.parent = root; q.visible_shadow = False

def set_compass(show=1.0, scale=0.8, rot_deg=0.0, ping=0.0, xz=None, frame=None):
    """Compass rose with a red N point, flat on the map (default COMPASS_XZ, scale 0.8 = 0.24 D). show 0/1 (also a pop scale);
    ping 0..1 = a scale bump x(1 + 0.35 ping) for the 45.15 ping (key 0 -> 1 -> 0 over 6 frames); rot_deg turns it (clockwise)."""
    r = STATE['objects']['compass_root']
    if xz is not None: r.location = (xz[0], MAP_Y - 0.0035, xz[1])
    s = max(1e-4, scale * show * (1 + 0.35 * ping)); r.scale = (s, s, s); r.rotation_euler = (0, math.radians(rot_deg), 0)
    _key(r, frame); _vis(r, show > 1e-3, frame)

# ---- no-turn pictograms on the corridor faces
def _build_pictos():
    for sd, name in (('E', 'no_right_turn'), ('W', 'no_left_turn')):
        m = _lit('picto_' + sd, image=X.paper_png(name, (0.22, 0.22), 600), gain=0.30, alpha=True); _alpha_mask(m, _drv(m.node_tree, 'picto_alpha'))
        root = _empty('picto%s_root' % sd); q = _quad('picto_' + sd, 0.22, 0.22, m); q.parent = root
        mb = S.MB(); post = _lit('picto_post', '#6b5a48', gain=0.4); mb.frustum((0, 0.0, 0), (0, 0.06, 0), 0.006, 0.006, post, seg=8)
        bob = mb.obj('picto%s_bracket' % sd, STATE['coll']); bob.parent = root; STATE['objects'][bob.name] = bob

def set_picto(side, show=1.0, scale=1.0, s=None, h=None, yaw_deg=35.0, wobble_deg=0.0, tilt_deg=0.0, frame=None):
    """Round no-turn pictogram on a short bracket, standing out of the corridor face of wall `side` ('E' = no right turn, 'W' = no left
    turn). s = D along the line (default: 0.05 D north of the spinner at u 0.10), h = height of its centre (default 0.62 x wall height);
    yaw_deg turns the card from facing straight across the lane toward the south (the camera behind the spinner); tilt_deg tips its
    face toward the room (for a camera above the walls: s19 uses W yaw 60 / tilt 35, seen from the south-west); show 0..1 pops it
    (scale), wobble_deg rocks it after the pop. The wall face it sits on is the LOCKED face (a = +-0.11)."""
    r = STATE['objects']['picto%s_root' % side]; sign = 1.0 if side == 'E' else -1.0
    s = 0.15 * TLEN if s is None else s; h = 0.62 * STATE['H'] if h is None else h
    p = Vector(world(sign * (LANE_HALF - 0.065), s, h)); r.location = p
    uu = s / TLEN; td, ed = tangent(uu), east(uu)                   # the local direction of the hand-drawn line
    nrm = (-sign * ed).normalized()
    nrm = (nrm * math.cos(math.radians(yaw_deg)) - td * math.sin(math.radians(yaw_deg))).normalized()
    if tilt_deg: nrm = (nrm * math.cos(math.radians(tilt_deg)) - YDIR * math.sin(math.radians(tilt_deg))).normalized()   # tip toward the room
    M3 = face_basis(nrm, -YDIR) @ Matrix.Rotation(math.radians(wobble_deg), 3, 'Y')
    r.rotation_euler = M3.to_euler(); sc = max(1e-4, scale * show); r.scale = (sc, sc, sc)
    _key(r, frame); _vis(r, show > 1e-3, frame)

# ---- wind arrows (shot 20): pale arrowhead cards streaming north up the corridor
WIND_N = 14
def _build_wind():
    m = _lit('wind', image=STATE['tex']['wind_arrow'], gain=0.36, shade_mul=1.3, alpha=True); _alpha_mask(m, _drv(m.node_tree, 'wind_alpha'))
    STATE['wind'] = []
    import random
    rr = random.Random(11)
    for i in range(WIND_N):
        q = _quad('wind_%02d' % i, 0.07, 0.14, m); q.visible_shadow = False
        STATE['wind'].append(dict(ob=q, off=i / WIND_N + rr.uniform(-0.02, 0.02), a=rr.uniform(-0.075, 0.075), h=rr.uniform(0.05, 0.30),
                                  tilt=rr.uniform(35, 60), size=rr.uniform(0.75, 1.25)))

def set_wind(progress, amount=1.0, span=(-0.45, 1.05), frame=None):
    """Wind arrow cards streaming north up the corridor. progress: 1.0 = every arrow travels the whole span once (key it every frame,
    e.g. progress = 0.9 x seconds for a gust); amount 0..1 = how many arrows are out (the waves of shot 20: 0.33, 0.66, 1) and their
    size; span = u range they travel (from behind a corridor lens at u -0.12 to past N.Y.). Cards lie tilted 35-60 deg off the paper,
    pointing north, so they read from the low corridor camera and from above."""
    for i, w in enumerate(STATE['wind']):
        ob = w['ob']; on = (i % 3) < 3 * amount - 1e-6 if amount < 1 else True
        f = (progress + w['off']) % 1.0; u = span[0] + (span[1] - span[0]) * f
        env = min(1.0, f / 0.08, (1 - f) / 0.12)
        sc = max(1e-4, w['size'] * env * (1 if on else 0) * min(1.0, amount * 1.5))
        ob.location = world(w['a'], 0, w['h'], u=u)
        tilt = math.radians(w['tilt'])                     # card normal: out of the paper, tipped `tilt` toward the south
        td = tangent(u)                                    # stream along the hand-drawn line
        nrm = (-YDIR * math.cos(tilt) - td * math.sin(tilt)).normalized()
        ob.rotation_euler = face_basis(nrm, td).to_euler(); ob.scale = (sc, sc, sc)
        _key(ob, frame); _vis(ob, sc > 1e-3, frame)

# ---- speed sign on a pin at the roadside (foot of the east wall, u 0.62), above the wall top
SIGN_D = 0.26
def _build_sign():
    root = _empty('sign_root'); spin = _empty('sign_spin', parent=root)
    fm = _lit('sign_front', image=X.paper_png('speed_sign', (SIGN_D, SIGN_D), 900), gain=0.30, alpha=True)
    bm = _lit('sign_back', image=X.paper_png('speed_sign_back', (SIGN_D, SIGN_D), 600), gain=0.30, alpha=True)
    for m in (fm, bm): _alpha_mask(m, _drv(m.node_tree, 'sign_alpha'))
    f = _quad('sign_front', SIGN_D, SIGN_D, fm); f.parent = spin; f.location = (0, -0.002, 0)
    b = _quad('sign_back', SIGN_D, SIGN_D, bm); b.parent = spin; b.location = (0, 0.002, 0); b.rotation_euler = (0, 0, math.pi)
    post = _lit('sign_post', '#8a8f9a', gain=0.45); mb = S.MB()
    mb.frustum((0, 0, -0.08), (0, 0, -0.08 - 1.0), 0.0075, 0.0075, post, seg=8)        # post: from the sign down (scaled in set_speed_sign)
    po = mb.obj('sign_post', STATE['coll']); po.parent = root; STATE['objects']['sign_post'] = po

def set_speed_sign(show=1.0, spin_deg=0.0, scale=0.80, u=0.62, a=None, height=None, frame=None):
    """Round speed sign '100' with THAI 'กม./ชม.' on a pin. It stands on a post at the foot of the east wall (a = 0.085 D east of the
    line, u 0.62) and its disc rides above the wall top (height = centre above the paper, default wall height + 0.12 D), facing south
    down the corridor, text upright for a camera whose up is the wall normal. spin_deg turns it about the post (it spins in the wake
    and settles on 0 = '100' to the south; 180 shows the back); scale 0.8 = 0.21 D across; show 0..1 pops it."""
    r = STATE['objects']['sign_root']; sp = STATE['objects']['sign_spin']; po = STATE['objects']['sign_post']
    a = 0.085 if a is None else a; height = STATE['H'] + 0.12 if height is None else height
    r.location = world(a, 0, height, u=u)
    r.rotation_euler = face_basis(-tangent(u), -YDIR).to_euler()     # faces south down the (local) line
    sc = max(1e-4, scale * show); sp.scale = (sc, sc, sc); sp.rotation_euler = (0, 0, math.radians(spin_deg))
    po.scale = (1, 1, max(1e-3, (height - 0.08 * sc) / 1.0)); po.location = (0, 0, 0.08 - 0.08 * sc)
    _key(r, frame); _key(sp, frame); _key(po, frame); _vis(r, show > 1e-3, frame)

# ---- spinner extras (shot 19): pulsing isobar rings and a sweat drop, riding on office_props' spinner
def _build_spinner_fx():
    root = X.STATE['objects']['spinner_root']
    rm = _lit('rings', image=STATE['tex']['rings'], gain=0.30, alpha=True); _alpha_mask(rm, _drv(rm.node_tree, 'ring_alpha'))
    q = _quad('spinner_rings', 0.46, 0.46, rm); q.parent = root; q.location = (0, -0.0035, 0); q.visible_shadow = False
    dm = _lit('drop', image=STATE['tex']['drop'], gain=0.40, shade_mul=1.3, alpha=True); _alpha_mask(dm, _drv(dm.node_tree, 'drop_alpha'))
    d = _quad('spinner_drop', 0.034, 0.048, dm); d.parent = root; d.location = (0.075, -0.05, 0.07); d.visible_shadow = False
    STATE['ring'] = q; STATE['drop'] = d

def set_spinner_fx(ring=None, ring_pulse=0.0, drop=None, drop_slide=0.0, frame=None):
    """Isobar rings round the storm spinner (alpha `ring`, scale x(1 + 0.25 ring_pulse): key the pulse in time with the spin) and one
    sweat drop at the disc's upper right (alpha `drop`; drop_slide 0..1 slides it 0.06 D down the disc). They ride on the spinner root
    of office_props (they follow X.set_spinner's position)."""
    q, d = STATE['ring'], STATE['drop']; s = 1 + 0.25 * ring_pulse; q.scale = (s, s, s); d.location = (0.075, -0.05, 0.07 - 0.06 * drop_slide)
    _key(q, frame, loc=False, rot=False); _key(d, frame, rot=False, scale=False)
    if ring is not None or frame is not None: _setp('ring_alpha', ring if ring is not None else _ctl()['ring_alpha'], frame)
    if drop is not None or frame is not None: _setp('drop_alpha', drop if drop is not None else _ctl()['drop_alpha'], frame)

# ---- wake streak (shots 20, 21, 25): red-hot tail behind the spinner along the line
def _build_wake():
    s0, s1 = -0.1 * TLEN, 1.0 * TLEN; n = 160; w = 0.07
    m = _lit('wake', '#ff7a3a', gain=0.35); nt = m.node_tree; ux, uy = _uv_x(nt)
    head = _drv(nt, 'wake_head', '(v + 0.1) / 1.1'); ln = _drv(nt, 'wake_len', 'max(v / 1.1, 0.0005)'); al = _drv(nt, 'wake_alpha')
    t = _math(nt, 'DIVIDE', _math(nt, 'SUBTRACT', ux, _math(nt, 'SUBTRACT', head, ln)), ln)            # 0 at the tail end .. 1 at the head
    inside = _math(nt, 'MULTIPLY', _math(nt, 'GREATER_THAN', t, 0.0), _math(nt, 'LESS_THAN', t, 1.0))
    across = _math(nt, 'SUBTRACT', 1.0, _math(nt, 'MULTIPLY', _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', uy, 0.5)), 2.0))
    wid = _math(nt, 'GREATER_THAN', across, _math(nt, 'SUBTRACT', 1.0, t))                             # tapers to the tail
    a = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', inside, wid), _math(nt, 'MULTIPLY', al, _math(nt, 'POWER', t, 0.7)))
    _alpha_mask(m, a); _add_glow(m, _rgb(nt, '#ff4a1c'), _math(nt, 'MULTIPLY', a, 0.9))
    V = []; F = []; UV = []
    for i in range(n + 1):
        s = s0 + (s1 - s0) * i / n; V += [world(-w / 2, s, 0.0045), world(w / 2, s, 0.0045)]
    for i in range(n):
        a_, b_ = 2 * i, 2 * i + 2; F.append((a_, b_, b_ + 1, a_ + 1)); UV.append([(i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1)])
    ob = _mesh('wake', V, F, m, uvs=UV); ob.visible_shadow = False
    if ob.data.polygons[0].normal.y > 0:
        for p in ob.data.polygons: p.flip()

def set_wake(head_u, length_u, alpha=1.0, frame=None):
    """Red-hot wake streak on the line: from u = head_u - length_u (thin, faint) to head_u (full width, bright). alpha 0 hides it."""
    _setp('wake_head', head_u, frame); _setp('wake_len', length_u, frame); _setp('wake_alpha', alpha, frame)

# ---- ghost spinners for the speed comparison (shot 21): office_props' three grey copies, moved along the six ghost tracks
def _build_shell():
    sm = _lit('shell', image=STATE['tex']['shell'], gain=0.36, alpha=True)
    q = _quad('ghost_shell', 0.10, 0.10, sm); q.visible_shadow = True; STATE['shell'] = q

GHOST_FOR = {1: 3, 2: 1, 3: 6}          # ghost spinner i rides ghost track GHOST_FOR[i] of office_props (the faded old curved tracks)
def ghost_point(i, s):
    """(x, z) and heading of ghost track GHOST_FOR[i] at fraction s (0 start .. 1 end)."""
    pts = X.STATE['ghost_pts'][GHOST_FOR[i] - 1]; n = len(pts) - 1; f = max(0.0, min(1.0, s)) * n; k = min(n - 1, int(f)); t = f - k
    a, b = Vector(pts[k]), Vector(pts[k + 1]); p = a.lerp(b, t); d = b - a
    return (p.x, p.y), math.degrees(math.atan2(d.y, d.x))

def set_ghost_spinner(i, s, angle=None, show=1.0, alpha=None, scale=1.0, frame=None):
    """Grey ghost spinner i (1..3) at fraction s along its faded curved track (GHOST_FOR). angle = its turn in degrees (key every frame;
    a crawl is about a sixth of the storm's speed); alpha = the shared ghost opacity (office_props 'ghost_spinner_alpha', 0.6 default);
    show 0/1. Brighten the tracks themselves with office_props.set_ghost(k, 1.0, alpha=0.6)."""
    xz, _ = ghost_point(i, s)
    X.set_spinner(xz=xz, angle=angle, show=show, scale=scale, which='ghost%d' % i, frame=frame)
    if alpha is not None: X._setp('ghost_spinner_alpha', alpha, frame)

def set_shell(show=1.0, which=2, frame=None):
    """Snail shell card on ghost spinner `which` (it rides the ghost's root, beside the disc, and does not spin)."""
    q = STATE['shell']; q.parent = X.STATE['objects']['ghost%d_root' % which]
    q.location = (-0.07, -0.03, 0.035); s = max(1e-4, show); q.scale = (s, s, s)
    _key(q, frame); _vis(q, show > 1e-3, frame)

# ----------------------------------------------------------------------------- cameras (shots 19-22)
def _setup(loc, look, lens=22.0, up=None, roll=0.0):
    d = dict(loc=tuple(round(x, 5) for x in loc), look_at=tuple(round(x, 5) for x in look), lens=lens)
    if up is not None: d['up'] = tuple(up)
    if roll: d['roll'] = roll
    return d

def sight_margin(lens_lat, lens_sc, lens_h, tgt_lat, tgt_sc, tgt_h=0.0, n=80):
    """Smallest clearance (D) between the straight sight line lens -> target and the corridor faces of the locked walls, over the
    stretch where the line runs lower than the wall tops (negative = a wall hides the target)."""
    H = STATE.get('H', 0.50); s0w, s1w = sc_of_u(U_WALL[0]), sc_of_u(U_WALL[1]); m = 1e9
    for i in range(n + 1):
        sc = s0w + (s1w - s0w) * i / n
        if (sc - lens_sc) * (sc - tgt_sc) > 0: continue
        f = (sc - lens_sc) / ((tgt_sc - lens_sc) or 1e-9); lat = lens_lat + (tgt_lat - lens_lat) * f; h = lens_h + (tgt_h - lens_h) * f
        if h > H * (1 + 0.15 * 0) + 0.01: continue
        c = dev_s(sc); hw = LANE_HALF * kf(sc); m = min(m, lat - (c - hw), (c + hw) - lat)
    return m

def clear_lateral(u_lens, h, target_u=1.0, lo=-0.30, hi=0.30):
    """Chord-frame lateral for a lens at u_lens (< U_WALL[0]), h D up, from which the line of sight to the track point target_u
    clears both corridor faces best (the hand-drawn corridor bends, so the lens sits off the chord where it can see N.Y.)."""
    sl = sc_of_u(u_lens); st = sc_of_u(target_u); tl = lateral(0.0, st); best = (-1e9, 0.0)
    for i in range(121):
        x = lo + (hi - lo) * i / 120.0; mg = sight_margin(x, sl, h, tl, st)
        if mg > best[0]: best = (mg, x)
    return best[1], best[0]

def corridor(u_lens=-0.12, h=0.35, look_u=0.85, look_h=0.06, a='auto', look_a=None, lens=22.0, roll=0.0, target_u=1.0):
    """THE CORRIDOR VIEW: lens `h` D above the paper behind the storm at u_lens, looking up the corridor at track point look_u
    (look_h above the paper), up vector = the wall normal (out of the paper).  a = east offset of the lens from the line; 'auto'
    (default) puts the lens where the sight line to the track point target_u (N.Y.) clears both corridor faces best (the hand-drawn
    corridor bends west and back, so seen from straight behind the storm the east wall would hide N.Y.).  look_a: east offset of
    the look point from the line (default: on the line)."""
    if a == 'auto':
        x, _ = clear_lateral(u_lens, h, target_u); sc = sc_of_u(u_lens); loc = world_sc(x, sc, h)
    else:
        loc = world(a, 0, h, u=u_lens)
    la = 0.0 if look_a is None else look_a
    return _setup(loc, world(la, 0, look_h, u=look_u), lens, up=tuple(-YDIR), roll=roll)

def rake(target, dist, elev_deg, az_deg, lens=22.0, up=None):
    """Camera `dist` D from world point `target`, `elev_deg` above the paper plane, coming from azimuth az_deg measured in the map plane
    from the line's south direction (0 = straight behind the storm looking north, +90 = from the east, -90 = from the west)."""
    e, z = math.radians(elev_deg), math.radians(az_deg); t = Vector(target)
    horiz = (-TDIR * math.cos(z) + NDIR * math.sin(z)); loc = t + dist * (horiz * math.cos(e) - YDIR * math.sin(e))
    return _setup(loc, t, lens, up=up)

def plan(u_center, dist=1.2, a=0.0, roll=0.0, lens=22.0):
    """PLAN VIEW: square-on to the wall, `dist` D from the paper, centred on the track at u_center (a = east offset), north up
    the frame (up = +z) with `roll` degrees of roll (shot 19: -12 easing to 0)."""
    c = Vector(world(a, 0, 0, u=u_center)); loc = c - dist * YDIR
    return _setup(loc, c, lens, up=(0, 0, 1), roll=roll)

def cams():
    """Named camera setups {loc, look_at, lens, (up), (roll)} for shots 19-22 (use office3d.make_camera(setup)). Spinner at u 0.10."""
    sp = world(0, 0, 0.02, u=0.10); H = STATE.get('H', 0.55)
    return dict(
        rake_spinner=rake(world(0.02, 0, 0.03, u=0.12), 0.80, 30.0, -55.0),              # 19 (0): tight on the spinner, 30 deg rake from below-left
        rake_north=rake(world(0.05, 0, 0.0, u=0.40), 1.80, 35.0, -12.0),                  # 19 (1): x0.45 back, 35 deg rake looking north, both walls
        corridor_cam=corridor(),                                                          # 19 (2), 20, 22 start: THE CORRIDOR VIEW
        corridor_far=corridor(u_lens=-0.20, h=0.70, look_u=0.95, look_h=0.10),            # the gate's fallback: same choreography from 0.7 D
        plan_view=plan(0.62, 1.2),                                                        # 19 (3) end of the truck north: N.Y. in the upper third
        plan_view_start=plan(0.03, 1.2, roll=-12.0),                                      # 19 (3) landing of the snap (roll -12)
        spinner_high=rake(world(0.0, 0, 0.0, u=0.17), 0.80, 52.0, -8.0),                  # 19 (4): push x2 back onto the spinner from behind and above
        sign_cam=_setup(world(-0.04, 0, 0.30, u=0.42), world(0.085, 0, H + 0.12, u=0.62), up=tuple(-YDIR)),   # 20 end: beside the speed sign (about 300 px)
        launch_end=corridor(u_lens=0.33, h=0.35, look_u=1.1, look_h=0.10),               # 20: corridor view after 0.45 D of travel
        atlantic_rake=rake(world(0.35, 0, 0.0, u=0.55), 1.90, 30.0, 40.0, up=(0, 0, 1)),  # 21: whole western Atlantic, 30 deg rake from the south-east
        label_end=_setup((0.10, -1.55, 2.85), (0.10, -0.054, 3.26)),   # 22 start: facing the label at the lane's end
        whole_map=_setup((-0.45, -4.30, 2.55), (0.05, -0.05, 2.50)),                      # 22: near-square-on whole map, about 8 deg of yaw
        ny_arrow=_setup((-0.05, -1.30, 2.45), (0.07, -0.05, 2.60)),                       # 22 end: push x3 onto the arrow head at N.Y. and Long Island
    )

def cam(name, **kw):
    """A named setup, or a parametric one: cam('corridor', u_lens=..), cam('plan', u_center=..), cam('rake', target=.., ...)."""
    if name == 'corridor': return corridor(**kw)
    if name == 'plan': return plan(**kw)
    if name == 'rake': return rake(**kw)
    return cams()[name]

def lerp_setup(a, b, t):
    """Blend two setups (loc, look_at, lens, roll; up blended and renormalised). For snaps use an eased t."""
    L = lambda p, q: tuple(x + (y - x) * t for x, y in zip(p, q))
    d = dict(loc=L(a['loc'], b['loc']), look_at=L(a['look_at'], b['look_at']), lens=a.get('lens', 22) + (b.get('lens', 22) - a.get('lens', 22)) * t)
    ua, ub = a.get('up'), b.get('up')
    if ua or ub:
        def up_of(s):
            if s.get('up'): return Vector(s['up'])
            f = (Vector(s['look_at']) - Vector(s['loc'])).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); return r.cross(f)
        d['up'] = tuple(up_of(a).lerp(up_of(b), t).normalized())
    ra, rb = a.get('roll', 0.0), b.get('roll', 0.0)
    if ra or rb: d['roll'] = ra + (rb - ra) * t
    return d
