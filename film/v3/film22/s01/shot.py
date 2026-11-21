"""s01 (0.00-3.55 s, film frames 0-107): the HOOK. Beck's lodgings NIGHT. Low hero 3/4, always moving: push + arc left past the ink bottles, then at 2.3 s a swing right to the window.
Beats: f0 red line being ruled; f22 (0.65) set square snaps the 45 deg corner; f58 (1.82) thumb slides a station tick; f74 (2.35) camera swings to the window (crowd below).
Run: python3 shot.py [draft|final] [first last]   (frames land in ./frames, resumable)"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c22 as C
B, H = C.B, C.H
V = C.V
bpy = C.bpy

SHOT = 's01'
G0, G1 = 0, 108
FIRST, LAST = 0, 113          # 6 handle frames after (travel join into s02), none before (film start)

def _poly(pts, s):
    segs = [(V(p), V(q)) for p, q in zip(pts, pts[1:])]; L = [(q - p).length for p, q in segs]; s = s * sum(L)
    for (p, q), l in zip(segs, L):
        if s <= l: return p + (q - p) * (s / l)
        s -= l
    return V(pts[-1])
SW0, SW1 = 58, 107
SW_LOC = [(-0.5, -1.5, 2.8), (3.4, -1.4, 3.4), (7.3, 1.2, 4.5), (7.3, 8.0, 5.0), (6.6, 12.4, 5.0)]
SW_LOOK = [(0.6, 8.0, 3.3), (4.0, 8.5, 3.6), (6.2, 11.0, 4.6), (6.6, 14.0, 5.0), (6.6, 14.0, 5.0)]
def _u(g):
    x = C.fl(g, SW0, SW1); return 0.9 * C.ez(x) + 0.1 * x
def _lens(g):
    base = 30.0 + 4.0 * (1 - C.ez(C.fl(g, 50, 100)))
    return base - 6.5 * math.sin(math.pi * C.fl(g, 70, 104)) ** 1.5      # a wider moment while crossing the room (more wallpaper and window frame in view), back to 30 mm at the pane
CAMS = [
    (0,   (2.0, -1.3, 2.3), (0.9, 7.4, 3.0), 36),
    (28,  (1.1, -1.3, 2.4), (0.8, 7.5, 3.1), 36),
    (SW0, (-0.5, -1.5, 2.8), (0.8, 8.0, 3.3), 34),
] + [(g, tuple(_poly(SW_LOC, _u(g))), tuple(_poly(SW_LOOK, _u(g))), _lens(g)) for g in range(SW0 + 3, SW1 + 1, 3)] + [(107, (6.6, 12.4, 5.0), (6.6, 14.0, 5.0), 30)]
CAMS = sorted({k[0]: k for k in CAMS}.values())
sh = C.configure(SHOT, CAMS, state=dict(diagram=dict(red=0.46, blue=0, green=0, yellow=0, hot='red', ruler=None)))

CORNER2 = 0.616                                   # fraction of the red polyline at the top of the 45 deg diagonal
def red_frac(g):
    if g <= 16: return 0.46 + (CORNER2 - 0.46) * C.ez(C.fl(g, 0, 16)) ** 0.8 if g > 0 else 0.46
    if g < 37: return CORNER2
    return CORNER2 + (1.0 - CORNER2) * C.ez(C.fl(g, 37, 53))

def bob(g, a=0.04): return a * math.sin(g * 2 * math.pi / 14.0)

def tick_u(g):                                    # the station tick Beck slides (red line, horizontal run): u from 0.9 to 2.3
    return 0.9 + 1.5 * C.ez(C.fl(g, 56, 72))

def window_glow(g):
    """the street beyond the window is a baked card (emissive): lift its brightness a little while the camera crosses the room (it reads as the lit street pulling the eye)
    and ease back to exactly 1.0 by the pane so the end equals s02 frame 0."""
    k = 1.0 + 0.32 * math.sin(math.pi * C.fl(g, 68, 104)) ** 1.2
    for m in bpy.data.materials:
        if m.name == 'BK_e_nightcity' and m.node_tree:
            for n in m.node_tree.nodes:
                if 'Strength' in n.inputs: n.inputs['Strength'].default_value = k

def actors(g):
    window_glow(g)
    cam = B.cam_eval(CAMS, g)[0]
    hot = 'red' if (g < 17 or 37 <= g < 54) else None
    ruler = (45.0, -0.30, -0.45) if g < 17 else None
    H.set_diagram(dict(red=red_frac(g), hot=hot, ruler=ruler))
    st = C
    yb = 4.9                                       # Beck stands in front of the board's lower edge
    hr = -4 + 3 * math.sin(g * 0.45); ln = 14 + 2.5 * math.sin(g * 0.33 + 1)
    if g < 17:
        tip = H.hot_tip('red', H.DIAG['red'])
        C.place_ray('beck_rule_line', 'pen_r', tip, cam, yb, pose=dict(board=0, prop_l=None, head_roll=hr, lean=ln))
    elif g < 37:
        c2 = H.board_pt(-0.15, -0.55, 0.1)
        C.place_ray('beck_set_square', 'hand_r', c2, cam, yb, pose=dict(board=0, head_roll=-3 + 2 * math.sin(g * 0.5)))
    elif g < 54:
        tip = H.hot_tip('red', H.DIAG['red'])
        C.place_ray('beck_rule_line', 'pen_r', tip, cam, yb, pose=dict(board=0, prop_l=None, head_roll=hr, lean=ln))
    else:
        u = tick_u(g); tp = H.board_pt(u, -0.05, 0.12)
        fa = 1.0 - C.ez(C.fl(g, 72, 75.5))                        # Beck dissolves as the camera whips past him to the window (he would leave the frame edge / caption band)
        if fa > 0.02:
            ob = C.place_ray('beck_thumb_push', 'hand_r', tp, cam, yb, pose=dict(board=0, head_roll=-3 + 2 * math.sin(g * 0.5), gaze=(0.9, 0.2) if g < 76 else (-0.6, -0.2)), shadow=fa > 0.5)
            if fa < 1.0: C.fade_card(ob, fa)
        mk = B.Part('station_marker', ink=False, shadow=False); mb = mk.mb; E = B.STATE['E']
        import math as m
        def disc(r, z, mat, n=16):
            mb.pid += 1; mb.face([H.board_pt(u + r * m.cos(2 * m.pi * i / n), -0.05 + r * m.sin(2 * m.pi * i / n), z) for i in range(n)], mat, [(0, 0)] * n)
        disc(0.26, 0.10, E('mk_ink', color='#1a1840', k=0.9)); disc(0.19, 0.105, E('mk_white', color='#ffffff', k=1.2)); mk.done()

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'
    only = None
    if len(sys.argv) > 2:
        if ',' in sys.argv[2]: only = [int(x) for x in sys.argv[2].split(',')]
        else:
            a = [int(x) for x in sys.argv[2:]]; only = a if len(a) == 1 else list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    C.main(SHOT, FIRST, LAST, actors, quality='preview' if mode == 'draft' else 'final', outdir=os.path.join(C.HERE, 'draft' if mode == 'draft' else 'frames'), only=only)
