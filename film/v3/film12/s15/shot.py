#!/usr/bin/env python3
"""shot.py -- film 12 take s15: shots 15-18, the REVEAL (t 34.98-44.66 s).  One process = one street build ('rank_rush', RAIN), my own cameras.
  15  g1049-1115  coach_close push: head coachman counts coins in his purse, then looks up at the rain, grinning (rank still empty, rain swells)
  16  g1116-1199  rank_rush: rain pours, the crowd runs from the left kerb and pushes in at the coach doors, coaches fill one by one
  17  g1200-1271  rank_wide: every coach full and rolling away, coachmen cheering
  18  g1272-1339  hero_track: Hanway strolls past the wet queue, dry; the head coachman's grin drops
Handles: 6 frames each side (g1043-1345).  Mouths: nobody speaks (no quote in 15-18): every pose keeps its own held mouth.
    python3 shot.py stills a:b[:step] <out_dir> [samples]      draft 360x640
    python3 shot.py final a:b[:step] [samples]                 720x1280 into frames/
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
from c12 import S, bpy, cast12, Vector, lerp, clamp, ez, g_of, g_bound

H = 6
SH = {15: (g_bound(34.98), g_bound(37.20) - 1), 16: (g_bound(37.20), g_bound(40.00) - 1),
      17: (g_bound(40.00), g_bound(42.40) - 1), 18: (g_bound(42.40), g_bound(44.66) - 1)}
G0, G1 = SH[15][0] - H, SH[18][1] + H
CUTS = [SH[16][0], SH[17][0], SH[18][0]]
SC = cast12.STORY12
def shot_of(g):
    for k in (15, 16, 17, 18):
        if g <= SH[k][1] or k == 18: return k
    return 18
PRESET = {15: 'coach_close', 16: 'rank_rush', 17: 'rank_wide', 18: 'hero_track'}
LENS = {15: 25.0, 16: 22.0, 17: 22.0, 18: 22.0}

CAM17 = dict(loc=(-2.6, -1.0, 2.1), look_at=(3.4, 26.0, 3.8), loc_b=(-2.0, 2.5, 2.3), look_b=(3.4, 28.0, 3.9), lens=22.0)
CAM15 = dict(loc=(-0.6, 11.4, 3.4), look_at=(3.5, 18.7, 6.0), loc_b=(1.9, 14.4, 4.7), look_b=(3.55, 18.6, 6.0), lens=25.0)
CAM16 = dict(loc=(-3.4, 1.0, 3.0), look_at=(1.6, 24.0, 3.9), loc_b=(-2.9, 5.0, 3.1), look_b=(2.6, 33.0, 4.0), lens=22.0)

def cam_for(g):
    k = shot_of(g); a, b = SH[k]; x = (g - a) / float(b - a)
    u = 0.3 * ez(clamp(x)) + 0.7 * x                      # mostly linear (never static), mild ease at the start
    u = clamp(u, -0.12, 1.12)
    cs = {15: CAM15, 16: CAM16, 17: CAM17}.get(k) or S.CAMS[PRESET[k]]
    L = lambda p, q: tuple(pp + (qq - pp) * u for pp, qq in zip(p, q))
    return L(cs['loc'], cs['loc_b']), L(cs['look_at'], cs['look_b']), cs['lens']

# ----- beats
G_SKY = g_of(36.00)        # looks up at the rain
G_THUNDER = g_of(37.2)
RUSH0, RUSH1 = SH[16][0] + 2, SH[16][0] + 62            # rush k 0.35 .. 1.0
G_COIN2 = g_of(39.0)       # coins clink: purse close-up pose
G_DROP = g_bound(43.55)    # the grin drops as Hanway passes beneath
BOX_A = (3.55, 18.6, 4.22); BOX_B = (3.55, 35.1, 4.22); BOX_C = (3.55, 51.6, 4.22)
ROLL = (SH[17][0] - 2, SH[17][1] + H + 2)                # coaches pull away
ROLL_DY = {0: -4.0, 1: -9.0, 2: -9.0, 3: -9.0}
HAN_A, HAN_C = Vector((-1.2, 8.0, 0.0)), Vector((-1.2, 17.8, 0.0))
RUSH_MEM = ['crowd_man_a', 'crowd_man_b', 'crowd_man_c', 'crowd_man_d', 'crowd_woman_a', 'crowd_woman_b']
RUSH_PICK = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 18, 20, 21]   # which of the 24 anchors get a card (16 shot)

def coach_dy(i, g):
    r0, r1 = ROLL; u = clamp((g - r0) / float(r1 - r0))
    return ROLL_DY[i] * (u if g < r1 else 1.0) * (0.35 + 0.65 * u if False else 1.0)

def box_pos(base, i, g):
    return (base[0], base[1] + coach_dy(i, g), base[2])

def build_set(quality):
    S.shot('rank_rush', 'RAIN', u=0.5, placeholders=False, figures=False, quality=quality)
    sc = bpy.context.scene
    S.crowd_figures(False)
    S.rain(0.70, frame=G0); S.rain(1.0, frame=SH[15][0] + 52); S.rain(1.0, frame=G1)
    S.set_rank_busy(0.0, frame=G0); S.set_rank_busy(0.0, frame=SH[16][0] + 18)
    S.set_rank_busy(0.1, frame=SH[16][0] + 22); S.set_rank_busy(0.3, frame=SH[16][0] + 38); S.set_rank_busy(0.55, frame=SH[16][0] + 52)
    S.set_rank_busy(0.8, frame=SH[16][0] + 68); S.set_rank_busy(1.0, frame=SH[16][0] + 83); S.set_rank_busy(1.0, frame=G1)
    # hide the 3D rush placeholders in any case: cards do the crowd
    r0, r1 = ROLL
    for i in (0, 1, 2, 3):
        ob = bpy.data.objects['coach_%d' % i]; y0 = ob.location.y
        for f, y in ((r0, y0), (r1, y0 + ROLL_DY[i])):
            ob.location = (ob.location.x, y, 0.0); ob.keyframe_insert('location', frame=f)
        for _, fc in S._fcs(ob):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
        ob.location = (ob.location.x, y0, 0.0)
    bpy.context.view_layer.update()

def coach_card(name, pose_name, mark, cl, g, over=None):
    o = dict(blink=cast12.blink_at(g, 83, 11), t=g / 30.0); o.update(over or {})
    return C.card(name, SC[pose_name], mark, cl, over=o, mirror=True)

def build_cards(g, cl):
    C.drop_cards(); k = shot_of(g); heads = {}
    def hd(nm, ob, h):
        pass
    # --- the head coachman (all four shots)
    pa = box_pos(BOX_A, 0, g)
    if k == 15 or (k == 16 and g < G_COIN2 - 4):
        pose = 'coachman_count_coins' if g < G_SKY else 'coachman_count_coins_sky'
        if k == 16: pose = 'coachman_count_coins_sky'
        over = dict(purse_open=0.55 + 0.45 * math.sin(g * 0.7) ** 2) if pose == 'coachman_count_coins' else dict(purse_open=0.8)
    elif k == 16:
        pose, over = 'coachman_count_coins', dict(purse_open=0.55 + 0.45 * math.sin(g * 0.8) ** 2)
    elif k == 17:
        pose, over = 'coachman_gloat', None
    else:
        pose, over = ('coachman_gloat' if g < G_DROP else 'coachman_grin_drop'), None
    bob = 0.05 * math.sin(g * 0.55) if k in (15, 16) else 0.0
    coach_card('actor_box_a', pose, (pa[0], pa[1], pa[2] + bob), cl, g, over)
    heads['box_a'] = pa
    if k in (16, 17, 18):
        pb = box_pos(BOX_B, 1, g)
        coach_card('actor_box_b', 'coachman_b_nod' if k != 17 else 'coachman_b_laugh', (pb[0], pb[1], pb[2] + 0.04 * math.sin(g * 0.6 + 1)), cl, g)
    if k == 17:
        pc = box_pos(BOX_C, 2, g)
        coach_card('actor_box_c', 'coachman_c_nod', (pc[0], pc[1], pc[2]), cl, g)
    # --- the rush (shot 16; a few stragglers still pushing in shot 17's first frames are inside coaches by then)
    if k == 16:
        kk = lerp(0.35, 1.0, clamp((g - RUSH0) / float(RUSH1 - RUSH0)))
        for n, j in enumerate(RUSH_PICK):
            r = S.STATE['rush_slots'][j]; d = r['delay']; e = clamp((kk - d) / (1 - d))
            p0, p1 = Vector(r['start']), Vector(r['end']); pos = p0 + (p1 - p0) * (e * (2 - e) if e < 1 else 1.0)   # ease out at the door
            m = RUSH_MEM[j % 6]
            if e >= 0.97:
                c_, pz = SC[m + '_push']; sh = 0.07 * math.sin(g * 0.9 + j)
                pos = Vector((pos.x + sh, pos.y, 0.0))
                C.card('actor_rush_%02d' % n, (c_, dict(pz, t=g / 30.0)), pos, cl)
            else:
                C.card('actor_rush_%02d' % n, cast12.cycle_frame(m + '_rush', (g * 1.0 / 16.0 + j * 0.13) % 1.0, facing=1), (pos.x, pos.y, 0.0), cl)
    # --- hanway + the wet queue (shot 18 only)
    if k == 18:
        a, b = SH[18]; x = clamp((g - a) / float(b - a + 1))
        pos = HAN_A.lerp(HAN_C, x)
        c_, p_ = cast12.cycle_frame('hanway_walk_umbrella', (g / 28.0) % 1.0, facing=1)
        p_ = dict(p_, expr='smug', mouth='smirk', head_roll=-3.0, pitch=-0.35, blink=cast12.blink_at(g, 97, 4))
        C.card('actor_hanway', (c_, p_), (pos.x, pos.y, 0.0), cl, rim='#f2b25c')
        cm, pm = SC['crowd_man_c_wring_wig']; C.card('actor_q_a', (cm, dict(pm, t=g / 30.0)), (-0.1, 23.8 + 0.0, 0.0), cl, over=dict(blink=cast12.blink_at(g, 71, 2)))
        cm, pm = SC['crowd_man_a_wring_wig']; C.card('actor_q_b', (cm, dict(pm, t=g / 30.0 + 0.5)), (0.5, 27.2, 0.0), cl)
        heads['hanway'] = (pos.x, pos.y, pos.z + 3.5)
    return heads

def frame_setup(g):
    loc, look, lens = cam_for(g)
    C.set_cam(loc, look, lens)
    bpy.context.scene.frame_set(g)
    bpy.context.view_layer.update()
    return C.cam_loc()

def parse(spec):
    p = spec.split(':'); a = int(p[0]); b = int(p[1]) if len(p) > 1 and p[1] else a; st = int(p[2]) if len(p) > 2 else 1
    return list(range(a, b + 1, st))

def main():
    cmd = sys.argv[1]
    if cmd == 'stills':
        gs = parse(sys.argv[2]); out = sys.argv[3]; os.makedirs(out, exist_ok=True); q = 'preview'
        if len(sys.argv) > 4: os.environ['SAMPLES'] = sys.argv[4]
    else:
        gs = parse(sys.argv[2]); out = os.path.join(HERE, 'frames'); os.makedirs(out, exist_ok=True); q = 'final'
        if len(sys.argv) > 3: os.environ['SAMPLES'] = sys.argv[3]
    build_set(q)
    log = []
    for g in gs:
        t0 = time.time(); cl = frame_setup(g); heads = build_cards(g, cl)
        cam = bpy.context.scene.camera; hy = {}
        for nm, p in heads.items():
            hz = {'box_a': 3.19, 'hanway': 3.5}.get(nm, 3.2); px = S.project_px(cam, (p[0], p[1], p[2] + hz)); hy[nm] = round(px[1])
        bpy.context.view_layer.update()
        S.render(os.path.join(out, 'g_%04d.png' % g))
        print('g%d shot %d %.1fs heads %s' % (g, shot_of(g), time.time() - t0, hy), flush=True)
        log.append(dict(g=g, heads=hy))
        bpy.ops.outliner.orphans_purge(do_recursive=True) if False else None
    json.dump(log, open(os.path.join(HERE, 'log_%d_%d.json' % (gs[0], gs[-1])), 'w'))

if __name__ == '__main__':
    main()
