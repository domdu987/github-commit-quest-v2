#!/usr/bin/env python3
"""ghost_shots.py : the 19 shots of film 23 (film23/shot_plan.md, ESTIMATED timing): location, light, the camera move, the foreground prop, the set
state at the middle of the move and the stand marks of every character.  Pure python except dress() (builds the foreground prop).

Camera move model (local frame of the location; ghost.pose() adds the location origin):
  start = dict(loc, look_at, lens); the move runs over the planned length x 1.25 (t = 0 .. 1.25; t = 1 is the planned end) and is EASED:
  s(t) = 0.6 * sine-in-out(x) + 0.4 * x with x = t / 1.25 (no near-static ends, no linear look).  Moves:
    push  fraction of the camera-to-subject distance per second (+ in, - out; the plan's 6-10 %/s), exponential (constant zoom rate)
    slide lateral px/s at 720 wide (+ right), converted at the subject distance; both loc and look_at slide (a truck)
    rise  D/s of the camera height (+ up), look_at follows by `rise_look` x that
    end   an explicit pose at t = 1 instead (crane / reveal); the tail extrapolates the same eased path
    path  [(t, pose), ...] key poses for the BIGZOOMs (S01, S12), Catmull-Rom through them, distance to the subject interpolated in log space
"""
import math
from collections import OrderedDict

FPS = 30
SHOTS = OrderedDict()

def C(loc, look, lens=22.0): return dict(loc=tuple(float(x) for x in loc), look_at=tuple(float(x) for x in look), lens=float(lens))

def shot(n, t0, t1, loc, light, cam, move, note='', fg=None, state='', marks=None, trans=''):
    SHOTS['S%02d' % n] = dict(n=n, t0=t0, t1=t1, dur=round(t1 - t0, 3), loc=loc, light=light, cam=cam, move=move, note=note, fg=fg, state=state, marks=marks or {}, trans=trans)

def frames(name):
    """Frames of the take: planned length x 1.25 at 30 fps (the move covers all of them)."""
    return int(round(SHOTS[name]['dur'] * 1.25 * FPS))

def ease(x):
    x = max(0.0, min(1.0, x)); return 0.6 * (0.5 - 0.5 * math.cos(math.pi * x)) + 0.4 * x

# ----------------------------------------------------------------------------- vector helpers (pure python)
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _mul(a, k): return tuple(x * k for x in a)
def _len(a): return math.sqrt(sum(x * x for x in a))
def _lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))
def _norm(a): l = _len(a) or 1.0; return _mul(a, 1.0 / l)

def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return tuple(0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3) for a, b, c, d in zip(p0, p1, p2, p3))

def _path(keys, u):
    """keys: [(u_k, pose)], u in key units (u may run past the last key: linear extrapolation of the last segment).  Positions / look_at:
    Catmull-Rom; the eye-to-target vector is rebuilt with a log-interpolated length so zooms keep a steady rate."""
    us = [k[0] for k in keys]; P = [k[1] for k in keys]; n = len(keys)
    if u >= us[-1]:
        a, b = P[-2], P[-1]; t = 1.0 + (u - us[-1]) / (us[-1] - us[-2]); i = n - 2
    else:
        i = max(0, max(j for j in range(n - 1) if us[j] <= u)); t = (u - us[i]) / (us[i + 1] - us[i])
    def get(j): return P[max(0, min(n - 1, j))]
    if t > 1.0:                                                                   # the tail: keep pushing gently along the last direction
        a, b = get(i), get(i + 1); x = (t - 1.0) * (us[-1] - us[-2]) / us[-1]       # tail fraction of the whole path (0 .. ~0.25)
        look = _add(b['look_at'], _mul(_sub(b['look_at'], a['look_at']), 0.15 * x))
        db = _sub(b['loc'], b['look_at']); L = _len(db) * math.exp(-1.2 * x)
        return dict(loc=_add(look, _mul(_norm(db), L)), look_at=look, lens=b['lens'])
    look = _cr(get(i - 1)['look_at'], get(i)['look_at'], get(i + 1)['look_at'], get(i + 2)['look_at'], t)
    dirs = [_sub(get(j)['loc'], get(j)['look_at']) for j in (i - 1, i, i + 1, i + 2)]
    d = _norm(_cr(*[_norm(x) for x in dirs], t)); la, lb = _len(dirs[1]), _len(dirs[2]); L = la * (lb / la) ** t
    lens = get(i)['lens'] + (get(i + 1)['lens'] - get(i)['lens']) * t
    return dict(loc=_add(look, _mul(d, L)), look_at=look, lens=lens)

def pose(name, t, local=False):
    """Camera pose dict(loc, look_at, lens) of shot `name` at t (0 = start, 1 = planned end, 1.25 = end of the tail).  World frame unless local."""
    sh = SHOTS[name]; c0 = sh['cam']; mv = sh['move']; T = sh['dur'] * 1.25; s = ease(t / 1.25); s1 = ease(1.0 / 1.25)
    if 'path' in mv:
        keys = mv['path']; c = _path(keys, keys[-1][0] * s / s1)
    elif 'end' in mv:
        e = mv['end']; k = s / s1
        c = dict(loc=_lerp(c0['loc'], e['loc'], k), look_at=_lerp(c0['look_at'], e['look_at'], k), lens=c0['lens'] + (e['lens'] - c0['lens']) * k)
    else:
        loc, look = c0['loc'], c0['look_at']; d = _sub(loc, look); D = _len(d); tau = T * s
        D2 = D * math.exp(-mv.get('push', 0.0) * tau); loc = _add(look, _mul(_norm(d), D2))
        fwd = _norm((look[0] - c0['loc'][0], look[1] - c0['loc'][1], 0.0)); right = (fwd[1], -fwd[0], 0.0)
        half_w = D * 10.125 / c0['lens']; sh_ = mv.get('slide', 0.0) * tau * (2.0 * half_w / 720.0)
        loc = _add(loc, _mul(right, sh_)); look = _add(look, _mul(right, sh_))
        dz = mv.get('rise', 0.0) * tau; loc = _add(loc, (0, 0, dz)); look = _add(look, (0, 0, dz * mv.get('rise_look', 0.3)))
        if mv.get('orbit'):
            a = math.radians(mv['orbit'] * tau); v = _sub(loc, look); v = (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a), v[2]); loc = _add(look, v)
        c = dict(loc=loc, look_at=look, lens=c0['lens'] + mv.get('zoom', 0.0) * tau)
    if local: return c
    import ghost as GH
    return dict(loc=GH.to_world(c['loc'], sh['loc']), look_at=GH.to_world(c['look_at'], sh['loc']), lens=c['lens'])

# ----------------------------------------------------------------------------- marks
def face(p, cam):
    dx, dy = cam['loc'][0] - p[0], cam['loc'][1] - p[1]; return round(math.degrees(math.atan2(dx, -dy)), 1)

def M_(x, y, ph='soldier', pose='stand', z=None, parent=None, airborne=False, yaw=None):
    """One stand mark (local): z None = on the ground (ray cast at build), else kept (on a tank deck, a crate, a jeep seat)."""
    return dict(p=(x, y, z or 0.0), keep=z is not None, ph=ph, pose=pose, parent=parent, airborne=airborne, yaw=yaw)

def marks_local(name):
    """{role: [(x, y, z, keep_z or None, yaw, extra)]} local frame; yaw faces the START camera unless the mark sets one."""
    sh = SHOTS[name]; out = {}
    mk = sh['marks'] if isinstance(sh['marks'], dict) else sh['marks']()
    for role, lst in mk.items():
        out[role] = []
        for m in lst:
            yaw = m['yaw'] if m['yaw'] is not None else face(m['p'], sh['cam'])
            out[role].append((m['p'][0], m['p'][1], m['p'][2], True if m['keep'] else None, yaw, dict(ph=m['ph'], pose=m['pose'], parent=m['parent'], airborne=m['airborne'])))
    return out

# ----------------------------------------------------------------------------- foreground props (1-2 D from the lens), built per shot by build(shot)
def dress(name, Bk, M):
    """Build the shot's foreground prop (sh['fg'] = (kind, (x, y), yaw[, scale])) - a real grounded prop in the set, placed 1-2 D in front of the
    lens along the move (checked by ghost_sheet.fg_report)."""
    sh = SHOTS[name]
    if not sh['fg']: return
    import ghost_fg as FG
    for spec in (sh['fg'] if isinstance(sh['fg'], list) else [sh['fg']]): FG.make(spec, Bk, M)

# ============================================================================= the shot table
import ghost_shot_table   # noqa: E402,F401  (fills SHOTS)
