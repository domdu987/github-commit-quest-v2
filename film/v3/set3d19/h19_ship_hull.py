"""h19_ship_hull.py : the 1760s 50-gun ship (HMS Deptford type): lofted hull, masts, billowing canvas, rigging, DECK (waist, quarterdeck, forecastle),
bulwark with cap rail, guns, wheel, binnacle, marks.  Authoring in METRES (objects are parented to the metres body empty by the caller).
Grown from styleboard part_ship6.py / part_ship.py.  Ship frame: bow +y (waterline stem y=21), stern y=-21, starboard +x, z up, waterline z=0."""
import os, sys, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h19_kit as K
from h19_kit import mat, mat_emit, metal_mat, MB, hexc, rnd, ring_xy
MATS = K.MATS
THEME = {}           # per-build look switches (set by h19_ship.build_ship): warm=True -> warm-wood masts, cream canvas, wood wheel (deck / rail / rocks presets)
BODY = [None]          # the metres body empty (set by build)
YS, YB = -21.0, 21.0; BH = 5.6                       # stern / bow at the waterline (local y), max half beam
def ss(a, b, x):
    t = np.clip((np.asarray(x, dtype=np.float64) - a) / (b - a), 0.0, 1.0); return t * t * (3 - 2 * t)
def w_wl(t):
    t = np.asarray(t, dtype=np.float64)
    bow = BH * np.maximum(0.0, 1 - np.maximum(0.0, (t - 0.5) / 0.5) ** 2.3) ** 0.9
    ster = BH * (1 - 0.42 * np.maximum(0.0, (0.5 - t) / 0.5) ** 2)
    return np.where(t > 0.5, bow, ster)
def ztop(t):
    t = np.asarray(t, dtype=np.float64)
    return 6.2 + 2.3 * ss(0.30, 0.20, t) + 0.9 * ss(0.82, 0.92, t) + 0.5 * (2 * t - 1) ** 2
def hull_y(t, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return a + np.asarray(t) * (b - a)
def hull_t(y, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return (np.asarray(y) - a) / (b - a)
def hull_x(t, z):
    t = np.asarray(t, dtype=np.float64); z = np.asarray(z, dtype=np.float64); zp = np.clip(z, 0, None)
    flare = 0.32 * ss(0.5, 1.0, t); tumble = 0.16 * (1 - ss(0.5, 1.0, t)) + 0.06
    up = 1 + flare * zp / 6.0 - tumble * (zp / 7.0) ** 2
    dn = np.sqrt(np.clip(1 - (np.clip(-z, 0, None) / 2.45) ** 2, 0.0, 1.0))
    return w_wl(t) * np.where(z >= 0, up, dn)
def deck_z(y): return float(ztop(np.clip((y - YS) / (YB - YS), 0, 1))) - 0.95

def vnoise2(x, y, seed=1):
    G = np.random.RandomState(seed).rand(64, 64).astype(np.float32)
    x = np.asarray(x, dtype=np.float32); y = np.asarray(y, dtype=np.float32)
    xi = np.floor(x).astype(np.int32); yi = np.floor(y).astype(np.int32); fx = x - xi; fy = y - yi
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    a = G[xi & 63, yi & 63]; b = G[(xi + 1) & 63, yi & 63]; c = G[xi & 63, (yi + 1) & 63]; d = G[(xi + 1) & 63, (yi + 1) & 63]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
def fbm2(x, y, seed=1, octs=3):
    s = 0.0; a = 1.0; tot = 0.0; f = 1.0
    for i in range(octs):
        s = s + a * vnoise2(x * f + 17.0 * i, y * f + 31.0 * i, seed + i); tot += a; a *= 0.5; f *= 2.03
    return s / tot

def mesh_obj(name, verts, faces, mats, midx=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces]); me.update()
    for m in mats: me.materials.append(m)
    for i, p in enumerate(me.polygons):
        p.use_smooth = smooth
        if midx is not None: p.material_index = int(midx[i])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob

def ship_mats():
    M = {}
    M['deck1'] = mat('deck1', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['deck2'] = mat('deck2', '#a67c44', '#bc9255', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['seam'] = mat('seam', '#2c1c20')
    M['hullb'] = mat('hullb', '#2a2622', '#36302a', scale=2, aniso=(0.3, 0.3, 1))
    M['ochre'] = mat('ochre', '#cf9230', '#bd7f26', scale=3)
    M['bulw'] = mat('bulw', '#a24c2c', '#8f3f28', scale=3, aniso=(0.2, 1, 1))
    M['cap'] = mat('cap', '#2a2622', '#3a342c', scale=3)
    M['iron'] = mat('iron', '#2a2622', '#38322c', scale=6, rough=0.6)
    M['carr'] = mat('carr', '#8a3e28', '#9c4a30', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.8, metallic=0.9)
    M['sail'] = mat('sail', '#e6d4a0', '#d8c48c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.08)
    M['sail2'] = mat('sail2', '#dac690', '#cbb77c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.06)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#6f9a78', 0.9); M['isle2'] = mat_emit('isle2', '#4f7e68', 0.8); M['beach'] = mat_emit('beach', '#e8dcb8', 1.0)
    M['darksail'] = mat('darksail', '#2c2838')
    M['lamp'] = mat_emit('lamp', '#ffd890', 6.0); M['spray'] = mat('spray', '#eef4f0', '#dbe8e6', scale=2); M['lid'] = mat('lid', '#a07a48', '#8e6a3c', scale=6); M['port'] = mat('port', '#7a2c22', '#8e3828', scale=4)
    return M
def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_obj(M, name, PF, nx, ny, thick=0.03):
    """smooth, two-sided (solidified) sail mesh from a (i,j)->xyz function; canvas strips alternate between two materials"""
    verts = [PF(i, j) for j in range(ny + 1) for i in range(nx + 1)]
    faces = []; midx = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; faces.append((a, a + 1, a + nx + 2, a + nx + 1)); midx.append(i % 2)
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(M['sail']); me.materials.append(M['sail2'])
    for p, mi in zip(me.polygons, midx): p.use_smooth = True; p.material_index = mi
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    md = ob.modifiers.new('thick', 'SOLIDIFY'); md.thickness = thick; md.offset = 0.0
    return ob
def _mix_self(m, hexcol, k, fac):
    nt = m.node_tree; bs = nt.nodes['bsdf']; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = fac
    nt.links.new(bs.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])

def _sail_self_cream(m, k, fac=0.85):
    """deck / rail sails: part of the shading is pure cream emission (strength k) so the blue ambient cannot turn the canvas lavender; Principled part keeps the cream base, translucency / transmission 0"""
    nt = m.node_tree; bs = nt.nodes['bsdf']; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc('#e8dcc0'); em.inputs['Strength'].default_value = k
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = fac
    nt.links.new(bs.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])
    if 'Transmission Weight' in bs.inputs: bs.inputs['Transmission Weight'].default_value = 0.0

def ship6_mats():
    M = ship_mats()
    M['mast'] = mat('mast6', '#7a6458', '#8c7466', scale=3, aniso=(0.2, 0.2, 0.05)); M['oak'] = mat('oak6', '#7e6454', '#8e7462', scale=5, aniso=(0.15, 1, 1))
    M['hull6'] = mat('hull6', '#28262c', '#36343a', scale=2.5, aniso=(0.25, 0.25, 4.5), contrast=1.2)
    M['ochre6'] = mat('ochre6', '#d89a34', '#c4832a', scale=3, aniso=(0.3, 0.3, 2.0))
    M['cap6'] = mat('cap6', '#2c2a30', '#3c3a42', scale=3)
    M['port6'] = mat('port6', '#241410', '#3a1c16', scale=3)
    M['deck6'] = mat('deck6', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['canv'] = mat('canv', '#c6b67e', '#baa874', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a8', emit_k=0.07)
    M['canv2'] = mat('canv2', '#bcac74', '#b0a06c', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a8', emit_k=0.06)
    M['gold'] = mat('gold', '#d8a840', '#c08c30', scale=4, sheen=0.3)
    M['pen'] = mat('pen', '#c0392f', '#a8302a', scale=4)
    M['rig6'] = mat('rig6', '#2c2430', '#40343e', scale=3)
    if THEME.get('warm'):
        M['mast'] = mat('mast6w', '#3a2e26', '#4a3a2e', scale=3, aniso=(0.2, 0.2, 0.05)); M['oak'] = mat('oak6w', '#6a4628', '#7e5632', scale=5, aniso=(0.15, 1, 1))
        M['canv'] = mat('canvw', '#e8dcc0', '#e8dcc0', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#e8dcc0', emit_k=0.0)     # cream like ship_hero; no translucency (0)
        M['canv2'] = mat('canv2w', '#e2d6b8', '#e2d6b8', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#e8dcc0', emit_k=0.0)
        M['rig6'] = mat('rig6w', '#2e2620', '#40342a', scale=3); M['iron'] = mat('iron_w', '#4a4038', '#5c5248', scale=6, rough=0.6)
        for _k in ('canv', 'canv2'): _sail_self_cream(M[_k], THEME.get('sail_k', 0.5), THEME.get('sail_fac', 0.85))
    M['sail'] = M['canv']; M['sail2'] = M['canv2']
    return M
def build_hull6(M):
    nt = 130; T = np.linspace(0.0, 1.0, nt)
    base = [-2.35, -1.6, -0.9, -0.35, 0.0, 0.5, 1.2, 2.0, 3.1, 3.6, 4.4, 5.3, 5.7]
    zt = ztop(T)
    Z = np.zeros((nt, len(base) + 3))
    Z[:, :len(base)] = np.array(base)[None, :]; Z[:, len(base)] = 5.7 + (zt - 5.7) * 0.5; Z[:, len(base) + 1] = zt; Z[:, len(base) + 2] = zt + 0.16
    Kc = Z.shape[1]; Tm = T[:, None] * np.ones((1, Kc))
    X = hull_x(Tm, Z); Y = hull_y(Tm, Z)
    X[:, -1] = hull_x(T, zt) + 0.12; Y[:, -1] = hull_y(T, zt) + 0.0; Y[:, -2] = hull_y(T, zt)
    verts = []; faces = []; midx = []
    for s in (-1, 1):
        for i in range(nt):
            for j in range(Kc): verts.append((s * X[i, j], Y[i, j], Z[i, j]))
    ctr = np.array([0, 0, 2.5])
    for si, s in enumerate((-1, 1)):
        off = si * nt * Kc
        for i in range(nt - 1):
            for j in range(Kc - 1):
                a = off + i * Kc + j; b = off + (i + 1) * Kc + j; c = off + (i + 1) * Kc + j + 1; d = off + i * Kc + j + 1
                zm = 0.5 * (Z[i, j] + Z[i, j + 1])
                if j == Kc - 2: mi = 2
                elif (3.1 <= zm <= 3.6) or (5.3 <= zm <= 5.7): mi = 1
                else: mi = 0
                if s == 1: faces.append((a, b, c, d))
                else: faces.append((d, c, b, a))
                midx.append(mi)
    # transom (stern) and flat keel closure
    off0 = 0; off1 = nt * Kc
    for j in range(Kc - 1):
        faces.append((off0 + j, off1 + j, off1 + j + 1, off0 + j + 1)); midx.append(1 if j == Kc - 2 else 0)
    ob = mesh_obj('ship6_hull', verts, faces, [M['hull6'], M['ochre6'], M['cap6']], midx, True)
    # deck fill (barely visible from the low camera, closes the hull for shadows)
    dv = []; df = []
    for i in range(nt):
        zd = zt[i] - 0.95; bd = hull_x(T[i], zd) * 0.97; yd = hull_y(T[i], zd)
        for xx in (-1.0, -0.33, 0.33, 1.0): dv.append((xx * bd, yd, zd))
    for i in range(nt - 1):
        for c in range(3): a = i * 4 + c; df.append((a, a + 1, a + 5, a + 4))
    mesh_obj('ship6_deck', dv, df, [M['deck6']], None, False)
    # gun ports (two rows) as flat frames on the hull side, ochre frame + dark port
    mb = MB('ship6_ports')
    def pquad(m, y0, y1, z0, z1, s, off):
        pts = []
        for (yy, zz) in ((y0, z0), (y1, z0), (y1, z1), (y0, z1)):
            t = float(hull_t(yy, zz)); pts.append((s * (float(hull_x(t, zz)) + off), yy, zz))
        mb.quad(m, pts)
    for zc in (2.55, 4.45):
        y = -15.2
        while y < 16.0:
            for s in (-1, 1):
                pquad(M['ochre6'], y - 0.52, y + 0.52, zc - 0.45, zc + 0.41, s, 0.03)
                pquad(M['port6'], y - 0.44, y + 0.44, zc - 0.38, zc + 0.34, s, 0.06)
            y += 2.4
    mb.finish()
    return ob

def sq_sail(M, name, my, zb, zt_, hw_top, hw_foot, belly, nx=22, ny=16, yoff=0.55):
    def PF(i, j):
        u = 2.0 * i / nx - 1.0; v = j / ny
        hwv = hw_foot + (hw_top - hw_foot) * v
        by = belly * (1 - abs(u) ** 2.3) ** 0.8 * math.sin(math.pi * (0.07 + 0.86 * v)) ** 0.85 * (1 + 0.05 * math.sin(u * 8.0 + v * 3.0))
        z = zb + (zt_ - zb) * v + 0.05 * (zt_ - zb) * (1 - u * u) * (1 - v) ** 2
        return (u * hwv, my + yoff + by, z)
    ob = sail_obj(M, name, PF, nx, ny, 0.04); ob.visible_glossy = False; return ob

def spanker(M, name, my, z0, H):
    A = Vector((0, my - 0.7, z0 + 0.52 * H)); B = Vector((0, my - 8.6, z0 + 0.60 * H)); C = Vector((0, my - 11.8, z0 + 0.09 * H)); D = Vector((0, my - 0.7, z0 + 0.09 * H))
    nx, ny = 14, 12
    def PF(i, j):
        u = i / nx; v = j / ny
        P = (D * (1 - u) + C * u) * (1 - v) + (A * (1 - u) + B * u) * v
        b = -1.6 * math.sin(math.pi * u) ** 0.8 * math.sin(math.pi * (0.1 + 0.8 * v))
        return (P.x + b, P.y, P.z)
    ob = sail_obj(M, name, PF, nx, ny, 0.04); ob.visible_glossy = False; return ob

def jib(M, name, T, C, Hd, bulge, n=10, m=10):
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def PF(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m; p = L + (Rr - L) * u
        b = -bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.1 + 0.9 * v)) * (1 - 0.4 * v)
        return (p.x + b, p.y, p.z)
    ob = sail_obj(M, name, PF, m, n, 0.04); ob.visible_glossy = False; return ob

def rigging6(mb, M, my, z0, H, s_sides=(-1, 1), nshr=5):
    top = z0 + 0.41 * H
    for s in s_sides:
        for k in range(nshr):
            yy = my - 1.8 + 0.9 * k; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
            a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * k, top))
            mb.rod(M['rig6'], a, b, 0.05, 0.04, 4)
        for q in np.linspace(0.08, 0.92, 15):
            for k in range(nshr - 1):
                def pt(kk):
                    yy = my - 1.8 + 0.9 * kk; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
                    a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * kk, top)); return a + (b - a) * q
                mb.rod(M['rig6'], pt(k), pt(k + 1), 0.026, 0.026, 4)
        for k in range(3):           # topmast shrouds
            mb.rod(M['rig6'], Vector((s * 0.9, my - 0.6 + 0.4 * k, top + 0.2)), Vector((s * 0.12, my - 0.3, z0 + 0.77 * H)), 0.035, 0.03, 4)
        mb.rod(M['rig6'], Vector((s * 0.2, my - 0.4, z0 + 0.77 * H)), Vector((s * (float(hull_x(float(hull_t(my - 7.0, 4.4)), 4.4)) + 0.4), my - 7.0, deck_z(my - 7.0) - 0.6)), 0.04, 0.035, 4)    # backstay

def mast6(mb, M, my, H, yards):
    z0 = deck_z(my); ms = 0.62 if THEME.get('warm') else 1.0
    tube(mb, M['mast'], (0, my, z0 - 0.5), (0, my, z0 + 0.52 * H), 0.58 * ms, 0.36 * ms, 12)
    tube(mb, M['mast'], (0, my, z0 + 0.40 * H), (0, my, z0 + 0.80 * H), 0.30, 0.19, 10)
    tube(mb, M['mast'], (0, my, z0 + 0.76 * H), (0, my, z0 + H), 0.17, 0.08, 8)
    mb.box(M['mast'], (0, my - 0.2, z0 + 0.41 * H), (3.2, 2.6, 0.22)); mb.box(M['rig6'], (0, my - 0.2, z0 + 0.41 * H - 0.13), (3.3, 2.7, 0.04))
    for (fz, ln, r) in yards:
        zy = z0 + fz * H; tube(mb, M['mast'], (-ln / 2, my, zy), (ln / 2, my, zy), r, r * 0.55, 8)
        for s in (-1, 1): mb.rod(M['rig6'], (s * ln / 2, my, zy), (s * 0.4, my, zy + 0.18 * H * (0.8 if fz < 0.6 else 0.55)), 0.025, 0.025, 4)
    # pennant at the truck
    mb.quad(M['pen'], [(0, my, z0 + H), (0.0, my - 5.5, z0 + H - 0.2), (0.0, my - 5.2, z0 + H - 0.75), (0, my, z0 + H - 0.5)])
    mb.quad(M['pen'], [(0, my, z0 + H - 0.5), (0.0, my - 5.2, z0 + H - 0.75), (0.0, my - 5.5, z0 + H - 0.2), (0, my, z0 + H)])
    rigging6(mb, M, my, z0, H)
def build_ship6(P):
    before = set(bpy.data.objects)
    M = ship6_mats(); mb = MB('ship6'); sc = bpy.context.scene
    build_hull6(M)
    # quarter gallery + stern lantern + beakhead + figurehead
    for s in (-1, 1):
        mb.box(M['hull6'], (s * 4.25, -16.6, 7.7), (1.2, 3.6, 2.7)); mb.box(M['ochre6'], (s * 4.25, -16.6, 9.1), (1.3, 3.7, 0.18))
        for k in range(3): mb.box(M['port6'], (s * 4.88, -18.0 + 1.2 * k, 7.8), (0.06, 0.7, 1.1))
    if not THEME.get('no_stern_lamp'):
        mb.box(M['gold'], (0, -21.2, 10.0), (0.9, 0.9, 1.3)); mb.cyl(M['gold'], (0, -21.2, 10.8), 0.38, 0.4, seg=10)
    tube(mb, M['gold'], (0, YB + 2.2, 4.6), (0, YB + 4.8, 5.8), 0.36, 0.22, 8); mb.ell(M['gold'], (0, YB + 5.0, 5.9), (0.3, 0.55, 0.38), (10, 6))
    for s in (-1, 1): tube(mb, M['ochre6'], (s * 0.15, YB + 1.0, 4.9), (s * 0.5, YB + 4.8, 5.4), 0.1, 0.07, 6)
    # three masts: fore, main, mizzen
    mast6(mb, M, 11.5, 36.0, [(0.27, 15.5, 0.20), (0.55, 12.2, 0.16), (0.77, 8.8, 0.12), (0.91, 5.8, 0.09)])
    mast6(mb, M, -0.5, 40.0, [(0.27, 17.8, 0.22), (0.55, 13.6, 0.17), (0.77, 9.8, 0.13), (0.91, 6.4, 0.09)])
    mast6(mb, M, -12.5, 29.0, [(0.27, 12.5, 0.17), (0.52, 10.0, 0.13), (0.74, 7.2, 0.10)])
    # square sails (head on the yard, foot above the deck), billowing forward
    for (nm, my, H, spec) in (('fore', 11.5, 36.0, [(0.27, 0.07, 7.2, 8.0, 2.0), (0.55, 0.31, 5.6, 6.4, 1.7), (0.77, 0.58, 4.0, 4.5, 1.2), (0.91, 0.80, 2.6, 3.0, 0.7)]),
                              ('main', -0.5, 40.0, [(0.27, 0.07, 8.0, 8.9, 2.3), (0.55, 0.31, 6.2, 7.0, 1.9), (0.77, 0.58, 4.4, 4.9, 1.3), (0.91, 0.80, 2.8, 3.2, 0.8)]),
                              ('miz', -12.5, 29.0, [(0.52, 0.30, 4.8, 5.4, 1.4), (0.74, 0.55, 3.4, 3.8, 1.0)])):
        z0 = deck_z(my)
        for k, (fy, ff, hwt, hwf, bel) in enumerate(spec): sq_sail(M, 'ship6_sail_%s%d' % (nm, k), my, z0 + ff * H, z0 + fy * H, hwt, hwf, bel)
    spanker(M, 'ship6_spanker', -12.5, deck_z(-12.5), 29.0)
    # bowsprit, jib boom, spritsail yard, stays, jibs
    tube(mb, M['mast'], (0, YB - 4.0, 5.2), (0, YB + 10.5, 10.6), 0.42, 0.20, 10); tube(mb, M['mast'], (0, YB + 10.0, 10.4), (0, YB + 15.5, 12.2), 0.16, 0.08, 8)
    z0f = deck_z(11.5); z0m = deck_z(-0.5)
    fore_top = Vector((0, 11.5, z0f + 0.80 * 36.0)); fore_t2 = Vector((0, 11.5, z0f + 0.45 * 36.0)); main_top = Vector((0, -0.5, z0m + 0.80 * 40.0)); miz_top = Vector((0, -12.5, deck_z(-12.5) + 0.78 * 29.0))
    for (a, b) in ((Vector((0, YB + 15.5, 12.2)), fore_top), (Vector((0, YB + 10.5, 10.6)), fore_t2), (fore_top, main_top), (fore_t2, Vector((0, -0.5, z0m + 0.45 * 40.0))), (main_top, miz_top), (Vector((0, -0.5, z0m + 0.45 * 40.0)), Vector((0, -12.5, deck_z(-12.5) + 0.42 * 29.0)))):
        mb.rod(M['rig6'], a, b, 0.05, 0.05, 4)
    jib(M, 'ship6_jib1', (0, YB + 15.0, 12.0), (0, YB + 9.5, 9.0), (0, 31.2, z0f + 0.78 * 36.0), 1.3)
    jib(M, 'ship6_jib2', (0, YB + 10.0, 10.4), (0, YB + 4.6, 7.8), (0, 28.6, z0f + 0.52 * 36.0), 1.2)
    jib(M, 'ship6_jib3', (0, YB + 4.0, 7.4), (0, YB - 3.0, 6.9), (0, 24.0, z0f + 0.40 * 36.0), 1.0)
    # square spritsail under the bowsprit
    tube(mb, M['mast'], (-3.4, YB + 4.6, 8.0), (3.4, YB + 4.6, 8.0), 0.12, 0.08, 6)
    sq_sail(M, 'ship6_sprit', YB + 4.6, 5.0, 8.0, 3.0, 3.3, 0.9, 10, 8, 0.2)
    mb.finish()
    return M, before
