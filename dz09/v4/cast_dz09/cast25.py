"""cast25.py -- registers the DEAD ZONE 09 cast in the v2 puppet module (extension pattern of v3/cast/cast_ext.py).

v2/puppet/puppet.py and v3/cast/cast_ext.py are NOT edited.  On import this module
  * adds kong, kong_wet, crew, crew_wet, driver, namnuea to puppet.CAST (entries marked "draw25d": True),
  * wraps puppet.figure so that these names are drawn by draw25d (flat composite of all layers, same return keys:
    svg, feet_y, bbox, anchors), every other name falls through to the original,
  * adds feet-relative canvases for them to v3 stage sprites.DEFAULT_CANVAS when that module is (or gets) imported,
  * adds STORY poses for the EP.1 hook (puppet.STORY["dz_*"]).

So v3 stage code (`Actor(name, "kong")`, `sprites.render_sprites`) can already put Kong on ONE card (2D-flat);
stage25.Actor25 puts him on the layered 2.5D stack.

    import cast25, puppet
    f = puppet.figure("kong", {"yaw": 0.5, "expr": "alarmed", "arm_l": "hold", "prop_l": {"type": "cutter", "bars": 2}})
    L = cast25.layers("kong", pose)        # the layered form (draw25d.build)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draw25d
import puppet

NAMES = tuple(draw25d.CAST25.keys())
CANVAS = {n: (-2.0, -4.5, 2.0, 0.125) for n in NAMES}          # feet-relative, D (stage sprites convention)

STORY = {
    "dz_kong_cutter": ("kong", {"expr": "determined", "yaw": 0.4, "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 96, "bars": 3}}),
    "dz_kong_phone": ("kong", {"expr": "tired", "yaw": -0.4, "arm_r": "phone_look", "prop_r": {"type": "phone"},
                               "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 96, "bars": 3}}),
    "dz_kong_call": ("kong", {"expr": "guilty", "yaw": 0.5, "arm_l": "phone_ear", "prop_l": "phone", "head_roll": -6}),
    "dz_crew_shout": ("crew", {"expr": "shouting", "yaw": -0.5, "arm_l": "wave", "arm_r": "point", "mouth": "shout"}),
    "dz_driver_still": ("driver", {"expr": "still", "yaw": 0.5, "legs": "seated", "lean": 22, "head_dy": 0.18,
                                   "head_roll": 18, "arm_r": "lap", "arm_l": "lap"}),
    "dz_driver_lift": ("driver", {"expr": "head_lift", "yaw": 0.4, "legs": "seated", "lean": 8, "arm_r": "wheel", "arm_l": "lap"}),
    "dz_infected_lunge": ("driver", {"expr": "lunge", "yaw": -0.5, "legs": "lunge", "lean": -22, "arm_r": "claw", "arm_l": "reach"}),
    "dz_kong_shout": ("kong", {"expr": "shouting", "yaw": 0.5, "arm_r": "raise", "prop_r": {"type": "crowbar", "angle": -60},
                               "arm_l": "push", "legs": "step"}),
    "dz_namnuea_photo": ("namnuea", {"expr": "smile", "arm_r": "wave"}),
}

_orig_figure = puppet.figure


def layers(name, pose=None):
    return draw25d.build(name, pose)


def figure(cast_name, pose=None, uid="p"):
    if cast_name in NAMES:
        P = dict(pose or {})
        P.setdefault("uid", uid)
        f = draw25d.build(cast_name, P)
        svg = '<g id="%s_fig">%s</g>' % (uid, draw25d.flat_svg(f))
        return {"svg": svg, "feet_y": f["feet_y"], "bbox": f["bbox"], "anchors": dict(f["anchors"]), "layers": f["layers"]}
    return _orig_figure(cast_name, pose, uid)


def register_stage(mod):
    try:
        for n, c in CANVAS.items():
            mod.DEFAULT_CANVAS.setdefault(n, c)
    except AttributeError:
        pass


if not getattr(puppet, "_dz25_registered", False):
    for n in NAMES:
        puppet.CAST.setdefault(n, {"draw25d": True, "label": draw25d.CAST25[n]["label"]})
    puppet.figure = figure
    puppet.STORY.update(STORY)
    puppet._dz25_registered = True
    for mn in ("sprites", "stage.sprites"):
        if mn in sys.modules:
            register_stage(sys.modules[mn])

if __name__ == "__main__":
    for k, (n, p) in STORY.items():
        f = puppet.figure(n, p, k)
        print(k, n, "layers", len(f["layers"]), "feet_y %.2f" % f["feet_y"], "svg %d chars" % len(f["svg"]))
    print("hero still drawn by v2:", "hero_fig" in puppet.figure("hero", {}, "hero")["svg"])
