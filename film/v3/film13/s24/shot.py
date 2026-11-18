#!/usr/bin/env python3
"""shot.py -- film 13, render team 6: the REVEAL, shots 20-25 (one take per shot, folders s20..s25; run with the shot number)

  20  g1300-1361 under_wide  : pullman blows the whistle (g1344 = 44.69 s); push down the aisle
  21  g1362-1415 under_rows  : the workers turn their bars half a turn TOGETHER (set_jack_turn 0 -> 180), rows ripple in sync
  22  g1416-1466 jack_close  : one jack, hands push the bar half a turn, screw climbs, beam above lifts a hair
  23  g1467-1536 hotel_front : outside, the whole hotel rises evenly (h 0.5 -> 0.8), crane
  24  g1537-1601 street_wide : aha wide, the hotel high on its cribbing (h 0.8 -> 0.9), tiny workers beneath
  25  g1602-1679 under_rows  : high wide over thousands of jacks turning together, slow rise
    python3 shot.py probe|stills|final SHOT a:b[:step] [out scale samples]
"""
import math, os, sys, json, random, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c13 as C
from mathutils import Vector
D, actors, camrig, cast13, sprites = C.D, C.actors, C.camrig, C.cast13, C.sprites
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
SHOT = int(sys.argv[2]) if len(sys.argv) > 2 else 20
TMP = os.path.join(HERE, "work")
SPR = os.path.join(TMP, "sprites")
os.makedirs(SPR, exist_ok=True)

def gb(t): return int(round((t + 0.10) * 30))
BOUNDS = {20: (gb(43.22), gb(45.30)), 21: (gb(45.30), gb(47.10)), 22: (gb(47.10), gb(48.80)), 23: (gb(48.80), gb(51.13)),
          24: (gb(51.13), gb(53.30)), 25: (gb(53.30), gb(55.89))}
G0, G1 = BOUNDS[SHOT]                      # shot frames g0 .. g1-1
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = {20: "under_wide", 21: "under_wide", 22: "jack_close", 23: "hotel_front", 24: "street_wide", 25: "under_rows"}[SHOT]
G_WHISTLE = gb(44.69)                      # 1344
G_PUSH = G_WHISTLE + 10                    # the men start together (1354)
LENS = {20: 24.0, 21: 28.0, 22: 28.0, 23: 17.0, 24: 22.0, 25: 28.0}[SHOT]
PPD = 384 if SHOT == 22 else 256

def lerp3(a, b, u): return tuple(lerp(a[i], b[i], u) for i in range(3))
def mix(g, a, b, k=0.35):
    x = clamp((g - a) / float(b - a)); return k * ez(x, "sine") + (1 - k) * x      # mostly linear: the camera always moves

# ----------------------------------------------------------------------------- per-shot timelines
def lift_of(g):
    """street h (plan): reveal 0.4 -> 0.8 (shot 23: 0.5 -> 0.8), aha 0.9.  cellar hook: small beam rise only (the sprite hands ride on it)."""
    if SHOT in (20, 21, 22, 25):
        # cellar CELL_LIFT = 1 D at h 1: hairline rise, starts with the first turn
        if SHOT == 22: return lerp(0.45, 0.50, mix(g, G0 - H, G1 + H, 0.2))
        return 0.40
    if SHOT == 23: return lerp(0.50, 0.80, mix(g, G0 - H, G1 + H, 0.2))
    return lerp(0.80, 0.90, mix(g, G0 - H, G1 + H, 0.2))

def turn_of(g):
    """bars: 0 -> 180 degrees from the whistle response (half turn), then keeps turning (ratchet)."""
    return 180.0 * clamp((g - G_PUSH) / float(1416 - G_PUSH)) if g > G_PUSH else 0.0

def cam_of(g):
    u = lambda a, b: mix(g, a, b)
    if SHOT == 20:
        x = u(G0 - H, G1 + H)
        return lerp3((3.7, -1.6, 1.8), (2.9, 1.4, 1.95), x), lerp3((3.0, 14.0, 2.3), (3.0, 14.0, 2.5), x), 24.0
    if SHOT == 21:
        x = u(G0 - H, G1 + H)
        return lerp3((5.5, -9.0, 9.0), (2.0, 1.0, 7.4), x), lerp3((3.0, 17.0, 0.6), (3.0, 20.0, 0.6), x), 24.0
    if SHOT == 22:
        x = u(G0 - H, G1 + H)
        c = lerp3((11.9, 11.9, 2.1), (10.7, 13.2, 2.0), x)
        d = Vector((7.5 - c[0], 14.1 - c[1], 0)).normalized(); rt = Vector((d.y, -d.x, 0))
        la = (7.5 - rt.x * 0.75, 14.1 - rt.y * 0.75, lerp(2.3, 2.6, x))
        return c, la, 28.0
    if SHOT == 23:
        x = u(G0 - H, G1 + H)
        return lerp3((-2.5, -17.0, 1.3), (1.5, -20.0, 2.4), x), lerp3((0.0, -3.0, 6.0), (0.0, 0.0, 8.5), x), 17.0
    if SHOT == 24:
        x = u(G0 - H, G1 + H)
        return lerp3((-1.0, -41.0, 2.5), (5.0, -37.0, 3.2), x), lerp3((0.0, 0.0, 14.5), (1.0, 0.0, 14.0), x), 22.0
    x = u(G0 - H, G1 + H)
    return lerp3((5.0, -3.0, 10.5), (7.5, -16.0, 31.0), x), lerp3((6.5, 24.0, 2.0), (6.5, 20.0, 0.5), x), 28.0

# ----------------------------------------------------------------------------- poses
def bpy_objs(name):
    return [o for o in C.bpy.data.objects if o.name == name]

def jack_feet(loc, jx, jy):
    f = Vector((jx - loc[0], jy - loc[1], 0)).normalized(); rt = Vector((f.y, -f.x, 0))
    return (jx - rt.x * 1.29, jy - rt.y * 1.29)

def pose_pullman(g):
    calm = cast13.STORY13["pullman_stand_calm"][1]
    blow = cast13.STORY13["pullman_blow_whistle"][1]
    u = u_of(g, G_WHISTLE - 10, G_WHISTLE - 3)
    p = dict(blow if u >= 1.0 else calm)
    if 0 < u < 1:
        import puppet
        p = dict(puppet.lerp_pose("pullman", calm, blow, u)); p["whistle_hang"] = 1.0 if u < 0.5 else 0.0
        p["prop_r"] = blow["prop_r"] if u > 0.5 else None
        if p["prop_r"] is None: del p["prop_r"]
    p["legs"] = dict(crouch=0.3, spread=0.08)
    if u >= 1.0:
        p["blast"] = clamp((g - G_WHISTLE + 3) / 6.0) * (0.85 + 0.15 * math.sin(g * 0.9)); p["t"] = (g - G_WHISTLE) / 30.0
    p["yaw"] = 0.25 + 0.04 * math.sin(g * 0.07)
    p["blink"] = blink(g, [G0 + 14, G_WHISTLE - 18])
    return p

def worker_variants(kind):
    """sprite png pairs (A, B) per worker cast letter, with the bar only (jack drawn by the 3D set)."""
    jobs, boxes = [], []
    for L in kind:
        for ab in "AB":
            name = "worker_turn_bar_%s_%s" % (ab, L); c, p = cast13.STORY13[name]; p = copy.deepcopy(p); p["jack"] = 0
            for arm in ("arm_r", "arm_l"):                      # raise the hands 0.6 D: the bar hole sits at 1.9 D above the feet = the 3D lever height
                h = p[arm]["hand"]; p[arm]["hand"] = (h[0], h[1] - 0.6)
            jobs.append((c, p, PPD, cast13.CANVAS13_POSE[name])); boxes.append(cast13.CANVAS13_POSE[name])
    return C.sprite_files(jobs, SPR), boxes

# street cards: (cast, pose, stand point | (x, y), scale, flip)
STREET = {23: [("pullman", "pullman_look_up_confident", (-1.0, -12.5), 1.0, False),
               ("worker13_a", "worker_stand_a", (3.0, -10.5), 1.0, False),
               ("foreman13", "foreman_stand", (7.5, -13.5), 1.0, False),
               ("worker13_b", "worker_cheer_b", (-7.0, -10.5), 1.0, False),
               ("worker13_c", "worker_stand_c", (10.5, -11.0), 1.0, False)],
          24: [("pullman", "pullman_look_up_confident", (-9.0, -16.0), 1.0, False),
               ("foreman13", "foreman_stand", (-4.0, -14.0), 1.0, False),
               ("worker13_a", "worker_stand_a", (4.0, -15.0), 1.0, False),
               ("worker13_b", "worker_cheer_b", (8.5, -14.0), 1.0, False),
               ("worker13_c", "worker_cheer_c", (-12.0, -13.0), 1.0, False),
               ("worker13_a", "worker_stand_a", (13.0, -16.0), 1.0, False),
               ("worker13_b", "worker_stand_b", (-1.0, -17.5), 1.0, False)]}

# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, lens=LENS, name="cam_s%d" % SHOT)
        self.cards = C.Cards(self.scene)
        self.crowd = []
        self.pull = None
        self.setup_shot()
        self.on_frame = self.frame_hook

    def setup_shot(self):
        if SHOT == 21:
            D.set_cutaway(True)
            for ob in bpy_objs("floor_beams"):
                ob.visible_camera = False                    # keep the shadows: the beam stripes fall on the floor
        if SHOT == 20:
            self.pull = C.make_actor("pul", "pullman", SPR); self.actors["pul"] = self.pull
            self.PULL = Vector((3.0, 5.3, 0.0))
        if SHOT in (20, 21, 22):
            self.make_workers()
        if SHOT in (23, 24):
            self.make_street()
        if SHOT == 25:
            self.make_dense_bars()
            self.make_lanterns()

    def make_workers(self):
        pngs, boxes = worker_variants("abc")
        rnd = random.Random(7)
        cam0 = Vector(cam_of(RANGE[0])[0]); cam1 = Vector(cam_of(RANGE[1])[0])
        jacks = [(x, y) for x in D.UX for y in D.UY]
        cand = []
        for (jx, jy) in jacks:
            if SHOT == 20 and (abs(jx - 4.5) < 0.1 or abs(jx - 1.5) < 0.1) and abs(jy - 6.0) < 1.5: continue
            if SHOT == 22 and abs(jx - 7.5) < 0.1 and abs(jy - 14.1) < 0.1: continue
            cand.append((jx, jy))
        if SHOT == 22:
            cand = [(7.5, 14.1)] + [c for c in cand if c[1] > 14.5 and c[1] < 40 and abs(c[0] - 7.5) < 7.1][:40]
            self.hero_jack = (7.5, 14.1)
        self.crowd = []
        for (jx, jy) in cand:
            if SHOT == 20 and jy < 8.0: continue
            if SHOT in (20, 21) and rnd.random() < 0.33: continue         # a third of the jacks keep their (3D) lever: set_jack_turn shows
            k = rnd.randrange(3)
            it = self.cards.add("w_%d_%d" % (round(jx * 10), round(jy * 10)), [pngs[2 * k], pngs[2 * k + 1]], boxes[2 * k], (jx, jy), 0.0, block=D.STATE['M']['timber_d'])
            # per-variant box: both variants of one cast share the canvas
            self.crowd.append(dict(it=it, jx=jx, jy=jy, ph=rnd.randrange(0, 2) if SHOT != 22 else 0, kind=k))

    def make_dense_bars(self):
        """a short iron lever across the brass cap of every dense-field jack: 4 phase classes x 4 angles (0, 45, 90, 135 deg = a half turn,
        the bar looks the same after 180), one mesh per (class, angle); on_frame shows exactly one angle per class -> a wave of turning bars."""
        S = D.STATE; M = S["M"]; SET = S["SET"]
        self.dbars = []
        mats = M["iron_k"]
        for cl in range(4):
            row = []
            for a in range(4):
                mb = D.MB(); ang = math.radians(a * 45.0); dx, dy = math.cos(ang) * 0.25, math.sin(ang) * 0.25
                for r in range(D.DENSE_ROWS):
                    y = 5.0 + r * D.DENSE_DX
                    for i in range(D.DENSE_COLS):
                        if (r + i) % 4 != cl: continue
                        x = -8.3 + i * D.DENSE_DX
                        D.rod(mb, (x - dx, y - dy, 4.3), (x + dx, y + dy, 4.3), 0.045, mats, seg=4)
                ob = D._obj(mb, "dbar_%d_%d" % (cl, a), SET); ob.hide_render = a != 0; ob.visible_shadow = False
                row.append(ob)
            self.dbars.append(row)

    def make_lanterns(self):
        """tall iron posts with glowing oil lanterns along both long sides of the field (the preset's lamps sit under the jack forest)."""
        S = D.STATE; M = S["M"]; SET = S["SET"]
        mb = D.MB(); sites = [(-9.6, y) for y in (12.0, 28.0, 44.0, 60.0)] + [(19.6, y) for y in (20.0, 36.0, 52.0)]
        for k, (x, y) in enumerate(sites):
            D.rod(mb, (x, y, 0.0), (x, y, 7.0), 0.07, M["iron_d"], seg=5)
            c = D.Vector((x + (0.8 if x < 0 else -0.8), y, 6.6)); D.rod(mb, (x, y, 6.9), (c.x, c.y, 6.9), 0.05, M["iron_d"], seg=4)
            mb.frustum(c - D.Vector((0, 0, 0.5)), c + D.Vector((0, 0, 0.5)), 0.26, 0.34, M["lamp_glass"], seg=7)
            mb.frustum(c + D.Vector((0, 0, 0.5)), c + D.Vector((0, 0, 0.8)), 0.38, 0.05, M["iron_d"], seg=7)
            D._halo(mb, c, 3.2, M)
            D.D._flame_light("lan_%d" % k, tuple(c), D.LAMP, 900, radius=0.15, shadow=False)
        D._obj(mb, "lanterns", SET, shadow=False)

    def make_street(self):
        """cast cards standing in the street: real cast13 sprites, stand points, contact decals."""
        gz = D._gnd()
        spec = STREET[SHOT]
        rnd = random.Random(5)
        self.street = []
        for (cast, pose, where, scale, flip) in spec:
            c, p = cast13.STORY13[pose]
            png = C.sprite_files([(c, p, PPD, None)], SPR)[0]
            box = C.card_box(c)
            if isinstance(where, str):
                x, y, z = D.stand(where)
            else:
                x, y = where; z = gz(x, y) if y < -9.5 else 0.0
            it = self.cards.add("st%d" % len(self.street), [png], box, (x, y), z, scale=scale)
            self.street.append(dict(it=it, pose=pose, x=x, y=y, z=z))

    def pose(self, shot, gs):
        scene = self.scene
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            D.set_lift(lift_of(g), frame=f)
            D.set_jack_turn(turn_of(g), frame=f)
            if self.pull is not None:
                C.place(self.pull, f, self.PULL)
        if self.pull is not None:
            for g in gs:
                f = bf(shot, g); scene.frame_set(f)
                self.pull.pose(f, pose_pullman(g), camera=self.cam)
            self.sprites_for([(self.pull, PPD)], [bf(shot, g) for g in gs])

    def frame_hook(self, f):
        g = f - 1000 * (SHOT - 1) - 1
        loc, look, lens = cam_of(g)
        L = lift_of(g)
        for w in self.crowd:
            feet = jack_feet(loc, w["jx"], w["jy"])
            self.cards.move(w["it"], (feet[0], feet[1]), z=L, block=True)
            if g < G_PUSH - 6: i = 0
            else:
                i = int(((g - G_PUSH + 6 + 2 * w["ph"]) // 6) % 2)
            self.cards.show(w["it"], i)
        if SHOT == 25:
            for cl, row in enumerate(self.dbars):
                k = int(max(0, g - G_PUSH + 6) // 3 + cl) % 4 if g > G_PUSH - 6 else 0
                for a, ob in enumerate(row): ob.hide_render = a != k
        for (bo, bz, ph, x, y) in D.STATE.get("bars", []):
            if any(abs(w["jx"] - x) < 0.05 and abs(w["jy"] - y) < 0.05 for w in self.crowd):
                bo.hide_render = True

    def report(self, shot, g):
        f = bf(shot, g); self.scene.frame_set(f)
        loc, look, lens = cam_of(g)
        v = Vector(look) - Vector(loc)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

RANGES = {SHOT: RANGE}
if __name__ == "__main__":
    cmd = sys.argv[1]
    spec = sys.argv[3] if len(sys.argv) > 3 else "%d:%d:6" % RANGE
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        gs = [g for g in C.parse(spec) if RANGE[0] <= g <= RANGE[1]]
        Tk.pose(SHOT, gs)
        for g in gs:
            print(json.dumps(Tk.report(SHOT, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (SHOT, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (SHOT, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, s: Take(q), [SHOT], spec, RANGES, HERE, scale=scale, samples=samples)
