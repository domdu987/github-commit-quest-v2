#!/usr/bin/env python3
"""shot.py -- film 4 take s13: shot 13 (SUNSET, g 1055..1179 + 7-frame handles each side: renders g 1048..1186).

    shot 13  street two-shot in front of the red gate at sunset (ref a t0055-t0059: the hero thrown out at the gate, the
             court smug on both sides).  The master (left, nearer) pats kenta's shoulder on "ช่างใหญ่ตบไหล่เขา" (pat lands
             g 1077), smug; his mouth moves only on the quote "หอของข้านิ่งยังกับภูเขา เจดีย์เมาของเจ้าใกล้ล้มแล้ว"
             (36.25..39.29 s -> g 1090..1182, lip-sync from narration_bankky.wav); kenta worried, looks up at him.
             A g 1048-1092 two-shot, slow push; B snap punch-in on the master g 1092-1099 (quote starts g 1090);
             C snap to the kenta-favoured two-shot g 1131-1139 (on "เจดีย์เมาของเจ้า" 37.55 s = g 1130), drift to the end.

    python3 shot.py probe 13 1048:1186:10 | stills 13 a:b <out> [scale] [samples] | final 13 1048:1186
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base4 import *                                   # noqa: F401,F403
import base4 as B

G_IN, G0, G1, G_OUT = 1048, 1055, 1180, 1186        # take frames: handle in, shot start, shot end (excl.), last handle frame
G_PAT = g_of(35.80)                                  # 1077 "ไหล่เขา": the pat lands
Q0, Q1 = g_of(36.25), g_of(39.29)                   # 1090..1182 the quote (mouth)
G_B = (1092, 1099)                                   # punch-in on the master
G_C = (1131, 1139)                                   # snap to the kenta-favoured two-shot ("เจดีย์เมาของเจ้า" g 1130)
PATS = [G_PAT, 1091, 1104]

MASTER = (-0.85, -40.70, 0.0)                        # nearer to the camera by 0.12 D: his hand lies over kenta's shoulder
KENTA = (0.30, -40.50, 0.0)


class Take13(B.Take):
    PRESET = "SUNSET"
    NAME = "s13"
    HERE = os.path.dirname(os.path.abspath(__file__))
    SHOTS = {13: (G_IN, G_OUT)}
    CAST = ["kenta", "master"]

    def camera_at(self, shot, g):
        ks = [(G_IN, V(0.45, -46.2, 2.25), V(-0.15, -40.5, 2.45), "sine"),
              (G_B[0], V(0.30, -45.35, 2.25), V(-0.20, -40.5, 2.47), "quint"),
              (G_B[1], V(-2.10, -43.50, 2.18), V(-0.55, -40.6, 2.30), "sine"),
              (G_C[0], V(-2.00, -43.25, 2.15), V(-0.55, -40.6, 2.28), "quint"),
              (G_C[1], V(1.05, -43.70, 2.15), V(0.10, -40.5, 2.25), "sine"),
              (G_OUT + 1, V(0.92, -43.25, 2.15), V(0.06, -40.5, 2.22), "hold")]
        loc, look = path(g, ks)
        loc, look, roll = apply_shake(loc, look, g, 0.06, seed=3)
        return loc, look, roll

    def dof(self, shot, g):
        if g < G_B[0] + 3:
            return "master", 3.5
        if g < G_C[0] + 4:
            return "master", 3.0
        return "kenta", 3.0

    def actors_at(self, shot, g):
        return {"kenta": dict(pos=KENTA, pose=kenta_pose(g), ppd=320),
                "master": dict(pos=MASTER, pose=master_pose(g), hands=master_hands(g), ppd=320)}


def patlift(g):
    """height of the master's hand over kenta's shoulder (D): descends 1066..1072, then pats"""
    if g < 1066:
        return 0.45
    if g < 1072:
        return lerp(0.45, 0.12, ease((g - 1066) / 6.0, "sine"))
    v = 0.0
    for p in PATS:
        v = max(v, pulse(g, p - 6, p - 3, p, 0.14, "quad_out", "quad_in"))
    if g < PATS[0]:
        v = max(v, lerp(0.12, 0.0, ease((g - 1072) / 5.0, "quad_in")))
    return v


def master_pose(g):
    p = dict(cast4.STORY4["master_pat_shoulder"][1])
    p["expr"] = "smug"
    m = mouth_at(g, Q0, Q1)
    talk = m is not None
    p["mouth"] = m if talk else "flat"
    p["arm_l"] = "akimbo"
    if g < 1066:
        p["arm_r"] = dict(hand=(0.88, 0.36), bend=-0.3, stretch=1.25)
    # chin up and a slow smug bob while he talks; looks down at kenta on the pats
    nod = 0.0 if not talk else 0.12 * math.sin((g - Q0) * 0.35)
    p["pitch"] = lerp(0.25, -0.15, ease((g - Q0 + 6) / 10.0, "sine")) + nod if g > Q0 - 6 else 0.25
    p["yaw"] = 0.4 if g < 1140 else lerp(0.4, 0.3, ease((g - 1140) / 10.0))
    p["gaze"] = (0.6, 0.3) if g < Q0 else (0.4, 0.1)
    p["head_roll"] = 6 + (3 * math.sin((g - Q0) * 0.21) if talk else 0)
    p["lean"] = 3 - 2.5 * pulse(g, PATS[0] - 5, PATS[0] - 2, PATS[0] + 6, 1.0) + (1.5 * math.sin(g * 0.09) if talk else 0)
    p["blink"] = blink(g, [1058, 1118, 1162])
    return p


def master_hands(g):
    if g < 1066:
        return None
    lift = patlift(g)

    def fn(tk, f):
        k = tk.act["kenta"]
        kp = k.poses[f]
        an = sprites.puppet.figure("kenta", kp, "q")["anchors"]
        sh = min((an["shoulder_l"], an["shoulder_r"]), key=lambda s: s[0])     # the shoulder on the master's side
        w = actors.local_to_world(k, (sh[0] + 0.12, sh[1] - 0.04), f)
        return {"r": {"hand": (w.x, w.y, w.z + lift), "stretch": 1.3}}
    return fn


def kenta_pose(g):
    p = dict(cast4.STORY4["kenta_worried"][1])
    hit = sum(pulse(g, pg - 2, pg + 1, pg + 7, 1.0) for pg in PATS)
    p["squash"] = (1.0 + 0.03 * hit, 1.0 - 0.05 * hit)
    p["yaw"] = -0.35
    look_away = pulse(g, 1150, 1158, 1172, 1.0, "sine", "sine")              # a worried glance off toward the pagoda
    p["pitch"] = lerp(-0.25, 0.1, look_away)
    p["gaze"] = (lerp(-0.7, 0.5, look_away), lerp(-0.6, -0.2, look_away))
    p["head_roll"] = 6 - 4 * hit + 2 * math.sin(g * 0.15)
    p["lean"] = -2 - 3 * hit
    p["t"] = (g % 40) / 40.0
    p["blink"] = blink(g, [1066, 1124, 1176])
    return p


if __name__ == "__main__":
    B.main(Take13)
