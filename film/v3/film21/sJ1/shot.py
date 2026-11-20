#!/usr/bin/env python3
"""shot.py -- film 21 segment J1 (plan v3), g 1640..1708 (CUT in, whip pan left out; no handles): the ENDING table, EMPTY (Cressingham is not staged).
Stool with his cloak, the "KING'S TREASURY" chest, the lantern. The camera pushes in; the coin scale TIPS on "เร็วดี" (g 1677) and the chest lid SLAMS on "ประหยัดดี" (g 1690);
the last 6 frames whip pan left.
    python3 shot.py path_draft | frames a:b[:step] <out_dir> [draft|final] [samples]"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
from c21 import K, lerp, clamp, sm, bpy, Vector, np
G0, G1 = 1640, 1709
G_TIP = C.g_of(55.80); G_SLAM = C.g_of(56.22)       # 1677, 1690
WHIP0 = G1 - 6                                       # 1703

def u_lin(g, a, b): return (g - a) / float(b - a)

def cam_for(g, A):
    pr = K.PRESETS["camp_table"]; c0 = Vector(K.preset_pose("camp_table")[0]); l0 = Vector(K.preset_pose("camp_table")[1])
    tx, ty, tz = A["camp"]["table"]
    t = (g - G0) / 30.0; x = u_lin(g, G0, G1)
    # start a little off to the right and higher, push in 8 %/s with a lateral slide (arc) toward the chest
    fwd = (l0 - c0); fwd.z = 0; fwd.normalize(); right = Vector((fwd.y, -fwd.x, 0))
    u = 0.3 * sm(x) + 0.7 * x
    c = c0 + Vector((0, 0, 0.35 * (1 - u))) - fwd * 0.55 + fwd * (1.0 * u * 1.0) + right * (0.55 - 1.1 * u)
    l = l0 + Vector((0, 0, -0.15 * u)) + right * (0.2 - 0.5 * u)
    d = l - c; yaw = 0.0
    if g >= WHIP0:
        k = (g - WHIP0 + 1) / 6.0
        yaw = 95.0 * k ** 2.2                          # accelerating pan to the left
    a = math.radians(yaw)
    d = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), d.z))
    cam = bpy.context.scene.camera; cam.location = c
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 22.0
    K.STATE["vivid"] = K.VIVID.get("camp_table", (1.05, 1.1))
    return dict(loc=tuple(c), look=tuple(c + d))

def scale_deg(g):
    if g < G_TIP: return 0.0 + 0.6 * math.sin(g * 0.3)            # idle quiver
    k = g - G_TIP
    return 15.0 * (1 - math.exp(-k / 3.0) * math.cos(k * 0.55))

def lid_deg(g):
    if g < G_SLAM: return 72.0 + 1.5 * math.sin(g * 0.2)
    k = g - G_SLAM
    if k < 3: return 72.0 * (1 - (k + 1) / 3.0) ** 2
    return max(0.0, 5.0 * math.exp(-(k - 3) / 2.0) * math.sin((k - 3) * 1.4)) if k < 10 else 0.0

def hooks(g, A):
    t = g / 30.0
    K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
    K.set_scale_tip(A, scale_deg(g)); K.set_chest_lid(A, lid_deg(g))
    L = bpy.data.objects.get("lantern")
    if L and L.type == "LIGHT": L.data.energy = 140.0 * (1.0 + 0.09 * math.sin(g * 0.9) + 0.05 * math.sin(g * 2.3))
    G = bpy.data.objects.get("lantern_glow")
    if G: G.scale = (1 + 0.06 * math.sin(g * 1.1),) * 3

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

if __name__ == "__main__":
    cmd = sys.argv[1]
    mode = "draft" if cmd == "path_draft" else (sys.argv[4] if len(sys.argv) > 4 else "draft")
    samples = 6 if cmd == "path_draft" else (int(sys.argv[5]) if len(sys.argv) > 5 else None)
    T = C.Take("camp_table", mode, samples, world=["camp_table"])
    for o in bpy.data.objects:
        if o.name.startswith("table_extras_t_cream"): o.hide_render = True              # rug stripes
    A = T.A
    if cmd == "path_draft":
        out = os.path.join(HERE, "work", "path"); os.makedirs(out, exist_ok=True)
        for g in range(G0, G1, 3):
            cam_for(g, A); hooks(g, A); K.render(os.path.join(out, "p_%04d.png" % g), "draft", 6)
        os.system("ffmpeg -v error -y -framerate 10 -pattern_type glob -i '%s/p_*.png' -c:v libx264 -pix_fmt yuv420p %s/path_draft.mp4" % (out, HERE)); print("ok")
    else:
        gs = [g for g in parse(sys.argv[2]) if G0 <= g < G1]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        for g in gs:
            if os.path.exists(os.path.join(out, "g_%04d.png" % g)) and os.environ.get("RESUME"): continue
            def hk(f, g=g): cam_for(g, A); hooks(g, A)
            st = T.render([g + 1], out + "/raw", scale=1.0, hook=hk)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, "%.1fs" % st["wall"], flush=True)
