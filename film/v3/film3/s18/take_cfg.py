"""take s18 configuration for deliver.py"""
FIRST_G, LAST_G = 1676, 1864
SHOT_RANGES_OUT = {18: (1676, 1743), 19: (1744, 1864)}
QA_RANGES = {18: (1676, 1743), 19: (1744, 1864)}
QA_DEPTH = {18: 4.0, 19: 25.0}
INTERNAL = [dict(at=1744, type="cut", from_shot=18, to_shot=19)]
HUE_ROWS = {"s18 shot 18 (g 1676-1743)": (1676, 1743), "s18 shot 19 (g 1744-1855)": (1744, 1855), "s18 all (g 1676-1864)": (1676, 1864)}


def camfun(mod, s):
    return mod.CAMS[s]


META = {"take": "s18", "shots": [18, 19], "g0": 1676, "g1": 1856, "handle_in": 0, "handle_out": 9,
        "transition_in": {"type": "cut", "frames": 0},
        "transition_out": {"type": "dissolve", "frames": 15, "note": "handle g 1856..1864 rendered in 3D (shot 19 camera and wave run on)"},
        "internal": INTERNAL,
        "shot_ranges": {"18": [1676, 1743], "19": [1744, 1855]},
        "set": "v3/set3d3/harbor.py + fx.py (bulge, 3D rivets, tracers) + flood.py (smooth wave, rolling lip, spray, gloss)", "light": "NOON",
        "state": "shot 18: bulge 0.44 -> 0.66 D, 64 rivets pop g 1697..1734, seam splits g 1734..1743; shot 19: set_flood replaced by flood.py, u 0.08 -> 1.0"}

POPS = [1697 + (int(round(37.0 * (k / 63.0) ** 0.62)) if k else 0) for k in range(64)]
CUES = [(1676, 1744, "drone", "the wall at breaking point: deep strained groan, metal creaks, a rising whine", {}),
        (1697, 1697, "accent", "first rivet goes: a sharp crack like a rifle shot ('mut lek diit')", {"impact_frame": 1697})]
seen = {}
for g in POPS[1:]:
    seen[g] = seen.get(g, 0) + 1
for g, n in sorted(seen.items()):
    CUES.append((g, g, "rivet_shot", "rivet%s shoot%s out like bullets: crack + ricochet whizz past the lens (%d)" % ("s" if n > 1 else "", "" if n > 1 else "s", n),
                 {"impact_frame": g, "count": n}))
CUES += [(1697, 1743, "squirts", "molasses squirting from the empty rivet holes (wet hiss, splatter)", {}),
         (1715, 1724, "camera_snap", "punch-in on 'ok muean' (short whoosh)", {}),
         (1729, 1729, "accent", "the volley peaks on 'krasun' (several cracks at once)", {"impact_frame": 1729}),
         (1734, 1744, "burst", "the seam tears open: shrieking steel rip + a heavy gush, violent camera shake", {}),
         (1744, 1744, "cut", "hard cut to Commercial Street", {}),
         (1744, 1865, "wave", "the molasses wave: a deep rolling roar and slosh, louder as it nears; wood and iron creak in its way", {}),
         (1748, 1840, "people", "panicked shouts and running footsteps of two workers and two kids sprinting toward camera (no screams of pain)", {}),
         (1755, 1800, "rumble", "ground rumble under the low camera (tremor)", {}),
         (1790, 1830, "camera_move", "camera cranes up and back to the wide view (big whoosh)", {}),
         (1856, 1865, "dissolve", "dissolve to the bucket (sound of the wave fades into a drip)", {})]
