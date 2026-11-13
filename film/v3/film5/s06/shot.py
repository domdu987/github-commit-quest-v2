#!/usr/bin/env python3
"""shot.py -- film 5 take s06: shot 6 (plan t 14.38-17.63 = g 431..528), tunnel LAMP.  "ส่วนเขาเป็นเด็กเหมืองที่อายุน้อยที่สุด
ตัวเล็กพอ ๆ กับกรงนก" -- alfie, the youngest, the smallest among big miners, about as small as the bird cage.

    6a  g 424..465  (in-handle 424..430)  eye level on alfie (2.48 D) between the big miners (miner1 3.32, gaffer 3.31, miner3
                    3.38): he stands small in the middle holding the brass cage, the men tower round him; slow push  (ref a t0037)
    6b  g 466..497  hard cut, the height gag: from miner3's face high up, tilt down past his chest to alfie looking up at him
                    on "น้อยที่สุด" (g 478)
    6c  g 498..535  hard cut, medium on alfie and the cage side by side: he lifts it up beside his torso on "กับกรงนก" (g 516),
                    cage as big as his torso, the canary singing inside the bars; push in (out-handle 529..535)
The cage is ALWAYS the cast's 2D held cage (prop_r "cage" + pose key "bird", bars drawn over the bird); the set's 3D cage is
hidden.  Mouths closed.  NO depth of field (client rule).

Internal sub-shot ids 1 (6a), 2 (6b), 3 (6c).  python3 shot.py probe|stills|final <sids> <g spec> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5 as L                                        # noqa: E402
from lib5 import TP, Vector, ez, lerp, lerpv, clamp, blink, pulse, camkeys, g_of, bf  # noqa: E402
import cast5                                            # noqa: E402


class S(object):
    NAME = "s06"
    G0, G1, H = 431, 529, 7
    G_6B, G_6C = 466, 498
    RANGES = {1: (G0 - H, G_6B - 1), 2: (G_6B, G_6C - 1), 3: (G_6C, G1 + H - 1)}
    CAST = {"alfie": "alfie", "miner1": "miner1", "miner3": "miner3", "gaffer": "gaffer"}
    PPD = {1: {"alfie": 448, "miner1": 256, "miner3": 256, "gaffer": 192},
           2: {"alfie": 448, "miner3": 384, "miner1": 256},
           3: {"alfie": 640}}
    LAMP_NAMES = ("lamp_alfie", "lamp_gaffer", "lamp_m1")
    G_YOUNG = g_of(15.83)                                       # 478 "น้อยที่สุด"
    G_CAGE = g_of(17.10)                                        # 516 "กับกรงนก"

    ALFIE = TP(11.0, -0.85, 0)
    MINER1 = TP(11.15, -1.95, 0)
    MINER3 = TP(10.9, 0.25, 0)
    GAFFER = TP(12.4, -0.30, 0)

    @staticmethod
    def cam(sid, g):
        if sid == 1:
            return camkeys(g, [(424, TP(6.0, -0.75, 1.30), TP(11.0, -0.75, 2.15), "sine"),
                               (466, TP(6.7, -0.75, 1.32), TP(11.0, -0.75, 2.17), "hold")])
        if sid == 2:
            return camkeys(g, [(466, TP(8.6, 0.35, 2.60), TP(10.9, 0.45, 3.50), "hold"),
                               (470, TP(8.6, 0.35, 2.60), TP(10.9, 0.45, 3.50), "sine"),
                               (488, TP(8.3, -0.45, 1.75), TP(11.0, -0.55, 1.75), "sine"),
                               (498, TP(8.25, -0.47, 1.70), TP(11.0, -0.57, 1.72), "hold")])
        return camkeys(g, [(498, TP(8.55, -0.45, 1.55), TP(11.0, -0.55, 1.65), "sine"),
                           (536, TP(9.05, -0.50, 1.55), TP(11.0, -0.55, 1.68), "hold")])

    # ------------------------------------------------------------------ poses
    @staticmethod
    def bird(g, notes=3):
        return dict(state="perch_sing", notes=notes, beak=0.65 + 0.25 * math.sin(g * 0.9), t=g / 30.0, swing=3 * math.sin(g * 0.17))

    @staticmethod
    def alfie(sid, g):
        p = dict(yaw=0.2, pitch=-0.2, expr="happy", head_roll=-3, legs="narrow", arm_l="akimbo", prop_r="cage", t=g / 30.0)
        p["bird"] = S.bird(g)
        p["blink"] = blink(g, [446, 486, 520])
        if sid == 1:
            p["arm_r"] = dict(hand=(0.62, 0.38), bend=-0.5, stretch=1.2)
            u = ez((g - 440) / 16.0)
            p["gaze"] = (lerp(0.0, 0.5, u), lerp(0.0, -0.9, u))       # glances up at the big men
            p["pitch"] = lerp(-0.1, -0.45, u)
            p["head_roll"] = -3 + 2 * math.sin(g * 0.12)
            return p
        if sid == 2:
            p["arm_r"] = dict(hand=(0.62, 0.38), bend=-0.5, stretch=1.2)
            p["expr"] = "determined"
            p["gaze"] = (0.6, -0.9); p["pitch"] = -0.55; p["yaw"] = 0.35
            p["head_roll"] = -5 + 2 * math.sin(g * 0.15)
            p["lean"] = -2 * pulse(g, S.G_YOUNG - 2, S.G_YOUNG + 3, S.G_YOUNG + 12, 1.0)
            return p
        u = ez((g - (S.G_CAGE - 6)) / 9.0, "back_out")
        p["arm_r"] = dict(hand=(lerp(0.62, 0.70, u), lerp(0.38, 0.05, u)), bend=lerp(-0.5, -0.9, u), stretch=1.25)
        p["expr"] = "happy"
        p["gaze"] = (lerp(0.2, 0.75, u), lerp(-0.1, 0.25, u))
        p["head_roll"] = lerp(-3, -7, u) + 1.5 * math.sin(g * 0.13)
        p["yaw"] = lerp(0.15, 0.3, u)
        p["bird"] = S.bird(g, notes=3)
        p["bird"]["swing"] = 6 * pulse(g, S.G_CAGE - 2, S.G_CAGE + 4, S.G_CAGE + 16, 1.0) + 2 * math.sin(g * 0.17)
        return p

    @staticmethod
    def miner1(sid, g):
        p = dict(yaw=0.45, pitch=0.45, expr="smirk", head_roll=6, arm_l="akimbo", arm_r="akimbo", legs="wide", t=g / 30.0)
        p["head_roll"] = 6 + 2 * math.sin(g * 0.1)
        p["blink"] = blink(g, [438, 492])
        return p

    @staticmethod
    def miner3(sid, g):
        p = dict(yaw=-0.45, pitch=0.5, expr="smirk", head_roll=-6, legs="stand", t=g / 30.0,
                 arm_l="akimbo", arm_r="akimbo")
        p["head_roll"] = -6 + 2 * math.sin(g * 0.11 + 1)
        p["blink"] = blink(g, [452, 483, 525])
        if sid == 2:
            p["expr"] = "grinning"
        return p

    @staticmethod
    def gaffer(sid, g):
        p = dict(cast5.STORY5["gaffer_arms_crossed"][1])
        p["yaw"] = -0.25; p["pitch"] = 0.3; p["t"] = g / 30.0
        p["blink"] = blink(g, [459])
        return p

    @staticmethod
    def stage(sid, g):
        out = {"alfie": dict(pos=S.ALFIE, pose=S.alfie(sid, g))}
        if sid in (1, 2):
            out["miner1"] = dict(pos=S.MINER1, pose=S.miner1(sid, g))
        if sid in (1, 2):
            out["miner3"] = dict(pos=S.MINER3, pose=S.miner3(sid, g))
        if sid == 1:
            out["gaffer"] = dict(pos=S.GAFFER, pose=S.gaffer(sid, g))
        return out

    @staticmethod
    def lamps(sid, g, T):
        f = bf(sid, g)
        on = {}
        an = T.anch[("alfie", f)]
        hx, hy = an["hip"]
        on["lamp_alfie"] = (L.actors.local_to_world(T.actors["alfie"], (hx + 0.30, hy + 0.12), f) + Vector((0, 0, 0)), 0.6)
        if sid == 1:
            on["lamp_gaffer"] = (T.anchor_world("gaffer", "chest", f, toward_cam=0.3) + Vector((0, 0, 0.6)), 0.6)
        if sid in (1, 2):
            on["lamp_m1"] = (T.anchor_world("miner1", "chest", f, toward_cam=0.4) + Vector((0, 0, 0.9)), 0.35)
        return on

    @staticmethod
    def gas(sid, g):
        return 0.0

    @staticmethod
    def flame(sid, g):
        return None

    # ------------------------------------------------------------------ delivery (deliver5.py)
    SHOT = 6
    SUB = {1: "6a", 2: "6b", 3: "6c"}
    CAST_NOTE = "v3/cast5: alfie with the 2D held cage (prop_r 'cage' + bird perch_sing 3 notes), miner1, miner3, gaffer (6a), miner1/3 (6b)"
    TRANS_IN = {"type": "cut_or_dissolve", "frames": 10, "note": "in-handle g 424..430 rendered in 3D (6a push already moving)"}
    TRANS_OUT = {"type": "cut_or_dissolve", "frames": 10, "note": "out-handle g 529..535 rendered in 3D (6c push continues)"}
    PAIRS = [("6a", 450, 37), ("6b", 490, 37), ("6c", 520, 37)]
    CUES = [
        (424, 536, "tunnel room tone; the canary keeps chirping softly in the cage", "ambience"),
        (440, 456, "alfie glances up at the big men: a small gulp", "accent"),
        (466, 466, "hard cut: tilt down from the tall miner to the boy", "cut"),
        (470, 490, "camera tilts down the tall miner (a descending comic slide whistle, soft)", "camera"),
        (498, 498, "hard cut: medium on alfie and his cage", "cut"),
        (510, 524, "alfie lifts the cage beside his torso: cage ring jingle, the bird chirps brightly", "prop", {"peak_frame": 516}),
    ]


if __name__ == "__main__":
    L.main(S, sys.argv)
