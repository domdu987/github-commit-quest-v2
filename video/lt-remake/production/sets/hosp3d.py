"""Male general ward (หอผู้ป่วยชาย 2) of a Thai community hospital, the morning after the storm, as a real 3D set (bpy 5.3, Cycles CPU).
World: 1 unit = 1 m, Z up, floor z = 0. The ward runs along +y: camera-end wall (double doors) y = -2, nurse station at the far end, back wall y = 15.
Side walls x = -3.5 (left row of beds) and x = +3.5 (right row, sun side). Ceiling 3.5. Beds: heads against the side walls, feet to the aisle (x -1.37..1.37).
Light model from office3d.mat_lit: ambient as emission (blue-violet shade, per-material shade_fix as soi3d) + one hard low sun through the right-hand
windows (venetian blinds, ventilation blocks) that rakes across the aisle and the left row; fluorescent tubes and screens are emissive.
Swappable screens: objects + materials `phone_screen_<i>` (i = 0..5, one per bed) and `monitor_screen`: see set_phone_screen / set_monitor_screen.
CLI: python3 hosp3d.py stills [day] [final|preview] [cam ...]   -> out_hosp/<cam>.png (+ timing.json, anchors.json)
     python3 hosp3d.py land [day]                               -> out_hosp/wide_ward_16x9.png (1920x1080)"""
import os, sys, math, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix, Euler
import office3d as S
import tex_hosp
MB = S.MB
OUT = os.path.join(HERE, 'out_hosp')

XW, Y0, Y1, HC = 3.5, -2.0, 15.0, 3.5            # side walls at +-XW, end walls, ceiling
WALL_T = 0.22                                     # wall thickness at the window reveals
WIN_Y, WIN_HW, WIN_Z = tex_hosp.WIN_Y, tex_hosp.WIN_HW, (0.95, 2.9)
VENT_Z = (3.0, 3.38)                              # ventilation blocks (ช่องลม) above every window
BED_Y = tex_hosp.BED_Y; BED_HEAD = tex_hosp.BED_HEAD; BED_LEN = tex_hosp.BED_LEN
HERO = 1                                          # bed index of the hero bed (left row, middle)
CAB_A = tex_hosp.CAB_A                            # bedside locker centre, distance from the head wall (a)
PRESETS = {
    'day': dict(shade=(0.205, 0.185, 0.43), key=(2.5, 2.16, 1.3), lift=(0.012, 0.012, 0.03), key_dir=(-0.78, -0.26, -0.30), sun_angle=0.3,
                form=(0.06, 0.0, 0.2), falloff_y=0.0, bloom_size=0.05, grade_offset=(0.003, 0.003, 0.010), grade_saturation=1.08,
                tubes=2.4, gain=0.43, screens=1.0, monitor=1.15, shafts=0.1, ext=1.0),
}
A = {}; P = {}; M = {}; TX = {}

# ----------------------------------------------------------------------------- materials (as soi3d)
_MEAN = {}
def art_mean(img=None, color='#808080'):
    if img is None: return S.hex_lin(color)
    if img not in _MEAN:
        from PIL import Image
        import numpy as np
        a = np.asarray(Image.open(TX[img]).convert('RGBA').resize((64, 64)), dtype=float) / 255; m = a[..., 3] > 0.5
        c = a[..., :3][m] if m.any() else a[..., :3].reshape(-1, 3); c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        _MEAN[img] = tuple(float(x) for x in c.mean(0))
    return _MEAN[img]

def shade_fix(mean, strength=0.8):
    """Per-channel shade multiplier: art x SHADE -> the preset's blue-violet shade hue, at the luminance a neutral art of the same luminance would
    have (soi3d's version also lifted every surface to the art's own luminance; here the brightness of the shade is set by P['shade'] alone)."""
    sh = P['shade']; lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    L = max(lum(mean), 1e-4); want = [x * L for x in sh]; got = [max(m * x, 1e-5) for m, x in zip(mean, sh)]
    return tuple(min(2.2, max(0.45, (w / g) ** strength)) for w, g in zip(want, got))

def lit(name, img=None, color='#808080', gain=0.9, shade=None, alpha=False, fix=0.3, lift=1.0):
    sm = shade if shade is not None else shade_fix(art_mean(img, color), fix)
    sm = tuple(x * lift for x in sm)
    return S.mat_lit('HOSP_' + name, color=color, image=img and TX[img], gain=gain * P['gain'], shade_mul=sm, alpha=alpha, form=P['form'])

def emit(name, color='#ffffff', strength=1.0, img=None):
    return S.mat_emit('HOSP_E_' + name, color, image=img and TX[img], strength=strength)

def flat(hexcol, gain=0.85, fix=0.3):
    nm = 'f_%s_%g_%g' % (hexcol.lstrip('#'), gain, fix)
    if nm not in M: M[nm] = lit(nm, color=hexcol, gain=gain, fix=fix)
    return M[nm]

def screen_mat(name, img, strength):
    """Swappable screen: Image (node 'SCREEN_TEX') x tint (node 'SCREEN_TINT', input 7) -> Emission (node 'SCREEN_EMIT'). Unlit, never lights the set."""
    m = bpy.data.materials.get(name)
    if m: bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); nt = m.node_tree if m.node_tree else None
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.name = 'SCREEN_TEX'; tex.image = S._img(img)
    tex.extension = 'EXTEND'; mix = nt.nodes.new('ShaderNodeMix'); mix.name = 'SCREEN_TINT'; mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs[0].default_value = 1.0
    mix.inputs[7].default_value = (1, 1, 1, 1); emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'SCREEN_EMIT'; emi.inputs['Strength'].default_value = strength
    L(tex.outputs['Color'], mix.inputs[6]); L(mix.outputs[2], emi.inputs['Color']); L(emi.outputs['Emission'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def shaft_mat(strength):
    """Fake light shaft: transparent + warm emission fading with the UV v (0 at the window, 1 where the shaft meets the floor). Camera rays only."""
    name = 'HOSP_shaft'; m = bpy.data.materials.get(name)
    if m: bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
    inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; inv.use_clamp = True
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.2
    mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = strength
    lp = nt.nodes.new('ShaderNodeLightPath'); mc = nt.nodes.new('ShaderNodeMath'); mc.operation = 'MULTIPLY'
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*S.hex_lin('#fff1d6'), 1); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); ad = nt.nodes.new('ShaderNodeAddShader')
    L(tc.outputs['UV'], sx.inputs[0]); L(sx.outputs['Y'], inv.inputs[1]); L(inv.outputs[0], pw.inputs[0]); L(pw.outputs[0], mu.inputs[0])
    L(mu.outputs[0], mc.inputs[0]); L(lp.outputs['Is Camera Ray'], mc.inputs[1]); L(mc.outputs[0], emi.inputs['Strength'])
    L(tr.outputs['BSDF'], ad.inputs[0]); L(emi.outputs['Emission'], ad.inputs[1]); L(ad.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def materials():
    m = dict(
        floor=lit('floor', 'floor', gain=0.92, fix=0.3), wall_low=lit('wall_low', 'wall_low', gain=0.9, fix=0.3, lift=1.05), wall_up=lit('wall_up', 'wall_up', gain=0.9, fix=0.3, lift=1.1),
        ceiling=lit('ceiling', 'ceiling', gain=0.9, fix=0.3, lift=0.82), ceiling_stain=lit('ceiling_stain', 'ceiling_stain', gain=0.9, fix=0.3, lift=0.82),
        curtain_g=lit('curtain_g', 'curtain_g', gain=0.85, fix=0.3, lift=1.0), curtain_b=lit('curtain_b', 'curtain_b', gain=0.85, fix=0.3, lift=1.0),
        net=lit('net', 'net', gain=0.85, alpha=True, lift=1.1), blanket=lit('blanket', 'blanket', gain=0.88, fix=0.3, lift=1.0), sheet=lit('sheet', 'sheet', gain=0.85, lift=1.15),
        pillow=lit('pillow', 'pillow', gain=0.85, lift=1.15), headwall=lit('headwall', 'headwall', gain=0.85, lift=1.1), cabinet=lit('cabinet', 'cabinet', gain=0.85, lift=1.1),
        monitor_body=lit('monitor_body', 'monitor_body', gain=0.85, lift=1.1), station_front=lit('station_front', 'station_front', gain=0.85),
        back_wall=lit('back_wall', 'back_wall', gain=0.9, fix=0.3, lift=1.15), near_wall=lit('near_wall', 'near_wall', gain=0.9, fix=0.3, lift=1.15),
        binders=lit('binders', 'binders', gain=0.85), signs=lit('signs', 'signs', gain=0.85, fix=0.3, lift=1.1), posters=lit('posters', 'posters', gain=0.85, fix=0.3, lift=1.1),
        clock=lit('clock', 'clock', gain=0.85, lift=1.15), leaves=lit('leaves', 'leaves', gain=0.85, alpha=True), ivbag=lit('ivbag', 'ivbag', gain=0.85, lift=1.1),
        chart=lit('chart', 'chart', gain=0.85, lift=1.1), wc_seat=lit('wc_seat', 'wc_seat', gain=0.85), cart=lit('cart', 'cart', gain=0.85, fix=0.3),
        vent=lit('vent', 'vent', gain=0.85, alpha=True, lift=1.1),
        tube=emit('tube', '#f2f8ff', P['tubes']), ext_r=emit('ext_r', strength=P['ext'], img='ext_r'), ext_l=emit('ext_l', strength=P['ext'] * 0.95, img='ext_l'),
        led_g=emit('led_g', '#58f070', 1.4), led_r=emit('led_r', '#ff4030', 1.4), shaft=shaft_mat(P['shafts']),
    )
    M.update(m)

# ----------------------------------------------------------------------------- geometry helpers
def newell(pts):
    n = Vector((0, 0, 0))
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]; n += Vector(((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y)))
    return n

def F(mb, pts, mat, uvs=None, n=None):
    pts = [Vector(p) for p in pts]; uvs = list(uvs) if uvs else ([(0, 0), (1, 0), (1, 1), (0, 1)] if len(pts) == 4 else None)
    if n is not None and newell(pts).dot(Vector(n)) < 0: pts = pts[::-1]; uvs = uvs[::-1] if uvs else None
    keep = [i for i in range(len(pts)) if (pts[i] - pts[i - 1]).length > 1e-6]
    if len(keep) < 3: return
    mb.pid += 1; mb.face([pts[i] for i in keep], mat, [uvs[i] for i in keep] if uvs else None)

def rect(mb, c, u, v, mat, uv=(0, 0, 1, 1), n=None):
    c, u, v = Vector(c), Vector(u), Vector(v); u0, v0, u1, v1 = uv
    F(mb, [c - u - v, c + u - v, c + u + v, c - u + v], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], n)

def tube(mb, pts, r, mat, seg=5):
    pts = [Vector(p) for p in pts]
    if len(pts) < 2: return
    mb.pid += 1; t = (pts[1] - pts[0]).normalized(); u = t.cross(Vector((0, 0, 1)))
    if u.length < 1e-3: u = t.cross(Vector((1, 0, 0)))
    u.normalize(); rings = []
    for i, p in enumerate(pts):
        tn = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        u = (u - tn * u.dot(tn)); u = u.normalized() if u.length > 1e-6 else tn.orthogonal().normalized(); v = tn.cross(u)
        rings.append([p + r * (math.cos(2 * math.pi * k / seg) * u + math.sin(2 * math.pi * k / seg) * v) for k in range(seg)])
    for i in range(len(rings) - 1):
        for k in range(seg):
            j = (k + 1) % seg; mb.face([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]], mat)

def smooth(pts, n=6):
    """Catmull-Rom through pts."""
    pts = [Vector(p) for p in pts]; out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n; out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1]); return out

def ring(c, r, n=24, axis='z'):
    c = Vector(c); out = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n; d = {'z': (math.cos(a), math.sin(a), 0), 'x': (0, math.cos(a), math.sin(a)), 'y': (math.cos(a), 0, math.sin(a))}[axis]
        out.append(c + r * Vector(d))
    return out

def blob(mb, c, ex, ey, ez, mat, nu=14, nv=8, p=0.45):
    """Superellipsoid (pillows, bags, lumps). ex, ey, ez = half-axis vectors; UV = planar projection on the ex/ey plane."""
    c, ex, ey, ez = Vector(c), Vector(ex), Vector(ey), Vector(ez); f = lambda w: math.copysign(abs(w) ** p, w); mb.pid += 1; R = []
    for i in range(nv + 1):
        th = -math.pi / 2 + math.pi * i / nv; row = []
        for j in range(nu):
            ph = 2 * math.pi * j / nu; a, b = f(math.cos(th)) * f(math.cos(ph)), f(math.cos(th)) * f(math.sin(ph))
            row.append((c + ex * a + ey * b + ez * f(math.sin(th)), (0.5 + 0.5 * a, 0.5 + 0.5 * b)))
        R.append(row)
    for i in range(nv):
        for j in range(nu):
            k = (j + 1) % nu; q = [R[i][j], R[i][k], R[i + 1][k], R[i + 1][j]]
            pts = [x[0] for x in q]; uvs = [x[1] for x in q]
            keep = [t for t in range(4) if (pts[t] - pts[t - 1]).length > 1e-7]
            if len(keep) >= 3: mb.face([pts[t] for t in keep], mat, [uvs[t] for t in keep])

class BF:
    """Frame of one bed: a = from the head (wall) toward the foot (aisle), b = across (left row: +y), z up. side 'L' (x = -XW) or 'R'."""
    def __init__(s, side, cy):
        s.s = 1 if side == 'L' else -1; s.cy = cy; s.L = side == 'L'; s.side = side; s.off = 0.0
    def P(s, a, b, z): a = a + s.off; return Vector((-s.s * BED_HEAD + s.s * a, s.cy + s.s * b, z))
    def vec(s, a, b, z): return Vector((s.s * a, s.s * b, z))
    def box(s, mb, a0, a1, b0, b1, z0, z1, mat, front=None, tile=None, mats=None):
        p, q = s.P(a0, b0, z0), s.P(a1, b1, z1); lo = (min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)); hi = (max(p.x, q.x), max(p.y, q.y), max(p.z, q.z))
        mm = dict(mats or {})
        if front: mm['right' if s.L else 'left'] = front
        mb.box(lo, hi, mat, mats=mm or None, tile=tile)
    def cyl(s, mb, a, b, z0, z1, r, mat, seg=10): mb.frustum(tuple(s.P(a, b, z0)), tuple(s.P(a, b, z1)), r, r, mat, seg=seg)
    def wheel(s, mb, a, b, r=0.05):
        blk = flat('#26262a', 0.8); mb.box(tuple(s.P(a, b, 0.07) - Vector((0.02, 0.02, 0))), tuple(s.P(a, b, 0.07) + Vector((0.02, 0.02, 0.09))), flat('#9ea4aa'))
        mb.frustum(tuple(s.P(a - 0.03, b - 0.018, r)), tuple(s.P(a - 0.03, b + 0.018, r)), r, r, blk, seg=12)

# ----------------------------------------------------------------------------- room: floor, walls with windows, ceiling, exterior
def room(G):
    mb, mba = G['room'], G['alpha']
    mb.quad((-XW, Y0, 0), (2 * XW, 0, 0), (0, Y1 - Y0, 0), M['floor'])
    # ceiling: tiles (1.2 m), one stained tile above the leak
    F(mb, [(-XW, Y0, HC), (XW, Y0, HC), (XW, Y1, HC), (-XW, Y1, HC)], M['ceiling'], [(-XW / 1.2, Y0 / 1.2), (XW / 1.2, Y0 / 1.2), (XW / 1.2, Y1 / 1.2), (-XW / 1.2, Y1 / 1.2)], (0, 0, -1))
    F(mb, [(0.6, 9.0, HC - 0.004), (1.8, 9.0, HC - 0.004), (1.8, 10.2, HC - 0.004), (0.6, 10.2, HC - 0.004)], M['ceiling_stain'], None, (0, 0, -1))
    # end walls (painted art) and side walls with window openings
    F(mb, [(-XW, Y1, 0), (XW, Y1, 0), (XW, Y1, HC), (-XW, Y1, HC)], M['back_wall'], None, (0, -1, 0))
    F(mb, [(XW, Y0, 0), (-XW, Y0, 0), (-XW, Y0, HC), (XW, Y0, HC)], M['near_wall'], None, (0, 1, 0))
    for s in (-1, 1):
        x = s * XW; n = (-s, 0, 0)
        def wq(y0, y1, z0, z1, mat, tu, tv, zo=0.0, d=0.0):
            xx = x - s * d
            F(mb, [(xx, y0, z0), (xx, y1, z0), (xx, y1, z1), (xx, y0, z1)], mat, [(y0 / tu, (z0 - zo) / tv), (y1 / tu, (z0 - zo) / tv), (y1 / tu, (z1 - zo) / tv), (y0 / tu, (z1 - zo) / tv)], n)
        wq(Y0, Y1, 0, WIN_Z[0], M['wall_low'], 4, 1)
        ys = [Y0] + sum([[wy - WIN_HW, wy + WIN_HW] for wy in WIN_Y], []) + [Y1]
        for k in range(0, len(ys), 2):
            wq(ys[k], ys[k + 1], WIN_Z[0], VENT_Z[1], M['wall_up'], 4, 2, 1.0)
        for wy in WIN_Y:
            wq(wy - WIN_HW, wy + WIN_HW, WIN_Z[1], VENT_Z[0], M['wall_up'], 4, 2, 1.0)
        wq(Y0, Y1, VENT_Z[1], HC, M['wall_up'], 4, 2, 1.0)
        # chair rail / bumper strip along the wainscot top
        for (ya, yb) in zip(ys[0::2], ys[1::2]): mb.box((min(x, x - s * 0.035), ya, 0.9), (max(x, x - s * 0.035), yb, 0.98), flat('#5d7f86', 0.85))
        for wy in WIN_Y:
            y0, y1 = wy - WIN_HW, wy + WIN_HW; xo = x + s * WALL_T
            for (z0, z1) in (WIN_Z, VENT_Z):                     # reveals (they throw the window edge shadows)
                F(mb, [(x, y0, z0), (xo, y0, z0), (xo, y0, z1), (x, y0, z1)], flat('#ece6d6', 0.9), None, (0, 1, 0))
                F(mb, [(x, y1, z0), (xo, y1, z0), (xo, y1, z1), (x, y1, z1)], flat('#ece6d6', 0.9), None, (0, -1, 0))
                F(mb, [(x, y0, z1), (xo, y0, z1), (xo, y1, z1), (x, y1, z1)], flat('#e2dccc', 0.9), None, (0, 0, -1))
                F(mb, [(x, y0, z0), (xo, y0, z0), (xo, y1, z0), (x, y1, z0)], flat('#ece6d6', 0.9), None, (0, 0, 1))
            F(mb, [(x, y0, WIN_Z[1]), (xo, y0, WIN_Z[1]), (xo, y0, VENT_Z[0]), (x, y0, VENT_Z[0])], flat('#ece6d6', 0.9), None, (0, 1, 0))
            F(mb, [(x, y1, WIN_Z[1]), (xo, y1, WIN_Z[1]), (xo, y1, VENT_Z[0]), (x, y1, VENT_Z[0])], flat('#ece6d6', 0.9), None, (0, -1, 0))
            # vent blocks in the middle of the wall thickness
            xv = x + s * WALL_T * 0.5
            F(mba, [(xv, y0, VENT_Z[0]), (xv, y1, VENT_Z[0]), (xv, y1, VENT_Z[1]), (xv, y0, VENT_Z[1])], M['vent'], [(0, 0), ((y1 - y0) / 1.6, 0), ((y1 - y0) / 1.6, 1), (0, 1)], n)
            # sill (inside ledge) and aluminium frame: outer frame, central mullion, transom (top hopper)
            mb.box((min(x, x - s * 0.14), y0 - 0.04, WIN_Z[0] - 0.05), (max(x, x - s * 0.14), y1 + 0.04, WIN_Z[0] + 0.0), flat('#d9d4c6', 0.9))
            al = flat('#c3c8cc', 0.9); xf0, xf1 = sorted((x + s * 0.08, x + s * 0.13)); t = 0.045
            mb.box((xf0, y0, WIN_Z[0]), (xf1, y0 + t, WIN_Z[1]), al); mb.box((xf0, y1 - t, WIN_Z[0]), (xf1, y1, WIN_Z[1]), al)
            mb.box((xf0, y0, WIN_Z[1] - t), (xf1, y1, WIN_Z[1]), al); mb.box((xf0, y0, WIN_Z[0]), (xf1, y1, WIN_Z[0] + t), al)
            mb.box((xf0, wy - t / 2, WIN_Z[0]), (xf1, wy + t / 2, WIN_Z[1]), al); mb.box((xf0, y0, 2.32), (xf1, y1, 2.32 + t), al)
            # one top hopper tilted open on the sun side
            if s > 0 and wy in (2.6, 9.0):
                hz = 2.32 + t; F(mb, [(xf0, y0 + t, hz), (xf0, y1 - t, hz), (xf0 - 0.18, y1 - t, WIN_Z[1] - t), (xf0 - 0.18, y0 + t, WIN_Z[1] - t)], flat('#dfe9ee', 0.8), None, (-1, 0, 0.3))
    # exterior views (camera-only cards, no shadow)
    ex = MB(); ex.quad((XW + 4.0, Y0, -1.0), (0, Y1 - Y0, 0), (0, 0, 6.0), M['ext_r']); ex.quad((-XW - 4.0, Y1, -1.0), (0, -(Y1 - Y0), 0), (0, 0, 6.0), M['ext_l'])
    eo = ex.obj('hosp_exterior', G['coll']); eo.visible_shadow = False
    # near-end wall: door frame boxes, kick plates; far wall: skirting, clock, ward number
    mb.box((-1.1, Y0, 0), (-1.0, Y0 + 0.06, 2.42), flat('#4f6f86')); mb.box((1.0, Y0, 0), (1.1, Y0 + 0.06, 2.42), flat('#4f6f86')); mb.box((-1.1, Y0, 2.36), (1.1, Y0 + 0.06, 2.46), flat('#4f6f86'))

def blinds(G, s, wy, z_bot, tilt):
    """Venetian blind inside one window: head rail, slats every 4.5 cm down to z_bot (tilted), stacked slats above when raised, ladder cords, wand."""
    mb = G['blinds']; x = s * (XW - 0.04); y0, y1 = wy - WIN_HW + 0.03, wy + WIN_HW - 0.03; zt = WIN_Z[1] - 0.06
    col = flat('#e6eaec', 0.85); mb.box((min(x, x - s * 0.06), y0, zt), (max(x, x - s * 0.06), y1, WIN_Z[1] - 0.005), flat('#d8dcde', 0.85))
    raised = z_bot > WIN_Z[0] + 0.05
    if raised:                                             # stack of pulled-up slats under the head rail
        n_st = int((WIN_Z[1] - z_bot) / 0.045); hst = n_st * 0.006 + 0.04
        mb.box((min(x, x - s * 0.05), y0, zt - hst), (max(x, x - s * 0.05), y1, zt), col); zs = zt - hst
    else: zs = zt
    z = zs - 0.03; tl = math.radians(tilt); d = Vector((-s * math.cos(tl), 0, -math.sin(tl))) * 0.026
    while z > z_bot + 0.02:
        c = Vector((x - s * 0.025, wy, z)); F(mb, [c - d + Vector((0, y0 - wy, 0)), c - d + Vector((0, y1 - wy, 0)), c + d + Vector((0, y1 - wy, 0)), c + d + Vector((0, y0 - wy, 0))], col, None, (0, 0, 1))
        z -= 0.045
    mb.box((min(x, x - s * 0.05), y0, z_bot), (max(x, x - s * 0.05), y1, z_bot + 0.02), flat('#d0d4d6', 0.85))
    cord = flat('#f4f4f0', 0.85)
    for yy in (y0 + 0.2, wy, y1 - 0.2): tube(mb, [(x - s * 0.025, yy, zt), (x - s * 0.025, yy, z_bot)], 0.003, cord, 3)
    tube(mb, [(x - s * 0.07, y1 - 0.08, zt), (x - s * 0.07, y1 - 0.08, zt - 0.8)], 0.005, flat('#dfe3e6'), 4)

# ----------------------------------------------------------------------------- the bed and what stands around it
def bed(G, i, side, cy, state):
    """Metal hospital bed, mattress, sheet, pillow(s), blanket, side rails, castors; returns the frame."""
    f = BF(side, cy); mb = G['beds']; metal = flat('#e6e4dc', 0.85); grey = flat('#8c9298', 0.85); dark = flat('#4c5056', 0.8); blue = flat('#8fb3cf', 0.85)
    # frame + legs + castors
    for a in (0.06, 1.99):
        for b in (-0.45, 0.45): f.cyl(mb, a, b, 0.14, 1.0 if a < 1 else 0.86, 0.022, metal, 10)
        f.box(mb, a - 0.02, a + 0.02, -0.45, 0.45, 0.4, 0.46, metal)
    f.box(mb, 0.03, 0.07, -0.43, 0.43, 0.5, 0.97, blue); f.box(mb, 1.97, 2.01, -0.43, 0.43, 0.5, 0.83, blue)        # head and foot boards
    f.box(mb, 0.03, 0.075, -0.43, 0.43, 0.95, 0.99, metal); f.box(mb, 1.965, 2.015, -0.43, 0.43, 0.81, 0.85, metal)
    for b in (-0.45, 0.45): f.box(mb, 0.06, 1.99, b - 0.02, b + 0.02, 0.4, 0.47, grey)
    f.box(mb, 0.08, 1.97, -0.43, 0.43, 0.44, 0.47, dark)
    for a in (0.16, 1.88):
        for b in (-0.38, 0.38): f.box(mb, a - 0.02, a + 0.02, b - 0.02, b + 0.02, 0.16, 0.42, grey); f.wheel(mb, a, b)
    f.box(mb, 0.16, 1.88, -0.02, 0.02, 0.24, 0.28, grey); f.box(mb, 1.86, 1.9, -0.38, 0.38, 0.2, 0.24, grey)          # cross members, pedal bar
    f.box(mb, 0.9, 1.4, -0.05, 0.05, 0.28, 0.42, flat('#6a7076'))                                                       # actuator box
    # chart clipboard on the footboard (outside)
    rect(mb, f.P(2.025, 0, 0.68), (0, 0.12 * f.s, 0), (0, 0, 0.15), M['chart'], n=f.vec(1, 0, 0))
    # mattress + sheet, pillow(s)
    f.box(mb, 0.08, 1.97, -0.44, 0.44, 0.47, 0.62, M['sheet'])
    f.box(mb, 0.08, 1.97, -0.445, 0.445, 0.47, 0.5, flat('#5f8fbf', 0.85))
    np_ = 2 if state.get('pillows') == 2 else 1
    for k in range(np_):
        blob(mb, f.P(0.36 + k * 0.03, 0.0, 0.69 + k * 0.1), f.vec(0.2, 0, 0), f.vec(0, 0.33, 0), (0, 0, 0.07), M['pillow'], 14, 8, 0.3)
    # blanket
    bm = M['blanket']
    if state.get('blanket') == 'folded':
        f.box(mb, 1.5, 1.93, -0.36, 0.36, 0.62, 0.71, bm, tile=(0.5, 0.5)); f.box(mb, 1.52, 1.91, -0.34, 0.34, 0.71, 0.77, bm, tile=(0.5, 0.5))
    else:
        a0 = state.get('blanket_a', 0.78); zt = 0.665; lump = state.get('lump', 0.0)
        if lump > 0: blob(mb, f.P(1.25, 0.04, 0.63), f.vec(0.55, 0, 0), f.vec(0, 0.22, 0), (0, 0, lump), bm, 12, 6, 0.6)
        F(mb, [f.P(a0, -0.46, zt), f.P(2.0, -0.46, zt), f.P(2.0, 0.46, zt), f.P(a0, 0.46, zt)], bm, [(0, 0), (2.4, 0), (2.4, 1.8), (0, 1.8)], (0, 0, 1))
        for b, sb in ((-0.46, -1), (0.46, 1)):
            pts = [f.P(a0, b, zt), f.P(2.0, b, zt), f.P(2.02, b + sb * 0.05, 0.4), f.P(a0 + 0.04, b + sb * 0.05, 0.42)]
            F(mb, pts, bm, [(0, 0), (2.4, 0), (2.4, 0.5), (0, 0.5)], f.vec(0, sb, 0.2))
        F(mb, [f.P(2.0, -0.46, zt), f.P(2.0, 0.46, zt), f.P(2.05, 0.5, 0.5), f.P(2.05, -0.5, 0.5)], bm, [(0, 0), (1.8, 0), (1.8, 0.3), (0, 0.3)], f.vec(1, 0, 0.3))
        tube(mb, [f.P(a0, -0.47, zt - 0.01), f.P(a0 - 0.02, 0, zt + 0.012), f.P(a0, 0.47, zt - 0.01)], 0.03, M['sheet'], 8)        # turned-down sheet edge
    # side rails (head half): raised (top 0.93) or lowered (top 0.6)
    for b, up in ((-0.5, state.get('rail_minus', True)), (0.5, state.get('rail_plus', True))):
        zt = 0.93 if up else 0.6; zb = zt - 0.3
        for z in (zt, zb + 0.02): f.box(mb, 0.25, 1.15, b - 0.012, b + 0.012, z - 0.02, z, metal)
        for a in (0.35, 0.55, 0.75, 0.95): f.box(mb, a - 0.01, a + 0.01, b - 0.008, b + 0.008, zb, zt, metal)
        f.box(mb, 0.25, 0.29, b - 0.02, b + 0.02, 0.44, zt, grey); f.box(mb, 1.11, 1.15, b - 0.02, b + 0.02, 0.44, zt, grey)
    # nurse call handset on its cord, from the headwall to the pillow
    cd = flat('#e8e8e0', 0.8); tube(mb, smooth([f.P(-0.04, -0.3, 1.45), f.P(0.1, -0.32, 1.0), f.P(0.25, -0.36, 0.72), f.P(0.45, -0.38, 0.66)], 4), 0.006, cd, 4)
    f.box(mb, 0.44, 0.58, -0.4, -0.35, 0.62, 0.66, flat('#d8dcd8')); f.box(mb, 0.5, 0.53, -0.39, -0.36, 0.66, 0.663, M['led_r'])
    return f

def cabinet(G, i, f, items):
    """Bedside locker beside the foot end of the bed (-b side, a 1.40..1.86), front toward the aisle, so the phones line the aisle;
    things on top; the phone on its stand (screen = separate object)."""
    mb = G['props']; f = BF(f.side, f.cy); f.off = CAB_A - 0.3
    f.box(mb, 0.07, 0.53, -1.09, -0.63, 0.06, 0.84, flat('#e9e4d6', 0.85), front=M['cabinet'])
    f.box(mb, 0.05, 0.55, -1.11, -0.61, 0.84, 0.87, flat('#b9c4cc', 0.85))
    f.box(mb, 0.1, 0.5, -1.06, -0.66, 0.0, 0.06, flat('#5a6066'))
    r = random.Random(500 + i); top = 0.87
    if 'jug' in items:
        jx = f.P(0.14, -0.99, top); mb.frustum(tuple(jx), tuple(jx + Vector((0, 0, 0.2))), 0.055, 0.045, flat('#e8f2f8', 0.85), seg=12)
        mb.frustum(tuple(jx + Vector((0, 0, 0.2))), tuple(jx + Vector((0, 0, 0.23))), 0.045, 0.045, flat('#3a8ad0', 0.85), seg=12)
        cx_ = f.P(0.3, -0.72, top); mb.frustum(tuple(cx_), tuple(cx_ + Vector((0, 0, 0.09))), 0.03, 0.036, flat(r.choice(['#e84a3a', '#f0c030', '#4ab0d0']), 0.85), seg=10)
    if 'tissue' in items: f.box(mb, 0.1, 0.24, -0.84, -0.67, top, top + 0.08, flat('#f4a8c0', 0.85)); f.box(mb, 0.15, 0.19, -0.79, -0.72, top + 0.08, top + 0.1, flat('#ffffff'))
    if 'bag' in items: blob(mb, f.P(0.3, -1.0, top + 0.08), f.vec(0.1, 0, 0), f.vec(0, 0.07, 0), (0, 0, 0.09), flat(r.choice(['#f0f0f0', '#e83a3a', '#3a6ad0']), 0.8), 10, 6, 0.7)
    if 'fruit' in items:
        for k in range(4): mb.sphere(tuple(f.P(0.2 + 0.05 * (k % 2), -0.72 - 0.05 * (k // 2), top + 0.035)), 0.035, flat('#f08a20', 0.85), 10, 6)
    if 'bottle' in items:
        bx = f.P(0.47, -0.7, top); mb.frustum(tuple(bx), tuple(bx + Vector((0, 0, 0.2))), 0.03, 0.03, flat('#cfe8f4', 0.85), seg=10); mb.frustum(tuple(bx + Vector((0, 0, 0.2))), tuple(bx + Vector((0, 0, 0.23))), 0.014, 0.014, flat('#2a6ad0'), seg=8)
    # phone on a stand, screen toward the aisle and the camera end
    fd = Vector((0.75 * f.s, -0.66, 0)).normalized() if f.L else Vector((-0.75, -0.66, 0)).normalized()
    pc = f.P(0.4, -0.95, top); side = Vector((0, 0, 1)).cross(fd).normalized(); tl = math.radians(18)
    up = (Vector((0, 0, 1)) * math.cos(tl) - fd * math.sin(tl)).normalized(); nrm = side.cross(up).normalized()
    if nrm.dot(fd) < 0: side = -side; nrm = -nrm
    mb.box(tuple(pc - Vector((0.04, 0.04, 0))), tuple(pc + Vector((0.04, 0.04, 0.025))), flat('#3a3e44'))      # stand
    base = pc + Vector((0, 0, 0.02)); hc = base + up * 0.08; mb.pid += 1
    half_w, half_h, th = 0.037, 0.078, 0.009; body = flat('#1e2228', 0.8)
    corners = [hc + side * sx * half_w + up * sy * half_h for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    back = [p - nrm * th for p in corners]
    F(mb, corners, body, None, nrm); F(mb, back, body, None, -nrm)
    for k in range(4): F(mb, [corners[k], corners[(k + 1) % 4], back[(k + 1) % 4], back[k]], body)
    tube(mb, smooth([base - up * 0.01 + nrm * -0.004, base - fd * 0.06 + Vector((0, 0, -0.01)), f.P(0.1, -0.86, top + 0.005), f.P(0.0, -0.9, top - 0.25), f.P(-0.1, -0.8, 0.3), f.P(-0.3, -0.75, 0.02)], 4), 0.004, flat('#f4f4f0'), 4)
    sc = MB(); sm = screen_mat(f'phone_screen_{i}', TX['phone_screen'], P['screens']); sh = 0.0012
    q = [hc + nrm * sh + side * sx * (half_w - 0.004) + up * sy * (half_h - 0.006) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    F(sc, q, sm, [(0, 0), (1, 0), (1, 1), (0, 1)], nrm); so = sc.obj(f'phone_screen_{i}', G['coll']); so.visible_shadow = False; S.no_bounce(so)
    return dict(phone=tuple(round(v, 4) for v in hc + nrm * sh), phone_normal=tuple(round(v, 4) for v in nrm), cabinet_top=tuple(round(v, 4) for v in f.P(0.3, -0.86, top)),
                screen_object=f'phone_screen_{i}', screen_material=f'phone_screen_{i}')

def headwall(G, i, f, side):
    """Wall above the bed head: gas panel, flowmeter + humidifier, suction jar, reading lamp, bed number plate, gel dispender."""
    mb = G['props']; x = -f.s * XW; nx = f.s; y = f.cy; n = (nx, 0, 0); uu = Vector((0, f.s, 0))
    mb.box((min(x, x + nx * 0.05), y - 0.76, 1.29), (max(x, x + nx * 0.05), y + 0.76, 1.69), flat('#b6bcc0', 0.85))
    rect(mb, (x + nx * 0.052, y, 1.4875), uu * 0.75, (0, 0, 0.1875), M['headwall'], n=n)
    o2 = Vector((x + nx * 0.1, y + f.s * (-0.75 + 0.176), 1.38)); mb.frustum(tuple(o2), tuple(o2 + Vector((0, 0, 0.16))), 0.02, 0.02, flat('#d8f0e0', 0.85), seg=10)
    mb.sphere(tuple(o2 + Vector((0, 0, 0.17))), 0.022, flat('#2aa04a', 0.85), 10, 6)
    mb.frustum(tuple(o2 - Vector((0, 0, 0.2))), tuple(o2 - Vector((0, 0, 0.02))), 0.035, 0.035, flat('#cfe6f0', 0.85), seg=12)
    mb.frustum(tuple(o2 - Vector((0, 0, 0.215))), tuple(o2 - Vector((0, 0, 0.2))), 0.03, 0.03, flat('#f4f4f0'), seg=12)
    tube(mb, smooth([o2 - Vector((0, 0, 0.2)) + Vector((nx * 0.03, 0, 0)), o2 + Vector((nx * 0.25, 0, -0.5)), Vector((x + nx * 0.4, y - f.s * 0.2, 0.72))], 5), 0.005, flat('#d8f4e8', 0.8), 4)
    va = Vector((x + nx * 0.09, y + f.s * (-0.75 + 0.55), 1.0)); mb.frustum(tuple(va), tuple(va + Vector((0, 0, 0.24))), 0.065, 0.065, flat('#e0eef4', 0.85), seg=14)
    mb.frustum(tuple(va + Vector((0, 0, 0.24))), tuple(va + Vector((0, 0, 0.27))), 0.068, 0.068, flat('#3a8ad0', 0.85), seg=14)
    mb.box((min(x, x + nx * 0.06), va.y - 0.07, 0.97), (max(x, x + nx * 0.06), va.y + 0.07, 1.0), flat('#9aa0a6'))
    # gas pipes and cable conduit rising from the panel to the ceiling
    for dy, col in ((-0.62, '#2aa04a'), (-0.5, '#e8e8e2'), (0.66, '#e8e8e2')):
        tube(mb, [(x + nx * 0.03, y + f.s * dy, 1.69), (x + nx * 0.03, y + f.s * dy, HC)], 0.016 if col != '#e8e8e2' else 0.022, flat(col, 0.85), 6)
    # reading lamp on an arm
    la = Vector((x, y + f.s * 0.35, 2.05)); tube(mb, [la, la + Vector((nx * 0.35, 0, 0.0)), la + Vector((nx * 0.45, 0, -0.05))], 0.012, flat('#c8ccd0'), 6)
    mb.box(tuple(la + Vector((nx * 0.38 - 0.08, -0.12, -0.1))), tuple(la + Vector((nx * 0.38 + 0.08, 0.12, -0.04))), flat('#e8eaec', 0.85))
    # bed plate (signs atlas row 3, cell i)
    u0, u1 = (i * 170 + 2) / 1024, (i * 170 + 168) / 1024
    rect(mb, (x + nx * 0.015, y, 2.02), uu * 0.085, (0, 0, 0.128), M['signs'], (u0, 0.004, u1, 0.248), n)
    # hand-gel dispenser
    gy = y + f.s * 0.95; mb.box((min(x, x + nx * 0.1), gy - 0.06, 1.15), (max(x, x + nx * 0.1), gy + 0.06, 1.38), flat('#f4f6f8', 0.85))
    mb.box((min(x + nx * 0.1, x + nx * 0.102), gy - 0.03, 1.2), (max(x + nx * 0.1, x + nx * 0.102), gy + 0.03, 1.28), flat('#2a8ad0', 0.85))

def iv_stand(G, p, f=None, bags=1, pump=False, to=None):
    mb = G['props']; x, y = p[0], p[1]; grey = flat('#b8bec4', 0.85); blk = flat('#2a2a2e')
    for k in range(5):
        a = k * 2 * math.pi / 5 + 0.3; e = Vector((x + 0.28 * math.cos(a), y + 0.28 * math.sin(a), 0.08))
        tube(mb, [Vector((x, y, 0.1)), e], 0.012, grey, 5); mb.frustum(tuple(e + Vector((0, -0.015, -0.04))), tuple(e + Vector((0, 0.015, -0.04))), 0.035, 0.035, blk, seg=10)
    mb.frustum((x, y, 0.08), (x, y, 2.05), 0.013, 0.013, grey, seg=8); mb.frustum((x, y, 0.06), (x, y, 0.14), 0.04, 0.03, grey, seg=10)
    tube(mb, [(x - 0.16, y, 2.0), (x - 0.14, y, 2.05), (x + 0.14, y, 2.05), (x + 0.16, y, 2.0)], 0.007, grey, 4)
    tube(mb, [(x, y - 0.16, 2.0), (x, y - 0.14, 2.05), (x, y + 0.14, 2.05), (x, y + 0.16, 2.0)], 0.007, grey, 4)
    tips = []
    for k in range(bags):
        bx, by = (x - 0.15, y) if k == 0 else (x, y + 0.15); top = Vector((bx, by, 1.97))
        blob(mb, top + Vector((0, 0, -0.14)), (0.065, 0, 0), (0, 0.022, 0), (0, 0, 0.12), M['ivbag'], 10, 6, 0.4)
        rect(mb, top + Vector((0, -0.026, -0.14)), (0.06, 0, 0), (0, 0, 0.11), M['ivbag'], n=(0, -1, 0))
        mb.frustum(tuple(top + Vector((0, 0, -0.3))), tuple(top + Vector((0, 0, -0.26))), 0.006, 0.006, flat('#f4f4f4'), seg=6)
        mb.frustum(tuple(top + Vector((0, 0, -0.38))), tuple(top + Vector((0, 0, -0.3))), 0.012, 0.012, flat('#e0eef6', 0.8), seg=8); tips.append(top + Vector((0, 0, -0.38)))
    if pump:
        mb.box((x - 0.07, y - 0.12, 1.15), (x + 0.07, y - 0.01, 1.33), flat('#e8eaec', 0.85)); mb.box((x - 0.05, y - 0.121, 1.25), (x + 0.05, y - 0.12, 1.3), M['led_g'])
    if to is not None:
        for t in tips: tube(mb, smooth([t, Vector((t.x, t.y, 1.2)), (Vector(to) + Vector((t.x, t.y, 1.2))) / 2 + Vector((0, 0, -0.25)), Vector(to)], 6), 0.003, flat('#eaf4f8', 0.8), 4)

def monitor(G, f):
    """Heart monitor on a wheeled stand beside the hero bed (nurse side, head end). Body + separate screen plane `monitor_screen`."""
    mb = G['props']; base = f.P(0.32, 0.98, 0); x, y = base.x, base.y; grey = flat('#c4c8cc', 0.85); blk = flat('#2a2a2e')
    for k in range(5):
        a = k * 2 * math.pi / 5; e = Vector((x + 0.26 * math.cos(a), y + 0.26 * math.sin(a), 0.07))
        tube(mb, [Vector((x, y, 0.09)), e], 0.014, grey, 5); mb.frustum(tuple(e + Vector((0, -0.015, -0.035))), tuple(e + Vector((0, 0.015, -0.035))), 0.035, 0.035, blk, seg=10)
    mb.frustum((x, y, 0.07), (x, y, 1.1), 0.018, 0.018, grey, seg=10); mb.box((x - 0.12, y - 0.08, 0.72), (x + 0.12, y + 0.08, 0.76), grey)       # basket shelf
    mb.box((x - 0.1, y - 0.06, 0.76), (x + 0.04, y + 0.05, 0.8), flat('#3a8ad0'))                                                             # cable bag
    fd = Vector((0.62 * f.s, -0.78, 0)).normalized(); yaw = math.atan2(fd.x, -fd.y); tilt = math.radians(8)
    ctr = Vector((x, y, 1.32)) + fd * 0.02
    rot = Matrix.Rotation(yaw, 4, 'Z') @ Matrix.Rotation(-tilt, 4, 'X')
    body = MB(); body.box((-0.18, -0.08, -0.15), (0.18, 0.08, 0.15), flat('#d9dde0', 0.85), mats={'front': M['monitor_body']})
    body.box((-0.14, 0.08, -0.11), (0.14, 0.12, 0.09), flat('#c0c6ca', 0.85)); body.box((-0.03, 0.1, -0.24), (0.03, 0.16, -0.12), grey)
    body.box((-0.17, -0.07, 0.15), (0.17, 0.05, 0.175), flat('#c8ccd0', 0.85))                                                             # handle
    body.box((0.12, -0.081, 0.12), (0.15, -0.08, 0.135), M['led_g'])
    bo = body.obj('monitor_body', G['coll']); bo.matrix_world = Matrix.Translation(ctr) @ rot; S.no_bounce(bo)
    sc = MB(); sm = screen_mat('monitor_screen', TX['monitor_screen'], P['monitor'])
    sc.quad((-0.156, -0.0815, -0.092), (0.281, 0, 0), (0, 0, 0.215), sm); so = sc.obj('monitor_screen', G['coll']); so.matrix_world = Matrix.Translation(ctr) @ rot
    so.visible_shadow = False; S.no_bounce(so)
    mw = Matrix.Translation(ctr) @ rot; cen = mw @ Vector((-0.0155, -0.0815, 0.0155)); nrm = (rot.to_3x3() @ Vector((0, -1, 0))).normalized()
    # lead cables from the monitor down to the patient's chest under the blanket
    for k, col in enumerate(('#f4f4f0', '#d8302a', '#2a8a4a')):
        st = mw @ Vector((0.05 - k * 0.04, 0.1, -0.16)); tube(G['props'], smooth([st, st + Vector((0, 0, -0.35)), f.P(0.55, 0.3 - k * 0.05, 0.75), f.P(0.78, 0.1 - k * 0.06, 0.67)], 5), 0.004, flat(col, 0.8), 4)
    return dict(center=tuple(round(v, 4) for v in cen), normal=tuple(round(v, 4) for v in nrm), size=(0.281, 0.215), stand=(round(x, 3), round(y, 3), 0.0),
                object='monitor_screen', material='monitor_screen')

# ----------------------------------------------------------------------------- curtains on ceiling rails
def curtain(G, p0, p1, mat, depth=0.05, pleat=0.11, z0=0.32, zn=2.25, z1=2.7):
    """Pleated curtain hanging from a rail between p0 and p1 (xy): print below zn, mesh band above, hooks on the rail."""
    mb, mba = G['curtains'], G['alpha']; p0, p1 = Vector((p0[0], p0[1], 0)), Vector((p1[0], p1[1], 0)); d = p1 - p0; L = d.length
    if L < 0.05: return
    t = d.normalized(); nrm = Vector((-t.y, t.x, 0)); n = max(3, int(L / pleat)); pts = []; acc = [0.0]
    for k in range(n + 1):
        off = (depth / 2) * (1 if k % 2 else -1) * (0 if k in (0, n) else 1)
        pts.append(p0 + t * (L * k / n) + nrm * off)
    for k in range(n): acc.append(acc[-1] + (pts[k + 1] - pts[k]).length)
    hem = lambda k: z0 + 0.012 * math.sin(k * 1.7)
    for k in range(n):
        a, b = pts[k], pts[k + 1]; ua, ub = acc[k] / 0.8, acc[k + 1] / 0.8
        mb.pid += 1; mb.face([Vector((a.x, a.y, hem(k))), Vector((b.x, b.y, hem(k + 1))), Vector((b.x, b.y, zn)), Vector((a.x, a.y, zn))], mat, [(ua, z0 / 0.8), (ub, z0 / 0.8), (ub, zn / 0.8), (ua, zn / 0.8)])
        mba.pid += 1; mba.face([Vector((a.x, a.y, zn)), Vector((b.x, b.y, zn)), Vector((b.x, b.y, z1)), Vector((a.x, a.y, z1))], M['net'], [(ua * 0.8 / 0.8, 0), (ub, 0), (ub, 1), (ua, 1)])

def rails(G):
    """U-shaped ceiling tracks around each bed bay (shared side tracks between beds) and the curtains, partly drawn."""
    mb = G['curtains']; al = flat('#d0d4d8', 0.85); zr = 2.74
    seg = []
    for s in (-1, 1):
        xa, xf = s * (XW - 0.02), s * (BED_HEAD - BED_LEN - 0.25)     # wall end, foot line
        lines = [BED_Y[0] - 1.6] + [(BED_Y[k] + BED_Y[k + 1]) / 2 for k in range(2)] + [BED_Y[-1] + 1.6]
        for yl in lines: seg.append(((xa, yl), (xf, yl)))
        for k in range(3): seg.append(((xf, lines[k]), (xf, lines[k + 1])))
    for (a, b) in seg:
        tube(mb, [(a[0], a[1], zr), (b[0], b[1], zr)], 0.016, al, 6)
        L = (Vector(b) - Vector(a)).length; n = max(1, int(L / 1.2))
        for k in range(n + 1):
            p = Vector(a).lerp(Vector(b), k / n); mb.frustum((p.x, p.y, zr), (p.x, p.y, HC), 0.007, 0.007, al, seg=6)
    return seg

def curtains(G):
    g, b = M['curtain_g'], M['curtain_b']
    for s in (-1, 1):
        xa, xf = s * (XW - 0.04), s * (BED_HEAD - BED_LEN - 0.25); lines = [BED_Y[0] - 1.6] + [(BED_Y[k] + BED_Y[k + 1]) / 2 for k in range(2)] + [BED_Y[-1] + 1.6]
        mat = g if s < 0 else b
        for k, yl in enumerate(lines):                                         # side curtains: open ones bunched at the wall end (over the mullion), some drawn
            drawn = {(-1, 2): 1.35, (1, 0): 1.0, (1, 3): 2.2, (1, 2): 2.2}.get((s, k), 0.0)
            if (s, k) == (-1, 2): curtain(G, (-2.05, yl), (xa - s * 0.02, yl), mat, 0.06, 0.1)          # behind the nurse mark, wall side
            elif drawn > 0: curtain(G, (xf, yl), (xf + (xa - xf) * drawn / abs(xa - xf), yl), mat, 0.06, 0.1)
            if drawn < 1.9 and (s, k) != (-1, 2): curtain(G, (xa - s * 0.02, yl), (xa - s * 0.38, yl), mat, 0.15, 0.035)
        for k in range(3):                                                     # foot curtains: R2 fully closed, L2 partly drawn; the rest went round to the wall
            y0, y1 = lines[k], lines[k + 1]
            if (s, k) == (1, 2): curtain(G, (xf, y0), (xf, y1), mat, 0.06, 0.1)
            elif (s, k) == (-1, 2): curtain(G, (xf, y1), (xf, y1 - 1.1), mat, 0.07, 0.1)

# ----------------------------------------------------------------------------- ceiling: tubes, fans; signs, clock, posters
def ceiling_stuff(G):
    mb = G['props']; wh = flat('#f2f2ee', 0.85)
    tubes = MB()
    def batten(c, along):
        x, y = c; u = Vector((0.62, 0, 0)) if along == 'x' else Vector((0, 0.62, 0)); v = Vector((0.07, 0, 0)) if along == 'y' else Vector((0, 0.07, 0))
        p = Vector((x, y, HC)); mb.box(tuple(p - u - v - Vector((0, 0, 0.06))), tuple(p + u + v), wh)
        for o in (-0.035, 0.035):
            q = p + (v.normalized() * o) - Vector((0, 0, 0.075)); tubes.frustum(tuple(q - u * 0.96), tuple(q + u * 0.96), 0.014, 0.014, M['tube'], seg=8)
    for fy in tex_hosp.FIX_Y: batten((0.0, fy), 'y')
    for s in (-1, 1):
        for by in BED_Y: batten((s * 2.45, by), 'x')
        batten((s * 2.45, 11.2), 'x')
    batten((0.5, 13.6), 'x')
    to = tubes.obj('hosp_tubes', G['coll']); to.visible_shadow = False; S.no_bounce(to)
    # ceiling hardware: smoke detectors, sprinkler heads, AC cassettes, return-air grilles, speakers, hanging exit signs
    grille = flat('#dcdcd6', 0.85); slot = flat('#6a6e72', 0.8)
    for (x, y) in ((-1.2, 1.8), (1.2, 7.0), (-1.2, 9.6), (1.2, 12.6)):
        mb.box((x - 0.31, y - 0.31, HC - 0.03), (x + 0.31, y + 0.31, HC), grille)
        for k in range(4):
            for (dx, dy, w, h) in ((0, -0.24, 0.42, 0.035), (0, 0.24, 0.42, 0.035), (-0.24, 0, 0.035, 0.42), (0.24, 0, 0.035, 0.42)):
                pass
        for (dx, dy, w, h) in ((0, -0.24, 0.42, 0.035), (0, 0.24, 0.42, 0.035), (-0.24, 0, 0.035, 0.42), (0.24, 0, 0.035, 0.42)):
            F(mb, [(x + dx - w / 2, y + dy - h / 2, HC - 0.031), (x + dx + w / 2, y + dy - h / 2, HC - 0.031), (x + dx + w / 2, y + dy + h / 2, HC - 0.031), (x + dx - w / 2, y + dy + h / 2, HC - 0.031)], slot, None, (0, 0, -1))
        F(mb, [(x - 0.15, y - 0.15, HC - 0.032), (x + 0.15, y - 0.15, HC - 0.032), (x + 0.15, y + 0.15, HC - 0.032), (x - 0.15, y + 0.15, HC - 0.032)], flat('#c8c8c2', 0.85), None, (0, 0, -1))
    for (x, y) in ((1.2, 1.8), (-1.2, 7.0), (1.2, 4.4), (-1.2, 12.0)):
        mb.box((x - 0.3, y - 0.3, HC - 0.012), (x + 0.3, y + 0.3, HC), flat('#e4e2da', 0.85))
        for k in range(9): F(mb, [(x - 0.27, y - 0.27 + k * 0.065, HC - 0.013), (x + 0.27, y - 0.27 + k * 0.065, HC - 0.013), (x + 0.27, y - 0.25 + k * 0.065, HC - 0.013), (x - 0.27, y - 0.25 + k * 0.065, HC - 0.013)], slot, None, (0, 0, -1))
    for k in range(14):
        x, y = (-1.8 + (k % 4) * 1.2, -1.0 + k * 1.15); mb.frustum((x, y, HC), (x, y, HC - 0.04), 0.06, 0.055, flat('#f4f4f0', 0.85), seg=12); mb.box((x - 0.01, y - 0.01, HC - 0.05), (x + 0.01, y + 0.01, HC - 0.04), M['led_r'])
        x2 = 1.8 - (k % 3) * 1.8; mb.frustum((x2, y + 0.5, HC), (x2, y + 0.5, HC - 0.06), 0.012, 0.012, flat('#d8b040'), seg=6); mb.frustum((x2, y + 0.5, HC - 0.06), (x2, y + 0.5, HC - 0.07), 0.03, 0.03, flat('#d8d8d0'), seg=8)
    for (x, y) in ((0.0, 1.6), (0.0, 7.2)): mb.frustum((x, y, HC), (x, y, HC - 0.03), 0.11, 0.1, flat('#f0f0ea', 0.85), seg=16); mb.frustum((x, y, HC - 0.03), (x, y, HC - 0.031), 0.08, 0.08, slot, seg=16)
    for (x, y) in ((-2.6, 11.4), (2.9, 11.4)):
        mb.box((x - 0.18, y - 0.02, 2.62), (x + 0.18, y + 0.02, 2.78), flat('#f4f4f0', 0.85)); mb.box((x - 0.16, y - 0.021, 2.64), (x + 0.16, y - 0.02, 2.76), emit('exit', '#30d070', 1.3))
        tube(mb, [(x, y, 2.78), (x, y, HC)], 0.006, flat('#c8ccd0'), 4)
    # ceiling fans
    for (fx, fy) in ((0.0, 4.4), (0.0, 10.0)):
        mb.frustum((fx, fy, HC), (fx, fy, 2.95), 0.012, 0.012, wh, seg=8); mb.frustum((fx, fy, HC - 0.02), (fx, fy, HC), 0.06, 0.06, wh, seg=12)
        mb.frustum((fx, fy, 2.98), (fx, fy, 2.86), 0.11, 0.09, flat('#e8e4dc', 0.85), seg=16); mb.frustum((fx, fy, 2.86), (fx, fy, 2.83), 0.06, 0.04, flat('#c8c4bc'), seg=12)
        for k in range(3):
            a = k * 2 * math.pi / 3 + (0.4 if fy > 5 else 1.1); d = Vector((math.cos(a), math.sin(a), 0)); e = Vector((-d.y, d.x, 0))
            c = Vector((fx, fy, 2.9)) + d * 0.42
            F(mb, [c - d * 0.3 - e * 0.05, c + d * 0.3 - e * 0.06, c + d * 0.3 + e * 0.06 + Vector((0, 0, 0.015)), c - d * 0.3 + e * 0.05 + Vector((0, 0, 0.012))], flat('#ece8de', 0.85), None, (0, 0, 1))
            F(mb, [c - d * 0.3 - e * 0.05 - Vector((0, 0, 0.005)), c + d * 0.3 - e * 0.06 - Vector((0, 0, 0.005)), c + d * 0.3 + e * 0.06 + Vector((0, 0, 0.01)), c - d * 0.3 + e * 0.05 + Vector((0, 0, 0.007))], flat('#ece8de', 0.85), None, (0, 0, -1))
    # hanging ward sign (atlas row 0), clock on the back wall, no-phone signs above the hero bed and on the right wall, posters
    sy = 11.6; mb.box((-0.45, sy - 0.03, 2.5), (1.35, sy + 0.03, 2.98), flat('#1f7a52', 0.85)); rect(mb, (0.45, sy - 0.031, 2.74), (0.88, 0, 0), (0, 0, 0.22), M['signs'], (0, 0.75, 1, 1.0), (0, -1, 0))
    for xx in (-0.3, 1.2): tube(mb, [(xx, sy, 2.98), (xx, sy, HC)], 0.004, flat('#9aa0a6'), 4)
    cx, cz = -0.2, 2.85; mb.frustum((cx, Y1, cz), (cx, Y1 - 0.05, cz), 0.19, 0.19, flat('#2a2a2e'), seg=32)
    F(mb, [(cx - 0.18, Y1 - 0.051, cz - 0.18), (cx + 0.18, Y1 - 0.051, cz - 0.18), (cx + 0.18, Y1 - 0.051, cz + 0.18), (cx - 0.18, Y1 - 0.051, cz + 0.18)], M['clock'], None, (0, -1, 0))
    for (s, yc, z) in ((-1, BED_Y[HERO], 2.42), (1, BED_Y[0], 2.42)):           # ห้ามใช้โทรศัพท์ (atlas row 1)
        x = s * (XW - 0.01); u = Vector((0, -s * 1.0, 0)) * 0.62
        mb.box((min(x, x - s * 0.015), yc - 0.63, z - 0.165), (max(x, x - s * 0.015), yc + 0.63, z + 0.165), flat('#d8302a', 0.85))
        rect(mb, (x - s * 0.017, yc, z), u, (0, 0, 0.155), M['signs'], (0, 0.5, 1, 0.75), (-s, 0, 0))
    for (s, yc, pi) in ((1, BED_Y[1], 0), (1, BED_Y[2], 1), (-1, BED_Y[0], 3), (-1, BED_Y[2], 2)):
        x = s * (XW - 0.012); u = Vector((0, -s * 1.0, 0)) * 0.27; col, row = pi % 2, pi // 2
        rect(mb, (x, yc, 2.4), u, (0, 0, 0.27), M['posters'], (col * 0.5, 1 - (row + 1) * 0.5, col * 0.5 + 0.5, 1 - row * 0.5), (-s, 0, 0))
    # wall-mounted TV bracket (old CRT-style box) above the far right bed, and a crucifix-free Buddha shelf? keep: a small shelf with a radio
    tvx = XW - 0.35; mb.box((tvx - 0.25, 9.8, 2.3), (tvx + 0.15, 10.3, 2.65), flat('#2a2c30')); mb.box((tvx - 0.252, 9.83, 2.33), (tvx - 0.25, 10.27, 2.6), flat('#1a2a3a', 0.6))
    mb.box((tvx + 0.1, 9.85, 2.25), (XW, 10.25, 2.3), flat('#9aa0a6'))

# ----------------------------------------------------------------------------- far end: nurse station; misc props
def station(G, r):
    mb = G['props']; x0, x1, y0, y1 = -1.6, 2.4, 12.1, 12.5
    mb.box((x0, y0, 0), (x1, y1, 1.08), flat('#d8cbb0', 0.85), mats={'front': M['station_front']})
    mb.box((x0 - 0.05, y0 - 0.08, 1.08), (x1 + 0.05, y1 + 0.02, 1.12), flat('#f0ece2', 0.85))
    mb.box((x0, y1, 0.72), (x1, 13.2, 0.76), flat('#e0d4bc', 0.85)); mb.box((x0, 13.15, 0), (x1, 13.2, 0.72), flat('#c8bca4', 0.85))
    mb.box((x0 - 0.05, y0, 0), (x0, 13.2, 1.12), flat('#3d7f9c', 0.85)); mb.box((x1, y0, 0), (x1 + 0.05, 13.2, 1.12), flat('#3d7f9c', 0.85))
    top = 1.12
    # files: stacks of folders, chart rack with coloured patient charts, desk phone, PC monitor (back to us), pen cup, bell, kidney dish
    for k, (xx, n) in enumerate(((-1.35, 6), (-0.95, 4), (1.95, 5))):
        z = top
        for j in range(n):
            h = r.uniform(0.012, 0.03); c = r.choice(['#2a5ab0', '#f0c030', '#d8302a', '#2a9a5a', '#f4f4f0', '#f08a30', '#8ab8e0'])
            dx, dy = r.uniform(-0.02, 0.02), r.uniform(-0.02, 0.02); mb.box((xx - 0.16 + dx, 12.12 + dy, z), (xx + 0.16 + dx, 12.42 + dy, z + h), flat(c, 0.85)); z += h
    rk0 = -0.55
    mb.box((rk0, 12.2, top), (rk0 + 0.6, 12.48, top + 0.03), flat('#a8aeb4'))
    for j in range(10):
        xx = rk0 + 0.03 + j * 0.057; c = r.choice(['#2a5ab0', '#d8302a', '#2a9a5a', '#f0c030', '#8a3ab0'])
        F(mb, [(xx, 12.2, top + 0.03), (xx, 12.46, top + 0.03), (xx + 0.012, 12.5, top + 0.33), (xx + 0.012, 12.24, top + 0.33)], flat(c, 0.85), None, (1, 0, 0))
        F(mb, [(xx + 0.004, 12.2, top + 0.03), (xx + 0.004, 12.46, top + 0.03), (xx + 0.016, 12.5, top + 0.33), (xx + 0.016, 12.24, top + 0.33)], flat(c, 0.85), None, (-1, 0, 0))
    mb.box((0.35, 12.2, top), (0.6, 12.42, top + 0.06), flat('#e8e6de', 0.85)); mb.box((0.36, 12.21, top + 0.06), (0.59, 12.29, top + 0.1), flat('#e8e6de', 0.85))   # desk phone
    tube(mb, smooth([(0.37, 12.25, top + 0.06), (0.3, 12.2, top - 0.05), (0.25, 12.3, top + 0.01), (0.4, 12.4, top + 0.05)], 5), 0.005, flat('#e8e6de'), 4)
    mb.box((0.44, 12.2, top + 0.055), (0.56, 12.3, top + 0.062), flat('#3a3e44'))
    mb.box((0.8, 12.55, 0.76), (1.3, 12.62, 1.12), flat('#2a2c30')); mb.box((1.0, 12.62, 0.76), (1.1, 12.7, 0.9), flat('#2a2c30'))                      # PC monitor (behind counter)
    mb.frustum((1.55, 12.3, top), (1.55, 12.3, top + 0.1), 0.035, 0.035, flat('#3a8ad0', 0.85), seg=10)
    for k in range(5): tube(mb, [(1.55 + 0.01 * (k - 2), 12.3, top + 0.05), (1.55 + 0.02 * (k - 2), 12.3 + 0.01 * k, top + 0.17)], 0.004, flat(['#d8302a', '#2a5ab0', '#1a1a1a', '#2a9a5a', '#f0c030'][k]), 4)
    mb.frustum((1.75, 12.25, top), (1.75, 12.25, top + 0.03), 0.04, 0.03, flat('#c8ccd0'), seg=12); mb.sphere((1.75, 12.25, top + 0.035), 0.012, flat('#9aa0a6'), 8, 4)
    # office chair behind, medicine trolley, shelving with binders on the right wall, filing cabinet
    cx, cy = 0.0, 13.6; mb.box((cx - 0.23, cy - 0.23, 0.45), (cx + 0.23, cy + 0.23, 0.52), flat('#2a3a5a')); mb.box((cx - 0.21, cy + 0.2, 0.52), (cx + 0.21, cy + 0.26, 0.95), flat('#2a3a5a'))
    mb.frustum((cx, cy, 0.1), (cx, cy, 0.45), 0.025, 0.025, flat('#555a60'), seg=8)
    for k in range(5): a = k * 1.2566; tube(mb, [(cx, cy, 0.1), (cx + 0.28 * math.cos(a), cy + 0.28 * math.sin(a), 0.05)], 0.015, flat('#2a2a2e'), 4)
    shx = XW - 0.38
    for k in range(5): mb.box((shx, 12.8, 0.15 + k * 0.42), (XW, 14.6, 0.17 + k * 0.42), flat('#c8ccd0', 0.85))
    for k in range(4):
        F(mb, [(shx + 0.02, 12.82, 0.17 + k * 0.42), (shx + 0.02, 14.58, 0.17 + k * 0.42), (shx + 0.02, 14.58, 0.48 + k * 0.42), (shx + 0.02, 12.82, 0.48 + k * 0.42)], M['binders'],
          [(k * 0.25, 0), (k * 0.25 + 1.6, 0), (k * 0.25 + 1.6, 1), (k * 0.25, 1)], (-1, 0, 0))
    for yy in (12.8, 14.6): mb.box((shx, yy - 0.02, 0), (XW, yy, 1.9), flat('#a8aeb4'))
    mb.box((-XW, 12.9, 0), (-XW + 0.5, 13.6, 1.3), flat('#d8dce0', 0.85)); mb.box((-XW + 0.5, 13.0, 0.2), (-XW + 0.505, 13.5, 1.25), flat('#9aa0a6'))     # filing cabinet
    for k in range(4): mb.box((-XW + 0.5, 13.15, 0.3 + k * 0.28), (-XW + 0.52, 13.35, 0.33 + k * 0.28), flat('#7a8086'))
    # potted plant beside the counter
    px, py = -2.25, 12.2; mb.frustum((px, py, 0), (px, py, 0.45), 0.17, 0.23, flat('#b8603e', 0.85), seg=16); mb.frustum((px, py, 0.43), (px, py, 0.46), 0.22, 0.22, flat('#3a2a1e'), seg=16)
    for k in range(3):
        a = k * math.pi / 3 + 0.2; u = Vector((math.cos(a), math.sin(a), 0)) * 0.42
        rect(G['alpha'], (px, py, 0.46 + 0.6), u, (0, 0, 0.6), M['leaves'])
    # rubbish bins
    for (bx, by, c, lid) in ((2.6, 12.3, '#f0c428', '#e0b418'), (2.95, 12.3, '#2a2a2e', '#3a3a3e'), (-3.15, 11.6, '#f0c428', '#e0b418')):
        mb.frustum((bx, by, 0), (bx, by, 0.55), 0.14, 0.17, flat(c, 0.85), seg=14); mb.frustum((bx, by, 0.55), (bx, by, 0.6), 0.18, 0.16, flat(lid, 0.85), seg=14)
    return dict(counter_top=(0.4, 12.3, 1.12), staff_mark=(0.4, 13.3, 0.0), front_mark=(0.4, 11.65, 0.0), sign=(0.45, sy_ := 11.6, 2.74))

def wheelchair(G, loc, yaw):
    w = MB(); chrome = flat('#c8ccd0', 0.85); blk = flat('#1e1e22', 0.8); seat = M['wc_seat']
    for s in (-1, 1):
        y = s * 0.3
        tube(w, ring((0.05, y, 0.3), 0.3, 28, 'y'), 0.016, blk, 6); tube(w, ring((0.05, y + s * 0.03, 0.3), 0.27, 28, 'y'), 0.006, chrome, 4)
        for k in range(12): a = k * math.pi / 6; tube(w, [(0.05, y, 0.3), (0.05 + 0.27 * math.cos(a), y, 0.3 + 0.27 * math.sin(a))], 0.002, chrome, 3)
        w.frustum((0.05, y - 0.03, 0.3), (0.05, y + 0.03, 0.3), 0.03, 0.03, flat('#5a5e64'), seg=10)
        tube(w, [(-0.35, y, 0.1), (-0.35, y, 0.5), (0.1, y, 0.5), (0.12, y, 0.95), (0.25, y, 1.0)], 0.012, chrome, 6)        # frame + push handle
        tube(w, [(-0.35, y * 0.95, 0.5), (-0.45, y * 0.9, 0.2), (-0.5, y * 0.9, 0.12)], 0.01, chrome, 5)
        w.box((-0.52, y * 0.9 - 0.06, 0.1), (-0.38, y * 0.9 + 0.06, 0.115), blk)                                             # foot plate
        w.frustum((-0.36, y - 0.012, 0.06), (-0.36, y + 0.012, 0.06), 0.06, 0.06, blk, seg=12)                                  # front castor
        w.box((-0.3, y - 0.02, 0.68), (0.1, y + 0.02, 0.71), blk); tube(w, [(-0.25, y, 0.5), (-0.25, y, 0.68)], 0.008, chrome, 4)
        w.box((0.24, y - 0.02, 0.96), (0.34, y + 0.02, 1.02), blk)
    w.box((-0.32, -0.29, 0.48), (0.08, 0.29, 0.52), seat); F(w, [(0.08, -0.29, 0.52), (0.08, 0.29, 0.52), (0.13, 0.29, 0.92), (0.13, -0.29, 0.92)], seat, None, (-1, 0, 0.1))
    ob = w.obj('wheelchair', G['coll']); ob.location = loc; ob.rotation_euler = (0, 0, yaw); S.no_bounce(ob)

def misc(G, r):
    mb = G['props']
    # crash cart (red) with defibrillator, oxygen cylinder on a trolley
    cx, cy = -3.05, 10.4; mb.box((cx - 0.25, cy - 0.32, 0.1), (cx + 0.25, cy + 0.32, 1.0), flat('#c8302a', 0.85), mats={'right': M['cart']})
    mb.box((cx - 0.27, cy - 0.34, 1.0), (cx + 0.27, cy + 0.34, 1.04), flat('#e8e8e8', 0.85)); mb.box((cx - 0.18, cy - 0.2, 1.04), (cx + 0.15, cy + 0.15, 1.22), flat('#f0c030', 0.85))
    mb.box((cx + 0.15, cy - 0.12, 1.08), (cx + 0.151, cy + 0.08, 1.2), flat('#1a1a1a'))
    for dx in (-0.2, 0.2):
        for dy in (-0.27, 0.27): mb.frustum((cx + dx, cy + dy - 0.015, 0.05), (cx + dx, cy + dy + 0.015, 0.05), 0.05, 0.05, flat('#26262a'), seg=10)
    ox, oy = -2.55, 11.0; mb.frustum((ox, oy, 0.12), (ox, oy, 1.15), 0.09, 0.09, flat('#2a8a4a', 0.85), seg=14); mb.sphere((ox, oy, 1.15), 0.09, flat('#2a8a4a', 0.85), 14, 7)
    mb.frustum((ox, oy, 1.22), (ox, oy, 1.32), 0.02, 0.02, flat('#c8ccd0'), seg=8); mb.frustum((ox + 0.0, oy - 0.03, 1.3), (ox, oy - 0.07, 1.3), 0.04, 0.04, flat('#f4f4f0'), seg=12)
    mb.box((ox - 0.15, oy - 0.15, 0.05), (ox + 0.15, oy + 0.15, 0.12), flat('#4a5056'))
    # wet floor sign + bucket under the leak, mop
    wx, wy = 1.0, 9.75; sgn = M['signs']
    for s in (-1, 1):
        F(mb, [(wx - 0.16, wy + s * 0.18, 0.0), (wx + 0.16, wy + s * 0.18, 0.0), (wx + 0.16, wy + s * 0.02, 0.62), (wx - 0.16, wy + s * 0.02, 0.62)], flat('#ffd21e', 0.85), None, (0, s, 0.3))
    rect(mb, (wx, wy - 0.105, 0.33), (0.15, 0, 0), (0, -0.07, 0.25), sgn, (0.04, 0.5, 0.96, 0.75), (0, -1, 0.3))
    bx, by = 1.45, 9.95; mb.frustum((bx, by, 0), (bx, by, 0.3), 0.13, 0.16, flat('#2a6ad0', 0.85), seg=14); mb.frustum((bx, by, 0.24), (bx, by, 0.245), 0.15, 0.15, flat('#9ab4d4', 0.85), seg=14)
    tube(mb, [(bx - 0.16, by, 0.3), (bx, by, 0.42), (bx + 0.16, by, 0.3)], 0.005, flat('#c8ccd0'), 4)
    tube(mb, [(1.75, 10.15, 0.05), (1.95, 10.35, 1.45)], 0.014, flat('#c8a060'), 6); blob(mb, (1.74, 10.14, 0.06), (0.1, 0, 0), (0, 0.1, 0), (0, 0, 0.06), flat('#e8e4d8', 0.8), 10, 5, 0.8)
    # slippers by the beds, over-bed tables
    for (s, by) in ((-1, BED_Y[0]), (-1, BED_Y[1]), (1, BED_Y[1]), (1, BED_Y[2])):
        x = s * (BED_HEAD - 0.8); y = by - s * 0.62
        for d in (-0.06, 0.06): mb.box((x - 0.12, y + d - 0.04, 0), (x + 0.12, y + d + 0.04, 0.025), flat(r.choice(['#2a5ab0', '#3a3a3a', '#c8302a']), 0.85))
    for (s, by) in ((-1, BED_Y[0]), (1, BED_Y[1]), (-1, BED_Y[2])):
        f = BF('L' if s < 0 else 'R', by); mb2 = mb; grey = flat('#c8ccd0', 0.85)
        f.box(mb2, 1.2, 1.5, 0.55, 0.62, 0.0, 0.04, grey); f.cyl(mb2, 1.35, 0.6, 0.04, 0.88, 0.018, grey)
        f.box(mb2, 1.05, 1.65, 0.1, 0.62, 0.88, 0.91, flat('#e8dcc4', 0.85)); f.box(mb2, 1.2, 1.4, 0.25, 0.4, 0.91, 0.93, flat('#7aa8d8', 0.85))
        b0 = f.P(1.32, 0.33, 0.93); mb.frustum(tuple(b0), tuple(b0 + Vector((0, 0, 0.05))), 0.05, 0.065, flat('#f4f4f0', 0.85), seg=12)

def shafts(G):
    """Camera-only light shafts from the sun-side windows (fake volume: the swept window opening, fading toward the floor)."""
    kd = Vector(P['key_dir']).normalized(); mb = MB(); m = M['shaft']
    for wy in WIN_Y:
        cs = [Vector((XW, wy - WIN_HW + 0.05, WIN_Z[0])), Vector((XW, wy + WIN_HW - 0.05, WIN_Z[0])), Vector((XW, wy + WIN_HW - 0.05, WIN_Z[1])), Vector((XW, wy - WIN_HW + 0.05, WIN_Z[1]))]
        es = [c + kd * (c.z / -kd.z) for c in cs]
        for k in range(4):
            j = (k + 1) % 4; mb.pid += 1; mb.face([cs[k], cs[j], es[j], es[k]], m, [(0, 0), (1, 0), (1, 1), (0, 1)])
    ob = mb.obj('hosp_shafts', G['coll']); ob.visible_shadow = False; S.no_bounce(ob)

# ----------------------------------------------------------------------------- swappable screens
def _screen(name):
    m = bpy.data.materials[name]; nt = m.node_tree
    return nt.nodes['SCREEN_TEX'], nt.nodes['SCREEN_TINT'], nt.nodes['SCREEN_EMIT']

def set_phone_screen(i, image=None, color=None, strength=None, frame=None):
    """Bed i's phone (0..5). image: PNG path (or a bpy image); color: '#rrggbb' or (r, g, b) linear tint multiplied over the image; strength: emission
    (day 1.0; > 1 blooms). frame: also keyframe tint/strength at that frame (the image itself can be an image sequence: tex.image.source = 'SEQUENCE')."""
    return _set(f'phone_screen_{i}', image, color, strength, frame)

def set_monitor_screen(image=None, color=None, strength=None, frame=None):
    """The heart monitor screen (object + material 'monitor_screen'): same arguments as set_phone_screen."""
    return _set('monitor_screen', image, color, strength, frame)

def _set(name, image, color, strength, frame):
    tex, tint, emi = _screen(name)
    if image is not None: tex.image = image if isinstance(image, bpy.types.Image) else bpy.data.images.load(image, check_existing=True)
    if color is not None:
        c = S.hex_lin(color) if isinstance(color, str) else tuple(color); tint.inputs[7].default_value = (*c[:3], 1.0)
        if frame is not None: tint.inputs[7].keyframe_insert('default_value', frame=frame)
    if strength is not None:
        emi.inputs['Strength'].default_value = strength
        if frame is not None: emi.inputs['Strength'].keyframe_insert('default_value', frame=frame)
    return tex.image

# ----------------------------------------------------------------------------- build
BED_STATE = {
    0: dict(blanket='used', lump=0.06, rail_minus=True, rail_plus=False, items=('jug', 'tissue', 'fruit')),
    1: dict(blanket='used', blanket_a=0.95, rail_minus=False, rail_plus=True, items=('jug', 'tissue', 'bottle')),     # hero bed (L middle)
    2: dict(blanket='folded', pillows=2, rail_minus=False, rail_plus=False, items=('bag',)),
    3: dict(blanket='used', lump=0.07, pillows=2, rail_minus=True, rail_plus=True, items=('jug', 'bag', 'bottle')),
    4: dict(blanket='used', lump=0.05, rail_minus=True, rail_plus=False, items=('jug', 'fruit', 'tissue')),
    5: dict(blanket='used', lump=0.06, rail_minus=True, rail_plus=True, items=('jug', 'bottle')),
}

def build(preset='day', clear=True):
    scene = bpy.context.scene
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True); scene = bpy.context.scene
    P.clear(); P.update(PRESETS[preset]); S.STATE.clear(); S.STATE['P'] = P; M.clear(); A.clear(); _MEAN.clear()
    TX.clear(); TX.update(tex_hosp.build_all())
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    materials(); r = random.Random(20261114)
    G = dict(coll=coll, room=MB(), alpha=MB(), blinds=MB(), beds=MB(), props=MB(), curtains=MB())
    room(G)
    for s in (-1, 1):
        for k, wy in enumerate(WIN_Y):
            zb = {(1, 0): 2.25, (1, 1): 2.3, (1, 2): 1.7, (1, 3): 2.4, (1, 4): 2.1}.get((s, k), [1.0, 1.4, 1.0, 1.25, 1.6][k])
            blinds(G, s, wy, zb, 6 if s > 0 else 30)
    beds = []
    for i in range(6):
        side = 'L' if i < 3 else 'R'; cy = BED_Y[i % 3]; st = BED_STATE[i]
        f = bed(G, i, side, cy, st); ph = cabinet(G, i, f, st['items']); headwall(G, i, f, side)
        beds.append(dict(index=i, row=side, center=tuple(round(v, 3) for v in f.P(BED_LEN / 2, 0, 0)), head=tuple(round(v, 3) for v in f.P(0.36, 0, 0.78)),
                         number=i + 1, hero=(i == HERO), **ph))
        if i == HERO: hf = f
    mon = monitor(G, hf)
    iv_stand(G, tuple(hf.P(0.3, -0.72, 0))[:2], bags=2, pump=True, to=hf.P(0.95, -0.3, 0.68))
    for (i, a, b) in ((3, 0.9, 0.62), (5, 0.7, 0.66), (0, 1.0, 0.64)):
        f = BF('L' if i < 3 else 'R', BED_Y[i % 3]); iv_stand(G, tuple(f.P(a, b, 0))[:2], bags=1, pump=(i == 3), to=f.P(a, 0.3, 0.7))
    rails(G); curtains(G); ceiling_stuff(G); A['station'] = station(G, r); misc(G, r)
    wheelchair(G, (2.55, 10.9, 0.0), math.radians(-115)); shafts(G)
    for nm in ('room', 'alpha', 'blinds', 'beds', 'props', 'curtains'): G[nm].obj('hosp_' + nm, coll)
    for ob in coll.objects: S.no_bounce(ob)
    for nm in ('hosp_exterior', 'hosp_shafts', 'hosp_tubes', 'monitor_screen') + tuple(f'phone_screen_{i}' for i in range(6)): bpy.data.objects[nm].visible_shadow = False
    sd = bpy.data.lights.new('key_sun', 'SUN'); kmax = max(P['key']); sd.energy = math.pi * kmax; sd.color = tuple(c / kmax for c in P['key']); sd.angle = math.radians(P['sun_angle'])
    sd.use_shadow = True; so = bpy.data.objects.new('key_sun', sd); lc.objects.link(so)
    so.rotation_euler = Vector(P['key_dir']).normalized().to_track_quat('-Z', 'Y').to_euler()
    w = bpy.data.worlds.new('hosp_world'); scene.world = w; w.use_nodes = True; bg = w.node_tree.nodes.get('Background')
    if bg: bg.inputs['Color'].default_value = (0.02, 0.02, 0.04, 1); bg.inputs['Strength'].default_value = 0.0
    w.cycles.sampling_method = 'NONE'
    S.setup_render(scene, 'fast'); scene.cycles.samples = 12; scene.render.use_persistent_data = False; S.setup_grade(scene, bloom=True)
    scene.cycles.transparent_max_bounces = 12
    # anchors
    hb = beds[HERO]; f = hf
    A['hero_bed'] = dict(index=HERO, number=HERO + 1, center=hb['center'], row='L', head_wall_x=-XW, foot_x=round(-BED_HEAD + BED_LEN, 3), width_y=(round(f.cy - 0.47, 3), round(f.cy + 0.47, 3)),
                         mattress_top_z=0.62, pillow=hb['head'], phone=hb['phone'])
    A['hero_lie'] = tuple(round(v, 3) for v in f.P(0.36, 0, 0.8))
    A['hero_sit'] = dict(hips=tuple(round(v, 3) for v in f.P(0.85, -0.42, 0.62)), feet=tuple(round(v, 3) for v in f.P(0.85, -0.8, 0.0)), facing=(0.0, -1.0, 0.0))
    A['hero_stand'] = tuple(round(v, 3) for v in f.P(0.95, -1.1, 0.0))
    A['nurse_mark'] = tuple(round(v, 3) for v in f.P(0.85, 0.95, 0.0))
    A['aisle'] = [(-0.25, y, 0.0) for y in (-0.6, 2.0, 4.6, 7.2, 9.4)]
    A['beds'] = beds; A['monitor'] = mon
    A['key_dir'] = tuple(round(v, 4) for v in Vector(P['key_dir']).normalized()); A['preset'] = preset; A['units'] = 1.0
    A['room'] = dict(x=(-XW, XW), y=(Y0, Y1), ceiling=HC, windows_y=WIN_Y, window_halfwidth=WIN_HW, window_z=WIN_Z, sun_side='+x (right row windows)')
    A['cams'] = CAMS; A['cams_16x9'] = CAMS_16x9
    mc = Vector(mon['center']); mn = Vector(mon['normal'])
    CAMS['monitor_insert'] = dict(loc=tuple(round(v, 3) for v in mc + mn * 0.7 + Vector((0.12, 0, 0.1))), look_at=tuple(round(v, 3) for v in mc - Vector((0, 0, 0.1))), lens=26)
    return A

CAMS = dict(
    wide_ward=dict(loc=(-0.75, -1.75, 1.6), look_at=(0.35, 14.0, -0.6), lens=21),
    bed_high=dict(loc=(-1.5, 3.5, 2.62), look_at=(-2.95, 4.4, 0.62), lens=19),
    bed_side=dict(loc=(-1.9, 1.2, 1.52), look_at=(-2.75, 4.5, 1.0), lens=22),
    aisle_low=dict(loc=(-1.2, 2.5, 0.92), look_at=(-2.2, 9.0, 0.8), lens=14),
    monitor_insert=dict(loc=(0, 0, 0), look_at=(0, 1, 0), lens=30),
)
CAMS_16x9 = dict(wide_ward=dict(loc=(-0.75, -1.75, 1.6), look_at=(0.3, 14.0, 0.45), lens=17))

def render_cam(name, path, res=(720, 1280), cam=None):
    scene = bpy.context.scene; scene.render.resolution_x, scene.render.resolution_y = res; scene.render.resolution_percentage = 100
    S.make_camera(cam or CAMS[name], name='cam'); return S.render(path)

if __name__ == '__main__':
    args = sys.argv[1:]; cmd = args[0] if args else 'stills'
    preset = args[1] if len(args) > 1 and args[1] in PRESETS else 'day'
    rest = [a for a in args[1:] if a not in PRESETS]
    q = 'preview' if 'preview' in rest else 'final'; cams = [a for a in rest if a in CAMS] or list(CAMS)
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); build(preset); tb = time.time() - t0; scene = bpy.context.scene
    tag = '' if preset == 'day' else '_' + preset
    times = {}
    if cmd == 'stills':
        if q == 'preview': scene.cycles.samples = 6
        for c in cams:
            res = (720, 1280) if q == 'final' else (360, 640)
            w, cpu = render_cam(c, os.path.join(OUT, f'{c}{tag}.png'), res); times[c] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(c, times[c], flush=True)
    elif cmd == 'land':
        w, cpu = render_cam('wide_ward', os.path.join(OUT, f'wide_ward_16x9{tag}.png'), (1920, 1080), CAMS_16x9['wide_ward']); times['wide_ward_16x9'] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(times, flush=True)
    elif cmd == 'debug':                                                    # top view of the set, preview quality
        scene.render.resolution_x, scene.render.resolution_y = 700, 1700; scene.cycles.samples = 4
        cd = bpy.data.cameras.new('top'); cd.type = 'ORTHO'; cd.ortho_scale = 17.2; ob = bpy.data.objects.new('top', cd); scene.collection.objects.link(ob)
        ob.location = (0, 6.5, 3.3); cd.clip_start = 0.01; ob.rotation_euler = (0, 0, 0); scene.camera = ob; S.render(os.path.join(OUT, '_top.png'))
    jp = os.path.join(OUT, 'timing.json'); old = json.load(open(jp)) if os.path.exists(jp) else {}
    old.update({f'{k}{tag}': dict(v, samples=scene.cycles.samples, quality=q, build_s=round(tb, 1)) for k, v in times.items()}); json.dump(old, open(jp, 'w'), indent=1)
    an = {k: v for k, v in A.items()}; json.dump(an, open(os.path.join(OUT, f'anchors{tag}.json'), 'w'), indent=1, default=str)
