#!/usr/bin/env python3
"""Take s20 = shot 20 (47.296-50.529, film g 1419..1515, handles 7 in / 7 out): THE CORRIDOR VIEW, the launch.
Continues s19 (same scene, office_grey, hand-drawn red line, walls locked, lane lit).  No characters.
  creep 6 %/s behind the spinner while three waves of wind arrows stream past from behind the lens (47.4, 47.7, 48.0);
  snap 47.95-48.45 = the launch: the third wave flings the spinner north, the camera shoots after it along the bent lane
  (0.45 D in 1.1 s, 5 Hz shake), from 49.0 it eases to rest beside the speed sign (u 0.62, roadside); the spinner blasts past
  the sign at 49.10, the sign spins in the wake and settles on '100' by 50.30; push with decaying shake.
    python3 shot.py probe | still g,g [draft] | draft [a:b:step] | render | motion | cues"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, DIR)
import mc                                                   # noqa: E402
from mc import gf, clamp, smooth, smoother, lin, snap_e, hsh, Vector   # noqa: E402

TAKE, SHOTS = 's20', [20]
G0, G1 = 1419, 1516                                       # round(47.296 * 30), round(50.529 * 30)
H_IN, H_OUT = 7, 7                                        # dissolve 9 in (4.5 + 2, up), dissolve 10 out (5 + 2)
R0, R1 = G0 - H_IN, G1 + H_OUT                            # 1412 .. 1522
LENS_H = 0.35
WAVES = (gf(47.4), gf(47.7), gf(48.0))                    # 1425, 1434, 1443
SNAP = (gf(47.95), gf(48.45))                             # 1442 -> 1457
LAUNCH = gf(48.0)                                         # 1443
EASE = (gf(49.0), gf(49.25))                              # 1473 -> 1480 travel eases to rest
PASS = gf(49.10)                                          # 1476 spinner passes the sign
SETTLE = gf(50.30)                                        # 1512
SIGN_U, SIGN_A, SIGN_H, SIGN_S = 0.62, 0.040, 0.42, 0.52  # sign on its pin at the roadside, disc below the wall tops
U_SP0 = 0.17                                              # where shot 19 leaves the spinner

_C = {}
def lat0():
    import office_mech as M
    if 'a' not in _C: _C['a'] = M.clear_lateral(-0.10, LENS_H)[0]      # chord lateral where the lens sees N.Y. (-0.15)
    return _C['a']

# ----------------------------------------------------------------------------- the lens travels ALONG the line
FOLLOW_END, REST = gf(48.82), gf(49.35)                     # 1467 the lens stops following the spinner, 1484 at rest
GAP = 0.255
def _creep(g):
    t = (g - R0) / 30.0; return -0.115 + 0.02 * t + 0.004 * t * t      # 6 %/s creep toward the spinner (slowly accelerating)

def u_lens(g):
    """Creep; from the launch the lens rides GAP behind the flung spinner (shooting after it), then brakes to rest
    (cubic Hermite from the follow speed) and pushes on slowly."""
    if g <= LAUNCH:
        return _creep(g)
    def follow(x):
        e = smooth(LAUNCH, LAUNCH + 5, x)                               # from the creep onto the spinner's tail
        return (1 - e) * _creep(x) + e * (u_spin(x) - GAP)
    if g <= FOLLOW_END: return follow(g)
    p0 = follow(FOLLOW_END); v0 = follow(FOLLOW_END) - follow(FOLLOW_END - 1); T = float(REST - FOLLOW_END)
    p1 = p0 + 0.5 * v0 * T
    if g <= REST:
        s = (g - FOLLOW_END) / T; h10 = s ** 3 - 2 * s * s + s; h01 = -2 * s ** 3 + 3 * s * s
        return p0 + h10 * T * v0 + h01 * (p1 - p0)
    tt = (g - REST) / 30.0; return p1 + 0.03 * tt - 0.005 * tt * tt

def lens_pt(g):
    import office_mech as M
    ul = u_lens(g); sc = M.sc_of_u(ul); w = smooth(-0.075, 0.05, ul)
    la = (1 - w) * lat0() + w * M.lateral(-0.035, sc)
    h = LENS_H + 0.02 * smooth(SNAP[0], REST, g)
    return Vector(M.world_sc(la, sc, h)), ul

def look_pt(g):
    import office_mech as M
    ul = u_lens(g)
    corr = Vector(M.world(0.0, 0, 0.06, u=min(1.0, max(0.85, ul + 0.55))))     # up the corridor (N.Y. end)
    sign = Vector(M.world(SIGN_A, 0, SIGN_H - 0.10, u=SIGN_U))         # below the sign: it sits in the upper half
    return corr.lerp(sign, smooth(SNAP[0] + 10, REST + 4, g))

def shake(g):
    out = Vector((0, 0, 0))
    k = g - LAUNCH
    if k >= 0:
        a = 0.010 * math.exp(-k / 16.0) + 0.0025 * math.exp(-max(0, g - PASS) / 10.0) * (g >= PASS)
        ph = 2 * math.pi * 5.0 * k / 30.0                              # 5 Hz
        out += Vector((a * math.sin(ph), 0.4 * a * math.sin(ph * 1.3 + 0.7), a * 0.8 * math.sin(ph * 0.9 + 1.9)))
    return out

def cam_setup(g):
    loc, _ = lens_pt(g); look = look_pt(g) + shake(g)
    return dict(loc=tuple(loc), look_at=tuple(look), lens=22.0, up=(0.0, -1.0, 0.0))

# ----------------------------------------------------------------------------- the map's state per frame
def u_spin(g):
    if g < LAUNCH: return U_SP0 - 0.006 * smooth(LAUNCH - 5, LAUNCH, g)            # squashed back by the gust
    k = (g - LAUNCH) / float(PASS - LAUNCH)                              # 0 .. 1 at the sign
    if k <= 1: return U_SP0 - 0.006 + (SIGN_U - U_SP0 + 0.006) * k ** 1.15
    v = (SIGN_U - U_SP0 + 0.006) * 1.15 / (PASS - LAUNCH)              # u per frame at the pass
    d = g - PASS; return min(0.985, SIGN_U + v * d - 0.00008 * d * d)

def spin_angle(g):
    deg = 0.0
    for k in range(R0, g): deg += 10.0 + 14.0 * smooth(LAUNCH - 2, LAUNCH + 6, k)
    return deg

def state(g):
    _ = mc._M; M, X = _['M'], _['X']
    mc.base_state()
    u = u_spin(g); sq = 1.0; wob = 3.0 * math.sin(math.radians(spin_angle(g)))
    k = g - (LAUNCH - 3)
    if 0 <= k < 4: sq = 0.70 + 0.05 * k                                 # the gust squashes it flat
    if g >= LAUNCH:                                                     # rockets north, tall and leaning forward
        sq = 1.0 + 0.35 * math.exp(-(g - LAUNCH) / 10.0) + 0.12; wob = 16.0 + 4 * math.sin((g - LAUNCH) * 1.3)
    a_sp = -0.04 * smooth(PASS - 12, PASS - 4, g) * (1 - smooth(PASS + 3, PASS + 10, g))   # swerves past the sign post
    xz = M.world(a_sp, 0, 0, u=u)
    X.set_spinner(xz=(xz[0], xz[2]), angle=spin_angle(g), wobble=wob, squash=sq, fast=0.25 + 0.6 * smooth(LAUNCH, LAUNCH + 4, g))
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (g - R0) / 18.0)
    M.set_spinner_fx(ring=0.75 * (1 - 0.7 * smooth(LAUNCH, LAUNCH + 6, g)), ring_pulse=pulse, drop=0.0)
    # wind: three waves (amount 0.33 / 0.66 / 1), progress about 0.9 per second of gust, faster after the launch
    amt = 0.0; prog = 0.0
    for i, w in enumerate(WAVES):
        amt = max(amt, (i + 1) / 3.0 * smooth(w - 3, w + 2, g))
    for kk in range(R0, g): prog += (0.9 + 0.8 * smooth(WAVES[2] - 2, WAVES[2] + 4, kk)) / 30.0 * (0.4 + 0.6 * smooth(WAVES[0] - 4, WAVES[0], kk))
    amt *= 1 - 0.55 * smooth(PASS + 6, SETTLE, g)
    M.set_wind(prog, amount=max(amt, 1e-4) if amt > 0.01 else 0.0)
    # wake: red-hot streak behind the spinner
    if g >= LAUNCH:
        M.set_wake(u, min(0.32, u - (U_SP0 - 0.02)), alpha=1.0 - 0.6 * smooth(PASS + 14, R1, g))
    # the speed sign: spins in the wake at the pass, settles on '100' (two turns, ease-out, small rocking settle)
    x = clamp((g - PASS) / 22.0); spin = 720.0 * (1 - (1 - x) ** 3) if g >= PASS else 0.0
    if g >= PASS + 22: spin = 720.0 + 9.0 * math.exp(-(g - PASS - 22) / 5.0) * math.sin((g - PASS - 22) * 1.15)
    if g >= SETTLE: spin = 720.0
    M.set_speed_sign(show=1.0, spin_deg=spin, scale=SIGN_S, u=SIGN_U, a=SIGN_A, height=SIGN_H)
    po = M.STATE['objects']['sign_post']; po.location = (0.0, 0.012, po.location.z)    # the pin behind the disc, not across its face
    # the no-turn pictograms: the first two gusts flap them and fold them back into the wall faces (the lens flies past there)
    f = smooth(WAVES[0] - 1, WAVES[1] + 4, g)
    for sd in 'EW':
        M.set_picto(sd, show=1.0 - f, scale=0.5, s=0.22, h=0.30, yaw_deg=(22.0 if sd == 'E' else 60.0) * (1 - f),
                    tilt_deg=(0.0 if sd == 'E' else 35.0) * (1 - f), wobble_deg=14 * math.sin((g - WAVES[0]) * 1.7) * smooth(WAVES[0] - 2, WAVES[0] + 2, g) * (1 - f))

def apply(g):
    _ = mc._M; state(g); cam = _['S'].make_camera(cam_setup(g)); _['bpy'].context.view_layer.update(); return cam

def probe_frame(g):
    import office_mech as M
    apply(g); loc, ul = lens_pt(g)
    u = u_spin(g); c = mc.project(M.world(0, 0, 0.02, u=u)); e = mc.project(M.world(0.08, 0, 0.02, u=u))
    sgn = M.world(SIGN_A, 0, SIGN_H, u=SIGN_U); sc_ = mc.project(sgn)
    r = 0.13 * SIGN_S; tg = Vector(M.east(SIGN_U)); s1 = mc.project(Vector(sgn) + r * tg); s2 = mc.project(Vector(sgn) - r * tg)
    ny = mc.project(M.S.track_point(1.0))
    return dict(g=g, u_lens=round(ul, 3), lens_h=round(-(loc.y - M.MAP_Y), 3), spin_u=round(u, 3), spinner_xy=[round(c[0]), round(c[1])],
                spinner_px=round(2 * math.hypot(e[0] - c[0], e[1] - c[1])), sign_xy=[round(sc_[0]), round(sc_[1])],
                sign_px=round(math.hypot(s1[0] - s2[0], s1[1] - s2[1])), ny=[round(ny[0]), round(ny[1])])

CUES = [
    (47.20, 0.4, 'whoosh', 'whoosh: the dissolve into the corridor view behind the spinner'),
    (47.40, 0.5, 'gust', 'gust 1 (low): first wave of wind arrows streams past from behind the lens'),
    (47.70, 0.5, 'gust', 'gust 2 (higher): second wave'),
    (48.00, 0.5, 'gust', 'gust 3 (highest): third wave catches the spinner, it squashes flat'),
    (48.00, 0.5, 'thwump', 'cannon thwump and slingshot twang: the spinner is flung north, the camera launches after it'),
    (48.20, 2.2, 'roar', 'doppler roar bed with rattle, whine rising (48.2-50.4): travel up the bent lane, red-hot wake; music: the ostinato doubles in tempo'),
    (49.10, 0.3, 'vwip', 'pass-by vwip: the spinner blasts past the speed sign'),
    (49.12, 0.9, 'ratchet', 'sign-spin ratchet: the sign spins two turns on its pin in the wake'),
    (50.30, 0.6, 'ting', 'sign settles on 100 (ting)'),
]

if __name__ == '__main__':
    mc.main(sys.modules[__name__])
