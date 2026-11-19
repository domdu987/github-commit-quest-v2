"""c17.py -- helper for film 17 take s08 (copy-adapted from film8/common.py: cast17 + set3d17/bertillon.py)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast17                                    # noqa: E402  (before sprites)
import bpy                                       # noqa: E402
from mathutils import Vector                     # noqa: E402
import bertillon as K                            # noqa: E402
import actors, camrig, render, sprites           # noqa: E402

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def smooth(x): x = clamp(x); return x * x * (3 - 2 * x)
def sine(x): x = clamp(x); return 0.5 - 0.5 * math.cos(math.pi * x)

def g_of(t):  return int(round((t + 0.10) * 30))     # narration time -> film frame of an event

def cam_path(waypoints, g):
    """waypoints [(g, loc, look, kind)], kind of the segment ENDING at that waypoint: 'drift' (0.35 sine + 0.65 linear: never dead) or 'snap' (smoothstep)."""
    if g <= waypoints[0][0]: return Vector(waypoints[0][1]), Vector(waypoints[0][2])
    for (ga, la, ka, _), (gb, lb, kb, kind) in zip(waypoints, waypoints[1:]):
        if g <= gb:
            x = (g - ga) / float(gb - ga)
            u = smooth(x) if kind == 'snap' else 0.35 * sine(x) + 0.65 * x
            return Vector(la).lerp(Vector(lb), u), Vector(ka).lerp(Vector(kb), u)
    return Vector(waypoints[-1][1]), Vector(waypoints[-1][2])

class Take(object):
    def __init__(self, preset, light, quality="draft", sprite_dir=None):
        self.A = K.build(preset=preset, light=light)
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        K.clear_keys()
        self.quality = quality; K.setup_render(self.scene, quality)
        self.sprite_dir = sprite_dir
        os.makedirs(sprite_dir, exist_ok=True)
        self.actors = {}
        self.anch = {}

    def add_actor(self, name, story, mark=None, xyz=None, rim=True, H=None):
        cast, pose = cast17.STORY17[story]
        a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], self.sprite_dir, contact=True); a.head_flip = True
        sc = (H or K.CAST_H[cast]) / K.CAST_HD[cast]
        if xyz is None:
            x, y, z = self.A['marks'][mark][:3]; xyz = (x, y, z)
        a.k_scale = sc; a.k_xyz = tuple(xyz); a.k_rim = K.RIM_FOR.get(cast) if rim else None
        self.actors[name] = a
        return a

    def key_cam(self, g, loc, look):
        camrig.key_camera(g, Vector(loc), Vector(look), cam=self.cam, interp="LINEAR", easing="AUTO")

    def pose_actor(self, a, g, pose, dxyz=(0, 0, 0), scale=1.0):
        pose = dict(pose); pose['seat17'] = None
        if a.k_rim: pose['rim'] = a.k_rim; pose['rim_opacity'] = 0.55; pose['rim_w'] = 0.02
        x, y, z = a.k_xyz
        a.place(g, (x + dxyz[0], y + dxyz[1], z + dxyz[2]), scale=a.k_scale * scale)
        self.scene.frame_set(g)
        a.pose(g, pose, camera=self.cam)

    def sprites_for(self, gs, ppd):
        for a in self.actors.values():
            for g, r in zip(gs, a.render_sprites(ppd, frames=gs)):
                self.anch[(a.name, g)] = r["anchors"]
                if r.get("clipped"): print("WARNING clipped", a.name, g, flush=True)

    def heads(self, g, W=720, radius=0.5):
        out = {}
        self.scene.frame_set(g)
        for a in self.actors.values():
            if (a.name, g) not in self.anch: continue
            res = a.feet.get(g)
            hx, hy = self.anch[(a.name, g)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), g, res)
            l = actors.local_to_screen(a, self.cam, (hx - radius, hy), g, res)
            r = actors.local_to_screen(a, self.cam, (hx + radius, hy), g, res)
            k = 720.0 / W; out[a.name] = dict(x=round(c[0] * k, 1), y=round(c[1] * k, 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]) * k, 1))
        return out

    def render(self, g, path, scale_mode, samples):
        sc = self.scene; sc.frame_set(g)
        K.setup_render(sc, 'draft' if scale_mode == 'quick' else scale_mode, samples)
        if scale_mode == 'quick': sc.render.resolution_x, sc.render.resolution_y = 180, 320
        sc.cycles.use_adaptive_sampling = True
        for a in self.actors.values(): a.sync(self.cam, sc)
        sc.render.threads_mode = "FIXED"; sc.render.threads = 2; sc.render.filepath = path
        t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t
        K.grade(path)
        return dt
