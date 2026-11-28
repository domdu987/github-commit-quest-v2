"""ck.py -- generic close / medium shot runner for the T1 takes: a take file only defines
    PRESET, HAZE, ROWS=(row, g0, g1), PRE (dict edits to the factory preset), ACTORS={name: member}, PLATE=(centre xyz, face_deg, w, h, colour) or None,
    FLOOR=(r,g,b), cam(g) -> (loc, look, lens), acts(g) -> {name: dict(pos, pose, flip, vis)}, focus(g) -> world point for DOF, hook(rig, g) optional, build_extra(rig) optional.
and ends with `ck.main(sys.modules[__name__])`."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
from mathutils import Vector

RIG = [None]


def main(M):
    M.RIG = RIG
    M.HANDLE = getattr(M, "HANDLE", 6)
    M.G_TAKE = (M.ROWS[1] - M.HANDLE, M.ROWS[2] - 1 + M.HANDLE)
    M.PRESET_NAME = M.PRESET

    def pre():
        import factory as FA
        for k, v in getattr(M, "PRE", {}).items():
            FA.PRESETS[M.PRESET][k] = v
        if getattr(M, "pre_extra", None): M.pre_extra()

    def build(rig):
        RIG[0] = rig
        rig.set_look(True)
        if getattr(M, "FACTORY", True):
            rig.open_shell(floor_col=getattr(M, "FLOOR", (0.30, 0.12, 0.07)))
        for nm, mem in M.ACTORS.items():
            setattr(rig, nm, rig.actor(nm, mem))
        if getattr(M, "PLATE", None):
            pl = M.PLATE if isinstance(M.PLATE, list) else [M.PLATE]
            for i, (c, fd, w, h, col) in enumerate(pl):
                rig.backdrop(c, fd, w=w, h=h, col=col, name="plate%d" % i)
        if getattr(M, "build_extra", None): M.build_extra(rig)

    def state(g):
        S = dict(cam=M.cam(g), actors=M.acts(g))
        f = M.focus(g) if hasattr(M, "focus") else None
        if f is not None and getattr(M, "DOF", True):
            S["dof"] = (getattr(M, "FSTOP", 2.6), R.dist(S["cam"][0], f))
        if getattr(M, "hook", None):
            S["hook"] = lambda gg: M.hook(RIG[0], gg)
        return S
    M.pre, M.build, M.state = pre, build, state
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(M, cmd, gs)


def push(g, M, d0, pct, ease=C.calm):
    u = ease((g - M.G_TAKE[0]) / float(M.G_TAKE[1] - M.G_TAKE[0]))
    return d0 / (1.0 + pct * u), u


def pose(name, g, **kw):
    p = R.story(name); p["light25"] = -1; p["rim25"] = 0.6
    p.update(kw)
    return p
