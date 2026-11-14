"""The welder's rented room (ห้องเช่า) in Thonburi, at night, as a real 3D set (bpy 5.3, Cycles CPU). For 'ช่างเชื่อมสายฟ้า'.
World: 1 unit = 1 m, Z up, floor z = 0. Room interior x -1.6..1.6, y 0..4.0, ceiling 2.6 (walls 0.12 thick).
  far wall y = 4.0 : the wooden door (opening x -0.40..0.50, leaf hinged at x -0.34, opens INTO the room), cloth rack, apron + mask on nails
  right wall x = 1.6 : window with grille / mosquito screen (y 2.0..3.1, z 0.95..2.05), mattress below it, calendar, posters, TV in the corner
  outside the door: open-air corridor y 4.12..5.6 with a parapet and railing, neighbours' doors, shoes, a hanging fluorescent tube (cold).
Light model (toonlit.py): blue-violet ambient as emission + Toon key from real lights: the warm bare bulb (hard shadows), two neon spills
through the window grille (teal, orange), the corridor tube (area light). The fluorescent strip in the room is OFF.
    import room3d; A = room3d.build('night')        # -> anchors (sit_mark, door_inside_mark, doorway_mark, door_hinge, bulb, cams ...)
    room3d.set_door(80)                              # door leaf angle in degrees (0 shut, + opens into the room)
    room3d.set_lights(False)                         # bulb off (room goes to neon + ambient); outside lights stay on
CLI: python3 room3d.py stills [night] [final|preview] [cam ...]   -> out_room/<cam>.png (+ timing.json, anchors.json)
     python3 room3d.py land                                       -> out_room/room_wide_16x9.png (1920x1080)"""
import os, sys, math, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import office3d as S
import toonlit as TL
import tex_room
from soi3d import F, rect, tube, smooth, catenary
MB = S.MB
OUT = os.path.join(HERE, 'out_room')

X0, X1, Y0, Y1, H, WT = -1.6, 1.6, 0.0, 4.0, 2.6, 0.12
DOOR = dict(x0=-0.40, x1=0.50, z1=2.05, hinge=(-0.34, 3.985), w=0.78, t=0.04, h=1.977, z0=0.018)
WIN = dict(y0=2.0, y1=3.1, z0=0.95, z1=2.05)
CY = 5.6                                            # corridor parapet line
PRESETS = {
    'night': dict(shade=(0.046, 0.058, 0.168), lift=(0.006, 0.005, 0.015), form=(0.0, 0.0, 0.20), gain=0.55, bloom_size=0.05, lambert=0.6,
                  grade_offset=(0.002, 0.002, 0.009), grade_saturation=1.28,
                  bulb=dict(color='#ffd29a', K=1.4, d=2.075), corr=dict(color='#d6efff', K=1.5, d=2.27),
                  neon_teal=dict(color='#2ee6d6', K=1.7), neon_orange=dict(color='#ff9440', K=0.95)),
}
A = {}; P = {}; M = {}; TX = {}; OBJ = {}

# ----------------------------------------------------------------------------- materials
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
    """Per-channel ambient multiplier that turns art x SHADE into the preset's blue-violet at the art's own luminance (as soi3d)."""
    sh = P['shade']; lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    L = max(lum(mean), 1e-4); want = [x / lum(sh) * L for x in sh]; got = [max(m * x, 1e-5) for m, x in zip(mean, sh)]
    return tuple(min(2.2, max(0.45, (w / g) ** strength)) for w, g in zip(want, got))

def lit(name, img=None, color='#808080', gain=0.9, shade=None, alpha=False, fix=0.8, **kw):
    nm = 'ROOM_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    sm = shade if shade is not None else shade_fix(art_mean(img, color), fix)
    kw.setdefault('lambert', P.get('lambert', 0.0))
    return TL.mat_toon(nm, P, color=color, image=img and TX[img], gain=gain * P['gain'], shade_mul=sm, alpha=alpha, form=P['form'], **kw)

def flat(hexcol, gain=0.85):
    nm = 'f_%s_%g' % (hexcol.lstrip('#'), gain)
    if nm not in M: M[nm] = lit(nm, color=hexcol, gain=gain)
    return M[nm]

def emit(name, color, strength): return S.mat_emit('ROOM_E_' + name, color, strength=strength)

def materials():
    m = dict(wall_far=lit('wall_far', 'wall_far'), wall_right=lit('wall_right', 'wall_right'), wall_left=lit('wall_left', 'wall_left'),
             wall_near=lit('wall_near', 'wall_near'), wall_out=lit('wall_out', 'wall_out'), floor=lit('floor', 'floor', gain=0.95),
             ceiling=lit('ceiling', 'ceiling', gain=0.14), door_in=lit('door_in', 'door_in', gain=0.95), door_out=lit('door_out', 'door_out', gain=0.95),
             doors=lit('doors', 'doors', gain=0.9), mattress=lit('mattress', 'mattress', gain=0.9), blanket=lit('blanket', 'blanket', gain=1.0),
             pillow=lit('pillow', 'pillow', gain=0.85), wardrobe=lit('wardrobe', 'wardrobe', gain=0.9), clothes=lit('clothes', 'clothes', gain=0.9, alpha=True),
             apron=lit('apron', 'apron', gain=0.95, alpha=True), gecko=lit('gecko', 'gecko', gain=0.9, alpha=True), shoes=lit('shoes', 'shoes', gain=0.9, alpha=True),
             posters=lit('posters', 'posters', gain=0.85), calendar=lit('calendar', 'calendar', gain=0.85), paybook=lit('paybook', 'paybook', gain=0.8),
             calc=lit('calc', 'calc', gain=0.9), yantra=lit('yantra', 'yantra', gain=0.85), photos=lit('photos', 'photos', gain=0.85), notice=lit('notice', 'notice', gain=0.85), bag=lit('bag', 'bag', gain=0.9), drawers=lit('drawers', 'drawers', gain=0.9), cup=lit('cup', 'cup', gain=0.85), tv=lit('tv', 'tv', gain=0.9), mask=lit('mask', 'mask', gain=0.95),
             grille=lit('grille', 'grille', gain=0.85, alpha=True), screen=lit('screen', 'screen', gain=0.9, alpha=True),
             corr_floor=lit('corr_floor', 'corr_floor', gain=0.95), meter=lit('meter', 'meter', gain=0.85),
             city_win=emit('city_win_x', '#ffffff', 1.0), city_far=emit('city_far_x', '#ffffff', 1.0),
             bulb=TL.mat_glow('ROOM_G_bulb', '#fff2d0', 9.0, off=0.0, off_color='#8a8478'), filament=TL.mat_glow('ROOM_G_fil', '#ffffff', 22.0, off=0.0),
             corr_tube=S.mat_emit('ROOM_E_ctube', '#e8f6ff', strength=5.0), coil_tip=S.mat_emit('ROOM_E_tip', '#ff5a20', strength=4.0),
             tube_off=flat('#c8ccc8', 0.9), alu=flat('#b8bcc0', 0.9), black=flat('#1a1a1c', 0.8), white=flat('#ecebe4', 0.85),
             wood=flat('#7a4a2a', 0.9), plastic_red=flat('#d8302a', 0.85), plastic_blue=flat('#3a7ad8', 0.85), chrome=flat('#c8ccd0', 0.95),
             brass=flat('#c8a040', 0.9), conduit=flat('#cfcabc', 0.7), concrete=flat('#9a9a8e', 0.9), parapet=lit('parapet', 'wall_out', gain=0.9))
    for k, im in (('city_win', 'city_win'), ('city_far', 'city_far')):
        nt = m[k].node_tree; tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = S._img(TX[im]); em = [n for n in nt.nodes if n.type == 'EMISSION'][0]
        nt.links.new(tx.outputs['Color'], em.inputs['Color'])
    M.update(m)

# ----------------------------------------------------------------------------- helpers
def cyl(mb, p0, p1, r0, mat, seg=16, r1=None, cap0=True, cap1=True, u_rep=1.0, v=(0.0, 1.0)):
    """Cylinder / cone with wrapped UVs (u around 0..u_rep, v along)."""
    r1 = r0 if r1 is None else r1; p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0).normalized(); mb.pid += 1
    u = a.cross(Vector((0, 0, 1)))
    if u.length < 1e-4: u = Vector((1, 0, 0))
    u.normalize(); w = a.cross(u)
    ring = lambda p, r: [p + r * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * w) for i in range(seg + 1)]
    A_, B_ = ring(p0, r0), ring(p1, r1)
    for i in range(seg):
        mb.face([A_[i], A_[i + 1], B_[i + 1], B_[i]], mat, [(i / seg * u_rep, v[0]), ((i + 1) / seg * u_rep, v[0]), ((i + 1) / seg * u_rep, v[1]), (i / seg * u_rep, v[1])])
    if cap0 and r0 > 0: mb.face(A_[:seg][::-1], mat)
    if cap1 and r1 > 0: mb.face(B_[:seg], mat)

def blob(mb, c, rx, ry, rz, mat, seg=16, rings=8, rnd=None, amp=0.0, flat_bottom=True):
    """Lumpy ellipsoid (pillow, helmet, rice sack). Planar UVs over x, y."""
    c = Vector(c); R_ = []; mb.pid += 1; ph = [rnd.uniform(0, 6.28) for _ in range(4)] if rnd else [0] * 4
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            phi = 2 * math.pi * i / seg; n = 1 + amp * (math.sin(3 * phi + ph[0]) * math.sin(2 * th + ph[1]) + 0.5 * math.sin(5 * phi + ph[2]))
            z = -rz * math.cos(th)
            if flat_bottom and z < -rz * 0.6: z = -rz * 0.6
            row.append(c + Vector((rx * math.sin(th) * math.cos(phi) * n, ry * math.sin(th) * math.sin(phi) * n, z * (1 + 0.3 * amp * math.sin(phi * 2 + ph[3])))))
        R_.append(row)
    uv = lambda p: (0.5 + (p.x - c.x) / (2 * rx), 0.5 + (p.y - c.y) / (2 * ry))
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; q = [R_[k][i], R_[k][j], R_[k + 1][j], R_[k + 1][i]]; mb.face(q, mat, [uv(p) for p in q])

def heightfield(mb, x0, x1, y0, y1, nx, ny, hf, mat, uvs=(1.0, 1.0)):
    mb.pid += 1; pts = [[Vector((x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny, 0)) for j in range(ny + 1)] for i in range(nx + 1)]
    for i in range(nx + 1):
        for j in range(ny + 1): pts[i][j].z = hf(pts[i][j].x, pts[i][j].y)
    for i in range(nx):
        for j in range(ny):
            q = [pts[i][j], pts[i + 1][j], pts[i + 1][j + 1], pts[i][j + 1]]
            mb.face(q, mat, [(p.x / uvs[0], p.y / uvs[1]) for p in q])

def wall_holes(mb, origin, du, dz, L, Hh, mat, holes=(), n=None):
    """Wall rectangle origin + u*du + z*dz (u 0..L, z 0..Hh), cut by rectangular holes (u0, u1, z0, z1); UV continuous over the wall."""
    o, du, dz = Vector(origin), Vector(du), Vector(dz); P_ = lambda u, z: o + du * u + dz * z; uv = lambda u, z: (u / L, z / Hh)
    pieces = [(0, L, 0, Hh)]
    for (a, b, c, d) in holes:
        nxt = []
        for (u0, u1, z0, z1) in pieces:
            if b <= u0 or a >= u1 or d <= z0 or c >= z1: nxt.append((u0, u1, z0, z1)); continue
            if a > u0: nxt.append((u0, a, z0, z1))
            if b < u1: nxt.append((b, u1, z0, z1))
            aa, bb = max(a, u0), min(b, u1)
            if c > z0: nxt.append((aa, bb, z0, c))
            if d < z1: nxt.append((aa, bb, d, z1))
        pieces = nxt
    for (u0, u1, z0, z1) in pieces:
        q = [P_(u0, z0), P_(u1, z0), P_(u1, z1), P_(u0, z1)]; F(mb, q, mat, [uv(u0, z0), uv(u1, z0), uv(u1, z1), uv(u0, z1)], n)

def bx(mb, lo, hi, mat, **kw): mb.box(lo, hi, mat, **kw)

# ----------------------------------------------------------------------------- the room shell
def shell(G):
    mb = G['shell']
    F(mb, [(X0, Y0, 0), (X1, Y0, 0), (X1, Y1, 0), (X0, Y1, 0)], M['floor'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    F(mb, [(X0, Y0, H), (X1, Y0, H), (X1, Y1, H), (X0, Y1, H)], M['ceiling'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, -1))
    d = DOOR; wa, wb = d['x0'] - X0, d['x1'] - X0
    wall_holes(mb, (X0, Y1, 0), (1, 0, 0), (0, 0, 1), X1 - X0, H, M['wall_far'], [(wa, wb, -1, d['z1'])], (0, -1, 0))
    wall_holes(mb, (X1, Y1, 0), (0, -1, 0), (0, 0, 1), Y1 - Y0, H, M['wall_right'], [(Y1 - WIN['y1'], Y1 - WIN['y0'], WIN['z0'], WIN['z1'])], (-1, 0, 0))
    wall_holes(mb, (X0, Y0, 0), (0, 1, 0), (0, 0, 1), Y1 - Y0, H, M['wall_left'], [], (1, 0, 0))
    wall_holes(mb, (X1, Y0, 0), (-1, 0, 0), (0, 0, 1), X1 - X0, H, M['wall_near'], [], (0, 1, 0))
    # door frame: jambs, head, stops, inner casing
    fw = flat('#5a3a20', 0.9)
    bx(mb, (d['x0'], Y1 - 0.02, 0), (d['x0'] + 0.05, Y1 + WT, d['z1']), fw); bx(mb, (d['x1'] - 0.05, Y1 - 0.02, 0), (d['x1'], Y1 + WT, d['z1']), fw)
    bx(mb, (d['x0'], Y1 - 0.02, d['z1'] - 0.05), (d['x1'], Y1 + WT, d['z1']), fw)
    for (a, b) in ((d['x0'] + 0.05, d['x0'] + 0.065), (d['x1'] - 0.065, d['x1'] - 0.05)): bx(mb, (a, 4.027, 0), (b, 4.05, d['z1'] - 0.05), fw)
    bx(mb, (d['x0'] + 0.05, 4.027, d['z1'] - 0.065), (d['x1'] - 0.05, 4.05, d['z1'] - 0.05), fw)
    cs = flat('#6a4426', 0.9)
    bx(mb, (d['x0'] - 0.07, Y1 - 0.03, 0), (d['x0'], Y1, d['z1'] + 0.07), cs); bx(mb, (d['x1'], Y1 - 0.03, 0), (d['x1'] + 0.07, Y1, d['z1'] + 0.07), cs)
    bx(mb, (d['x0'] - 0.07, Y1 - 0.03, d['z1']), (d['x1'] + 0.07, Y1, d['z1'] + 0.07), cs)
    bx(mb, (d['x0'] + 0.05, 3.99, -0.01), (d['x1'] - 0.05, Y1 + WT, 0.004), flat('#8a8070', 0.9))            # worn threshold strip
    # window reveal, sill, aluminium sliding sashes, grille (inside), mosquito screen, curtain
    w = WIN; gr = flat('#d8d2c4', 0.9)
    bx(mb, (X1, w['y0'] - 0.01, w['z0'] - 0.01), (X1 + WT, w['y1'] + 0.01, w['z0']), gr); bx(mb, (X1, w['y0'] - 0.01, w['z1']), (X1 + WT, w['y1'] + 0.01, w['z1'] + 0.01), gr)
    bx(mb, (X1, w['y0'] - 0.01, w['z0']), (X1 + WT, w['y0'], w['z1']), gr); bx(mb, (X1, w['y1'], w['z0']), (X1 + WT, w['y1'] + 0.01, w['z1']), gr)
    bx(mb, (X1 - 0.06, w['y0'] - 0.08, w['z0'] - 0.04), (X1 + 0.02, w['y1'] + 0.08, w['z0']), flat('#cfc8b8', 0.9))
    al = M['alu']; ym = (w['y0'] + w['y1']) / 2
    for (xx, ya, yb) in ((X1 + 0.06, w['y0'], ym + 0.03), (X1 + 0.09, ym - 0.03, w['y1'])):          # two sashes, slid half open
        for (a, b, c_, e) in ((ya, yb, w['z0'], w['z0'] + 0.035), (ya, yb, w['z1'] - 0.035, w['z1']), (ya, ya + 0.035, w['z0'], w['z1']), (yb - 0.035, yb, w['z0'], w['z1'])):
            bx(mb, (xx - 0.012, a, c_), (xx + 0.012, b, e), al)
    rect(G['alpha'], (X1 + 0.075, (w['y0'] + ym) / 2, (w['z0'] + w['z1']) / 2), (0, (ym - w['y0']) / 2 - 0.02, 0), (0, 0, (w['z1'] - w['z0']) / 2 - 0.03), M['screen'], (0, 0, 2.0, 2.0), (-1, 0, 0))
    rect(G['alpha'], (X1 - 0.025, (w['y0'] + w['y1']) / 2, (w['z0'] + w['z1']) / 2), (0, -(w['y1'] - w['y0']) / 2, 0), (0, 0, (w['z1'] - w['z0']) / 2), M['grille'], n=(-1, 0, 0))
    hy = 2.86; tube(mb, [(X1 - 0.03, hy, w['z1'] - 0.03), (X1 - 0.06, hy, w['z1'] - 0.07), (X1 - 0.06, hy, w['z1'] - 0.1)], 0.003, M['chrome'], 4)
    F(G['alpha'], [(X1 - 0.07, hy + 0.2, w['z1'] - 0.62), (X1 - 0.07, hy - 0.2, w['z1'] - 0.62), (X1 - 0.07, hy - 0.2, w['z1'] - 0.08), (X1 - 0.07, hy + 0.2, w['z1'] - 0.08)], M['clothes'],
      [(0.505, 0.04), (0.745, 0.04), (0.745, 0.98), (0.505, 0.98)], (-1, 0, 0))
    for k, (yy, zz, a) in enumerate(((1.66, 1.22, 4), (1.78, 1.16, -6), (1.56, 1.06, 9))):
        q = [Vector((X1 - 0.003, yy + 0.05, zz - 0.07)), Vector((X1 - 0.003, yy - 0.05, zz - 0.07)), Vector((X1 - 0.003, yy - 0.05, zz + 0.07)), Vector((X1 - 0.003, yy + 0.05, zz + 0.07))]
        uvs = [((0.0, 0.35), (0.5, 0.35), (0.5, 1.0), (0.0, 1.0)), ((0.5, 0.35), (1.0, 0.35), (1.0, 1.0), (0.5, 1.0)), ((0.0, 0.0), (0.5, 0.0), (0.5, 0.6), (0.0, 0.6))][k]
        F(mb, q, M['paybook'] if k != 1 else M['notice'], list(uvs), (-1, 0, 0))
    for (yy, zz, a) in ((1.66, 1.22, 4), (1.78, 1.16, -6), (1.56, 1.06, 9)): bx(mb, (X1 - 0.005, yy - 0.02, zz + 0.06), (X1 - 0.003, yy + 0.02, zz + 0.075), flat('#e8dca8'))
    for (yy, zz) in ((w['y0'] + 0.02, w['z0'] + 0.1), (w['y1'] - 0.02, w['z0'] + 0.1), (w['y0'] + 0.02, w['z1'] - 0.1), (w['y1'] - 0.02, w['z1'] - 0.1)):
        bx(mb, (X1 - 0.03, yy - 0.015, zz - 0.015), (X1, yy + 0.015, zz + 0.015), flat('#8a4a1a'))     # rusty grille anchors
    # curtain rod + a faded curtain bunched at the far side of the window
    tube(mb, [(X1 - 0.07, w['y0'] - 0.25, w['z1'] + 0.12), (X1 - 0.07, w['y1'] + 0.35, w['z1'] + 0.12)], 0.009, M['chrome'], 6)
    cur = flat('#d8905a', 0.85); n = 9; yb, ye = w['y1'] - 0.1, w['y1'] + 0.32
    pts = [Vector((X1 - 0.07 + (0.05 if i % 2 else -0.0), yb + (ye - yb) * i / n, 0)) for i in range(n + 1)]
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        F(mb, [(a.x, a.y, w['z0'] - 0.25), (b.x, b.y, w['z0'] - 0.22), (b.x, b.y, w['z1'] + 0.1), (a.x, a.y, w['z1'] + 0.1)], cur, None)
    # fluorescent strip on the ceiling (OFF), pull cord; ceiling rose + cord + socket + bare bulb
    bx(mb, (-0.95, 3.32, H - 0.05), (0.3, 3.42, H), M['white']); cyl(mb, (-0.9, 3.37, H - 0.07), (0.25, 3.37, H - 0.07), 0.014, M['tube_off'], 10)
    for xx in (-0.92, 0.27): bx(mb, (xx - 0.02, 3.35, H - 0.09), (xx + 0.02, 3.39, H - 0.05), M['white'])
    tube(mb, [(0.28, 3.37, H - 0.05), (0.29, 3.37, H - 0.33)], 0.0025, M['white'], 4); cyl(mb, (0.29, 3.37, H - 0.39), (0.29, 3.37, H - 0.33), 0.008, M['black'], 8)
    b = A['bulb']; cyl(mb, (b[0], b[1], H - 0.02), (b[0], b[1], H), 0.04, M['white'], 12)
    tube(mb, smooth([Vector((b[0], b[1], H - 0.02)), Vector((b[0] + 0.01, b[1], H - 0.25)), Vector((b[0], b[1], b[2] + 0.075))], 4), 0.004, M['black'], 5)
    cyl(mb, (b[0], b[1], b[2] + 0.03), (b[0], b[1], b[2] + 0.075), 0.015, M['black'], 12)
    blob(G['bulb'], (b[0], b[1], b[2] - 0.004), 0.03, 0.03, 0.036, M['bulb'], 14, 8, flat_bottom=False)
    tube(G['bulb'], [(b[0] - 0.008, b[1], b[2] + 0.005), (b[0], b[1], b[2] - 0.01), (b[0] + 0.008, b[1], b[2] + 0.005)], 0.0015, M['filament'], 4)
    # door chain: anchor plate on the casing, the chain hangs unhooked
    ch = flat('#9a9a96', 0.95); bx(mb, (0.515, Y1 - 0.036, 1.41), (0.555, Y1 - 0.03, 1.5), ch)
    cpts = [Vector((0.535 + 0.012 * math.sin(i * 1.3), Y1 - 0.04, 1.455 - i * 0.022)) for i in range(11)]
    for i in range(10): tube(mb, [cpts[i], cpts[i + 1]], 0.0035, ch, 4)
    cyl(mb, cpts[-1], cpts[-1] - Vector((0, 0, 0.02)), 0.008, ch, 8)
    rect(mb, (0.05, Y1 - 0.004, 2.27), (0.18, 0, 0), (0, 0, 0.126), M['yantra'], n=(0, -1, 0))                           # yantra cloth above the door
    for k, (xx, zz, a) in enumerate(((-0.95, 1.98, 0.05), (-0.74, 2.02, -0.06), (-0.53, 1.97, 0.08))):                    # snapshots taped left of the door
        c = Vector((xx, Y1 - 0.004, zz)); u = Vector((0.085 * math.cos(a), 0, 0.085 * math.sin(a))); v = Vector((-0.085 * math.sin(a), 0, 0.085 * math.cos(a)))
        F(mb, [c - u - v, c + u - v, c + u + v, c - u + v], M['photos'], [(k / 3, 0), ((k + 1) / 3, 0), ((k + 1) / 3, 1), (k / 3, 1)], (0, -1, 0))
    # clothesline above the mattress along the right wall: socks, a towel, a vest
    lp = catenary((X1 - 0.25, 0.12, 2.12), (X1 - 0.25, 1.5, 2.12), 0.1, 16); tube(mb, lp, 0.003, flat('#3a8a5a'), 4)
    for k, (t_, cell, ww, hh) in enumerate(((0.12, 3, 0.26, 0.42), (0.38, 0, 0.2, 0.3), (0.62, 2, 0.3, 0.46), (0.85, 1, 0.12, 0.3))):
        pc = lp[int(t_ * 16)]; F(G['alpha'], [(pc.x, pc.y - ww / 2, pc.z - hh), (pc.x, pc.y + ww / 2, pc.z - hh), (pc.x, pc.y + ww / 2, pc.z), (pc.x, pc.y - ww / 2, pc.z)], M['clothes'],
                                 [(cell * 0.25 + 0.24, 0.3), (cell * 0.25 + 0.01, 0.3), (cell * 0.25 + 0.01, 0.98), (cell * 0.25 + 0.24, 0.98)], (-1, 0, 0))
        for dy in (-ww / 2 + 0.02, ww / 2 - 0.02): bx(mb, (pc.x - 0.01, pc.y + dy - 0.006, pc.z - 0.02), (pc.x + 0.01, pc.y + dy + 0.006, pc.z + 0.015), flat(['#e83a2a', '#2a8ae0', '#f0c030', '#30b050'][k]))
    # small pink-framed mirror and a laminated Buddha picture left of the door, above the switch
    bx(mb, (-0.7, Y1 - 0.015, 1.5), (-0.46, Y1 - 0.005, 1.84), flat('#e87aa0', 0.85)); bx(mb, (-0.68, Y1 - 0.017, 1.52), (-0.48, Y1 - 0.015, 1.82), flat('#9ab0c8', 0.6))
    F(mb, [(-0.66, Y1 - 0.018, 1.56), (-0.6, Y1 - 0.018, 1.56), (-0.52, Y1 - 0.018, 1.78), (-0.58, Y1 - 0.018, 1.78)], flat('#dce8f4', 0.8), None, (0, -1, 0))
    # conduit from the switch (left of the door) up the wall and across the ceiling to the rose
    sw = (-0.56, Y1, 1.3); bx(mb, (sw[0] - 0.045, Y1 - 0.025, sw[2] - 0.06), (sw[0] + 0.045, Y1, sw[2] + 0.06), M['white'])
    bx(mb, (sw[0] - 0.012, Y1 - 0.03, sw[2] - 0.005), (sw[0] + 0.012, Y1 - 0.024, sw[2] + 0.03), flat('#3a3a3a'))
    cd = M['conduit']; bx(mb, (sw[0] - 0.01, Y1 - 0.018, sw[2] + 0.06), (sw[0] + 0.01, Y1, H), cd)
    bx(mb, (sw[0] - 0.01, b[1] - 0.01, H - 0.018), (sw[0] + 0.01, Y1, H), cd); bx(mb, (sw[0] - 0.01, b[1] - 0.01, H - 0.018), (b[0], b[1] + 0.01, H), cd)
    bx(mb, (sw[0] - 0.01, 3.36, H - 0.018), (-0.6, 3.38, H), cd)
    # outlet + extension strip by the TV corner
    bx(mb, (1.0, Y1 - 0.02, 0.28), (1.08, Y1, 0.36), M['white']); bx(mb, (1.03, Y1 - 0.018, 0.36), (1.05, Y1, H), cd)      # outlet fed from the ceiling
    bx(mb, (0.75, 3.78, 0), (1.05, 3.84, 0.04), M['white'])
    for k in range(4): bx(mb, (0.78 + k * 0.065, 3.79, 0.04), (0.82 + k * 0.065, 3.83, 0.042), flat('#2a2a2a'))
    tube(mb, smooth([Vector((1.04, 3.98, 0.3)), Vector((1.05, 3.92, 0.08)), Vector((1.0, 3.84, 0.02))], 3), 0.004, M['white'], 4)

def door_obj(G):
    """The door leaf as its own object, origin on the hinge axis: rotation_euler.z = -radians(angle). Local: x' along the leaf from the
    hinge (0 .. 0.78), y' through it (0 = room face .. 0.04 = corridor face), z up."""
    d = DOOR; mb = MB(); w, t, z0, z1 = d['w'], d['t'], d['z0'], d['z0'] + d['h']
    mb.box((0, 0, z0), (w, t, z1), flat('#6a4426', 0.9), mats=dict(front=M['door_in'], back=M['door_out']))
    br, bk = M['brass'], M['black']
    for zz in (0.25, 1.0, 1.75): mb.box((-0.006, -0.003, zz - 0.05), (0.025, t + 0.003, zz + 0.05), flat('#4a4a46'))        # hinges
    for (yy, s) in ((-0.004, -1), (t + 0.004, 1)):                                                                   # lever handles both faces
        cyl(mb, (w - 0.09, yy, 1.0), (w - 0.09, yy + s * 0.012, 1.0), 0.028, br, 14)
        cyl(mb, (w - 0.09, yy + s * 0.012, 1.0), (w - 0.09, yy + s * 0.05, 1.0), 0.009, br, 8)
        mb.box((w - 0.21, min(yy + s * 0.04, yy + s * 0.05) - 0.004, 0.99), (w - 0.09, max(yy + s * 0.04, yy + s * 0.05) + 0.004, 1.01), br)
        mb.box((w - 0.1, yy + s * 0.003 - 0.002, 0.88), (w - 0.08, yy + s * 0.003 + 0.002, 0.92), bk)                 # keyhole plate
    cyl(mb, (0.39, -0.008, 1.55), (0.39, t + 0.008, 1.55), 0.011, br, 12)                                           # peephole
    cyl(mb, (0.39, -0.0085, 1.55), (0.39, -0.0083, 1.55), 0.006, flat('#1a2a3a', 0.6), 10)
    mb.box((w - 0.2, -0.012, 1.44), (w - 0.06, 0.0, 1.47), flat('#9a9a96', 0.95)); mb.box((w - 0.19, -0.016, 1.452), (w - 0.07, -0.012, 1.458), bk)  # chain slide track
    mb.box((w - 0.12, t, 1.12), (w - 0.06, t + 0.012, 1.2), flat('#7a7a76', 0.95)); cyl(mb, (w - 0.09, t + 0.012, 1.13), (w - 0.09, t + 0.03, 1.13), 0.005, flat('#7a7a76'), 6)   # hasp
    mo = flat('#5e3a1e', 0.9)
    for (yy, s_) in ((-0.0, -1), (t, 1)):                                                                            # moulded panels, both faces
        for (a0, a1, c0, c1) in ((0.1, 0.68, 1.12, 1.86), (0.1, 0.68, 0.14, 0.88)):
            for (p0, p1, q0, q1) in ((a0, a1, c0, c0 + 0.025), (a0, a1, c1 - 0.025, c1), (a0, a0 + 0.025, c0, c1), (a1 - 0.025, a1, c0, c1)):
                y0_, y1_ = (yy - 0.008, yy) if s_ < 0 else (yy, yy + 0.008); mb.box((p0, y0_, q0), (p1, y1_, q1), mo)
    hk = flat('#c8ccd0', 0.95); mb.box((0.3, -0.02, z1 - 0.01), (0.36, t + 0.005, z1 + 0.012), hk)                                   # over-door hook
    mb.box((0.31, -0.03, z1 - 0.12), (0.35, -0.02, z1 + 0.012), hk); tube(mb, [(0.33, -0.03, z1 - 0.12), (0.33, -0.06, z1 - 0.14), (0.33, -0.065, z1 - 0.1)], 0.005, hk, 4)
    blob(mb, (0.33, -0.1, z1 - 0.2), 0.1, 0.06, 0.07, flat('#1a1a2a', 0.9), 12, 6, None, 0.0, False); mb.box((0.25, -0.17, z1 - 0.25), (0.41, -0.1, z1 - 0.235), flat('#1a1a2a', 0.9))   # cap
    F(mb, [(0.18, -0.035, z1 - 0.15), (0.5, -0.035, z1 - 0.15), (0.52, -0.05, z1 - 0.62), (0.16, -0.05, z1 - 0.6)], M['clothes'], [(0.76, 0.35), (0.99, 0.35), (0.99, 0.98), (0.76, 0.98)], (0, -1, 0))
    ob = mb.obj('room_door', G['coll']); ob.location = (d['hinge'][0], d['hinge'][1], 0.0); S.no_bounce(ob); OBJ['door'] = ob
    return ob

def set_door(angle_deg=0.0):
    """Door leaf angle in degrees: 0 = shut, positive = open into the room (80 = wide open, leaf along the left of the opening)."""
    ob = OBJ.get('door') or bpy.data.objects.get('room_door')
    ob.rotation_euler = (0.0, 0.0, -math.radians(angle_deg)); A['door_angle'] = angle_deg
    return ob

# ----------------------------------------------------------------------------- furniture and props
def furniture(G, r):
    mb, pm, al = G['shell'], G['props'], G['alpha']
    # mattress (1.0 x 2.0 x 0.085) along the right wall, pillow, crumpled plaid blanket, phone on charge
    mx0, mx1, my0, my1, mz = 0.58, 1.56, 0.35, 2.35, 0.085
    pm.box((mx0, my0, 0), (mx1, my1, mz), flat('#c07272', 0.85), mats=dict(top=M['mattress']))
    blob(pm, (1.08, 0.62, mz + 0.06), 0.3, 0.17, 0.08, M['pillow'], 16, 8, r, 0.06)
    def hf(x, y):
        u = (x - 0.8) / 0.78; v = (y - 0.95) / 1.4; edge = max(0.0, min(1.0, u * 4, (1 - u) * 6, v * 5, (1 - v) * 5))
        h = 0.07 + 0.05 * math.sin(9 * x + 4 * y) + 0.035 * math.sin(17 * y - 6 * x + 1) + 0.03 * math.sin(23 * x + 13 * y) + 0.06 * math.exp(-((x - 1.25) ** 2 + (y - 1.3) ** 2) / 0.05)
        return mz + 0.004 + max(0.0, h) * edge
    heightfield(pm, 0.8, 1.58, 0.95, 2.35, 26, 44, hf, M['blanket'], (0.9, 0.9))
    pm.box((0.95, 0.95, mz), (1.03, 1.1, mz + 0.008), M['black']); tube(pm, smooth([Vector((0.99, 1.1, mz + 0.004)), Vector((1.1, 1.6, mz + 0.01)), Vector((1.5, 2.45, 0.012)), Vector((1.45, 3.3, 0.006)), Vector((1.0, 3.8, 0.02))], 4), 0.0025, flat('#3a3a3e'), 4)
    # low folding table with the night's business: open สมุดผ่อน, calculator, noodle cups, pen, water, coins, receipts
    tx0, tx1, ty0, ty1, tz = -0.34, 0.30, 1.40, 2.02, 0.33
    pm.box((tx0, ty0, tz - 0.025), (tx1, ty1, tz), flat('#e6d2b8', 0.9)); pm.box((tx0 + 0.02, ty0 + 0.02, tz - 0.06), (tx1 - 0.02, ty1 - 0.02, tz - 0.025), flat('#b8a088', 0.85))
    for xx in (tx0 + 0.06, tx1 - 0.06):
        for (ya, yb) in ((ty0 + 0.05, ty0 + 0.08), (ty1 - 0.08, ty1 - 0.05)): pm.box((xx - 0.015, ya, 0), (xx + 0.015, yb, tz - 0.06), M['chrome'])
        pm.box((xx - 0.015, ty0 + 0.05, 0), (xx + 0.015, ty1 - 0.05, 0.025), M['chrome'])
    bk = MB(); rect(bk, (0, 0, 0.0012), (0.15, 0, 0), (0, 0.105, 0), M['paybook']); bk.box((-0.15, -0.105, -0.006), (0.15, 0.105, 0), flat('#1e5aa0', 0.85))
    bo = bk.obj('room_paybook', G['coll']); bo.location = (0.02, 1.68, tz + 0.007); bo.rotation_euler = (0, 0, math.radians(84)); S.no_bounce(bo)
    cc = MB(); rect(cc, (0, 0, 0.012), (0.04, 0, 0), (0, 0.06, 0), M['calc']); cc.box((-0.04, -0.06, 0), (0.04, 0.06, 0.0118), flat('#2a2a30'))
    co = cc.obj('room_calc', G['coll']); co.location = (0.14, 1.88, tz); co.rotation_euler = (0, 0, math.radians(70)); S.no_bounce(co)
    for (cx, cy, open_) in ((-0.2, 1.55, True), (-0.22, 1.86, False)):
        cyl(pm, (cx, cy, tz), (cx, cy, tz + 0.105), 0.042, M['cup'], 18, r1=0.05, cap0=True, cap1=not open_)
        if open_:
            cyl(pm, (cx, cy, tz + 0.06), (cx, cy, tz + 0.062), 0.047, flat('#c87a3a', 0.8), 18, cap0=False)
            F(pm, [(cx + 0.03, cy - 0.04, tz + 0.105), (cx + 0.08, cy - 0.06, tz + 0.2), (cx + 0.11, cy + 0.02, tz + 0.19), (cx + 0.06, cy + 0.03, tz + 0.105)], flat('#e8e4d8', 0.9))
            tube(pm, [(cx - 0.01, cy, tz + 0.06), (cx - 0.03, cy + 0.01, tz + 0.2)], 0.004, flat('#f0f0f0'), 4)
    tube(pm, [(0.1, 1.55, tz + 0.006), (0.22, 1.6, tz + 0.006)], 0.005, M['plastic_blue'], 6)
    cyl(pm, (0.22, 1.47, tz), (0.22, 1.47, tz + 0.11), 0.032, flat('#c8e0e8', 0.7), 14, r1=0.035); cyl(pm, (0.22, 1.47, tz + 0.005), (0.22, 1.47, tz + 0.06), 0.03, flat('#9ac0d8', 0.75), 14)
    for k in range(6):
        x, y = r.uniform(-0.1, 0.26), r.uniform(1.44, 1.98); cyl(pm, (x, y, tz), (x, y, tz + 0.003), r.uniform(0.01, 0.013), flat(r.choice(['#c8a040', '#b8bcc0'])), 10)
    for k in range(3):
        x, y = r.uniform(-0.3, 0.0), r.uniform(1.95, 2.0); s_ = MB(); rect(s_, (0, 0, 0), (0.04, 0, 0), (0, 0.07, 0), flat('#f4f0e4')); so = s_.obj('room_slip%d' % k, G['coll']); so.location = (x + k * 0.06, y - 0.02 * k, tz + 0.001 + k * 0.001); so.rotation_euler = (0, 0, r.uniform(-1, 1)); S.no_bounce(so)
    # standing fan aimed at the mattress
    fx, fy = -0.78, 2.9; fan = M['plastic_blue']; wh = M['white']
    cyl(pm, (fx, fy, 0), (fx, fy, 0.035), 0.17, wh, 18); cyl(pm, (fx, fy, 0.035), (fx, fy, 0.05), 0.08, fan, 12); cyl(pm, (fx, fy, 0.05), (fx, fy, 1.05), 0.016, M['chrome'], 8)
    for k in range(4): bx(pm, (fx + 0.05 - 0.03 * k, fy - 0.06, 0.035), (fx + 0.07 - 0.03 * k, fy - 0.045, 0.045), flat(['#e83a2a', '#e8e4d8', '#e8e4d8', '#e8e4d8'][k]))
    fc = Vector((fx, fy, 1.12)); dv = (Vector((0.62, 1.7, 0.75)) - fc).normalized()
    pm.frustum(tuple(fc - dv * 0.12), tuple(fc + dv * 0.03), 0.075, 0.07, fan, seg=14); cyl(pm, fc - dv * 0.05, fc - Vector((0, 0, 0.07)), 0.02, fan, 8)
    up = Vector((0, 0, 1)); sd = dv.cross(up).normalized(); up2 = sd.cross(dv).normalized(); hub = fc + dv * 0.09
    for k in range(3):
        a = k * 2.094 + 0.4; e = math.cos(a) * up2 + math.sin(a) * sd; e2 = -math.sin(a) * up2 + math.cos(a) * sd
        rect(pm, hub + e * 0.1, e * 0.085, e2 * 0.045, flat('#5ab8e8', 0.8))
    cyl(pm, hub - dv * 0.01, hub + dv * 0.03, 0.03, flat('#2a5ab0'), 10)
    for k in range(12):
        a = k * math.pi / 12; e = (math.cos(a) * up2 + math.sin(a) * sd) * 0.19
        tube(pm, [hub - dv * 0.04 + e, hub + dv * 0.07, hub - dv * 0.04 - e], 0.0025, M['chrome'], 3)
    tube(pm, [hub - dv * 0.04 + up2 * 0.19 * math.cos(t) + sd * 0.19 * math.sin(t) for t in [i * math.pi / 12 for i in range(25)]], 0.003, M['chrome'], 3)
    tube(pm, smooth([Vector((fx, fy, 0.03)), Vector((fx + 0.3, fy + 0.3, 0.01)), Vector((0.75, 3.8, 0.02))], 4), 0.004, wh, 4)
    # TV on a red plastic stool in the far right corner, turned toward the mattress
    sx, sy = 1.24, 3.62; cyl(pm, (sx, sy, 0), (sx, sy, 0.43), 0.17, M['plastic_red'], 16, r1=0.14); cyl(pm, (sx, sy, 0.43), (sx, sy, 0.45), 0.155, M['plastic_red'], 16)
    tv = MB(); tv.box((-0.21, -0.18, 0), (0.21, 0.0, 0.35), flat('#3a3a3e', 0.85), mats=dict(front=M['tv'])); tv.box((-0.17, 0.0, 0.03), (0.17, 0.2, 0.32), flat('#2e2e32', 0.85))
    for s_ in (-1, 1): tube(tv, [(s_ * 0.03, 0.05, 0.32), (s_ * 0.2, 0.12, 0.62)], 0.004, M['chrome'], 4)
    tv.box((-0.05, 0.02, 0.32), (0.05, 0.1, 0.35), flat('#2a2a2a'))
    to = tv.obj('room_tv', G['coll']); to.location = (sx, sy + 0.03, 0.45); to.rotation_euler = (0, 0, math.atan2(-(0.6 - sx), (1.6 - sy)) + math.pi); S.no_bounce(to)
    tube(pm, smooth([Vector((sx, sy + 0.2, 0.5)), Vector((sx - 0.1, 3.9, 0.2)), Vector((1.0, 3.84, 0.02))], 4), 0.004, M['black'], 4)
    # cloth rack against the far wall, left of the door: work clothes, jeans, football shirt, towel
    rx0, rx1, ry, rz = -1.52, -0.66, 3.78, 1.62
    for xx in (rx0, rx1): cyl(pm, (xx, ry, 0.0), (xx, ry, rz), 0.012, M['chrome'], 8); bx(pm, (xx - 0.03, ry - 0.2, 0), (xx + 0.03, ry + 0.15, 0.03), M['chrome'])
    cyl(pm, (rx0, ry, rz), (rx1, ry, rz), 0.012, M['chrome'], 8)
    for k, (xc, cell, yoff, ww) in enumerate(((-1.38, 0, 0.0, 0.46), (-1.12, 1, -0.05, 0.42), (-0.9, 2, -0.1, 0.44), (-0.74, 3, -0.14, 0.4))):
        rect(al, (xc, ry + yoff, rz - 0.42), (ww / 2, 0, 0), (0, 0, 0.44), M['clothes'], (cell * 0.25 + 0.005, 0.02, cell * 0.25 + 0.245, 0.98), (0, -1, 0))
    blob(pm, (-0.88, 3.5, 0.12), 0.22, 0.16, 0.12, flat('#4a6a9a', 0.85), 12, 6, r, 0.15)              # pile of dirty clothes
    pm.box((-1.55, 3.45, 0), (-1.15, 3.95, 0.6), flat('#e8ecf0', 0.85), mats=dict(front=M['drawers']))   # 3-drawer plastic cabinet under the rack
    cyl(pm, (-1.35, 3.62, 0.6), (-1.35, 3.62, 0.78), 0.1, flat('#e8e4dc', 0.9), 14, r1=0.09); cyl(pm, (-1.35, 3.62, 0.78), (-1.35, 3.62, 0.82), 0.07, flat('#c8302a'), 12)   # rice cooker
    cyl(pm, (-1.22, 3.8, 0.6), (-1.22, 3.8, 0.9), 0.05, flat('#a8d0e8', 0.7), 12, r1=0.035)
    blob(pm, (-0.62, 3.62, 0.08), 0.14, 0.12, 0.08, flat('#e8e4d8', 0.85), 12, 6, r, 0.2)
    # landlord's notice, key hook with the motorbike key, a plastic bag hanging on a nail, floor clutter by the mattress
    rect(pm, (0.84, Y1 - 0.003, 1.95), (0.105, 0, 0), (0, 0, 0.15), M['notice'], n=(0, -1, 0))
    pm.box((0.62, Y1 - 0.02, 1.76), (0.62 + 0.2, Y1, 1.79), M['wood'])
    for k in range(4): cyl(pm, (0.65 + k * 0.05, Y1 - 0.02, 1.765), (0.65 + k * 0.05, Y1 - 0.05, 1.77), 0.003, M['chrome'], 4)
    for (kx, col) in ((0.65, '#c8302a'), (0.75, '#2a6ad0')):
        tube(pm, [(kx, Y1 - 0.045, 1.765), (kx, Y1 - 0.04, 1.69)], 0.0025, M['chrome'], 3); pm.box((kx - 0.012, Y1 - 0.05, 1.63), (kx + 0.012, Y1 - 0.035, 1.69), flat(col))
    F(al, [(-0.3, 0.012, 0.9), (0.02, 0.012, 0.9), (0.04, 0.03, 1.3), (-0.32, 0.03, 1.3)], M['bag'], None, (0, 1, 0))
    for (bx_, by_, a, s_) in ((0.38, 0.62, 0.3, 0.16), (-0.6, 1.2, 1.1, 0.14)):
        bg_ = MB(); blob(bg_, (0, 0, s_ * 0.6), s_, s_ * 0.8, s_ * 0.6, M['bag'], 12, 6, r, 0.25); go = bg_.obj('room_bag', G['coll']); go.location = (bx_, by_, 0); go.rotation_euler = (0, 0, a); S.no_bounce(go)
    cyl(pm, (0.45, 2.55, 0), (0.45, 2.55, 0.28), 0.04, flat('#c8e8f0', 0.7), 12, r1=0.03); cyl(pm, (0.45, 2.55, 0.28), (0.45, 2.55, 0.31), 0.015, flat('#2a6ad0'), 8)
    rk = MB(); rk.box((-0.012, 0, 0), (0.012, 0.25, 0.02), flat('#e8c020')); rk.box((-0.09, 0.25, 0), (0.09, 0.5, 0.012), flat('#e8c020'))
    for k in range(6): rk.box((-0.085 + k * 0.034, 0.26, 0.012), (-0.08 + k * 0.034, 0.49, 0.016), flat('#3a3a3a'))
    ro = rk.obj('room_racket', G['coll']); ro.location = (-0.55, 0.75, 0); ro.rotation_euler = (0, 0, 0.6); S.no_bounce(ro)
    for k in range(5):
        pp = MB(); rect(pp, (0, 0, 0), (0.105, 0, 0), (0, 0.148, 0), flat(['#f4f0e4', '#f8e8c0', '#e8f0f8', '#f4f0e4', '#ffd8d8'][k])); po = pp.obj('room_papers', G['coll'])
        po.location = (0.45 + r.uniform(-0.05, 0.05), 1.2 + r.uniform(-0.05, 0.05), 0.001 + k * 0.001); po.rotation_euler = (0, 0, r.uniform(-0.6, 0.6)); S.no_bounce(po)
    # plastic zip wardrobe on the left wall
    wx0, wx1, wy0, wy1, wz = -1.58, -1.12, 2.15, 3.05, 1.5
    pm.box((wx0, wy0, 0.04), (wx1, wy1, wz), flat('#9ab8d8', 0.85), mats=dict(right=M['wardrobe'], front=M['wardrobe']))
    for (yy) in (wy0, wy1):
        for xx in (wx0 + 0.02, wx1 - 0.02): cyl(pm, (xx, yy, 0), (xx, yy, wz + 0.02), 0.01, M['white'], 6)
    blob(pm, (-1.35, 2.6, wz + 0.1), 0.2, 0.36, 0.1, flat('#e8b830', 0.85), 12, 6, r, 0.12)               # bag on top
    # apron and welding mask on nails right of the door; calendar, posters, gecko
    ax0, ax1, az0, az1 = 0.6, 1.08, 0.86, 1.66
    F(al, [(ax0, Y1 - 0.035, az0), (ax1, Y1 - 0.045, az0), (ax1, Y1 - 0.012, az1), (ax0, Y1 - 0.012, az1)], M['apron'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    cyl(pm, ((ax0 + ax1) / 2, Y1, az1 + 0.1), ((ax0 + ax1) / 2, Y1 - 0.04, az1 + 0.11), 0.004, flat('#5a5a5a'), 5)
    tube(pm, [(ax0 + 0.12, Y1 - 0.015, az1 - 0.01), ((ax0 + ax1) / 2, Y1 - 0.03, az1 + 0.1), (ax1 - 0.12, Y1 - 0.015, az1 - 0.01)], 0.009, flat('#3a2412'), 5)
    mk = MB(); blob(mk, (0, 0, 0), 0.12, 0.07, 0.16, flat('#2a3a2e', 0.9), 16, 8, None, 0.0, False)
    rect(mk, (0, -0.072, 0.0), (0.105, 0, 0), (0, 0, 0.13), M['mask'], n=(0, -1, 0))
    tube(mk, [(-0.12, 0.0, 0.02), (-0.13, 0.08, 0.05), (0.0, 0.11, 0.1), (0.13, 0.08, 0.05), (0.12, 0, 0.02)], 0.01, M['black'], 5)
    mo = mk.obj('room_mask', G['coll']); mo.location = (1.3, Y1 - 0.085, 1.5); mo.rotation_euler = (math.radians(-12), 0, math.radians(8)); S.no_bounce(mo)
    cyl(pm, (1.3, Y1, 1.68), (1.3, Y1 - 0.05, 1.69), 0.004, flat('#5a5a5a'), 5)
    rect(pm, (X1 - 0.004, 3.5, 1.78), (0, -0.21, 0), (0, 0, 0.315), M['calendar'], n=(-1, 0, 0))
    rect(pm, (-1.2, Y1 - 0.004, 2.08), (0.21, 0, 0), (0, 0, 0.3), M['posters'], (0.0, 0.0, 1 / 3, 1.0), (0, -1, 0))
    rect(pm, (X1 - 0.004, 1.1, 1.62), (0, -0.21, 0), (0, 0, 0.3), M['posters'], (1 / 3, 0.0, 2 / 3, 1.0), (-1, 0, 0))
    rect(pm, (X1 - 0.004, 0.62, 1.55), (0, -0.21, 0), (0, 0, 0.3), M['posters'], (2 / 3, 0.0, 1.0, 1.0), (-1, 0, 0))
    rect(al, (0.18, Y1 - 0.003, 2.3), (0.06, 0, 0), (0, 0, 0.06), M['gecko'], n=(0, -1, 0))
    # above the mattress, behind the sit mark: a Buddha shelf with a garland, a battery clock, a round mirror, a cap and a towel on hooks
    sy = 1.82; pm.box((X1 - 0.16, sy - 0.22, 1.98), (X1, sy + 0.22, 2.0), flat('#8a5a30')); pm.box((X1 - 0.14, sy - 0.03, 1.9), (X1, sy + 0.03, 1.98), flat('#8a5a30'))
    blob(pm, (X1 - 0.07, sy, 2.07), 0.035, 0.035, 0.07, flat('#e8b030', 0.95), 10, 6, None, 0.0); blob(pm, (X1 - 0.07, sy, 2.15), 0.022, 0.022, 0.025, flat('#e8b030', 0.95), 8, 5, None, 0.0, False)
    tube(pm, [(X1 - 0.12, sy - 0.12, 2.0), (X1 - 0.13, sy - 0.08, 1.93), (X1 - 0.13, sy + 0.08, 1.93), (X1 - 0.12, sy + 0.12, 2.0)], 0.012, flat('#f2c030', 0.9), 6)
    for k in range(5): blob(pm, (X1 - 0.13, sy - 0.08 + k * 0.04, 1.93), 0.014, 0.014, 0.014, flat(['#f08a20', '#ffffff', '#f08a20', '#ffffff', '#f08a20'][k], 0.9), 6, 4, None, 0.0, False)
    cyl(pm, (X1 - 0.11, sy + 0.17, 2.0), (X1 - 0.11, sy + 0.17, 2.08), 0.02, flat('#c8302a'), 8)
    cyl(pm, (X1, 1.42, 1.62), (X1 - 0.03, 1.42, 1.62), 0.11, M['white'], 20); cyl(pm, (X1 - 0.03, 1.42, 1.62), (X1 - 0.032, 1.42, 1.62), 0.095, flat('#f4f0e4'), 20)
    for a in range(12): t = a * math.pi / 6; bx(pm, (X1 - 0.034, 1.42 + 0.08 * math.cos(t) - 0.004, 1.62 + 0.08 * math.sin(t) - 0.004), (X1 - 0.032, 1.42 + 0.08 * math.cos(t) + 0.004, 1.62 + 0.08 * math.sin(t) + 0.004), M['black'])
    tube(pm, [(X1 - 0.035, 1.42, 1.62), (X1 - 0.035, 1.42 + 0.03, 1.68)], 0.004, M['black'], 4); tube(pm, [(X1 - 0.035, 1.42, 1.62), (X1 - 0.035, 1.48, 1.6)], 0.003, M['black'], 4)
    for (yy, zz) in ((1.15, 1.25), (1.0, 1.25)): cyl(pm, (X1, yy, zz), (X1 - 0.05, yy, zz + 0.01), 0.005, flat('#5a5a5a'), 5)
    blob(pm, (X1 - 0.08, 1.15, 1.17), 0.07, 0.1, 0.08, flat('#2a4a8a', 0.9), 12, 6, None, 0.05)
    F(pm, [(X1 - 0.03, 0.92, 1.25), (X1 - 0.03, 1.08, 1.25), (X1 - 0.05, 1.07, 0.75), (X1 - 0.05, 0.93, 0.74)], flat('#e8e4d8', 0.9), None, (-1, 0, 0))
    rect(al, (X1 - 0.003, 3.0, 2.3), (0, -0.05, 0), (0, 0, 0.05), M['gecko'], n=(-1, 0, 0))
    # motorbike helmet, work gloves, mosquito coil with a glowing tip, water bottles
    blob(pm, (1.18, 2.62, 0.12), 0.14, 0.14, 0.13, flat('#f0c020', 0.85), 16, 8, None, 0.0); cyl(pm, (1.1, 2.62, 0.08), (1.04, 2.62, 0.14), 0.08, flat('#2a3a4a', 0.6), 12, r1=0.07)
    for (gx, gy, a) in ((0.32, 0.95, 0.4), (0.42, 0.85, 1.2)):
        gl = MB(); blob(gl, (0, 0, 0.02), 0.09, 0.05, 0.025, flat('#c8a060', 0.85), 10, 5, r, 0.2); go = gl.obj('room_glove', G['coll']); go.location = (gx, gy, 0); go.rotation_euler = (0, 0, a); S.no_bounce(go)
    cyl(pm, (0.2, 1.08, 0), (0.2, 1.08, 0.008), 0.09, flat('#9a9a9a'), 14)
    coil = [Vector((0.2 + 0.07 * (1 - t / 18) * math.cos(t * 0.75), 1.08 + 0.07 * (1 - t / 18) * math.sin(t * 0.75), 0.014)) for t in range(18)]
    tube(pm, coil, 0.004, flat('#3a5a2a', 0.8), 4); blob(G['bulb'], tuple(coil[0]), 0.005, 0.005, 0.005, M['coil_tip'], 6, 4, flat_bottom=False)
    for k in range(3): cyl(pm, (-1.3 + k * 0.2, 0.3, 0), (-1.3 + k * 0.2, 0.3, 0.32), 0.08, flat('#a8d0e8', 0.7), 14)
    return dict(sit_mark=(0.66, 1.72, 0.0), sit_seat_z=mz, table_top=dict(x=(tx0, tx1), y=(ty0, ty1), z=tz), paybook=(0.02, 1.68, round(tz + 0.007, 3)),
                mattress=dict(x=(mx0, mx1), y=(my0, my1), z=mz))

# ----------------------------------------------------------------------------- outside: the corridor and the city
def corridor(G, r):
    mb, pm, al = G['corr'], G['props'], G['alpha']; xa, xb = -8.0, 8.0; d = DOOR
    F(mb, [(xa, Y1 + WT, 0), (xb, Y1 + WT, 0), (xb, CY + 0.15, 0), (xa, CY + 0.15, 0)], M['corr_floor'], [(0, 0), (1, 0), (1, (CY + 0.15 - Y1 - WT) / 2), (0, (CY + 0.15 - Y1 - WT) / 2)], (0, 0, 1))
    F(mb, [(xa, Y1 + WT, H), (xb, Y1 + WT, H), (xb, CY + 0.3, H), (xa, CY + 0.3, H)], flat('#b8b4a8', 0.8), None, (0, 0, -1))
    mb.box((xa, CY + 0.15, H), (xb, CY + 0.3, H + 0.25), M['concrete'])
    wall_holes(mb, (xb, Y1 + WT, 0), (-1, 0, 0), (0, 0, 1), xb - xa, H, M['wall_out'], [(xb - d['x1'], xb - d['x0'], -1, d['z1'])], (0, 1, 0))
    # parapet + steel railing, columns
    mb.box((xa, CY, 0), (xb, CY + 0.15, 0.92), M['parapet'], tile=(16, 2.6)); mb.box((xa, CY - 0.02, 0.92), (xb, CY + 0.17, 0.96), flat('#8a8a80', 0.85))
    st = flat('#3a4a5a', 0.85)
    tube(mb, [(xa, CY + 0.07, 1.12), (xb, CY + 0.07, 1.12)], 0.022, st, 8)
    for k in range(int((xb - xa) / 0.12)):
        xx = xa + 0.06 + k * 0.12; mb.box((xx - 0.008, CY + 0.06, 0.96), (xx + 0.008, CY + 0.08, 1.12), st)
    for xx in (-5.6, 5.6): mb.box((xx - 0.15, CY - 0.05, 0), (xx + 0.15, CY + 0.2, H), M['parapet'], tile=(0.3, 2.6))
    # neighbours' doors (205 left, 207 right, 204 far left), shoes, mats
    for (x0, cell) in ((-4.2, 1), (3.4, 2), (-7.6, 0)):
        F(mb, [(x0 + 0.78, Y1 + WT + 0.01, 0.02), (x0, Y1 + WT + 0.01, 0.02), (x0, Y1 + WT + 0.01, 2.0), (x0 + 0.78, Y1 + WT + 0.01, 2.0)], M['doors'],
          [(cell / 3, 0), ((cell + 1) / 3, 0), ((cell + 1) / 3, 1), (cell / 3, 1)], (0, 1, 0))
        for (a, b, c_, e) in ((x0 - 0.06, x0, 0, 2.06), (x0 + 0.78, x0 + 0.84, 0, 2.06), (x0 - 0.06, x0 + 0.84, 2.0, 2.06)): mb.box((a, Y1 + WT, c_), (b, Y1 + WT + 0.03, e), flat('#5a4a3a'))
    def shoe_pair(x, y, cell, a=0.0, s=0.27):
        sh = MB(); rect(sh, (0, 0, 0), (s / 2, 0, 0), (0, s / 2, 0), M['shoes'], (cell * 0.25, 0.0, cell * 0.25 + 0.25, 1.0)); so = sh.obj('room_shoes', G['coll'])
        so.location = (x, y, 0.012); so.rotation_euler = (0, 0, a); S.no_bounce(so)
    shoe_pair(0.68, 4.42, 1, 0.3); shoe_pair(-0.62, 4.38, 0, -0.2); shoe_pair(0.95, 4.75, 3, 1.4)
    shoe_pair(3.7, 4.4, 2, 0.1); shoe_pair(4.25, 4.45, 3, -0.3); shoe_pair(-3.9, 4.4, 0, 0.2); shoe_pair(-7.3, 4.35, 2, 0.0)
    pm.box((-1.05, Y1 + WT, 0), (-0.7, Y1 + WT + 0.28, 0.75), flat('#5a5e64', 0.85))                     # small shoe shelf left of our door
    for z in (0.25, 0.5): pm.box((-1.05, Y1 + WT, z), (-0.7, Y1 + WT + 0.28, z + 0.015), flat('#3a3e44'))
    blob(pm, (-0.88, Y1 + 0.26, 0.6), 0.1, 0.08, 0.06, flat('#e83a2a', 0.85), 10, 5, r, 0.2)
    rect(mb, (1.15, Y1 + WT + 0.005, 1.55), (-0.1, 0, 0), (0, 0, 0.125), M['meter'], n=(0, 1, 0)); pm.box((1.04, Y1 + WT, 1.42), (1.26, Y1 + WT + 0.1, 1.68), flat('#c8c8c0'))
    tube(pm, [(1.15, Y1 + WT + 0.05, 1.68), (1.15, Y1 + WT + 0.05, H)], 0.012, M['conduit'], 6)
    tube(pm, [(xa, Y1 + WT + 0.04, 2.45), (xb, Y1 + WT + 0.04, 2.45)], 0.02, flat('#7a8a8a', 0.85), 8)          # water pipe along the wall
    # pots on the parapet, towel over the railing, broom, bag of rubbish
    for xx in (-2.2, -1.6, 1.9, 2.6, 6.4):
        cyl(pm, (xx, CY + 0.07, 0.96), (xx, CY + 0.07, 1.16), 0.09, flat(r.choice(['#a85a3a', '#3a6ab0', '#e8e4d8'])), 12, r1=0.11)
        for k in range(3):
            a = k * 1.05 + r.uniform(0, 1); rect(al, (xx + 0.12 * math.cos(a), CY + 0.07 + 0.12 * math.sin(a), 1.35), (0.16 * math.cos(a + 1.57), 0.16 * math.sin(a + 1.57), 0), (0, 0, 0.2), flat('#3a8a3a', 0.85))
    F(al, [(-0.6, CY + 0.05, 1.13), (-0.05, CY + 0.05, 1.13), (-0.05, CY + 0.0, 0.62), (-0.6, CY + 0.0, 0.6)], M['clothes'], [(0.755, 0.35), (0.995, 0.35), (0.995, 0.98), (0.755, 0.98)], (0, -1, 0))
    F(al, [(-0.6, CY + 0.09, 1.13), (-0.05, CY + 0.09, 1.13), (-0.05, CY + 0.14, 0.62), (-0.6, CY + 0.14, 0.6)], M['clothes'], [(0.755, 0.35), (0.995, 0.35), (0.995, 0.98), (0.755, 0.98)], (0, 1, 0))
    tube(pm, [(1.55, Y1 + 0.2, 0.02), (1.62, Y1 + 0.18, 1.2)], 0.012, flat('#d83a2a'), 5); pm.frustum((1.55, Y1 + 0.2, 0.0), (1.555, Y1 + 0.2, 0.22), 0.1, 0.03, flat('#c8a060'), seg=10)
    blob(pm, (2.3, Y1 + 0.35, 0.18), 0.2, 0.17, 0.2, flat('#1e1e22', 0.6), 12, 6, r, 0.25)
    # a folding laundry rack by the parapet (in the doorway view, behind whoever stands there)
    for xx in (-0.7, 0.75):
        for s_ in (-1, 1): tube(pm, [(xx, 5.2 + s_ * 0.25, 0), (xx, 5.2 - s_ * 0.05, 1.3)], 0.008, M['chrome'], 4)
    for zz, dy in ((1.3, 0.0), (1.1, -0.1), (1.1, 0.1)): tube(pm, [(-0.7, 5.2 + dy, zz), (0.75, 5.2 + dy, zz)], 0.006, M['chrome'], 4)
    for k, (x0_, cell, w_) in enumerate(((-0.62, 2, 0.34), (-0.22, 0, 0.36), (0.18, 3, 0.3), (0.5, 1, 0.24))):
        rect(al, (x0_ + w_ / 2, 5.2 + (k % 2) * 0.06 - 0.03, 1.3 - 0.36), (w_ / 2, 0, 0), (0, 0, 0.36), M['clothes'], (cell * 0.25 + 0.01, 0.12, cell * 0.25 + 0.24, 0.98), (0, -1, 0))
    # the corridor tube: batten on two chains, cold tube, a few moths; and a second one far down the corridor (dimmer, for depth)
    for (cx, cy, cz) in ((0.35, 5.05, 2.27), (-5.0, 5.05, 2.3)):
        pm.box((cx - 0.64, cy - 0.04, cz + 0.02), (cx + 0.64, cy + 0.04, cz + 0.06), M['white'])
        cyl(pm, (cx - 0.6, cy, cz), (cx + 0.6, cy, cz), 0.014, M['corr_tube'], 10)
        for s_ in (-1, 1): bx(pm, (cx + s_ * 0.62 - 0.015, cy - 0.02, cz - 0.015), (cx + s_ * 0.62 + 0.015, cy + 0.02, cz + 0.03), M['white'])
        for s_ in (-0.45, 0.45): tube(pm, [(cx + s_, cy, cz + 0.06), (cx + s_, cy, H)], 0.003, M['chrome'], 3)
    for k in range(9):
        p = Vector((0.35 + r.uniform(-0.7, 0.7), 5.05 + r.uniform(-0.3, 0.3), 2.2 + r.uniform(-0.3, 0.3))); blob(pm, tuple(p), 0.012, 0.006, 0.004, flat('#5a4a3a'), 6, 3, flat_bottom=False)
    # city backdrops (camera-only: no shadows, not lighting anything)
    bd = MB(); F(bd, [(-22, 22, -9), (22, 22, -9), (22, 22, 13), (-22, 22, 13)], M['city_far'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    F(bd, [(4.6, 8.0, -3.0), (4.6, -1.0, -3.0), (4.6, -1.0, 6.0), (4.6, 8.0, 6.0)], M['city_win'], [(0, 0), (1, 0), (1, 1), (0, 1)], (-1, 0, 0))
    ob = bd.obj('room_backdrops', G['coll']); ob.visible_shadow = False; S.no_bounce(ob)

# ----------------------------------------------------------------------------- lights
def lights(lc):
    b = P['bulb']; TL.point(lc, 'bulb', A['bulb'], b['color'], b['K'], b['d'], radius=0.018)
    c = P['corr']
    for (cx, kk) in ((0.35, 1.0), (-5.0, 0.6)):
        TL.area(lc, 'corridor_tube' if cx > 0 else 'corridor_tube2', (cx, 5.05, 2.25), (0, 0, -1), c['color'], c['K'] * kk, c['d'], size=1.2, size_y=0.05, practical=False)
    t = P['neon_teal']; o = P['neon_orange']
    p0, p1 = Vector((4.4, 4.3, 3.6)), Vector((0.35, 1.95, 0.0)); TL.spot(lc, 'neon_teal', tuple(p0), tuple(p1 - p0), t['color'], t['K'], (p1 - p0).length, 21, 0.35, 0.012, practical=False)
    p0, p1 = Vector((4.6, 0.9, 2.6)), Vector((-1.0, 3.9, 0.9)); TL.spot(lc, 'neon_orange', tuple(p0), tuple(p1 - p0), o['color'], o['K'], (p1 - p0).length, 18, 0.35, 0.012, practical=False)

def set_lights(on=True):
    """The bulb (light + glass + filament) on / off. The corridor tube and the neon outside belong to the building and the city: they stay on."""
    return TL.set_lights(on)

# ----------------------------------------------------------------------------- build
def build(preset='night', clear=True):
    scene = bpy.context.scene
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True); scene = bpy.context.scene
    P.clear(); P.update(PRESETS[preset]); S.STATE.clear(); S.STATE['P'] = P; M.clear(); A.clear(); OBJ.clear(); TL.reset()
    TX.clear(); TX.update(tex_room.build_all())
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    A['bulb'] = (0.05, 2.05, 2.075)
    materials(); r = random.Random(20261114)
    G = dict(coll=coll, shell=MB(), props=MB(), alpha=MB(), corr=MB(), bulb=MB())
    shell(G); A.update(furniture(G, r)); corridor(G, r); door_obj(G)
    for nm in ('shell', 'props', 'alpha', 'corr', 'bulb'): G[nm].obj('room_' + nm, coll)
    for ob in coll.objects: S.no_bounce(ob)
    bpy.data.objects['room_bulb'].visible_shadow = False
    lights(lc); set_door(0.0)
    w = bpy.data.worlds.new('room_world'); scene.world = w; w.use_nodes = True; bg = w.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value = (0, 0, 0, 1)
    S.setup_render(scene, 'fast'); scene.cycles.samples = 12; scene.cycles.use_light_tree = True; scene.render.use_persistent_data = False; S.setup_grade(scene, bloom=True)
    bl = Vector(A['bulb']); sm = Vector(A['sit_mark']) + Vector((0, 0, 0.7))
    A.update(door_inside_mark=(1.08, 3.2, 0.0), doorway_mark=(0.05, 4.45, 0.0), door_hinge=(DOOR['hinge'][0], DOOR['hinge'][1], 0.0),
             sit_face=(-1.0, 0.0, 0.0), door_inside_face=(-0.6, 0.8, 0.0), doorway_face=(0.0, -1.0, 0.0), corridor_light=(0.35, 5.05, 2.25),
             door_opening=dict(x=(DOOR['x0'] + 0.05, DOOR['x1'] - 0.05), z=(0.0, DOOR['z1'] - 0.05), y=Y1), window=dict(x=X1, y=(WIN['y0'], WIN['y1']), z=(WIN['z0'], WIN['z1'])),
             room=dict(x=(X0, X1), y=(Y0, Y1), ceiling=H, wall_t=WT, corridor_y=(Y1 + WT, CY)),
             key_dir=tuple(round(v, 4) for v in (sm - bl).normalized()), key_note='point light: shadows radiate from A["bulb"]; key_dir = bulb -> sit_mark chest',
             preset=preset, cams=CAMS, cams_16x9=CAMS_16x9, units=1.0, door_angle=0.0)
    return A

CAMS = dict(
    room_wide=dict(loc=(-1.38, 0.18, 1.66), look_at=(0.40, 2.85, 0.32), lens=15),
    fist_close=dict(loc=(-1.08, 1.42, 0.95), look_at=(0.66, 1.84, 0.82), lens=36),
    door_pov=dict(loc=(1.5, 1.68, 1.6), look_at=(-0.08, 4.6, 1.12), lens=22, door=80),
    door_closed=dict(loc=(1.5, 1.68, 1.6), look_at=(-0.08, 4.6, 1.12), lens=22, door=0),
)
CAMS_16x9 = dict(room_wide=dict(loc=(-1.4, 0.16, 1.7), look_at=(0.55, 2.75, 0.62), lens=17))

def render_cam(name, path, res=(720, 1280), cam=None):
    scene = bpy.context.scene; scene.render.resolution_x, scene.render.resolution_y = res; scene.render.resolution_percentage = 100
    c = cam or CAMS[name]; set_door(c.get('door', 0)); S.make_camera(c, name='cam'); return S.render(path)

if __name__ == '__main__':
    args = sys.argv[1:]; cmd = args[0] if args else 'stills'
    preset = args[1] if len(args) > 1 and args[1] in PRESETS else 'night'
    rest = [a for a in args[1:] if a not in PRESETS]
    q = 'preview' if 'preview' in rest else 'final'; cams = [a for a in rest if a in CAMS] or list(CAMS)
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); build(preset); tb = time.time() - t0; scene = bpy.context.scene
    tag = '' if preset == 'night' else '_' + preset; times = {}
    if cmd == 'stills':
        if q == 'preview': scene.cycles.samples = 6
        for c in cams:
            res = (720, 1280) if q == 'final' else (360, 640)
            w, cpu = render_cam(c, os.path.join(OUT, f'{c}{tag}.png'), res); times[c] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(c, times[c], flush=True)
    elif cmd == 'land':
        w, cpu = render_cam('room_wide', os.path.join(OUT, f'room_wide_16x9{tag}.png'), (1920, 1080), CAMS_16x9['room_wide']); times['room_wide_16x9'] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(times, flush=True)
    jp = os.path.join(OUT, 'timing.json'); old = json.load(open(jp)) if os.path.exists(jp) else {}
    old.update({f'{k}{tag}': dict(v, samples=scene.cycles.samples, quality=q, build_s=round(tb, 1)) for k, v in times.items()}); json.dump(old, open(jp, 'w'), indent=1)
    json.dump({k: v for k, v in A.items()}, open(os.path.join(OUT, f'anchors{tag}.json'), 'w'), indent=1, default=str)
