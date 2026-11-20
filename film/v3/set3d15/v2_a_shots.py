#!/usr/bin/env python3
"""v2_a_shots.py : camera paths + the seven stills of location A v2.   python3 v2_a_shots.py [final|preview] [still ...]   (no still = all seven + sheet)
Camera paths (metres, set-local; convert to D with *V.U): bigzoom1_path(t), t in 0..4.4 s, eased; key_camera(cam, fn, t0, t1) writes one key per frame."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import v2_a as V
from v2_a import F, STATE, U, DM
import bpy
from mathutils import Vector

# ============================================================================= camera paths
def ease_io(u, a=2.6):
    """smooth ease in/out (symmetric power smoothstep): 0..1 -> 0..1, zero speed at both ends. a = steepness of the middle (2 = smoothstep-like, 3+ = long holds at the ends)."""
    u = min(max(u, 0.0), 1.0); return u ** a / (u ** a + (1 - u) ** a)

def catmull(pts, s):
    """uniform Catmull-Rom through pts (list of 3-vectors) at s in [0, len-1] (end points duplicated)."""
    n = len(pts) - 1; s = min(max(s, 0.0), n - 1e-9); i = int(s); u = s - i
    p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[min(i + 1, n)]; p3 = pts[min(i + 2, n)]
    return tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u * u + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u ** 3) for k in range(3))

# BIGZOOM 1 control points (metres). Camera starts 100 m above the school's south-east looking north (pit at 68 % of the frame height, gym at 50 %, the town and hills above), descends over the
# east pine grove (x 36-54, tops at 13-19 m), skims the bleacher (x 11-15) 8 m up, drops behind the pit side and ends medium on Dick at his mark (5.6, -0.8): 3.1 m away, he is 40 % of the frame height.
BZ1 = dict(dur=4.4,
           loc=[(24.0, -12.0, 100.0), (40.0, -30.0, 58.0), (37.0, -16.0, 21.0), (24.0, -9.0, 8.5), (11.0, -6.8, 3.0), (4.6, -3.9, 1.3)],
           look=[(6.0, 50.0, 0.0), (8.0, 16.0, 0.0), (8.0, 8.0, 1.5), (6.5, 3.0, 1.5), (5.8, -0.4, 1.3), (5.7, -0.6, 1.2)],
           ease=2.4)

def bigzoom1_path(t, spec=BZ1):
    """(loc_m, look_m) of the BIGZOOM 1 camera at time t (s), 0..4.4: eased Catmull-Rom through the control points; the look point leads slightly (s + 0.12) so the descent feels like a swoop."""
    u = ease_io(t / spec['dur'], spec['ease']); n = len(spec['loc']) - 1
    return catmull(spec['loc'], u * n), catmull(spec['look'], min(u * n + 0.12, n))

def key_camera(cam, fn, t0, t1, fps=30, lens=22.0, interp='LINEAR'):
    """Key `cam` (object from F.make_camera) every frame from round(t0*fps) to round(t1*fps) following fn(t) -> (loc_m, look_m). Scene frame = round(t*30), as the plan. Returns (f0, f1)."""
    f0 = int(round(t0 * fps)); f1 = int(round(t1 * fps)); sc = bpy.context.scene; sc.frame_start = min(sc.frame_start, f0); sc.frame_end = max(sc.frame_end, f1)
    for f in range(f0, f1 + 1):
        loc, look = fn(f / fps); loc = Vector(loc) * U; look = Vector(look) * U
        cam.location = loc; cam.rotation_euler = (look - loc).to_track_quat('-Z', 'Y').to_euler()
        cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)
    for fc in F.T._fcurves(cam):
        for kp in fc.keyframe_points: kp.interpolation = interp
    cam.data.lens = lens; return f0, f1

def setup_bigzoom1(t0=0.0, light='HERO', **build_kw):
    """Build A v2 and key the BIGZOOM 1 camera 0.0-4.4 s. Place the cast cards afterwards (stills: see below; for a render team: V.ground_card at the marks, facing the camera at that frame)."""
    A = V.build_a2(light, **build_kw); loc, look = bigzoom1_path(0.0)
    cam = F.make_camera(F.cam_from(tuple(c * U for c in loc), tuple(c * U for c in look), lens=22.0)); key_camera(cam, bigzoom1_path, 0.0, BZ1['dur']); return A, cam

# the hero low angle after the zoom (4.45-6.1): a short low push along the run-up to the bar, keyed with the same helper
def t1_hero_low(t):
    u = ease_io((t - 4.45) / 1.65, 1.8); a = np.array((4.6, -3.9, 1.3)); b = np.array((-3.4, 2.6, 0.55)); lk = np.array((0.0, 5.3, 1.9)); la = np.array((5.7, -0.6, 1.2))
    p = a + (b - a) * u; return tuple(p), tuple(la + (lk - la) * u)

# ============================================================================= stills
W, H = 720, 1280
STILL_DIR = os.path.join(V.WORK, 'stills'); os.makedirs(STILL_DIR, exist_ok=True)

def _D(p): return tuple(c * U for c in p)

def _cam(loc_m, look_m, lens=22.0):
    c = F.make_camera(F.cam_from(_D(loc_m), _D(look_m), lens=lens)); return c, tuple(c.location)

GRADE_SAT = dict(s1=1.3, s2=1.3, s3=1.2, s4=1.0, s5=1.1, s6=1.35, s7=1.15)
EXPO = dict(s1=-0.7, s2=-0.85, s3=-1.15, s4=-1.15, s5=-1.15, s6=-0.9, s7=-1.6)
CUR = ['s3']
def _base(light='HERO', **kw):
    A = V.build_a2(light, **kw); sc = bpy.context.scene; F.setup_render(sc, 'final'); sc.cycles.samples = 14; sc.view_settings.exposure = EXPO.get(CUR[0], -0.8); V.set_grade_sat(sc, GRADE_SAT.get(CUR[0], 1.15)); V.CT(); return A, sc

def _put_hero_cards(cl, dick_pose='rock_a', boys=True, coach=True, scale_ppd=128, only=None):
    """Dick at his mark, boys waiting beside him, the coach at the bleacher front: all grounded (feet on the surface, contact + cast shadow)."""
    import cast15
    M = STATE['marks_m']; rep = {}
    def D(p): return (p[0] * U, p[1] * U)
    if coach: rep['coach'] = V.ground_card('c_coach', 'coach', dict(cast15.pose_for('coach_laugh', 'coach'), bob=0.0), D(M['coach_bleacher']), cl, ppd=scale_ppd, contact=(1.9, 0.6))
    if boys:
        rep['b1'] = V.ground_card('c_b1', 'boy1', cast15.pose_for('stand', 'boy1'), D(M['boy_wait_a']), cl, ppd=scale_ppd, yaw_off=8)
        rep['b2'] = V.ground_card('c_b2', 'boy2', cast15.pose_for('laugh', 'boy2'), D(M['boy_wait_b']), cl, ppd=scale_ppd)
        rep['b3'] = V.ground_card('c_b3', 'boy3', cast15.pose_for('rock_b', 'boy3'), D(M['boy_c']), cl, ppd=scale_ppd)
    rep['dick'] = V.ground_card('c_dick', 'dick', cast15.pose_for(dick_pose, 'dick'), D(M['dick_mark']), cl, ppd=scale_ppd, contact=(1.4, 0.5))
    return rep

RAYS_ON = False   # director review: the shafts read as glitches from these angles; set True to use them (V.god_rays)
def rays(seed=11, k=0.28):
    """4 clean soft shafts falling out of the west pine grove edge (x -48..-38) toward the field; strength k."""
    if not RAYS_ON: return
    rr = V.rnd(seed); V.god_rays(STATE['P'], n=4, seed=seed, strength=k, width=(6.0, 9.0), length=(15.0, 20.0), where=[(rr.uniform(-48, -38), 12 + 6 * i) for i in range(4)])

def hero_beam(x, y, k=1.5, width=4.0):
    """one visible shaft that lands on (x, y) m: the sun beam that makes Dick findable in the BIGZOOM start."""
    kd = Vector(STATE['P']['key_dir']).normalized(); top = Vector((x, y, 0)) - kd * 30.0
    V.god_rays(STATE['P'], where=[(top.x, top.y)], width=(width, width), length=(34.0, 34.0), strength=k)

def s1_bigzoom_start(q):
    A, sc = _base(); loc, look = bigzoom1_path(0.0); cam, cl = _cam(loc, look); import cast15
    _put_hero_cards(cl, scale_ppd=48)
    V.spot(5.6, -0.4, r=6.0, k=0.9)
    
    sc.frame_set(0); return cam, 'BIGZOOM 1 start (t 0.0): bird\'s-eye over Medford, Dick at his mark'

def s2_bigzoom_mid(q):
    A, sc = _base(); loc, look = bigzoom1_path(2.65); cam, cl = _cam(loc, look); _put_hero_cards(cl, scale_ppd=96)
    rays()
    return cam, 'BIGZOOM 1 mid (t 2.65): past the pines and the bleacher'

def s3_bigzoom_end(q):
    A, sc = _base(); loc, look = bigzoom1_path(4.4); cam, cl = _cam(loc, look); V.rim_on(to_light=(-0.7, -0.5), width=5, strength=0.9); _put_hero_cards(cl, scale_ppd=160)
    rays()
    return cam, 'BIGZOOM 1 end (t 4.4): medium on Dick at his mark'

def s4_flop_low(q):
    import cast15
    A, sc = _base(); cam, cl = _cam((-1.9, 2.2, 0.45), (0.1, 5.5, 2.3)); V.rim_on(to_light=(-0.8, -0.4), width=5, strength=1.0)
    bar = Vector((0.0, STATE['J']['y'] * U, F.bar_height_m() * U)); t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * 0.3
    pose = cast15.pose_for('flop', 'dick'); zg = (0.44 * U)
    r = V.ground_card_anchor('f_dick', 'dick', pose, ('bar', tuple(bar)), cl, zg, ppd=192, canvas=cast15.CANVAS15_WIDE)
    M = STATE['marks_m']
    V.ground_card('f_b1', 'boy1', cast15.pose_for('gape', 'boy1'), (M['boys_bench_a'][0] * U + 0.8, M['boys_bench_a'][1] * U - 2.2), cl, ppd=128)
    rays()
    
    return cam, 'T1 low hero: Dick flops over the bar'

def s5_ots_coach(q):
    import cast15
    A, sc = _base(); M = STATE['marks_m']; cam, cl = _cam((7.6, -0.2, 1.3), (10.4, 2.6, 1.3)); V.rim_on(to_light=(0.6, -0.7), width=5, strength=0.8)
    # coach: the subject (30 % of the frame height), 4 m from the lens; real Dick card in the left foreground, head turned away toward the coach (shoulder view)
    V.ground_card('o_coach', 'coach', dict(cast15.pose_for('coach_laugh', 'coach'), bob=0.0), (10.4 * U, 2.6 * U), cl, ppd=160, contact=(1.9, 0.6))
    V.ground_card('o_dick', 'dick', dict(cast15.pose_for('rock_a', 'dick'), yaw=-0.9), (8.85 * U, 1.35 * U), cl, ppd=160, yaw_off=35)
    V.ground_card('o_b1', 'boy1', cast15.pose_for('point_laugh', 'boy1'), (11.2 * U, 0.2 * U), cl, ppd=128)
    rays(); return cam, 'T2 over-the-shoulder toward the coach on the bleachers'

def s6_newspaper(q):
    A, sc = _base(people=True, rays=False); cam, cl = _cam((10.7, 4.0, 1.4), (0.0, 7.0, 1.2)); V.newspaper(cl, tuple(_D((0.0, 7.0, 1.2))), dist=0.72, fill=1.0, roll_deg=-2.0, hands=False)
    sc.frame_set(1); return cam, 'T2 newspaper: the front page fills the frame'

def s7_buried(q):
    import cast15
    A, sc = _base(); M = STATE['marks_m']; cam, cl = _cam((-0.5, 6.2, 1.15), (-1.35, 8.9, 1.25)); V.rim_on(to_light=(-0.8, -0.5), width=5, strength=0.9); ct = V.CT()
    mk = Vector(_D((-1.35, 8.0, 0.80))); pose = cast15.pose_for('coach_buried', 'coach')
    r = ct.put('b_coach', 'coach', pose, tuple(mk), cl, canvas=cast15.CANVAS15_WIDE, dz=0.0, shadow=None, ppd=192)
    f0 = 2040; F.sawdust_spray(f0 - 9, (mk.x, mk.y, mk.z + 0.2), strength=1.7, seed=3)
    for i, (cast, pn, sz) in enumerate((('boy1', 'sit_laugh', 0), ('boy2', 'sit_gape', 1), ('boy3', 'sit_laugh', 2))):
        p = M['boys_bench_a'] if i == 0 else (M['boys_bench_b'] if i == 1 else M['boys_bench_c']); V.ground_card('s_b%d' % i, cast, cast15.pose_for(pn, cast), (p[0] * U + 0.2, p[1] * U), cl, z=0.0, ppd=128)
    rays()
    
    sc.frame_set(f0); return cam, 'T7 coach buried in the sawdust'

STILLS = [('s1', s1_bigzoom_start), ('s2', s2_bigzoom_mid), ('s3', s3_bigzoom_end), ('s4', s4_flop_low), ('s5', s5_ots_coach), ('s6', s6_newspaper), ('s7', s7_buried)]

def sheet(names=None):
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, V.WORK); import stats as ST
    names = names or [n for n, _ in STILLS]; fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17); LB = 44; PW, PH = 360, 640
    Sh = Image.new('RGB', (PW * len(names), PH + LB), (16, 16, 20)); d = ImageDraw.Draw(Sh)
    for i, n in enumerate(names):
        p = os.path.join(STILL_DIR, n + '.png')
        if not os.path.exists(p): continue
        st = ST.stats(p); Sh.paste(Image.open(p).convert('RGB').resize((PW, PH), Image.LANCZOS), (i * PW, 0))
        d.text((i * PW + 6, PH + 3), '%s' % LABELS.get(n, n), fill=(235, 235, 235), font=fnt); d.text((i * PW + 6, PH + 23), 'sat %.2f viv %d luma %d' % (st['sat'], st['vivid'], st['luma']), fill=(255, 214, 80), font=fnt)
    Sh.save(os.path.join(V.WORK, 'sheet.jpg'), quality=90)
LABELS = dict(s1='1 BIGZOOM start', s2='2 BIGZOOM mid', s3='3 BIGZOOM end', s4='4 T1 low hero flop', s5='5 T2 over-shoulder', s6='6 T2 newspaper', s7='7 T7 coach buried')

if __name__ == '__main__':
    q = 'final'; names = []
    for a in sys.argv[1:]:
        if a in ('final', 'preview'): q = a
        else: names.append(a)
    log = {}; sys.path.insert(0, V.WORK); import stats as ST
    for n, fn in STILLS:
        if names and n not in names and names != ['sheet']: continue
        if names == ['sheet']: break
        bpy.ops.wm.read_factory_settings(use_empty=True) if False else None
        CUR[0] = n; cam, label = fn(q); sc = bpy.context.scene
        if q == 'preview': F.setup_render(sc, 'preview'); sc.cycles.samples = 6; sc.view_settings.exposure = EXPO.get(CUR[0], -0.8)
        out = os.path.join(STILL_DIR, n + ('' if q == 'final' else '_prev') + '.png'); t0 = time.time(); wall, cpu = F.T.render(out); st = ST.stats(out)
        log[n] = dict(label=label, wall=round(wall, 1), cpu=round(cpu, 1), build_s=round(STATE.get('v2_build_s', 0), 1), **{k: round(v, 3) for k, v in st.items()}); print(n, json.dumps(log[n]), flush=True)
    if q == 'final' and (not names or names == ['sheet']): sheet()
