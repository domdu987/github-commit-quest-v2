#!/usr/bin/env python3
"""shot.py -- film 5 take s05: shot 5 (plan t 10.50-14.38 = g 315..430), tunnel LAMP.  "หัวหน้าเชื่อแค่ตะเกียงของเขา ไฟยังสว่าง
ก็แปลว่าปลอดภัย" -- the foreman trusts only his flame lamp.

    5a  g 308..354  (in-handle 308..314 under the 10-f dissolve from s01's 4d)  low angle on the gaffer, his flame lamp hanging at
                    his side; he hoists it up beside his head on "แค่ตะเกียง" (g 341..352), slow crane up  (ref a t0013)
    5b  g 355..397  hard cut, ECU of the lamp in his raised fist: the flame flares up bright on "ไฟยังสว่าง" (g 372..381),
                    his smug face behind; slow push in  (ref a t0045 / plan lamp_insert)
    5c  g 398..437  hard cut, low wide-ish: the gaffer holding the bright lamp high, miner2 digging in the depth; a smug nod on
                    "ปลอดภัย" (g 416); slow push (out-handle 431..437)  (ref a t0013)
Mouths closed (no quoted line here).  NO depth of field (client rule).

Internal sub-shot ids 1 (5a), 2 (5b), 3 (5c).  python3 shot.py probe|stills|final <sids> <g spec> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5 as L                                        # noqa: E402
from lib5 import TP, Vector, ez, lerp, lerpv, clamp, blink, pulse, camkeys, g_of, bf  # noqa: E402


class S(object):
    NAME = "s05"
    G0, G1, H = 315, 431, 7                                     # shot 5 = [315, 431), handles 7 each side
    G_5B, G_5C = 355, 398
    RANGES = {1: (G0 - H, G_5B - 1), 2: (G_5B, G_5C - 1), 3: (G_5C, G1 + H - 1)}
    CAST = {"gaffer": "gaffer", "miner2": "miner2"}
    PPD = {1: {"gaffer": 384}, 2: {"gaffer": 1536}, 3: {"gaffer": 320, "miner2": 160}}
    LAMP_NAMES = ("lamp_gaffer", "lamp_miner2", "lamp_key")
    G_LIFT = (g_of(11.28) - 2, g_of(11.28) + 9)                 # 339..350 "แค่ตะเกียง": the lamp comes up
    G_BRIGHT = (g_of(12.45) - 5, g_of(12.45) + 4)               # 372..381 "ไฟยังสว่าง": the flame flares
    G_NOD = g_of(13.77)                                         # 413 "ปลอดภัย"

    GAFFER = TP(12.2, -0.85, 0)
    MINER2 = TP(6.4, -1.35, 0)
    FLAME = None                                                # world flame point in 5b (prepare)

    # ------------------------------------------------------------------ cameras
    @staticmethod
    def cam(sid, g):
        if sid == 1:
            return camkeys(g, [(308, TP(9.15, -0.25, 0.62), TP(12.2, -0.85, 2.55), "sine"),
                               (355, TP(9.35, -0.30, 0.80), TP(12.2, -0.85, 2.85), "hold")])
        if sid == 2:
            F = S.FLAME if S.FLAME is not None else TP(12.0, -0.3, 3.3)
            u = ez((g - 355) / 43.0, "sine")
            d = S._dir()
            sr = Vector((-d.y, d.x, 0))
            loc = F - d * lerp(0.72, 0.56, u) + sr * lerp(-0.16, -0.12, u) + Vector((0, 0, lerp(-0.30, -0.24, u)))
            look = F + sr * lerp(-0.04, -0.03, u) + Vector((0, 0, lerp(0.02, 0.03, u)))
            return loc, look
        return camkeys(g, [(398, TP(16.2, -1.75, 0.95), TP(12.2, -0.75, 2.40), "sine"),
                           (438, TP(15.6, -1.65, 1.02), TP(12.2, -0.75, 2.50), "hold")])

    @staticmethod
    def _dir():
        a = TP(9.35, -0.30, 0.80); b = S.GAFFER
        d = b - a; d.z = 0; d.normalize(); return d

    @staticmethod
    def prepare(T):
        """5b: where the flame of the raised lamp is in the world (two passes: the card faces the ECU camera)."""
        f = bf(2, 375)
        T.actors["gaffer"].place(f, tuple(S.GAFFER))
        for _ in range(2):
            loc, look = S.cam(2, 375)
            S.FLAME = T.probe_anchor("gaffer", f, S.gaffer(2, 375), "prop_tip_r", loc, look)
        print("s05: 5b flame at", tuple(round(v, 3) for v in S.FLAME), flush=True)

    # ------------------------------------------------------------------ poses
    @staticmethod
    def gaffer(sid, g):
        p = dict(yaw=0.25, pitch=-0.35, expr="smug", head_roll=4, legs="wide", lean=-2,
                 prop_r={"type": "flame_lamp", "scale": 1.25}, flame=1.0, t=g / 30.0)
        p["blink"] = blink(g, [326, 366, 404, 428])
        if sid == 1:
            u = ez((g - S.G_LIFT[0]) / float(S.G_LIFT[1] - S.G_LIFT[0]), "back_out")
            p["arm_r"] = dict(hand=(lerp(0.78, 1.0, u), lerp(1.0, -0.45, u)), bend=lerp(0.4, -0.9, u), stretch=1.3)
            p["arm_l"] = "akimbo"
            p["pitch"] = lerp(-0.2, -0.5, u)
            p["gaze"] = (lerp(0.1, 0.8, u), lerp(0.2, -0.8, u))
            p["head_roll"] = lerp(2, 7, u) + 1.5 * math.sin(g * 0.15)
            p["lean"] = lerp(0, -4, u)
            p["flame"] = 1.0 + 0.15 * u
            return p
        # 5b, 5c: lamp held high, pointing across at it
        p.update(cast_lift())
        p["t"] = g / 30.0
        if sid == 2:
            k = ez((g - S.G_BRIGHT[0]) / float(S.G_BRIGHT[1] - S.G_BRIGHT[0]), "cubic_out")
            p["flame"] = 1.15 + 0.85 * k + 0.04 * math.sin(g * 1.3)
            p["head_roll"] = 6 + 1.5 * math.sin(g * 0.12)
            p["arm_r"] = dict(p["arm_r"], hand=(1.0, -0.45 - 0.02 * math.sin(g * 0.2)))
            p["blink"] = blink(g, [366, 390])
            return p
        nod = pulse(g, S.G_NOD - 3, S.G_NOD + 2, S.G_NOD + 9, 1.0)
        p["flame"] = 1.85 + 0.05 * math.sin(g * 1.1)
        p["pitch"] = -0.55 + 0.45 * nod
        p["head_dy"] = 0.03 * nod
        p["head_roll"] = 6 + 2 * math.sin(g * 0.1)
        p["gaze"] = (lerp(0.8, 0.1, ez((g - 398) / 12.0)), lerp(-0.8, 0.1, ez((g - 398) / 12.0)))
        p["lean"] = -4 - 2 * nod
        p["blink"] = blink(g, [404, 428])
        return p

    @staticmethod
    def miner2(g):
        import cast5
        p = dict(cast5.STORY5["miners_work_miner2"][1])
        d = 0.5 - 0.5 * math.cos(2 * math.pi * g / 34.0)
        p["arm_r"] = dict(p["arm_r"], hand=(0.55, 0.72 - 0.12 * d))
        p["lean"] = 14 + 5 * d
        p["yaw"] = -0.4
        p["blink"] = blink(g, [409, 431])
        return p

    @staticmethod
    def stage(sid, g):
        out = {"gaffer": dict(pos=S.GAFFER, pose=S.gaffer(sid, g))}
        if sid == 3:
            out["miner2"] = dict(pos=S.MINER2, pose=S.miner2(g))
        return out

    @staticmethod
    def lamps(sid, g, T):
        f = bf(sid, g)
        on = {}
        k = T.actors["gaffer"].poses[f].get("flame", 1.0)
        on["lamp_gaffer"] = (T.anchor_world("gaffer", "prop_tip_r", f, toward_cam=0.10), 0.8 + 0.35 * (k - 1.0))
        if sid == 2:                                            # a soft warm key on his face from the lamp side
            on["lamp_key"] = (S.FLAME + Vector((0, 0, -0.35)) - S._dir() * 0.6, 0.10)
        if sid == 3:
            on["lamp_miner2"] = (T.anchor_world("miner2", "hip", f, toward_cam=0.15) + Vector((0, 0, 0.15)), 0.6)
        return on

    @staticmethod
    def gas(sid, g):
        return 1.2 if sid == 1 else 0.0

    @staticmethod
    def flame(sid, g):
        return None

    # ------------------------------------------------------------------ delivery (deliver5.py)
    SHOT = 5
    SUB = {1: "5a", 2: "5b", 3: "5c"}
    CAST_NOTE = "v3/cast5: gaffer (5a-5c, his flame_lamp prop, flame 1 -> 2), miner2 digging (5c)"
    TRANS_IN = {"type": "dissolve", "frames": 10, "from": "s01 shot 4d", "mixed": [310, 319],
                "note": "in-handle g 308..314 rendered in 3D (5a camera already moving); s01's out-handle covers g 315..321"}
    TRANS_OUT = {"type": "cut_or_dissolve", "frames": 10, "note": "out-handle g 431..437 rendered in 3D (5c push continues)"}
    PAIRS = [("5a", 350, 13), ("5b", 385, 45), ("5c", 420, 13)]
    CUES = [
        (308, 438, "tunnel room tone: drips, timber creak, faint hiss of the lamps", "ambience"),
        (339, 352, "the gaffer hoists his lamp: brass ring creak, a little swing of the lamp", "prop", {"peak_frame": 345}),
        (355, 355, "hard cut to the ECU of the lamp", "cut"),
        (372, 382, "the flame flares up bright: a soft whoomp and a rising hiss of the flame", "lamp", {"peak_frame": 377}),
        (382, 398, "the bright flame purrs steadily", "lamp"),
        (398, 398, "hard cut: low reverse angle, the gaffer with the lamp held high", "cut"),
        (398, 438, "miner2 digs in the background: shovel scrapes", "work"),
        (410, 420, "the gaffer's smug nod: a satisfied 'hm' (no words, mouth closed)", "accent", {"peak_frame": 413}),
    ]


def cast_lift():
    import cast5
    p = dict(cast5.STORY5["gaffer_lift_lamp"][1])
    p["arm_r"] = dict(p["arm_r"]); p["arm_l"] = dict(p["arm_l"])
    return p


if __name__ == "__main__":
    L.main(S, sys.argv)
