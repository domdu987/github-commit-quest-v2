# exec'd by lt_ep1.py: the hospital (e1_11..e1_14) and rented-room (e1_20..e1_21) shots + their fx hooks
H = ANCH.get('hosp', {})
if H:
    SIT = tuple(H['hero_sit']['feet']) if isinstance(H['hero_sit'], dict) else (-2.57, 3.4, 0)
    STAND = tuple(H['hero_stand']); NURSE = tuple(H['nurse_mark'])
    # e1_11 he wakes up three days later: high over the bed, then he tries to comb the spikes down
    shot(n='H11a', set='hosp', t0=45.72, t1=48.3, dof=1.6,
         keys=[(45.72, (-1.6, 2.7, 2.6), (-2.6, 3.7, 1.2), 22), (48.3, (-1.75, 2.85, 2.2), (-2.6, 3.75, 1.25), 27, 's')],
         actors=[('you', 'welder', SIT, T((0, 'welder_sit_stool', {'stool': False, 'hair_state': 'bolt', 'expr': 'stunned', 'yaw': 0.3, 'fx': ['sweat']}),
                                           (47.0, 'welder_sit_stool', {'stool': False, 'hair_state': 'bolt', 'expr': 'shocked', 'yaw': 0.3})), False)], fx=[])
    shot(n='H11b', set='hosp', t0=48.3, t1=50.76, dof=1.8,
         keys=[(48.3, (-1.2, 1.0, 1.5), (-2.5, 3.2, 1.45), 26), (50.76, (-1.4, 1.4, 1.5), (-2.5, 3.2, 1.5), 32, 's')],
         actors=[('you', 'welder', STAND, T((0, 'welder_idle_bolt', {'expr': 'worried', 'arm_r': 'rub', 'arm_l': 'rub', 'head_roll': -6}),
                                             (49.6, 'welder_idle_bolt', {'expr': 'unimpressed', 'arm_r': 'down', 'arm_l': 'hip'})), False)], fx=[])
    # e1_12 he walks down the aisle toward us and every phone he passes jumps to 100%
    shot(n='H12', set='hosp', t0=50.76, t1=54.88,
         keys=[(50.76, (-0.6, -1.6, 1.0), (-0.3, 9.0, 1.1), 18), (54.88, (-0.6, -1.2, 1.0), (-0.3, 6.0, 1.0), 20, 's')],
         actors=[('you', 'welder', [(50.76, (-0.25, 9.4, 0)), (54.6, (-0.25, 1.0, 0))], T((0, 'welder_idle_bolt', {'expr': 'happy', 'walk': True})), False)], fx=['phones'])
    # e1_13 the nurse takes his pulse; her hair springs up too
    shot(n='H13', set='hosp', t0=54.88, t1=59.81, dof=1.8,
         keys=[(54.88, (1.0, 3.95, 1.45), (-1.6, 3.95, 1.3), 24), (57.4, (0.7, 3.95, 1.42), (-1.6, 3.95, 1.32), 28, 'q'), (59.81, (0.55, 3.95, 1.42), (-1.6, 3.95, 1.36), 31, 's')],
         actors=[('nurse', 'nurse', (-1.6, 4.55, 0), T((0, 'nurse_idle', {'arm_r': {'preset': 'forward', 'hand': (-0.75, 0.6)}, 'yaw': -0.4}),
                                              (57.4, 'nurse_bolt', {'arm_r': {'preset': 'forward', 'hand': (-0.75, 0.6)}, 'yaw': -0.4, 'expr': 'shocked'})), False),
                 ('you', 'welder', (-1.6, 3.3, 0), T((0, 'welder_idle_bolt', {'expr': 'neutral', 'arm_l': {'preset': 'forward', 'hand': (0.7, 0.62)}, 'yaw': 0.4}),
                                             (57.6, 'welder_idle_bolt', {'expr': 'stunned', 'arm_l': {'preset': 'forward', 'hand': (0.7, 0.62)}, 'yaw': 0.4, 'fx': ['sweat']})), False)], fx=[])
    # e1_14 the heart monitor draws a lightning bolt
    shot(n='H14', set='hosp', t0=59.81, t1=63.53, actors=[], fx=['monitor'],
         keys=[(59.81, (-2.42, 4.47, 1.58), (-3.051, 5.093, 1.30), 24), (63.53, (-2.62, 4.68, 1.48), (-3.051, 5.093, 1.33), 30, 's')])

def _phones(mb, g, t, A, SET, sh, X):
    full = [f for f in os.listdir(os.path.join(HERE, 'hosp_tex')) if f.startswith('phone_screen_full')][0]
    y = pos_at(sh['actors'][0][2], t)[1]
    for i, (px, py, pz) in enumerate(PHONES):
        if y <= py + 0.3: SET.set_phone_screen(i, image=os.path.join(HERE, 'hosp_tex', full), color='#9dffb0', strength=2.4)
    return False
PHONES = [(-1.708, 0.066, 0.967), (-1.708, 3.266, 0.967), (-1.708, 6.466, 0.967), (1.708, 1.966, 0.967), (1.708, 5.166, 0.967), (1.708, 8.366, 0.967)]

def _monitor(mb, g, t, A, SET, sh, X):
    """ECG that scrolls in, beats twice, then draws a lightning bolt; the numbers go wild."""
    from PIL import Image, ImageDraw, ImageFont
    d = os.path.join(HERE, 'mon_frames'); os.makedirs(d, exist_ok=True); p = os.path.join(d, f'm_{g:04d}.png')
    if not os.path.exists(p):
        W, Hh = 512, 384; im = Image.new('RGB', (W, Hh), (8, 16, 20)); dr = ImageDraw.Draw(im)
        for x in range(0, W, 32): dr.line((x, 0, x, Hh), fill=(14, 34, 30))
        for y in range(0, Hh, 32): dr.line((0, y, W, y), fill=(14, 34, 30))
        u = t - sh['t0']; base = 190
        def ecg(x):   # normal beats every 160 px of trace
            q = x % 160
            if 60 < q < 66: return -14
            if 66 <= q < 72: return 70
            if 72 <= q < 80: return -40
            if 90 < q < 110: return 10
            return 0
        bolt = [(0, 0), (30, -120), (52, -40), (88, -150), (108, -60), (150, -170), (170, 40)]   # lightning-shaped spike, relative
        head = int(min(W - 20, 40 + u * 170))        # the drawing head sweeps left to right
        pts = []
        for x in range(0, head):
            bx = x - 260
            if 0 <= bx <= 170 and u > 1.2:
                for (a, ya), (b, yb) in zip(bolt[:-1], bolt[1:]):
                    if a <= bx <= b: pts.append((x, base + ya + (yb - ya) * (bx - a) / (b - a))); break
            else: pts.append((x, base - ecg(x)))
        if len(pts) > 1:
            dr.line(pts, fill=(30, 255, 120), width=5); dr.line(pts, fill=(200, 255, 220), width=2)
            hx, hy = pts[-1]; dr.ellipse((hx - 7, hy - 7, hx + 7, hy + 7), fill=(220, 255, 230))
        f = ImageFont.truetype(os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'), 58)
        hr = '72' if u < 1.3 else str(72 + int((u - 1.3) * 900) % 900)
        dr.text((W - 16, 14), hr, font=f, fill=(255, 230, 60) if u > 1.3 else (60, 255, 140), anchor='ra')
        dr.text((16, 18), 'HR', font=ImageFont.truetype(os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'), 28), fill=(60, 255, 140))
        im.save(p)
    img = X['bpy'].data.images.load(p, check_existing=False); SET.set_monitor_screen(image=img, strength=2.2)
    return False

FX_HOOKS = {'phones': _phones, 'monitor': _monitor}

R = ANCH.get('room', {})
if R:
    SITM = tuple(R['sit_mark']); DIN = tuple(R['door_inside_mark']); DWY = tuple(R['doorway_mark'])
    # e1_20 night in the rented room: fists clenched, then the knock
    shot(n='R20a', set='room', t0=83.52, t1=86.6, fx=['door'],
         keys=[(83.52, (-1.38, 0.18, 1.66), (0.45, 2.4, 0.5), 16), (86.6, (-1.25, 0.45, 1.5), (0.6, 2.1, 0.6), 20, 's')],
         actors=[('you', 'welder', SITM, T((0, 'welder_sit_stool', {'stool': True, 'yaw': -0.5, 'expr': 'sad', 'pitch': 0.6, 'arm_r': 'fists', 'arm_l': 'fists'}),
                                            (85.2, 'welder_sit_stool', {'stool': True, 'yaw': -0.5, 'expr': 'angry', 'arm_r': 'fists', 'arm_l': 'fists', 'zap': ['hair']})), False)])
    shot(n='R20b', set='room', t0=86.6, t1=89.23, dof=1.6, fx=['door'],
         keys=[(86.6, (-1.08, 1.42, 0.95), (0.66, 1.84, 0.8), 30), (89.23, (-0.8, 1.5, 0.92), (0.66, 1.84, 0.8), 36, 's')],
         actors=[('you', 'welder', SITM, T((0, 'welder_sit_stool', {'stool': True, 'yaw': -0.5, 'expr': 'angry', 'arm_r': 'fists', 'arm_l': 'fists'}),
                                            (87.6, 'welder_sit_stool', {'stool': True, 'yaw': 0.6, 'expr': 'stunned', 'arm_r': 'fists', 'arm_l': 'fists', 'fx': ['sweat']})), False)])
    # e1_21 he opens the door: an old man whose hair stands straight up like his
    shot(n='R21a', set='room', t0=89.23, t1=92.0, fx=['door'],
         keys=[(89.23, (1.5, 1.68, 1.6), (-0.08, 4.6, 1.12), 22), (92.0, (1.3, 2.1, 1.55), (-0.05, 4.6, 1.2), 26, 's')],
         actors=[('you', 'welder', DIN, T((0, 'welder_idle_bolt', {'yaw': -0.6, 'expr': 'neutral'}), (90.2, 'welder_idle_bolt', {'yaw': -0.6, 'expr': 'shocked', 'fx': ['sweat']})), False),
                 ('kim', 'kim', DWY, T((0, 'kim_point', {'expr': 'smug', 'arm_r': 'down', 'arm_l': 'behind', 'yaw': 0.3})), False)])
    shot(n='R21b', set='room', t0=92.0, t1=DUR, fx=['door'],
         keys=[(92.0, (0.55, 2.7, 1.55), (0.05, 4.45, 1.55), 26), (DUR, (0.4, 3.2, 1.62), (0.05, 4.45, 1.7), 34, 'o')],
         actors=[('kim', 'kim', DWY, T((0, 'kim_explain', {'expr': 'smug', 'mouth': None, 'zap': ['hair']})), False)])

# 16:9 reframes (LT_ORI=L): the landscape frame is shorter, so these two shots need their own keys
KEYS_L = {
    'H11a': [(45.72, (-1.5, 2.35, 2.45), (-2.6, 3.45, 0.95), 19), (48.3, (-1.65, 2.55, 2.1), (-2.6, 3.45, 1.0), 23, 's')],
    'R20b': [(86.6, (-1.15, 1.38, 1.0), (0.66, 1.84, 1.1), 24), (89.23, (-0.85, 1.48, 0.98), (0.66, 1.84, 1.1), 28, 's')],
}
for _s in SHOTS:
    if _s['n'] in KEYS_L: _s['keysL'] = KEYS_L[_s['n']]
