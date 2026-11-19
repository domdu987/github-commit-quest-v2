"""c17.py -- helpers for film-17 take s12 (copy of the film8/common.py ideas on cast17 + set3d17/bertillon.py).
GOTCHAS: one location per process; key every animated hook every frame; cards need sync_all before each render."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17"), os.path.join(V3, "..", "v2", "shots")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                            # before sprites
import puppet
import bpy
from mathutils import Vector
import bertillon as K
import actors, camrig, sprites
from anim import ease, blink, lerp, clamp                # noqa

def g_of(t): return int(round((t + 0.10) * 30))
def ez(u, kind="sine"): return ease(clamp(u), kind)

# fake-beard dupont: same man, a big false beard
def register_fb():
    c = dict(puppet.CAST["dupont"]); c["beard17"] = dict(color="#c9c2b6", light="#e8e2d6"); puppet.CAST["dupont_fb"] = c
    sprites.DEFAULT_CANVAS["dupont_fb"] = sprites.DEFAULT_CANVAS["dupont"]
register_fb()

def fade_setup(a):
    """insert alpha * fade into the card material; returns the Math node (key inputs[1])."""
    nt = a.material.node_tree
    mix = [n for n in nt.nodes if n.type == "MIX_SHADER"][0]
    lk = [l for l in nt.links if l.to_node == mix and l.to_socket == mix.inputs[0]][0]
    m = nt.nodes.new("ShaderNodeMath"); m.operation = "MULTIPLY"; m.inputs[1].default_value = 1.0
    nt.links.new(lk.from_socket, m.inputs[0]); nt.links.new(m.outputs[0], mix.inputs[0]); return m

def key_fade(a, node, f, v):
    node.inputs[1].default_value = float(v); node.inputs[1].keyframe_insert("default_value", frame=f)
    for n in (a.contact,):
        if n is not None: n.hide_render = v < 0.5; n.keyframe_insert("hide_render", frame=f)

def make_actor(name, cast, who, sprite_dir, rim=True):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True); a.head_flip = True
    a.who = who; a.rim = rim; return a

def pose_of(story, expr=None, cast=None, rim=True, mirror=False):
    c, p = cast17.STORY17[story]; p = dict(p)
    if expr: p = cast17.with_expr(p, expr)
    p["seat17"] = None
    if mirror: p["mirror"] = True
    cc = cast or c
    r = K.RIM_FOR.get(c) if rim else None
    if r: p["rim"] = r; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
    return cc, p

def scale_of(who): return K.CAST_H[who] / K.CAST_HD[who]

def render_frames(scene, cam, frames, out_dir, mode, samples, key_cb=None):
    os.makedirs(out_dir, exist_ok=True); st = []
    K.setup_render(scene, mode, samples); scene.render.threads = int(os.environ.get("THREADS", "2"))
    for f in frames:
        path = os.path.join(out_dir, "g_%04d.png" % f)
        if os.path.exists(path): continue
        scene.frame_set(f); actors.sync_all(scene, cam)
        scene.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True); K.grade(path)
        st.append(time.time() - t); print("g %d %.1fs" % (f, st[-1]), flush=True)
    return st
