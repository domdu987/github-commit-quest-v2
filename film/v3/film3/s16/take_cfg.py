"""take s16 configuration for deliver.py"""
FIRST_G, LAST_G = 1455, 1675
SHOT_RANGES_OUT = {16: (1455, 1577), 17: (1587, 1675)}          # single-source frames (the dissolve is in INTERNAL)
QA_RANGES = {16: (1455, 1587), 17: (1576, 1675)}               # rendered ranges (camera QA)
QA_DEPTH = 4.0                                                  # D: screen points re-projected at the wall distance
INTERNAL = [dict(at=1582, type="dissolve", frames=9, mixed=[1578, 1586], from_shot=16, to_shot=17,
                 mix="smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 16 to g 1587, shot 17 from g 1576 (raw/)")]
HUE_ROWS = {"s16 shot 16 (g 1462-1581)": (1462, 1581), "s16 shot 17 (g 1582-1675)": (1582, 1675), "s16 all (g 1455-1675)": (1455, 1675)}


def camfun(mod, s):
    return mod.CAMS[s]


META = {"take": "s16", "shots": [16, 17], "g0": 1462, "g1": 1676, "handle_in": 7, "handle_out": 0,
        "transition_in": {"type": "dissolve", "frames": 10, "note": "handle g 1455..1461 rendered in 3D (shot 16 camera runs on before g 1462)"},
        "transition_out": {"type": "cut", "frames": 0},
        "internal": INTERNAL,
        "shot_ranges": {"16": [1462, 1581], "17": [1582, 1675]},
        "set": "v3/set3d3/harbor.py + fx.py (runtime: bulging seam patch, 3D rivets, glossy drip)", "light": "NOON",
        "state": "set_paint(1), set_seep(1), bucket fill 0.72 in place; bulge amp 0.04 -> 0.44 D with groan pulses"}

DRIP_LAND = [int(a + 0.86 * (b - a)) for a, b in [(1455, 1500), (1500, 1548), (1548, 1592), (1592, 1636), (1636, 1680)]]
CUES = [(1455, 1676, "ambience", "noon waterfront bed: distant harbour, gulls, a steady low creak of loaded steel under it", {}),
        (1462, 1676, "drone", "the tank's groan grows: a low sustained metal moan rising in pitch and volume to the cut (x2 layers)", {})]
for g in (1495, 1540, 1570, 1610, 1650):
    CUES.append((g - 3, g + 22, "groan", "deep metal groan of the swelling wall (camera tremor peaks)", {"peak_frame": g + 2}))
for g in DRIP_LAND:
    if 1455 <= g <= 1675:
        CUES.append((g, g, "drip", "thick drop of molasses plops into the half-full bucket (soft, viscous)", {"impact_frame": g}))
CUES += [(1490, 1503, "camera_snap", "small reframe on the first groan (soft whoosh)", {}),
         (1530, 1552, "camera_move", "camera cranes back and down to the low angle up the wall (whoosh, low)", {}),
         (1578, 1587, "dissolve", "dissolve to the rivet close-up", {}),
         (1590, 1676, "rattle", "tiny metallic chatter of one rivet trembling in its hole (grows)", {}),
         (1601, 1617, "camera_move", "pull back: tommy's worried face rises into the near foreground (soft whoosh)", {}),
         (1633, 1645, "creak", "sharp steel creak on 'khue siang mut' (the rivets are the groan)", {}),
         (1641, 1643, "accent", "tommy's eyes go wide (ring eyes) behind a blink: tiny gulp, optional", {})]
