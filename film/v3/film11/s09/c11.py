#!/usr/bin/env python3
"""c11.py -- helpers for film-11 takes (copy of film8/common.py adapted to cast11 + set3d11/dairy.py).
Blender frame f = g + 1 (one take per process).  Hooks are frame drivers: every frame is alive when rendered with frame_set."""
import math, os, sys, json, time
FILM = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(FILM)))      # .../film
V3 = os.path.join(PROJ, "v3")
for p in (os.path.join(V3, "cast11"), os.path.join(V3, "stage"), os.path.join(V3, "set3d11"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast11                                           # noqa  (before sprites)
import bpy                                              # noqa
from mathutils import Vector                            # noqa
import dairy as D                                       # noqa
import actors, camrig, render, sprites                  # noqa
from PIL import Image, ImageDraw                        # noqa

def g_of(t): return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))
def bf(g): return int(g) + 1
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def ez(u):
    u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def u_of(g, a, b): return ez((g - a) / float(b - a))
def blink(g, period=90, off=0): return cast11.blink_at(g, period, off)

def make_actor(name, cast, sprite_dir, canvas=None, contact=True, **kw):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow="proxy")
    a.head_flip = kw.get("head_flip", False)
    D.no_bounce(a.card)
    return a

def place(actor, f, pos, scale=1.0):
    actor.place(f, (float(pos[0]), float(pos[1]), float(pos[2])), scale=scale)

# ---------------------------------------------------------------- small flat card (sore etc.)
def _png_sore(path, kind):
    S = 256; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S // 2
    if kind == "dot":
        d.ellipse((c - 70, c - 70, c + 70, c + 70), fill=(222, 70, 62, 255), outline=(150, 40, 40, 255), width=8)
        d.ellipse((c - 30, c - 40, c - 5, c - 18), fill=(246, 150, 140, 255))
    else:  # blister: pale dome with a red ring
        d.ellipse((c - 95, c - 95, c + 95, c + 95), fill=(214, 70, 62, 255))
        d.ellipse((c - 66, c - 66, c + 66, c + 66), fill=(246, 232, 190, 255), outline=(190, 150, 110, 255), width=6)
        d.ellipse((c - 34, c - 44, c - 6, c - 22), fill=(255, 252, 235, 255))
    im.save(path)

class Sore(object):
    """flat card pinned to a world point, faces the camera (yaw). kinds: dot / blister / None (hidden)."""
    def __init__(self, work, size=0.16):
        os.makedirs(work, exist_ok=True)
        self.size = size; self.mats = {}
        self.root = bpy.data.objects.new("sore_root", None); bpy.context.scene.collection.objects.link(self.root)
        me = actors._quad("sore_quad", -size / 2, -size / 2, size / 2, size / 2)
        me.materials.append(None); self.obs = {}
        for k in ("dot", "blister"):
            p = os.path.join(work, "sore_%s.png" % k); _png_sore(p, k)
            img = bpy.data.images.load(p, check_existing=True); img.alpha_mode = "STRAIGHT"
            m, tex = actors.card_material("sore_" + k, img, "Cubic")
            ob = bpy.data.objects.new("sore_" + k, me); bpy.context.scene.collection.objects.link(ob); ob.parent = self.root
            ob.material_slots[0].link = "OBJECT"; ob.material_slots[0].material = m
            ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_shadow = False; ob.hide_render = True
            self.obs[k] = ob
    def key(self, f, kind, world, cam_loc, toward=0.04, scale=1.0):
        d = Vector(cam_loc) - Vector(world); d.z = 0
        if d.length > 1e-6: d.normalize()
        loc = Vector(world) + Vector((d.x, d.y, 0)) * toward
        self.root.location = loc; self.root.rotation_euler = (0, 0, math.atan2(d.x, -d.y)); self.root.scale = (scale,) * 3
        for p in ("location", "rotation_euler", "scale"): self.root.keyframe_insert(p, frame=f)
        for k, ob in self.obs.items():
            ob.hide_render = (k != kind); ob.keyframe_insert("hide_render", frame=f)

# ---------------------------------------------------------------- the take
class Take(object):
    def __init__(self, preset, light=None, lens=22.0, name="cam_take"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.preset = preset
        self.A = D.build(preset, light=light)
        sc.cycles.samples = 12; sc.render.threads_mode = "FIXED"; sc.render.threads = 2
        sc.render.use_persistent_data = False
        sc.frame_start, sc.frame_end = 1, 9000
        self.cam = camrig.make_camera(sc, name=name, lens=lens)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 4000
        self.cam.data.dof.use_dof = False
        sc.camera = self.cam
        # director note 2026-11-18: the set's chimney smoke is a stack of round white blobs -> hide it (hook kind 'smoke')
        for h in self.A["hooks"]:
            if h["kind"] == "smoke" and bpy.data.objects.get(h["obj"]) is not None:
                bpy.data.objects[h["obj"]].hide_render = True
        self.stand = self.A["stand"][preset]
        self.actors = {}; self.anch = {}
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)
    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")
    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"): print("WARNING sprite %s clipped f%d" % (a.name, f), flush=True)
    def world_anchor(self, a, name, f):
        self.scene.frame_set(f)
        return actors.local_to_world(a, self.anch[(a.name, f)][name], f, camera=self.cam)
    def head_report(self, f):
        out = {}; self.scene.frame_set(f)
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch: continue
            res = a.feet.get(f); hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - .5, hy), f, res); r = actors.local_to_screen(a, self.cam, (hx + .5, hy), f, res)
            out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        return out
    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam; self.cam.data.dof.use_dof = False
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def final_loop(Tk, gs, here, scale=1.0, samples=12, threads=2, outname="raw"):
    out = os.path.join(here, outname); os.makedirs(out, exist_ok=True)
    todo = []
    for g in gs:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
        ok = os.path.exists(png) and os.path.exists(js)
        if ok:
            m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok: todo.append(g)
    print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
    if not todo: return
    Tk.pose(todo)
    for g in todo:
        st = Tk.render([bf(g)], out, scale=scale, samples=samples, threads=threads)[0]
        png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
        rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
        json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
