"""T1b (film 17 v2, take T1, g172-342): REAL cast17 cards via stage_cast2 on every frame, motion blur 0.5 on g172-278 only.
usage: python3 render.py still <g> <out.png> | full [g_first g_last]   (resume: skips frames/g_NNNN.png > 50 kB)"""
import sys, os, time, math
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(V3, 'set3d17')); import prefecture17 as P, bpy
TAKE = 'T1'; G0, G1 = 172, 342
CIV = {'lamplighter': 'prisoner_standing_b', 'flaneur_a': 'prisoner_standing_a', 'flaneur_b': 'prisoner_standing_c', 'flaneur_c': 'prisoner_standing_b',
       'newsboy': 'prisoner_standing_c', 'newsboy2': 'prisoner_standing_a', 'cafe_a': 'prisoner_standing_b', 'prisoner_c': 'prisoner_standing_a'}
def assign_for(g):
    a = {'bertillon': ('bertillon_measuring', {'mirror': True}), 'prisoner_a': ('prisoner_sitting_a', {'seated': 'bench'}), 'prisoner_b': ('prisoner_sitting_b', {'seated': 'bench'}),
         'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'}), 'gend_room': ('gendarme_standing_a', {}),
         'gend_door_l': ('gendarme_standing_a', {}), 'gend_door_r': ('gendarme_standing_b', {}), 'gend_wagon': ('gendarme_standing_b', {}), 'desk_gend': ('gendarme_standing_a', {})}
    for k, v in CIV.items(): a[k] = (v, {})
    return a            # no 'talk' anywhere: every mouth closed (no quote window in T1)
def setup(g0, g1):
    A = P.world_build(TAKE); P.key_take(TAKE, g0=g0, g1=g1); P.setup_render2((720, 1280), samples=16, threads=2); return A
def mb(g):
    r = bpy.context.scene.render; on = 152 <= g <= 278; r.use_motion_blur = on
    if on: r.motion_blur_shutter = 0.5
def one(g, out):
    sc = bpy.context.scene; sc.frame_set(g + 1); mb(g); P.stage_cast2(TAKE, g, assign_for(g)); sc.render.filepath = out
    t = time.time(); bpy.ops.render.render(write_still=True); P.grade2(out); return time.time() - t
if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'still': setup(max(G0, int(a[1]) - 3), int(a[1]) + 3); print('still g%s %.1fs' % (a[1], one(int(a[1]), a[2])))
    else:
        g0 = int(a[1]) if len(a) > 1 else G0; g1 = int(a[2]) if len(a) > 2 else G1; setup(g0, g1); fd = os.path.join(HERE, 'frames')
        for g in range(g0, g1 + 1):
            out = os.path.join(fd, 'g_%04d.png' % g)
            if os.path.exists(out) and os.path.getsize(out) > 50000: continue
            print('g%d %.1fs' % (g, one(g, out)), flush=True)
