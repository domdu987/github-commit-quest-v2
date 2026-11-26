"""sets.py -- one entry point for the EP.1 sets and their registration with ep1/pipe/stage_ep.py.

    import sets
    R = sets.dress(A, "X1" | "X1s" | "X2" | "X2c" | "CAB" | "UND")     on a built v11 deck (A = beauty.build() anchors)
    sets.register()            stage_ep.LOCATIONS[...] for X1s, X2, X2c, CAB, UND (X1 keeps the hook's builder; a scene-02
                               shot calls sets.dress(F.A, "X1") once in its setup(), guarded by sets.dressed("X1"))
Each location is the hook's Stage (v11 deck, cast, props) plus the dressing; one location per Blender process.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import core as K

_DONE = {}

# Post options a shot should merge into what it returns for these locations.  post9.sparkle() scatters wet-road glints
# on every pixel of object index 1 and 4 within 90 D; all of this dressing is index 4, so without "sparkle": 0 the seats,
# the head lining, the equipment wall and the dry concrete under the deck are sprinkled with white specks.
POST = {
    "X1": {}, "X1s": {}, "X2": {}, "X2c": {},
    "CAB": {"sparkle": 0.0},                                  # add "rain": False for inserts that do not look out
    "UND": {"sparkle": 0.0, "RAIN": 0.0, "SPLASH": 0.0,       # the rain under the deck is geometry
            "flat": {"GLOW": 0.07, "AMB": 0.30}},             # v8 puppets: less white halo, a little more own fill (Stage._stage reads post["flat"])
}


def post(key, **more):
    d = dict(POST[{"X1S": "X1s", "X2C": "X2c"}.get(key, key)]); d.update(more); return d


def dressed(key):
    return key in _DONE


def dress(A, key):
    key = {"X1S": "X1s", "X2C": "X2c"}.get(key, key)
    if key in _DONE: return _DONE[key]
    if key == "X1":
        import x1; R = dict(x1=x1.dress(A))
    elif key == "X1s":
        import x1, sedan; R = dict(x1=x1.dress(A), sedan=sedan.build(A))
    elif key in ("X2", "X2c"):
        import x2; R = dict(x2=x2.build(A))
    elif key == "CAB":
        import x2, cab; R = dict(x2=x2.build(A)); R["cab"] = cab.build(A)
    elif key == "UND":
        import x2, under; R = dict(x2=x2.build(A)); R["und"] = under.build(A)
    else:
        raise KeyError(key)
    _DONE[key] = R
    return R


def register():
    PIPE = os.path.join(HERE, "..", "pipe")
    for p in (PIPE, os.path.join(HERE, "..", "..", "v10", "film")):
        if p not in sys.path: sys.path.insert(0, os.path.abspath(p))
    import stage_ep

    def mk(key):
        def builder(tier, W, H, threads, spp):
            import stage
            F = stage.Stage(tier, W, H, threads=threads, spp=spp)
            F.sets = dress(F.A, key)
            F.sets_post = post(key)
            K.retarget(F.cam)
            return F
        return builder
    for key in ("X1s", "X2", "X2c", "CAB", "UND"):
        stage_ep.LOCATIONS[key] = mk(key)
    return stage_ep
