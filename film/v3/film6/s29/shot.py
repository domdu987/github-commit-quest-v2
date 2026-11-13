#!/usr/bin/env python3
"""shot.py -- film 6 take s29: shots 29-30 (81.58-86.24 s = g 2447..2586) + 6-frame handles (g 2441..2592), market AFTERNOON.

    shot 29  g 2447..2525  "ตาชั่งค่อย ๆ เอียงลง ผ่านพอดี"
        29a  g 2441..2484  big_scale_insert (slow push): the bread pan with 13 loaves (the paler 13th on top) hangs high at -7
                           (short), then the beam slowly tips: -7 held to g 2455, eases to +6 by g 2492, a small overshoot (+7.2,
                           g 2497) and settles at +6 (g 2506).  The pan sinks ~180 px through the frame.
        29b  g 2485..2525  cut on "ผ่านพอดี" (82.73 s = g 2485): low wide from the south-west under the whole balance -- the beam
                           tilted toward the bread, the pan down; kit beside the pan (hands clasped, hopeful) springs into a proud
                           grin (fists on hips) at g 2497; two townsfolk far behind still hold their rotten veg up.
    shot 30  g 2526..2586  "ลุงเฮนรี่ยืน หน้าซีด ผู้ตรวจ พยักหน้าช้า ๆ"
        30a  g 2526..2556  low medium at the foot of the pillory steps: henry held by both arms between guard1 (left) and guard2
                           (right); the colour drains from his face (pale 0.55 -> 1.0 on "หน้าซีด" g 2529..2541), sweat, a small
                           head tremble; woman1 / man1 at the sides slowly LOWER their raised tomato / cabbage (g 2532..2552).
        30b  g 2557..2592  low on inspector_royal in front of the big balance: one slow nod (cast6.NOD, 5 frames per key, g 2563..
                           2588) on "พยักหน้าช้า ๆ" (85.27 s = g 2561), looking down at kit (left foreground, beaming up at him).
Mouths: nobody speaks (no quoted line in 29-30): every mouth is the static mouth of its expression (talk_* poses overridden).
NO depth of field (client rule): C.Take switches it off at build and before every render.

    python3 shot.py probe 29,30 a:b[:step]
    python3 shot.py stills 29,30 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 29,30 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing (film frames g)
G0, G1 = C.g_bound(81.58), C.g_bound(86.24)     # 2447, 2587
G30 = C.g_bound(84.20)                          # 2526
H = 6
RANGES = {29: (G0 - H, G30 - 1), 30: (G30, G1 - 1 + H)}
G_CUT29 = C.g_of(82.73) - 1                     # 2485 "ผ่านพอดี": 29b starts here (2484 = last 29a frame)
G_CUT29 = 2485
G_CUT30 = 2557
TIP = (2455, 2492)                              # -7 -> +6
G_PROUD = 2497
G_PALE = (C.g_of(84.19), C.g_of(84.19) + 12)    # 2529 .. 2541
G_LOWER = (2532, 2552)
G_NOD0 = C.g_of(85.27) + 2                      # 2563
NOD_STEP = 5


def bf(shot, g):
    return (0 if shot == 29 else 3000) + int(g) - 2400


def framing(shot, g):
    if shot == 29:
        return "29a" if g < G_CUT29 else "29b"
    return "30a" if g < G_CUT30 else "30b"


def beam_angle(g):
    if g <= TIP[0]:
        return -7.0
    if g <= TIP[1]:
        return lerp(-7.0, 6.0, ez((g - TIP[0]) / float(TIP[1] - TIP[0]), "sine"))
    # small overshoot + settle
    u = (g - TIP[1]) / 14.0
    if u >= 1.0:
        return 6.0
    return 6.0 + 1.2 * math.sin(math.pi * u) * (1 - 0.3 * u)


# ----------------------------------------------------------------------------- cameras (loc, look, lens) per framing, start -> end
CAMS = {
    "29a": (((2.30, 1.30, 2.50), (3.00, 6.00, 3.55)), ((2.42, 1.85, 2.42), (3.00, 6.00, 3.40)), 24.0, (G0 - H, G_CUT29 - 1)),
    "29b": (((0.30, 0.40, 1.15), (4.40, 6.00, 2.75)), ((0.60, 0.95, 1.15), (4.40, 6.00, 2.70)), 22.0, (G_CUT29, G30 - 1)),
    "30a": (((-3.10, -1.40, 1.60), (-4.00, 6.20, 3.10)), ((-3.15, 0.10, 1.55), (-4.00, 6.20, 3.00)), 24.0, (G30, G_CUT30 - 1)),
    "30b": (((2.45, -0.60, 1.85), (3.95, 4.45, 2.55)), ((2.60, 0.20, 1.85), (4.00, 4.45, 2.60)), 24.0, (G_CUT30, G1 - 1 + H)),
}


def cam_at(shot, g):
    fr = framing(shot, g)
    (l0, k0), (l1, k1), lens, (a, b) = CAMS[fr]
    u = ez((g - a) / float(max(1, b - a)), "sine")
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lens


# ----------------------------------------------------------------------------- staging (market world D)
KIT_29 = (4.15, 4.25)
TOWN_29 = {"woman1": (1.6, 11.0), "man1": (9.4, 10.6)}
HENRY_30 = (-4.0, 5.55)
GUARD1_30 = (-5.20, 5.15)
GUARD2_30 = (-2.80, 5.15)
TOWN_30 = {"woman1": (-6.95, 8.1), "man1": (-1.6, 9.6)}
INSP_30 = (4.45, 4.45)
KIT_30 = (3.00, 4.10)

WHO = {"29a": [], "29b": ["kit"], "30a": ["henry", "guard1", "guard2", "woman1", "man1"],
       "30b": ["inspector", "kit"]}


def no_mouth(p):
    p = dict(p)
    p.pop("mouth", None)
    return p


def story(name):
    return dict(cast6.STORY6[name][1])


# ----------------------------------------------------------------------------- poses
def kit29(g):
    u = ez((g - G_PROUD) / 6.0) if g >= G_PROUD else 0.0
    if u <= 0.0:
        p = story("kit_watch_steam")
        p.update(expr="worried", yaw=-0.45, pitch=-0.35, gaze=(-0.7, -0.7), head_roll=-4 + 2 * math.sin(g * 0.3))
    else:
        p = story("kit_proud")
        p.update(gaze=(-0.4, -0.5), yaw=-0.30)
        p["squash"] = (1.0 - 0.06 * math.sin(math.pi * clamp(u * 1.5)), 1.0 + 0.06 * math.sin(math.pi * clamp(u * 1.5)))
    p["blink"] = blink(g, [G_PROUD - 1, 2518])
    p["t"] = g / 30.0
    return no_mouth(p)


def town_veg(c, g, frame_lower=None, yaw_sign=1):
    """raised veg (town_raise_veg without the shout); lowered over frame_lower=(a, b)."""
    p = story("town_raise_veg" if c == "woman1" else "town_raise_veg_man1")
    p = no_mouth(p)
    p["expr"] = "angry"
    u = 0.0
    if frame_lower:
        a, b = frame_lower
        u = ez((g - a) / float(b - a)) if g >= a else 0.0
    hx, hy = lerp((0.66, -0.74), (0.46, 0.62), u)
    p["arm_r"] = dict(hand=(hx, hy), bend=lerp(-1.0, 0.4, u), stretch=1.3, layer="top")
    p["arm_l"] = dict(hand=lerp((-0.50, 0.40), (-0.30, 0.70), u), bend=0.4, shape="open", stretch=1.2)
    p["pitch"] = lerp(-0.45, 0.10, u)
    p["yaw"] = yaw_sign * 0.40
    p["lean"] = lerp(-6, 2, u)
    if u > 0.3:
        p["expr"] = "stunned" if u < 0.9 else "neutral"
    p["blink"] = blink(g, [2470 + (7 if c == "man1" else 0), 2545 + (3 if c == "man1" else 0)])
    p["t"] = g / 30.0
    return p


def henry30(g):
    p = no_mouth(story("henry_dragged"))
    p["expr"] = "stunned"
    p["arm_r"] = dict(hand=(0.88, 1.00), bend=-0.3, shape="open", stretch=1.3)
    p["arm_l"] = dict(hand=(-0.88, 1.02), bend=0.3, shape="open", stretch=1.3)
    u = ez((g - G_PALE[0]) / float(G_PALE[1] - G_PALE[0])) if g >= G_PALE[0] else 0.0
    p["pale"] = lerp(0.55, 1.0, u)
    p["head_roll"] = 3 + 2.5 * math.sin(g * 1.9) * (0.4 + 0.6 * u)      # trembling
    p["pitch"] = lerp(-0.10, 0.15, u)
    p["yaw"] = 0.05
    p["lean"] = -2
    p["blink"] = blink(g, [2527, 2548])
    p["t"] = g / 30.0
    return p


def guard30(c, g, side):
    p = no_mouth(story("guard_drag" if c == "guard1" else "guard_drag_guard2"))
    p["expr"] = "determined"
    if side < 0:            # guard2, right of henry, facing screen-left: mirror the pose by hand
        p["yaw"] = -0.55
        p["lean"] = 6
        p["arm_l"] = dict(hand=(-0.80, 0.30), bend=0.5, stretch=1.3, shape="open")
        p["arm_r"] = dict(hand=(0.30, 0.55), bend=-0.4)
        p.pop("prop_l", None)
        p["prop_r"] = dict(type="spear", angle=-110)
        p["head_roll"] = 4
    p["legs"] = "wide"
    p["blink"] = blink(g, [2535 + (9 if side < 0 else 0)])
    p["t"] = g / 30.0
    return p


def insp30(g):
    p = no_mouth(story("inspector_nod"))
    p["expr"] = "determined"
    k = (g - G_NOD0) / float(NOD_STEP)
    nod = 0.0
    if 0 <= k < len(cast6.NOD) - 1:
        i = int(k)
        nod = lerp(cast6.NOD[i], cast6.NOD[i + 1], ez(k - i))
    p["pitch"] = 0.15 + nod
    p["yaw"] = -0.35
    p["gaze"] = (-0.6, 0.6)
    if g >= G_NOD0 + 6:
        p["expr"] = "smug"                          # the grudging approval sets in on the way down (static mouth)
    p["blink"] = blink(g, [G_NOD0 + 5])
    p["t"] = g / 30.0
    return p


def kit30(g):
    p = no_mouth(story("kit_proud"))
    p.update(yaw=0.45, pitch=-0.55, gaze=(0.6, -0.8), head_roll=-6, expr="grinning")
    p["arm_r"] = dict(hand=(0.30, 0.70), bend=0.6)
    p["arm_l"] = dict(hand=(-0.25, 0.72), bend=-0.6)
    p["blink"] = blink(g, [2575])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
PPD = {"kit": 288, "woman1": 96, "man1": 96, "henry": 224, "guard1": 224, "guard2": 224, "inspector": 320}


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=24.0, name="cam_s29")
        sd = os.path.join(TMP, "sprites")
        for n, c in (("kit", "kit"), ("woman1", "woman1"), ("man1", "man1"), ("henry", "henry"), ("guard1", "guard1"),
                     ("guard2", "guard2"), ("inspector", "inspector_royal")):
            cv = None
            if n in ("guard1", "guard2"):
                cv = (-2.25, -5.5, 2.25, 0.125) if n == "guard1" else (-2.25, -5.0625, 2.25, 0.125)
            self.actors[n] = C.make_actor(n, c, sd, cv)
            self.actors[n].set_hidden(True)

    def show_for(self, shot, g):
        who = WHO[framing(shot, g)]
        for n, a in self.actors.items():
            a.set_hidden(n not in who)

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            self.key_cam(f, loc, look, lens)
            B.set_loaves(13, frame=f)
            B.set_big_scale(beam_angle(g) if shot == 29 else 6.0, frame=f)
            self.key_set(f, oven=1.0)
            fr = framing(shot, g)
            if fr == "29b":
                C.place(A["kit"], f, KIT_29)
                for c, xy in TOWN_29.items():
                    C.place(A[c], f, xy)
            elif fr == "30a":
                C.place(A["henry"], f, HENRY_30)
                C.place(A["guard1"], f, GUARD1_30)
                C.place(A["guard2"], f, GUARD2_30)
                for c, xy in TOWN_30.items():
                    C.place(A[c], f, xy)
            elif fr == "30b":
                C.place(A["inspector"], f, INSP_30)
                C.place(A["kit"], f, KIT_30)
        jobs = {}
        for g in gs:
            f = bf(shot, g)
            fr = framing(shot, g)
            self.scene.frame_set(f)
            if fr == "29b":
                A["kit"].pose(f, kit29(g), camera=self.cam)
                A["woman1"].pose(f, town_veg("woman1", g, None, 1), camera=self.cam)
                A["man1"].pose(f, town_veg("man1", g, None, -1), camera=self.cam)
            elif fr == "30a":
                A["henry"].pose(f, henry30(g), camera=self.cam)
                A["woman1"].pose(f, town_veg("woman1", g, G_LOWER, 1), camera=self.cam)
                A["man1"].pose(f, town_veg("man1", g, (G_LOWER[0] + 3, G_LOWER[1] + 3), -1), camera=self.cam)
            elif fr == "30b":
                A["inspector"].pose(f, insp30(g), camera=self.cam)
                A["kit"].pose(f, kit30(g), camera=self.cam)
            for n in WHO[fr]:
                if n not in ("guard1", "guard2"):
                    jobs.setdefault(n, []).append(f)
        for n, frs in jobs.items():
            self.sprites_for([(A[n], PPD[n])], frs)
        # guards grab henry's hands: pin their open hands on henry's drawn hands (henry's anchors are known now)
        gj = []
        for g in gs:
            if framing(shot, g) != "30a":
                continue
            f = bf(shot, g)
            self.scene.frame_set(f)
            an = self.anch[("henry", f)]
            hl = actors.local_to_world(A["henry"], an["hand_l"], f, A["henry"].feet.get(f), self.cam)
            hr = actors.local_to_world(A["henry"], an["hand_r"], f, A["henry"].feet.get(f), self.cam)
            A["guard1"].pose(f, guard30("guard1", g, 1), hands={"r": {"hand": tuple(hl), "bend": -0.5, "stretch": 1.3}},
                             camera=self.cam)
            A["guard2"].pose(f, guard30("guard2", g, -1), hands={"l": {"hand": tuple(hr), "bend": 0.5, "stretch": 1.3}},
                             camera=self.cam)
            gj.append(f)
        if gj:
            self.sprites_for([(A["guard1"], PPD["guard1"]), (A["guard2"], PPD["guard2"])], gj)

    def report(self, shot, g):
        f = bf(shot, g)
        self.show_for(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(shot, g)
        out = dict(shot=shot, g=g, framing=framing(shot, g), cam=[round(c, 3) for c in loc], lens=lens,
                   beam=round(beam_angle(g) if shot == 29 else 6.0, 2), heads=C.head_report(self, f))
        pan = B.STATE["big"]["pans"][0]
        out["pan_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(pan.matrix_world.translation), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        res = []
        for g in gs:
            self.show_for(shot, g)
            res += C.Take.render(self, [bf(shot, g)], out_dir, scale=scale, samples=samples, threads=threads)
        return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
