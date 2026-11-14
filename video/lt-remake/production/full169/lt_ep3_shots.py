# EP.3 — ทารกสามคนในตู้อบ กับกฎข้อที่สามที่ถูกฝ่าฝืน (e3_01..e3_14, 63.79 s), exec'd by lt_epx.py (LT_EP=3). 16:9 cameras.
DUR = 63.79
INC = [(-1.75, 4.2), (0.0, 4.2), (1.75, 4.2)]
BABY = [os.path.join(HERE, 'props_tex', 'baby%d.png' % k) for k in range(3)]
def babies(gain=0.85): return [('b%d' % i, 'png:' + BABY[i], (x - 0.05, y, 0.86), T((0, '', {})), False, {'gain': gain}) for i, (x, y) in enumerate(INC)]
CTRL_HERO = (-1.15, 2.5, 0.0); CABLE_END = (-1.7, 2.55, 1.15)
SOI_RUN = [(-0.6, 11.5, 0.0), (-0.4, 2.0, 0.0)]

def P_inc(*levels):
    def f(A, SET, lv):
        for i, l in enumerate(levels): SET.set_incubator(i, l)
        return {}
    return f
def _inc_on(mb, g, t, A, SET, sh, X):
    for i, ton in sh['inc_on']: SET.set_incubator(i, 1.0 if t >= ton else 0.0)
    return False
def _glow(mb, g, t, A, SET, sh, X):
    import lt_props as LP; pts = sh['glow']; lv = pts[0][1]
    for (a, va), (b, vb) in zip(pts[:-1], pts[1:]):
        if a <= t < b: lv = va + (vb - va) * (t - a) / (b - a)
    if t >= pts[-1][0]: lv = pts[-1][1]
    if lv <= 0: return False
    feet = pos_at(sh['actors'][0][2], t); LP.glow_body(mb, feet, t, lv, height=1.6, g=g); return True
def _cable_arc(mb, g, t, A, SET, sh, X):
    if t < sh.get('arc_t', 0): return False
    Vector = X['Vector']; p = Vector(CABLE_END); X['sparks_at'](mb, p, g, n=18, big=1.2)
    ra = random.Random(g)
    for k in range(5):
        a = p; b = p + Vector((ra.uniform(0.1, 0.7), ra.uniform(-0.4, 0.4), ra.uniform(-0.3, 0.5))); pts = [a]
        for q in range(1, 6): pts.append(a.lerp(b, q / 6) + Vector((ra.uniform(-0.05, 0.05), ra.uniform(-0.05, 0.05), ra.uniform(-0.05, 0.05))))
        pts.append(b)
        for p0, p1 in zip(pts[:-1], pts[1:]): mb.frustum(tuple(p0), tuple(p1), 0.007, 0.007, X['boltc'], seg=4); mb.frustum(tuple(p0), tuple(p1), 0.022, 0.022, X['bolth'], seg=5)
    pl = X['plight']
    if pl is not None: pl.location = p + Vector((0.4, 0, 0.3)); pl.data.color = (0.7, 0.85, 1.0); pl.data.energy = 300.0 + 300 * ra.random()
    return True
FX_HOOKS.update(inc_on=_inc_on, glow=_glow, cable_arc=_cable_arc)

FLOAT = lambda t0, t1, z1, z0=0.0: [(t0, (CTRL_HERO[0], CTRL_HERO[1], z0)), (t1, (CTRL_HERO[0], CTRL_HERO[1], z1))]
# ---------------- e3_01 cold incubators
shot(n='G1', set='nurs', preset='dark', t0=0.0, t1=3.3, props=[P_inc(0, 0, 0)], fx=[],
     keys=[(0.0, (0.0, 0.6, 1.6), (0.0, 4.2, 1.0), 21), (3.3, (0.0, 1.3, 1.5), (0.0, 4.2, 1.0), 24, 's')], actors=babies())
shot(n='G2', set='nurs', preset='dark', t0=3.3, t1=6.72, dof=1.6, props=[P_inc(0, 0, 0)], fx=[],
     keys=[(3.3, (0.95, 3.25, 1.3), (0.15, 4.2, 1.05), 30), (6.72, (0.85, 3.35, 1.28), (0.15, 4.2, 1.05), 36, 's')], actors=babies()[1:2])
# ---------------- e3_02 .. e3_04 the welder in the storm
shot(n='G3', set='soi', preset='night_blackout', t0=6.72, t1=12.93, dof=1.6, fx=['rain', 'glow'], glow=[(6.72, 0.15), (12.93, 0.3)], rain_n=600,
     keys=[(6.72, (-0.2, 4.4, 0.7), (-0.6, 6.3, 1.55), 24), (12.93, (-0.35, 4.75, 0.72), (-0.6, 6.3, 1.6), 31, 's')],
     actors=[('you', 'welder', (-0.6, 6.3, 0.0), T((0, 'welder_idle_bolt', {'expr': 'worried', 'pitch': -0.7, 'yaw': 0.1}), (9.9, 'welder_angry', {'expr': 'determined', 'fx': [], 'zap': ['hair']})), False)])
shot(n='G4', set='ctrl', preset='dark', t0=12.93, t1=15.4, fx=[],
     keys=[(12.93, (0.4, 1.0, 1.15), (2.05, 2.4, 0.85), 26), (15.4, (0.55, 1.15, 1.12), (2.05, 2.4, 0.85), 31, 's')], actors=[])
shot(n='G5', set='soi', preset='night_blackout', t0=15.4, t1=17.86, fx=['rain'], rain_n=600,
     keys=[(15.4, (0.6, 0.0, 1.6), (-0.6, 9.0, 1.4), 22), (17.86, (0.5, 0.6, 1.6), (-0.6, 9.0, 1.4), 24, 's')],
     actors=[('you', 'welder', (-0.6, 6.3, 0.0), T((0, 'welder_angry', {'expr': 'determined', 'fx': [], 'yaw': -1.0, 'zap': ['hair']})), True)])
shot(n='G6', set='soi', preset='night_blackout', t0=17.86, t1=20.79, fx=['rain'], rain_n=700,
     keys=[(17.86, (0.5, -1.5, 1.4), (-0.5, 9.0, 1.3), 22), (20.79, (0.4, -2.6, 1.3), (-0.4, 4.0, 1.3), 22, 's')],
     actors=[('you', 'welder', [(17.86, (-0.6, 9.6, 0.0)), (20.79, (-0.4, 0.4, 0.0))], T((0, 'welder_angry', {'expr': 'determined', 'fx': [], 'walk': True, 'zap': ['hair']})), False)])
# ---------------- e3_05 the nursery
shot(n='G7', set='nurs', preset='dark', t0=20.79, t1=25.66, props=[P_inc(0, 0, 0)], fx=[],
     keys=[(20.79, (-2.4, 2.5, 1.45), (-1.4, 4.3, 0.95), 24), (25.66, (1.9, 2.55, 1.45), (1.2, 4.3, 0.95), 24, 's')],
     actors=babies() + [('nurse', 'nurse', (2.9, 5.2, 0.0), T((0, 'nurse_surprise', {'yaw': -0.4})), True)])
# ---------------- e3_06 .. e3_07 the power room: the main cable bare-handed
shot(n='G8', set='ctrl', preset='dark', t0=25.66, t1=30.29, fx=['cable_arc'], arc_t=28.4, plight=True,
     keys=[(25.66, (0.9, 0.5, 1.5), (-1.0, 3.2, 1.1), 20), (30.29, (0.6, 1.0, 1.4), (-1.3, 2.6, 1.15), 24, 's')],
     actors=[('you', 'welder', [(25.66, (-0.5, -0.3, 0.0)), (27.6, CTRL_HERO)], T((0, 'welder_angry', {'expr': 'determined', 'fx': [], 'walk': True}), (27.6, 'welder_point_spark', {'expr': 'determined'})), True)])
shot(n='G9', set='ctrl', preset='dark', t0=30.29, t1=33.03, dof=1.6, fx=['cable_arc', 'glow', 'shake'], arc_t=30.29, plight=True, glow=[(30.29, 0.35), (33.03, 0.6)],
     keys=[(30.29, (0.1, 1.9, 1.5), (-1.25, 2.55, 1.45), 32), (33.03, (-0.05, 2.0, 1.5), (-1.25, 2.55, 1.5), 38, 's')],
     actors=[('you', 'welder', CTRL_HERO, T((0, 'welder_point_spark', {'expr': 'furious', 'zap': ['hair', 'body', 'finger_r']})), True, {'gain': 1.18})])
# ---------------- e3_08 .. e3_09 one, two ... not three
shot(n='G10', set='nurs', preset='dark', t0=33.03, t1=36.25, fx=['inc_on'], inc_on=[(0, 33.5), (1, 34.9)],
     keys=[(33.03, (0.0, 1.1, 1.5), (0.0, 4.2, 1.0), 22), (36.25, (0.0, 1.5, 1.45), (0.0, 4.2, 1.0), 25, 's')], actors=babies())
shot(n='G11', set='nurs', preset='dark', t0=36.25, t1=40.65, dof=1.6, props=[P_inc(1, 1, 0)], fx=[],
     keys=[(36.25, (2.55, 3.3, 1.3), (1.75, 4.2, 1.0), 30), (40.65, (2.4, 3.4, 1.25), (1.75, 4.2, 0.98), 38, 's')], actors=babies()[2:3])
# ---------------- e3_10 rule three broken: 100 %
shot(n='G12', set='ctrl', preset='dark', t0=40.65, t1=46.37, fx=['cable_arc', 'glow', 'shake'], arc_t=40.65, plight=True, glow=[(40.65, 0.6), (46.37, 1.0)],
     keys=[(40.65, (0.8, 1.2, 1.0), (-1.2, 2.55, 1.35), 24), (46.37, (0.35, 1.75, 0.95), (-1.2, 2.55, 1.45), 32, 'q')],
     actors=[('you', 'welder', CTRL_HERO, T((0, 'welder_point_spark', {'expr': 'furious', 'zap': ['hair', 'body', 'finger_r']}), (43.5, 'welder_shocked', {'expr': 'furious'})), True, {'gain': 1.25})])
# ---------------- e3_11 .. e3_12 BANG: everything lights up
shot(n='G13', set='nurs', preset='dark', t0=46.37, t1=48.75, props=[P_inc(1, 1, 1)], fx=[], gain=1.3,
     keys=[(46.37, (0.0, 0.8, 1.55), (0.0, 4.2, 1.05), 20), (48.75, (0.0, 1.3, 1.5), (0.0, 4.2, 1.05), 22, 's')], actors=babies(1.1))
shot(n='G14', set='roof', flash=0, split='lights', lights_fn=lambda t: t < 49.55, city_k={1: 0.04, 0: 2.6}, t0=48.75, t1=51.5, actors=[], fx=['rain_fast'],
     keys=[(48.75, (-58, -120, 66), (0, 50, 6), 22), (51.5, (-62, -126, 70), (0, 52, 8), 21, 's')])
shot(n='G15', set='soi', preset='evening', split='lights', lights_fn=lambda t: t >= 52.0, t0=51.5, t1=54.25, fx=['rain'], rain_n=500, dark_gain=0.7,
     keys=[(51.5, (0.9, -3.0, 1.7), (-1.2, 14.0, 3.6), 20), (54.25, (0.8, -2.2, 1.75), (-1.2, 14.0, 3.9), 21, 's')], actors=[])
# ---------------- e3_13 .. e3_14 he glows and floats
shot(n='G16', set='ctrl', preset='dark', t0=54.25, t1=59.04, fx=['glow', 'cable_arc'], arc_t=54.25, plight=True, glow=[(54.25, 1.0), (59.04, 1.0)],
     keys=[(54.25, (0.9, 0.5, 0.45), (-1.1, 2.6, 1.4), 18), (59.04, (0.75, 0.8, 0.45), (-1.1, 2.6, 1.9), 20, 's')],
     actors=[('you', 'welder', FLOAT(54.25, 59.04, 0.55), T((0, 'welder_shocked', {'expr': 'stunned'})), True, {'gain': 1.30})])
shot(n='G17', set='ctrl', preset='dark', t0=59.04, t1=DUR, dof=1.6, fx=['glow', 'shake'], plight=True, glow=[(59.04, 1.0), (DUR, 1.0)],
     keys=[(59.04, (-0.1, 1.6, 2.1), (-1.15, 2.5, 2.25), 30), (DUR, (-0.25, 1.75, 2.25), (-1.15, 2.5, 2.45), 38, 'q')],
     actors=[('you', 'welder', FLOAT(59.04, DUR, 0.85, 0.55), T((0, 'welder_shocked', {'expr': 'scream'})), True, {'gain': 1.30})])
