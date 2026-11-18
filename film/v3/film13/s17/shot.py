#!/usr/bin/env python3
"""shot.py -- film 13 take s17: shots 17, 18, 19 (g 1107..1296 + 6 handle frames each side: g 1101..1302), the FALSE PAYOFF.
One location (suite, light SUITE; the plan's MORNING / DAY are not available for the suite location, SUITE is the DAY-blue-sky variant).

    id 17  g 1101..1169  suite_window set-up: two days later the rich man stands at the open window, smug, cup + saucer in hand, the muddy
                         street far below (cast13 townsfolk).  Slow push in + drift.
    id 18  g 1170..1251  tea_close: the tea in the cup is a perfectly flat mirror (set_tea_ripple 0 keyed every frame), window behind; push in.
    id 19  g 1252..1302  suite_two: Q2 lip-sync 41.72-43.22 s ("เห็นมั้ย ไม่ขยับสักนิ้ว!"): he raises his cup, smug; lady and gentleman guests beside.

    python3 shot.py probe 17,18,19 a:b[:step]
    python3 shot.py stills 17,18,19 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 17,18,19 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast13, bpy = C.D, C.actors, C.camrig, C.cast13, C.bpy
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G17, G18, G19, G_END = C.g_bound(36.90), C.g_bound(39.00), C.g_bound(41.72), C.g_bound(43.22)   # 1107 1170 1252 1297
H = 6
RANGES = {17: (G17 - H, G18 - 1), 18: (G18, G19 - 1), 19: (G19, G_END + H - 1)}
Q2 = (C.g_of(41.72), C.g_of(43.22))                      # mouth window (narration +-0.15 s is allowed; we use the exact line)
PRESET = "suite_two"
LIGHT = None

RICH17 = Vector((1.2, 1.0, 30.0))
RICH19 = Vector((2.3, 1.0, 30.0))
LADY, GENT = Vector((-1.2, 1.0, 30.0)), Vector((0.7, 1.0, 30.0))

CAMS = {
    17: (((-3.0, 5.8, 32.9), (1.0, -1.0, 31.0), 22.0), ((-2.0, 4.6, 32.8), (1.3, -1.0, 31.1), 22.0)),
    18: (((-0.4, 6.4, 33.9), (-3.6, 2.0, 31.6), 30.0), ((-1.6, 4.9, 33.4), (-3.6, 2.0, 31.6), 30.0)),
    19: (((-1.0, 8.6, 32.4), (0.6, -2.0, 30.9), 22.0), ((-0.4, 7.7, 32.3), (0.7, -2.0, 30.9), 22.0)),
}
PPD = {17: 256, 18: 256, 19: 256}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    c0, c1 = CAMS[shot]
    return (Vector([lerp(c0[0][i], c1[0][i], u) for i in range(3)]), Vector([lerp(c0[1][i], c1[1][i], u) for i in range(3)]),
            lerp(c0[2], c1[2], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
RICH_BASE = cast13.STORY13["rich_look_window_smug"][1]


def rich_pose(shot, g):
    p = dict(RICH_BASE)
    p["blink"] = blink(g, [1130, 1190, 1235, 1270])
    p["t"] = g / 30.0
    sway = math.sin(g * 0.09)
    p["lean"] = 1.2 * sway
    if shot == 17:                                        # smug, looking out of the window; a slow nod of satisfaction
        p["head_roll"] = -3 + 1.5 * math.sin(g * 0.07)
        p["pitch"] = -0.25 + 0.05 * math.sin(g * 0.11)
        p["gaze"] = (0.9, 0.05 * math.sin(g * 0.05))
    elif shot == 18:                                      # tea shot: he is only a hint at the edge; keep the idle pose
        p["head_roll"] = -3 + 1.0 * math.sin(g * 0.07)
    else:                                                 # 19: turns to us / the guests, raises the cup, speaks
        up = u_of(g, G19 - 4, G19 + 14)
        p["yaw"] = lerp(0.85, 0.45, u_of(g, G19 - 6, G19 + 10))
        p["gaze"] = (lerp(0.9, 0.3, up), 0.0)
        p["pitch"] = lerp(-0.25, -0.40, up) + 0.04 * math.sin(g * 0.2)
        p["head_roll"] = lerp(-3, 6, up) + 1.2 * math.sin(g * 0.13)
        bob = 0.03 * up * math.sin((g - G19) * 0.3)
        p["arm_l"] = "behind"
        p["prop_l"] = None
        p["arm_r"] = dict(hand=(lerp(0.30, 0.95, up), lerp(0.95, 0.15, up) + bob), bend=lerp(0.4, -0.5, up), stretch=1.25, layer="front")
        p["prop_r"] = dict(type="teacup_saucer", scale=1.5)
        if Q2[0] - 2 <= g <= Q2[1] + 1:
            p["mouth"] = cast13.talk_mouth(g, 1.0)
        p["expr"] = "smug"
    return p


LADY_P = cast13.STORY13["lady_stand"][1]
GENT_P = cast13.STORY13["gentleman_stand"][1]


def guest_pose(which, g):
    p = dict(LADY_P if which == "lady" else GENT_P)
    p["blink"] = blink(g, [1260] if which == "lady" else [1285])
    p["head_roll"] = (2 if which == "lady" else -2) + math.sin(g * 0.08 + (0 if which == "lady" else 2))
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the street crowd: real cast13 cards
CROWD = [("town_a", "town_stand_a"), ("town_b", "town_stand_b"), ("town_c", "town_stand_c"), ("worker13_a", "worker_stand_a"),
         ("worker13_b", "worker_stand_b"), ("gentleman13", "gentleman_stand"), ("lady13", "lady_stand")]


def make_crowd(sprite_dir, n=44, seed=22):
    """n standing cast13 cards in the street below the window (hip-high mud), PropCards sharing one PNG per kind."""
    rnd = random.Random(seed)
    gnd = D._gnd()
    protos = []
    for member, posename in CROWD:
        cast, pose = cast13.STORY13[posename]
        a = C.make_actor("cp_" + member, member, os.path.join(TMP, "proto"))
        f = 9000 + len(protos)
        a.place(f, (0, 0, 0))
        a.pose(f, dict(pose), camera=None)
        a.set_hidden(True)
        res = a.render_sprites(256, frames=[f])[0]
        canvas = C.sprites.DEFAULT_CANVAS[member]
        protos.append((a, f, res, canvas))
    pts = []
    t = 0
    while len(pts) < n and t < 4000:
        t += 1
        x, y = rnd.uniform(-40, 40), rnd.uniform(-64, -20)
        if all((x - a) ** 2 + (y - b) ** 2 >= 2.4 ** 2 for a, b in pts):
            pts.append((x, y))
    cards = []
    for i, (x, y) in enumerate(pts):
        a, f, res, canvas = protos[rnd.randrange(len(protos))]
        png = os.path.join(TMP, "crowd", os.path.basename(a.sprite_path(f)).replace("cp_", "town_"))
        os.makedirs(os.path.dirname(png), exist_ok=True)
        if not os.path.exists(png):
            shutil.copyfile(a.sprite_path(f), png)
        pc = C.PropCard("crowd%d" % i, [png], canvas, scale=rnd.uniform(0.93, 1.07), shadow=True)
        pc.put((x, y, float(gnd(x, y))))
        cards.append(pc)
    for a, f, res, canvas in protos:                     # the prototype actors only existed to rasterise one sprite each
        for o in a.objects() + [a.root]:
            bpy.data.objects.remove(o, do_unlink=True)
        if a in actors.REGISTRY:
            actors.REGISTRY.remove(a)
    for im in list(bpy.data.images):                     # the prototypes' unused default image (frame 100, never rendered)
        if os.sep + "proto" + os.sep in im.filepath:
            bpy.data.images.remove(im)
    return cards


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=17):
        C.Take.__init__(self, PRESET, quality=quality, lens=22.0, name="cam_s17", light=LIGHT, state="tea0")
        sd = os.path.join(TMP, "sprites")
        self.rich = self.actors["rich"] = C.make_actor("rich", "rich", sd)
        self.lady = self.actors["lady"] = C.make_actor("lady", "lady13", sd)
        self.gent = self.actors["gent"] = C.make_actor("gent", "gentleman13", sd)
        self.crowd = make_crowd(sd)
        for pc in self.crowd:
            pc.put(pc.root.location, face=(-1.0, 5.5, 32.7))
        for n in ('chandelier', 'candles'):                  # out of the frame in shot 19; light and shadows stay
            ob = bpy.data.objects.get(n)
            if ob is not None:
                ob.visible_camera = False
        self.shot_now = None

    def pose(self, shot, gs):
        rich, lady, gent = self.rich, self.lady, self.gent
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(rich, f, RICH17 if shot != 19 else RICH19, z=30.0)
            C.place(lady, f, LADY, z=30.0)
            C.place(gent, f, GENT, z=30.0)
            for a in (lady, gent):
                for o in a.objects():
                    o.hide_render = shot != 19
                    o.keyframe_insert("hide_render", frame=f)
            for o in rich.objects():
                o.hide_render = False
                o.keyframe_insert("hide_render", frame=f)
            D.set_tea_ripple(0.0, frame=f)                      # tea: perfectly flat mirror, keyed on EVERY rendered frame
            for pc in self.crowd:                                # turn the street cards to the moving camera
                pc.put(pc.root.location, face=loc, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            rich.pose(f, rich_pose(shot, g), camera=self.cam)
            if shot == 19:
                lady.pose(f, guest_pose("lady", g), camera=self.cam)
                gent.pose(f, guest_pose("gent", g), camera=self.cam)
            else:
                lady.pose(f, guest_pose("lady", g), camera=self.cam)
                gent.pose(f, guest_pose("gent", g), camera=self.cam)
        frames = [bf(shot, g) for g in gs]
        jobs = [(rich, PPD[shot])] + ([(lady, PPD[shot]), (gent, PPD[shot])] if shot == 19 else [])
        self.sprites_for(jobs, frames)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), mouth=bool(Q2[0] - 2 <= g <= Q2[1] + 1 and shot == 19))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
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
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
