import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S, jimo_r2 as R2
SHOT = 's02'; G0, G1, HB, HA = 78, 156, 0, 10
HERD = S.herd(72, (-27, 8.0), (-2, 8.0), 8.0, 11, yaw=180.0)
# ONE smooth pull-out while the camera rises from 1.3 D to ~2.1 D (rows stack up the frame); no pulses
CAM = C.cam_path(((-31.0, 11.6, 1.5), (6.0, 10.2, 2.2), 20), ((-34.0, 10.6, 5.8), (-21.0, 8.6, 0.3), 20), punches=[(0.3, 0.07, -0.10)], slide=0.6)
def tweak(stage, A=None):
    if stage == 'pre':
        import jimo_shots as S2, jimo_r2 as R2
        S2.SHOTS[SHOT]['fg'] = None; R2.POST.pop('s02', None); R2.SKIP['s02'] = [(-34.0, 8.5, 6.5), (-27.0, 8.5, 3.0)]
    elif stage == 'post':
        C.hide('baskets', 'props', 'digtools', 'straw', 'rainstreaks', 'wallpools', 'patches')
        import bpy
        for k, (lx, ly) in enumerate(((-28.0, 8.0), (-18.0, 8.0), (-8.0, 8.0))):
            d = bpy.data.lights.new('c18_fill%d' % k, 'POINT'); d.color = (1.0, 0.62, 0.30); d.energy = 5200.0; d.shadow_soft_size = 2.0; d.use_shadow = False
            lo = bpy.data.objects.new('c18_fill%d' % k, d); bpy.context.scene.collection.objects.link(lo); lo.location = (lx, ly, 5.0); lo.visible_camera = False
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    import atexit
    C.person_card('tiandan', 'tiandan_tie_blade', (-29.0, 12.3, 0), cam, 0, bob=C.hop(f, 0, 0.04, 2.0), roll=2.5 * math.sin(2 * math.pi * 1.5 * t), mods=dict(gaze=(0.8, -0.4), yaw=0.5))
    C.ox_card(SHOT, 0, (-26.6, 11.4, 0), 180, 1.0, cam, view='front_three_quarter', gait='stand', bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9))
    # dark, lit carriers in the lower third (cast props: baskets of earth), walking with the herd
    C.person_card('townsfolk', 'woman_carry_basket', (-32.5, 12.0, 0), cam, 8, bob=0.05 * abs(math.sin(2 * math.pi * 1.7 * t + 1)), roll=C.sway(f, 8, 2, 1.0))
    for i, m in enumerate(HERD):
        x, y, z, yaw, sc = m
        xx = x - 0.9 * t
        near = math.hypot(x + 31, y - 11.4) < 24
        ph = int((f * 0.42 + i * 3) % 8)
        if i % 2 == 0: R2.LIT.append((C.V((xx, y, 0)), C.V((1.0, 0.0, 0.0)), sc))
        C.ox_card(SHOT, i + 1, (xx, y, 0), 180, sc, cam, view='three_quarter', gait='walk', shadow=False, tint=(0.98, 0.84, 0.78), k=0.9, pitch_bb=0.95, phase=ph, bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.42 + i) / 8)))
    R2.lit_pools(cam, nlights=0)

if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.012, cam_fn=CAM, dress=2)
