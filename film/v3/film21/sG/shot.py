#!/usr/bin/env python3
"""shot.py -- film 21 segment G (plan v3), g 1141..1238 (hard cut in at 1141, cut out at 1239; no handles).
Open behind the Scots on Abbey Craig (hill_over pose) looking down at the calm English column crossing the bridge (a knight on the causeway yawns), the camera ARCS
down and around to the LOW hero angle (hill_low) against the sky and the pine light shafts; on "เสียงแตร" (g 1194) the horn blower blows, Wallace lifts his sword arm, snap push
(14 f, x1.5) with a 2-frame shake.
    python3 shot.py path_draft            # 10 fps 360x640 path draft -> path_draft.mp4
    python3 shot.py frames a:b[:step] <out_dir> [draft|final] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
from c21 import K, cast21, lerp, clamp, sm, blink, bpy, Vector, np
S21 = cast21.STORY21
G0, G1 = 1141, 1239            # frames G0..G1-1
G_HORN = C.g_of(39.69)         # 1194
G_ARRIVE = 1186
PRESETS = ["hill_over", "hill_low"]

def u_lin(g, a, b): return (g - a) / float(b - a)

# ------------------------------------------------------------------ camera
def start_cam():
    ho = K.preset_pose("hill_over"); v = (np.array(ho[1][:2]) - np.array(ho[0][:2])); v = v / np.linalg.norm(v)
    c = np.array(ho[0][:2]) - v * 2.5
    return Vector((c[0], c[1], max(ho[0][2], float(K.ground(c[0], c[1])) + 3.0))), v

def base_path(g):
    hl = K.preset_pose("hill_low"); c0, v = start_cam()
    end_loc = hl[0]; end_look = (hl[1][0], hl[1][1], hl[1][2] + 3.0)
    fwd = Vector((v[0], v[1], 0))
    keys = [(G0, tuple(c0), (0.0, 14.0, 2.0), 72.0),
            (1154, tuple(c0 + fwd * 2.5 + Vector((0, 0, 0.3))), (0.0, 14.0, 2.0), 64.0),
            (1162, (159.0, 149.0, 53.0), (60.0, 60.0, 10.0), 40.0),
            (1171, (150.0, 137.0, 47.0), (134.0, 127.0, 23.0), 30.0),
            (1178, (131.0, 115.0, 24.0), (140.0, 132.0, 21.0), 25.0),
            (G_ARRIVE, end_loc, end_look, 22.0)]
    return K.cam_path(None, keys, min(g, G_ARRIVE))

TGT = [None]
def cam_for(g):
    r = base_path(g)
    cam = bpy.context.scene.camera
    loc = Vector(r["loc"]); look = Vector(r["look"]); lens = r["lens"]
    if g > G_ARRIVE:
        k = g - G_ARRIVE
        tgt = TGT[0]
        snap = C.sm(clamp((g - G_HORN) / 14.0))
        zoom = lerp(1.0, 1.5, snap) * (1.0 + 0.0035 * k)
        fwd = (tgt - loc).normalized(); right = Vector((fwd.y, -fwd.x, 0)).normalized()
        d = (tgt - loc).length
        loc = loc + fwd * (d * (1 - 1 / zoom)) + right * (0.006 * k)
        look = look + (tgt - look) * (0.85 * snap) + right * (0.006 * k)
    sh = 0.0
    if g in (G_HORN, G_HORN + 1):                       # 2-frame shake on the blast
        sh = 0.24 * (1 if g == G_HORN else -0.8)
    if sh:
        fwd = (look - loc).normalized(); right = Vector((fwd.y, -fwd.x, 0)).normalized()
        loc = loc + Vector((0, 0, sh)) + right * (sh * 0.6); look = look + Vector((0, 0, sh * 0.4))
    cam.location = loc; cam.rotation_euler = (look - loc).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
    return dict(loc=tuple(loc), look=tuple(look), lens=lens)

# ------------------------------------------------------------------ cast
def rim(p): return K.with_rim(p)

def setup(T):
    A = T.A; M1 = A["marks"]["hill_over"]; M2 = A["marks"]["hill_low"]; out = []
    # group 1: Scots on the ledge, three-quarter from behind (profile toward the bridge), spear shafts up
    g1 = [("s1", "scot_b", "scot_b_fold_spear"), ("s2", "scot_a", "scot_a_chew_grass"), ("s3", "scot_c", "scot_c_fold_spear"),
          ("s4", "scot_a_v1", "scot_a_fold_spear"), ("s5", "scot_b_v2", "scot_b_fold_spear")]
    for i, (nm, cst, pn) in enumerate(g1):
        x, y, z = M1[nm][:3]; _c, _v = start_cam(); x += _v[0] * 1.5; y += _v[1] * 1.5; z = float(K.ground(x, y))
        T.actor("o_" + nm, cst); out.append(("o_" + nm, cst, pn, (x, y, z), 1, i))
    g2 = [("s1", "scot_b", "scot_b_fold_spear"), ("s2", "scot_a", "scot_a_chew_grass"), ("horn", "scot_horn", "scot_horn_lower"),
          ("w", "wallace", "wallace_calm"), ("s3", "scot_c", "scot_c_fold_spear")]
    for i, (nm, cst, pn) in enumerate(g2):
        x, y, z = M2[nm][:3]; T.actor("l_" + nm, cst); out.append(("l_" + nm, cst, pn, (x, y, z), 2, 10 + i))
    mh, mw = M2["horn"], M2["w"]
    TGT[0] = Vector(((mh[0] + mw[0]) / 2, (mh[1] + mw[1]) / 2, (mh[2] + mw[2]) / 2 + 1.1))
    # causeway foot soldiers (x2 so the crowd reads from 230 m), marching north in threes
    rs2 = np.random.RandomState(5); cs = ["footman_a", "footman_b", "footman_a_v1", "footman_b_v2", "footman_a_v3", "footman_b_v1"]
    for i in range(12):
        row, col = divmod(i, 3); x = (-2.4, 0.2, 2.6)[col] + rs2.uniform(-0.4, 0.4); y = 40.5 + 2.6 * row + rs2.uniform(-0.4, 0.4)
        cst = cs[i % len(cs)]; T.actor("c_%d" % i, cst, scale=2.0 * C.TRUE_H["footman_a"] / C.CAST_H[cst.split("_v")[0]])
        out.append(("c_%d" % i, cst, cst.split("_v")[0] + "_stand", (x, y, float(K.ground(x, y))), 4, 50 + i))
    # the yawning knight on the causeway (true height, scaled x2.2 so it reads from 230 m)
    cx, cy = 1.2, 44.0
    T.actor("knight", "knight_a_open", scale=4.0 * C.TRUE_H["knight_a_open"] / C.CAST_H["knight_a_open"])
    out.append(("knight", "knight_a_open", "knight_a_open_yawn", (cx, cy, float(K.ground(cx, cy))), 3, 20))
    # more Scots behind the hero group: two ranks up the slope, a ragged line across the frame
    rs = np.random.RandomState(11); hl = K.preset_pose("hill_low"); cxy = np.array(hl[0][:2]); lk = np.array(hl[1][:2]); vv = (lk - cxy) / np.linalg.norm(lk - cxy); LL = np.array([-vv[1], vv[0]])
    types = ["scot_a", "scot_b", "scot_c", "scot_a_v1", "scot_b_v2", "scot_c_v1", "scot_a_v2"]
    poses = ["fold_spear", "stand_still", "fold_spear", "scratch_nose", "fold_spear"]
    n = 0
    for rank, (dist, cnt) in enumerate(((13.5, 7), (19.0, 8))):
        for j in range(cnt):
            lat = (j - (cnt - 1) / 2.0) * (3.1 if rank == 0 else 3.4) + rs.uniform(-0.8, 0.8)
            q = cxy + vv * (dist + rs.uniform(-1.0, 1.0)) + LL * lat
            cst = types[(n + rank) % len(types)]; base = cst.split("_v")[0]
            pn = base + "_" + poses[n % len(poses)]
            if pn not in S21: pn = base + "_fold_spear"
            T.actor("x_%d" % n, cst); out.append(("x_%d" % n, cst, pn, (q[0], q[1], float(K.ground(q[0], q[1]))), 2, 30 + n)); n += 1
    return out

def pose_of(nm, cst, pn, grp, i, g):
    p = dict(S21[pn][1])
    if grp == 1:
        p["yaw"] = 1.15 * (1 if i % 2 == 0 else -1) * 0.0 + 1.15      # profile toward the valley (screen-right = away from camera's left? profile reads as looking out)
        p["lean"] = 2 * math.sin(g * 0.09 + i)
        if "stalk21" in p and p["stalk21"]: p["stalk21"] = 1.0
    elif grp == 4:
        ph = (g * 0.034 + i * 0.27); p = cast21.walk_spear(cst.split("_v")[0], ph, 1 if i % 2 else -1, "march"); p["yaw"] = 0.3 * (1 if i % 2 else -1)
        if "_v" in cst: p["variant21"] = int(cst.split("_v")[1])
    elif nm == "l_horn":
        blow = sm(u_lin(g, G_HORN, G_HORN + 4)) if g >= G_HORN else 0.0
        if g >= G_HORN: p = dict(S21["scot_horn_blow"][1]); p["puff21"] = blow * (0.75 + 0.25 * math.sin(g * 0.9)); p["lean"] = 1.5 * math.sin(g * 0.4)
        else: p["lean"] = 1.5 * math.sin(g * 0.1)
    elif nm == "l_w":
        if g >= G_HORN + 6: p = dict(S21["wallace_raise_sword"][1])
        elif g >= G_HORN + 2: p = dict(S21["wallace_eyebrow"][1])
    elif nm == "knight":
        yw = sm(u_lin(g, 1144, 1148)) * (1 - sm(u_lin(g, 1158, 1161)))        # held about 14 frames
        p = dict(S21["knight_a_open_yawn"][1] if yw > 0.5 else S21["knight_a_open_stand_arms_down"][1])
        p["lean"] = 3 * yw + 1.2 * math.sin(g * 0.11)
    if grp != 3: p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(g * 0.13 + i * 2)
    p["blink"] = blink(g, 53 + 9 * (i % 6), 4 * i); p["t"] = g / 30.0
    return rim(p)

T_REF = [None]
def hooks(g):
    for o in getattr(T_REF[0], "col", []): o.location.y = 0.7 * (g - G0) / 30.0
    K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def column(T):
    """the English column on the bridge, two by two, about half over: pairs from the middle to the north end (3D riders), moving north slowly."""
    Bk = K.Batch(84); ys = [-4.0 + 3.9 * i for i in range(11)]
    K.knight_pair_column(Bk, ys, K.BRIDGE_X, np.random.RandomState(9), K.KNIGHT_MATS)
    return Bk.finalize('s08_column')

def build(mode, samples, cast=True):
    T = C.Take(None, mode, samples, world=PRESETS, fg=["hill_low"], over=dict(shaft_k=0.9))
    for o in bpy.data.objects:
        if o.name.startswith(("fg_generic_steel", "fg_generic_wood")): o.hide_render = True        # the spear that crossed the hero faces
    T.col = column(T)
    K.place_troops(T.A, "meadow", 18, seed=3)
    T_REF[0] = T
    items = setup(T) if cast else []
    M2 = T.A["marks"]["hill_low"]; mh, mw = M2["horn"], M2["w"]
    TGT[0] = Vector(((mh[0] + mw[0]) / 2, (mh[1] + mw[1]) / 2, (mh[2] + mw[2]) / 2 + 1.1))
    return T, items

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "path_draft":
        T, items = build("draft", 6, cast=False)
        out = os.path.join(HERE, "work", "path"); os.makedirs(out, exist_ok=True)
        for g in range(G0, G1, 3):
            cam_for(g); hooks(g); K.render(os.path.join(out, "p_%04d.png" % g), "draft", 6)
        os.system("ffmpeg -v error -y -framerate 10 -pattern_type glob -i '%s/p_*.png' -c:v libx264 -pix_fmt yuv420p %s/path_draft.mp4" % (out, HERE))
        print("path draft ok")
    else:
        gs = [g for g in parse(sys.argv[2]) if G0 <= g < G1]; out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else None
        T, items = build(mode, samples)
        for g in gs: cam_for(g)
        for g in gs:
            cam_for(g)
            for nm, cst, pn, (x, y, z), grp, i in items:
                f = g + 1; bob = 0.03 * abs(math.sin(g * 0.35 + i))
                T.place(nm, f, (x, y, z + (bob if nm == "l_horn" else 0)))
                T.pose(nm, f, pose_of(nm, cst, pn, grp, i, g))
        T.sprites_for([g + 1 for g in gs], ppd=160)
        os.makedirs(out, exist_ok=True)
        for g in gs:
            if os.path.exists(os.path.join(out, "g_%04d.png" % g)) and os.environ.get("RESUME"): continue
            def hk(f, g=g): cam_for(g); hooks(g)
            st = T.render([g + 1], out + "/raw", scale=1.0, hook=hk)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, "%.1fs" % st["wall"], flush=True)
