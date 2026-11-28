"""gait8.py -- walk and run cycles with planted feet (pure Python, D units, figure frame).

    G = Gait(spec, kind="walk" | "run")
    pose = G.pose(t, s=+1, view="q", base=dict(expr=...))   # per-frame pose dict for draw8.build
    G.root_x(t)                                              # distance travelled (D) along the facing direction

The root moves at constant speed v.  A foot in stance stays at a fixed world position: its figure-frame x is
x_land - v * (t - t_land) (times s for the facing), its y is 0 (on the ground).  The swing carries it forward
to the next landing with a lift arc.  The hip height is lowered when needed so every planted ankle is reachable
by the (fixed-length) leg, so the IK never pulls a planted foot.  Arms swing opposite to the legs.
"""
import math
import draw8

PRESET = {
    #            period s, stance share, step length D, bob D, lean deg, lift D, arm swing D
    "walk": dict(T=0.92, beta=0.60, step=0.70, bob=0.035, lean=4.0, lift=0.20, arm=0.30),
    "run": dict(T=0.62, beta=0.36, step=1.05, bob=0.07, lean=12.0, lift=0.38, arm=0.42),
}


def smooth(u):
    return u * u * (3 - 2 * u)


class Gait:
    def __init__(self, spec, kind="walk", **kw):
        self.sp = draw8.get_spec(spec)
        self.kind = kind
        P = dict(PRESET[kind])
        P.update(kw)
        self.P = P
        self.v = 2 * P["step"] / P["T"]                        # D per second
        self.S = self.v * P["beta"] * P["T"]                   # stance travel of a foot (figure frame)
        ank_h = min(self.sp["boot_h"] * 0.42, 0.24)
        self.ank_h = ank_h
        self.L = self.sp["legs"] + 0.06 - ank_h                # hip -> ankle length
        self.hip0 = self.sp["legs"] + 0.06                     # rest hip height above the soles

    def root_x(self, t):
        return self.v * t

    def foot(self, t, offset):
        """figure-frame forward x (for s=+1) and lift of one foot; offset 0 or 0.5.  Returns (x, lift, planted)."""
        P = self.P
        ph = (t / P["T"] + offset) % 1.0
        S = self.S
        if ph < P["beta"]:
            return S / 2 - self.v * ph * P["T"], 0.0, True, ph
        u = (ph - P["beta"]) / (1 - P["beta"])
        x = -S / 2 + S * smooth(u)
        return x, P["lift"] * math.sin(math.pi * u) ** 1.2, False, ph

    def pose(self, t, s=1, view="q", base=None):
        P = self.P
        pose = dict(base or {})
        fn = self.foot(t, 0.0)
        ff = self.foot(t, 0.5)
        # bob: up at mid-stance (walk) / up in flight (run)
        ph = (t / P["T"]) % 1.0
        if self.kind == "walk":
            bob = -P["bob"] * math.cos(4 * math.pi * (ph - P["beta"] / 2))
        else:
            bob = -P["bob"] * math.cos(4 * math.pi * (ph - P["beta"] - (1 - 2 * P["beta"]) / 4) + math.pi)
        # crouch the hip so every planted ankle is reachable (keeps planted feet exactly in place)
        hip_h = self.hip0 + (-bob)
        if self.kind == "run":
            hip_h -= 0.10
        for x, lift, planted, _ in (fn, ff):
            if planted:
                dx = abs(x) + 0.05
                hmax = math.sqrt(max(self.L ** 2 - dx ** 2, 0.0)) * 0.995 + self.ank_h
                hip_h = min(hip_h, hmax)
        dy = self.hip0 - hip_h                                 # + = hip lower (figure y is down)
        pose["hip"] = (0.0, dy)
        pose["lean"] = P["lean"]
        # feet: figure x = s * forward x; y = -lift; toe tilt in swing
        def foot_xy(fx):
            x, lift, planted, phf = fx
            return (s * x, -lift)
        legs = dict(foot_n=foot_xy(fn), foot_f=foot_xy(ff))
        if not fn[2]:
            legs["toe_n"] = -12.0 * math.sin(math.pi * (fn[3] - P["beta"]) / (1 - P["beta"]))
        if not ff[2]:
            legs["toe_f"] = -12.0 * math.sin(math.pi * (ff[3] - P["beta"]) / (1 - P["beta"]))
        pose["legs"] = legs
        # arms: opposite to the same-side leg
        a = P["arm"]
        sw_n = math.sin(2 * math.pi * (ph + 0.5) - math.pi * P["beta"])   # near arm swings with the far leg
        sw_f = -sw_n
        if self.kind == "walk":
            pose["arm_n"] = dict(hand=(a * sw_n, 1.02 - 0.05 * abs(sw_n)), elbow=None)
            pose["arm_f"] = dict(hand=(a * sw_f, 1.02 - 0.05 * abs(sw_f)), elbow=None)
        else:
            pose["arm_n"] = dict(hand=(0.18 + a * sw_n, 0.62 - 0.18 * sw_n), elbow=-1)
            pose["arm_f"] = dict(hand=(0.18 + a * sw_f, 0.62 - 0.18 * sw_f), elbow=-1)
        pose["view"] = view
        pose["s"] = s
        pose["_planted"] = (fn[2], ff[2])
        return pose
