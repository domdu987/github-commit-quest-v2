#!/usr/bin/env python3
"""shot.py -- film 22 take s03 (team 4): BIGZOOM 1 part B.  Through the grate (the s02 grille), down the shaft, the noodle-tunnel knot seen
from OUTSIDE the tubes, down the straight tunnel, out onto the platform, MEDIUM on old_gent squinting at the OLD map (9.3 s), pass_man bumps
him (9.81 s), push into the OLD map centre (grey-lavender tint, title uncut) for the match dissolve to s04.
    python3 shot.py stills 192,215 outdir | draft a:b:step | final a:b [samples]
Frames g 192..323 (local 0..131) + handles 186..191 and 324..329."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import V, lerp, clamp, ez
import numpy as np
beck, U, BU, bpy = C.beck, C.U, C.BU, C.bpy
GX, GY = BU.GX, BU.GY
O = BU.ORG_HALL
def hl(x, y, z): return (O[0] + x, O[1] + y, O[2] + z)

# ------------------------------------------------------------------ camera (local frames; g = 192 + local)
kn = (GX, GY + 38, -46.0)
CAM = [(0, (GX, GY - 0.3, 6.0), (GX, GY + 3.7, -66.0), 30),
       (4, (GX + 0.57, GY - 0.9, 2.0), (GX + 0.57, GY + 3.1, -70.0), 30),
       (16, (GX + 0.57, GY - 0.9, -10.0), (GX + 0.57, GY + 3.1, -80.0), 29),
       (30, (GX, GY - 1.5, -26.5), (GX, GY + 12, -42.0), 25),
       (38, (GX - 6.0, GY - 6.0, -31.0), (GX, GY + 38, -47.0), 22),
       (47, (GX - 12.0, GY - 8.0, -36.0), (GX + 3, GY + 42, -49.0), 22),
       (54, (GX - 4.0, GY + 2.0, -52.0), (GX, GY - 20, -59.6), 24),
       (60, (GX, GY + 12.0, -59.0), (GX, GY - 20, -59.6), 24),
       (70, (GX, GY - 8.0, -59.6), (GX, GY - 30, -59.6), 24),
       (72, hl(0.3, 43.0, 2.6), hl(-3.0, 28.0, 2.9), 24),
       (80, hl(-1.0, 32.0, 3.6), hl(-9.0, 18.0, 3.4), 26),
       (88, hl(-2.4, 24.0, 3.5), hl(-10.5, 15.8, 3.0), 28),
       (96, hl(-3.2, 18.8, 3.3), hl(-11.0, 15.0, 2.9), 28),
       (110, hl(-3.5, 16.6, 3.3), hl(-11.5, 15.4, 2.9), 29),
       (131, hl(-4.2, 16.0, 3.4), hl(-12.0, 15.9, 3.0), 32)]
G0, G1 = 192, 324
OLD_X, OLD_Y = -10.5, 14.4

def hook():
    C.mount(['ribs', 'globes', 'hang_signs', 'clock', 'clock_face', 'liner', 'way_out', 'old_map', 'old_map_img', 'posters', 'name_panels', 'roundel_name', 'columns'])
    C.mount(['tunnel_lamps', 'globe_halos', 'light_pools', 'headlights', 's03_lamps', 'noodle_trains', 'noodles', 'tube'], airborne=True)
    ob = bpy.data.objects.get('machine')
    if ob: ob.hide_render = True    # vending machine on the left wall is never in frame in this take
    # --- J2: the s02 grille (7 bars, 3 cross bars, frame, rivets) replaces the old pill-tile plate; warm plane + lamps only for the first frames
    for n in ('grate', 'grate_beams', 'street_glow', 'shaft_ribs'):
        ob = bpy.data.objects.get(n)
        if ob: ob.hide_render = True
    C_, TX, E, CARD = BU._cs(); B = beck
    hx, hy = BU.GRATE_SIZE[0] / 2, BU.GRATE_SIZE[1] / 2
    gr = B.Part('grate_s02', (GX, GY, 0.1), ink=True); mb = gr.mb; iron = C_('#26204e', 0.5, 1.0)
    for k in range(7): xx = GX - hx + (k + 0.5) * (2 * hx / 7); mb.box((xx - 0.14, GY - hy, -0.05), (xx + 0.14, GY + hy, 0.3), iron)
    for yy in (GY - hy + 0.2, GY, GY + hy - 0.2): mb.box((GX - hx, yy - 0.18, -0.05), (GX + hx, yy + 0.18, 0.3), iron)
    fr_ = C_('#3a3070')
    mb.box((GX - hx - 0.4, GY - hy - 0.4, -0.2), (GX + hx + 0.4, GY - hy, 0.35), fr_); mb.box((GX - hx - 0.4, GY + hy, -0.2), (GX + hx + 0.4, GY + hy + 0.4, 0.35), fr_)
    mb.box((GX - hx - 0.4, GY - hy, -0.2), (GX - hx, GY + hy, 0.35), fr_); mb.box((GX + hx, GY - hy, -0.2), (GX + hx + 0.4, GY + hy, 0.35), fr_)
    for k in range(7):
        for yy in (GY - hy + 0.2, GY, GY + hy - 0.2): xx = GX - hx + (k + 0.5) * (2 * hx / 7); mb.sphere((xx, yy, 0.32), 0.11, C_('#8a90c8', 1.2, 1.4), seg=6, rings=4)
    gr.done((GX, GY, 0.1), px=3)
    gu = B.Part('grate_under_s02', ink=False, shadow=False)
    B.plane(gu.mb, (GX - hx, GY - hy, 0.12), (2 * hx, 0, 0), (0, 2 * hy, 0), E('gu', color='#ff9a3a', k=0.6), (0, 0, 1, 1))
    for (lx_, ly_) in ((GX - 2.4, GY - 1.6), (GX + 2.4, GY - 1.6), (GX - 2.4, GY + 1.6), (GX + 2.4, GY + 1.6), (GX, GY)): B.halo_card(gu.mb, (lx_, ly_, 0.25), 1.1, E('gl', 'halo_white', k=0.7, additive=True))
    C.GU = gu.done()
    # --- noodle / tunnel lamps: the fan-shaped halo quads go; round glow spheres on the signal posts and a lamp string in the straight tube instead
    for n in ('tube_lamps', 'signal_lamps', 'tunnel_lamps'):
        ob = bpy.data.objects.get(n)
        if ob: ob.hide_render = True
    tl = B.Part('s03_lamps', ink=False, shadow=False); mb = tl.mb
    lamp = E('s03lamp', color='#ffd890', k=2.2)
    for k, yy in enumerate(np.arange(GY - 4.0, GY + 52.0, 3.5)):
        for sx in (-2.7, 2.7): mb.sphere((GX + sx, yy, -62.0 + 4.6), 0.3, lamp, seg=8, rings=6)
    for ci, (col, pts) in enumerate(BU.noodle_curves()):
        path = BU.catmull(pts, 8)
        for frac in (0.1, 0.4, 0.65, 0.9):
            p = path[int(frac * (len(path) - 1))]; mb.sphere(p + V((0, 0, 2.3)), 0.45, E('s03sig%d' % ((ci + int(frac * 10)) % 3), color=['#ff7a3a', '#ffd060', '#7affc0'][(ci + int(frac * 10)) % 3], k=1.8), seg=8, rings=6)
    tl.done()
    # --- OLD map: down 1.2 D (the vault no longer cuts it), grey-lavender tone like s04's lodgings map
    for n in ('old_map', 'old_map_img'):
        ob = bpy.data.objects[n]; ob.location = (ob.location[0], ob.location[1], ob.location[2] - 1.2)
    from PIL import Image
    src = beck.STATE['tx']['old_map']; os.makedirs(os.path.join(HERE, 'work'), exist_ok=True); tp = os.path.join(HERE, 'work', 'old_map_lav.png')
    if not os.path.exists(tp):
        a = np.asarray(Image.open(src).convert('RGB'), 'float32') / 255.0
        a = a * np.array([0.74, 0.87, 1.12], 'float32'); a = np.clip(a, 0, 1)
        Image.fromarray((a * 255).astype('uint8')).save(tp)
    m = bpy.data.materials['BK_oldmap_lodg']
    for nd in m.node_tree.nodes:
        if nd.bl_idname == 'ShaderNodeTexImage': nd.image = bpy.data.images.load(tp, check_existing=True)
    # --- platform people: clear the near platform around the camera path, restage the named trio at the old map
    C.hide_cards(lambda x, y, z: z > -70 and x < O[0] - 1.0 and (O[1] + 8) < y < (O[1] + 30) and x > O[0] - 9.0 and False)
    for nm in list(U.ACTORS):
        x, y, z = U.ACTORS[nm]['mark']
        if nm.startswith('np') and (O[1] + 8.0) < y < (O[1] + 34.0): C.hide_actor(nm)
    for nm in ('old_gent', 'pass_man', 'pass_woman', 'porter'): C.hide_actor(nm)
    C.W = [C.Walker('w1', 3, '#ffb878', mirror=False), C.Walker('w2', 9, '#a8bcff', mirror=True), C.Walker('w3', 6, '#ffb878', mirror=False)]
    C.OG = C.Idle('og', 'old_squint', hl(OLD_X, OLD_Y, 0), '#ffb878', period=34, n=8, lean=2.5, roll=2.0, pitch=0.04)
    C.PM = C.Idle('pm', 'pass_squint', hl(OLD_X - 0.3, OLD_Y + 1.9, 0), '#a8bcff', period=30, n=8, lean=2.0, roll=2.0, alt='pass_bump', phase=0.3, mirror=True)
    C.PW = C.Idle('pw', 'pass_unfold_map', hl(-9.6, OLD_Y + 5.0, 0), '#a8bcff', period=44, n=8, lean=1.5, roll=2.5, phase=0.6)

def anim(f, n):
    U.face_cards()
    gu = getattr(C, 'GU', None)
    if gu is not None: gu.hide_render = f > 3
    W = getattr(C, 'W', None)
    if W:
        W[0].at(O[0] - 9.3, O[1] + 38.0 - 1.4 * f / 30.0, O[2], f * 1.4 / 30.0 / 2.2)
        W[1].at(O[0] - 8.9, O[1] + 28.0 + 1.4 * f / 30.0, O[2], f * 1.4 / 30.0 / 2.2)
        W[2].at(O[0] - 6.0, O[1] + 29.0, O[2], 0.0); W[2].hide()
    for nm in ('OG', 'PM', 'PW'):
        o = getattr(C, nm, None)
        if o is not None: o.update(f, alt=(f >= 103) if nm == 'PM' else False)

C.smooth_cam(CAM, G1 - G0, sigma=3.0)
CFG = dict(f0=G0, f1=G1, cam=CAM, animate={'a': anim}, state={})
if __name__ == '__main__':
    C.run('s03', CFG, sys.argv[1:], hook_after_build=hook)
