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
    """film-21 colour rule: ALL English are crimson and gold (blue = Scots).  knight_b_crim_mtd: the second rider in a crimson surcoat / red great helm on a GOLD caparison;
    knight_b_crim_bare_mtd: the same with NO helmet (bare head) for after the pop; helmet_air: a lone bascinet with a crimson plume."""
    base = P.CAST["knight_b_great"]
    crim = dict(base)
    crim.update(hat_colors=dict(cast21.GREAT_RED), colors=dict(base["colors"], base=cast21.ENGLISH_RED, alt="#e8b52e", trim="#e8b52e"))
    bare = dict(crim)
    bare.update(hat_style="bare7", hat_colors={"light": "#8a6038", "base": "#6a4a2a", "dark": "#4a3220"}, hair=dict(color="#6a4a2a", front=0.08, grow=0.2))
    P.CAST["knight_b_crim"] = crim; P.CAST["knight_b_crim_bare"] = bare
    cv = cast21.CANVAS_SPECIAL21["knight_b_great_mtd"] if "knight_b_great_mtd" in cast21.CANVAS_SPECIAL21 else MTD_CANVAS
    for nm in ("knight_b_crim", "knight_b_crim_bare"):
        cast21.MOUNTED[nm + "_mtd"] = nm
        cast21.DEFAULT_CAP[nm] = "gold"
        P.CAST[nm + "_mtd"] = dict(P.CAST["knight_a_mtd"])
        cast21.CANVAS_SPECIAL21[nm + "_mtd"] = cv
        sprites.DEFAULT_CANVAS[nm + "_mtd"] = cv
    prev = P.figure

    def figure2(name, pose=None, uid="p"):
        if name == "helmet_air":
            pd = pose if isinstance(pose, dict) else {}
            k = cast21._ctx(uid, P.INK, None)
            steel = dict(light="#f4f6fa", base="#b4bcc8", dark="#6a7482", shine="#ffffff", plume="#c8282c")
            C = dict(hat_colors=steel, hat_tilt=0.0)
            hat, top = cast21._hat_bascinet21(k, C, 0.0)
            svg = "<defs>%s</defs><g transform=\"rotate(%.2f 0 -0.59)\"><g transform=\"translate(0 -0.05)\">%s</g></g>" % ("".join(k.defs), float(pd.get("tilt", 0.0)), hat)
            an = dict(feet=(0.0, 0.0), hip=(0.0, -0.2), head=(0.0, -0.4), head_top=(0.0, -0.8), hat_top=(0.0, -0.8), mouth=(0.0, -0.3))
            return dict(svg=svg, feet_y=0.0, bbox=(-1.2, -1.4, 1.2, 0.4), anchors=an)
        return prev(name, pose, uid)
    P.figure = figure2
    P.CAST["helmet_air"] = dict(P.CAST["helmet_float"])
    sprites.DEFAULT_CANVAS["helmet_air"] = (-1.625, -1.625, 1.625, 0.4375)


register_extras()
