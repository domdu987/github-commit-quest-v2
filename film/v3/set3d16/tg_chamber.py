"""tg_chamber.py : CHAMBER location of set3d16 (generic 1840s legislative chamber), grown from styleboard/sb.py sb2. Sb frame (metres, +y into the hall, windows on the
back wall y = 34), scale only. Tiers of walnut desks around C = (0, 7), the front table (0, 4.2) with the telegraph, the speaker's door-screen behind the dais.
Hooks: set_tape(len, clicking), set_click(on), set_moneybag(on), set_mailsacks(on), set_flames(level)."""
import telegraph_kit as K
from telegraph_kit import *
import tg_line as LN
import telegraph_tex as TX

BY = 34.0
C = (0.0, 7.0)
TABLE = (0.0, 4.2); TW = 4.8
TG_S = 3.0                                   # telegraph scale on the table
TG_C = (TABLE[0] - 0.35, TABLE[1] + 0.1, 0.96)
TAPE_W = 0.12
STOOL = (-1.45, 3.05)
SCREEN_Y = 13.4
TIERS = [6.5, 9.0, 11.5, 14.0, 16.5]
MOCK_A = math.radians(136)                    # front-row desk of the mocker
def desk_pos(ti, a):
    r = TIERS[ti]; return (C[0] + r * math.cos(a), C[1] + r * math.sin(a)), 0.38 * ti
def seat(ti, a, d=0.95):
    (x, y), z = desk_pos(ti, a); return (x + d * math.cos(a), y + d * math.sin(a), z)
MARKS = dict(morse_table=(-1.9, 5.4, 0.0), clerk_table=(2.0, 5.4, 0.0), mocker_table=(0.35, 6.5, 0.0), mocker_stool=(STOOL[0], STOOL[1], 0.0), mocker_desk=seat(0, MOCK_A),
             cong_a=seat(1, math.radians(98)), cong_b=seat(1, math.radians(140)), cong_c=seat(2, math.radians(70)), cong_d=seat(0, math.radians(150)), cong_e=seat(0, math.radians(40)),
             morse_door=(0.05, SCREEN_Y - 0.15, 0.0), mocker_post=seat(0, MOCK_A), table_front=(0.0, 3.0, 0.0), dais=(0.0, 10.0, 0.4))
SEAT = dict(mocker_stool=0.56)

def mats():
    M = palette()
    M['sack'] = mat('sack', '#b89c70', '#d4b888', 8, contrast=1.2)
    M['sackdk'] = mat('sackdk', '#8a7250', '#a48a62', 8)
    M['screenw'] = mat('screenw', '#7a4424', '#9a5c32', 6, aniso=(1, 0.3, 1), contrast=1.5, rough=0.45, sheen=0.4)
    M['panel'] = mat('panel', '#5e3418', '#7a4824', 7, aniso=(1, 0.3, 1), contrast=1.6, rough=0.45, sheen=0.4)
    M['moneyb'] = mat('moneyb', '#8c6a38', '#b08848', 6, contrast=1.3)
    M['coin'] = mat('coin', '#e8c04a', '#f8dc78', 4, rough=0.25, sheen=1.0)
    M['doorlit'] = mat_emit('doorlit', '#ffc880', 2.4)
    return M

def tg_arm_parts(mb, M, c, s):
    """the telegraph as sb2 builds it, without the lever (its own object): base, battery jars, coils, yoke, key, register"""
    mb.push(Matrix.Translation(c) @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M['walnut'], (0, 0, 0.03), (0.95, 0.42, 0.06)); mb.box(M['walnut'], (0, 0, 0.075), (0.9, 0.38, 0.03))
    mb.box(M['brass'], (-0.22, 0.0, 0.1), (0.3, 0.2, 0.025))
    for sy in (-0.06, 0.06):
        mb.cyl(M['copper'], (-0.22, sy, 0.2), 0.045, 0.16, 'z', 16, True); mb.cyl(M['brass'], (-0.22, sy, 0.285), 0.05, 0.015, 'z', 16); mb.cyl(M['brass'], (-0.22, sy, 0.118), 0.05, 0.015, 'z', 16)
    mb.box(M['metal'], (-0.22, 0, 0.31), (0.08, 0.2, 0.02))
    mb.box(M['walnut'], (0.18, -0.12, 0.1), (0.22, 0.1, 0.03)); mb.box(M['brass'], (0.2, -0.12, 0.125), (0.14, 0.03, 0.02))
    mb.rod(M['brass'], (0.12, -0.12, 0.14), (0.3, -0.12, 0.16), 0.01, 0.01, 6); mb.ell(M['dark'], (0.31, -0.12, 0.172), (0.03, 0.03, 0.026), (10, 6))
    mb.box(M['wood'], (0.18, 0.1, 0.12), (0.32, 0.2, 0.1)); mb.cyl(M['paper'], (0.1, 0.1, 0.24), 0.08, 0.1, 'y', 20)
    mb.cyl(M['brass'], (0.1, 0.1, 0.24), 0.02, 0.16, 'y', 10); mb.cyl(M['brass'], (0.26, 0.1, 0.2), 0.03, 0.12, 'y', 12)
    mb.box(M['paper'], (0.3, 0.1, 0.178), (0.18, 0.06, 0.004), ry=-0.18)
    for k, bx in enumerate((-0.34, -0.12)):
        mb.cyl(M['glassjar'], (bx, 0.27, 0.14), 0.07, 0.17, 'z', 16, True); mb.cyl(M['copper'], (bx, 0.27, 0.15), 0.035, 0.14, 'z', 10); mb.cyl(M['gold'], (bx, 0.27, 0.235), 0.075, 0.015, 'z', 16)
    mb.pop()

def build_tape(ST, M):
    """paper strip from the register slot over the table front and down to the floor, looping round the mocker's stool; clipped by TG_CLIP_TAPE (UV 'CLIP' x)"""
    tex = TX.ensure(); sx, sy, sz = TG_C[0] + TG_S * 0.36, TG_C[1] + TG_S * 0.10, TG_C[2] + TG_S * 0.172
    P = [Vector((sx, sy, sz)), Vector((sx + 0.25, sy - 0.12, sz - 0.05))]
    # across the table top toward the front edge
    ty = TABLE[1]; zt = 0.972
    P += [Vector((sx + 0.45, sy - 0.3, zt + 0.25)), Vector((sx + 0.55, sy - 0.65, zt + 0.06)), Vector((sx + 0.35, sy - 1.0, zt + 0.005)), Vector((sx + 0.05, ty - 0.55, zt + 0.005)), Vector((sx - 0.3, ty - 0.82, zt + 0.004))]
    # over the front edge and down
    xe = sx - 0.45; ye = ty - 0.86
    P += [Vector((xe - 0.05, ye - 0.04, 0.95)), Vector((xe - 0.1, ye - 0.1, 0.80)), Vector((xe - 0.15, ye - 0.12, 0.55)), Vector((xe - 0.25, ye - 0.14, 0.3)), Vector((xe - 0.4, ye - 0.2, 0.08))]
    # floor loops around the stool (lying flat, stacked)
    rr = rnd(9); cx, cy = STOOL
    for k in range(34):
        a = -0.3 + k * 0.52; rad = 0.55 + 0.35 * math.sin(k * 0.7) + 0.02 * k; z = 0.012 + 0.0042 * k + (0.012 if k % 6 == 3 else 0.0)
        P.append(Vector((cx + rad * math.cos(a) * 1.15, cy + rad * math.sin(a) * 0.8, z)))
    # smooth with a Catmull-Rom pass
    pts = []
    for i in range(len(P) - 1):
        p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(len(P) - 1, i + 2)]
        for t in np.linspace(0, 1, 7, endpoint=False):
            t2, t3 = t * t, t * t * t
            pts.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    pts.append(P[-1])
    cum = [0.0]
    for a, b in zip(pts[:-1], pts[1:]): cum.append(cum[-1] + (b - a).length)
    tot = cum[-1]; verts = []; uv1 = []; uv2 = []; faces = []; prev_l = Vector((1, 0, 0))
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized(); l = t.cross(Vector((0, 0, 1)))
        if l.length < 0.35: l = prev_l.copy()
        l = l.normalized()
        if l.dot(prev_l) < 0: l = -l
        prev_l = l; verts += [tuple(p - l * TAPE_W / 2), tuple(p + l * TAPE_W / 2)]
        uv1 += [(cum[i] / 5.7, 0.0), (cum[i] / 5.7, 1.0)]; uv2 += [(cum[i] / tot, 0.0), (cum[i] / tot, 1.0)]
    for i in range(len(pts) - 1):
        a = 2 * i; faces.append((a, a + 1, a + 3, a + 2))
    me = bpy.data.meshes.new('tape'); T = frame_mat(); me.from_pydata([tuple(T @ Vector(v)) for v in verts], [], faces); me.update()
    u1 = me.uv_layers.new(name='UVMap'); u2 = me.uv_layers.new(name='CLIP')
    for poly in me.polygons:
        for li, vi in zip(poly.loop_indices, poly.vertices): u1.data[li].uv = uv1[vi]; u2.data[li].uv = uv2[vi]
    m = bpy.data.materials.new('tape'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.9; bs.inputs['Specular IOR Level'].default_value = 0.1
    tx = N('ShaderNodeTexImage'); tx.image = bpy.data.images.load(tex['tape'], check_existing=True); tx.extension = 'REPEAT'; L(tx.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Emission Strength'].default_value = 0.15; L(tx.outputs['Color'], bs.inputs['Emission Color'])
    uvm = N('ShaderNodeUVMap'); uvm.uv_map = 'UVMap'; L(uvm.outputs[0], tx.inputs[0])
    uvc = N('ShaderNodeUVMap'); uvc.uv_map = 'CLIP'; sp = N('ShaderNodeSeparateXYZ'); L(uvc.outputs[0], sp.inputs[0])
    cv = K.clip_out(nt, 'TAPE'); cmp_ = N('ShaderNodeMath'); cmp_.operation = 'GREATER_THAN'; L(sp.outputs['X'], cmp_.inputs[0]); L(cv, cmp_.inputs[1])
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(cmp_.outputs[0], mx.inputs[0]); L(bs.outputs[0], mx.inputs[1]); L(tr.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('tape', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = True
    ST['tape'] = ob; ST['tape_len'] = tot

def bag(mb, M, c, s=1.0):
    """tied cloth money sack: slumped body, gathered neck with a flared ruffle, rope tie, gold coins spilled on the baize"""
    x, y, z = c
    mb.ell(M['moneyb'], (x, y, z + 0.27 * s), (0.4 * s, 0.34 * s, 0.27 * s), (16, 10)); mb.ell(M['moneyb'], (x + 0.05 * s, y, z + 0.42 * s), (0.3 * s, 0.26 * s, 0.22 * s), (14, 8))
    mb.cyl(M['moneyb'], (x, y, z + 0.64 * s), 0.17 * s, 0.22 * s, 'z', 12, True, r2=0.085 * s)
    mb.rod(M['rope'], (x, y, z + 0.7 * s), (x, y, z + 0.74 * s), 0.1 * s, 0.1 * s, 12, caps=False)
    mb.cyl(M['moneyb'], (x + 0.02 * s, y, z + 0.84 * s), 0.085 * s, 0.14 * s, 'z', 12, True, r2=0.19 * s)
    rs = rnd(8)
    for k in range(10):
        a = rs.uniform(0, 6.28); rr_ = rs.uniform(0.3, 0.6) * s
        mb.cyl(M['coin'], (x + 0.3 * s + rr_ * math.cos(a) * 0.9, y + rr_ * math.sin(a) * 0.9, z + 0.012 + 0.012 * (k % 3)), 0.055 * s, 0.014 * s, 'z', 12)
    for k in range(3): mb.cyl(M['coin'], (x - 0.05 * s + 0.0 * k, y - 0.32 * s, z + 0.03 + 0.016 * k), 0.055 * s, 0.014 * s, 'z', 12)

def sack(mb, M, c, s=1.0, yaw=0.0, tall=1.0):
    """canvas mail sack: slumped body, cinched neck with a flared top, rope tie, red band (no text), a few letters spilled at its foot"""
    x, y, z = c
    mb.ell(M['sack'], (x, y, z + 0.26 * s * tall), (0.36 * s, 0.28 * s, 0.26 * s * tall), (14, 9), (0, 0, yaw)); mb.ell(M['sack'], (x, y, z + 0.42 * s * tall), (0.3 * s, 0.24 * s, 0.2 * s * tall), (12, 8), (0, 0, yaw))
    mb.ell(M['red'], (x, y - 0.27 * s, z + 0.3 * s * tall), (0.2 * s, 0.02, 0.04 * s), (10, 6), (0, 0, yaw))
    mb.cyl(M['sack'], (x, y, z + 0.6 * s * tall), 0.15 * s, 0.2 * s, 'z', 10, True, r2=0.075 * s)
    mb.rod(M['rope'], (x, y, z + 0.66 * s * tall), (x, y, z + 0.69 * s * tall), 0.085 * s, 0.085 * s, 10, caps=False)
    mb.cyl(M['sack'], (x, y, z + 0.78 * s * tall), 0.075 * s, 0.14 * s, 'z', 10, True, r2=0.17 * s)
    for k in range(3): mb.box(M['paper'], (x + 0.3 * s + 0.08 * k * s, y - 0.1 * s + 0.1 * k * s, z + 0.015 + 0.012 * k), (0.16 * s, 0.1 * s, 0.01), rz=yaw + 0.7 * k)

def build_chamber(ST, P):
    sc = bpy.context.scene; M = mats(); ST['M'] = M
    ST['hill_mats'] = LN.hills_ring(P); ST['cloud_mat'] = LN.clouds(Wd(Vector((-0.4, 0.8, -0.4)).normalized()), 8, (40, 90), 0.8, seed=9)
    LN.ground(z=-0.4); ST['puddles'] = []
    mb = MB('room'); rr = rnd(5)
    mb.box(M['floor'], (0, 13, -0.15), (46, 44, 0.3)); mb.box(M['carpet'], (0, 14, -0.12), (3.0, 40, 0.3))
    mb.box(M['wall'], (-22.5, 13, 7), (1, 44, 14)); mb.box(M['wall'], (22.5, 13, 7), (1, 44, 14)); mb.box(M['wall'], (0, -9, 7), (46, 1, 14))
    mb.box(M['wall'], (0, 13, 12.8), (46, 44, 0.6))
    for i in range(-5, 6):
        mb.box(M['wall'], (i * 4.0, 13, 12.3), (0.6, 44, 0.4)); mb.box(M['gold'], (i * 4.0 - 0.33, 13, 12.12), (0.06, 44, 0.07)); mb.box(M['gold'], (i * 4.0 + 0.33, 13, 12.12), (0.06, 44, 0.07))
    for j in range(0, 5):
        mb.box(M['wall'], (0, j * 9.0 - 5, 12.25), (46, 0.6, 0.5)); mb.box(M['gold'], (0, j * 9.0 - 5.33, 12.0), (46, 0.06, 0.07)); mb.box(M['gold'], (0, j * 9.0 - 4.67, 12.0), (46, 0.06, 0.07))
    for sx in (-1.3, 1.3): mb.box(M['carpetdk'], (sx, 14, 0.04), (0.28, 40, 0.02)); mb.box(M['gold'], (sx * 0.86, 14, 0.045), (0.04, 40, 0.02))
    for yy in np.arange(-5.0, 34.0, 1.2):
        mb.box(M['gold'], (0, yy, 0.045), (0.5, 0.12, 0.02)); mb.box(M['carpetdk'], (0, yy + 0.6, 0.04), (0.9, 0.2, 0.02))
    win_x = [-18, -12, -6, 0, 6, 12, 18]
    K.window_wall(mb, M, BY, win_x)
    for sx in (-1, 1):
        for yy in (8, 16, 24): mb.box(M['cream'], (sx * 21.9, yy, 5.0), (0.2, 2.4, 6.0)); mb.box(M['dark'], (sx * 21.8, yy, 5.0), (0.1, 2.0, 5.6))
    mb.box(M['walnut'], (0, BY - 0.45, 0.2), (44, 0.2, 0.4))
    for cx in (-15, -9, -3, 3, 9, 15):
        mb.cyl(M['marble'], (cx, BY - 1.2, 5.0), 0.62, 10.0, 'z', 20, True); mb.box(M['marble'], (cx, BY - 1.2, 0.2), (1.6, 1.6, 0.4)); mb.box(M['marble'], (cx, BY - 1.2, 10.2), (1.7, 1.7, 0.4)); mb.cyl(M['gold'], (cx, BY - 1.2, 9.8), 0.8, 0.3, 'z', 20)
    for c in win_x:
        for sg in (-1, 1):
            mb.rod(M['drape'], (c + sg * 1.85, BY - 0.9, 8.7), (c + sg * 1.85, BY - 0.9, 1.0), 0.3, 0.38, 10, smooth=True); mb.rod(M['drape'], (c + sg * 1.55, BY - 0.9, 8.4), (c + sg * 1.62, BY - 0.9, 3.0), 0.16, 0.18, 8, smooth=True)
            mb.cyl(M['gold'], (c + sg * 1.85, BY - 0.9, 3.0), 0.34, 0.05, 'z', 10)
        mb.box(M['drape'], (c, BY - 0.9, 8.7), (4.0, 0.5, 0.55)); mb.cyl(M['gold'], (c, BY - 1.17, 8.4), 0.05, 4.0, 'x', 6)
        for k in range(7): mb.ell(M['drape'], (c - 1.8 + k * 0.6, BY - 1.1, 8.45), (0.35, 0.2, 0.3), (10, 6))
    sconces = [(-9, BY - 2.1, 4.8), (3, BY - 2.1, 4.8), (9, BY - 2.1, 4.8)]
    for x in (-9, 3, 9):
        mb.box(M['gold'], (x, BY - 1.9, 4.2), (0.1, 0.3, 0.1)); mb.cyl(M['gold'], (x, BY - 2.1, 4.35), 0.08, 0.1, 'z', 10); mb.cyl(M['cream'], (x, BY - 2.1, 4.55), 0.03, 0.3, 'z', 8); mb.ell(M['flame'], (x, BY - 2.1, 4.8), (0.035, 0.035, 0.09), (6, 4))
    # speaker's dais + rostrum + the door-screen behind it
    mb.box(M['floor'], (0, 10.5, 0.2), (7.0, 3.6, 0.4)); mb.box(M['carpet'], (0, 10.0, 0.42), (5.0, 2.4, 0.04))
    mb.box(M['walnut'], (0, 11.2, 1.0), (2.4, 0.9, 1.2)); mb.box(M['walnut'], (0, 11.2, 1.65), (2.7, 1.1, 0.1)); mb.box(M['leather'], (0, 11.0, 1.72), (2.4, 0.8, 0.04))
    mb.box(M['leather'], (0, 12.6, 0.95), (0.8, 0.7, 0.1)); mb.box(M['walnut'], (0, 13.0, 1.9), (0.8, 0.1, 2.2)); mb.box(M['leather'], (0, 12.95, 2.0), (0.6, 0.03, 1.7))
    mb.box(M['gold'], (0.8, 11.2, 1.8), (0.1, 0.1, 0.3)); mb.cyl(M['gold'], (-0.8, 11.2, 1.85), 0.1, 0.3, 'z', 10)
    sw, sh = 6.8, 4.6                                                                                          # screen: panelled wall with a doorway at x 0
    for (xa, xb) in ((-sw / 2, -0.62), (0.62, sw / 2)):
        mb.box(M['screenw'], ((xa + xb) / 2, SCREEN_Y, sh / 2), (xb - xa, 0.3, sh))
        for k in range(int((xb - xa) / 1.2)):
            px_ = xa + 0.6 + k * 1.2; mb.box(M['panel'], (px_, SCREEN_Y - 0.17, 1.0), (0.9, 0.06, 1.3)); mb.box(M['panel'], (px_, SCREEN_Y - 0.17, 3.0), (0.9, 0.06, 1.6))
    mb.box(M['screenw'], (0, SCREEN_Y, 3.7 + (sh - 3.7) / 2), (1.24, 0.3, sh - 3.7)); mb.box(M['doorlit'], (0, SCREEN_Y + 0.3, 1.85), (1.24, 0.1, 3.7)); mb.box(M['doorlit'], (0, SCREEN_Y + 0.15, 0.02), (1.24, 0.4, 0.04))
    mb.box(M['gold'], (0, SCREEN_Y - 0.2, sh + 0.12), (sw + 0.3, 0.3, 0.24)); mb.box(M['gold'], (0, SCREEN_Y - 0.2, 3.75), (1.5, 0.22, 0.08))
    for sgn in (-1, 1): mb.box(M['gold'], (sgn * 0.66, SCREEN_Y - 0.2, 1.85), (0.1, 0.2, 3.8))
    mb.cyl(M['gold'], (0, SCREEN_Y - 0.35, sh + 0.4), 0.5, 0.12, 'y', 16); mb.ell(M['gold'], (0, SCREEN_Y - 0.4, sh + 0.8), (0.4, 0.1, 0.25), (10, 6))                                # crest
    for (sx_, sy_) in [(-1.8, 3.0), (1.9, 9.0), (-2.1, 15.0), (2.2, 19.0)]:
        mb.ell(M['brass'], (sx_, sy_, 0.16), (0.24, 0.24, 0.16), (14, 8)); mb.cyl(M['brass'], (sx_, sy_, 0.3), 0.15, 0.12, 'z', 14, True, r2=0.2)
    gx, gy = -2.8, 10.4
    mb.cyl(M['walnut'], (gx, gy, 0.55), 0.22, 0.03, 'z', 12); mb.rod(M['walnut'], (gx, gy, 0.42), (gx, gy, 1.05), 0.04, 0.03, 8)
    for k in (-1, 1): mb.rod(M['walnut'], (gx, gy, 0.42), (gx + k * 0.4, gy, 0.42), 0.03, 0.03, 6); mb.rod(M['walnut'], (gx, gy, 0.42), (gx, gy + k * 0.4, 0.42), 0.03, 0.03, 6)
    mb.ell(M['globe'], (gx, gy, 1.5), (0.5, 0.5, 0.5), (24, 16)); mb.cyl(M['brass'], (gx, gy, 1.5), 0.53, 0.03, 'x', 24); mb.cyl(M['brass'], (gx, gy, 1.5), 0.53, 0.03, 'y', 24)
    rp = rnd(77)
    for k, c in enumerate(win_x):
        mb.box(M['frame'], (c, BY - 0.62, 10.4), (3.1, 0.14, 2.1)); mb.box(M['paintsky'], (c, BY - 0.72, 10.65), (2.8, 0.06, 1.3)); mb.box(M['paintgrn'], (c, BY - 0.72, 9.75), (2.8, 0.06, 0.6))
        for j in range(3): mb.ell(M['paintdk'], (c - 0.9 + j * 0.9 + rp.uniform(-0.2, 0.2), BY - 0.76, 10.0), (0.22, 0.03, 0.34 + 0.1 * j), (8, 6))
        mb.ell(M['paintgrn'], (c + rp.uniform(-0.6, 0.6), BY - 0.76, 9.8), (0.9, 0.03, 0.3), (10, 6))
    # tiers of desks (semicircle around C); the front row skips the screen
    cand = []
    for ti, r in enumerate(TIERS):
        zt = 0.38 * ti; a0, a1 = math.radians(14), math.radians(166); n = int((a1 - a0) * r / 1.75)
        for i in range(n):
            a = a0 + (i + 0.5) * (a1 - a0) / n
            if abs(a - math.pi / 2) < math.radians(5.5) or abs(abs(a - math.pi / 2) - math.radians(38)) < math.radians(2.0): continue
            px, py = C[0] + r * math.cos(a), C[1] + r * math.sin(a)
            if ti == 0 and abs(a - math.pi / 2) < math.radians(30) and py > SCREEN_Y - 1.6: continue
            if ti:
                mb.box(M['floor'], (C[0] + (r + 0.3) * math.cos(a), C[1] + (r + 0.3) * math.sin(a), zt / 2 - 0.04), (2.65, 2.55, zt + 0.0), rz=a - math.pi / 2)
            K.desk(mb, M, (px, py), a - math.pi / 2, zt, rr); cand.append((ti, a, px, py, zt))
    ST['desks'] = cand
    # candlesticks on the front-row desks (lit at NIGHT, small pools) and on the dais
    cl = []
    for (ti, a, px, py, zt) in cand:
        if ti == 0 and int(math.degrees(a)) % 2 == 0:
            cx_, cy_ = px + 0.0, py + 0.0; mb.cyl(M['gold'], (cx_, cy_, zt + 0.9), 0.05, 0.06, 'z', 10); mb.cyl(M['cream'], (cx_, cy_, zt + 1.05), 0.022, 0.2, 'z', 8); mb.ell(M['flame'], (cx_, cy_, zt + 1.2), (0.022, 0.022, 0.055), (6, 4)); cl.append((cx_, cy_, zt + 1.25))
    ST['desk_candles'] = cl
    mb.finish()
    # ----- front table + telegraph + extras
    mb = MB('table'); tx, ty = TABLE
    mb.box(M['walnut'], (tx, ty, 0.9), (TW, 1.7, 0.1)); mb.box(M['baize'], (tx, ty, 0.955), (TW - 0.2, 1.5, 0.012)); mb.box(M['gold'], (tx, ty - 0.86, 0.9), (TW, 0.03, 0.07))
    for sx in (-TW / 2 + 0.2, TW / 2 - 0.2):
        for sy in (-0.7, 0.7): mb.rod(M['walnut'], (tx + sx, ty + sy, 0.0), (tx + sx, ty + sy, 0.86), 0.09, 0.06, 8, smooth=True)
    mb.box(M['walnut'], (tx, ty, 0.35), (TW - 0.4, 0.08, 0.1))
    tg_arm_parts(mb, M, TG_C, TG_S)
    mb.box(M['paper'], (tx + 1.95, ty - 0.2, 0.99), (0.5, 0.65, 0.06), rz=0.2); mb.box(M['paper'], (tx + 1.9, ty - 0.18, 1.04), (0.46, 0.6, 0.05), rz=0.35)
    mb.cyl(M['ink'], (tx + 1.8, ty + 0.5, 0.99), 0.06, 0.1, 'z', 10); mb.cyl(M['brass'], (tx + 1.8, ty + 0.5, 1.05), 0.065, 0.02, 'z', 10); mb.rod(M['paper'], (tx + 1.8, ty + 0.5, 1.05), (tx + 1.95, ty + 0.62, 1.4), 0.008, 0.003, 4)
    mb.cyl(M['gold'], (tx - 1.9, ty - 0.45, 1.3), 0.02, 0.6, 'z', 6); mb.cyl(M['gold'], (tx - 1.9, ty - 0.45, 1.65), 0.15, 0.12, 'z', 12, True, r2=0.08); mb.ell(M['flame'], (tx - 1.9, ty - 0.45, 1.8), (0.06, 0.06, 0.12), (8, 6))
    mb.cyl(M['gold'], (tx - 2.1, ty - 0.2, 1.05), 0.1, 0.22, 'z', 10); mb.cyl(M['cream'], (tx - 2.1, ty - 0.2, 1.25), 0.03, 0.2, 'z', 8); mb.ell(M['flame'], (tx - 2.1, ty - 0.2, 1.38), (0.025, 0.025, 0.06), (6, 4))
    mb.rod(M['wiremat'], (tx - 0.7, ty + 0.5, 0.97), (tx - 1.4, ty + 0.8, 0.5), 0.015, 0.015, 5); mb.rod(M['wiremat'], (tx - 1.4, ty + 0.8, 0.5), (tx - 2.2, ty + 1.3, 0.02), 0.015, 0.015, 5)
    for sx in (-3.4, 3.4):
        mb.box(M['leather'], (tx + sx, ty - 0.2, 0.5), (0.55, 0.5, 0.07)); mb.box(M['walnut'], (tx + sx, ty + 0.05, 0.9), (0.55, 0.06, 0.8))
        for dx in (-0.25, 0.25):
            for dy in (-0.4, 0.0): mb.rod(M['walnut'], (tx + sx + dx, ty + dy, 0.0), (tx + sx + dx, ty + dy, 0.46), 0.03, 0.025, 5)
    # the mocker's stool beside the register
    sx_, sy_ = STOOL; mb.cyl(M['leather'], (sx_, sy_, 0.58), 0.28, 0.08, 'z', 16)
    for k in range(3):
        a = k * 2.094 + 0.5; mb.rod(M['walnut'], (sx_ + math.cos(a) * 0.18, sy_ + math.sin(a) * 0.18, 0.55), (sx_ + math.cos(a) * 0.3, sy_ + math.sin(a) * 0.3, 0.0), 0.035, 0.03, 6)
    ST['table_objs'] = mb.finish()
    # lever (own object): pivot at the yoke
    mb = MB('lever'); piv = Vector((TG_C[0] + TG_S * 0.0, TG_C[1], TG_C[2] + TG_S * 0.36))
    mb.T = frame_mat() @ Matrix.Translation(-piv)
    mb.push(Matrix.Translation(TG_C) @ Matrix.Diagonal((TG_S, TG_S, TG_S, 1)))
    mb.rod(M['brass'], (-0.35, 0, 0.335), (0.0, 0, 0.36), 0.01, 0.01, 6); mb.box(M['brass'], (-0.35, 0, 0.32), (0.025, 0.08, 0.06)); mb.ell(M['brass'], (-0.35, 0, 0.345), (0.018, 0.018, 0.018), (8, 6))
    mb.pop(); lo = mb.finish(); lv = bpy.data.objects.new('lever_pivot', None); sc.collection.objects.link(lv); lv.location = W(piv)
    for o in lo: o.parent = lv
    ST['lever'] = lv
    build_tape(ST, M)
    # money bag + sacks (hooks)
    mb = MB('moneybag'); bag(mb, M, (0, 0, 0), 1.3); ob = mb.finish(); mbr = bpy.data.objects.new('moneybag_root', None); sc.collection.objects.link(mbr)
    for o in ob: o.parent = mbr
    mbr.location = W((tx + 1.15, ty - 0.1, 0.96)); ST['moneybag'] = mbr; ST['moneybag_base'] = mbr.location.copy()
    mb = MB('mailsacks'); ax, ay, az = MARKS['mocker_desk']; rs = rnd(15)
    for i, (dx, dy, tl) in enumerate([(-1.5, -1.1, 1.0), (-0.9, -1.9, 0.9), (0.2, -2.3, 1.1), (1.2, -1.7, 1.0), (1.7, -0.8, 0.9), (-1.9, 0.0, 1.1), (-0.5, -1.4, 1.2), (0.6, -1.2, 0.8), (1.9, 0.5, 1.0), (-2.2, -0.7, 0.9)]):
        sack(mb, M, (ax + dx, ay + dy, az + (0.5 if i in (6, 7) else 0.0)), 1.15, rs.uniform(0, 3), tl)
    mb.cyl(M['gold'], (ax - 0.4, ay - 1.0, az + 0.99), 0.0, 0.0, 'z', 4) if False else None
    ST['mailsacks'] = mb.finish()
    # FG inkwell desk for chamber_low
    # chandelier + sun shafts
    mb = MB('chand'); K.chandelier(mb, M, (0.0, 17.0, 8.4)); mb.finish()
    ST['shafts'] = []
    mb = MB('shafts')
    kdd = Vector(kdir_sb(P));
    for c in win_x:
        z0, z1 = 2.5, 8.0; hw = 1.4; yy = BY - 0.4
        cor = [(c - hw, yy, z0), (c + hw, yy, z0), (c + hw, yy, z1), (c - hw, yy, z1)]
        def flo(p): t = p[2] / -kdd.z; return (p[0] + kdd.x * t, p[1] + kdd.y * t, 0.02)
        fl = [flo(p) for p in cor]
        for i in range(4): j = (i + 1) % 4; mb.quad(M['shaft'], [cor[i], cor[j], fl[j], fl[i]])
    for o in mb.finish(): o.visible_shadow = False; ST['shafts'].append(o)
    lights(ST, win_x, sconces)
    # flame materials for flicker
    ST['flame_mat'] = M['flame']

def kdir_sb(P):
    import telegraph as TG; return TG.kdir(TG.CHAMBER_LIGHTS['DAY']['az'], TG.CHAMBER_LIGHTS['DAY']['el'])

def lights(ST, win_x, sconces):
    sc = bpy.context.scene; L = ST['lamps']
    for g in ('fill', 'win', 'candle', 'lamp', 'nightc'): L[g] = []
    def area(name, loc, rot, size, col, en, grp, cam=False):
        l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = size[0] * SC; l.size_y = size[1] * SC; l.color = col; l.energy = en * SC * SC
        ob = bpy.data.objects.new(name, l); ob.location = W(loc); ob.rotation_euler = rot; sc.collection.objects.link(ob); ob.visible_camera = cam; l.use_shadow = (grp != 'fill'); L[grp].append((ob, l.energy))
    def point(name, loc, col, en, grp, r=0.15):
        l = bpy.data.lights.new(name, 'POINT'); l.color = col; l.energy = en * SC * SC; l.shadow_soft_size = r * SC
        ob = bpy.data.objects.new(name, l); ob.location = W(loc); sc.collection.objects.link(ob); L[grp].append((ob, l.energy))
    area('fill', (0, 13, 12.2), (0, 0, 0), (36, 36), (0.81, 0.69, 0.53), 6500.0, 'fill')
    for k, c in enumerate(win_x): area('win%d' % k, (c, 33.3, 5.2), (-math.pi / 2, 0, 0), (2.8, 5.5), (0.19, 0.24, 0.69), 2500.0, 'win')
    for (x, y) in [(-1.4, 17), (1.4, 17), (0, 18.4), (0, 15.6)]: point('flame', (x, y, 8.6), (1.0, 0.68, 0.34), 90, 'candle')
    for (x, y, z) in sconces: point('sconce', (x, y + 0.5, z - 0.2), (1.0, 0.66, 0.3), 70, 'candle')
    point('lamp', (-0.9, 3.2, 2.3), (1.0, 0.72, 0.4), 160, 'lamp', 0.3)
    tx, ty = TABLE
    point('tablecandle', (tx - 1.9, ty - 0.5, 1.9), (1.0, 0.68, 0.32), 45, 'lamp', 0.1); point('tablecandle2', (tx - 2.1, ty - 0.2, 1.5), (1.0, 0.68, 0.32), 22, 'lamp', 0.1)
    for i, (x, y, z) in enumerate(ST['desk_candles']): point('deskc%d' % i, (x, y, z + 0.08), (1.0, 0.68, 0.32), 14, 'lamp', 0.08)
    point('daisc', (0.0, 10.4, 2.0), (1.0, 0.66, 0.3), 30, 'candle', 0.1)
    point('stoolc', (STOOL[0] + 0.45, STOOL[1] - 0.15, 1.9), (1.0, 0.62, 0.28), 70, 'nightc', 0.08); point('doorlight', (0.0, SCREEN_Y + 1.2, 2.2), (1.0, 0.7, 0.35), 60, 'candle', 0.2)

def apply_state(ST, st):
    set_tape(st.get('tape', 0.0)); set_click(st.get('click', 0)); set_moneybag(st.get('moneybag', False)); set_mailsacks(st.get('mailsacks', False)); set_flames(1.0)
    set_shafts(bool(st.get('shafts', True)) and ST['P'].get('shafts', 0.0) > 0)

# ----------------------------------------------------------------------------- hooks
def _TG():
    import telegraph as TG; return TG

def set_tape(length, clicking=None, frame=None):
    """paper tape out of the register: length 0..1 of the strip (table top -> over the edge -> loops on the floor round the stool); marks are dots and dashes only.
    clicking 0..1 (optional) also drives set_click. Key per frame."""
    TG = _TG(); g = bpy.data.node_groups.get('TG_CLIP_TAPE')
    if g is not None: TG._keysock(g.nodes['clip'].outputs[0], float(length), frame)
    if clicking is not None: set_click(clicking, frame)

def set_click(on, frame=None):
    """armature lever tilt (0..1: 0 up, 1 pulled down onto the coils); key on/off per frame for the click"""
    TG = _TG(); lv = TG.STATE['lever']; lv.rotation_euler = (0, -0.13 * float(on), 0)
    if frame is not None: TG._key(lv, 'rotation_euler', frame, 'CONSTANT')

def set_moneybag(on, frame=None, lift=0.0):
    """fat money bag on the front table (lift = height above the table in D, key a bounce with it)"""
    TG = _TG(); b = TG.STATE['moneybag']; TG._show([b] + list(b.children), bool(on), frame)
    b.location = TG.STATE['moneybag_base'] + Vector((0, 0, float(lift)))
    if frame is not None: TG._key(b, 'location', frame)

def set_mailsacks(on, frame=None):
    """sacks of letters around the front-row desk of the mocker (mark mocker_post)"""
    TG = _TG(); TG._show(TG.STATE['mailsacks'], bool(on), frame)

def set_flames(level=1.0, frame=None, flicker=0.12):
    """candle flame flicker (emission strength + lamp energy). Key per frame; level 0 snuffs the candles."""
    TG = _TG(); t = (frame if frame is not None else bpy.context.scene.frame_current)
    n = 0.5 + 0.5 * math.sin(t * 1.7) * math.sin(t * 0.63 + 1.0) + 0.25 * math.sin(t * 4.1); k = float(level) * (1.0 + flicker * (n - 0.4))
    fm = TG.STATE.get('flame_mat')
    if fm is not None: TG._keysock(fm.node_tree.nodes['Emission'].inputs['Strength'], 22.0 * k, frame)
    P = TG.STATE['P']
    for grp in ('candle', 'lamp'):
        for l, e in TG.STATE['lamps'][grp]:
            l.data.energy = e * P.get(grp, 0.0) * k
            if frame is not None: l.data.keyframe_insert('energy', frame=frame)
    TG.STATE['flame_k'] = k

def set_shafts(on, frame=None):
    """sun / moon shaft planes through the windows (DAY on, NIGHT off by default)"""
    TG = _TG(); TG._show(TG.STATE['shafts'], bool(on), frame)

def fg_desk(ST, cam, look):
    """desk-corner foreground for chamber_low: green baize top with a big inkwell + quill 1-2 D from the lens"""
    M = ST['M']; rr = rnd(3); c0 = Vector(cam[:2]); f = (Vector(look[:2]) - c0).normalized(); r = Vector((f.y, -f.x)); p = c0 + f * 1.1 - r * 0.45
    yaw = math.atan2(f.y, f.x) - math.pi / 2
    mb = MB('fgdesk'); mb.push(Matrix.Translation((p.x, p.y, 0.8)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['walnut'], (0.2, 0.0, 0.0), (1.1, 0.8, 0.06)); mb.box(M['baize'], (0.2, 0.0, 0.035), (0.95, 0.66, 0.012))
    mb.cyl(M['glassjar'], (0.0, 0.0, 0.09), 0.07, 0.12, 'z', 14, True); mb.cyl(M['ink'], (0.0, 0.0, 0.08), 0.06, 0.09, 'z', 14); mb.cyl(M['brass'], (0.0, 0.0, 0.16), 0.075, 0.025, 'z', 14)
    mb.rod(M['paper'], (0.0, 0.0, 0.14), (0.16, 0.12, 0.62), 0.008, 0.003, 5); mb.ell(M['paper'], (0.12, 0.09, 0.5), (0.03, 0.012, 0.14), (8, 6), (0, 0.2, 0.7))
    mb.box(M['paper'], (0.4, -0.12, 0.05), (0.3, 0.4, 0.03), rz=0.3); mb.box(M['paper'], (0.42, -0.1, 0.075), (0.28, 0.38, 0.03), rz=0.1)
    mb.pop(); ST['fg'] = mb.finish()

def congress_marks(ST, n=14):
    """seats of congressmen across tiers 1-3 (the desks behind the front row), evenly spread"""
    ds = [d for d in ST['desks'] if d[0] in (1, 2, 3)]; ds.sort(key=lambda d: (d[1], d[0])); out = {}
    if not ds: return out
    step = max(1, len(ds) // n); picks = ds[::step][:n]
    for i, (ti, a, px, py, zt) in enumerate(picks): out['cong_%d' % (i + 1)] = (px + 0.95 * math.cos(a), py + 0.95 * math.sin(a), zt)
    return out
