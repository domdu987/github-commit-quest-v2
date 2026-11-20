"""T5a render: g1039-1210. usage: python3 render_t5a.py still <g> <out.png> | range [g0 g1]  (resume: skips frames > 50 kB)"""
import sys, os, math
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d17')
import prefecture17 as P, bpy
for _p in ('stage', 'cast17'): sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/' + _p)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t5a_override; t5a_override.apply()
import t5a_stage   # Bertillon back view as hair + coat (T6b approach)
take = 'T5'
import cast17
for _s in ('a', 'b'):   # 'heh' pose: the standing pose with a small open grin (held shape, not lip-sync)
    _c, _p = cast17.STORY17['gendarme_standing_' + _s]; _p = dict(_p); _p['mouth'] = ('open', 0.22, 0.12); cast17.STORY17['gendarme_heh_' + _s] = (_c, _p)
HERE = os.path.dirname(os.path.abspath(__file__))
BEAMONLY = bool(os.environ.get('T5A_BEAMONLY'))   # test mode: only the beam change, everything else as the first full render
def beam_off():
    # director: beam OFF (milky veil flickers). Drop the keyed strength of every beam_fx material and force it to 0.
    n = 0
    for m in bpy.data.materials:
        if m.name.startswith('beam_fx') and m.node_tree:
            ad = m.node_tree.animation_data
            if ad: m.node_tree.animation_data_clear()
            nd = m.node_tree.nodes.get('strength')
            if nd: nd.inputs[1].default_value = 0.0; n += 1
    print('beam_off materials', n, flush=True)
def _ease(g, g0=1196, g1=1210):
    u = min(max((g - g0) / (g1 - g0), 0.0), 1.0); return u * u * (3 - 2 * u)
def assign_for(g):
    a = {}
    a['bertillon'] = ('bertillon_tired', {})
    if g < 1120: a['inspector'] = ('inspector_arms_crossed', {})
    elif g < 1196: a['inspector'] = ('inspector_shouting', {'talk': 1128 <= g <= 1196})   # lip-sync only in the quote window
    else: a['inspector'] = ('inspector_arms_crossed', {})
    OFF = (-0.6, 0.3)   # green gendarme (gend_b) kept off the left edge: constant offset while g<1196, eased out over g1196-1210 (T5b lane x15.9 at g1211)
    if g >= 1196:
        k = 1.0 - _ease(g)
        a['dupont'] = ('dupont_held', {}); a['gend_a'] = ('gendarme_escort_a', {})
        a['gend_b'] = ('gendarme_escort_b', {} if BEAMONLY else {'dx': OFF[0] * k, 'dy': OFF[1] * k})
    elif BEAMONLY:
        bz = 0.06 * 0.5 * (1 - math.cos(2 * math.pi * 3.0 * g / 30.0)) if 1111 <= g < 1196 else 0.0
        a['gend_a'] = ('gendarme_standing_a', {'expr': 'smug', 'dz': bz}); a['gend_b'] = ('gendarme_standing_b', {'expr': 'smug', 'dz': bz * 0.8})
    else:
        sn = 1111 <= g <= 1171      # planted chuckle (feet fixed): squash/stretch scale-z 0.94<->1.0 at 3 Hz about the feet + 0.04 head bob; open 'heh' grin on the up beat
        ph = (3.0 * g / 30.0) % 1.0; c = 0.5 * (1 + math.cos(2 * math.pi * ph)) if sn else 1.0      # 1 = stretched (up), 0 = squashed
        heh = sn and c > 0.5
        for _s in ('a', 'b'):
            _c, _p = cast17.STORY17['gendarme_standing_' + _s]; _p = dict(_p); _p['expr'] = 'smug'; _p['squash'] = (1.0, 0.94 + 0.06 * c); _p['head_dy'] = 0.04 * (c - 0.5) * -1 if sn else 0.0
            if heh: _p['mouth'] = ('open', 0.22, 0.12)
            cast17.STORY17['gendarme_snk_' + _s] = (_c, _p)
        a['gend_a'] = ('gendarme_snk_a', {})
        a['gend_b'] = ('gendarme_snk_b', {'dx': OFF[0], 'dy': OFF[1]})
    return a
def clear_cast():
    # stage_cast2 builds NEW actors every call and never removes the old ones (stale shadow proxies -> black slabs): remove them first.
    sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_', 'bk_', 't6b_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def setup():
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); beam_off(); P.setup_render2((720, 1280), samples=16, threads=2); return A
if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    A = setup()
    if a[0] == 'stills':     # stills <outdir> g g g ... (one process, clear_cast each frame)
        os.makedirs(a[1], exist_ok=True)
        for g in [int(x) for x in a[2:]]:
            bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
            fp = os.path.join(a[1], 'g_%04d.png' % g); bpy.context.scene.render.filepath = fp; bpy.ops.render.render(write_still=True); P.grade2(fp); print('still', g, flush=True)
    elif a[0] == 'still':
        g = int(a[1]); bpy.context.scene.frame_set(g + 1); clear_cast(); acts = P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = a[2]; bpy.ops.render.render(write_still=True); P.grade2(a[2]); print('still done', sorted(acts))
    else:
        g0, g1 = (int(a[1]), int(a[2])) if len(a) > 2 else P.TAKES[take]['render']
        g1 = min(g1, 1210)
        for g in range(g0, g1 + 1):
            fp = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
            if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
            bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
            bpy.context.scene.render.filepath = fp; bpy.ops.render.render(write_still=True); P.grade2(fp); print('g', g, flush=True)
