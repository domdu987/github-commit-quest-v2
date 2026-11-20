#!/usr/bin/env python3
"""segment H2b (BIGZOOM 2), g 1392-1519 (+3 handle before, +3 after): P_TOP -> swoop -> medium of Cressingham + Surrey -> CU3 push.
python3 sh2b.py <draft|final> <g spec> [samples]"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21
from c21 import *
G0, G1 = 1392, 1519
S = cast21.STORY21
M = {"cressingham": 0.551, "surrey": 0.519, "footman_a": 0.553, "footman_b": 0.553, "knight_b": 0.526}
def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    return out

# ---- stage (south bank, west of the bridge). 3/4 two-shot: the camera looks NE (az 50), the trap (river, blue wall, crimson block) is in the background at the right
C = np.array([-92.0, -13.0]); AZ = math.radians(50.0); VIEW = np.array([math.cos(AZ), math.sin(AZ)]); RV = np.array([math.sin(AZ), -math.cos(AZ)])
def gz(x, y): return float(K.ground(x, y))
CRESS = C; SURREY = C + RV * 0.65 + VIEW * 2.0
def at(base, along, lat): return base + VIEW * along + RV * lat
CAM_M = at(C, -4.4, -0.3); CAM_E = at(C, -2.4, -0.1); CAM_E2 = at(C, -2.15, -0.1)
def cam3(p, h): return (float(p[0]), float(p[1]), gz(p[0], p[1]) + h)
def keys():
    zc = gz(*C)
    mid = (CRESS + SURREY) / 2
    lk_m = at(mid, 3.0, 0.0)
    return [
        (1392, 'P_TOP'),
        (1422, (-14.0, -111.0, 109.0), (2.0, 66.0, 0.0), 22.0),
        (1446, (-52.0, -84.0, 46.0), (-82.0, -30.0, 2.0), 22.0),
        (1464, (-77.0, -60.0, 13.0), (-86.0, -16.0, 2.5), 24.0),
        (1479, (-86.0, -34.0, 5.0), (-89.0, -10.0, 2.5), 26.0),
        (1495, cam3(CAM_M, 1.5), (float(lk_m[0]), float(lk_m[1]), zc + 2.7), 26.0),
        (1519, cam3(CAM_E, 1.55), (float(at(C, 1.0, 0.0)[0]), float(at(C, 1.0, 0.0)[1]), zc + 1.75), 26.0),
        (1530, cam3(CAM_E2, 1.57), (float(at(C, 1.0, 0.0)[0]), float(at(C, 1.0, 0.0)[1]), zc + 1.78), 26.0),
    ]

def story_colours(rs):
    """cork image (QA: team 3 H2a): English in the loop + on the south bank solid CRIMSON, packed tight; the Scots wall 5 ranks BLUE with big saltire banners."""
    K.PH_COL['crimson'] = '#c4202c'; K.PH_COL['saltire'] = '#2456c8'
    for o in list(bpy.data.objects):
        if (o.name.startswith('crowd') and o.name not in ('crowd_banners', 'crowd_horses')) or o.name.startswith(('spear_wall', 'wall_banners')):
            bpy.data.objects.remove(o, do_unlink=True)
    items = []
    for r in range(11):
        for c in range(17):
            x = -19 + c * 2.35 + rs.uniform(-0.35, 0.35) + (1.2 if r % 2 else 0); y = 36 + r * 3.0 + rs.uniform(-0.35, 0.35)
            if math.hypot(x - K.LOOP_C[0], y - K.LOOP_C[1]) < K.LOOP_R - 20 and float(K.sd_at(x, y)) > 3: items.append((x, y, float(K.ground(x, y)), 'crimson', 1.0))
    for i in range(30):
        x = rs.uniform(-70, -20) if i % 2 else rs.uniform(20, 70); y = float(K.bank_y(x)) - rs.uniform(4, 26); items.append((x, y, float(K.ground(x, y)), 'crimson', 1.0))
    for i in range(24):
        y = -36 - i * 2.4; x = (-1.2 if i % 2 else 1.2) + rs.uniform(-0.3, 0.3); items.append((x, y, float(K.ground(x, y)), 'crimson', 1.0))
    K.stage_crowd(items)
    # the Scots wall: 5 ranks across the neck, spears level, blue
    sc = []; Bs = K.Batch(83)
    for rank in range(5):
        for k in range(16):
            x = -9 + 18 * k / 15.0 + (0.5 if rank % 2 else 0); y = 27.0 + 1.1 * rank; z = float(K.ground(x, y)); sc.append((x, y, z, 'saltire', 1.0))
            K.spear(Bs, (x, y - 0.4, z), tilt=(0.0, -0.9), h=2.4)
    Bs.finalize('spear_wall', ink=False)
    K.stage_crowd(sc)
    Bp = K.Batch(87)
    for sx, yy in ((-10.5, 26.5), (-6.0, 25.5), (-2.0, 25.0), (2.0, 25.0), (6.0, 25.5), (10.5, 26.5)):
        K.banner(Bp, (sx, yy, float(K.ground(sx, yy))), 11.0, 190, 't_saltire', 't_white', 'saltire', rs, size=(7.0, 4.7))
    Bp.finalize('wall_banners')

YAW = 0.7
def blink(g, off=0, period=67): return 1.0 if (g + off) % period in (0, 1) else 0.0

# stand points (world xy) of the other English: 2nd rank behind and to the sides, fully inside the frame at the medium shot
def extra_positions():
    out = []
    for (d, lat, who, cast) in [(4.0, -1.7, "footman_a", "a"), (5.0, 2.3, "footman_b", "b"), (7.0, -0.2, "footman_a", "c"), (6.0, -3.2, "knight_b", "d"), (9.0, 3.0, "footman_b", "e")]:
        out.append((at(C, d, lat), who, cast))
    return out

def hide_near_path(kk, radius=15.0):
    """hide every banner part (objects flag_*) whose bbox centre is within `radius` m (horizontal) of the camera path below 70 m height"""
    from mathutils import Vector
    bpy.context.view_layer.update()
    pts = []
    for g in range(1392, 1523, 3):
        r = K.cam_path(None, kk, g)
        if r['loc'][2] < 70: pts.append(np.array(r['loc'][:2]))
    n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.name.startswith(('flag_', 'pole_')): continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; c = sum(bb, Vector()) / 8
        if min(np.hypot(c.x - p[0], c.y - p[1]) for p in pts) < radius: o.hide_render = True; n += 1
    print("hidden banner parts:", n, flush=True)

def main(quality, gs, samples):
    T = Take.world(['valley_loop', 'camp_bank'], quality, samples, fg=['valley_loop'])
    rs = np.random.RandomState(4); story_colours(rs)
    # foreground dressing (world-fixed): a barrel left of the pair, reed clumps and a gorse bush low at the bottom edge between camera and pair (the camera passes between them)
    Bf = K.Batch(96); Bg = K.Batch(97)
    pb = at(C, -1.0, -1.7); K.barrel(Bf, (float(pb[0]), float(pb[1]), gz(*pb)), rs=rs)
    for (al, la) in [(-3.2, -1.5), (-3.0, 1.6), (-2.2, 2.4), (-3.6, 0.2), (-1.6, -2.4)]:
        pr_ = at(C, al, la)
        for j in range(3): K.reed_cluster(Bg, (float(pr_[0] + rs.uniform(-.25, .25)), float(pr_[1] + rs.uniform(-.25, .25)), gz(*pr_)), rs)
    K.gorse(Bg, (float(at(C, -2.6, -1.0)[0]), float(at(C, -2.6, -1.0)[1]), gz(*at(C, -2.6, -1.0))), 0.55, rs)
    Bf.finalize('fg_h2b'); Bg.finalize('fg_h2b_g', ink=False)
    # crimson/gold banners at the loop edge so the trapped English read at P_TOP
    Bl = K.Batch(98)
    for i, (x, y) in enumerate([(-30, 44), (30, 44), (-36, 78), (36, 78), (0, 100)]):
        K.banner(Bl, (x, y, float(K.ground(x, y))), 13.0, 20 + 30 * i, 't_red', 't_gold', ['chevron', 'lion'][i % 2], rs, size=(7.0, 4.6))
    Bl.finalize('loop_banners', shadow=False)
    bpy.context.view_layer.update()
    from mathutils import Vector
    south_flags = []
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith('flag_'):
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; c_ = sum(bb, Vector()) / 8
            if c_.y < -10: south_flags.append(o)
    print("south-bank banner parts:", len(south_flags), flush=True)
    def wide(cast):
        c = sprites.DEFAULT_CANVAS[cast]; return (c[0] - 0.8125, c[1] - 0.5, c[2] + 0.8125, c[3])
    cres = T.actor("cress", "cressingham", wide("cressingham")); surr = T.actor("surrey", "surrey", wide("surrey"))
    ex = []
    for i, (p, who, tag) in enumerate(extra_positions()):
        cast = "footman_a" if who == "footman_a" else "footman_b" if who == "footman_b" else "knight_b"
        ex.append((T.actor("e_" + tag, cast, wide(cast)), p, cast, i))
    kk = keys()
    path = lambda g: K.cam_path(None, kk, g)
    for g in gs:
        f = g + 1
        path(g)
        T.scene.frame_set(f)
        T.cam.data.lens = T.cam.data.lens
        shock = g >= 1488
        # Cressingham
        cres.place(f, (float(CRESS[0]), float(CRESS[1]), gz(*CRESS)), scale=M["cressingham"])
        base = S["cressingham_shocked" if shock else "cressingham_sweating"][1]
        p = dict(base); p["blink"] = blink(g, 9) if not (1486 <= g <= 1487) else 1.0
        if g < 1486: p["expr"] = "worried"; p["fx"] = ["sweat"]
        p["head_roll"] = 2.5 * math.sin(g * 0.21); p["lean"] = 1.5 * math.sin(g * 0.17); p["yaw"] = YAW
        cres.pose(f, K.with_rim(p), camera=T.cam)
        surr.place(f, (float(SURREY[0]), float(SURREY[1]), gz(*SURREY)), scale=M["surrey"])
        base = S["surrey_shocked" if g >= 1490 else "surrey_worried"][1]
        p = dict(base); p["blink"] = 1.0 if 1488 <= g <= 1489 else blink(g, 31)
        p["head_roll"] = 3 * math.sin(g * 0.19 + 1); p["yaw"] = YAW
        surr.pose(f, K.with_rim(p), camera=T.cam)
        for a, pxy, cast, i in ex:
            ph = i * 1.3
            tip = 0.18 * (0.5 + 0.5 * math.sin(g * 2 * math.pi / 14.0 + ph))     # tiptoe bobbing, about 2 Hz
            a.place(f, (float(pxy[0]), float(pxy[1]), gz(*pxy) + tip * M[cast] * 1.0), scale=M[cast])
            nm = cast + ("_tiptoe" if cast != "knight_b" else "_worried")
            p = dict(S[nm][1])
            if shock and (i % 2 == 0): p = dict(S[cast + "_shocked"][1])
            p["blink"] = blink(g, 13 * i + 5); p["head_roll"] = 4 * math.sin(g * 0.23 + ph); p["yaw"] = 0.45
            a.pose(f, K.with_rim(p), camera=T.cam)
    T.sprites_for(dict(default=256, cress=384, surrey=384))
    out = os.path.join(HERE, "raw", "h2b_" + quality); os.makedirs(out, exist_ok=True)
    for g in gs:
        r = path(g)
        for o in bpy.data.objects:
            if o.name == 'crowd_banners': o.hide_render = g >= 1436
        for o in south_flags: o.hide_render = g >= 1426
        for o in bpy.data.objects:
            pass
        K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0)
        dt = T.render(g + 1, os.path.join(out, "g_%04d.png" % g))
        print("g", g, "%.1fs" % dt, "cam", [round(v, 1) for v in r['loc']], flush=True)

if __name__ == "__main__":
    main(sys.argv[1], parse(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
