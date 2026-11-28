#!/usr/bin/env python3
"""shot.py -- film 25 row 57: "มันไม่ได้มีไว้ใส่น้ำ" g 1688-1723 (1724 exclusive), 56.27-57.47 s.
Insert: a plain galvanised water bucket by the trench lip with a drip falling from its rim (a drop falls with gravity every 14 frames and
splashes flat on the ground); behind it the tank crawls over the trench (set_crossing u 0.47 -> 0.53, links scrolling).  PUSH 12 %.
Mild DOF on the bucket.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F
bpy = C.bpy
G0, G1 = 1688, 1724
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_bucket"
B = (-5.2, -5.5)
DROPS = []


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.12 * T.smooth(k)
    gz = F.gh(*B)
    d = 7.5 / push
    cx = T.lerp(-1.0, -1.8, k)
    loc = (B[0] + 2.2 * (1 - 0.0) + (cx - -1.0) * 0.3, B[1] - d, gz + 1.2)
    look = (B[0] + 0.6, B[1], gz + 0.8)
    return loc, look, 32.0, (2.4, d)


def hooks(g, Tk):
    u = T.lerp(0.47, 0.53, min(max((g - 1682) / 48.0, 0.0), 1.0))
    Tk.TK.set_crossing(Tk.H, u)
    gz = F.gh(*B)
    for i, ob in enumerate(DROPS):                       # a drop every 14 frames, two phases
        t = ((g + i * 7) % 14) / 30.0
        z = gz + 0.75 - 0.5 * 18.5 * t * t
        if z <= gz + 0.02:
            ob.location = (B[0] + 0.5, B[1], gz + 0.02); ob.scale = (4.0, 4.0, 0.4)            # splash flat
            if t > 0.30:
                ob.hide_render = True
            else:
                ob.hide_render = False
        else:
            ob.location = (B[0] + 0.5, B[1], z); ob.scale = (1.5, 1.5, 2.2); ob.hide_render = False


def report(Tk, g):
    c = cam_of(g)
    return dict(cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_bucket", cards=[], cam=dict(loc=(-3.0, -12.0, 1.4), look_at=(-4.5, -5.5, 1.0), lens=32.0), dress_n=0.8, near=False,
               cross=dict(F._CR, u=0.5), tune=dict(green_k=1.2, cloud_k=0.95),
               world=dict(F.PRESETS["cross_bucket"].get("world", {}), crates=[], barrels=[]))
    Tk = T.Take(PRESET, cam_of, hooks)
    m = bpy.data.materials.new("drop"); m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (0.55, 0.75, 0.95, 1); bs.inputs["Roughness"].default_value = 0.05
    for i in range(2):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(B[0] + 0.5, B[1], F.gh(*B) + 0.75), segments=12, ring_count=8)
        ob = bpy.context.active_object; ob.data.materials.append(m); ob.name = "drip%d" % i; DROPS.append(ob)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
