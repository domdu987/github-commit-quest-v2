#!/usr/bin/env python3
"""s02 (film 22): BIGZOOM 1 part A, london DUSK. Through Beck's window glass, crane up and back to EXTREME WIDE over London (HQ, roundel, river, dome, clock tower,
Beck at his lit window < 5 % of frame), dive to the glowing pavement grate. Film frames 107-191 (n 85), handles 6.
Run:  python3 shot.py [--draft] [--frames a:b] [--step n] [--part k/n]"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, bpy, V = C.B, C.bpy, C.V
import beck_london as L

F0, F1, HANDLES = 107, 192, 6
# camera (frame_local, loc, look_at, lens). 0..9 = the s01 join (unchanged); wide key 46; end key 1.5 D higher over the grate (join J2 with s03).
CAM = [(0, (-30.5, -5.6, 10.4), (-30.5, 10.0, 10.4), 30), (9, (-30.5, -2.9, 10.6), (-29.5, 12.0, 12.0), 28),
       (19, (-31.0, 1.5, 24.0), (-27.0, 15.0, 5.0), 27), (28, (-29.0, -5.0, 44.0), (-14.0, 36.0, 6.0), 25),
       (38, (-19.0, -43.0, 70.0), (-4.0, 44.0, 0.0), 22), (48, (-12.0, -53.0, 80.0), (-3.0, 44.0, 0.0), 22),
       (62, (-4.0, -32.0, 62.0), (6.0, 22.0, 0.0), 24), (74, (7.5, 0.0, 26.0), (8.0, 19.0, 0.0), 27), (80, (8.0, 15.0, 11.0), (8.0, 19.0, 0.0), 28), (84, (8.0, 18.7, 7.5), (8.0, 19.0, 0.0), 28)]
B.ALL_SHOTS['s02']['cam'] = CAM

# walking crowd streaming into the station entrance (cast22 crowd_member cards, warm rim, contact shadows)
ENT = (-33.0, 19.0)
rs = __import__('random').Random(22)
SPECS = []
for n in range(18):
    row = rs.choice([18.2, 19.4, 20.6, 21.8]); x0 = rs.uniform(-30, 6) if n < 12 else rs.uniform(-26, -16)
    if n < 12: p0, p1 = (x0, row), (ENT[0] + rs.uniform(-1.5, 2.0), row + rs.uniform(-0.6, 0.6))           # along the far pavement, toward the entrance
    else: p0, p1 = (x0, rs.uniform(1.5, 9.0)), (ENT[0] + rs.uniform(0, 3), 16.0)                          # crossing the road toward the pavement
    SPECS.append(dict(i=n * 5 + 1, p0=p0, p1=p1, speed=rs.uniform(4.0, 5.2), t0=-rs.randint(0, 40), stride=rs.uniform(2.9, 3.4)))
for n in range(7):                                                      # people crossing / walking along the road in front of the rising camera (k 8-30)
    d = 1 if n % 2 else -1; y_ = rs.uniform(1.5, 9.5); x_ = rs.uniform(-44, -14)
    SPECS.append(dict(i=n * 11 + 7, p0=(x_, y_), p1=(x_ + d * 40, y_ + rs.uniform(-1, 1)), speed=rs.uniform(4.2, 5.2), t0=107 - rs.randint(0, 40), stride=3.1, loop=True))
BOXES = [(-62, -6, -9, 24)]                     # static flat crowd cards hidden here (about 25 D around the camera path / entrance)

W = {}
def setup(scene):
    E, C_ = B.STATE['E'], B.STATE['C']
    # (1) bus roof: flat red (no streaks)
    flat = C_('#c8201e', 1.0, 1.0, form=False, smix=0.0)
    for nm in ('bus',):
        o = bpy.data.objects.get(nm)
        if o:
            for i, sl in enumerate(o.material_slots):
                if sl.material and sl.material.name.startswith('BK_c_c8201e'): sl.material = flat
    # (2) grate: hide the flat orange plate, build a real warm shaft below the bars (walls graded dark->warm, floor with lamps), dim the glow ~30 %
    for nm in ('grate_under',):
        o = bpy.data.objects.get(nm)
        if o: o.hide_render = True
    gx, gy, hx, hy = 8.0, 19.0, 4.0, 3.5; DEPTH = 8.0; nb = 8
    C.ground_with_hole((gx - hx - 0.4, gx + hx + 0.4, gy - hy - 0.4, gy + hy + 0.4))
    sh_ = B.Part('shaft_bands', ink=False, shadow=False)
    for i in range(nb):
        z1 = -0.3 - i * DEPTH / nb; z0 = z1 - DEPTH / nb; t = i / (nb - 1.0)
        col = '#%02x%02x%02x' % (int(255 * (1.0 - 0.35 * t)), int(255 * (0.62 - 0.22 * t)), int(255 * (0.22 - 0.06 * t)))
        sh_.mb.box((gx - hx - 0.01, gy - hy - 0.01, z0), (gx + hx + 0.01, gy + hy + 0.01, z1), E('shb%d' % i, color=col, k=1.25), skip='top,bottom')
    sh_.mb.box((gx - hx, gy - hy, -DEPTH - 0.3), (gx + hx, gy + hy, -DEPTH - 0.2), E('shfloor', color='#ffb25a', k=1.1)); sh_.done()
    # brickwork: dark mortar courses on the shaft walls (every 0.28 D, running-bond joints every 0.9 D) and a floor tile grid (every 0.4 D) -> real surface detail at close range
    mo = B.Part('shaft_mortar', ink=False, shadow=False); dk = E('shmort', color='#3a1006', k=1.0); w_ = 0.07; zf = -DEPTH - 0.18
    nC = int(DEPTH / 0.19)
    for i in range(nC):
        z = -0.3 - i * 0.19 - 0.12
        mo.mb.box((gx - hx - 0.02, gy - hy - 0.02, z), (gx + hx + 0.02, gy - hy + 0.0, z + w_), dk); mo.mb.box((gx - hx - 0.02, gy + hy, z), (gx + hx + 0.02, gy + hy + 0.02, z + w_), dk)
        mo.mb.box((gx - hx - 0.02, gy - hy, z), (gx - hx, gy + hy, z + w_), dk); mo.mb.box((gx + hx, gy - hy, z), (gx + hx + 0.02, gy + hy, z + w_), dk)
        off = 0.3 * (i % 2)
        for j in range(int(2 * hx / 0.6) + 1):
            xx = gx - hx + off + j * 0.6
            if gx - hx < xx < gx + hx:
                mo.mb.box((xx - 0.035, gy - hy - 0.02, z + w_), (xx + 0.035, gy - hy, z + 0.19), dk); mo.mb.box((xx - 0.035, gy + hy, z + w_), (xx + 0.035, gy + hy + 0.02, z + 0.19), dk)
        for j in range(int(2 * hy / 0.6) + 1):
            yy = gy - hy + off + j * 0.6
            if gy - hy < yy < gy + hy:
                mo.mb.box((gx - hx - 0.02, yy - 0.035, z + w_), (gx - hx, yy + 0.035, z + 0.19), dk); mo.mb.box((gx + hx, yy - 0.035, z + w_), (gx + hx + 0.02, yy + 0.035, z + 0.19), dk)
    for i in range(int(2 * hx / 0.26) + 1): xx = gx - hx + i * 0.26; mo.mb.box((xx - 0.035, gy - hy, zf), (xx + 0.035, gy + hy, zf + 0.04), dk)
    for i in range(int(2 * hy / 0.26) + 1): yy = gy - hy + i * 0.26; mo.mb.box((gx - hx, yy - 0.035, zf), (gx + hx, yy + 0.035, zf + 0.04), dk)
    mo.done()
    lamps_ = B.Part('shaft_lamps', ink=False, shadow=False)
    for (lx_, ly_) in ((gx - 2.4, gy - 1.6), (gx + 2.4, gy - 1.6), (gx - 2.4, gy + 1.6), (gx + 2.4, gy + 1.6), (gx, gy)): B.halo_card(lamps_.mb, (lx_, ly_, -DEPTH + 0.2), 1.2, E('shl', 'halo_white', k=0.9, additive=True))
    lamps_.done()
    for nm in ('grate_glow',):
        o = bpy.data.objects.get(nm)
        if o:
            for sl in o.material_slots:
                m = sl.material
                if m and m.use_nodes:
                    for nd in m.node_tree.nodes:
                        if 'Strength' in nd.inputs: nd.inputs['Strength'].default_value *= 0.7
    gl = bpy.data.objects.get('grate_up')
    if gl: gl.data.energy *= 0.7
    # (3) Beck at his lit lodgings window (back wall seen from the wide key): bright window + cast22 Beck card, rim-lit
    TX = B.STATE['TX']
    bk = B.Part('lodge_back', ink=True); bk.mb.pid += 1
    bk.mb.quad((-34.0, -16.0, 0.0), (14.0, 0, 0), (0, 0, 25.0), TX('brick', 1.0, 1.0), (0, 0, 1, 1)); bk.done((-27, -16, 12))
    bw = B.Part('beck_win', ink=False, shadow=False); y = -16.07
    B.plane(bw.mb, (-33.0, y, 8.0), (5.0, 0, 0), (0, 0, 5.0), E('bwin', color='#ffd070', k=2.0), (0, 0, 1, 1)); bw.done()
    sill = B.Part('beck_sill', ink=True); sill.mb.box((-33.4, -16.5, 7.6), (-27.6, -15.9, 8.4), C_('#3a3070')); sill.done((-30.5, -16.2, 8))
    W['beck'] = B.cast_card('beck_hold_circuit', (-30.5, -16.45, 8.2), yaw_deg=0, tilt=0, scale=1.25, rim='#ffb070', shadow=False, pose=dict(desk=0))
    C.fill_foreground()
    # (4) walking crowd
    W['wk'] = C.Walkers(SPECS, scale=1.45)

def sstep(a, b, x): u = max(0.0, min(1.0, (x - a) / float(b - a))); return u * u * (3 - 2 * u)
def frame(g, k, n):
    bpy.context.scene.camera.data.shift_y = -0.10 * sstep(20, 38, k) * (1 - sstep(56, 74, k))      # crop the bare ground in the extreme wide, back to centre for the grate
    hg = bpy.data.objects.get('beck_window_glow')
    if hg: hg.hide_render = 6 <= k <= 24
    cam = B.STATE['cam']
    W['wk'].update(g, cam, hide=lambda x, y, g_: k >= 66 and math.hypot(x - 8.0, y - 19.0) < 15.0)

if __name__ == '__main__':
    unp = C.hide_static_crowd(BOXES)
    C.run('s02', 'london', 'DUSK', F0, F1, (HANDLES, 5), setup, frame, segments=[(-10**6, 0), (70, 82)])
