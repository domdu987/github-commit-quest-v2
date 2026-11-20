#!/usr/bin/env python3
"""c21.py -- helper for film 21 segment I (the AHA): paths, cast21 + stage + the Stirling set in ONE process, plus a few segment-local extras
(bare-headed knight variant, a flying-helmet card).  Nothing in set3d21 / cast21 / stage is edited."""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                            # noqa: E402  (BEFORE sprites / stage)
import puppet                                            # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import stirling as K                                     # noqa: E402
import actors, camrig, render, sprites                   # noqa: E402

P = puppet
MTD_CANVAS = cast21.CANVAS_SPECIAL21.get("knight_a_mtd") or (-3.0625, -5.4375, 3.0625, 0.25)


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def sm(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def u_of(g, a, b):
    return sm((g - a) / float(b - a)) if b != a else (1.0 if g >= a else 0.0)


# ------------------------------------------------------------------ segment-local cast extras
def register_extras():
    """knight_b_great_bare_mtd: the blue knight with NO helmet (bare head, brown hair), for after the pop; helmet_air: a lone great helm (no foam ring)."""
    base = P.CAST["knight_b_great"]
    bare = dict(base)
    bare.update(hat_style="bare7", hat_colors={"light": "#8a6038", "base": "#6a4a2a", "dark": "#4a3220"},
                hair=dict(color="#6a4a2a", front=0.08, grow=0.2))
    P.CAST["knight_b_great_bare"] = bare
    cast21.MOUNTED["knight_b_great_bare_mtd"] = "knight_b_great_bare"
    cast21.DEFAULT_CAP["knight_b_great_bare"] = "blue"
    P.CAST["knight_b_great_bare_mtd"] = dict(P.CAST["knight_a_mtd"])
    cv = cast21.CANVAS_SPECIAL21["knight_b_great_mtd"] if "knight_b_great_mtd" in cast21.CANVAS_SPECIAL21 else MTD_CANVAS
    cast21.CANVAS_SPECIAL21["knight_b_great_bare_mtd"] = cv
    sprites.DEFAULT_CANVAS["knight_b_great_bare_mtd"] = cv
    # lone helmet (great helm, blue plume), tilted, no water
    prev = P.figure

    def figure2(name, pose=None, uid="p"):
        if name == "helmet_air":
            pd = pose if isinstance(pose, dict) else {}
            ink = P.INK
            k = cast21._ctx(uid, ink, None)
            C = dict(hat_colors=cast21.GREAT_BLUE if hasattr(cast21, "GREAT_BLUE") else cast21.GREAT, hat_tilt=float(pd.get("tilt", 0.0)))
            hat, top = cast21._hat_greathelm21(k, C, 0.0)
            svg = "<defs>%s</defs><g transform=\"translate(0 0.55)\">%s</g>" % ("".join(k.defs), hat)
            an = dict(feet=(0.0, 0.0), hip=(0.0, -0.2), head=(0.0, -0.4), head_top=(0.0, -0.8), hat_top=(0.0, -0.8), mouth=(0.0, -0.3))
            return dict(svg=svg, feet_y=0.0, bbox=(-1.2, -1.4, 1.2, 0.4), anchors=an)
        return prev(name, pose, uid)
    P.figure = figure2
    P.CAST["helmet_air"] = dict(P.CAST["helmet_float"])
    sprites.DEFAULT_CANVAS["helmet_air"] = (-1.625, -1.625, 1.625, 0.4375)


register_extras()
