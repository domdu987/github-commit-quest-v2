
# ============================================================================= hooks
def _lift_world(h): return float(h) * (LIFT_MAX if STATE.get('loc') == 'street' else CELL_LIFT)

def set_lift(h, frame=None):
    """Lift the building. street: h 0..1 -> 0..LIFT_MAX (3.6 D): the hotel, awnings, portico (door threshold z = GF + lift), jack screws / heads / bars, lamps rise;
    the front stair stays at the old street level (its top is LIFT_MAX below the door at h 1); timber crib layers show once the building clears them.
    under: h 0..1 -> beams, screws and bars rise CELL_LIFT (1 D). Keys linear when frame is given."""
    Lw = _lift_world(h); STATE['lift_k'] = float(h); STATE['lift'] = Lw
    def _k(ob, path, idx): 
        if frame is not None: ob.keyframe_insert(path, index=idx, frame=frame)
    for ob, base in STATE.get('movers', []): ob.location.z = base + Lw; _k(ob, 'location', 2)
    for (bo, bz, ph, x, y) in STATE.get('bars', []): bo.location.z = bz + Lw; _k(bo, 'location', 2)
    for li, ztop, ob in STATE.get('crib_layers', []):
        vis = ztop <= Lw - 0.05 and Lw > 0.4; ob.hide_render = not vis; ob.hide_viewport = not vis
        if frame is not None: ob.keyframe_insert('hide_render', frame=frame)
    if frame is not None:
        for ob in bpy.data.objects:
            if ob.animation_data and ob.animation_data.action:
                for fc in T._fcurves(ob):
                    for kp in fc.keyframe_points: kp.interpolation = 'LINEAR' if fc.data_path != 'hide_render' else 'CONSTANT'
    return Lw

def set_jack_turn(angle, frame=None):
    """Turn every jack lever by `angle` degrees about its screw axis (a half turn = 180). Keys linear when frame is given."""
    for (bo, bz, ph, x, y) in STATE.get('bars', []):
        bo.rotation_euler.z = ph + math.radians(angle)
        if frame is not None:
            bo.keyframe_insert('rotation_euler', index=2, frame=frame)
            for fc in T._fcurves(bo):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    STATE['jack_angle'] = float(angle)

def set_fill(k, frame=None):
    """Street fill level k 0..1 raises mud, puddles, scum, piles, carts, barrels, planks by k * FILL_MAX (2.5 D); buildings, stair and sidewalks stay."""
    for ob in STATE.get('fill_objs', []):
        ob.location.z = float(k) * FILL_MAX
        if frame is not None: ob.keyframe_insert('location', index=2, frame=frame)
    STATE['fill'] = float(k)

def set_tea_ripple(k, frame=None):
    """Tea surface: k 0 = perfectly still flat mirror (no normal perturbation at all), 1 = visible ripples. The phase follows the frame number."""
    m = STATE['M']['tea']; f = frame if frame is not None else bpy.context.scene.frame_current
    D._keyval(m, 'ripple_k', float(k), frame, 'LINEAR'); D._keyval(m, 'ripple_p', f * 0.35, frame, 'LINEAR'); STATE['tea_k'] = float(k)

def set_rain(level, frame=None, speed=1.0):
    """Rain streaks (compositor overlay, RAIN light only; level 0..1.5). See wall.set_rain."""
    if STATE.get('rain'): W9.set_rain(level, frame=frame, speed=speed)

def set_cutaway(on):
    """Hide the cellar ceiling (beams, joists, floor slab) from the camera only: it keeps casting shadows, so the lighting does not change (under_rows)."""
    for ob in STATE.get('cut_objs', []): ob.visible_camera = not bool(on)
    STATE['cut'] = bool(on)

def clear_keys():
    for ob in bpy.data.objects:
        if ob.animation_data: ob.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()

def apply_state(state):
    for tok in [t for t in (state or '').replace(' ', '').split(',') if t]:
        if tok.startswith('lift'): set_lift(float(tok[4:]))
        elif tok.startswith('fill'): set_fill(float(tok[4:]))
        elif tok.startswith('jack'): set_jack_turn(float(tok[4:]))
        elif tok.startswith('tea'): set_tea_ripple(float(tok[3:]))
        elif tok.startswith('cut'): set_cutaway(float(tok[3:]) > 0)
        elif tok.startswith('rain'): set_rain(float(tok[4:]))

def stand(name):
    """world position of a named stand point at the current lift (marks flagged 'moves with the lift' add the lift)."""
    x, y, z, lk = STATE['marks'][name]; return (x, y, z + (STATE.get('lift', 0.0) if lk else 0.0))

# ----------------------------------------------------------------------------- placeholder cast + crowd
T.PH.update(
    worker=('beach_man', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    foreman=('senior_b', dict(yaw=-0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), 3.0),
    rich=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), 3.3),
    maid=('beach_woman', dict(yaw=-0.2, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.9),
    clerk=('senior_a', dict(yaw=0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 3.0),
    kid=('beach_kid', dict(yaw=-0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.4),
    towns_m=('senior_a', dict(yaw=-0.2, expr='smug', arm_l='hip', arm_r='down', legs='stand'), 3.1),
    towns_f=('beach_woman', dict(yaw=0.2, expr='happy', arm_l='down', arm_r='hip', legs='stand'), 2.9),
    towns_o=('beach_man', dict(yaw=-0.25, expr='happy', arm_l='hip', arm_r='hip', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor
KINDS_STREET = ['worker', 'clerk', 'foreman', 'towns_m', 'towns_f', 'towns_o', 'maid', 'kid']
KINDS_WORK = ['worker', 'foreman', 'worker', 'clerk', 'worker']

def _cards_face(scene, *args):
    """Handler: every background / crowd card yaws to face the scene camera (cards read from any preset)."""
    cam = scene.camera if scene else None
    if cam is None: return
    cp = cam.matrix_world.translation
    for ob in STATE.get('cards', []):
        try:
            p = ob.matrix_world.translation; d = cp - p; ob.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
        except ReferenceError: pass

def _proto(role):
    pr = STATE.setdefault('protos', {})
    if role not in pr:
        ob = T.placeholder_actor(role, (0, 0, -500), name='bgproto_' + role)
        for c in list(ob.users_collection): c.objects.unlink(ob)
        STATE['SET'].objects.link(ob); ob.hide_render = True; ob.hide_viewport = True; pr[role] = ob
    return pr[role]

def crowd(n, regions, seed=1, kinds=None, ground=0.0, min_dist=1.5, scale=(0.93, 1.07), points=None):
    """Place n placeholder cards (cast cards copied from prototypes, sharing mesh + material, turned to the camera every frame by _cards_face).
    regions: [(x0, x1, y0, y1), ...] random rejection sampling with min_dist; or points=[(x, y), ...] exact positions. ground: z or f(x, y) -> z.
    kinds: list of roles (default KINDS_STREET). Returns the objects (names 'bgcard_*'; they are not removed by stage_placeholders)."""
    r = _rnd(seed); kinds = kinds or KINDS_STREET; out = []; pts = []
    if points is None:
        tries = 0
        while len(pts) < n and tries < n * 80:
            tries += 1; (x0, x1, y0, y1) = regions[r.randrange(len(regions))]; x, y = r.uniform(x0, x1), r.uniform(y0, y1)
            if all((x - a) ** 2 + (y - b) ** 2 >= min_dist ** 2 for a, b in pts): pts.append((x, y))
    else: pts = list(points)[:n]
    for i, (x, y) in enumerate(pts):
        role = kinds[r.randrange(len(kinds))]; pro = _proto(role); ob = pro.copy(); ob.name = 'bgcard_%d_%s' % (len(STATE['cards']), role)
        STATE['SET'].objects.link(ob); ob.hide_render = False; ob.hide_viewport = False; s = r.uniform(*scale); ob.scale = (s, s, s)
        z = ground(x, y) if callable(ground) else float(ground); ob.location = (x, y, z); ob.visible_shadow = True; STATE['cards'].append(ob); out.append(ob)
    return out

def crowd_aisles(n, seed=1, kinds=None, rows=None):
    """workers standing in the cellar aisles beside the jacks (one per aisle slot: x = jack column + 1.3, y = beam row - 1.35)."""
    r = _rnd(seed); slots = [(UX[k] + 1.3, UY[j] - 1.35) for k in range(len(UX) - 1) for j in range(len(UY)) if rows is None or j in rows]; r.shuffle(slots)
    return crowd(n, None, seed=seed, kinds=kinds or KINDS_WORK, ground=0.0, points=slots[:n], scale=(0.95, 1.05))

# ----------------------------------------------------------------------------- staging
STAGING = dict(
    street_wide=[('rich', 'front_a'), ('worker', 'front_b'), ('foreman', 'walk_a'), ('clerk', 'sidewalk_r')],
    hotel_front=[('rich', 'front_c'), ('worker', 'front_b'), ('foreman', 'front_a')],
    front_stair=[('rich', 'door'), ('clerk', 'stair_foot'), ('worker', 'mud_fall')],
    mud_low=[('worker', 'cart_c'), ('foreman', 'walk_b')],
    rain_street=[('worker', 'front_a'), ('clerk', 'sidewalk_r'), ('foreman', 'walk_a')],
    crowd_street=[('rich', 'front_c')],
    under_wide=[('worker', 'worker_a'), ('worker', 'worker_b'), ('foreman', 'foreman'), ('worker', 'worker_c'), ('worker', 'worker_d')],
    under_rows=[('foreman', 'foreman')],
    jack_close=[('worker', 'jack_hands')],
    suite_window=[('rich', 'window_r')],
    tea_close=[],
    suite_two=[('rich', 'window')])
PRESET_CROWD = dict(
    crowd_street=lambda: crowd(24, [(-16, 16, -26, -14)], seed=5, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=1.7) + crowd(8, [(-28, -10, -7.5, -4)], seed=8, ground=1.3, min_dist=1.7),
    street_wide=lambda: crowd(10, [(-30, 30, -30, -14)], seed=6, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=3.0),
    rain_street=lambda: crowd(6, [(-20, 20, -30, -14)], seed=7, ground=lambda x, y: float(STATE['mud_z'](np.array([x]), np.array([y]))[0]), min_dist=4.0),
    under_wide=lambda: crowd_aisles(16, seed=3, rows=range(0, 9)),
    under_rows=lambda: crowd_aisles(70, seed=4),
    jack_close=lambda: crowd_aisles(6, seed=9, rows=range(5, 9)),
)

def stage_placeholders(A, name, cam_loc, with_crowd=True):
    """actor cards at the named stand points of the preset (STAGING) + the preset's crowd (PRESET_CROWD)."""
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(STAGING.get(name, [])):
        pos = stand(mk) if isinstance(mk, str) else tuple(mk); d = Vector(cam_loc) - Vector(pos); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, tuple(pos), face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    if with_crowd and name in PRESET_CROWD and not STATE.get('crowd_done'): PRESET_CROWD[name](); STATE['crowd_done'] = True
    return out

def head_pixels(name):
    """[(role, mark, chin_y_px, feet_y_px)] at 720x1280 for the preset's staged actors (rule: chin y < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for (role, mk) in STAGING.get(name, []):
        pos = Vector(stand(mk) if isinstance(mk, str) else mk); h = T.PH[role][2]
        b = world_to_camera_view(sc, cam, pos + Vector((0, 0, h - 1.0))); f = world_to_camera_view(sc, cam, pos)
        out.append((role, mk, round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

def anchors():
    P = STATE['P']; PR = PRESETS[STATE['preset']]
    return dict(location=STATE['loc'], preset=STATE['preset'], light=STATE['light'], cams={k: dict(v) for k, v in CAMS.items()}, cam=dict(CAMS[PR['cam']]), cam_name=PR['cam'],
                key_dir=tuple(Vector(P['key_dir']).normalized()), marks={k: tuple(v[:3]) for k, v in STATE.get('marks', {}).items()}, lights=[o.name for o in STATE['LIGHTS'].objects],
                lift_max=LIFT_MAX, cell_lift=CELL_LIFT, fill_max=FILL_MAX, staging={k: list(v) for k, v in STAGING.items()})

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def render_preset(preset, out, quality='final', actors=True, state=None, light=None, crowds=True):
    scene = bpy.context.scene; A = build(preset, light=light, state=state)
    setup_render(scene, quality); cam = make_camera(A['cam'])
    if actors: stage_placeholders(A, A['cam_name'], tuple(cam.location), with_crowd=crowds)
    return T.render(out)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stills'; names = sys.argv[2:] or list(PRESETS)
    q = 'final' if mode == 'final' else 'preview'; od = os.path.join(WORK, 'final' if mode == 'final' else 'stills'); os.makedirs(od, exist_ok=True)
    for n in names:
        parts = n.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None; stt = parts[2] if len(parts) > 2 else None
        t = render_preset(pr, os.path.join(od, n.replace(':', '_').replace(',', '-') + '.png'), q, light=lt, state=stt); print(n, 'wall %.1f cpu %.1f' % t, flush=True)
