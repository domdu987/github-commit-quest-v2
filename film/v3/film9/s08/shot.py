#!/usr/bin/env python3
"""shot.py -- film 9 take s08: shots 8 + 9 (g 507..696 + 6 handle frames each side: g 501..702).
Same location (wall_site), two lights -> two builds (final_loop take_key):

    id 8  g 501..614  shot 8, two_sections / DAY: the wall seen from the site, the general's grey plain-mortar section (screen-left)
                      and lin's creamy rice-mortar section (screen-right) meeting at x 0.  The general stands at the seam and chops
                      the air down the seam ("แบ่งกำแพงเป็นสองช่วง"), then points proudly at his own grey section ("ช่วงของแม่ทัพ
                      ใช้ปูนธรรมดา", g 567) and stands akimbo; lin waits calmly with arms folded in front of his section; a worker
                      carries a stack of bricks across the general's side.  Slow push + drift toward the grey section.
    id 9  g 615..702  shot 9, cauldron / DAWN: pink-gold dawn, lin alone on his platform stirring the steaming rice soup again, his
                      section behind him waiting.  Slow push.  Out-handle g 697..702.
Mouths: no quote in shots 8-9 -> static mouths only.  NO depth of field.  Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 8,9 a:b[:step]
    python3 shot.py stills 8,9 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 8|9 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.W, C.actors, C.camrig, C.cast9
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(16.90)              # 507 shot 8
G9 = C.g_bound(20.50)              # 615 shot 9
G1 = C.g_bound(23.24)              # 697 shot 10 (next take)
H = 6
RANGES = {8: (G0 - H, G9 - 1), 9: (G9, G1 + H - 1)}
G_SPLIT = (C.g_of(17.44) - 6, C.g_of(18.09) + 4)     # 520..549: the chop down the seam ("แบ่งกำแพง")
G_MINE = (C.g_of(18.81) - 6, C.g_of(18.81) + 4)      # 561..571: points at his own grey section ("ช่วงของแม่ทัพ")
G_AKIMBO = (C.g_of(20.11) - 4, C.g_of(20.11) + 6)    # 602..612: hands to the hips
HEIGHTS = (16, 16)                 # before the race: both sections level (month 1 = 18 / 21 in shot 10)
LIGHT = {8: "DAY", 9: "DAWN"}
PRESET = {8: "two_sections", 9: "cauldron"}

# ----------------------------------------------------------------------------- staging
GEN = Vector((1.3, 10.6, 0.0))             # at the seam, a little on his own side
LIN8 = Vector((-3.9, 10.2, 0.0))           # in front of his rice section
WK0, WK1 = Vector((5.4, 12.0, 0.0)), Vector((10.6, 11.8, 0.0))   # brick carrier walks screen-left along the general's side
LIN9 = Vector((-15.15, 13.3, 1.5))         # W mark lin_stir


def aim(loc, look):
    return (tuple(loc), tuple(look))


CAM = {8: (aim((-0.4, 20.2, 4.6), (0.2, 5.0, 3.6)), aim((0.7, 18.7, 4.4), (1.3, 5.0, 3.5))),
       9: (aim((-12.0, 21.8, 6.6), (-13.6, 12.5, 3.5)), aim((-12.5, 20.4, 6.2), (-14.0, 12.6, 3.6)))}
LENS = {8: 20.0, 9: 24.0}
PPD = {8: 256, 9: 256}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    (l0, k0), (l1, k1) = CAM[shot]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def bump(g, a, b):
    """0 -> 1 -> 0 over a..b (sine)."""
    if g <= a or g >= b:
        return 0.0
    return math.sin(math.pi * (g - a) / float(b - a))


# ----------------------------------------------------------------------------- poses
STIR = cast9.STORY9["lin_stir"][1]


def pose_stir(g):
    p = json.loads(json.dumps(STIR))
    ph = 2 * math.pi * g / 24.0
    dx, dy = 0.12 * math.cos(ph), 0.05 * math.sin(ph)
    p["arm_l"]["hand"] = (p["arm_l"]["hand"][0] + dx, p["arm_l"]["hand"][1] + dy)
    p["arm_r"]["hand"] = (p["arm_r"]["hand"][0] + dx, p["arm_r"]["hand"][1] + dy)
    p["prop_l"]["angle"] = 58 + 8 * math.sin(ph)
    p["lean"] = 8 + 2.5 * math.sin(ph)
    p["t"] = g / 30.0
    p["expr"] = "determined" if g < 662 else "happy"      # a small content smile late in the shot (behind the blink)
    p["mouth"] = "smile"
    p["mirror"] = True
    p["blink"] = C.blink(g, [640, 662, 690])
    return p


def pose_gen(g):
    """at the seam: smug -> the chop down the seam (right arm up high, then down) -> points at his own section (screen-left: the
    pose is mirrored, so 'screen-right' arm work points left) -> akimbo, chin up.  Static smug mouth (no quote here)."""
    k = g - RANGES[8][0]
    chop = u_of(g, *G_SPLIT)
    up = bump(g, G_SPLIT[0], G_SPLIT[0] + 16) if g < G_SPLIT[0] + 8 else 1.0 - chop
    mine = u_of(g, *G_MINE) * (1.0 - u_of(g, *G_AKIMBO))
    p = dict(yaw=0.35, pitch=-0.3 + 0.05 * math.sin(k * 0.13), expr="smug", head_roll=4 + 2.5 * math.sin(k * 0.11),
             lean=1.5 * math.sin(k * 0.09), legs="wide", arm_l="akimbo", mirror=False)
    if g < G_MINE[0]:
        # the chop: right hand rises above the head (g 520..536), then cuts down to the waist (536..549); facing the camera
        if g < G_SPLIT[0]:
            p["arm_r"] = "akimbo"
        else:
            r = u_of(g, G_SPLIT[0], G_SPLIT[0] + 14)
            d = u_of(g, G_SPLIT[0] + 16, G_SPLIT[1])
            hy = lerp(lerp(0.9, -0.9, r), 0.55, d)
            p["arm_r"] = dict(hand=(lerp(0.45, 0.62, r), hy), shape="open", bend=-0.2, stretch=1.15)
            p["yaw"] = lerp(0.35, 0.1, r)
    else:
        # mirrored: he turns to his own section (screen-left) and points at it, then akimbo
        p["mirror"] = True
        p["yaw"] = 0.45
        p["head_roll"] = 7 + 2 * math.sin(k * 0.2)
        p["gaze"] = (0.6, -0.2)
        p["arm_r"] = dict(hand=(lerp(0.45, 1.05, mine), lerp(0.95, -0.15 + 0.04 * math.sin(k * 0.5), mine)), shape="point" if mine > 0.4 else "ball",
                          bend=lerp(0.6, -0.5, mine), stretch=lerp(1.0, 1.3, mine))
        if g >= G_AKIMBO[1]:
            p["arm_r"] = "akimbo"
            p["pitch"] = -0.45
    p["blink"] = C.blink(g, [512, 558, 596])
    p["t"] = g / 30.0
    return p


def pose_lin8(g):
    p = json.loads(json.dumps(cast9.STORY9["lin_calm"][1]))
    k = g - RANGES[8][0]
    p["head_roll"] = -5 + 2.0 * math.sin(k * 0.1)
    p["lean"] = 1.2 * math.sin(k * 0.08)
    p["mirror"] = True                                # looks screen-left, toward the general at the seam
    p["gaze"] = (0.5, -0.05)
    p["blink"] = C.blink(g, [530, 585])
    p["t"] = g / 30.0
    return p


def pose_worker(g):
    base = json.loads(json.dumps(cast9.STORY9["workers_carry_b"][1]))
    ph = (g - RANGES[8][0]) / 26.0
    p = cast9.cycle("worker_b", ph, "walk", facing=-1, base=base, arms="none", speed=0.8)
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=8):
        C.Take.__init__(self, "wall_site", PRESET[shot], quality=quality, lens=LENS[shot], name="cam_s08", light=LIGHT[shot])
        self.shot = shot
        sd = os.path.join(TMP, "sprites%d" % shot)
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", sd, canvas=(-2.625, -4.875, 2.625, 0.125))
        if shot == 8:
            self.gen = self.actors["gen"] = C.make_actor("gen", "general", sd, canvas=(-2.25, -5.375, 2.25, 0.125))
            self.wk = self.actors["wk"] = C.make_actor("wk", "worker_b", sd)

    def pose(self, shot, gs):
        assert shot == self.shot
        a, b = RANGES[shot]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            self.key_set(f, steam=1.1, heights=HEIGHTS)
            if shot == 8:
                C.place(self.lin, f, LIN8)
                C.place(self.gen, f, GEN)
                C.place(self.wk, f, WK0.lerp(WK1, 1.0 - (g - a) / float(b - a)))
            else:
                C.place(self.lin, f, LIN9, z=LIN9.z)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 8:
                self.lin.pose(f, pose_lin8(g), camera=self.cam)
                self.gen.pose(f, pose_gen(g), camera=self.cam)
                self.wk.pose(f, pose_worker(g), camera=self.cam)
            else:
                self.lin.pose(f, pose_stir(g), camera=self.cam)
        jobs = [(self.lin, PPD[shot])]
        if shot == 8:
            jobs += [(self.gen, PPD[shot]), (self.wk, PPD[shot])]
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
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: LIGHT[shot])
