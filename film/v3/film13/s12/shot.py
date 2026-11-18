#!/usr/bin/env python3
"""shot.py -- film 13 take s12: shots 12 + 13 (g 720..917: 6 in-handle frames before 726, 6 out-handle frames after 912), STREET, DAY, lift 0.
    id 12  g 720..842  (plan 24.20-28.09): Q1 continues, lip-sync (rich_mock_point).  Framing A (g 720..779): camera hanging in the air in
                       front of the facade, medium on the rich man leaning out of the top window, slow push + orbit.  Framing B (g 780..842,
                       hard cut at 26.0 s): starts close on him (push in), then a crane DOWN the facade (rich exits the top of frame) that
                       arrives on Pullman, calm, looking up at him, fists on hips.
    id 13  g 843..917  (plan 28.09-30.41): the nickname: townsfolk laugh and point at Pullman who walks past with an iron jack on his shoulder;
                       the nickname lands on 29.73 (g 895): the crowd bursts into a big bounce.
Mouth rule: rich talk_mouth through all of shot 12 (inside Q1 to 28.09 + 0.15), nobody else speaks.
Blender frame = 1000 * (id - 1) + g + 1.   One process per shot (cheap):
    python3 shot.py probe|stills|final <shot> a:b[:step] [out] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
D, actors, cast13, T, bpy = C.D, C.actors, C.cast13, C.T, C.bpy
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G_A = C.g_bound(24.20)            # 726
G_CUT = C.g_bound(28.09)          # 843
G_B = C.g_bound(26.00)            # 780: framing B
G_NICK = C.g_of(29.73)            # 895: the nickname lands
RANGES = {12: (G_A - 6, G_CUT - 1), 13: (G_CUT, C.g_bound(30.41) + 5)}
LENS = {12: 22.0, 13: 24.0}

# ----------------------------------------------------------------------------- cameras
# A: in the air in front of the top-floor window; B1: push in; B2: crane down the facade to the street; C13: crowd_street preset + a slow drift
CAM_A = [((5.5, -9.5, 32.2), (0.2, -0.5, 31.3)), ((3.5, -7.4, 32.3), (0.1, -0.5, 31.4))]
CAM_B1 = ((-3.4, -7.0, 32.4), (0.0, -0.5, 31.4))
CAM_B2 = ((-1.0, -9.0, 31.0), (0.0, -0.5, 31.0))
CAM_B3 = ((-3.5, -25.0, 2.3), (-1.3, -13.0, 4.8))
CAM_C = [((-6.0, -34.0, 2.6), (0.0, -8.0, 7.5)), ((-3.2, -33.0, 2.6), (-2.0, -8.0, 7.3))]


def _mix(c0, c1, u):
    return Vector(lerp(c0[0], c1[0], u)), Vector(lerp(c0[1], c1[1], u))


def cam_of(shot, g):
    if shot == 13:
        a, b = RANGES[13]; x = (g - a) / float(b - a); u = 0.35 * ez(x, "sine") + 0.65 * x
        return _mix(CAM_C[0], CAM_C[1], u)
    if g < G_B:
        x = (g - RANGES[12][0]) / float(G_B - RANGES[12][0]); u = 0.35 * ez(x, "sine") + 0.65 * x
        return _mix(CAM_A[0], CAM_A[1], u)
    g1 = G_B + 20                                          # B1: a short push in on him, then the crane down
    if g < g1:
        x = (g - G_B) / 20.0
        return _mix(CAM_B1, CAM_B2, 0.4 * x + 0.6 * ez(x, "sine"))
    x = (g - g1) / float(G_CUT - 1 - g1)
    u = 0.55 * x + 0.45 * ez(x, "sine")
    return _mix(CAM_B2, CAM_B3, u)


# ----------------------------------------------------------------------------- cast
RICH_POS = Vector(D.STATE['marks']['top_window'][:3]) if False else None


def rich_pose(g):
    p = dict(cast13.STORY13["rich_mock_point"][1])
    p["mouth"] = cast13.talk_mouth(g, 1.0)
    p["head_roll"] = 8 + 2.0 * math.sin(g * 0.15)
    p["lean"] = 5.0 + 2.0 * math.sin(g * 0.11)
    p["yaw"] = 0.4 + 0.05 * math.sin(g * 0.07)
    p["pitch"] = -0.2 + 0.08 * math.sin(g * 0.17)
    p["arm_r"] = dict(hand=(1.1, 0.5 + 0.05 * math.sin(g * 0.32)), shape="point", bend=-0.5, stretch=1.3)
    p["blink"] = blink(g, [731, 761, 790, 822])
    p["t"] = g / 30.0
    return p


def pullman_pose12(g):
    p = dict(cast13.STORY13["pullman_look_up_confident"][1])
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.09)
    p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.07)
    p["blink"] = blink(g, [748, 800])
    p["t"] = g / 30.0
    return p


PULL12 = (-1.5, -17.0)
PULL13 = ((9.0, -27.5), (-8.0, -27.5))


def pullman_pose13(g):
    ph = g / 24.0 * 0.5
    b = cast13.cycle("pullman", ph, "walk", -1, base=dict(expr="determined", mouth="smile", prop_r=dict(type="iron_jack", angle=-62, scale=1.0)), arms="l")
    b["arm_r"] = dict(hand=(0.42, 0.34), bend=-0.7, stretch=1.2, layer="top")
    b["blink"] = blink(g, [870, 905])
    return b


def pull13_xy(g):
    """Pullman walks across the lower frame at 6.8 D in front of the camera, from screen-right to screen-left."""
    a, b = RANGES[13]
    x = clamp((g - a) / float(b - a))
    loc, look = cam_of(13, g)
    F = Vector((look.x - loc.x, look.y - loc.y, 0.0)).normalized(); R = Vector((F.y, -F.x, 0.0))
    s = lerp(2.0, -2.0, x)
    p = loc + F * 6.8 + R * s
    return p.x, p.y


CROWD_POSE = {}


def setup_crowd_roles():
    S = cast13.STORY13
    mir = lambda p: dict(p, mirror=True)
    heights = dict(town_a=3.30, town_b=3.22, town_c=2.56, worker13_a=3.33, worker13_b=3.30, lady13=3.22, gentleman13=3.48)
    for k in "abc":
        c, p = S["town_laugh_point_" + k]
        T.PH["tl_%s_r" % k] = (c, dict(p), heights[c])
        T.PH["tl_%s_l" % k] = (c, mir(p), heights[c])
        c, p = S["town_stand_" + k]
        T.PH["ts_%s" % k] = (c, dict(p, expr="happy", mouth="smile"), heights[c])
    c, p = S["worker_cheer_a"]; T.PH["wc_a"] = (c, dict(p), heights[c])
    c, p = S["gentleman_stand"]; T.PH["gs"] = (c, dict(p), heights[c])
    c, p = S["lady_stand"]; T.PH["ld"] = (c, dict(p), heights[c])


def make_crowd(cam, n=34, seed=11):
    import random
    D.STATE["cards"] = []
    setup_crowd_roles()
    r = random.Random(seed); gnd = D._gnd(); pts = []; tries = 0
    bpy.context.view_layer.update()
    while len(pts) < n and tries < 6000:
        tries += 1
        x, y = r.uniform(-24, 24), r.uniform(-27, -11)
        if (x - 0) ** 2 * 0 + abs(y + 27.5) < 2.4 and abs(x) < 12:           # keep Pullman's lane clear
            continue
        z = gnd(x, y)
        if all((x - a) ** 2 + (y - b) ** 2 >= 2.0 ** 2 for a, b in pts) and D._visible(cam, x, y, z, 3.4, chin_max=868):
            pts.append((x, y))
    out = []
    for i, (x, y) in enumerate(pts):
        sx = (x - (-1.0))
        side = "r" if sx < 0 else "l"                     # point toward the middle of the street, where Pullman walks
        roll = r.random()
        if roll < 0.62:
            role = "tl_%s_%s" % (r.choice("abc"), side)
        elif roll < 0.75:
            role = r.choice(["wc_a", "ts_a", "ts_b"])
        elif roll < 0.88:
            role = r.choice(["gs", "ld", "ts_c"])
        else:
            role = "tl_c_%s" % side
        ob = D.crowd(1, None, seed=seed + i, kinds=[role], ground=gnd, points=[(x, y)], scale=(0.95, 1.05))[0]
        out.append(ob)
    return out


def key_crowd(cards, f, g):
    import random
    for i, ob in enumerate(cards):
        z0 = ob.get("z0")
        if z0 is None:
            z0 = ob["z0"] = ob.location.z
        ph = i * 0.7
        amp = 0.05 + 0.04 * ((i * 7) % 5) / 4.0
        rate = 0.55
        if g >= G_NICK - 2:                               # the nickname lands: a big shared jump that settles
            k = clamp((g - (G_NICK - 2)) / 14.0)
            amp = lerp(0.18, 0.07, k) + 0.05 * ((i * 3) % 4) / 3.0; rate = 0.7
        ob.location.z = z0 + amp * abs(math.sin(g * rate + ph))
        ob.keyframe_insert("location", frame=f, index=2)


def remove_near(points, r=1.5, zmax=3.5):
    """runtime set edit: delete the mesh faces of loose props (the burlap sacks) standing within r of the given ground points."""
    import bmesh
    n = 0
    for ob in list(D.STATE["SET"].objects):
        if ob.type != "MESH" or ob.name != "street_props":
            continue
        me = ob.data
        bm = bmesh.new(); bm.from_mesh(me)
        mw = ob.matrix_world
        kill = []
        for v in bm.verts:
            w = mw @ v.co
            if w.z < zmax and any((w.x - px) ** 2 + (w.y - py) ** 2 < r * r for px, py in points):
                kill.append(v)
        if kill:
            if len(kill) > 3000:
                bm.free(); continue                 # a big structure (street / building): not a prop
            bmesh.ops.delete(bm, geom=kill, context="VERTS"); n += len(kill)
            bm.to_mesh(me); me.update()
        bm.free()
    print("remove_near: %d verts" % n, flush=True)


class Take(C.Take):
    def __init__(self, quality="preview", shot=12):
        self.shot = shot
        C.Take.__init__(self, "hotel_front", quality=quality, lens=LENS[shot], name="cam_s12", state="lift0")
        S = os.path.join(TMP, "sprites")
        if shot == 12:
            self.rich = self.actors["rich"] = C.make_actor("rich", "rich", S)
            self.pul = self.actors["pul"] = C.make_actor("pul", "pullman", S)
            self.rich_xyz = tuple(D.STATE["marks"]["top_window"][:3])
        else:
            self.pul = self.actors["pul"] = C.make_actor("pul", "pullman", S)
            remove_near([(-3.0, -26.0), (-1.8, -26.6)], 1.3, 3.0)
            c0, l0 = _mix(CAM_C[0], CAM_C[1], 0.5)
            self.key_cam(bf(13, 850), c0, l0, lens=LENS[13])
            self.scene.frame_set(bf(13, 850))
            self.scene.camera = self.cam
            bpy.context.view_layer.update()
            self.cards = make_crowd(self.cam)
            print("crowd cards: %d" % len(self.cards), flush=True)

    def pose(self, shot, gs):
        gnd = D._gnd()
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            D.set_flames(1.0, frame=f)
            if shot == 12:
                C.place(self.rich, f, self.rich_xyz)
                C.place(self.pul, f, (PULL12[0], PULL12[1], gnd(*PULL12)))
            else:
                x, y = pull13_xy(g)
                C.place(self.pul, f, (x, y, gnd(x, y)))
                key_crowd(self.cards, f, g)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 12:
                self.rich.pose(f, rich_pose(g), camera=self.cam)
                self.pul.pose(f, pullman_pose12(g), camera=self.cam)
            else:
                self.pul.pose(f, pullman_pose13(g), camera=self.cam, )
        jobs = [(a, 320) for a in self.actors.values()]
        self.sprites_for(jobs, [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd in ("probe", "stills"):
        Tk = Take("preview", shot)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]
                os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, shot), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
