"""s01 BIGZOOM A (film 18): g 0-155, jimo_in NIGHT. One continuous eased crane-down + push from an EXTREME WIDE over the wall top / roofs down to a MEDIUM on Tian Dan (g 108), then a slow push + orbit."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S, jimo_r2 as R2
from mathutils import Vector as V
SHOT = 's01'; G0, G1, HB, HA = 0, 156, 0, 6
TD = V((-3.4, 16.0, 0.0)); OX = V((-0.9, 15.4, 0.0))
LOOK0 = V((-4.1, 16.8, 0.0)); LOOK1 = V((-3.4, 16.1, 2.1)); LOOK2 = V((-3.2, 16.0, 2.1))
CAM0 = V((-45.0, -15.0, 70.0)); CAM1 = V((-8.6, 11.0, 2.0)); CAM2 = V((-8.2, 11.9, 2.1))
ZOOM_END = 108.0
def sm(u): u = min(1.0, max(0.0, u)); return u * u * u * (u * (6 * u - 15) + 10)           # smootherstep: eased at both ends, no dead hold
def camera(f):
    """(loc, look, lens) at film frame f: zoom g 0-108 (log distance, direction blended, arc over the roofs), then push 6 %/s + a slight orbit g 108-155."""
    if f <= ZOOM_END:
        u0 = f / ZOOM_END; e = 0.5 * sm(u0) + 0.5 * u0; ee = e
        look = LOOK0 * (1 - e) + LOOK1 * e
        r0 = CAM0 - LOOK0; r1 = CAM1 - LOOK1
        L = math.exp(math.log(r0.length) * (1 - ee) + math.log(r1.length) * ee)
        d = (r0.normalized() * (1 - ee) + r1.normalized() * ee); d.normalize()
        side = d.cross(V((0, 0, 1))); side.normalize()
        arc = side * (math.sin(math.pi * e) * 13.0)                                        # curve over the wall top / roofs (parallax), perpendicular to the view axis
        loc = look + d * L + arc
        lens = 24.0 + 8.0 * e
    else:
        u = (f - ZOOM_END) / (155.0 - ZOOM_END)
        look = LOOK1 * (1 - u) + LOOK2 * u
        r1 = CAM1 - LOOK1; ang = math.radians(7.0) * u                                  # slight orbit
        rr = V((r1.x * math.cos(ang) - r1.y * math.sin(ang), r1.x * math.sin(ang) + r1.y * math.cos(ang), r1.z)) * (1.0 - 0.15 * u)
        loc = look + rr; lens = 32.0
    return loc, look, lens
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['fg'] = None
    elif stage == 'post':
        import bpy
        C.hide('baskets', 'props', 'digtools', 'jars', 'reeds')
        C.world_lantern((-1.4, 14.0, 0.0), sc=1.1)
        C.world_plaque((-15.0, 17.6, 0.0), (-28.0, 11.0, 12.0), w=5.2, h=2.05, z=5.6)
        # warm pool + light on Tian Dan and the ox he dresses (findable from far away)
        d = bpy.data.lights.new('c18_td_light', 'POINT'); d.color = (1.0, 0.62, 0.28); d.energy = 3800.0; d.shadow_soft_size = 1.0; d.use_shadow = False
        lo = bpy.data.objects.new('c18_td_light', d); bpy.context.scene.collection.objects.link(lo); lo.location = (-2.2, 15.4, 4.5); lo.visible_camera = False
        M = C.STATE['M']; sm_ = R2._shadow_quad('c18_pool', 1.0, 1.0)
        if not sm_.materials: sm_.materials.append(M['pool_w'])
        po = bpy.data.objects.new('c18_td_pool', sm_); C.STATE['SET'].objects.link(po); po.location = (-2.2, 15.7, 0.07); po.scale = (7.0, 7.0, 1.0); po.visible_shadow = False; C.J.no_bounce(po)
HERD = S.herd(46, (-34, 21.5), (34, 21.5), 12.0, 31, yaw=180.0) + S.herd(24, (-30, 9.2), (30, 9.2), 2.0, 33, yaw=180.0)
HERD = [m for m in HERD if math.hypot(m[0] + 2.0, m[1] - 15.5) > 5.0 and math.hypot(m[0] + 15.0, m[1] - 17.6) > 3.2]
def actors(f, cam, ctx):
    t = f / 30.0
    pull = math.sin(2 * math.pi * 2.0 * t)
    pose = 'tiandan_tug_cloth' if f < 90 else 'tiandan_tie_blade'
    C.person_card('tiandan', pose, (TD.x + 0.25 * pull * (f < 90), TD.y, 0), cam, 0, bob=C.hop(f, 0, 0.04, 1.6), roll=(4.0 * pull if f < 90 else 3.0 * math.sin(2 * math.pi * 1.4 * t) + 1.5 * math.sin(2 * math.pi * 3.1 * t)), sz=1 + 0.015 * pull, rim=True, k=0.8,
                  mods=dict(gaze=(0.9, 0.2), yaw=0.55) if f < 90 else dict(gaze=(0.8, -0.4), yaw=0.5))
    C.ox_card(SHOT, 0, (OX.x + 0.04 * pull, OX.y, 0), 165, 1.0, cam, gait='stand', coat=0.55 + 0.45 * min(1.0, max(0.0, (f - 4) / 80.0)), bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9), rim=True, k=0.8)
    if f >= 60:                                                                          # basket carriers in the lower third once the camera is low
        loc, look, _ = camera(f); fw = look - loc; fw.z = 0; fw.normalize(); rt = V((fw.y, -fw.x, 0.0)); k = min(1.0, (f - 60) / 40.0)
        pa = loc + fw * 4.8 - rt * 1.25; pb = loc + fw * 4.2 + rt * 1.55
        C.person_card('townsfolk', 'woman_carry_basket', (pa.x, pa.y, 0), cam, 8, h=1.9, bob=0.05 * abs(math.sin(2 * math.pi * 1.7 * t + 1)), roll=C.sway(f, 8, 2, 1.0))
        C.person_card('child', 'child_carry_basket', (pb.x, pb.y, 0), cam, 9, h=1.4, bob=0.06 * abs(math.sin(2 * math.pi * 2.0 * t)), roll=C.sway(f, 9, 2, 1.0), mirror=True)
    for i, (x, y, z, yaw, sc) in enumerate(HERD):
        dd = (V((x, y, 0)) - cam).length
        C.ox_card(SHOT, 20 + i, (x, y, 0), 175 + (i % 5) * 6, sc, cam, gait='stand' if dd > 40 else 'walk', phase=int((f * 0.25 + i * 3) % 8), shadow=(dd < 45), pitch_bb=0.9,
                  bob=C.hop(f, i + 5, 0.03, 0.7), roll=C.sway(f, i + 9, 1.6, 0.6))
def cam_fn(t):
    f = G0 + t * (G1 - 1 - G0); return camera(f)
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.004, cam_fn=cam_fn)
