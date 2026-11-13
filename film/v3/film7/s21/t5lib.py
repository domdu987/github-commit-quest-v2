#!/usr/bin/env python3
"""t5lib.py -- small runtime helpers shared by takes s21, s23, s25 (render team 5).  Import AFTER film7/common.py.

  variants()            registers crowd colour variants of cast7 members at runtime (lady_b/c/d, gentleman_b/c) in puppet.CAST and
                        sprites.DEFAULT_CANVAS -- nothing in v3/cast7 is edited; the copies only change costume colours, so a queue
                        or a street is not a row of clones.
  hat_doff_patch()      pose key "hat_off": True draws the gentleman's derby off his head (the hat style function returns nothing
                        while that figure is drawn); the hat then travels in his hand as an overlay (hat_overlay).
  hat_overlay(...)      the derby as an SVG fragment in puppet-local D units at a point, rotated (for Actor.render_sprites overlay=).
  sway(g, seed)         small deterministic idle motion numbers (head roll / lean / gaze drift) so a crowd never stands still.
"""
import copy, math
import common as C

P = C.cast7.P
CE = C.cast7.CE
sprites = C.sprites

_DONE = {}


def _variant(base, name, colors=None, sleeve=None, hat_colors=None, **top):
    c = copy.deepcopy(P.CAST[base])
    if colors:
        c["colors"].update(colors)
    if sleeve:
        c["sleeve"].update(sleeve)
    if hat_colors:
        c["hat_colors"].update(hat_colors)
    c.update(top)
    P.CAST[name] = c
    sprites.DEFAULT_CANVAS[name] = sprites.DEFAULT_CANVAS[base]
    try:
        CE.CANVAS[name] = CE.CANVAS[base]
    except Exception:
        pass


def variants():
    if _DONE.get("v"):
        return
    _DONE["v"] = True
    # ladies: teal, mustard, navy (hat ribbons / roses changed with them)
    _variant("lady", "lady_b", colors=dict(jacket="#2e6a66", skirt="#2a5c5c", skirt_d="#183c3c", trim="#e8d8a8", pants="#2a5c5c"),
             sleeve=dict(color="#2e6a66", dark="#1c4442"), hat_colors=dict(ribbon="#2e6a66", rose="#f0c060", rose2="#f8e0a0"), hat_side=-1)
    _variant("lady", "lady_c", colors=dict(jacket="#a8742a", skirt="#8a5c22", skirt_d="#5a3a14", trim="#f4e4c0", pants="#8a5c22"),
             sleeve=dict(color="#a8742a", dark="#70481a"), hat_colors=dict(ribbon="#3a5a8a", rose="#e86a5a", plume="#fbf4e8"))
    _variant("lady", "lady_d", colors=dict(jacket="#2c3a6c", skirt="#26325e", skirt_d="#161e3c", trim="#d8c8f0", pants="#26325e"),
             sleeve=dict(color="#2c3a6c", dark="#1a2446"), hat_colors=dict(ribbon="#b03a3a", rose="#f4f0f0", rose2="#e0a0a0"), hat_side=-1)
    # gentlemen: brown coat + brown derby, bottle-green coat + grey derby
    _variant("gentleman", "gentleman_b", colors=dict(base="#6e4e36", dark="#4a3222", lapel="#5e4230", vest="#c8b080", tie="#7a2a2a",
                                                     tie_dark="#4a1a1a", pants="#5a5048", moustache="#2a2020"),
             sleeve=dict(color="#6e4e36", dark="#4a3222"),
             hat_colors=dict(light="#8a6a4a", base="#5a3e28", dark="#36241a", shine="#b0906a", band="#24180e", brim="#4a3220", edge="#8a6e50"),
             hair=dict(color="#2a2020", front=0.07, grow=0.20))
    _variant("gentleman", "gentleman_c", colors=dict(base="#3e5a4c", dark="#26382e", lapel="#344c40", vest="#d8c8a0", tie="#6a3a7a",
                                                     tie_dark="#40224a", pants="#4a4a52", moustache="#a8a4a0"),
             sleeve=dict(color="#3e5a4c", dark="#26382e"),
             hat_colors=dict(light="#9a98a0", base="#6a6872", dark="#3e3c44", shine="#c8c6d0", band="#24222a", brim="#5a5862", edge="#a8a6b0"),
             hair=dict(color="#a8a4a0", front=0.07, grow=0.20), age_lines=True)


# ----------------------------------------------------------------------------- the bowler comes off
_HAT = {"off": False}


def hat_doff_patch():
    if _DONE.get("hat"):
        return
    _DONE["hat"] = True
    orig_fig = P.figure
    orig_derby = CE.HATS["derby"]

    def figure(cast_name, pose=None, uid="p"):
        _HAT["off"] = bool(isinstance(pose, dict) and pose.get("hat_off"))
        try:
            return orig_fig(cast_name, pose, uid)
        finally:
            _HAT["off"] = False

    def derby(k, Cd, yaw):
        if _HAT["off"]:
            return "", (0.0, -0.484)
        return orig_derby(k, Cd, yaw)

    P.figure = figure
    CE.HATS["derby"] = derby


def hat_overlay(cast, at, rot=0.0, yaw=0.0, scale=1.0, uid="hov"):
    """the cast's derby drawn standalone: its head-centre origin put at `at` (puppet-local D), rotated `rot` deg."""
    k = P._Ctx(uid, P.INK, None)
    s, _ = CE.HATS["derby"](k, P.CAST[cast], yaw)
    return '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)"><defs>%s</defs>%s</g>' % (
        at[0], at[1], rot, scale, "".join(k.defs), s)


# ----------------------------------------------------------------------------- idle motion
def sway(g, seed, amp=1.0):
    """(head_roll deg, lean deg, gaze dx, gaze dy) small smooth idle numbers."""
    a = g * 0.11 + seed * 1.7
    b = g * 0.07 + seed * 2.9
    return (amp * (3.0 * math.sin(a) + 1.2 * math.sin(2.3 * a + 0.5)),
            amp * (1.6 * math.sin(b)),
            0.12 * math.sin(0.5 * a + seed),
            0.08 * math.sin(0.43 * b + 2 * seed))


def blinks(g, seed, period=70):
    """blink amount: one blink every ~period frames, offset by seed."""
    off = int(seed * 37) % period
    ph = (g + off) % period
    return C.blink(ph, [period // 2])
