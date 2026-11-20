#!/usr/bin/env python3
"""s10 shot 26 (g 1512..1578): bridge_deck. python3 shot26.py <draft|final> <g spec e.g. 1512:1578:6> [samples]"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21, crowd
from c21 import *

G0, G1 = 1519, 1578
S = cast21.STORY21
QUOTE = None                                   # nobody speaks in this shot
F_FLIP, F_POP, F_LAND = 1540, 1550, 1570       # A turns back (hop) / helmet pops off / helmet lands on the deck

def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
    return out

# --- camera: eased push of ~8 %/s on the jam, a lateral slide, plus a snap in on the turn (F_FLIP..)
FOC = np.array([0.0, 0.6, 3.1])
P0 = np.array([-5.6, -1.6, 3.5])
SLOTS = [(0.62, y) for y in (-4.2, -0.9, 2.4, 5.7, 9.0, 12.3, 15.6)] + [(-0.62, y) for y in (-4.4, 5.3, 8.6, 11.9, 15.2)]; RIGHT = None

def cam_at(g):
    t = (g - G0) / 30.0
    d = (FOC - P0); fwd = d.copy(); fwd[2] = 0; fwd /= np.linalg.norm(fwd); right = np.array([fwd[1], -fwd[0], 0.0])
    k = 0.92 ** t                                   # 8 %/s push
    snap = ez((g - F_FLIP) / 14.0) * 0.10            # extra snap push on the turn
    k *= (1.0 - snap)
    loc = FOC + (P0 - FOC) * k + right * (0.22 * t)   # slide ~0.22 m/s (about 50 px/s at 3.5 m)
    look = FOC + right * (0.22 * t) * 0.6 + np.array([0, 0, -0.15 * ez((g - F_FLIP) / 14.0)])
    return tuple(loc), tuple(look)

def blink(g, off=0, period=71):
    return 1.0 if (g + off) % period in (0, 1) else 0.0

def main(quality, gs, samples):
    register_bare_knights(); patch_air_helmet()
    T = Take("bridge_deck", quality, samples)
    A_h = T.actor("A_h", "knight_a_mtd")             # front rider, helmet on
    A_b = T.actor("A_b", "knight_a_bare_mtd")        # same, bare head (after the pop)
    B = T.actor("B", "knight_b_mtd")                 # behind him, pressed against the rail, sucking his belly in
    C = T.actor("C", "knight_a_open_mtd")            # third rider behind B, bumps and bobs
    H = T.actor("H", "helmet_float")
    flat = {}
    for g in gs:
        f = g + 1
        loc, look = cam_at(g); T.set_cam(loc, look)
        sc = T.scene; sc.frame_set(f)
        t = g / 30.0
        # horses: idle mode (head bob + tail swish), phase from g
        idle = (g / 70.0) % 1
        wob = math.sin(g * 0.45) * 0.5
        # A turns back at F_FLIP with a hop; before: faces north (mirror=True = screen-left), after: faces south (mirror=False)
        flipped = g >= F_FLIP
        hop = 0.0
        if F_FLIP - 2 <= g <= F_FLIP + 8:
            u = (g - (F_FLIP - 2)) / 10.0; hop = 0.5 * 4 * u * (1 - u)           # a 0.5 D hop
        axy = (-0.65, 1.5) if not flipped else (-0.65, 1.5 - 0.25 * ez((g - F_FLIP) / 8.0))
        bxy = (-0.65, -0.4 + 0.05 * math.sin(g * 0.5))
        cxy = (0.65, 0.3)
        popped = g >= F_POP
        for a in (A_h, A_b, B, C):
            pass
        base_a = dict(mode21="idle", t=idle, mirror=not flipped, horse21="red")
        if g < F_FLIP:
            pa = dict(S["knight_a_mounted_shocked"][1], **base_a); pa["expr"] = "worried"; pa["mouth"] = "wavy"; pa["fx"] = ["sweat"]
        else:
            pa = dict(S["knight_a_mounted_wobble"][1], **base_a)
            if g > F_POP: pa["expr"] = "shocked"; pa["head_roll"] = 12.0 * math.sin(g * 0.8); pa["lean"] = -10
            pa["fx"] = ["sweat"]
        pa["blink"] = blink(g, 5)
        pa["mode21"] = "idle"
        pb = dict(S["knight_b_mounted_suck_belly"][1], mode21="idle", t=(idle + 0.3) % 1, mirror=True, horse21="blue")
        pb["blink"] = blink(g, 31); pb["head_roll"] = 4 * math.sin(g * 0.5)
        pc = dict(S["knight_a_mounted_shocked"][1], mode21="idle", t=(idle + 0.6) % 1, mirror=True, horse21="gold")
        pc["head_roll"] = 6 * math.sin(g * 0.7 + 1); pc["blink"] = blink(g, 47)
        # place
        A_h.place(f, (axy[0], axy[1], K.DECK_Z + hop * M_PER_D), scale=M_PER_D)
        A_b.place(f, (axy[0], axy[1], K.DECK_Z + hop * M_PER_D), scale=M_PER_D)
        B.place(f, (bxy[0], bxy[1], K.DECK_Z), scale=M_PER_D)
        C.place(f, (cxy[0], cxy[1], K.DECK_Z), scale=M_PER_D)
        A_h.set_hidden(popped); A_b.set_hidden(not popped)
        (A_b if popped else A_h).pose(f, pa, camera=T.cam)
        B.pose(f, pb, camera=T.cam); C.pose(f, pc, camera=T.cam)
        # the helmet: leaves A's head at F_POP, flies up and over to the front, lands on the deck at F_LAND and rocks
        if g >= F_POP:
            u = (g - F_POP) / float(F_LAND - F_POP)
            if u <= 1.0:
                hx = lerp(axy[0], -1.35, u); hy = lerp(axy[1], 0.9, u)
                hz = K.DECK_Z + 2.55 * M_PER_D * 1.9 + 2.0 * 4 * u * (1 - u) * 1.0 - (2.55 * M_PER_D * 1.9 * 0) - 2.6 * u * u * 0.0
                hz = lerp(K.DECK_Z + 2.3, 2.98, u * u) + 1.5 * math.sin(math.pi * u) * (1 - 0.3 * u)
            else:
                hx, hy, hz = -1.35, 0.9, 2.98
            tilt = (g - F_POP) * 12.0 if u <= 1.0 else 16.0 * math.exp(-(g - F_LAND) * 0.25) * math.sin((g - F_LAND) * 1.1)
            H.place(f, (hx, hy, hz), scale=M_PER_D * 0.9)
            H.set_hidden(False)
            H.pose(f, dict(helm21="great", air21=1, tilt=tilt, t=0.0), camera=T.cam)
        else:
            H.place(f, (0, 1.9, K.DECK_Z), scale=M_PER_D); H.set_hidden(True)
            H.pose(f, dict(helm21="great", air21=1), camera=T.cam)
    # sprites + rendering
    T.sprites_for(256)
    out = os.path.join(HERE, "raw", "s26_" + quality); os.makedirs(out, exist_ok=True)
    for g in gs:
        f = g + 1
        loc, look = cam_at(g); T.set_cam(loc, look)
        K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        # the column ahead on the bridge: still marching, wobbling
        crowd.column(g, SLOTS, wob=1.0, jam=0.0 if g < F_FLIP else 0.5, seed=3)
        A_h.set_hidden(g >= F_POP); A_b.set_hidden(g < F_POP); H.set_hidden(g < F_POP)
        dt = T.render(f, os.path.join(out, "g_%04d.png" % g))
        print("g", g, "%.1fs" % dt, flush=True)

if __name__ == "__main__":
    q = sys.argv[1]; gs = parse(sys.argv[2]); sm = int(sys.argv[3]) if len(sys.argv) > 3 else None
    main(q, gs, sm)
