#!/usr/bin/env python3
"""shot.py -- film 7 take s01: shot 1 only (g 0..71 + 7 out-handle frames g 72..78), the hook: "this man walks out of the museum
holding the Mona Lisa".  Plan: louvre / exit_door -> paris street, vincenzo_smock walks out of the opened door into daylight, the
bulge under his smock, nervous smile at the camera.  Two set-ups inside the take (a framing change at 1.33 s, cut on the caption):

    id 1  g 0..39    louvre exit_door, CORRIDOR_MORNING: the service door swings open (g 0..14) and the courtyard daylight floods
                     the corridor; vincenzo (white smock, the panel a stiff bulge under it, sweating) watches it open, turns to us
                     (g 10..16) and gives a stiff nervous grin, both hands pressing the bulge flat (g 16..30, a gulp g 22..26, on
                     "ถือโมนาลิซ่า" 0.75 s = g 26), then walks off toward the bright doorway glancing back at us (g 30..39).
                     Slow push the whole set-up.
    id 2  g 40..78   paris street_wide, STREET_GOLDEN, papers 0 (nobody knows yet): CUT on "ออกจาก" (1.48 s): he walks toward
                     us down the rue in the sun (kiosk, cafe awning, gas lamps, fiacre, Notre-Dame far behind), hand on the bulge,
                     eyes darting left / right then the nervous grin into the lens (g 58..); the camera tracks back ahead of him
                     a little slower than he walks (slow push in).  Handle g 72..78: walk + track continue (rendered in 3D).
Mouths: nobody speaks (no quoted line in shot 1): the static mouth of each expression (worried -> grinning).
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402  (paths, cast7 first, bpy, louvre, stage)
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_END = C.g_bound(2.40)            # 72: shot 2 starts here
H_OUT = 7                          # out-handle g 72..78
G_CUT = C.g_bound(1.48 - 0.15)     # 40: corridor -> street, just before "ออกจาก" (1.48 s, event g 47)
RANGES = {1: (0, G_CUT - 1), 2: (G_CUT, G_END + H_OUT - 1)}
LOC = {1: ("louvre", "exit_door"), 2: ("paris", "street_wide")}
G_DOOR = (0, 14)                   # door 28 -> 92 deg
G_TURN = (10, 16)                  # turns from the door to the lens
G_GULP = (22, 26)
G_HOLD = C.g_of(0.75)              # 26 "ถือโมนาลิซ่า"
G_WALK = 30                        # walks off toward the doorway
G_GRIN2 = 58                       # street: grin into the lens

# ----------------------------------------------------------------------------- set-up 1: the service corridor (world D, floor z 0)
VIN_A = Vector((0.95, 6.75, 0.0))
WALK_A = Vector((-0.42, 0.62, 0.0)).normalized() * 0.072      # per frame, toward the doorway (screen-left, away)
CAM_A0 = ((1.72, 2.55, 2.45), (-0.80, 10.0, 2.80))
CAM_A1 = ((1.50, 3.35, 2.42), (-0.85, 10.0, 2.80))
LENS_A = 20.0
NO_SHAFT = os.environ.get('S01_SHAFT', '0') == '0'      # fanlight shaft sheet off: it hazed the whole left half (sat 0.19 -> crisper)

# ----------------------------------------------------------------------------- set-up 2: the rue (road z 0, pavements z 0.25)
VIN_B0 = Vector((-1.0, 9.6, 0.0))                              # mid-road: the kerb gas lamps (x +-4.5) stay off the near frame edge
WALK_B = Vector((0.010, -0.066, 0.0))                          # per frame: toward the camera, a little to screen-right (+x)
CAM_BACK = 0.052                                               # the camera tracks back this much per frame (< his speed: push in)
CAM_B_OFF = Vector((0.60, -3.55, 2.30))                         # camera relative to his feet at g G_CUT
LOOK_B_OFF = Vector((-0.35, 6.0, 1.45))
LENS_B = 22.0

PAL = dict(bulge=1.0)
HANDS_ON_BULGE = dict(arm_r=dict(hand=(0.22, 0.95), bend=0.7, shape="open"), arm_l=dict(hand=(-0.20, 1.00), bend=0.7, shape="open"))


def cam_a(g):
    u = ez(g / float(RANGES[1][1] + 1), "sine")
    return Vector(lerp(CAM_A0[0], CAM_A1[0], u)), Vector(lerp(CAM_A0[1], CAM_A1[1], u))


def vin_b(g):
    return VIN_B0 + WALK_B * (g - G_CUT)


def cam_b(g):
    d = g - G_CUT
    loc = VIN_B0 + CAM_B_OFF + Vector((0.004 * d, -CAM_BACK * d, -0.004 * d))
    look = VIN_B0 + LOOK_B_OFF + Vector((0.006 * d, -CAM_BACK * d, 0.0))
    return loc, look


def cam_of(shot, g):
    return cam_a(g) if shot == 1 else cam_b(g)


def vin_a(g):
    if g <= G_WALK:
        return VIN_A
    d = g - G_WALK
    return VIN_A + WALK_A * (d * d / 6.0 if d < 3 else d - 1.5)        # eases into the stride


def door_at(g):
    return lerp(28.0, 92.0, ez((g - G_DOOR[0]) / float(G_DOOR[1] - G_DOOR[0])))


# ----------------------------------------------------------------------------- poses
def vin_pose_a(g):
    t = g / 30.0
    if g < G_WALK:
        p = dict(cast7.STORY7["vincenzo_nervous_smile"][1])
        p.update(HANDS_ON_BULGE)
        ut = ez((g - G_TURN[0]) / float(G_TURN[1] - G_TURN[0])) if g >= G_TURN[0] else 0.0
        p["mirror"] = True                                    # faces screen-left (the door) -> turns to us
        p["yaw"] = lerp(0.62, 0.10, ut)
        p["gaze"] = (lerp(0.95, 0.0, ut), lerp(0.10, 0.0, ut))
        p["expr"] = "worried" if g < 13 else "grinning"
        gulp = pulse(g, G_GULP[0], G_GULP[0] + 1, G_GULP[1], 1.0)
        p["pitch"] = lerp(0.05, -0.05, ut) + 0.18 * gulp
        p["head_roll"] = lerp(4.0, -6.0, ut) + 1.5 * math.sin(g * 0.35)
        p["sweat"] = lerp(0.5, 0.9, ut)
        p["pale"] = 0.25
        p["lean"] = 2.0 * math.sin(g * 0.21)
        p["blink"] = blink(g, [12, 27])                       # the worried -> grin change sits behind the blink
        p["legs"] = "narrow"
    else:
        ph = (g - G_WALK) / 28.0
        u = ez(min(1.0, (g - G_WALK) / 6.0))               # ease from the stand into the stride (no pop at g 30)
        base = dict(expr="grinning", bulge=1.0, sweat=0.9, pale=0.25, yaw=lerp(0.10, 0.55, u),
                    gaze=(lerp(0.0, -0.75, u), 0.05 * u), head_roll=lerp(-6.0, -5.0, u), pitch=-0.05)
        p = cast7.cycle("vincenzo_smock", ph, "walk", facing=-1, base=base, arms="l", speed=lerp(0.3, 0.85, u))
        p["arm_r"] = dict(hand=(0.16, 0.94), bend=0.7, shape="open")
        if u < 1.0:                                          # the swinging hand leaves the bulge gradually
            hx, hy = p["arm_l"]["hand"]
            p["arm_l"] = dict(p["arm_l"], hand=(lerp(-0.20, hx, u), lerp(1.00, hy, u)), bend=lerp(0.7, p["arm_l"].get("bend", 0.5), u),
                              layer="front" if u < 0.75 else "back", shape="open")      # stays in front while it leaves the bulge
            p["lean"] = lerp(2.0 * math.sin(g * 0.21), p.get("lean", 0.0), u)
            if "legs" in p and isinstance(p["legs"], dict):
                p["legs"] = dict(p["legs"], stride=p["legs"]["stride"] * u, lift_r=p["legs"]["lift_r"] * u, lift_l=p["legs"]["lift_l"] * u)
        p["blink"] = blink(g, [36])
    p["t"] = t
    p.update(bulge=1.0)
    return p


def vin_pose_b(g):
    ph = (g - G_CUT) / 26.0 + 0.15
    # eyes dart: left (g 40..48), right (49..56), then the grin into the lens
    if g < 49:
        gz = (-0.85, 0.05)
    elif g < G_GRIN2 - 2:
        gz = (0.85, 0.05)
    else:
        gz = (0.0, 0.0)
    expr = "worried" if g < G_GRIN2 - 1 else "grinning"
    base = dict(expr=expr, bulge=1.0, sweat=0.9, pale=0.15, yaw=0.22, gaze=gz, head_roll=-3, pitch=-0.08)
    p = cast7.cycle("vincenzo_smock", ph, "walk", facing=1, base=base, arms="l", speed=0.75)
    p["arm_r"] = dict(hand=(0.16, 0.94), bend=0.7, shape="open")
    p["blink"] = blink(g, [G_GRIN2 - 1, 70])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- runtime set dressing (dense set; set module untouched)
def dress_corridor():
    """The exit_door corridor is bare inside the shot camera (its smocks rail / pipes sit high on the side walls, out of frame):
    add a glazier's corner and workers' clutter from louvre.py's own helpers + materials, in this scene only."""
    S = L.STATE; M = S['M']; SET = S['SET']
    mb, fl, cards = L.MB(), L.MB(), L.MB()
    x0, x1 = -3.0, 3.0
    # left wall: a low peg rail with three white smocks + caps (the workers' Monday uniform)
    L.rod(mb, (x0 + 0.06, 5.9, 3.45), (x0 + 0.06, 8.9, 3.45), 0.05, M['wood_d'], seg=6)
    for k, y in enumerate((6.25, 7.15, 8.2)):
        L._smock(mb, (x0 + 0.32, y, 3.4), M, 300 + k, s=0.82)
    for y in (6.7, 7.7):
        L.lumpy(mb, (x0 + 0.25, y, 3.3), 0.24, M['black'], int(y * 10), seg=8, rings=4, rough=0.15, squash=0.45)
    # left, beyond the smocks by the door wall: the glazier's crates of panes, panes leaning on them, a lit storm lantern on top;
    # a zinc bucket and a sack nearer
    mb.box((x0 + 0.1, 8.75, 0.0), (x0 + 1.3, 9.85, 1.0), M['crate'], tile=(1, 1))
    mb.box((x0 + 0.2, 8.9, 1.0), (x0 + 1.1, 9.8, 1.6), M['crate'], tile=(1, 1))
    for k in range(3):
        L.beam(mb, Vector((x0 + 1.5 + 0.07 * k, 8.85 + 0.28 * k, 0.02)), Vector((x0 + 1.26 + 0.07 * k, 8.85 + 0.28 * k, 1.3 - 0.1 * k)), 0.8, 0.02, M['glass'], up=(1, 0, 0))
    f = L._lantern(mb, fl, cards, (x0 + 0.65, 9.35, 1.6), M, hang=True, s=0.75)
    L._flame_light('s01_lantern', tuple(f), L.LANTERN, 60.0, radius=0.12, shadow=False)
    L.rod(mb, (-1.95, 5.9, 0), (-1.95, 5.9, 0.62), 0.27, M['zinc'], seg=12, r1=0.32)
    L.chain_rod(mb, [(-2.27, 5.9, 0.62), (-1.95, 5.9, 0.95), (-1.63, 5.9, 0.62)], 0.015, M['iron'])
    L.lumpy(mb, (-2.45, 7.0, 0.35), 0.42, M['rag'], 91, seg=10, rings=5, rough=0.25, squash=0.8)
    # back wall either side of the door: framed notices / the duty roster, a key board with keys
    for k, (xa, xb) in enumerate(((-2.75, -1.75), (1.75, 2.75))):
        z0, z1 = (2.3, 3.6) if k == 0 else (2.6, 3.5)
        mb.box((xa, 9.86, z0), (xb, 9.95, z1), M['wood_d'])
        nb = L.MB(); nb.oface([(xa + 0.08, 9.85, z0 + 0.08), (xb - 0.08, 9.85, z0 + 0.08), (xb - 0.08, 9.85, z1 - 0.08), (xa + 0.08, 9.85, z1 - 0.08)],
                              M['posters'][5] if k == 0 else M['posters'][3], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        L._obj(nb, 's01_notice_%d' % k, SET)
    mb.box((1.9, 9.84, 1.5), (2.6, 9.95, 2.2), M['wood'])
    for k in range(4):
        L.rod(mb, (2.0 + 0.16 * k, 9.84, 2.05), (2.0 + 0.16 * k, 9.72, 2.05), 0.015, M['brass'], seg=4)
        L.rod(mb, (2.0 + 0.16 * k, 9.74, 2.02), (2.0 + 0.16 * k, 9.74, 1.75), 0.022, M['iron'], seg=4)
    # right side, past the bench: a ladder and a broom against the wall by the lead pipe, the glazier's toolbox and putty tin
    for dy in (0.0, 0.62):
        L.beam(mb, Vector((x1 - 0.75, 7.0 + dy, 0.0)), Vector((x1 - 0.12, 7.0 + dy, 5.2)), 0.07, 0.07, M['wood_l'], up=(0, 1, 0))
    for k in range(1, 9):
        z = 0.55 * k; xx = x1 - 0.75 + (0.63 * z / 5.2)
        L.rod(mb, (xx, 7.0, z), (xx, 7.62, z), 0.035, M['wood_l'], seg=5)
    L.beam(mb, Vector((x1 - 0.55, 8.35, 0.05)), Vector((x1 - 0.1, 8.25, 3.6)), 0.05, 0.05, M['wood_l'], up=(1, 0, 0))
    L.lumpy(mb, (x1 - 0.5, 8.35, 0.32), 0.3, M['straw'], 77, seg=8, rings=4, rough=0.3, squash=1.5)
    mb.box((1.55, 8.4, 0.0), (2.35, 8.95, 0.45), M['wood'], tile=(1, 1))
    L.rod(mb, (1.6, 8.67, 0.45), (2.3, 8.67, 0.45), 0.03, M['iron'], seg=4)
    L.rod(mb, (1.3, 8.2, 0.0), (1.3, 8.2, 0.22), 0.12, M['zinc'], seg=10)
    L._obj(mb, 's01_dressing', SET, hull=0.012); L._obj(fl, 's01_glow', SET, shadow=False); L._obj(cards, 's01_halos', SET, shadow=False)
    for ob in SET.objects:
        if ob.name.startswith('s01_'):
            L.no_bounce(ob)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        loc, preset = LOC[shot]
        C.Take.__init__(self, loc, preset, quality=quality, lens=LENS_A if shot == 1 else LENS_B, name="cam_s01_%d" % shot)
        self.shot = shot
        sd = os.path.join(TMP, "sprites")
        if shot == 1:
            dress_corridor()
            if NO_SHAFT:
                for ob in self.scene.objects:
                    if ob.name.startswith('sun_shafts'):
                        ob.hide_render = True
        self.actors["vin"] = C.make_actor("vin", "vincenzo_smock", sd)

    def pose(self, shot, gs):
        assert shot == self.shot
        vin = self.actors["vin"]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look)
            if shot == 1:
                C.place(vin, f, vin_a(g), 0.0)
                self.key_set(f, door=door_at(g))
            else:
                C.place(vin, f, vin_b(g), 0.0)
                self.key_set(f, papers=0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            vin.pose(f, vin_pose_a(g) if shot == 1 else vin_pose_b(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(vin, 320)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads=C.head_report(self, f))
        if shot == 1:
            out["door"] = round(door_at(g), 1)
        return out

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
                     take_key=lambda shot: LOC[shot])
