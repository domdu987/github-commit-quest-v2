#!/usr/bin/env python3
"""shot.py -- film 21 take s08: shots 20-22 (g 1141..1294, handles 1135..1140 and 1295..1300).
 20 g1141-1193 bridge_end_north: calm before, the column crossing, a knight yawns.
 21 g1194-1238 hill_low: the horn blower blows, Wallace lifts his sword, snap push.
 22 g1239-1294 hill_over: whip in, the Scots run down the slope, the lens rides down behind them.
One location/preset per process:  python3 shot.py <shot> stills|final a:b[:step] [out_dir] [mode] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
from c21 import K, cast21, lerp, clamp, sm, blink, bpy, Vector, np
S21 = cast21.STORY21

G0, G1, H = 1141, 1295, 6
CUT20, CUT21, CUT22 = 1141, 1194, 1239
RANGE = {20: (G0 - H, CUT21 - 1), 21: (CUT21, CUT22 - 1), 22: (CUT22, G1 + H - 1)}
PRESET = {20: "bridge_end_north", 21: "hill_low", 22: "hill_over"}

COL = []
def u_lin(g, a, b): return (g - a) / float(b - a)
def ease_mix(x): return 0.3 * sm(x) + 0.7 * x          # mostly linear: never dead ends

def aim_pt(loc, look, back): pass

# ------------------------------------------------------------------ shot 20
def cam20(g):
    x = u_lin(g, CUT20, CUT21)                           # 0..1 over the shot (extrapolated in the handle)
    u = ease_mix(clamp(x, -0.2, 1.0)) if x < 0 else ease_mix(x)
    c0 = Vector((-2.0, 50.0, 2.5)); l0 = Vector((0.0, 22.0, 2.3))
    fwd = (l0 - c0).normalized()
    right = Vector((fwd.y, -fwd.x, 0)).normalized()
    push = 0.115 * 2.4                                   # ~7 %/s of the 1.77 s shot -> ~12 % of the distance
    slide = 1.1 * u                                      # m, ~45 px/s at 10 m
    c = c0 + fwd * (push * 8.0 * u) + right * slide
    l = l0 + right * (slide * 1.0) + Vector((0, 0, 0.0))
    sway = 0.05 * math.sin(g * 0.21)
    return c + Vector((0, 0, sway)), l

def setup20(T):
    A = T.A; m = A['marks']
    got = []
    K.place_troops(A, 'causeway', 14, seed=3, cb=lambda it: got.extend(it))      # real cast cards instead of the placeholder crowd
    for o in [o for o in bpy.data.objects if o.name.startswith('troops_causeway')]: o.hide_render = True
    T.col = column(T)
    out = []
    x, y, z = m["e2"][:3]
    T.actor("a_yawn", "knight_a_open"); out.append(("a_yawn", "knight_a_open", 99, (-1.2, 40.8, float(K.ground(-1.2, 40.8)))))
    cs = ["footman_a", "footman_b", "footman_a_v1", "footman_b_v2", "footman_a_v3", "footman_b_v1", "footman_a_v2"]
    rs = np.random.RandomState(5)
    for i in range(14):
        row, col = divmod(i, 3)
        x = (-2.6, 0.2, 2.8)[col] + rs.uniform(-0.4, 0.4) + (0.7 if row % 2 else 0); y = 41.4 - 1.5 * row + rs.uniform(-0.3, 0.3)
        cst = cs[i % len(cs)]; T.actor("a_t%d" % i, cst); out.append(("a_t%d" % i, cst, i, (x, y, float(K.ground(x, y)))))
    return out

def column(T):
    for o in [o for o in bpy.data.objects if o.name.startswith('troops_bridge')]: o.hide_render = True
    Bk = K.Batch(84); ys = [-4.0 + 5.4 * i for i in range(8)]
    K.knight_pair_column(Bk, ys, K.BRIDGE_X, np.random.RandomState(9), K.KNIGHT_MATS)
    return Bk.finalize('s08_column')

def pose20(T, items, g):
    for nm, cst, i, (x, y, z) in items:
        f = g + 1
        ph = (g * 0.034 + i * 0.27)
        bob = 0.03 * abs(math.sin(ph * 2 * math.pi)) if i != 99 else 0.0
        T.place(nm, f, (x, y, z + bob))
        base = cst.split("_v")[0]
        if i == 99:
            yw = sm(u_lin(g, 1146, 1154)) * (1 - sm(u_lin(g, 1176, 1184)))
            p = dict(S21["knight_a_open_yawn"][1] if yw > 0.5 else S21["knight_a_open_stand_arms_down"][1])
            p["lean"] = 1.2 * math.sin(g * 0.11) + 3 * yw
        else:
            fc = 1 if i % 2 else -1
            p = cast21.walk_spear(base, ph, fc, "march"); p["yaw"] = 0.3 * fc
            p["prop_r"] = dict(p.get("prop_r", {}))
            if "_v" in cst: p["variant21"] = int(cst.split("_v")[1])
        p["blink"] = blink(g, 61 + 7 * (i % 5), 5 * (i % 7))
        p["t"] = g / 30.0
        T.pose(nm, f, p)

def hook(g):
    if COL: 
        for o in COL: o.location.y = 0.9 * (g - 1141) / 30.0 * 2.0

    K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)


# ------------------------------------------------------------------ shot 21
WHIP_OFF = (1235, 1238)        # shot 21's last 4 frames pan away (whip off); shot 22 starts on the whip on (7 frames)
def yaw_about(loc, look, deg):
    v = look - loc; a = math.radians(deg); c, s_ = math.cos(a), math.sin(a)
    return loc + Vector((v.x * c - v.y * s_, v.x * s_ + v.y * c, v.z))

def whip_off_deg(g):                       # 0 .. 48 deg to the right (negative yaw = clockwise = right) over 4 frames, accelerating
    return 0.0 if g < WHIP_OFF[0] else -48.0 * ((g - WHIP_OFF[0] + 1) / 4.0) ** 2

TGT21 = Vector((0, 0, 0))
def cam21(g):
    pr = K.PRESETS["hill_low"]
    c0 = Vector(pr["cam"]); l0 = Vector(pr["look"]) + Vector((0, 0, 3.4))
    tgt = TGT21                                                            # horn blower / Wallace midpoint, chest height
    t = (g - CUT21) / 30.0
    snap = sm(clamp((g - CUT21) / 14.0))                                   # 14-frame snap push x1.5
    k = lerp(1.0, 1.0 / 1.4, ease_mix(snap)) * (1 + 0.0 * t)
    drift = 1.0 - 0.07 * t * 0.0                                           # gentle push on after the snap (below)
    c = tgt + (c0 - tgt) * k
    right = Vector((0.7, -0.7, 0)); c = c + right * (0.9 * t) + (tgt - c).normalized() * (0.45 * t)
    l = l0 + (tgt + Vector((0, 0, 0.5)) - l0) * 0.0 + right * (0.9 * t)
    if 1207 <= g <= 1208:                                                    # 2-frame shake on the landing
        sh = 0.18 * (1 if g == 1207 else -0.7); c = c + Vector((0, 0, sh)) + right * sh * 0.5
    lo = yaw_about(c, l, whip_off_deg(g))
    return c, lo

def setup21(T):
    A = T.A; m = A["marks"]; out = []
    spec = [("s1", "scot_b", "scot_b_fold_spear"), ("s2", "scot_a", "scot_a_chew_grass"), ("horn", "scot_horn", "scot_horn_blow"),
            ("w", "wallace", "wallace_calm"), ("s3", "scot_c", "scot_c_fold_spear")]
    for nm, cst, pn in spec:
        x, y, z = m[nm][:3]; T.actor("a_" + nm, cst); out.append((nm, cst, pn, (x, y, z)))
    mh, mw = m['horn'], m['w']
    TGT21[:] = Vector(((mh[0] + mw[0]) / 2, (mh[1] + mw[1]) / 2, (mh[2] + mw[2]) / 2 + 1.5))
    return out

def pose21(T, items, g):
    for i, (nm, cst, pn, (x, y, z)) in enumerate(items):
        f = g + 1
        bob = 0.0
        p = dict(S21[pn][1])
        if nm == "horn":
            blow = sm(u_lin(g, 1194, 1198))
            p["puff21"] = blow * (0.75 + 0.25 * math.sin(g * 0.9))
            p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.4)
            T.place("a_" + nm, f, (x, y, z + 0.03 * abs(math.sin(g * 0.45))))
        elif nm == "w":
            if g >= 1200: p = dict(S21["wallace_raise_sword"][1])
            elif g >= 1196: p = dict(S21["wallace_eyebrow"][1])
            T.place("a_" + nm, f, (x, y, z))
        else:
            T.place("a_" + nm, f, (x, y, z))
            p["lean"] = p.get("lean", 0) + 2 * math.sin(g * 0.1 + i)
        p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(g * 0.13 + i * 2)
        p["blink"] = blink(g, 53 + 9 * i, 4 * i); p["t"] = g / 30.0
        T.pose("a_" + nm, f, p)


# ------------------------------------------------------------------ shot 22
SPEED_RUN = 0.13            # m per frame (about 5 m/s)
RUN_START = {}
def run_dir():
    pr = K.PRESETS["hill_over"]; c = np.array(pr["cam"][:2]); l = np.array(pr["look"][:2]); v = (l - c) / np.linalg.norm(l - c)
    return v, v

def whip_on_deg(g):          # 7 frames: from 48 deg left of the target settling to 0 (ease out)
    if g >= CUT22 + 7: return 0.0
    u = (g - CUT22) / 7.0
    return 48.0 * (1 - u) ** 2

def shake22(g):
    t = (g - CUT22) / 30.0
    if t < 0: return 0.0, 0.0
    a = 0.55 * math.exp(-t / 0.45); return a * math.sin(2 * math.pi * 5 * t), a * 0.7 * math.cos(2 * math.pi * 5 * t)

RUNNERS = []     # (fwd distance m from the preset camera, lateral m, speed factor)
def gsm(x, y, rad=1.6):
    pts = [(0, 0)] + [(rad * math.cos(a), rad * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 8, endpoint=False)]
    return float(np.mean([K.ground(x + p, y + q) for p, q in pts]))

def runner_xy(i, g):
    v, r = run_dir(); d0, lat, sp = RUNNERS[i]; t = (g - CUT22) / 30.0
    c = np.array(K.PRESETS["hill_over"]["cam"][:2]); L = np.array([-r[1], r[0]])
    d = d0 + 5.2 * sp * t
    return c[0] + r[0] * d + L[0] * lat, c[1] + r[1] * d + L[1] * lat

def cam22(g):
    v, r = run_dir(); pr = K.PRESETS["hill_over"]; k = g - CUT22
    pts = [runner_xy(i, g) for i in range(len(RUNNERS))]
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    behind = 8.5
    fx, fy = cx - r[0] * behind, cy - r[1] * behind
    fc = Vector((fx, fy, gsm(fx, fy) + 2.6 + 3.6 * math.sin(math.pi * clamp(k / 50.0))))
    fl = Vector((cx + r[0] * 1.0, cy + r[1] * 1.0, gsm(cx, cy) + 1.0))
    c0 = Vector(pr["cam"]); l0 = Vector(pr["look"])
    w = sm(k / 12.0)
    c = c0.lerp(fc, w); l = l0.lerp(fl, w)
    d = l - c; a = math.radians(whip_on_deg(g))
    d = Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), d.z))
    sy, sp = shake22(g)
    right = Vector((d.y, -d.x, 0)).normalized()
    return c, c + d + right * (sy * d.length * 0.012) + Vector((0, 0, sp * d.length * 0.012))

def setup22(T):
    out = []
    spec = [("wallace", 8.6, 0.6), ("scot_c", 4.4, -2.2), ("scot_b", 6.0, 2.6), ("scot_a", 7.0, -0.8), ("scot_b", 7.6, -3.4),
            ("scot_a", 8.4, 3.8), ("scot_c", 9.2, -1.6), ("scot_a", 9.8, 1.8), ("scot_b", 10.6, -2.8)]
    for i, (cst, d, lat) in enumerate(spec):
        nm = "r%d" % i; T.actor("r_" + nm, cst); out.append((nm, cst, i, (0, 0))); RUNNERS.append((d, lat, 0.95 + 0.1 * (i % 4)))
    return out

def pose22(T, items, g):
    v, r = run_dir(); n = 0
    for nm, cst, i, (x, y) in items:
        f = g + 1; k = g - CUT22
        px, py = runner_xy(i, g)
        z = gsm(px, py)
        ph = (g / 16.0 + i * 0.31) % 1.0
        bob = 0.05 * abs(math.sin(ph * 2 * math.pi))
        T.place("r_" + nm, f, (px, py, z + bob))
        if cst == "wallace":
            p = dict(S21["wallace_run_sword"][1])
            p = cast21.cycle("wallace", ph, "run", -1, base=p, arms="l")
        else:
            p = cast21.run_spear(cst, ph, -1)
        p["blink"] = blink(g, 47 + 5 * i, 3 * i); p["t"] = g / 30.0
        T.pose("r_" + nm, f, p)

# ------------------------------------------------------------------ driver
def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

if __name__ == "__main__":
    shot = int(sys.argv[1]); cmd = sys.argv[2]; gs = [g for g in parse(sys.argv[3]) if RANGE[shot][0] <= g <= RANGE[shot][1]]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "work", "stills")
    mode = sys.argv[5] if len(sys.argv) > 5 else "draft"; samples = int(sys.argv[6]) if len(sys.argv) > 6 else None
    hide = {20: ("fg_generic_steel", "fg_generic_wood"), 21: ("fg_generic_steel", "fg_generic_wood"), 22: ()}[shot]
    T = C.Take(PRESET[shot], mode, samples, hide=hide)
    items = {20: setup20, 21: setup21, 22: setup22}[shot](T); COL[:] = getattr(T, 'col', [])
    cams = {20: cam20, 21: cam21, 22: cam22}[shot]
    posef = {20: pose20, 21: pose21, 22: pose22}[shot]
    for g in gs:
        loc, look = cams(g); T.key_cam(g + 1, loc, look)
    for g in gs: posef(T, items, g)
    T.sprites_for([g + 1 for g in gs], ppd=160)
    sc = 1.0
    os.makedirs(out, exist_ok=True)
    for g in gs:
        if os.path.exists(os.path.join(out, 'g_%04d.png' % g)) and os.environ.get('RESUME'): continue
        st = T.render([g + 1], out + "/raw", scale=sc, hook=lambda f: hook(f - 1))[0]
        os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("shot", shot, "g", g, "%.1fs" % st["wall"], flush=True)
