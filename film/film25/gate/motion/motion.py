#!/usr/bin/env python3
"""motion.py -- film 25 MOTION TEST gate: the general mocking the tank, shot-plan v2 rows 19-22, g 522..675 (17.39-22.52 s).
One build of set25 preset trial_close_general (TRIAL location), one general25 card, four hard-cut setups:

  row 19  g 522-551  belly laugh (laugh / laugh_b every 3-4 frames), waist-up on the hull side; PUNCH 20 % over g 522-529, then drift
  row 20  g 552-601  "ถังน้ำเหล็ก จะไปรบเนี่ยนะ!": point_stick at the tank, lip-sync; eased PUSH 10 %
  row 21  g 602-625  "ของเล่นชัดๆ!": toy_dangle (toy swings, pose key t every frame), sneer, lip-sync; low angle, sky behind;
                     PUNCH 20 % over g 602-609, then a slow drift
  row 22  g 626-675  "ถ้ามันข้าม สนามเพลาะได้จริง": over his shoulder behind the tank, stick toward the test trench; PUSH 8 %

Blender frame = g.  Every camera / sun / actor value is computed here per frame (smooth eased splines) and keyed CONSTANT.
    python3 motion.py probe  <gspec>                          # reports only
    python3 motion.py draft  <gspec> [scale 0.4] [samples 12] # -> work/draft/g_%04d.png
    python3 motion.py final  <gspec>                          # set final (64 samples, native) -> frames/g_%04d.png (+ .json), resumable
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c25 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
F, cast25 = C.F, C.cast25

PRESET = "trial_close_general"
ROWS = [(19, 522, 552), (20, 552, 602), (21, 602, 626), (22, 626, 676)]     # g0, g1 exclusive
G_ALL = (522, 675)
PPD = 384
LEVEL = None
G22 = (-7.6, -31.6)                                      # row 22 mark: south of the tank nose: the test trench to his right, the tank behind


def row_of(g):
    for r, a, b in ROWS:
        if a <= g < b:
            return r, a, b
    raise ValueError(g)


def lvl(g):
    global LEVEL
    if LEVEL is None:
        LEVEL = C.audio_level()
    return LEVEL[g] if g < len(LEVEL) else 0.0


# ----------------------------------------------------------------------------- camera
def mark():
    m = F.S["mark"]
    return Vector(m["pos"]), m["face_deg"]


def cam_of(g):
    """(loc, look, lens) of frame g: an orbit position around the general at azimuth az (deg, world), distance d,
    camera height cz, look height lz, a lateral slide `side` (D, along the camera's right axis)."""
    r, a, b = row_of(g)
    u = (g - a) / float(b - 1 - a)
    P, f0 = mark()
    if r == 19:
        k = C.out_cubic((g - 522) / 7.0)                     # PUNCH 20 % in 7 frames
        d = 5.1 / (1.0 + 0.20 * k)
        w = C.calm((g - 529) / float(551 - 529))
        d = d / (1.0 + 0.04 * w)                             # then a slow drift in (+4 %) and to the side
        az, cz, lz, lens, side, lx = f0 + 10.0, 2.30, 2.25, 40.0, 0.35 * w, 0.0
    elif r == 20:
        w = C.calm(u)
        d = 5.0 / (1.0 + 0.10 * w)                           # PUSH 10 %
        az, cz, lz, lens, side, lx = f0 - 38.0, 2.35 + 0.1 * w, 2.25, 40.0, -0.25 * w, 0.32
    elif r == 21:
        k = C.out_cubic((g - 602) / 7.0)                     # PUNCH 20 % over g 602-609
        d = 5.0 / (1.0 + 0.20 * k)
        w = C.calm((g - 609) / float(625 - 609))
        d = d / (1.0 + 0.04 * w)
        az, cz, lz, lens, side, lx = f0 + 24.0, 1.50, 2.65, 36.0, 0.25 * w, -0.10
    else:
        w = C.calm(u)
        P = Vector((G22[0], G22[1], F.gh(*G22)))
        d = 2.9 / (1.0 + 0.08 * w)                           # PUSH 8 %
        az, cz, lz, lens, side, lx = 304.0, 2.9, 1.9, 20.0, -0.25 * w, None
    A = math.radians(az)
    loc = Vector((P.x + math.cos(A) * d, P.y + math.sin(A) * d, P.z + cz))
    fwd = Vector((-math.cos(A), -math.sin(A), 0.0))
    right = fwd.cross(Vector((0, 0, 1))).normalized()
    if r == 22:                                               # look 12 deg to the right of the general, out over the tank to the trench
        la = math.radians(az + 180.0 - 21.0)
        look = Vector((loc.x + 10 * math.cos(la), loc.y + 10 * math.sin(la), P.z + lz))
        loc = loc + right * side
        look = look + right * side
    else:
        loc = loc + right * side
        look = Vector((P.x, P.y, P.z + lz)) + right * (side * 0.6 + lx)
    return loc, look, lens


def feet_of(g):
    r = row_of(g)[0]
    if r == 22:
        return Vector((G22[0], G22[1], F.gh(*G22)))
    P, _ = mark()
    return Vector((P.x, P.y, F.gh(P.x, P.y)))


# ----------------------------------------------------------------------------- acting
def story(name):
    c, p = cast25.STORY25[name]
    return json.loads(json.dumps(p))


def blink(g, at):
    for b in at:
        if g - b in (0, 2):
            return 1
        if g - b == 1:
            return 2
    return 0


def squash_accent(g, g0):
    """squash 0.92 -> 1.05 -> 1.0 over 6 frames from g0 (x, y)"""
    k = g - g0
    seq = {0: 0.93, 1: 0.92, 2: 0.98, 3: 1.05, 4: 1.03, 5: 1.0}
    if k not in seq:
        return None
    s = seq[k]
    return [round(2.0 - s, 3) if s < 1 else round(1.0 - (s - 1.0) * 0.6, 3), s]


LAUGH_SEQ = [3, 4, 3, 3, 4, 3, 4, 3, 3]


def laugh_frame(g):
    k, i, use_b = g - 522, 0, False
    while k >= LAUGH_SEQ[i % len(LAUGH_SEQ)]:
        k -= LAUGH_SEQ[i % len(LAUGH_SEQ)]; i += 1; use_b = not use_b
    return use_b, i


def pose_of(g):
    r = row_of(g)[0]
    talk = C.cast25.talk_mouth(g, lvl(g))
    if r == 19:
        use_b, i = laugh_frame(g)
        p = story("general25_laugh_b" if use_b else "general25_laugh")
        u = (g - 522) / 29.0
        p["yaw"] = round(0.25 - 0.2 * u + 0.05 * math.sin(i * 1.7), 3)           # the head rolls round as he laughs
        p["head_roll"] = p["head_roll"] + (4 if i % 3 == 0 else -2)
        p["lean"] = p.get("lean", 0) - 3.0 * math.sin(math.pi * u)
        if g >= 545:                                                         # winds down, wipes the grin into a smug look
            p["pitch"] = -0.45
    elif r == 20:
        p = story("general25_point_stick")
        p["mouth"] = talk
        if g < 574:                                                          # "ถังน้ำเหล็ก": head toward the tank
            p["yaw"] = 0.55; p["head_roll"] = 9; p["gaze"] = [0.7, -0.1]
            jab = math.exp(-((g - 558) / 3.0) ** 2)                           # a jab of the stick on the noun
            p["arm_r"]["stretch"] = round(1.3 + 0.12 * jab, 3)
            p["prop_r"]["angle"] = round(8 - 10 * jab, 2)
        else:                                                                # "จะไปรบเนี่ยนะ!": turns to us, scoffing
            w = C.smooth((g - 574) / 6.0)
            p["yaw"] = round(0.55 - 0.40 * w, 3); p["head_roll"] = round(9 - 15 * w, 2); p["gaze"] = [round(0.7 - 0.7 * w, 2), 0.0]
            p["expr"] = "smirk" if g >= 576 else "smug"
            p["prop_r"]["angle"] = round(6 + 12 * math.sin((g - 576) * 2 * math.pi / 10.0), 2)   # stick wags at the tank
            p["lean"] = -5.0 * w
            sq = squash_accent(g, 594)                                       # accent on "นะ!"
            if sq:
                p["squash"] = sq
        p["blink"] = blink(g, [565, 574])
    elif r == 21:
        p = story("general25_toy_dangle")
        p["mouth"] = talk
        p["t"] = round(0.2 + (g - 602) / 24.0, 4)                            # the toy swings, every frame
        sq = squash_accent(g, 602)
        if sq:
            p["squash"] = sq
        if g < 614:                                                          # eyes on the toy
            p["gaze"] = [0.6, 0.45]; p["yaw"] = 0.35; p["head_roll"] = 10
        else:                                                                # "ชัดๆ!": sneers at us, lifts the toy
            w = C.smooth((g - 614) / 5.0)
            p["gaze"] = [round(0.6 - 0.6 * w, 2), round(0.45 - 0.45 * w, 2)]; p["yaw"] = round(0.35 - 0.2 * w, 3); p["head_roll"] = round(10 - 14 * w, 2)
            p["expr"] = "unimpressed" if g >= 615 else "smug"
            p["arm_r"]["hand"] = [0.62, round(0.30 - 0.14 * w, 3)]
        p["blink"] = blink(g, [613])
    else:
        p = story("general25_point_stick")
        p["mouth"] = talk
        w = C.smooth((g - 656) / 7.0)                                        # looks out at the trench, then back to us
        p["yaw"] = round(0.95 - 0.55 * w, 3)
        p["head_roll"] = round(4 - 10 * w, 2)
        p["gaze"] = [round(0.9 - 0.8 * w, 2), 0.05]
        jab = math.exp(-((g - 646) / 3.5) ** 2)                               # jab on "สนามเพลาะ"
        p["arm_r"]["stretch"] = round(1.3 + 0.15 * jab, 3)
        p["arm_r"]["hand"] = [0.95, round(0.12 - 0.12 * jab, 3)]
        p["prop_r"]["angle"] = round(-10 - 8 * jab + 3 * math.sin((g - 626) * 0.45), 2)
        p["expr"] = "smug" if g < 657 else "smirk"
        p["blink"] = blink(g, [655])
    p["light25"] = -1                                                        # key sun from screen-left (front.finish rule)
    p["rim25"] = 0.7
    return p


# ----------------------------------------------------------------------------- take
class Take(C.Take):
    def __init__(self):
        C.Take.__init__(self, PRESET)
        sd = os.environ.get("SPRITES", os.path.join(HERE, "work", "sprites"))
        os.makedirs(sd, exist_ok=True)
        self.gen = self.make_actor("gen", "general25", sd, contact=dict(width=1.5, depth=0.7, opacity=0.55))

    def pose(self, gs):
        for g in gs:
            loc, look, lens = cam_of(g)
            self.key_cam(g, loc, look, lens)
            C.camrig.key(self.gen.root, "location", g, feet_of(g), "CONSTANT", "AUTO")
            C.camrig.key(self.gen.root, "scale", g, Vector((1, 1, 1)), "CONSTANT", "AUTO")
            self.gen.flips[g] = False
        for g in gs:
            self.scene.frame_set(g)
            self.gen.pose(g, pose_of(g), camera=self.cam)
        self.sprites_for([(self.gen, PPD)], list(gs))

    def on_frame(self, f):
        loc, look, _ = cam_of(f)
        self.aim_sun(loc, look)

    def report(self, g):
        self.scene.frame_set(g)
        loc, look, lens = cam_of(g)
        return dict(g=g, row=row_of(g)[0], cam=[round(c, 3) for c in loc], look=[round(c, 3) for c in look], lens=lens,
                    heads=C.head_report(self, g), feet=C.feet_report(self, g), mouth=pose_of(g).get("mouth"))


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_ALL[0] <= g <= G_ALL[1]]
    Tk = Take()
    Tk.pose(gs)
    if cmd == "corners":                                  # screen corners of the card canvas per frame (for post25.py: exact puppet composite)
        out = {}
        cv = Tk.gen.canvas
        for g in gs:
            Tk.scene.frame_set(g)
            fx, fy = Tk.gen.feet[g]
            pts = [(cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3])]   # top-left, top-right, bottom-right, bottom-left (y down)
            out[g] = dict(quad=[list(C.actors.local_to_screen(Tk.gen, Tk.cam, (fx + x, fy + y), g, (fx, fy))) for x, y in pts],
                          canvas=list(cv), ppd=PPD)
        json.dump(out, open(os.path.join(HERE, "work", "corners.json"), "w"))
        print("corners", len(out))
    elif cmd == "probe":
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
    elif cmd == "draft":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        out = os.path.join(HERE, "work", "draft")
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            print(json.dumps(Tk.report(g)), "%.1f s" % st["wall"], flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "frames")
        os.makedirs(out, exist_ok=True)
        for g in gs:
            js = os.path.join(out, "g_%04d.json" % g)
            if os.path.exists(js) and os.path.exists(js[:-5] + ".png"):
                continue
            st = Tk.render([g], out, scale=1.0, samples=None)[0]
            rep = Tk.report(g)
            rep.update(wall=round(st["wall"], 1), cpu=round(st["cpu"], 1), samples=Tk.scene.cycles.samples, scale=1.0)
            json.dump(rep, open(js + ".tmp", "w")); os.replace(js + ".tmp", js)
            print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
