#!/usr/bin/env python3
"""shot.py -- film 12 take s22: shots 22 + 23, the ENDING (g 1573..1784; in-handle 1573..1578).
  shot 22 g 1579..1655 (52.64-55.20 s): the empty rank, rank_idle RAIN, set_rank_busy 0, bored coachmen, slow move A -> B.
  shot 23 g 1656..1784 (55.20-59.50 s): box_seat RAIN, the head coachman sulks on his empty coach under the pink lace umbrella, slow push.
One process = one shot (one set build).   usage: python3 shot.py <22|23> <a:b[:step]> <out_dir> [scale] [samples]
Blender frame = g.  Hard cut at the end of the film (last word 58.99 s = g 1770; narration ends, picture runs to 1784)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = '/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj'
sys.path.insert(0, PROJ + '/v3/set3d12')
G0, G_CUT, G1, H_IN = 1579, 1656, 1784, 6
RANGES = {22: (G0 - H_IN, G_CUT - 1), 23: (G_CUT, G1)}
CUSTOM22 = (dict(loc=(-2.6, 0.5, 1.9), look_at=(2.4, 30.0, 3.6), lens=22.0), dict(loc=(-1.0, 7.5, 2.3), look_at=(3.2, 26.0, 4.3), lens=22.0))
CFG = {22: dict(preset='rank_idle', mid=0.5), 23: dict(preset='box_seat', mid=0.5)}

def parse(s):
    p = s.split(':'); a, b = int(p[0]), int(p[1]); st = int(p[2]) if len(p) > 2 else 1
    return list(range(a, b + 1, st))

def build(shot):
    import street as S, bpy
    from mathutils import Vector
    c = CFG[shot]
    S.CAST_ROLE['cb_glare'] = ('story', 'coachman_b_glare'); S.CAST_ROLE['cc_glare'] = ('story', 'coachman_c_glare')
    A = S.shot(c['preset'], 'RAIN', u=c['mid'], placeholders=False, figures=False)   # lights picked near the middle pose
    cam = A['cam']; sc = bpy.context.scene
    r0, r1 = RANGES[shot]
    # camera move A -> B over the whole shot, linear (never static)
    ga, gb = (G0 - H_IN, G_CUT - 1) if shot == 22 else (G_CUT, G1)
    for g, u in ((ga, 0.0), (gb, 1.0)):
        S.make_camera(CUSTOM22[int(u)] if shot == 22 else S.camera_pose(c['preset'], u)); cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g)
    ad = cam.animation_data
    for fc in ad.action.layers[0].strips[0].channelbags[0].fcurves if hasattr(ad.action, 'layers') else ad.action.fcurves:
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    cards = []
    if shot == 22:
        S.set_rank_busy(0.0)
        cards = S.stage_cards([('box_a', 'coachman_sulk', S.STAND['box_a']['pos'], None), ('box_b', 'cb_glare', S.STAND['box_b']['pos'], None), ('box_c', 'cc_glare', S.STAND['box_c']['pos'], None)])
    else:
        S.set_rank_busy(0.0)
        cards = S.stage_cards([('box_a', 'coachman_sulk', S.STAND['box_a']['pos'], None)])
        S.set_pink_umbrella(1.0)
        S.pink_to_hand(cards[0], dx=0.55, up=-0.1)
    S.rain(1.0)
    bpy.context.view_layer.update()
    return S, bpy, A, cards, cam

def breathe(S, bpy, cards, g, shot):
    """tiny sulking sway so the card is never frozen: z-scale breath + 0.6 deg lean."""
    for i, c in enumerate(cards):
        ph = g / 30.0 * 2 * math.pi * 0.28 + i * 1.7
        c.scale = (1.0, 1.0, 1.0 + 0.012 * math.sin(ph))
        c.rotation_euler[1] = math.radians(0.7 * math.sin(ph * 0.5 + i))

if __name__ == '__main__':
    shot = int(sys.argv[1]); gs = [g for g in parse(sys.argv[2]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 20
    os.environ['SAMPLES'] = str(samples)
    S, bpy, A, cards, cam = build(shot); sc = bpy.context.scene
    if scale != 1.0: sc.render.resolution_percentage = int(scale * 100)
    sc.cycles.samples = samples
    os.makedirs(out, exist_ok=True)
    for g in gs:
        sc.frame_set(g); breathe(S, bpy, cards, g, shot)
        if shot == 23: S.pink_to_hand(cards[0], dx=0.55, up=-0.1)
        bpy.context.view_layer.update()
        heads = {c.name: [round(v) for v in S.project_px(cam, (c.location.x, c.location.y, c.location.z + 3.2))[:2]] for c in cards}
        w, cpu = S.render(os.path.join(out, 'g_%04d.png' % g))
        print('shot %d g %d %.1f s wall heads %s' % (shot, g, w, heads), flush=True)
