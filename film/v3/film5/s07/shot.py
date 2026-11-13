#!/usr/bin/env python3
"""shot.py -- film 5 take s07: shot 7 (plan t 17.63-23.03 = g 529..690), tunnel LAMP.  "หัวหน้าหัวเราะ  'เอานกมาร้องเพลงกล่อม
พวกข้าเหรอ ไอ้หนู ตะเกียงข้ายังสว่างอยู่เลย'" -- the gaffer laughs at alfie; the quoted line (18.59-23.0 s = g 561..693) is
the only time a mouth moves (his, lip-synced to the narration loudness, a new drawing every 2 frames).

    7a  g 522..570  (in-handle 522..528)  two-shot, eye level: the gaffer near on screen-right bursts out laughing on "หัวเราะ"
                    (g 547), alfie small and far on screen-left with his cage; the quote starts g 561; slow push  (ref a t0013)
    7b  g 571..607  hard cut, closer and a little low on the gaffer laughing and talking ("เอานกมาร้องเพลงกล่อมพวกข้าเหรอ"),
                    tears, his lamp swinging  (ref a t0015)
    7c  g 608..644  hard cut, side two-shot: the gaffer leans down over little alfie ("ไอ้หนู" g 626) and lifts his lamp
                    ("ตะเกียงข้า" g 639); alfie looks up, worried, hugging the cage  (ref a t0011)
    7d  g 645..697  hard cut at plan t 21.5: the miners laughing and pointing (closed laughing grins; the gaffer's voice goes on
                    off screen), slow push (out-handle 691..697)  (ref a t0047)
Cage = the cast's 2D held cage (bird drawn inside the bars); the set's 3D cage hidden.  NO depth of field (client rule).

Internal sub-shot ids 1 (7a), 2 (7b), 3 (7c), 4 (7d).  python3 shot.py probe|stills|final <sids> <g spec> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5 as L                                        # noqa: E402
from lib5 import TP, Vector, ez, lerp, lerpv, clamp, blink, pulse, camkeys, g_of, bf  # noqa: E402
import cast5                                            # noqa: E402


class S(object):
    NAME = "s07"
    G0, G1, H = 529, 691, 7
    G_7B, G_7C, G_7D = 571, 608, 645
    RANGES = {1: (G0 - H, G_7B - 1), 2: (G_7B, G_7C - 1), 3: (G_7C, G_7D - 1), 4: (G_7D, G1 + H - 1)}
    CAST = {"gaffer": "gaffer", "alfie": "alfie", "miner1": "miner1", "miner2": "miner2", "miner3": "miner3"}
    PPD = {1: {"gaffer": 448, "alfie": 192},
           2: {"gaffer": 640},
           3: {"gaffer": 512, "alfie": 256},
           4: {"miner1": 384, "miner2": 320, "miner3": 256}}
    LAMP_NAMES = ("lamp_gaffer", "lamp_alfie", "lamp_m1", "lamp_m3")
    G_LAUGH = g_of(18.04)                                       # 545 "หัวเราะ"
    Q0, Q1 = g_of(18.59), g_of(23.0)                            # 561..693 the quoted line
    G_NOO = g_of(20.76)                                         # 626 "ไอ้หนู"
    G_LAMP = g_of(21.21)                                        # 639 "ตะเกียงข้า"

    GAFFER = TP(11.4, -0.15, 0)
    ALFIE = TP(15.6, -1.85, 0)
    GAFFER_C = TP(11.9, -0.15, 0)
    ALFIE_C = TP(13.5, -2.0, 0)
    MINERS = {"miner1": TP(12.6, -1.95, 0), "miner2": TP(13.6, -0.35, 0), "miner3": TP(15.4, -1.05, 0)}

    @staticmethod
    def cam(sid, g):
        if sid == 1:
            return camkeys(g, [(522, TP(8.0, -1.35, 2.05), TP(13.0, -0.55, 2.25), "sine"),
                               (571, TP(8.5, -1.25, 2.05), TP(13.0, -0.55, 2.25), "hold")])
        if sid == 2:
            return camkeys(g, [(571, TP(9.35, -0.25, 1.75), TP(11.4, -0.35, 2.85), "sine"),
                               (608, TP(9.65, -0.27, 1.80), TP(11.4, -0.35, 2.85), "hold")])
        if sid == 3:
            return camkeys(g, [(608, TP(9.1, 0.15, 1.20), TP(12.6, -0.95, 2.50), "sine"),
                               (645, TP(9.25, 0.12, 1.22), TP(12.6, -0.95, 2.44), "hold")])
        return camkeys(g, [(645, TP(8.9, -0.85, 1.95), TP(14.0, -1.30, 2.45), "sine"),
                           (698, TP(9.4, -0.90, 1.95), TP(14.0, -1.30, 2.45), "hold")])

    # ------------------------------------------------------------------ poses
    @staticmethod
    def gaffer(sid, g):
        p = dict(cast5.STORY5["gaffer_laugh"][1])
        p["arm_r"] = dict(p["arm_r"]); p["arm_l"] = dict(p["arm_l"]); p["prop_l"] = dict(p["prop_l"])
        p["t"] = g / 30.0
        laugh = ez((g - (S.G_LAUGH - 4)) / 6.0, "back_out") if sid == 1 else 1.0
        shake = math.sin(g * 0.9)
        if sid == 1 and laugh < 0.5:                             # before the laugh: smug, looking across at the boy
            p.update(expr="smug", mouth="flat", head_roll=4, lean=-1, squash=(1.0, 1.0), head_dy=0.0, fx=[], blink=blink(g, [530]))
            p["yaw"] = -0.25; p["gaze"] = (-0.8, 0.1)
            p["arm_r"] = dict(hand=(0.5, 0.9), bend=0.6)
            return p
        p["expr"] = "laughing"
        p["blink"] = 0
        p["head_roll"] = 12 + 2.5 * shake
        p["head_dy"] = 0.03 + 0.01 * shake
        p["lean"] = -6 - 0.8 * shake
        p["squash"] = (1.0 + 0.015 * shake, 1.0 - 0.015 * shake)
        m = L.lip(g, S.Q0, S.Q1, silent="grin")
        p["mouth"] = m if m is not None else "grin"             # outside the quote: a held laughing grin (no lip motion)
        p["yaw"] = -0.1 if sid == 1 else 0.1
        if sid == 3:                                            # leans down over the boy, lifts the lamp on "ตะเกียงข้า"
            p["expr"] = "smug" if g >= S.G_NOO - 4 else "laughing"
            p["fx"] = [] if g >= S.G_NOO - 4 else ["tears"]
            bend = ez((g - (S.G_NOO - 8)) / 10.0)
            p["lean"] = lerp(-6, 10, bend) - 0.6 * shake
            p["pitch"] = lerp(-0.2, 0.55, bend)
            p["yaw"] = -0.45
            p["gaze"] = (-0.8, 0.6 * bend)
            p["head_roll"] = lerp(12, -4, bend) + 1.5 * shake
            lift = ez((g - (S.G_LAMP - 5)) / 8.0, "back_out")
            p["arm_l"] = dict(hand=(lerp(-0.72, -0.95, lift), lerp(0.9, -0.2, lift)), bend=lerp(0.4, 0.9, lift), stretch=1.3)
            p["arm_r"] = dict(hand=(0.45, 0.95), bend=0.6)
            p["flame"] = 1.0 + 0.5 * lift
        return p

    @staticmethod
    def alfie(sid, g):
        p = dict(yaw=0.35, pitch=-0.2, expr="happy", head_roll=-3, legs="narrow", arm_l="akimbo", prop_r="cage", t=g / 30.0,
                 arm_r=dict(hand=(0.62, 0.38), bend=-0.5, stretch=1.2))
        p["bird"] = dict(state="perch_sing", notes=3, beak=0.65 + 0.25 * math.sin(g * 0.9), t=g / 30.0, swing=2 * math.sin(g * 0.17))
        p["blink"] = blink(g, [534, 590, 630])
        if sid == 1:
            u = ez((g - (S.G_LAUGH + 2)) / 8.0)
            p["expr"] = "happy" if u < 0.5 else "worried"
            p["gaze"] = (lerp(0.2, 0.8, u), 0.0)
            return p
        p["expr"] = "worried"
        p["yaw"] = 0.5
        p["pitch"] = -0.6
        p["gaze"] = (0.7, -0.9)
        p["head_roll"] = -6 + 1.5 * math.sin(g * 0.13)
        p.pop("prop_r", None)                                   # the cage moves to his far hand, hugged in close
        p["prop_l"] = "cage"
        p["arm_l"] = dict(hand=(-0.48, 0.36), bend=0.6, stretch=1.15)
        p["arm_r"] = dict(hand=(-0.05, 0.62), bend=0.6)
        p["fx"] = ["sweat"]
        return p

    @staticmethod
    def miner(n, g):
        p = dict(cast5.STORY5["miners_laugh" + ("" if n == "miner1" else "_" + n)][1])
        p["arm_l"] = dict(p["arm_l"]); p["arm_r"] = dict(p["arm_r"])
        off = {"miner1": 0.0, "miner2": 1.3, "miner3": 2.6}[n]
        sh = math.sin(g * 1.6 + off)
        p["t"] = g / 30.0
        p["head_roll"] = p.get("head_roll", -10) + 4 * sh
        p["head_dy"] = 0.015 * sh
        p["lean"] = -5 - 3 * sh
        p["squash"] = (1.0 + 0.02 * sh, 1.0 - 0.02 * sh)
        ax, ay = p["arm_l"]["hand"]
        p["arm_l"]["hand"] = (ax, ay + 0.05 * math.sin(g * 1.1 + off))
        if n == "miner2":                                       # the short bearded one doubles over
            p["lean"] = 6 + 3 * sh; p["pitch"] = 0.1
        if n == "miner3":
            p["yaw"] = -0.2
        return p

    @staticmethod
    def stage(sid, g):
        if sid == 1:
            return {"gaffer": dict(pos=S.GAFFER, pose=S.gaffer(1, g)), "alfie": dict(pos=S.ALFIE, pose=S.alfie(1, g))}
        if sid == 2:
            return {"gaffer": dict(pos=S.GAFFER, pose=S.gaffer(2, g))}
        if sid == 3:
            return {"gaffer": dict(pos=S.GAFFER_C, pose=S.gaffer(3, g)), "alfie": dict(pos=S.ALFIE_C, pose=S.alfie(3, g))}
        return {n: dict(pos=p, pose=S.miner(n, g)) for n, p in S.MINERS.items()}

    @staticmethod
    def lamps(sid, g, T):
        f = bf(sid, g)
        on = {}
        if "gaffer" in S.PPD[sid]:
            k = T.actors["gaffer"].poses[f].get("flame", 1.0)
            on["lamp_gaffer"] = (T.anchor_world("gaffer", "prop_tip_l", f, toward_cam=0.10), 0.8 + 0.3 * (k - 1.0))
        if "alfie" in S.PPD[sid]:
            an = T.anch[("alfie", f)]; hx, hy = an["hip"]
            on["lamp_alfie"] = (L.actors.local_to_world(T.actors["alfie"], (hx + 0.30, hy + 0.12), f), 0.55)
        if sid == 4:
            on["lamp_m1"] = (T.anchor_world("miner1", "chest", f, toward_cam=0.5) + Vector((0, 0, 0.7)), 0.45)
            on["lamp_m3"] = (T.anchor_world("miner2", "chest", f, toward_cam=0.5) + Vector((0, 0, 0.6)), 0.4)
        return on

    @staticmethod
    def gas(sid, g):
        return 0.0

    @staticmethod
    def flame(sid, g):
        return None

    # ------------------------------------------------------------------ delivery (deliver5.py)
    SHOT = 7
    SUB = {1: "7a", 2: "7b", 3: "7c", 4: "7d"}
    CAST_NOTE = "v3/cast5: gaffer (7a-7c, lip-synced only inside the quote g 561..693), alfie with the 2D held cage (7a, 7c), miner1/2/3 laughing (7d)"
    TRANS_IN = {"type": "cut_or_dissolve", "frames": 10, "note": "in-handle g 522..528 rendered in 3D (7a push already moving)"}
    TRANS_OUT = {"type": "cut_or_dissolve", "frames": 10, "note": "out-handle g 691..697 rendered in 3D (7d push continues; the quote ends g 693)"}
    PAIRS = [("7a", 555, 13), ("7b", 590, 15), ("7c", 640, 11), ("7d", 670, 47)]
    CUES = [
        (522, 698, "tunnel room tone", "ambience"),
        (543, 561, "the gaffer bursts out laughing (big belly laugh, under the narration)", "laugh", {"peak_frame": 547}),
        (561, 693, "QUOTED LINE (narrator voices the gaffer): mouth lip-synced to the narration", "dialogue"),
        (571, 571, "hard cut: closer on the laughing gaffer", "cut"),
        (608, 608, "hard cut: the gaffer looms over alfie", "cut"),
        (618, 630, "the gaffer leans down: coat rustle, boots creak", "foley", {"peak_frame": 626}),
        (634, 644, "he lifts his lamp: brass ring creak", "prop", {"peak_frame": 639}),
        (645, 645, "hard cut (plan t 21.5): the miners laughing", "cut"),
        (645, 698, "the miners roar with laughter (three voices, wheezy, under the gaffer's line)", "laugh"),
    ]


if __name__ == "__main__":
    L.main(S, sys.argv)
