"""c12.py -- helpers for the film-12 takes: per-frame cast12 cards on the set3d12 street. Import first in shot.py."""
import sys, os, math, json
PROJ = '/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj'
for p in (PROJ + '/v3/set3d12', PROJ + '/v3/cast12', PROJ + '/v3/cast10'):
    if p not in sys.path: sys.path.insert(0, p)
import street as S, bpy, cast12
from mathutils import Vector

def gof(t, shift=True):                      # film frame for a time in narration seconds
    return int(round((t + (0.10 if shift else 0.0)) * 30))

class Cards:
    def __init__(self): self.objs = {}
    def clear(self):
        for o, k in list(self.objs.values()): self._rm(o)
        self.objs = {}
    def _rm(self, o):
        me = o.data; bpy.data.objects.remove(o, do_unlink=True)
        if me and me.users == 0: bpy.data.meshes.remove(me)
    def hide(self, name):
        if name in self.objs:
            o, k = self.objs.pop(name); self._rm(o)
    def put(self, name, cast, pose, mark, key=None, mirror=False, tint=None, rim=None, tilt=0.0, over=None, roll=0.0, dz=0.0):
        cam = bpy.context.scene.camera; cl = cam.matrix_world.translation
        mark = (mark[0], mark[1], mark[2] + dz)
        k = (key, mirror, tint, rim, round(tilt, 2), json.dumps(over, sort_keys=True, default=str) if over else None)
        if name in self.objs and self.objs[name][1] == k and key is not None:
            o = self.objs[name][0]; o.location = mark
        else:
            self.hide(name)
            o = S.cast_card('c_' + name, cast, pose, mark, cl, tilt=tilt, tint=tint, rim=rim, mirror=mirror, over=over); self.objs[name] = (o, k)
        d = Vector(cl) - Vector(mark); o.rotation_euler = (math.radians(-tilt), math.radians(roll), math.atan2(-d.x, d.y) if False else math.atan2(Vector(cl).x - mark[0], -(Vector(cl).y - mark[1])))
        return o
    def walk(self, name, cyc, g, mark, speed=28.0, facing=1, **kw):
        cast, pose = cast12.cycle_frame(cyc, (g / speed) % 1.0, facing=facing)
        return self.put(name, cast, pose, mark, key=None, **kw)
    def story(self, name, pose_name, mark, over=None, **kw):
        cast, pose = cast12.STORY12[pose_name]
        return self.put(name, cast, pose, mark, key=pose_name, over=over, **kw)

def head_px(mark, h, tilt=0.0):
    cam = bpy.context.scene.camera
    return S.project_px(cam, (mark[0], mark[1], mark[2] + h))

def lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))
def sm(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
