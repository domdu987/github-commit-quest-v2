"""c17.py -- helpers for the film-17 take s09 (copy of the film8/common.py ideas on cast17 + set3d17/bertillon.py)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17"), os.path.join(V3, "..", "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast17                                    # noqa: E402  (before sprites)
import bpy                                       # noqa: E402
from mathutils import Vector                     # noqa: E402
import bertillon as K                            # noqa: E402
import actors, camrig, render, sprites           # noqa: E402
from anim import ease, blink, lerp, clamp        # noqa: E402,F401


def g_of(t):
    return int(round((t + 0.10) * 30))


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def smooth(u):
    u = clamp(u); return u * u * (3 - 2 * u)


def make_actor(name, cast, sprite_dir):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True)
    a.head_flip = True
    return a


def story(name, expr=None, mirror=False, seat=False):
    cast, pose = cast17.STORY17[name]
    pose = dict(pose)
    if expr:
        pose = cast17.with_expr(pose, expr)
    pose["seat17"] = None
    if mirror:
        pose["mirror"] = True
    rim = K.RIM_FOR.get(cast)
    if rim:
        pose["rim"] = rim; pose["rim_opacity"] = 0.55; pose["rim_w"] = 0.02
    return cast, pose


def hide_keys(actor, f, hidden):
    for o in actor.objects():
        o.hide_render = bool(hidden)
        o.keyframe_insert("hide_render", frame=f)
