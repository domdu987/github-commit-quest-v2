#!/usr/bin/env python3
"""shot.py -- film 6 take s05: shots 5-6 (plan 8.62-15.34 s = g 259..459) + 6 handle frames each side (g 253..465).
Transition in: DISSOLVE from the bakery (shot 4); out: cut to shot 7 (bakery).

    shot 5  market MORNING, establishing (narration "คืออย่างนี้ อังกฤษเมื่อเจ็ดร้อยปีก่อน")
      sid 1  g 253..312  market_wide: high over the square, slow crane down + push: timber houses, stalls, bunting, the
                         balance, the (empty) pillory, a market crowd strolling (walk cycles) and standing in groups.
      sid 2  g 313..359  eye level in the square (square_eye family): townsfolk cross the frame, a guard by the balance,
                         bunting overhead; slow lateral drift.
    shot 6  market AFTERNOON (the busts happen in the afternoon sun: shot 20), pillory ("ร้านไหนขายขนมปังน้ำหนักขาด
            จะถูกจับใส่ขื่อ ให้คนทั้งตลาดปาผักเน่าใส่")
      sid 3  g 360..414  medium, slightly low: baker2 locked in the pillory (cast6 board; the set's 3D board is cut away at
                         runtime), sad; a rotten tomato flies in from screen-left and SPLATS on the board beside his head
                         (g 392, cartoon splat), he flinches; slow push.
      sid 4  g 415..465  wider, from behind two townsfolk in the foreground: woman1 laughing + pointing, man1 raises a rotten
                         cabbage, throws (g 433..436) -> it arcs to the pillory and splats (g 446, "เน่าใส่" 14.80 s = g 447),
                         baker2 flinches, man1 laughs.  Comic, no injury: the veg splats on the board and the cap.
Mouths: no quoted line here -> every mouth is the static mouth of its expression (laughing faces are static drawings).
NO depth of field; the set's blurred sky is replaced by a sharp redraw (mk.sharp_sky).

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
G5, G6, G7 = C.g_bound(8.62), C.g_bound(12.00), C.g_bound(15.34)       # 259, 360, 460
H = 6
G_5B = 313
G_6B = 415
TOMATO_HIT = 392
CABBAGE_THROW = (433, 436)
CABBAGE_HIT = 446


def strip_mouth(p):
    p = dict(p); p.pop("mouth", None); return p


def facing_of(T, a, b, f):
    pa = C.render.world_to_screen(T.cam, tuple(a), f); pb = C.render.world_to_screen(T.cam, tuple(b), f)
    return 1 if pb[0] >= pa[0] else -1


class Walkers(object):
    """people strolling on straight lines (walk cycle, travel ~0.5 D per step) or standing with a little life."""

    def __init__(self, T, spec, ppd):
        self.T, self.spec, self.ppd = T, spec, ppd
        self.a = {}
        for s in spec:
            self.a[s["name"]] = C.make_actor(s["name"], s["cast"], T.sd)
            T.actors[s["name"]] = self.a[s["name"]]

    def pos(self, s, g):
        if "to" not in s:
            return s["at"]
        u = (g - s.get("g0", 0)) * s.get("speed", 0.036)
        a, b = Vector(s["at"]), Vector(s["to"])
        d = (b - a); L = d.length
        u = max(0.0, min(L, u))
        return tuple(a + d.normalized() * u)

    def place(self, g, f):
        for s in self.spec:
            p = self.pos(s, g)
            C.place(self.a[s["name"]], f, (p[0], p[1]), 0.0)

    def pose(self, g, f):
        for i, s in enumerate(self.spec):
            a = self.a[s["name"]]
            if "to" in s:
                fc = facing_of(self.T, Vector(s["at"]) + Vector((0, 0, 1.5)), Vector(s["to"]) + Vector((0, 0, 1.5)), f)
                p = cast6.cycle(s["cast"], (g + 7 * i) / 28.0, "walk", facing=fc, base=dict(expr=s.get("expr", "happy")))
            else:
                p = strip_mouth(s["pose"]) if isinstance(s.get("pose"), dict) else strip_mouth(cast6.STORY6[s["pose"]][1])
                p["head_roll"] = p.get("head_roll", 0) + 3 * math.sin(g * 0.09 + i)
                p["yaw"] = p.get("yaw", 0) + 0.06 * math.sin(g * 0.05 + 2 * i)
            p["blink"] = blink(g, [(17 * i + 23) % 60 + 250, (17 * i + 23) % 60 + 310, (17 * i + 23) % 60 + 370])
            p["t"] = g / 30.0
            a.pose(f, p, camera=self.T.cam)

    def jobs(self):
        return [(a, self.ppd) for a in self.a.values()]


# ============================================================================= shot 5
class Wide(mk.MShot):
    SID, PRESET, G = 1, "MORNING", (G5 - H, G_5B - 1)
    CA = ((11.0, -14.5, 15.5), (-3.0, 9.0, 3.6))
    CB = ((8.6, -12.2, 11.4), (-3.4, 8.0, 3.9))
    LENS = 22.0

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        spec = [
            dict(name="w1", cast="woman1", at=(-6.0, 1.0, 0), to=(5.0, -1.0, 0), g0=250),
            dict(name="m1", cast="man1", at=(7.0, 2.5, 0), to=(-4.0, 3.5, 0), g0=250, expr="smirk"),
            dict(name="w2", cast="woman1", at=(1.0, -1.5, 0), to=(-4.0, 5.5, 0), g0=250),
            dict(name="m2", cast="man1", at=(3.0, 0.5, 0), to=(9.0, 9.0, 0), g0=250, expr="smirk"),
            dict(name="g1", cast="guard1", at=(-5.8, 6.0, 0), pose="guard_stand"),
            dict(name="g2", cast="guard2", at=(8.5, 3.0, 0), pose="guard_stand_guard2"),
            dict(name="w3", cast="woman1", at=(-1.5, 6.5, 0), pose="town_point"),
            dict(name="m3", cast="man1", at=(-0.4, 7.2, 0), pose="town_laugh_man1"),
            dict(name="w4", cast="woman1", at=(2.0, 2.5, 0), pose=dict(yaw=-0.4, expr="happy", arm_r="down", arm_l="akimbo", legs="stand")),
            dict(name="m4", cast="man1", at=(0.9, 1.7, 0), pose=dict(yaw=0.4, expr="smirk", arm_r="akimbo", arm_l="down", legs="stand")),
            dict(name="w5", cast="woman1", at=(-9.0, 4.0, 0), to=(-9.0, 14.0, 0), g0=250),
            dict(name="m5", cast="man1", at=(12.0, 12.0, 0), to=(4.0, 14.0, 0), g0=250, expr="happy"),
        ]
        self.W = Walkers(self, spec, 64)

    def place_g(self, g, f):
        self.W.place(g, f)
        C.B.set_big_scale(0.0, frame=f)

    def pose_g(self, g, f):
        self.W.pose(g, f)

    def jobs(self):
        return self.W.jobs()


class Square(mk.MShot):
    SID, PRESET, G = 2, "MORNING", (G_5B, G6 - 1)
    CA = ((2.4, -4.0, 2.7), (0.2, 12.0, 4.0))
    CB = ((0.9, -3.6, 2.65), (-0.6, 12.0, 4.0))
    LENS = 22.0

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        spec = [
            dict(name="w1", cast="woman1", at=(-4.5, 1.6, 0), to=(4.0, 1.4, 0), g0=300),
            dict(name="m1", cast="man1", at=(5.0, 4.2, 0), to=(-4.0, 4.6, 0), g0=290, expr="smirk"),
            dict(name="g1", cast="guard1", at=(4.2, 7.6, 0), pose="guard_stand"),
            dict(name="w2", cast="woman1", at=(-2.6, 7.4, 0), pose="town_point"),
            dict(name="m2", cast="man1", at=(-1.4, 7.8, 0), pose="town_laugh_man1"),
            dict(name="g2", cast="guard2", at=(-6.6, 7.0, 0), pose="guard_stand_guard2"),
        ]
        self.W = Walkers(self, spec, 144)

    def place_g(self, g, f):
        self.W.place(g, f)
        C.B.set_big_scale(0.0, frame=f)

    def pose_g(self, g, f):
        self.W.pose(g, f)

    def jobs(self):
        return self.W.jobs()


# ============================================================================= shot 6
STAND = (-4.0, 9.40)          # baker2's feet on the platform (z 1.0), just in front of the (cut away) set board
VEG_BOX = (-0.22, -0.22, 0.22, 0.22)


def bezier(a, b, h, u):
    a, b = Vector(a), Vector(b)
    m = (a + b) / 2 + Vector((0, 0, h))
    return tuple((1 - u) ** 2 * a + 2 * (1 - u) * u * m + u * u * b)


class PilloryShot(mk.MShot):
    PRESET = "AFTERNOON"
    CUT_BOARD = True

    def setup_pillory(self, ppd):
        self.baker = C.make_actor("baker2", "baker2", self.sd)
        self.actors["baker2"] = self.baker
        self.ppd = ppd
        vs = [cast6.tomato_svg("tm%d" % k, r=0.12, rot=45 * k) for k in range(4)]
        self.tomato = self.card("tomato", vs, VEG_BOX, scale=1.0, shadow=True)
        cs = [cast6.cabbage_svg("cb%d" % k, r=0.16, rot=60 * k) for k in range(4)]
        self.cabbage = self.card("cabbage", cs, VEG_BOX, scale=1.0, shadow=True)
        self.splats = {}

    def splat(self, name, kind, k, seed):
        pc = self.card(name, [mk.splat_svg(name, kind, k, seed)], (-0.42, -0.36, 0.42, 0.36), scale=1.0, shadow=False)
        self.splats[name] = pc
        return pc

    def fly(self, pc, g, g0, g1, a, b, h, f, face, spin=1):
        if g0 <= g < g1:
            u = (g - g0) / float(g1 - g0)
            pc.put(bezier(a, b, h, u), face=face, frame=f)
            pc.show((g * spin) % 4, frame=f)
        else:
            pc.put(b, face=face, frame=f)
            pc.show(None, frame=f)

    def stick(self, pc, g, gh, pos, f, face):
        pc.put(pos, face=face, frame=f)
        pc.show(0 if g >= gh else None, frame=f)

    def baker_pose(self, g, hits):
        fl = 0.0
        for gh in hits:
            fl = max(fl, pulse(g, gh, gh + 1, gh + 9, 1.0))
        expr = "shouting" if fl > 0.5 else ("worried" if any(gh <= g < gh + 22 for gh in hits) else "sad")
        p = mk.pillory_pose("baker2", g, shake=0.06, phase=0.3, expr=expr, flinch=fl)
        p["blink"] = blink(g, [372, 420, 455])
        if fl > 0.3:
            p["fx"] = ["sweat"]
        return p


class Hit(PilloryShot):
    SID, G = 3, (G6, G_6B - 1)
    CA = ((-2.75, 5.35, 1.75), (-4.0, 9.5, 3.55))
    CB = ((-3.05, 6.05, 2.05), (-4.0, 9.5, 3.62))
    LENS = 26.0

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        self.setup_pillory(288)
        self.splat("splat_t", "tomato", 1.0, 3)

    def place_g(self, g, f):
        face = self.camv(g)[0]
        C.place(self.baker, f, STAND, 1.0)
        hit = (-4.55, 9.30, 3.45)
        self.fly(self.tomato, g, TOMATO_HIT - 9, TOMATO_HIT, (-8.5, 7.5, 3.2), hit, 1.2, f, face)
        self.stick(self.splats["splat_t"], g, TOMATO_HIT, (-4.55, 9.28, 3.36), f, face)
        self.cabbage.put((0, 0, -5), frame=f); self.cabbage.show(None, frame=f)

    def pose_g(self, g, f):
        self.baker.pose(f, self.baker_pose(g, [TOMATO_HIT]), camera=self.cam)

    def jobs(self):
        return [(self.baker, self.ppd)]


class Throw(PilloryShot):
    SID, G = 4, (G_6B, G7 - 1 + H)
    CA = ((-3.90, 1.20, 2.15), (-3.90, 9.5, 3.70))
    CB = ((-3.90, 1.75, 2.20), (-3.90, 9.5, 3.75))
    LENS = 24.0
    WOMAN = (-5.05, 6.30)
    MAN = (-2.80, 6.25)

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        self.setup_pillory(192)
        self.splat("splat_t", "tomato", 1.0, 3)
        self.splat("splat_c", "cabbage", 1.15, 8)
        self.woman = C.make_actor("woman1", "woman1", self.sd); self.actors["woman1"] = self.woman
        self.man = C.make_actor("man1", "man1", self.sd); self.actors["man1"] = self.man

    def place_g(self, g, f):
        face = self.camv(g)[0]
        C.place(self.baker, f, STAND, 1.0)
        C.place(self.woman, f, self.WOMAN, 0.0)
        C.place(self.man, f, self.MAN, 0.0)
        self.stick(self.splats["splat_t"], g, 0, (-4.55, 9.28, 3.36), f, face)
        self.stick(self.splats["splat_c"], g, CABBAGE_HIT, (-3.55, 9.27, 3.40), f, face)
        start = (self.MAN[0] - 0.55, self.MAN[1] + 0.1, 3.55)
        self.fly(self.cabbage, g, CABBAGE_THROW[1], CABBAGE_HIT, start, (-3.55, 9.30, 3.45), 1.4, f, face, spin=1)
        self.tomato.put((0, 0, -5), frame=f); self.tomato.show(None, frame=f)

    def pose_g(self, g, f):
        self.baker.pose(f, self.baker_pose(g, [CABBAGE_HIT]), camera=self.cam)
        # woman1: laughing and pointing at the pillory (screen-left of her is the pillory? she is left of it: point right)
        pw = strip_mouth(cast6.STORY6["town_laugh"][1])
        pw.update(mirror=True, yaw=0.35, head_roll=-8 + 4 * math.sin(g * 0.35), lean=-4 + 3 * math.sin(g * 0.35),
                  blink=blink(g, [425, 458]), t=g / 30.0)
        self.woman.pose(f, pw, camera=self.cam)
        # man1 (screen-right of the pillory): raise the cabbage, throw toward screen-left, then laugh
        if g < CABBAGE_THROW[0]:
            pm = strip_mouth(cast6.STORY6["town_raise_veg_man1"][1]); pm.update(expr="smirk", mirror=True, yaw=-0.40)
            pm["arm_r"] = dict(pm["arm_r"], hand=(0.66, -0.74 - 0.08 * math.sin(g * 0.4)))
        elif g <= CABBAGE_THROW[1]:
            pm = strip_mouth(cast6.STORY6["town_throw_man1"][1]); pm.update(expr="grinning", mirror=True, yaw=-0.55)
        else:
            pm = strip_mouth(cast6.STORY6["town_laugh_man1"][1])
            pm.update(yaw=0.35, mirror=False, head_roll=10 + 4 * math.sin(g * 0.4), lean=-5 + 3 * math.sin(g * 0.4))
            pm["arm_l"] = dict(pm["arm_l"])
        pm["blink"] = blink(g, [418, 452]); pm["t"] = g / 30.0
        self.man.pose(f, pm, camera=self.cam)

    def jobs(self):
        return [(self.baker, self.ppd), (self.woman, 256), (self.man, 256)]


CLASSES = {1: Wide, 2: Square, 3: Hit, 4: Throw}
for _c in CLASSES.values():
    _c.HERE = HERE

if __name__ == "__main__":
    mk.run(CLASSES, sys.argv, HERE)
