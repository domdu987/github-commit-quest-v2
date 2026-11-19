"""common.py : the few things every example shot shares (no bpy, no project state).

Paths: an example lives at <PROJ>/examples/<family>/shot.py after scripts/bootstrap.py, so PROJ is two folders up.
Clock: film frame g is 0-based, time g / 30 s; Blender frame f = g + 1.  The narration is laid into the film 0.100 s late
(film 1's convention, `audio_offset` of the timing file), so an event at narration clock t sits on film frame round((t + 0.1) * 30)
(`gf`) and a shot boundary at narration clock t on round(t * 30) (`gb`).  The runners carry the same two functions.
"""
import math
import os
import random

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30


def gf(t):
    """film frame of an in-shot event at narration clock t (s)."""
    return int(round((t + 0.1) * FPS))


def gb(t):
    """film frame of a shot boundary at narration clock t (s)."""
    return int(round(t * FPS))


def synth_loud(seconds, seed=1, syll_hz=5.5, pause_every=1.1, pause_len=0.18):
    """A stand-in for acting.loudness(t0, t1) when there is no narration WAV yet: one float per frame, 0 = silence,
    about 1 = speech, 1.5 = loud (the same scale).  Syllables at about syll_hz with a short pause every pause_every s.
    Replace it with acting.loudness(t0, t1, path=<your narration.wav>) once the voice is recorded."""
    rnd = random.Random(seed)
    out = []
    n = int(round(seconds * FPS))
    for k in range(n):
        t = k / float(FPS)
        if (t % pause_every) > pause_every - pause_len:
            out.append(0.0)
            continue
        s = 0.5 + 0.5 * math.sin(2 * math.pi * syll_hz * t + rnd.uniform(-0.3, 0.3))
        out.append(round(0.35 + 1.2 * s * rnd.uniform(0.7, 1.15), 3))
    return out


def creep(u):
    """0..1 ease for a creep under a hold: accelerating (0.4 u + 0.6 u^2), so qa never finds a constant-speed (linear) run."""
    u = min(1.0, max(0.0, u))
    return 0.4 * u + 0.6 * u * u


def blend_cam(a, b, u):
    """Linear blend of two framings given as (loc, look_at): returns (loc, look_at)."""
    return (tuple(x + (y - x) * u for x, y in zip(a[0], b[0])), tuple(x + (y - x) * u for x, y in zip(a[1], b[1])))
