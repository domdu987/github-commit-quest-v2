#!/usr/bin/env python3
"""Take s24 = shot 24 (57.349-59.607, film g 1720..1787, handle out 5): beach, storm. THE WAVE.

HARD CUT in (3 frames before 'มันคือ') to the low angle beach_low_wave on the axis of the beach framing, turned toward the sea: close
on the two shocked faces (near head about 300 px), a near-hold of 6 frames; crash pull-out x0.27 (57.55-58.15) with a tilt up that
keeps going as a drift: behind them a cottage (one cottage stood seaward of the fence for this shot, front to the lens, lit windows)
and behind and above it the fog bank is a wall of water (the set's mesh wave, set_wave, growing about 6 %/s); by 'สูงกว่า บ้านทั้งหลัง'
the pitch is +30 deg, the cottage small at the bottom of the frame, the crest at the top. 5 Hz shake from 58.3. beach_man and
beach_woman shocked (ring eyes, sweat, focus lines), his boater pops off at 57.5 and sails away (the extension's flying boater
card); they jump (squash, leap, hang, land) and run to screen right and out (58.0-58.7). Puppets tinted (0.71, 0.71, 0.94).
Out: object wipe (the foam sheet crossing the lens) added by the conform step: clean frames plus a 5-frame handle out.
    python3 shot.py probe|still|draft|render|post|qa   (see set3d_ext/beach/bshot.py)"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d_ext', 'beach'))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'acting'))
import bshot as BS                                    # noqa: E402
import acting as AC                                   # noqa: E402
P = AC.P
gf, smooth, smoother, lerp, clamp = BS.gf, BS.smooth, BS.smoother, BS.lerp, BS.clamp

TAKE, SHOTS, LIGHT, VERSION = 's24', [24], 'storm', 1
G0, G1 = 1720, 1788                                    # round(57.349 * 30), round(59.607 * 30)
H_IN, H_OUT = 0, 5                                     # hard cut in; 6-frame object wipe out (3 + 2)
R0, R1 = G0 - H_IN, G1 + H_OUT
TRANSITION_IN = dict(type='cut', frames=0, note='HARD CUT, 3 frames before the word: the fog bank is a wall of water')
TRANSITION_OUT = dict(type='object_wipe', frames=6, note='the foam sheet crosses the lens (conform overlay); clean frames delivered with 5 handle frames')

SHOCK = 57.42                                          # shocked swap (behind a blink), hat pop starts
HATFLY = gf(57.52)                                     # 1729 the flying boater card takes over
PULL = (gf(57.55), gf(58.15))                          # 1730 -> 1748 crash pull-out x0.27
JUMP = 57.73                                           # squash 2, leap 2, hang 2, land 2 -> run from 58.0
SHAKE = gf(58.3)                                       # 1752 5 Hz shake
HIGHER = gf(59.08)                                     # 1775 'บ้านทั้งหลัง': pitch +30

AZ = math.radians(12.0)                                # the beach framing's axis (-3.9 deg) turned about 15 deg toward the sea
FWD = (math.cos(AZ), math.sin(AZ), 0.0)
RIGHT = (math.sin(AZ), -math.cos(AZ), 0.0)             # screen right on the sand = away from the sea

MAN = (1.0, 9.0, 0.0)
WOMAN = (2.3, 10.75, 0.0)

# ----------------------------------------------------------------------------- camera
def _dir(az, pi):
    return (math.cos(pi) * math.cos(az), math.cos(pi) * math.sin(az), math.sin(pi))

D0, D1 = 2.45, 10.6                                    # horizontal lens distance to the man before and after the pull-out
Z0, Z1 = 1.30, 0.70

def _pose(g):
    """distance, height, pitch (deg), yaw offset (deg) without the shake."""
    if g < PULL[0]:
        k = (g - R0) / 30.0
        return D0 + 0.06 * k + 0.25 * k * k, Z0, 15.0 + 1.4 * k + 2.0 * k * k, 6.0 - 1.0 * k                    # the near-hold: a creep, never parked
    if g < PULL[1]:
        x = (g - PULL[0] + 1) / float(PULL[1] - PULL[0] + 1); s = smoother(x) * 0.75 + (1 - (1 - x) ** 3) * 0.25
        d0, z0, p0, _ = _pose(PULL[0] - 1)
        return d0 + (D1 - d0) * s, z0 + (Z1 - z0) * s, p0 + (21.0 - p0) * s, (6.0 - 1.0 * (PULL[0] - 1 - R0) / 30.0) * (1 - s) - 3.0 * s
    d1, z1, p1, y1 = D1, Z1, 21.0, -3.0
    k = (g - PULL[1]) / 30.0
    u = clamp((g - PULL[1]) / float(HIGHER - PULL[1]))
    pitch = p1 + 9.0 * u ** 1.35 + 2.0 * max(0.0, (g - HIGHER) / 30.0)                # tilt keeps going: +30 on 'บ้านทั้งหลัง', then a slow drift
    v = clamp((g - PULL[1]) / 16.0)
    return d1 + 0.25 * k, z1, pitch, y1 + 10.0 * (1 - (1 - v) ** 2) + 1.2 * k            # and turns toward the sea (the wave)

def cam(g):
    d, z, pitch, yaw = _pose(g)
    loc = (MAN[0] - d * FWD[0], MAN[1] - d * FWD[1], z)
    a = 0.0
    if g >= SHAKE:                                     # 5 Hz shake, about 86 px peak to peak in pitch (3.2 deg), smaller in yaw
        e = smooth(SHAKE, SHAKE + 4, g); t = (g - SHAKE) / 30.0
        pitch += e * 3.15 * (0.8 * math.sin(2 * math.pi * 5.0 * t) + 0.2 * math.sin(2 * math.pi * 7.3 * t + 1.1))
        yaw += e * 1.2 * math.sin(2 * math.pi * 5.0 * t + 1.7)
    dd = _dir(AZ + math.radians(yaw), math.radians(pitch))
    return loc, tuple(loc[i] + 10.0 * dd[i] for i in range(3))

# ----------------------------------------------------------------------------- set state
def state(g):
    t = (g - R0) / 30.0
    return dict(fog=1.0, fog_r=1.0, rain=0.55, wind=0.9 + 0.1 * smooth(SHAKE - 6, SHAKE, g), sea=3.0 + 1.6 * t,
                wave=0.84 + 0.06 * t + 0.02 * t * t, sign_sw=0.10, windows=0.95, shutters=smooth(gf(58.6), gf(58.8), g), towel_on=1.0,
                vane=60.0 + 25.0 * math.sin(g * 0.9))

# ----------------------------------------------------------------------------- actors
TINT = '#b5b5f0'                                       # (0.71, 0.71, 0.94) as the puppet's hex tint
ACTORS = [dict(name='man24', cast='beach_man', ppd=320, shadow='proxy', contact=True),
          dict(name='woman24', cast='beach_woman', ppd=256, shadow='proxy', contact=True)]

RUN_SPEED = 6.2                                        # D/s (the walk at double rate, pushed): out at screen right by about 58.7

def _strip(p): return {k: v for k, v in p.items() if not k.startswith('_')}

def _pose_of(cast, g, jump, shock):
    T = g / 30.0 - 0.1
    sh = AC.beach_shocked(T - shock + 0.1, 0.1, cast=cast, facing=-1, hat_pop=(cast == 'beach_man'), focus=True)
    jr = AC.jump_run(T - jump, 0.0, cast=cast, facing=1, height=0.55, run_speed=RUN_SPEED, hat_off=(cast == 'beach_man'))
    fj = gf(jump)
    if g < fj - 1: p, lift, adv = sh, 0.0, 0.0
    elif g < fj + 1:
        p = P.lerp_pose(cast, _strip(sh), _strip(jr), (g - (fj - 1)) / 2.0); lift, adv = jr.get('_lift', 0.0), jr.get('_adv', 0.0)
    else: p, lift, adv = jr, jr.get('_lift', 0.0), jr.get('_adv', 0.0)
    q = _strip(p); q['tint'] = TINT
    return q, lift, adv

def _feet(base, lift, adv):
    return (base[0] + RIGHT[0] * adv, base[1] + RIGHT[1] * adv, base[2] + lift)

def actors(g):
    pm, lm, am = _pose_of('beach_man', g, JUMP, SHOCK)
    pw, lw, aw = _pose_of('beach_woman', g, JUMP + 0.07, SHOCK + 0.03)
    return {'man24': dict(feet=_feet(MAN, lm, am), pose=pm), 'woman24': dict(feet=_feet(WOMAN, lw, aw), pose=pw)}

def boater(g):
    """the flying boater: leaves the man's head at 57.52, sails up and inland (screen right) with a spin, out of frame."""
    if g < HATFLY: return None
    t = (g - HATFLY) / 30.0
    h = (MAN[0], MAN[1], 3.25)
    up = 2.6 * t + 1.6 * t * t; side = 1.4 * t + 2.2 * t * t
    loc = (h[0] + RIGHT[0] * side - FWD[0] * 0.6 * t, h[1] + RIGHT[1] * side - FWD[1] * 0.6 * t, h[2] + up)
    return dict(loc=loc, spin=-25.0 - 420.0 * t, scale=0.55)

CUES = [
    (57.25, 0.2, 'hit', 'orchestra hit on the hard cut, then 6 frames of near silence'),
    (57.40, 0.3, 'gasp', 'two gasps (non-verbal): the shocked swap, focus lines (g1719-1723)'),
    (57.50, 0.3, 'pop', 'hat pop: the boater flies off (g1729 on)'),
    (57.60, 0.6, 'whoosh', 'crash whoosh out: the pull-out (g1730-1748); the roar swells to 59.6 (loudest sound of the film)'),
    (57.73, 0.27, 'jump', 'jump scare: squash, leap, hang, land'),
    (58.00, 0.6, 'steps', 'running steps on sand (they run out at screen right)'),
    (58.30, 1.3, 'rumble', 'ground rumble, timber creaks, wires whine (the shake starts, g1752)'),
    (58.80, 0.6, 'shutters', 'shutters bang x3, buoy bell'),
    (59.45, 0.4, 'crash', 'wave crash, white roar carried over the wipe'),
]

# ----------------------------------------------------------------------------- one cottage stood seaward of the fence (this take only)
DUP_FROM = 'cottage_06'
DUP_AT = (19.2, 9.4)                                   # under the curl; front (porch) turned to the lens (+90 deg)
DUP_ROT = 90.0

def _patch():
    import beach_ext as BX
    import bshot
    if getattr(BX, '_s24', False): return
    orig = BX.build
    def build(light='grey_drizzle', clear=True, dressing=True, boater=False):
        A = orig(light, clear=clear, dressing=dressing, boater=True)
        import bpy
        from mathutils import Matrix, Vector
        B = BX.B; S = BX.S
        c = next(c for c in B.STATE['A']['cottages'] if c['name'] == DUP_FROM)
        ox, oy = c['center'][0], c['center'][1]
        M = Matrix.Translation((DUP_AT[0], DUP_AT[1], 0.0)) @ Matrix.Rotation(math.radians(DUP_ROT), 4, 'Z') @ Matrix.Translation((-ox, -oy, 0.0))
        src = bpy.data.objects[DUP_FROM]; dup = src.copy(); dup.name = 'cottage_s24'
        for col in src.users_collection: col.objects.link(dup)
        dup.matrix_world = M @ src.matrix_world
        coll = S._coll('BEACH_EXT', bpy.context.scene)
        x0, x1 = c['x']; sc = (x1 - x0) / B.BT.W_C; yf = c['y_front'] + 0.012; zf = B.BT.Z_FLOOR * sc
        mb = S.MB(); gm = BX._glow_mat()
        for wx in (x0 + 0.62 * sc, x1 - 0.62 * sc):
            w, h = 0.40 * sc, 0.60 * sc; zb = zf + (1.6 - 0.72 + 0.06) * sc
            mb.quad((wx - w / 2, yf, zb), (w, 0, 0), (0, 0, h), gm)
        wo = mb.obj('s24_windows', coll); S.no_bounce(wo); wo.visible_shadow = False; wo.matrix_world = M @ wo.matrix_world
        for o in bpy.data.objects:                     # 'No readable text': the LONG ISLAND board is hidden for this take
            if o.name.startswith('li_sign'): o.hide_render = True
        if 'boat' in bpy.data.objects:                 # the rowing boat sat in the lower left corner as a big grey block: hidden for this take
            for o in bpy.data.objects:
                if o.name.startswith('boat'): o.hide_render = True
        A['s24'] = dict(cottage=dup.name, at=DUP_AT, ridge=c.get('ridge'))
        return A
    BX.build = build; BX._s24 = True
    # key the flying boater with the rest of the frame
    okey = bshot.Take.key
    def key(s, g):
        first = g not in s.keyed
        okey(s, g)
        if first:
            b = boater(g); f = BS.bf(g)
            if b is None: BX.set_boater(f, visible=False)
            else: BX.set_boater(f, b['loc'], b['spin'], b['scale'], True, cam=s.cam)
    bshot.Take.key = key

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('probe', 'still', 'draft', 'render'): _patch()
    BS.run(sys.modules[__name__], sys.argv[1:])
