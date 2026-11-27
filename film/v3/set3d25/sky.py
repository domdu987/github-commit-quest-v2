#!/usr/bin/env python3
"""sky.py : an RFC biplane (BE.2c-like) over the rooftops of Flers (film 25 shot 32).  The plane has its own root empty `plane_root`; set_plane(t, frame) flies it along a straight path (propeller spins,
wheels trail); roundels are plain discs.  Preset: sky_plane.  build(preset) reuses street.street_scene as the Flers rooftops."""
import math, time
from mathutils import Vector
import front as F
import lib25 as L
import street as ST
import tank25 as TK
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, J

def build_plane(name='plane'):
    M = S['M']; root = F.empty(name + '_root'); wing = M['canvas']; fus = M['p_green']; X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    mb = MB(); mf = MB(); mp = MB(); H = dict(root=root)
    for zz, ch, x0 in ((0.0, 3.0, 0.4), (3.4, 3.2, 0.9)):
        obox(mb, (x0, 0, zz), X, Y, Z, ch / 2, 11.5, 0.12, wing); obox(mb, (x0 - ch / 2, 0, zz), X, Y, Z, 0.06, 11.5, 0.14, M['beam'])
        for sg in (-1, 1):
            for (rr, col, dz) in ((1.0, 'p_blue', 0.0), (0.68, 'p_white', 0.01), (0.34, 'p_red', 0.02)):
                mb.frustum((x0, sg * 7.0, zz + 0.12 + dz), (x0, sg * 7.0, zz + 0.14 + dz), rr, rr, M[col], seg=24); mb.frustum((x0, sg * 7.0, zz - 0.14 - dz), (x0, sg * 7.0, zz - 0.12 - dz), rr, rr, M[col], seg=24)
    for sg in (-1, 1):
        for yy in (3.0, 8.0): beam(mb, (0.2, sg * yy, 0.0), (0.9, sg * yy, 3.4), 0.16, 0.16, M['beam']); beam(mb, (1.4, sg * yy, 0.0), (1.9, sg * yy, 3.4), 0.16, 0.16, M['beam'])
        rod(mb, (0.2, sg * 8, 0.1), (1.0, sg * 0.9, 3.3), 0.025, M['wire'], 4)
    mf.frustum((-8.5, 0, 0.7), (0.5, 0, 0.9), 0.25, 0.9, fus, seg=12); mf.frustum((0.5, 0, 0.9), (3.0, 0, 0.9), 0.9, 0.85, fus, seg=12); mf.frustum((3.0, 0, 0.9), (3.5, 0, 0.9), 0.85, 0.85, M['galv'], seg=12)
    obox(mf, (-1.0, 0, 1.55), X, Y, Z, 0.9, 0.7, 0.08, M['p_black']); obox(mf, (1.6, 0, 1.6), X, Y, Z, 0.5, 0.7, 0.08, M['p_black'])
    mf.sphere((-0.8, 0, 1.75), 0.3, M['p_cream'], 10, 8); mf.frustum((-0.9, 0, 1.95), (-0.9, 0, 2.05), 0.34, 0.34, M['p_black'], seg=12)
    obox(mf, (-8.4, 0, 1.3), X, Y, Z, 0.6, 0.06, 1.0, fus); obox(mf, (-8.0, 0, 0.8), X, Y, Z, 0.8, 3.0, 0.1, wing); obox(mf, (-9.0, 0, 1.3), X, Y, Z, 0.1, 0.06, 1.0, M['p_red'])
    for sg in (-1, 1):
        beam(mf, (0.8, sg * 1.0, 0.3), (0.8, sg * 2.0, -2.6), 0.14, 0.14, M['beam']); beam(mf, (1.8, sg * 1.0, 0.3), (1.2, sg * 2.0, -2.6), 0.14, 0.14, M['beam']); mf.frustum((1.0, sg * 2.0 - 0.1, -2.6), (1.0, sg * 2.0 + 0.1, -2.6), 0.95, 0.95, M['p_black'], seg=18)
    rod(mf, (1.0, -2.0, -2.6), (1.0, 2.0, -2.6), 0.07, M['steel'], 6)
    mkobj(mb, name + '_wings', parent=root); mkobj(mf, name + '_body', parent=root, smooth=False)
    pe = F.empty(name + '_prop', parent=root, loc=(3.6, 0, 0.9)); obox(mp, (0, 0, 0), X, Y, Z, 0.06, 0.18, 1.9, M['beam']); mp.sphere((0.05, 0, 0), 0.22, M['brass'], 8, 6); mkobj(mp, name + '_propmesh', parent=pe); H['prop'] = pe
    S['plane'] = H; return H

def set_plane(H, t, frame=None, p0=(-50.0, 70.0, 32.0), p1=(60.0, 62.0, 36.0), dur=1.74):
    u = t / dur; p = Vector(p0).lerp(Vector(p1), u); d = Vector(p1) - Vector(p0); yaw = math.atan2(d.y, d.x)
    H['root'].location = p; H['root'].rotation_euler = (math.radians(6.0 * math.sin(u * 4)), math.radians(-3.0), yaw); H['prop'].rotation_euler = (t * 90.0, 0, 0)
    if frame is not None:
        for o, ps in ((H['root'], 'location'), (H['root'], 'rotation_euler'), (H['prop'], 'rotation_euler')): o.keyframe_insert(ps, frame=frame)

def build(preset, samples=None, quality=None):
    P = PRESETS[preset]; t0 = time.time(); F.begin('sky', preset); S.update(flat=True, trenches=[], craters=[], corridors=[], mud_zones=[]); ST.street_scene(P)
    H = build_plane(); set_plane(H, P.get('t', 0.9))
    cam = P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []; F.finish(cam, P, samples, quality, sun=P.get('sun')); S['build_s'] = time.time() - t0; return F.anchors()

PRESETS = dict(
    sky_plane=dict(cam=dict(loc=(6.0, 10.0, 2.0), look_at=(2.0, 66.0, 25.0), lens=26), t=0.9, green=True, sun=(-110.0, 34.0), note='shot 32: RFC biplane over Flers rooftops (plane on its own empty, flies along a path)'),
)
