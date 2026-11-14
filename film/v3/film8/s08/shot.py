#!/usr/bin/env python3
"""shot.py -- film 8 take s08: shots 8 + 9 (g 608..780, plan 20.28-26.03 s) + 6 handle frames each side (g 602..786).
"But he did not care: he built a mud wall as tall as a three-storey building to shade the channels, and a giant mud dome beside it."
One location (desert_ice plain, DAWN light, thick ice in the channels as the first winter nights pass), two set-ups, a cut at g 720:

    id 8  g 602..719  shot 8, wall_low-ish 3/4 from the channels looking ESE along the wall: TIME-LAPSE.  farid at the wall foot stacks
                      mud bricks in a fast repeated cycle (bend to the brick pile, heave a brick up to the course), while the wall rises
                      from ~2 D to its full 15 D (3 storeys) -- the set's wall mesh is keyed down into the ground and rises (runtime only,
                      desert.py untouched).  Pink-gold sunrise sky beyond, the dome far at the end.  The camera cranes up with the crest.
    id 9  g 720..786  shot 9, dome_wide at DAWN: the giant stepped mud dome finishes its time-lapse growth (z scale 0.62 -> 1, eased, by
                      g 762) beside the finished wall; farid stands proud at its glowing door, arms folded.  Slow push + crane up.
transition_in: dissolve 8 frames from shot 7 (the bazaar) -- g 602..607 are the in-handle (shot 8 starts its action at once).
Mouths: no quote -> static expression mouths.  NO depth of field anywhere (C.Take).

    python3 shot.py stills 8,9 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 8|9 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
import puppet                                            # noqa: E402  (same module object cast8 extends)
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G_CUT, G1 = C.g_bound(20.28), C.g_bound(24.00), C.g_bound(26.03)      # 608, 720, 781
H = 6
RANGES = {8: (G0 - H, G_CUT - 1), 9: (G_CUT, G1 + H - 1)}
LOC = ("desert_ice", "wall_low")
LIGHT = "DAWN"
WALL_H = D.WALL['h']


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# ----------------------------------------------------------------------------- shot 8: the wall rises
FARID8 = Vector((-3.0, 0.05, 0.0))          # on the strip between the wall foot (y -0.8) and channel 1's lip (y 0.68)
PILE = (-1.9, 0.15)                          # the brick pile, screen-right of him
CAM8_0 = ((-10.6, 7.8, 2.9), 120.0, 2.5)     # (loc, az, pitch)
CAM8_1 = ((-9.6, 6.9, 3.1), 124.0, 6.5)


def wall_h(g):
    """wall height: 2.2 D at the first handle frame -> 15 D at g 712 (mostly linear, eased at the end), the crest settles."""
    x = clamp((g - (G0 - H)) / float(712 - (G0 - H)))
    return lerp(2.2, WALL_H, 0.75 * x + 0.25 * ez(x, "sine"))


# ----------------------------------------------------------------------------- shot 9: the dome
FARID9 = Vector((12.6, 6.0, 0.0))
CAM9_0 = ((1.6, 2.6, 2.3), 79.0, 8.5)
CAM9_1 = ((3.2, 2.4, 2.8), 80.5, 8.5)


def dome_k(g):
    return lerp(0.62, 1.0, ez(clamp((g - G_CUT + 2) / 44.0), "sine") * 0.7 + 0.3 * clamp((g - G_CUT + 2) / 44.0))


def cam_of(shot, g):
    if shot == 8:
        x = (g - RANGES[8][0]) / float(RANGES[8][1] - RANGES[8][0]); a0, a1 = CAM8_0, CAM8_1
    else:
        x = (g - RANGES[9][0]) / float(RANGES[9][1] - RANGES[9][0]); a0, a1 = CAM9_0, CAM9_1
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc = Vector(lerp(a0[0], a1[0], u))
    return loc, Vector(aim(loc, lerp(a0[1], a1[1], u), lerp(a0[2], a1[2], u)))


# ----------------------------------------------------------------------------- poses
def _grip(p, src="l"):
    an = puppet.figure("farid", p, "q")["anchors"]
    k = "grip_far_%s" % src
    if k in an:
        gx, gy = an[k]
        p["arm_r" if src == "l" else "arm_l"] = dict(hand=(gx, gy), bend=-0.6, stretch=1.3, layer="front")
    return p


PERIOD = 15                                    # time-lapse: one brick every half second


def pose8(g):
    """bend to the pile (screen-right, low) -> heave the brick up to head height on the wall side -> drop down again."""
    ph = ((g - RANGES[8][0]) % PERIOD) / float(PERIOD)
    # 0..0.35 down at the pile, 0.35..0.75 lift, 0.75..1 back down (empty-handed quick)
    if ph < 0.35:
        up = 0.0
    elif ph < 0.75:
        up = ez((ph - 0.35) / 0.40)
    else:
        up = 1.0 - ez((ph - 0.75) / 0.25)
    carry = ph < 0.80
    hand = (lerp(0.62, 0.74, up), lerp(1.28, -0.05, up))
    p = dict(yaw=0.55, pitch=lerp(0.70, -0.45, up), expr="determined", head_roll=lerp(-2, -7, up) + 1.5 * math.sin(g * 0.3),
             gaze=(0.8, lerp(0.9, -0.6, up)), lean=lerp(22.0, -5.0, up),
             arm_l=dict(hand=hand, bend=-0.6, stretch=1.3, layer="front"),
             legs=dict(preset="crouch", crouch=lerp(0.40, 0.0, up / 0.5)) if up < 0.5 else "wide",
             fx=["sweat"] if (g // 40) % 2 else [])
    if carry:
        p.update(prop_l="mud_brick", panel_grip="bottom", panel_side=1)
        _grip(p, "l")
    else:
        p["arm_r"] = dict(hand=(lerp(0.40, 0.55, up), lerp(1.0, 0.4, up)), bend=0.3)
    p["blink"] = blink(g, [630, 668, 700])
    p["t"] = g / 30.0
    return p


def pose9(g):
    p = dict(cast8.STORY8["farid_smile"][1])
    p.update(head_roll=-5 + 2.5 * math.sin(g * 0.12), lean=1.5 * math.sin(g * 0.09), pitch=-0.25 + 0.08 * math.sin(g * 0.1),
             gaze=(0.2 + 0.2 * math.sin(g * 0.07), -0.2))
    p["blink"] = blink(g, [748])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- runtime set dressing (desert.py untouched)
def dress():
    """brick piles, straw, a water jar, baskets, a wooden mould, footprints of work: at the wall foot (shot 8) and by the dome (shot 9)."""
    S = D.STATE; M = S['M']; SET = S['SET']; mb = D.MB()
    import random
    r = random.Random(808)

    def brick(x, y, z, a=0.0):
        cx, cy = math.cos(a), math.sin(a)
        D.obox(mb, (x, y, z + 0.09), (cx, cy, 0), (-cy, cx, 0), (0, 0, 1), 0.24, 0.12, 0.09, M['mudbrick'], 0.25)

    def pile(x0, y0, nx, ny, nz, a=0.0):
        for k in range(nz):
            for i in range(nx - k):
                for j in range(ny):
                    brick(x0 + (i + 0.5 * k) * 0.5 * math.cos(a) - j * 0.26 * math.sin(a), y0 + (i + 0.5 * k) * 0.5 * math.sin(a) + j * 0.26 * math.cos(a),
                          0.18 * k, a + r.uniform(-0.06, 0.06))
    pile(PILE[0], PILE[1] - 0.25, 3, 2, 3)                      # the pile he works from
    pile(-6.4, -0.2, 4, 2, 3, 0.05); pile(-8.6, 0.0, 3, 2, 2)    # more stacks along the foot
    pile(1.2, -0.1, 4, 2, 2, -0.04); pile(5.0, 0.1, 3, 2, 3)
    for k in range(3):                                          # bricks drying on the sand (west of him)
        brick(-5.2 + 0.55 * k, 0.25, 0.0, 0.0)
    # the wooden brick mould and a mud heap with straw
    D.beam(mb, (-4.6, 0.45, 0.06), (-4.0, 0.45, 0.06), 0.30, 0.12, M['wood'])
    D.lumpy(mb, (-5.4, -0.1, 0.0), 0.55, M['mudbrick_d'], 811, seg=10, rings=5, rough=0.2, squash=0.45)
    D.lumpy(mb, (-5.0, 0.4, 0.0), 0.32, M['straw'], 812, seg=8, rings=4, rough=0.35, squash=0.4)
    D._bucket(mb, (-4.1, -0.3, 0.0), M, s=0.62)
    D._jar(mb, (-7.2, 0.35, 0.0), M, h=1.1, r=0.38, seed=3)
    D._jar(mb, (-7.75, 0.15, 0.0), M, h=0.9, r=0.32, seed=4)
    # basket of straw on the strip
    D.rod(mb, (-0.6, 0.25, 0.0), (-0.6, 0.25, 0.32), 0.30, M['basket'], seg=12, r1=0.36)
    D.lumpy(mb, (-0.6, 0.25, 0.32), 0.3, M['straw'], 813, seg=8, rings=4, rough=0.3, squash=0.5)
    # shot 9: by the dome -- brick stacks, a ladder against the porch, jars, palms, ice blocks waiting
    pile(17.6, 10.6, 4, 2, 3, 0.2); pile(19.4, 5.6, 3, 2, 2, -0.3)
    D._jar(mb, (23.0, 11.6, 0.0), M, h=1.3, r=0.45, seed=5); D._jar(mb, (23.7, 12.1, 0.0), M, h=1.0, r=0.36, seed=6)
    D._palm(mb, (14.5, 17.5, 0.0), M, h=7.5, seed=21); D._palm(mb, (30.5, 21.5, 0.0), M, h=8.0, seed=22)
    for k, c in enumerate(((16.0, 15.0), (26.0, 19.0), (8.0, 17.0))):
        D._shrub(mb, (c[0], c[1], 0.0), M, 90 + k, s=1.0)
    for k, c in enumerate(((11.0, 16.0), (19.0, 18.0), (28.5, 16.0))):
        D.lumpy(mb, (c[0], c[1], 0.1), 0.45, M['rock'], 830 + k, seg=8, rings=4, rough=0.3, squash=0.6)
    ob = D._obj(mb, 's08_dress', SET, hull=0.012)
    D.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- the take
SUN = {8: ((-0.55, -0.83), 11.0),             # DAWN override per set-up: shot 8 sunrise in the north-east so the wall's north face
       9: ((0.62, -0.78), 13.0)}              # catches the warm light; shot 9 a warm key from the north-west on the dome's face (the
                                              # painted sunrise glow stays behind the dome as a rim) -- one build per set-up


class Take(C.Take):
    def __init__(self, quality="preview", shot=8):
        tr, el = SUN[shot]
        D.LIGHTS["DAWN"] = dict(D.LIGHTS["DAWN"], key_dir=D.G._kd(tr, el), sun_elev=el)
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=20.0, name="cam_s08", light=LIGHT)
        import bpy
        self.wall = bpy.data.objects["wall"]
        self.dome = [bpy.data.objects[n] for n in ("dome", "dome_vent")]
        self.far = self.actors["far"] = C.make_actor("far", "farid", os.path.join(TMP, "sprites"))
        self.dress = dress()

    def pose(self, shot, gs):
        far = self.far
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=20.0 if shot == 8 else 22.0)
            C.place(far, f, FARID8 if shot == 8 else FARID9)
            self.key_set(f, ice="water" if shot == 8 else (0.06, 0.0))
            h = wall_h(g) if shot == 8 else WALL_H
            self.wall.location.z = h - WALL_H; self.wall.keyframe_insert("location", frame=f)
            k = dome_k(g) if shot == 9 else 1.0
            for ob in self.dome:
                ob.scale = (1.0, 1.0, k); ob.keyframe_insert("scale", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            far.pose(f, pose8(g) if shot == 8 else pose9(g), camera=self.cam)
        self.sprites_for([(far, 256 if shot == 8 else 192)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), wall_h=round(wall_h(g) if shot == 8 else WALL_H, 2), dome_k=round(dome_k(g) if shot == 9 else 1.0, 3))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            Tk = Take("preview", shot)
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
