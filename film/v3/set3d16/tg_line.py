"""tg_line.py : LINE location of set3d16 (Maryland countryside beside an 1840s railway), grown from styleboard/sb.py (sb1 + sb3).
Authored in the sb frame (metres, +y along the road / rail / pole line, +x right, z up); telegraph_kit.W() turns it into world D
(rotated -90 deg about z: the line runs along world +x, camera-right of sb1 is world -y)."""
import telegraph_kit as K
from telegraph_kit import *

TX = -7.0                                   # rail x
POLE_H = 5.0; BS = 2.3                      # pole height (m), bottle scale
NPOLE = 16
POLES_Y = [4.0 + 9.0 * k for k in range(NPOLE)]
Y0, Y1 = 2.0, 62.0                          # furrow start / end (y, m)
PIT = (52.0, 12.0)                          # cut-away pit centre (x, y)
PIT_HW, PIT_HL, PIT_D = 0.85, 7.0, 1.25     # pit half width, half length, depth
LS = 1.6                                    # train scale
LY0 = 27.0                                  # loco origin y at x-param 0
WAGON = (xc(56) - 2.6, 56.0)                # wagon centre (x, y), long axis along y
KEYCRATE = (xc(Y1 + 2.5) + 2.2, Y1 + 2.5)   # test key crate on the ground at the furrow end
PLAT = (-4.4, 34.0, 62.0)                   # station platform: x edge (towards the rail), y0, y1
SAG = 0.55

def px(y): return xc(y) + 3.4

# ----------------------------------------------------------------------------- ground (with a hole for the pit)
def ground_mat():
    if 'ground' in MATS: return MATS['ground']
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord')
    def noise(sc_, det):
        n = N('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = sc_ / SC; n.inputs['Detail'].default_value = det; L(tc.outputs['Object'], n.inputs[0]); return n
    def ramp(n, a, b):
        r = N('ShaderNodeValToRGB'); L(n.outputs['Fac'], r.inputs[0]); r.color_ramp.elements[0].position = a; r.color_ramp.elements[1].position = b; return r
    c1 = N('ShaderNodeMix'); c1.data_type = 'RGBA'; c1.inputs[6].default_value = hexc('#c4a244'); c1.inputs[7].default_value = hexc('#8aa83a'); L(ramp(noise(0.06, 5), 0.4, 0.6).outputs[0], c1.inputs[0])
    c2 = N('ShaderNodeMix'); c2.data_type = 'RGBA'; L(c1.outputs[2], c2.inputs[6]); c2.inputs[7].default_value = hexc('#b07a38'); L(ramp(noise(0.5, 6), 0.45, 0.62).outputs[0], c2.inputs[0])
    c3 = N('ShaderNodeMix'); c3.data_type = 'RGBA'; c3.blend_type = 'MULTIPLY'; c3.inputs[0].default_value = 0.8; L(c2.outputs[2], c3.inputs[6])
    r3 = ramp(noise(5.0, 6), 0.35, 0.65); r3.color_ramp.elements[0].color = (0.75, 0.75, 0.75, 1); r3.color_ramp.elements[1].color = (1.12, 1.12, 1.12, 1); L(r3.outputs[0], c3.inputs[7])
    wn = wet_out(nt); dk = N('ShaderNodeMix'); dk.data_type = 'RGBA'; dk.blend_type = 'MULTIPLY'; dk.inputs[7].default_value = (0.52, 0.4, 0.42, 1.0); L(wn, dk.inputs[0]); L(c3.outputs[2], dk.inputs[6])
    L(dk.outputs[2], bs.inputs['Base Color'])
    rm = N('ShaderNodeMath'); rm.operation = 'MULTIPLY_ADD'; rm.inputs[1].default_value = -0.65; rm.inputs[2].default_value = 1.0; L(wn, rm.inputs[0]); L(rm.outputs[0], bs.inputs['Roughness'])
    sm = N('ShaderNodeMath'); sm.operation = 'MULTIPLY'; sm.inputs[1].default_value = 0.5; L(wn, sm.inputs[0]); L(sm.outputs[0], bs.inputs['Specular IOR Level'])
    L(bs.outputs[0], out.inputs['Surface']); MATS['ground'] = m; return m

def ground(hole=None, size=700.0, z=0.0):
    mb = MB('ground'); g = ground_mat(); S_ = size
    if hole is None: pieces = [(-S_, -S_, S_, S_)]
    else:
        a, b, c, d = hole; pieces = [(-S_, -S_, a, S_), (c, -S_, S_, S_), (a, -S_, c, b), (a, d, c, S_)]
    for (x0, y0, x1, y1) in pieces: mb.quad(g, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)][::-1])
    return mb.finish()

# ----------------------------------------------------------------------------- sky ring: hills + clouds all around
def hills_ring(P):
    mb = MB('hills'); rr = rnd(3); mats = []
    for li, (r, bh, amp) in enumerate([(250, 8, 16), (310, 20, 28), (380, 34, 30)]):
        m = mat_emit('hill%d' % li, '#9a9ad2', 1.0); mats.append(m); n = 180; ph = [rr.uniform(0, 6) for _ in range(4)]
        for i in range(n):
            a0 = 2 * math.pi * i / n; a1 = 2 * math.pi * (i + 1) / n
            def hh(a): return bh + amp * (0.5 * math.sin(a * 3 + ph[0]) + 0.3 * math.sin(a * 7 + ph[1]) + 0.15 * math.sin(a * 17 + ph[2]))
            p0 = (r * math.cos(a0), r * math.sin(a0)); p1 = (r * math.cos(a1), r * math.sin(a1))
            mb.quad(m, [(p0[0], p0[1], -5), (p1[0], p1[1], -5), (p1[0], p1[1], hh(a1)), (p0[0], p0[1], hh(a0))])
    mb.finish(); return mats

def cloud_mat(kd):
    m = bpy.data.materials.new('cloudG'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); gm = N('ShaderNodeNewGeometry'); vm = N('ShaderNodeVectorMath'); vm.operation = 'DOT_PRODUCT'
    vm.name = 'cdot'; vm.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(gm.outputs['Normal'], vm.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -0.35; mr.inputs['From Max'].default_value = 0.45; L(vm.outputs['Value'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.name = 'cmix'; mx.inputs[6].default_value = hexc('#7c84d8'); mx.inputs[7].default_value = hexc('#ffeacc'); L(mr.outputs['Result'], mx.inputs[0])
    em.name = 'cem'; em.inputs['Strength'].default_value = 1.0; L(mx.outputs[2], em.inputs['Color']); L(em.outputs[0], out.inputs['Surface']); MATS['cloudG'] = m; return m

def clouds(kd_world, ncloud=14, zr=(40, 130), scale=0.5, seed=9):
    """kd in WORLD (D) direction so the sky puffs shade like sb: cloud normals are world normals."""
    mb = MB('clouds'); rr = rnd(seed); a = cloud_mat(kd_world)
    for i in range(ncloud):
        ang = rr.uniform(0, 6.283); rad = rr.uniform(300, 420); cx = rad * math.cos(ang); cy = rad * math.sin(ang)
        cz = rr.uniform(*zr); sz = rr.uniform(25, 55) * (1.0 + cz / 160.0) * scale; tx_ = -math.sin(ang); ty_ = math.cos(ang)
        for j in range(rr.randint(4, 7)):
            ox = rr.uniform(-1.4, 1.4) * sz; oz = rr.uniform(0, 0.35) * sz
            mb.ell(a, (cx + tx_ * ox, cy + ty_ * ox, cz + oz - 0.25 * sz), (sz * rr.uniform(0.6, 1.0), sz * 0.5, sz * 0.32), (18, 10), (0, 0, ang))
            mb.ell(a, (cx + tx_ * ox, cy + ty_ * ox, cz + oz), (sz * rr.uniform(0.5, 0.9), sz * 0.45, sz * 0.27), (14, 8), (0, 0, ang))
    mb.finish(shadow=False); return a

# ----------------------------------------------------------------------------- poles
def pole_body(mb, M, x, y, h):
    mb.rod(M['pole'], (x, y, -0.2), (x + 0.03, y, h), 0.14, 0.085, 10, smooth=True)
    mb.cyl(M['polecut'], (x + 0.03, y, h + 0.02), 0.085, 0.04, 'z', 10)

def pole_peg(mb, M, x, y, h, bs):
    mb.rod(M['wood'], (x + 0.03, y, h), (x + 0.03, y, h + 0.14 * bs), 0.03 * bs / 2, 0.026 * bs / 2, 6)
    bottle(mb, M, (x + 0.03, y, h + 0.01), bs)

def span(a, b, sag, n=None):
    L = math.hypot(b[0] - a[0], b[1] - a[1]); n = n or max(6, int(L / 0.6))
    return [wire_pt(a, b, i / n, sag) for i in range(n + 1)]

def build_poles(ST, M):
    top_b = []; top_n = []
    P = ST['poles'] = []; SB = ST['spans_bottle'] = []; SN = ST['spans_bare'] = []
    for i, y in enumerate(POLES_Y):
        x = px(y)
        mb = MB('pole%d' % i); pole_body(mb, M, x, y, POLE_H); body = mb.finish()
        mb = MB('peg%d' % i); pole_peg(mb, M, x, y, POLE_H, BS); peg = mb.finish()
        P.append(dict(body=body, peg=peg, x=x + 0.03, y=y))
        top_b.append((x + 0.03, y, POLE_H + 0.255 * BS + 0.012)); top_n.append((x + 0.03, y, POLE_H + 0.06))
    rb = rnd(4); birds = {(1, 0.35), (1, 0.5), (2, 0.6), (3, 0.3), (3, 0.38), (4, 0.5), (6, 0.4), (7, 0.55), (9, 0.3)}
    ST['wire_pts'] = {}
    for nm, tops, store in (('bottle', top_b, SB), ('bare', top_n, SN)):
        pts_all = []
        for i in range(NPOLE - 1):
            a, b = tops[i], tops[i + 1]; mb = MB('wire%s%d' % (nm[0], i)); pts = span(a, b, SAG, 12)
            for p, q in zip(pts[:-1], pts[1:]): mb.rod(M['wiremat'], p, q, 0.03, 0.03, 5, caps=False)
            for (bi, u) in birds:
                if bi == i:
                    p = wire_pt(a, b, u, SAG); mb.ell(M['bird'], (p[0], p[1], p[2] + 0.12), (0.1, 0.18, 0.1), (8, 5)); mb.ell(M['bird'], (p[0], p[1] - 0.15, p[2] + 0.2), (0.06, 0.06, 0.06), (6, 4))
            store.append(mb.finish()); pts_all += pts if i == 0 else pts[1:]
        ST['wire_pts'][nm] = pts_all
    for nm in ('bottle', 'bare'):                           # cumulative arc length for the pulse bead
        pts = ST['wire_pts'][nm]; cum = [0.0]
        for p, q in zip(pts[:-1], pts[1:]): cum.append(cum[-1] + (Vector(q) - Vector(p)).length)
        ST['wire_pts'][nm] = (pts, cum)

# ----------------------------------------------------------------------------- props
def beer_bottle(mb, M, c, s=1.8, yaw=0.0):
    """upright green beer bottle (body + shoulder + neck + lip), s scales the real 0.3 m bottle (film bottles are oversize)"""
    x, y, z = c; G = M['glass']
    prof = [(0.037, 0.0), (0.037, 0.12), (0.034, 0.15), (0.02, 0.19), (0.0155, 0.22), (0.0155, 0.27), (0.019, 0.275), (0.019, 0.29), (0.0155, 0.295)]
    for (r0, z0), (r1, z1) in zip(prof[:-1], prof[1:]): mb.rod(G, (x, y, z + z0 * s), (x, y, z + z1 * s), r0 * s, r1 * s, 12, caps=False, smooth=True)
    mb.cyl(G, (x, y, z), 0.037 * s, 0.01 * s, 'z', 12); mb.cyl(M['gold'], (x, y, z + 0.298 * s), 0.014 * s, 0.006 * s, 'z', 10) if False else None

def bottle_crate(mb, M, c, yaw=0.0, nb=(5, 3), s=1.8):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    w, d, h = nb[0] * 0.095 * s * 0.55 + 0.1, nb[1] * 0.095 * s * 0.55 + 0.1, 0.26 * s * 0.8
    for sx in (-1, 1): mb.box(M['woodpale'], (sx * w / 2, 0, h / 2), (0.04, d, h))
    for sy in (-1, 1): mb.box(M['woodpale'], (0, sy * d / 2, h / 2), (w, 0.04, h))
    mb.box(M['wood'], (0, 0, 0.03), (w, d, 0.04))
    for i in range(nb[0]):
        for j in range(nb[1]):
            bx = -w / 2 + 0.07 + i * (w - 0.14) / max(1, nb[0] - 1); by = -d / 2 + 0.07 + j * (d - 0.14) / max(1, nb[1] - 1)
            beer_bottle(mb, M, (bx, by, 0.05), s)
    mb.pop()

def key_station(mb, M, c, yaw=0.0):
    """test key + paper-tape register on a crate (sb: telegraph kit, tidy), at the furrow end"""
    crate(mb, M, c, (1.1, 0.8, 0.6), yaw)
    mb.push(Matrix.Translation((c[0], c[1], c[2] + 0.6)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['walnut'], (0, 0, 0.02), (1.0, 0.7, 0.04)); mb.box(M['brass'], (-0.28, 0.1, 0.07), (0.26, 0.2, 0.03))
    for sy in (-0.07, 0.07): mb.cyl(M['copper'], (-0.28, 0.1 + sy, 0.16), 0.055, 0.16, 'z', 14, True)
    mb.box(M['metal'], (-0.28, 0.1, 0.26), (0.08, 0.24, 0.02))
    mb.box(M['brass'], (0.2, -0.2, 0.06), (0.22, 0.08, 0.03)); mb.rod(M['brass'], (0.12, -0.2, 0.1), (0.3, -0.2, 0.15), 0.012, 0.012, 6); mb.ell(M['dark'], (0.31, -0.2, 0.16), (0.035, 0.035, 0.03), (10, 6))
    mb.box(M['wood'], (0.15, 0.15, 0.1), (0.34, 0.24, 0.12)); mb.cyl(M['paper'], (0.08, 0.15, 0.24), 0.09, 0.12, 'y', 18)
    mb.box(M['paper'], (0.36, 0.15, 0.17), (0.2, 0.07, 0.005), ry=-0.2)
    mb.pop()

def reel(mb, M, c, r=0.62, wide=0.7):
    """drum of lead pipe on its side (axis y): flanges + wound lead"""
    x, y, z = c
    for sy in (-1, 1): mb.cyl(M['woodpale'], (x, y + sy * (wide / 2 + 0.05), z), r * 1.2, 0.1, 'y', 22)
    mb.cyl(M['lead'], (x, y, z), r, wide, 'y', 22, True); mb.cyl(M['wood'], (x, y, z), 0.12, wide + 0.3, 'y', 10)
    for k in range(5): mb.cyl(M['lead'], (x, y - wide / 2 + (k + 0.5) * wide / 5, z), r * 1.05, 0.03, 'y', 22)

def wagon2(mb, M, c, yaw=0.0):
    """supply wagon, long axis x: spool at the front, crate of empty beer bottles in the middle, key crate at the tail"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.95), (4.4, 1.6, 0.12))
    for sy in (-1, 1): mb.box(M['wood'], (0, sy * 0.8, 1.25), (4.4, 0.07, 0.5))
    for sx in (-1, 1): mb.box(M['wood'], (sx * 2.2, 0, 1.25), (0.07, 1.6, 0.5))
    for sx in (-1.4, 1.5):
        mb.box(M['wood'], (sx, 0, 0.8), (0.12, 1.9, 0.12))
        for sy in (-1, 1): wheel(mb, M, (sx, sy * 0.95, 0.62 if sx < 0 else 0.5), 0.62 if sx < 0 else 0.5)
    mb.rod(M['wood'], (2.2, 0, 0.85), (5.0, 0, 0.45), 0.06, 0.05, 6)
    z0 = 1.95
    for sy in (-0.52, 0.52): mb.cyl(M['woodpale'], (1.2, sy, z0 - 0.1), 0.85, 0.1, 'y', 24)
    mb.cyl(M['spool'], (1.2, 0, z0 - 0.1), 0.66, 0.96, 'y', 24, True); mb.cyl(M['wood'], (1.2, 0, z0 - 0.1), 0.15, 1.3, 'y', 10)
    mb.rod(M['wiremat'], (1.2, -0.3, z0 - 0.1 + 0.66), (1.9, -0.3, 1.1), 0.02, 0.02, 4)
    bottle_crate(mb, M, (-0.35, 0.0, 1.01), 0.0, (5, 3), 1.8)
    key_station(mb, M, (-1.55, 0.0, 1.01), 0.0)
    mb.pop()

def plough(mb, M):
    """Cornell's trench plough at the origin, travelling +y: beam, share, coulter, two handles, whiffletree + chain"""
    mb.rod(M['wood'], (0, -0.3, 0.9), (0, 2.4, 0.75), 0.07, 0.06, 6)                                  # beam
    mb.box(M['metal'], (0, 0.2, 0.35), (0.07, 0.9, 0.7), rx=0.2)                                      # coulter / body
    mb.box(M['metal'], (0.0, 0.6, 0.1), (0.5, 0.6, 0.05), rx=-0.3)                                    # share
    for sx in (-0.3, 0.3): mb.rod(M['wood'], (sx * 0.2, -0.2, 0.5), (sx, -1.5, 1.15), 0.04, 0.035, 6)      # handles
    mb.rod(M['wood'], (-0.3, -1.5, 1.15), (0.3, -1.5, 1.15), 0.03, 0.03, 5)
    mb.rod(M['wood'], (-0.9, 2.4, 0.75), (0.9, 2.4, 0.75), 0.05, 0.05, 6)                              # whiffletree
    for sx in (-0.9, 0.9): mb.rod(M['metal'], (sx, 2.4, 0.75), (sx * 1.1, 4.0, 0.9), 0.015, 0.015, 4)       # traces to the mules
    mb.cyl(M['metal'], (0, 0.5, 0.55), 0.18, 0.06, 'x', 12)                                            # small wheel

def buggy(mb, M, wheels):
    """open 1840s buggy at the origin heading +y (parts that do not spin); wheels returned as (axle, r) for spinning objects"""
    mb.box(M['carriage'], (0, 0, 0.78), (1.2, 2.0, 0.34))                                              # lower body
    for sx in (-1, 1): mb.box(M['carriage'], (sx * 0.6, -0.1, 1.1), (0.06, 1.5, 0.36))               # low side panels
    mb.box(M['carriage2'], (0, 0.95, 1.12), (1.2, 0.06, 0.55), rx=-0.25)                              # dash front
    mb.box(M['leather'], (0, -0.35, 1.0), (1.0, 0.7, 0.14)); mb.box(M['leather'], (0, -0.72, 1.35), (1.0, 0.12, 0.6), rx=-0.15)   # seat + back
    mb.box(M['black'], (0, -0.1, 0.55), (0.08, 2.2, 0.08))
    for sy_ in (-0.7, 0.8): mb.box(M['metal'], (0, sy_, 0.55), (1.7, 0.1, 0.1))                          # axles
    for sx in (-1, 1): mb.rod(M['wood'], (sx * 0.38, 0.9, 0.7), (sx * 0.38, 3.6, 0.55), 0.045, 0.04, 6)       # shafts
    mb.rod(M['black'], (0, 0.55, 1.5), (0, 0.2, 1.7), 0.01, 0.01, 4) if False else None
    for sx in (-1, 1): mb.box(M['gold'], (sx * 0.64, 0.95, 1.0), (0.04, 0.04, 0.25))                     # lamp posts
    mb.box(M['woodpale'], (0.7, -0.1, 0.5), (0.2, 0.5, 0.04))                                           # step

def wheel_obj(M, name, axle, r, axis_x=True, spokes=10, parent=None, wide=0.07, tyre=True, hub=0.1):
    """a spinnable wheel (axis = sb x) at axle (sb metres); mesh local to the axle, object at W(axle). rotate about WORLD Y for the line."""
    mb = MB(name); mb.T = frame_mat() @ Matrix.Translation((0, 0, 0)) if False else frame_mat()
    # disc in the sb y-z plane
    mb.cyl(M['wood'], (0, 0, 0), hub, wide * 2.4, 'x', 10)
    for i in range(spokes):
        a = i * math.pi * 2 / spokes; mb.rod(M['wood'], (0, 0, 0), (0, math.cos(a) * r * 0.94, math.sin(a) * r * 0.94), wide * 0.55, wide * 0.4, 5)
    for i in range(16):
        a = i * math.pi * 2 / 16; b = (i + 1) * math.pi * 2 / 16
        mb.rod(M['red'], (0, math.cos(a) * r, math.sin(a) * r), (0, math.cos(b) * r, math.sin(b) * r), wide * 0.8, wide * 0.8, 5)
        if tyre: mb.rod(M['black'], (0, math.cos(a) * (r + 0.02), math.sin(a) * (r + 0.02)), (0, math.cos(b) * (r + 0.02), math.sin(b) * (r + 0.02)), wide * 0.6, wide * 0.6, 4)
    objs = mb.finish(); o = bpy.data.objects.new(name + '_axle', None); bpy.context.scene.collection.objects.link(o); o.location = W(axle)
    for ob in objs: ob.parent = o
    return o

# ----------------------------------------------------------------------------- train
def lc(lx, ly, lz): return (TX + ly * LS, LY0 - lx * LS, 0.2 + lz * LS)      # loco-local (x forward, y lateral, z) -> sb frame

def loco_static(mb, M):
    """sb loco without wheels / rods (they spin as separate objects)"""
    mb.push(Matrix.Translation((TX, LY0, 0.2)) @ Euler((0, 0, -math.pi / 2)).to_matrix().to_4x4() @ Matrix.Diagonal((LS, LS, LS, 1)))
    mb.box(M['black'], (0.4, 0, 0.95), (4.4, 1.5, 0.3))
    mb.cyl(M['green'], (0.8, 0, 1.75), 0.72, 3.2, 'x', 20, True)
    for bx in (-0.4, 0.6, 1.6): mb.cyl(M['brass'], (bx, 0, 1.75), 0.74, 0.08, 'x', 20)
    mb.cyl(M['black'], (2.5, 0, 1.75), 0.7, 0.6, 'x', 20, True); mb.cyl(M['black'], (2.82, 0, 1.75), 0.52, 0.06, 'x', 20); mb.cyl(M['brass'], (2.86, 0, 1.75), 0.26, 0.05, 'x', 14)
    mb.cyl(M['black'], (2.45, 0, 3.1), 0.2, 1.7, 'z', 14, True, r2=0.34); mb.cyl(M['brass'], (2.45, 0, 3.98), 0.37, 0.08, 'z', 14)
    mb.ell(M['brass'], (1.0, 0, 2.55), (0.32, 0.32, 0.4), (14, 10)); mb.cyl(M['brass'], (1.0, 0, 2.2), 0.14, 0.4, 'z', 10)
    mb.cyl(M['brass'], (1.8, 0, 2.58), 0.13, 0.5, 'z', 10); mb.ell(M['brass'], (1.8, 0, 2.86), (0.15, 0.15, 0.1), (8, 6))
    mb.box(M['red'], (-1.35, 0, 1.9), (1.4, 1.5, 1.6)); mb.box(M['red'], (-1.35, 0, 2.7), (1.7, 1.8, 0.14))
    mb.box(M['dark'], (-1.35, 0.76, 2.0), (0.8, 0.04, 0.6)); mb.box(M['dark'], (-1.35, -0.76, 2.0), (0.8, 0.04, 0.6))
    for sy in (-0.7, 0.7): mb.cyl(M['black'], (1.5, sy * 0.85, 1.05), 0.14, 1.0, 'x', 10)
    mb.box(M['black'], (3.1, 0, 0.7), (0.3, 1.9, 0.3))
    mb.cyl(M['brass'], (3.25, 0, 2.15), 0.18, 0.2, 'x', 10); mb.cyl(M['gold'], (3.37, 0, 2.15), 0.14, 0.04, 'x', 10)
    for i in range(7):
        yy = -0.85 + i * 0.283; mb.rod(M['black'], (3.1, yy * 0.8, 0.65), (4.1, yy * 1.05, 0.2), 0.045, 0.04, 5)
    mb.rod(M['black'], (3.1, -0.8, 0.62), (4.1, -0.9, 0.2), 0.05, 0.05, 5); mb.rod(M['black'], (3.1, 0.8, 0.62), (4.1, 0.9, 0.2), 0.05, 0.05, 5); mb.rod(M['black'], (4.1, -0.9, 0.2), (4.1, 0.9, 0.2), 0.05, 0.05, 5)
    mb.pop()

def carriage_static(mb, M, y, body):
    mb.push(Matrix.Translation((TX, y, 0.2)) @ Euler((0, 0, -math.pi / 2)).to_matrix().to_4x4() @ Matrix.Diagonal((LS, LS, LS, 1)))
    L_ = 5.4
    mb.box(M['black'], (0, 0, 0.8), (L_, 1.7, 0.25)); mb.box(M[body], (0, 0, 1.95), (L_, 2.2, 2.0)); mb.box(M['cream'], (0, 0, 1.2), (L_ + 0.04, 2.24, 0.12)); mb.box(M['cream'], (0, 0, 2.95), (L_ + 0.04, 2.24, 0.1))
    prism_roof(mb, M['dark'], -L_ / 2, L_ / 2, -1.1, 1.1, 3.0, 3.5, ov=0.15)
    for i in range(5):
        wx = -L_ / 2 + 0.7 + i * (L_ - 1.4) / 4
        for sy in (-1, 1): mb.box(M['dark'], (wx, sy * 1.11, 2.1), (0.7, 0.04, 0.8)); mb.box(M['cream'], (wx, sy * 1.12, 2.1), (0.82, 0.03, 0.92))
    mb.pop()

def build_train(ST, M):
    root = bpy.data.objects.new('train_root', None); bpy.context.scene.collection.objects.link(root); ST['train'] = T = dict(root=root, wheels=[], rods=[], puffs=[], hist=None)
    mb = MB('train'); loco_static(mb, M)
    cy = [LY0 + 7.2 * LS, LY0 + 13.4 * LS]; carriage_static(mb, M, cy[0], 'carriage'); carriage_static(mb, M, cy[1], 'carriage2')
    mb.rod(M['black'], (TX, LY0 + 3.6 * LS, 0.95), (TX, LY0 + 4.6 * LS, 0.95), 0.06, 0.06, 5); mb.rod(M['black'], (TX, LY0 + 9.9 * LS, 0.95), (TX, LY0 + 10.7 * LS, 0.95), 0.06, 0.06, 5)
    for ob in mb.finish(): ob.parent = root
    # wheels: (name, axle sb, radius m)
    ws = []
    for sy in (-0.7, 0.7):
        for wx in (-1.5, 0.1): ws.append((lc(wx, sy * 1.07, 0.7), 0.7 * LS))
        for wx in (1.5, 2.3): ws.append((lc(wx, sy * 1.07, 0.45), 0.45 * LS))
    for yy in cy:
        for sy in (-1, 1):
            for wx in (-1.8, 1.8): ws.append(((TX + sy * 0.95 * LS, yy - wx * LS * 0 + (wx * LS), 0.2 + 0.5 * LS), 0.5 * LS))
    for i, (ax, r) in enumerate(ws):
        o = wheel_obj(M, 'twheel%d' % i, ax, r, spokes=10, wide=0.07 * LS * 0.8)
        o.parent = root; T['wheels'].append((o, r))
    # connecting rods (both sides): rest position between the two drive wheels
    for k, sy in enumerate((-1, 1)):
        mb = MB('rod%d' % k); a = lc(-1.5, sy * 1.2, 0.82); b = lc(0.1, sy * 1.2, 0.82)
        mb.T = frame_mat() @ Matrix.Translation(-Vector(a))
        mb.rod(M['metal'], a, b, 0.05 * LS, 0.05 * LS, 6)
        mb.rod(M['metal'], lc(-0.7, sy * 1.2, 0.82), lc(0.1, sy * 1.2, 0.82), 0.03 * LS, 0.03 * LS, 5) if False else None
        objs = mb.finish(); o = bpy.data.objects.new('rodpivot%d' % k, None); bpy.context.scene.collection.objects.link(o); o.location = W(a); o.parent = root
        for ob in objs: ob.parent = o
        T['rods'].append((o, W(a).copy(), sy))
    T['drive_r'] = 0.7 * LS; T['crank'] = 0.18 * LS
    T['funnel'] = Vector(lc(2.45, 0, 4.1)); T['front0'] = W(lc(4.1, 0, 0)).x
    for i in range(10):
        mb = MB('puff%d' % i); puff(mb, M, (0, 0, 0), 1.0); o = mb.finish()[0]; o.visible_shadow = False
        T['puffs'].append(o)
    T['hist'] = None

# ----------------------------------------------------------------------------- station
def station(mb, M):
    px0, y0, y1 = PLAT; ph = 1.0
    xm = px0 + 3.0 / 2 * 2; xw = px0 + 3.0                                           # platform back edge
    mb.box(M['brick'], ((px0 + xw) / 2, (y0 + y1) / 2, ph / 2 - 0.05), (xw - px0, y1 - y0, ph - 0.1))
    mb.box(M['woodpale'], ((px0 + xw) / 2, (y0 + y1) / 2, ph - 0.03), (xw - px0 + 0.1, y1 - y0 + 0.1, 0.08))
    mb.box(M['cream'], (px0 + 0.1, (y0 + y1) / 2, ph + 0.01), (0.12, y1 - y0, 0.02))
    # station hut (wood, red roof) on the platform, back part
    hx, hy = xw - 1.2, y0 + 5.0
    mb.box(M['barnred'], (hx, hy, ph + 1.3), (2.0, 5.0, 2.6)); prism_roof(mb, M['roofred'], hx - 1.0, hx + 1.0, hy - 2.5, hy + 2.5, ph + 2.6, ph + 3.5, ov=0.35, ridge='y')
    for yy in (hy - 1.4, hy + 1.4): mb.box(M['cream'], (hx - 1.02, yy, ph + 1.5), (0.06, 0.9, 1.1)); mb.box(M['dark'], (hx - 1.05, yy, ph + 1.5), (0.04, 0.7, 0.9))
    mb.box(M['dark'], (hx - 1.02, hy, ph + 1.1), (0.06, 0.9, 2.0))
    mb.box(M['woodpale'], (hx - 1.0, hy + 3.3, ph + 0.35), (0.4, 1.8, 0.1)); mb.box(M['wood'], (hx - 1.0, hy + 3.3, ph + 0.7), (0.1, 1.8, 0.5))       # bench
    for yy in (hy + 2.6, hy + 4.0): mb.box(M['wood'], (hx - 1.0, yy, ph + 0.15), (0.3, 0.08, 0.3))
    for yy in (y0 + 1.0, y1 - 1.0):                                                                    # lamp posts
        mb.rod(M['black'], (px0 + 0.5, yy, ph), (px0 + 0.5, yy, ph + 3.2), 0.05, 0.04, 6); mb.box(M['gold'], (px0 + 0.5, yy, ph + 3.35), (0.3, 0.3, 0.4)); mb.box(M['cream'], (px0 + 0.5, yy, ph + 3.35), (0.22, 0.22, 0.34))
    for (yy, k) in ((y1 - 3.0, 0), (y1 - 3.8, 1)): crate(mb, M, (px0 + 1.3, yy, ph), (0.8, 0.6, 0.55 + 0.1 * k), 0.4)
    barrel(mb, M, (px0 + 1.0, y1 - 1.8, ph))
    for k in range(4):                                                                                  # luggage (trunks)
        mb.box(M['leather'], (px0 + 1.0 + 0.2 * k, y0 + 2.2 + 0.0, ph + 0.15 + 0.3 * k), (0.8 - 0.1 * k, 0.5, 0.3))

# ----------------------------------------------------------------------------- the whole location
def build_line(ST, P):
    sc = bpy.context.scene; M = palette(); ST['M'] = M
    ground(hole=(PIT[0] - PIT_HW, PIT[1] - PIT_HL, PIT[0] + PIT_HW, PIT[1] + PIT_HL))
    ST['hill_mats'] = hills_ring(P)
    kd = Wd(Vector((-0.4, 0.8, -0.4)).normalized()); ST['cloud_mat'] = clouds(kd, P.get('ncloud', 14), P.get('cloud_z', (40, 130)), P.get('cloud_scale', 0.5))
    # ----- road, ruts, rail
    ys = [float(i) for i in np.arange(-40, 150, 1.0)]
    mb = MB('roads')
    ribbon(mb, M['verge'], xc, ys, 6.5, 0.01); ribbon(mb, M['road'], xc, ys, 3.0, 0.03)
    ribbon(mb, M['rut'], xc, ys, 0.3, 0.04, -0.6); ribbon(mb, M['rut'], xc, ys, 0.3, 0.04, 0.6); ribbon(mb, M['verge'], xc, ys, 0.35, 0.045, 0.0)
    ribbon(mb, M['ballast'], lambda y: TX, ys, 3.4, 0.04)
    for y in np.arange(-40, 150, 0.85): mb.box(M['sleeper'], (TX, y, 0.12), (2.2, 0.26, 0.14))
    for sx in (-0.72, 0.72):
        for y in np.arange(-40, 150, 4.0): mb.box(M['rail'], (TX + sx, y + 2.0, 0.24), (0.1, 4.02, 0.16))
    for y0 in (-1.0, 14.0, 30.0, 48.0):
        for i in range(5): mb.ell(M['earth'], (xc(y0) + 3.4 + i * 0.4 + 0.0, y0 + i * 0.2, 0.15), (0.55, 0.45, 0.28), (8, 6)) if False else None
    mb.finish()
    # ----- trench (clipped by the TRENCH group) + pipe (PIPE group)
    mtd = mat('trdark', '#2a1a16', '#3a2a22', 3, clip='TRENCH'); mte = mat('trearth', '#8c5233', '#b06c44', 6, contrast=1.3, wet=True, clip='TRENCH')
    mpl = mat('leadclip', '#8c929c', '#b6bcc6', 3, rough=0.35, sheen=0.7, clip='PIPE'); mbd = mat('trwall', '#5a3a28', '#7a5036', 5, contrast=1.3, clip='TRENCH')
    mb = MB('trench')
    for y0 in range(int(Y0), int(Y1) + 4, 2):
        xt = xc(y0 + 1) + 2.3
        mb.box(mtd, (xt, y0 + 1, 0.0), (0.75, 2.0, 0.06)); mb.box(mbd, (xt - 0.36, y0 + 1, 0.1), (0.1, 2.0, 0.2)); mb.box(mbd, (xt + 0.36, y0 + 1, 0.1), (0.1, 2.0, 0.2))
        mb.box(mte, (xt + 0.78, y0 + 1, 0.12), (0.55, 2.0, 0.24)); mb.box(mte, (xt - 0.62, y0 + 1, 0.08), (0.32, 2.0, 0.16))
    mb.finish()
    mb = MB('pipe')
    for y0 in range(int(Y0), int(Y1) + 4, 2): mb.rod(mpl, (xc(y0) + 2.3, y0 - 0.02, 0.12), (xc(y0 + 2) + 2.3, y0 + 2.02, 0.12), 0.09, 0.09, 10, smooth=True)
    mb.finish()
    ST['plough'] = None
    mb = MB('plough'); plough(mb, M); ob = mb.finish(); pr = bpy.data.objects.new('plough_root', None); sc.collection.objects.link(pr)
    for o in ob: o.parent = pr
    ST['plough_root'] = pr
    mb = MB('reel'); reel(mb, M, (0, 0, 0.7)); ob = mb.finish(); rr_ = bpy.data.objects.new('reel_root', None); sc.collection.objects.link(rr_)
    for o in ob: o.parent = rr_
    mb = MB('reelcart'); mb.box(M['wood'], (0, 0, 0.12), (1.1, 1.3, 0.1)); mb.cyl(M['metal'], (0, 0, 0.3), 0.04, 1.2, 'y', 6)
    for sy in (-1, 1): mb.cyl(M['wood'], (0, sy * 0.6, 0.3), 0.3, 0.06, 'x', 14) if False else None
    for o in mb.finish(): o.parent = rr_
    ST['reel_root'] = rr_
    # ----- poles / wires / ladders
    build_poles(ST, M); build_train(ST, M)
    mb = MB('ladder0'); ladder(mb, M, (px(4.0) + 0.95, 2.9, 0.0), (px(4.0) + 0.38, 3.78, POLE_H - 0.15), 0.5, 15); ST['ladder'] = [mb.finish()]
    mb = MB('ladder3'); ladder(mb, M, (px(31.0) + 0.9, 29.9, 0.0), (px(31.0) + 0.3, 30.8, POLE_H - 0.3), 0.5, 14); ST['ladder'].append(mb.finish())
    # ----- work props along the line
    mb = MB('work')
    ladder(mb, M, (-3.0, 1.0, 0.08), (-3.2, 5.2, 0.1), 0.5, 10)
    for (x, y, yw) in [(xc(3) + 3.0, 1.0, 0.2), (xc(3) + 3.8, 3.0, 0.9), (xc(7) + 4.0, 8.0, -0.4), (xc(40) + 3.6, 38.0, 0.5)]: pick(mb, M, (x, y, 0.15), yw)
    for (x, y, yw) in [(xc(5) + 4.4, 5.0, 1.3), (xc(12) + 3.6, 12.0, 0.3), (xc(46) + 4.2, 46.0, 2.0), (xc(22) + 4.0, 23.0, 0.8)]: shovel(mb, M, (x, y, 0.05), yw)
    crate(mb, M, (xc(10) + 1.9, 7.2, 0.0), (0.8, 0.6, 0.55), 0.3); crate(mb, M, (xc(10) + 2.1, 8.0, 0.0), (0.7, 0.55, 0.5), -0.2); crate(mb, M, (xc(10) + 2.0, 7.6, 0.55), (0.6, 0.5, 0.45), 0.6)
    barrel(mb, M, (xc(12) + 1.9, 11.0, 0.0)); barrel(mb, M, (xc(12) + 2.5, 11.4, 0.0)); barrel(mb, M, (xc(28) + 5.0, 27.0, 0.0))
    mb.cyl(M['woodpale'], (xc(2) + 2.0, -0.2, 0.05), 0.55, 0.1, 'z', 20); mb.cyl(M['woodpale'], (xc(2) + 2.0, -0.2, 0.62), 0.55, 0.1, 'z', 20); mb.cyl(M['spool'], (xc(2) + 2.0, -0.2, 0.33), 0.42, 0.5, 'z', 20, True)
    for (x, y) in [(-1.0, 12.6), (-0.4, 13.3)]: crate(mb, M, (x, y, 0.0), (0.7, 0.55, 0.5), 0.4)
    wagon2(mb, M, (WAGON[0], WAGON[1], 0.0), math.pi / 2 + 0.06)
    key_station(mb, M, (KEYCRATE[0], KEYCRATE[1], 0.0), 0.5)
    for k in range(3): mb.cyl(M['wiremat'], (KEYCRATE[0] - 1.8, KEYCRATE[1] - 0.8, 0.08 + k * 0.12), 0.6, 0.1, 'z', 22, True); mb.cyl(M['dark'], (KEYCRATE[0] - 1.8, KEYCRATE[1] - 0.8, 0.08 + k * 0.12), 0.26, 0.12, 'z', 14)
    mb.rod(M['lead'], (xc(Y1) + 2.3, Y1 - 0.5, 0.12), (KEYCRATE[0] - 0.1, KEYCRATE[1] - 0.5, 0.6), 0.04, 0.04, 6)      # pipe end rising to the key
    mb.finish()
    # ----- station
    mb = MB('station'); station(mb, M); mb.finish()
    # ----- fences
    mb = MB('fences')
    worm_fence(mb, M, [(xc(y) - 2.6, y) for y in (-20, 6, 20, 40, 62, 85, 110, 135)], seg=3.2)
    worm_fence(mb, M, [(xc(y) + 7.5, y) for y in (-20, 6, 24, 46, 70, 100, 130)], seg=3.2)
    mb.finish()
    # ----- fields, stooks, hay
    mb = MB('wheat'); rw = rnd(21)
    for i in range(P.get('nwheat', 3200)):
        y = rw.uniform(-10, 100); x = rw.uniform(xc(y) + 8.4, xc(y) + 34)
        if (x - PIT[0]) ** 2 < 30 and abs(y - PIT[1]) < 12: continue
        wheat_clump(mb, M, (x, y, 0.0), rw, rw.uniform(0.75, 1.05))
    for i in range(P.get('nwheatL', 1200)):
        y = rw.uniform(-10, 95); x = rw.uniform(-34, -11)
        wheat_clump(mb, M, (x, y, 0.0), rw, rw.uniform(0.7, 1.0))
    mb.finish()
    mb = MB('stooks'); rs = rnd(22)
    for row in range(5):
        for i in range(12):
            y = -6 + i * 6.5 + row * 1.3 + rs.uniform(-.5, .5); x = xc(y) + 11 + row * 4.2 + rs.uniform(-.4, .4)
            if abs(x - PIT[0]) < 4 and abs(y - PIT[1]) < 9: continue
            stook(mb, M, (x, y, 0.0), rs, rs.uniform(0.9, 1.2) * (1 + y * 0.004))
    for i in range(10):
        y = -6 + i * 8 + rs.uniform(-2, 2); x = xc(y) - 7.5 + rs.uniform(-1, 1)
        if abs(x - TX) < 2.5: continue
        stook(mb, M, (x, y, 0.0), rs, 1.1)
    for (x, y) in [(10.0, 70.0), (26.0, 64.0), (-16.0, 30.0)]:
        mb.cyl(M['hay'], (x, y, 1.0), 2.0, 2.0, 'z', 16, True); mb.cyl(M['strawdk'], (x, y, 2.4), 1.8, 1.0, 'z', 16, True, r2=0.2)
    mb.finish()
    mb = MB('verge'); rg = rnd(23)
    for i in range(P.get('ngrass', 1100)):
        y = rg.uniform(-30, 120); side = rg.choice((-1, 1)); x = xc(y) + side * rg.uniform(2.4, 5.0)
        if side > 0 and x < xc(y) + 5.0 and rg.random() < 0.5: continue
        if abs(x - TX) < 2.2: continue
        if Y0 - 1 < y < Y1 + 3 and abs(x - (xc(y) + 2.3)) < 1.0: continue
        grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.5, 1.1))
    for i in range(P.get('nwheatV', 500)):
        y = rg.uniform(-20, 100); x = rg.uniform(-9, -2.5) if rg.random() < 0.6 else rg.uniform(-30, -13)
        if abs(x - TX) < 2.4 or abs(x - (xc(y) - 2.6)) < 0.8: continue
        wheat_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.5, 0.9))
    mb.finish()
    # ----- trees + farm
    mb = MB('trees'); rt = rnd(24)
    for (x, y, s_) in [(-30, 44, 1.6), (-34, 58, 1.8), (-24, 76, 1.6), (22, 40, 1.5), (30, 28, 1.3), (36, 60, 1.8), (-34, 30, 1.6), (4, 92, 1.8), (-8, 100, 1.9), (46, 76, 2.0), (-44, 70, 2.1),
                       (16, 110, 2.0), (-24, 100, 2.2), (30, 104, 2.2), (38, 6, 1.9), (26, -22, 2.0), (50, 40, 2.2), (60, 90, 2.4), (-60, 40, 2.2),
                       (-28, 120, 2.2), (20, 130, 2.3), (70, 20, 2.2), (-70, 90, 2.3), (40, -36, 2.3)]:
        oak(mb, M, (x, y, 0.0), s_, int(x * 7 + y))
    for (yy, ss) in [(33, 1.6), (46, 1.8), (58, 1.7), (72, 1.8)]: oak(mb, M, (xc(yy) + 9.6, yy, 0.0), ss, int(yy * 3))
    mb.finish()
    mb = MB('farm'); farmhouse(mb, M, (20.0, 86.0, 0.0), 0.08); barn(mb, M, (-12.0, 96.0, 0.0), -0.05); mb.finish()
    # ----- sun disc for DAY (hidden from the shade test) is not used: sky painted
    pm = mat('puddle', '#1c2a78', None, rough=0.03, sheen=1.0); pm.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.55
    mb = MB('puddles'); rp_ = rnd(88)
    for (x, y, rx, ry) in [(px(4.0) - 0.9, 3.4, 0.9, 0.6), (px(13.0) - 0.8, 12.4, 0.8, 0.5), (px(22.0) - 0.9, 21.6, 1.0, 0.6), (px(31.0) - 1.0, 30.4, 0.9, 0.7), (xc(8) - 0.2, 8.0, 1.4, 0.8), (xc(20) + 0.3, 20.0, 1.2, 0.7),
                           (xc(35) - 0.6, 34.0, 1.6, 0.9), (xc(47) + 0.5, 47.0, 1.4, 0.8), (xc(58) - 0.2, 59.0, 1.5, 0.8), (KEYCRATE[0] - 1.0, KEYCRATE[1] - 1.8, 1.0, 0.6), (WAGON[0] + 1.6, WAGON[1] - 1.0, 1.1, 0.7),
                           (xc(2) + 0.2, 1.2, 1.3, 0.7), (xc(14) + 0.9, 15.0, 1.0, 0.6), (3.0, -2.2, 1.2, 0.6), (xc(26) + 4.0, 26.0, 0.9, 0.5)]:
        mb.ell(pm, (x, y, 0.035), (rx, ry, 0.012), (16, 6), (0, 0, rp_.uniform(0, 3)))
    ST['puddles'] = mb.finish()
    ST['pit'] = build_pit(ST, M)
    return M

# ----------------------------------------------------------------------------- the cut-away pit (trench_cut)
def build_pit(ST, M):
    cx, cy = PIT; hw, hl, d = PIT_HW, PIT_HL, PIT_D
    strata = mat('strata', '#4a2e22', '#6a4430', 4, zgrad=(-0.45, -0.1, '#c89a60'), contrast=1.4, wet=True)
    strata2 = mat('strata2', '#c88a50', '#e0a868', 5, contrast=1.3, wet=True)
    clay = mat('clay', '#9a8a98', '#b8a8b4', 5, contrast=1.2, wet=True)
    gravel = mat('gravel', '#9a8f88', '#c8b8a8', 14, contrast=1.8, wet=True)
    mb = MB('pit')
    # walls in 4 strata bands (z from top 0 down to -d)
    bands = [(0.0, -0.25, strata), (-0.25, -0.55, strata2), (-0.55, -0.85, clay), (-0.85, -d, gravel)]
    for sg in (-1, 1):
        x = cx + sg * hw
        for (za, zb, m) in bands:
            # slightly sloped walls
            xi = x - sg * 0.12 * ((-zb) / d); xo = x - sg * 0.12 * ((-za) / d)
            q = [(xo, cy - hl, za), (xo, cy + hl, za), (xi, cy + hl, zb), (xi, cy - hl, zb)]
            mb.quad(m, q if sg > 0 else q[::-1])
    for sy in (-1, 1):
        yy = cy + sy * hl
        for (za, zb, m) in bands:
            q = [(cx - hw, yy, za), (cx + hw, yy, za), (cx + hw - 0.12, yy, zb), (cx - hw + 0.12, yy, zb)]
            mb.quad(m, q if sy < 0 else q[::-1])
    mb.quad(M['trdark'] if False else gravel, [(cx - hw + 0.12, cy - hl, -d), (cx + hw - 0.12, cy - hl, -d), (cx + hw - 0.12, cy + hl, -d), (cx - hw + 0.12, cy + hl, -d)][::-1])
    # spoil heaps along the lip, root stubs, a plank across
    rp = rnd(61)
    for sg in (-1, 1):
        for i in range(10): mb.ell(M['earth'], (cx + sg * (hw + 0.35 + rp.uniform(0, 0.4)), cy - hl + i * 1.45 + rp.uniform(-0.3, 0.3), 0.1), (0.45, 0.6, 0.25), (8, 6))
    mb.box(M['woodpale'], (cx, cy - 4.8, 0.05), (hw * 2 + 0.9, 0.3, 0.06)); mb.rod(M['wood'], (cx - hw - 0.3, cy + 5.6, 0.0), (cx - hw + 0.4, cy + 5.8, -0.05), 0.03, 0.03, 6)
    mb.finish()
    # pipe on the floor, split open for 3 m in the middle; wire with torn cloth wrapping
    mb = MB('pitpipe'); zf = -d + 0.12; w0, w1 = cy - 1.6, cy + 1.6
    mb.rod(M['lead'], (cx, cy - hl + 0.1, zf), (cx, w0, zf), 0.1, 0.1, 12, smooth=True); mb.rod(M['lead'], (cx, w1, zf), (cx, cy + hl - 0.1, zf), 0.1, 0.1, 12, smooth=True)
    # split section: two lead half-shell flaps curled outward + the lower half trough
    n = 14
    for i in range(n):
        ya = w0 + (w1 - w0) * i / n; yb = w0 + (w1 - w0) * (i + 1) / n
        for k in range(6):
            a0 = math.pi + k * math.pi / 6 * 1.0; a1 = a0 + math.pi / 6                     # lower half circle
            mb.quad(M['lead'], [(cx + 0.1 * math.cos(a0), ya, zf + 0.1 * math.sin(a0)), (cx + 0.1 * math.cos(a0), yb, zf + 0.1 * math.sin(a0)), (cx + 0.1 * math.cos(a1), yb, zf + 0.1 * math.sin(a1)), (cx + 0.1 * math.cos(a1), ya, zf + 0.1 * math.sin(a1))])
        for sg in (-1, 1):                                                                  # the peeled upper flaps
            for k in range(3):
                a0 = k * 0.35; a1 = a0 + 0.35; r_ = 0.1 + 0.02 * k
                mb.quad(M['lead'], [(cx + sg * (0.1 + 0.07 * math.sin(a0 * 2)), ya, zf + 0.02 + 0.09 * math.cos(a0 * 1.6) * 0.5), (cx + sg * (0.1 + 0.07 * math.sin(a0 * 2)), yb, zf + 0.02 + 0.09 * math.cos(a0 * 1.6) * 0.5),
                                     (cx + sg * (0.1 + 0.07 * math.sin(a1 * 2)), yb, zf + 0.02 + 0.09 * math.cos(a1 * 1.6) * 0.5), (cx + sg * (0.1 + 0.07 * math.sin(a1 * 2)), ya, zf + 0.02 + 0.09 * math.cos(a1 * 1.6) * 0.5)])
    mb.finish()
    cloth = mat('cloth', '#d8c8a0', '#b8a070', 10, contrast=1.3, wet=True); tar = mat('tarcloth', '#3a2a22', '#5a4636', 10)
    mb = MB('pitwire')
    zw = zf + 0.04
    mb.rod(M['wiremat'], (cx, cy - hl + 0.2, zf), (cx, w0, zw), 0.025, 0.025, 6)
    mb.rod(M['copper'], (cx - 0.01, w0, zw), (cx + 0.01, w1, zw), 0.035, 0.035, 8)                 # bare copper in the opened section
    mb.rod(M['wiremat'], (cx, w1, zw), (cx, cy + hl - 0.2, zf), 0.025, 0.025, 6)
    rcl = rnd(62)
    for i in range(10):                                                                     # cloth wrapping: spiral wraps in the intact parts + torn ragged strips hanging
        yy = w0 - 0.15 - i * 0.16
        mb.rod(cloth if i % 2 else tar, (cx - 0.05, yy, zw), (cx + 0.05, yy + 0.1, zw + 0.02), 0.05, 0.05, 8)
    for i in range(10):
        yy = w1 + 0.15 + i * 0.16
        mb.rod(cloth if i % 2 else tar, (cx - 0.05, yy, zw), (cx + 0.05, yy + 0.1, zw + 0.02), 0.05, 0.05, 8)
    for i in range(9):                                                                      # torn strips
        yy = rcl.uniform(w0 - 0.4, w1 + 0.4); sg = rcl.choice((-1, 1)); ln = rcl.uniform(0.25, 0.6)
        mb.quad(cloth, [(cx, yy, zw + 0.04), (cx, yy + 0.07, zw + 0.04), (cx + sg * ln, yy + rcl.uniform(-0.1, 0.1) + 0.12, zw - 0.0), (cx + sg * ln * 0.9, yy - 0.02, zw - 0.01)])
    mb.finish()
    mb = MB('pitdamp'); dm = mat('damp', '#2a1c1a', '#3e2a26', 6)
    for i in range(7): mb.ell(dm, (cx + rcl.uniform(-0.6, 0.6), cy + rcl.uniform(-1.8, 1.8), -d + 0.02), (rcl.uniform(0.2, 0.45), rcl.uniform(0.3, 0.6), 0.01), (10, 6))
    mb.finish()
    return dict(c=(cx, cy), hw=hw, hl=hl, d=d, zf=zf, w=(w0, w1))

# ----------------------------------------------------------------------------- foreground dressing around a camera
def fg_dress(ST, M, cam, look, items, seed=31, ngrass=260):
    """items: list of (kind, right_m, fwd_m, [extra]) relative to the camera ground point; kinds crate/spool/coil/bottles/pick/shovel/grass/barrel"""
    rr = rnd(seed); c = Vector(cam[:2]); f = (Vector(look[:2]) - c).normalized(); r = Vector((f.y, -f.x))
    mb = MB('fg')
    for kind, rt, fw, *ex in items:
        p = c + f * fw + r * rt; x, y = p.x, p.y
        if kind == 'crate': crate(mb, M, (x, y, 0.0), (0.9, 0.7, 0.6), rr.uniform(0, 1)); crate(mb, M, (x + 0.8, y + 0.2, 0.0), (0.7, 0.55, 0.5), rr.uniform(-1, 0.5))
        elif kind == 'spool':
            mb.cyl(M['woodpale'], (x, y, 0.05), 0.62, 0.1, 'z', 22); mb.cyl(M['woodpale'], (x, y, 0.7), 0.62, 0.1, 'z', 22); mb.cyl(M['spool'], (x, y, 0.38), 0.46, 0.6, 'z', 22, True)
            mb.rod(M['wiremat'], (x + 0.45, y, 0.5), (x + 1.3, y + 0.3, 0.02), 0.02, 0.02, 5)
        elif kind == 'coil':
            for k in range(3): mb.cyl(M['wiremat'], (x, y, 0.08 + k * 0.12), 0.6, 0.1, 'z', 22, True); mb.cyl(M['dark'], (x, y, 0.08 + k * 0.12), 0.26, 0.12, 'z', 14)
        elif kind == 'bottles':
            for k in range(5): beer_bottle(mb, M, (x + rr.uniform(-0.5, 0.5), y + rr.uniform(-0.4, 0.4), 0.0), 1.8)
        elif kind == 'pick': pick(mb, M, (x, y, 0.15), rr.uniform(0, 6))
        elif kind == 'shovel': shovel(mb, M, (x, y, 0.05), rr.uniform(0, 6))
        elif kind == 'barrel': barrel(mb, M, (x, y, 0.0))
        elif kind == 'keybox': key_station(mb, M, (x, y, 0.0), rr.uniform(-0.6, 0.6))
        elif kind == 'grass':
            for i in range(ex[0] if ex else 120):
                q = p + f * rr.uniform(-1.5, 3.5) + r * rr.uniform(-3.2, 3.2)
                grass_clump(mb, M, (q.x, q.y, 0.0), rr, rr.uniform(0.45, 0.95)) if rr.random() < 0.6 else wheat_clump(mb, M, (q.x, q.y, 0.0), rr, rr.uniform(0.6, 1.0))
    return mb.finish()
