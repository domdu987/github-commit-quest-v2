#!/usr/bin/env python3
"""Take s26 = shot 26 (62.442-65.400, film g 1873..1964): kitchen_storm. The last image of the film.

Out of the white flash tight on the window (the wall of water fills the panes, spray, lightning); snap 63.28-63.82 (16 f):
pull back x0.43 and tilt down into THE TABLE FRAMING (the framing shot 15 ends on); from 64.2 a slow push onto the weather
box easing to 0 by 65.0; the last 12 frames are still. 5 Hz shake decaying to 0 by 64.6. No characters: rings race across
the coffee, the cup and saucer creep toward the table edge, the paper flutters under the saucer, a pane cracks at 64.00,
one drop lands on 'ฝนตก' at 64.95 and the ink bleeds.
    python3 shot.py still|draft|render|post|contact   (see set3d_kitchen/kshot.py)"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d_kitchen'))
import kshot as KS                                    # noqa: E402
import kitchen_geom as KG                             # noqa: E402
gf, smooth, smoother, lerp = KS.gf, KS.smooth, KS.smoother, KS.lerp

TAKE, SHOTS, LIGHT, VERSION = 's26', [26], 'kitchen_storm', 4
G0, G1 = 1873, 1965                                    # round(62.442 * 30), end of film
H_IN, H_OUT = 0, 0                                     # white flash in (made by the conform on these frames), end of film out
R0, R1 = G0 - H_IN, G1 + H_OUT
TRANSITION_IN = dict(type='flash', frames=9, note='5 frames to white at the end of s25, 4 frames out over g 1873-1876 (conform)')

SNAP = (gf(63.28), gf(63.82))                          # 1901 -> 1918
PUSH = (gf(64.2), gf(65.0))                            # 1929 -> 1953, then still to 1964
SHAKE_END = gf(64.6)                                   # 1941
CRACK = gf(64.00)                                      # 1923
DROP = gf(64.95)                                       # 1952: the drop lands, bleed frame 0
FLUTTER = (gf(63.90), gf(64.60))                       # 1920 - 1941

WIN_LOC, WIN_LOOK = KG.CAM_WINDOW
TAB_LOC, TAB_LOOK = KG.CAM_TABLE
PUSH_K = 0.15                                          # the push covers 15 percent of the way to the weather box centre
FIN_LOC = lerp(TAB_LOC, KG.WBC, PUSH_K)
FIN_DZ = -0.05                                         # the push also tilts down a hair, so the words rise clear of y 600

def _hash(g, s=0):
    x = math.sin(g * 12.9898 + s * 78.233) * 43758.5453; return x - math.floor(x)

def cam_base(g):
    if g < SNAP[0]:                                    # tight on the window: a slow drift in (2 %/s) so it never parks
        t = (g - G0) / 30.0; loc = lerp(WIN_LOC, WIN_LOOK, 0.02 * t); return loc, WIN_LOOK
    if g < SNAP[1]:
        u = smoother((g - SNAP[0]) / float(SNAP[1] - SNAP[0]))
        # the pull-back leads, the tilt down follows a little behind (it arrives on the same frame)
        ut = smoother(max(0.0, ((g - SNAP[0]) / float(SNAP[1] - SNAP[0]) - 0.08) / 0.92))
        loc0 = lerp(WIN_LOC, WIN_LOOK, 0.02 * (SNAP[0] - G0) / 30.0)
        return lerp(loc0, TAB_LOC, u), lerp(WIN_LOOK, TAB_LOOK, ut)
    if g < PUSH[0]:                                    # settles in the table framing with a hair of creep (0.6 %/s)
        c = 0.006 * (g - SNAP[1]) / 30.0; return lerp(TAB_LOC, KG.WBC, c), lerp(TAB_LOOK, KG.WBC, c)
    c0 = 0.006 * (PUSH[0] - SNAP[1]) / 30.0
    if g < PUSH[1]:                                    # push: fast start, eased to zero at 65.0
        x = (g - PUSH[0]) / float(PUSH[1] - PUSH[0]); u = 1 - (1 - x) ** 1.6
        c = c0 + (PUSH_K - c0) * u
    else: c = PUSH_K                                   # the last 12 frames are still
    lk = lerp(TAB_LOOK, KG.WBC, c); dz = FIN_DZ * (c - c0) / (PUSH_K - c0)
    return lerp(TAB_LOC, KG.WBC, c), (lk[0], lk[1], lk[2] + dz)

def cam(g):
    loc, look = cam_base(g)
    if g >= SHAKE_END: return loc, look
    a = 0.028 * (1 - smooth(G0, SHAKE_END, g)) ** 1.3       # 5 Hz shake, decaying to 0 by 64.6
    t = g / 30.0; sx = math.sin(2 * math.pi * 5 * t); sz = math.sin(2 * math.pi * 5 * t * 1.37 + 1.1)
    lx = (look[0] + a * sx, look[1], look[2] + 0.7 * a * sz); px = (loc[0] + 0.3 * a * sz, loc[1], loc[2] + 0.3 * a * sx)
    return px, lx

def state(g):
    k = g - G0
    # cup and saucer: they rattle (62.5-63.5 hardest) and creep toward the near table edge
    creep = smooth(gf(62.5), gf(64.7), g)
    rat = 1.0 if gf(62.5) <= g <= gf(63.5) else (0.4 if g < SHAKE_END else 0.0)
    step = math.floor(creep * 14) / 14.0 * 0.6 + creep * 0.4  # jerky: steps plus a slow slide
    sx = KG.CUP_REST[0] + 0.05 * step + rat * 0.006 * (_hash(g, 1) - 0.5)
    sy = KG.CUP_REST[1] - 0.17 * step + rat * 0.006 * (_hash(g, 2) - 0.5)
    sr = 4.0 * step + rat * 3.0 * (_hash(g, 3) - 0.5)
    cz = rat * 0.010 * _hash(g, 4); crot = rat * 6.0 * (_hash(g, 5) - 0.5)
    ripple = (-0.9 * k, 0.85 if g < SHAKE_END else 0.85 * (1 - smooth(SHAKE_END, gf(65.2), g)) + 0.25)
    fl_amp = 0.006 + 0.030 * smooth(FLUTTER[0] - 3, FLUTTER[0] + 3, g) * (1 - smooth(FLUTTER[1] - 4, FLUTTER[1] + 2, g))
    drop = None
    if DROP - 4 <= g < DROP:                           # the drop falls onto the word for 4 frames (from a crack in the sash above)
        f = (DROP - g) / 4.0; drop = (KG.W1[0] - 0.05, KG.W1[1] - 0.03 - 0.08 * f, KG.W1[2] + 0.02 + 0.85 * f * f)
    return dict(saucer=(sx, sy, 0.0, sr), cup=(0.0, 0.0, cz, KG.CUP_ROT + crot), ripple=ripple, steam=None, window=('wave', k),
                flutter=(g / 30.0, fl_amp), bleed=(g - DROP) if g >= DROP else None, lightning=KS_LIGHTNING.get(g, 0.0),
                crack=(g - CRACK) if g >= CRACK else None, chair=smooth(gf(62.45), gf(62.9), g), drop=drop)

def arm(g): return None
def cup_in_hand(g): return False

import kitchen_tex as _KT                             # noqa: E402
KS_LIGHTNING = _KT.LIGHTNING

CUES = [
    (62.34, 0.5, 'flash', 'flash hiss with a ringing tail (white flash into the kitchen; the window is still lit by lightning g1873-1876)'),
    (62.45, 2.55, 'bed', 'muffled roar outside, house timbers groan (bed); the wall of water fills the panes'),
    (62.50, 1.0, 'rattle', 'cup rattling on its saucer (cup hops, saucer jitters)'),
    (62.45, 0.45, 'chair', 'the chair is shoved back by the shaking house (out of the frame edge at right)'),
    (62.90, 0.3, 'thunder', 'thunder crack with the lightning in the window (g1890-1894)'),
    (63.28, 0.54, 'whoosh', 'whoosh: the snap pull-back from the window into the table framing'),
    (63.90, 0.70, 'flutter', 'newspaper flutter under the saucer'),
    (64.00, 0.2, 'crack', 'a window pane cracks (lower right pane, crack grows over 4 frames)'),
    (64.20, 0.8, 'push', 'slow push onto the weather box (no sound needed; music under)'),
    (64.95, 0.1, 'plip', 'single plip on paper and one soft piano note: the drop lands on ฝนตก, the ink starts to bleed'),
    (65.00, 0.4, 'silence', 'everything cuts to silence; music out on the drip'),
]

if __name__ == '__main__':
    KS.run(sys.modules[__name__], sys.argv[1:])
