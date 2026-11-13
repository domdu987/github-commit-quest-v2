#!/usr/bin/env python3
"""shot.py -- film 7 take s21: shots 21-22 (plan 68.13-74.53 s = g 2044..2235) + 6 handle frames each side (g 2038..2241).
Plan: 21 louvre / empty_wall_queue: reopening day, a long queue behind velvet ropes staring at the empty wall (set_queue);
      22 louvre / wall_eye: ECU the four hooks, a lady gasps, a gentleman takes off his bowler.
One location (the Salon Carre, empty_wall_queue build: Mona gone, queue ropes on), five camera set-ups (framing change every 1.1-1.8 s):

    id 1  g 2038..2091  A  high wide over the queue: the rope lane full of visitors (ladies in picture hats, gentlemen in bowlers, a
                           newsboy), all staring up at the empty spot; a guard at the rope; slow drift in.     "แล้วเรื่องประหลาดก็เกิดขึ้น"
    id 2  g 2092..2135  B  reverse from beside the empty wall: the faces of the queue staring up at us, the lane receding into the
                           hung room; slow lateral drift.                                                       "พอลูฟวร์เปิดอีกครั้ง"
    id 3  g 2136..2169  C  (shot 22) ECU the four iron hooks on the unfaded damask patch, push in.             "คนต่อแถวยาวเหยียด"
    id 4  g 2170..2207  D  two-shot at the rope from the wall side: the lady gasps (gloved hand to her mouth, g 2174..2178),
                           the gentleman lifts his bowler off (g 2182..2200) and holds it to his chest.          "เพื่อมาดู ผนังว่าง ๆ"
    id 5  g 2208..2241  E  the hooks again, low and a little wider (plaque, gilt neighbours), push in to land on "ตะปูสี่ตัว"
                           (74.07 s = g 2225).  Out-handle g 2236..2241 continues the push.
Mouths: no quoted line -> static expression mouths only (stunned / shocked), changes hidden behind blinks.
NO depth of field (client rule): C.Take switches it off at build and before every render.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2|.. a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import common as C                                       # noqa: E402
import t5lib as T5                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")
T5.variants()
T5.hat_doff_patch()

# ----------------------------------------------------------------------------- timing
G0, G1, H = C.g_bound(68.13), C.g_bound(74.53), 6          # 2044, 2236
G22 = C.g_bound(71.20)                                    # 2136 shot 22
SETUPS = {1: (G0 - H, 2091), 2: (2092, G22 - 1), 3: (G22, 2169), 4: (2170, 2207), 5: (2208, G1 + H - 1)}
RANGES = SETUPS
G_GASP = 2174                                             # lady: hand to mouth 2174..2178
G_DOFF = (2182, 2189, 2200)                               # gentleman: hand up to the brim, hat off, down to the chest

# ----------------------------------------------------------------------------- the crowd (feet, world D; floor z 0)
# name: (cast, (x, y), seed, mirror)
CROWD = {
    "lady":   ("lady",        (-0.55, 19.85), 0.3, False),
    "gent":   ("gentleman",   (0.80, 19.75), 1.1, True),
    "boy":    ("newsboy",     (-1.75, 19.45), 2.2, False),
    "ladyb":  ("lady_b",      (1.85, 19.05), 3.4, True),
    "gentb":  ("gentleman_b", (-1.20, 18.45), 4.1, False),
    "ladyc":  ("lady_c",      (0.35, 18.00), 5.3, True),
    "gentc":  ("gentleman_c", (1.70, 17.20), 6.6, True),
    "ladyd":  ("lady_d",      (-1.55, 16.85), 7.2, False),
    "gentb2": ("gentleman_b", (0.05, 16.05), 8.8, False),
    "ladyb2": ("lady_c",      (1.30, 15.20), 9.5, True),
    "ladyd2": ("lady_d",      (-0.95, 14.80), 10.1, False),
    "gentc2": ("gentleman_c", (0.75, 13.70), 11.3, False),
    "guard":  ("guard",       (3.55, 19.95), 12.7, True),
}
VISIBLE = {1: [n for n in CROWD if n != "gentc2"], 2: [n for n in CROWD if n != "guard"], 3: [], 4: [n for n in CROWD if n != "guard"], 5: []}
PPD = {1: 160, 2: 240, 3: 160, 4: 288, 5: 160}            # sprite px per D per set-up (heads ~2x the screen size)

# ----------------------------------------------------------------------------- cameras: (loc0, look0, lens0), (loc1, look1, lens1)
CAMS = {
    1: (((3.70, 9.30, 6.95), (-0.35, 22.0, 0.75), 22.0), ((3.15, 10.55, 6.60), (-0.30, 22.0, 0.70), 23.0)),   # tilted down: near heads above y 880
    2: (((2.55, 21.65, 4.70), (-0.80, 15.2, 0.55), 18.0), ((1.95, 21.65, 4.60), (-1.05, 15.2, 0.60), 18.0)),
    3: (((0.30, 18.55, 3.70), (0.02, 22.0, 3.62), 30.0), ((0.16, 19.35, 3.66), (0.0, 22.0, 3.62), 30.0)),
    4: (((2.15, 21.60, 3.30), (-0.45, 18.6, 2.55), 22.0), ((1.85, 21.60, 3.25), (-0.40, 18.6, 2.55), 22.0)),
    5: (((0.75, 17.40, 2.75), (0.0, 22.0, 3.55), 26.0), ((0.40, 18.70, 3.05), (0.0, 22.0, 3.60), 26.0)),
}


def cam_of(sid, g):
    a, b = SETUPS[sid]
    u = ez((g - a) / float(max(1, b - a)), "lin" if sid in (1, 2) else "sine")
    (l0, k0, n0), (l1, k1, n1) = CAMS[sid]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lerp(n0, n1, u)


# ----------------------------------------------------------------------------- poses
def stare_pose(name, g, sid):
    cast, xy, seed, mir = CROWD[name]
    base = {"lady": "crowd_stare", "newsboy": "crowd_stare_newsboy", "guard": "guard_at_ease"}.get(cast.split("_")[0], "crowd_stare_gentleman")
    if cast == "newsboy":
        base = "crowd_stare_newsboy"
    p = dict(cast7.STORY7[base][1])
    hr, ln, gx, gy = T5.sway(g, seed)
    p["head_roll"] = p.get("head_roll", 0.0) + hr
    p["lean"] = p.get("lean", 0.0) + ln
    if cast == "guard":
        p.update(expr="neutral", yaw=-0.35, gaze=(-0.6 + gx, -0.2))
    elif sid == 2 or sid == 4:                     # from the wall side: they stare up at the empty spot = toward the lens
        p["yaw"] = (0.10 if not mir else -0.10) + 0.05 * math.sin(seed)
        p["pitch"] = -0.40
        p["gaze"] = (gx * 0.6 + (-0.15 if mir else 0.15), -0.55 + gy)
    else:
        p["gaze"] = (p["gaze"][0] + gx, p["gaze"][1] + gy)
    p["mirror"] = mir
    p["blink"] = T5.blinks(g, seed)
    p["t"] = g / 30.0
    return p


def lady_pose(g, sid):
    p = stare_pose("lady", g, sid)
    if sid != 4 or g < G_GASP:
        return p
    u = ez((g - G_GASP) / 4.0)
    q = cast7.STORY7["lady_gasp"][1]
    ha, hb = p["arm_r"]["hand"], q["arm_r"]["hand"]
    p["arm_r"] = dict(q["arm_r"], hand=(lerp(ha[0], hb[0], u), lerp(ha[1], hb[1], u)), bend=lerp(p["arm_r"].get("bend", 0.6), q["arm_r"]["bend"], u))
    p["expr"] = "shocked" if g >= G_GASP + 1 else p["expr"]
    p["blink"] = blink(g, [G_GASP - 1]) or p["blink"]
    p["pitch"] = lerp(-0.40, -0.25, u) - 0.06 * pulse(g, G_GASP, G_GASP + 3, G_GASP + 10, 1.0)
    p["lean"] = p["lean"] - 4.0 * u
    return p


def _bez(p0, p1, p2, u):
    return tuple((1 - u) ** 2 * a + 2 * (1 - u) * u * b + u * u * c for a, b, c in zip(p0, p1, p2))


def gent_pose(g, sid):
    p = stare_pose("gent", g, sid)
    if sid != 4 or g < G_DOFF[0]:
        return p
    a, b, c = G_DOFF
    rest = (-0.22, 0.72)
    brim = (-0.30, -0.42)                          # the left hand on the brim (head-centred puppet D, y down; mirror flips x)
    side = (-0.90, -0.05)                           # swung out to the side, clear of the face
    chest = (-0.22, 0.74)
    if g <= b:
        u = ez((g - a) / float(b - a))
        h = (lerp(rest[0], brim[0], u), lerp(rest[1], brim[1], u))
    else:
        u = ez(min(1.0, (g - b) / float(c - b)))
        h = _bez(brim, side, chest, u)
        p["hat_off"] = True
        p["pitch"] = -0.40 + 0.25 * u                  # a small respectful bow of the head
    p["arm_l"] = dict(hand=h, bend=-0.5 if g <= b else lerp(-0.5, 0.7, ez((g - b) / float(c - b))), shape="fist", layer="front")
    p["expr"] = "stunned"
    p["blink"] = blink(g, [b + 4]) or p["blink"]
    return p


_HAT0 = {}


def _hand(pose):
    fig = cast7.P.figure("gentleman", pose, "o")
    an = fig["anchors"]
    return an["hand_r" if pose.get("mirror") else "hand_l"], an["head"]     # mirror swaps the anchor names


def gent_overlay(f, pose):
    """the bowler in his hand once it is off (hat_off): it keeps the offset (head centre - hand) it had at the switch frame,
    so it leaves the head exactly where it sat and then travels with the hand."""
    if not pose.get("hat_off"):
        return ""
    if "off" not in _HAT0:
        pb = gent_pose(G_DOFF[1], 4)
        (hx, hy), (cx, cy) = _hand(pb)
        r = pb.get("head_roll", 0.0)
        _HAT0.update(off=(cx - hx, cy - hy), rot=(-r if pb.get("mirror") else r))
    (hx, hy), _ = _hand(pose)
    u = clamp((pose["t"] * 30.0 - G_DOFF[1]) / float(G_DOFF[2] - G_DOFF[1]))
    rot = lerp(_HAT0["rot"], -14.0 if pose.get("mirror") else 14.0, ez(u))
    ox, oy = _HAT0["off"]
    ox, oy = lerp(ox, 0.25 * ox, ez(u)), lerp(oy, 0.22, ez(u))      # the hat settles into the hand, in front of the chest
    return T5.hat_overlay("gentleman", (hx + ox, hy + oy), rot=rot, yaw=0.0)


def pose_of(name, g, sid):
    if name == "lady":
        return lady_pose(g, sid)
    if name == "gent":
        return gent_pose(g, sid)
    return stare_pose(name, g, sid)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "louvre", "empty_wall_queue", quality=quality, lens=22.0, name="cam_s21")
        sd = os.path.join(TMP, "sprites")
        for n, (cast, xy, seed, mir) in CROWD.items():
            a = C.make_actor(n, cast, sd)
            if n == "gent":
                a.round_head = False                     # the hat overlay is drawn in unstretched figure units
            self.actors[n] = a

    def pose(self, sid, gs):
        for g in gs:
            f = bf(sid, g)
            loc, look, lens = cam_of(sid, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, mona=False, queue=True)
            for n, a in self.actors.items():
                C.place(a, f, CROWD[n][1], 0.0)
        for n, a in self.actors.items():
            if n not in VISIBLE[sid]:
                continue
            fr = []
            for g in gs:
                f = bf(sid, g)
                self.scene.frame_set(f)
                a.pose(f, pose_of(n, g, sid), camera=self.cam)
                fr.append(f)
            res = a.render_sprites(PPD[sid], frames=fr, overlay=gent_overlay if n == "gent" else None)
            for f, r in zip(fr, res):
                self.anch[(a.name, f)] = r["anchors"]

    def report(self, sid, g):
        f = bf(sid, g)
        self._vis(sid)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(sid, g)
        v = look - loc
        return dict(shot=sid, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1),
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))

    def _vis(self, sid):
        for n, a in self.actors.items():
            a.set_hidden(n not in VISIBLE[sid])

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self._vis(sid)
        return C.Take.render(self, [bf(sid, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    sids = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for sid in sids:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[sid][0] <= g <= RANGES[sid][1]]
            if not gs:
                continue
            Tk.pose(sid, gs)
            for g in gs:
                print(json.dumps(Tk.report(sid, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(sid, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
                    print("set-up %d g %d  %.1f s wall %.1f cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), sids, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
