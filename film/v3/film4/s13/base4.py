#!/usr/bin/env python3
"""base4.py -- shared machinery of render-team-3 takes s13 / s14 / s16 (film 4, pagoda set v2).  Identical copy in each take
folder (each take is self-contained).  A take's shot.py subclasses Take and defines:

    PRESET, SHOTS = {shot: (g_first, g_last)}  (render ranges incl. handles), CAST = [names]
    camera_at(shot, g) -> (loc Vector, look Vector, roll deg)
    actors_at(shot, g) -> {name: dict(pos=(x, y, z), pose=dict, hands=None|dict, ppd=int)}   (visible actors of that frame)
    set_state(shot, g, f)   key the set controls (sway, quake, collapse) on Blender frame f
    dof(shot, g) -> (focus, fstop)   focus: actor name, (x, y, z) or None

Blender frame of (shot, g) = 1000 * (shot - 1) + g + 1.  Camera shake / lip-sync helpers below.
CLI (from the take's shot.py):  probe <shots> a:b[:step] | stills <shots> a:b[:step] <out> [scale] [samples] | final <shots> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json, wave

HERE_B = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE_B))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast4"), os.path.join(V3, "stage"), os.path.join(V3, "set3d4"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast4                                            # noqa: E402  (first)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

NARR = os.path.join(PROJ, "film4", "audio", "narration_bankky.wav")
TINT = {"SUNSET": dict(tint="#ffe2cc"), "NIGHT": dict(tint="#b8bfe8", ink="#1e142e"), "DAY": {}, "DAWN": {}}


def g_of(t):
    """narration time (s) -> film frame of an event (narration laid at +0.10 s)"""
    return int(round((t + 0.10) * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def V(*a):
    return Vector(a)


# ----------------------------------------------------------------------------- camera helpers
def path(g, ks):
    """ks = [(g, loc, look, ease)], eased between keys -> (loc, look)"""
    k = keys(g, [(f, tuple(l) + tuple(k_), e) for f, l, k_, e in ks])
    return Vector(k[:3]), Vector(k[3:])


def shake(g, amp_deg, seed=0):
    """deterministic hand-held / quake shake: (look offset factor vector in camera-ish units, roll deg).  Sum of sines,
    5..11 Hz, amplitude amp_deg (degrees of view rotation)."""
    t = g / 30.0
    a = math.radians(amp_deg)
    sx = math.sin(2 * math.pi * 6.1 * t + 1.3 + seed) * 0.6 + math.sin(2 * math.pi * 9.7 * t + 0.4 + seed * 2) * 0.4
    sy = math.sin(2 * math.pi * 7.3 * t + 2.1 + seed) * 0.6 + math.sin(2 * math.pi * 11.3 * t + 3.0 + seed * 3) * 0.4
    sr = math.sin(2 * math.pi * 5.2 * t + 0.7 + seed) * 0.7 + math.sin(2 * math.pi * 8.9 * t + 1.9 + seed) * 0.3
    return a * sx, a * sy, amp_deg * 0.6 * sr


def apply_shake(loc, look, g, amp_deg, seed=0):
    if amp_deg <= 0:
        return loc, look, 0.0
    dx, dy, roll = shake(g, amp_deg, seed)
    f = (look - loc); dist = f.length; f.normalize()
    r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    look2 = look + (r * dx + u * dy) * dist
    loc2 = loc + (r * dx + u * dy) * 0.15                  # a little translation too (the ground moves)
    return loc2, look2, roll


# ----------------------------------------------------------------------------- lip-sync from the narration
_ENV = None


def _envelope():
    global _ENV
    if _ENV is None:
        import numpy as np
        w = wave.open(NARR); sr = w.getframerate(); n = w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        hop = sr // 60                                     # 1/60 s bins
        m = len(a) // hop
        _ENV = (np.sqrt((a[:m * hop].reshape(m, hop) ** 2).mean(axis=1)), 60.0)
    return _ENV


def mouth_at(g, g0, g1):
    """lip-sync mouth for film frame g inside a quoted line [g0, g1]: a new drawing every 2 frames (held on even blocks),
    level from the narration RMS over that block: flat / talk_a / talk_b, an 'o' now and then.  Outside: None."""
    if g < g0 or g > g1:
        return None
    import numpy as np
    env, rate = _envelope()
    gb = g0 + 2 * ((g - g0) // 2)
    t0 = gb / 30.0 - 0.10; t1 = (gb + 2) / 30.0 - 0.10
    seg = env[int(t0 * rate):max(int(t0 * rate) + 1, int(t1 * rate))]
    lo = env[int((g0 / 30.0 - 0.1) * rate):int((g1 / 30.0 - 0.1) * rate)]
    ref = float(np.percentile(lo, 90)) if len(lo) else 1.0
    v = float(seg.mean()) / max(ref, 1e-6)
    if v < 0.18:
        return "flat"
    if v < 0.55:
        return "talk_o" if (gb // 2) % 5 == 3 else "talk_a"
    return "talk_b"


# ----------------------------------------------------------------------------- the take
class Take(object):
    PRESET = "NIGHT"
    SHOTS = {}
    CAST = []
    NAME = "sXX"
    HERE = HERE_B

    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = G.build(self.PRESET)
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 20000
        self.extra_set()
        self.cam = camrig.make_camera(scene, name="cam_" + self.NAME)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(self.HERE, "work", "sprites")
        self.act = {}
        for n in self.CAST:
            a = actors.Actor(n, n); a.build(self.canvas(n), sd, contact=True); self.act[n] = a
            T.no_bounce(a.card)
        kd = Vector(self.A["key_dir"][:2]) if "key_dir" in self.A else Vector((0.5, 0.5))
        self.light_src = -kd.normalized()                   # horizontal direction toward the key
        self.anch = {}
        self.vis = {}
        if verbose:
            print("%s: built in %.1f s" % (self.NAME, time.time() - t0), flush=True)

    # hooks -------------------------------------------------------------------
    def extra_set(self):
        pass

    def canvas(self, name):
        return sprites.DEFAULT_CANVAS[name]

    def camera_at(self, shot, g):
        raise NotImplementedError

    def actors_at(self, shot, g):
        return {}

    def set_state(self, shot, g, f):
        pass

    def dof(self, shot, g):
        return None, None

    # machinery ---------------------------------------------------------------
    def head_flip_for(self, loc, look):
        d = look - loc; r = Vector((d.y, -d.x)).normalized()
        return r.dot(self.light_src) > 0.0

    def pose(self, shot, gs):
        """key camera, placements, set state for frames gs of shot; pose and rasterise the visible actors"""
        plan = {}
        for g in gs:
            f = bf(shot, g)
            loc, look, roll = self.camera_at(shot, g)
            camrig.key_camera(f, loc, look, roll=roll, cam=self.cam, interp="LINEAR", easing="AUTO")
            ats = self.actors_at(shot, g)
            plan[g] = ats
            for n, d in ats.items():
                self.act[n].place(f, d["pos"])
            self.set_state(shot, g, f)
        jobs = {}
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            loc, look, roll = self.camera_at(shot, g)
            flip = self.head_flip_for(loc, look)
            for n, d in plan[g].items():
                a = self.act[n]
                p = dict(d["pose"]); p.update({k: v for k, v in TINT.get(self.PRESET, {}).items() if k not in p})
                a.head_flip = flip
                hands = d.get("hands")
                if callable(hands):
                    hands = hands(self, f)
                a.pose(f, p, hands=hands, camera=self.cam)
                jobs.setdefault((n, d.get("ppd", 256), flip), []).append(f)
            self.vis[(shot, g)] = set(plan[g].keys())
        for (n, ppd, flip), fr in jobs.items():
            a = self.act[n]; a.head_flip = flip
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("%s: WARNING sprite of %s clipped on frame %d" % (self.NAME, n, f), flush=True)

    def visible(self, shot, g):
        v = self.vis.get((shot, g), set())
        for n, a in self.act.items():
            a.set_hidden(n not in v)

    def setup_dof(self, shot, g):
        foc, fs = self.dof(shot, g)
        if isinstance(foc, str):
            foc = self.act[foc].card
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)
        return foc, fs

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, roll = self.camera_at(shot, g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for n in sorted(self.vis.get((shot, g), ())):
            a = self.act[n]
            if (n, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(n, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = self.points()
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def points(self):
        return {"pagoda_top": (0, 0, G.SORIN_TOP), "tower_top": (14.0, 0.0, 20.8), "gate": (0.0, -32.0, 4.0)}

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        res = []
        for g in gs:
            self.visible(shot, g)
            self.setup_dof(shot, g)
            self.scene.cycles.samples = samples
            res += render.render_frames([bf(shot, g)], out_dir, scale=scale, threads=threads, scene=self.scene,
                                        camera=self.cam, verbose=False)
        return res


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(TakeCls):
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    R = TakeCls.SHOTS
    if cmd in ("probe", "stills"):
        Tk = TakeCls()
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if R[shot][0] <= g <= R[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        Tk = None
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if R[shot][0] <= g <= R[shot][1]]
            out = os.path.join(TakeCls.HERE, "raw", "s%d" % shot)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = TakeCls(quality="final")
            for i in range(0, len(todo), 24):                 # pose in chunks (sprites), render each frame
                chunk = todo[i:i + 24]
                Tk.pose(shot, chunk)
                for g in chunk:
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    png = os.path.join(out, "g_%04d.png" % g)
                    os.replace(st["path"], png)
                    rep = Tk.report(shot, g)
                    rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                    json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                    print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
