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

# ============================================================================ state + helpers
STATE = {}
def _coll(): return bpy.context.scene.collection
def _hide(ob, on):
    ob.hide_render = bool(on); ob.hide_viewport = bool(on)
def _sm(x): x = float(np.clip(x, 0, 1)); return x * x * (3 - 2 * x)

# ============================================================================ the beehive fence: posts, roofs, hives, bars, the one wire
def hive_local(mb, M, ropes=True):
    """top-bar hive hanging 0.68 below its pivot (the wire): long trapezoid box, top bars, end slots + landing boards, battens, two ropes. Local x = along the wire."""
    L, Wd, Hh = 1.25, 0.42, 0.34; hz = -0.68
    vt = [(-L / 2, -Wd / 2, hz + Hh / 2), (L / 2, -Wd / 2, hz + Hh / 2), (L / 2, Wd / 2, hz + Hh / 2), (-L / 2, Wd / 2, hz + Hh / 2)]
    vb = [(-L / 2 + 0.03, -Wd * 0.18, hz - Hh / 2), (L / 2 - 0.03, -Wd * 0.18, hz - Hh / 2), (L / 2 - 0.03, Wd * 0.18, hz - Hh / 2), (-L / 2 + 0.03, Wd * 0.18, hz - Hh / 2)]
    mb.quad(M['hive'], vt[::-1]); mb.quad(M['hive'], vb)
    for i in range(4): j = (i + 1) % 4; mb.quad(M['hive'], [vb[i], vb[j], vt[j], vt[i]])
    for i in range(10): mb.box(M['hivetop'], (-L / 2 + 0.07 + i * 0.12, 0, hz + Hh / 2 + 0.014), (0.115, Wd + 0.05, 0.028))
    for sy in (-1, 1):
        for i in range(4):
            x = -L / 2 + 0.2 + i * 0.28; mb.quad(M['woodpale'], [(x - 0.03, sy * (Wd / 2 + 0.004), hz + Hh / 2), (x + 0.03, sy * (Wd / 2 + 0.004), hz + Hh / 2), (x + 0.025, sy * (Wd * 0.18 + 0.004), hz - Hh / 2), (x - 0.025, sy * (Wd * 0.18 + 0.004), hz - Hh / 2)])
    for ex in (-1, 1):
        for dz in (0.04, -0.05): mb.box(M['dark'], (ex * (L / 2 + 0.004), 0.0, hz + dz), (0.014, 0.15, 0.028))
        mb.box(M['woodpale'], (ex * (L / 2 + 0.05), 0, hz - 0.1), (0.1, 0.3, 0.025))
    if ropes:
        for sx in (-0.45, 0.45): mb.rod(M['rope'], (sx, 0, -0.0), (sx * 0.96, 0, hz + Hh / 2 + 0.03), 0.017, 0.017, 5)
def bar_local(mb, M):
    mb.box(M['wood'], (0, 0, 0), (0.95, 0.07, 0.07))
    for sx in (-0.45, 0.45): mb.box(M['metal'], (sx, 0, 0), (0.05, 0.1, 0.1)); mb.ell(M['metal'], (sx, 0, -0.03), (0.04, 0.04, 0.04), (6, 4))
def roof_local(mb, M):
    """pitched corrugated-tin roof (real sine ribs), warm planked underside, crossbeam, sedge ridge cap; local origin on the ring line, z absolute."""
    rw = 0.98; rh = 0.34; x0 = -1.4; ln = 2.8; sl = math.hypot(rw, rh)
    for sgn in (-1, 1):
        o = (x0, sgn * rw, 2.48); dv = Vector((0, -sgn * rw, rh)).normalized(); nv = Vector((0, sgn * rh, rw)).normalized()
        mb.corrugated(M['tin'], o, dv, (1, 0, 0), nv, sl, ln, 0.09, 0.022)
        mb.corrugated(M['tinunder'], Vector(o) - nv * 0.035, dv, (1, 0, 0), -nv, sl, ln, 0.09, 0.012)
        mb.box(M['woodpale'], (0, sgn * (rw + 0.0), 2.46), (ln, 0.06, 0.07))
    for ex in (x0, x0 + ln): mb.tri(M['tinunder'], [(ex, -rw, 2.48), (ex, rw, 2.48), (ex, 0, 2.48 + rh)])
    mb.box(M['thatchold'], (0, 0, 2.48 + rh + 0.03), (ln + 0.1, 0.16, 0.09)); mb.box(M['wood'], (0, 0, 2.38), (2.3, 0.1, 0.1))
    for dx in (-1.0, 1.0): mb.rod(M['wood'], (dx, -0.0, 2.38), (dx, 0, 2.48), 0.03, 0.03, 5)

def build_fence(M):
    sc = bpy.context.scene; rr = rnd(31)
    # posts (always there: stage 0 = posts only)
    mb = MB('posts')
    unit_s = {round(u['s'] + d, 4): u for u in UNITS for d in (-1.0, 1.0)}
    for s in POST_S:
        (x, y), t, n, _ = ring_at(s); h = 2.58 if round(s, 4) in unit_s else 2.45; lean = rr.uniform(-0.035, 0.035)
        mb.rod(M['wood'], (x, y, -0.15), (x + lean * h * n[0], y + lean * h * n[1], h), 0.075, 0.062, 7, smooth=True)
        mb.ell(M['woodpale'], (x + lean * h * n[0], y + lean * h * n[1], h + 0.01), (0.07, 0.07, 0.025), (6, 4))
        mb.box(M['metal'], (x - n[0] * 0.07, y - n[1] * 0.07, WIRE_Z), (0.05, 0.05, 0.1) if abs(n[0]) < 0.5 else (0.05, 0.05, 0.1))
        for q in range(3): a = rr.random() * 6.28; mb.ell(M['stonewarm'], (x + math.cos(a) * 0.16, y + math.sin(a) * 0.16, 0.05), (0.1, 0.08, 0.06), (6, 4))     # packed stones at the foot
    mb.finish()
    # roofs by tier (visible with the hive)
    tiers = {1: STAGE_UNITS[1], 2: [u for u in STAGE_UNITS[2] if u not in STAGE_UNITS[1]], 3: [u for u in STAGE_UNITS[3] if u not in STAGE_UNITS[2]]}
    STATE['roofs'] = {}
    for tk, ids in tiers.items():
        mb = MB('roof%d' % tk)
        for i in ids:
            u = UNITS[i]; mb.push(Matrix.Translation((u['pos'][0], u['pos'][1], 0)) @ Euler((0, 0, u['yaw'])).to_matrix().to_4x4()); roof_local(mb, M); mb.pop()
        STATE['roofs'][tk] = mb.finish(join=True)
    # hives + bars
    STATE['hive'] = {}; STATE['bar'] = {}
    mh = MB('hive'); hive_local(mh, M); hproto = mh.finish(join=True)[0]
    mbp = MB('bar'); bar_local(mbp, M); bproto = mbp.finish(join=True)[0]
    for u in UNITS:
        h = bpy.data.objects.new('hive_%d' % u['i'], hproto.data); sc.collection.objects.link(h); b = bpy.data.objects.new('bar_%d' % u['i'], bproto.data); sc.collection.objects.link(b)
        STATE['hive'][u['i']] = h; STATE['bar'][u['i']] = b
    bpy.data.objects.remove(hproto); bpy.data.objects.remove(bproto)
    # wire (rebuilt every call of _update_fence)
    keys = sorted(set(POST_S + [round(u['s'], 4) for u in UNITS] + [round(u['s'] + d, 4) for u in UNITS for d in (-0.45, 0.45)]))
    nodes = []
    for a, b in zip(keys, keys[1:] + [keys[0] + S_TOT]):
        n = max(1, int(math.ceil((b - a) / 0.45))); nodes += [a + (b - a) * q / n for q in range(n)]
    nodes.append(nodes[0] + S_TOT); S = np.array(nodes)
    base = np.zeros((len(S), 3)); nrm = np.zeros((len(S), 2)); cs = [float(c) for c in S_CORNER[:4]]
    for k, s in enumerate(S):
        sm = s % S_TOT; ci = [i for i, c in enumerate(cs) if abs(sm - c) < 1e-6 or abs(sm - c - S_TOT) < 1e-6]
        if ci:
            c = ci[0]; (p, t, n, _) = ring_at(cs[c] + 1e-4); pn = SIDES[(c - 1) % 4][1]; nprev = (-pn[1], pn[0]); nn = np.array(n) + np.array(nprev); nn = nn / np.linalg.norm(nn)
            pos = np.array(p) - np.array(n) * WIRE_OFF - np.array(nprev) * WIRE_OFF; base[k] = (pos[0], pos[1], WIRE_Z); nrm[k] = nn
        else:
            (p, t, n, _) = ring_at(s); base[k] = (p[0] - n[0] * WIRE_OFF, p[1] - n[1] * WIRE_OFF, 0); nrm[k] = n
    base[:, 2] = wire_z(S)
    seg_unit = np.full(len(S) - 1, -1)
    for k in range(len(S) - 1):
        sm = ((S[k] + S[k + 1]) / 2) % S_TOT
        for u in UNITS:
            if abs(sm - u['s']) < 1.0: seg_unit[k] = u['i']
    STATE['wire'] = dict(S=S, base=base, nrm=nrm, seg_unit=seg_unit)
    me = bpy.data.meshes.new('wire'); ob = bpy.data.objects.new('wire', me); ob.data.materials.append(M['wire']); sc.collection.objects.link(ob); STATE['wire_ob'] = ob
    STATE['stage'] = 3; STATE['push_t'] = -1.0; STATE['push_s0'] = PUSH_S0

def _pivot(i, t, s0=None):
    u = UNITS[i]; (p, tt, n, _) = ring_at(u['s']); d = float(wire_disp([u['s']], t, s0)[0]); z = float(wire_z([u['s']])[0])
    return Vector((p[0] - n[0] * WIRE_OFF + n[0] * d, p[1] - n[1] * WIRE_OFF + n[1] * d, z))

def _update_fence():
    """pose every hive + bar and rebuild the wire mesh for the current stage and push time."""
    t = STATE['push_t']; s0 = STATE['push_s0']; stage = STATE['stage']; vis = STAGE_UNITS[stage]
    for u in UNITS:
        i = u['i']; h = STATE['hive'][i]; b = STATE['bar'][i]; on = i in vis; _hide(h, not on); _hide(b, not on)
        if not on: continue
        pv = _pivot(i, t, s0); th, tw = hive_swing([u['s']], t, s0); b.location = pv; b.rotation_euler = (0, 0, u['yaw']); h.location = pv; h.rotation_euler = (float(th[0]), 0, u['yaw'] + float(tw[0]))
    for tk, objs in STATE['roofs'].items():
        for o in objs: _hide(o, not (stage >= tk))
    W_ = STATE['wire']; S = W_['S']; base = W_['base']; d = wire_disp(S, t, s0) if t >= 0 else np.zeros(len(S))
    P = base.copy(); P[:, 0] += W_['nrm'][:, 0] * d; P[:, 1] += W_['nrm'][:, 1] * d
    show = np.array([(stage >= 3) or (su >= 0 and su in vis) for su in W_['seg_unit']])
    tg = np.gradient(P, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1, keepdims=True), 1e-9)
    up = np.array([0, 0, 1.0]); sd = np.cross(tg, up); sd /= np.maximum(np.linalg.norm(sd, axis=1, keepdims=True), 1e-9); uu = np.cross(sd, tg)
    NS = 6; ang = np.linspace(0, 2 * math.pi, NS, endpoint=False); verts = np.zeros((len(S), NS, 3))
    for q, a in enumerate(ang): verts[:, q] = P + WIRE_R * (math.cos(a) * sd + math.sin(a) * uu)
    faces = []
    for k in range(len(S) - 1):
        if not show[k]: continue
        for q in range(NS): q2 = (q + 1) % NS; faces.append((k * NS + q, k * NS + q2, (k + 1) * NS + q2, (k + 1) * NS + q))
    me = STATE['wire_ob'].data; me.clear_geometry(); me.from_pydata(verts.reshape(-1, 3).tolist(), [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    _hide(STATE['wire_ob'], stage < 1)
    if STATE.get('bees_args'): _bees_apply(*STATE['bees_args'])

# ----------------------------------------------------------------------------- bees (one mesh rebuilt per call: gold-black spindles + wing triangles)
BEE_PER_HIVE = 150; BEE_L = 0.075
def _bee_seed():
    rr = np.random.RandomState(14); n = BEE_PER_HIVE * 16
    d = rr.normal(size=(n, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True); d[:, 2] = np.abs(d[:, 2]) * 0.8 + 0.3
    return dict(u=rr.rand(n), dir=d, spd=rr.uniform(0.6, 1.6, n), ph=rr.uniform(0, 6.283, n), om=rr.uniform(1.8, 4.5, n), orr=rr.uniform(0.5, 1.9, n), jit=rr.uniform(0, 6.283, (n, 3)), zlift=rr.uniform(0.6, 2.2, n))
_BS = None
def _bees_apply(t, burst, target, local):
    """t: 0..1 of SEQ_T (< 0 = sleeping only). burst: 0..1 share of the cloud shown. target: world point the swarms stream toward (the elephant's eyes). local=(centre, radius, n): an extra cloud."""
    global _BS
    if _BS is None: _BS = _bee_seed()
    S_ = _BS; vis = STAGE_UNITS[STATE['stage']]; sc = bpy.context.scene
    if STATE.get('bees_ob') is None:
        STATE['bees_ob'] = []
    for o in STATE['bees_ob']:
        me = o.data; bpy.data.objects.remove(o); bpy.data.meshes.remove(me)
    STATE['bees_ob'] = []
    if not vis: return
    sec = t * SEQ_T; pts = []; asleep = []
    ent = []; hid = []
    for i in vis:
        u = UNITS[i]; h = STATE['hive'][i]; mw = h.matrix_world; dly = float(_ring_dist([u['s']], STATE['push_s0'])[0]) / WAVE_C + 0.15
        for ex in (-1, 1): ent.append((mw @ Vector((ex * 0.66, 0, -0.68)), ex, u, dly, (mw.to_3x3() @ Vector((ex, 0, 0)))))
    allp = []; allsleep = []
    idx = 0
    for (e, ex, u, dly, outv) in ent:
        i = u['i']; sl = slice(i * BEE_PER_HIVE + (0 if ex < 0 else BEE_PER_HIVE // 2), i * BEE_PER_HIVE + (BEE_PER_HIVE // 2 if ex < 0 else BEE_PER_HIVE))
        u_ = S_['u'][sl]; dr = S_['dir'][sl].copy(); n = len(u_); age = sec - dly
        sleep = np.arange(n) < 5
        if t < 0 or age <= 0:
            m = sleep; pos = np.array(e) + np.stack([S_['jit'][sl][:, 0] * 0.01 + ex * 0.04, np.cos(S_['jit'][sl][:, 1]) * 0.05, np.sin(S_['jit'][sl][:, 2]) * 0.07 - 0.02], 1); pos = pos[m]; allsleep.append(np.ones(m.sum(), bool)); allp.append(pos); continue
        ramp = _sm(age / 0.8); show = (u_ < burst * ramp) | sleep
        a = age; o = np.array(outv) / max(np.linalg.norm(outv), 1e-6)
        dirv = dr * 0.5 + o * 0.9; dirv /= np.linalg.norm(dirv, axis=1, keepdims=True)
        dist = (1.2 * np.sqrt(a) + 0.35 * a) * S_['spd'][sl] * (0.6 + 0.8 * u_)
        ph = S_['ph'][sl] + S_['om'][sl] * a; orr = S_['orr'][sl] * (1 - np.exp(-a / 0.6)) * 0.55
        pos = np.array(e) + dirv * dist[:, None] + np.stack([np.cos(ph) * orr, np.sin(ph) * orr * 0.7, 0.4 * np.sin(1.7 * ph) * orr + S_['zlift'][sl] * (1 - np.exp(-a / 1.0)) * 0.6], 1)
        if target is not None:
            w = _sm((a - 0.9) / 1.8) * (0.55 + 0.4 * u_); tg = np.array(target) + np.stack([np.cos(ph * 1.3) * 0.5, np.sin(ph * 1.1) * 0.35, np.sin(ph * 0.9) * 0.4], 1); pos = pos * (1 - w[:, None]) + tg * w[:, None]
        pos = pos + 0.04 * np.stack([np.sin(a * 23 + S_['jit'][sl][:, 0]), np.sin(a * 29 + S_['jit'][sl][:, 1]), np.sin(a * 31 + S_['jit'][sl][:, 2])], 1)
        allp.append(pos[show]); allsleep.append(sleep[show] & False)
    if local is not None:
        c, rad, nn = local; rr_ = np.random.RandomState(5); k = int(nn); ph = rr_.uniform(0, 6.283, k); om = rr_.uniform(2.0, 5.0, k); r = rr_.uniform(0.15, 1.0, k) * rad; z0 = rr_.uniform(-0.6, 0.6, k) * rad
        lp = np.array(c) + np.stack([np.cos(ph + om * sec) * r, np.sin(ph * 1.3 + om * sec * 0.9) * r * 0.8, z0 + 0.12 * np.sin(om * sec * 2.3 + ph)], 1); allp.append(lp); allsleep.append(np.zeros(k, bool))
    if not allp: return
    P = np.concatenate(allp); n = len(P)
    if n == 0: return
    rr = np.random.RandomState(int(sec * 30) % 997 + 3); yaw = rr.uniform(0, 6.283, n); pit = rr.uniform(-0.5, 0.5, n); fl = rr.uniform(0.35, 1.2, n); s = BEE_L
    cy, sy_, cp, sp_ = np.cos(yaw), np.sin(yaw), np.cos(pit), np.sin(pit)
    fw = np.stack([cy * cp, sy_ * cp, sp_], 1); sd = np.stack([-sy_, cy, np.zeros(n)], 1); up = np.cross(fw, sd)
    def pt(a, b, c): return P + fw * (a * s)[:, None] + sd * (b * s)[:, None] + up * (c * s)[:, None] if hasattr(a, '__len__') else P + fw * (a * s) + sd * (b * s) + up * (c * s)
    ring = lambda x, r: [pt(x, r, 0.0), pt(x, 0.0, r), pt(x, -r, 0.0), pt(x, 0.0, -r)]
    head = pt(0.62, 0, 0); tail = pt(-0.62, 0, 0); r1 = ring(0.22, 0.2); r2 = ring(-0.18, 0.22); r3 = ring(0.5, 0.11)
    vs = [head, tail] + r1 + r2 + r3 + [pt(0.12, 0.0, 0.18), pt(-0.1, 0.0, 0.18), pt(0.12, 0.0, 0.18), pt(-0.1, 0.0, 0.18)]
    wl = [pt(0.1, 0.1, 0.12), pt(-0.12, 0.1, 0.12), pt(-0.05, 1.0 * 0.95, 0.12 + 0.8 * fl[0] * 0 + 0.0)]
    # wings: two triangles with flap angle fl (per bee, rebuilt each call)
    wing = []
    for sg in (-1, 1):
        wing.append((pt(0.12, 0.12 * sg, 0.18), pt(-0.1, 0.12 * sg, 0.18), P + sd * (sg * 0.95 * s * np.cos(fl))[:, None] + up * (0.75 * s * np.sin(fl) + 0.18 * s)[:, None] + fw * (-0.05 * s)))
    V = np.stack(vs[:14] + [w[2] for w in wing] + [w[0] for w in wing] + [w[1] for w in wing], 1)         # (n, 20, 3)
    Vf = V.reshape(-1, 3); nv = V.shape[1]; base = (np.arange(n) * nv)[:, None]
    # indices: 0 head, 1 tail, 2-5 ring1 (x .22), 6-9 ring2 (x -.18), 10-13 ring3 (x .5), 14,15 wing tips, 16,17 wing roots front, 18,19 wing roots back
    tris_b = []; tris_g = []; tris_w = []
    for q in range(4):
        q2 = (q + 1) % 4
        tris_b += [(0, 10 + q, 10 + q2), (10 + q, 2 + q, 2 + q2), (10 + q, 2 + q2, 10 + q2)]
        tris_g += [(2 + q, 6 + q, 6 + q2), (2 + q, 6 + q2, 2 + q2), (6 + q, 1, 6 + q2)]
    tris_w = [(16, 18, 14), (17, 19, 15)]
    F = []; MI = []
    for mi, tl in enumerate((tris_g, tris_b, tris_w)):
        for tr in tl: F.append(base + np.array(tr)[None, :]); MI += [mi] * n
    Fall = np.concatenate(F).astype(np.int64); MIa = np.array(MI, dtype=np.int32)
    me = bpy.data.meshes.new('bees'); me.vertices.add(len(Vf)); me.vertices.foreach_set('co', Vf.astype(np.float32).ravel())
    nl = len(Fall) * 3; me.loops.add(nl); me.loops.foreach_set('vertex_index', Fall.ravel()); me.polygons.add(len(Fall)); me.polygons.foreach_set('loop_start', np.arange(len(Fall)) * 3); me.polygons.foreach_set('loop_total', np.full(len(Fall), 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('material_index', MIa)
    M = STATE['M']
    for k in ('beegold', 'beeblack', 'beewing'): me.materials.append(M[k])
    ob = bpy.data.objects.new('bees', me); sc.collection.objects.link(ob); ob.visible_shadow = False; STATE['bees_ob'].append(ob)

def set_bees(t, burst=1.0, target=None, local=None):
    """t: 0..1 over SEQ_T (5 s) from the start of set_wire_push. t < 0: sleeping (a few bees at each entrance, silent). Each hive releases its cloud when the wave reaches it. burst: 0..1 share of
    the cloud. target (x,y,z): swarms stream toward it (the eyes of the elephant). local=((x,y,z), radius, count): an extra swarm cloud around a point (the head in trunk_close)."""
    STATE['bees_args'] = (t, burst, target, local); _bees_apply(t, burst, target, local)

def set_fence_stage(k):
    """0 posts only, 1 one hive (unit 1: front row), 2 ten hives, 3 all 16 hives + the continuous wire ring."""
    STATE['stage'] = int(k); _update_fence()

def set_wire_push(t, point=None):
    """t 0..1 over 5 s: the wire bows in at the push point (front row x 1.0) and the wave travels outward around the ring at 15 m/s; every hive swings (damped). t < 0: at rest.
    point: optional arc length (m, from the front-left corner, counter-clockwise) of another push point."""
    STATE['push_t'] = float(t)
    if point is not None: STATE['push_s0'] = float(point)
    _update_fence()

# ============================================================================ the world
STAND = {   # name -> (x, y, z, facing): floor points for actor cards (card bottom = feet), heights in HEIGHT
 'hero_yard': (-3.9, 1.0, 0.0), 'hero_fence': (-8.8, 3.4, 0.0), 'hero_hive': (-6.5, 3.6, 0.0), 'hero_proud': (-1.2, 2.4, 0.0),
 'uncle_yard': (-0.3, 0.3, 0.0), 'uncle_night': (3.6, 1.2, 0.0),
 'villager_woman': (-8.9, -1.1, 0.0), 'villager_kid': (-7.5, -2.4, 0.0), 'villager_oldman': (-1.9, -2.1, 0.0), 'villager_woman2': (2.4, -1.7, 0.0), 'villager_man': (5.4, -0.6, 0.0),
 'matriarch_push': (1.0, 4.3, 0.0), 'matriarch_arrive': (-1.8, 0.4, 0.0),
 'ele_2': (-6.2, 2.0, 0.0), 'ele_3': (6.4, 1.4, 0.0), 'ele_4': (-11.0, 0.6, 0.0), 'calf': (-3.2, -0.8, 0.0),
 'herd_a': (-8.5, -2.0, 0.0), 'herd_b': (-3.0, -3.6, 0.0), 'herd_c': (5.5, -2.4, 0.0), 'herd_d': (10.0, 0.4, 0.0), 'herd_calf': (2.0, -3.4, 0.0),
 'uncle_stool': (-22.4, 2.4, 0.0), 'uncle_field': (-27.0, 1.2, 0.0), 'uncle_fence_hive': (-23.0, 5.0, 0.0),
}
HEIGHT = dict(hero=1.75, uncle=1.72, woman=1.62, kid=1.15, oldman=1.6, man=1.75, matriarch=3.3, elephant=3.0, calf=1.5)

def _hero_field(M, vars_, light):
    sc = bpy.context.scene; rr = rnd(7); n = 0
    for ix in range(-12, 12):
        for iy in range(0, 44):
            x = -12.3 + (ix + 12) * 0.95 + rr.uniform(-0.1, 0.1); y = 5.9 + iy * 0.44 + rr.uniform(-0.08, 0.08)
            if y > 24.9 or x > 10.0 or rr.random() < 0.025: continue
            v = vars_[rr.randrange(len(vars_))]; ob = bpy.data.objects.new('mz', v.data); ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rr.random() * 6.283)
            s = rr.uniform(0.85, 1.18); ob.scale = (s, s, s * rr.uniform(0.92, 1.12)); sc.collection.objects.link(ob); n += 1
    return n

def _uncle_field(M, vars_):
    sc = bpy.context.scene; rr = rnd(17); plants = []
    for ix in range(0, 24):
        for iy in range(0, 44):
            x = -45.0 + ix * 0.98 + rr.uniform(-0.1, 0.1); y = 6.4 + iy * 0.44 + rr.uniform(-0.08, 0.08)
            if y > 25.6 or rr.random() < 0.03: continue
            v = vars_[rr.randrange(len(vars_))]; ob = bpy.data.objects.new('umz', v.data); rz = rr.random() * 6.283; s = rr.uniform(0.85, 1.15); zs = s * rr.uniform(0.92, 1.1)
            ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rz); ob.scale = (s, s, zs); sc.collection.objects.link(ob)
            plants.append(dict(ob=ob, loc=(x, y, 0.0), rz=rz, s=s, zs=zs, thr=rr.uniform(0.05, 0.85), fall=rr.uniform(1.15, 1.5), phi=rr.uniform(0, 6.283), eaten=rr.random() < 0.28, gone=rr.random() < 0.12))
    STATE['uplants'] = plants

def _uncle_fence(M, light):
    """thorn-branch fence: piles between stakes (each its own object so k=1 can break it) and tin cans on strings along the front."""
    sc = bpy.context.scene; STATE['upiles'] = []; STATE['ucans'] = []; ux0, ux1, uy0, uy1 = -46.8, -21.2, 5.0, 26.6; rr = rnd(23); pid = 0
    segs = []
    for x in np.arange(ux0 + 1.5, ux1, 3.0): segs += [((x, uy0), 0.0), ((x, uy1), 0.0)]
    for y in np.arange(uy0 + 1.5, uy1, 3.0): segs += [((ux0, y), 1.5708), ((ux1, y), 1.5708)]
    for (c, yaw) in segs:
        mb = MB('thorn'); G.thorn_pile(mb, M, (0, 0, 0), yaw, 3.0, 1.15, pid + 5); ob = mb.finish(join=True)[0]; ob.location = (c[0], c[1], 0.0)
        broken = (pid % 3 == 0) and (c[1] in (uy0, uy1) or c[0] == ux0)
        STATE['upiles'].append(dict(ob=ob, loc=(c[0], c[1], 0.0), yaw=yaw, broken=broken, dirv=(rr.uniform(-1, 1), rr.uniform(0.6, 1.6)))); pid += 1
    for k, x in enumerate(np.arange(ux0 + 3.0, ux1 - 2.0, 6.0)):
        mb = MB('cans'); G.tin_can_line(mb, M, (-1.5, 0, 1.55), (1.5, 0, 1.45), 5, 40 + k)
        for sx in (-1.5, 1.5): mb.rod(M['wood'], (sx, 0, 0), (sx, 0, 1.65), 0.04, 0.035, 5)
        ob = mb.finish(join=True)[0]; ob.location = (x, uy0 - 0.35, 0); STATE['ucans'].append(dict(ob=ob, loc=(x, uy0 - 0.35, 0.0), brk=(k % 2 == 0)))
    # footprints (big round pads) along three herd tracks, visible with set_uncle_field
    STATE['ufoot'] = []; mbf = MB('foot'); rrf = rnd(41); objs = []
    for tx in (-39.5, -33.0, -27.5):
        for j in range(18):
            y = 27.0 - j * 1.55; x = tx + rrf.uniform(-0.4, 0.4) + (0.55 if j % 2 else -0.55); r = rrf.uniform(0.26, 0.33)
            mbf2 = MB('fp'); mbf2.rod(M['foot'], (0, 0, 0.0), (0, 0, 0.03), r, r, 10); mbf2.rod(M['dust'], (0, 0, 0.0), (0, 0, 0.022), r * 1.3, r * 1.3, 10); o = mbf2.finish(join=True)[0]
            o.location = (x, y, 0.0); o.scale = (0.01, 0.01, 0.01); STATE['ufoot'].append(dict(ob=o, thr=rrf.uniform(0.0, 0.7), s=rrf.uniform(0.9, 1.2)))
    # chewed cobs + pulled stalks
    mc = MB('chew'); rc = rnd(43)
    for i in range(70):
        x = rc.uniform(-45, -22); y = rc.uniform(6.5, 25.5); mc.ell(M['cob'], (x, y, 0.06), (0.13, 0.045, 0.045), (7, 5), (0, 0, rc.random() * 6.28))
        if i % 2: mc.ell(M['husk'], (x + 0.1, y, 0.04), (0.14, 0.07, 0.03), (6, 4), (0, 0, rc.random() * 6.28))
        if i % 5 == 0: mc.rod(M['stalk'], (x, y, 0.05), (x + rc.uniform(-1, 1), y + rc.uniform(-1, 1), 0.07), 0.03, 0.02, 5)
    STATE['uchew'] = mc.finish(); 

def _uncle_farm(M, light, props):
    G.house_tin(props, M, (-34.0, 34.5, 0.0), 6.5, 4.0, 2.6, yaw=0.08, roof='tinred', walls='plaster2', seed=3, door='doorred')
    G.hut_round(props, M, (-43.0, 32.0, 0.0), r=1.55, rt=2.2, ht=1.8, door_yaw=0.3, thatch='thatchold', seed=9); G.granary(props, M, (-26.5, 32.5, 0.0))
    for i, (x, y) in enumerate([(-20.5, 29.5), (-48.8, 30.0), (-30.0, 38.0)]): G.banana(props, M, (x, y, 0.0), 300 + i, 1.0)
    G.stool(props, M, (-22.4, 1.8)); G.bench(props, M, (-28.5, 0.4), 0.2); G.bucket(props, M, (-27.4, 0.8)); G.basket(props, M, (-30.5, 1.0), True, 8)
    G.jerrycan(props, M, (-31.4, 0.2, 0.0), 0.4); G.jerrycan(props, M, (-31.7, 0.55, 0.0), 1.2); G.hoe(props, M, (-26.0, 2.2, 0.0), 2.3); G.pot_clay(props, M, (-29.4, 1.6))
    G.firepit(props, M, (-21.4, 1.4, 0.0), light in ('NIGHT', 'DUSK', 'MORNING'))
    if light != 'NIGHT':
        for i, (x, y) in enumerate([(-32.4, 2.2), (-24.8, -0.4), (-33.2, -1.0), (-19.6, 0.6)]): G.chicken(props, M, (x, y, 0.0), i * 2.1, 1.15, i % 4, 0.5 if i % 2 else 0.0)
    for i, (x, y) in enumerate([(-45.0, 38.0), (-24.0, 40.0), (-38.0, 44.0)]): G.bush(props, M, (x, y, 0.0), 1.3, 50 + i)

def _hero_yard(M, light, props):
    day = light != 'NIGHT'
    for (x, y, yw) in [(-6.6, 0.4, 0.7), (-6.2, 0.75, 1.3), (-6.55, 0.05, 2.2), (-6.3, 0.2, 0.2), (-7.0, 0.8, 1.9)]: G.jerrycan(props, M, (x, y, 0.0), yw)
    G.hoe(props, M, (-7.4, 1.9, 0.0), 0.6); G.hoe(props, M, (-7.8, 1.5, 0.0), 0.9, 1.15)
    G.stool(props, M, (-5.0, 1.4)); G.stool(props, M, (-4.4, 0.9), 0.5); G.bench(props, M, (-9.8, 0.8), 0.3)
    G.basket(props, M, (-7.9, 0.8), True, 4); G.basket(props, M, (-8.6, -0.1), True, 6)
    G.wheelbarrow(props, M, (4.2, -1.4, 0.0), 0.5); G.firewood(props, M, (6.3, 0.9, 0.0), 0.2, 4)
    for i, (x, y, z) in enumerate([(-9.3, -0.3, 0.0), (-9.3, -0.3, 0.38), (-9.0, -0.8, 0.0)]):          # spare hives stacked on the ground
        props.push(Matrix.Translation((x, y, 0.85 + z)) @ Euler((0, 0, 0.3 + i * 0.2)).to_matrix().to_4x4()); G.MB.finish if False else None
        _hive_ground(props, M); props.pop()
    props.corrugated(M['tin'], (-10.3, 3.2, 0.0), (0.3, 0.0, 1.0), (0.97, 0.25, 0), (0.25, -0.95, 0.1), 2.3, 1.6, 0.1, 0.025)                # tin sheets leaned on a post
    props.corrugated(M['tin'], (-10.9, 3.15, 0.0), (0.3, 0.0, 1.0), (0.97, 0.25, 0), (0.25, -0.95, 0.1), 2.2, 1.6, 0.1, 0.025)
    for (x, y) in [(-4.4, -0.4), (-3.7, -0.7)]: _spool(props, M, (x, y, 0.0))
    G.bucket(props, M, (-2.3, 2.4, 0.0), 'jcap'); G.pot_clay(props, M, (4.9, -0.6, 0.0)); G.pot_clay(props, M, (5.3, -0.9, 0.0), 0.8)
    for i in range(3): G.sack(props, M, (7.0 + i * 0.35, -0.6 + (i % 2) * 0.2, 0.0), i * 1.1)
    # ladder leaning on the fence
    for sx in (-0.22, 0.22): props.rod(M['woodpale'], (-3.5 + sx, 3.7, 0.0), (-3.5 + sx, 4.55, 2.35), 0.035, 0.03, 5)
    for i in range(7): z = 0.3 + i * 0.32; props.rod(M['woodpale'], (-3.72, 3.7 + 0.85 * z / 2.35, z), (-3.28, 3.7 + 0.85 * z / 2.35, z), 0.022, 0.022, 4)
    G.firepit(props, M, (1.3, 0.5, 0.0), light in ('NIGHT', 'DUSK', 'MORNING'))
    G.metal_pot(props, M, (1.3, 0.5, 0.3), 1.0) if light == 'DAY' and False else None
    if light in ('NIGHT', 'DUSK'):
        for i in range(14):
            a = i * 0.45; r = 0.2 + (i % 5) * 0.15; props.ell(M['ember'], (1.3 + math.cos(a) * r, 0.5 + math.sin(a) * r, 0.03 + 0.03 * (i % 3)), (0.025, 0.025, 0.015), (6, 4))
    props.rod(M['wood'], (1.9, 2.8, 0), (1.9, 2.8, 2.5), 0.06, 0.05, 6); props.rod(M['wood'], (1.9, 2.8, 2.45), (1.9, 3.5, 2.45), 0.04, 0.04, 5); props.rod(M['rope'], (1.9, 2.8, 2.4), (1.9, 2.8, 2.2), 0.01, 0.01, 4)
    props.ell(M['lamp'], (1.9, 2.8, 2.1), (0.1, 0.1, 0.14), (8, 6)); props.lathe(M['glass'], (1.9, 2.8, 1.95), [(0.0, 0.0), (0.11, 0.0), (0.11, 0.32), (0.0, 0.32)], 8) if False else None
    if day:
        for i, (x, y) in enumerate([(-4.2, 0.1), (-8.3, 1.2), (-3.4, 1.6), (-5.6, -0.6), (-7.3, -0.4), (1.4, -1.0), (2.0, 1.8)]): G.chicken(props, M, (x, y, 0.0), i * 1.9, 1.15, i % 4, 0.7 if i % 3 == 0 else 0.0)
        G.goat(props, M, (-2.0, 0.6, 0.0), 0.5, 1.3, 0); G.goat(props, M, (-1.0, 2.0, 0.0), 2.2, 0.95, 1)
    else:
        G.goat(props, M, (-2.6, 2.2, 0.0), 0.5, 1.2, 0)
    # kitchen garden + sunflowers + papaya + pumpkins
    rk = rnd(61)
    for i in range(5): G.kale_row(props, M, (6.8 + i * 0.7, -1.6, 0.0), (6.8 + i * 0.7, 3.8, 0.0), rk)
    for i in range(14): G.sunflower(props, M, (12.8 + rk.uniform(-.25, .25), -1.0 + i * 0.5, 0.0), rk)
    G.papaya(props, M, (13.6, 2.6, 0.0), 1.1, 5); G.papaya(props, M, (-15.0, 2.0, 0.0), 1.0, 6); G.pumpkin_patch(props, M, (9.5, 1.5, 0.0), rk, 5)
    # beans along the field edge, a woven twig fence round the yard's right side
    for i in range(24):
        x = -12.6 + i * 1.0; props.rod(M['bean'], (x, 4.2, 0.0), (x, 4.2, 0.5), 0.015, 0.012, 4)
        for k in range(4): a = rk.random() * 6.28; props.ell(M['bean'], (x + math.cos(a) * 0.12, 4.2 + math.sin(a) * 0.12, 0.2 + 0.1 * k), (0.12, 0.07, 0.015), (6, 4), (0, 0, a))

def _hive_ground(mb, M):
    # hive without ropes (stacked spares)
    hive_local(mb, M, ropes=False)
def _spool(mb, M, c):
    x, y, z = c
    mb.lathe(M['woodpale'], (x, y, z), [(0.0, 0.0), (0.36, 0.0), (0.36, 0.035), (0.0, 0.035)], 18); mb.lathe(M['wire'], (x, y, z), [(0.2, 0.035), (0.31, 0.04), (0.31, 0.3), (0.2, 0.3)], 18)
    mb.lathe(M['woodpale'], (x, y, z), [(0.0, 0.3), (0.36, 0.3), (0.36, 0.335), (0.0, 0.335)], 18)

def _village(M, light, props):
    G.hut_round(props, M, (20.0, 14.0, 0.0), door_yaw=0.35, seed=1); G.hut_round(props, M, (28.5, 11.5, 0.0), r=1.5, rt=2.15, ht=1.8, door_yaw=-0.4, seed=2)
    G.hut_round(props, M, (22.5, 22.0, 0.0), r=1.6, rt=2.3, ht=1.9, door_yaw=0.2, thatch='thatchold', seed=3, walls='mudpale', band='mud')
    G.hut_round(props, M, (38.0, 14.0, 0.0), r=1.4, rt=2.0, ht=1.7, door_yaw=-0.9, seed=4)
    G.house_tin(props, M, (31.0, 21.0, 0.0), 7.0, 4.2, 2.7, yaw=-0.12, seed=1); G.house_tin(props, M, (44.0, 26.0, 0.0), 5.0, 3.6, 2.5, yaw=0.15, roof='tin2', walls='plaster3', seed=2, door='doorred')
    G.granary(props, M, (15.5, 19.5, 0.0)); G.granary(props, M, (36.0, 29.0, 0.0))
    G.tripod_pot_fire(props, M, (24.0, 8.5, 0.0), light in ('NIGHT', 'DUSK', 'MORNING'))
    for dx in (-1.0, 1.0): props.rod(M['wood'], (24.0 + dx, 8.9, 0.0), (24.0 + dx, 8.9, 1.2), 0.04, 0.04, 5)
    for (x, y, yw) in [(17.0, 8.0, 0.2), (17.35, 8.1, 1.0), (16.8, 8.45, 2.0), (33.6, 17.2, 0.4), (33.1, 17.0, 1.4)]: G.jerrycan(props, M, (x, y, 0.0), yw)
    props.box(M['woodpale'], (18.5, 10.4, 0.2), (0.9, 0.35, 0.4)); G.bench(props, M, (21.5, 9.4), 1.57); G.bench(props, M, (26.4, 6.6), 0.1)
    G.washing_line(props, M, (25.0, 4.2, 0.0), 0.15, 4.5, 2); G.washing_line(props, M, (35.5, 12.5, 0.0), 1.5, 3.5, 5)
    G.water_tank(props, M, (35.4, 18.2, 0.0)); G.bicycle(props, M, (26.6, 8.0, 0.0), 0.5); G.wheelbarrow(props, M, (17.0, 5.0, 0.0), 2.2, 'bluetank')
    G.firewood(props, M, (31.0, 13.6, 0.0), 0.1, 4); G.firewood(props, M, (19.0, 17.3, 0.0), 1.5, 3)
    for i in range(4): G.sack(props, M, (19.4 + i * 0.4, 16.7 - (i % 2) * 0.2, 0.0), i)
    for i, (x, y) in enumerate([(25.0, 12.5), (26.0, 13.0), (18.2, 11.4), (23.6, 4.6)]): G.pot_clay(props, M, (x, y, 0.0), 0.9 + 0.1 * i)
    G.basket(props, M, (22.0, 12.2), True, 11); G.basket(props, M, (30.6, 15.5), True, 12)
    for i, (x, y) in enumerate([(13.0, 11.0), (14.0, 15.0), (33.0, 14.5), (26.0, 16.0), (35.0, 24.0), (12.5, 22.5), (41.0, 18.0), (19.0, 26.5)]): G.banana(props, M, (x, y, 0.0), int(x * 7 + y), 1.0)
    G.papaya(props, M, (27.0, 25.0, 0.0), 1.1, 9); G.papaya(props, M, (39.0, 22.0, 0.0), 1.0, 10)
    # goat boma: a ring of thorn piles with goats asleep inside
    for i in range(10):
        a = i / 10 * 6.283; mb2 = MB('bomapile'); G.thorn_pile(mb2, M, (0, 0, 0), a + 1.5708, 2.4, 1.0, 70 + i); o = mb2.finish(join=True)[0]; o.location = (36.0 + math.cos(a) * 3.6, 7.0 + math.sin(a) * 3.6, 0)
    for i, (x, y, yw, c) in enumerate([(35.4, 6.4, 0.4, 0), (36.8, 7.6, 2.0, 1), (35.0, 8.0, 3.5, 2), (37.0, 5.8, 1.1, 0), (36.0, 7.0, 5.2, 1)]): G.goat(props, M, (x, y, 0.0), yw, 0.95 + 0.1 * (i % 2), c)
    if light != 'NIGHT':
        for i, (x, y) in enumerate([(14.3, 4.5), (23.0, 5.0), (19.6, 9.0), (27.4, 14.5), (21.0, 18.0), (31.0, 9.0), (16.4, 13.0), (24.6, 18.4)]): G.chicken(props, M, (x, y, 0.0), i * 1.7, 1.15, (i + 1) % 4, 0.6 if i % 2 else 0.0)
        G.goat(props, M, (28.0, 5.5, 0.0), 2.4, 0.9, 1); G.goat(props, M, (17.6, 14.4, 0.0), 0.7, 1.0, 0)
    # coop: small hut on stilts
    for dx in (-0.5, 0.5):
        for dy in (-0.4, 0.4): props.rod(M['wood'], (18.0 + dx, 6.4 + dy, 0), (18.0 + dx, 6.4 + dy, 0.5), 0.04, 0.04, 5)
    props.box(M['woodpale'], (18.0, 6.4, 0.85), (1.2, 1.0, 0.7)); props.cone(M['thatch'], (18.0, 6.4, 1.15), 0.95, 0.05, 0.6, 4); props.box(M['dark'], (18.0, 5.89, 0.85), (0.3, 0.05, 0.35))
    # woven twig fence along the yard front
    rw = rnd(66)
    for i in range(28):
        x = 14.0 + i * 0.95; props.rod(M['wood'], (x, 2.0 + rw.uniform(-.05, .05), 0), (x, 2.0, 0.9 + rw.uniform(-.1, .1)), 0.025, 0.022, 4)
    for z in (0.35, 0.6, 0.85): props.poly(M['woodgrey'], [(14.0 + k * 1.9, 2.0, z) for k in range(15)], 0.014, 0.014, 4, smooth=False)

def _trees(M, light):
    mb = MB('trees')
    for i, (x, y, s, yw) in enumerate([(-20.0, 20.0, 1.5, 0.3), (35.0, 5.0, 1.3, 1.1), (-33.0, 6.0, 1.1, 2.1), (0.0, 44.0, 1.7, 0.5), (-6.0, 60.0, 1.4, 1.5), (26.0, 34.0, 1.2, 0.9),
                                (-56.0, 20.0, 1.4, 0.2), (-52.0, 50.0, 1.5, 1.7), (50.0, 18.0, 1.4, 2.2), (14.0, 70.0, 1.6, 0.4), (-26.0, 75.0, 1.5, 1.0), (-70.0, 40.0, 1.6, 0.8), (62.0, 45.0, 1.5, 2.6),
                                (-42.0, 90.0, 1.7, 0.1), (30.0, 95.0, 1.7, 1.2), (-4.0, 110.0, 1.9, 0.6), (70.0, 85.0, 1.8, 2.0), (-80.0, 80.0, 1.8, 1.4), (46.0, 52.0, 1.3, 0.2)]):
        G.acacia(mb, M, (x, y, 0.0), s, i + 1, yw, 'leafgreen' if i % 2 else 'acacia2')
    mb.finish()
    mb = MB('scrub'); rr = rnd(81)
    for i in range(46):
        x = rr.uniform(-80, 80); y = rr.uniform(32, 120)
        if abs(x) < 6 and y < 50: continue
        G.bush(mb, M, (x, y, 0.0), rr.uniform(1.2, 2.4), 100 + i, 'acacia2' if i % 2 else 'leafgreen')
    for i in range(10): G.termite_mound(mb, M, (rr.uniform(-60, 60), rr.uniform(36, 90), 0.0), rr.uniform(0.8, 1.6))
    for i in range(30): G.rock(mb, M, (rr.uniform(-70, 70), rr.uniform(30, 110), 0.0), rr.uniform(1.0, 2.6), 200 + i, 'rockwarm' if i % 2 else 'rock')
    mb.finish()
    if light in ('DAY', 'MORNING'):
        mb = MB('giraffes'); G.giraffe(mb, M, (46.0, 78.0, 0.0), 2.0, 1.0); G.giraffe(mb, M, (54.0, 84.0, 0.0), 2.4, 0.8); mb.finish()

def _grass(M, light, cam_locs):
    mb = MB('grass'); rg = rnd(11)
    def ok(x, y):
        if 10.0 < x < 18.0 and -3 < y < 3: return False
        if -13.3 < x < 10.4 and 4.2 < y < 25.8: return False
        if -46.8 < x < -21.0 and 4.5 < y < 27.0: return False
        if math.hypot(x - 20, y - 14) < 4.6 or math.hypot(x - 29, y - 10) < 3 or math.hypot(x - 22, y - 21) < 3 or (27 < x < 36 and 17 < y < 24): return False
        if -4.5 < y < -1.5 and (light != 'NIGHT') and rg.random() < 0.85: return False
        return True
    for i in range(2600):
        t = rg.random()
        if t < 0.30: x, y = rg.uniform(-60, 16), rg.uniform(-1.8, 3.8)
        elif t < 0.5: x, y = rg.uniform(-21, -14), rg.uniform(4, 30)
        elif t < 0.75: x, y = rg.uniform(11.8, 46), rg.uniform(-1, 34)
        else: x, y = rg.uniform(-60, 60), rg.uniform(26, 70)
        if not ok(x, y): continue
        gm = 'grassgreen' if rg.random() < 0.3 else 'grass'; G.grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.6, 1.4), gm)
    # camera-side foreground tufts: dense near every preset camera, thinning with distance
    for (cx, cy, fx, fy, n) in cam_locs:
        for i in range(n):
            d = rg.uniform(1.8, 12.0) ** 1.0; a = math.atan2(fy, fx) + rg.uniform(-0.62, 0.62); x = cx + math.cos(a) * d; y = cy + math.sin(a) * d
            if not ok(x, y) or -0.6 < y < 0.0 and rg.random() < 0.0: continue
            if -4.8 < y < -1.2 and 0.0 < x < 8.0 and rg.random() < 0.9: continue         # keep the cart track clear
            G.grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.35, 1.0), 'grassgreen' if rg.random() < 0.35 else 'grass', 7)
    mb.finish()
    mb = MB('flowers'); rf = rnd(13)
    for i in range(520):
        x = rf.uniform(-60, 50); y = rf.uniform(-5.5, 5.0)
        if not ok(x, y): continue
        G.flower_tuft(mb, M, (x, y, 0.0), rf, 4)
    for (cx, cy, fx, fy, n) in cam_locs:
        for i in range(n // 4):
            d = rf.uniform(2.0, 10.0); a = math.atan2(fy, fx) + rf.uniform(-0.6, 0.6); x = cx + math.cos(a) * d; y = cy + math.sin(a) * d
            if ok(x, y) and not (-4.8 < y < -1.2): G.flower_tuft(mb, M, (x, y, 0.0), rf, 5)
    mb.finish()
    mb = MB('pebbles'); rp = rnd(14)
    for i in range(700):
        x = rp.uniform(-60, 55); y = rp.uniform(-8, 6); s = rp.uniform(0.04, 0.13)
        mb.ell(M['rock'] if i % 2 else M['rockwarm'], (x, y, s * 0.3), (s * 1.3, s, s * 0.6), (6, 4), (0, 0, rp.random() * 6))
    for i in range(260):
        x = rp.uniform(-60, 55); y = rp.uniform(-5, 4); a = rp.random() * 6.28; mb.rod(M['woodgrey'], (x, y, 0.02), (x + math.cos(a) * 0.4, y + math.sin(a) * 0.4, 0.04), 0.012, 0.01, 4)
    mb.finish()

# ============================================================================ uncle's field / hive, crowd props
def set_uncle_field(k):
    """0 intact, 1 trampled and eaten (stalks flattened and torn out, thorn fence broken, tin-can strings down, big footprints, chewed cobs). k may be fractional (the herd passes): each plant falls at its own threshold."""
    k = float(np.clip(k, 0, 1)); STATE['uf'] = k
    for p in STATE['uplants']:
        f = _sm((k - p['thr']) / 0.14); ob = p['ob']
        if p['gone'] and f > 0.5: ob.scale = (0.001, 0.001, 0.001); ob.location = (p['loc'][0], p['loc'][1], -5); continue
        a = p['fall'] * f; ob.location = (p['loc'][0], p['loc'][1], 0.10 * f)
        ob.rotation_euler = (a * math.cos(p['phi']), a * math.sin(p['phi']), p['rz']); z = p['zs'] * (1 - (0.45 if p['eaten'] else 0.12) * f); ob.scale = (p['s'], p['s'], z)
    for pl in STATE['upiles']:
        ob = pl['ob']; f = _sm((k - 0.15) / 0.2) if pl['broken'] else 0.0
        ob.location = (pl['loc'][0] + pl['dirv'][0] * 1.3 * f, pl['loc'][1] + pl['dirv'][1] * 1.0 * f, 0.0); ob.rotation_euler = (0, 0, 0.7 * f * pl['dirv'][0]); ob.scale = (1, 1, 1 - 0.65 * f)
    for c in STATE['ucans']:
        ob = c['ob']; f = _sm((k - 0.1) / 0.2) if c['brk'] else 0.0
        ob.location = (c['loc'][0], c['loc'][1] + 0.6 * f, c['loc'][2] - 0.0); ob.rotation_euler = (1.25 * f, 0, 0.2 * f); ob.scale = (1, 1, 1 - 0.3 * f)
    for fp in STATE['ufoot']:
        f = _sm((k - fp['thr'] * 0.8 - 0.05) / 0.1); s = max(0.001, fp['s'] * f); fp['ob'].scale = (s, s, 1 if f > 0 else 0.001)
    for o in STATE['uchew']: _hide(o, k < 0.3)

def set_uncle_hive(k):
    """uncle's first hive on his own fence (unit at x -23, y 5): 0 = nothing, 0..1 = the hive is lifted up to its hook (hand height to the wire), 1 = hung."""
    k = float(np.clip(k, 0, 1)); STATE['uh'] = k; on = k > 0
    for o in STATE['uhive_static']: _hide(o, not on)
    h = STATE['uhive']; _hide(h, not on)
    if on:
        e = _sm(k); h.location = (-23.0, 5.0 - WIRE_OFF - 0.55 * (1 - e) * 0 + 0.0 - 0.7 * (1 - e), 2.0 - 0.0 - 0.75 * (1 - e)); h.rotation_euler = (0.25 * (1 - e) * 0, 0, 0)

def _uncle_hive_unit(M):
    sc = bpy.context.scene; x, y = -23.0, 5.0; st = []
    mb = MB('uposts')
    for dx in (-1.0, 1.0): mb.rod(M['wood'], (x + dx, y, -0.15), (x + dx, y, 2.58), 0.075, 0.062, 7, smooth=True); mb.ell(M['woodpale'], (x + dx, y, 2.59), (0.07, 0.07, 0.025), (6, 4))
    mb.rod(M['wire'], (x - 1.0, y - WIRE_OFF, WIRE_Z), (x + 1.0, y - WIRE_OFF, WIRE_Z), WIRE_R, WIRE_R, 6)
    mb.push(Matrix.Translation((x, y, 0))); roof_local(mb, M); mb.pop(); mb.push(Matrix.Translation((x, y - WIRE_OFF, WIRE_Z))); bar_local(mb, M); mb.pop()
    st += mb.finish(join=True)
    mh = MB('uhive'); hive_local(mh, M); h = mh.finish(join=True)[0]; STATE['uhive'] = h; STATE['uhive_static'] = st; STATE['uh'] = 0.0
    for o in st: _hide(o, True)
    _hide(h, True)

def set_crowd_props(k):
    """villagers' props for the pivot: torches (lit, with lights) and banged pots held at the villager stand points. 0 = off, 1 = on."""
    on = k > 0; STATE['cr'] = float(k)
    for o in STATE['crowd_objs']: _hide(o, not on)
    for l in STATE['crowd_lights']: _hide(l, not on or STATE['light'] == 'DAY' and False)

def _crowd(M, light):
    sc = bpy.context.scene; STATE['crowd_objs'] = []; STATE['crowd_lights'] = []
    mb = MB('crowd')
    spots = [('villager_woman', 'pot'), ('villager_kid', 'pot'), ('villager_oldman', 'torch'), ('villager_woman2', 'torch'), ('villager_man', 'torch'), ('uncle_night', 'torch')]
    for nm, kind in spots:
        x, y, z = STAND[nm]
        if kind == 'torch':
            G.torch(mb, M, (x + 0.42, y - 0.05, 0.0), 1.45, True, 1.2)
            l = bpy.data.lights.new('torch', 'POINT'); l.color = (1.0, 0.58, 0.24); l.energy = 140 if light != 'DAY' else 40; l.shadow_soft_size = 0.12
            ob = bpy.data.objects.new('torchlight', l); ob.location = (x + 0.42, y - 0.1, 1.9); sc.collection.objects.link(ob); STATE['crowd_lights'].append(ob)
        else:
            G.metal_pot(mb, M, (x - 0.38, y - 0.05, 1.0), 1.3); mb.rod(M['wood'], (x - 0.2, y - 0.05, 1.28), (x - 0.38, y - 0.05, 1.5), 0.02, 0.02, 4)
    STATE['crowd_objs'] = mb.finish()
    for o in STATE['crowd_objs']: _hide(o, True)
    for l in STATE['crowd_lights']: _hide(l, True)

# ============================================================================ placeholder actor cards (flat plum-outlined puppets, PIL)
INK = (58, 34, 50, 255); SKIN = (138, 90, 58, 255)
def _card_art(role, path):
    if os.path.exists(path): return
    S = 3
    if role in ('matriarch', 'elephant', 'calf'):
        w, h = 1200, 800; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = S
        body = (140, 146, 170, 255) if role != 'calf' else (150, 154, 176, 255); shade = (104, 110, 140, 255); lw = 9 * k
        def E(box, fill): d.ellipse([c * k for c in box], fill=fill, outline=INK, width=lw)
        for lx in (300, 400, 760, 860):                                           # legs
            d.rounded_rectangle([lx * k, 470 * k, (lx + 110) * k, 770 * k], radius=30 * k, fill=shade if lx in (400, 860) else body, outline=INK, width=lw)
        E((200, 190, 930, 620), body); E((780, 250, 1000, 520), body)               # body, head
        d.polygon([(a * k, b * k) for a, b in [(930, 340), (1010, 470), (1060, 640), (1090, 720), (1150, 760), (1160, 700), (1120, 640), (1100, 520), (1050, 380), (990, 290)]], fill=body, outline=INK, width=lw)  # trunk
        E((690, 230, 900, 520), shade)                                              # ear
        d.polygon([(a * k, b * k) for a, b in [(950, 470), (1010, 560), (1090, 590), (1000, 520)]], fill=(226, 218, 196, 255), outline=INK, width=6 * k)   # tusk
        E((955, 330, 985, 360), INK); d.line([(215 * k, 360 * k), (170 * k, 560 * k)], fill=INK, width=14 * k)
        im = im.resize((w, h), Image.LANCZOS); im.save(path); return
    w, h = 400, 1000; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = S; lw = 7 * k
    spec = dict(hero=dict(shirt=(224, 120, 42, 255), pants=(184, 160, 112, 255), hat=(214, 200, 170, 255), hair=(40, 28, 28, 255), belly=0, wid=1.0),
                uncle=dict(shirt=(190, 70, 60, 255), pants=(96, 84, 70, 255), hat=(110, 112, 122, 255), hair=(150, 150, 150, 255), belly=1, wid=1.15),
                woman=dict(shirt=(46, 110, 170, 255), pants=(46, 110, 170, 255), hat=(240, 196, 48, 255), hair=(40, 28, 28, 255), belly=0, wid=1.0, dress=1),
                kid=dict(shirt=(232, 196, 60, 255), pants=(70, 110, 170, 255), hat=None, hair=(40, 28, 28, 255), belly=0, wid=1.0),
                oldman=dict(shirt=(170, 150, 120, 255), pants=(100, 90, 80, 255), hat=(200, 190, 160, 255), hair=(236, 236, 236, 255), belly=0, wid=0.95),
                man=dict(shirt=(70, 140, 90, 255), pants=(80, 90, 120, 255), hat=None, hair=(40, 28, 28, 255), belly=0, wid=1.0))[role]
    cx = 200; hr = 82 if role != 'kid' else 98; headc = (cx, 150 if role != 'kid' else 400 if False else 150); fy = 985
    if role == 'kid': top = 1000 * 0.0; hr = 95
    wd = 85 * spec['wid']; bt = 270; bb = 560 if not spec.get('dress') else 700
    def R_(x0, y0, x1, y1, f, r=24): d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=r * k, fill=f, outline=INK, width=lw)
    ytop = 240 if role != 'kid' else 430
    scale = 1.0 if role != 'kid' else 0.6; oy = 0 if role != 'kid' else 400
    def Y(v): return (v * scale + oy)
    R_(cx - 60 * scale, Y(560), cx - 12 * scale, Y(960), spec['pants'] if not spec.get('dress') else SKIN, 16); R_(cx + 12 * scale, Y(560), cx + 60 * scale, Y(960), spec['pants'] if not spec.get('dress') else SKIN, 16)
    for sx in (-1, 1): R_(cx + sx * 12 * scale - 34 * scale, Y(950), cx + sx * 12 * scale + 34 * scale, Y(990), (70, 56, 50, 255), 10)
    R_(cx - 105 * scale * spec['wid'], Y(270), cx - 62 * scale * spec['wid'], Y(560), SKIN, 14); R_(cx + 62 * scale * spec['wid'], Y(270), cx + 105 * scale * spec['wid'], Y(560), SKIN, 14)
    if spec['belly']: d.ellipse([(cx - 120 * scale) * k, Y(250) * k, (cx + 120 * scale) * k, Y(650) * k], fill=spec['shirt'], outline=INK, width=lw)
    else: R_(cx - 78 * scale * spec['wid'], Y(250), cx + 78 * scale * spec['wid'], Y(bb if not spec.get('dress') else 760), spec['shirt'], 36)
    if role == 'uncle':
        for q in range(-5, 6): d.line([((cx + q * 20 * scale) * k, Y(280) * k), ((cx + q * 20 * scale) * k, Y(620) * k)], fill=(240, 230, 220, 160), width=4 * k)
        d.polygon([((cx - 100 * scale) * k, Y(270) * k), ((cx - 40 * scale) * k, Y(260) * k), ((cx + 110 * scale) * k, Y(600) * k), ((cx + 40 * scale) * k, Y(610) * k)], fill=(60, 90, 170, 230), outline=INK)
        d.line([((cx + 150 * scale) * k, Y(420) * k), ((cx + 170 * scale) * k, Y(985) * k)], fill=(120, 80, 48, 255), width=12 * k)
    d.ellipse([(cx - hr * scale) * k, (Y(150) - hr * scale) * k, (cx + hr * scale) * k, (Y(150) + hr * scale) * k], fill=SKIN, outline=INK, width=lw)
    if spec['hat'] is not None:
        if role == 'hero': d.ellipse([(cx - hr * 1.25 * scale) * k, (Y(150) - hr * 1.3 * scale) * k, (cx + hr * 1.25 * scale) * k, (Y(150) - hr * 0.2 * scale) * k], fill=spec['hat'], outline=INK, width=lw)
        else: d.chord([(cx - hr * scale) * k, (Y(150) - hr * 1.05 * scale) * k, (cx + hr * scale) * k, (Y(150) + hr * 0.5 * scale) * k], 180, 360, fill=spec['hat'], outline=INK, width=lw)
    else: d.chord([(cx - hr * scale) * k, (Y(150) - hr * scale) * k, (cx + hr * scale) * k, (Y(150) + hr * 0.4 * scale) * k], 180, 360, fill=spec['hair'], outline=INK, width=lw)
    for sx in (-1, 1): d.ellipse([(cx + sx * 30 * scale - 7) * k, (Y(150) - 8) * k, (cx + sx * 30 * scale + 7) * k, (Y(150) + 8) * k], fill=INK)
    d.arc([(cx - 28 * scale) * k, (Y(150) + 12 * scale) * k, (cx + 28 * scale) * k, (Y(150) + 50 * scale) * k], 20, 160, fill=INK, width=5 * k)
    im = im.resize((w, h), Image.LANCZOS); im.save(path)

def place_actor(role, mark, face_to=None, name=None):
    """flat placeholder puppet card (emission-only, shadow-casting) standing at `mark` (feet), turned to face `face_to` (yaw only)."""
    P = STATE['P']; name = name or 'actor_' + role; h = HEIGHT[role]; wide = role in ('matriarch', 'elephant', 'calf'); asp = 1.5 if wide else 0.4
    png = os.path.join(TEX, 'card_%s.png' % role); _card_art(role, png); w = h * asp
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    m = mat_card(name + '_mat', png, P.get('card_k', 1.0)); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = mark
    yaw = 0.0
    if face_to is not None: d = Vector(face_to) - Vector(mark); yaw = math.atan2(d.x, -d.y)
    ob.rotation_euler = (0, 0, yaw); return ob
def _clear_actors():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o)

# ============================================================================ presets, cameras, staging
def _roles(): return HEIGHT
CAMS = dict(
 village_wide=dict(loc=(-14.0, -30.0, 11.5), look=(14.0, 14.0, 1.2), lens=20),
 fence_line=dict(loc=(-19.0, 0.4, 1.65), look=(2.0, 5.6, 1.5), lens=22),
 hive_close=dict(loc=(-9.7, 2.4, 1.2), look=(-5.2, 5.0, 1.45), lens=24),
 yard_two_shot=dict(loc=(-2.6, -6.0, 1.45), look=(-1.8, 2.0, 1.35), lens=22),
 field_night_wide=dict(loc=(-4.0, -13.5, 9.0), look=(-0.5, 10.0, 0.8), lens=22),
 fence_low_night=dict(loc=(6.0, -2.4, 1.2), look=(-1.2, 5.0, 1.8), lens=22),
 push_side=dict(loc=(-17.5, -2.8, 2.1), look=(3.5, 5.2, 1.6), lens=22),
 trunk_close=dict(loc=(-1.0, -0.6, 2.3), look=(1.2, 4.2, 2.4), lens=26),
 uncle_field_morning=dict(loc=(-24.0, -6.0, 3.4), look=(-32.5, 12.0, 0.4), lens=22),
 uncle_hang=dict(loc=(-18.6, -3.0, 1.5), look=(-22.6, 3.6, 1.45), lens=22),
)
NOTES = dict(
 village_wide='high wide: the beehive-fenced maize field, hero yard, the village of huts and tin house to the right, the uncle farm to the left, acacias, hills and the blue mountain',
 fence_line='eye level along the hive fence from its front-left corner: posts, tin roofs, hives and the wire receding past the maize',
 hive_close='one hive hanging on the wire under its tin roof, the wire and the next hives receding (bees dormant at the slots)',
 yard_two_shot='hero and uncle in the yard in front of the fence: jerrycans, stools, baskets, hoes, chickens, the goat, the fire pit',
 field_night_wide='high wide at night: the whole fence ring round the field, the herd outside it, fire and lantern pools, moon key',
 fence_low_night='low at the fence at night: hives and wire in the moonlight, the matriarch arriving, firelight pool in the yard',
 push_side='side view along the front fence for the push: the wire bows in and the wave travels outward with the swinging hives and bees',
 trunk_close='close on the matriarch head height at the fence: bees at eyes and trunk, wire and hives behind',
 uncle_field_morning="the uncle's trampled field in morning light: flattened stalks, broken thorn fence, footprints, cans down",
 uncle_hang='the uncle on his stool by his own fence hanging his first hive: morning light, trampled field behind',
)
PRESETS = dict(
 village_wide=dict(light='DAY', state='fs3', staging=[('hero', 'hero_fence'), ('uncle', 'uncle_yard'), ('woman', 'villager_woman'), ('kid', 'villager_kid'), ('oldman', 'villager_oldman')]),
 fence_line=dict(light='DAY', state='fs3', staging=[('hero', 'hero_hive')]),
 hive_close=dict(light='DUSK', state='fs3,bees-1', staging=[]),
 yard_two_shot=dict(light='DAY', state='fs3', staging=[('hero', 'hero_yard'), ('uncle', 'uncle_yard')]),
 field_night_wide=dict(light='NIGHT', state='fs3', staging=[('elephant', 'herd_a'), ('matriarch', 'herd_b'), ('elephant', 'herd_c'), ('elephant', 'herd_d'), ('calf', 'herd_calf')]),
 fence_low_night=dict(light='NIGHT', state='fs3', staging=[('matriarch', 'matriarch_arrive'), ('elephant', 'ele_3')]),
 push_side=dict(light='NIGHT', state='fs3,wp0.35,bees0.35', staging=[('matriarch', 'matriarch_push'), ('elephant', 'ele_3')]),
 trunk_close=dict(light='NIGHT', state='fs3,wp0.5,bees0.55,bloc', staging=[('matriarch', 'matriarch_push')]),
 uncle_field_morning=dict(light='MORNING', state='fs3,uf1', staging=[('uncle', 'uncle_field')]),
 uncle_hang=dict(light='MORNING', state='fs3,uf1,uh1', staging=[('uncle', 'uncle_stool')]),
)
CROWD_STAGING = [('uncle', 'uncle_night'), ('woman', 'villager_woman'), ('kid', 'villager_kid'), ('oldman', 'villager_oldman'), ('woman', 'villager_woman2'), ('man', 'villager_man')]
MATRIARCH_EYE = (1.0, 4.0, 2.55)

def apply_state(state):
    """CLI state tokens (comma separated): fs<k> fence stage, wp<t> wire push, bees<t>[/<burst>] (t<0 sleeping), btgt (stream to the matriarch's eyes), bloc (local cloud at her head),
    uf<k> uncle field, uh<k> uncle hive, cr<k> crowd props."""
    toks = [s for s in (state or '').split(',') if s]; push = None; bees = None; tgt = None; loc = None
    for tk in toks:
        if tk.startswith('fs'): STATE['stage'] = int(float(tk[2:]))
        elif tk.startswith('wp'): push = float(tk[2:])
        elif tk.startswith('bees'): v = tk[4:].split('/'); bees = (float(v[0]), float(v[1]) if len(v) > 1 else 1.0)
        elif tk == 'btgt': tgt = MATRIARCH_EYE
        elif tk == 'bloc': loc = ((1.5, 3.9, 2.45), 0.9, 380)
        elif tk.startswith('uf'): set_uncle_field(float(tk[2:]))
        elif tk.startswith('uh'): set_uncle_hive(float(tk[2:]))
        elif tk.startswith('cr'): set_crowd_props(float(tk[2:]))
    STATE['push_t'] = push if push is not None else -1.0
    STATE['bees_args'] = None; _update_fence()
    if bees is not None: set_bees(bees[0], bees[1], tgt, loc)

def make_camera(c):
    sc = bpy.context.scene; cd = bpy.data.cameras.new('cam'); cd.lens = c.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False; cd.clip_end = 3000; cd.clip_start = 0.05
    ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); ob.location = c['loc']
    ob.rotation_euler = (Vector(c['look']) - Vector(c['loc'])).to_track_quat('-Z', 'Y').to_euler(); sc.camera = ob; return ob

def build(preset=None, light=None, clear=True, dress=True):
    """build the whole set for a preset (and light state DAY | DUSK | NIGHT | MORNING, default = the preset's), return the anchors dict. Hooks are at the preset's default state."""
    t0 = time.time(); preset = preset or 'village_wide'; PR = PRESETS[preset]; light = light or PR['light']
    if light not in LIGHTS: raise ValueError('light %r not in %s' % (light, LIGHT_NAMES))
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True)
    global _BS
    G.MATS.clear(); STATE.clear(); _BS = None
    sc = bpy.context.scene; P = LIGHTS[light]; M = palette(light); STATE.update(M=M, light=light, preset=preset, P=P)
    sky(P); hills(light, P); ground(light); clouds(M, light, P)
    if P.get('birds'): birds(M)
    vars_ = [G.maize_variant(M, 100 + i)[0] for i in range(2)] + [G.maize_variant(M, 110, ('maize2', 'cob', 'stalk', 'tassel', 'husk'))[0], G.maize_variant(M, 111, ('maize2', 'cob', 'stalk', 'tassel', 'husk'))[0]]
    for v in vars_: v.hide_render = True; v.hide_viewport = True
    _hero_field(M, vars_, light)
    uvars = [G.maize_variant(M, 120 + i, ('maize2', 'cob', 'stalk', 'tassel', 'husk'))[0] for i in range(2)] + [G.maize_variant(M, 130, ('maize', 'cob', 'stalk', 'tassel', 'husk'))[0]]
    for v in uvars: v.hide_render = True; v.hide_viewport = True
    _uncle_field(M, uvars)
    build_fence(M)
    props = MB('props'); _hero_yard(M, light, props); _village(M, light, props); _uncle_farm(M, light, props); props.finish()
    _trees(M, light)
    cams = {k: dict(v) for k, v in CAMS.items()}
    cl = [(c['loc'][0], c['loc'][1], c['look'][0] - c['loc'][0], c['look'][1] - c['loc'][1], 160 if dress else 0) for k, c in cams.items() if k not in ('village_wide', 'field_night_wide')]
    _grass(M, light, cl if dress else [])
    _uncle_fence(M, light); _uncle_hive_unit(M); _crowd(M, light)
    # --- lights
    k = P['key']; kd = Vector(P['key_dir']).normalized(); d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    fl = P['fill']; a = bpy.data.lights.new('bounce', 'AREA'); a.shape = 'SQUARE'; a.size = 160.0; a.color = fl[:3]; a.energy = 2600 * fl[3]; a.use_shadow = False
    ob = bpy.data.objects.new('bounce', a); ob.location = (0, 30, 0.04); ob.rotation_euler = (math.pi, 0, 0); sc.collection.objects.link(ob)
    for (pos, col, watt, rad) in P.get('lamps', []):
        l = bpy.data.lights.new('lamp', 'POINT'); l.color = col; l.energy = watt; l.shadow_soft_size = rad; ob = bpy.data.objects.new('lamp', l); ob.location = pos; sc.collection.objects.link(ob)
    if P.get('moon'):
        mb = MB('moon'); mm = mat_emit('moon', '#c4d4ff', 1.15); cp = Vector(CAMS[preset]['loc']) - kd * 330; mb.ell(mm, cp, (4.2, 4.2, 4.2), (24, 16)); mb.finish()
    STATE['uf'] = 0.0; set_uncle_field(0.0); STATE['stage'] = 3; STATE['push_t'] = -1.0; _update_fence(); STATE['bees_args'] = None
    apply_state(PR['state'])
    A = anchors(preset); A['build_s'] = round(time.time() - t0, 1); return A

def anchors(preset=None):
    preset = preset or STATE['preset']; PR = PRESETS[preset]
    return dict(preset=preset, light=STATE['light'], cams={k: dict(loc=v['loc'], look_at=v['look'], lens=v['lens']) for k, v in CAMS.items()}, cam=dict(loc=CAMS[preset]['loc'], look_at=CAMS[preset]['look'], lens=CAMS[preset]['lens']),
                cam_name=preset, cam_notes=dict(NOTES), stand=dict(STAND), heights=dict(HEIGHT), units=[dict(i=u['i'], s=round(float(u['s']), 3), pos=tuple(round(c, 3) for c in u['pos']), yaw=round(u['yaw'], 4)) for u in UNITS],
                wire=dict(z=WIRE_Z, ring=(RX0, RY0, RX1, RY1), length=round(float(S_TOT), 2), push_point=PUSH_S0, push_xy=(1.0, RY0), seq_s=SEQ_T, wave_speed=WAVE_C), matriarch_eye=MATRIARCH_EYE,
                staging={k: [(r, m) for r, m in v['staging']] for k, v in PRESETS.items()}, render=dict(samples_final=SAMPLES_FINAL, resolution=(W, H), threads=4, denoise='OIDN', dof=None), key_dir=tuple(Vector(STATE['P']['key_dir']).normalized()))

def _staging(preset, state=''):
    if 'cr' in (state or '') and any(t.startswith('cr') and float(t[2:] or 0) > 0 for t in state.split(',')): return CROWD_STAGING
    return PRESETS[preset]['staging']

def stage_placeholders(preset, cam_loc, state=''):
    _clear_actors(); out = []
    for i, (role, mk) in enumerate(_staging(preset, state)): out.append(place_actor(role, STAND[mk], face_to=cam_loc, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(preset, state=''):
    """[(role, stand, head_top_y_px, chin_y_px, feet_y_px)] at 720x1280 (caption rule: chins above y 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for (role, mk) in _staging(preset, state):
        h = HEIGHT[role]; m = Vector(STAND[mk]); big = role in ('matriarch', 'elephant', 'calf'); top = m + Vector((0, 0, h)); chin = m + Vector((0, 0, h * (0.62 if big else 0.84)))
        a = world_to_camera_view(sc, cam, top); b = world_to_camera_view(sc, cam, chin); f = world_to_camera_view(sc, cam, m)
        out.append((role, mk, round((1 - a.y) * H), round((1 - b.y) * H), round((1 - f.y) * H)))
    return out

# ============================================================================ render
SAMPLES_FINAL = 40
def setup_render(sc, quality='final'):
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = SAMPLES_FINAL if quality == 'final' else 14; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 1; cy.transmission_bounces = 0; cy.transparent_max_bounces = 6
    cy.use_light_tree = True; cy.filter_width = 1.2; cy.sample_clamp_indirect = 8.0; sc.render.threads = 4
    f = 1 if quality == 'final' else 2; sc.render.resolution_x = W // f; sc.render.resolution_y = H // f; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = STATE['P'].get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'

def render(path):
    """render the current scene to path (PNG) with the light-state grade; returns (wall s, cpu s)."""
    sc = bpy.context.scene; t0 = time.time(); c0 = time.process_time(); sc.render.filepath = path + '.tmp.png'; bpy.ops.render.render(write_still=True)
    im = Image.open(path + '.tmp.png').convert('RGB'); a = np.asarray(im, dtype=np.float32) / 255.0; g = a.mean(-1, keepdims=True); a = np.clip(g + (a - g) * STATE['P'].get('sat', 1.12), 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(path); os.remove(path + '.tmp.png'); return time.time() - t0, time.process_time() - c0

def cli_render(specs=None, quality='final', outdir=None, actors=True):
    """specs: ['preset' | 'preset:LIGHT' | 'preset:LIGHT:state' | 'preset:LIGHT:state:cam']"""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        p = spec.split(':'); pr = p[0]; lt = p[1] if len(p) > 1 and p[1] else None; st = p[2] if len(p) > 2 else None; nm = p[3] if len(p) > 3 and p[3] else pr
        A = build(pr, lt); sc = bpy.context.scene; setup_render(sc, quality)
        if st is not None: apply_state(st)
        stt = st if st is not None else PRESETS[pr]['state']; c = CAMS[nm]; make_camera(c)
        if actors: stage_placeholders(pr, c['loc'], stt)
        bpy.context.view_layer.update(); hp = head_pixels(pr, stt) if actors else []
        tag = '%s_%s' % (nm, STATE['light']) + ('_' + stt.replace(',', '_').replace('/', '-') if st is not None else '')
        w, cpu = render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(cpu, 1), hp)
        print('%s %s: build %.0f s, %.1f s wall, %.1f s cpu, heads %s' % (quality, tag, A['build_s'], w, cpu, hp), flush=True)
    return res

def digest():
    return hashlib.sha1(json.dumps([[o.name, [round(v, 3) for v in o.matrix_world.translation]] for o in sorted(bpy.data.objects, key=lambda o: o.name)]).encode()).hexdigest()[:12]

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'): cli_render(arg or None, 'final' if cmd == 'final' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
    elif cmd == 'digest': build(arg[0] if arg else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)
