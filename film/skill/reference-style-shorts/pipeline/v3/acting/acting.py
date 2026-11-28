#!/usr/bin/env python3
"""acting.py -- poses and cycles for the shot animators (build-order step 5 of plan/shot_plan.md).

    import sys; sys.path.insert(0, PROJ + "/v3/acting")
    import acting                      # registers the new drawings on import (also imports v3/cast/cast_ext)
    pose = acting.boss_walk(t)         # a plain v2 puppet pose dict for time t (seconds from the start of the action)
    puppet = acting.P                  # the v2 puppet module (same object as stage.sprites.puppet)

Every acting function is a PURE function of time: same inputs, same pose dict.  Times are seconds measured from the
start of the action (t = 0 on its first frame); event times passed as arguments are on the same local clock.  To drive
one from a film frame g: t = (g - g_start) / 30.  Bodies move on ones with eased curves; faces are whole drawings that
change on one frame (expression swaps sit on the closed frame of a blink: half, closed, half).

Keys a function may add that the puppet ignores (they start with an underscore) are for the shot's placement:
    _lift   D: raise the feet point (the card root) this far above the floor (jumps, run flight)
    _adv    D: forward travel along the facing direction since t = 0 (walk and run cycles: feet stay planted only if the
            card root moves by _adv; screen-right when the figure faces right, i.e. yaw > 0 unmirrored)
    _notes  list of (age_s, index) for the whistle's note glyphs (draw them with note_glyphs_svg)

New drawings registered on import (puppet.py is not edited; same wrapping method as v3/cast/cast_ext.py):
    mouths       whistle, laugh_open, talk_teeth, talk_small   (puppet.MOUTHS is extended)
    expressions  whistling, guffaw, cackle, gloat_talk, sleeping (hat-over-eyes sleep, no Z unless fx), sad_down, dazed
    props        ruler, tape, stamp, stub (pencil stub)        (puppet.PROP_TYPES / PROP_TIP are extended)
    pose keys    hat_dx, hat_dy, hat_rot (D, D, degrees in the head frame), hat_off (bool): move or remove the hat
See API.md next to this file.
"""
import math, os, sys, wave, array, bisect

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
for _p in (os.path.join(PROJ, "v3", "cast"), os.path.join(PROJ, "v2", "puppet"), os.path.join(PROJ, "v2", "shots")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import cast_ext                                   # noqa: E402  registers senior_a, senior_b, beach_man, beach_woman ...
import puppet as P                                # noqa: E402  the same module object stage.sprites uses
from anim import ease, keys, blink, pulse, lerp, clamp   # noqa: E402  (v2/shots/anim.py, read-only)

FPS = 30
NARRATION = os.path.join(PROJ, "audio", "th", "full_v2", "narration.wav")
AUDIO_OFFSET = 0.100                              # the narration is laid at +0.100 s in the film


def fr(t):
    """frame index of time t (s) on the 30 fps grid."""
    return int(round(t * FPS))


def blinks(t, starts):
    """blink drawing at time t for blinks starting at the given times (s): half, closed, half, one frame each.
    Returns 0, 1 or 2 (the puppet's `blink` key)."""
    return blink(fr(t), [fr(s) for s in starts])


def closed_at(t, at):
    """True from the closed frame of a blink that starts one frame before `at` (put expression swaps here)."""
    return fr(t) >= fr(at)


def go(u, c=1.2):
    """gesture ease: in-out with a small anticipation (dip of about 4 percent) and overshoot (about 4 percent), so a
    gesture starts and ends at rest (LOOK_SPEC 5.5.8: eased over 8 to 10 frames).  u = 0..1 (clamped)."""
    u = clamp(u)
    c2 = c * 1.525
    if u < 0.5:
        return ((2 * u) ** 2 * ((c2 + 1) * 2 * u - c2)) / 2
    return ((2 * u - 2) ** 2 * ((c2 + 1) * (u * 2 - 2) + c2) + 2) / 2


def arm_blend(cast, a, b, u):
    """an arm spec between two arm specs (preset names or dicts) at u = 0..1, through puppet.lerp_pose: the hand
    travels continuously (layer and hand shape switch at u = 0.5, as the puppet does)."""
    return P.lerp_pose(cast, {"arm_r": a}, {"arm_r": b}, clamp(u))["arm_r"]


def _merge(base, over):
    p = dict(base or {})
    p.update(over)
    return p


# ============================================================================= new drawings (registered on import)
_O = {}
_CURP = [None]
_INK_CAV = "#6b2a3c"
_TONGUE = "#e0707a"
_TEETH = "#fffaf4"


def _m_whistle(k, mx, my, C):
    """puckered round mouth, slightly toward the facing side: lip ring + dark hole + one lip highlight."""
    my = my - 0.012
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.036" ry="0.040" fill="%s" stroke="%s" stroke-width="0.024"/>'
            % (mx, my, k.c(_INK_CAV), k.ink))


def _m_laugh(k, mx, my, w=0.36, h=0.22, uid="lg"):
    """wide laughing mouth: flat-ish upper edge, deep lower curve, maroon cavity, upper teeth band, tongue."""
    hw = w / 2
    d = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (mx - hw, my - 0.035, mx, my - 0.005, mx + hw, my - 0.035, mx, my - 0.035 + 2 * h, mx - hw, my - 0.035))
    cid = k.uid + "_" + uid
    return ('<clipPath id="%s"><path d="%s"/></clipPath>'
            '<path d="%s" fill="%s"/>'
            '<g clip-path="url(#%s)"><rect x="%.4f" y="%.4f" width="%.4f" height="0.060" fill="%s"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/></g>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
            % (cid, d, d, k.c(_INK_CAV), cid, mx - hw, my - 0.060, w, k.c(_TEETH),
               mx + 0.01, my + h * 0.95, hw * 0.62, h * 0.45, k.c(_TONGUE), d, k.ink))


def _m_talk_teeth(k, mx, my, uid="tt"):
    """open talking mouth (wide oval) with the upper teeth showing."""
    cid = k.uid + "_" + uid
    return ('<clipPath id="%s"><ellipse cx="%.4f" cy="%.4f" rx="0.125" ry="0.064"/></clipPath>'
            '<ellipse cx="%.4f" cy="%.4f" rx="0.125" ry="0.064" fill="%s"/>'
            '<g clip-path="url(#%s)"><rect x="%.4f" y="%.4f" width="0.26" height="0.036" fill="%s"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="0.07" ry="0.03" fill="%s"/></g>'
            '<ellipse cx="%.4f" cy="%.4f" rx="0.125" ry="0.064" fill="none" stroke="%s" stroke-width="0.018"/>'
            % (cid, mx, my + 0.01, mx, my + 0.01, k.c(_INK_CAV), cid, mx - 0.13, my - 0.06, k.c(_TEETH),
               mx, my + 0.07, k.c(_TONGUE), mx, my + 0.01, k.ink))


def _m_talk_small(k, mx, my):
    """small o: the 'oo / w' drawing, smaller than talk_o."""
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.055" ry="0.050" fill="%s" stroke="%s" stroke-width="0.018"/>'
            % (mx, my + 0.01, k.c(_INK_CAV), k.ink))


NEW_MOUTHS = ("whistle", "laugh_open", "talk_teeth", "talk_small")
NEW_EXPR = {
    "whistling":  dict(eyes="closed", eye_dy=0.0, brows=("both", 0.190, -12.0, 0.040, 0.16, 0.0), mouth="whistle", mouth_dy=0.0),
    "guffaw":     dict(eyes="squeeze", brows=("both", 0.170, -14.0, 0.040, 0.16, 0.0), mouth="laugh_open", mouth_dy=0.0),
    "cackle":     dict(eyes="happy", brows=("both", 0.205, -10.0, 0.034, 0.15, 0.0), mouth="laugh_open", mouth_dy=0.0),
    "gloat_talk": dict(eyes="happy", brows=("both", 0.200, -8.0, 0.038, 0.16, 0.0), mouth="talk_teeth", mouth_dy=0.0),
    "sleeping":   dict(eyes="closed", eye_dy=0.02, brows=("both", 0.105, 0.0, 0.036, 0.15, 0.0), mouth="o_small_sleep"),
    "sad_down":   dict(eyes="half", brows=("both", 0.150, -24.0, 0.037, 0.16, 0.0), mouth="frown", mouth_dy=0.01),
    "dazed":      dict(eyes="ring", pupil=0.022, brows=None, mouth="dash"),
}


def _face(k, C, Pn, white):
    svg, L = _O["_face"](k, C, Pn, white)
    E = P.EXPRESSIONS.get(Pn["expr"]) or P.EXPRESSIONS["neutral"]
    m = Pn["mouth"] if Pn["mouth"] is not None else E.get("mouth")
    mdy = E.get("mouth_dy", 0.0) if Pn["mouth"] is None else 0.0
    mx, my = L["mx"], L["my"] + mdy
    add = ""
    if m == "whistle":
        add = _m_whistle(k, mx + 0.025 * Pn["yaw"], my, C)
    elif m == "laugh_open":
        add = _m_laugh(k, mx, my)
    elif m == "talk_teeth":
        add = _m_talk_teeth(k, mx, my)
    elif m == "talk_small":
        add = _m_talk_small(k, mx, my)
    elif m == "o_small_sleep":
        add = ('<ellipse cx="%.4f" cy="%.4f" rx="0.030" ry="0.026" fill="%s" stroke="%s" stroke-width="0.016"/>'
               % (mx + 0.02, my + 0.01, k.c(_INK_CAV), k.ink))
    return (add + svg if add else svg), L          # under the moustache and the eyes


def _norm(C, pose):
    _CURP[0] = pose if isinstance(pose, dict) else {}
    return _O["_norm"](C, pose)


def _hat_wrap(name):
    def f(k, C, yaw):
        pz = _CURP[0] or {}
        if pz.get("hat_off"):
            return "", (0.0, -0.484)
        svg, top = _O[name](k, C, yaw)
        dx, dy, rot = float(pz.get("hat_dx", 0.0) or 0.0), float(pz.get("hat_dy", 0.0) or 0.0), float(pz.get("hat_rot", 0.0) or 0.0)
        if dx == 0.0 and dy == 0.0 and rot == 0.0:
            return svg, top
        r = math.radians(rot)
        tx = top[0] * math.cos(r) - (top[1]) * math.sin(r) + dx
        ty = top[0] * math.sin(r) + top[1] * math.cos(r) + dy
        k.ext.append((tx, ty, 0.08))
        return '<g transform="translate(%.4f %.4f) rotate(%.3f 0 -0.30)">%s</g>' % (dx, dy, rot, svg), (tx, ty)
    return f


NEW_PROPS = ("ruler", "tape", "stamp", "stub")
NEW_TIP = {"ruler": 0.84, "tape": 0.50, "stamp": 0.21, "stub": 0.20}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS:
        return _O["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind == "ruler":            # wooden yard ruler, 0.96 long, held 0.12 from its near end, tick marks, no lettering
        o.append('<path d="M-0.120,-0.045 L0.840,-0.045 L0.840,0.045 L-0.120,0.045 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#e2b866"), ink))
        o.append('<path d="M-0.110,-0.028 L0.830,-0.028" stroke="%s" stroke-width="0.006" opacity="0.6"/>' % k.c("#f6dc9c"))
        d = "".join("M%.3f,0.045 L%.3f,%.3f" % (-0.10 + 0.0625 * i, -0.10 + 0.0625 * i, 0.045 - (0.040 if i % 4 == 0 else 0.022)) for i in range(15))
        o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (d, ink))
        ends = ((-0.12, -0.045), (0.84, -0.045), (0.84, 0.045), (-0.12, 0.045))
    elif kind == "tape":           # narrow teletype tape / paper strip, 0.55 x 0.09
        o.append('<path d="M-0.040,-0.045 L0.500,-0.045 L0.520,-0.010 L0.500,0.020 L0.515,0.045 L-0.040,0.045 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#fcf4e1"), ink))
        d = "".join("M%.3f,-0.012 L%.3f,-0.012" % (x, x + 0.025) for x in (0.05, 0.11, 0.17, 0.26, 0.33, 0.41))
        o.append('<path d="%s" stroke="%s" stroke-width="0.014" stroke-linecap="round" fill="none" opacity="0.8"/>' % (d, k.c("#8d8089")))
        ends = ((-0.04, -0.045), (0.52, -0.045), (0.52, 0.045), (-0.04, 0.045))
    elif kind == "stamp":          # rubber stamp: wooden knob and stem, red rubber foot at the working end
        o.append('<circle cx="-0.045" cy="0" r="0.055" fill="%s" stroke="%s" stroke-width="0.013"/>' % (k.c("#9a5a32"), ink))
        o.append('<rect x="-0.005" y="-0.025" width="0.150" height="0.050" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#b97845"), ink))
        o.append('<rect x="0.140" y="-0.090" width="0.050" height="0.180" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#7a4a2c"), ink))
        o.append('<rect x="0.188" y="-0.085" width="0.024" height="0.170" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#c8352e"), ink))
        ends = ((-0.10, -0.06), (0.21, -0.09), (0.21, 0.09), (-0.10, 0.06))
    else:                          # stub: worn red pencil, 0.26 long
        o.append('<path d="M-0.050,-0.019 L0.135,-0.019 L0.135,0.019 L-0.050,0.019 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#d5392f"), ink))
        o.append('<path d="M0.135,-0.019 L0.200,0 L0.135,0.019 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#ecd2a8"), ink))
        o.append('<path d="M0.180,-0.006 L0.200,0 L0.180,0.006 Z" fill="%s"/>' % k.c("#c8281f"))
        ends = ((-0.05, 0.0), (0.20, 0.0))
    o.append('</g>')
    for e in ends:
        x, y = P._rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = P._rot(NEW_TIP[kind] * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


def register():
    if getattr(P, "_acting_registered", False):
        return
    for name in ("_face", "_norm", "_hat_newsboy", "_hat_homburg", "_prop"):
        _O[name] = getattr(P, name)
    P._face = _face
    P._norm = _norm
    P._hat_newsboy = _hat_wrap("_hat_newsboy")
    P._hat_homburg = _hat_wrap("_hat_homburg")
    P._prop = _prop
    P.MOUTHS = tuple(P.MOUTHS) + tuple(m for m in NEW_MOUTHS + ("o_small_sleep",) if m not in P.MOUTHS)
    for n, e in NEW_EXPR.items():
        P.EXPRESSIONS.setdefault(n, e)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP)
    P._acting_registered = True


register()


# ============================================================================= overlays
def note_glyphs_svg(notes, origin=(0.25, -0.10), facing=1, ink="#3a2832", fill="#3a2832"):
    """SVG fragment (puppet-local D units) of the whistle's floating notes.  notes = pose["_notes"] = [(age_s, index)];
    each glyph rises 0.9 D and drifts 0.5 D ahead of the mouth over 1.1 s, rocking, fading out over its last 0.3 s.
    origin = where they start (pass the pose's anchors["mouth"]); facing = +1 right, -1 left.
    The sprite canvas must reach 1.2 D above the hat and 0.8 D ahead of the face (canvas_for + margin), or draw it in the
    overlay pass of the shot (same fragment, transformed to the screen)."""
    o = []
    for age, i in notes:
        u = clamp(age / 1.1)
        if u >= 1.0:
            continue
        x = origin[0] + facing * (0.12 + 0.50 * ease(u, "quad_out"))
        y = origin[1] - 0.15 - 0.90 * u
        rot = 14.0 * math.sin(age * 9.0 + i)
        op = 1.0 - ease((u - 0.73) / 0.27, "sine") if u > 0.73 else min(1.0, age / 0.07)
        s = 0.9 + 0.25 * ease(min(1.0, age / 0.15), "back_out")
        dbl = (i % 2 == 1)
        g = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.3f)" opacity="%.3f">' % (x, y, rot, s, op)]
        if dbl:   # beamed pair
            g.append('<ellipse cx="-0.07" cy="0.10" rx="0.045" ry="0.033" transform="rotate(-20 -0.07 0.10)" fill="%s"/>'
                     '<ellipse cx="0.07" cy="0.08" rx="0.045" ry="0.033" transform="rotate(-20 0.07 0.08)" fill="%s"/>'
                     '<path d="M-0.032,0.095 L-0.032,-0.10 L0.108,-0.12 L0.108,0.075" fill="none" stroke="%s" stroke-width="0.016"/>'
                     '<path d="M-0.032,-0.10 L0.108,-0.12" stroke="%s" stroke-width="0.040"/>' % (fill, fill, ink, ink))
        else:     # single quaver
            g.append('<ellipse cx="0" cy="0.10" rx="0.048" ry="0.035" transform="rotate(-20 0 0.10)" fill="%s"/>'
                     '<path d="M0.040,0.095 L0.040,-0.11 Q0.10,-0.05 0.11,0.01" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (fill, ink))
        g.append('</g>')
        o.append("".join(g))
    return "".join(o)


def flying_hat_svg(cast, yaw=0.5, uid="fh", tint=None):
    """the hat of `cast` alone (SVG fragment, D units, centred on the head-frame origin; the hat sits at y -0.3 .. -0.6)
    for a flying-hat card or overlay (beach_man's boater popping off, shot 24).  Pair with pose key hat_off=True."""
    C = P.CAST[cast]
    k = P._Ctx(uid, P.INK, P._norm(C, {"tint": tint})["tint"] if tint else None)
    _CURP[0] = {}
    if C["hat"] == "homburg":
        svg, _ = P._hat_homburg(k, C, yaw)
    else:
        svg, _ = P._hat_newsboy(k, C, yaw)
    return "<defs>%s</defs>%s" % ("".join(k.defs), svg)


# ============================================================================= loudness from the narration
_WAV = {}


def _wav_samples(path):
    if path not in _WAV:
        w = wave.open(path, "rb")
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
        w.close()
        if sw != 2:
            raise ValueError("16-bit WAV expected")
        a = array.array("h")
        a.frombytes(raw)
        if ch > 1:
            a = a[::ch]
        _WAV[path] = (a, sr)
    return _WAV[path]


def loudness(t0, t1, path=NARRATION, fps=FPS, win=0.033, median_win=1.0, gate=0.04):
    """per-frame loudness of the narration between narration-clock times t0 and t1 (s), as LOOK_SPEC 5.5 measures it:
    33 ms RMS centred on each frame time, divided by its running median (over +/- median_win/2 s of voiced frames).
    Returns a list of floats, one per frame: frame k is narration time t0 + k / fps, i.e. film frame
    round((t0 + 0.1) * 30) + k (the narration is laid at +0.100 s).  Values: 0 = silence (RMS below `gate` x the
    span's peak RMS), about 1 = typical speech, 1.5+ = loud.  Feed the list to boss_talk / talk_mouth."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path}: no narration here. The default is film 1's narration, which the skill does not ship: "
                                "pass path=<your narration.wav> (or a synthetic loudness list, examples/common.py synth_loud)")
    a, sr = _wav_samples(path)
    n = int(round((t1 - t0) * fps))
    hw = int(win * sr / 2)
    rms = []
    for i in range(n):
        c = int(round((t0 + i / float(fps)) * sr))
        lo, hi = max(0, c - hw), min(len(a), c + hw)
        if hi <= lo:
            rms.append(0.0)
            continue
        s = 0.0
        for j in range(lo, hi, 2):
            v = a[j]
            s += v * v
        rms.append(math.sqrt(s / max(1, (hi - lo + 1) // 2)) / 32768.0)
    peak = max(rms) if rms else 0.0
    voiced = [r if r > gate * peak else 0.0 for r in rms]
    out = []
    m = int(median_win * fps / 2)
    for i, r in enumerate(voiced):
        if r <= 0.0:
            out.append(0.0)
            continue
        w = sorted(x for x in voiced[max(0, i - m):i + m + 1] if x > 0.0)
        med = w[len(w) // 2] if w else r
        out.append(r / med if med > 0 else 0.0)
    return out


# ============================================================================= mouth flapping
_MCACHE = {}


def talk_mouth(loud, hold_min=3, hold_max=6):
    """mouth drawing per frame for a loudness list (see loudness()): a new drawing every 2 to 6 frames, chosen by level:
    silent (< 0.35) = 'flat' bar, low = 'talk_a', mid = 'talk_teeth', high (> 1.25) = 'talk_b' (held up to 4 frames);
    every fourth open change is the round 'talk_o' / 'talk_small' instead.  Deterministic; cached per list."""
    key = (tuple(round(x, 4) for x in loud), hold_min, hold_max)
    if key in _MCACHE:
        return _MCACHE[key]
    out = []
    cur, held, n_open = None, 0, 0
    for i, v in enumerate(loud):
        if v < 0.35:
            want = "flat"
        elif v < 0.8:
            want = "talk_a"
        elif v < 1.25:
            want = "talk_teeth"
        else:
            want = "talk_b"
        lim = 4 if cur == "talk_b" else hold_max
        change = cur is None or (held >= hold_min and want != cur) or held >= lim
        if change:
            if want == cur:            # forced change on a long steady level: the neighbouring drawing
                want = {"flat": "talk_small", "talk_a": "talk_small", "talk_teeth": "talk_a", "talk_b": "talk_teeth",
                        "talk_o": "talk_a", "talk_small": "flat"}[want]
                if v < 0.35:
                    want = "flat" if cur != "flat" else "talk_small"
            if want not in ("flat",):
                n_open += 1
                if n_open % 4 == 0:
                    want = "talk_o" if v >= 0.8 else "talk_small"
            if want != cur:
                cur, held = want, 0
        out.append(cur)
        held += 1
    _MCACHE[key] = out
    return out


def speaker_motion(t, accents=None, amp_roll=15.0, amp_dx=0.22, amp_dy=0.10, period=1.25, dur=10):
    """head and torso moves of a speaker (LOOK_SPEC 5.5.2): at each accent time (s; default every `period` s from
    0.05) the head moves to a new target, eased over `dur` frames: roll alternating +/- 10..20 deg, 0.15..0.30 D
    sideways, 0.08..0.15 D vertical; the torso follows at half amplitude.  Returns dict(head_roll, head_dx, head_dy, lean)."""
    if accents is None:
        accents = [0.05 + period * i for i in range(int(60 / period))]
    pts = [(-1.0, (0.0, 0.0, 0.0))]
    for i, a in enumerate(accents):
        s = 1 if i % 2 == 0 else -1
        k = 0.65 + 0.35 * ((i * 7) % 5) / 4.0                 # 0.65 .. 1.0 of the amplitude, deterministic
        pts.append((a, (s * amp_roll * k, s * amp_dx * k, (amp_dy if i % 3 == 1 else -0.4 * amp_dy) * k)))
    f = t * FPS
    ks = [(0.0, pts[0][1], "sine")]
    prev = pts[0][1]
    for (a, v) in pts[1:]:
        ks.append((a * FPS, prev, "sine"))
        ks.append((a * FPS + dur, v, "sine"))
        prev = v
    roll, dx, dy = keys(f, ks)
    return dict(head_roll=roll, head_dx=dx, head_dy=dy, lean=0.5 * roll * 0.6)


# ============================================================================= BOSS (the chief)
def boss_talk(t, loud, base=None, accents=None, expr="talking", eyes_expr=None):
    """the chief speaking one quoted line.
    t       s from the first frame of the line (frame k of `loud` is t = k / 30)
    loud    per-frame loudness list for the line (loudness(t0, t1)); after its end the mouth closes ('smirk')
    base    pose dict (or callable t -> dict) for the body and the gesture (e.g. boss_finger_wag(t)); its head_roll,
            head_dx, head_dy and lean are ADDED to the speaker motion
    accents phrase-accent times (s, local) for the head moves; default every 1.25 s
    expr    face drawing held while talking ('talking': half-lids and one brow; 'gloat_talk': laughing eyes)
    Eyes and brows hold; only the mouth changes, every 2-6 frames.  No blinks inside the line."""
    b = base(t) if callable(base) else dict(base or {})
    i = fr(t)
    ms = talk_mouth(loud)
    mouth = ms[i] if 0 <= i < len(ms) else ("flat" if i < 0 else "smirk")
    sm = speaker_motion(t, accents)
    p = dict(dict(yaw=-0.45, arm_r="hip", arm_l="down", legs="stand"), **b)
    p["head_roll"] = b.get("head_roll", 0.0) + sm["head_roll"]
    p["head_dx"] = b.get("head_dx", 0.0) + sm["head_dx"]
    p["head_dy"] = b.get("head_dy", 0.0) + sm["head_dy"]
    p["lean"] = b.get("lean", 0.0) + sm["lean"]
    p["expr"] = eyes_expr or b.get("expr", expr)
    if p["expr"] in ("smug", "unimpressed", "neutral"):
        p["expr"] = "talking"
    p["mouth"] = mouth
    p["blink"] = 0
    return p


def boss_walk(t, speed=0.75, facing=1, step=0.68, bob=0.47, sway=0.13, yaw=0.95, arms="behind", pointer=True,
              expr="smug", blinks_at=(), cast="boss"):
    """near-profile walk cycle (LOOK_SPEC 5.5.6): one step every `step` s (0.68), head bob `bob` D peak to peak
    (lowest at heel contact, highest at the passing position), `sway` D fore-and-aft head sway on the stride,
    legs alternating with the feet PLANTED while the body moves at `speed` D/s (the root must travel pose['_adv']).
    facing +1 = walks screen-right (yaw +), -1 = screen-left.  arms: 'behind' (hands behind the back, the pointer
    tucked under the arm if pointer=True) or 'swing'.  Works for every cast member (cast=...)."""
    C = P.CAST[cast]
    ph = t / step                                  # steps since t = 0
    k = ph % 2.0                                   # 0..2: right foot stance in 0..1, left foot stance in 1..2
    S = speed * step                               # step length (D)
    hip_h = C["leg"]
    # bob: crouch is deepest at contact (k = 0, 1), zero at passing (k = 0.5, 1.5)
    u = 0.5 - 0.5 * math.cos(2 * math.pi * ph)     # 0 at contact, 1 at passing
    crouch = clamp((0.6 * bob / (hip_h * 1.02)) * (1.0 - u), 0.0, 0.75)      # 60 % of the bob from the knees
    lift = 0.4 * bob * u                                                        # 40 % as a rise of the root at passing
    gy = _ankle_y(cast, crouch)

    def foot(k_):
        # stance (k_ in 0..1): planted, slides back from +S/2 to -S/2; swing (1..2): arcs forward
        if k_ < 1.0:
            return (S / 2 - S * k_, gy, 0.0)
        s = (k_ - 1.0)
        e = ease(s, "sine")
        return (-S / 2 + S * e, gy - 0.20 * math.sin(math.pi * s) * (0.6 + 0.4 * bob / 0.47), s)
    fr_, fl_ = foot(k), foot((k + 1.0) % 2.0)
    sx = 1 if facing >= 0 else -1
    legs = dict(preset="stand", crouch=crouch, foot_r=(sx * fr_[0] + 0.02 * sx, fr_[1]), foot_l=(sx * fl_[0] - 0.02 * sx, fl_[1]),
                toe_r=sx * (0.9 if fr_[2] == 0 else 0.6), toe_l=sx * (0.9 if fl_[2] == 0 else 0.6))
    hdx = sx * sway / 2 * math.sin(math.pi * ph)
    p = dict(yaw=sx * yaw, expr=expr, legs=legs, head_dx=hdx, lean=sx * (3.0 + 1.5 * u), head_roll=sx * 3.0 * math.sin(math.pi * ph),
             pitch=-0.1, blink=blinks(t, blinks_at), _adv=speed * t, _lift=lift)
    if arms == "behind":
        p["arm_r"] = "behind"
        p["arm_l"] = "behind"
        if pointer:   # far arm keeps the pointer tucked under it: hand at the chest, pointer running back past the hip
            near = "arm_r" if sx > 0 else "arm_l"
            p[near] = dict(hand=(sx * 0.18, 0.62 + 0.02 * u), bend=0.8, layer="front")
            p["prop_" + near[-1]] = dict(type="pointer", angle=(160.0 if sx > 0 else 20.0) + 4.0 * math.sin(math.pi * ph))
    else:
        sw = math.sin(math.pi * ph)
        near, far = ("r", "l") if sx > 0 else ("l", "r")
        p["arm_" + near] = dict(hand=(sx * (0.05 + 0.30 * sw), 0.66 - 0.06 * abs(sw)), bend=0.6, layer="front")
        p["arm_" + far] = dict(hand=(sx * (0.05 - 0.30 * sw), 0.66 - 0.06 * abs(sw)), bend=0.6, layer="back")
    return p


_ANK = {}


def _ankle_y(cast, crouch):
    key = (cast, round(crouch, 3))
    if key not in _ANK:
        f = P.figure(cast, dict(legs=dict(preset="stand", crouch=crouch)), "q")
        _ANK[key] = f["anchors"]["foot_r"][1]
    return _ANK[key]


def boss_whistle_stroll(t, notes_at=(0.3, 0.6, 0.9), speed=0.75, facing=1, **kw):
    """the chief strolling in, whistling (shot 17): boss_walk with the HELD whistle drawing ('whistling': eyes shut,
    brows up, round pucker; never flapping), hands behind the back, pointer under the arm.  notes_at: times (s) a note
    glyph leaves the mouth; pose['_notes'] lists the live ones for note_glyphs_svg(pose['_notes'], mouth anchor)."""
    p = boss_walk(t, speed=speed, facing=facing, expr="whistling", **kw)
    p["blink"] = 0
    p["pitch"] = -0.35
    p["head_roll"] = p["head_roll"] + (-6.0 if facing >= 0 else 6.0)
    p["_notes"] = [(t - a, i) for i, a in enumerate(notes_at) if 0.0 <= t - a < 1.1]
    return p


def boss_laugh_doubled(t, t_in=0.0, ramp=0.33, lean=25.0, facing=-1, bounce_hz=4.5, slap_at=(0.5,), pull_strip_at=None,
                       cast="boss"):
    """doubled over with laughter (shot 12, far at the wall): a HELD 'guffaw' drawing (squeezed eyes, wide open mouth),
    torso bowed `lean` deg toward `facing`, shoulders shaking `bounce_hz`, tears and blush; one hand on the belly, the
    other slapping the thigh at each time in slap_at.  t_in: start of the fold (s), eased over `ramp` s (expression
    swaps on a squeezed frame at t_in).  pull_strip_at: time (s) he pulls the paper strip (tape) out of his waistcoat
    with the far hand (eased over 0.4 s)."""
    sx = 1 if facing >= 0 else -1
    a = go((t - t_in) / ramp) if t >= t_in else 0.0
    sh = math.sin(2 * math.pi * bounce_hz * t) * (0.5 + 0.5 * a)
    slap = 0.0
    for s in slap_at:
        slap = max(slap, pulse(fr(t), fr(s) - 3, fr(s), fr(s) + 5, 1.0, "cubic_in", "sine"))
    on = t >= t_in
    p = dict(yaw=sx * 0.45, expr="guffaw" if on else "smug", lean=sx * lean * a + 1.2 * sh * a, head_roll=sx * (-14.0 * a) + 4.0 * sh * a,
             head_dx=sx * 0.10 * a, head_dy=0.03 * sh * a, pitch=0.3 * a,
             squash=(1.0 + 0.012 * sh * a, 1.0 - 0.018 * sh * a),
             legs=dict(preset="stand", crouch=0.10 * a, spread=0.10 * a),
             fx=(["tears", "blush"] if on else []), t=(t * 1.4) % 1.0)
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    p["arm_" + far] = dict(hand=(-sx * 0.05, 0.95), bend=0.9)                 # on the belly
    p["arm_" + near] = dict(hand=(sx * (0.50 + 0.10 * slap), 1.30 + 0.25 * slap - 0.25 * (1 - a)), bend=0.4, shape="open")
    if pull_strip_at is not None and t >= pull_strip_at - 0.05:
        u = ease((t - pull_strip_at) / 0.4, "cubic_out")
        p["arm_" + far] = dict(hand=(-sx * (0.05 - 0.45 * u), 0.85 - 0.25 * u), bend=0.6)
        p["prop_" + far] = dict(type="tape", angle=(-90.0 + sx * 40.0 * u) if sx > 0 else (-90.0 - 40.0 * u), scale=0.4 + 0.6 * u)
    return p


def boss_shocked(t, t_shock=0.2, before="smug", yaw=-0.45, drop_pointer_at=None, base=None, cast="boss"):
    """smug -> shocked behind a 3-frame blink (shot 25; also any cast member with cast=...).
    t_shock: closed frame of the blink (the face swaps there: ring eyes, O mouth, sweat); a 2-frame squash of 0.03 D
    on the swap, head pops back 0.08 D and up, arms flinch open over 5 frames (back_out).  drop_pointer_at: time the
    pointer (held in the near hand until then) falls out of the hand (it is simply gone from that frame: the falling
    pointer is a set prop)."""
    b = base(t) if callable(base) else dict(base or {})
    f = fr(t)
    fs = fr(t_shock)
    on = f >= fs
    sq = pulse(f, fs - 1, fs, fs + 2, 1.0, "lin", "lin")
    rec = ease((f - fs) / 6.0, "back_out") if on else 0.0
    sx = 1 if yaw >= 0 else -1
    p = dict(dict(yaw=yaw, arm_r="hip", arm_l="down", legs="stand"), **b)
    p.update(expr="shocked" if on else before, blink=blink(f, [fs - 1]),
             squash=(1.0 + 0.03 * sq, 1.0 - 0.03 * sq), head_dy=-0.06 * rec, head_dx=-sx * 0.08 * rec,
             lean=b.get("lean", 0.0) - sx * 4.0 * rec, pitch=-0.25 * rec, fx=(["sweat"] if on else []))
    if on:
        p["arm_r"] = dict(preset="shrug", hand=(0.62 * (0.6 + 0.4 * rec), 0.25 - 0.25 * rec), bend=-0.6, shape="open")
        p["arm_l"] = dict(preset="shrug", hand=(-0.62 * (0.6 + 0.4 * rec), 0.25 - 0.25 * rec), bend=-0.6, shape="open")
    near = "r" if sx > 0 else "l"
    if drop_pointer_at is not None:
        if t < drop_pointer_at:
            p["prop_" + near] = dict(type="pointer", angle=sx * 70.0 if sx > 0 else 110.0)
        else:
            p.pop("prop_" + near, None)
    return p


def boss_finger_wag(t, t0=0.0, dur=0.4, yaw=-0.45, wags=3):
    """'มันไม่ขึ้น' (shot 10): the near hand comes up to the shoulder with the index finger up and wags `wags` times
    within `dur` s from t0 (8 frames in, wag 5 Hz, 8 frames out).  Use as `base` of boss_talk."""
    sx = 1 if yaw >= 0 else -1
    near = "r" if sx > 0 else "l"
    up = go((t - t0) / 0.30) * (1 - ease((t - t0 - dur - 0.15) / 0.27, "sine"))
    w = math.sin(2 * math.pi * (wags / max(dur, 0.1)) * clamp(t - t0, 0, dur))
    p = dict(yaw=yaw, arm_r="hip", arm_l="hip", legs="stand", expr="smug")
    p["arm_" + near] = dict(preset="point", hand=(sx * (0.40 + 0.08 * w * up), 0.50 - 0.80 * up), bend=-0.7, shape="point")
    p["head_roll"] = -sx * 6.0 * w * up
    return p


def boss_lean_wink(t, t0=0.0, wink_at=0.6, wink_len=0.15, yaw=-0.45, horn=False):
    """'ทางด่วนหรอก' / 'รถติดเหรอ' (shots 10, 18): leans 0.25 D toward the side he faces with laughing eyes
    ('gloat_talk'), then a HELD wink from wink_at for wink_len s.  horn=True: both hands in front of the chest squeeze
    an imaginary car horn twice (shot 18).  Use as `base` of boss_talk (its expr is kept)."""
    sx = 1 if yaw >= 0 else -1
    a = go((t - t0) / 0.33) if t >= t0 else 0.0
    p = dict(yaw=yaw, arm_r="hip", arm_l="hip", legs=dict(preset="stand", stride=0.3 * sx * a), lean=sx * 9.0 * a,
             head_dx=sx * 0.12 * a, expr="gloat_talk" if t >= t0 else "smug")
    if wink_at <= t < wink_at + wink_len:
        p["expr"] = "wink"
    if horn:
        sq = abs(math.sin(2 * math.pi * 3.0 * max(0.0, t - t0 - 0.1)))
        p["arm_r"] = dict(hand=(0.30 * sx + 0.12, 0.70 - 0.05 * sq), bend=0.5, shape="open")
        p["arm_l"] = dict(hand=(0.30 * sx - 0.12, 0.72 - 0.05 * sq), bend=0.5, shape="open")
    return p


def boss_mock_search(t, t0=0.0, yaw=-0.3):
    """'ไหนล่ะ' (shot 18): hand shading his eyes ('shade'), torso turning left and right looking for something."""
    a = go((t - t0) / 0.30) if t >= t0 else 0.0
    sw = math.sin(2 * math.pi * 1.4 * max(0.0, t - t0))
    p = dict(yaw=yaw + 0.35 * sw * a, arm_r=arm_blend("boss", "hip", "shade", a), arm_l="hip", lean=4.0 * sw * a, pitch=-0.2 * a,
             head_dx=0.06 * sw * a, legs="stand", expr="smug")
    return p


def boss_pointer_whack(t, t_land=0.5, yaw=0.4, raise_len=0.3, target=(1.05, -0.35)):
    """pointer raised then whacked down (shot 6; the taps of shot 18 with two calls): the near hand rises with the
    pointer over raise_len s (anticipation, pointer tip up), whips down onto `target` (puppet-local tip position) at
    t_land in 3 frames, 2-frame squash on contact, small rebound.  Pin the tip in 3D by passing the returned
    prop angle with a world tip to Actor.pose(hands=...); the pose here is the unpinned drawing."""
    sx = 1 if yaw >= 0 else -1
    near = "r" if sx > 0 else "l"
    t_up = t_land - 0.1 - raise_len
    up = ease((t - t_up) / raise_len, "sine") if t >= t_up else 0.0
    dn = ease((t - (t_land - 0.1)) / 0.1, "cubic_in") if t >= t_land - 0.1 else 0.0
    reb = pulse(fr(t), fr(t_land), fr(t_land) + 2, fr(t_land) + 7, 1.0)
    ang_up, ang_dn = -70.0, math.degrees(math.atan2(target[1] + 0.0, target[0]))
    ang = lerp(lerp(-20.0, ang_up, up), ang_dn - 6.0 * reb, dn) if sx > 0 else 180.0 - lerp(lerp(-20.0, ang_up, up), ang_dn - 6.0 * reb, dn)
    hand = lerp(lerp((0.40, 0.55), (0.42, 0.05), up), (0.46, 0.30 - 0.03 * reb), dn)
    sq = pulse(fr(t), fr(t_land) - 1, fr(t_land), fr(t_land) + 2, 1.0, "lin", "lin")
    p = dict(yaw=yaw, expr="smug", arm_r="hip", arm_l="hip", legs="stand", lean=sx * (-4.0 * up + 8.0 * dn),
             head_roll=sx * (-6.0 * up + 6.0 * dn), squash=(1.0 + 0.02 * sq, 1.0 - 0.02 * sq))
    p["arm_" + near] = dict(hand=(sx * hand[0], hand[1]), bend=-0.5)
    p["prop_" + near] = dict(type="pointer", angle=ang)
    return p


def boss_thumb_jerk(t, t0=0.0, yaw=0.4, expr="smug", cast="boss"):
    """jerks a thumb back over his shoulder (shots 9, 12): the far hand snaps up beside the far shoulder, point shape
    toward the back, in 5 frames (back_out), holds, goes back after 0.8 s.  Works for every cast member."""
    sx = 1 if yaw >= 0 else -1
    far = "l" if sx > 0 else "r"
    a = go((t - t0) / 0.30) * (1 - ease((t - t0 - 0.8) / 0.3, "sine")) if t >= t0 else 0.0
    p = dict(yaw=yaw, expr=expr, arm_r="hip", arm_l="hip", legs="stand", head_roll=sx * 8.0 * a, lean=-sx * 3.0 * a)
    p["arm_" + far] = dict(preset="point", hand=(-sx * (0.30 + 0.15 * a), 0.55 - 0.45 * a), bend=-0.6 * a + 0.5 * (1 - a), shape="point" if a > 0.3 else "ball")
    return p


def boss_eraser_bounce(t, yaw=-0.45, hz=1.6):
    """shot 10 opening: bounces the eraser in his near palm (the eraser hops 0.12 D, palm dips on the catch), smirk."""
    sx = 1 if yaw >= 0 else -1
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    ph = (t * hz) % 1.0
    hop = math.sin(math.pi * ph)                        # eraser in the air
    dip = (1.0 - hop) ** 4
    p = dict(yaw=yaw, expr="smirk", arm_r="hip", arm_l="hip", legs="stand", head_roll=sx * 3.0 * hop, pitch=0.15)
    p["arm_" + near] = dict(hand=(sx * 0.48, 0.58 - 0.14 * hop + 0.04 * dip), bend=0.3, shape="open")
    p["prop_" + near] = dict(type="eraser", angle=-90.0 + 10.0 * math.sin(2 * math.pi * ph), scale=1.0)
    return p


def boss_rub_furious(t, t0=0.0, stroke=0.33, fill_len=0.8, yaw=0.5):
    """shot 11c: rubs with big strokes (one stroke every `stroke` s), face reddening (anger_fill rising over fill_len s),
    steam, 'furious'.  Pin the eraser face in 3D (prop eraser in the near hand, returned angle)."""
    sx = 1 if yaw >= 0 else -1
    near = "r" if sx > 0 else "l"
    ph = 2 * math.pi * max(0.0, t - t0) / stroke
    rmp = ease((t - t0) / 0.2, "sine")                  # strokes grow over the first 6 frames
    lev = ease((t - t0) / fill_len, "sine")
    p = dict(yaw=yaw, expr="furious" if lev > 0.3 else "angry", pitch=-0.6, lean=sx * (6.0 + 5.0 * math.sin(ph)),
             head_roll=sx * 4.0 * math.sin(ph + 0.6), legs=dict(preset="stand", crouch=0.05, stride=0.4 * sx),
             fx=[dict(type="anger_fill", level=lev, t=(t * 2) % 1.0)] + ([dict(type="steam", t=(t * 1.5) % 1.0)] if lev > 0.5 else []),
             arm_r="hip", arm_l="hip")
    p["arm_" + near] = dict(preset="rub", hand=(sx * (0.55 + 0.18 * rmp * math.sin(ph)), -0.35 + 0.10 * rmp * math.cos(ph)), stretch=1.15, bend=-0.5)
    p["prop_" + near] = dict(type="eraser", angle=(-140.0 if sx > 0 else -40.0) + 10.0 * math.sin(ph))
    return p


def boss_frozen_purple(t, twitch_every=0.4, yaw=0.5):
    """shot 11 'ลากอีก': frozen, full purple, one eye twitching (a half-lid frame every twitch_every s), steam."""
    f = fr(t)
    tw = 1 if (f % max(2, fr(twitch_every))) in (0,) else 0
    return dict(yaw=yaw, expr="furious", pitch=-0.6, blink=tw, gaze=(0.3, 0.0), arm_r="hip", arm_l="hip", legs="stand",
                fx=[dict(type="anger_fill", level=1.0, t=(t * 2) % 1.0), dict(type="steam", t=(t * 1.5) % 1.0)])


def boss_pant(t, pants_at=(0.1, 0.55), yaw=0.45, nub=True):
    """shot 11d: two pants (shoulders heave 0.05 D, mouth open on each) holding a worn eraser nub at his side."""
    f = fr(t)
    h = 0.0
    op = False
    for a in pants_at:
        v = pulse(f, fr(a), fr(a) + 4, fr(a) + 11, 1.0)
        h = max(h, v)
        op = op or (fr(a) <= f < fr(a) + 7)
    sx = 1 if yaw >= 0 else -1
    near = "r" if sx > 0 else "l"
    p = dict(yaw=yaw, expr="worried", mouth="talk_a" if op else "frown", head_dy=-0.05 * h, lean=sx * 3.0 * h,
             squash=(1.0 - 0.01 * h, 1.0 + 0.015 * h), legs=dict(preset="wide", crouch=0.06), arm_r="down", arm_l="down",
             fx=["sweat"], pitch=0.2)
    if nub:
        p["arm_" + near] = dict(hand=(sx * 0.42, 0.75), bend=0.5)
        p["prop_" + near] = dict(type="eraser", angle=-90.0, scale=0.6)
    return p


def boss_stamp_thrust(t, stamp_at=0.0, tear_at=0.13, thrust_at=0.28, yaw=0.35):
    """shot 14: stamp down onto the teletype header at stamp_at (stamp in the near hand, 4 frames down, squash),
    tear the sheet off at tear_at (both hands snap up), thrust it at the lens at thrust_at (sheet in the near hand,
    arm straight forward, leaning in), smug nod after."""
    sx = 1 if yaw >= 0 else -1
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    f = fr(t)
    p = dict(yaw=yaw, expr="smug", arm_r="hip", arm_l="hip", legs="stand")
    if t < tear_at:
        d = ease((t - (stamp_at - 0.13)) / 0.13, "cubic_in") if t >= stamp_at - 0.13 else 0.0
        p["arm_" + near] = dict(hand=(sx * 0.55, 0.05 + 0.55 * d), bend=-0.3)
        p["prop_" + near] = dict(type="stamp", angle=90.0)
        sq = pulse(f, fr(stamp_at) - 1, fr(stamp_at), fr(stamp_at) + 2, 1.0, "lin", "lin")
        p["squash"] = (1 + 0.02 * sq, 1 - 0.02 * sq)
    elif t < thrust_at:
        u = ease((t - tear_at) / 0.1, "cubic_out")
        p["arm_" + near] = dict(hand=(sx * 0.55, 0.35 - 0.25 * u), bend=-0.5)
        p["prop_" + near] = dict(type="paper", angle=-90.0 + sx * 20.0 * u if sx > 0 else -90.0 - 20.0 * u)
        p["arm_" + far] = dict(hand=(sx * 0.15, 0.30 - 0.10 * u), bend=-0.3)
    else:
        u = go((t - thrust_at) / 0.30)
        nod = pulse(f, fr(thrust_at) + 6, fr(thrust_at) + 10, fr(thrust_at) + 18, 1.0)
        p["arm_" + near] = dict(hand=(sx * (0.55 + 0.15 * u), 0.10 + 0.25 * u), bend=-0.4, stretch=1.1)
        p["prop_" + near] = dict(type="paper", angle=sx * 0.0 if sx > 0 else 180.0)
        p["lean"] = sx * 8.0 * u
        p["head_dx"] = sx * 0.08 * u
        p["pitch"] = 0.35 * nod
    return p


def boss_read_tape(t, tear_at=0.4, yaw=-0.35):
    """shot 4 (wide, by the teletype): reads a paper tape held in both hands at chest height, tears it at tear_at
    (hands part 0.15 D in 3 frames), eyes down.  Blinks: pass via the shot."""
    sx = 1 if yaw >= 0 else -1
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    tr = ease((t - tear_at) / 0.1, "cubic_out") if t >= tear_at else 0.0
    p = dict(yaw=yaw, expr="unimpressed", pitch=0.6, gaze=(0.0, 0.8), arm_r="hip", arm_l="hip", legs="stand", lean=sx * 2.0)
    p["arm_" + near] = dict(hand=(sx * (0.42 + 0.10 * tr), 0.55 - 0.05 * tr), bend=0.4)
    p["prop_" + near] = dict(type="tape", angle=180.0 if sx > 0 else 0.0, scale=0.9 - 0.4 * tr)
    p["arm_" + far] = dict(hand=(-sx * (0.05 + 0.10 * tr), 0.58), bend=0.6)
    return p


# ============================================================================= HERO
def hero_slumped(t, yaw=0.5, blinks_at=(0.83,), turn_hz=0.8, expr="sad_down"):
    """shot 17: slumped at gloat_near (lean 4 deg toward the facing side, head down, pitch 1), sad, both hands in front
    of the belt turning the pencil STUB slowly (a rocking twist, 0.8 turns per second), nearly frozen (breathing:
    0.01 D).  Head stays under 0.04 D of travel (listener)."""
    sx = 1 if yaw >= 0 else -1
    tw = math.sin(2 * math.pi * turn_hz * t)
    br = math.sin(2 * math.pi * t / 3.2)
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    p = dict(yaw=yaw, expr=expr, pitch=1.0, lean=sx * 4.0, head_dx=sx * 0.04, head_dy=0.06 + 0.008 * br, head_roll=sx * 5.0,
             legs=dict(preset="narrow", crouch=0.03), blink=blinks(t, blinks_at), gaze=(0.0, 0.6))
    p["arm_" + near] = dict(hand=(sx * 0.10 + 0.02 * tw, 0.86), bend=0.8)
    p["arm_" + far] = dict(hand=(-sx * 0.02 - 0.02 * tw, 0.90), bend=0.8)
    p["prop_" + near] = dict(type="stub", angle=-20.0 + 55.0 * tw if sx > 0 else 200.0 - 55.0 * tw)
    return p


def hero_sad_listener(t, yaw=0.55, blinks_at=(0.28, 0.88), shut=(1.48, 0.13), sweat_at=0.98, expr="sad"):
    """shot 18 near hero: frozen, sad, eyes down; blinks at blinks_at; shuts his eyes for shut[1] s from shut[0]
    (closed lines, held); sweat drop from sweat_at.  His mouth never moves.  Travel under 0.02 D."""
    f = fr(t)
    s0, sl = shut
    b = blinks(t, blinks_at)
    if fr(s0) <= f < fr(s0 + sl):
        b = 2
    elif f == fr(s0) - 1 or f == fr(s0 + sl):
        b = max(b, 1)
    return dict(yaw=yaw, expr=expr, pitch=0.9, gaze=(0.2, 0.7), blink=b, head_dy=0.005 * math.sin(t * 2.0),
                arm_r=dict(hand=(0.12, 0.80), bend=0.8), arm_l=dict(hand=(-0.02, 0.84), bend=0.8),
                prop_r=dict(type="stub", angle=-30.0), legs="narrow", fx=(["sweat"] if t >= sweat_at else []))


def hero_listener(t, yaw=0.6, expr="unimpressed", blinks_at=(0.33, 0.93, 1.73), gaze_shift=(1.53, (0.9, -0.1), (-0.4, 0.1)),
                  pencil_ear=True):
    """the frozen listener (shot 10 near hero; 11c): three-quarter, half-lids, pencil behind the ear, blinks only and
    one sideways gaze shift (time, gaze before, gaze after; the pupils jump on one frame).  Under 0.04 D of travel."""
    g = gaze_shift[1] if t < gaze_shift[0] else gaze_shift[2]
    return dict(yaw=yaw, expr=expr, blink=blinks(t, blinks_at), gaze=g, head_dy=0.004 * math.sin(t * 2.2),
                arm_r="down", arm_l="down", legs="stand")


def hero_stunned(t, t_swap=0.1, close_at=0.6, from_expr="unimpressed", yaw=0.55):
    """shot 25 near hero: stunned (ring eyes, raised brow) behind a blink at t_swap, then from close_at shuts his eyes
    (held closed lines) and lowers his head 0.1 D over 12 frames.  No triumph, no mouth."""
    f = fr(t)
    on = f >= fr(t_swap)
    p = dict(yaw=yaw, expr="stunned" if on else from_expr, blink=blink(f, [fr(t_swap) - 1]), legs="stand",
             arm_r="down", arm_l="down")
    if on:
        sq = pulse(f, fr(t_swap) - 1, fr(t_swap), fr(t_swap) + 2, 1.0, "lin", "lin")
        p["squash"] = (1 - 0.02 * sq, 1 + 0.03 * sq)
    if t >= close_at:
        d = ease((t - close_at) / 0.4, "sine")
        p["blink"] = 2 if f > fr(close_at) else 1
        p["expr"] = "sad"
        p["head_dy"] = 0.10 * d
        p["pitch"] = 0.9 * d
        p["head_roll"] = 4.0 * d
    return p


def hero_redraw(t, t0=0.0, swipe=8, yaw=0.55, start=(0.30, 0.15), end=(0.62, -0.62), ruler=False, stub=False):
    """the redraw-with-ruler arm cycle (shots 9, 11): the near hand sweeps the pencil point from `start` to `end`
    (puppet-local tip positions, D) in `swipe` frames from t0 (quint ease), the far hand holds the ruler along the
    same line, pressed to the map.  Before t0 he is set (pencil on start); after the swipe the arm stays at the end
    with a 3-frame overshoot.  In 3D pin the tip: Actor.pose(hands={'r': {'tip': world, 'prop': 'pencil',
    'angle': pose['_tip_angle']}}).  pose['_tip'] is the unpinned local tip target."""
    u = ease((t - t0) / (swipe / float(FPS)), "sine") if t >= t0 else 0.0
    ov = pulse(fr(t), fr(t0) + swipe, fr(t0) + swipe + 2, fr(t0) + swipe + 6, 1.0)
    dx, dy = end[0] - start[0], end[1] - start[1]
    L = math.hypot(dx, dy)
    tip = (start[0] + dx * (u + 0.04 * ov), start[1] + dy * (u + 0.04 * ov))
    ang = math.degrees(math.atan2(dy, dx)) - 25.0
    pr = "stub" if stub else "pencil"
    hand = P.hand_for_tip(pr, tip, ang)
    p = dict(yaw=yaw, expr="determined", pitch=-0.3 - 0.3 * u, head_roll=6.0 + 6.0 * u, lean=-3.0 * u, legs=dict(preset="wide", crouch=0.05),
             gaze=(0.7, -0.6 * u), arm_r=dict(hand=hand, stretch=1.1, bend=-0.3), prop_r=dict(type=pr, angle=ang),
             _tip=tip, _tip_angle=ang)
    if ruler:
        ra = math.degrees(math.atan2(dy, dx))
        rh = (start[0] - 0.22 + dx * 0.15, start[1] + 0.08 + dy * 0.15)
        p["arm_l"] = dict(hand=(rh[0] + 0.25, rh[1]), bend=-0.6, layer="front")
        p["prop_l"] = dict(type="ruler", angle=ra)
    else:
        p["arm_l"] = "hip"
    return p


def hero_ruler_rest(t, yaw=0.5, blinks_at=(0.4,)):
    """shot 11d: at ease with the ruler shouldered like a rifle, chin up, calm half-lids; blinks."""
    return dict(yaw=yaw, expr="neutral", pitch=-0.3, head_roll=-4.0, blink=blinks(t, blinks_at), legs="stand",
                arm_r=dict(hand=(0.36, 0.50), bend=0.9), prop_r=dict(type="ruler", angle=-62.0), arm_l="down",
                head_dy=0.004 * math.sin(t * 2.0))


def hero_study(t, yaw=-0.5, blinks_at=(0.6,)):
    """shot 4: three-quarter, chin in hand, pencil behind the ear, studying the map (held, blinks)."""
    return dict(yaw=yaw, expr="neutral", pitch=-0.4, gaze=(-0.6, -0.6), arm_l="chin", arm_r=dict(hand=(-0.05, 0.75), bend=0.9),
                blink=blinks(t, blinks_at), legs="stand", head_roll=-5.0)


# ============================================================================= SENIORS
def senior_nod(t, nods_at=(0.0,), cast="senior_a", yaw=0.4, expr="unimpressed", depth=0.6, blinks_at=()):
    """nod: head pitches down `depth` (puppet pitch units) and dips 0.05 D in 4 frames, comes back in 6, at each
    time in nods_at (shot 6: 10.80 and 11.00 together).  Torso follows slightly."""
    f = fr(t)
    n = 0.0
    for a in nods_at:
        n = max(n, pulse(f, fr(a), fr(a) + 4, fr(a) + 10, 1.0, "quad_out", "sine"))
    arms = "behind" if cast == "senior_b" else "down"
    return dict(yaw=yaw, expr=expr, pitch=depth * n, head_dy=0.05 * n, head_roll=(5.0 if yaw >= 0 else -5.0) * n,
                lean=(2.0 if yaw >= 0 else -2.0) * n, blink=blinks(t, blinks_at), arm_r=arms, arm_l=arms, legs="stand")


def senior_laugh(t, cast="senior_a", yaw=0.4, phase=0.0, hz=3.0, bounce=0.06, roll=15.0, thumb_at=None, expr="laughing"):
    """laughing as a HELD drawing (shot 12, also any cast): happy-arc eyes and wide grin (`expr`), head rolled `roll`
    deg, tears and blush; the BODY bounces 0.06 D at 3 Hz (phase in cycles: give the two seniors 0.0 and 0.5),
    shoulders hunching, head rocking a few degrees on the bounce.  thumb_at: time (s) he jerks a thumb back at the
    map with the far hand (held 0.8 s).  pose['_lift'] carries the bounce (feet-point lift, D)."""
    sx = 1 if yaw >= 0 else -1
    ph = 2 * math.pi * (hz * t + phase)
    b = 0.5 - 0.5 * math.cos(ph)                     # 0..1
    j = math.sin(ph)
    p = dict(yaw=yaw, expr=expr, head_roll=sx * roll + 5.0 * j, lean=sx * (9.0 + 4.0 * b), head_dy=-0.04 * b, head_dx=sx * (0.08 + 0.04 * j),
             squash=(1.0 - 0.015 * b, 1.0 + 0.02 * b), pitch=-0.2,
             legs=dict(preset="stand", crouch=0.035 * (1 - b)), fx=["tears", "blush"], t=(t * 1.3 + phase) % 1.0)
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    p["arm_" + near] = dict(hand=(sx * 0.25, 0.80 - 0.04 * b), bend=0.8)        # holding his belly
    p["arm_" + far] = dict(hand=(-sx * 0.30, 0.78 - 0.04 * b), bend=0.8)
    if thumb_at is not None and t >= thumb_at:
        a = go((t - thumb_at) / 0.30) * (1 - ease((t - thumb_at - 0.8) / 0.3, "sine"))
        if a > 0.01:
            p["arm_" + far] = dict(preset="point", hand=(-sx * (0.45 + 0.20 * a), 0.78 - 0.80 * a), bend=-0.6, shape="point", layer="top")
    p["_lift"] = bounce * b
    return p


# ============================================================================= BEACH
def beach_sleep(t, breath=1.3, facing=1, recline=42.0, z=True, cast="beach_man"):
    """asleep in a deck chair, side-on (shot 8): near-profile (facing +1 = toward screen-right), torso reclined
    `recline` deg back, legs out in front with knees up (foot targets), hands folded on the belly, the boater tipped
    over his eyes (hat_dy / hat_rot), 'sleeping' face with a little o of a mouth, Z rising (fx zzz) and a slow chest
    rise every `breath` s (shoulders and head lift 0.03 D, eased).  The feet point is the heels on the sand; put the
    card in the side plane of the chair with its root at the heels and the seat under the hips (pose['_seat'] is the
    local hip point the chair seat must carry)."""
    sx = 1 if facing >= 0 else -1
    b = 0.5 - 0.5 * math.cos(2 * math.pi * t / breath)
    hip = _hip_after_lean(cast, -sx * recline)
    gy = hip[1] + 0.55
    p = dict(yaw=sx * 1.0, expr="sleeping", lean=-sx * (recline - 2.0 * b), head_roll=-sx * (recline * 0.55 - 2.0 * b), head_dy=-0.03 * b,
             hat_dy=0.25, hat_rot=-sx * 14.0, hat_dx=sx * 0.06, pitch=0.3,
             legs=dict(preset="stand", foot_r=(hip[0] + sx * 1.05, gy), foot_l=(hip[0] + sx * 0.95, gy + 0.02),
                       knee_r=sx * 1.0, knee_l=sx * 1.0, toe_r=sx * 0.6, toe_l=sx * 0.6),
             arm_r=dict(hand=(hip[0] + sx * 0.05, hip[1] - 0.25 - 0.02 * b), bend=0.9), arm_l=dict(hand=(hip[0] - sx * 0.02, hip[1] - 0.20 - 0.02 * b), bend=0.9),
             fx=([dict(type="zzz", t=(t / 0.65) % 1.0)] if z else []), _seat=hip)
    return p


_HIPL = {}


def _hip_after_lean(cast, lean):
    k = (cast, round(lean, 2))
    if k not in _HIPL:
        f = P.figure(cast, dict(lean=lean, yaw=1.0 if lean <= 0 else -1.0), "q")
        _HIPL[k] = f["anchors"]["hip"]
    return _HIPL[k]


def beach_stretch(t, t0=0.0, facing=1, cast="beach_man"):
    """shot 16: steps off and stretches (arms up and out over 10 frames, back arched 8 deg, eyes closed, 'happy'),
    holds 0.4 s, arms come down; looks up from t0 + 0.9 (pitch -0.8)."""
    sx = 1 if facing >= 0 else -1
    a = go((t - t0) / 0.33) if t >= t0 else 0.0
    d = ease((t - t0 - 0.75) / 0.3, "sine") if t >= t0 + 0.75 else 0.0
    up = a * (1 - d)
    look = ease((t - t0 - 0.9) / 0.27, "sine") if t >= t0 + 0.9 else 0.0
    p = dict(yaw=sx * 0.55, expr="happy" if up > 0.3 else "neutral", blink=2 if 0.3 < up and t < t0 + 0.75 else 0,
             lean=-sx * 8.0 * up, pitch=-0.6 * up - 0.8 * look, head_roll=-sx * 6.0 * up, squash=(1 - 0.02 * up, 1 + 0.04 * up),
             legs=dict(preset="stand", crouch=0.02 * (1 - up)),
             arm_r=dict(hand=lerp((0.20, 0.62), (0.62, -0.42), up), bend=-0.7 * up + 0.5 * (1 - up), stretch=1.0 + 0.3 * up, shape="open" if up > 0.5 else "ball"),
             arm_l=dict(hand=lerp((-0.20, 0.62), (-0.58, -0.45), up), bend=-0.7 * up + 0.5 * (1 - up), stretch=1.0 + 0.3 * up, shape="open" if up > 0.5 else "ball"))
    return p


def beach_palm_out(t, t0=0.0, drops_at=(0.1, 0.25, 0.4), facing=1, cast="beach_man", expr="unimpressed"):
    """shot 16: the near palm comes out flat (open hand, shoulder height) over 8 frames from t0 and feels for rain;
    each drop (times) dips the palm 0.04 D on 2 frames; eyes on the palm."""
    sx = 1 if facing >= 0 else -1
    near = "r" if sx > 0 else "l"
    a = go((t - t0) / 0.30) if t >= t0 else 0.0
    dip = 0.0
    for d_ in drops_at:
        dip = max(dip, pulse(fr(t), fr(d_), fr(d_) + 1, fr(d_) + 4, 1.0, "lin", "sine"))
    p = dict(yaw=sx * 0.5, expr=expr, pitch=0.2 - 0.6 * a, gaze=(0.6 * sx, -0.4), legs="stand", arm_r="down", arm_l="down")
    p["arm_" + near] = dict(hand=lerp((sx * 0.20, 0.62), (sx * 0.72, 0.44 + 0.04 * dip), a), bend=-0.4, shape="open", layer="top")
    return p


def beach_shrug(t, t0=0.0, facing=1, cast="beach_man", expr="unimpressed", hold=0.5):
    """shrug: shoulders up (head sinks 0.06 D), both open hands out, head tilts 12 deg, over 6 frames (back_out);
    held `hold` s, settles over 8 frames.  'unimpressed' face."""
    sx = 1 if facing >= 0 else -1
    a = go((t - t0) / 0.30) if t >= t0 else 0.0
    d = ease((t - t0 - 0.2 - hold) / 0.27, "sine") if t >= t0 + 0.2 + hold else 0.0
    s = a * (1 - d)
    return dict(yaw=sx * 0.35, expr=expr, head_dy=0.06 * s, head_roll=sx * 12.0 * s, pitch=0.1,
                squash=(1 + 0.015 * s, 1 - 0.01 * s), legs="stand",
                arm_r=dict(preset="shrug", hand=lerp((0.20, 0.62), (0.62, 0.40), s), bend=0.6, shape="open" if s > 0.4 else "ball"),
                arm_l=dict(preset="shrug", hand=lerp((-0.20, 0.62), (-0.62, 0.40), s), bend=0.6, shape="open" if s > 0.4 else "ball"))


def beach_shade(t, t0=0.0, facing=-1, cast="beach_man", stunned_at=None, expr="neutral"):
    """shot 23: shades his eyes looking out to sea (near-profile toward `facing`, pitch -0.2, hand 'shade'), leaning
    forward a little; stunned_at: face swaps to 'stunned' behind a blink (closed frame at that time)."""
    sx = 1 if facing >= 0 else -1
    a = go((t - t0) / 0.3) if t >= t0 else 0.0
    f = fr(t)
    st = stunned_at is not None and f >= fr(stunned_at)
    p = dict(yaw=sx * 0.7, expr="stunned" if st else expr, pitch=-0.2 * a, lean=sx * 4.0 * a, legs="stand", arm_r="down", arm_l="down",
             blink=blink(f, [fr(stunned_at) - 1]) if stunned_at is not None else 0, head_dy=0.005 * math.sin(t * 2))
    near = "r" if sx > 0 else "l"
    p["arm_" + near] = arm_blend(cast, "down", "shade", a)
    return p


def beach_hold_hat(t, cast="beach_woman", facing=1, gust_at=None, expr="worried"):
    """holding the hat brim down (shot 23 woman; beach_man too): near hand on the brim ('shade'-like, top layer),
    profile; a gust at gust_at lifts the brim 6 deg for 6 frames and the hand presses it back."""
    sx = 1 if facing >= 0 else -1
    g = pulse(fr(t), fr(gust_at), fr(gust_at) + 3, fr(gust_at) + 9, 1.0) if gust_at is not None else 0.0
    far = "l" if sx > 0 else "r"
    p = dict(yaw=sx * 0.85, expr=expr, legs="stand", arm_r="down", arm_l="down", hat_rot=-sx * 6.0 * g, hat_dy=-0.02 * g,
             head_roll=-sx * 3.0 * g, pitch=0.1)
    p["arm_" + far] = dict(hand=(-sx * 0.50, -0.40 - 0.03 * g), bend=-0.8, layer="top", shape="open", stretch=1.2)
    return p


def beach_shocked(t, t_shock=0.1, cast="beach_man", facing=-1, hat_pop=True, focus=True, before="worried"):
    """shot 24: shocked (ring eyes, O mouth, sweat) behind a blink at t_shock; 2-frame squash; 3 frames of focus lines;
    beach_man's boater pops off: lifts 0.45 D and spins 25 deg over 3 frames, then is gone (hat_off) -- hand the
    flight to a flying-hat card (flying_hat_svg) from t_shock + 0.1."""
    sx = 1 if facing >= 0 else -1
    f, fs = fr(t), fr(t_shock)
    on = f >= fs
    sq = pulse(f, fs - 1, fs, fs + 2, 1.0, "lin", "lin")
    rec = ease((f - fs) / 5.0, "back_out") if on else 0.0
    p = dict(yaw=sx * 0.55, expr="shocked" if on else before, blink=blink(f, [fs - 1]), squash=(1 + 0.03 * sq, 1 - 0.03 * sq),
             head_dy=-0.05 * rec, lean=-sx * 5.0 * rec, pitch=-0.2 * rec, legs=dict(preset="wide", crouch=0.04 * rec),
             fx=(["sweat"] if on else []) + ([dict(type="focus_lines", seed=f)] if (focus and fs <= f < fs + 3) else []),
             arm_r=dict(preset="raised", hand=(0.35 + 0.15 * rec, 0.55 - 0.85 * rec), bend=-0.8, shape="open") if on else "down",
             arm_l=dict(preset="raised", hand=(-0.35 - 0.15 * rec, 0.55 - 0.85 * rec), bend=-0.8, shape="open") if on else "down")
    if hat_pop and cast == "beach_man" and on:
        u = clamp((f - fs) / 3.0)
        if f - fs >= 3:
            p["hat_off"] = True
        else:
            p["hat_dy"] = -0.45 * ease(u, "cubic_out")
            p["hat_rot"] = 25.0 * u * (-sx)
    return p


def run_cycle(t, cast="beach_man", facing=1, speed=3.2, step=0.34, expr="shocked", lean=14.0):
    """run: the walk at double rate (one step every 0.34 s), lean forward `lean` deg, arms pumping, longer strides,
    a short flight phase (pose['_lift'] up to 0.10 D at mid-step), knees high.  The root must travel pose['_adv']."""
    p = boss_walk(t, speed=speed, facing=facing, step=step, bob=0.30, sway=0.05, yaw=0.85, arms="swing", expr=expr, cast=cast)
    sx = 1 if facing >= 0 else -1
    ph = t / step
    sw = math.sin(math.pi * ph)
    u = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
    p["lean"] = sx * lean
    p["head_dx"] = sx * 0.06
    p["pitch"] = -0.2
    near, far = ("r", "l") if sx > 0 else ("l", "r")
    p["arm_" + near] = dict(hand=(sx * (0.15 + 0.42 * sw), 0.42 - 0.18 * sw), bend=0.8, sharp=0.6, layer="front")
    p["arm_" + far] = dict(hand=(sx * (0.15 - 0.42 * sw), 0.42 + 0.18 * sw), bend=0.8, sharp=0.6, layer="back")
    p["fx"] = ["sweat"]
    p["_lift"] = p.get("_lift", 0.0) + 0.06 * u
    return p


def jump_run(t, t_jump=0.0, cast="beach_man", facing=1, height=0.55, run_speed=3.2, hat_off=None):
    """shot 24 jump scare then run (LOOK_SPEC 5.5.9): from t_jump: squash 2 frames (crouch, squash 1.10 x 0.86),
    leap 2 (stretch 0.90 x 1.14, rising), hang 2 (pose['_lift'] = height D, arms up, knees tucked, shocked),
    land 2 (squash), then turn to `facing` and run_cycle (pose['_adv'] from the start of the run).
    hat_off: True removes the hat (beach_man after the pop); default: beach_man has none, others keep theirs."""
    f, fj = fr(t), fr(t_jump)
    sx = 1 if facing >= 0 else -1
    k = f - fj
    if hat_off is None:
        hat_off = cast == "beach_man"
    base = dict(expr="shocked", fx=["sweat"], hat_off=hat_off)
    if k < 0:
        p = dict(base, yaw=sx * 0.5, legs="stand", arm_r="down", arm_l="down")
        p["_lift"] = 0.0
        return p
    if k < 8:
        tbl = {  # frame: (squash x, squash y, crouch, lift fraction, arms up)
            0: (1.06, 0.92, 0.18, 0.0, 0.2), 1: (1.10, 0.86, 0.26, 0.0, 0.3),
            2: (0.94, 1.08, 0.0, 0.45, 0.9), 3: (0.90, 1.14, 0.0, 0.85, 1.0),
            4: (0.98, 1.03, 0.10, 1.0, 1.0), 5: (1.0, 1.0, 0.12, 0.97, 0.95),
            6: (1.04, 0.95, 0.05, 0.45, 0.6), 7: (1.10, 0.87, 0.24, 0.0, 0.4)}
        sxq, syq, cr, lf, au = tbl[k]
        tuck = 1.0 if k in (4, 5) else 0.0
        p = dict(base, yaw=sx * 0.5, squash=(sxq, syq), legs=dict(preset="stand", crouch=cr, lift_r=0.6 * tuck, lift_l=0.4 * tuck),
                 arm_r=dict(preset="raised", hand=(0.35 + 0.1 * au, 0.55 - 1.05 * au), bend=-0.8, shape="open"),
                 arm_l=dict(preset="raised", hand=(-0.35 - 0.1 * au, 0.55 - 1.05 * au), bend=-0.8, shape="open"),
                 head_roll=sx * 6.0 * au)
        p["_lift"] = height * lf
        p["_adv"] = 0.0
        return p
    tr = (k - 8) / float(FPS)
    p = run_cycle(tr, cast=cast, facing=facing, speed=run_speed)
    p.update(hat_off=hat_off)
    # first 4 frames of the run blend in from the landing crouch
    if k - 8 < 4:
        w = (k - 8 + 1) / 5.0
        p["legs"] = dict(p["legs"], crouch=lerp(0.20, p["legs"]["crouch"], w))
    return p


def woman_peg_towel(t, peg_at=0.6, facing=1):
    """shot 8 (far, profile): beach_woman reaches up to the line with both hands, pegs the towel at peg_at (a small
    push up and a 2-frame squash), lowers the arms after."""
    sx = 1 if facing >= 0 else -1
    a = ease(t / 0.4, "sine")
    d = ease((t - peg_at - 0.2) / 0.4, "sine") if t >= peg_at + 0.2 else 0.0
    push = pulse(fr(t), fr(peg_at) - 2, fr(peg_at), fr(peg_at) + 4, 1.0)
    u = a * (1 - d)
    return dict(yaw=sx * 0.9, expr="happy", pitch=-0.5 * u, legs="stand", squash=(1 + 0.015 * push, 1 - 0.015 * push),
                arm_r=dict(hand=lerp((sx * 0.15, 0.58), (sx * 0.78, -0.30 - 0.05 * push), u), bend=-0.6 * u + 0.4 * (1 - u), stretch=1.25, layer="front", shape="open" if u > 0.5 else "ball"),
                arm_l=dict(hand=lerp((sx * 0.05, 0.60), (sx * 0.70, -0.24 - 0.05 * push), u), bend=-0.6 * u + 0.4 * (1 - u), stretch=1.25, layer="front"))


def woman_hand_out(t, facing=1):
    """shot 16 far: beach_woman on the porch, one palm held out for rain (held), eyes up, blink at 0.9 s."""
    sx = 1 if facing >= 0 else -1
    near = "r" if sx > 0 else "l"
    p = dict(yaw=sx * 0.7, expr="worried", pitch=-0.5, legs="stand", arm_r="down", arm_l="down", blink=blinks(t, (0.9,)),
             head_dy=0.004 * math.sin(t * 2.0))
    p["arm_" + near] = dict(hand=(sx * 0.66, 0.42), bend=-0.4, shape="open", layer="top")
    return p


# ============================================================================= hand sprites (close inserts)
def hand_canvas(cast, pose, side="r", margin=0.12):
    """a tight sprite canvas (feet-relative, for sprites.render_sprites 'canvas') around the forearm, hand and held
    prop of `side` only: the hi-res hand sprite of the inserts (shots 5, 7, 9, 11, 13) at 512 px per D.  The canvas
    starts at the elbow, so the torso stays out of it when the hand is 0.5 D or more from the body; give the arm a
    sideways or raised target."""
    f = P.figure(cast, pose, "hc")
    a = f["anchors"]
    fx, fy = a["feet"][0], f["feet_y"]
    pts = [a["elbow_" + side], a["hand_" + side], a["prop_tip_" + side]]
    x0 = min(p[0] for p in pts) - margin
    x1 = max(p[0] for p in pts) + margin
    y0 = min(p[1] for p in pts) - margin
    y1 = max(p[1] for p in pts) + margin
    g = 1 / 16.0
    return (math.floor((x0 - fx) / g) * g, math.floor((y0 - fy) / g) * g, math.ceil((x1 - fx) / g) * g, math.ceil((y1 - fy) / g) * g)


# ============================================================================= catalogue (for the strips and tests)
def _loud_q1():
    return loudness(21.07, 23.13)


CATALOGUE = None


def catalogue():
    """name -> (cast, function of t, duration s).  The demo parameters the strips and tests use."""
    global CATALOGUE
    if CATALOGUE is not None:
        return CATALOGUE
    q1 = _loud_q1()
    C = {
        "boss_talk": ("boss", lambda t: boss_talk(t, q1, base=dict(yaw=-0.45, arm_r="hip", arm_l="down")), 2.06),
        "boss_talk_wag": ("boss", lambda t: boss_talk(t, q1, base=lambda s: boss_finger_wag(s, 0.9, 0.4)), 2.06),
        "boss_talk_lean_wink": ("boss", lambda t: boss_talk(t, q1, base=lambda s: boss_lean_wink(s, 0.3, 1.0, 0.15)), 1.6),
        "boss_walk": ("boss", lambda t: boss_walk(t, pointer=False, arms="swing"), 1.36),
        "boss_whistle_stroll": ("boss", lambda t: boss_whistle_stroll(t), 1.36),
        "boss_laugh_doubled": ("boss", lambda t: boss_laugh_doubled(t, 0.1, pull_strip_at=1.1), 1.6),
        "boss_shocked": ("boss", lambda t: boss_shocked(t, 0.2, drop_pointer_at=0.4), 0.8),
        "boss_mock_search": ("boss", lambda t: boss_mock_search(t, 0.05), 1.0),
        "boss_pointer_whack": ("boss", lambda t: boss_pointer_whack(t, 0.5), 0.8),
        "boss_thumb_jerk": ("boss", lambda t: boss_thumb_jerk(t, 0.1), 1.0),
        "boss_eraser_bounce": ("boss", lambda t: boss_eraser_bounce(t), 1.25),
        "boss_rub_furious": ("boss", lambda t: boss_rub_furious(t, 0.0), 1.0),
        "boss_frozen_purple": ("boss", lambda t: boss_frozen_purple(t), 0.8),
        "boss_pant": ("boss", lambda t: boss_pant(t), 0.9),
        "boss_stamp_thrust": ("boss", lambda t: boss_stamp_thrust(t, 0.15, 0.3, 0.45), 1.0),
        "boss_read_tape": ("boss", lambda t: boss_read_tape(t, 0.4), 0.8),
        "hero_slumped": ("hero", lambda t: hero_slumped(t, blinks_at=(0.5,)), 1.2),
        "hero_sad_listener": ("hero", lambda t: hero_sad_listener(t, blinks_at=(0.2,), shut=(0.6, 0.13), sweat_at=0.3), 1.0),
        "hero_listener": ("hero", lambda t: hero_listener(t, blinks_at=(0.2, 0.8), gaze_shift=(0.55, (0.9, -0.1), (-0.4, 0.1))), 1.1),
        "hero_stunned": ("hero", lambda t: hero_stunned(t, 0.1, 0.5), 1.0),
        "hero_redraw": ("hero", lambda t: hero_redraw(t, 0.12), 0.6),
        "hero_ruler_rest": ("hero", lambda t: hero_ruler_rest(t, blinks_at=(0.3,)), 0.8),
        "hero_study": ("hero", lambda t: hero_study(t, blinks_at=(0.3,)), 0.8),
        "senior_a_nod": ("senior_a", lambda t: senior_nod(t, (0.1, 0.5), "senior_a", 0.4), 0.9),
        "senior_b_nod": ("senior_b", lambda t: senior_nod(t, (0.1, 0.5), "senior_b", -0.4, expr="smug"), 0.9),
        "senior_a_laugh": ("senior_a", lambda t: senior_laugh(t, "senior_a", 0.45, 0.0, thumb_at=0.4), 0.8),
        "senior_b_laugh": ("senior_b", lambda t: senior_laugh(t, "senior_b", -0.45, 0.5), 0.8),
        "beach_sleep": ("beach_man", lambda t: beach_sleep(t), 1.3),
        "beach_stretch": ("beach_man", lambda t: beach_stretch(t, 0.05), 1.4),
        "beach_palm_out": ("beach_man", lambda t: beach_palm_out(t, 0.0, (0.35, 0.5, 0.65)), 0.9),
        "beach_shrug": ("beach_man", lambda t: beach_shrug(t, 0.1), 1.0),
        "beach_shade": ("beach_man", lambda t: beach_shade(t, 0.05, stunned_at=0.6), 1.0),
        "man_hold_hat": ("beach_man", lambda t: beach_hold_hat(t, "beach_man", -1, gust_at=0.3), 0.8),
        "woman_hold_hat": ("beach_woman", lambda t: beach_hold_hat(t, "beach_woman", 1, gust_at=0.3), 0.8),
        "man_shocked": ("beach_man", lambda t: beach_shocked(t, 0.1, "beach_man"), 0.5),
        "woman_shocked": ("beach_woman", lambda t: beach_shocked(t, 0.1, "beach_woman", 1), 0.5),
        "man_jump_run": ("beach_man", lambda t: jump_run(t, 0.0, "beach_man", 1), 0.95),
        "woman_jump_run": ("beach_woman", lambda t: jump_run(t, 0.0, "beach_woman", 1), 0.95),
        "man_run": ("beach_man", lambda t: run_cycle(t, "beach_man"), 0.68),
        "woman_peg_towel": ("beach_woman", lambda t: woman_peg_towel(t, 0.6), 1.2),
        "woman_hand_out": ("beach_woman", lambda t: woman_hand_out(t), 1.0),
    }
    CATALOGUE = C
    return C
