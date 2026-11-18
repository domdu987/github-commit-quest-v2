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
PRESET = {20: "under_wide", 21: "under_wide", 22: "jack_close", 23: "hotel_front", 24: "street_wide", 25: "under_wide"}[SHOT]
G_WHISTLE = gb(44.69)                      # 1344
G_PUSH = G_WHISTLE + 10                    # the men start together (1354)
LENS = {20: 24.0, 21: 20.0, 22: 28.0, 23: 22.0, 24: 17.0, 25: 18.0}[SHOT]
PPD = 384 if SHOT == 22 else 256

def lerp3(a, b, u): return tuple(lerp(a[i], b[i], u) for i in range(3))
def mix(g, a, b, k=0.35):
    x = clamp((g - a) / float(b - a)); return k * ez(x, "sine") + (1 - k) * x      # mostly linear: the camera always moves

# ----------------------------------------------------------------------------- timelines (rework: all bars swing 180 deg TOGETHER in 12 frames)
SW = [(1370, 1382), (1396, 1408), (1431, 1443), (1612, 1624), (1650, 1662)]
def prog(g, k): a, b = SW[k]; return clamp((g - a) / float(b - a))
def swung(g): return sum(prog(g, k) for k in range(len(SW)))
def swinging(g): return any(0 < prog(g, k) < 1 for k in range(len(SW)))
def lift_of(g):
    if SHOT in (21, 22, 25): return 0.40 + 0.08 * swung(g)          # beams step up with every swing (0.08 D)
    if SHOT == 23: return lerp(0.50, 0.85, mix(g, G0 - H, G1 + H, 0.1))
    return lerp(0.85, 1.0, mix(g, G0 - H, G1 + H, 0.1))
def theta_of(g):
    if SHOT == 22: return 201.0 - 180.0 * prog(g, 2)                  # away from the camera side: the worker walks round BEHIND the jack
    return 180.0 + 180.0 * swung(g)
BAR_R = 1.25
def cam_of(g):
    x = mix(g, G0 - H, G1 + H)
    if SHOT == 21: return lerp3((6.2, -3.5, 2.3), (4.0, 1.5, 2.4), x), lerp3((-1.0, 26.0, 3.0), (1.0, 28.0, 3.0), x), 22.0
    if SHOT == 22:
        c = lerp3((9.7, 9.7, 2.4), (9.5, 10.6, 2.5), x); return c, (7.6, 14.4, 3.0), 25.0
    if SHOT == 23: return lerp3((-18.0, -8.0, 1.8), (-17.6, -8.2, 1.85), x), lerp3((-2.0, -1.0, 4.5), (-2.0, -1.0, 4.6), x), 22.0
    if SHOT == 24: return lerp3((-3.0, -16.0, 1.0), (1.0, -16.5, 1.2), x), lerp3((0.0, 0.0, 5.0), (0.0, 0.0, 5.2), x), 17.0
    return lerp3((15.0, -3.0, 2.9), (11.5, 0.5, 3.0), x), lerp3((-2.0, 26.0, 3.1), (-1.0, 28.0, 3.1), x), 22.0

def jack_feet(loc, jx, jy, th):
    f = Vector((jx - loc[0], jy - loc[1], 0)).normalized(); rt = Vector((f.y, -f.x, 0))
    t = math.radians(th); tx, ty = jx + BAR_R * math.cos(t), jy + BAR_R * math.sin(t)
    return (tx - rt.x * 0.27, ty - rt.y * 0.27)

def worker_variants():
    jobs, boxes = [], []
    for L in "abc":
        for ab in "AB":
            name = "worker_turn_bar_%s_%s" % (ab, L); c, p = cast13.STORY13[name]; p = copy.deepcopy(p); p["jack"] = 0; p.pop("prop_r", None); p["mouth"] = "flat"
            for arm in ("arm_r", "arm_l"):
                h = p[arm]["hand"]; p[arm]["hand"] = (h[0], h[1] - 0.6)
            jobs.append((c, p, PPD, cast13.CANVAS13_POSE[name])); boxes.append(cast13.CANVAS13_POSE[name])
    return C.sprite_files(jobs, SPR), boxes

def pose_stand(base):
    c, p = cast13.STORY13[base]; p = copy.deepcopy(p); p["legs"] = dict(crouch=0.3, spread=0.08); p["mouth"] = "flat"; return c, p

STREET = {23: [("pullman", "pullman_look_up_confident", (-1.0, -12.5), 1.0),
               ("worker13_a", "worker_stand_a", (3.5, -10.5), 1.0),
               ("foreman13", "foreman_stand", (8.0, -13.5), 1.0)],
          24: [("worker13_a", "worker_stand_a", (-15.0, 2.5), 0.9), ("worker13_b", "worker_stand_b", (-10.0, 2.0), 0.9),
               ("worker13_c", "worker_stand_c", (-5.0, 2.5), 0.9), ("worker13_a", "worker_stand_a", (4.0, 2.0), 0.9),
               ("worker13_b", "worker_stand_b", (9.0, 2.5), 0.9), ("worker13_c", "worker_stand_c", (14.0, 2.0), 0.9),
               ("foreman13", "foreman_stand", (0.0, 3.0), 0.9)]}

# ----------------------------------------------------------------------------- the take
def objs(*names):
    return [o for o in C.bpy.data.objects if o.name in names]

class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, lens=LENS, name="cam_s%d" % SHOT)
        self.cards = C.Cards(self.scene)
        self.crowd = []; self.street = []
        if SHOT in (21, 22, 25): self.setup_cellar()
        else: self.setup_street()
        self.on_frame = self.frame_hook

    # ---- cellar: enclosed, beams + slab visible, thick bars, every worker holds a bar end and walks it round
    def setup_cellar(self):
        D.set_cutaway(False)
        if SHOT == 21:
            for o in objs('cellar_props'): o.hide_render = True
        for (bo, bz, ph, x, y) in D.STATE["bars"]:
            bo.scale = (1.0, 3.0, 3.0) if SHOT != 22 else (1.0, 2.2, 2.2)
            if SHOT == 22 and not ((abs(x - 7.5) < .1 and abs(y - 14.1) < .1) or y > 16.5): bo.hide_render = True
        pngs, boxes = worker_variants()
        rnd = random.Random(11)
        cam0 = cam_of(RANGE[0])[0]
        for x in D.UX:
            for y in D.UY:
                if SHOT in (21, 25) and y < cam0[1] + 3.5: continue
                if SHOT == 22 and not ((abs(x - 7.5) < .1 and abs(y - 14.1) < .1) or y > 16.5): continue
                k = rnd.randrange(3)
                it = self.cards.add("w_%d_%d" % (round(x * 10), round(y * 10)), [pngs[2 * k], pngs[2 * k + 1]], [boxes[2 * k], boxes[2 * k + 1]], (x, y), 0.0, block=D.STATE["M"]["timber_d"])
                self.crowd.append(dict(it=it, jx=x, jy=y))
        if SHOT == 22:                                   # a fixed timber post with a chalk mark at the beam underside of the first frame
            M = D.STATE["M"]; mb = D.MB(); px, py = 5.3, 15.4
            D.sbox(mb, (px - 0.2, py - 0.2, 0.0), (px + 0.2, py + 0.2, 7.0), M["timber_d"], 0.3)
            D.sbox(mb, (px - 0.23, py - 0.23, 3.24), (px + 0.23, py + 0.23, 3.34), M["cream"], 0.3)
            D._obj(mb, "mark_post", D.STATE["SET"])

    def setup_street(self):
        for o in objs("puddles", "scum"): o.hide_render = True
        for i, (cast, pose, xy, sc) in enumerate(STREET[SHOT]):
            c, p = pose_stand(pose) if SHOT == 24 else (cast13.STORY13[pose][0], cast13.STORY13[pose][1])
            png = C.sprite_files([(c, p, PPD, None)], SPR)[0]
            gz = D._gnd()(xy[0], xy[1]) if xy[1] < -9.5 else 0.0
            self.cards.add("st%d" % i, [png], C.card_box(c), xy, gz, scale=sc)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            D.set_lift(lift_of(g), frame=f)
            if SHOT in (23, 24): D.set_jack_turn(180.0 * clamp((g - G0) / float(G1 - G0)), frame=f)

    def frame_hook(self, f):
        g = f - 1000 * (SHOT - 1) - 1
        if SHOT not in (21, 22, 25): return
        loc, look, lens = cam_of(g); L = lift_of(g); th = theta_of(g); sw = swinging(g)
        for (bo, bz, ph, x, y) in D.STATE["bars"]:
            bo.rotation_euler.z = math.radians(th)
        for w in self.crowd:
            fx, fy = jack_feet(loc, w["jx"], w["jy"], th)
            self.cards.move(w["it"], (fx, fy), z=L, block=True)
            self.cards.show(w["it"], 1 if sw else 0)

    def report(self, shot, g):
        loc, look, lens = cam_of(g); v = Vector(look) - Vector(loc)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    lift=round(lift_of(g), 3), theta=round(theta_of(g), 1))

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
