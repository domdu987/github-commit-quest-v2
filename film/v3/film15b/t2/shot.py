#!/usr/bin/env python3
"""T2 of film 15 v2 (16.30-28.73 s, g 489-862 + 6 handle frames each side: g 483..868). Location A (Medford 1963), HERO golden hour.

 s1  g483-564  over-the-shoulder push-in on the laughing coach (back-view Dick, left foreground, rocking)
 s2  g564-687  side tracking along the bleacher front (coach mimes the broken neck, points; boys laugh); coach quote 17.80-23.55
 s3  g687-708  PUNCH CLOSE-UP 1 on the coach, "ดูเอง" (22.9-23.6)
 s4  g708-740  swing back to a wide of the pit: Dick runs, flops (arch at 24.6 = g738), the photographer's FLASH
 s5  g740-751  push THROUGH the flash: white-out, the newspaper page arrives
 s6  g751-838  page fills the frame (25.0-26.0), pulls back to reveal the reader, the laughing coach and boys (-27.9)
 s7  g838-868  push INTO the newspaper photo; at g 862 the photo fills the frame (T3 starts there).

    python3 shot.py probe g1,g2,...            preview stills -> work/probe_gXXX.png
    python3 shot.py render a:b[:step] out_dir [--scale 0.5] [--samples 6]
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'set3d15'), os.path.join(V3, 'cast15'), os.path.join(V3, 'stage')]
import numpy as np
import v2_a as V
import v2_a_shots as SHT
from v2_a import F, STATE, U, DM
import cast15
import bpy
from mathutils import Vector, Matrix

WORK = os.path.join(HERE, 'work'); os.makedirs(WORK, exist_ok=True)
G0, G1 = 489, 862                      # take range (T2 owns g 489..861; 862 is the first frame of T3)
FIRST_G, LAST_G = G0 - 6, G1 + 6       # 483 .. 868 with handles
def T(g): return g / 30.0

# ---------------------------------------------------------------- marks (metres)
COACH = (10.4, 2.6)
DICK_MARK = (5.6, -0.8)
PAGE_C = Vector((10.2, 4.2, 1.18))     # the newspaper page centre (world m); the page faces -x (towards the field)
PAGE_W = 0.74                           # page width m (the reader holds it wide)
PAGE_H = PAGE_W * 3200 / 2400
# photo rectangle on the page texture (px of the 2400 x 3200 page): see v2_a.tex_newspaper
PHOTO = dict(x0=110, x1=110 + (2400 - 220 - 650), y0=1450, y1=1450 + int((2400 - 220 - 650) * 1050 / 1500))

# ---------------------------------------------------------------- helpers: smooth interpolation
def ease(u, a=2.2):
    u = min(max(u, 0.0), 1.0); return u ** a / (u ** a + (1 - u) ** a)

def hermite(knots, t):
    """C1 cubic Hermite through (t_i, vec_i) with Catmull-Rom (finite difference) tangents; zero tangent at both ends (eased start / stop)."""
    ts = [k[0] for k in knots]; ps = [np.array(k[1], float) for k in knots]
    if t <= ts[0]: return ps[0]
    if t >= ts[-1]: return ps[-1]
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t)
    def tan(j):
        if j == 0 or j == len(ts) - 1: return np.zeros_like(ps[0])
        return 0.6 * (ps[j + 1] - ps[j - 1]) / (ts[j + 1] - ts[j - 1])
    h = ts[i + 1] - ts[i]; u = (t - ts[i]) / h; u2, u3 = u * u, u * u * u
    return (2 * u3 - 3 * u2 + 1) * ps[i] + (u3 - 2 * u2 + u) * h * tan(i) + (-2 * u3 + 3 * u2) * ps[i + 1] + (u3 - u2) * h * tan(i + 1)

# ---------------------------------------------------------------- camera paths (metres)
# A: g483..741 (before the white-out): OTS -> side tracking -> punch CU -> swing to the pit wide
CAM_A = [  # t (s), loc, look
    (T(483), (4.6, -2.7, 1.55), (10.2, 2.3, 1.38)),
    (T(564), (7.9, 0.5, 1.38), (10.4, 2.7, 1.32)),
    (T(621), (7.5, 3.5, 1.22), (10.5, 2.8, 1.28)),
    (T(668), (8.5, 4.7, 1.15), (10.4, 2.7, 1.30)),
    (T(684), (9.05, 4.0, 1.30), (10.4, 2.62, 1.30)),        # punch in
    (T(707), (9.25, 3.72, 1.32), (10.4, 2.62, 1.28)),       # CU 1 (slow creep, never static)
    (T(724), (3.0, -0.7, 1.6), (0.6, 5.4, 1.5)),            # swing to the pit
    (T(741), (2.1, 0.2, 1.5), (-0.1, 5.6, 1.6)),
]
def cam_a(t):
    ts = [k[0] for k in CAM_A]; L = hermite([(k[0], k[1]) for k in CAM_A], t); K = hermite([(k[0], k[2]) for k in CAM_A], t)
    return L, K

def page_cam(t):
    """B: g >= 744: camera in front of the page (page faces -x). dist d (m), lateral arc, look at the page centre -> photo centre."""
    # distance profile
    kn = [(T(744), 0.80), (T(780), 0.92), (T(800), 1.25), (T(838), 3.6), (T(862), 0.50), (T(868), 0.44)]
    # use ease between 780->838 (pull back) and 838->862 (push in) separately
    t0, t1 = T(780), T(838)
    if t <= T(780): d = 0.80 + 0.12 * ((t - T(744)) / (T(780) - T(744)))
    elif t <= T(838): d = 0.92 + (3.6 - 0.92) * ease((t - t0) / (t1 - t0), 1.9)
    else:
        u = (t - T(838)) / (T(862) - T(838)); d = 3.6 + (0.50 - 3.6) * ease(u, 2.0) if u <= 1 else 0.50 - 0.5 * (u - 1) * 0.0 - 0.30 * (u - 1)   # after g862: keep creeping in
    # look target on the page: page centre -> photo centre as we push in
    pc = page_point(0.365, 0.62)
    w = ease((t - T(838)) / (T(862) - T(838)), 1.6) if t > T(838) else 0.0
    look = PAGE_C * (1 - w) + pc * w
    arc = 0.0
    if T(780) < t < T(862):
        u = (t - T(780)) / (T(862) - T(780)); arc = -1.1 * math.sin(math.pi * min(u, 1.0)) * (1 - ease((t - T(838)) / (T(862) - T(838)), 1.4) if t > T(838) else 1.0)
    rise = 0.0
    if T(780) < t < T(862):
        u = (t - T(780)) / (T(862) - T(780)); rise = 0.30 * math.sin(math.pi * min(u, 1.0)) * (1 - w)
    loc = Vector((look.x - d, look.y + arc, look.z + rise))
    return loc, look

def page_point(u, v):
    """world point (m) of page texture coordinates u (0..1 from the left of the page as the viewer sees it) and v (0..1 from the BOTTOM)."""
    return Vector((PAGE_C.x, PAGE_C.y - (u - 0.5) * PAGE_W, PAGE_C.z + (v - 0.5) * PAGE_H))

# ---------------------------------------------------------------- the page mesh in the world
_PAGE_MAT = {}
def world_page(name='newspaper', bend=0.045, roll_deg=-2.0):
    png = V.tex_newspaper()
    m = V.mat_tex('newspaper', png, k=0.92, tint=(1.0, 0.95, 0.84))
    w, h = PAGE_W, PAGE_H; right = Vector((0, -1, 0)); up = Vector((0, 0, 1)); fwd = Vector((1, 0, 0))   # viewer looks +x, so the page front faces -x
    cr, sr = math.cos(math.radians(roll_deg)), math.sin(math.radians(roll_deg)); rt = right * cr + up * sr; upv = up * cr - right * sr
    nu, nv = 14, 18; Vv = []; Fc = []; UV = []
    for j in range(nv + 1):
        for i in range(nu + 1):
            u = i / nu; v = j / nv; xx = (u - 0.5) * w; yy = (v - 0.5) * h
            z = bend * w * (1 - (2 * u - 1) ** 2) * 0.5                                       # the page bows toward the viewer (-x)
            Vv.append(PAGE_C + rt * xx + upv * yy - fwd * z); UV.append((u, v))
    for j in range(nv):
        for i in range(nu): a = j * (nu + 1) + i; Fc.append((a, a + 1, a + nu + 2, a + nu + 1))
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in Vv], [], Fc); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for pi, poly in enumerate(me.polygons):
        for li, vi in zip(poly.loop_indices, poly.vertices): uvl.data[li].uv = UV[vi]
    me.materials.append(m); ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob); ob.parent = V.root(); V.L.T.no_bounce(ob); ob.visible_shadow = False
    return ob

# ---------------------------------------------------------------- back-view Dick (cast15 has none): the front sprite with the face painted over by hair
def _back_post(png, res, ppd):
    from PIL import Image, ImageDraw
    im = Image.open(png).convert('RGBA'); d = ImageDraw.Draw(im)
    ox, oy = res['origin_px']; fx, fy = res['feet']; hx, hy = res['anchors']['head']
    cx = ox + (hx - fx) * ppd; cy = oy + (hy - fy) * ppd; r = 0.50 * ppd
    hair = (112, 70, 36, 255); ink = (40, 24, 20, 255); skin = (240, 190, 160, 255)
    for sx in (-1, 1): d.ellipse([cx + sx * r * 0.98 - r * 0.20, cy - r * 0.12, cx + sx * r * 0.98 + r * 0.20, cy + r * 0.34], fill=skin, outline=ink, width=2)   # big ears
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hair, outline=ink, width=3)
    for k in range(-3, 4):                                                                          # tousled spikes on top
        a = math.radians(-90 + k * 22); x0 = cx + math.cos(a) * r * 0.92; y0 = cy + math.sin(a) * r * 0.92
        x1 = cx + math.cos(a + 0.12) * r * 1.30; y1 = cy + math.sin(a + 0.12) * r * 1.30; x2 = cx + math.cos(a + 0.30) * r * 0.92; y2 = cy + math.sin(a + 0.30) * r * 0.92
        d.polygon([(x0, y0), (x1, y1), (x2, y2)], fill=hair, outline=ink)
    for k in range(5): d.arc([cx - r * 0.7 + k * r * 0.1, cy - r * 0.6, cx + r * 0.7 - k * r * 0.1, cy + r * 0.7], 20, 160, fill=(80, 48, 26, 255), width=2)
    im.save(png)

_BACK = {'on': False}
def _patch_sprites():
    ct = V.CT(); sp = ct.sprites
    if getattr(sp, '_orig_render', None) is None:
        sp._orig_render = sp.render_sprites
        def rs(jobs, *a, **k):
            r = sp._orig_render(jobs, *a, **k)
            if _BACK['on']:
                for j, x in zip(jobs, r): _back_post(x['out'], x, j['px_per_D'])
            return r
        sp.render_sprites = rs

def clean_set():
    """remove the infield clutter (hurdle beams, mats, loungers) from the OTS / bleacher-front area so the coach and boys read (faces of midA / folk meshes whose centre lies in the box)."""
    import bmesh
    bpy.context.view_layer.update(); M = V.root().matrix_world.inverted(); n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.name.startswith(('midA', 'folk', 'gdetail')): continue
        bm = bmesh.new(); bm.from_mesh(o.data); kill = []
        for f in bm.faces:
            c = M @ (o.matrix_world @ f.calc_center_median())
            if 3.3 < c.x < 10.9 and -5.2 < c.y < 3.6 and c.z > 0.03: kill.append(f)
        if kill: bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(o.data); o.data.update(); n += len(kill)
        bm.free()
    return n

# ---------------------------------------------------------------- scene state
S = {}
def build(light='HERO'):
    A = V.build_a2(light, rays=False); sc = bpy.context.scene; _patch_sprites()
    SHT.RAYS_ON = False; clean_set()
    sc.frame_start = FIRST_G; sc.frame_end = LAST_G
    S['A'] = A; S['sc'] = sc; S['M'] = STATE['marks_m']
    mb = V.S.MB('rbench'); Mm = STATE['M']
    mb.box(Mm['wood'], (10.75, 4.2, 0.15), (0.6, 0.9, 0.30)); mb.box(Mm['wood'], (11.0, 4.2, 0.62), (0.5, 0.9, 0.07)); V.L.fin(mb)
    S['page'] = world_page('newspaper_f')
    S['cam'] = F.make_camera(F.cam_from((0, 0, 0), (0, 1, 0), lens=22.0))
    sc.camera = S['cam']
    return A

def set_quality(q, scale=None, samples=None):
    sc = S['sc']; F.setup_render(sc, 'final' if q == 'final' else 'preview')
    if q != 'final': sc.cycles.samples = 6
    if samples: sc.cycles.samples = samples
    if scale: sc.render.resolution_percentage = int(scale * 100)
    sc.view_settings.exposure = EXPOSURE; V.set_grade_sat(sc, GRADE)
EXPOSURE = -1.25; GRADE = 1.12

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.orphans_purge(do_recursive=True)

def talk(g, seed=0.0, lvl=1.0): return cast15.talk_mouth(g, lvl, seed)
def in_quote(g): return 534 <= g <= 706          # 17.80 .. 23.55 s (g = round(t*30)), the only frames where a mouth moves

def D(p): return (p[0] * U, p[1] * U)

def put_stand(tag, cast, pose, xy_m, cl, ppd=160, yaw_fixed=None, contact=(1.7, 0.55), **kw):
    return V.ground_card(tag, cast, pose, D(xy_m), cl, ppd=ppd, contact=contact, yaw_fixed=yaw_fixed, **kw)

# runner path (metres): the J-curve from the mark to the take-off
RUN = [(5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9), (1.2, 4.2)]
def run_pos(u):
    u = min(max(u, 0), 1); n = len(RUN) - 1; s = u * n; i = min(int(s), n - 1); f = s - i
    return (RUN[i][0] + (RUN[i + 1][0] - RUN[i][0]) * f, RUN[i][1] + (RUN[i + 1][1] - RUN[i][1]) * f)

G_RUN0, G_TAKE = 709, 730          # run starts / take-off ; arch over the bar at 738 (24.6 s), flash 738
G_FLASH = 738

def bar_pt(cl):
    J = STATE['J']; bar = Vector((0.0, J['y'] * U, F.bar_height_m() * U)); t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * 0.3; return bar

def place_cards(g, cl):
    """all characters for film frame g (camera location cl in D)"""
    M = S['M']; rep = {}
    cam_a = g < 742
    # --- coach
    bob = cast15.laugh_bob(g)
    if g < 534: cp = dict(cast15.pose_for('coach_laugh', 'coach'), bob=bob)
    elif g < 565: cp = dict(cast15.pose_for('coach_wag_a' if (g // 8) % 2 else 'coach_wag_b', 'coach'), mouth=talk(g, 1.0), bob=bob * 0.6)
    elif g < 621: cp = dict(cast15.pose_for('coach_neck', 'coach'), mouth=talk(g, 2.0), bob=bob * 0.5, roll=9 + 6 * math.sin(g * 0.5))
    elif g < 687: cp = dict(cast15.pose_for('coach_point' if (g // 14) % 2 else 'coach_jab', 'coach'), mouth=talk(g, 3.0), bob=bob * 0.5)
    elif g < 707: cp = dict(cast15.pose_for('coach_shout', 'coach'), mouth=talk(g, 4.0), bob=bob * 0.4)
    else: cp = dict(cast15.pose_for('coach_laugh' if g < 770 or (g // 10) % 2 else 'coach_point', 'coach'), bob=bob)
    if g >= 707 and cp.get('mouth') == 'flat': cp['mouth'] = 'smile'
    rep['coach'] = put_stand('c_coach', 'coach', cp, COACH, cl, ppd=(384 if 680 <= g <= 712 else 192), contact=(1.9, 0.6))
    # --- boys at the bleacher front (laugh bob 3 Hz, alternate laugh / point_laugh)
    def boy(tag, cast, xy, ph):
        nm = 'point_laugh' if ((g + ph) // 12) % 2 else 'laugh'
        p = dict(cast15.pose_for(nm, cast), bob=cast15.laugh_bob(g + ph))
        rep[tag] = put_stand(tag, cast, p, xy, cl, ppd=128)
    boy('b1', 'boy1', (9.6, 0.5), 0); boy('b2', 'boy2', (9.4, 5.6), 4); boy('b3', 'boy3', (9.9, 7.0), 7)
    # --- Dick
    if g < 709:
        _BACK['on'] = True
        p = cast15.pose_for('rock_a' if (g // 7) % 2 else 'rock_b', 'dick')
        rep['dick'] = put_stand('d_dick', 'dick', p, (5.8, -1.0), cl, ppd=192, yaw_fixed=None, contact=(1.4, 0.5)); _BACK['on'] = False
    elif g < G_TAKE:
        ph = (g - G_RUN0) / 16.0; xy = run_pos((g - G_RUN0) / float(G_TAKE - G_RUN0))
        rep['dick'] = put_stand('d_dick', 'dick', cast15.run_curved('dick', ph, facing=-1), xy, cl, ppd=192, contact=(1.4, 0.5))
    elif g < 742:
        stages = [(730, 'flop_rise'), (733, 'flop_head'), (736, 'flop_back'), (738, 'flop')]
        nm = [n for s0, n in stages if g >= s0][-1]
        u = (g - G_TAKE) / float(G_FLASH - G_TAKE); u = min(max(u, 0), 1.3)
        bp = bar_pt(cl); x0, z0, y0 = 1.5 * U, 1.15 * U, 4.3 * U
        e = ease(min(u, 1.0), 1.4); x = x0 + (bp.x - x0) * e; y = y0 + (bp.y - y0) * e; z = z0 + (bp.z + 0.03 - z0) * (math.sin(e * math.pi / 2)) + 0.0
        zg = 0.0 if y < 4.7 * U else 0.44 * U
        rep['dick'] = V.ground_card_anchor('f_dick', 'dick', cast15.pose_for(nm, 'dick', facing=-1), ('bar', (x, y, z)), cl, zg, ppd=192, canvas=cast15.CANVAS15_WIDE)
    # --- photographer, flash on G_FLASH
    fl = max(0.0, 1.0 - (g - G_FLASH) / 4.0) if g >= G_FLASH else 0.0
    pn = 'photog_flash' if G_FLASH <= g < G_FLASH + 6 else 'photog_ready'
    pp = dict(cast15.pose_for(pn, 'photographer', facing=1), flash=fl)
    rep['ph'] = put_stand('p_ph', 'photographer', pp, (-3.6, 3.4), cl, ppd=160, contact=(1.5, 0.5))
    # --- reader on the bleacher (card faces the field, -x), 3D page in front of him
    rp = dict(cast15.pose_for('sit_read', 'crowd4'), bob=0.0)
    rep['reader'] = V.ground_card('r_reader', 'crowd4', rp, D((PAGE_C.x + 0.45, PAGE_C.y)), cl, z=0.30 * U, ppd=192, yaw_fixed=-math.pi / 2, contact=(1.2, 0.5))
    return rep

def aim(cam, loc_m, look_m):
    loc = Vector(loc_m) * U; look = Vector(look_m) * U
    cam.location = loc; cam.rotation_euler = (look - loc).to_track_quat('-Z', 'Y').to_euler()
    return tuple(loc)

def cam_for(g):
    t = T(g)
    if g < 744: L, K = cam_a(t); return Vector(L), Vector(K)
    return page_cam(t)

# ---------------------------------------------------------------- per frame
def set_frame(g):
    sc = S['sc']; clear_cards(); sc.frame_set(g)
    loc, look = cam_for(g); cl = aim(S['cam'], loc, look)
    V.rim_on(to_light=(-0.7, -0.6), width=5, strength=0.9)
    rep = place_cards(g, cl)
    S['page'].hide_render = g < 744; S['page'].hide_viewport = g < 744
    if g == G_FLASH: F.flash_bulb(G_FLASH)
    return rep

def white_amount(g):
    if g < G_FLASH: return 0.0
    if g < 744: return min(1.0, 0.3 + 0.25 * (g - G_FLASH))
    if g < 752: return 1.0 - (g - 744) / 8.0
    return 0.0

def render_frame(g, path):
    set_frame(g); sc = S['sc']; sc.render.filepath = path; bpy.ops.render.render(write_still=True)
    w = white_amount(g)
    if w > 0.0:
        from PIL import Image
        a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32) / 255; a = a * (1 - w) + w; Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(path)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'probe':
        gs = [int(x) for x in sys.argv[2].split(',')]; build(); set_quality('preview')
        for g in gs: render_frame(g, os.path.join(WORK, 'probe_g%03d.png' % g)); print('ok', g, flush=True)
    elif cmd == 'render':
        rng = [int(x) for x in sys.argv[2].split(':')]; step = rng[2] if len(rng) > 2 else 1; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        q = 'final'; scale = None; smp = None
        a = sys.argv[4:]
        if '--scale' in a: scale = float(a[a.index('--scale') + 1]); q = 'preview'
        if '--samples' in a: smp = int(a[a.index('--samples') + 1])
        build(); set_quality(q, scale, smp)
        for g in range(rng[0], rng[1] + 1, step):
            p = os.path.join(out, 'g_%04d.png' % g)
            if os.path.exists(p): continue
            t0 = time.time(); render_frame(g, p); print('g', g, round(time.time() - t0, 1), flush=True)
