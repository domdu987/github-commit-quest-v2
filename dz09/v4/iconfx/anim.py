"""anim.py -- pop-in / hold / pop-out timing for icon effects, as pure functions of the film frame g (30 fps).

    from anim import Cue, pop_state
    cue = Cue(g_in=120, hold=45)                 # pops in at g 120, holds 45 frames, pops out (3 frames)
    s = pop_state(cue, g)                        # -> PopState(visible, scale, opacity, rot_deg, t, phase)

`t` is the icon's own clock in seconds since its pop-in started (drives the icon's inner animation: ring growth,
stopwatch sweep, blinking battery...).  `scale` multiplies the icon about its anchor; `opacity` multiplies alpha.

Profiles (scale per frame from the pop-in frame):
  "brief"  0, 0.62, 1.15, 1.06, 1.00          -- the director's brief: 4-frame overshoot 0 -> 115 % -> 100 %
  "snap"   0.65, 1.00                         -- measured on the reference clip (green check at t 50.4 s:
                                                 widths 91, 139, 141, 141 px at 30 fps: 65 % then 100 %, no overshoot)
  "soft"   0, 0.35, 0.75, 1.04, 1.08, 1.03, 1.00  -- a slower 6-frame pop for big world cards (title / warning)
Pop-out (3 frames): 1.0 -> 1.08 -> 0.55 -> 0 with opacity 1, 1, 0.6, 0  ("brief" and "soft"); "snap" cuts out in 1.
"""
from collections import namedtuple

FPS = 30.0
PROFILES = {
    "brief": [0.0, 0.62, 1.15, 1.06, 1.0],
    "snap": [0.65, 1.0],
    "soft": [0.0, 0.35, 0.75, 1.04, 1.08, 1.03, 1.0],
}
OUT_PROFILES = {
    "brief": ([1.08, 0.55, 0.0], [1.0, 0.6, 0.0]),
    "soft": ([1.08, 0.55, 0.0], [1.0, 0.6, 0.0]),
    "snap": ([0.0], [0.0]),
}
# a small rotation kick that rides on the overshoot (degrees per frame of the pop-in), as hand-made pops do
ROT_KICK = {"brief": [-8.0, -5.0, 3.0, 1.0, 0.0], "snap": [0.0, 0.0], "soft": [-6, -4, -1, 2, 1, 0, 0]}

PopState = namedtuple("PopState", "visible scale opacity rot_deg t phase")


class Cue(object):
    """One appearance of one icon.  g_in: first frame of the pop-in (0-based film frame).  hold: frames at full size
    after the pop-in.  profile: key of PROFILES.  pop_out: False keeps it up for ever after g_in.  rot: allow the
    rotation kick."""

    def __init__(self, g_in, hold=45, profile="brief", pop_out=True, rot=True):
        self.g_in, self.hold, self.profile, self.pop_out, self.rot = int(g_in), int(hold), profile, pop_out, rot

    @property
    def n_in(self):
        return len(PROFILES[self.profile])

    @property
    def g_hold(self):
        return self.g_in + self.n_in

    @property
    def g_out(self):                       # first frame of the pop-out
        return self.g_hold + self.hold

    @property
    def g_end(self):                       # first frame after the icon is gone
        return self.g_out + (len(OUT_PROFILES[self.profile][0]) if self.pop_out else 10 ** 9)

    def frames(self):
        return range(self.g_in, self.g_end if self.pop_out else self.g_hold + self.hold)


def pop_state(cue, g):
    t = (g - cue.g_in) / FPS
    if g < cue.g_in or (cue.pop_out and g >= cue.g_end):
        return PopState(False, 0.0, 0.0, 0.0, t, "off")
    k = g - cue.g_in
    prof = PROFILES[cue.profile]
    if k < len(prof):
        s = prof[k]
        rot = ROT_KICK[cue.profile][k] if cue.rot else 0.0
        return PopState(s > 0, s, 1.0 if s > 0 else 0.0, rot, t, "in")
    if (not cue.pop_out) or g < cue.g_out:
        return PopState(True, 1.0, 1.0, 0.0, t, "hold")
    j = g - cue.g_out
    sc, op = OUT_PROFILES[cue.profile]
    return PopState(sc[j] > 0, sc[j], op[j], 0.0, t, "out")


def overlap(cues):
    """frames where two or more cues are visible at once (the brief allows that only in the climax)."""
    seen = {}
    for c in cues:
        for g in c.frames():
            if pop_state(c, g).visible:
                seen[g] = seen.get(g, 0) + 1
    return sorted(g for g, n in seen.items() if n > 1)


# ---- small easing helpers used by the icons' inner animation -------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


if __name__ == "__main__":
    for p in PROFILES:
        c = Cue(0, hold=3, profile=p)
        print(p, [(g, round(pop_state(c, g).scale, 2), round(pop_state(c, g).opacity, 2)) for g in range(c.g_end + 1)])
