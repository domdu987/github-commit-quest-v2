#!/usr/bin/env python3
"""anim.py -- timing helpers shared by every shot file (stdlib only).

The timing grammar measured on the reference (spec/camera_motion.md, v2/out/HOOK_STUDY.md):
  * bodies and cameras are tweened on ones with eased curves (never linear, never stepped);
  * faces are whole drawings swapped in one frame; a blink is three one-frame drawings (half, closed, half) and an
    expression change happens on the closed frame;
  * camera snaps are 14-24 frames, sine to quintic in-out; drifts are eased and slow; whips are 3-5 blurred frames.
"""
import math

FPS = 30


def clamp(u, a=0.0, b=1.0):
    return a if u < a else b if u > b else u


def ease(u, kind="sine"):
    """eased progress for u in 0..1.  kinds: lin, sine (in-out, peak speed 1.57 x mean), smooth (smoothstep, 1.50),
    quint (in-out, 1.88), cubic (in-out), quad_out, cubic_out, quart_out, quad_in, cubic_in, back_out (small overshoot)."""
    u = clamp(u)
    if kind == "lin":
        return u
    if kind == "sine":
        return 0.5 - 0.5 * math.cos(math.pi * u)
    if kind == "smooth":
        return u * u * (3 - 2 * u)
    if kind == "quint":
        return 16 * u ** 5 if u < 0.5 else 1 - 16 * (1 - u) ** 5
    if kind == "cubic":
        return 4 * u ** 3 if u < 0.5 else 1 - 4 * (1 - u) ** 3
    if kind == "quad_out":
        return 1 - (1 - u) ** 2
    if kind == "cubic_out":
        return 1 - (1 - u) ** 3
    if kind == "quart_out":
        return 1 - (1 - u) ** 4
    if kind == "quad_in":
        return u * u
    if kind == "cubic_in":
        return u ** 3
    if kind == "back_out":                      # overshoots by about 6 percent, then settles
        c = 1.2
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    if kind == "hold":
        return 0.0 if u < 1.0 else 1.0
    raise ValueError(kind)


def lerp(a, b, t):
    if isinstance(a, (tuple, list)):
        return tuple(lerp(x, y, t) for x, y in zip(a, b))
    return a + (b - a) * t


def keys(f, ks):
    """piecewise eased keyframes.  ks = [(frame, value, ease_kind_of_the_segment_that_starts_here), ...]; values are numbers
    or tuples.  Before the first key the first value holds, after the last key the last value holds."""
    if f <= ks[0][0]:
        return ks[0][1]
    for (f0, v0, k0), nxt in zip(ks[:-1], ks[1:]):
        f1, v1 = nxt[0], nxt[1]
        if f <= f1:
            return lerp(v0, v1, ease((f - f0) / float(f1 - f0), k0))
    return ks[-1][1]


def cam_keys(f, ks):
    """camera keyframes [(frame, (cx, cy, zoom), ease)]: centre is interpolated linearly, zoom geometrically (a push-in
    that looks even is exponential in scale: s = s0 * (s1 / s0) ** e)."""
    ks2 = [(k[0], (k[1][0], k[1][1], math.log(k[1][2])), k[2]) for k in ks]
    cx, cy, lz = keys(f, ks2)
    return (cx, cy, math.exp(lz))


def blink(f, starts):
    """blink drawing for frame f: each start frame s gives half (s), closed (s + 1), half (s + 2).  Returns 0, 1 or 2."""
    for s in starts:
        d = f - s
        if d == 0 or d == 2:
            return 1
        if d == 1:
            return 2
    return 0


def swap(f, at, before, after):
    """a drawing that changes in one frame: `before` up to frame at - 1, `after` from frame `at` (put `at` on the closed
    frame of a blink: blink(f, [at - 1]))."""
    return after if f >= at else before


def pulse(f, f0, f1, f2, amp, k_in="quad_out", k_out="sine"):
    """0 -> amp over f0..f1, back to 0 over f1..f2 (a squash, a hop, an anticipation)."""
    if f <= f0 or f >= f2:
        return 0.0
    if f <= f1:
        return amp * ease((f - f0) / float(f1 - f0), k_in)
    return amp * (1 - ease((f - f1) / float(f2 - f1), k_out))


def smoothstep_mix(i, n):
    """weight of the incoming shot on frame i (1..n) of an n-frame dissolve: P*P*(3-2P) with P = i / (n + 1)."""
    p = i / float(n + 1)
    return p * p * (3 - 2 * p)
