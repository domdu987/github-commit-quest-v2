#!/usr/bin/env python3
"""shot.py -- film 24 take s01: shots 1 + 2 (g 0..150 + 6 out-handle frames g 151..156), the hook: "this admiral hammers iron
spikes all over a ship's roof and puts a smoke-breathing dragon head on the bow".  One location (yard), two presets, two builds
(the sun follows each preset's camera), joined by the plan's hard cut at 2.60 s:

    id 1  g 0..77    shot 1, yard roof_low: the turtle ship on its cradles on the slipway, spikes half done (set_spikes 2), no smoke.
                     kor_a24 kneels on the port roof edge (parented to J.ship_root('turtle'), knees on the roof) and hammers a spike
                     on the beat (arm_r only, a strike every 12 frames, g 1, 13, ... 73: one lands on "ตอก" = g 49).
                     kor_d24 stands planted on the same roof edge (bow side) with a bundle of spikes and a rope coil.  Yi stands on the quay in front,
                     arms behind his back, looking at the ship, a slight idle sway (feet planted).  Camera: one slow eased push-in.
    id 2  g 78..156  shot 2, yard macro_dragon: 55 mm f/2.8 on the dragon head's mouth, the bay in bokeh.  The mouth starts to puff
                     grey-yellow smoke at g 84 ("แล้วติดหัวมังกร"), swelling on "พ่นควัน" (g 115); puffs leave the mouth one after
                     another (common.key_set smoke_start).  Camera: one slow push ~5 %.  Handle g 151..156: the smoke and the push go on.
Mouths: nobody speaks (no quote): fixed expression mouths only.

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale 0.4] [samples 10]
    python3 shot.py final 1|2|1,2 a:b[:step] [scale 0.75] [samples 24]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402  (paths, cast24 first, bpy, joseon, stage)
from mathutils import Vector                             # noqa: E402

J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_CUT = C.g_bound(2.60)            # 78: shot 2 starts (plan cut, hard)
G_END = C.g_bound(5.02)            # 151: shot 3 (sea fleet_wide) starts here
H_OUT = 6                          # out-handle g 151..156
RANGES = {1: (0, G_CUT - 1), 2: (G_CUT, G_END + H_OUT - 1)}
PRESET = {1: "roof_low", 2: "macro_dragon"}
BEAT = 12                          # hammer strike every 12 frames ...
G_HIT0 = C.g_of(1.54) % BEAT       # ... phased so one strike lands on "ไปตอก" (1.54 s -> g 49): strikes g 1, 13, 25, 37, 49, 61, 73
HITS = [g for g in range(G_HIT0, RANGES[1][1] + 1, BEAT)]
G_SMOKE = C.g_of(2.74)             # 85 "แล้วติดหัวมังกร": the first puff leaves the mouth
G_PUFF = C.g_of(3.72)              # 115 "พ่นควัน": the smoke swells
SMOKE_SPEED = 1.3

# ----------------------------------------------------------------------------- staging (world D; yard: land z 2.2, quay z 2.25)
YI = (9.5, 1.2, J.Z_Q)             # set mark yi_quay: on the quay in front, nearest figure
KD_X = 6.1                         # kor_d24 stands on the same port roof edge, 3.6 D toward the bow (screen-right of the hammerer; at 5.5 his spike bundle overlapped the hammer swing)
                                   # (no quay point is both in this narrow frame and farther than Yi: the far quay is off-frame left)
ROOF_MARK = "worker_roof_p3"       # port (east) roof edge, facing the camera; ship-local point from A['parented']
KA_YAW = 90.0                      # the kneeling card's width axis = world +y (the ship's long axis).  With the default
                                   # camera-facing yaw the card ran 38 deg across the roof: its left half (the shins, drawn
                                   # behind the knees) went 0.6 D UP the 49 deg eave slope and the roof hid them -> he looked
                                   # like a legless man floating above the anchor.  Along the ship the card only meets the
                                   # 7 deg slipway pitch (toes 0.1 D into the roof, never above it).
PPD = dict(yi=160, kd=128, ka=128)

# shot 1: the roof_low preset camera, pushed in 8 % along its view line (look point drifts a little up onto the roof)
CAM1_0 = ((15.8, 9.0, 3.6), (-0.5, -3.5, 5.9))
PUSH1 = 0.08
LENS1 = 22.0
# shot 2: the macro_dragon preset camera (55 mm f/2.8, focus on the mouth), pushed 5 %
PUSH2 = 0.05
LENS2 = 55.0


def cam_of(shot, g, A=None):
    if shot == 1:
        x = (g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0])
        u = C.calm(x)
        loc0, look = Vector(CAM1_0[0]), Vector(CAM1_0[1])
        loc = loc0 + (look - loc0) * (PUSH1 * u)
        look = look + Vector((0.0, 0.0, 0.25 * u))
        return loc, look, LENS1
    x = (g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0])
    u = C.calm(x)
    loc0, look = Vector(CAM2_0[0]), Vector(CAM2_0[1])
    loc = loc0 + (look - loc0) * (PUSH2 * u)
    return loc, look, LENS2


MOUTH = (0.0, 19.1318, 3.2004)     # J.ship_root('turtle').matrix_world @ S['turtle']['mouth'] (the preset's look_at and focus)
# The preset camera (-5.2, 25.4, 4.4) is 8.2 D in front of the mouth: the puffs (they drift 5 D toward the bow and 5-6 D up)
# fly into the lens as huge blurred blobs and leave through the top within a second.  s01 keeps the preset's lens, f-stop and
# focus point (an empty on the mouth) but stands 11 D off on the same (west) side at 50 deg, looking a little above / ahead of
# the mouth: the snout sits lower right, the smoke rises into the open sky upper left.  The sun is re-aimed for this camera.
_A2 = math.radians(-50.0)
CAM2_0 = ((MOUTH[0] + 11.0 * math.sin(_A2), MOUTH[1] + 11.0 * math.cos(_A2), 4.9), (MOUTH[0], MOUTH[1] + 1.8, MOUTH[2] + 1.4))


# ----------------------------------------------------------------------------- poses
def _arm(u):
    """hammer arm: u 0 = raised (0.60, -0.50), angle -70;  1 = strike (0.78, 0.62), angle 20 (cast24 STORY24_META note)."""
    return dict(hand=(lerp(0.60, 0.78, u), lerp(-0.50, 0.62, u)), bend=lerp(-0.7, -0.2, u), stretch=1.2, layer="front"), lerp(-70.0, 20.0, u)


def hammer_u(g):
    """0 raised .. 1 strike.  3 frames down onto the strike, 5 frames back up, 4 frames of wind-up (slightly higher, < 0)."""
    p = (g - G_HIT0) % BEAT                       # 0 = strike frame
    if p == 0:
        return 1.0
    if p <= 5:                                    # up: 1 -> 0 over 5 frames
        return 1.0 - ez(p / 5.0)
    if p <= 8:                                    # wind-up: lift a little more
        return -0.12 * ez((p - 5) / 3.0)
    return lerp(-0.12, 1.0, ((p - 8) / 4.0) ** 1.6)   # down: accelerating onto the next strike (p 9, 10, 11 -> 12 = strike)


def pose_ka(g):
    c, p = C.story("kor_a24_kneel_hammer")
    u = hammer_u(g)
    arm, ang = _arm(u)
    p["arm_r"] = arm
    p["prop_r"] = dict(type="hammer24", angle=ang)
    p["blink"] = blink(g, [22, 58])
    p["t"] = g / 30.0
    return p


def pose_kd(g):
    c, p = C.story("kor_d24_stand_carry_spikes")
    p["mirror"] = True                            # faces screen-left, toward the ship
    p["lean"] = p.get("lean", 0) + 0.8 * math.sin(g * 0.11 + 1.0)
    p["head_roll"] = 1.5 * math.sin(g * 0.07)
    p["gaze"] = (0.6, -0.4)                       # looking up at the roof
    p["blink"] = blink(g, [40])
    p["t"] = g / 30.0
    return p


def pose_yi(g):
    c, p = C.story("yi24_stand_arms_behind")
    # (not mirrored: yaw 0.3 turns him screen-right, toward the workers on the roof)
    p["lean"] = 1.2 * math.sin(g * 0.09)          # slight idle sway; feet planted
    p["head_roll"] = -2.0 + 1.5 * math.sin(g * 0.06 + 0.7)
    p["pitch"] = -0.25 + 0.04 * math.sin(g * 0.08)   # looking up at the roof
    p["gaze"] = (0.6, -0.7)
    p["blink"] = blink(g, [30, 66])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, shot=1):
        C.Take.__init__(self, PRESET[shot], name="cam_s01")
        self.shot = shot
        if shot == 2:
            self.aim_sun(*CAM2_0)
        if shot == 1:
            sd = os.path.join(TMP, "sprites")
            self.yi = self.actors["yi"] = C.make_actor("yi", "yi24", sd)
            self.kd = self.actors["kd"] = C.make_actor("kd", "kor_d24", sd, contact=False)
            self.ka = self.actors["ka"] = C.make_actor("ka", "kor_a24", sd, story="kor_a24_kneel_hammer", contact=False)
            self.roof_lp = tuple(self.A["parented"][ROOF_MARK]["local"])
            C.parent_to_ship(self.ka, "turtle")
            self.ka.yaw_fixed = KA_YAW                  # card along the ship (see KA_YAW)
            self.roofc = C.roof_contact(self.ka, "turtle", self.roof_lp)
            y = -0.99 * J.t_ye(KD_X)
            self.kd_lp = (KD_X, y, J.roof_z(KD_X, y))
            C.parent_to_ship(self.kd, "turtle")
            self.roofc_d = C.roof_contact(self.kd, "turtle", self.kd_lp, width=0.9, depth=0.45)

    def pose(self, shot, gs):
        assert shot == self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            if shot == 1:
                self.key_set(f, spikes=2, ports=0, dragon_smoke=0.0)
                C.place(self.yi, f, YI)
                C.place_on_ship(self.kd, f, self.kd_lp)
                C.place_on_ship(self.ka, f, self.roof_lp)
            else:
                lvl = 0.0 if g < G_SMOKE else (lerp(0.35, 0.85, ez((g - G_SMOKE) / 16.0)) if g < G_PUFF - 6
                                               else lerp(0.85, 1.2, ez((g - G_PUFF + 6) / 10.0)))
                self.key_set(f, spikes=2, ports=0, dragon_smoke=lvl, smoke_start=bf(2, G_SMOKE), smoke_speed=SMOKE_SPEED)
        if shot != 1:
            return
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.yi.pose(f, pose_yi(g), camera=self.cam)
            self.kd.pose(f, pose_kd(g), camera=self.cam)
            self.ka.pose(f, pose_ka(g), camera=self.cam)
        fs = [bf(shot, g) for g in gs]
        self.sprites_for([(self.yi, PPD["yi"]), (self.kd, PPD["kd"]), (self.ka, PPD["ka"])], fs)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        r = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                 pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f),
                 feet=C.feet_report(self, f))
        if shot == 1:
            r["hammer_u"] = round(hammer_u(g), 2)
        return r

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take(shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        for shot in shots:                     # samples: the preset's own count (joseon PRESETS 'samples', 24 by default; macro_dragon 16)
            samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples(PRESET[shot])
            C.final_loop(lambda s_: Take(s_), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
