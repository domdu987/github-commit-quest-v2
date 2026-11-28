"""gait9.py -- EP.1 motion: runs, the infected sprint, the support walk and stepped actions, all with planted feet.

Pure Python.  Every cycle object has
    .dur                      seconds of one take (cyclic ones: any length; .T is the period)
    .root(t) -> (x, z)        root position along the motion axis and up, in D of that actor (x forward for s = +1)
    .pose(t, s, view) -> pose for draw9.build, with pose["_planted"] = (near, far)
While a foot is planted its sole is a fixed world point: figure x = s * (x_world - root_x), figure y = -(z_world - root_z).
The hip is lowered (never the bones stretched) until every planted ankle is reachable.  A stance the leg cannot
reach at all is reported in .unreachable (and would show up as drift in the measurement).
"""
import math, random
import draw8 as D
import gait8

FPS = 24


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------------------------------------- constant-speed cycles
#                 period s, stance share, step D, bob, lean deg, lift, arm swing
RUNS = {
    # checker's revision: the first presets gave a stance sweep of under 1 D (a shuffle: the legs never opened).
    # step = D per footfall, so stance sweep = 2 * step * beta (about 1.3-1.5 D on legs of 1.8 D) with a real flight phase.
    "kong": dict(T=0.62, beta=0.31, step=2.35, bob=0.08, lean=14.0, lift=0.45, kick=0.70, arm=0.40),     # heavy, tool in hand
    "james": dict(T=0.56, beta=0.28, step=2.60, bob=0.09, lean=16.0, lift=0.55, kick=0.85, arm=0.50),    # light and quick
    "praew": dict(T=0.54, beta=0.30, step=2.15, bob=0.07, lean=12.0, lift=0.42, kick=0.65, arm=0.38),    # short quick steps
    "tos": dict(T=0.60, beta=0.34, step=2.05, bob=0.10, lean=8.0, lift=0.36, kick=0.50, arm=0.30),       # stiff, upright, heavy landing
    "sprint": dict(T=0.50, beta=0.25, step=3.00, bob=0.06, lean=30.0, lift=0.55, kick=0.90, arm=0.0),    # infected: thrown forward
}


def _hermite(keys, u, m0, m1):
    """cubic Hermite through keys [(u, v), ...] with end slopes m0 / m1 (dv/du) and finite-difference slopes inside."""
    n = len(keys)
    for i in range(n - 1):
        if u <= keys[i + 1][0] or i == n - 2:
            break
    (ua, va), (ub, vb) = keys[i], keys[i + 1]
    def slope(k):
        if k == 0: return m0
        if k == n - 1: return m1
        return (keys[k + 1][1] - keys[k - 1][1]) / (keys[k + 1][0] - keys[k - 1][0])
    h = ub - ua
    t = max(0.0, min(1.0, (u - ua) / h))
    ma, mb = slope(i) * h, slope(i + 1) * h
    return (2 * t ** 3 - 3 * t ** 2 + 1) * va + (t ** 3 - 2 * t ** 2 + t) * ma + (-2 * t ** 3 + 3 * t ** 2) * vb + (t ** 3 - t ** 2) * mb


class Stride(gait8.Gait):
    """a run with a readable stride (replaces gait8's run for EP.1): the foot lands ahead of the hip, pushes off well
    behind it, kicks up behind (heel toward the seat), the knee drives through and the foot reaches past the landing
    point before coming back to the ground at ground speed.  The hip rides low in stance and rises in flight.
    Planted soles are still exact fixed points of the motion plane (same rule as gait8)."""

    def __init__(self, spec, **P):
        gait8.Gait.__init__(self, spec, "run", **P)
        self.P.setdefault("kick", 0.7); self.P.setdefault("fore", 0.46); self.P.setdefault("crouch", 0.27)

    def foot(self, t, offset):
        P = self.P
        ph = (t / P["T"] + offset) % 1.0
        S = self.S
        a = S * P["fore"]; b = S - a
        if ph < P["beta"]:
            return a - self.v * ph * P["T"], 0.0, True, ph
        u = (ph - P["beta"]) / (1 - P["beta"])
        vg = -self.v * (1 - P["beta"]) * P["T"]                # ground speed in the figure frame, per unit u
        kx = [(0.0, -b), (0.20, -b - 0.16), (0.44, -0.30 * b), (0.66, 0.45 * a + 0.12), (0.86, a + 0.20), (1.0, a)]
        ky = [(0.0, 0.0), (0.20, 0.72 * P["kick"]), (0.44, P["kick"]), (0.66, P["lift"]), (0.86, 0.40 * P["lift"]), (1.0, 0.0)]
        x = _hermite(kx, u, vg, vg)
        y = max(0.0, _hermite(ky, u, 1.6 * P["kick"], -1.2 * P["lift"]))
        return x, y, False, ph

    def pose(self, t, s=1, view="side", base=None):
        P = self.P
        pose = dict(base or {})
        fn, ff = self.foot(t, 0.0), self.foot(t, 0.5)
        ph = (t / P["T"]) % 1.0
        ph_fl = P["beta"] + (0.5 - P["beta"]) / 2              # middle of the flight after the near foot's stance
        hip_h = self.hip0 - P["crouch"] + P["bob"] * math.cos(4 * math.pi * (ph - ph_fl))
        for x, lift, planted, _ in (fn, ff):
            if planted:
                dx = abs(x) + 0.05
                hip_h = min(hip_h, math.sqrt(max(self.L ** 2 - dx ** 2, 0.0)) * 0.995 + self.ank_h)
        pose["hip"] = (0.0, self.hip0 - hip_h)
        pose["lean"] = P["lean"]
        legs = dict(foot_n=(s * fn[0], -fn[1]), foot_f=(s * ff[0], -ff[1]))
        for key, f in (("toe_n", fn), ("toe_f", ff)):
            if not f[2]:
                u = (f[3] - P["beta"]) / (1 - P["beta"])
                # toes hang down behind in the kick, come up for the landing
                legs[key] = TOE_SIGN * (38.0 * math.sin(math.pi * min(1.0, u / 0.55)) ** 2 if u < 0.55 else -14.0 * math.sin(math.pi * (u - 0.55) / 0.45))
        pose["legs"] = legs
        a = P["arm"]
        sw_n = math.sin(2 * math.pi * (ph + 0.5) - math.pi * P["beta"])
        pose["arm_n"] = dict(hand=(0.08 + 1.35 * a * sw_n, 0.60 - 0.24 * sw_n), elbow=-1)
        pose["arm_f"] = dict(hand=(0.08 - 1.35 * a * sw_n, 0.60 + 0.24 * sw_n), elbow=-1)
        pose["view"] = view
        pose["s"] = s
        pose["_planted"] = (fn[2], ff[2])
        return pose


TOE_SIGN = 1.0


class Run(Stride):
    """survivor run: the planted-foot Stride with a per-character preset (RUNS) and style."""

    def __init__(self, spec, who="kong", phase=0.0, **kw):
        P = dict(RUNS[who]); P.update(kw)
        Stride.__init__(self, spec, **P)
        self.who, self.T, self.phase = who, P["T"], phase
        self.dur = 4 * P["T"]
        self.unreachable = []

    def root(self, t):
        return (self.v * t, 0.0)

    def pose(self, t, s=1, view="side", base=None):
        p = Stride.pose(self, t + self.phase * self.T, s=s, view=view, base=base)
        ph = ((t / self.T) + self.phase) % 1.0
        sw = math.sin(2 * math.pi * (ph + 0.5) - math.pi * self.P["beta"])
        if self.who == "tos":                                # arms held in tight, elbows out, head back
            p["arm_n"] = dict(hand=(0.26 + 0.16 * sw, 0.50 - 0.08 * sw), elbow=-1)
            p["arm_f"] = dict(hand=(0.26 - 0.16 * sw, 0.50 + 0.08 * sw), elbow=-1)
            p["head"] = (0, -6, 0, 0)
        elif self.who == "praew":
            p["coat_sway"] = 0.20 + 0.06 * sw
            p["head"] = (0, 2, 0.02, 0)
        elif self.who == "kong":                             # the near arm carries weight: a shorter swing
            p["arm_n"] = dict(hand=(0.10 + 0.20 * sw, 0.80 - 0.08 * sw), elbow=-1, hand_shape="grip")
        elif self.who == "james":
            p["head"] = (0, -3 + 3 * sw, 0, 0)
        return p


class Sprint(Stride):
    """infected sprint: a different gait from the survivors' run.  Longer, faster strides, the trunk thrown 30 deg
    forward, the head leading, arms NOT pumping: they hang loose and trail, flail, or reach (spec["run_style"])."""

    def __init__(self, spec, phase=0.0, style=None, seed=None, **kw):
        sp = D.get_spec(spec)
        rnd = random.Random(seed if seed is not None else hash(sp.get("name", "x")) % 9973)
        P = dict(RUNS["sprint"])
        P["T"] *= rnd.uniform(0.94, 1.08)
        P["step"] *= rnd.uniform(0.94, 1.05)
        P["lean"] += rnd.uniform(-5, 5)
        P.update(kw)
        Stride.__init__(self, sp, **P)
        self.T, self.phase = P["T"], phase
        self.style = style or sp.get("run_style", "trail")
        self.jit = rnd.uniform(0, 6.28)
        self.dur = 4 * P["T"]
        self.unreachable = []

    def root(self, t):
        return (self.v * t, 0.0)

    def pose(self, t, s=1, view="side", base=None):
        b = dict(expr="lunging"); b.update(base or {})
        p = Stride.pose(self, t + self.phase * self.T, s=s, view=view, base=b)
        w = 2 * math.pi * (t / self.T + self.phase)
        a, c = math.sin(w + self.jit), math.sin(2 * w + 1.3 + self.jit)
        st = self.style
        if st == "trail":                                    # both arms streaming behind
            p["arm_n"] = dict(hand=(-0.62 + 0.10 * a, 0.62 + 0.10 * c), elbow=1, hand_shape="claw")
            p["arm_f"] = dict(hand=(-0.50 - 0.10 * a, 0.74 - 0.08 * c), elbow=1, hand_shape="claw")
        elif st == "reach":                                  # both arms out for the prey
            p["arm_n"] = dict(hand=(0.92 + 0.05 * a, 0.02 + 0.10 * c), elbow=None, hand_shape="claw")
            p["arm_f"] = dict(hand=(0.82 - 0.05 * a, 0.22 - 0.10 * c), elbow=None, hand_shape="claw")
        elif st == "one_up":                                 # one clawing forward, one dragging
            p["arm_n"] = dict(hand=(0.80 + 0.08 * a, -0.25 + 0.12 * c), elbow=None, hand_shape="claw")
            p["arm_f"] = dict(hand=(-0.45 + 0.12 * a, 0.80), elbow=1, hand_shape="claw")
        else:                                                # flail: loose, out of step with the legs
            p["arm_n"] = dict(hand=(0.15 + 0.55 * math.sin(0.5 * w + self.jit), 0.70 - 0.35 * abs(c)), elbow=None, hand_shape="claw")
            p["arm_f"] = dict(hand=(0.10 - 0.55 * math.sin(0.5 * w + self.jit + 1.0), 0.75 - 0.30 * abs(a)), elbow=None, hand_shape="claw")
        p["head"] = (0, -14 + 4 * a, 0.10, 0.02 + 0.015 * c)   # chin up and forward out of the leaning trunk
        return p


class SupportWalk:
    """Kong half-carrying the junior: two upright cards, the same world speed, both with planted feet.
    .a / .b are the two gaits (Kong, junior); pose(t, s) -> (pose_kong, pose_junior); off = the junior's root offset
    (along the motion, in Kong's D).  Stage the junior's card about 0.4 BU nearer the camera than Kong's: his far arm
    goes up behind Kong's neck, Kong's far arm (hidden) holds him."""

    def __init__(self, kong_spec, junior_spec, sc_k, sc_j, T=1.10, step=0.52):
        self.a = gait8.Gait(kong_spec, "walk", T=T, step=step, beta=0.64, bob=0.03, lean=7.0, lift=0.14, arm=0.0)
        self.b = gait8.Gait(junior_spec, "walk", T=T, step=step * sc_k / sc_j, beta=0.72, bob=0.02, lean=9.0, lift=0.07, arm=0.0)
        self.sc_k, self.sc_j = sc_k, sc_j
        self.T, self.dur = T, 3 * T
        self.off = -1.00          # checker: was -0.60, the two heads and trunks overlapped into one shape
        self.v = self.a.v
        self.unreachable = []

    def root(self, t):
        return (self.a.v * t, 0.0)

    def root_b(self, t):
        return ((self.a.v * t + self.off) * self.sc_k / self.sc_j, 0.0)

    def pose(self, t, s=1, view="side", stage=0):
        pk = self.a.pose(t, s=s, view=view, base=dict(expr="resolve"))
        pj = self.b.pose(t + 0.30 * self.T, s=s, view=view, base=dict(expr="pain" if stage < 2 else "fading"))
        w = math.sin(2 * math.pi * t / self.T)
        # Kong: the camera-side hand holds the wrist that hangs over his shoulder; the far arm (hidden) is round the junior's back
        pk["arm_n"] = dict(hand=(-0.34, 0.42 + 0.02 * w), elbow=None, hand_shape="grip")
        pk["arm_f"] = dict(hand=(-0.30, 0.55), elbow=None)
        pk["head"] = (0, 4, 0, 0)
        # the junior: sagging, head down, the arm over Kong's shoulders (target = Kong's near shoulder, in the junior's D)
        k_sh = (self.a.sp["legs"] + self.a.sp["torso"] - 0.22) * self.sc_k / self.sc_j
        dx = -self.off * self.sc_k / self.sc_j
        pj["arm_f"] = dict(fig=(s * (dx + 0.10), -(k_sh - 0.02) + 0.03 * w), elbow=1, hand_shape="glove")
        pj["arm_n"] = dict(hand=(0.10, 0.92), elbow=None, hand_shape="open")
        pj["lean"] = 9.0 + 2.0 * w
        pj["head"] = (0, 16, 0.04, 0.04)
        hp = pj.get("hip", (0.0, 0.0))
        pj["hip"] = (hp[0], hp[1] + 0.07)
        return pk, pj


# ---------------------------------------------------------------------------------------------- stepped actions
class Seq:
    """one take of a stepped action.  feet = {"n": [(t0, t1, x, z), ...], "f": [...]}: stance intervals (seconds) with
    the planted sole point in the take's own axis (D).  root_fn(t) -> (x, z).  act(t, pose) may add arms, lean, face."""

    def __init__(self, spec, dur, root_fn, feet, act=None, lift=0.30, crouch=None, expr=None):
        self.sp = D.get_spec(spec)
        self.dur, self.root_fn, self.feet, self.act = dur, root_fn, feet, act
        self.lift, self.crouch, self.expr = lift, crouch, expr
        self.ank_h = min(self.sp["boot_h"] * 0.42, 0.24)
        self.L = self.sp["legs"] + 0.06 - self.ank_h
        self.hip0 = self.sp["legs"] + 0.06
        self.unreachable = []

    def root(self, t):
        return self.root_fn(max(0.0, min(self.dur, t)))

    def _foot(self, key, t):
        st = self.feet[key]
        for i, (t0, t1, x, z) in enumerate(st):
            if t0 <= t <= t1:
                return x, z, True, 0.0
        prev = [q for q in st if q[1] < t]
        nxt = [q for q in st if q[0] > t]
        if not prev:
            return nxt[0][2], nxt[0][3], False, 0.0
        if not nxt:
            return prev[-1][2], prev[-1][3], False, 0.0
        a, b = prev[-1], nxt[0]
        u = (t - a[1]) / max(b[0] - a[1], 1e-6)
        k = smooth(u)
        lift = (self.lift + 0.25 * abs(b[3] - a[3])) * math.sin(math.pi * u) ** 1.1
        return lerp(a[2], b[2], k), lerp(a[3], b[3], k) + lift, False, u

    def pose(self, t, s=1, view="side", base=None):
        t = max(0.0, min(self.dur, t))
        rx, rz = self.root(t)
        p = dict(base or {})
        if self.expr and "expr" not in p:
            p["expr"] = self.expr
        fn, ff = self._foot("n", t), self._foot("f", t)
        hh = self.hip0 - (self.crouch(t) if self.crouch else 0.0)
        for (x, z, planted, u) in (fn, ff):
            fx, ay = x - rx, (z - rz) + self.ank_h
            if planted:
                if abs(fx) >= self.L * 0.999:
                    self.unreachable.append((round(t, 3), round(fx, 3)))
                    continue
                r = math.sqrt(self.L ** 2 - fx ** 2) * 0.995
                hh = min(hh, ay + r)
        for (x, z, planted, u) in (fn, ff):                 # a foot planted ABOVE the hip (climbing): do not sink below its reach
            fx, ay = x - rx, (z - rz) + self.ank_h
            if planted and abs(fx) < self.L * 0.999:
                hh = max(hh, ay - math.sqrt(self.L ** 2 - fx ** 2) * 0.995)
        p["hip"] = (0.0, self.hip0 - hh)
        legs = dict(foot_n=(s * (fn[0] - rx), -(fn[1] - rz)), foot_f=(s * (ff[0] - rx), -(ff[1] - rz)))
        if not fn[2]:
            legs["toe_n"] = -14.0 * math.sin(math.pi * fn[3])
        if not ff[2]:
            legs["toe_f"] = -14.0 * math.sin(math.pi * ff[3])
        p["legs"] = legs
        p["view"], p["s"] = view, s
        if self.act:
            self.act(t, p, s)
        p["_planted"] = (fn[2], ff[2])
        return p


def _keys(pts):
    """piecewise smooth interpolation through (t, value...) keys."""
    def fn(t):
        if t <= pts[0][0]:
            return pts[0][1:]
        for a, b in zip(pts, pts[1:]):
            if t <= b[0]:
                k = smooth((t - a[0]) / (b[0] - a[0]))
                return tuple(lerp(a[i], b[i], k) for i in range(1, len(a)))
        return pts[-1][1:]
    return fn


def stagger_back(spec, wall=1.62):
    """thrown back three steps until the back hits the truck side (`wall` D behind the start), then pinned there."""
    root = _keys([(0.0, 0.0, 0.0), (0.30, -0.42, 0.0), (0.62, -1.02, 0.0), (0.95, -wall + 0.12, 0.0), (1.8, -wall + 0.12, 0.0)])
    feet = {"n": [(0.0, 0.16, 0.16, 0.0), (0.36, 0.62, -0.62, 0.0), (0.84, 1.8, -wall + 0.30, 0.0)],
            "f": [(0.0, 0.30, -0.16, 0.0), (0.52, 0.78, -1.12, 0.0), (1.00, 1.8, -wall - 0.02, 0.0)]}
    lean = _keys([(0.0, -4.0), (0.3, -12.0), (0.8, -10.0), (0.97, -16.0), (1.15, -7.0), (1.8, -6.0)])
    arm = _keys([(0.0, 0.0), (0.25, 1.0), (0.9, 0.8), (1.0, 1.25), (1.3, 0.5), (1.8, 0.35)])

    def act(t, p, s):
        p["lean"] = lean(t)[0]
        k = arm(t)[0]
        p["arm_n"] = dict(hand=(0.30 + 0.45 * k, 0.80 - 0.85 * k), elbow=None, hand_shape="open")
        p["arm_f"] = dict(hand=(0.20 + 0.50 * k, 0.85 - 0.60 * k), elbow=None, hand_shape="open")
        hit = max(0.0, 1 - abs(t - 1.0) / 0.12)
        p["head"] = (0, -8 - 10 * hit, -0.03 * hit, 0)
        p.setdefault("expr", "alarmed" if t < 0.95 else "shouting")
    return Seq(spec, 1.8, lambda t: root(t), feet, act, lift=0.16)


def raise_crowbar(spec):
    """one step in, both hands bring the crowbar up over the head and hold it there, trembling (S160-S161)."""
    root = _keys([(0.0, 0.0, 0.0), (0.25, 0.05, 0.0), (0.70, 0.52, 0.0), (1.8, 0.56, 0.0)])
    feet = {"n": [(0.0, 0.22, 0.20, 0.0), (0.55, 1.8, 0.95, 0.0)], "f": [(0.0, 1.8, -0.22, 0.0)]}
    up = _keys([(0.0, 0.0), (0.30, 0.10), (0.85, 1.0), (1.8, 1.0)])

    def act(t, p, s):
        k = up(t)[0]
        tr = 0.012 * math.sin(t * 31.0) * (k > 0.95)
        hx, hy = lerp(0.30, -0.28, k) + tr, lerp(0.62, -0.92, k)
        p["arm_n"] = dict(hand=(hx, hy), elbow=None, hand_shape="grip")
        p["arm_f"] = dict(hand=(hx + 0.17, hy + 0.08), elbow=None, hand_shape="grip")
        p["prop_n"] = dict(type="crowbar", angle=lerp(-70.0, 198.0, k) * s)
        p["z"] = {"arm_f": 2.4}
        p["lean"] = lerp(6.0, -5.0, k)
        p["head"] = (0, -4 * k, 0, 0)
        p.setdefault("expr", "resolve")
    return Seq(spec, 1.8, lambda t: root(t), feet, act, lift=0.14)


def throw_flare(spec, t_release=0.62):
    """strike, wind up, one step, overarm throw, follow through.  The flare is in the hand until t_release
    (.release = (t, hand figure point is read from the built figure's anchor wrist)); after it the stage flies a prop."""
    root = _keys([(0.0, 0.0, 0.0), (0.35, -0.10, 0.0), (0.70, 0.50, 0.0), (1.5, 0.56, 0.0)])
    feet = {"n": [(0.0, 0.34, 0.20, 0.0), (0.58, 1.5, 0.98, 0.0)], "f": [(0.0, 1.5, -0.24, 0.0)]}
    arm = _keys([(0.0, 0.25, 0.55), (0.34, -0.55, -0.55), (0.50, -0.30, -1.00), (0.62, 0.55, -0.80), (0.80, 0.95, 0.20), (1.5, 0.55, 0.75)])
    lean = _keys([(0.0, 2.0), (0.34, -12.0), (0.62, 12.0), (0.85, 20.0), (1.5, 8.0)])

    def act(t, p, s):
        hx, hy = arm(t)
        p["arm_n"] = dict(hand=(hx, hy), elbow=None, hand_shape="grip" if t < t_release else "open")
        p["arm_f"] = dict(hand=(0.45 - 0.5 * smooth((t - 0.3) / 0.4), 0.35 + 0.3 * smooth((t - 0.3) / 0.4)), elbow=None)
        if t < t_release:
            p["prop_n"] = dict(type="flare", lit=t > 0.12, angle=(-20 - 120 * smooth(t / 0.34) + 200 * smooth((t - 0.34) / 0.28)) * s, flick=int(t * 12))
        p["lean"] = lean(t)[0]
        p.setdefault("expr", "shouting" if 0.4 < t < 1.0 else "serious")
    q = Seq(spec, 1.5, lambda t: root(t), feet, act, lift=0.14)
    q.t_release = t_release
    return q


def pull_out(spec):
    """the rescuer hauling a man out of a tipped car by the arms: weight back, two steps backward."""
    root = _keys([(0.0, 0.0, 0.0), (0.35, -0.12, 0.0), (0.80, -0.62, 0.0), (1.25, -1.10, 0.0), (1.7, -1.16, 0.0)])
    feet = {"n": [(0.0, 0.42, 0.42, 0.0), (0.66, 1.7, -0.50, 0.0)], "f": [(0.0, 0.86, -0.42, 0.0), (1.10, 1.7, -1.42, 0.0)]}
    heave = _keys([(0.0, 0.0), (0.30, 1.0), (0.75, 0.55), (1.0, 1.0), (1.7, 0.3)])

    def act(t, p, s):
        k = heave(t)[0]
        p["lean"] = 14.0 - 30.0 * k
        p["arm_n"] = dict(hand=(0.86 - 0.16 * k, 0.40 - 0.10 * k), elbow=None, hand_shape="grip")
        p["arm_f"] = dict(hand=(0.80 - 0.16 * k, 0.50 - 0.10 * k), elbow=None, hand_shape="grip")
        p.setdefault("expr", "shouting")
    return Seq(spec, 1.7, lambda t: root(t), feet, act, lift=0.12, crouch=lambda t: 0.26)


def bang_glass(spec, period=0.46, dur=1.84):
    """slam loop at a window: feet planted for the whole take, fists and claws alternating on the glass plane."""
    feet = {"n": [(0.0, dur, 0.30, 0.0)], "f": [(0.0, dur, -0.26, 0.0)]}

    def act(t, p, s):
        u = (t % period) / period
        v = ((t + period / 2) % period) / period
        hit_n = math.exp(-((u - 0.5) / 0.14) ** 2)           # 1 at the moment of the hit
        hit_f = math.exp(-((v - 0.5) / 0.14) ** 2)
        p["arm_n"] = dict(hand=(0.30 + 0.38 * hit_n, -0.70 + 0.22 * hit_n), elbow=None, hand_shape="fist_side")
        p["arm_f"] = dict(hand=(0.28 + 0.38 * hit_f, -0.30 + 0.16 * hit_f), elbow=None, hand_shape="claw")
        p["lean"] = 10.0 + 7.0 * max(hit_n, hit_f)
        p["head"] = (0, -6, 0.04 * max(hit_n, hit_f), 0)
        p.setdefault("expr", "lunging")
    return Seq(spec, dur, lambda t: (0.0, 0.0), feet, act)


def hold(spec, pose, dur=1.6, shiver=0.0, breath=0.0):
    """a static pose as a take (sit against the wheel, crouch-hide, seated): feet planted, optional shiver / breathing."""
    base = dict(pose)
    lg = base.get("legs")

    class H:
        pass
    h = H()
    h.dur, h.unreachable, h.sp = dur, [], D.get_spec(spec)
    h.root = lambda t: (0.0, 0.0)

    def pose_fn(t, s=1, view=None, base_=None):
        p = dict(base)
        p.update(base_ or {})
        if shiver:
            k = int(t * FPS)
            rnd = random.Random(k * 7 + 1)
            hd = tuple(p.get("head", (0, 0, 0, 0))) + (0,) * 4
            p["head"] = (hd[0], hd[1] + rnd.uniform(-1.5, 1.5) * shiver, hd[2] + rnd.uniform(-0.012, 0.012) * shiver, hd[3] + rnd.uniform(-0.008, 0.008) * shiver)
            p["lean"] = p.get("lean", 0.0) + rnd.uniform(-0.7, 0.7) * shiver
        if breath:
            hp = p.get("hip", (0.0, 0.0))
            p["hip"] = (hp[0], hp[1] + breath * 0.012 * math.sin(t * 5.0))
        p["_planted"] = (True, True)
        return p
    h.pose = pose_fn
    return h


def roof_run(spec, profile, x0, x1, stride=1.25, contact=0.15, speed=5.2, hands=True):
    """climb and run along car roofs.  profile(x) -> surface height (D of this actor) under the path at x.
    Footfalls are planned along x: on the deck before the first car, then every `stride` on whatever is under the
    foot; a footfall that would land in a gap between cars (or far below the last one) is skipped, which makes that
    stride a leap.  Returns a Seq whose root arcs through the leaps; .falls lists the footfalls (t, x, z, kind)."""
    falls = []
    x, t, side, last_z = x0, 0.0, 0, profile(x0)
    falls.append((x, last_z))
    while x < x1:
        nx = x + stride
        z = profile(nx)
        tries = 0
        while last_z - z > 0.9 and tries < 5:               # the next step would drop into a gap: leap further
            nx += stride * 0.5; z = profile(nx); tries += 1
        if z - last_z > 2.2:                                 # too high for one bound: plant closer to the edge first
            pass
        falls.append((nx, z)); x, last_z = nx, z
    # timing: flight time grows with the distance and the height change
    T = [0.0]
    for a, b in zip(falls, falls[1:]):
        d = math.hypot(b[0] - a[0], (b[1] - a[1]) * 1.4)
        T.append(T[-1] + max(0.24, d / speed))
    dur = T[-1] + 0.5
    feet = {"n": [], "f": []}
    for i, ((x, z), t) in enumerate(zip(falls, T)):
        key = "n" if i % 2 == 0 else "f"
        c = contact if 0 < i < len(falls) - 1 else 0.30
        feet[key].append((max(0.0, t - c / 2), min(dur, t + c / 2), x, z))
    feet["n"][0] = (0.0, feet["n"][0][1], feet["n"][0][2], feet["n"][0][3])
    feet["f"].insert(0, (0.0, max(0.02, T[1] - 0.16), falls[0][0] - 0.35, falls[0][1]))
    last = feet["n" if (len(falls) - 1) % 2 == 0 else "f"][-1]
    other = "f" if (len(falls) - 1) % 2 == 0 else "n"
    feet[other].append((min(dur, last[0] + 0.22), dur, last[2] + 0.30, last[3]))
    kn = "n" if (len(falls) - 1) % 2 == 0 else "f"
    feet[kn][-1] = (last[0], dur, last[2], last[3])
    keys = [(t, x, z) for (x, z), t in zip(falls, T)]

    def root(t):
        if t <= keys[0][0]:
            return (keys[0][1], keys[0][2])
        for a, b in zip(keys, keys[1:]):
            if t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0])
                gap = (b[0] - a[0])
                arc = 0.5 * 9.0 * (gap * 0.5) ** 2 * 4 * u * (1 - u) * 1.0     # ballistic bump of a flight lasting `gap`
                return (lerp(a[1], b[1], u), lerp(a[2], b[2], smooth(u)) + min(arc, 0.9))
        return (keys[-1][1] + 0.15 * smooth((t - keys[-1][0]) / 0.4), keys[-1][2])

    def act(t, p, s):
        w = math.sin(2 * math.pi * t / 0.5)
        fl = 0.0
        for a, b in zip(keys, keys[1:]):
            if a[0] <= t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0])
                big = min(1.0, (b[0] - a[0] - 0.24) / 0.2)
                fl = math.sin(math.pi * u) * max(0.0, big)
        p["lean"] = 14.0 + 8.0 * fl
        p["arm_n"] = dict(hand=(0.18 + 0.40 * w * (1 - fl) + 0.55 * fl, 0.62 - 0.18 * w - 0.75 * fl), elbow=-1)
        p["arm_f"] = dict(hand=(0.18 - 0.40 * w * (1 - fl) + 0.40 * fl, 0.62 + 0.18 * w - 0.55 * fl), elbow=-1)
    q = Seq(spec, dur, root, feet, act, lift=0.34, crouch=lambda t: 0.10)
    q.falls = [(round(t, 3), round(x, 3), round(z, 3)) for (x, z), t in zip(falls, T)]
    return q
