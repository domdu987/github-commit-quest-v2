#!/usr/bin/env python3
"""shot.py -- film 3 take s18: shots 18 and 19 (NOON, the disaster), harbor set NOON, painted brown.

    shot 18  g 1676..1743  hard cut in.  Low on the swollen bucket seam, looking up the wall: the plate strains, then from
                           "หมุดเหล็กดีด" (g 1697) the rivets shoot out like bullets: 3D rivet heads fly at the lens with
                           bright tracer streaks, molasses squirts from every hole, a camera jolt on each pop; punch-in g 1717
                           ("ออกเหมือน"), the volley peaks on "กระสุน" (g 1729); g 1734..1743 the seam splits open (dark jagged
                           crack + a gush of glossy blobs), violent shake.  Hard cut.
    shot 19  g 1744..1855  hard cut in.  Down Commercial Street from 1.4 D high: the glossy brown wave (taller than the row houses,
                           rolling lip, spray, gloss) pours down the street toward the lens; two workers and two kids sprint
                           ahead of it toward the camera; g 1790..1830 the camera cranes up and back to the wide view over the
                           street (street_wide side), the wave filling the street, the runners still ahead of it, slow push.
                           Handle out g 1856..1864 (15-frame dissolve into s20), rendered in 3D.

No casualties: the runners stay 5+ D ahead of the front on every frame (QA.md has the numbers).
Blender frame of (shot s, film frame g) = 1000 * (s - 17) + g - 1600.

    python3 shot.py probe 18|19 a:b:step
    python3 shot.py stills 18|19 a:b:step <out_dir> [scale] [samples]
    python3 shot.py final 18|19 a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d3"), os.path.join(PROJ, "v2", "shots"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector, Quaternion               # noqa: E402
import fx                                               # noqa: E402
import flood as FL                                      # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

H = fx.H
U = fx.HT.SEAM_U
TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G18, G19, G20 = 1676, 1744, 1856
H_OUT = 15 // 2 + 2                              # 9
RANGES = {18: (G18, G19 - 1), 19: (G19, G20 + H_OUT - 1)}
G_POP = g_of(56.474)                             # 1697 "หมุดเหล็กดีด"
G_LIKE = g_of(57.128)                            # 1717 "ออกเหมือน"
G_BULLET = g_of(57.521)                          # 1729 "กระสุน"
G_SPLIT = 1734
G_WAVE = g_of(58.49)                             # 1758 "กากน้ำตาลสูง"
G_HOUSE = g_of(59.243)                           # 1780 "กว่าบ้าน"
G_FLOOD = g_of(59.799)                           # 1797 "ก็ไหลท่วมถนน"
G_FASTER = g_of(60.616)                          # 1821 "เร็วกว่าคน"
G_RUN = g_of(61.173)                             # 1838 "วิ่ง"
NPOP = 64


def bf(shot, g):
    return 1000 * (shot - 17) + int(g) - 1600


def W(u, z, r=0.0):
    return fx.wall(U + u, z, fx.R + r)


# ----------------------------------------------------------------------------- shot 18 state
def bulge_amp(g):
    return keys(g, [(1676, 0.44, "sine"), (G_SPLIT, 0.52, "quad_out"), (1744, 0.66, "hold")]) + 0.02 * math.sin(g * 1.3) * clamp((g - 1676) / 20.0)


POPS = []                                        # (g_pop, rivet index, velocity) filled in Take


def plan_pops(rivets, cam_loc):
    r = random.Random(1919)
    # only rivets inside the punched-in frame (|u| < 2.1 D of the seam, z 2.4..6.6); near the seam first, then spread, jittered
    idx = [i for i in range(len(rivets)) if abs(rivets[i]["u"] - U) < 2.1 and 2.4 < rivets[i]["z"] < 6.6]
    idx.sort(key=lambda i: 0.45 * abs(rivets[i]["u"] - U) + 0.25 * abs(rivets[i]["z"] - 3.0) + r.uniform(0, 2.2))
    idx = idx[:NPOP]
    out = []
    for k, i in enumerate(idx):
        gp = G_POP + int(round(37.0 * (k / float(NPOP - 1)) ** 0.62)) if k else G_POP
        rv = rivets[i]; p = fx.wall_bulged(rv["u"], rv["z"])
        to_cam = (Vector(cam_loc) - p).normalized()
        d = (rv["n"] * 0.55 + to_cam * 0.45 + Vector((r.uniform(-0.35, 0.35), r.uniform(-0.35, 0.35), r.uniform(-0.15, 0.4)))).normalized()
        out.append((gp, i, d * r.uniform(0.75, 1.35)))
    return out


def pop_of(i):
    for gp, j, v in POPS:
        if j == i:
            return gp, v
    return None, None


def rivet_fn(g):
    def fn(i, rv):
        gp, v = pop_of(i)
        if gp is None or g < gp - 6:
            return Vector((0, 0, 0)), None, True
        if g < gp:                                       # creeps out and rattles before it goes
            k = (g - (gp - 6)) / 6.0
            jit = Vector((math.sin(g * 2.9 + i), math.cos(g * 3.7 + i), math.sin(g * 4.3 + 2 * i))) * 0.008 * k
            return rv["n"] * 0.025 * k + jit, None, True
        tau = g - gp + 0.5
        off = v * tau + Vector((0, 0, -0.004 * tau * tau))
        q = Quaternion(Vector((1, 0.3, 0)).normalized(), 0.9 * tau)
        return off, q, tau < 14
    return fn


def jet_state(g, gp, i):
    """length of the molasses squirt from the hole of a popped rivet (0 before the pop)."""
    if gp is None or g < gp:
        return 0.0
    tau = g - gp
    return min(1.0, 0.12 + 0.11 * tau) * (1.0 + 0.15 * math.sin(g * 1.7 + i))


def crack_w(g):
    return keys(g, [(G_SPLIT, 0.0, "cubic_out"), (1743, 0.42, "hold")])


def shake18(g):
    dx = dz = 0.0
    for gp, i, v in POPS:
        d = g - gp
        if 0 <= d <= 7:
            a = 0.022 * math.exp(-0.5 * d)
            dz += a * math.cos(d * 2.4 + i); dx += a * math.sin(d * 3.1 + 2 * i)
    if g >= G_SPLIT:
        a = 0.06 * clamp((g - G_SPLIT) / 4.0)
        dz += a * math.sin(g * 2.3); dx += a * math.cos(g * 3.4)
    dx += 0.004 * math.sin(g * 1.9); dz += 0.004 * math.cos(g * 2.6)                  # the wall groans: tremor
    return dx, dz


CAM18 = [(1676, W(1.05, 1.35, 4.70), W(0.05, 4.30), "sine"),
         (G_POP - 1, W(1.00, 1.38, 4.50), W(0.05, 4.25), "cubic_out"),
         (G_LIKE - 2, W(0.92, 1.40, 4.25), W(0.02, 4.15), "quint"),
         (G_LIKE + 7, W(0.70, 1.45, 3.55), W(0.00, 3.80), "sine"),
         (1744, W(0.62, 1.50, 3.35), W(-0.02, 3.95), "hold")]


def cam18(g):
    ks = [(f, tuple(l) + tuple(k), e) for f, l, k, e in CAM18]
    v = lerp(keys(g, ks), keys(g, [(f, x, "lin") for f, x, e in ks]), 0.15)
    loc, look = Vector(v[:3]), Vector(v[3:])
    dx, dz = shake18(g)
    f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized()
    look = look + r * dx * (look - loc).length + Vector((0, 0, dz * (look - loc).length))
    return loc, look


# ----------------------------------------------------------------------------- shot 19 state
def flood_u(g):
    return keys(g, [(1740, 0.08, "sine"), (G_HOUSE, 0.42, "lin"), (G_FASTER, 0.72, "lin"), (1866, 1.0, "hold")])


CAM19 = [(1744, (1.2, -50.0, 1.4), (3.0, 0.0, 6.6), "sine"),
         (1790, (1.3, -48.8, 1.6), (3.0, 0.0, 6.4), "quint"),
         (1830, (1.6, -80.0, 19.5), (3.4, -30.0, 0.0), "sine"),
         (1866, (1.7, -77.0, 18.6), (3.4, -30.0, -0.6), "hold")]


def cam19(g):
    ks = [(f, tuple(l) + tuple(k), e) for f, l, k, e in CAM19]
    v = lerp(keys(g, ks), keys(g, [(f, x, "lin") for f, x, e in ks]), 0.12)
    loc, look = Vector(v[:3]), Vector(v[3:])
    # the ground rumbles as the wave nears the low camera
    k = 0.006 * clamp((g - 1755) / 30.0) * (1.0 - clamp((g - 1795) / 20.0))
    look = look + Vector((math.sin(g * 2.1), 0, math.cos(g * 2.9))) * k * (look - loc).length
    return loc, look


CAMS = {18: cam18, 19: cam19}

RUNNERS = {  # name: cast, x, y at g 1744, speed D/frame, phase
    "worker1": ("worker1", -2.4, -31.0, 0.195, 0.0),
    "worker2": ("worker2", 3.4, -34.0, 0.185, 0.4),
    "kid1": ("kid1", -0.4, -28.0, 0.200, 0.2),
    "kid2": ("kid2", 1.7, -26.0, 0.205, 0.7),
}


def runner_y(name, g):
    c, x, y0, sp, ph = RUNNERS[name]
    return y0 - sp * (g - 1744) - 0.6 * ease(clamp((g - 1744) / 12.0), "sine") * 0


def runner_feet(name, g):
    c, x, y0, sp, ph = RUNNERS[name]
    hop = 0.10 * abs(math.sin(math.pi * (g / 8.0 + ph)))
    return (x + 0.15 * math.sin(g * 0.21 + ph * 6), runner_y(name, g), hop)


def run_pose(name, g):
    c, x, y0, sp, ph = RUNNERS[name]
    base = cast3.STORY3["kids_run_girl" if c == "kid2" else "kids_run"][1]
    p = json.loads(json.dumps(base))
    p["yaw"] = 0.32 if x < 1 else -0.32
    p["lean"] = 9 if x < 1 else -9
    step = int(math.floor(g / 4.0 + ph * 2)) % 2
    if step:
        ar, al = p["arm_r"], p["arm_l"]
        p["arm_r"] = dict(al, hand=(-al["hand"][0], al["hand"][1]), layer="front")
        p["arm_l"] = dict(ar, hand=(-ar["hand"][0], ar["hand"][1]), layer="back")
        lg = dict(p["legs"]); lg["stride"] = -lg["stride"]; p["legs"] = lg
    if c in ("worker1", "worker2"):
        p["expr"] = "shocked"; p.pop("fx", None); p["fx"] = ["sweat"]
    p["head_roll"] = (-6 if x < 1 else 6) + 3 * math.sin(g * 0.8 + ph)
    p["squash"] = (1.0, 1.0 + 0.03 * math.sin(math.pi * (g / 4.0 + ph * 2)))
    return p


# ----------------------------------------------------------------------------- set additions for shot 18
def build_extras(M):
    S = {}
    M['jet'] = fx.mat_glossy('S18_jet', '#2a0c04', gloss=0.012, rough=0.35, rim=0.18)
    mb = H.MB(); mb.frustum((0, 0, 0), (0, 0, 1), 1.0, 0.75, M['jet'], seg=8, cap0=False, cap1=True)
    proto = mb.obj('s18_jet_proto', fx._coll(), smooth=True); proto.hide_render = True
    S['jets'] = []
    for k in range(NPOP):
        ob = bpy.data.objects.new('s18_jet_%02d' % k, proto.data); fx._coll().objects.link(ob); fx.T.no_bounce(ob)
        ob.rotation_mode = 'QUATERNION'; ob.hide_render = True; ob.visible_shadow = False; S['jets'].append(ob)
    # crack ribbon on the bucket seam
    r = random.Random(7); n = 26
    S['crack_pts'] = [(0.25 + 6.5 * j / n, (0.10 if j % 2 else -0.10) + r.uniform(-0.06, 0.06)) for j in range(n + 1)]
    vs = [(0, 0, 0)] * (2 * (n + 1)); fs = [(2 * j, 2 * j + 1, 2 * j + 3, 2 * j + 2) for j in range(n)]
    me = bpy.data.meshes.new('s18_crack'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['crack'])
    S['crack'] = bpy.data.objects.new('s18_crack', me); fx._coll().objects.link(S['crack']); fx.T.no_bounce(S['crack'])
    mb = H.MB(); mb.sphere((0, 0, 0), 1.0, M['jet'], seg=12, rings=7); gp = mb.obj('s18_gush_proto', fx._coll(), smooth=True); gp.hide_render = True
    rr = random.Random(5); S['gush'] = []
    for k in range(40):
        ob = bpy.data.objects.new('s18_gush_%02d' % k, gp.data); fx._coll().objects.link(ob); fx.T.no_bounce(ob); ob.visible_shadow = False
        ob.rotation_mode = 'QUATERNION'
        S['gush'].append(dict(ob=ob, z=rr.uniform(0.6, 6.0), t0=G_SPLIT + rr.uniform(0, 8), v=rr.uniform(0.10, 0.26),
                              side=rr.uniform(-0.25, 0.25), up=rr.uniform(-0.05, 0.2), s=rr.uniform(0.06, 0.16)))
    return S


def set_extras18(S, g):
    for k, (gp, i, v) in enumerate(POPS):
        ob = S['jets'][k]; L = 0.45 * jet_state(g, gp, i) if k % 3 == 0 else 0.0
        if L <= 0:
            ob.hide_render = True; continue
        rv = fx.S['rivets'][i]; p = fx.wall_bulged(rv["u"], rv["z"], 0.01)
        d = rv["n"] * L + Vector((0, 0, -0.9 * L))
        ob.location = p; ob.rotation_quaternion = d.to_track_quat('Z', 'Y'); ob.scale = (0.022, 0.022, d.length); ob.hide_render = False
    NT = len(fx.S['tracers']); act = {}
    for k, (gp, i, v) in enumerate(POPS):
        tau = g - gp + 0.5
        if 0 <= tau <= 9:
            act[k % NT] = (tau, i, v)
    for tr in range(NT):
        if tr not in act:
            fx.streak(tr, (0, 0, 0), (0, 0, 0), 0, 0); continue
        tau, i, v = act[tr]
        rv = fx.S['rivets'][i]; p0 = fx.wall_bulged(rv["u"], rv["z"])
        fx.streak(tr, p0 + v * max(0.0, tau - 3.0), p0 + v * tau, 0.03, 1.0 - clamp((tau - 4) / 5.0))
    w = crack_w(g); cr = S['crack']
    cr.hide_render = w <= 0.005
    if w > 0.005:
        co = []
        for z, du in S['crack_pts']:
            ww = w * (0.4 + 0.6 * math.sin(math.pi * clamp(z / 6.8)) ** 0.5)
            co += list(fx.wall_bulged(U + du - ww / 2, z, 0.02)) + list(fx.wall_bulged(U + du + ww / 2, z, 0.02))
        cr.data.vertices.foreach_set('co', co); cr.data.update()
    for b in S['gush']:
        tau = g - b['t0']
        if tau < 0:
            b['ob'].hide_render = True; continue
        p = fx.wall_bulged(U, b['z'], 0.05); n = H.OUT(fx.th_u(U)); t = H.TAN(fx.th_u(U))
        pos = p + n * (b['v'] * tau) + t * (b['side'] * tau) + Vector((0, 0, b['up'] * 0.4 * tau - 0.02 * tau * tau))
        s = b['s'] * (0.6 + 0.06 * tau)
        b['ob'].location = pos; b['ob'].scale = (s, s, s * 2.2); b['ob'].rotation_quaternion = n.to_track_quat('Z', 'Y'); b['ob'].hide_render = False


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True, shot=18):
        global POPS
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = H.build("NOON")
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 4000
        H.set_paint(1.0); H.set_seep(1.0); H.set_bucket(fill=0.9, visible=True); H.set_flood(0.0)
        M = fx.init(rivets=True, span=4.2, tracers=40, haze=0)
        POPS = plan_pops(fx.S["rivets"], CAM18[0][1])
        self.S = build_extras(M)
        FL.init()
        self.cam = camrig.make_camera(scene, name="cam_s18")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.run = {}
        for nm, (c, x, y0, sp, ph) in RUNNERS.items():
            a = actors.Actor(nm, c); a.build(sprites.DEFAULT_CANVAS[c], sd, contact=True)
            a.head_flip = False                           # sun behind the camera, a little screen-left
            H.T.no_bounce(a.card); self.run[nm] = a
        self.anch = {}
        if verbose:
            print("s18: built in %.1f s" % (time.time() - t0), flush=True)

    def state(self, shot, g):
        if shot == 18:
            fx.set_bulge(bulge_amp(g), 0.3 * bulge_amp(g))
            fx.place_rivets(rivet_fn(g))
            set_extras18(self.S, g)
            FL.set(0.0, g)
            fx.drip(0.3, k=0, land_z=0.035 + (H.BUCKET_H - 0.05) * 0.9)
        else:
            fx.set_bulge(0.66, 0.2)
            fx.place_rivets(lambda i, rv: (Vector((0, 0, 0)), None, pop_of(i)[0] is None))
            for ob in self.S['jets']: ob.hide_render = True
            for b in self.S['gush']: b['ob'].hide_render = True
            for k in range(len(fx.S['tracers'])): fx.streak(k, (0, 0, 0), (0, 0, 0), 0, 0)
            for ob in fx.S['drip']: ob.hide_render = True
            fx.S['ring'].hide_render = True
            FL.set(flood_u(g), g)
            H.STATE['rupture'].hide_render = False; H.STATE['rupture'].scale = (1, 1, 1)
            H.STATE['rupture'].location = tuple(H.OUT(H.TH_B) * 0.7)
            self.S['crack'].hide_render = True
            # the bucket is buried under the flood near the burst
            H.set_bucket(visible=False)

    def key(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            for nm, a in self.run.items():
                a.place(f, runner_feet(nm, g))

    def pose(self, shot, gs):
        self.key(shot, gs)
        for a in self.run.values():
            a.set_hidden(shot != 19)
        if shot != 19:
            return
        fr = [bf(shot, g) for g in gs]
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for nm, a in self.run.items():
                a.pose(f, run_pose(nm, g), camera=self.cam)
        for a in self.run.values():
            for f, r in zip(fr, a.render_sprites(128, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s18: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[shot](g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads={})
        if shot == 19:
            u = flood_u(g); out["u"] = round(u, 3); out["front_y_x0"] = round(FL.front_y(0.0, u), 2) if u > 0.05 else None
            for nm, a in self.run.items():
                if f not in a.poses:
                    continue
                res = a.feet.get(f)
                hx, hy = self.anch[(nm, f)]["head"]
                c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
                l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
                r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
                x = RUNNERS[nm][1]
                out["heads"][nm] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1),
                                        ahead=round(FL.front_y(x, u) - runner_y(nm, g), 2) if u > 0.05 else None)
        else:
            out["pops_so_far"] = sum(1 for gp, i, v in POPS if gp <= g)
            out["seam"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(W(0, 3.0)), f)[:2]]
        return out

    def render(self, shot, g, out_dir, scale=1.0, samples=12, threads=2):
        for a in self.run.values():
            a.set_hidden(shot != 19)
        self.scene.cycles.samples = samples
        H.set_tank_ink(shot == 19)
        return render.render_frames([bf(shot, g)], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False, on_frame=lambda f: self.state(shot, g))[0]


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd == "probe":
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)))
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            st = Tk.render(shot, g, out, scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(quality="final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, g, out, scale=scale, samples=samples)
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
