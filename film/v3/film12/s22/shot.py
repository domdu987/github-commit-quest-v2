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
CUSTOM22 = (dict(loc=(-3.6, -3.0, 2.5), look_at=(3.8, 34.0, 4.9), lens=32.0), dict(loc=(-3.2, 2.5, 2.5), look_at=(4.2, 34.0, 5.0), lens=32.0))
CUSTOM23 = (dict(loc=(-2.4, 8.5, 3.6), look_at=(4.4, 21.5, 6.9), lens=24.0), dict(loc=(-1.2, 10.6, 3.9), look_at=(4.4, 21.0, 7.1), lens=24.0))
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
        S.make_camera((CUSTOM22 if shot == 22 else CUSTOM23)[int(u)]); cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g)
    ad = cam.animation_data
    for fc in ad.action.layers[0].strips[0].channelbags[0].fcurves if hasattr(ad.action, 'layers') else ad.action.fcurves:
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    cards = []
    if shot == 22:
        S.set_rank_busy(0.0)
        cards = S.stage_cards([('box_a', 'coachman_sulk', S.STAND['box_a']['pos'], None), ('box_b', 'cb_glare', S.STAND['box_b']['pos'], None), ('box_c', 'cc_glare', S.STAND['box_c']['pos'], None)])
    else:
        S.set_rank_busy(0.0)
        cards = [held_card(S, bpy, S.STAND['box_a']['pos'])]
        S.set_pink_umbrella(1.0)
        place_pole(S, bpy, cards[0])
        slate_lamps(bpy)
    S.rain(1.0)
    bpy.context.view_layer.update()
    return S, bpy, A, cards, cam

CLIPY = -0.72                # the sprite pole is kept from the fist up to this y (above the hat); the 3D pink umbrella continues it

def held_card(S, bpy, pos):
    """The sulking coachman WITH his own fist gripping the pole (sprite prop kept), but the sprite canopy clipped away: the 3D pink umbrella carries on from the pole."""
    for p in (PROJ + '/v3/cast12', PROJ + '/v3/cast10'):
        if p not in sys.path: sys.path.insert(0, p)
    import cast12, puppet
    orig = puppet.figure; store = {}
    def fig(cast, pose, name):
        clip = pose.get('_clipy')
        if clip is not None: pose = {k: v for k, v in pose.items() if k != '_clipy'}
        f = orig(cast, pose, name)
        if clip is not None:
            f = dict(f); f['svg'] = '<defs><clipPath id="cpy"><rect x="-50" y="%.4f" width="100" height="100"/><rect x="-0.62" y="-0.77" width="0.92" height="1"/></clipPath></defs><g clip-path="url(#cpy)">%s</g>' % (clip, f['svg'])
            store['an'] = f['anchors']; store['fy'] = f['feet_y']
        return f
    puppet.figure = fig
    try:
        cast, pose = cast12.STORY12['coachman_sulk_standing']
        cl = bpy.context.scene.camera.matrix_world.translation
        c = S.cast_card('actor_box_a', cast, pose, pos, cl, mirror=True, over=dict(_clipy=CLIPY))
    finally:
        puppet.figure = orig
    an = store['an']; fx = an['feet'][0]
    (hx, hy), (mx, my) = an['hand_l'], an['umb_mid_l']
    px = hx + (mx - hx) * (hy - CLIPY) / (hy - my)
    c['pole_local'] = (float(px - fx), float(store['fy'] - CLIPY))
    return c

def place_pole(S, bpy, c):
    bpy.context.view_layer.update()
    px, pz = c['pole_local']
    S.STATE['pink_obj'].location = c.matrix_world @ __import__('mathutils').Vector((px, 0.0, pz))

def slate_lamps(bpy):
    """Unlit coach lanterns: dark slate glass instead of pure black."""
    m = bpy.data.materials.new('slate_lamp'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.07, 0.09, 0.2, 1); b.inputs['Roughness'].default_value = 0.35
    for o in bpy.data.objects:
        if o.name.startswith('coach_') and o.name.endswith('_lamps'): o.hide_render = True      # box lanterns are out on an empty coach (black boxes read as holes)

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
    gs = [g for g in gs if not os.path.exists(os.path.join(out, 'g_%04d.png' % g))]
    for g in gs:
        sc.frame_set(g); breathe(S, bpy, cards, g, shot)
        if shot == 23: place_pole(S, bpy, cards[0])
        bpy.context.view_layer.update()
        heads = {c.name: [round(v) for v in S.project_px(cam, (c.location.x, c.location.y, c.location.z + 3.2))[:2]] for c in cards}
        w, cpu = S.render(os.path.join(out, 'g_%04d.png' % g))
        print('shot %d g %d %.1f s wall heads %s' % (shot, g, w, heads), flush=True)
