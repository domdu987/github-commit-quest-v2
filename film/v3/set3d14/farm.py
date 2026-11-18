"""set3d14 / farm.py : film 14 set ("ไอ้บ้าผึ้ง", the beehive fence, Kenyan smallholding at the savanna edge). bpy 5.x, Cycles CPU, headless.
Grown from styleboard/sb.py (the client-approved look: warm hard key, blue-violet shade, painterly noise materials, red laterite, blue Mt Kenya).
World: METRES, +x right, +y away from the camera rig, z up. Floor z 0. Camera 22 mm / 36 mm sensor (AUTO fit on the 1280 side), 720x1280, NO depth of field.
API: see API.md.   usage: python3 farm.py final|stills [preset[:LIGHT[:state]] ...]    (state tokens: fs<k> wp<t> bees<t>[/<burst>] uf<k> uh<k> cr<k>)
"""
import os, sys, math, time, json, hashlib
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import farm_geo as G
from farm_geo import MB, mat, mat_emit, mat_glow, mat_card, hexc, rnd, R, palette, join_objs
W, H = 720, 1280
WORK = os.path.join(HERE, 'farm_work'); TEX = os.path.join(HERE, 'tex'); os.makedirs(WORK, exist_ok=True); os.makedirs(TEX, exist_ok=True)

# ============================================================================ the fence ring (hero field)
RX0, RX1, RY0, RY1 = -14.0, 11.0, 5.0, 25.5          # ring corners (the wire's plan), outside = away from the field
WIRE_Z = 2.0; WIRE_OFF = 0.09; WIRE_R = 0.038
SIDES = [((RX0, RY0), (1, 0), RX1 - RX0, 5), ((RX1, RY0), (0, 1), RY1 - RY0, 3), ((RX1, RY1), (-1, 0), RX1 - RX0, 5), ((RX0, RY1), (0, -1), RY1 - RY0, 3)]
S_TOT = sum(s[2] for s in SIDES); S_CORNER = np.cumsum([0.0] + [s[2] for s in SIDES])
def ring_at(s):
    """(pos xy, tangent, normal-into-field, side index) at arc length s (mod S_TOT) from the front-left corner, counter-clockwise."""
    s = s % S_TOT; k = int(np.searchsorted(S_CORNER, s, side='right') - 1); k = min(k, 3); (p0, t, L, n) = SIDES[k]; u = s - S_CORNER[k]
    return (p0[0] + t[0] * u, p0[1] + t[1] * u), t, (-t[1], t[0]), k
UNITS = []                                            # 16 hive units: front 5, right 3, back 5, left 3
for k, (p0, t, L, n) in enumerate(SIDES):
    for j in range(n):
        s = S_CORNER[k] + (j + 0.5) * L / n; pos, tt, nn, _ = ring_at(s)
        UNITS.append(dict(i=len(UNITS), s=s, pos=pos, t=tt, n=nn, yaw=math.atan2(tt[1], tt[0]), side=k))
UNIT_ORDER = [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]     # stage 1 = unit 1 (front, x -6.5), stage 2 = the first ten, stage 3 = all 16
STAGE_UNITS = {0: [], 1: UNIT_ORDER[:1], 2: UNIT_ORDER[:10], 3: UNIT_ORDER[:]}
POST_S = sorted(set([round(u['s'] + d, 4) for u in UNITS for d in (-1.0, 1.0)] + [float(c) for c in S_CORNER[:4]]))
_ps = []
for a, b in zip(POST_S, POST_S[1:] + [POST_S[0] + S_TOT]):                      # intermediate posts: no free span longer than 3.7 m
    _ps.append(a)
    if b - a > 3.7:
        n = int(math.ceil((b - a) / 3.7)); _ps += [a + (b - a) * q / n for q in range(1, n)]
POST_S = sorted(set(round(x % S_TOT, 4) for x in _ps)); PUSH_S0 = 1.0 + 14.0              # push point: front row x = 1.0, mid-span between unit 2 and 3
SEQ_T = 5.0                                                                      # seconds covered by t 0..1 of set_wire_push / set_bees
WAVE_C = 15.0; WAVE_F = 1.1; WAVE_D = 1.3; PUSH_A = 0.95

def _post_dist(s):
    d = np.abs(np.asarray(POST_S)[None, :] - np.asarray(s)[:, None]); d = np.minimum(d, S_TOT - d); return d.min(1)
def _ring_dist(s, s0):
    d = np.abs(np.asarray(s) - s0) % S_TOT; return np.minimum(d, S_TOT - d)
def _q(tau):
    """wire displacement profile of the push (unit): 0 before the wave arrives, bows in over 0.55 s, then rings down (cosine, damped)."""
    tau = np.asarray(tau, dtype=float); rise = 0.55; x = np.clip(tau / rise, 0, 1); bow = x * x * (3 - 2 * x)
    u = np.maximum(tau - rise, 0.0); ring = np.cos(2 * math.pi * WAVE_F * u) * np.exp(-u / WAVE_D)
    return np.where(tau <= 0, 0.0, np.where(tau < rise, bow, ring))
def _h(tau):
    tau = np.asarray(tau, dtype=float); return np.where(tau <= 0, 0.0, np.sin(2 * math.pi * 1.0 * tau) * np.exp(-np.maximum(tau, 0) / 1.5))
def _amp(d): return np.exp(-np.asarray(d) / 30.0)
def wire_z(s):
    """sag between neighbouring posts (post-to-post span)."""
    ps = np.asarray(POST_S + [POST_S[0] + S_TOT]); s = np.asarray(s) % S_TOT; k = np.clip(np.searchsorted(ps, s, side='right') - 1, 0, len(ps) - 2)
    u = (s - ps[k]) / np.maximum(ps[k + 1] - ps[k], 1e-6); L = ps[k + 1] - ps[k]; return WIRE_Z - 0.035 * L * 4 * u * (1 - u)
def wire_disp(s, t, s0=None):
    """horizontal displacement of the wire (m, along the inward normal) at arc s, time t (0..1 of SEQ_T). t < 0: at rest."""
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s)
    s0 = PUSH_S0 if s0 is None else s0; d = _ring_dist(s, s0); env = 1 - 0.7 * np.exp(-(_post_dist(s) / 0.45) ** 2)
    return PUSH_A * env * _amp(d) * _q(t * SEQ_T - d / WAVE_C)
def hive_swing(s, t, s0=None):
    """(swing angle about the wire tangent, twist about z) of the hive hanging at arc s."""
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s), np.zeros_like(s)
    s0 = PUSH_S0 if s0 is None else s0; d = _ring_dist(s, s0); tau = t * SEQ_T - d / WAVE_C - 0.12
    return 0.72 * _amp(d) * _h(tau), 0.22 * _amp(d) * np.where(tau <= 0, 0.0, np.sin(2 * math.pi * 1.7 * tau) * np.exp(-np.maximum(tau, 0) / 1.2))

# ============================================================================ light states
def kdir(az, el):
    a = math.radians(az); e = math.radians(el); return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))
LIGHTS = dict(
 DAY=dict(sky=[(0.0, '#8aa3d8'), (0.42, '#e9b98c'), (0.5, '#f7d49c'), (0.56, '#f0d8b4'), (0.64, '#a9c6ec'), (0.8, '#5a8ee0'), (1.0, '#3a68c8')], sky_k=1.0,
          key=(1.0, 0.78, 0.5, 4.2), key_dir=kdir(-60, 27), sun_angle=1.0, exposure=-0.10, sat=1.12, fill=(1.0, 0.62, 0.36, 0.9), mount_x=250, card_k=1.0,
          hills=[(120, 6, 14, '#9a8fc0'), (170, 18, 26, '#8d9cca'), (205, 30, 30, '#7f9ed0')], hill_k=1.0, mount='#6f8fd4', cap='#f7e6dc', clouds=1.0, cloud_col=1.0, birds=True,
          lamps=[((24.0, 8.5, 0.9), (1.0, 0.5, 0.2), 120, 0.3)]),
 MORNING=dict(sky=[(0.0, '#8fa0d4'), (0.42, '#f0c29c'), (0.5, '#fbdcae'), (0.56, '#f6e2c6'), (0.64, '#b6d2f0'), (0.8, '#6fa6ec'), (1.0, '#4a7ed4')], sky_k=1.0,
          key=(1.0, 0.80, 0.55, 3.8), key_dir=kdir(64, 17), sun_angle=1.2, exposure=-0.06, sat=1.12, fill=(1.0, 0.7, 0.45, 0.7), mount_x=250, card_k=1.0,
          hills=[(120, 6, 14, '#a8a0c8'), (170, 18, 26, '#9aa8d2'), (205, 30, 30, '#88a8d8')], hill_k=1.0, mount='#7a98d8', cap='#fbeee4', clouds=1.0, cloud_col=1.0, birds=True,
          lamps=[((24.0, 8.5, 0.9), (1.0, 0.5, 0.2), 200, 0.3)]),
 DUSK=dict(sky=[(0.0, '#2c3a82'), (0.44, '#d9806e'), (0.5, '#f4a868'), (0.58, '#6a74c0'), (1.0, '#1d2d78')], sky_k=0.9,
          key=(1.0, 0.55, 0.3, 3.4), key_dir=kdir(-115, 8), sun_angle=1.0, exposure=-0.02, sat=1.12, fill=(1.0, 0.5, 0.3, 1.0), mount_x=250, card_k=0.95,
          hills=[(120, 6, 14, '#6a5a98'), (170, 18, 26, '#5f6aa8'), (205, 30, 30, '#5470b0')], hill_k=0.85, mount='#4a62a8', cap='#e8b8b0', clouds=0.8, cloud_col=0.7, birds=False,
          lamps=[((1.3, 0.5, 0.55), (1.0, 0.5, 0.18), 420, 0.25), ((1.9, 2.8, 2.1), (1.0, 0.6, 0.26), 420, 0.12), ((18.2, 11.5, 1.6), (1.0, 0.62, 0.28), 420, 0.15),
                 ((24.0, 8.6, 1.0), (1.0, 0.5, 0.2), 500, 0.3), ((30.5, 18.3, 1.8), (1.0, 0.65, 0.3), 420, 0.15), ((21.5, 20.0, 1.5), (1.0, 0.6, 0.3), 300, 0.15),
                 ((-30.0, 27.0, 1.6), (1.0, 0.62, 0.28), 300, 0.15)]),
 NIGHT=dict(sky=[(0.0, '#2a2a6c'), (0.46, '#38418a'), (0.52, '#52589e'), (0.6, '#2c3178'), (1.0, '#181a58')], sky_k=2.0, stars=True,
          key=(0.50, 0.60, 1.0, 3.2), key_dir=kdir(-12, 33), sun_angle=1.2, exposure=0.0, sat=1.12, fill=(0.5, 0.45, 0.8, 0.5), mount_x=-100, card_k=0.9,
          hills=[(120, 6, 14, '#2c3274'), (170, 18, 26, '#272e72'), (205, 30, 30, '#232b70')], hill_k=0.95, mount='#2a3478', cap='#8a9cd8', clouds=0.5, cloud_col=0.5, birds=False, moon=True,
          lamps=[((1.3, 0.5, 0.55), (1.0, 0.5, 0.18), 650, 0.25), ((1.9, 2.8, 2.1), (1.0, 0.6, 0.26), 700, 0.12), ((18.2, 11.5, 1.6), (1.0, 0.62, 0.28), 900, 0.15),
                 ((24.0, 8.6, 1.0), (1.0, 0.5, 0.2), 700, 0.3), ((30.5, 18.3, 1.8), (1.0, 0.65, 0.3), 700, 0.15), ((21.5, 20.0, 1.5), (1.0, 0.6, 0.3), 450, 0.15),
                 ((-30.0, 27.0, 1.6), (1.0, 0.62, 0.28), 600, 0.15), ((-21.6, 1.4, 1.0), (1.0, 0.6, 0.28), 350, 0.12), ((-5.0, 3.6, 1.1), (1.0, 0.62, 0.3), 160, 0.1)]),
)
LIGHT_NAMES = list(LIGHTS)

# ============================================================================ ground / sky / hills
def ground(light):
    S = 1280; x0, x1, y0, y1 = -64.0, 64.0, -40.0, 88.0
    im = Image.new('RGB', (S, S), (0, 0, 0)); d = ImageDraw.Draw(im)
    def px(x, y): return ((x - x0) / (x1 - x0) * S, (1 - (y - y0) / (y1 - y0)) * S)
    def line(pts, w, col=(255, 0, 0)): d.line([px(*p) for p in pts], fill=col, width=max(1, int(w / (x1 - x0) * S)), joint='curve')
    def disc(c, r, col=(255, 0, 0)): a = px(c[0] - r, c[1] + r); b = px(c[0] + r, c[1] - r); d.ellipse([a, b], fill=col)
    line([(-64, -3), (-30, -2.5), (0, -3.2), (30, -2.2), (64, -3)], 4.2)
    line([(-14, 2.6), (14, 2.6)], 2.0); line([(-30, 1.8), (-14, 2.6)], 1.6)
    line([(3.6, -9), (3.4, -4), (2.2, 1), (0.6, 5)], 2.6)
    line([(2.95, -9), (2.75, -4), (1.6, 1), (0.0, 5)], 0.3, (255, 0, 255)); line([(4.25, -9), (4.05, -4), (2.8, 1), (1.2, 5)], 0.3, (255, 0, 255))
    line([(15, -3), (15.5, 5), (17, 12), (19, 18)], 2.2); line([(15.5, 6), (30, 8), (40, 6)], 1.6)
    line([(10.8, 3), (10.8, 26)], 1.4); line([(-14.8, 3), (-14.8, 26)], 1.2); line([(-17.5, 3), (-17.5, 30)], 1.6)
    line([(-22, -3), (-23, 4)], 1.6); line([(-34, -3), (-34.5, 30)], 1.2)
    disc((20, 14), 7.5); disc((29, 10), 4); disc((22, 21), 4); disc((-4, 0.5), 6.5); disc((-26, 1.0), 4); disc((-35, 31), 5); disc((36, 8), 5)
    d.rectangle([px(-13.2, 25.3), px(10.2, 4.7)], fill=(0, 255, 0)); d.rectangle([px(-46.2, 26.0), px(-21.4, 5.8)], fill=(0, 255, 0))
    im = im.filter(ImageFilter.GaussianBlur(2)); p = os.path.join(TEX, 'mask_ground.png'); im.save(p)
    img = bpy.data.images.load(p); img.colorspace_settings.name = 'Non-Color'
    me = bpy.data.meshes.new('ground'); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=420); bm.to_mesh(me)
    ob = bpy.data.objects.new('ground', me); ob.location = (0, 60, 0); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); L(tc.outputs['Object'], mp.inputs[0])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.1; nz.inputs['Detail'].default_value = 6; L(mp.outputs[0], nz.inputs[0])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 7; nz2.inputs['Detail'].default_value = 5; L(mp.outputs[0], nz2.inputs[0])
    sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
    mx_ = N('ShaderNodeMath'); mx_.operation = 'MULTIPLY_ADD'; L(sp.outputs['X'], mx_.inputs[0]); mx_.inputs[1].default_value = 1 / (x1 - x0); mx_.inputs[2].default_value = (0 - x0) / (x1 - x0)
    my_ = N('ShaderNodeMath'); my_.operation = 'MULTIPLY_ADD'; L(sp.outputs['Y'], my_.inputs[0]); my_.inputs[1].default_value = 1 / (y1 - y0); my_.inputs[2].default_value = (60 - y0) / (y1 - y0)
    cu = N('ShaderNodeCombineXYZ'); L(mx_.outputs[0], cu.inputs['X']); L(my_.outputs[0], cu.inputs['Y'])
    wp = N('ShaderNodeVectorMath'); wp.operation = 'ADD'; L(cu.outputs[0], wp.inputs[0])
    wn = N('ShaderNodeTexNoise'); wn.inputs['Scale'].default_value = 25; wn.inputs['Detail'].default_value = 3; L(mp.outputs[0], wn.inputs[0])
    sc_ = N('ShaderNodeVectorMath'); sc_.operation = 'SCALE'; sc_.inputs['Scale'].default_value = 0.010; L(wn.outputs['Color'], sc_.inputs[0]); L(sc_.outputs[0], wp.inputs[1])
    ti = N('ShaderNodeTexImage'); ti.image = img; ti.extension = 'EXTEND'; ti.interpolation = 'Linear'; L(wp.outputs[0], ti.inputs['Vector'])
    sm = N('ShaderNodeSeparateColor'); L(ti.outputs['Color'], sm.inputs[0])
    def mixc(fac, A, B):
        x = N('ShaderNodeMix'); x.data_type = 'RGBA'; x.inputs[6].default_value = hexc(A); x.inputs[7].default_value = hexc(B); L(fac, x.inputs[0]); return x
    ramp = N('ShaderNodeValToRGB'); L(nz.outputs['Fac'], ramp.inputs[0]); ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[1].position = 0.65
    grass = mixc(ramp.outputs[0], '#8a9436', '#cdb256')
    ramp2 = N('ShaderNodeValToRGB'); L(nz2.outputs['Fac'], ramp2.inputs[0]); ramp2.color_ramp.elements[0].position = 0.4; ramp2.color_ramp.elements[1].position = 0.6
    redd = mixc(ramp2.outputs[0], '#b0583a', '#cf7e4c'); soil = mixc(ramp2.outputs[0], '#8f4a2c', '#ad5e36')
    # furrows in the fields: sin(x * 2pi / 0.95)
    fx = N('ShaderNodeMath'); fx.operation = 'MULTIPLY'; fx.inputs[1].default_value = 2 * math.pi / 0.95; L(sp.outputs['X'], fx.inputs[0])
    fs = N('ShaderNodeMath'); fs.operation = 'SINE'; L(fx.outputs[0], fs.inputs[0])
    fr = N('ShaderNodeMapRange'); fr.inputs['From Min'].default_value = -1; fr.inputs['From Max'].default_value = 1; fr.inputs['To Min'].default_value = 0.72; fr.inputs['To Max'].default_value = 1.05; L(fs.outputs[0], fr.inputs['Value'])
    sm2 = N('ShaderNodeMix'); sm2.data_type = 'RGBA'; sm2.blend_type = 'MULTIPLY'; L(soil.outputs[2], sm2.inputs[6]); L(fr.outputs['Result'], sm2.inputs[7]); sm2.inputs[0].default_value = 1.0
    m1 = N('ShaderNodeMix'); m1.data_type = 'RGBA'; L(grass.outputs[2], m1.inputs[6]); L(sm2.outputs[2], m1.inputs[7]); L(sm.outputs['Green'], m1.inputs[0])
    m2 = N('ShaderNodeMix'); m2.data_type = 'RGBA'; L(m1.outputs[2], m2.inputs[6]); L(redd.outputs[2], m2.inputs[7]); L(sm.outputs['Red'], m2.inputs[0])
    rb = N('ShaderNodeMath'); rb.operation = 'MULTIPLY'; rb.inputs[1].default_value = 0.75; L(sm.outputs['Blue'], rb.inputs[0])
    m3 = N('ShaderNodeMix'); m3.data_type = 'RGBA'; m3.blend_type = 'MULTIPLY'; L(m2.outputs[2], m3.inputs[6]); m3.inputs[7].default_value = (0.3, 0.25, 0.24, 1); L(rb.outputs[0], m3.inputs[0])
    nz3 = N('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 55; nz3.inputs['Detail'].default_value = 8; L(mp.outputs[0], nz3.inputs[0])
    r3 = N('ShaderNodeValToRGB'); L(nz3.outputs['Fac'], r3.inputs[0]); r3.color_ramp.elements[0].position = 0.3; r3.color_ramp.elements[0].color = (0.7, 0.7, 0.7, 1); r3.color_ramp.elements[1].position = 0.7; r3.color_ramp.elements[1].color = (1.14, 1.14, 1.14, 1)
    m4 = N('ShaderNodeMix'); m4.data_type = 'RGBA'; m4.blend_type = 'MULTIPLY'; m4.inputs[0].default_value = 0.85; L(m3.outputs[2], m4.inputs[6]); L(r3.outputs[0], m4.inputs[7])
    L(m4.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

def sky(P):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]: e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    if P.get('stars'):
        vo = N('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 260; vo.feature = 'F1'; L(tc.outputs['Generated'], vo.inputs[0])
        sr = N('ShaderNodeValToRGB'); sr.color_ramp.elements[0].position = 0.0; sr.color_ramp.elements[1].position = 0.035; sr.color_ramp.elements[0].color = (1, 1, 1, 1); sr.color_ramp.elements[1].color = (0, 0, 0, 1); L(vo.outputs['Distance'], sr.inputs[0])
        zm = N('ShaderNodeMapRange'); L(sp.outputs['Z'], zm.inputs['Value']); zm.inputs['From Min'].default_value = 0.6; zm.inputs['From Max'].default_value = 0.8
        mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(sr.outputs[0], mu.inputs[0]); L(zm.outputs['Result'], mu.inputs[1])
        ma = N('ShaderNodeMath'); ma.operation = 'MULTIPLY'; ma.inputs[1].default_value = 9.0; L(mu.outputs[0], ma.inputs[0])
        ad = N('ShaderNodeMix'); ad.data_type = 'RGBA'; ad.blend_type = 'ADD'; L(cr.outputs[0], ad.inputs[6]); ad.inputs[7].default_value = (0.8, 0.9, 1.0, 1); L(ma.outputs[0], ad.inputs[0]); L(ad.outputs[2], bg.inputs['Color'])
    L(bg.outputs[0], out.inputs['Surface'])

def hills(light, P):
    mb = MB('hills'); rr = rnd(3)
    for li, (yy, bh, amp, col) in enumerate(P['hills']):
        m = mat_emit('hill%d_%s' % (li, light), col, P['hill_k']); n = 150; xs = np.linspace(-420, 420, n); ph = [rr.uniform(0, 6) for _ in range(4)]
        hs = [bh + amp * (0.5 * math.sin(x / 55 + ph[0]) + 0.3 * math.sin(x / 23 + ph[1]) + 0.15 * math.sin(x / 9 + ph[2])) for x in xs]
        for i in range(n - 1): mb.quad(m, [(xs[i], yy, -5), (xs[i + 1], yy, -5), (xs[i + 1], yy, hs[i + 1]), (xs[i], yy, hs[i])])
    m = mat_emit('mount_%s' % light, P['mount'], P['hill_k']); cx = P['mount_x']; base = 230
    prof = [(-190, 0), (-110, 22), (-60, 52), (-34, 70), (-26, 78), (-18, 84), (-10, 92), (-4, 97), (0, 98), (5, 94), (10, 90), (20, 80), (28, 74), (45, 62), (62, 50), (110, 24), (190, 0)]
    for (a, b) in zip(prof[:-1], prof[1:]): mb.quad(m, [(cx + a[0], base, -5), (cx + b[0], base, -5), (cx + b[0], base, b[1]), (cx + a[0], base, a[1])])
    # shaded flank (second, darker plane in front gives the mountain a lit/shade split) + cap
    m2 = mat_emit('mountsh_%s' % light, P['hills'][2][3], P['hill_k'])
    for (a, b) in zip(prof[:-1], prof[1:]):
        if a[0] >= -4: mb.quad(m2, [(cx + a[0], base - 0.5, -5), (cx + b[0], base - 0.5, -5), (cx + b[0], base - 0.5, b[1] * 0.98), (cx + a[0], base - 0.5, a[1] * 0.98)])
    ms = mat_emit('cap_%s' % light, P['cap'], P['hill_k'])
    mb.quad(ms, [(cx - 11, base - 1, 86), (cx + 11, base - 1, 84), (cx + 2, base - 1, 97.5), (cx - 3, base - 1, 97)])
    mb.finish()

def clouds(M, light, P):
    """cartoon cumulus (lit spheres): fills the sky above the horizon at every azimuth."""
    k = P['clouds']
    if k <= 0: return
    mb = MB('clouds'); rr = rnd(77); n = int(16 * k) + 4
    for i in range(n):
        az = rr.uniform(0, 2 * math.pi) if i > 5 else rr.uniform(-0.9, 0.9) + 1.5708; r = rr.uniform(230, 360); h = rr.uniform(35, 120) * (0.7 if i % 3 == 0 else 1.0)
        G.cloud_puff(mb, M, (math.cos(az) * r, 60 + math.sin(az) * r * (1.2 if math.sin(az) > 0 else 0.6), h), rr.uniform(11, 26), i)
    mb.finish(shadow=False)

def birds(M):
    mb = MB('birds'); rr = rnd(21)
    for i in range(9):
        c = (rr.uniform(-18, 6) + i * 0.7, rr.uniform(55, 90) - i * 1.2, rr.uniform(15, 26) + (i % 3) * 1.2); G.bird(mb, M, c, 0.5 + rr.uniform(-.3, .3), rr.uniform(0.2, 0.7), 0.55)
    mb.finish(shadow=False)
