#!/usr/bin/env python3
"""c13.py -- helpers for my film-13 takes (copy of film8/common.py switched to cast13 + set3d13/chicago.py).
GOTCHAS: one location per process; key EVERY animated hook on every rendered frame (a keyed hook beats un-keyed calls);
set_jack_count keys constant; moves must move (never static > 6 frames); NO DOF."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast13"), os.path.join(V3, "stage"), os.path.join(V3, "set3d13"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path: sys.path.insert(0, p)
import cast13                                           # noqa: E402  (before sprites: registers the cast)
import puppet                                           # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import chicago as S                                     # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, clamp, lerp                      # noqa: E402,F401
N_FILM = 1995

def g_of(t): return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))
def bf(shot, g): return 1000 * (shot - 1) + int(g) + 1
def ez(u, kind="sine"): return ease(clamp(u), kind)

def make_actor(name, cast, sprite_dir, canvas=None, contact=True):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow="proxy")
    a.head_flip = False
    S.no_bounce(a.card)
    return a

def place(actor, f, xy, z=0.0, scale=1.0): actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale)

# real cast13 stand-ins for the set's crowd cards (T.PH roles -> cast13 members; heights in D)
def use_cast13_crowd():
    P = lambda **k: dict(dict(yaw=0.25, expr="neutral", mouth="smile", arm_l="down", arm_r="down", legs="stand"), **k)
    S.T.PH.update(
        worker=("worker13_a", P(arm_l="hip"), 3.2), foreman=("foreman13", P(arm_l="hip"), 3.27), rich=("rich", P(), 3.3),
        maid=("town_b", P(), 3.0), clerk=("gentleman13", P(), 3.2), kid=("town_c", P(), 2.44),
        towns_m=("town_a", P(), 3.24), towns_f=("town_b", P(yaw=-0.2), 3.0), towns_o=("worker13_b", P(yaw=-0.25, arm_l="hip"), 3.2))

class Take(object):
    """one Chicago preset (location) in a fresh scene, one custom camera, DOF off, 12 samples."""
    def __init__(self, preset, quality="preview", lens=22.0, light=None, state=None, name="cam_take"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        use_cast13_crowd()
        self.A = S.build(preset, light=light, state=state)
        S.clear_keys()
        S.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"; scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.05; self.cam.data.clip_end = 6000
        self.no_dof()
        scene.camera = self.cam
        self.actors, self.anch = {}, {}
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)
    def no_dof(self): self.cam.data.dof.use_dof = False
    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")
    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"): print("WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)
    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam; self.no_dof(); self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)

def head_report(take, f, radius=0.5):
    out = {}; take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch: continue
        res = a.feet.get(f); hx, hy = take.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, take.cam, (hx - radius, hy), f, res); r = actors.local_to_screen(a, take.cam, (hx + radius, hy), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
    return out

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def final_loop(make_take, gs_spec, g_range, here, shot, scale=1.0, samples=12, threads=2, quality="final"):
    gs = [g for g in parse(gs_spec) if g_range[0] <= g <= g_range[1]]
    out = os.path.join(here, "raw"); os.makedirs(out, exist_ok=True); todo = []
    for g in gs:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g); ok = os.path.exists(png) and os.path.exists(js)
        if ok: m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok: todo.append(g)
    print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
    if not todo: return
    Tk = make_take(quality); Tk.pose(todo)
    for g in todo:
        st = Tk.render([g], out, scale=scale, samples=samples, threads=threads)[0]
        png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
        rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
        json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
