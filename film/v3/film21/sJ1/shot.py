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
G_TIP = C.g_of(55.80) + 1; G_SLAM = C.g_of(56.22)       # 1677, 1690
WHIP0 = G1 - 6                                       # 1703

def u_lin(g, a, b): return (g - a) / float(b - a)

def cam_for(g, A):
    mid = Vector((-13.75, -26.85, 0.0)); x = u_lin(g, G0, G1); u = 0.3 * sm(x) + 0.7 * x          # one monotone eased arc + push
    ang = math.radians(-9.0 + 15.0 * u)
    d = 4.3 - 0.7 * u                                       # push in about 8 %/s, table about 30 % of the frame height
    c = Vector((mid.x + d * math.sin(ang), mid.y - d * math.cos(ang), 1.6 - 0.05 * u))
    l = Vector((mid.x, mid.y, 2.05 + 0.1 * u))
    dd = l - c
    if g >= WHIP0:
        k = (g - WHIP0 + 1) / 6.0; a = math.radians(95.0 * k ** 2.2)
        dd = Vector((dd.x * math.cos(a) - dd.y * math.sin(a), dd.x * math.sin(a) + dd.y * math.cos(a), dd.z))
    cam = bpy.context.scene.camera; cam.location = c
    cam.rotation_euler = dd.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 22.0
    K.STATE["vivid"] = K.VIVID.get("camp_table", (1.05, 1.1))
    return dict(loc=tuple(c), look=tuple(c + dd))

def scale_deg(g):
    if g < G_TIP: return 0.0 + 0.5 * math.sin(g * 0.3)            # idle quiver
    k = g - G_TIP
    return 15.0 * (1 - math.exp(-k / 3.0) * math.cos(k * 0.55))

def lid_deg(g):
    if g < G_SLAM: return 72.0 + 1.5 * math.sin(g * 0.2)
    k = g - G_SLAM
    if k < 3: return 72.0 * (1 - (k + 1) / 3.0) ** 2
    return max(0.0, 5.0 * math.exp(-(k - 3) / 2.0) * math.sin((k - 3) * 1.4)) if k < 10 else 0.0

def dress(A):
    """the table's own props: the scale moved to the middle third with coins in the pans, a rug and floor props, and a stool with Cressingham's cloak in clear view."""
    tx, ty, tz = A["camp"]["table"]
    for o in bpy.data.objects:
        if o.name.startswith(("scale_beam", "scale_stand")): o.location.x += -1.05
    bpy.context.view_layer.update()
    steel = bpy.data.objects["scale_beam_steel"]
    bb = [steel.matrix_world @ Vector(v) for v in steel.bound_box]
    x0 = min(p.x for p in bb); x1 = max(p.x for p in bb); yc = sum(p.y for p in bb) / 8.0; zt = max(p.z for p in bb)
    B = K.Batch(131)
    for sx_, n in ((x0 + 0.17, 1), (x1 - 0.17, 5)):                    # right pan heavy
        for i in range(n): B.cyl('gold', (sx_ + 0.03 * (i % 2), yc + 0.03 * (i // 2), zt + 0.02 + 0.022 * i), 0.075, 0.02, seg=10)
    coins = B.finalize('s08_pancoins', ink=False, shadow=False)
    for o in coins:
        o.parent = steel; o.matrix_parent_inverse = steel.matrix_world.inverted()
    R = K.Batch(132)
    # rug in front of the table (crimson, gold border) so the ground is warm
    R.box('cloth_red', (tx - 0.4, ty - 3.0, tz + 0.015), (4.6, 4.4, 0.03)); R.box('gold', (tx - 0.4, ty - 5.18, tz + 0.03), (4.6, 0.07, 0.01)); R.box('gold', (tx - 0.4, ty - 0.82, tz + 0.03), (4.6, 0.07, 0.01))
    for sg in (-1, 1): R.box('gold', (tx - 0.4 + sg * 2.28, ty - 3.0, tz + 0.03), (0.07, 4.4, 0.01))
    for k in range(5): R.box('t_gold', (tx - 2.2 + 1.0 * k, ty - 3.0, tz + 0.032), (0.22, 3.6, 0.005))
    # stool with the cloak, front left, in clear view
    sx, sy = tx - 1.7, ty - 1.5
    R.box('wood', (sx, sy, tz + 0.56), (0.55, 0.45, 0.07))
    for ox in (-0.22, 0.22):
        for oy in (-0.18, 0.18): R.rod('wood', (sx + ox, sy + oy, tz + 0.03), (sx + ox * 0.9, sy + oy * 0.9, tz + 0.55), 0.035, seg=5)
    R.box('wood_dk', (sx, sy + 0.2, tz + 0.88), (0.55, 0.05, 0.5)); R.box('cloth_red', (sx, sy + 0.0, tz + 0.64), (0.62, 0.52, 0.1)); R.box('cloth_red', (sx - 0.01, sy + 0.26, tz + 0.78), (0.62, 0.08, 0.62))
    R.box('gold', (sx, sy - 0.02, tz + 0.7), (0.64, 0.03, 0.04)); R.box('gold', (sx, sy + 0.3, tz + 0.5), (0.64, 0.02, 0.04))
    # floor props: coin sacks, crate, scattered coins, a ledger and a toppled cup
    for (px, py) in ((tx + 1.3, ty - 1.7), (tx + 1.55, ty - 1.45)): R.cyl('sack', (px, py, tz + 0.2), 0.2, 0.4, seg=8, r2=0.14)
    R.box('wood_dk', (tx - 0.3, ty - 3.3, tz + 0.2), (0.55, 0.4, 0.4)); R.box('iron', (tx - 0.3, ty - 3.3, tz + 0.41), (0.57, 0.42, 0.03))
    rs = np.random.RandomState(4)
    for i in range(11): R.cyl('gold', (tx + rs.uniform(-1.4, 1.2), ty - rs.uniform(1.6, 3.2), tz + 0.045), 0.07, 0.015, seg=10)
    R.box('t_cream', (tx + 0.6, ty - 2.3, tz + 0.05), (0.3, 0.22, 0.05)); R.cyl('iron', (tx + 0.1, ty - 1.9, tz + 0.07), 0.07, 0.12, axis='x', seg=8)
    R.finalize('s08_dress')
    ld = bpy.data.lights.new('s08_warm', 'POINT'); ld.energy = 450.0; ld.color = (1.0, 0.66, 0.36); ld.shadow_soft_size = 0.6
    lo = bpy.data.objects.new('s08_warm', ld); bpy.context.scene.collection.objects.link(lo); lo.location = (tx - 0.2, ty - 2.6, tz + 1.9)

def hooks(g, A):
    t = g / 30.0
    K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
    K.set_scale_tip(A, scale_deg(g)); K.set_chest_lid(A, lid_deg(g))
    b = bpy.data.objects["scale_beam_gold"]
    for nm in ("scale_beam_rope", "scale_beam_steel"):
        o = bpy.data.objects.get(nm)
        if o: o.rotation_euler = b.rotation_euler
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
        if o.name.startswith(("table_extras_t_cream", "table_extras_t_gold")): o.hide_render = True              # rug stripes
    A = T.A; dress(A)
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
