#!/usr/bin/env python3
"""c17.py -- helpers for film-17 take s03 (copy of the film8/common.py idea, switched to cast17 + set3d17/bertillon.py).
One location per process ('records').  Blender frame bf(g) = g - FIRST_G + 1."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast17                                    # noqa: E402  (before sprites)
import bpy                                       # noqa: E402
from mathutils import Vector                     # noqa: E402
import bertillon as K                            # noqa: E402
import actors, camrig, sprites                   # noqa: E402

def g_of(t):
    return int(round((t + 0.10) * 30))

def lerp(a, b, u):
    return a + (b - a) * u

def blink(g, period=96, off=0):
    return cast17.blink_at(g, period, off)

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out

def make_cast(mark_A, story, opts, cam, sprite_dir, ppd=256):
    """actor for the stand point; returns (actor, cast, base pose, scale, feet position)."""
    x, y, z, fz, who = mark_A
    cast, pose = cast17.STORY17[story]; pose = dict(pose)
    if opts.get("expr"):
        pose = cast17.with_expr(pose, opts["expr"])
    pose["seat17"] = None
    if opts.get("mirror"):
        pose["mirror"] = True
    rim = opts.get("rim", K.RIM_FOR.get(cast))
    if rim:
        pose["rim"] = rim; pose["rim_opacity"] = 0.55; pose["rim_w"] = 0.02
    a = actors.Actor("c_%s_%s" % (story, int(x * 100)), cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True)
    a.head_flip = True
    sc = opts.get("H", K.CAST_H[cast]) / K.CAST_HD[cast]
    pos = (x + opts.get("dx", 0.0), y + opts.get("dy", 0.0), z + opts.get("dz", 0.0))
    return a, cast, pose, sc, pos

def render_frame(path, scale=1.0, samples=24, threads=2):
    """K.render without its thread / sample override; sync the cards, render, grade."""
    sc = bpy.context.scene
    K.setup_render(sc, "draft" if scale < 1 else "final", samples)
    sc.render.threads = threads
    sc.render.filepath = path
    t = time.time()
    actors.sync_all(sc, sc.camera)
    bpy.ops.render.render(write_still=True)
    K.grade(path)
    return time.time() - t
