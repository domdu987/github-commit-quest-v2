# EP.4 (ตอนจบ) — วิธีปิดสวิตช์เทพเจ้าสายฟ้า กับค่าแรงที่เพิ่มขึ้นหนึ่งบาท (e4_01..e4_17, 80.1 s), exec'd by lt_epx.py (LT_EP=4). 16:9 cameras.
DUR = 80.1
INC = [(-1.75, 4.2), (0.0, 4.2), (1.75, 4.2)]
BABY = [os.path.join(HERE, 'props_tex', 'baby%d.png' % k) for k in range(3)]
def babies(gain=0.95): return [('b%d' % i, 'png:' + BABY[i], (x - 0.05, y, 0.86), T((0, '', {})), False, {'gain': gain}) for i, (x, y) in enumerate(INC)]
CTRL_HERO = (-1.15, 2.5, 0.0); PUDDLE_SIT = (0.15, 2.35, -0.42)
FUSE = ((-2.83, 12.25, 0.95), math.pi / 2)
WS = (-3.6, 6.6, 0.0); HONG_T = (-3.3, 5.0, 0.0)

def P_inc(*levels):
    def f(A, SET, lv):
        for i, l in enumerate(levels): SET.set_incubator(i, l)
        return {}
    return f
def P_fuse(door=165.0, plate=0.0):
    def f(A, SET, lv):
        import lt_props as LP; return dict(fb=LP.fuse_box(FUSE[0], FUSE[1], door_deg=door, plate_deg=plate))
    return f
def P_poster(A, SET, lv):
    import lt_props as LP; LP.poster((1.7, 14.84, 1.2), (1.3, 0, 0), (0, 0, 0.975), 'drawing', gain=1.6); return {}
def _glow(mb, g, t, A, SET, sh, X):
    import lt_props as LP; pts = sh['glow']; lv = pts[0][1]
    for (a, va), (b, vb) in zip(pts[:-1], pts[1:]):
        if a <= t < b: lv = va + (vb - va) * (t - a) / (b - a)
    if t >= pts[-1][0]: lv = pts[-1][1]
    if lv <= 0.01: return False
    feet = pos_at(sh['actors'][0][2], t); LP.glow_body(mb, feet, t, lv, height=1.6, g=g); return True
def _plate(mb, g, t, A, SET, sh, X):
    import lt_props as LP; a0, a1 = sh['plate_t']; u = max(0.0, min(1.0, (t - a0) / (a1 - a0))); LP.set_fuse(X['P']['fb'], plate_deg=100.0 * ease(u)); return False
def _splash(mb, g, t, A, SET, sh, X):
    u = t - sh['splash_t']
    if not 0 <= u < 0.9: return False
    Vector = X['Vector']; c = Vector(PUDDLE_SIT[:2] + (0.02,)); m = X['S'].mat_emit('FX_drop', '#bfe0ff', strength=2.0)
    for k in range(40):
        rs = random.Random(300 + k); v = Vector((rs.uniform(-1, 1), rs.uniform(-1, 1), rs.uniform(0.6, 1.6))).normalized() * rs.uniform(1.5, 3.2)
        p = c + Vector((rs.uniform(-0.35, 0.35), rs.uniform(-0.25, 0.25), 0)) + v * u + Vector((0, 0, -4.9 * u * u))
        if p.z > 0: mb.sphere(tuple(p), 0.018, m, seg=6, rings=4)
    return True
FX_HOOKS.update(glow=_glow, plate=_plate, splash=_splash)

# ---------------- e4_01 .. e4_02 about to float through the ceiling
shot(n='H1', set='ctrl', preset='lit', t0=0.0, t1=5.9, fx=['glow'], glow=[(0.0, 1.0), (5.9, 1.0)], plight=True,
     keys=[(0.0, (0.9, 0.45, 0.5), (-1.1, 2.6, 1.9), 18), (5.9, (0.7, 0.75, 0.55), (-1.1, 2.6, 2.1), 19, 's')],
     actors=[('you', 'welder', [(0.0, (CTRL_HERO[0], CTRL_HERO[1], 0.85)), (5.9, (CTRL_HERO[0], CTRL_HERO[1], 1.05))], T((0, 'welder_shocked', {'expr': 'scream'})), True, {'gain': 1.30})])
shot(n='H2', set='ctrl', preset='lit', t0=5.9, t1=11.53, dof=1.6, fx=['glow'], glow=[(5.9, 1.0), (11.53, 1.0)],
     keys=[(5.9, (-0.15, 1.65, 2.35), (-1.15, 2.5, 2.5), 32), (11.53, (-0.25, 1.75, 2.4), (-1.15, 2.5, 2.55), 36, 's')],
     actors=[('you', 'welder', [(5.9, (CTRL_HERO[0], CTRL_HERO[1], 1.05)), (11.53, (CTRL_HERO[0], CTRL_HERO[1], 1.15))], T((0, 'welder_shocked', {'expr': 'worried'})), True, {'gain': 1.30})])
# ---------------- e4_03 .. e4_05 Kim at the door: "think of your wage!"
shot(n='H3', set='ctrl', preset='lit', t0=11.53, t1=16.09, fx=['glow', 'rain'], glow=[(11.53, 1.0), (16.09, 1.0)], rain_n=250,
     keys=[(11.53, (-1.4, 4.6, 1.6), (-0.4, -0.4, 1.7), 20), (16.09, (-1.4, 4.4, 1.6), (-0.5, -0.4, 1.6), 22, 's')],
     actors=[('you', 'welder', (CTRL_HERO[0], CTRL_HERO[1], 1.15), T((0, 'welder_shocked', {'expr': 'stunned'})), False, {'gain': 1.30, 'static': True}),
             ('kim', 'kim', [(11.53, (-0.5, -2.6, 0.0)), (14.2, (-0.5, -0.45, 0.0))], T((0, 'kim_point', {'expr': 'determined', 'walk': True}), (14.2, 'kim_point', {'expr': 'shocked'})), False)])
shot(n='H4', set='ctrl', preset='lit', t0=16.09, t1=18.62, fx=['rain'], rain_n=250,
     keys=[(16.09, (-0.35, 1.6, 0.6), (-0.5, -0.45, 1.6), 22), (18.62, (-0.35, 1.4, 0.62), (-0.5, -0.45, 1.65), 26, 's')],
     actors=[('kim', 'kim', (-0.5, -0.45, 0.0), T((0, 'kim_shout_cupped', {})), False)])
shot(n='H5', set='ctrl', preset='lit', t0=18.62, t1=21.46, dof=1.6, fx=['rain'], rain_n=250,
     keys=[(18.62, (-0.4, 0.55, 1.6), (-0.5, -0.45, 1.66), 30), (21.46, (-0.42, 0.45, 1.6), (-0.5, -0.45, 1.68), 36, 's')],
     actors=[('kim', 'kim', (-0.5, -0.45, 0.0), T((0, 'kim_shout_cupped', {'expr': 'furious' if False else 'shouting'})), False)])
# ---------------- e4_06 .. e4_08 450 baht: the power is gone; down into the puddle
shot(n='H6', set='ctrl', preset='lit', t0=21.46, t1=26.94, dof=1.6, fx=['glow'], glow=[(21.46, 1.0), (26.94, 0.9)],
     keys=[(21.46, (-0.2, 1.7, 2.4), (-1.15, 2.5, 2.55), 34), (26.94, (-0.3, 1.8, 2.42), (-1.15, 2.5, 2.57), 40, 's')],
     actors=[('you', 'welder', (CTRL_HERO[0], CTRL_HERO[1], 1.15), T((0, 'welder_shocked', {'expr': 'stunned'}), (22.4, 'welder_sad', {'expr': 'sad', 'blink': 2, 'hair_state': 'bolt'})), True, {'gain': 1.30})])
shot(n='H7', set='ctrl', preset='lit', t0=26.94, t1=29.4, fx=['glow'], glow=[(26.94, 0.9), (27.9, 0.9), (28.15, 0.0)],
     keys=[(26.94, (0.6, 0.6, 1.0), (-1.15, 2.5, 1.95), 22), (29.4, (0.55, 0.7, 1.0), (-1.15, 2.5, 1.9), 24, 's')],
     actors=[('you', 'welder', (CTRL_HERO[0], CTRL_HERO[1], 1.15), T((0, 'welder_sad', {'expr': 'sad', 'blink': 2, 'hair_state': 'bolt'}), (28.0, 'welder_idle_bolt', {'expr': 'stunned'})), True, {'gain': 1.12})])
shot(n='H8', set='ctrl', preset='lit', t0=29.4, t1=31.81, fx=[],
     keys=[(29.4, (1.5, 0.3, 1.7), (-0.9, 3.4, 1.3), 18), (31.81, (1.4, 0.5, 1.65), (-0.9, 3.4, 1.3), 19, 's')],
     actors=[('you', 'welder', (CTRL_HERO[0], CTRL_HERO[1], 1.15), T((0, 'welder_idle_bolt', {'expr': 'stunned'})), True)])
shot(n='H9', set='ctrl', preset='lit', t0=31.81, t1=35.4, fx=['splash', 'shake'], splash_t=32.35,
     keys=[(31.81, (1.3, 0.6, 1.2), (-0.3, 2.5, 0.9), 22), (35.4, (1.2, 0.8, 1.1), (-0.1, 2.45, 0.7), 26, 's')],
     actors=[('you', 'welder', [(31.81, (CTRL_HERO[0], CTRL_HERO[1], 1.15)), (32.0, (CTRL_HERO[0], CTRL_HERO[1], 1.12)), (32.35, PUDDLE_SIT)],
              T((0, 'welder_shocked', {'expr': 'shocked'}), (32.35, 'welder_sit_stool', {'stool': False, 'expr': 'stunned', 'yaw': 0.3, 'fx': ['sweat'], 'squash': (1.06, 0.93)}),
                (32.7, 'welder_sit_stool', {'stool': False, 'expr': 'unimpressed', 'yaw': 0.3})), True)])
# ---------------- e4_09 the district is back; three warm incubators
shot(n='H10', set='nurs', preset='lit', t0=35.4, t1=38.5, props=[P_inc(1, 1, 1)], fx=[],
     keys=[(35.4, (0.0, 0.8, 1.6), (0.0, 4.2, 1.05), 20), (38.5, (0.0, 1.3, 1.55), (0.0, 4.2, 1.05), 22, 's')],
     actors=babies() + [('nurse', 'nurse', (2.85, 4.9, 0.0), T((0, 'nurse_idle', {'expr': 'happy', 'yaw': -0.3})), True)])
shot(n='H11', set='nurs', preset='lit', t0=38.5, t1=41.58, dof=1.6, props=[P_inc(1, 1, 1)], fx=[],
     keys=[(38.5, (-0.9, 3.15, 1.35), (0.0, 4.2, 1.0), 28), (41.58, (0.9, 3.15, 1.35), (0.0, 4.2, 1.0), 28, 's')], actors=babies())
# ---------------- e4_10 .. e4_12 the innermost plate: the last rule
shot(n='H12', set='soi', preset='evening', t0=41.58, t1=47.63, props=[P_fuse(165.0, 0.0)], fx=['plate'], plate_t=(44.6, 45.6),
     keys=[(41.58, (0.4, 10.2, 1.5), (-2.4, 12.0, 1.25), 22), (47.63, (-0.2, 10.8, 1.45), (-2.6, 12.1, 1.3), 27, 's')],
     actors=[('kim', 'kim', (-2.0, 12.95, 0.0), T((0, 'kim_point', {'expr': 'determined', 'yaw': -0.6})), True),
             ('you', 'welder', (-0.6, 12.6, 0.0), T((0, 'welder_idle_bolt', {'expr': 'neutral', 'yaw': -0.4})), True)])
shot(n='H13', set='soi', preset='evening', t0=47.63, t1=50.2, props=[P_fuse(165.0, 100.0)], fx=[],
     keys=[(47.63, (-1.95, 12.3, 1.52), (-2.98, 12.25, 1.42), 30), (50.2, (-2.05, 12.28, 1.5), (-2.98, 12.25, 1.42), 36, 's')], actors=[])
shot(n='H14', set='soi', preset='evening', t0=50.2, t1=53.6, props=[P_fuse(165.0, 100.0)], fx=[],
     keys=[(50.2, (-2.15, 12.27, 1.46), (-2.98, 12.25, 1.42), 36), (53.6, (-2.25, 12.26, 1.44), (-2.98, 12.25, 1.42), 44, 's')], actors=[])
# ---------------- e4_13 the morning after: the nursery's hero
shot(n='H15', set='nurs', preset='morning', t0=53.6, t1=57.3, props=[P_inc(1, 1, 1), P_poster], fx=[],
     keys=[(53.6, (-0.4, 0.4, 1.6), (1.4, 12.0, 1.3), 21), (57.3, (-0.2, 1.6, 1.6), (1.6, 12.5, 1.4), 24, 's')],
     actors=babies() + [('nurse', 'nurse', (1.2, 12.9, 0.0), T((0, 'nurse_idle', {'expr': 'happy', 'yaw': 0.4})), False)])
shot(n='H16', set='nurs', preset='morning', t0=57.3, t1=60.89, props=[P_inc(1, 1, 1), P_poster], fx=[],
     keys=[(57.3, (2.35, 12.7, 1.66), (2.35, 14.84, 1.68), 30), (60.89, (2.35, 12.95, 1.66), (2.35, 14.84, 1.68), 36, 's')], actors=[])
# ---------------- e4_14 .. e4_15 Hong, moved to tears: +1 baht
def P_table30(A, SET, lv):
    import lt_props as LP; return dict(ct=LP.charge_table((-2.55, 5.0, 0.0), math.pi / 2, price=30))
shot(n='H17', set='soi', preset='day', t0=60.89, t1=66.36, props=[P_table30], fx=[],
     keys=[(60.89, (-0.6, 6.0, 1.45), (-2.85, 5.6, 1.35), 24), (66.36, (-0.8, 5.9, 1.4), (-2.85, 5.6, 1.4), 29, 's')],
     actors=[('you', 'welder', (-2.4, 6.3, 0.0), T((0, 'welder_idle_bolt', {'expr': 'happy', 'yaw': 0.6})), True),
             ('hong', 'hong', HONG_T, T((0, 'hong_idle_fan', {'expr': 'sad'}), (63.6, 'hong_shout_up', {'expr': 'happy'})), False)])
shot(n='H18', set='soi', preset='day', t0=66.36, t1=69.4, dof=1.6, props=[P_table30], fx=[],
     keys=[(66.36, (-1.15, 4.3, 1.3), (-3.3, 5.1, 1.35), 30), (69.4, (-1.35, 4.5, 1.28), (-3.3, 5.1, 1.35), 37, 's')],
     actors=[('hong', 'hong', HONG_T, T((0, 'hong_calculator', {'expr': 'happy'})), False)])
# ---------------- e4_16 .. e4_17 the same welder, the same motorbike: the soi never goes dark again
shot(n='H19', set='soi', preset='day', t0=69.4, t1=73.33, fx=[],
     keys=[(69.4, (-0.5, 12.6, 1.35), (-3.3, 15.2, 1.0), 24), (73.33, (-0.7, 12.9, 1.3), (-3.3, 15.2, 1.0), 28, 's')],
     actors=[('you', 'welder', (-2.55, 14.6, 0.0), T((0, 'welder_proud', {})), True)])
shot(n='H20', set='soi', preset='evening', t0=73.33, t1=DUR, fx=[],
     keys=[(73.33, (0.6, -2.2, 1.6), (-1.0, 12.0, 2.0), 20), (DUR, (0.8, -5.5, 6.5), (-1.0, 14.0, 3.0), 20, 's')],
     actors=[('you', 'welder', (-0.5, 4.0, 0.0), T((0, 'welder_idle_bolt', {'expr': 'happy', 'yaw': 0.1})), False),
             ('kim', 'kim', (0.5, 6.5, 0.0), T((0, 'kim_explain', {'expr': 'smug', 'mouth': None})), True, {'static': True})])
