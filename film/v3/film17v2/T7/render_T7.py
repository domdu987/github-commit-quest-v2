import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'film/v3/set3d17')); os.chdir(os.path.join(ROOT, 'film/v3/set3d17'))
import prefecture17 as P, bpy
take = 'T7'
def assign_for(g):
    a = {'inspector': ('inspector_shocked', {}), 'gend_b': ('gendarme_standing_b', {})}
    if g < 1792:   # 7a: Bertillon holds the card up, Dupont (fake moustache gag)
        a['bertillon'] = ('bertillon_holding_card', {}); a['dupont'] = ('dupont_caught' if g < 1730 else 'dupont_innocent', {})
    else:          # 7b: escort line + triumph
        a['bertillon'] = ('bertillon_triumphant', {}); a['dupont'] = ('dupont_innocent', {})
        a['gend_a'] = ('gendarme_escort_a', {}); a['thief1'] = ('prisoner_standing_a', {}); a['thief2'] = ('prisoner_standing_b', {})
    return a
def main(g0, g1, outdir, samples=16):
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=samples, threads=2)
    sc = bpy.context.scene
    for g in range(g0, g1 + 1):
        fp = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
        t = time.time(); sc.frame_set(g + 1)
        sc.render.use_motion_blur = 1800 <= g <= 1867
        if sc.render.use_motion_blur: sc.render.motion_blur_shutter = 0.5
        P.stage_cast2(take, g, assign_for(g)); sc.render.filepath = fp
        bpy.ops.render.render(write_still=True); P.grade2(fp); print('g', g, '%.0fs' % (time.time() - t), flush=True)
if __name__ == '__main__': main(int(sys.argv[1]), int(sys.argv[2]), os.path.abspath(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 16)
