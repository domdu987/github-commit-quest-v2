#!/usr/bin/env python3
"""shot.py -- film 5 take s09: shots 9 and 10 (the song countdown), mine set tunnel LAMP, g 757..970 + 8-frame handles.

    shot 9   9a  g 749.. 786  day 1, insert wide: the cage on its nail on the pit prop, chalk tally "1" (one stroke) above the nail,
                              the canary on its perch INSIDE the bars singing 5 notes; slow push (ref a t0039)
             9b  g 787.. 811  cut, ECU between the front wires: 5 notes floating up (ref a t0041)
             --  10-frame dissolve g 807..816 (days pass)
             9c  g 812.. 841  day 5, insert wide: tally "5" (four strokes + a slash), 3 notes, the bird a little ruffled (ref a t0043)
             9d  g 842.. 870  cut, ECU, 3 notes
    shot 10  --  10-frame dissolve g 866..875
             10a g 871.. 905  day 10, insert wide: tally "10" (two groups), 3 notes, the bird tired (ref a t0067)
             10b g 906.. 935  cut, ECU push: the last notes drift away, the beak closes on "แล้วก็เงียบ" (g 913), silence (ref a t0069)
             10c g 936.. 970  HARD CUT on "เขาตะโกน": alfie, the cage (2D held cage, bird quiet inside the bars) in his hand, shouts
                              "run", pointing; men in the depth turn; push (ref a t0071); out-handle g 971..978 rendered in 3D
Cage rule (client): hanging cage = the set's 3D cage with the canary sprite INSIDE on the perch (bird card at the perch, the front
wires in front of it); held cage = cast5 2D held cage (prop "cage" + pose key "bird"), the set's 3D cage hidden.
NO depth of field anywhere.   python3 shot.py probe|stills|final <sids> <g spec|all> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk                                                     # noqa: E402
from tk import Vector, TP, ez, lerp, lerpv, blink, pulse, keys, cam_keys, g_of, cast5  # noqa: E402

G0, G1, H = 757, 971, 8                    # shot 9 = 757..870, shot 10 = 871..970
D1, D2, DISS = 812, 871, 10                # dissolves: days 1 -> 5, 5 -> 10 (mixed at-5 .. at+4)
G_9B, G_9D, G_10B, G_10C = 787, 842, 906, 936
G_SILENT = g_of(30.32)                      # 913 "แล้วก็เงียบ"

PERCH = Vector((-0.136, 16.326, 2.812))
CAGE_C = PERCH + Vector((0, 0, 0.12))


def _wide(g, ga, gb, side):
    """insert wide: the cage + the tally above the nail, seen from inside the tunnel; slow push and a little arc."""
    u = ez((g - ga) / float(gb - ga), "sine")
    a0 = (Vector((1.10, 16.33 - 0.40 * side, 2.98)), Vector((-0.20, 16.33, 3.14)))
    a1 = (Vector((0.92, 16.33 - 0.28 * side, 2.96)), Vector((-0.20, 16.33, 3.12)))
    return lerpv(a0[0], a1[0], u), lerpv(a0[1], a1[1], u)


def _ecu(g, ga, gb, side, push=0.10):
    u = ez((g - ga) / float(gb - ga), "sine")
    d0, d1 = 0.70, 0.70 - push
    az = math.radians(lerp(10.0, 16.0, u) * side)
    dv = Vector((math.cos(az), -math.sin(az), 0.0))
    loc = PERCH + dv * lerp(d0, d1, u) + Vector((0, 0, 0.16))
    look = PERCH + Vector((0, 0.07, lerp(0.26, 0.30, u) - (push - 0.10) * 0.9))
    return loc, look


def bird(day):
    def f(g):
        t = g / 30.0
        if day == 1:
            return dict(state="perch_sing", notes=5, beak=0.75 + 0.2 * math.sin(g * 0.9), eyes=1.0, t=t, blink=0)
        if day == 5:
            return dict(state="perch_sing", notes=3, beak=0.55 + 0.18 * math.sin(g * 0.8), eyes=0.85, ruffle=0.15, t=t)
        # day 10: three notes, then silence
        if g < G_SILENT - 6:
            return dict(state="perch_sing", notes=3, beak=0.45 + 0.15 * math.sin(g * 0.7), eyes=0.7, ruffle=0.25, droop=0.12, t=t)
        if g < G_SILENT:
            n = 2 if g < G_SILENT - 3 else 1
            return dict(state="perch_sing", notes=n, beak=lerp(0.4, 0.05, (g - (G_SILENT - 6)) / 6.0), eyes=0.65, ruffle=0.25,
                        droop=0.15, t=t)
        u = ez((g - G_SILENT) / 14.0)
        return dict(state="perch_quiet", notes=0, beak=0.0, eyes=lerp(0.65, 0.5, u), ruffle=0.3, droop=lerp(0.15, 0.25, u), t=t)
    return f


def lamps_insert(T, g, f):
    loc, _ = T.shots[T._sid]["cam"](g)
    d = loc - PERCH; d.z = 0; d.normalize()
    return {"lamp_a": (PERCH + d * 1.1 + Vector((0, 0.45, 0.65)), 0.09),          # warm key from the camera side, above
            "lamp_b": (Vector((-0.62, 15.92, 3.18)), 0.10)}                       # warm rim behind the cage, off the leg


# ----------------------------------------------------------------------------- 10c: alfie shouts "run"
ALFIE_10 = TP(15.9, -1.50, 0)
BG_10 = {"gaffer": TP(9.8, 0.95, 0), "miner2": TP(11.0, 1.35, 0), "miner1": TP(11.6, 0.05, 0)}


def cam_10c(g):
    a = (TP(19.0, -0.85, 1.92), TP(14.0, -1.0, 2.02))
    b = (TP(18.45, -0.88, 1.95), TP(14.0, -1.0, 2.06))
    return cam_keys(g, [(G_10C, a, "cubic_out"), (G_10C + 18, b, "sine"), (G1 + H, (b[0] + Vector((0.0, -0.12, 0.01)), b[1]), "hold")])


def alfie_10(g):
    p = dict(cast5.STORY5["alfie_shout_run"][1])
    u = ez((g - G_10C) / 6.0, "back_out")
    p["bird"] = dict(state="perch_quiet", eyes=0.5, droop=0.25, ruffle=0.3, swing=-6 + 5 * math.sin(g * 0.35), t=g / 30.0)
    p["arm_l"] = dict(hand=(-0.66, lerp(0.55, 0.22, u)), bend=0.5, stretch=1.3)
    p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.45, 0.82, u), lerp(0.55, -0.12, u)))
    p["lean"] = 8 + 5 * u + 1.5 * math.sin(g * 0.5)
    p["head_roll"] = -8 + 2 * math.sin(g * 0.6)
    p["t"] = g / 30.0
    p["mirror"] = True                      # faces screen-left: shouts and points at the men and the far exit
    return p


def bg_pose(n):
    def f(g):
        u = ez((g - (G_10C + 8)) / 8.0)
        if n == "gaffer":
            p = dict(cast5.STORY5["gaffer_smug"][1])
            p["yaw"] = lerp(-0.1, 0.35, u); p["expr"] = "unimpressed"
        else:
            p = dict(yaw=lerp(-0.3, 0.3, u), pitch=-0.1, expr="stunned" if u > 0.5 else "neutral", arm_l="down", arm_r="down", legs="stand")
        p["blink"] = blink(g, [940 + len(n)])
        p["t"] = g / 30.0
        return p
    return f


def lamps_10c(T, g, f):
    a = T.actors["alfie"]; an = T.anch[("alfie", f)]
    hx, hy = an["hip"]
    p = tk.actors.local_to_world(a, (hx - 0.30, hy + 0.12), f)
    loc, _ = cam_10c(g)
    tc = loc - p; tc.z = 0; tc.normalize()
    return {"lamp_a": (p + tc * 0.12, 0.75),
            "lamp_c": (TP(17.4, -0.6, 2.7), 0.35),                               # soft warm key on his face (the hanging lamp above)
            "lamp_d": (tk.actors.local_to_world(T.actors["gaffer"], T.anch[("gaffer", f)]["prop_tip_l"], f), 0.8)}


def _spec(name, g0, g1, cam, **kw):
    d = dict(name=name, g=(g0, g1), cam=cam)
    d.update(kw)
    return d


SHOTS = {
    0: _spec("9a", G0 - H, G_9B - 1, lambda g: _wide(g, G0 - H, G_9B, 1), cage="nail", bird=bird(1), bird_ppd=1024, tally=1,
             lamps=lamps_insert),
    1: _spec("9b", G_9B, D1 + DISS // 2 + 2, lambda g: _ecu(g, G_9B, D1 + 7, 1), cage="nail", bird=bird(1), bird_ppd=2048, tally=1,
             lamps=lamps_insert),
    2: _spec("9c", D1 - DISS // 2 - 2, G_9D - 1, lambda g: _wide(g, D1 - 7, G_9D, -1), cage="nail", bird=bird(5), bird_ppd=1024, tally=5,
             lamps=lamps_insert),
    3: _spec("9d", G_9D, D2 + DISS // 2 + 2, lambda g: _ecu(g, G_9D, D2 + 7, -1), cage="nail", bird=bird(5), bird_ppd=2048, tally=5,
             lamps=lamps_insert),
    4: _spec("10a", D2 - DISS // 2 - 2, G_10B - 1, lambda g: _wide(g, D2 - 7, G_10B, 1), cage="nail", bird=bird(10), bird_ppd=1024,
             tally=10, lamps=lamps_insert),
    5: _spec("10b", G_10B, G_10C - 1, lambda g: _ecu(g, G_10B, G_10C, 1, push=0.16), cage="nail", bird=bird(10), bird_ppd=2048, tally=10,
             lamps=lamps_insert),
    6: _spec("10c", G_10C, G1 + H - 1, cam_10c, cage="hidden",
             actors={"alfie": dict(cast="alfie", ppd=448, place=lambda g: ALFIE_10, pose=alfie_10),
                     "gaffer": dict(cast="gaffer", ppd=160, place=lambda g: BG_10["gaffer"], pose=bg_pose("gaffer")),
                     "miner2": dict(cast="miner2", ppd=160, place=lambda g: BG_10["miner2"], pose=bg_pose("miner2")),
                     "miner1": dict(cast="miner1", ppd=160, place=lambda g: BG_10["miner1"], pose=bg_pose("miner1"))},
             lamps=lamps_10c),
}

# key_lamps needs the shot id: wrap the lamp functions so they know it
for _sid, _s in SHOTS.items():
    if _s.get("lamps"):
        _f = _s["lamps"]
        def _w(T, g, f, _f=_f, _sid=_sid):
            T._sid = _sid
            return _f(T, g, f)
        _s["lamps"] = _w

if __name__ == "__main__":
    tk.main(SHOTS, "s09", sys.argv)
