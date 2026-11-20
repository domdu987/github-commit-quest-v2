"""T1b (film 17 v2, take T1, g172-342): REAL cast17 cards via stage_cast2 on every frame, motion blur 0.5 on g172-278 only.
usage: python3 render.py still <g> <out.png> | full [g_first g_last]   (resume: skips frames/g_NNNN.png > 50 kB)"""
import sys, os, time, math
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(V3, 'set3d17')); import prefecture17 as P, bpy
TAKE = 'T1'; G0, G1 = 191, 342; IDLE = True
CIV = {'lamplighter': 'prisoner_standing_b', 'flaneur_a': 'prisoner_standing_a', 'flaneur_b': 'prisoner_standing_c', 'flaneur_c': 'prisoner_standing_b',
       'newsboy': 'prisoner_standing_c', 'newsboy2': 'prisoner_standing_a', 'cafe_a': 'prisoner_standing_b', 'prisoner_c': 'prisoner_standing_a'}
def assign_for(g):
    a = {'bertillon': ('bertillon_measuring', {'mirror': True}), 'prisoner_a': ('prisoner_sitting_a', {'seated': 'bench'}), 'prisoner_b': ('prisoner_sitting_b', {'seated': 'bench'}),
         'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'}), 'gend_room': ('gendarme_standing_a', {}),
         'gend_door_l': ('gendarme_standing_a', {}), 'gend_door_r': ('gendarme_standing_b', {}), 'gend_wagon': ('gendarme_standing_b', {}), 'desk_gend': ('gendarme_standing_a', {})}
    for k, v in CIV.items(): a[k] = (v, {})
    a['gend_door_l'][1]['mirror'] = False
    if g >= 286:   # TAKE gate: the blue gendarme (gend_door_l) and the second kepi (desk_gend) are cut by the right edge in g310-342. They are out of frame at g286, so from there on
        for nm in ('gend_door_l', 'desk_gend'): a[nm] = (a[nm][0], dict(a[nm][1], dx=0.67, dy=-0.52))   # a constant 0.85 m shift along the camera's right axis moves both fully out of frame
    return {nm: (idle_story(nm, st, g), o) for nm, (st, o) in a.items()} if IDLE else a            # no 'talk' anywhere: every mouth closed (no quote window in T1)
# ---- street liveliness (TAKE gate FIX): eased secondary motion, one visible change per character every <= 40 frames (1.33 s), feet planted
def _sstep(a, b, x): t = max(0.0, min(1.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
GEST = {   # per cast family: list of (name, pose-modifications)
    'gendarme': [('turn', dict(yaw=0.45, gaze=(0.8, 0.1))), ('kepi', dict(arm_r='rub', yaw=0.15)), ('hip', dict(arm_l='hip')), ('turn2', dict(yaw=-0.4, head_roll=6, gaze=(-0.8, 0.1)))],
    'prisoner': [('glance', dict(yaw=-0.55, gaze=(-0.9, 0.0), head_roll=-5)), ('shuffle', dict(legs={'preset': 'step', 'stride': 0.25}, lean=-2)), ('shrug', dict(arm_r='shrug', arm_l='shrug')), ('hip', dict(arm_r='hip', yaw=0.3))],
    'bertillon': [('calipers', dict(arm_r={'hand': (0.8, 0.5), 'bend': -0.2, 'stretch': 1.0, 'layer': 'front'})), ('lean', dict(lean=8, yaw=0.3)), ('calipers2', dict(arm_r={'hand': (0.92, 0.25), 'bend': -0.2, 'stretch': 1.0, 'layer': 'front'}))]}
SWAY = {'gendarme': 2.4, 'prisoner': 1.6, 'bertillon': 1.8}
_IDLE = {}
def idle_story(name, story, g):
    """register and return a per-frame story key: the base pose eased toward one of the character's gestures (cycle 40 frames, eased in and out) plus a slow sway."""
    sys.path.insert(0, os.path.join(V3, 'cast17')); sys.path.insert(0, os.path.join(V3, 'stage')); import cast17, puppet
    cast, base = cast17.STORY17[story]; fam = 'gendarme' if story.startswith('gendarme') else 'bertillon' if story.startswith('bertillon') else 'prisoner'
    seed = sum(ord(c) for c in name); L = 40; ph = (seed * 7) % L; k, r = divmod(g + ph, L); t = r / L
    amt = _sstep(0.0, 0.3, t) * (1 - _sstep(0.62, 0.92, t)); gl = GEST[fam]; _, mods = gl[(k + seed) % len(gl)]
    mods = dict(mods)
    if 'yaw' in mods and seed % 2: mods['yaw'] = -mods['yaw']; mods['gaze'] = (-mods['gaze'][0], mods['gaze'][1]) if 'gaze' in mods else None
    if mods.get('gaze') is None: mods.pop('gaze', None)
    tgt = dict(base); tgt.update(mods); pose = puppet.lerp_pose(cast, base, tgt, amt)
    pose['lean'] = pose.get('lean', 0.0) + SWAY[fam] * math.sin(2 * math.pi * (g + seed) / 70.0)
    pose['expr'] = base.get('expr', 'neutral'); pose['mouth'] = base.get('mouth', 'flat')
    key = 'idle_' + name; cast17.STORY17[key] = (cast, pose); return key
def setup(g0, g1):
    A = P.world_build(TAKE); P.key_take(TAKE, g0=g0, g1=g1); P.setup_render2((720, 1280), samples=16, threads=2); return A
def mb(g):
    r = bpy.context.scene.render; on = 152 <= g <= 278; r.use_motion_blur = on
    if on: r.motion_blur_shutter = 0.5
def clear_cast():
    # stage_cast2 builds NEW actors every call and never removes the old ones (stale shadow proxies stack into black slabs): remove them first.
    sys.path.insert(0, os.path.join(V3, 'stage')); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def one(g, out):
    clear_cast(); sc = bpy.context.scene; sc.frame_set(g + 1); mb(g); P.stage_cast2(TAKE, g, assign_for(g)); sc.render.filepath = out
    t = time.time(); bpy.ops.render.render(write_still=True); P.grade2(out); return time.time() - t
if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'still': setup(max(G0, int(a[1]) - 3), int(a[1]) + 3); print('still g%s %.1fs' % (a[1], one(int(a[1]), a[2])))
    else:
        g0 = int(a[1]) if len(a) > 1 else G0; g1 = int(a[2]) if len(a) > 2 else G1; setup(g0, g1); fd = os.path.join(HERE, 'frames')
        rng = range(g1, g0 - 1, -1) if 'rev' in a else range(g0, g1 + 1)   # 'rev' as 4th arg: render downward so two processes meet in the middle
        for g in rng:
            out = os.path.join(fd, 'g_%04d.png' % g)
            if os.path.exists(out) and os.path.getsize(out) > 50000: continue
            print('g%d %.1fs' % (g, one(g, out)), flush=True)
