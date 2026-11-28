"""epbase.py -- base of the EP.1 shot modules (3D shots).  `from epbase import *` gives everything the hook's
shots/base.py gives (driver_seated, kong_cutter, crew_pry, kong_phone, rescue_lamp, once, hand_cam, attack, Z, DM0 ...
plus C, Vector, clamp, smooth, lerp, ramp, ease_out, ease_in, facing, WARM, COOL) and the scene-timing helpers below.

Shot contract (the hook's, plus three optional names; the cut table fills what a module leaves out):
    ID      set by the loader from the file name (s025.py -> "S025")
    CLASS   "A" | "B" | "C2" | "C1"      render class (final tier: A 100 %, B 75 %, C2 75 % 4 spp; C1 = draw(), see ep2d.py)
    LOC     location key of stage_ep.LOCATIONS ("X1" = the hook's expressway)
    CAST    extra actor keys of stage_ep.CAST to build for this shot
    setup(F)  frame(F, g, t, u) -> post options   late(F, g, t, u)   PPD / PCT / SPP dicts as in the hook
g is the stage frame (scene g_base + scene-local frame), t = g / 24, u = 0..1 through the shot.
"""
import epcommon as E                                       # first: puts v10/film on sys.path
import bpy                                                 # before mathutils (shots.base needs it)
from shots.base import *                                   # v10/film/shots/base.py, unchanged


def W(text, end=False, sid=None, n=0):
    """stage time (the same clock as a shot's t) at which a caption starts / ends: cues are written against words."""
    return E.scene().word(text, end, sid, n)


def CUE(name):
    return E.scene().cue(name)


def T0(F):
    """stage time of the shot's first frame."""
    return E.scene().range(F.shot.ID)[0] / float(C.FPS)


def speaker(g):
    return E.scene().speaker(g)


def talk(actor, g, shape=None):
    """pose keywords for lip sync: {'mouth': level} while the line being spoken at g is this actor's, else {}.
        F.kong.set(..., **talk("kong", g))            talk("crew", g, "o") for the round mouth"""
    name = actor if isinstance(actor, str) else actor.name
    m = E.scene().mouth(name, g)
    if m <= 0:
        return {}
    return {"mouth": (shape, m) if shape else m}
