"""T2b g494-657. usage: render_t2b.py still <g> <out.png> [W H] | range g0 g1"""
import sys, os, time, json
SET = "/home/user/github-commit-quest-v2/film/v3/set3d17"; sys.path.insert(0, SET); os.chdir(SET)
sys.path.insert(0, SET + '/../stage'); sys.path.insert(0, SET + '/../cast17')
import prefecture17 as P, bpy
take = 'T2'; OUT = "/home/user/github-commit-quest-v2/film/v3/film17v2/T2b/frames"; os.makedirs(OUT, exist_ok=True)
# continuity with T2a (director): same T2 measure/corridor overrides
P.TAKE_OVER['T2'] = {'corridor': dict(lamp_k=4.0, shade_mul=1.6, fill_w=300, gain=0.95), 'measure': dict(shade_mul=1.2)}
LIFT = dict(gain=1.0, lamp=1.0, fill=1.0, key=1.0, g0=497, g1=510); LIFT.update(json.loads(os.environ.get('T2B_LIFT', '{}')))
def smooth(g):
    t = min(1.0, max(0.0, (g - LIFT['g0']) / float(LIFT['g1'] - LIFT['g0']))); return t * t * (3 - 2 * t)
def apply_lift(g):
    """measure-room lift, smoothstep g497-510 then held. Lights + painted ambient only (no haze, no desaturation). Keyed on this frame only."""
    s = smooth(g)
    if s <= 0: return 0.0
    L = P.W['locs']['measure']; f = g + 1
    for o in L.coll.objects:
        if o.type == 'LIGHT' and o.data.type in ('POINT', 'AREA'):
            n = o.name
            m = LIFT['lamp'] if (n.startswith('lamp') or n.startswith('bracket') or n.startswith('gas')) else LIFT['fill'] if 'fill' in n else LIFT['key'] if n.startswith('win') else LIFT['lamp']
            o.data.energy = o.data.energy * (1 + (m - 1) * s); o.data.keyframe_insert('energy', frame=f)
    seen = set()
    for o in L.coll.objects:
        if o.type == 'MESH':
            for mt in o.data.materials:
                if mt and mt.name not in seen and mt.node_tree and 'amb_gain' in mt.node_tree.nodes:
                    seen.add(mt.name); sk = mt.node_tree.nodes['amb_gain'].inputs['Scale']
                    if 'g_base' not in mt: mt['g_base'] = sk.default_value
                    sk.default_value = mt['g_base'] * (1 + (LIFT['gain'] - 1) * s); sk.keyframe_insert('default_value', frame=f)
    return s
HOLD_END, BLEND_END, TALK_FROM = 496, 500, 498   # director's join fix: laugh held g494-496, blended into the talk pose by g500
def _sm(u): u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)
def _lerp(a, b, u):
    if isinstance(a, (tuple, list)): return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u
def blend_pose(pa, pb, u):
    """pa (laugh) -> pb (talk): numbers and hand positions are lerped; discrete things (expr, mouth, fx, arm shapes, legs, string arm poses) switch at u 0.5."""
    out = dict(pb); D = dict(yaw=0.0, pitch=0.0, head_roll=0.0, lean=0.0, t=0.0, squash=(1.0, 1.0))
    for k in D: out[k] = _lerp(pa.get(k, D[k]), pb.get(k, D[k]), u)
    sw = pb if u >= 0.5 else pa
    for k in ('expr', 'mouth', 'legs'): out[k] = sw[k]
    if u >= 0.5: out.pop('fx', None)
    else: out['fx'] = pa.get('fx')
    for k in ('arm_r', 'arm_l'):
        a, b = pa[k], pb[k]
        if isinstance(a, dict) and isinstance(b, dict):
            o = dict(b); o['hand'] = _lerp(a['hand'], b['hand'], u); o['bend'] = _lerp(a.get('bend', 0.0), b.get('bend', 0.0), u); o['stretch'] = _lerp(a.get('stretch', 1.0), b.get('stretch', 1.0), u); o['shape'] = sw[k]['shape']; out[k] = o
        else: out[k] = sw[k]
    return out
def story_blend(g, laugh, calm, name):
    import cast17
    u = _sm((g - HOLD_END) / float(BLEND_END - HOLD_END))
    if u <= 0: return laugh
    if u >= 1: return calm
    (c, pa), (_, pb) = cast17.STORY17[laugh], cast17.STORY17[calm]
    cast17.STORY17[name] = (c, blend_pose(pa, pb, u)); return name
def assign_for(g):
    return {'inspector': (story_blend(g, 'inspector_laughing', 'inspector_pointing_mock', 't2b_insp'), {'talk': TALK_FROM <= g <= 651}),   # lip-sync once the mouth is in the talk pose (g498), through g651
            'bertillon': ('bertillon_measuring', {'mirror': True}), 'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
            'gend_room': (story_blend(g, 'gendarme_laughing_a', 'gendarme_standing_a', 't2b_ga'), {}), 'gend_room2': (story_blend(g, 'gendarme_laughing_b', 'gendarme_standing_b', 't2b_gb'), {}),
            'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'})}
def clear_cards():
    import actors
    for o in list(bpy.data.objects):
        if 'c2_' in o.name or o.name.startswith('back_hair_') or o.name.startswith('back_coat_'): bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def frame(g, out, A):
    clear_cards(); P.shot(take, g, A, cards=False); apply_lift(g)
    P.stage_cast2(take, g, assign_for(g)); bpy.context.scene.render.filepath = out
    t = time.time(); bpy.ops.render.render(write_still=True); P.grade2(out); return time.time() - t
if __name__ == '__main__':
    a = sys.argv[1:]; assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take)
    if a[0] == 'still':
        W_, H_ = (int(a[3]), int(a[4])) if len(a) > 4 else (720, 1280); P.setup_render2((W_, H_), samples=16, threads=2); bpy.context.scene.render.use_motion_blur = False
        print('still g%s %.1fs lift %.2f' % (a[1], frame(int(a[1]), a[2], A), smooth(int(a[1]))), flush=True)
    else:
        P.setup_render2((720, 1280), samples=16, threads=2); bpy.context.scene.render.use_motion_blur = False
        for g in range(int(a[1]), int(a[2]) + 1):
            o = '%s/g_%04d.png' % (OUT, g)
            if os.path.exists(o) and os.path.getsize(o) > 50000: continue
            print('done', g, '%.1fs' % frame(g, o, A), flush=True)
