"""s05 (15.00-19.22 s, film frames 450-576): Beck's lodgings NIGHT. Crane UP over Beck's shoulder to TOP-DOWN over the board, slow rotate (roll to -10 deg) and push.
Continues s04 (travel join, one move): the camera starts exactly on s04's end key/speed.  Beck is a card (upright at the board's lower edge, head in the top of frame) only for the first ~1 s;
after that only his 3D forearm/sleeve/hand/pen enter from the bottom edge (SET_GATE 8: no card lying on the paper).  The OLD map lies on the floor in the lower-right corner (all take).
Beats (local k = g - 450): k5 (15.08) the circuit diagram beside the new map; k28-46 (16.02) blue line ruled; k46-64 (16.83) set square lands, GREEN bends 45 deg;
 k70-112 yellow line drawn then squeezed by his thumb (18.09 = k96).
Run: python3 shot.py [draft|final] [first last [step] | a,b,c]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c22 as C
B, H = C.B, C.H
V = C.V
bpy = C.bpy
import cast22

SHOT = 's05'
G0, G1 = 450, 577
FIRST, LAST = 444, 576          # 6 handle frames before (travel join from s04), hard cut after (s06)
CAMS = [  # local frame, loc, look_at, lens, roll
    (0,   (-2.594, -1.962, 4.608), (0.518, 7.988, 1.888), 30),                  # = s04 frame 450 (continued)
    (10,  (-2.45, -2.45, 4.75), (0.75, 7.9, 1.95), 30),
    (24,  (-1.5, -1.9, 5.6), (1.4, 7.6, 0.8), 30, -1),
    (44,  (0.0, -0.8, 6.7), (2.0, 7.7, 1.2), 29, -2.5),
    (84,  (1.6, 2.0, 8.3), (2.4, 7.8, 2.0), 27, -6.5),
    (126, (2.4, 3.6, 9.0), (2.4, 7.6, 2.4), 26.0, -10),
]
CAMS = C.smooth_keys(CAMS, 126, sigma=4.0)          # gaussian-smoothed, one key per frame (QA section L)
sh = C.configure(SHOT, CAMS, state=dict(diagram=dict(red=1.0, blue=0, green=0, yellow=0, bend=45.0, squeeze=0.0, hot=None, ruler=None)))

def green_bend_frac(): return H.green_bend_frac()
def s05_state(k):
    """strict 0/45/90 geometry: blue ruled (k20-44), green runs flat (46-56), THEN the set square lands (k56..64) and the 45 deg diagonal + vertical appear, yellow drawn (70-86), squeezed (88-112)."""
    fb = green_bend_frac(); gk = C.fl(k, 46, 56) * fb + C.fl(k, 58, 64) * (1 - fb)
    d = dict(red=1.0, blue=C.fl(k, 28, 46), green=gk, yellow=C.fl(k, 70, 86), bend=45.0, squeeze=C.fl(k, 88, 112), ruler=None, hot=None)
    d['hot'] = 'blue' if 28 < k < 46 else 'green' if 46 < k < 64 else 'yellow' if 70 < k < 86 else None
    if 28 < k < 48: d['ruler'] = (90.0, -1.55 + 0.02, -0.3)
    return d

# ----------------------------------------------------------------------------- a 3D arm: shirt sleeve (garter, rolled cuff), forearm, hand
SKIN, SLEEVE, GARTER, CUFF = '#ffc4a0', '#f6f2ff', '#1d1b44', '#e9e4f4'
def lerp3(a, b, t): return a + (b - a) * t

def arm3d(name, W, side=1.0, hand='fist', tool=None, far=6.2, lift=1.3, elbow_out=0.7):
    """Right (side +1) or left (-1) arm whose hand is at world point W; the shoulder is `far` D toward the camera side (outside the frame)."""
    S_ = B.STATE['C']
    W = V(W); S = V((W.x + side * 1.0, W.y - far, W.z + lift)); E = lerp3(S, W, 0.55) + V((side * elbow_out, -0.2, -0.45))
    p = B.Part(name, ink=True); mb = p.mb
    shirt = S_(SLEEVE, 1.7, 2.2, smix=0.2); skin = S_(SKIN, 1.35, 2.2, smix=0.15); dark = S_(GARTER, 1.0, 1.4); cuff = S_(CUFF, 1.6, 2.0, smix=0.2)
    B.rod(mb, S, E, 0.21, shirt, seg=12, r1=0.18)
    g0 = lerp3(S, E, 0.62); g1 = lerp3(S, E, 0.72); B.rod(mb, g0, g1, 0.225, dark, seg=12, r1=0.215)          # black sleeve garter
    c0 = lerp3(E, W, 0.04); c1 = lerp3(E, W, 0.16); B.rod(mb, c0, c1, 0.2, cuff, seg=12, r1=0.2)            # rolled cuff
    B.rod(mb, c1, lerp3(E, W, 0.93), 0.125, skin, seg=12, r1=0.095)                                         # forearm
    d = (W - E).normalized()
    if hand == 'fist':
        mb.sphere(W + d * 0.04, 0.17, skin, seg=12, rings=8)
    else:                                                                                                    # open hand pushing: palm + thumb
        mb.sphere(W + d * 0.05, 0.15, skin, seg=12, rings=8); B.rod(mb, W + d * 0.05, W + d * 0.05 + (d + V((side * 0.6, 0, 0))).normalized() * 0.28, 0.05, skin, seg=6)
    if tool:
        kind, a, b = tool
        if kind == 'pen':                                                                                    # fountain pen held like a pencil: slanted from the hand to the nib at W
            nib = V(a); body = nib + V((0.28, -0.75, 0.55)).normalized() * 1.1
            B.rod(mb, body, nib, 0.05, S_('#1c2a6a', 1.1, 1.5), seg=8, r1=0.025); B.rod(mb, lerp3(body, nib, 0.78), lerp3(body, nib, 0.86), 0.055, S_('#e8b84a', 1.4, 1.6), seg=8)
    p.done(tuple(W), px=2.5)

def set_square_3d(k):
    if not (56 <= k < 70): return
    z = 0.015                                                    # lands flat on the paper (clack) at k56
    sq = B.Part('set_square3d', ink=True)
    pts = [H.board_pt(-0.1, -0.1, z), H.board_pt(1.3, -0.1, z), H.board_pt(-0.1, 1.3, z)]
    sq.mb.pid += 1; sq.mb.face(pts, B.STATE['C']('#ffb347', 1.5, 1.4, smix=0.2)); sq.done(tuple(H.board_pt(0.4, 0.4, z)), px=2.5)

def circuit_on_ledge(k):
    """the circuit diagram sheet lies beside the new map on the board's lower-left (so 'circuit + map side by side' reads from above)"""
    if k < 4: return
    p = B.Part('circuit_beside', ink=True)
    S_ = B.STATE; z = 0.012
    pts = [H.board_pt(-2.95, -1.85, z), H.board_pt(-2.95 + 1.5, -1.85, z), H.board_pt(-2.95 + 1.5, -1.85 + 1.25, z), H.board_pt(-2.95, -1.85 + 1.25, z)]
    # drawn flat on the board's frame/paper edge region: use a pinned look at the left margin of the board
    p.mb.pid += 1; p.mb.face([V(q) + V((0, 0, 0)) for q in pts], S_['TX']('circuit0', 1.1, 1.0, glow='circuit0', glow_k=0.35), [(0, 0), (1, 0), (1, 1), (0, 1)]); p.done(tuple(pts[0]), px=2)

def floor_point(cam_ob, u, v, z=0.07):
    """world point on the plane z where the ray through screen fraction (u from left, v from top) hits (vertical sensor fit)."""
    sc = bpy.context.scene; Wp, Hp = sc.render.resolution_x, sc.render.resolution_y
    lens = cam_ob.data.lens; s = 36.0 / lens
    d_cam = V(((u - 0.5) * s * Wp / Hp, (0.5 - v) * s, -1.0)).normalized()
    M = cam_ob.matrix_world; o = M.translation; d = (M.to_3x3() @ d_cam).normalized()
    return o + d * ((z - o.z) / d.z)

MAPC = None
def old_map_corner(k):
    global MAPC
    if MAPC is None:
        B.set_frame_cam(SHOT, G0 + 112)
        bpy.context.view_layer.update(); c = floor_point(bpy.context.scene.camera, 0.80, 0.90); MAPC = (c.x, c.y); B.set_frame_cam(SHOT, G0 + k)
    p = B.Part('old_map_floor', ink=True); S_ = B.STATE
    c = V((MAPC[0], MAPC[1], 0.13)); a = math.radians(-12)
    ex, ey = V((math.cos(a), math.sin(a), 0)) * 1.25, V((-math.sin(a), math.cos(a), 0)) * 0.9
    p.mb.quad(c - ex - ey, ex * 2, ey * 2, S_['TX']('old_map', 1.15, 1.0, glow='old_map', glow_k=0.5), (0, 0, 1, 1)); p.done(tuple(c), px=2)

def actors(g):
    k = g - G0
    cam = B.cam_eval(CAMS, k)[0]
    d = s05_state(k); H.set_diagram(d)
    old_map_corner(k)
    if k < 30:                                                 # Beck card: upright at the board's lower edge (head in the top of frame), then he steps back out of frame
        tip = H.board_pt(-1.55, -1.45, 0.07)
        if k < 4: C.place_ray('beck_rule_line', 'pen_r', tip, cam, 4.9, pose=dict(board=0, head_roll=-4 + 2 * math.sin(k * 0.4), lean=12 + 2 * math.sin(k * 0.3)))
        elif k < 14: B.cast_card('beck_hold_circuit', (-0.9 + 0.5 * C.ez(C.fl(k, 4, 14)), 4.9, 0.0), face_to=cam, rim='#8fb0ff', pose=dict(head_roll=-3 + 2 * math.sin(k * 0.45)), tilt=8 + 12 * C.ez(C.fl(k, 4, 14)))
        else:
            u = C.ez(C.fl(k, 14, 30)); x = -0.4 - 2.6 * u; y = 4.9 - 0.9 * u
            p = cast22.walk('beck', ((k - 14) / 16.0) * 1.3, yaw=-0.5); p['prop_r'] = dict(type='circuit', angle=-6)
            fa = 1.0 - C.ez(C.fl(k, 21, 26))
            ob = B.cast_card(('beck', p), (x, y, 0.0), face_to=cam, rim='#8fb0ff', tilt=20, shadow=fa > 0.5)                       # he leaves: dissolves as the arms come in (never cut by the frame edge)
            if fa < 1.0: C.fade_card(ob, max(fa, 0.0))
        if k >= 14: circuit_on_ledge(k)
        if k < 27: return
    circuit_on_ledge(k)
    if k < 46:                                                 # ruling the BLUE line: pen in the right hand, ruler held in the left
        tip = H.hot_tip('blue', H.DIAG['blue']); arm3d('arm_r', tip, 1.0, 'fist', ('pen', tuple(tip), None))
        arm3d('arm_l', H.board_pt(-1.5, -1.45, 0.16), -1.0, 'fist', elbow_out=0.9)
    elif k < 70:                                               # set square lands (left hand), pen on the green run (right hand)
        set_square_3d(k)
        gp = H.hot_tip('green', min(1.0, H.DIAG['green']))
        arm_ = arm3d('arm_r', gp, 1.0, 'fist', ('pen', tuple(gp), None))
        sqhand = H.board_pt(0.15, 0.1, 0.1)
        arm3d('arm_l', sqhand, -1.0, 'fist')
    else:                                                      # yellow drawn, then squeezed by his open hand (thumb push)
        top = H.line_pts('yellow', 45.0, H.DIAG['squeeze'])
        w = H.board_pt(top[1][0], top[1][1], 0.1) if k >= 88 else H.hot_tip('yellow', max(0.02, H.DIAG['yellow']))
        arm3d('arm_r', w, 1.0, 'open' if k >= 88 else 'fist', None if k >= 88 else ('pen', tuple(w), None))
        if k < 88:
            arm3d('arm_l', H.board_pt(1.2, -1.6, 0.16), -1.0, 'fist')

def dim_bulbs():
    for m in bpy.data.materials:
        if m.name in ('BK_e_bulb3', 'BK_e_bulb2') and m.node_tree:
            for n in m.node_tree.nodes:
                if 'Strength' in n.inputs: n.inputs['Strength'].default_value *= 0.55

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'
    if mode == 'ground':
        C.ground(SHOT, FIRST, LAST, actors, os.path.join(C.HERE, 'GROUND.md'), pre=dim_bulbs); sys.exit(0)
    only = None
    if len(sys.argv) > 2:
        if ',' in sys.argv[2]: only = [int(x) for x in sys.argv[2].split(',')]
        else:
            a = [int(x) for x in sys.argv[2:]]; only = a if len(a) == 1 else list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    C.main(SHOT, FIRST, LAST, actors, quality='preview' if mode == 'draft' else 'final', outdir=os.path.join(C.HERE, 'draft' if mode == 'draft' else 'frames'), only=only, pre=dim_bulbs)
