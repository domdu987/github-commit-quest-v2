"""stage_ep.py -- the stage of an EP.1 render process: one LOCATION per Blender process, cast built on demand.

    F = stage_ep.build("X1", tier, W, H, threads=1, spp=None, cast=["james"])

LOCATIONS  key -> builder(tier, W, H, threads, spp) returning an object with the hook Stage's interface
           (begin(shot), frame(shot, g) -> post, render(out_noext, g, post), cast, cam, screen(), pct, sc).
CAST       key -> builder(F): creates the actor on F (F.<key> = stage.Act(...); F.cast.append(...)).
Register new sets and characters from their own modules:
    import stage_ep; stage_ep.LOCATIONS["CAB"] = build_cab; stage_ep.CAST["praew"] = add_praew
Only "X1" (the hook's expressway with Kong, the crew member, the driver and the ten extras) exists today.
"""
import epcommon as E

LOCATIONS = {}
CAST = {}
ALIASES = {}                     # e.g. {"X1s": "X1"} once the overturned sedan is dressing that a shot's setup() switches on


def _x1(tier, W, H, threads, spp):
    import stage                                         # v10/film/stage.py: builds the v11 set + the v8 cast
    return stage.Stage(tier, W, H, threads=threads, spp=spp)


LOCATIONS["X1"] = _x1


def build(loc, tier, W, H, threads=1, spp=None, cast=(), pct=0):
    key = ALIASES.get(loc, loc)
    if key not in LOCATIONS:
        raise SystemExit("location %r is not built yet (stage_ep.LOCATIONS has %s)" % (loc, sorted(LOCATIONS)))
    if pct:
        import stage
        stage.PCT_FORCE = pct
    F = LOCATIONS[key](tier, W, H, threads, spp)
    F.loc_key = key
    have = {a.name for a in F.cast}
    for name in cast:
        if name in have or hasattr(F, name): continue
        if name not in CAST:
            raise SystemExit("cast %r is not built yet (stage_ep.CAST has %s)" % (name, sorted(CAST)))
        CAST[name](F)
    return F
