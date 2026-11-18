"""c12.py -- helpers of the film-12 s19 take: per-frame cast12 cards in the street set (street.py).
Cards are rebuilt per frame from a pose (the PNG raster is cached by content hash, so a repeating cycle costs nothing after the first lap)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # .../film  (the PROJ symlink target)
V3 = os.path.join(PROJ, 'v3')
for p in (os.path.join(V3, 'set3d12'), os.path.join(V3, 'cast12'), os.path.join(V3, 'cast10')):
    if p not in sys.path: sys.path.insert(0, p)
import bpy
from mathutils import Vector
import street as S
import cast12
S.T.ACT = os.path.join(HERE, 'actors_cache')                           # raster cache stays in the take folder (git-ignored)
os.makedirs(S.T.ACT, exist_ok=True)

RIM = '#f2b25c'

def g_of(t):  return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))

def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def mixu(u):                       # camera move parameter: no dead ends (0.35 sine + 0.65 linear)
    u = max(0.0, min(1.0, u)); return 0.35 * (0.5 - 0.5 * math.cos(math.pi * u)) + 0.65 * u

def cam_setup(preset, w):
    cs = S.CAMS[preset]; lerp = lambda a, b: tuple(x + (y - x) * w for x, y in zip(a, b))
    return dict(loc=lerp(cs['loc'], cs['loc_b']), look_at=lerp(cs['look_at'], cs['look_b']), lens=cs['lens'])

def set_cam(preset, w):
    s = cam_setup(preset, w); S.make_camera(s); bpy.context.view_layer.update()
    return bpy.context.scene.camera

def cam_pitch_deg(preset, w):
    s = cam_setup(preset, w); d = Vector(s['look_at']) - Vector(s['loc']); return math.degrees(math.atan2(-d.z, math.hypot(d.x, d.y)))

def drop(ob):
    if ob is None: return
    me = ob.data; mats = list(me.materials) if me else []
    bpy.data.objects.remove(ob, do_unlink=True)
    if me and me.users == 0: bpy.data.meshes.remove(me)
    for m in mats:
        if m and m.users == 0: bpy.data.materials.remove(m)

class Cards:
    """named dynamic cards: put(name, cast, pose, mark, tilt, ...) replaces the previous card of that name"""
    def __init__(self): self.d = {}; self.cache = {}
    def put(self, name, cast, pose, mark, face_to, tilt=0.0, mirror=False, over=None, rim=None, tint=None):
        drop(self.d.pop(name, None))
        ob = S.cast_card('actor_' + name, cast, pose, mark, face_to, tilt, mirror=mirror, over=over, rim=rim, tint=tint)
        ob.visible_glossy = True; self.d[name] = ob; return ob
    def clear(self):
        for k in list(self.d): drop(self.d.pop(k))

def story(name, over=None):
    cast, pose = cast12.STORY12[name]; pose = dict(pose)
    if over: pose.update(over)
    return cast, pose

def cyc(name, frame, facing=1, period=28.0):
    return cast12.cycle_frame(name, (frame / period) % 1.0, facing=facing)

def blinkpose(pose, g, period=90, off=0):
    p = dict(pose); p['blink'] = cast12.blink_at(g, period, off); return p
