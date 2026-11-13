#!/usr/bin/env python3
"""shot.py -- film 6 take s03: shot 3 (plan 3.60-6.00 s = g 108..179) + 6 handle frames each side (g 102..185),
market AFTERNOON, the EMPTY pillory on its platform with crows on it; slow push; cut in, cut out.

    sid 1  g 102..143  low among the (absent) crowd, up at the empty pillory against the north row and sky (pillory_low family):
                       slow push.  Crow A on the post top (looks about), crow B on the board's left end pecking at a splat,
                       crow C on the right end caws (g 118..125), a fourth crow flaps across the sky right -> left.
    sid 2  g 144..185  punch-in (framing change at 1.2 s): closer, from the right, along the board with its three empty holes;
                       crow B hops to the neck hole (g 150..157) and pecks, crow C caws again (g 160..166), crow A takes off
                       from the post top (g 168..) and flaps out of frame up-left.  Slow push.
Nobody in frame (no mouths).  The crows are 2D cards (mk.crow_svg) in the 3D set, switched per frame.  NO depth of field.

    python3 shot.py probe|stills|final <sid> a:b[:step] [...]   (see mk.run)
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import common as C                                       # noqa: E402
import mk                                                # noqa: E402

ez, lerp = C.ez, mk.lerpv
G0, G1 = C.g_bound(3.60), C.g_bound(6.00)                # 108, 180 (shot 3 = g 108..179)
H = 6
G_SPLIT = 144                                            # punch-in
POSES = ["stand", "peck", "look", "caw", "flap_up", "flap_down"]
BOARD_Z = 3.35                                           # top of the pillory board (set: neck z 3.05 + 0.30)
BOARD_Y = 9.62
POST_TOP = (-4.0, 9.80, 4.60)
CROW_S = 1.15


def crow_cards(T, flips):
    for name, flip in flips.items():
        T.card(name, [mk.crow_svg("%s_%s" % (name, p), p, flip=flip) for p in POSES], mk.CROW_BOX, scale=CROW_S, shadow=True)


def show_crow(T, name, pose, pos, f, face):
    pc = T.cards[name]
    pc.put(pos, face=face, frame=f)
    pc.show(None if pose is None else POSES.index(pose), frame=f)


def peck_cycle(g, period=11, on=4, off=0):
    return "peck" if (g + off) % period < on else ("look" if (g + off) % (2 * period) < period + 3 and (g + off) % (2 * period) >= period else "stand")


class Push(mk.MShot):
    SID, PRESET, G = 1, "AFTERNOON", (G0 - H, G_SPLIT - 1)
    CA = ((-1.00, 4.05, 1.60), (-4.0, 9.6, 3.65))
    CB = ((-1.55, 5.05, 1.85), (-4.05, 9.6, 3.70))
    LENS = 24.0

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        crow_cards(self, dict(crowA=False, crowB=False, crowC=True, crowD=True))

    def place_g(self, g, f):
        face = self.camv(g)[0]
        a_pose = "look" if (g // 14) % 2 else "stand"
        show_crow(self, "crowA", a_pose, POST_TOP, f, face)
        show_crow(self, "crowB", peck_cycle(g), (-5.05, BOARD_Y, BOARD_Z), f, face)
        c_pose = "caw" if 118 <= g <= 125 else ("look" if g > 125 else "stand")
        show_crow(self, "crowC", c_pose, (-2.70, BOARD_Y, BOARD_Z), f, face)
        # a crow flapping across the sky, right -> left, behind the pillory
        u = (g - self.G[0]) / float(self.G[1] - self.G[0])
        x = lerp((4.0,), (-14.0,), u)[0]
        z = 8.6 + 0.6 * math.sin(u * 3.0) + 0.15 * math.sin(g * 1.3)
        show_crow(self, "crowD", "flap_up" if (g // 3) % 2 else "flap_down", (x, 15.0, z), f, face)


class Close(mk.MShot):
    SID, PRESET, G = 2, "AFTERNOON", (G_SPLIT, G1 - 1 + H)
    CA = ((-1.85, 6.30, 2.45), (-4.30, 9.65, 3.65))
    CB = ((-2.15, 6.80, 2.60), (-4.35, 9.65, 3.70))
    LENS = 26.0

    def camv(self, g):
        u = ez((g - self.G[0]) / float(self.G[1] - self.G[0]), "sine")
        return lerp(self.CA[0], self.CB[0], u), lerp(self.CA[1], self.CB[1], u), self.LENS

    def setup(self):
        crow_cards(self, dict(crowA=False, crowB=False, crowC=True))

    def place_g(self, g, f):
        face = self.camv(g)[0]
        # crow A: looks about, takes off at g 168 up and to screen-left
        if g < 168:
            show_crow(self, "crowA", "look" if (g // 12) % 2 else "stand", POST_TOP, f, face)
        else:
            u = (g - 168) / 14.0
            pos = (POST_TOP[0] - 0.3 - 2.2 * u, POST_TOP[1] - 0.2 * u, POST_TOP[2] + 0.25 + 2.6 * u * u + 0.9 * u)
            show_crow(self, "crowA", "flap_up" if (g // 2) % 2 else "flap_down", pos, f, face)
        # crow B: hop from the left end to beside the neck hole (g 150..157), then pecks at the splat there
        x0, x1 = -5.05, -4.45
        if g < 150:
            show_crow(self, "crowB", peck_cycle(g), (x0, BOARD_Y, BOARD_Z), f, face)
        elif g <= 157:
            u = (g - 150) / 7.0
            pos = (x0 + (x1 - x0) * ez(u), BOARD_Y, BOARD_Z + 0.35 * math.sin(math.pi * u))
            show_crow(self, "crowB", "flap_up" if g < 154 else "stand", pos, f, face)
        else:
            show_crow(self, "crowB", peck_cycle(g, 9, 4, 3), (x1, BOARD_Y, BOARD_Z), f, face)
        c_pose = "caw" if 160 <= g <= 166 else ("look" if (g // 10) % 2 else "stand")
        show_crow(self, "crowC", c_pose, (-3.40, BOARD_Y, BOARD_Z), f, face)     # nearer the post than in sid 1: the right end is cut by the frame here

    def extra_report(self, g):
        return dict(crows_px={n: [round(v, 1) for v in C.render.world_to_screen(self.cam, tuple(pc.root.location), self.bf(g))[:2]]
                              for n, pc in self.cards.items()})


CLASSES = {1: Push, 2: Close}
for _c in CLASSES.values():
    _c.HERE = HERE

if __name__ == "__main__":
    mk.run(CLASSES, sys.argv, HERE)
