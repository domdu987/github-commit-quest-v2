"""rig.py -- a light test stage for the EP.1 sets: the v11 deck, a camera with the film's conventions, the user's rain
levels, and two v8 paper puppets (kong_wet, crew_wet) through v10/film's Act wrapper (flat, camera-facing cards).
Nothing here is for the film itself: shots use ep1/pipe's Stage; this is what tests.py renders proofs with."""
import os, sys, math, time, json, resource
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(PROJ, "v11", "set"), os.path.join(PROJ, "v8", "cast"), os.path.join(PROJ, "v10", "film"), HERE):
    if p not in sys.path: sys.path.insert(0, p)
import bpy
from mathutils import Vector, Quaternion, Euler
import core as K
import beauty as B
import post11

LEVELS = dict(RAIN=0.2, SPLASH=0.25, HAZE=0.3, TILT=0.0, DOF=0.25, BLOOM=0.55)      # the user's standing levels
TIERS = {"draft": dict(q="preview", spp=2, pct=100), "final": dict(q="final", spp=5, pct=75), "finalA": dict(q="final", spp=5, pct=100)}


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF); c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime + c.ru_utime + c.ru_stime


class Rig:
    def __init__(self, tier="draft", W=360, H=640, threads=1, puppets=True):
        t0 = time.time(); c0 = cpu()
        self.tier = tier; self.W, self.H = W, H
        T = TIERS[tier]
        self.A = B.build()
        B.setup_render(T["q"], threads=threads)
        sc = self.sc = bpy.context.scene
        sc.cycles.samples = T["spp"]; self.spp = T["spp"]
        B.X._STATE["pct"] = T["pct"]; self.pct = T["pct"]
        sc.render.use_motion_blur = False
        sc.cycles.adaptive_min_samples = min(sc.cycles.adaptive_min_samples, sc.cycles.samples)
        sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 32)
        sc.render.resolution_x, sc.render.resolution_y = W, H
        sc.render.resolution_percentage = T["pct"]
        sc.render.fps = 24
        post11.set_levels(**LEVELS)
        self.cam = B.X.make_camera(); sc.camera = self.cam
        K.retarget(self.cam)
        self.acts = []
        if puppets:
            import stage as ST, stage8 as S8
            self.ST = ST; self.S8 = S8
            S8.set_mode("flat")
            self.kong = ST.Act(self, "kong", "kong_wet", ST.KONG_H, ppd=240)
            self.crew = ST.Act(self, "crew", "crew_wet", ST.CREW_H, ppd=240)
            self.acts = [self.kong, self.crew]
            for a in self.acts: a.hide()
            S8.tune_flat(**dict(S8.FLAT_DEFAULT, EXPO=1.6)); ST.tune_skin()
        self.build_cpu = cpu() - c0; self.build_wall = time.time() - t0
        print("rig built: %.1f CPU s, %.1f wall s" % (self.build_cpu, self.build_wall), flush=True)

    def set_pct(self, pct):
        B.X._STATE["pct"] = pct; self.sc.render.resolution_percentage = pct; self.pct = pct

    def camera(self, loc, look, lens, roll=0.0, focus=None, k=7.0, kmax=22.0, clip=0.05):
        cam = self.cam
        loc = Vector(loc); look = Vector(look)
        q = (look - loc).to_track_quat("-Z", "Y") @ Quaternion((0, 0, 1), math.radians(roll))
        cam.rotation_mode = "XYZ"; cam.location = loc; cam.rotation_euler = q.to_euler()
        cam.data.lens = lens; cam.data.clip_start = clip
        cam["preset"] = "look"; cam["aspect"] = "9:16"
        cam["focus"] = tuple(focus if focus is not None else look); cam["coc_k"] = float(k); cam["coc_max"] = float(kmax); cam["dof_k"] = 1.0
        bpy.context.view_layer.update()
        K.retarget(cam)
        return cam

    def pose(self, act, loc, face, view=None, s=None, exposure=1.6, **pose):
        act.set(loc=loc, face=face, view=view, s=s, **pose)

    def apply(self, exposure=1.6, shadow_at=None, ppd_auto=True, flat=None):
        if not self.acts: return
        self.S8.tune_flat(**dict(self.S8.FLAT_DEFAULT, EXPO=exposure, **(flat or {}))); self.ST.tune_skin()      # as Stage._stage does with post['flat']
        long_px = max(self.W, self.H)
        for a in self.acts:
            if a.visible and ppd_auto:
                from bpy_extras.object_utils import world_to_camera_view as w2c
                z = w2c(self.sc, self.cam, Vector(a.loc) + Vector((0, 0, 2.3))).z
                if z > 0.05:
                    d_px = a.a.sc * self.cam.data.lens / 36.0 / z * long_px
                    want = int(min(780, max(240, math.ceil(d_px * 1.25 / 60.0) * 60)))
                    if want != a.a.ppd: a.a.ppd = want; a.key = None
            a.apply(self.cam)
        bpy.context.view_layer.update()
        vis = [a.a for a in self.acts if a.visible and a.posed]
        if vis and shadow_at is not None:
            L = self.ST.dominant_light(shadow_at)
            if L is not None:
                try: self.S8.shadow_link(vis, L)
                except Exception as ex: print("shadow_link failed", ex)

    def render(self, out_noext, frame=7, post=None, keep=False):
        po = {"exposure": 1.6, "sharp_idx": [2]}
        po.update(post or {})
        c0 = cpu(); w0 = time.time()
        r = B.render6.render(out_noext, frame=frame, post_opts=po)
        r["cpu"] = round(cpu() - c0, 2); r["wall"] = round(time.time() - w0, 2)
        if not keep:
            for suf in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_shafts.pkl", "_info.json", "_raw.png", "_depth.png"):
                p = out_noext + suf
                if os.path.exists(p): os.remove(p)
        return r
