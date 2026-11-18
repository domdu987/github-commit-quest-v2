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

CAM17 = dict(loc=(-2.6, 6.0, 1.7), look_at=(4.6, 26.0, 4.4), loc_b=(-2.0, 9.0, 1.9), look_b=(4.7, 28.0, 4.5), lens=22.0)
CAM15 = dict(loc=(-0.6, 11.4, 3.4), look_at=(3.5, 18.7, 6.0), loc_b=(1.9, 14.4, 4.9), look_b=(3.55, 18.6, 6.1), lens=25.0)
CAM16 = dict(loc=(-1.8, 8.5, 2.7), look_at=(2.3, 22.0, 4.7), loc_b=(-1.0, 12.5, 2.9), look_b=(4.4, 28.0, 5.0), lens=22.0)

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
SEAT_DZ = -0.9; PASS_X, PASS_Z = 1.95, 1.9
BOX_A = (3.55, 18.6, 4.22); BOX_B = (3.55, 35.1, 4.22); BOX_C = (3.55, 51.6, 4.22)
ROLL = (SH[17][0] - 2, SH[17][1] + H + 2)                # coaches pull away
ROLL_DY = {0: -4.0, 1: -9.0, 2: -9.0, 3: -9.0}
HAN_A, HAN_C = Vector((-2.5, 7.0, 0.0)), Vector((-2.5, 17.0, 0.0))
RUSH_MEM = ['crowd_man_a', 'crowd_man_b', 'crowd_man_c', 'crowd_man_d', 'crowd_woman_a', 'crowd_woman_b']
RUSH_PICK = list(range(24))   # which of the 24 anchors get a card (16 shot)

BUSY_KEYS = [(G0, 0.02), (SH[16][0] + 18, 0.02), (SH[16][0] + 22, 0.1), (SH[16][0] + 38, 0.3), (SH[16][0] + 52, 0.55), (SH[16][0] + 68, 0.8), (SH[16][0] + 83, 1.0), (G1, 1.0)]
def busy_of(g):
    for (f0, v0), (f1, v1) in zip(BUSY_KEYS, BUSY_KEYS[1:]):
        if f0 <= g <= f1: return lerp(v0, v1, (g - f0) / float(f1 - f0))
    return BUSY_KEYS[-1][1]
COACH_Y0 = [22.0, 38.5, 55.0, 71.5]
PASS = [('passenger_a_seated', -1.5), ('passenger_b_laugh', 0.2), ('passenger_a_laugh', 1.9)]    # (pose, y offset from the coach origin)

def coach_dy(i, g):
    r0, r1 = ROLL; u = clamp((g - r0) / float(r1 - r0))
    return ROLL_DY[i] * (u if g < r1 else 1.0) * (0.35 + 0.65 * u if False else 1.0)

def box_pos(base, i, g):
    return (base[0], base[1] + coach_dy(i, g), base[2])

def build_set(quality):
    S.shot('rank_rush', 'RAIN', u=0.5, placeholders=False, figures=False, quality=quality)
    sc = bpy.context.scene
    S.crowd_figures(False)
    RAIN_K = 1.0                                        # rain intensity multiplier probe: the hook accepts >1 (more streaks)?
    S.rain(0.70, frame=G0); S.rain(1.4, frame=SH[15][0] + 52); S.rain(1.5, frame=SH[16][0] + 10); S.rain(1.5, frame=G1)
    for f, v in BUSY_KEYS: S.set_rank_busy(v, frame=f)
    for i in range(4):                                  # the set's black pin silhouettes are replaced by passenger cards
        o = bpy.data.objects.get('coach_%d_pass' % i)
        if o: o.hide_render = True
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

def shadow_disc(name, x, y, r=1.1, a=0.55):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-r, -r, 0.03), (r, -r, 0.03), (r, r, 0.03), (-r, r, 0.03)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    m = bpy.data.materials.new(name + '_m'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Location'].default_value = (-0.5, -0.5, 0); mp.inputs['Scale'].default_value = (2, 2, 2)
    gr = N('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'; mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = a
    tr = N('ShaderNodeBsdfTransparent'); df = N('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (0.03, 0.025, 0.06, 1); mx = N('ShaderNodeMixShader'); out = N('ShaderNodeOutputMaterial')
    L(tc.outputs['UV'], mp.inputs['Vector']); L(mp.outputs['Vector'], gr.inputs['Vector']); L(gr.outputs['Fac'], mu.inputs[0]); L(mu.outputs['Value'], mx.inputs['Fac'])
    L(tr.outputs['BSDF'], mx.inputs[1]); L(df.outputs['BSDF'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = (x, y, 0.0)
    ob.visible_glossy = False; ob.visible_shadow = False; S.no_bounce(ob)
    C._cards.append(ob); return ob

def build_cards(g, cl):
    C.drop_cards(); k = shot_of(g); heads = {}
    # --- the head coachman: SEATED on the plank (box twin, no drawn box), same card in all four shots
    pa = box_pos(BOX_A, 0, g)
    ov = dict(coach_box=0)
    if k == 15 and g < G_SKY:
        pose = 'coachman_box_count_coins'; ov['purse_open'] = 0.6 + 0.4 * math.sin(g * 1.3) ** 2
    elif k == 15 or (k == 16 and g < G_COIN2 - 4):
        pose = 'coachman_box_count_coins_sky'; ov['purse_open'] = 0.7 + 0.3 * math.sin(g * 1.3) ** 2
    elif k == 16:
        pose = 'coachman_box_count_coins'; ov['purse_open'] = 0.5 + 0.5 * math.sin(g * 1.6) ** 2
    elif k == 17:
        pose = 'coachman_box_gloat'
    else:
        pose = 'coachman_box_gloat' if g < G_DROP else 'coachman_box_grin_drop'
    shake = 0.05 * math.sin(g * 1.9) if (k == 15 or (k == 16 and G_COIN2 - 6 <= g <= G_COIN2 + 14)) else 0.0
    bob = 0.04 * math.sin(g * 0.55) if k in (15, 16) else 0.0
    ov.update(blink=cast12.blink_at(g, 83, 11), t=g / 30.0)
    C.card('actor_box_a', SC[pose], (pa[0] + shake, pa[1], pa[2] + SEAT_DZ + bob), cl, over=ov, mirror=True)
    heads['box_a'] = (pa[0], pa[1], pa[2] + SEAT_DZ)
    if k in (16, 17):
        pb = box_pos(BOX_B, 1, g)
        C.card('actor_box_b', SC['coachman_b_box_laugh' if k == 17 else 'coachman_b_box_nod'], (pb[0], pb[1], pb[2] + SEAT_DZ + 0.04 * math.sin(g * 0.6 + 1)), cl, over=dict(coach_box=0), mirror=True)
    if k == 17:
        pc = box_pos(BOX_C, 2, g)
        C.card('actor_box_c', SC['coachman_c_box_nod'], (pc[0], pc[1], pc[2] + SEAT_DZ), cl, over=dict(coach_box=0), mirror=True)
    # --- passengers in the windows of every full coach (parented by construction: same y key as the coach)
    if k in (16, 17, 18):
        bz = busy_of(g)
        for i in range(4):
            if bz > i / 4.0 + 0.001 or (k == 17 and True):
                if k == 16 and not (bz > i / 4.0 + 0.001): continue
                for q, (pn, dyo) in enumerate(PASS):
                    cpos = (PASS_X, COACH_Y0[i] + dyo + coach_dy(i, g), PASS_Z)
                    C.card('actor_pass_%d_%d' % (i, q), SC[pn], cpos, cl, over=dict(blink=cast12.blink_at(g + 13 * q, 90, 5)), mirror=(q % 2 == 1))
    # --- the rush (shot 16)
    if k == 16:
        kk = lerp(0.35, 1.0, clamp((g - RUSH0) / float(RUSH1 - RUSH0)))
        for n, j in enumerate(RUSH_PICK):
            r = S.STATE['rush_slots'][j]; d = r['delay']; e = clamp((kk - d) / (1 - d))
            p0, p1 = Vector(r['start']), Vector(r['end']); pos = p0 + (p1 - p0) * (e * (2 - e) if e < 1 else 1.0); pos = Vector((pos.x + 0.45 * math.sin(j * 2.1) * (1 - e * 0.5), pos.y, 0.0))
            m = RUSH_MEM[j % 6]
            if e >= 0.97:
                c_, pz = SC[m + '_push']; pos = Vector((pos.x + 0.07 * math.sin(g * 0.9 + j), pos.y + 0.12 * math.sin(g * 0.7 + 2 * j), 0.0))
                C.card('actor_rush_%02d' % n, (c_, dict(pz, t=g / 30.0)), pos, cl)
            else:
                C.card('actor_rush_%02d' % n, cast12.cycle_frame(m + '_rush', (g * 1.0 / 16.0 + j * 0.13) % 1.0, facing=1), (pos.x, pos.y, 0.0), cl)
    # --- shot 17: leftover runners chase the coaches, one hand up with coins
    if k == 17:
        for n, (m, x0, y0) in enumerate((('crowd_man_a', -1.2, 21.0), ('crowd_woman_a', -0.2, 24.5), ('crowd_man_d', -2.2, 19.0), ('crowd_man_c', 0.5, 28.0))):
            u = (g - SH[17][0]) / 72.0; pos = (x0 + 0.5 * math.sin(n), y0 - 5.0 * u, 0.0)
            C.card('actor_run_%d' % n, cast12.cycle_frame(m + '_rush', (g / 16.0 + n * 0.21) % 1.0, facing=-1), pos, cl, mirror=False)
    # --- shot 18: hanway strolls dry, a soaked queue waits at the coach
    if k == 18:
        a, b = SH[18]; x = clamp((g - a) / float(b - a + 1))
        pos = HAN_A.lerp(HAN_C, x)
        c_, p_ = cast12.cycle_frame('hanway_walk_umbrella', (g / 28.0) % 1.0, facing=1)
        p_ = dict(p_, expr='smug', mouth='smirk', head_roll=-3.0, pitch=-0.35, blink=cast12.blink_at(g, 97, 4))
        shadow_disc('hshadow', pos.x, pos.y)
        C.card('actor_hanway', (c_, p_), (pos.x, pos.y, 0.0), cl, rim='#f2b25c')
        cyd = coach_dy(0, g)
        Q = [('crowd_man_c_wring_wig', 0.5, 15.6), ('crowd_woman_b_dry_pass', 1.1, 18.2), ('crowd_man_a_wring_wig', 0.4, 21.0), ('crowd_man_b_push', 1.0, 23.6),
             ('crowd_man_d_wring_wig', 0.3, 26.2), ('crowd_woman_a_push', 0.9, 28.6)]
        for n, (pn, qx, qy) in enumerate(Q):
            cm, pm = SC[pn]; C.card('actor_q_%d' % n, (cm, dict(pm, t=g / 30.0 + 0.3 * n)), (qx, qy + cyd - ROLL_DY[0] + (-0.0), 0.0), cl, over=dict(blink=cast12.blink_at(g, 71, 2 * n)))
        heads['hanway'] = (pos.x, pos.y, 3.5)
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
        if cmd == 'final' and os.path.exists(os.path.join(out, 'g_%04d.png' % g)): continue
        t0 = time.time(); cl = frame_setup(g); heads = build_cards(g, cl)
        cam = bpy.context.scene.camera; hy = {}
        for nm, p in heads.items():
            hz = {'box_a': 2.3, 'hanway': 0.0}.get(nm, 3.2); px = S.project_px(cam, (p[0], p[1], p[2] + hz)); hy[nm] = round(px[1])
        bpy.context.view_layer.update()
        S.render(os.path.join(out, 'g_%04d.png' % g))
        print('g%d shot %d %.1fs heads %s' % (g, shot_of(g), time.time() - t0, hy), flush=True)
        log.append(dict(g=g, heads=hy))
        bpy.ops.outliner.orphans_purge(do_recursive=True) if False else None
    if log: json.dump(log, open(os.path.join(HERE, 'work_log_%d_%d.json' % (gs[0], gs[-1])), 'w'))

if __name__ == '__main__':
    main()
