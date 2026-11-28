#!/usr/bin/env python3
"""office_props.py : build-order step 4 of the shot plan, an EXTENSION of the office set (v3/set3d/office3d.py is imported, never edited).

    import sys; sys.path.insert(0, PROJ + '/v3/set3d'); sys.path.insert(0, PROJ + '/v3/set3d_ext/props')
    import office3d as S, office_props as X
    A = S.build('INTERIOR_DAY')            # the reviewed set
    PA = X.build(A)                        # adds collection PROPS + control empty 'props_ctl'; returns anchors (cams, marks, prop anchors)
    X.set_spinner(u=0.0, angle=30, frame=10)          # every setter: frame=None sets statically, frame=N inserts keyframes
    cam = S.make_camera(PA['cams']['label_insert'])

Contents (shots 4-7, 9-14 of plan/shot_plan.md): storm spinner + 3 ghost spinners, white dashed chalk curve with a travelling arrow head,
six ghost tracks, tick stamp, ruler (on the map, and a hand-held copy), nickname label with its red pin, smudge halo (three levels),
eraser crumbs, forecast sheet quad (layers that pop), teletype paper feed, rubber stamp, calendar pad / leaf with lift, flutter and tear,
6000 px map swap, new cameras and marks, track_shadow_report for the nickname label. See API.md next to this file."""
import os, sys, math, json, random
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d'))
import office3d as S                                        # noqa: E402

PAPER = os.path.join(PROJ, 'v3', 'paper')
TEXD = os.path.join(HERE, 'tex')
MAP_Y = S.MAP_Y
STATE = {}

# ----------------------------------------------------------------------------- paper registry (v3/paper, read-only)
def registry():
    """{name: entry} of v3/paper/tex/registry.json. Missing items -> placeholder cards (see PLACEHOLDERS)."""
    p = os.path.join(PAPER, 'tex', 'registry.json')
    return json.load(open(p)) if os.path.exists(p) else {}

PLACEHOLDERS = []          # names that had to fall back to a placeholder card at the last build (swap by registry name)

def _placeholder(name, size_D, px=512):
    from PIL import Image, ImageDraw
    os.makedirs(TEXD, exist_ok=True); w, h = size_D; W, H = (px, max(8, int(px * h / w))) if w >= h else (max(8, int(px * w / h)), px)
    out = os.path.join(TEXD, 'PLACEHOLDER_%s.png' % name)
    im = Image.new('RGBA', (W, H), (255, 0, 200, 255)); d = ImageDraw.Draw(im)
    for k in range(-H, W, 24): d.line([(k, 0), (k + H, H)], fill=(255, 255, 255, 255), width=6)
    d.rectangle([2, 2, W - 3, H - 3], outline=(0, 0, 0, 255), width=4); d.text((8, 8), 'PLACEHOLDER ' + name, fill=(0, 0, 0, 255))
    im.save(out); PLACEHOLDERS.append(name); return out

def paper_png(name, size_D=(0.2, 0.2), max_px=None):
    """Path of a paper texture by registry name, optionally down-scaled to max_px on the long side (Cycles does not mip-map:
    keep about 1.5 x the on-screen size). Falls back to a magenta striped placeholder card if the item is missing."""
    e = registry().get(name)
    if not e or not os.path.exists(e['png']): return _placeholder(name, size_D)
    src = e['png']
    if not max_px: return src
    from PIL import Image
    im = Image.open(src); W, H = im.size
    if max(W, H) <= max_px: return src
    os.makedirs(TEXD, exist_ok=True); out = os.path.join(TEXD, '%s_%d.png' % (name, max_px))
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        k = max_px / max(W, H); im.resize((max(1, round(W * k)), max(1, round(H * k))), Image.LANCZOS).save(out)
    return out

# ----------------------------------------------------------------------------- derived textures (PIL, cached in tex/)
def _derived():
    """Textures made here from the paper artwork or from scratch: fast spinner (rotational blur), ruler face, smudge blotches,
    ink-bloom halos of the two typed words. Returns {key: path}."""
    from PIL import Image, ImageDraw, ImageFilter
    import numpy as np
    os.makedirs(TEXD, exist_ok=True); out = {}
    # 1. fast spinner: the disc averaged over 100 degrees of turn (the spiral smears into rings)
    src = paper_png('spinner_disc', (0.16, 0.16), 512); p = os.path.join(TEXD, 'spinner_fast_512.png'); out['spinner_fast'] = p
    if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(src):
        im = Image.open(src).convert('RGBA'); acc = np.zeros((im.size[1], im.size[0], 4)); n = 24
        for i in range(n): acc += np.asarray(im.rotate(100.0 * i / n, resample=Image.BICUBIC), dtype=np.float64)
        Image.fromarray(np.clip(acc / n, 0, 255).astype('uint8'), 'RGBA').save(p)
    # 2. ruler face: maple wood with tick marks, no lettering (1.30 x 0.11 D at 1600 px per D)
    p = os.path.join(TEXD, 'ruler_face.png'); out['ruler'] = p
    if not os.path.exists(p):
        ppd = 1600; L, Wd = 1.30, 0.11; W, H = int(L * ppd), int(Wd * ppd); r = random.Random(3)
        im = Image.new('RGB', (W, H), (214, 164, 100)); d = ImageDraw.Draw(im)
        for k in range(60):                                  # grain streaks along the length
            y = r.uniform(0, H); c = r.choice([(196, 146, 86), (226, 178, 114), (204, 152, 90)])
            d.line([(0, y), (W, y + r.uniform(-6, 6))], fill=c, width=r.randint(1, 3))
        for i in range(int(L / 0.025) + 1):                  # ticks from the -x (near) edge of the face: every 0.025, 0.125, 0.25 D
            x = int(i * 0.025 * ppd); ln = 0.045 if i % 10 == 0 else (0.032 if i % 5 == 0 else 0.018)
            d.line([(x, 0), (x, int(ln * ppd))], fill=(62, 34, 20), width=4 if i % 5 == 0 else 3)
        d.rectangle([0, 0, W - 1, H - 1], outline=(42, 23, 18), width=8)
        im.save(p)
    # 3. smudge blotch: soft irregular pink-grey rubbing (alpha)
    p = os.path.join(TEXD, 'smudge_blotch.png'); out['blotch'] = p
    if not os.path.exists(p):
        S_ = 256; rng = np.random.default_rng(7); yy, xx = np.mgrid[0:S_, 0:S_] / (S_ - 1) * 2 - 1
        ang = np.arctan2(yy, xx); rad = np.hypot(xx * 0.8, yy * 1.4)
        wob = 0.75 + 0.12 * np.sin(3 * ang + 1.3) + 0.08 * np.sin(5 * ang + 0.4) + 0.05 * np.sin(9 * ang)
        a = np.clip((wob - rad) / 0.35, 0, 1) ** 1.3
        noise = np.asarray(Image.fromarray((rng.random((64, 64)) * 255).astype('uint8')).resize((S_, S_), Image.BICUBIC), dtype=float) / 255
        a = a * (0.55 + 0.45 * noise); rgba = np.zeros((S_, S_, 4), dtype='uint8')
        rgba[..., 0], rgba[..., 1], rgba[..., 2] = 232, 158, 146; rgba[..., 3] = (a * 255).astype('uint8')
        Image.fromarray(rgba, 'RGBA').save(p)
    # 4. ink bloom of the two typed words: the word's alpha dilated and blurred, dark brown-blue ink
    for k in (1, 2):
        src = paper_png('forecast_word_%d' % k, (1.08, 1.40)); p = os.path.join(TEXD, 'forecast_bloom_%d.png' % k); out['bloom%d' % k] = p
        if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(src):
            im = Image.open(src).convert('RGBA'); a = im.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10))
            a = a.point(lambda v: int(min(255, v * 0.8))); col = Image.new('RGBA', im.size, (70, 52, 66, 0)); col.putalpha(a); col.save(p)
    return out

# ----------------------------------------------------------------------------- materials (built with office3d.mat_lit, so they follow the preset's light model)
def _pre(): return S.STATE['preset'] + '_px_'

def _lit(key, color='#808080', image=None, gain=1.0, shade_mul=1.0, alpha=False, form=True):
    P = S.STATE['P']; f = tuple(P.get('form', (0, 0, 0))) if form else None
    return S.mat_lit(_pre() + key, color, image=image, gain=gain, shade_mul=shade_mul, alpha=alpha, form=f)

def _ctl():
    return STATE['ctl']

def _driven_value(nt, prop, expr='v', label=None):
    """A Value node whose output follows props_ctl[prop] through a driver (simple expression, no Python at render time)."""
    n = nt.nodes.new('ShaderNodeValue'); n.label = label or prop; n.name = 'drv_' + (label or prop)
    fc = n.outputs[0].driver_add('default_value'); d = fc.driver; d.type = 'SCRIPTED'
    v = d.variables.new(); v.name = 'v'; v.type = 'SINGLE_PROP'; v.targets[0].id = _ctl(); v.targets[0].data_path = '["%s"]' % prop
    d.expression = expr
    return n.outputs[0]

def _math(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    for i, x in enumerate((a, b)):
        if x is None: continue
        if isinstance(x, (int, float)): n.inputs[i].default_value = float(x)
        else: nt.links.new(x, n.inputs[i])
    return n.outputs[0]

def _alpha_mask(m, fac):
    """Multiply the material's opacity by the socket `fac` (0 transparent .. 1 as before): inserts Mix(Transparent, surface)."""
    nt = m.node_tree; out = next(n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial')
    src = out.inputs['Surface'].links[0].from_socket
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(fac, mx.inputs['Fac']); nt.links.new(tr.outputs['BSDF'], mx.inputs[1]); nt.links.new(src, mx.inputs[2])
    nt.links.new(mx.outputs['Shader'], out.inputs['Surface'])
    return m

def _uv_x(nt):
    uv = nt.nodes.new('ShaderNodeUVMap'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(uv.outputs['UV'], sp.inputs[0]); return sp.outputs['X'], sp.outputs['Y']

def _image_node(m):
    return next(n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage')

# ----------------------------------------------------------------------------- geometry helpers
def _catmull(ctrl, n=120):
    """Smooth curve through the (x, z) control points (centripetal-ish Catmull-Rom), resampled to n points evenly in arc length."""
    P = [Vector((x, z)) for x, z in ctrl]; P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]; dense = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(40):
            t = k / 40; t2 = t * t; t3 = t2 * t
            dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    dense.append(P[-2]); L = [0.0]
    for a, b in zip(dense, dense[1:]): L.append(L[-1] + (b - a).length)
    out = []; j = 0
    for i in range(n):
        s = L[-1] * i / (n - 1)
        while j < len(L) - 2 and L[j + 1] < s: j += 1
        t = 0 if L[j + 1] == L[j] else (s - L[j]) / (L[j + 1] - L[j]); out.append(dense[j].lerp(dense[j + 1], t))
    return [(p.x, p.y) for p in out], L[-1]

def _ribbon(mb, pts, width, mat, y, uvx=None, uvy=(0.0, 1.0)):
    """Flat strip in the plane y facing -y along the (x, z) points; UV x = arc fraction (or uvx list), UV y across."""
    n = len(pts); L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    uvx = uvx or [l / L[-1] for l in L]; mb.pid += 1; mb._in = True
    def perp(i):
        a = Vector(pts[max(0, i - 1)]); b = Vector(pts[min(n - 1, i + 1)]); d = (b - a).normalized(); return Vector((-d.y, d.x))
    for i in range(n - 1):
        pa, pb = Vector(pts[i]), Vector(pts[i + 1]); na, nb = perp(i) * width / 2, perp(i + 1) * width / 2
        q = [pa - na, pb - nb, pb + nb, pa + na]; w3 = [(p.x, y, p.y) for p in q]
        uvs = [(uvx[i], uvy[0]), (uvx[i + 1], uvy[0]), (uvx[i + 1], uvy[1]), (uvx[i], uvy[1])]
        nrm = (Vector(w3[1]) - Vector(w3[0])).cross(Vector(w3[3]) - Vector(w3[0]))
        if nrm.y > 0: w3 = w3[::-1]; uvs = uvs[::-1]
        mb.face(w3, mat, uvs)
    mb._in = False

def _grid_quad(name, w, h, mat, nx=1, nz=1, origin=(0.0, 0.0), coll=None, uv=(0, 0, 1, 1)):
    """Quad w x h in the local XZ plane facing local -Y, split nx x nz; vertex (0, 0) of the quad's local frame is its top-left
    corner minus `origin` (so `origin` = the pivot measured from the top-left corner, z down). UV (u0, v0, u1, v1), v up."""
    me = bpy.data.meshes.new(name); V = []; F = []; UV = []
    ox, oz = origin; u0, v0, u1, v1 = uv
    for j in range(nz + 1):
        for i in range(nx + 1): V.append((i / nx * w - ox, 0.0, -(j / nz) * h + oz))
    for j in range(nz):
        for i in range(nx):
            a = j * (nx + 1) + i; F.append((a + nx + 1, a + nx + 2, a + 1, a))      # normal -y
    me.from_pydata(V, [], F); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        for li in p.loop_indices:
            x, _, z = V[me.loops[li].vertex_index]; uvl.data[li].uv = (u0 + (u1 - u0) * (x + ox) / w, v0 + (v1 - v0) * (1 - (oz - z) / h))
    me.materials.append(mat); ob = bpy.data.objects.new(name, me); (coll or STATE['coll']).objects.link(ob)
    STATE['objects'][name] = ob; return ob

def _empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); STATE['coll'].objects.link(e); e.location = loc; e.empty_display_size = 0.05
    if parent: e.parent = parent
    STATE['objects'][name] = e; return e

def _mbobj(mb, name, hull=0.0):
    ob = mb.obj(name, STATE['coll'], hull=hull); STATE['objects'][name] = ob; return ob

def _shape_driver(ob, key, prop, expr='v'):
    fc = ob.data.shape_keys.driver_add('key_blocks["%s"].value' % key); d = fc.driver; d.type = 'SCRIPTED'
    v = d.variables.new(); v.name = 'v'; v.type = 'SINGLE_PROP'; v.targets[0].id = _ctl(); v.targets[0].data_path = '["%s"]' % prop
    d.expression = expr

# ----------------------------------------------------------------------------- keyframe helpers
def _setp(prop, value, frame=None, interp='LINEAR'):
    """Set (and with frame=N keyframe) one scalar control on props_ctl."""
    c = _ctl(); c[prop] = float(value)
    if frame is not None:
        c.keyframe_insert('["%s"]' % prop, frame=frame); _interp(c, '["%s"]' % prop, frame, interp)
    c.update_tag()

def _interp(idb, path, frame, interp):
    for fc in S._fcurves(idb):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5: kp.interpolation = interp

def _key_xform(ob, frame, loc=True, rot=True, scale=True, interp='LINEAR'):
    if frame is None: return
    for on, path in ((loc, 'location'), (rot, 'rotation_euler'), (scale, 'scale')):
        if on: ob.keyframe_insert(path, frame=frame); _interp(ob, path, frame, interp)

def _key_vis(ob, visible, frame):
    ob.hide_render = not visible; ob.hide_viewport = False
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame); _interp(ob, 'hide_render', frame, 'CONSTANT')

def _set_vis_tree(root, visible, frame):
    for o in [root] + list(root.children_recursive): _key_vis(o, visible, frame)

def _basis(normal, up=(0, 0, 1), roll_deg=0.0):
    """Rotation matrix whose local -Y points along `normal` (the face looks that way) and local Z is as close to `up` as possible."""
    n = Vector(normal).normalized(); Y = -n; Z = Vector(up)
    X = Y.cross(Z)
    if X.length < 1e-6: X = Vector((1, 0, 0))
    X.normalize(); Z = X.cross(Y).normalized()
    M = Matrix((X, Y, Z)).transposed()
    if roll_deg: M = M @ Matrix.Rotation(math.radians(roll_deg), 3, 'Y')
    return M

# ----------------------------------------------------------------------------- the map props: geometry data (map plane x, z)
TRACK0, TRACK1 = S.track_point(0.0), S.track_point(1.0)
def track_xz(u): p = S.track_point(u); return (p[0], p[2])
def _track_ext(u):
    """World point on the straight track's line at any u (u < 0 below the storm, u > 1 past N.Y.)."""
    a, b = Vector(TRACK0), Vector(TRACK1); return tuple(a + (b - a) * u)
# the white chalk curve (the old hands' forecast): from the storm north along the coast, bends north-east at z ~2.1 (track u ~0.48,
# where the hero's ruled line passes it in shot 9) and sails out to sea; arrow head at the far end
CHALK_CTRL = [(0.2349, 1.6183), (0.248, 1.78), (0.258, 1.93), (0.290, 2.06), (0.375, 2.175), (0.52, 2.28), (0.71, 2.37), (0.93, 2.44)]
CHALK_BEND = (0.290, 2.06)
# six faded old tracks, a fountain: each starts near the storm region and recurves out to sea, none reaches N.Y.
GHOST_CTRL = [
    [(0.05, 1.50), (0.02, 1.72), (0.04, 1.92), (0.16, 2.08), (0.40, 2.20), (0.70, 2.27)],
    [(0.38, 1.52), (0.36, 1.70), (0.40, 1.85), (0.55, 1.98), (0.82, 2.06), (1.08, 2.10)],
    [(-0.10, 1.62), (-0.08, 1.85), (0.00, 2.05), (0.18, 2.22), (0.44, 2.36), (0.72, 2.46)],
    [(0.55, 1.62), (0.56, 1.78), (0.66, 1.92), (0.88, 2.02), (1.18, 2.06)],
    [(0.22, 1.47), (0.15, 1.66), (0.13, 1.86), (0.22, 2.02), (0.48, 2.13), (0.90, 2.18)],
    [(-0.02, 1.80), (0.02, 2.00), (0.12, 2.18), (0.30, 2.34), (0.56, 2.50), (0.84, 2.60)],
]
LABEL_W, LABEL_H = 1.15, 0.34
LB_PIN = (0.50, 0.045)                                       # paper.LB_PIN: pin point from the label's top-left (D), clear of the lettering
CAL_PAD = (0.66, 0.90); CAL_LEAF = (0.02, 0.02, 0.62, 0.86)  # paper.LEAF
SHEET_W, SHEET_H = 1.08, 1.40
SHEET_WORD_C = {'word1': (0.4985, 0.4305), 'word2': (0.4985, 0.608), 'stamp': (0.7915, 0.1535)}   # centres (fraction of w, of h from top), from the alpha bboxes
TT_SCALE = 0.5                                               # the forecast artwork on the teletype sheet at half size (0.54 x 0.70 D)

# ----------------------------------------------------------------------------- build
def build(A=None, hi_map=False, replace_teletype_sheet=True, ghost_spinners=3):
    """Add every prop to the current scene after office3d.build(). Returns PA = dict(cams, marks, paths, anchors...)."""
    scene = bpy.context.scene; A = A or S.STATE['A']; PLACEHOLDERS.clear()
    coll = S._coll('PROPS', scene); S._wipe(coll)
    for m in list(bpy.data.materials):
        if '_px_' in m.name: bpy.data.materials.remove(m)
    STATE.clear(); STATE.update(coll=coll, objects={}, A=A)
    ctl = bpy.data.objects.new('props_ctl', None); coll.objects.link(ctl); ctl.hide_render = True; STATE['ctl'] = ctl; STATE['objects']['props_ctl'] = ctl
    for k, v in DEFAULTS.items(): ctl[k] = float(v)
    D = _derived(); STATE['tex'] = D
    _build_spinners(ghost_spinners); _build_chalk(); _build_ghosts(); _build_tick(); _build_ruler(); _build_label()
    _build_smudge(); _build_crumbs(); _build_sheet(); _build_teletype_feed(replace_teletype_sheet); _build_stamp(); _build_calendar()
    for ob in coll.objects: S.no_bounce(ob)
    PA = anchors(A); STATE['PA'] = PA
    set_map_res(hi_map)
    reset()
    return PA

DEFAULTS = dict(chalk_grow=0.0, chalk_crumble=0.0, chalk_alpha=1.0, smudge_level=0.0, crumbs=0.0, spinner_fast=0.0, ghost_spinner_alpha=0.6,
                tick_alpha=0.0, label_curl=0.0, label_flutter=0.0, cal_lift=0.0, cal_flutter=0.0, sheet_word1=1.0, sheet_word2=1.0,
                sheet_stamp=1.0, sheet_bloom1=0.0, sheet_bloom2=0.0, sheet_bow=0.0, tt_stamp=0.0, tt_feed=0.0,
                **{'ghost%d_grow' % i: 0.0 for i in range(1, 7)}, **{'ghost%d_alpha' % i: 0.35 for i in range(1, 7)})

def reset():
    """The clean map of shot 4: no spinner, no chalk, no ghosts, no tick, no label, no smudge halo, no crumbs, ruler off, sheet and
    stamp hidden, teletype feed in (0), calendar leaf 20 flat. (The red track is office3d.set_track's.)"""
    for k, v in DEFAULTS.items(): _ctl()[k] = float(v)
    set_spinner(show=0); [set_spinner(show=0, which='ghost%d' % i) for i in range(1, 1 + len(STATE.get('ghost_spinners', [])))]
    set_chalk(0.0); [set_ghost(i, 0.0) for i in range(1, 7)]; set_tick(0.0); set_ruler(0.0); set_ruler_hand(show=0)
    set_label(show=0); set_smudge(0); set_crumbs(0); set_sheet(show=0); set_teletype(feed=0.0, stamp=0.0, show=1); set_stamp(show=0)
    set_calendar(day=20, lift=0, flutter=0, tear=0)

# ---- storm spinner
SPIN_D = 0.16; SPIN_OFF = 0.022                              # disc diameter, distance in front of the map paper (hard shadow 0.02 D to the left)
def _build_spinners(n_ghost):
    D = STATE['tex']; pre = _pre()
    disc = _lit('spinner_disc', image=paper_png('spinner_disc', (SPIN_D, SPIN_D), 512), gain=0.45, alpha=True)
    nt = disc.node_tree; tex = _image_node(disc)              # 'fast' look: mix in the rotationally blurred disc
    t2 = nt.nodes.new('ShaderNodeTexImage'); t2.image = S._img(D['spinner_fast']); fast = _driven_value(nt, 'spinner_fast')
    for out_name in ('Color', 'Alpha'):
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA' if out_name == 'Color' else 'FLOAT'
        nt.links.new(fast, mx.inputs[0])
        ins = (mx.inputs[6], mx.inputs[7], mx.outputs[2]) if out_name == 'Color' else (mx.inputs[2], mx.inputs[3], mx.outputs[0])
        for l in list(tex.outputs[out_name].links):
            to = l.to_socket; nt.links.remove(l); nt.links.new(ins[2], to)
        nt.links.new(tex.outputs[out_name], ins[0]); nt.links.new(t2.outputs[out_name], ins[1])
    ghost = _lit('spinner_ghost', image=paper_png('spinner_disc_ghost', (SPIN_D, SPIN_D), 512), gain=0.45, alpha=True)
    _alpha_mask(ghost, _driven_value(ghost.node_tree, 'ghost_spinner_alpha'))
    brass = _lit('brass', S.O.BRASS, gain=0.5); pinr = _lit('pin_red', '#c8301c', gain=0.6)
    STATE['ghost_spinners'] = []
    for which, mat in [('spinner', disc)] + [('ghost%d' % i, ghost) for i in range(1, n_ghost + 1)]:
        root = _empty(which + '_root')                           # at the pin point on the paper; local -Y = toward the room
        spin = _empty(which + '_spin', parent=root)              # turns about local Y; wobble about local X; squash = scale X/Z
        dq = _grid_quad(which + '_disc', SPIN_D, SPIN_D, mat, origin=(SPIN_D / 2, SPIN_D / 2)); dq.parent = spin; dq.location = (0, -SPIN_OFF, 0)
        mb = S.MB(); mb.frustum((0, -SPIN_OFF - 0.004, 0), (0, 0.004, 0), 0.0035, 0.0035, brass, seg=8)
        mb.sphere((0, -SPIN_OFF - 0.009, 0), 0.011, brass if which == 'spinner' else pinr, seg=12, rings=6)
        pin = _mbobj(mb, which + '_pin'); pin.parent = root
        if which != 'spinner': STATE['ghost_spinners'].append(which)

def set_spinner(u=None, xz=None, angle=None, wobble=0.0, squash=1.0, scale=1.0, show=1.0, fast=None, pin_out=0.0, which='spinner', frame=None):
    """Storm spinner (or 'ghost1'..'ghost3'). u: position along the red track (0 storm symbol .. 1 N.Y.) or xz=(x, z) on the map;
    angle: turn about the pin in degrees (positive = clockwise as seen from the room; 0.5 rev/s = 6 deg per frame);
    wobble: tilt of the disc in degrees (the 3 deg wobble); squash: 1 = round, >1 tall and thin, <1 flat and wide (area kept);
    scale: overall size; show 0/1 (pop with scale 0..1); fast 0..1 blends in the motion-blurred disc (main spinner only);
    pin_out: the brass pin head stands this many D in front of the disc (0 = pushed home)."""
    root = STATE['objects'][which + '_root']; spin = STATE['objects'][which + '_spin']; pin = STATE['objects'][which + '_pin']
    if u is not None: x, z = track_xz(u); root.location = (x, MAP_Y, z)
    elif xz is not None: root.location = (xz[0], MAP_Y, xz[1])
    elif tuple(root.location) == (0, 0, 0): x, z = track_xz(0.0); root.location = (x, MAP_Y, z)
    if angle is not None: spin.rotation_euler.y = math.radians(angle)
    spin.rotation_euler.x = math.radians(wobble)
    sq = max(0.05, float(squash)); s = max(1e-4, scale * show)
    spin.scale = (s / math.sqrt(sq), s, s * math.sqrt(sq)); pin.scale = (max(1e-4, show),) * 3; pin.location = (0, -pin_out, 0)
    _key_xform(root, frame, rot=False, scale=False); _key_xform(spin, frame); _key_xform(pin, frame, rot=False)
    _set_vis_tree(root, show > 0.001, frame)
    if fast is not None and which == 'spinner': _setp('spinner_fast', fast, frame)
    STATE.setdefault('spinner', {})[which] = dict(loc=tuple(root.location), show=show)

def spinner_angle(t, rev_per_s=0.5, wobble_deg=3.0, t0=0.0):
    """(angle, wobble) at time t seconds for the lurking spin of shot 5: 0.5 rev/s and a 3 degree wobble at the same rate."""
    a = 360.0 * rev_per_s * (t - t0); return a, wobble_deg * math.sin(math.radians(a))

# ---- chalk curve (dashed, grows, crumbles) with a travelling arrow head
CHALK_W = 0.020
def _build_chalk():
    pts, L = _catmull(CHALK_CTRL, 160); STATE['chalk_pts'] = pts; STATE['chalk_len'] = L
    m = _lit('chalk', '#f4f2ec', gain=0.42, shade_mul=1.25); nt = m.node_tree
    ux, uy = _uv_x(nt); grow = _driven_value(nt, 'chalk_grow'); crumble = _driven_value(nt, 'chalk_crumble'); alpha = _driven_value(nt, 'chalk_alpha')
    vis = _math(nt, 'LESS_THAN', ux, _math(nt, 'ADD', grow, 0.0005))                                           # grown part
    dash = _math(nt, 'LESS_THAN', _math(nt, 'FRACT', _math(nt, 'MULTIPLY', ux, L / 0.055)), 0.62)                # 0.055 D period, 62 % ink
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 140.0; nz.inputs['Detail'].default_value = 3.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    thr = _math(nt, 'ADD', _math(nt, 'MULTIPLY', crumble, 0.20), 0.30)                                         # crumbled: more of the chalk breaks up
    edge = _math(nt, 'LESS_THAN', _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', uy, 0.5)), _math(nt, 'SUBTRACT', 0.5, _math(nt, 'MULTIPLY', crumble, 0.15)))
    grain = _math(nt, 'GREATER_THAN', nz.outputs['Fac'], thr)
    fac = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', vis, dash), _math(nt, 'MULTIPLY', grain, edge)), alpha)
    _alpha_mask(m, fac)
    mb = S.MB(); _ribbon(mb, pts, CHALK_W, m, MAP_Y - 0.0020); ob = _mbobj(mb, 'chalk_curve'); ob.visible_shadow = False
    # arrow head: two solid chalk barbs on their own root, moved to the growing tip
    ma = _lit('chalk_head', '#f4f2ec', gain=0.42, shade_mul=1.25); _alpha_mask(ma, _driven_value(ma.node_tree, 'chalk_alpha'))
    mb = S.MB(); Lb = 0.075
    for s in (1, -1):
        a = math.radians(180 - 28 * s); _ribbon(mb, [(Lb * math.cos(a), Lb * math.sin(a)), (0.004 * math.cos(a), 0.004 * math.sin(a))], CHALK_W * 1.1, ma, 0.0)
    head = _mbobj(mb, 'chalk_head'); head.visible_shadow = False
    root = _empty('chalk_head_root'); head.parent = root

def chalk_point(g):
    """(x, z) and heading (degrees, map plane, 0 = +x, 90 = up) of the chalk curve at grow fraction g."""
    pts = STATE['chalk_pts']; n = len(pts) - 1; f = max(0.0, min(1.0, g)) * n; i = min(n - 1, int(f)); t = f - i
    a, b = Vector(pts[i]), Vector(pts[i + 1]); p = a.lerp(b, t); d = b - a
    return (p.x, p.y), math.degrees(math.atan2(d.y, d.x))

def set_chalk(grow, crumble=0.0, alpha=1.0, head=True, frame=None):
    """White dashed chalk curve. grow 0..1 draws it from the storm (the arrow head rides the tip; it bends north-east at grow ~0.45);
    crumble 0..1 breaks the chalk up (the old forecast falling apart); alpha fades it. Key every frame while it grows (the head
    follows the curve, and linear interpolation between sparse keys would cut the bend)."""
    _setp('chalk_grow', grow, frame); _setp('chalk_crumble', crumble, frame); _setp('chalk_alpha', alpha, frame)
    root = STATE['objects']['chalk_head_root']; (x, z), h = chalk_point(max(grow, 0.01))
    root.location = (x, MAP_Y - 0.0022, z); root.rotation_euler = (0, -math.radians(h), 0); s = 1.0 if (head and grow > 0.02) else 1e-4
    root.scale = (s, s, s); _key_xform(root, frame)

# ---- six ghost tracks
GHOST_W = 0.013
def _build_ghosts():
    STATE['ghost_pts'] = []
    for i, ctrl in enumerate(GHOST_CTRL, 1):
        pts, L = _catmull(ctrl, 90); STATE['ghost_pts'].append(pts)
        m = _lit('ghost%d' % i, '#c7d2e6', gain=0.38, shade_mul=1.3); nt = m.node_tree; ux, uy = _uv_x(nt)
        g = _driven_value(nt, 'ghost%d_grow' % i); al = _driven_value(nt, 'ghost%d_alpha' % i)
        _alpha_mask(m, _math(nt, 'MULTIPLY', _math(nt, 'LESS_THAN', ux, _math(nt, 'ADD', g, 0.0005)), al))
        mb = S.MB(); _ribbon(mb, pts, GHOST_W, m, MAP_Y - 0.0012 - 0.0001 * i)
        (x, z), (x0, z0) = pts[-1], pts[-6]; h = math.atan2(z - z0, x - x0)          # small arrow head, shown with the last 3 percent
        for s in (1, -1):
            a = h + math.radians(180 - 30 * s); _ribbon(mb, [(x + 0.05 * math.cos(a), z + 0.05 * math.sin(a)), (x, z)], GHOST_W, m, MAP_Y - 0.0012 - 0.0001 * i, uvx=[0.985, 0.985])
        ob = _mbobj(mb, 'ghost_track%d' % i); ob.visible_shadow = False

def set_ghost(i, grow, alpha=None, frame=None):
    """Ghost track i (1..6): grow 0..1 draws it (arrow head with the last 3 percent); alpha = its brightness (rests at 0.35).
    Shot 7: one every 3 frames, 12.40-13.00 (ghost_fan_keys gives the keys)."""
    _setp('ghost%d_grow' % i, grow, frame)
    if alpha is not None: _setp('ghost%d_alpha' % i, alpha, frame)

def ghost_fan_keys(f_first, every=3, draw_frames=5, alpha_peak=0.75, alpha_rest=0.35):
    """Keys of shot 7's fan: track i starts at f_first + (i-1)*every and is drawn in draw_frames, flashing to alpha_peak then settling."""
    for i in range(1, 7):
        f0 = f_first + (i - 1) * every
        set_ghost(i, 0.0, alpha_peak, frame=f0 - 1); set_ghost(i, 1.0, alpha_peak, frame=f0 + draw_frames); set_ghost(i, 1.0, alpha_rest, frame=f0 + draw_frames + 6)

# ---- tick stamp (shot 7, lands on the chalk curve at 12.95)
TICK_D = 0.20
def _build_tick():
    m = _lit('tick', image=paper_png('tick_stamp', (TICK_D, TICK_D), 512), gain=0.40, alpha=True)
    _alpha_mask(m, _driven_value(m.node_tree, 'tick_alpha'))
    root = _empty('tick_root'); q = _grid_quad('tick_stamp', TICK_D, TICK_D, m, origin=(TICK_D / 2, TICK_D / 2)); q.parent = root; q.visible_shadow = False
    STATE['tick_xz'] = (CHALK_BEND[0] + 0.13, CHALK_BEND[1] + 0.02)

def set_tick(alpha=1.0, scale=1.0, xz=None, rot_deg=-12.0, frame=None):
    """Tick-mark stamp impression on the chalk curve (default: just right of the bend). alpha 0..1 (it lands at 1);
    scale > 1 for the 'thunk' pop (1.25 -> 1.0 over 3 frames)."""
    root = STATE['objects']['tick_root']; x, z = xz or STATE['tick_xz']
    root.location = (x, MAP_Y - 0.0026, z); root.rotation_euler = (0, -math.radians(rot_deg), 0); root.scale = (scale,) * 3
    _key_xform(root, frame); _setp('tick_alpha', alpha, frame)

# ---- ruler: on the map along the track (set prop) and a hand-held copy
RUL_L, RUL_W, RUL_T = 1.30, 0.11, 0.014
def _ruler_mesh(name):
    face = _lit('ruler_face', image=STATE['tex']['ruler'], gain=0.6); wood = _lit('ruler_wood', '#b9824c', gain=0.6)
    mb = S.MB(); w, l, t = RUL_W, RUL_L, RUL_T
    mb.box((-w / 2, -t, -l / 2), (w / 2, 0.0, l / 2), wood, mats=dict(front=wood))
    mb.quad((-w / 2, -t - 0.0005, l / 2), (0, 0, -l), (w, 0, 0), face, (0, 0, 1, 1))   # top face (toward the room), u along the length
    return _mbobj(mb, name, hull=0.004)

def _build_ruler():
    r = _empty('ruler_root'); _ruler_mesh('ruler').parent = r
    h = _empty('ruler_hand_root'); _ruler_mesh('ruler_hand').parent = h
    hd = math.radians(STATE['A']['track_heading_deg'])
    d = Vector((-math.sin(hd), 0, math.cos(hd))); left = Vector((-math.cos(hd), 0, -math.sin(hd)))     # along the track (up), and toward its west side
    mid = (Vector(TRACK0) + Vector(TRACK1)) / 2; off = RUL_W / 2 + S.TRACK_R + 0.003
    STATE['ruler_on'] = dict(loc=Vector((mid.x, MAP_Y, mid.z)) + left * off, rot=Euler((0, -hd, 0)))
    STATE['ruler_dir'] = d; STATE['ruler_left'] = left

def set_ruler(on, side=0.0, frame=None):
    """Ruler on the map. on = 1: flat on the paper, its east edge on the red line (the pencil runs up that edge; it shadows only the
    paper west of the line); on = 0: lifted off, 0.45 D into the room, swung 35 deg and tipped 60 deg (the slap-on / whip-off
    pose; it is hidden below on 0.02). side shifts it across the line (D, + = east)."""
    root = STATE['objects']['ruler_root']; st = STATE['ruler_on']; k = 1.0 - max(0.0, min(1.0, on))
    loc = st['loc'] - STATE['ruler_left'] * side + Vector((0.18 * k, -0.45 * k, -0.15 * k))
    R = st['rot'].to_matrix() @ Matrix.Rotation(math.radians(35 * k), 3, 'Y') @ Matrix.Rotation(math.radians(-60 * k), 3, 'Z')
    root.location = loc; root.rotation_euler = R.to_euler('XYZ'); _key_xform(root, frame, scale=False)
    _set_vis_tree(root, on > 0.02, frame)

def set_ruler_hand(loc=None, angle_deg=0.0, facing=(0, -1, 0), show=1.0, frame=None):
    """Hand-held ruler (shot 11d 'like a rifle'): its centre at world `loc` (put it on the hand ball the shot solved), its long axis
    at angle_deg from vertical in the plane facing `facing` (normal toward the camera, e.g. the actor card's normal)."""
    root = STATE['objects']['ruler_hand_root']
    if loc is not None: root.location = loc
    root.rotation_euler = _basis(facing, roll_deg=-angle_deg).to_euler('XYZ'); _key_xform(root, frame, scale=False); _set_vis_tree(root, show > 0.001, frame)

# ---- nickname label + red pin (shot 13 on)
def _build_label():
    A = STATE['A']; R = A['label_rect']
    m = _lit('label', image=paper_png('nickname_label', (LABEL_W, LABEL_H), 1200), gain=0.30, alpha=True)
    STATE['label_mats'] = {'lo': paper_png('nickname_label', (LABEL_W, LABEL_H), 1200), 'hi': paper_png('nickname_label', (LABEL_W, LABEL_H))}
    root = _empty('label_root', (R['x0'] + LB_PIN[0], MAP_Y - 0.004, R['z1'] - LB_PIN[1]))
    q = _grid_quad('label', LABEL_W, LABEL_H, m, nx=16, nz=5, origin=LB_PIN); q.parent = root
    q.shape_key_add(name='Basis'); kc = q.shape_key_add(name='curl', from_mix=False); kf = q.shape_key_add(name='flutter', from_mix=False)
    for i, v in enumerate(q.data.vertices):
        u = (v.co.x + LB_PIN[0]) / LABEL_W; w = (-v.co.z + LB_PIN[1]) / LABEL_H          # u 0 left .. 1 right, w 0 top .. 1 bottom
        c = max(0.0, (u - 0.72) / 0.28) * max(0.0, (w - 0.35) / 0.65); kc.data[i].co = v.co + Vector((-0.02 * c, -0.07 * c * c, 0.025 * c * c))
        kf.data[i].co = v.co + Vector((0, -0.022 * (0.5 + 0.5 * math.sin(math.pi * 3 * u + 0.7)) * (0.3 + w), 0))     # toward the room only
    _shape_driver(q, 'curl', 'label_curl'); _shape_driver(q, 'flutter', 'label_flutter')
    brass = _lit('pin_red', '#c8301c', gain=0.6); steel = _lit('pin_steel', '#9aa0ae', gain=0.5)
    mb = S.MB(); mb.frustum((0, -0.016, 0), (0, 0.006, 0), 0.003, 0.003, steel, seg=8); mb.sphere((0, -0.026, 0), 0.016, brass, seg=14, rings=7)
    pin = _mbobj(mb, 'label_pin'); pin.parent = root

def set_label(show=1.0, tilt_deg=4.0, swing_deg=0.0, away=0.0, scale=1.0, curl=0.0, flutter=0.0, pin=1.0, pin_out=0.0, res=None, raise_d=0.0, frame=None):
    """Nickname label 'ทางด่วนพายุ' (1.15 x 0.34 D) hanging from its red pin above the arrow head (label_rect). tilt_deg: its resting
    tilt (positive = counter-clockwise as seen from the room); swing_deg: extra rock about the pin (the 4 deg rock after the slap,
    the swing when the chief taps it); away: D off the wall toward the room (slap from 0.12 to 0); scale: slap pop; curl 0..1:
    the lower-right corner curls off the paper; flutter 0..1: a ripple; pin 0/1 shows the red pin; pin_out: its head stands
    this far from the paper (thumbed home = 0); res 'lo' (1200 px, default) / 'hi' (2400 px, for label_insert);
    raise_d moves the whole label up (D; the plan's fallback 0.1 if it must clear BOSTON or a shadow)."""
    root = STATE['objects']['label_root']; A = STATE['A']; R = A['label_rect']
    root.location = (R['x0'] + LB_PIN[0], MAP_Y - 0.004 - away, R['z1'] - LB_PIN[1] + raise_d); root.rotation_euler = (0, -math.radians(tilt_deg + swing_deg), 0)
    root.scale = (scale,) * 3; _key_xform(root, frame)
    pn = STATE['objects']['label_pin']; pn.location = (0, -pin_out, 0); pn.scale = (max(1e-4, pin),) * 3; _key_xform(pn, frame, rot=False)
    _key_vis(STATE['objects']['label'], show > 0.001, frame); _key_vis(pn, show > 0.001 and pin > 0.001, frame)
    _setp('label_curl', curl, frame); _setp('label_flutter', flutter, frame)
    if res: _image_node(STATE['objects']['label'].active_material).image = S._img(STATE['label_mats'][res])

def label_corners():
    """World corners (tl, tr, br, bl) and pin of the label as currently set (for registration of the chief's hand and QA)."""
    root = STATE['objects']['label_root']; bpy.context.view_layer.update(); M = root.matrix_world
    loc = [(-LB_PIN[0], 0, LB_PIN[1]), (LABEL_W - LB_PIN[0], 0, LB_PIN[1]), (LABEL_W - LB_PIN[0], 0, LB_PIN[1] - LABEL_H), (-LB_PIN[0], 0, LB_PIN[1] - LABEL_H)]
    return [tuple(M @ Vector(p)) for p in loc], tuple(M @ Vector((0, -0.026, 0)))

# ---- smudge halo (three levels) and eraser crumbs
def _build_smudge():
    r = random.Random(11); img = STATE['tex']['blotch']
    spans = {1: (0.70, 1.0, 7), 2: (0.40, 1.0, 9), 3: (0.0, 1.0, 12)}                 # level k: u range along the track, number of blotches
    for k, (u0, u1, n) in spans.items():
        m = _lit('smudge%d' % k, image=img, gain=0.40, alpha=True)
        _alpha_mask(m, _driven_value(m.node_tree, 'smudge_level', 'clamp(v-%d)*0.85' % (k - 1), label='smudge%d' % k))
        mb = S.MB()
        for j in range(n):
            u = u0 + (u1 - u0) * (j + r.uniform(0.1, 0.9)) / n; x, z = track_xz(min(1.03, u)); side = r.uniform(-0.07, 0.07)
            w = r.uniform(0.09, 0.16); h = r.uniform(0.06, 0.11); a = math.radians(r.uniform(-50, 50)); y = MAP_Y - 0.0004 - 0.00005 * (j + 10 * k)
            cx, cz = x + side, z + r.uniform(-0.03, 0.03); ca, sa = math.cos(a), math.sin(a)
            corners = [(cx + (-w / 2) * ca - (-h / 2) * sa, cz + (-w / 2) * sa + (-h / 2) * ca), (cx + (w / 2) * ca - (-h / 2) * sa, cz + (w / 2) * sa + (-h / 2) * ca),
                       (cx + (w / 2) * ca - (h / 2) * sa, cz + (w / 2) * sa + (h / 2) * ca), (cx + (-w / 2) * ca - (h / 2) * sa, cz + (-w / 2) * sa + (h / 2) * ca)]
            mb.pid += 1; mb.face([(px, y, pz) for px, pz in corners][::-1], m, [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
        ob = _mbobj(mb, 'smudge_halo%d' % k); ob.visible_shadow = False

def set_smudge(level, frame=None):
    """Halo of pink rubbing smudges round the red line, level 0..3 (continuous): 1 = round the N.Y. end, 2 = the upper half,
    3 = the whole line (shot 11d 'a bold red line inside a halo of pink smudges'). The set's own erase smudge is set_track's."""
    _setp('smudge_level', level, frame)

def _build_crumbs():
    r = random.Random(5); m = _lit('crumbs', '#e58d86', gain=0.6); nt = m.node_tree; ux, _ = _uv_x(nt)
    _alpha_mask(m, _math(nt, 'LESS_THAN', ux, _driven_value(nt, 'crumbs')))
    lz = STATE['A']['ledge']['z']; mb = S.MB(); n = 70
    for i in range(n):
        x = r.gauss(0.18, 0.22); y = r.uniform(-0.175, -0.03); s = r.uniform(0.008, 0.02); hgt = s * r.uniform(0.5, 0.9); rank = (i + 0.5) / n
        mb.pid += 1; mb._in = True
        for (p0, pu, pv) in (((x, y, lz + hgt), (s, 0, 0), (0, s * 0.8, 0)), ((x, y, lz), (s, 0, 0), (0, 0, hgt)), ((x + s, y, lz), (0, s * 0.8, 0), (0, 0, hgt)),
                             ((x, y + s * 0.8, lz), (0, -s * 0.8, 0), (0, 0, hgt))):
            mb.quad(p0, pu, pv, m, (rank, 0, rank, 1))
        mb._in = False
    _mbobj(mb, 'eraser_crumbs')

def set_crumbs(amount, frame=None):
    """Pink eraser crumbs on the chalk ledge under the N.Y. end, amount 0..1 (fraction of 70 crumbs shown, in a fixed random order)."""
    _setp('crumbs', amount, frame)

# ---- forecast sheet (hi-res quad of shot 14) with popping layers
def _build_sheet():
    D = STATE['tex']; root = _empty('sheet_root'); STATE['sheet_layers'] = {}
    layers = [('base', 'forecast_sheet_base', None, 0.0), ('stamp', 'forecast_stamp', 'sheet_stamp', 0.0012), ('bloom1', None, 'sheet_bloom1', 0.0018),
              ('word1', 'forecast_word_1', 'sheet_word1', 0.0024), ('bloom2', None, 'sheet_bloom2', 0.0030), ('word2', 'forecast_word_2', 'sheet_word2', 0.0036)]
    for key, reg, prop, dy in layers:
        img = D[key] if key.startswith('bloom') else paper_png(reg, (SHEET_W, SHEET_H))
        m = _lit('sheet_' + key, image=img, gain=0.28, alpha=True)
        if prop: _alpha_mask(m, _driven_value(m.node_tree, prop))
        cx, cy = SHEET_WORD_C.get(key.replace('bloom', 'word'), (0.5, 0.5))
        piv = _empty('sheet_%s_pivot' % key, parent=root); piv.location = ((cx - 0.5) * SHEET_W, -dy, (0.5 - cy) * SHEET_H)
        q = _grid_quad('sheet_' + key, SHEET_W, SHEET_H, m, nx=6, nz=8, origin=(cx * SHEET_W, cy * SHEET_H)); q.parent = piv
        q.shape_key_add(name='Basis'); kb = q.shape_key_add(name='bow', from_mix=False)
        for i, v in enumerate(q.data.vertices):
            xs = (v.co.x + cx * SHEET_W) / SHEET_W - 0.5; kb.data[i].co = v.co + Vector((0, 0.10 * (xs * xs * 4 - 1) * 0.25 + 0.025, 0))
        _shape_driver(q, 'bow', 'sheet_bow'); q.visible_shadow = key == 'base'
        STATE['sheet_layers'][key] = (piv, q)
    if 'forecast_sheet' in registry(): STATE['sheet_torn'] = paper_png('forecast_sheet', (SHEET_W, SHEET_H))

def set_sheet(loc=None, facing=None, roll_deg=0.0, show=1.0, scale=1.0, word1=1.0, word2=1.0, stamp=1.0, pop1=0.0, pop2=0.0, bow=0.0, frame=None):
    """Forecast sheet quad 1.08 x 1.40 D (base + stamp + two typed Thai words as layers). loc = its centre, facing = a world point it
    turns its printed face to (e.g. the camera) or None for -y; roll_deg tilts it in its plane; word1/word2/stamp 0..1 show the
    layers (the words pop at 30.85 and 31.30: pop 1 -> 0 over 4 frames gives scale 1.08 and the ink bloom); bow 0..1 bends it
    (trembling: small alternating values). Two finger balls at its bottom edge are the shot's hand sprites."""
    root = STATE['objects']['sheet_root']
    if loc is not None: root.location = loc
    n = (Vector(facing) - root.location) if facing is not None else Vector((0, -1, 0))
    root.rotation_euler = _basis(n, roll_deg=roll_deg).to_euler('XYZ'); root.scale = (scale,) * 3; _key_xform(root, frame)
    for k, p in (('word1', pop1), ('word2', pop2), ('bloom1', pop1), ('bloom2', pop2)):
        piv = STATE['sheet_layers'][k][0]; piv.scale = (1 + 0.08 * p,) * 3; _key_xform(piv, frame, loc=False, rot=False)
    _setp('sheet_word1', word1, frame); _setp('sheet_word2', word2, frame); _setp('sheet_stamp', stamp, frame)
    _setp('sheet_bloom1', 0.9 * pop1 * word1, frame); _setp('sheet_bloom2', 0.9 * pop2 * word2, frame); _setp('sheet_bow', bow, frame)
    _set_vis_tree(root, show > 0.001, frame)

def sheet_fill_camera(sheet_center, facing, fill=0.95, lens=22.0):
    """Camera setup that looks square at the sheet so that its width fills `fill` of the 720 px frame (the end of the crash push)."""
    n = (Vector(facing) - Vector(sheet_center)).normalized(); fpx = 782.22 * lens / 22.0; d = fpx * SHEET_W / (720 * fill)
    return dict(loc=tuple(Vector(sheet_center) + n * d), look_at=tuple(sheet_center), lens=lens)

# ---- teletype paper feed
TT = dict(x=3.17, y=-0.685, slot_z=1.88, w=0.54, h=0.70)
def _build_teletype_feed(replace):
    if replace:                                              # remove the set's blank paper box from the teletype mesh (runtime only)
        ob = S.STATE['objects'].get('teletype')
        if ob is not None:
            bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
            kill = [f for f in bm.faces if 2.89 < f.calc_center_median().x < 3.45 and -0.705 < f.calc_center_median().y < -0.665 and 1.87 < f.calc_center_median().z < 2.37]
            bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update(); STATE['tt_removed_faces'] = len(kill)
    root = _empty('tt_feed_root', (TT['x'], TT['y'], TT['slot_z'])); slide = _empty('tt_feed_slide', parent=root)
    for key, reg, prop, dy in (('paper', 'forecast_sheet_teletype', None, 0.0), ('stamp', 'forecast_stamp', 'tt_stamp', 0.0008)):
        m = _lit('tt_' + key, image=paper_png(reg, (SHEET_W, SHEET_H), 640), gain=0.28, alpha=True); nt = m.node_tree
        gp = nt.nodes.new('ShaderNodeNewGeometry'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(gp.outputs['Position'], sp.inputs[0])
        fac = _math(nt, 'GREATER_THAN', sp.outputs['Z'], TT['slot_z'] + 0.004)          # nothing below the slot: the feed comes out of the machine
        if prop: fac = _math(nt, 'MULTIPLY', fac, _driven_value(nt, prop))
        _alpha_mask(m, fac)
        q = _grid_quad('tt_' + key, TT['w'], TT['h'], m, origin=(TT['w'] / 2, 0.0)); q.parent = slide; q.location = (0, -dy, 0)
        if key == 'stamp': q.visible_shadow = False

def set_teletype(feed=1.0, stamp=0.0, yaw_deg=0.0, show=1.0, frame=None):
    """Teletype paper feed: feed 0 = the sheet is inside the machine, 1 = fully out (top 0.70 D above the slot); the artwork is the
    forecast sheet at half size (0.54 x 0.70 D) with the stamp layer (stamp 0..1, lands 29.82). yaw_deg turns the sheet about the
    vertical through the slot centre toward a camera at the left (negative = face toward -x; window_side sees it well at -45).
    show 0 after the tear (the chief's paper takes over)."""
    root = STATE['objects']['tt_feed_root']; sl = STATE['objects']['tt_feed_slide']
    root.rotation_euler = (0, 0, math.radians(yaw_deg)); sl.location = (0, 0, TT['h'] * max(0.0, min(1.0, feed)))
    _key_xform(root, frame, loc=False, scale=False); _key_xform(sl, frame, rot=False, scale=False)
    _setp('tt_feed', feed, frame); _setp('tt_stamp', stamp, frame); _set_vis_tree(root, show > 0.001, frame)

# ---- rubber stamp (3D, held by the chief)
STAMP_FACE_D = 0.17
def _build_stamp():
    root = _empty('rstamp_root'); wood = _lit('stamp_wood', '#7b3b26', gain=0.7); knob = _lit('stamp_knob', '#3d1c12', gain=0.8)
    face = _lit('stamp_face', image=paper_png('stamp_face', (0.34, 0.34), 512), gain=0.5, alpha=True)
    r = STAMP_FACE_D / 2 + 0.008; mb = S.MB()
    mb.frustum((0, 0, 0.004), (0, 0, 0.05), r, r, wood, seg=24); mb.frustum((0, 0, 0.05), (0, 0, 0.07), r, r * 0.55, wood, seg=24, cap0=False)
    mb.frustum((0, 0, 0.07), (0, 0, 0.17), 0.022, 0.03, knob, seg=12); mb.sphere((0, 0, 0.205), 0.05, knob, seg=16, rings=8)
    body = _mbobj(mb, 'rstamp_body', hull=0.004); body.parent = root
    q = _grid_quad('rstamp_face', STAMP_FACE_D, STAMP_FACE_D, face, origin=(STAMP_FACE_D / 2, STAMP_FACE_D / 2)); q.parent = root
    q.rotation_euler = (math.radians(90), 0, 0); q.location = (0, 0, 0.003)            # lies in the XY plane, facing -Z (down)

def set_stamp(loc=None, face_dir=(0, 0, -1), roll_deg=0.0, scale=1.0, show=1.0, frame=None):
    """3D rubber stamp: loc = centre of its rubber face; face_dir = where the face points (into the paper it stamps, e.g. the
    sheet's -normal). Face 0.17 D across at scale 1 (the impression on the half-size teletype sheet); scale 2 matches the hi-res sheet."""
    root = STATE['objects']['rstamp_root']
    if loc is not None: root.location = loc
    f = Vector(face_dir).normalized(); q = f.to_track_quat('-Z', 'Y'); M = q.to_matrix() @ Matrix.Rotation(math.radians(roll_deg), 3, 'Z')
    root.rotation_euler = M.to_euler('XYZ'); root.scale = (scale,) * 3; _key_xform(root, frame); _set_vis_tree(root, show > 0.001, frame)

# ---- calendar: pad (leaf 21 under) + leaf 20 on top with lift, flutter and tear
def _build_calendar():
    A = STATE['A']; R = A['calendar_rect']; k = (R['x1'] - R['x0']) / CAL_PAD[0]; STATE['cal_k'] = k     # the set maps the 0.66 x 0.90 pad art onto 0.60 x 0.82
    face = S.STATE['objects'].get('calendar_face')
    if face is not None: face.hide_render = True                                      # the set's printed leaf is replaced by our pad + leaf
    pad = _lit('cal_pad21', image=paper_png('calendar_pad_21', CAL_PAD, 800), gain=0.28, alpha=True)
    pad20 = _lit('cal_pad20', image=paper_png('calendar_pad_20', CAL_PAD, 800), gain=0.28, alpha=True)
    STATE['cal_pad_mats'] = dict(pad21=pad, pad20=pad20)
    q = _grid_quad('calendar_pad', R['x1'] - R['x0'], R['z1'] - R['z0'], pad, origin=(0, 0)); q.location = (R['x0'], R['y'], R['z1'])
    leaf = _lit('cal_leaf20', image=paper_png('calendar_leaf_20', CAL_PAD, 800), gain=0.28)
    lx, ly, lw, lh = CAL_LEAF; w, h = lw * k, lh * k
    root = _empty('cal_leaf_root', (R['x0'] + lx * k, R['y'] - 0.0025, R['z1'] - ly * k))           # hinge = the leaf's top edge
    lq = _grid_quad('calendar_leaf', w, h, leaf, nx=6, nz=14, origin=(0, 0)); lq.parent = root
    lq.shape_key_add(name='Basis'); kl = lq.shape_key_add(name='lift', from_mix=False); kf = lq.shape_key_add(name='flutter', from_mix=False)
    nz = 14; nx = 6
    for kb, fn in ((kl, lambda s, u: (1.25 * s ** 1.6, 0.0)), (kf, lambda s, u: (0.55 * s ** 2 * (1 + 0.6 * math.sin(math.pi * u * 2.2)), 0.025 * s * math.sin(math.pi * (u * 3 + s * 2))))):
        for i in range(nx + 1):                              # integrate down each column: segment angle phi(s) from straight down toward the room
            u = i / nx; p = Vector((u * w, 0.0, 0.0))
            for j in range(nz + 1):
                vi = j * (nx + 1) + i; s = j / nz; phi, dy = fn(s, u); kb.data[vi].co = p + Vector((0, -dy, 0))
                p = p + Vector((0, -math.sin(phi), -math.cos(phi))) * (h / nz)
    _shape_driver(lq, 'lift', 'cal_lift'); _shape_driver(lq, 'flutter', 'cal_flutter')

def set_calendar(day=20, lift=0.0, flutter=0.0, tear=0.0, frame=None):
    """Tear-off calendar (calendar_rect). day 20: leaf 20 TUESDAY on top of the pad (leaf 21 under it); day 21: the pad alone,
    leaf 21 WEDNESDAY on top (shots 17, 18, 25). lift 0..1: the leaf's lower part lifts toward the room in a draught (shot 4, 5.6);
    flutter 0..1: a rippling lift (alternate with lift for a flutter); tear 0..1: the leaf comes off and flies down-left into the room."""
    root = STATE['objects']['cal_leaf_root']; A = STATE['A']; R = A['calendar_rect']; k = STATE['cal_k']
    base = Vector((R['x0'] + CAL_LEAF[0] * k, R['y'] - 0.0025, R['z1'] - CAL_LEAF[1] * k)); t = max(0.0, min(1.0, tear))
    root.location = base + Vector((-0.35 * t, -1.1 * t, -1.6 * t * t)); root.rotation_euler = (math.radians(-70 * t), math.radians(40 * t), math.radians(25 * t))
    _key_xform(root, frame, scale=False); _set_vis_tree(root, day == 20 and t < 0.999, frame)
    _setp('cal_lift', lift, frame); _setp('cal_flutter', flutter, frame)
    pad = STATE['objects']['calendar_pad']
    if frame is None: pad.data.materials[0] = STATE['cal_pad_mats']['pad21']

# ---- 6000 px map
def set_map_res(hi=True):
    """Swap the map paper texture between the set's 3000 px (1000 px per D) and the 6000 px raster (tex/map_6000.png, 2000 px per D,
    same drawing) for lens positions closer than about 1 D to the paper (shot 9c corridor_cam, 19, 20, 22). Not animatable: switch per take."""
    ob = S.STATE['objects']['map_paper']; m = ob.active_material; n = _image_node(m)
    if 'map_std' not in STATE: STATE['map_std'] = n.image.filepath
    if hi:
        p = os.path.join(TEXD, 'map_6000.png')
        if not os.path.exists(p):
            sys.path.insert(0, HERE); import make_hi_map; p = make_hi_map.ensure()
        n.image = S._img(p)
    else: n.image = S._img(bpy.path.abspath(STATE['map_std']))
    STATE['map_hi'] = bool(hi)

# ----------------------------------------------------------------------------- QA helper: shadows on the track, the N.Y. label and the nickname label
def track_shadow_report(n=41, label_n=(9, 4)):
    """office3d.track_shadow_report() plus the nickname label: which parts of the red track, the printed N.Y. label and the pinned
    label 'ทางด่วนพายุ' are in cast shadow (sun ray cast, card alpha respected). Shadows of our own props (the spinner sitting on the
    storm end, the label's pin) are listed apart and do not fail the check; neither do the set's own window-bar shadows, which are
    the room's light (listed under label_by_blocker). ok = no ACTOR (or other non-set object) shadows the track, the N.Y. label or the label.
    Returns dict(track_shadowed, track_prop_shadowed, ny_label_shadowed, label_shadowed, label_by_blocker, label_actor_shadowed, ok)."""
    base = S.track_shadow_report(n); props = set(o.name for o in STATE['coll'].objects); setobs = set(S.STATE['objects'])
    trk = [(u, b) for u, b in base['track_shadowed'] if b not in props]; trk_p = [(u, b) for u, b in base['track_shadowed'] if b in props]
    (tl, tr, br, bl), _ = label_corners(); nx, nz = label_n; pts = []
    for i in range(nx):
        for j in range(nz):
            a, b = (i + 0.5) / nx, (j + 0.5) / nz; top = Vector(tl).lerp(Vector(tr), a); bot = Vector(bl).lerp(Vector(br), a); pts.append(top.lerp(bot, b))
    lab = STATE['objects']['label']; was = lab.visible_shadow; lab.visible_shadow = False         # the label must not shadow itself
    try: bl_ = [S.sun_blocker(tuple(p + Vector((0, -0.002, 0)))) for p in pts]
    finally: lab.visible_shadow = was
    by = {}
    for x in bl_:
        if x: by[x] = round(by.get(x, 0) + 1 / len(pts), 3)
    actor = lambda x: x and x not in props and x not in setobs
    lab_act = sum(1 for x in bl_ if actor(x)) / len(pts); ny_act = base['label_shadowed'] if any(actor(x) for x in base.get('label_blockers', [])) else 0.0
    return dict(track_shadowed=trk, track_prop_shadowed=trk_p, ny_label_shadowed=base['label_shadowed'], label_shadowed=round(sum(1 for x in bl_ if x) / len(pts), 3),
                label_by_blocker=by, label_actor_shadowed=round(lab_act, 3), ok=(not any(actor(b) for _, b in trk)) and lab_act == 0 and ny_act == 0)

# ----------------------------------------------------------------------------- anchors: cameras, marks, paths
def _cam(loc, look_at, lens=22, **kw):
    d = dict(loc=tuple(round(x, 4) for x in loc), look_at=tuple(round(x, 4) for x in look_at), lens=lens); d.update(kw); return d

def _aim(target, dist, yaw_deg, pitch_deg, lens=22, look_shift=(0, 0, 0)):
    """Camera `dist` from target: yaw_deg = how far the camera stands to the LEFT of the wall normal (looking toward +x),
    pitch_deg = how far BELOW the target it stands (looking up). look_shift moves the look-at point (not the camera)."""
    y, p = math.radians(yaw_deg), math.radians(pitch_deg); t = Vector(target)
    loc = t + dist * Vector((-math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), -math.sin(p)))
    return _cam(loc, t + Vector(look_shift), lens)

def _dir_cam(loc, yaw_deg, pitch_deg, lens=22):
    """Camera at loc looking along yaw (0 = straight at the map wall, + = turned toward -x) and pitch (+ = up)."""
    y, p = math.radians(yaw_deg), math.radians(pitch_deg); d = Vector((-math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), math.sin(p)))
    return _cam(loc, Vector(loc) + 3.0 * d, lens)

def push(setup, factor, toward=None, recentre=False):
    """The setup moved toward its look-at (or `toward`) so that the subject there grows by `factor` (x1.38 = shot 18's push into G')."""
    L, T = Vector(setup['loc']), Vector(toward or setup['look_at']); loc = T + (L - T) / factor
    out = dict(setup); out['loc'] = tuple(round(x, 4) for x in loc)
    if recentre and toward: out['look_at'] = tuple(toward)
    return out

def anchors(A):
    mx = lambda u: S.track_point(u)
    lab = A['label_rect']; lab_c = ((lab['x0'] + lab['x1']) / 2, MAP_Y, (lab['z0'] + lab['z1']) / 2)
    marks = dict(
        # shot 4 (wide_high): chief by the teletype 1.5 D clear of the walls; shot 14 (window_side re-aimed): hero near, chief by the machine
        teletype_mark=(2.25, -1.70, 0.0), hero_tt=(-1.10, -1.50, 0.0), chief_tt=(2.20, -1.95, 0.0),
        # shot 6 (low_three): three figures 1.2 D off the wall, chief half a pace forward
        senior_a_row=(-0.70, -1.20, 0.0), chief_row=(0.35, -1.45, 0.0), senior_b_row=(1.40, -1.20, 0.0),
        # shot 9a (high_wide): the three 2.2 D in front of the hero at hero_mark
        senior_a_front=(-1.55, -2.62, 0.0), chief_front=(0.40, -2.62, 0.0), senior_b_front=(1.25, -3.05, 0.0),
        # shot 10 G / 18 / 25: hero near at gloat_near (0.3 D from near_mark), chief at boss_mark
        gloat_near=(2.40, -1.70, 0.0),
        # shot 12 (desk_fg): two laughing seniors in the mid-ground 2.5-3.5 D from the lens; chief beside the hero at the wall
        senior_a_desk=(-1.95, -3.00, 0.0), senior_b_desk=(0.20, -2.80, 0.0), chief_wall12=(0.0, -0.55, 0.0),
    )
    cams = dict(
        calendar_cam=_aim((-1.84, -0.048, 4.08), 1.14, -12.0, 8.0, look_shift=(0, 0, -0.09)),          # shot 4 landing: leaf ~420 px wide, 12 deg rake, below the shades
        spinner_rake=_aim(mx(0.0), 0.92, 48.0, 10.0, look_shift=(0.12, 0, 0.14)),                         # shot 5 end of the fly-in (insert_rake family, lens below-left)
        coast_rake=_aim(mx(0.42), 1.55, 55.0, 16.0, look_shift=(0.0, 0, 0.12)),                           # shot 5 pull-back: FLA. low left, N.Y. at the top
        low_three=_dir_cam((2.40, -6.20, 1.0), 22.0, 17.0),                                               # shot 6: 1.0 D up, +17 deg, 22 deg off the wall normal; far enough (6 D) that the sign clears the hats
        chalk_rake=_aim((CHALK_BEND[0], MAP_Y, CHALK_BEND[1]), 0.92, 58.0, 18.0),
        chalk_wide=_aim((0.30, MAP_Y, 2.32), 2.05, 12.0, 4.0),                                            # shot 7b: x0.45 pull-back, 12 deg yaw kept
        high_wide=_cam((-0.45, -6.45, 4.0), (-0.5, -0.6, 1.40)),                                          # shot 9a: 4.0 D up, -24 deg
        insert_front=_aim(mx(0.42), 1.5, 10.0, 6.0),                                                      # shot 9b: 1.5 D from the paper, 10 deg yaw
        corridor_cam=_cam((_track_ext(-0.22)[0], MAP_Y - 0.40, _track_ext(-0.22)[2]), mx(0.80), up=(0, -1, 0)),   # shot 9c/19/20/22: 0.40 D off the paper, up = wall normal
        low_boss=_cam((1.92, -4.40, 1.2), (1.45, -0.42, 2.27)),                                          # shot 10(1): chief at boss_mark, 1.2 D up, ~4 D, +15 deg
        G=_cam((1.55, -4.95, 2.85), (1.25, -0.40, 2.62)),                                                 # THE GLOAT FRAMING (shots 10, 18, 25)
        low_two_wall=_cam((0.40, -3.70, 1.2), (0.40, 0.0, 2.12)),                                        # shot 11c: both at the wall, +14 deg
        insert_rake_ny=_cam((-1.30, -0.66, 2.55), (0.30, -0.05, 2.74)),                                   # shot 11a/b: reviewed insert_rake moved to the N.Y. end
        label_insert=_aim(lab_c, 1.84, 12.0, 12.0, look_shift=(0, 0, -0.40)),                            # shot 13: label ~480 px wide at y ~470, arrow head under it
        window_tt=_cam((-3.2, -2.6, 2.1), (2.6, -1.0, 1.85)),                                           # shot 14a: window_side re-aimed at the teletype
    )
    cams['G_prime'] = dict(cams['G'], look_at=(0.95, -0.40, 2.80), lens=round(22 * 1.38, 2))           # shot 18 push x1.38 as a zoom from G's exact pose, centred between the chief and the label
    cams['G_prime_dolly'] = push(cams['G'], 1.38, toward=(1.30, -0.42, 2.87)); cams['G_prime_dolly']['look_at'] = (1.05, -0.40, 2.90)   # the same x1.38 on the chief as a dolly (hero mostly out at right)
    sheet_hold = (1.75, -2.20, 2.05); sheet_face = (1.75 - 0.6, -2.20 - 0.8, 2.05)                       # in the sun beam, turned to face between the lens and the window (lit)
    cams['sheet_full'] = sheet_fill_camera(sheet_hold, sheet_face, fill=1.0)                             # shot 14c: the sheet fills the frame
    paths = dict(
        persist_steps=[('a', 'insert_rake_ny'), ('b', dict(cams['insert_rake_ny'], loc=tuple(Vector(cams['insert_rake_ny']['loc']) - Vector((0, 0, 0.4))),
                                                       look_at=tuple(Vector(cams['insert_rake_ny']['look_at']) - Vector((0, 0, 0.25))))),
                       ('c', 'low_two_wall'), ('d', 'high_two_shot')],
        flight_shot4=['wide_high', 'calendar_cam'], shot5=['spinner_rake', 'coast_rake'], shot7=['chalk_rake', 'chalk_wide'],
        shot9=['high_wide', 'insert_front', 'corridor_cam'], shot10=['low_boss', 'G'], shot14=['window_tt', 'sheet_full'])
    tt = dict(slot=(TT['x'], TT['y'], TT['slot_z']), feed_top_full=(TT['x'], TT['y'], TT['slot_z'] + TT['h']), size=(TT['w'], TT['h']))
    return dict(cams=cams, marks=marks, paths=paths, sheet_hold=sheet_hold, sheet_face=sheet_face, sheet_size=(SHEET_W, SHEET_H), teletype_feed=tt,
                chalk_ctrl=CHALK_CTRL, chalk_bend=CHALK_BEND, ghost_ctrl=GHOST_CTRL, tick_xz=STATE.get('tick_xz'),
                label_pin=(lab['x0'] + LB_PIN[0], MAP_Y - 0.004, lab['z1'] - LB_PIN[1]), label_size=(LABEL_W, LABEL_H),
                ruler=dict(center=tuple(STATE['ruler_on']['loc']), size=(RUL_W, RUL_L, RUL_T), east_edge_on_track=True),
                spinner_d=SPIN_D, stamp_face_d=STAMP_FACE_D, calendar_leaf_hinge=tuple(STATE['objects']['cal_leaf_root'].location),
                crumbs_area=dict(x=(-0.3, 0.65), y=(-0.175, -0.03), z=A['ledge']['z']), placeholders=list(PLACEHOLDERS))

def all_cams(A, PA):
    """Set cameras + the new ones (new names win)."""
    c = dict(A['cams']); c.update(PA['cams']); return c

def resolve_cam(name_or_setup, A, PA):
    return all_cams(A, PA)[name_or_setup] if isinstance(name_or_setup, str) else name_or_setup

# ----------------------------------------------------------------------------- debug markers
def add_markers(PA, size=0.025):
    """Small camera-only emissive spheres on every new anchor (debug stills): yellow = map props, cyan = marks (floor), magenta =
    sheet / teletype / stamp, green = calendar, orange = label pin and corners, white = chalk control points."""
    coll = S._coll('PROP_MARKERS', bpy.context.scene); S._wipe(coll); cols = dict(y='#ffe100', c='#18e0f0', m='#ff2bd6', g='#28f050', o='#ff8a00', w='#ffffff')
    mats = {k: S.mat_emit('px_marker_' + k, v, strength=2.0) for k, v in cols.items()}; pts = []
    for u in (0.0, 0.5, 1.0): pts.append(('y', S.track_point(u)))
    for x, z in PA['chalk_ctrl']: pts.append(('w', (x, MAP_Y - 0.01, z)))
    pts.append(('y', (PA['tick_xz'][0], MAP_Y - 0.01, PA['tick_xz'][1]))); pts.append(('y', PA['ruler']['center']))
    (tl, tr, br, bl), pin = label_corners(); pts += [('o', p) for p in (tl, tr, br, bl, pin)]
    for v in PA['marks'].values(): pts.append(('c', v))
    pts += [('m', PA['sheet_hold']), ('m', PA['teletype_feed']['slot']), ('m', PA['teletype_feed']['feed_top_full']), ('g', PA['calendar_leaf_hinge'])]
    R = STATE['A']['calendar_rect']; pts += [('g', (x, R['y'] - 0.01, z)) for x in (R['x0'], R['x1']) for z in (R['z0'], R['z1'])]
    ca = PA['crumbs_area']; pts += [('y', (ca['x'][i], -0.1, ca['z'])) for i in (0, 1)]
    for k, p in pts:
        mb = S.MB(); mb.sphere(p, size * (1.6 if k == 'c' else 1.0), mats[k], seg=10, rings=5); o = mb.obj('marker', coll); o.visible_shadow = False; S.no_bounce(o)
    return len(pts)

if __name__ == '__main__':
    print(__doc__)
