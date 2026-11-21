#!/usr/bin/env python3
"""s12 (film 22) mapworld ride-along on the red line.  g 1485..1558 (+6 handles each side).
    python3 shot.py stills 1479:1565:6 <out> [scale%] [samples]      python3 shot.py final 1479:1565 <out>
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, U, bpy, V = C.B, C.U, C.bpy, C.V
import beck_map as M
F0, F1 = 1485, 1559
XY, CUM = M.line_path('red')
RING = M.w_xy(16, 9)               # (30, 0)

def s_of(f):
    u = C.clamp(f / 74.0); return 70.0 + 102.0 * (0.30 * u + 0.70 * (1 - (1 - u) ** 2))

def P(s): return M.path_at(XY, CUM, s)

def cam_at(f):
    s = s_of(f); (px, py), (tx, ty) = P(s - 15.0); (lx, ly), (ltx, lty) = P(s + 16.0)
    nx, ny = ty, -tx                                  # right-hand normal
    k = f / 74.0
    off = 6.5 - 1.5 * k
    z = 9.5 + 2.5 * k
    return ((px + nx * off, py + ny * off, z), (lx - nx * 4.5, ly - ny * 4.5, 0.6), 24.0)

def _sph(v):
    r = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2); el = math.asin(v[2] / r); az = math.atan2(v[1], v[0]); return r, el, az
def _fromsph(r, el, az): return (r * math.cos(el) * math.cos(az), r * math.cos(el) * math.sin(az), r * math.sin(el))
# join with s11: f0 looks (almost) straight down on the paper centre (the pocket-map strip, about 100 x 178 D at z 67), then dives and banks into the ride at f26
DIVE = 36
_c26 = cam_at(DIVE)
_T0 = (0.0, 0.0, 0.0); _O0 = (0.0, -12.0, 66.0)
_O26 = tuple(_c26[0][i] - _c26[1][i] for i in range(3))
_r0, _e0, _a0 = _sph(_O0); _r1, _e1, _a1 = _sph(_O26)
while _a1 - _a0 > math.pi: _a1 -= 2 * math.pi
while _a1 - _a0 < -math.pi: _a1 += 2 * math.pi
def dive(f):
    u = C.ez(f / float(DIVE)); T = tuple(_T0[i] + (_c26[1][i] - _T0[i]) * u for i in range(3))
    O = _fromsph(_r0 + (_r1 - _r0) * u, _e0 + (_e1 - _e0) * u, _a0 + (_a1 - _a0) * u)
    return (tuple(T[i] + O[i] for i in range(3)), T, 24.0)
CAM = [(f,) + dive(f) for f in (0, 5, 10, 15, 20, 25, 30, 33)] + [(f,) + cam_at(f) for f in range(DIVE, 75, 5)] + [(74,) + cam_at(74)]

WALK = []
def post_build():
    for ob in M.CARS: ob.scale = (0.95, 0.95, 0.95)
    tg = C.obj('tag_change')
    cx, cy, cz = RING[0], RING[1] + 7.2, 3.0
    tg.scale = (1.6, 1.6, 1.6); tg.location = (cx - 1.6 * cx, cy - 1.6 * cy, cz - 1.6 * cz)
    C.scale_lights('key_sun', 0.88); C.tint_emission('BK_e_pp_LONDON', (1.0, 0.74, 0.42)); C.scale_emission('BK_e_pp_LONDON', 0.85)
    for i in range(4):                       # passengers who step off the train at the ring (new cards, so no name clash with the ring crowds)
        nm = 'wp%d' % i
        U.crowd_card(nm, i + 7, 'pass_walk', (RING[0] - 8.0 + i * 1.1, RING[1] - 3.0 - i * 1.0, 0.8), scale=0.42, rim='#ffd08a', shadow=True, mirror=False)
        WALK.append((nm, i))
    C.mount([o.name for o in C.bpy.context.scene.objects if o.name.startswith(('car', 'lt_'))])

def animate(f, n):
    s = s_of(f)
    M.place_train(s)
    for ob in M.CARS: ob.scale = (0.95, 0.95, 0.95); ob.location.z = 0.62 * 0.95 / 0.62 * 0.62
    M.place_line_trains(f); U.face_cards()
    for nm, i in WALK:                                   # 50.80 s (f 42): passengers step off at the ring and walk to the blue line
        u = C.ez((f - 40 - 2 * i) / 26.0)
        a = (RING[0] - 8.0 + i * 1.1, RING[1] - 3.0 - i * 1.0); b = (RING[0] + (-4.0, 3.5, -3.0, 4.0)[i], RING[1] + (8.5, -8.5, -9.0, 7.0)[i])
        C.move_card(nm, a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, 0.8)

if __name__ == '__main__':
    C.drive('s12', CAM, 'mapworld', 'MAPWORLD', animate, post_build, sys.argv[1:], F0, F1)
