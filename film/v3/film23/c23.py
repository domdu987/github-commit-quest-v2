#!/usr/bin/env python3
"""c23.py -- shared runner for the film-23 take scripts (copied from film8/common.py's role, switched to cast23 + set3d23/ghost).

A take script (sNN/shot.py) imports this file as C and calls C.main(CFG).  CFG describes the take:
  shot, g0, g1 (planned, g = film frame), h_in, h_out (handle frames), actors (list of dict), state(g, t, f) (keyed setters), tweak(GH) (set patch at build)
Frames: film frame g; Blender frame f = g - g_first + 1.  The camera is keyed from ghost_shots.pose (t = (g - g0) / n_take * 1.25, extrapolated linearly
in the handles); no random keys anywhere.
Commands:  python3 shot.py probe g,g,..  |  stills a:b:step out_dir [scale] [spp]  |  final a:b:step [scale] [spp]  |  ground
"""
import math, os, sys, json, time

HERE_C = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE_C)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast23"), os.path.join(V3, "stage"), os.path.join(V3, "set3d23"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast23                                            # noqa: E402  (before sprites / actors)
import puppet                                            # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import ghost as GH                                       # noqa: E402
import ghost_shots as SH                                 # noqa: E402
import actors, sprites, camrig                           # noqa: E402

lerp = lambda a, b, u: a + (b - a) * u
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))


def smooth(a, b, x):
    x = clamp((x - a) / float(b - a)); return x * x * (3 - 2 * x)


def parse(spec):
    out = []
    for part in str(spec).split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        elif part:
            out.append(int(part))
    return out


# ----------------------------------------------------------------------------- the clock
class Clock(object):
    def __init__(self, cfg):
        self.shot = cfg["shot"]
        self.g0, self.g1 = cfg["g0"], cfg["g1"]
        self.n = int(math.ceil((self.g1 - self.g0) * 1.25))            # frames of the x1.25 take
        self.g1r = self.g0 + self.n                                     # exclusive end of the take with its tail
        self.h_in, self.h_out = cfg.get("h_in", 0), cfg.get("h_out", 0)
        self.first = self.g0 - self.h_in
        self.last = self.g1r + self.h_out - 1                           # inclusive
        self.nf = self.last - self.first + 1

    def f(self, g): return int(g) - self.first + 1
    def t(self, g): return (g - self.g0) / float(self.n) * 1.25


def cam_pose(shot, t):
    """camera pose at t; linear extrapolation outside 0 .. 1.25 so the handles keep moving."""
    if 0.0 <= t <= 1.25:
        return SH.pose(shot, t)
    a, b = (0.0, 0.03) if t < 0 else (1.25, 1.22)
    pa, pb = SH.pose(shot, a), SH.pose(shot, b); k = (t - a) / (b - a) if b != a else 0.0
    L = lambda u, v: tuple(x + (y - x) * k for x, y in zip(u, v))
    return dict(loc=L(pa["loc"], pb["loc"]), look_at=L(pa["look_at"], pb["look_at"]), lens=pa["lens"] + (pb["lens"] - pa["lens"]) * k)


def key_cam(clk, gs):
    """key the scene camera over the frames gs (LINEAR keys, the easing is in the poses)."""
    cam = GH.shot_camera(clk.shot, 0.0); cam.animation_data_clear(); cd = cam.data; prev = None
    for g in gs:
        c = cam_pose(clk.shot, clk.t(g)); f = clk.f(g)
        cam.location = c["loc"]; fwd = (Vector(c["look_at"]) - Vector(c["loc"])).normalized()
        cam.rotation_euler = fwd.to_track_quat("-Z", "Y").to_euler()
        if prev is not None: cam.rotation_euler.make_compatible(prev)
        prev = cam.rotation_euler.copy(); cd.lens = c["lens"]
        cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cd.keyframe_insert("lens", frame=f)
    GH.STATE["PR"]._lin(cam); GH.STATE["PR"]._lin(cd)
    bpy.context.scene.camera = cam; GH.STATE["cam_ob"] = cam
    return cam


def tint_shade(names, mul):
    """QA_ART_SET (S07 / S12): per-surface shade tint.  Multiplies the painted shade colour (the MULTIPLY mix of ghost.mat_g) of the named materials
    (keys of GH.STATE['M']) by `mul` (r, g, b): more red = hue 236 -> ~250.  Returns the number of nodes changed."""
    n = 0
    for nm in names:
        m = GH.STATE["M"].get(nm)
        if m is None or not getattr(m, "node_tree", None): continue
        for nd in m.node_tree.nodes:
            if nd.bl_idname == "ShaderNodeMix" and nd.data_type == "RGBA" and nd.blend_type == "MULTIPLY":
                c = list(nd.inputs[7].default_value)
                if abs(c[0] - 0.30) < 0.4 and c[2] > 0.3:         # the shade colour (blue-violet), not an art tint
                    nd.inputs[7].default_value = (c[0] * mul[0], c[1] * mul[1], c[2] * mul[2], 1.0); n += 1
    return n


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, cfg, quality="preview", sprite_dir=None, here=None):
        self.cfg = cfg; self.clk = Clock(cfg); self.shot = cfg["shot"]
        self.here = here; self.sprite_dir = sprite_dir
        t0 = time.time()
        if cfg.get("prebuild"): cfg["prebuild"](SH)
        self.A = GH.build(self.shot, cards=False)
        self.sc = bpy.context.scene
        GH.quality(self.sc, quality)
        self.sc.render.threads = int(os.environ.get("C23_THREADS", cfg.get("threads", 4)))
        if cfg.get("tweak"): cfg["tweak"](GH, self)
        self.cam = None
        self.actors = {}; self.spec = {}; self.anch = {}
        self.marks = GH.marks(self.shot)
        for sp in cfg["actors"]:
            self.add_actor(sp)
        print("take %s: built in %.1f s" % (self.shot, time.time() - t0), flush=True)

    # -- actors
    def mark_xyz(self, m):
        role, i = m
        x, y, z, yaw, extra = self.marks[role][i]
        return Vector((x, y, z))

    def mark_local(self, m):
        role, i = m
        return Vector(SH.marks_local(self.shot)[role][i][:3])

    def add_actor(self, sp):
        name = sp["name"]; cast = sp["cast"]
        canvas = sp.get("canvas") or (cast23.CANVAS23_WIDE[cast] if sp.get("wide") else cast23.CANVAS23[cast])
        a = actors.Actor(name, cast)
        a.build(canvas, self.sprite_dir, shadow="proxy", contact=None)
        a.head_flip = False
        GH.no_bounce(a.card)
        a.card["gc_role"] = "card"
        for ob in (a.card,):
            ob.visible_glossy = False
        self.actors[name] = a; self.spec[name] = sp
        if sp.get("parent"):
            par = bpy.data.objects[sp["parent"]]
            self.spec[name]["_par"] = par

    def feet_world(self, sp, g):
        """world point of the feet at film frame g: a mark, a callable(g) or the parent's local frame."""
        at = sp["at"]
        p = at(g) if callable(at) else at
        if isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], str):
            p = self.mark_local(p) if sp.get("parent") else self.mark_xyz(p)
        p = Vector(p) + Vector(sp.get("off", (0, 0, 0)))
        if sp.get("parent"):
            par = sp["_par"]; bpy.context.view_layer.update()
            return par.matrix_world @ p
        return p

    def contact_blobs(self):
        for name, a in self.actors.items():
            sp = self.spec[name]
            if sp.get("parent") or sp.get("noshadow"): continue
            self.sc.frame_set(self.clk.f(self.clk.first)); bpy.context.view_layer.update()
            GH.contact_shadow(a.root, sp.get("shadow_r", 0.9), sp.get("shadow_d", 0.42))

    # -- keying
    def pose(self, gs):
        clk = self.clk; cfg = self.cfg
        self.cam = key_cam(clk, [g for g in range(clk.first, clk.last + 1)])
        st = cfg.get("state")
        for g in gs:                                              # keyed set state first (the jeep moves the seated cards)
            f = clk.f(g)
            self.sc.frame_set(f)                                  # the setters re-snap tanks to the ground: evaluate at this frame
            if st: st(GH, g, clk.t(g), f, self)
        bpy.context.view_layer.update()
        for g in gs:
            f = clk.f(g); self.sc.frame_set(f)
            for name, a in self.actors.items():
                sp = self.spec[name]; w = self.feet_world(sp, g)
                if not sp.get("parent") and not sp.get("air"):
                    gz = GH.ground_z(w.x, w.y, w.z + 6.0)
                    if gz is not None: w.z = gz - 0.005
                if sp.get("dz"): w.z += sp["dz"](g) if callable(sp["dz"]) else sp["dz"]
                fl = sp["flip"](g) if callable(sp.get("flip")) else bool(sp.get("flip"))
                a.place(f, (w.x, w.y, w.z), flip=fl)
        bpy.context.view_layer.update()
        for g in gs:
            f = clk.f(g); self.sc.frame_set(f)
            for name, a in self.actors.items():
                sp = self.spec[name]
                if sp.get("hide") and sp["hide"](g):
                    continue
                p = sp["pose"](g)
                a.pose(f, p, camera=self.cam, upper_k=sp.get("upper_k"))
        fs = [clk.f(g) for g in gs]
        for name, a in self.actors.items():
            sp = self.spec[name]
            fl = [clk.f(g) for g in gs if not (sp.get("hide") and sp["hide"](g))]
            if not fl: continue
            for f, r in zip(fl, a.render_sprites(sp.get("ppd", 160), frames=fl)):
                self.anch[(name, f)] = r["anchors"]
                if r.get("clipped"): print("WARNING sprite of %s clipped on frame %d" % (name, f), flush=True)

    def sync_hidden(self, g):
        for name, a in self.actors.items():
            sp = self.spec[name]; h = bool(sp.get("hide") and sp["hide"](g)); a.set_hidden(h)

    def render(self, g, out_png, samples=12, scale=1.0):
        f = self.clk.f(g); self.sc.frame_set(f); self.sc.camera = self.cam
        self.sync_hidden(g)
        for a in self.actors.values():
            a.sync(self.cam, self.sc)
        self.sc.cycles.samples = samples
        self.sc.render.resolution_percentage = int(round(scale * 100))
        os.makedirs(os.path.dirname(out_png), exist_ok=True)
        wall, cpu = GH.T.render(out_png)
        return wall, cpu

    def heads(self, g, radius=0.5):
        f = self.clk.f(g); self.sc.frame_set(f); out = {}
        for name, a in self.actors.items():
            if a.card.hide_render or (name, f) not in self.anch: continue
            res = a.feet.get(f)
            hx, hy = self.anch[(name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            out[name] = dict(x=round(c[0], 1), y=round(c[1], 1))
        return out


def main(cfg, here):
    cmd = sys.argv[1]
    work = os.path.join(here, "work"); os.makedirs(work, exist_ok=True)
    spr = os.path.join(work, "sprites")
    clk = Clock(cfg)
    if cmd in ("probe", "stills", "final", "ground"):
        q = "final" if cmd == "final" else "preview"
        Tk = Take(cfg, quality=q, sprite_dir=spr, here=here)
        if cmd == "ground":
            return ground(Tk, here, parse(sys.argv[2]) if len(sys.argv) > 2 else None)
        spec = sys.argv[2]
        gs = [g for g in parse(spec) if clk.first <= g <= clk.last]
        if cmd == "final":
            scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
            samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
            out = os.path.join(here, "frames"); os.makedirs(out, exist_ok=True)
            todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
            print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
            Tk.pose(todo); Tk.contact_blobs()
            for g in todo:
                png = os.path.join(out, "g_%04d.png" % g)
                wall, cpu = Tk.render(g, png + ".tmp.png", samples=samples, scale=scale); os.replace(png + ".tmp.png", png)
                rep = dict(g=g, wall=round(wall, 2), cpu=round(cpu, 2), heads=Tk.heads(g))
                json.dump(rep, open(os.path.join(out, "g_%04d.json" % g), "w"))
                print("g %d  %.1f s wall  %.1f cpu" % (g, wall, cpu), flush=True)
        else:
            out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(work, "stills")
            scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
            samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
            Tk.pose(gs); Tk.contact_blobs()
            for g in gs:
                if cmd == "probe":
                    print(json.dumps(dict(g=g, heads=Tk.heads(g))), flush=True); continue
                png = os.path.join(out, "g_%04d.png" % g)
                wall, cpu = Tk.render(g, png, samples=samples, scale=scale)
                print("g %d  %.1f s wall  heads %s" % (g, wall, json.dumps(Tk.heads(g))), flush=True)


def ground(Tk, here, gs=None):
    """ground_check (tools/ground_check.py) on the built take: every 10th frame + first + last, fixes nothing; writes GROUND.md."""
    GC = GH._gc(); clk = Tk.clk
    gs = gs or sorted(set(list(range(clk.first, clk.last + 1, 10)) + [clk.last]))
    Tk.pose(gs); Tk.contact_blobs()
    rows = []; air = {}
    for g in gs:
        f = clk.f(g); Tk.sc.frame_set(f); Tk.sync_hidden(g)
        for a in Tk.actors.values(): a.sync(Tk.cam, Tk.sc)
        with GH.dress_hidden(): res, a_ = GC.run_check(Tk.sc, every=10, gap=0.02, frame_list=[f])
        rows += res
        for k, v in a_.items(): air.setdefault(k, []).extend(v)
    fails = [r for r in rows if r["status"] != "OK"]
    L = ["# GROUND.md: ground_check on take %s (shot %s)" % (os.path.basename(here), Tk.shot), "",
         "tools/ground_check.py run_check, tolerance 0.02 D, frames every 10 (first and last included): %d frames, %d rows, %d objects, **%d FAIL**." % (len(gs), len(rows), len(set(r["obj"] for r in rows)), len(fails)), ""]
    if air: L.append("airborne (flagged): " + ", ".join(sorted(air)))
    if fails:
        L += ["| frame | object | gap | status |", "|---|---|---|---|"] + ["| %s | %s | %s | %s |" % (r["frame"] + clk.first - 1, r["obj"], r["gap"], r["status"]) for r in fails[:60]]
    open(os.path.join(here, "GROUND.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L[:12]))
    print("GROUND rows %d FAIL %d" % (len(rows), len(fails)))
