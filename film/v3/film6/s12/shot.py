#!/usr/bin/env python3
"""shot.py -- film 6 take s12: shots 12-15 (plan 31.09-41.29 s = g 933..1238) + 6 handle frames each side (g 927..1244).
Transition in: DISSOLVE from the bakery (shot 11); out: cut to shot 16 (bakery).

    shot 12  market MORNING, square ("ทั้งตลาดเลย เรียกเขาว่า ไอ้สิบสาม")
      sid 1  g  927.. 968  two-shot: woman1 + man1 laugh (mouths move: the townsfolk laugh is allowed in shot 12) and point
                           screen-right at the boy passing; slow push.
      sid 2  g  969..1004  kit walks past with the basket of 13 loaves (walk cycle, the basket arm held), sheepish grin, the
                           two laughing and pointing behind him; the camera pans with him.
    shot 13  market AFTERNOON, pillory, week 1 ("สัปดาห์แรก ร้านข้าง ๆ โดนจับขึ้นขื่อ")
      sid 3  g 1005..1043  one head: baker2 locked in the pillory (cast6 board; the set board is cut away), sad, crow on the post
      sid 4  g 1044..1079  punch-in on his face; he sighs (head droops)
    shot 14  week 2 ("สัปดาห์ที่สอง อีกร้าน")
      sid 5  g 1080..1115  two heads (baker2 + baker3, a stout baker in brown)
      sid 6  g 1116..1151  closer two-shot from the right; baker3 turns to baker2, both sad
    shot 15  week 3 ("สัปดาห์ที่สาม อีกสองร้าน ทั้งที่ทุกร้านสาบานว่าชั่งมาเป๊ะ")
      sid 7  g 1152..1197  four heads in a row (baker2..baker5), all shaking their heads "I weighed exactly!"
      sid 8  g 1198..1244  track along the row, closer; heads shaking out of phase, crow on the post caws
Mouths: only the shot-12 laughs move; the bakers' mouths are the static mouths of their expressions (no quoted line).
NO depth of field; sharp sky redraw (mk.sharp_sky).

    python3 shot.py probe|stills|final <sid> a:b[:step] [...]   (see mk.run)
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import common as C                                       # noqa: E402
import mk                                                # noqa: E402
from mathutils import Vector                             # noqa: E402

ez, lerp, blink, pulse = C.ez, mk.lerpv, C.blink, C.pulse
cast6 = C.cast6
mk.register_bakers()
G12, G13, G14, G15, G16 = [C.g_bound(t) for t in (31.09, 33.51, 36.00, 38.40, 41.29)]   # 933 1005 1080 1152 1239
H = 6
POSES = ["stand", "peck", "look", "caw", "flap_up", "flap_down"]
POST_TOP = (-4.0, 9.80, 4.60)


def strip_mouth(p):
    p = dict(p); p.pop("mouth", None); return p


def laugh_mouth(g, seed=0):
    """a 'ha-ha-ha' rhythm: the laughing expression's own open mouth alternating with a rounder one every 3 frames."""
    return "talk_o" if ((g + seed) // 3) % 2 else None


class Push(mk.MShot):
    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS


# ============================================================================= shot 12
WOMAN, MAN = (0.15, 3.35), (1.25, 3.70)


def town_pose(cast, g, seed, point_dir=1):
    p = strip_mouth(cast6.STORY6["town_laugh" + ("_man1" if cast == "man1" else "")][1])
    p["mirror"] = point_dir > 0                      # the drawing points screen-left; mirror -> points screen-right
    p["yaw"] = 0.35 if point_dir > 0 else -0.35
    k = math.sin((g + seed) * 0.55)
    p["head_roll"] = (8 if point_dir > 0 else -8) + 4 * k
    p["lean"] = -5 + 3 * k
    p["pitch"] = -0.3 + 0.08 * k
    m = laugh_mouth(g, seed)
    if m:
        p["mouth"] = m
    p["blink"] = blink(g, [941 + seed, 990 + seed])
    p["t"] = g / 30.0
    return p


class Laugh(Push):
    SID, PRESET, G = 1, "MORNING", (G12 - H, 968)
    CA = ((0.95, -1.35, 2.75), (0.75, 6.0, 2.85))
    CB = ((0.85, -0.55, 2.70), (0.70, 6.0, 2.85))
    LENS = 28.0

    def setup(self):
        self.woman = C.make_actor("woman1", "woman1", self.sd); self.actors["woman1"] = self.woman
        self.man = C.make_actor("man1", "man1", self.sd); self.actors["man1"] = self.man

    def place_g(self, g, f):
        C.place(self.woman, f, WOMAN); C.place(self.man, f, MAN)
        C.B.set_big_scale(0.0, frame=f)

    def pose_g(self, g, f):
        self.woman.pose(f, town_pose("woman1", g, 0), camera=self.cam)
        self.man.pose(f, town_pose("man1", g, 4), camera=self.cam)

    def jobs(self):
        return [(self.woman, 256), (self.man, 256)]


class Pass(Push):
    SID, PRESET, G = 2, "MORNING", (969, G13 - 1)
    CA = ((-0.55, -2.30, 1.70), (-0.30, 6.0, 2.45))
    CB = ((0.05, -2.20, 1.70), (0.95, 6.0, 2.45))
    LENS = 26.0
    K0, K1 = (-1.05, 1.95), (1.35, 1.80)

    def setup(self):
        self.kit = C.make_actor("kit", "kit", self.sd); self.actors["kit"] = self.kit
        self.woman = C.make_actor("woman1", "woman1", self.sd); self.actors["woman1"] = self.woman
        self.man = C.make_actor("man1", "man1", self.sd); self.actors["man1"] = self.man

    def kit_xy(self, g):
        u = (g - self.G[0]) / float(self.G[1] - self.G[0])
        return lerp(self.K0, self.K1, u)

    def place_g(self, g, f):
        C.place(self.kit, f, self.kit_xy(g))
        C.place(self.woman, f, (WOMAN[0] - 0.9, WOMAN[1] + 0.9)); C.place(self.man, f, (MAN[0] - 0.6, MAN[1] + 1.2))
        C.B.set_big_scale(0.0, frame=f)

    def pose_g(self, g, f):
        base = strip_mouth(cast6.STORY6["kit_hold_basket"][1])
        base.update(expr="happy", basket=dict(loaves=13))
        p = cast6.cycle("kit", g / 26.0, "walk", facing=1, base=base, arms="l")
        p["arm_r"] = dict(hand=(0.5, 0.3), bend=-0.7, stretch=1.3)
        p["prop_r"] = "basket"; p["basket"] = dict(loaves=13)
        p["yaw"] = 0.25 - 0.45 * pulse(g, 978, 984, 994, 1.0)              # glances back at the laughers, then on
        p["gaze"] = (0.6 - 1.4 * pulse(g, 978, 984, 994, 1.0), -0.1)
        p["expr"] = "happy" if not (982 <= g <= 996) else "grinning"
        p["head_roll"] = p.get("head_roll", 0) - 4
        p["blink"] = blink(g, [975, 1000]); p["t"] = g / 30.0
        self.kit.pose(f, p, camera=self.cam)
        self.woman.pose(f, town_pose("woman1", g, 2), camera=self.cam)
        self.man.pose(f, town_pose("man1", g, 5), camera=self.cam)

    def jobs(self):
        return [(self.kit, 256), (self.woman, 176), (self.man, 176)]


# ============================================================================= shots 13-15: the pillory count
ROW = {1: [-4.0], 2: [-4.55, -3.45], 4: [-5.55, -4.50, -3.45, -2.40]}
NAMES = ["baker2", "baker3", "baker4", "baker5"]
EXPR = ["sad", "worried", "sad", "worried"]


class Count(Push):
    PRESET = "AFTERNOON"
    CUT_BOARD = True
    N = 1
    SHAKE = 0.0
    PPD = 192
    CROW = True

    def setup(self):
        self.b = []
        for i in range(self.N):
            a = C.make_actor(NAMES[i], NAMES[i], self.sd); self.actors[NAMES[i]] = a; self.b.append(a)
        if self.CROW:
            self.card("crow", [mk.crow_svg("crow_%s" % p, p) for p in POSES], mk.CROW_BOX, scale=1.15)

    def place_g(self, g, f):
        for i, a in enumerate(self.b):
            C.place(a, f, (ROW[self.N][i], 9.45 - 0.03 * i), 1.0)
        if self.CROW:
            pc = self.cards["crow"]
            pc.put(POST_TOP, face=self.camv(g)[0], frame=f)
            pc.show(POSES.index(self.crow_pose(g)), frame=f)

    def crow_pose(self, g):
        return "look" if (g // 13) % 2 else "stand"

    def baker_pose(self, i, g):
        shake = self.SHAKE
        p = mk.pillory_pose(NAMES[i], g, shake=shake, phase=1.7 * i, expr=EXPR[i])
        if shake == 0:
            p["yaw"] = 0.12 * math.sin(g * 0.05 + i)
        p["blink"] = blink(g, [1010 + 23 * i, 1070 + 17 * i, 1130 + 19 * i, 1190 + 13 * i, 1235 - 7 * i])
        return p

    def pose_g(self, g, f):
        for i, a in enumerate(self.b):
            a.pose(f, self.baker_pose(i, g), camera=self.cam)

    def jobs(self):
        return [(a, self.PPD) for a in self.b]


class Week1(Count):
    SID, G, N = 3, (G13, 1043), 1
    CA = ((-3.55, 3.95, 2.05), (-4.0, 9.5, 3.75))
    CB = ((-3.65, 4.55, 2.15), (-4.0, 9.5, 3.80))
    LENS = 24.0


class Week1Close(Count):
    SID, G, N = 4, (1044, G14 - 1), 1
    CA = ((-2.85, 6.55, 2.85), (-4.05, 9.5, 3.75))
    CB = ((-3.00, 6.85, 2.92), (-4.05, 9.5, 3.80))
    LENS = 30.0
    PPD = 320

    def baker_pose(self, i, g):
        p = Count.baker_pose(self, i, g)
        s = pulse(g, 1050, 1058, 1072, 1.0)                    # a long sigh: head droops
        p["pitch"] = 0.30 + 0.35 * s
        p["head_roll"] = p["head_roll"] - 6 * s
        return p


class Week2(Count):
    SID, G, N = 5, (G14, 1115), 2
    CA = ((-3.40, 4.10, 2.10), (-4.0, 9.5, 3.75))
    CB = ((-3.55, 4.70, 2.20), (-4.0, 9.5, 3.80))
    LENS = 24.0


class Week2Close(Count):
    SID, G, N = 6, (1116, G15 - 1), 2
    CA = ((-2.55, 6.15, 2.70), (-3.95, 9.5, 3.75))
    CB = ((-2.75, 6.55, 2.80), (-4.00, 9.5, 3.80))
    LENS = 28.0
    PPD = 288
    CROW = False

    def baker_pose(self, i, g):
        p = Count.baker_pose(self, i, g)
        if i == 1:                                              # baker3 turns to baker2 (screen-left), then back
            k = pulse(g, 1122, 1128, 1142, 1.0)
            p["yaw"] = -0.45 * k; p["gaze"] = (-0.8 * k, 0.0)
        if i == 0:
            k = pulse(g, 1128, 1134, 1146, 1.0)
            p["yaw"] = 0.35 * k; p["gaze"] = (0.7 * k, 0.1)
        return p


class Week3(Count):
    SID, G, N = 7, (G15, 1197), 4
    CA = ((-3.95, 3.05, 2.45), (-3.95, 9.5, 3.55))
    CB = ((-3.95, 3.65, 2.50), (-3.95, 9.5, 3.60))
    LENS = 24.0
    SHAKE = 0.42


class Week3Track(Count):
    SID, G, N = 8, (1198, G16 - 1 + H), 4
    CA = ((-5.70, 6.10, 2.85), (-4.90, 9.5, 3.75))
    CB = ((-2.60, 6.25, 2.85), (-3.20, 9.5, 3.75))
    LENS = 30.0
    SHAKE = 0.42
    PPD = 256

    def crow_pose(self, g):
        return "caw" if 1212 <= g <= 1219 or 1232 <= g <= 1238 else ("look" if (g // 11) % 2 else "stand")


CLASSES = {1: Laugh, 2: Pass, 3: Week1, 4: Week1Close, 5: Week2, 6: Week2Close, 7: Week3, 8: Week3Track}
for _c in CLASSES.values():
    _c.HERE = HERE

if __name__ == "__main__":
    mk.run(CLASSES, sys.argv, HERE)
