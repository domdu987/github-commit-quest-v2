#!/usr/bin/env python3
"""vault.py : the gunpowder vault under San Nazaro (Brescia, 1769) as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import vault as V
    A = V.build("LANTERN")                       # collections SET and LIGHTS, world, render settings, grade -> anchors dict
    V.set_crack_glow(0.4)                        # fire glow runs along the crack from the stair (0) to the barrels (1)
    cam = V.make_camera(A["cams"]["dolly_barrels"])

World: 1 unit = 1 D (head diameter), Z up, floor z = 0, back wall (stair end) = plane y = 0, the vault runs toward -y
(front wall y = -12), x = 0 = vault axis, +x to the right for a viewer looking toward the back wall.
CLI: python3 vault.py stills [preview|final] | timing | digest | ratio
See vault_API.md."""
import os, sys, math, random, json, time
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'small_work'))
import smallkit as K                                         # noqa: E402
make_camera = K.make_camera; setup_render = K.setup_render; placeholder_actor = K.placeholder_actor; no_bounce = K.no_bounce

# ----------------------------------------------------------------------------- dimensions (D)
XW = 3.0                      # side walls at x = -XW and +XW
Y0, Y1 = -12.0, 0.0           # front wall, back wall
ZS, ZC = 2.0, 4.4             # springing line, crown (segmental barrel vault)
R_V = (XW ** 2 + (ZC - ZS) ** 2) / (2 * (ZC - ZS)); ZO = ZC - R_V        # arc radius 3.075, centre height 1.325
PHI0 = math.asin(XW / R_V)
HOLE = dict(x0=0.8, x1=XW, y0=-4.5, y1=0.0)                # stairwell opening in the vault
ZTOP = 8.0                                                  # top of the stair shaft
STAIR = dict(x0=1.55, x1=XW, n=15, rise=0.30, tread=0.45)  # stair rising toward the back wall (+y)
LANTERN = (0.15, -7.2, 2.75)                                # light centre of the hanging lantern
BURN_POS = (-1.0, -6.7, 3.0)                                # the fire glow under the crack (BURN key)
SOLDIER_MARK = (-1.05, -9.1, 0.0)
AISLE_MARK = (0.55, -10.2, 0.0)
INK = '#2a1712'

def vault_z(x):
    return ZO + math.sqrt(max(R_V ** 2 - x * x, 0.0))

# ----------------------------------------------------------------------------- presets
PRESETS = {
    'LANTERN': dict(key_type='POINT', key_pos=LANTERN, key=(1.9, 2.5, 0.05), key_falloff=2.6, key_radius=0.025,
                    shade=(0.15, 0.28, 1.14), shade_desat=0.85, lift=(0.006, 0.008, 0.030), form=(0.0, 0.0, 0.10),
                    amb_center=(LANTERN, 4.5, 0.94), amb_z=(2.6, 5.5, 0.85), pools=[(LANTERN, (0.30, 0.15, 0.04), 0.9)], flash_col=(0.55, 0.30, 0.08),
                    pane=4.0, glow=0.0, bloom_size=0.06, grade_offset=(0.003, 0.003, 0.012), grade_saturation=1.12),
    'BURN': dict(key_type='POINT', key_pos=BURN_POS, key=(3.0, 1.15, 0.22), key_falloff=2.6, key_radius=0.08,
                 shade=(0.10, 0.06, 0.24), shade_desat=0.6, lift=(0.016, 0.006, 0.020), form=(0.0, 0.0, 0.10),
                 amb_center=(BURN_POS, 9.0, 0.5), pools=[(LANTERN, (0.22, 0.11, 0.03), 0.9), (BURN_POS, (0.55, 0.16, 0.03), 1.3)],
                 flash_col=(0.85, 0.32, 0.06), pane=4.0, glow=1.0, bloom_size=0.10, bloom_strength=0.7, grade_offset=(0.004, 0.002, 0.008), grade_saturation=1.0),
}
STATE = {}

# ----------------------------------------------------------------------------- textures
def _brick_tile(base_cols, mortar, name, TW=1.2, TH=0.6, ppd=420):
    r = random.Random(11); o = []; ch = TH / 5; bl = 0.4; mt = 0.014
    cols = [r.choice(base_cols) for _ in range(15)]
    for j in range(5):
        off = (j % 2) * 0.2; y = j * ch
        for k in range(-1, 4):
            x = off + k * bl; c = cols[(j * 3 + (k % 3)) % 15]
            o.append(f'<rect x="{x + mt:.4f}" y="{y + mt:.4f}" width="{bl - 2 * mt:.4f}" height="{ch - 2 * mt:.4f}" fill="{c}" rx="0.008"/>')
            o.append(f'<line x1="{x + mt:.4f}" y1="{y + mt + 0.006:.4f}" x2="{x + bl - mt:.4f}" y2="{y + mt + 0.006:.4f}" stroke="{K.mulc(c, 1.16)}" stroke-width="0.008"/>')
            o.append(f'<line x1="{x + mt:.4f}" y1="{y + ch - mt - 0.005:.4f}" x2="{x + bl - mt:.4f}" y2="{y + ch - mt - 0.005:.4f}" stroke="{K.mulc(c, 0.74)}" stroke-width="0.007"/>')
            rr = random.Random(j * 7 + (k % 3))
            for _ in range(2):
                px = x + mt + rr.uniform(0.04, bl - 0.06); py = y + mt + rr.uniform(0.02, ch - 0.04)
                o.append(f'<circle cx="{px:.4f}" cy="{py:.4f}" r="{rr.uniform(0.006, 0.012):.4f}" fill="{K.mulc(c, 0.8)}"/>')
    return name, (K.svg_doc(int(TW * ppd), int(TH * ppd), TW, TH, ''.join(o), bg=mortar), int(TW * ppd), int(TH * ppd), False)

def _flags(name, TW=2.4, ppd=260):
    r = random.Random(5); o = []; cols = ['#a87448', '#9c6a42', '#b07e50', '#986440', '#b4845a']; joint = '#4a2c22'
    rows = [0.0, 0.85, 1.6, 2.4]
    for j in range(3):
        y0, y1 = rows[j], rows[j + 1]; x = r.uniform(0, 0.4); xs = []
        while x < TW + 0.01: xs.append(x); x += r.uniform(0.6, 1.0)
        xs = [v % TW for v in xs]; xs.sort()
        cuts = xs + [xs[0] + TW]
        for i in range(len(xs)):
            a, b = cuts[i], cuts[i + 1]; c = r.choice(cols)
            for sh in (-TW, 0.0, TW):
                o.append(f'<rect x="{a + sh + 0.02:.3f}" y="{y0 + 0.02:.3f}" width="{b - a - 0.04:.3f}" height="{y1 - y0 - 0.04:.3f}" fill="{c}" stroke="{joint}" stroke-width="0.02" rx="0.04"/>')
                o.append(f'<path d="M{a + sh + 0.12:.3f},{y0 + 0.1:.3f} q0.2,0.08 0.35,0.02" stroke="{K.mulc(c, 0.8)}" stroke-width="0.012" fill="none"/>')
    return name, (K.svg_doc(int(TW * ppd), int(TW * ppd), TW, TW, ''.join(o), bg=joint), int(TW * ppd), int(TW * ppd), False)

def _stone(name, ppd=300):
    o = []; c = '#a07c5c'
    o.append(f'<rect x="0" y="0" width="1" height="1" fill="{c}"/>')
    r = random.Random(3)
    for _ in range(14):
        x, y = r.uniform(0, 1), r.uniform(0, 1); o.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r.uniform(0.01, 0.025):.3f}" fill="{K.mulc(c, 0.82)}"/>')
    o.append(f'<path d="M0.1,0.3 l0.15,0.05 l0.1,-0.04" stroke="{K.mulc(c, 0.65)}" stroke-width="0.012" fill="none"/>')
    o.append(f'<rect x="0" y="0" width="1" height="0.05" fill="{K.mulc(c, 1.15)}"/>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _staves(name, n=16, ppd=512):
    o = []; cols = ['#ac6232', '#9c5a2e', '#b46c38', '#a46030']
    for i in range(n):
        x = i / n; c = cols[i % 4]
        o.append(f'<rect x="{x:.4f}" y="0" width="{1 / n:.4f}" height="1" fill="{c}"/>')
        r = random.Random(i)
        for g in range(3):
            gx = x + r.uniform(0.15, 0.85) / n
            o.append(f'<path d="M{gx:.4f},0 Q{gx + 0.008:.4f},0.5 {gx:.4f},1" stroke="{K.mulc(c, 0.8)}" stroke-width="0.0025" fill="none"/>')
        o.append(f'<line x1="{x:.4f}" y1="0" x2="{x:.4f}" y2="1" stroke="#4a2414" stroke-width="0.004"/>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _head(name, stencil=True, ppd=512):
    """Barrel head: boards, a dark rim, and the army stencil (two crossed cannons over three balls), with stencil bridges."""
    o = ['<rect x="0" y="0" width="1" height="1" fill="#b47c40"/>']
    for j, c in enumerate(['#b47c40', '#a8703a', '#bc8446', '#aa723c', '#b47c40']):
        o.append(f'<rect x="0" y="{j * 0.2:.2f}" width="1" height="0.2" fill="{c}"/><line x1="0" y1="{j * 0.2:.2f}" x2="1" y2="{j * 0.2:.2f}" stroke="#4a2414" stroke-width="0.006"/>')
    o.append('<circle cx="0.5" cy="0.5" r="0.47" fill="none" stroke="#5a2c18" stroke-width="0.05"/>')
    o.append('<circle cx="0.5" cy="0.5" r="0.43" fill="none" stroke="#c4884c" stroke-width="0.008"/>')
    if stencil:
        ink = '#1b1216'; g = []
        for ang in (-38, 38):
            # cannon barrel: tapered tube with muzzle ring and cascabel, pointing up
            g.append(f'<g transform="rotate({ang} 0.5 0.52)"><path d="M0.468,0.83 L0.476,0.24 L0.524,0.24 L0.532,0.83 Z" fill="{ink}"/>'
                     f'<rect x="0.462" y="0.22" width="0.076" height="0.035" fill="{ink}"/><circle cx="0.5" cy="0.86" r="0.032" fill="{ink}"/>'
                     f'<rect x="0.45" y="0.58" width="0.1" height="0.022" fill="{ink}"/></g>')
        for (cx, cy) in ((0.44, 0.79), (0.56, 0.79), (0.5, 0.72)):
            g.append(f'<circle cx="{cx}" cy="{cy}" r="0.042" fill="{ink}"/>')
        o.append('<g opacity="0.93">' + ''.join(g) + '</g>')
        for (x1, y1, x2, y2) in ((0.3, 0.47, 0.7, 0.47), (0.36, 0.66, 0.64, 0.66)):          # stencil bridges
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#a46a36" stroke-width="0.012"/>')
        o.append(f'<text x="0.5" y="0.2" font-family="Georgia, serif" font-size="0.085" font-weight="700" text-anchor="middle" fill="{ink}" opacity="0.9" letter-spacing="0.01">R·A</text>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _burlap(name, ppd=400):
    o = ['<rect x="0" y="0" width="1" height="1" fill="#b48a58"/>']
    for i in range(24):
        v = i / 24; o.append(f'<line x1="0" y1="{v:.4f}" x2="1" y2="{v:.4f}" stroke="#94703f" stroke-width="0.008"/><line x1="{v:.4f}" y1="0" x2="{v:.4f}" y2="1" stroke="#c49a66" stroke-width="0.006"/>')
    o.append('<path d="M0.2,0.4 l0.3,0.04 l0.25,-0.03" stroke="#6e4a28" stroke-width="0.014" fill="none"/>')
    o.append('<text x="0.5" y="0.7" font-family="Georgia, serif" font-size="0.16" font-weight="700" text-anchor="middle" fill="#3a2418" opacity="0.75">S</text>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _door(name, w=1.6, h=2.7, ppd=300):
    o = [f'<path d="M0,{h} L0,{w / 2} A{w / 2},{w / 2} 0 0 1 {w},{w / 2} L{w},{h} Z" fill="#6a3a20" stroke="#2a1712" stroke-width="0.04"/>']
    for i in range(1, 6):
        x = i * w / 6; o.append(f'<line x1="{x:.3f}" y1="{h}" x2="{x:.3f}" y2="0.1" stroke="#3e2014" stroke-width="0.02"/>')
    for y in (0.95, 1.9):
        o.append(f'<rect x="0.02" y="{y}" width="{w - 0.04}" height="0.1" fill="#3a3640" stroke="#1d1418" stroke-width="0.012"/>')
        for i in range(7): o.append(f'<circle cx="{0.12 + i * (w - 0.24) / 6:.3f}" cy="{y + 0.05}" r="0.022" fill="#7a7480"/>')
    o.append(f'<circle cx="{w * 0.8:.3f}" cy="1.5" r="0.07" fill="none" stroke="#2a2630" stroke-width="0.025"/>')
    return name, (K.svg_doc(int(w * ppd), int(h * ppd), w, h, ''.join(o)), int(w * ppd), int(h * ppd), True)

def textures():
    jobs = dict([_brick_tile(['#d08e4c', '#c05c3c', '#cc8448', '#b8543a', '#c88a4c', '#c8784a'], '#6a4030', 'v_brick'),
                 _flags('v_floor'), _stone('v_stone'), _staves('v_staves'), _head('v_head'), _head('v_head_plain', stencil=False),
                 _burlap('v_burlap'), _door('v_door')])
    return K.raster(jobs)

# ----------------------------------------------------------------------------- crack path
CRACK_WAY = [(0.86, -4.55), (0.42, -4.95), (0.05, -5.15), (-0.32, -5.55), (-0.62, -5.75), (-1.05, -6.15), (-1.5, -6.32),
             (-1.95, -6.72), (-2.35, -6.92), (-2.68, -7.18), (-2.9, -7.42)]

def crack_points(n_sub=6):
    r = random.Random(17); pts = []
    for i in range(len(CRACK_WAY) - 1):
        (xa, ya), (xb, yb) = CRACK_WAY[i], CRACK_WAY[i + 1]; dx, dy = xb - xa, yb - ya; L = math.hypot(dx, dy); px, py = -dy / L, dx / L
        for k in range(n_sub):
            t = k / n_sub; j = 0.0 if (k == 0) else r.uniform(-0.05, 0.05)
            pts.append((xa + dx * t + px * j, ya + dy * t + py * j))
    pts.append(CRACK_WAY[-1])
    out = []
    for (x, y) in pts:                                       # onto the vault surface, 0.012 D proud (radially inward)
        z = vault_z(x); v = Vector((x, 0, z - ZO)); v = v * ((v.length - 0.012) / v.length)
        out.append((round(v.x, 5), round(y, 5), round(v.z + ZO, 5)))
    return out

def crack_point(u):
    """World point at fraction u (0 = stair end, 1 = barrels) of the crack, by arc length."""
    pts = STATE['crack']; Ls = [0.0]
    for a, b in zip(pts, pts[1:]): Ls.append(Ls[-1] + math.dist(a, b))
    s = max(0.0, min(1.0, u)) * Ls[-1]
    for i in range(len(pts) - 1):
        if Ls[i + 1] >= s:
            t = (s - Ls[i]) / max(Ls[i + 1] - Ls[i], 1e-9); return tuple(pts[i][k] + (pts[i + 1][k] - pts[i][k]) * t for k in range(3))
    return pts[-1]

def _curve(name, pts, radius, mat, coll):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts): p.co = (*c, 1.0)
    cu.bevel_mode = 'ROUND'; cu.bevel_depth = radius; cu.bevel_resolution = 2; cu.use_fill_caps = True
    cu.bevel_factor_mapping_start = 'SPLINE'; cu.bevel_factor_mapping_end = 'SPLINE'
    cu.materials.append(mat); ob = bpy.data.objects.new(name, cu); coll.objects.link(ob); ob.visible_shadow = False
    return ob

# ----------------------------------------------------------------------------- geometry helpers
def _barrel(mb, c, axis, M, L=1.0, r_end=0.34, r_mid=0.42, seg=16, rings=8, stencil_end=1):
    """Lathe barrel along axis 'x' or 'z' centred at c; stencil on the +axis end if stencil_end = 1, on the -axis end if -1."""
    c = Vector(c); a = Vector((1, 0, 0)) if axis == 'x' else Vector((0, 0, 1))
    u = Vector((0, 1, 0)) if axis == 'x' else Vector((1, 0, 0)); v = a.cross(u)
    rad = lambda t: r_end + (r_mid - r_end) * (1 - (2 * t - 1) ** 2)
    ring = lambda t, rr: [c + a * (L * (t - 0.5)) + rr * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg)]
    mb.pid += 1
    R = [ring(k / rings, rad(k / rings)) for k in range(rings + 1)]
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; q = [R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]]
            ctr = sum(q, Vector()) / 4; rv = ctr - (c + a * a.dot(ctr - c)); nrm = (q[1] - q[0]).cross(q[3] - q[0])
            uvs = [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)]
            if nrm.dot(rv) < 0: q = q[::-1]; uvs = uvs[::-1]
            mb.face(q, M['staves'], uvs)
    for end, t in ((1, 1.0), (-1, 0.0)):                     # heads: viewer-right / up mapping so the stencil reads upright
        n = a * end; right = (-n).cross(Vector((0, 0, 1))) if axis == 'x' else Vector((1, 0, 0)); up = Vector((0, 0, 1)) if axis == 'x' else n.cross(right).normalized() * -1
        if axis == 'z': up = Vector((0, 1, 0)) if end == 1 else Vector((0, -1, 0)); right = up.cross(n)
        ctr = c + a * (L * (t - 0.5)); rr = r_end; pts = []; uvs = []
        for i in range(seg):
            th = 2 * math.pi * i / seg; pts.append(ctr + rr * (math.cos(th) * right + math.sin(th) * up)); uvs.append((0.5 + 0.5 * math.cos(th), 0.5 + 0.5 * math.sin(th)))
        if (pts[1] - pts[0]).cross(pts[2] - pts[0]).dot(n) < 0: pts = pts[::-1]; uvs = uvs[::-1]
        mb.pid += 1; mb.face(pts, M['head'] if end == stencil_end else M['head_plain'], uvs)
    for t in (0.1, 0.27, 0.73, 0.9):                        # iron hoops
        rr = rad(t) + 0.012; p0 = c + a * (L * (t - 0.5) - 0.025); p1 = c + a * (L * (t - 0.5) + 0.025)
        mb.pid += 1; A0 = [p0 + rr * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg)]
        A1 = [p1 + rr * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg)]
        for i in range(seg):
            j = (i + 1) % seg; q = [A0[i], A0[j], A1[j], A1[i]]; ctr = sum(q, Vector()) / 4; rv = ctr - (c + a * a.dot(ctr - c))
            if (q[1] - q[0]).cross(q[3] - q[0]).dot(rv) < 0: q = q[::-1]
            mb.face(q, M['hoop'])

def _sack(mb, c, s, mat, seed):
    r = random.Random(seed); c = Vector(c); seg, rings = 12, 7; R = []
    rx, ry, rz = 0.42 * s, 0.34 * s, 0.5 * s
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; w = 1 + 0.08 * math.sin(3 * ph + seed) + r.uniform(-0.03, 0.03)
            sq = 1.0 - 0.45 * max(0, math.cos(th)) ** 3      # flattened bottom
            pz = -rz * math.cos(th) * sq; top = max(0.0, -math.cos(th)) ** 4 * 0.5    # neck pulled in toward the tie
            p = c + Vector((rx * math.sin(th) * math.cos(ph) * w * (1 - top), ry * math.sin(th) * math.sin(ph) * w * (1 - top), pz + rz * 0.55))
            p.z = max(p.z, c.z); row.append(p)
        R.append(row)
    mb.pid += 1
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; q = [R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]]
            ctr = sum(q, Vector()) / 4; nrm = (q[1] - q[0]).cross(q[3] - q[0])
            if nrm.length < 1e-9: continue
            uvs = [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)]
            if nrm.dot(ctr - (c + Vector((0, 0, rz * 0.55)))) < 0: q = q[::-1]; uvs = uvs[::-1]
            mb.face(q, mat, uvs)
    top = c + Vector((0, 0, rz * 0.55 + rz * 0.98)); mb.frustum(top - Vector((0, 0, 0.05)), top + Vector((0.02, 0, 0.14 * s)), 0.07 * s, 0.1 * s, mat, seg=8)

# ----------------------------------------------------------------------------- build
def build(preset='LANTERN', clear=True):
    """Build the vault into the current scene. Returns the anchors dict."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear: K.reset_scene(scene, 'VAULT_')
    SET = K.coll('SET', scene); LIGHTS = K.coll('LIGHTS', scene)
    for c_ in (SET, LIGHTS):
        for ob in list(c_.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for m in list(bpy.data.materials):
        if m.name.startswith(('VAULT_', 'SM_ink_')): bpy.data.materials.remove(m)
    K.setup_render(scene, 'final'); K.build_groups(P, 'VAULT_' + preset)
    tx = textures(); pre = 'VAULT_%s_' % preset
    def C(h, gain=1.0, sm=1.0): return K.mat_lit('%sc_%s_%g_%s' % (pre, h.lstrip('#'), gain, sm), h, gain=gain, shade_mul=sm)
    def TX(n, gain=1.0, sm=1.0, alpha=False): return K.mat_lit('%st_%s_%g_%s' % (pre, n, gain, sm), image=tx[n], gain=gain, shade_mul=sm, alpha=alpha)
    def E(h, s): return K.mat_emit('%se_%s_%g' % (pre, h.lstrip('#'), s), h, strength=s)
    M = dict(brick=TX('v_brick', 0.68, 1.0), floor=TX('v_floor', 0.8, 1.15), stone=TX('v_stone', 0.6, 1.0), staves=TX('v_staves', 0.7, 1.0),
             head=TX('v_head', 0.66, 1.0), head_plain=TX('v_head_plain', 0.66, 1.0), hoop=C('#3c3644', 0.8, 1.3), burlap=TX('v_burlap', 0.55, 1.0),
             wood=C('#6e3a20', 0.7, 1.0), iron=C('#2e2a36', 0.8, 1.2), door=TX('v_door', 0.6, 1.0, alpha=True),
             pane=E('#ffcf7a', P['pane']), shaft_top=C('#3a3050', 1.0, 1.0))
    ink = INK

    # ---- vault shell: walls + segmental barrel vault (one profile swept along y), floor, end walls, stair shaft
    seg_arc = 28; prof = [(-XW, 0.0, 0.0)]                   # (x, z, arc length s)
    prof.append((-XW, ZS, ZS))
    s = ZS
    for i in range(1, seg_arc + 1):
        ph = -PHI0 + 2 * PHI0 * i / seg_arc; x = R_V * math.sin(ph); z = ZO + R_V * math.cos(ph); s += math.dist(prof[-1][:2], (x, z)); prof.append((x, z, s))
    prof.append((XW, 0.0, s + ZS)); TW, TH = 1.2, 0.6
    STATE['profile'] = prof
    mb = K.MB(); ny = 24; hole_x_edge = None
    for j in range(ny):
        ya, yb = Y0 + (Y1 - Y0) * j / ny, Y0 + (Y1 - Y0) * (j + 1) / ny
        for i in range(len(prof) - 1):
            (xa, za, sa), (xb, zb, sb) = prof[i], prof[i + 1]
            inhole = (min(xa, xb) >= HOLE['x0'] - 1e-6 and 0 < i < len(prof) - 2 and ya >= HOLE['y0'] - 1e-6)
            if inhole: continue
            # inward-facing quad: the profile runs left wall up, over the vault, down the right wall: (b - a) x (+y) points inward
            mb.pid += 1; mb.face([(xa, yb, za), (xb, yb, zb), (xb, ya, zb), (xa, ya, za)], M['brick'], [(yb / TW, sa / TH), (yb / TW, sb / TH), (ya / TW, sb / TH), (ya / TW, sa / TH)])
    K.obj(mb, 'vault_shell', SET)
    hole_pts = [(x, z) for (x, z, s_) in prof[1:-1] if x >= HOLE['x0'] - 1e-6]
    STATE['hole_edge_x'] = hole_pts[0][0]
    # end walls: lunette at the back (y = 0, faces -y) and the front (y = -12, faces +y)
    for (y, face_dir) in ((Y1, -1), (Y0, 1)):
        pts = [(x, y, z) for (x, z, s_) in prof]
        uvs = [(x / TW, z / TH) for (x, z, s_) in prof]
        if face_dir == -1: pts = pts[::-1]; uvs = uvs[::-1]
        mb = K.MB(); mb.face(pts, M['brick'], uvs); K.obj(mb, 'wall_back' if y == Y1 else 'wall_front', SET)
    # stair shaft walls above the opening
    mb = K.MB(); xe = STATE['hole_edge_x']; ze = vault_z(xe)
    mb.quad((xe, Y1, ze), (0, HOLE['y0'] - Y1, 0), (0, 0, ZTOP - ze), M['brick'], (0, ze / TH, -HOLE['y0'] / TW, ZTOP / TH))         # left shaft wall, faces +x
    mb.quad((XW, HOLE['y0'], ZS), (0, Y1 - HOLE['y0'], 0), (0, 0, ZTOP - ZS), M['brick'], (0, ZS / TH, -HOLE['y0'] / TW, ZTOP / TH))   # right shaft wall, faces -x
    for (xa, za), (xb, zb) in zip(hole_pts, hole_pts[1:]):
        mb.pid += 1; mb.face([(xa, HOLE['y0'], za), (xa, HOLE['y0'], ZTOP), (xb, HOLE['y0'], ZTOP), (xb, HOLE['y0'], zb)], M['brick'],
                             [(xa / TW, za / TH), (xa / TW, ZTOP / TH), (xb / TW, ZTOP / TH), (xb / TW, zb / TH)])       # front shaft wall, faces +y
        mb.pid += 1; mb.face([(xa, Y1, za), (xb, Y1, zb), (xb, Y1, ZTOP), (xa, Y1, ZTOP)], M['brick'],
                             [(xa / TW, za / TH), (xb / TW, zb / TH), (xb / TW, ZTOP / TH), (xa / TW, ZTOP / TH)])       # back shaft wall, faces -y
    mb.quad((xe, HOLE['y0'], ZTOP), (XW - xe, 0, 0), (0, Y1 - HOLE['y0'], 0), M['shaft_top'])
    K.obj(mb, 'stair_shaft', SET)
    # floor
    mb = K.MB(); mb.quad((-XW, Y0, 0), (2 * XW, 0, 0), (0, Y1 - Y0, 0), M['floor'], (-XW / 2.4, Y0 / 2.4, XW / 2.4, Y1 / 2.4)); K.obj(mb, 'floor', SET)

    # ---- the stone stair (solid steps against the back wall, rising toward +y along the right wall)
    st = STAIR; mb = K.MB(); y_start = -st['n'] * st['tread']
    for i in range(st['n']):
        y0 = y_start + i * st['tread']; zt = st['rise'] * (i + 1)
        mb.box((st['x0'], y0, 0.0), (st['x1'] - 0.001, Y1 - 0.001, zt), M['stone'], skip='back,right,left,bottom')
        mb.quad((st['x0'], y0, 0.0), (0, 0, zt), (0, st['tread'], 0), M['stone'], (y0, 0, y0 + st['tread'], zt))    # stringer seen from the aisle, faces -x
    K.obj(mb, 'stair', SET, hull=K.hull_t(5.0), ink=ink)
    STATE['stair_y_start'] = y_start

    # ---- barrels: three pyramid stacks on the left, two on the right (lying, heads with the stencil toward the aisle), on wooden chocks
    barrels = []; sp = 0.86; zc0 = 0.12 + 0.42; dz = 0.73
    groups_left = [-11.4, -8.32, -5.24]; groups_right = [-11.4, -8.32]
    for side, groups in ((-1, groups_left), (1, groups_right)):
        xc = side * 2.4
        for gi, gy in enumerate(groups):
            n0 = 3 if not (side == 1 and gi == 1) else 2
            for row in range(n0):
                for k in range(n0 - row):
                    y = gy + sp * (k + 0.5 * row); barrels.append(dict(c=(xc, y, zc0 + dz * row), axis='x', end=-side, side=side, row=row))
    standing = [dict(c=(0.95, -10.9, 0.5), axis='z', end=1, side=0, row=0), dict(c=(-0.55, -11.35, 0.5), axis='z', end=1, side=0, row=0)]
    mb = K.MB()
    for b in barrels + standing: _barrel(mb, b['c'], b['axis'], M, stencil_end=b['end'])
    K.obj(mb, 'barrels', SET, hull=K.hull_t(5.0), ink=ink)
    mb = K.MB()
    for side, groups in ((-1, groups_left), (1, groups_right)):
        for gx in (2.05, 2.75):
            mb.box((side * gx - 0.08, -11.95, 0.0), (side * gx + 0.08, groups[-1] + 2 * sp + 0.45 if side == -1 else -6.9, 0.12), M['wood'])
    K.obj(mb, 'chocks', SET, hull=K.hull_t(4.0), ink=ink)
    STATE['barrels'] = barrels
    # sacks of powder / shot
    mb = K.MB()
    for i, (x, y, s_) in enumerate(((1.35, -9.0, 0.8), (1.0, -8.55, 0.7), (-1.55, -11.4, 0.85), (0.4, -11.6, 0.75), (1.25, -6.3, 0.7))):
        _sack(mb, (x, y, 0.0), s_, M['burlap'], i + 3)
    K.obj(mb, 'sacks', SET, hull=K.hull_t(4.0), ink=ink)
    # front wall door (barred, the way the army brings the powder in)
    mb = K.MB(); mb.quad((-0.8, Y0 + 0.02, 0.0), (1.6, 0, 0), (0, 0, 2.7), M['door'], (0, 0, 1, 1)); K.obj(mb, 'door', SET)
    mb = K.MB(); mb.box((-0.95, Y0, 0.0), (-0.8, Y0 + 0.12, 1.9), M['stone']); mb.box((0.8, Y0, 0.0), (0.95, Y0 + 0.12, 1.9), M['stone'])
    K.obj(mb, 'door_jambs', SET, hull=0.02, ink=ink)
    # iron rings in the walls and a tie rod across the vault (density)
    mb = K.MB()
    for y in (-3.0, -6.7, -9.8):
        mb.frustum((-XW, y, 1.55), (-XW + 0.08, y, 1.55), 0.02, 0.02, M['iron'], seg=6)
        mb.frustum((XW, y - 0.6, 1.55), (XW - 0.08, y - 0.6, 1.55), 0.02, 0.02, M['iron'], seg=6)
    mb.frustum((-XW, -9.6, 2.05), (XW, -9.6, 2.05), 0.035, 0.035, M['iron'], seg=8)
    K.obj(mb, 'ironwork', SET, hull=0.012, ink=ink)

    # ---- the lantern (hanging from the crown; the light sits inside it; the lantern casts no shadow)
    lx, ly, lz = LANTERN; mb = K.MB(); w = 0.17
    mb.frustum((lx, ly, lz + 0.24), (lx, ly, vault_z(lx) + 0.05), 0.012, 0.012, M['iron'], seg=6)
    mb.frustum((lx, ly, lz + 0.2), (lx, ly, lz + 0.34), 0.2, 0.03, M['iron'], seg=12)
    mb.box((lx - w - 0.02, ly - w - 0.02, lz - 0.26), (lx + w + 0.02, ly + w + 0.02, lz - 0.21), M['iron'])
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box((lx + sx * w - 0.018, ly + sy * w - 0.018, lz - 0.21), (lx + sx * w + 0.018, ly + sy * w + 0.018, lz + 0.2), M['iron'])
    lo = K.obj(mb, 'lantern', SET, hull=0.008, ink=ink, shadow=False)
    mb = K.MB(); mb.box((lx - w + 0.01, ly - w + 0.01, lz - 0.2), (lx + w - 0.01, ly + w - 0.01, lz + 0.19), M['pane'])
    pn = K.obj(mb, 'lantern_glass', SET, shadow=False)

    # ---- crack (dark, always) + glow (orange emission, grows from the stair end with set_crack_glow)
    STATE['crack'] = crack_points()
    _curve('crack_dark', STATE['crack'], 0.016, K.mat_emit(pre + 'crack_ink', '#1a0f12', strength=1.0), SET)
    glow = _curve('crack_glow', STATE['crack'], 0.03, E('#ff5a10', 1.6), SET)
    ctl = bpy.data.objects.new('crack_ctl', None); SET.objects.link(ctl); ctl['glow'] = 0.0; ctl.hide_render = True
    fc = glow.data.driver_add('bevel_factor_end'); d = fc.driver; d.type = 'SCRIPTED'
    var = d.variables.new(); var.name = 'glow'; var.type = 'SINGLE_PROP'; var.targets[0].id = ctl; var.targets[0].data_path = '["glow"]'; d.expression = 'glow'
    STATE['crack_ctl'] = ctl; STATE['glow_ob'] = glow

    # ---- key light, grade, bounce rays off
    K.add_key(P, LIGHTS); K.setup_grade(scene, P)
    for ob in SET.objects: no_bounce(ob)
    set_crack_glow(P.get('glow', 0.0))
    A = anchors(); STATE['A'] = A
    return A

def set_crack_glow(u, frame=None):
    """Light the crack from the stair end (0) to fraction u (1 = at the barrels) with the orange glow; frame=N keyframes it (linear)."""
    u = max(0.0, min(1.0, float(u))); ctl = STATE['crack_ctl']; ctl['glow'] = u
    STATE['glow_ob'].data.bevel_factor_end = u; STATE['glow_ob'].hide_render = (u <= 1e-4 and frame is None)
    if frame is not None:
        STATE['glow_ob'].hide_render = False
        ctl.keyframe_insert('["glow"]', frame=frame)
        for fc in S_fcurves(ctl):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    ctl.update_tag()

def S_fcurves(idb):
    return K.S._fcurves(idb)

def flash(strength, frame=None):
    """Light pulse: the key's energy x (1 + strength) and the ambient flash term = strength (orange). frame=N keyframes both;
    call flash(0, N + 3) to come back."""
    key = K.ST['key']; base = K.ST['key_energy']; key.data.energy = base * (1.0 + strength)
    if frame is not None: key.data.keyframe_insert('energy', frame=frame)
    K.set_flash(0.6 * strength, frame)

def burn_pulse(f0, f1, period=7, depth=0.35, seed=3):
    """BURN: deterministic flicker of the fire light between frames f0 and f1 (keys every period/2 frames)."""
    r = random.Random(seed); f = f0
    while f <= f1:
        flash(r.uniform(-depth, depth), f); f += max(1, period // 2)

def anchors():
    P = STATE['P']; bs = STATE['barrels']
    ins = [b for b in bs if b['side'] == -1 and b['row'] == 1][2]          # middle group, second row, left stack
    head_c = (ins['c'][0] + 0.5, ins['c'][1], ins['c'][2])
    cams = dict(
        dolly_barrels=dict(loc=(-0.45, -3.2, 0.95), look_at=(-2.2, -7.4, 1.35), lens=22,
                           move=dict(loc=(-0.45, -6.4, 0.95), look_at=(-2.2, -10.6, 1.35), note='dolly 3.2 D toward -y along the left barrel rows')),
        stair_high=dict(loc=(1.3, -2.3, 4.3), look_at=(-0.5, -10.8, 0.2), lens=22),
        barrel_insert=dict(loc=(head_c[0] + 0.95, head_c[1] + 0.32, head_c[2] + 0.12), look_at=head_c, lens=22),
        crack_follow=dict(loc=(0.95, -3.5, 2.05), look_at=(-2.5, -7.6, 2.55), lens=22),
    )
    return dict(
        vault=dict(x_left=-XW, x_right=XW, y_front=Y0, y_back=Y1, springing=ZS, crown=ZC, arc_radius=round(R_V, 4), arc_centre_z=round(ZO, 4)),
        hole=dict(HOLE, x_edge=round(STATE['hole_edge_x'], 4), z_top=ZTOP),
        stair=dict(x0=STAIR['x0'], x1=STAIR['x1'], y_bottom=STATE['stair_y_start'], y_top=Y1, steps=STAIR['n'], rise=STAIR['rise'], tread=STAIR['tread'],
                   top=(2.27, -0.2, STAIR['rise'] * STAIR['n']), foot=(2.27, STATE['stair_y_start'] - 0.3, 0.0)),
        lantern=LANTERN, burn_light=BURN_POS, key_pos=tuple(P['key_pos']),
        crack_path=list(STATE['crack']), crack_start=STATE['crack'][0], crack_end=STATE['crack'][-1],
        barrels=[dict(c=b['c'], axis=b['axis'], side=b['side'], row=b['row']) for b in bs], stencil_insert=head_c, stencil_normal=(1.0, 0.0, 0.0),
        soldier_mark=SOLDIER_MARK, aisle_mark=AISLE_MARK,
        cams=cams,
        cam_notes=dict(dolly_barrels='low (0.95 D), runs 3.2 D along the left barrel rows (cams[...]["move"] = end pose)',
                       stair_high='from the head of the stair in the opening, 4.55 D high, down the whole vault to the barred door',
                       barrel_insert='1 D from a barrel head: the crossed-cannon stencil fills the frame width',
                       crack_follow='from under the stair opening along the crack toward the left barrel stack'),
        render=dict(preset=STATE['preset'], samples=12, resolution=(720, 1280), key=P['key'], key_type=P['key_type'], shade=P['shade']))

# ----------------------------------------------------------------------------- CLI
def stage(A, cam_name):
    K.clear_actors()
    cs = A['cams'][cam_name]
    if cam_name == 'barrel_insert': return
    placeholder_actor('boss', dict(yaw=-0.3, expr='neutral', arm_l='down', arm_r='hip', legs='stand'), A['soldier_mark'], face_to=cs['loc'], name='actor_soldier')
    if cam_name in ('stair_high', 'dolly_barrels'):
        placeholder_actor('hero', dict(yaw=0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), A['aisle_mark'], face_to=cs['loc'], name='actor_boy', scale=0.8)

def cli_stills(quality='preview', outdir=None, presets=('LANTERN', 'BURN')):
    outdir = outdir or os.path.join(HERE, 'small_work', 'stills'); os.makedirs(outdir, exist_ok=True)
    for pr in presets:
        A = build(pr); sc = bpy.context.scene; setup_render(sc, quality)
        if pr == 'LANTERN': set_crack_glow(0.0)
        for nm, cs in A['cams'].items():
            if pr == 'BURN' and nm == 'crack_follow': set_crack_glow(0.65)
            make_camera(cs); stage(A, nm)
            w, c = K.render(os.path.join(outdir, 'vault_%s_%s.png' % (pr, nm))); print('vault %s %s: %.1f s wall %.1f s cpu' % (pr, nm, w, c), flush=True)
            set_crack_glow(P_glow(pr))

def P_glow(pr): return PRESETS[pr].get('glow', 0.0)

def cli_timing(n=3, preset='LANTERN', cam='dolly_barrels'):
    A = build(preset); sc = bpy.context.scene; setup_render(sc, 'final'); cs = A['cams'][cam]; c = make_camera(cs); stage(A, cam)
    res = []
    for i in range(n):
        c.location.y -= 0.03; w, cp = K.render(os.path.join(HERE, 'small_work', 'timing_vault_%d.png' % i)); res.append((w, cp)); print('frame %d: %.2f s wall %.2f s cpu' % (i, w, cp), flush=True)
    print('TIMING vault %s %s: cpu median %.2f s, wall median %.2f s (720x1280, %d samples, %d threads)' % (preset, cam, sorted(r[1] for r in res)[n // 2], sorted(r[0] for r in res)[n // 2], sc.cycles.samples, sc.render.threads))

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else 'stills'
    if cmd == 'stills': cli_stills(a[1] if len(a) > 1 else 'preview', presets=tuple(a[2].split(',')) if len(a) > 2 else ('LANTERN', 'BURN'))
    elif cmd == 'timing': cli_timing(preset=a[1] if len(a) > 1 else 'LANTERN', cam=a[2] if len(a) > 2 else 'dolly_barrels')
    elif cmd == 'digest': build(a[1] if len(a) > 1 else 'LANTERN'); print('DIGEST', K.digest())
    else: print(__doc__)
