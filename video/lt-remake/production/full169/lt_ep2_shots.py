# EP.2 — กฎสามข้อหลังฝาตู้ไฟ กับกล้วยสุกทั้งเครือ (e2_01..e2_23, 118.54 s), exec'd by lt_epx.py (LT_EP=2). Cameras are framed for 16:9.
DUR = 118.54
DOOR_OPEN = (-2.0, -1.0)                    # the rented-room door stays open (Kim in the doorway)
WS = (-3.6, 6.6, 0.0)                       # the welder's steel stool in front of Hong's shop
WSTAND = (-2.4, 6.3, 0.0)
HONG_T = (-3.3, 4.15, 0.0)                   # Hong behind the charging table
TABLE = ((-2.55, 5.0, 0.0), math.pi / 2)
FUSE = ((-2.83, 12.25, 0.95), math.pi / 2)  # Kim's old fuse box on the pole at the head of the soi
TRANS = (-2.48, 12.25, 7.45)
HUG = (-6.25, 2.95, 0.0)
ROOM = ANCH.get('room', {})
DIN = tuple(ROOM.get('door_inside_mark', (0.0, 3.6, 0.0))); DWY = tuple(ROOM.get('doorway_mark', (0.05, 4.45, 0.0)))
ZAP_P = (-3.12, 6.78, 1.02)                 # where the phones touch his arm

def _nb(i): return ('nb_man', 'nb_man_phone') if i % 2 == 0 else ('nb_woman', 'nb_woman_phone')
def queue(n, x0=-1.75, y0=5.9, dy=-0.95, skip=0, exprs=('excited', 'happy', 'neutral', 'excited', 'shocked')):
    out = []
    for i in range(skip, n):
        who, pose = _nb(i); x = x0 + (0.18 if i % 2 else -0.05); y = y0 + dy * i
        out.append(('q%d' % i, who, (x, y, 0.0), T((0, pose, {'expr': exprs[i % len(exprs)], 'yaw': 0.3 if i % 2 else -0.3})), bool(i % 3 == 1), {'static': True}))
    return out
WELD_SIT = lambda expr='unimpressed', **k: ('you', 'welder', WS, T((0, 'welder_sit_stool', dict({'stool': True, 'expr': expr, 'yaw': 0.7}, **k))), False)

# ---------------------------------------------------------------- props
def P_table(price):
    def f(A, SET, lv):
        import lt_props as LP; return dict(ct=LP.charge_table(TABLE[0], TABLE[1], price=price))
    return f
def P_fuse(door=0.0, plate=0.0):
    def f(A, SET, lv):
        import lt_props as LP; return dict(fb=LP.fuse_box(FUSE[0], FUSE[1], door_deg=door, plate_deg=plate))
    return f
CABLE = [((-3.58, 6.62, 0.45), (-3.45, 9.0, 0.04), 0.05), ((-3.45, 9.0, 0.04), (-2.86, 12.05, 0.3), 0.05), ((-2.86, 12.05, 0.3), (-2.66, 12.2, 7.15), 0.0)]
def P_cable(A, SET, lv):
    import lt_props as LP; pts = []
    for k, (a, b, sag) in enumerate(CABLE): pts += LP.cable(a, b, sag=sag, name='hcable%d' % k, clamp=(k == 0))[(1 if pts else 0):]
    return dict(cable=pts)
def P_ripe(A, SET, lv):
    import lt_props as LP; LP.recolor('6aa83a', '#f5c518'); return {}

# ---------------------------------------------------------------- per-frame hooks
def _phone_zap(mb, g, t, A, SET, sh, X):
    Vector = X['Vector']; p = Vector(sh.get('zap_p', ZAP_P))
    if random.Random(g).random() < 0.8: X['sparks_at'](mb, p, g, n=10, big=0.6)
    ra = random.Random(g * 3)
    for k in range(3):
        a = p; b = p + Vector((ra.uniform(-0.25, 0.25), ra.uniform(-0.25, 0.25), ra.uniform(-0.2, 0.25))); pts = [a]
        for q in range(1, 5): pts.append(a.lerp(b, q / 5) + Vector((ra.uniform(-0.04, 0.04), ra.uniform(-0.04, 0.04), ra.uniform(-0.04, 0.04))))
        pts.append(b)
        for p0, p1 in zip(pts[:-1], pts[1:]): mb.frustum(tuple(p0), tuple(p1), 0.005, 0.005, X['boltc'], seg=4); mb.frustum(tuple(p0), tuple(p1), 0.016, 0.016, X['bolth'], seg=5)
    return True
def _fuse_open(mb, g, t, A, SET, sh, X):
    import lt_props as LP; a0, a1, d0, d1 = sh['door_t']; u = max(0.0, min(1.0, (t - a0) / (a1 - a0))); LP.set_fuse(X['P']['fb'], door_deg=d0 + (d1 - d0) * ease(u)); return False
def _ripen(mb, g, t, A, SET, sh, X):
    import lt_props as LP; a0, a1 = sh['ripe_t']; u = max(0.0, min(1.0, (t - a0) / (a1 - a0))); LP.recolor('6aa83a', LP.lerp_hex('#6aa83a', '#f5c518', u))
    if 0 < u <= 1 or a1 <= t < a1 + 0.8:              # sparkles around the bunch as it turns
        Vector = X['Vector']; c = Vector(ANCH.get('soi', {}).get('banana', (-5.65, 2.33, 2.9))) + Vector((0, 0, 0.6)); r = random.Random(g)
        star = X['S'].mat_emit('FX_star', '#fff6c0', strength=12.0)
        for k in range(14):
            p = c + Vector((r.uniform(-0.5, 0.5), r.uniform(-0.5, 0.5), r.uniform(-0.7, 0.6))); mb.sphere(tuple(p), r.uniform(0.012, 0.03), star, seg=6, rings=4)
        return True
    return False
def _current(mb, g, t, A, SET, sh, X):
    import lt_props as LP; a0, a1, u0, u1 = sh['cur']; u = u0 + (u1 - u0) * max(0.0, min(1.0, (t - a0) / (a1 - a0)))
    if t < a0: return False
    pts = X['P']['cable']; LP.current_along(mb, pts, u, g, n=4)
    pl = X['plight']
    if pl is not None:
        L = len(pts) - 1; i = min(L - 1, int(u * L)); pl.location = pts[i] + X['Vector']((0.2, 0, 0.3)); pl.data.energy = 220.0; pl.data.color = (0.7, 0.85, 1.0)
    return True
def _blast(mb, g, t, A, SET, sh, X):
    import lt_props as LP; u = t - sh['blast_t']; LP.blast(mb, TRANS, u, g)
    pl = X['plight']
    if pl is not None: pl.location = X['Vector'](TRANS) + X['Vector']((1.2, -1.0, 0.0)); pl.data.color = (1.0, 0.6, 0.3); pl.data.energy = 0.0 if u < 0 else (20000.0 * max(0.08, 1 - u / 1.5))
    return u >= 0
def _glow(mb, g, t, A, SET, sh, X):
    import lt_props as LP; a0, lv = sh['glow']
    if t < a0: return False
    LP.glow_body(mb, sh['glow_at'], t, lv, height=1.6, g=g); return True
FX_HOOKS.update(phone_zap=_phone_zap, fuse_open=_fuse_open, ripen=_ripen, current=_current, blast=_blast, glow=_glow)

# ================================================================ e2_01 / e2_02 the human power bank
shot(n='A1', set='soi', preset='day', t0=0.0, t1=3.6, props=[P_table(20)], fx=['phone_zap'],
     keys=[(0.0, (0.7, 9.4, 2.3), (-2.6, 5.6, 0.9), 20), (3.6, (0.4, 8.9, 2.1), (-2.7, 5.6, 0.95), 22, 's')],
     actors=[WELD_SIT('unimpressed'), ('n1', 'nb_man', (-2.75, 6.95, 0.0), T((0, 'nb_man_phone', {'expr': 'excited', 'yaw': -0.5})), True),
             ('hong', 'hong', HONG_T, T((0, 'hong_count_money', {'expr': 'laughing'})), False)] + queue(5, skip=1))
shot(n='A2', set='soi', preset='day', t0=3.6, t1=7.05, dof=1.8, props=[P_table(20)], fx=['phone_zap'],
     keys=[(3.6, (-2.0, 5.35, 1.15), (-3.35, 6.8, 1.0), 28), (7.05, (-2.15, 5.65, 1.1), (-3.4, 6.8, 1.0), 33, 's')],
     actors=[WELD_SIT('unimpressed', zap=['body']), ('n1', 'nb_woman', (-2.75, 6.95, 0.0), T((0, 'nb_woman_phone', {'expr': 'excited', 'arm_r': 'down', 'yaw': -0.5})), False)])
shot(n='A3', set='soi', preset='day', t0=7.05, t1=11.67, dof=1.8, props=[P_table(20)], fx=[],
     keys=[(7.05, (-1.2, 3.4, 1.35), (-3.3, 4.6, 1.35), 28), (11.67, (-1.4, 3.6, 1.32), (-3.3, 4.6, 1.38), 34, 's')],
     actors=[('hong', 'hong', HONG_T, T((0, 'hong_count_money', {'expr': 'laughing', 'yaw': 0.4}), (9.4, 'hong_count_money', {'expr': 'smug', 'yaw': 0.4, 'pitch': 0.9})), False),
             WELD_SIT('sad', pitch=0.8)])
# ================================================================ e2_03 .. e2_05 Kim at the door
shot(n='B1', set='room', t0=11.67, t1=16.42, fx=['door'],
     keys=[(11.67, (0.55, 2.6, 1.55), (0.05, 4.45, 1.5), 24), (16.42, (0.45, 3.0, 1.58), (0.05, 4.45, 1.6), 29, 's')],
     actors=[('kim', 'kim', DWY, T((0, 'kim_explain', {'expr': 'neutral', 'arm_r': 'down', 'mouth': None}), (13.9, 'kim_explain', {'expr': 'smug', 'mouth': None, 'arm_r': 'down'})), False)])
shot(n='B2', set='room', t0=16.42, t1=22.7, fx=['door'],
     keys=[(16.42, (1.45, 1.75, 1.6), (-0.06, 4.6, 1.18), 23), (22.7, (1.3, 2.15, 1.55), (-0.05, 4.6, 1.25), 27, 's')],
     actors=[('you', 'welder', DIN, T((0, 'welder_idle_bolt', {'yaw': -0.6, 'expr': 'stunned'}), (19.4, 'welder_idle_bolt', {'yaw': -0.6, 'expr': 'shocked', 'fx': ['sweat']})), False),
             ('kim', 'kim', DWY, T((0, 'kim_point', {'expr': 'determined', 'arm_l': 'behind'}), (19.4, 'kim_explain', {'expr': 'smug', 'zap': ['hair']})), False)])
shot(n='B3', set='room', t0=22.7, t1=25.73, dof=1.6, fx=['door'],
     keys=[(22.7, (0.3, 3.25, 1.62), (0.05, 4.45, 1.66), 33), (25.73, (0.28, 3.4, 1.63), (0.05, 4.45, 1.68), 38, 's')],
     actors=[('kim', 'kim', DWY, T((0, 'kim_explain', {'expr': 'talking'})), False)])
# ================================================================ e2_06 .. e2_10 the three rules behind the fuse-box door
shot(n='C1', set='soi', preset='evening', t0=25.73, t1=29.82, props=[P_fuse(0.0)], fx=['fuse_open'], door_t=(26.4, 27.5, 0.0, 165.0),
     keys=[(25.73, (0.4, 10.2, 1.5), (-2.4, 12.0, 1.25), 22), (29.82, (0.0, 10.6, 1.45), (-2.5, 12.0, 1.25), 26, 's')],
     actors=[('kim', 'kim', (-2.0, 12.95, 0.0), T((0, 'kim_point', {'expr': 'determined', 'yaw': -0.6})), True),
             ('you', 'welder', (-0.6, 12.6, 0.0), T((0, 'welder_idle_bolt', {'expr': 'neutral', 'yaw': -0.4}), (27.6, 'welder_idle_bolt', {'expr': 'stunned', 'yaw': -0.4})), True)])
shot(n='C2', set='soi', preset='evening', t0=29.82, t1=34.66, props=[P_fuse(165.0)], fx=[],
     keys=[(29.82, (-1.62, 11.92, 1.48), (-2.55, 11.7, 1.42), 30), (34.66, (-1.78, 11.88, 1.45), (-2.55, 11.7, 1.48), 36, 's')], actors=[])
shot(n='C3', set='soi', preset='evening', t0=34.66, t1=40.35, dof=1.8, props=[P_fuse(165.0)], fx=[],
     keys=[(34.66, (-0.55, 10.55, 1.45), (-2.15, 11.6, 1.5), 28), (40.35, (-0.7, 10.75, 1.45), (-2.15, 11.6, 1.52), 33, 's')],
     actors=[('kim', 'kim', (-2.1, 11.55, 0.0), T((0, 'kim_explain', {'expr': 'talking', 'yaw': 0.4}), (37.4, 'kim_shout_cupped', {'expr': 'shouting'})), False)])
shot(n='C4', set='soi', preset='evening', t0=40.35, t1=44.87, props=[P_fuse(165.0)], fx=[],
     keys=[(40.35, (-1.68, 11.9, 1.22), (-2.55, 11.7, 1.16), 34), (44.87, (-1.8, 11.86, 1.2), (-2.55, 11.7, 1.14), 40, 's')], actors=[])
shot(n='C5', set='roof', flash=0, split='lights', lights_fn=lambda t: t < 46.7, t0=44.87, t1=48.16, actors=[], fx=['rain_fast'],
     keys=[(44.87, (-62, -128, 72), (0, 60, 6), 22), (48.16, (-50, -108, 60), (2, 32, 8), 24, 's')])
# ================================================================ e2_11 .. e2_13 the queue, the table, the price
shot(n='D1', set='soi', preset='day', t0=48.16, t1=51.3, props=[P_table(20)], fx=['phone_zap'],
     keys=[(48.16, (0.9, 0.6, 4.3), (-2.4, 6.6, 0.8), 20), (51.3, (0.6, 1.4, 3.9), (-2.6, 6.6, 0.8), 21, 's')],
     actors=[WELD_SIT('neutral'), ('n1', 'nb_man', (-2.75, 6.95, 0.0), T((0, 'nb_man_phone', {'expr': 'excited', 'yaw': -0.5})), True),
             ('hong', 'hong', HONG_T, T((0, 'hong_count_money', {'expr': 'laughing'})), False)] + queue(9, skip=1))
shot(n='D2', set='soi', preset='day', t0=51.3, t1=54.57, dof=1.6, props=[P_table(20)], fx=['phone_zap'], zap_p=ZAP_P,
     keys=[(51.3, (-2.35, 6.2, 1.08), (-3.25, 6.8, 1.0), 34), (54.57, (-2.45, 6.3, 1.06), (-3.25, 6.8, 1.0), 40, 's')],
     actors=[WELD_SIT('unimpressed', zap=['body']), ('n1', 'nb_woman', (-2.75, 6.95, 0.0), T((0, 'nb_woman_phone', {'expr': 'shocked', 'yaw': -0.5}), (53.0, 'nb_woman_phone', {'expr': 'excited', 'yaw': -0.5})), False)])
shot(n='D3', set='soi', preset='day', t0=54.57, t1=58.73, props=[P_table(20)], fx=[],
     keys=[(54.57, (-0.9, 3.2, 1.45), (-2.9, 4.6, 1.15), 25), (58.73, (-1.1, 3.4, 1.4), (-2.9, 4.6, 1.15), 30, 's')],
     actors=[('hong', 'hong', HONG_T, T((0, 'hong_count_money', {'expr': 'laughing', 'yaw': 0.4})), False),
             ('n2', 'nb_man', (-1.95, 5.35, 0.0), T((0, 'nb_man_phone', {'expr': 'happy', 'yaw': -0.4})), True, {'static': True})])
shot(n='D4', set='soi', preset='day', t0=58.73, t1=61.9, props=[P_table(30)], fx=[],
     keys=[(58.73, (-0.2, -2.6, 1.7), (-1.7, 12.0, 1.2), 22), (61.9, (-0.3, -1.7, 1.65), (-1.8, 12.0, 1.2), 23, 's')],
     actors=[WELD_SIT('sad'), ('n1', 'nb_man', (-2.75, 6.95, 0.0), T((0, 'nb_man_phone', {'expr': 'excited', 'yaw': -0.5})), True, {'static': True}),
             ('hong', 'hong', HONG_T, T((0, 'hong_count_money', {'expr': 'laughing'})), False, {'static': True})] + queue(11, skip=1, dy=-0.8))
shot(n='D5', set='soi', preset='day', t0=61.9, t1=63.4, props=[P_table(30)], fx=[],
     keys=[(61.9, (-1.85, 5.0, 1.16), (-2.85, 5.0, 1.0), 30), (63.4, (-1.95, 5.0, 1.14), (-2.85, 5.0, 1.0), 36, 's')], actors=[])
shot(n='D6', set='soi', preset='day', t0=63.4, t1=65.16, dof=1.6, props=[P_table(30)], fx=[],
     keys=[(63.4, (-2.55, 6.15, 1.12), (-3.6, 6.65, 1.1), 36), (65.16, (-2.6, 6.2, 1.1), (-3.6, 6.65, 1.1), 40, 's')],
     actors=[WELD_SIT('sad', pitch=0.9)])
# ================================================================ e2_14 .. e2_15 "your power is MY property"
shot(n='E1', set='soi', preset='day', t0=65.16, t1=69.46, props=[P_table(30)], fx=[],
     keys=[(65.16, (-0.5, 3.2, 1.45), (-2.85, 5.3, 1.35), 24), (69.46, (-0.7, 3.4, 1.42), (-2.85, 5.3, 1.35), 28, 's')],
     actors=[('you', 'welder', WSTAND, T((0, 'welder_idle_bolt', {'expr': 'worried', 'yaw': 0.6, 'arm_r': 'shrug', 'arm_l': 'shrug'})), True),
             ('hong', 'hong', HONG_T, T((0, 'hong_crossed_smug', {'expr': 'unimpressed'}), (67.6, 'hong_angry_shout', {})), False)])
shot(n='E2', set='soi', preset='day', dof=1.6, t0=69.46, t1=74.6, props=[P_table(30)], fx=[],
     keys=[(69.46, (-1.4, 3.1, 0.75), (-3.3, 4.15, 1.62), 22), (72.0, (-1.8, 3.3, 0.78), (-3.3, 4.15, 1.66), 28, 's'), (74.6, (-2.05, 3.45, 0.8), (-3.3, 4.15, 1.7), 33, 'o')],
     actors=[('hong', 'hong', HONG_T, T((0, 'hong_angry_shout', {}), (72.2, 'hong_angry_shout', {'arm_r': 'up_point'})), False)])
# ================================================================ e2_16 .. e2_17 hug the banana tree: the whole bunch ripens
shot(n='E3', set='soi', preset='day', dof=1.6, t0=74.6, t1=77.0, props=[P_table(30)], fx=['shake'],
     keys=[(74.6, (-1.35, 5.55, 1.5), (-2.4, 6.3, 1.5), 30), (77.0, (-1.5, 5.7, 1.5), (-2.4, 6.3, 1.55), 36, 's')],
     actors=[('you', 'welder', WSTAND, T((0, 'welder_angry', {'zap': ['hair', 'body']})), True)])
shot(n='E4', set='soi', preset='day', t0=77.0, t1=80.31, fx=[],
     keys=[(77.0, (-0.6, 1.5, 1.6), (-3.5, 4.8, 1.2), 20), (78.6, (-0.8, 1.2, 1.55), (-5.2, 3.4, 1.3), 21, 's'), (80.31, (-1.0, 1.0, 1.5), (-5.8, 3.0, 1.4), 22, 's')],
     actors=[('you', 'welder', [(77.0, (-2.4, 6.3, 0.0)), (78.4, (-4.6, 3.55, 0.0)), (79.0, (-5.6, 3.5, 0.0)), (79.4, HUG)],
              T((0, 'welder_angry', {'walk': True, 'zap': ['hair']}), (79.4, 'welder_hug_tree', {'expr': 'furious', 'zap': ['hair']})), False)])
shot(n='E5', set='soi', preset='day', t0=80.31, t1=85.44, props=[], fx=['ripen'], ripe_t=(82.7, 83.05),
     keys=[(80.31, (-5.35, 3.75, 0.55), (-6.35, 2.75, 2.2), 17), (85.44, (-5.3, 3.65, 0.6), (-6.3, 2.7, 2.5), 19, 's')],
     actors=[('you', 'welder', HUG, T((0, 'welder_hug_tree', {'expr': 'furious', 'zap': ['hair']}), (82.7, 'welder_hug_tree', {'expr': 'shocked'}), (83.6, 'welder_hug_tree', {'expr': 'happy'})), False)])
# ================================================================ e2_18 .. e2_23 the storm, the jumper cable, the transformer
shot(n='F1', set='soi', preset='evening', t0=85.44, t1=89.3, fx=['rain'],
     keys=[(85.44, (1.0, -3.0, 1.8), (-1.4, 14.0, 3.6), 20), (89.3, (0.8, -2.0, 1.75), (-1.4, 14.0, 3.4), 21, 's')], actors=[])
shot(n='F2', set='soi', preset='evening', t0=89.3, t1=95.63, props=[P_cable], fx=['rain'], rain_n=400,
     keys=[(89.3, (-1.7, 8.0, 1.25), (-3.7, 6.7, 0.75), 24), (95.63, (-1.9, 7.6, 1.15), (-3.7, 6.7, 0.7), 28, 's')],
     actors=[WELD_SIT('sleepy' if False else 'neutral', pitch=0.7), ('hong', 'hong', (-4.15, 7.35, 0.0), T((0, 'hong_count_money', {'expr': 'smug', 'yaw': 0.6, 'pitch': 0.8})), True)])
shot(n='F3', set='soi', preset='evening', t0=95.63, t1=98.58, props=[P_cable], fx=['rain'], rain_n=400,
     keys=[(95.63, (-2.85, 7.7, 0.75), (-3.55, 6.7, 0.4), 24), (97.0, (-2.3, 8.8, 0.9), (-3.3, 10.6, 0.2), 22, 's'), (98.58, (-1.4, 9.9, 1.5), (-2.75, 12.2, 4.6), 20, 's')],
     actors=[WELD_SIT('neutral', pitch=0.7)])
shot(n='F4', set='soi', preset='evening', t0=98.58, t1=104.77, props=[P_cable], fx=['rain', 'glow'], rain_n=400, plight=True,
     glow=(100.6, 0.55), glow_at=WS,
     keys=[(98.58, (-2.2, 5.6, 1.12), (-3.6, 6.6, 0.95), 28), (100.6, (-2.4, 5.8, 1.1), (-3.6, 6.6, 0.95), 33, 's'), (104.77, (-2.5, 5.9, 1.1), (-3.6, 6.6, 0.95), 35, 's')],
     actors=[('you', 'welder', WS, T((0, 'welder_sit_stool', {'stool': True, 'expr': 'neutral', 'yaw': 0.7, 'pitch': 0.6}),
                                   (100.6, 'welder_sit_stool', {'stool': True, 'expr': 'scream', 'yaw': 0.7, 'zap': ['hair', 'body'], 'squash': (1.04, 0.96)})), False)])
shot(n='F5', set='soi', preset='evening', t0=104.77, t1=107.4, props=[P_cable], fx=['rain', 'current'], rain_n=400, plight=True, cur=(104.77, 107.4, 0.02, 0.62),
     keys=[(104.77, (-2.6, 8.4, 0.45), (-3.5, 7.2, 0.2), 20), (107.4, (-2.4, 9.6, 0.55), (-3.2, 11.3, 0.3), 20, 's')],
     actors=[WELD_SIT('scream', zap=['hair', 'body'])])
shot(n='F6', set='soi', preset='evening', t0=107.4, t1=110.48, props=[P_cable], fx=['rain', 'current'], rain_n=400, plight=True, cur=(107.4, 110.2, 0.62, 1.0),
     keys=[(107.4, (-0.9, 9.9, 1.2), (-2.8, 12.2, 1.4), 20), (110.48, (-0.6, 9.6, 1.3), (-2.6, 12.25, 7.0), 19, 's')], actors=[])
shot(n='F7', set='soi', preset='evening', split='lights', lights_fn=lambda t: t < 110.95, t0=110.48, t1=113.6, props=[P_cable], fx=['rain', 'blast', 'shake'], rain_n=400,
     plight=True, blast_t=110.75, dark_gain=0.6,
     keys=[(110.48, (0.6, 8.0, 1.2), (-2.5, 12.25, 6.4), 18), (113.6, (0.7, 7.6, 1.1), (-2.5, 12.25, 6.0), 17, 's')], actors=[])
shot(n='F8', set='roof', flash=0, split='lights', lights_fn=lambda t: t < 114.6, t0=113.6, t1=116.0, actors=[], fx=['rain_fast'],
     keys=[(113.6, (-58, -120, 66), (0, 50, 6), 22), (116.0, (-50, -106, 58), (2, 30, 8), 23, 's')])
BABY = [os.path.join(HERE, 'props_tex', 'baby%d.png' % k) for k in range(3)]
def P_babies_dark(A, SET, lv):
    for i in range(3): SET.set_incubator(i, 0.0)
    return {}
shot(n='F9', set='nurs', preset='dark', t0=116.0, t1=DUR, props=[P_babies_dark], fx=[], gain=0.8,
     keys=[(116.0, (0.0, 1.0, 1.55), (0.0, 4.2, 1.0), 22), (DUR, (0.0, 1.6, 1.5), (0.0, 4.2, 1.0), 26, 's')],
     actors=[('b%d' % i, 'png:' + BABY[i], (x - 0.05, 4.2, 0.86), T((0, '', {})), False) for i, x in enumerate((-1.75, 0.0, 1.75))])
