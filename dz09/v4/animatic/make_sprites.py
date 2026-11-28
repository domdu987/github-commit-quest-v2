"""Render the cast poses needed by the animatic to PNGs in animatic/sprites (import-only use of cast_dz09 + v3 sprite page)."""
import os, sys, json
PROJ = "/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09"
sys.path.insert(0, PROJ + "/v2/puppet"); sys.path.insert(0, PROJ + "/v4/cast_dz09"); sys.path.insert(0, PROJ + "/v3/stage")
import draw25d, sprites
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
PPD = 200
CANVAS = (-2.0, -0.9, 2.0, 4.3)   # figure coords (head centre 0,0; y down)
POSES = {
 "kong_cutter":   ("kong_wet", {"expr": "determined", "yaw": 0.4, "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 96, "bars": 3}}),
 "kong_cutter_b": ("kong_wet", {"expr": "determined", "yaw": 0.4, "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 90, "bars": 3}, "blink": 1}),
 "kong_phone":    ("kong_wet", {"expr": "tired", "yaw": -0.4, "arm_r": "phone_look", "prop_r": {"type": "phone"}, "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 96, "bars": 3}}),
 "kong_call":     ("kong_wet", {"expr": "guilty", "yaw": 0.5, "arm_l": "phone_ear", "prop_l": "phone", "head_roll": -6, "arm_r": "hold", "prop_r": {"type": "cutter", "angle": 96, "bars": 3}}),
 "kong_call_talk":("kong_wet", {"expr": "talk", "yaw": 0.5, "arm_l": "phone_ear", "prop_l": "phone", "head_roll": -4, "arm_r": "hold", "prop_r": {"type": "cutter", "angle": 96, "bars": 3}}),
 "kong_tired":    ("kong_wet", {"expr": "tired", "yaw": 0.3, "arm_l": "phone_look", "prop_l": "phone", "head_roll": 8, "arm_r": "hold", "prop_r": {"type": "cutter", "angle": 96, "bars": 3}}),
 "kong_alarmed":  ("kong_wet", {"expr": "alarmed", "yaw": -0.5, "arm_r": "hold", "prop_r": {"type": "cutter", "angle": 96, "bars": 3}, "legs": "step"}),
 "kong_shout":    ("kong_wet", {"expr": "shouting", "yaw": -0.5, "arm_r": "raise", "prop_r": {"type": "crowbar", "angle": -60}, "arm_l": "push", "legs": "step"}),
 "crew_shout":    ("crew_wet", {"expr": "shouting", "yaw": -0.5, "arm_l": "wave", "arm_r": "point", "mouth": "shout"}),
 "crew_lean":     ("crew_wet", {"expr": "neutral", "yaw": 0.9, "lean": 25, "arm_r": "reach", "arm_l": "down", "legs": "step"}),
 "crew_alarmed":  ("crew_wet", {"expr": "alarmed", "yaw": 0.9, "lean": 10, "arm_r": "guard", "legs": "step"}),
 "crew_pain":     ("crew_wet", {"expr": "pain", "yaw": 0.9, "lean": -15, "arm_r": "guard", "arm_l": "push", "legs": "step"}),
 "driver_still":  ("driver", {"expr": "still", "yaw": 0.5, "legs": "seated", "lean": 22, "head_dy": 0.18, "head_roll": 18, "arm_r": "lap", "arm_l": "lap"}),
 "driver_lift":   ("driver", {"expr": "head_lift", "yaw": 0.4, "legs": "seated", "lean": 8, "arm_r": "wheel", "arm_l": "lap"}),
 "driver_lunge":  ("driver", {"expr": "lunge", "yaw": -0.5, "legs": "lunge", "lean": -22, "arm_r": "claw", "arm_l": "reach"}),
 "namnuea_sad":   ("namnuea", {"expr": "sad", "yaw": 0.0}),
 "namnuea_smile": ("namnuea", {"expr": "smile", "arm_r": "wave"}),
}
def main():
    os.makedirs(OUT, exist_ok=True)
    pg = sprites._Page()
    meta = {}
    for k, (cast, pose) in POSES.items():
        P = dict(pose); P["uid"] = k
        f = draw25d.build(cast, P)
        svg, W, H = draw25d.doc(draw25d.flat_svg(f), CANVAS, PPD)
        out = os.path.join(OUT, k + ".png")
        pg.request({"svg": svg, "w": W, "h": H, "out": out, "mode": "canvas"})
        meta[k] = {"w": W, "h": H, "feet_y": f["feet_y"], "canvas": CANVAS, "ppd": PPD,
                   "anchors": {a: list(v) for a, v in f["anchors"].items()}}
        print(k, W, H, "feet %.2f" % f["feet_y"])
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    pg.stop()
main()
