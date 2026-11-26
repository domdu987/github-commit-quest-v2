"""epcommon.py -- EP.1 multi-scene timing on top of the hook pipeline (no bpy).  v10/film is imported, never edited.

A SCENE is a cut table  cut/scNN.json  written by cut.py from the plan's shot list and a caption-timing file:
    frames are scene-local (0-based, end exclusive); the Blender / stage frame is  g = g_base + local  with a fixed
    g_base per scene (scene number x 10000), so re-timing one scene never moves another scene's frames;
    the stage clock is  t = g / 24  (what a shot's frame(F, g, t, u) receives); word() and cue() answer on that clock.

    S = activate("sc02")            load the cut, and point v10's common.shot_range / shot_of / word / mouth at it
    S.range("S025") -> (g0, g1)     S.shot_at(local) -> shot dict     S.word("มันพุ่งใส่ก้อง") -> t     S.cue("name") -> t
    S.mouth("kong", g) -> 0, .25 .. 1     only while the sentence being spoken at g belongs to that speaker
"""
import os, sys, json, math, hashlib

PIPE = os.path.dirname(os.path.abspath(__file__))
EP1 = os.path.dirname(PIPE)
PROJ = os.path.dirname(EP1)
FILM = os.path.join(PROJ, "v10", "film")
if FILM not in sys.path:
    sys.path.insert(1, FILM)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
import common as C                                         # v10/film/common.py (numpy only)

FPS = C.FPS
FONTS = C.FONTS
KANIT = C.KANIT
# where things are looked for: the production folders first, then this package's own (the dummy scene lives here)
CUT_DIRS = [os.path.join(EP1, "cut"), os.path.join(PIPE, "cut")]
SHOT_DIRS = [os.path.join(EP1, "shots"), os.path.join(PIPE, "shots")]
OUT = os.environ.get("DZ09_EP1_OUT") or os.path.join(PIPE, "out")
G_PER_SCENE = 10000

# render classes (PRODUCTION_PLAN.md): the scale and samples a class gets at the final tier.  C1 is drawn, no Cycles.
CLASSES = {
    "A": dict(pct=100, spp=None, order=2, note="a named character's face is read: 100 % scale"),
    "B": dict(pct=75, spp=None, order=1, note="wide / crowd / prop insert: 75 %"),
    "C2": dict(pct=75, spp=4, order=1, note="the hook's macro staging: 75 %, 4 spp"),
    "C1": dict(pct=None, spp=None, order=0, note="2D drawn frames: module.draw(ctx), no Cycles"),
}
FINAL_TIERS = ("final", "final8")
# who moves his mouth for which speaker key of narration_ep1.json ("narr" and voices that are only heard move nobody)
SPEAKER_OF_ACTOR = {"kong": "kong", "crew": "crew", "james": "james", "praew": "praew", "tos": "tos", "guard": "guard",
                    "namnuea": "namnuea"}


def norm_id(sid):
    """'S25', 's025', '25' -> 'S025' (three digits, the folder / module name is the lower case of it)."""
    s = str(sid).strip().upper().lstrip("S")
    return "S%03d" % int(s)


def scene_name(x):
    s = str(x).lower()
    return s if s.startswith("sc") else "sc%02d" % int(s)


def find_cut(scene):
    for d in CUT_DIRS:
        p = os.path.join(d, scene + ".json")
        if os.path.exists(p):
            return p
    raise FileNotFoundError("no cut table %s.json in %s (run cut.py)" % (scene, CUT_DIRS))


def sha(*parts):
    h = hashlib.sha1()
    for p in parts:
        h.update(p if isinstance(p, bytes) else str(p).encode("utf-8"))
    return h.hexdigest()[:16]


class Scene:
    def __init__(self, scene, path=None):
        self.name = scene_name(scene)
        self.path = path or find_cut(self.name)
        d = self.d = json.load(open(self.path, encoding="utf-8"))
        self.g_base = int(d["g_base"]); self.frames = int(d["frames"]); self.narr0 = float(d.get("narr0", 0.0))
        self.shots = d["shots"]; self.ids = [s["id"] for s in self.shots]
        self.by_id = {s["id"]: s for s in self.shots}
        self.caps = d["captions"]                          # [{id, text, t0, t1, speaker, emph?, colour?}] scene seconds
        self.cues = d.get("cues", {})
        self.hard_cuts = set(d.get("hard_cuts", []))
        self.deps = {}                                     # what the shot being rendered looked up (run_ep stores it)
        self._mouth = None

    # ---- shots
    def shot(self, sid):
        return self.by_id[norm_id(sid)]

    def local(self, sid):
        s = self.shot(sid)
        return s["f0"], s["f1"]

    def range(self, sid):
        a, b = self.local(sid)
        return self.g_base + a, self.g_base + b

    def shot_at(self, local):
        for s in self.shots:
            if s["f0"] <= local < s["f1"]:
                return s
        return self.shots[-1]

    # ---- words and cues, on the stage clock
    def t_of(self, scene_seconds):
        return self.g_base / float(FPS) + scene_seconds

    def word(self, text, end=False, sid=None, n=0):
        """stage time at which a caption starts (or ends).  sid = sentence id when the text occurs twice; n = which one."""
        hits = [c for c in self.caps if c["text"] == text and (sid is None or c["id"] == sid)]
        if not hits:
            raise KeyError("caption %r not in %s" % (text, self.name))
        c = hits[min(n, len(hits) - 1)]
        v = c["t1"] if end else c["t0"]
        self.deps["word:%s:%s:%d:%d" % (sid or "", text, n, int(end))] = round(v, 4)
        return self.t_of(v)

    def cue(self, name):
        v = float(self.cues[name])
        self.deps["cue:" + name] = round(v, 4)
        return self.t_of(v)

    # ---- lip sync
    def mouth_track(self):
        if self._mouth is None:
            p = os.path.join(os.path.dirname(self.path), "mouth_%s.json" % self.name)
            if os.path.exists(p):
                self._mouth = json.load(open(p, encoding="utf-8"))
                import mouth as M
                if self._mouth.get("frames") != self.frames or self._mouth.get("caps_sig", M.caps_sig(self)) != M.caps_sig(self):
                    # the cut was rebuilt after the track was written: never use a stale track.  Rebuild it here from the
                    # same wav when that still exists (deterministic, so every worker gets the same one), else synthetic.
                    wav = self._mouth.get("source", "")
                    wav = wav if os.path.isfile(wav) else None
                    print("WARNING %s: mouth track is older than the cut (run mouth.py again): rebuilt in memory from %s" % (
                        self.name, wav or "the caption timing (synthetic)"), flush=True)
                    self._mouth = M.build(self, wav)
            else:
                import mouth as M                           # no track yet: the synthetic one from the caption timing
                self._mouth = M.build(self, None)
        return self._mouth

    def speaker(self, g):
        """speaker key of the sentence being spoken at stage frame g ('' between sentences, 'narr' for the narrator)."""
        k = g - self.g_base
        for a, b, who, _sid in self.mouth_track()["speakers"]:
            if a <= k < b:
                return who
        return ""

    def mouth(self, actor, g, floor=None):
        """mouth level (0, .25, .5, .75, 1) of an ACTOR at stage frame g: the track's level while the line is his, else 0."""
        who = SPEAKER_OF_ACTOR.get(actor, actor)
        k = g - self.g_base
        tr = self.mouth_track()
        if k < 0 or k >= len(tr["level"]) or self.speaker(g) != who:
            v = 0.0
        else:
            v = float(tr["level"][k])
        self.deps["mouth:%s:%d" % (who, k)] = v
        return v


_ACTIVE = None


def scene():
    if _ACTIVE is None:
        raise RuntimeError("no active scene: call epcommon.activate('scNN') first")
    return _ACTIVE


def activate(name, path=None):
    """load a scene and make v10's common answer for it: Stage and the hook's base helpers then work unchanged."""
    global _ACTIVE
    S = _ACTIVE = Scene(name, path)
    if not hasattr(C, "_hook_shot_range"):
        C._hook_shot_range, C._hook_shot_of, C._hook_word, C._hook_mouth = C.shot_range, C.shot_of, C.word, C.mouth

    def shot_range(sid):
        try:
            return scene().range(sid)
        except (KeyError, ValueError):
            return C._hook_shot_range(sid)

    def shot_of(g):
        S_ = scene()
        return S_.shot_at(g - S_.g_base)["id"]

    def word(text, end=False):
        return scene().word(text, end)

    def mouth_(g, floor=0.10):                             # the hook's helpers call C.mouth(g) for Kong (kong_phone(talk=True))
        return scene().mouth("kong", g)

    C.shot_range, C.shot_of, C.word, C.mouth = shot_range, shot_of, word, mouth_
    return S


# ------------------------------------------------------------------------------------------------ shot modules
def find_shot_file(scene_nm, sid):
    sid = norm_id(sid)
    for d in SHOT_DIRS:
        p = os.path.join(d, scene_nm, sid.lower() + ".py")
        if os.path.exists(p):
            return p
    return None


def load_shot(scene_nm, sid, tier=None):
    """import ep1/shots/scNN/sNNN.py under a unique module name; fill CLASS / LOC / PCT / SPP from the cut table when
    the module does not say (a module's own PCT / SPP win).  Returns the module, or None when the file does not exist."""
    import importlib.util
    sid = norm_id(sid)
    p = find_shot_file(scene_nm, sid)
    if p is None:
        return None
    name = "ep1_%s_%s" % (scene_nm, sid.lower())
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    row = scene().by_id.get(sid, {}) if _ACTIVE else {}
    mod.ID = sid
    mod.FILE = p
    if not hasattr(mod, "CLASS"): mod.CLASS = row.get("cls", "A")
    if not hasattr(mod, "LOC"): mod.LOC = row.get("set", "X1")
    if not hasattr(mod, "CAST"): mod.CAST = []
    cl = CLASSES[mod.CLASS]
    if cl["pct"] and not hasattr(mod, "PCT"):
        mod.PCT = {t: cl["pct"] for t in FINAL_TIERS}
    if cl["spp"] and not hasattr(mod, "SPP"):
        mod.SPP = {"final": cl["spp"]}
    return mod


def code_hash(mod):
    """hash of what a shot's picture is made from on the ep1 side: its module, the ep base modules, extra DEPS files."""
    files = [mod.FILE, os.path.join(PIPE, "epbase.py"), os.path.join(PIPE, "ep2d.py")] + list(getattr(mod, "DEPS", []))
    return sha(*[open(f, "rb").read() for f in files if os.path.exists(f)])


def out_dir(tier, W, H, scene_nm):
    return os.path.join(OUT, "%s_%dx%d" % (tier, W, H), scene_nm)


def frame_name(k):
    """file name of a shot's k-th frame (0-based within the shot)."""
    return "f_%04d" % (k + 1)
