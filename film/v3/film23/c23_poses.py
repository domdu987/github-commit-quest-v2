"""c23_poses.py: pose helpers for the film-23 takes (idle life: blinks, sway; cycles).  Pure python on top of cast23."""
import math, cast23


def base(key):
    """(cast, pose dict copy) of a STORY23 entry."""
    c, p = cast23.STORY23[key]
    return c, dict(p)


def life(p, g, seed=0, sway=1.0, blink=True):
    """idle life on a pose: a slow head roll + lean sway (about 1-2 degrees, never frozen) and blinks."""
    p = dict(p)
    ph = g / 30.0 * 2 * math.pi
    p["head_roll"] = p.get("head_roll", 0) + sway * 2.2 * math.sin(ph * 0.45 + seed * 1.7)
    p["lean"] = p.get("lean", 0) + sway * 1.6 * math.sin(ph * 0.33 + seed * 2.3 + 1.0)
    if blink:
        p["blink"] = cast23.blink_at(g, 37 + 11 * seed)
    p["t"] = g / 30.0
    return p


def loud(g, t0, t1, pauses=()):
    """synthetic loudness (0..1) of a speaker: a 5 Hz syllable pattern with irregular dips, silent outside t0..t1 (film frames) and in the pauses."""
    if g < t0 or g >= t1 or any(a <= g < b for a, b in pauses):
        return 0.0
    t = g / 30.0
    s = 0.5 + 0.5 * math.sin(2 * math.pi * 5.0 * t + 1.3 * math.sin(2 * math.pi * 0.9 * t))
    w = 0.5 + 0.5 * math.sin(2 * math.pi * 1.7 * t + 0.6)             # phrase swell with dips
    return max(0.0, min(1.0, 0.25 + 0.75 * s * (0.35 + 0.65 * w)))
