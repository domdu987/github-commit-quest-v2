#!/usr/bin/env python3
"""shot.py -- film 19 take s02 = the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H).  g 57..190 (1.91-6.37 s, 134 frames) + 9 handle frames each side
(hard cut in from s01 at g 57; DISSOLVE 13 f out into s04 at g 191): g 48..199.

ONE continuous eased camera move, no cut.  SHIP ship_aerial / NOON (set_sea + set_roll keyed on every frame):
  START  extreme wide from high above and behind: the lone warship on the endless glittering sea, small in the frame; captain19 and astro19_c on the
         quarterdeck are ~6 px tall (under 5 % of the frame), findable
  MIDDLE the camera descends and pushes in toward the stern, passing the spanker sail (a fore-and-aft sail, 1.8 D from the lens) as a parallax foreground
  END    (by ~5.9 s, g 177) a MEDIUM shot on the quarterdeck: captain19 holds a blank sea chart, astro19_c squints through a quadrant at the sky and
         scratches his head (g ~150-165); 35-60 % of the frame height; the camera rides the deck (C.on_ship)
No mouth movement.  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
TAKE = "s02"
PRESET, LIGHT = "ship_aerial", "NOON"
G0, G1 = 57, 191                                         # shot = g 57..190
H_IN, H_OUT = 9, 9
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 48..199
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 10
S = 1.85
PPD = 224                                                # sprite px per D (head ~110 px at the end; the start is downsampled)
G_ARRIVE = 182                                           # the medium shot is reached (5.9 s)
G_SCRATCH = (155, 175)       # head scratch; 157-190 the whole puzzled beat                                   # astro19_c scratches his head (comic), 4.9-5.5 s
BLINKS_C, BLINKS_A = [70, 128, 171], [92, 150, 188]

# ----------------------------------------------------------------------------- staging (ship rest frame = world D at t = 0; z of the quarterdeck 14.34)
Z_QD = 14.34 + 0.22                                        # the deck plus the shoe sole (the card base sat 0.2 D low)
CAP_XY = (-0.75, -31.3)                                  # captain19, beside the wheel, camera-left
AST_XY = (1.7, -30.6)                                   # astro19_c, camera-right (short: 2.8 D)

# ----------------------------------------------------------------------------- camera: a spline through key poses in the SHIP's rest frame (D), eased in and out
KEYS = [  # (u, loc, look)
    (0.00, (30.0, -530.0, 395.0), (0.0, -14.0, 14.0)),            # truly extreme wide: ~640 D away, the ship <= 12 % of the frame height, the crew ~4 px
    (0.50, (13.0, -125.0, 96.0), (1.0, -30.0, 15.0)),             # descending
    (0.76, (6.2, -52.0, 46.0), (0.8, -30.5, 16.0)),               # high over the stern, level with the mizzen yards / sails
    (0.91, (3.1, -40.5, 31.0), (0.6, -30.3, 16.0)),               # passes the spanker sail at ~1.9 D and the rigging, then dives
    (1.00, (0.45, -36.3, 16.5), (0.5, -30.0, 15.9)),              # medium on the quarterdeck
]


def _cr(p0, p1, p2, p3, t):
    """Catmull-Rom, uniform"""
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t)


TM = [(48, 0.0), (66, 0.07), (90, 0.27), (112, 0.52), (125, 0.66), (140, 0.80), (182, 1.0)]    # g -> FRACTION OF THE PATH LENGTH (ease in, one speed hump, ease OUT over g 138-170)


def _slopes():
    """Fritsch-Carlson monotone cubic slopes at the knots (C1: no velocity dips at the knots; zero speed at the landing)"""
    n = len(TM)
    h = [TM[i + 1][0] - TM[i][0] for i in range(n - 1)]
    d = [(TM[i + 1][1] - TM[i][1]) / h[i] for i in range(n - 1)]
    m = [d[0]] + [0.0 if d[i - 1] * d[i] <= 0 else 2 * d[i - 1] * d[i] / (d[i - 1] + d[i]) for i in range(1, n - 1)] + [0.0]
    m[0] = 0.5 * d[0]                                                      # a gentle ease-in, never a dead start
    return m


_M = _slopes()


G_FLOW0 = 140
FLOW_T = [(140, 5.4), (146, 5.0), (156, 4.5), (164, 4.0), (170, 2.9), (174, 1.9), (178, 1.0), (182, 0.0)]     # px/frame of the rigging / sail background at 360 wide
_FPTS = [Vector(p) for p in ((0.5, -26, 24), (2.5, -22, 20), (-2.5, -24, 22), (4, -27, 18), (1.0, -18, 16.5), (-3, -28, 17))]
_FU = {}


def _flow_per_du(u):
    """background screen speed (px at 360 wide) per unit of the spline parameter u"""
    ua, ub = _u_of_s(u), _u_of_s(min(1.0, u + 1e-3))                      # u here is the eased path fraction s (the spline is reparametrised by log distance)
    a, b = _spline_u(ua, 1), _spline_u(ub, 1)
    la, lb = _spline_u(ua, 2), _spline_u(ub, 2)
    tot = 0.0
    for P in _FPTS:
        pts = []
        for (loc, look) in ((a, la), (b, lb)):
            f = (look - loc).normalized(); r = Vector((f.y, -f.x, 0.0)).normalized(); up = r.cross(f)
            d = P - loc; z = d.dot(f)
            pts.append((360 + 782.2 * d.dot(r) / z, 640 - 782.2 * d.dot(up) / z))
        tot += math.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1]) / 2.0
    return tot / len(_FPTS) / 1e-3


def _flow_u(k):
    """integrate du/dg = k * F(g) / q(u) from g = G_FLOW0 (u0 = the table's value) to G_ARRIVE; returns the u(g) table"""
    u = _umap_tm(G_FLOW0)
    out = {G_FLOW0: u}
    for g in range(G_FLOW0, G_ARRIVE + 4):
        Fg = None
        for i in range(len(FLOW_T) - 1):
            if FLOW_T[i][0] <= g <= FLOW_T[i + 1][0]:
                t = (g - FLOW_T[i][0]) / float(FLOW_T[i + 1][0] - FLOW_T[i][0]); t = t * t * (3 - 2 * t)
                Fg = FLOW_T[i][1] + (FLOW_T[i + 1][1] - FLOW_T[i][1]) * t
        if Fg is None:
            Fg = FLOW_T[-1][1]
        u = min(1.0, u + k * Fg / max(1e-6, _flow_per_du(min(u, 0.999))))
        out[g + 1] = u
    return out


def _flow_table():
    if not _FU:
        lo, hi = 0.3, 3.0
        for _ in range(30):                                                      # bisect k so that u reaches 1 exactly at G_ARRIVE
            k = 0.5 * (lo + hi)
            if _flow_u(k)[G_ARRIVE] < 0.9995:
                lo = k
            else:
                hi = k
        _FU.update(_flow_u(0.5 * (lo + hi)))
    return _FU


def _umap(g):
    return _umap_tm(g)


def _umap_tm(g):
    if g <= TM[0][0]:
        return 0.0
    if g >= TM[-1][0]:
        return 1.0
    j = max(i for i in range(len(TM) - 1) if TM[i][0] <= g)
    (g0_, u0_), (g1_, u1_) = TM[j], TM[j + 1]
    h = g1_ - g0_
    t = (g - g0_) / float(h)
    h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
    return h00 * u0_ + h10 * h * _M[j] + h01 * u1_ + h11 * h * _M[j + 1]


_ARC = []


def _u_of_s(sf):
    """the spline is reparametrised by LOG DISTANCE to the pair (equal steps = equal zoom rate, so the image speed has ONE hump and an ease-out): s (0..1) -> the spline parameter u"""
    if not _ARC:
        N = 1800
        C0 = Vector((0.5, -30.5, 15.9))                                    # the pair: the zoom is measured toward it
        lg = [math.log((_spline_u(i / float(N), 1) - C0).length) for i in range(N + 1)]
        cum = [lg[0] - v for v in lg]                                      # progress in LOG distance (equal steps = equal zoom rate)
        for i in range(1, len(cum)):
            cum[i] = max(cum[i], cum[i - 1] + 1e-9)
        _ARC.extend([c / cum[-1] for c in cum])
    lo, hi = 0, len(_ARC) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _ARC[mid] <= sf:
            lo = mid
        else:
            hi = mid
    f = (sf - _ARC[lo]) / max(1e-9, _ARC[hi] - _ARC[lo])
    return (lo + f) / float(len(_ARC) - 1)


def _spline(g, which):
    return _spline_u(_u_of_s(_umap(g)), which)


def _spline_u(u, which):
    """position on the key spline at the parameter u (which 1 = loc, 2 = look)"""
    P = [Vector(k[which]) for k in KEYS]
    us = [k[0] for k in KEYS]
    j = max(i for i in range(len(us) - 1) if us[i] <= u) if u < 1.0 else len(us) - 2
    tt = (u - us[j]) / (us[j + 1] - us[j])
    p0 = P[j - 1] if j > 0 else P[j] * 2 - P[j + 1]
    p3 = P[j + 2] if j + 2 < len(P) else P[j + 1] * 2 - P[j]
    return Vector([_cr(p0[i], P[j][i], P[j + 1][i], p3[i], tt) for i in range(3)])


G_W0 = 96
FLOW_W = [(96, 1.5), (104, 2.4), (112, 3.2), (120, 4.4), (125, 5.4), (131, 6.2), (136, 6.0), (146, 5.0), (156, 4.5), (164, 4.0), (170, 2.9), (174, 1.9), (178, 1.1), (182, 0.0)]   # target background flow (px/frame at 360 wide)
_TAU = {}


def _fw(g):
    for i in range(len(FLOW_W) - 1):
        if FLOW_W[i][0] <= g <= FLOW_W[i + 1][0]:
            t = (g - FLOW_W[i][0]) / float(FLOW_W[i + 1][0] - FLOW_W[i][0]); t = t * t * (3 - 2 * t)
            return FLOW_W[i][1] + (FLOW_W[i + 1][1] - FLOW_W[i][1]) * t
    return 0.0


def _path_flow(tau):
    """background flow (px/frame at 360 wide) of the landing path (spline + aim) at path time tau"""
    a, b = _land_raw(tau), _land_raw(tau + 0.25)
    tot = 0.0
    for P in _FPTS:
        pts = []
        for (loc, look) in (a, b):
            f = (look - loc).normalized(); r = Vector((f.y, -f.x, 0.0)).normalized(); up = r.cross(f)
            d = P - loc; z = d.dot(f)
            pts.append((360 + 782.2 * d.dot(r) / z, 640 - 782.2 * d.dot(up) / z))
        tot += math.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1]) / 2.0
    return tot / len(_FPTS) / 0.25


def _land_raw(tau):
    """the landing path BEFORE the time warp: the spline + the look-up aim, at path time tau"""
    loc, look = _spline(min(tau, G_ARRIVE), 1), _spline(min(tau, G_ARRIVE), 2)
    uu = _umap(min(tau, G_ARRIVE))
    look = look + Vector((0.0, 0.0, 0.30 * (lambda t: t * t * (3 - 2 * t))(clamp((uu - 0.05) / 0.95))))
    return loc, look


def _tau_of_old(g):
    """time warp g -> path time tau for g in [G_W0, G_ARRIVE]: the path is re-timed so the measured background flow equals FLOW_W exactly (monotone from the g 131 peak)"""
    if not _TAU:
        n = int((G_ARRIVE - G_W0) / 0.25)
        A = [0.0]
        for i in range(n):
            A.append(A[-1] + _path_flow(G_W0 + i * 0.25) * 0.25)
        G = [0.0]
        for g_ in range(G_W0, G_ARRIVE):
            G.append(G[-1] + _fw(g_ + 0.5))
        k = A[-1] / G[-1]
        _TAU["k"] = k
        for gi in range(G_W0, G_ARRIVE + 1):
            tgt = G[gi - G_W0] * k
            lo, hi = 0, n
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if A[mid] <= tgt:
                    lo = mid
                else:
                    hi = mid
            f = (tgt - A[lo]) / max(1e-9, A[hi] - A[lo])
            _TAU[gi] = G_W0 + (lo + f) * 0.25
    if g <= G_W0:
        return float(g)
    if g >= G_ARRIVE:
        return float(G_ARRIVE)
    i = int(g); fr = g - i
    return _TAU[i] * (1 - fr) + _TAU[min(i + 1, G_ARRIVE)] * fr


# ---- round 14: for g < G_NEW1 the warp is re-derived with a flow measure that includes the NEAR DECK and the horizon (QA: the pitch from top-down to eye level showed mostly
# in the deck / top frame, which the rigging points missed): one rise to a peak at g 131, then a monotone fall, ending exactly where round 13's warp is at g 160.
G_NEW1 = 160
_DPTS = [Vector(p) for p in ((0.5, -33.5, 14.3), (-1.5, -31.8, 14.3), (2.5, -31.5, 14.3), (0.5, -29.0, 14.3), (-3.0, -34.0, 14.3), (4.0, -35.0, 14.3),
                              (0.5, 300.0, 16.0), (-80.0, 300.0, 16.0), (80.0, 300.0, 16.0))]
_TAU2 = {}


_SMP = {}
G_S0 = 108.0                                   # the smoothing blends in from path time 108 and out at the round-13 g160 path time (so g >= 160 is EXACTLY unchanged)


def _land(tau):
    """round 15: the landing path with a Gaussian (sigma 5 frames of path time) smoothing of BOTH loc and look over tau 108..tau160: the aim's pitch / yaw turn-around (it
    tilts down to -59 deg at g 126 and back up) is spread over >= 8 frames instead of 2; weight 0 at tau >= tau160 and below 108 (exact there)"""
    t160 = _tau_of_old(G_NEW1)
    if tau <= G_S0 or tau >= t160:
        return _land_raw(tau)
    q = tau * 4.0; i0 = int(math.floor(q)); fr = q - i0                       # cache on a 0.25-frame grid and interpolate linearly (no quantisation noise)
    a_, b_ = _land_grid(i0, t160), _land_grid(i0 + 1, t160)
    return (a_[0] * (1 - fr) + b_[0] * fr, a_[1] * (1 - fr) + b_[1] * fr)


def _land_grid(key, t160):
    tau = key / 4.0
    if tau <= G_S0 or tau >= t160:
        return _land_raw(tau)
    if key in _SMP:
        return _SMP[key]
    w_in = clamp((tau - G_S0) / 16.0); w_in = w_in * w_in * (3 - 2 * w_in)
    w_out = clamp((t160 - tau) / 12.0); w_out = w_out * w_out * (3 - 2 * w_out)
    w = min(w_in, w_out)
    raw = _land_raw(tau)
    ks = [math.exp(-0.5 * (k / 5.0) ** 2) for k in range(-15, 16)]
    tot = sum(ks)
    loc = Vector((0.0, 0.0, 0.0)); look = Vector((0.0, 0.0, 0.0))
    for k, wk in zip(range(-15, 16), ks):
        l, lk = _land_raw(min(max(tau + k, 96.0), t160 + 30.0))
        loc += l * (wk / tot); look += lk * (wk / tot)
    out = (raw[0] * (1 - w) + loc * w, raw[1] * (1 - w) + look * w)
    _SMP[key] = out
    return out


_SPTS = [Vector(p) for p in ((0.5, -27.0, 14.3), (-3.0, -26.0, 14.3), (4.0, -25.0, 14.3), (0.5, -22.0, 14.5), (8.5, -22.0, 14.5), (-8.5, -22.0, 14.5), (8.0, -14.0, 12.5),
                              (-8.0, -14.0, 12.5), (0.0, -10.0, 10.0), (0.0, 40.0, 14.0), (0.0, -25.0, 60.0), (0.0, 5.0, 70.0))]     # forward deck, hull sides, bow, mast tops: rigid ship features (always >= 5 D ahead)
_TAU2 = {}


def _path_flow2(tau):
    """camera POSITION speed (D per frame of path time) of the smoothed landing path: with the pitch now designed separately (_aim_design) the position speed is what the warp
    shapes (a rise to one peak, then a monotone fall that meets round 13's speed at g 160)"""
    a, b = _land(tau), _land(tau + 0.25)
    return (b[0] - a[0]).length / 0.25


def _tau_of(g):
    if g >= G_NEW1:
        return _tau_of_old(g)
    if g <= G_W0:
        return float(g)
    if not _TAU2:
        tau160 = _tau_of_old(G_NEW1)
        n = int(round((tau160 - G_W0) / 0.25))
        A = [0.0]
        for i in range(n):
            A.append(A[-1] + _path_flow2(G_W0 + i * 0.25) * 0.25)
        v0 = _path_flow2(G_W0)
        v1 = _path_flow2(tau160 - 0.25) * (_tau_of_old(G_NEW1 + 1) - _tau_of_old(G_NEW1))
        lv0, lv1 = math.log(max(v0, 1e-4)), math.log(max(v1, 1e-4))
        def prof(g_, al):
            t = clamp((g_ - G_W0) / float(G_NEW1 - G_W0))
            return math.exp(lv0 + (lv1 - lv0) * (t ** al))                       # monotone fall of the camera speed from round 13's value at g 96 to its value at g 160
        def total(al):
            return sum(prof(G_W0 + i + 0.5, al) for i in range(G_NEW1 - G_W0))
        lo, hi = 0.05, 12.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if total(mid) < A[-1]:                                               # larger alpha = slower fall = more length
                lo = mid
            else:
                hi = mid
        vp = 0.5 * (lo + hi)
        _TAU2["vp"] = vp; _TAU2["v0"] = v0; _TAU2["v1"] = v1
        G = [0.0]
        for g_ in range(G_W0, G_NEW1):
            G.append(G[-1] + prof(g_ + 0.5, vp))
        raw_tau = []
        for gi in range(G_W0, G_NEW1 + 1):
            tgt = G[gi - G_W0]
            lo_, hi_ = 0, n
            while hi_ - lo_ > 1:
                m_ = (lo_ + hi_) // 2
                if A[m_] <= tgt:
                    lo_ = m_
                else:
                    hi_ = m_
            f = (tgt - A[lo_]) / max(1e-9, A[hi_] - A[lo_])
            raw_tau.append(G_W0 + (lo_ + f) * 0.25)
        # smooth the per-frame warp steps over g 120-134 (QA: a 1.65-frame step at g 127 between 1.28 and 1.09), keeping both ends exact
        for it in range(0):                                                       # (the exact warp is already smooth; the extra filter created a dip at g 136)
            sm = list(raw_tau)
            for gi in range(120, 135):
                i = gi - G_W0
                sm[i] = 0.25 * raw_tau[i - 1] + 0.5 * raw_tau[i] + 0.25 * raw_tau[i + 1]
            raw_tau = sm
        for gi, t_ in zip(range(G_W0, G_NEW1 + 1), raw_tau):
            _TAU2[gi] = t_
    i = int(g); fr = g - i
    return _TAU2[i] * (1 - fr) + _TAU2[min(i + 1, G_NEW1)] * fr


_AD = {}
G_A0, G_A1 = 108, 160


def _aim_design(g, loc, look):
    """round 15 (QA: the aim tilts down to -59 deg at g 126 and back up, the turn-around squeezed into 2 frames, then the turning speed drops and climbs again = a second move):
    for g 108-160 the PITCH of the view direction follows a designed schedule (rate crosses zero over >= 8 frames: -0.5 deg/frame at g 112 -> 0 at g 124 -> ~1.0 at g 134 -> ~1.3
    at g 148 -> the raw rate at g 160), the YAW is the Gaussian-smoothed raw yaw; the distance to the aim point and the position are the path's.  Both are blended to the raw path
    at g 108 and g 160 (values and rates match there), so g >= 160 is EXACTLY unchanged."""
    if g < G_A0 or g > G_A1:
        return loc, look
    if not _AD:
        def raw(gi):
            l, k = _land(_tau_of(gi)); d = k - l
            return math.degrees(math.atan2(d.z, math.hypot(d.x, d.y))), math.degrees(math.atan2(d.x, d.y)), d.length
        R = {gi: raw(gi) for gi in range(G_A0 - 20, G_A1 + 21)}
        p0, p1 = R[G_A0][0], R[G_A1][0]
        s0 = R[G_A0 + 1][0] - R[G_A0 - 1][0]; s0 *= 0.5                         # raw pitch rate at the start (deg / frame)
        s1 = (R[G_A1 + 1][0] - R[G_A1 - 1][0]) * 0.5
        sm = lambda t: t * t * (3 - 2 * t)
        # rate schedule: start rate s0 -> 0 at g 124 (smoothly) -> up to 1.0 at g 134 -> 1.3 at g 148 -> s1 at g 160, amplitude of the rising part solved so p(160) = p1
        def rate(gi, k):
            if gi <= 124:
                return s0 * (1 - sm(clamp((gi - G_A0) / 16.0)))
            if gi <= 134:
                return k * 1.0 * sm((gi - 124) / 10.0)
            if gi <= 148:
                return k * (1.0 + 0.3 * sm((gi - 134) / 14.0))
            return k * 1.3 + (s1 - k * 1.3) * sm((gi - 148) / 12.0)
        def total(k):
            return p0 + sum(rate(gi + 0.5, k) for gi in range(G_A0, G_A1))
        lo, hi = 0.2, 3.0
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if total(mid) < p1:
                lo = mid
            else:
                hi = mid
        k = 0.5 * (lo + hi)
        _AD["k"] = k
        p = p0
        for gi in range(G_A0, G_A1 + 1):
            _AD[gi] = p
            p += rate(gi + 0.5, k)
        # yaw: Gaussian smoothing (sigma 4) of the raw yaw, blended in over 108-120 and out over 148-160
        for gi in range(G_A0, G_A1 + 1):
            ks = [math.exp(-0.5 * (j / 4.0) ** 2) for j in range(-12, 13)]
            tot = sum(ks); y = sum(R[min(max(gi + j, G_A0 - 20), G_A1 + 20)][1] * w for j, w in zip(range(-12, 13), ks)) / tot
            w_in = sm(clamp((gi - G_A0) / 12.0)); w_out = sm(clamp((G_A1 - gi) / 12.0)); w = min(w_in, w_out)
            _AD[("y", gi)] = R[gi][1] * (1 - w) + y * w
            _AD[("d", gi)] = R[gi][2]
    pw = 1.0                                                                   # pitch blends only through its own boundary conditions (value + rate match)
    p = _AD[int(g)] * (1 - (g - int(g))) + _AD[min(int(g) + 1, G_A1)] * (g - int(g))
    yv = _AD[("y", int(g))] * (1 - (g - int(g))) + _AD[("y", min(int(g) + 1, G_A1))] * (g - int(g))
    dist = _AD[("d", int(g))]
    pr, yr = math.radians(p), math.radians(yv)
    d = Vector((math.cos(pr) * math.sin(yr), math.cos(pr) * math.cos(yr), math.sin(pr))) * dist
    return loc, loc + d


_DR = {}


def _drift(g):
    """(orbit angle rad, push fraction) accumulated from per-frame speeds: v(k) = ramp(k) * (small + a bump over the hold)"""
    if not _DR:
        ang = push = 0.0
        for k in range(170, 260):
            r = clamp((k - 170) / 12.0); r = r * r * (3 - 2 * r)
            d = clamp((k - 170) / 70.0)
            _DR[k] = (ang, push)
            ang += math.radians(0.075 + 0.06 * 4 * d * (1 - d)) * r
            push += (0.0005 + 0.0003 * d) * r
        _DR[260] = (ang, push)
    return _DR.get(int(g), (0.0, 0.0) if g < 170 else _DR[259])


def cam_rest_raw(g):
    """(loc, look) in the ship's rest frame at film frame g: the time-warped landing path + the drift"""
    loc, look = _land(_tau_of(g))
    loc, look = _aim_design(g, loc, look)
    ang, push = _drift(g)
    c = Vector((0.5, -30.5, loc.z))
    loc = c + Matrix.Rotation(-ang, 3, "Z") @ (loc - c)                      # the drift continues the landing's travel direction (-x), eased in from zero
    loc = loc + (look - loc) * push
    return loc, look


# ----------------------------------------------------------------------------- the sea (ONE camera-fitted grid): fit it to a virtual camera far above and behind
def widen_sea(preset, nu, nv):
    import h19_ship as SH
    P = SH.PRESETS[preset]
    look = Vector(P["cam"]["look"])
    P["cam"] = dict(P["cam"], loc=tuple(Vector((14.0, -330.0, 255.0)) * 3.0 / S))   # metres: a virtual camera 3x as far / high as the start pose
    P["sea_nu"], P["sea_nv"] = nu, nv
    P["foam_k"] = float(os.environ.get("FOAMK", "0.55"))                # a calmer wake: less white lace (it dominated the frame statistics)


# ----------------------------------------------------------------------------- the BLANK chart (QA-art: no coastline, no compass, no red mark: "nobody knows where we are")
def _blank_chart_body(k):
    """the unrolled sea chart of cast19.chart19, but BLANK (no coast, no compass, no red mark, no text): parchment, a fold, a dark header band along ONE edge and a
    hanging tie at one corner, so a 180 deg turn reads on a phone."""
    g = cast19._g3(k, "ch", cast19.PARCH, 0, 0, 0.74, 0)
    o = ['<path d="M0,-0.26 L0.74,-0.26 L0.74,0.26 L0,0.26 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.02,-0.245 L0.72,-0.245 L0.72,-0.115 L0.02,-0.115 Z" fill="%s"/>' % k.c("#1c2a4a"))       # the header band (the top edge)
    o.append('<path d="M0.37,-0.16 L0.37,0.25" stroke="%s" stroke-width="0.006" opacity="0.18"/>' % k.ink)                          # the fold
    o.append('<path d="M0.66,0.26 Q0.69,0.34 0.64,0.40 M0.70,0.26 Q0.74,0.33 0.72,0.38" stroke="%s" stroke-width="0.020" fill="none" stroke-linecap="round"/>' % k.c("#8a5a3a"))  # the tie hanging from the bottom-right corner
    return "".join(o)


import puppet as _puppet
_orig_prop = _puppet._prop


def _prop_rot(k, kind, H, ang, sc=1.0):
    """cast19._prop, plus: a chart19 prop is turned by the pose's 'angle' about its centre (the captain turns the chart upside down)"""
    o, tip = _orig_prop(k, kind, H, ang, sc)
    if kind == "chart19" and abs(ang) > 1e-6:
        o = '<g transform="rotate(%.3f %.4f %.4f)">%s</g>' % (ang, H[0] + 0.37 * sc, H[1], o)
    return o, tip


_puppet._prop = _prop_rot                                    # the puppet drawer calls puppet._prop


cast19._chart_body = _blank_chart_body                        # the prop drawer looks it up at call time


# ----------------------------------------------------------------------------- poses
def _ramp(g, a, b):
    return u_of(g, a, b)


def pose_captain(g):
    """captain19: peers at the blank chart; from g 157 he lifts it, TURNS it 180 deg (upside down), brows up (shocked, then worried), looks at astro19_c and shrugs"""
    p = dict(cast19.STORY19["captain_peer_chart"][1])
    p["lean"] = 8 + 2.0 * math.sin(g * 0.13)
    p["head_roll"] = 4.0 * math.sin(g * 0.09)
    p["blink"] = blink(g, BLINKS_C)
    p["pitch"] = 0.35 + 0.08 * math.sin(g * 0.17)
    p["arm_r"] = dict(hand=(0.6, 0.96 + 0.05 * math.sin(g * 0.2)), bend=0.3, layer="front")
    p["arm_l"] = dict(hand=(1.3, 1.0 + 0.04 * math.sin(g * 0.23 + 1)), bend=0.0, stretch=1.3, layer="front")
    flip = _ramp(g, 160, 170)                     # the 180 deg turn, 160-170, held until the shrug
    lift = _ramp(g, 157, 167) * (1.0 - _ramp(g, 175, 185))
    if lift > 0.0:
        sw = math.sin((g - 159) * 0.6) * (1.0 if g < 175 else 0.3)
        p["arm_r"] = dict(hand=(lerp(0.6, 0.45, lift), lerp(0.96, 1.7, lift) + 0.12 * sw), bend=lerp(0.3, 0.9, lift), layer="front")
        p["arm_l"] = dict(hand=(lerp(1.3, 1.0, lift), lerp(1.0, 1.85, lift) - 0.12 * sw), bend=0.2, stretch=1.2, layer="front")
        p["pitch"] = lerp(0.35, -0.10, lift)
        p["head_roll"] = -10.0 * lift + 3.0 * sw
    p["prop_r"] = dict(type="chart19", scale=1.0, angle=180.0 * flip)
    if g >= 158:
        p["expr"] = "shocked" if g < 172 else "worried"                         # brows up: a clear double-take
    look = _ramp(g, 173, 179)
    if look > 0.0:
        p["gaze"] = (lerp(0.8, 1.0, look), lerp(0.9, 0.0, look))               # at astro19_c (screen-right): the shared look
        p["head_roll"] = lerp(p["head_roll"], 8.0, look)
        p["yaw"] = lerp(0.4, 0.9, look)                                          # the head turns ~20 deg toward astro19_c (screen-right)
    if g >= 172:
        p["expr"] = "shocked"; p["mouth"] = "flat"                              # eyes fully open under raised brows (no half-lid 'unimpressed'), no O
    shrug = _ramp(g, 181, 189)
    if shrug > 0.0:
        lift4 = 0.12 * math.sin(math.pi * _ramp(g, 183, 187))                      # a 4-frame shoulder lift on the shrug
        p["arm_r"] = dict(hand=(lerp(0.45, 0.95, shrug), lerp(1.2, 0.72, shrug) - lift4), bend=lerp(0.6, 0.0, shrug), shape="open", layer="front")      # symmetric: both forearms
        p["arm_l"] = dict(hand=(lerp(1.0, -0.95, shrug), lerp(1.4, 0.72, shrug) - lift4), bend=lerp(0.2, 0.0, shrug), shape="open", stretch=1.0, layer="front")   # rise at the same angle, palms open
                                                                                # the chart stays in his right hand (held low, upside down) through g 199
        p["head_roll"] = lerp(8.0, 7.0, shrug) + 2.0 * math.sin(g * 0.8)
        p["lean"] = 8 - 10.0 * shrug
        p["pitch"] = lerp(0.1, 0.15, shrug)
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


def pose_astro(g):
    """astro19_c: squints through the quadrant at the sky; g 155-173 an OBVIOUS head-scratch; 173-179 looks at the captain; 181-189 shrugs, palms up"""
    p = dict(cast19.STORY19["william_quadrant_sun"][1])                    # arms / prop of the quadrant pose
    p["expr"] = "squint"
    p["blink"] = blink(g, BLINKS_A)
    p["lean"] = -3 + 1.2 * math.sin(g * 0.15)
    p["head_roll"] = 3.0 * math.sin(g * 0.11 + 1.0)
    p["glint"] = 0.5 + 0.5 * math.sin(g * 0.2)
    scr = _ramp(g, 155, 161) * (1.0 - _ramp(g, 173, 177))
    if scr > 0.0:
        w = math.sin(g * 1.35)                                                 # the scratching wobble
        p["arm_r"] = dict(hand=(lerp(0.46, 0.5, scr), lerp(0.1, 0.5, scr)), bend=lerp(-0.7, 0.5, scr), stretch=1.1, layer="top")
        p["prop_r"] = dict(type="quadrant19", angle=lerp(-62, -8, scr), scale=0.95)
        p["arm_l"] = dict(hand=(lerp(-0.46, -0.10 + 0.10 * w, scr), lerp(0.96, 2.3 + 0.12 * w, scr)), bend=lerp(0.5, 1.0, scr), shape="open")
        p["pitch"] = lerp(-0.75, 0.2, scr)
        p["expr"] = "unimpressed" if scr > 0.4 else "squint"
        p["head_roll"] = 9.0 * scr * math.sin(g * 1.35 + 0.7)
        p["gaze"] = (0.2, 0.3)
        p["glint"] = 0.0
    look = _ramp(g, 173, 179)
    if look > 0.0:
        p["pitch"] = lerp(p.get("pitch", -0.75), 0.15, look)
        p["gaze"] = (lerp(0.2, -1.0, look), 0.0)                              # at the captain (screen-left; the card is mirrored)
        p["yaw"] = lerp(p.get("yaw", 0.4), 0.9, look)                          # the head turns ~20 deg toward the captain
        p["expr"] = "worried" if look > 0.5 else p["expr"]
    shrug = _ramp(g, 181, 189)
    if shrug > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.5, 0.95, shrug), lerp(0.5, 0.7, shrug)), bend=lerp(0.5, -0.2, shrug), shape="open", stretch=1.0, layer="top")
        p["arm_l"] = dict(hand=(lerp(-0.1, -0.9, shrug), lerp(2.2, 0.75, shrug)), bend=lerp(1.0, 0.4, shrug), shape="open")
        p["prop_r"] = dict(type="quadrant19", angle=lerp(-8, 25, shrug), scale=0.95)   # the quadrant stays in his right hand (lowered), never pops out
        p["head_roll"] = lerp(0.0, -8.0, shrug)
        p["lean"] = lerp(-3, -8, shrug)
        p["pitch"] = 0.1
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


def whitecaps_and_wake(n=int(os.environ.get("WC", "170")), seed=int(os.environ.get("WCSEED", "5")), L=300.0):
    """the aerial preset has no whitecaps and the set's wake fades by ~150 m, so the extreme wide start is smooth water (qa_auto: 'suspected blur').  The set's own
    'streaks' hook (broken foam lines, ship frame, metres) is only fed by hero / rocks / coast scenery: wrap LD.scenery so the aerial sea gets scattered whitecap lines over +-320 m (the set's own wake is already a long V seen from behind).  Runtime only, no set edit."""
    import random as _rnd
    import h19_ship_land as LD
    orig = LD.scenery

    def sc(S_, P, LT, sea_P, marks):
        orig(S_, P, LT, sea_P, marks)
        st = sea_P.setdefault("streaks", [])
        rg = _rnd.Random(seed)
        for _ in range(n):
            cx, cy = rg.uniform(-320, 320), rg.uniform(-330, 240)
            if abs(cx) < 18 + 0.40 * max(0.0, -cy - 20) and cy < 50:
                continue                                                   # not on the ship or in its wake
            a = math.radians(rg.uniform(-35, 35)); ln = rg.uniform(20, 50)
            st.append(((cx - 0.5 * ln * math.cos(a), cy - 0.5 * ln * math.sin(a)), (cx + 0.5 * ln * math.cos(a), cy + 0.5 * ln * math.sin(a)),
                       rg.uniform(2.0, 3.6), rg.uniform(0.7, 0.9)))
    LD.scenery = sc


class Take(C.Take):
    def __init__(self, quality="preview"):
        whitecaps_and_wake()
        widen_sea(PRESET, int(os.environ.get("NU", "1500")), int(os.environ.get("NV", "2000")))
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        root = self.A["ship_root"]
        self.cap = self.actors["cap"] = C.make_actor("cap", "captain19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.ast = self.actors["ast"] = C.make_actor("ast", "astro19_c", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        for a in (self.cap, self.ast):
            C.ride_ship(a, root)                                           # BEFORE place() and BEFORE any set_roll key: the inverse is taken at rest
        self.cam_pose(FIRST_G, root)

    def cam_pose(self, g, root):
        f = bf(g)
        self.key_set(f, sea=g / 30.0, roll=g / 30.0)                       # same t on every frame
        loc, look = cam_rest(g)
        self.key_cam(f, *C.on_ship(root, f, loc, look))                    # the camera rides the deck (rest-frame pose -> world)

    def pose(self, gs):
        root = self.A["ship_root"]
        for g in gs:
            f = bf(g)
            self.cam_pose(g, root)
            C.key_vis([o for o in (C.bpy.data.objects.get("gulls_gullt"), C.bpy.data.objects.get("gulls_gullw"), C.bpy.data.objects.get("headland")) if o], False, f)   # no gulls, and no pale 'headland' slab on the horizon
            C.place(self.cap, f, (CAP_XY[0], CAP_XY[1], Z_QD))
            C.place(self.ast, f, (AST_XY[0], AST_XY[1], Z_QD))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.cap.pose(f, pose_captain(g), camera=self.cam)
            pa = pose_astro(g)
            pa["mirror"] = True
            self.ast.pose(f, pa, camera=self.cam)
        self.sprites_for([(self.cap, PPD), (self.ast, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_rest(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def camreport():
    prev = None
    mx = 0
    for g in GS:
        loc, look = cam_rest(g)
        if prev is not None:
            d = (loc - prev).length
            mx = max(mx, d)
        if g % 12 == 0:
            print(g, [round(c, 1) for c in loc], [round(c, 1) for c in look])
        prev = loc


_SM = {}


def cam_rest(g):
    """cam_rest_raw smoothed in time (Gaussian, sigma 3 frames) from g ~112: kills the one-frame ticks at the table hand-offs (QA-tech round 13: flow must fall monotonically
    from g 131 with no up-tick at g 176); blended in with a smoothstep over g 112-128 so the opening is untouched."""
    g = int(g)
    if g not in _SM:
        w = 0.0
        raw = cam_rest_raw(g)
        if w <= 0.0:
            _SM[g] = raw
        else:
            ks = [math.exp(-0.5 * (k / 3.0) ** 2) for k in range(-9, 10)]
            tot = sum(ks)
            loc = Vector((0.0, 0.0, 0.0)); look = Vector((0.0, 0.0, 0.0))
            for k, wk in zip(range(-9, 10), ks):
                l, lk = cam_rest_raw(min(max(g + k, 48), 260))
                loc += l * (wk / tot); look += lk * (wk / tot)
            _SM[g] = (raw[0] * (1 - w) + loc * w, raw[1] * (1 - w) + look * w)
    return _SM[g]



if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        camreport()
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else FINAL_SPP
        quality = "final" if scale >= 1.0 else "preview"
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)

