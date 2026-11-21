"""s04 (10.81-15.00 s, film frames 324-449): Beck's lodgings NIGHT. MATCH PUSH: starts ON the OLD map pinned on Beck's wall (the same map as the platform at the end of s03, dissolve 9),
then the camera pulls back and slides right along the wall to Beck (side tracking).  Beats (local k = g - 324):
 k3   (10.81) Beck turns from the board (medium)   k26 (11.55) he pins a circuit diagram on the cork board   k49 (12.34) holds another one up next to the board
 k70  (13.03) he glances at the NOTICE letter on the table and pushes it aside with a sigh     k98 (13.97) picks up the ruler and leans in at the board (continues in s05).
Run: python3 shot.py [draft|final] [first last [step] | a,b,c]   (frames in ./frames, resumable)"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c22 as C
B, H = C.B, C.H
V = C.V
bpy = C.bpy
import cast22

SHOT = 's04'
G0, G1 = 324, 450
FIRST, LAST = 318, 455          # 9-frame dissolve in from s03 (4 + 2 handle frames) and a travel join into s05 (6 after)
CAMS = [  # local frame, loc, look_at, lens   (room coordinates; map centre (-6.1, 13.7, 4.6); frame = 0.675 d wide x 1.2 d tall at lens 30)
    (0,   (-6.1, 10.3, 4.6), (-6.1, 14.0, 4.6), 30),
    (12,  (-5.8, 9.0, 4.5), (-4.4, 14.0, 4.3), 30),
    (26,  (-4.0, 7.4, 4.2), (-0.5, 13.5, 3.9), 30),
    (40,  (-3.1, 5.9, 4.0), (-0.9, 12.5, 3.6), 30),
    (52,  (-2.6, 5.1, 3.95), (-1.2, 11.4, 3.3), 30),
    (70,  (-2.4, 4.5, 3.9), (-2.0, 10.2, 3.0), 30),
    (90,  (-2.6, 2.7, 4.1), (-1.6, 9.2, 2.8), 30),
    (100, (-2.9, 1.2, 4.2), (-0.4, 8.6, 2.5), 30),
    (125, (-2.6, -1.9, 4.6), (0.5, 8.0, 1.9), 30),
]
CAMS = C.smooth_keys(CAMS, 125, sigma=5.0)          # gaussian-smoothed, one key per frame (QA section L)
sh = C.configure(SHOT, CAMS, state=dict(diagram=dict(red=1.0, blue=0, green=0, yellow=0, hot=None, ruler=None)))
sh = B.ALL_SHOTS[SHOT]

def pre_scene():
    """runtime set changes (set modules are read-only): move the wastebasket out of the camera-to-Beck line (QA mandatory item 7)."""
    ob = bpy.data.objects.get('basket')
    for n in ('trunk', 'rolls', 'key_lamp'):                    # their ink hull sits 6 cm below the floor: lift so the base touches (ground_check)
        o = bpy.data.objects.get(n)
        if o: o.location = (0.0, 0.0, 0.063 if n in ('trunk', 'key_lamp') else 0.013)
    if ob: ob.location = (-5.2, 2.6, 0.0)          # to (-8.6, 8.8): the far left corner by the rolls pot
    for n in ('table',):                           # shift the little table 1.2 D left so Beck at the cork board is not behind it
        o = bpy.data.objects.get(n)
        if o: o.location = (-1.2, 0.0, 0.0)
    return ob
LETTER = None

def letter_obj():
    return bpy.data.objects.get('letter')

def pinned_sheet(on):
    if not on: return
    p = B.Part('pin_new', ink=True); S = B.STATE
    p.mb.quad(V((-0.9, 13.64, 3.3)), V((1.6, 0, 0)), V((0, 0, 1.15)), S['TX']('circuit1', 1.1, 1.0, glow='circuit1', glow_k=0.35), (0, 0, 1, 1)); p.done((0.0, 13.6, 3.9), px=2)

def beck(story_or_pose, mark, cam, pose=None, **kw):
    ob = B.cast_card(story_or_pose, mark, face_to=cam, rim='#8fb0ff', pose=pose, **kw)
    return ob

def actors(g):
    k = g - G0
    cam = B.cam_eval(CAMS, k)[0]
    bob = 0.025 * math.sin(k * 0.55)
    nt = letter_obj()
    if nt: nt.hide_render = 74 <= k < 92 or False
    if k < 26:                                                 # turning from the board toward us, circuit in hand
        yaw = 0.15 + 0.35 * C.ez(C.fl(k, 0, 20))
        beck(cast22.STORY22['beck_hold_circuit'], (-0.9, 11.8, 0.0), cam, pose=dict(yaw=yaw, head_roll=-3 + 2 * math.sin(k * 0.4)))
    elif k < 40:                                               # pins it: arm up to the cork (sheet lands at k36)
        u = C.ez(C.fl(k, 26, 34))
        C.place_ray('beck_hold_circuit', 'hand_r', V((-0.2, 13.5, 3.2 + 0.9 * u)), cam, 11.6, pose=dict(prop_r=dict(type='circuit', angle=-6 + 10 * u), head_roll=-3, pitch=-0.15 * u), rim='#8fb0ff', kmin=0.9, kmax=1.15)
        if k >= 36: pinned_sheet(True)
    elif k < 70:                                               # holds another sheet up next to the board and studies it
        pinned_sheet(True)
        w = 0.5 + 0.3 * math.sin((k - 40) * 0.2)
        beck(cast22.STORY22['beck_hold_circuit'], (-0.9, 11.8, 0.0), cam, pose=dict(prop_r=dict(type='circuit', angle=-6 + 8 * math.sin((k - 40) * 0.25)), head_roll=-4 + 3 * math.sin(k * 0.3), yaw=0.5))
    elif k < 78:                                               # steps to the table (walk)
        pinned_sheet(True)
        u = C.ez(C.fl(k, 70, 78)); x = -0.9 + (-2.2 + 0.9) * u; y = 11.8 + (8.2 - 11.8) * u
        p = cast22.walk('beck', (k - 70) / 8.0 * 0.9, yaw=0.3); p['prop_r'] = None
        beck(('beck', p), (x, y, 0.0), cam)
    elif k < 94:                                               # glances at the NOTICE letter, sighs, pushes it aside
        pinned_sheet(True)
        ph = C.fl(k, 78, 94)
        pose = dict(pitch=0.55 + 0.2 * math.sin(k * 0.5), lean=2 + 3 * math.sin(k * 0.35))
        beck(cast22.STORY22['beck_read_notice'], (-2.4, 8.2, 0.0), cam, pose=pose)
    elif k < 104:                                              # picks up the ruler, walks to the board
        pinned_sheet(True)
        u = C.ez(C.fl(k, 94, 104)); x = -2.4 + 2.3 * u; y = 8.2 - 2.7 * u
        p = cast22.walk('beck', (k - 94) / 10.0 * 1.0 + 0.4, yaw=0.45); p['prop_r'] = dict(type='ruler', angle=-30)
        beck(('beck', p), (x, y, 0.0), cam)
    else:                                                      # leans in at the board
        pinned_sheet(True)
        tip = H.board_pt(-1.55, -1.45, 0.07)
        C.place_ray('beck_rule_line', 'pen_r', tip, cam, 4.9, pose=dict(board=0, head_roll=-4, lean=14 + 2 * math.sin(k * 0.4)))
    if nt: nt.location = (-1.2 - (0.5 if k >= 94 else 0.0), 0.25 if k >= 94 else 0.0, 0)   # follows the table; pushed aside at k94

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'
    if mode == 'ground':
        C.ground(SHOT, FIRST, LAST, actors, os.path.join(C.HERE, 'GROUND.md'), pre=pre_scene); sys.exit(0)
    only = None
    if len(sys.argv) > 2:
        if ',' in sys.argv[2]: only = [int(x) for x in sys.argv[2].split(',')]
        else:
            a = [int(x) for x in sys.argv[2:]]; only = a if len(a) == 1 else list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    C.main(SHOT, FIRST, LAST, actors, quality='preview' if mode == 'draft' else 'final', outdir=os.path.join(C.HERE, 'draft' if mode == 'draft' else 'frames'), only=only, pre=pre_scene)
