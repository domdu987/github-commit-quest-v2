"""c21.py -- helpers of film-21 take s03 (copied from film8/common.py and switched to cast21 + set3d21/stirling.py).
Import FIRST in shot.py.  One location (bridge) per process; shot 8 (bridge_high) and shot 9 (bridge_end_south) run in separate processes."""
import math, os, sys, json
FILM = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.dirname(os.path.dirname(FILM)) if False else os.path.dirname(os.path.dirname(FILM))
V3 = os.path.dirname(os.path.dirname(FILM))                  # film/v3
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                              # noqa: E402  (BEFORE sprites)
import bpy                                                  # noqa: E402
from mathutils import Vector                                # noqa: E402
import stirling as K                                        # noqa: E402
import actors, camrig, sprites                              # noqa: E402

def g_of(t):  return int(round((t + 0.10) * 30))           # narration time -> film frame of an event
def bf(g):    return int(g) + 1                              # Blender frame (>= 1)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, u): return a + (b - a) * u
def ease(u):  u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def smooth(u): u = clamp(u); return u * u * (3 - 2 * u)
def blink(g, centres, w=3):
    return any(abs(g - c) <= w // 2 for c in centres)

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def hide_prefix(prefixes):
    n = 0
    for o in bpy.data.objects:
        if any(o.name.startswith(p) for p in prefixes): o.hide_render = True; n += 1
    return n

def key_cam(cam, g, loc, look, lens=22.0):
    camrig.key_camera(bf(g), Vector(loc), Vector(look), cam=cam, lens=lens, interp="LINEAR", easing="AUTO")

def make_actor(name, cast, sprite_dir, canvas=None, contact=True):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow="proxy")
    a.head_flip = False
    return a

def render_frame(g, out_png, mode="final", samples=24, threads=2):
    sc = bpy.context.scene; sc.frame_set(bf(g)); K.setup_render(sc, mode, samples); sc.render.threads = threads
    sc.cycles.denoising_prefilter = "FAST"
    return K.render(out_png, mode, samples)
