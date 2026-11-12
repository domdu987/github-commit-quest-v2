"""take s20 configuration for deliver.py"""
FIRST_G, LAST_G = 1847, 1967
SHOT_RANGES_OUT = {20: (1847, 1967)}
QA_RANGES = {20: (1847, 1967)}
QA_DEPTH = 2.5
INTERNAL = []
HUE_ROWS = {"s20 shot 20 (g 1856-1967)": (1856, 1967), "s20 all (g 1847-1967)": (1847, 1967)}


def camfun(mod, s):
    return mod.cam


META = {"take": "s20", "shots": [20], "g0": 1856, "g1": 1968, "handle_in": 9, "handle_out": 0,
        "transition_in": {"type": "dissolve", "frames": 15, "note": "handle g 1847..1855 rendered in 3D (shot 20 camera runs on before g 1856)"},
        "transition_out": {"type": "end", "frames": 0},
        "internal": [],
        "shot_ranges": {"20": [1856, 1967]},
        "set": "v3/set3d3/harbor.py + fx.py (swollen plate, glossy drip) + runtime: molasses sheet over the yard and the tank foot, split seam", "light": "NOON",
        "state": "bucket fill 1.0 (overflowing) in place at bucket_mark; bulge 0.66 D; most seam rivets gone"}

DRIPS = [(1840, 1872), (1872, 1902), (1902, 1931), (1931, 1960), (1960, 1990)]
CUES = [(1847, 1968, "ambience", "quiet after: far-off shouts and a bell, gulls, the slow seep of molasses; no music sting until the end", {})]
for a, b in DRIPS:
    g = int(a + 0.86 * (b - a))
    if 1847 <= g <= 1967:
        CUES.append((g, g, "drip", "a heavy drop falls into the brim-full bucket (thick 'plop', ring on the surface)", {"impact_frame": g}))
CUES += [(1847, 1856, "dissolve", "dissolve in from the flood", {}),
         (1899, 1899, "accent", "'yang wang yu' (still in its place): optional soft note", {"impact_frame": 1899}),
         (1927, 1967, "overflow", "slow overflow trickling down the bucket's sides ('tem jon lon')", {})]
