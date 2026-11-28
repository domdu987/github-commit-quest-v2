"""stage_ep.py -- the stage of an EP.1 render process: one LOCATION per Blender process, cast built on demand.

    F = stage_ep.build("X1", tier, W, H, threads=1, spp=None, cast=["james"])

LOCATIONS  key -> builder(tier, W, H, threads, spp) returning an object with the hook Stage's interface
           (begin(shot), frame(shot, g) -> post, render(out_noext, g, post), cast, cam, screen(), pct, sc).
CAST       key -> builder(F): creates the actor on F (F.<key> = stage.Act(...); F.cast.append(...)).
Register new sets and characters from their own modules:
    import stage_ep; stage_ep.LOCATIONS["CAB"] = build_cab; stage_ep.CAST["praew"] = add_praew
Only "X1" (the hook's expressway with Kong, the crew member, the driver and the ten extras) exists today.
_x1 also wraps the Stage's begin(): every actor gets back the card pitch it was built with and no walk lock (see _neutral_begin).
"""
import epcommon as E

LOCATIONS = {}
CAST = {}
ALIASES = {}                     # e.g. {"X1s": "X1"} once the overturned sedan is dressing that a shot's setup() switches on


def _x1(tier, W, H, threads, spp):
    import stage                                         # v10/film/stage.py: builds the v11 set + the v8 cast
    F = stage.Stage(tier, W, H, threads=threads, spp=spp)
    _neutral_begin(F)
    return F


def _neutral_begin(F):
    """EP.1 additions to the hook Stage's begin() (v10/film/stage.py is not edited): before the hook's own reset and the
    shot's setup(), every actor of the process -- the hook's four and every actor an EP.1 module added -- gets back the
    card pitch it was built with (pitch_override; the hook's begin() resets only the seated driver), no walk lock and its
    built spec (a shot that swapped an added actor's spec sets it again in its own setup()).  Without this a shot inherits
    whatever the previous shot of the same worker left, so a frame would depend on which worker rendered it."""
    import stage
    if not getattr(stage.Act, "_ep_patched", False):     # remember the pitch an actor was BUILT with (also for actors a
        init0 = stage.Act.__init__                         # shot module creates lazily inside its setup())

        def init(self, *a, **k):
            init0(self, *a, **k)
            self._ep_pitch0 = self.a.pitch_override
        stage.Act.__init__ = init
        stage.Act._ep_patched = True
    for a in F.cast:                                       # the hook's four, built by Stage() just now
        if not hasattr(a, "_ep_pitch0"): a._ep_pitch0 = a.a.pitch_override
    orig = F.begin

    def begin(shot):
        for a in F.cast:
            a.a.pitch_override = getattr(a, "_ep_pitch0", a.a.pitch_override)
            a.a.walk_lock = None
        return orig(shot)

    F.begin = begin


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
