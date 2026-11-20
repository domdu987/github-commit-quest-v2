"""T4 coach in the stands (g1205-1272): closer camera, cards on every tread in frame, no black void, coach >= 20 % of frame height, punch close-up 2."""
import math, random
import numpy as np
from mathutils import Vector
import bpy
import cast15, cast6
import set15 as F
import v2_b as B2, v2_b_shots as SHB, cast_test as CT
from set15_lib import U, STATE
import shot as S

CU = 103.2
def setup(qq, S_):
    A, sc = SHB._base('TENSE', qq, sparkles=False)
    F.clear_keys()
    cs = B2.stand_pos(7, CU, 0.5); S.CS = cs
    rr = random.Random(41); seats = []
    cam0 = Vector(B2.stand_pos(2.6, CU + 1.3, 0.0)); S.CAM0 = cam0
    crowd = ['crowd1', 'crowd2', 'crowd3', 'crowd4', 'crowd5', 'crowd6']; poses = ['sit_cheer', 'sit_laugh', 'sit_point', 'sit_gape', 'sit_cross', 'sit_cheer', 'sit_laugh']
    cards = []; SHB.rim(True, side='left', color=(255, 226, 180), width=0.045, k=0.6, tint=(0.82, 0.85, 0.98), cool=0.4)
    cam_loc = (cam0.x, cam0.y, cam0.z + 1.9); k = 0
    spots = []
    for row in range(1, 20):
        step = 0.62 + 0.0 * row
        for du in range(-19, 20):
            u = CU + du * step + (0.31 if row % 2 else 0.0) + rr.uniform(-0.12, 0.12)
            if row in (7, 8) and abs(u - CU) < 0.9: continue                     # the coach's own seat space
            if row == 9 and abs(u - CU) < 0.5: continue
            if row < 7 and abs(u - (CU + 0.45)) < 0.62: continue                  # a narrow aisle lane for the line of sight
            if rr.random() < 0.05: continue
            spots.append((row, u))
    # hide only the 3D figures that sit right under a card seat (no black void, no double crowd)
    pts = np.array([B2.stand_pos(r, u, 0.5) for r, u in spots] + [cs])
    hide_near(pts, 0.7)
    B2.hide_rails((cs[0], cs[1], cs[2]), 40.0)
    for i, (row, u) in enumerate(spots):
        cast = rr.choice(crowd); pose = rr.choice(poses)
        r = SHB.seat_card('cr%d' % i, cast, pose, row, u, cam_loc, ppd=96, mirror=rr.random() < 0.5, back=0.5 + rr.uniform(-0.1, 0.1))
        ob = bpy.data.objects['actor_cr%d' % i]; cards.append((ob, ob.location.z, rr.uniform(0, 6.28), rr.choice((2.2, 2.8, 3.1)), rr.uniform(0.02, 0.05)))
    SHB.rim(False); S.CARDS = cards
    pool = B2.mat_disc_glow('coach_pool', (1.0, 0.86, 0.6), 1.1, 0.9, 1.6); x, y, z = cs; rp = 2.1
    V, Fc, UV = B2.quad_uv((x - rp, y - rp, z + 0.04), (x + rp, y - rp, z + 0.04), (x + rp, y + rp, z + 0.04), (x - rp, y + rp, z + 0.04)); B2.mesh_obj('coach_pool', V, [Fc], pool, uv=UV)
    cam = B2.make_camera_m(cam_loc, (cs[0], cs[1], cs[2] + 1.0), lens=22.0); sc.camera = cam
    return A, sc, cam, lambda g: draw(g, sc, cam)

def hide_near(pts, r):
    from math import hypot
    for ob in STATE.get('crowd_objs', []):
        me = ob.data; co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 8, 3)
        ctr = co.mean(1); m = np.zeros(len(ctr), bool)
        sel = (np.abs(ctr[:, 0] - pts[:, 0].mean()) < 40) & (np.abs(ctr[:, 1] - pts[:, 1].mean()) < 40)
        idx = np.where(sel)[0]
        if len(idx) == 0: continue
        d = np.hypot(ctr[idx, None, 0] - pts[None, :, 0], ctr[idx, None, 1] - pts[None, :, 1]); dz = np.abs(ctr[idx, None, 2] - pts[None, :, 2] - 0.6)
        hit = ((d < r) & (dz < 1.6)).any(1); m[idx[hit]] = True
        if m.any():
            co[m, :, 2] -= 400.0; me.vertices.foreach_set('co', co.reshape(-1)); me.update()

def coach_cam(g):
    cs = S.CS; c = Vector(cs); look0 = c + Vector((0, 0, 0.95))
    def ucam(u, rowf, h):
        p = Vector(B2.stand_pos(rowf, u, 0.0)); return Vector((p.x, p.y, p.z + h))
    # medium: slides sideways along the tread and pushes in a little (parallax through the seated cards)
    t = (g - 1205) / 67.0
    if g < S.G_CU[0] - 8:
        u = (g - 1205) / float(S.G_CU[0] - 8 - 1205); e = S.sm(u)
        loc = ucam(CU + lerp(2.1, 0.9, e), lerp(3.1, 3.6, e), lerp(2.0, 1.9, e)); look = look0; lens = 22.0
    elif g < S.G_CU[0]:                                    # punch in
        u = S.sm5((g - (S.G_CU[0] - 8)) / 8.0); a = ucam(CU + 0.9, 3.6, 1.9)
        b = c + Vector((0.2, -1.75, 0.55)) * 1.0; b = Vector((b.x, b.y, 0)) + Vector((0, 0, c.z + 1.15))
        loc = a.lerp(b, u); look = look0.lerp(c + Vector((0, 0, 1.45)), u); lens = lerp(22.0, 34.0, u)
    else:                                                  # hold the close-up with a slow drift, then ease out
        b = Vector((c.x, c.y, c.z)) + Vector((0.2, -1.75, 0.55)); b = Vector((b.x, b.y, c.z + 1.15))
        k = (g - S.G_CU[0]) / 24.0; loc = b + Vector((0.12 * k, 0.0, 0.03 * k)); look = c + Vector((0.0, 0.0, 1.45)); lens = 34.0
        if g > S.G_CU[1] - 2:
            u = S.sm5((g - (S.G_CU[1] - 2)) / 8.0); a = ucam(CU + 0.9, 3.6, 1.9); loc = loc.lerp(a, u * 0.7); look = look.lerp(look0, u); lens = lerp(34.0, 24.0, u)
    # whip in (tilted below the coach) / whip out (tilting down to the treads)
    if g < 1211:
        w = 1 - S.sm5((g - 1205 + 1) / 7.0); look = look - Vector((0, 0, 9.0 * w * w)) if g < 1211 else look
    if g >= 1268:
        w = S.sm5((g - 1268 + 1) / 5.0); look = look - Vector((0, 0, 14.0 * w))
    return tuple(loc), tuple(look), lens

def lerp(a, b, u): return a + (b - a) * u

def draw(g, sc, cam):
    S.clear_dyn(); loc, look, lens = coach_cam(g)
    lc = Vector(loc) * U; cam.location = lc; cam.rotation_euler = SHB._cam_rot(lc, Vector(look) * U); cam.data.lens = lens; sc.frame_set(g)
    for ob, z0, ph, hz, amp in S.CARDS: ob.location.z = z0 + amp * U * max(0.0, math.sin(g / 30.0 * hz * 6.2832 + ph))
    pose = cast15.pose_for('coach_shout', 'coach'); pose = dict(pose)
    pose['mouth'] = cast6.talk_mouth(g, 1.0) if S.G_MOUTH[0] <= g <= S.G_MOUTH[1] else 'flat'
    cu_ = S.G_CU[0] - 4 <= g <= S.G_CU[1] + 2
    SHB.rim(True, side='left', color=(255, 236, 200), width=0.06, k=0.95, tint=(1.0, 1.0, 1.04), bright=1.1, cool=0.2)
    SHB.card('dyn_coach_%d' % g, 'coach', pose, (S.CS[0], S.CS[1]), tuple(loc), z=S.CS[2], ppd=(448 if cu_ else 176), shadow=(1.9, 0.6), kind='seat')
    SHB.rim(False)
